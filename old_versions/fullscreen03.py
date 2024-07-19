import pygame
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import threading
import time

from gpumonitor import GPUMonitor
from gpuploter import GPUPlot, gpu_monitoring_thread
from welcome_scroller import WelcomeScroller
from headline_scroller import HeadlineScroller
from newsapi import NEWSAPI

pygame.init()

# Get dims
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Welcome to Valfar Lab - {Esc} to exit')
pygame.mouse.set_visible(False)

background_color = (0, 0, 0)

newsapi = NEWSAPI()  
headlines = newsapi.get_stories()

#scroller code
welcome_scroller = WelcomeScroller('Welcome to Valafar Lab', screen_info, screen_width, scrollspeed=2)
headlines_scroller = HeadlineScroller(headlines, screen, 0, screen_height - screen_height // 2, screen_width // 2, screen_height // 2)

#gpu graph code
plt.style.use('dark_background')

gpu_plot00 = GPUPlot()
gpu_plot01 = GPUPlot()

gpu_monitor00 = GPUMonitor(http_listen=True, port=12345)
gpu_monitor00.start_monitoring()
gpu_monitor01 = GPUMonitor(http_listen=True, port=12346)
gpu_monitor01.start_monitoring()

# main  loop

clock = pygame.time.Clock()
update_interval = 5000  # 5 sec
news_update_interval = 900000  # 900 sec (15 minutes)
running = True

last_news_update = time.time() * 1000 

gpu_thread00 = threading.Thread(target=gpu_monitoring_thread, args=(gpu_monitor00, gpu_plot00, update_interval, running))
gpu_thread00.start()

gpu_thread01 = threading.Thread(target=gpu_monitoring_thread, args=(gpu_monitor01, gpu_plot01, update_interval, running))
gpu_thread01.start()

while running:
    current_time = time.time() * 1000  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # check if time to update news
    if current_time - last_news_update >= news_update_interval:
        new_headlines = newsapi.get_stories()
        headlines_scroller.update_headlines(new_headlines)
        last_news_update = current_time

    screen.fill(background_color)

    #welcome scroller
    welcome_scroller.update()
    welcome_scroller.draw(screen)

    # headlines scroller
    headlines_scroller.update()
    headlines_scroller.draw()

    #create outline of the 4 quadrents
    height_of_welcome_text = welcome_scroller.text_rect.height
    pygame.draw.rect(screen, (255,255,255), (0, height_of_welcome_text, screen_width//2, screen_height//2 - height_of_welcome_text), 1)
    pygame.draw.rect(screen, (255,255,255), (0, screen_height//2, screen_width//2, screen_height//2), 1)
    pygame.draw.rect(screen, (255,255,255), (screen_width//2, screen_height//2, screen_width//2, screen_height//2), 1)
    pygame.draw.rect(screen, (255,255,255), (screen_width//2, height_of_welcome_text, screen_width//2, screen_height//2 - height_of_welcome_text), 1)

    with gpu_plot00.lock:
        if gpu_plot00.surface:
            screen.blit(gpu_plot00.surface, (screen_width // 2 + 10, height_of_welcome_text + 10))

    with gpu_plot01.lock:
        if gpu_plot01.surface:
            screen.blit(gpu_plot01.surface, (screen_width // 2 + 10, screen_height//2 + 10))

    pygame.display.flip()
    clock.tick(60)  # frame rate = 60

running = False
gpu_thread00.join()
gpu_thread01.join()
pygame.quit()
sys.exit()