import pygame
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import threading

from gpumonitor import GPUMonitor
from gpuploter import GPUPlot, gpu_monitoring_thread
from welcome_scroller import WelcomeScroller
from headline_scroller import HeadlineScroller

pygame.init()

# Get dims
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Welcome to Valfar Lab - {Esc} to exit')
pygame.mouse.set_visible(False)

background_color = (0, 0, 0)

#will use api later this is for testing
headlines = [{'source': 'Associated Press',
  'headline': 'The son of Asia’s richest man gets married in the year’s most extravagant wedding; - T',
  'time': '2024-13-07 11:25',
  'body': "The youngest son of Mukesh Ambani, Asia’s richest man, has married his longtime girlfriend in what many have dubbed the wedding of the year. It's being attended by global celebrities, business tycoons and politicians, highlighting the billionaire’s staggering…"},
 {'source': 'Politico',
  'headline': 'Actor Matthew McConaughey tells governors he is still mulling future run for political office',
  'time': '2024-13-07 10:56',
  'body': None},
 {'source': 'CBS Sports',
  'headline': 'Jalen Brunson contract extension FAQ: How much did Knicks star really leave on table, what move means for NY',
  'time': '2024-13-07 10:51',
  'body': 'Brunson re-signed with the Knicks for $156.5 million over four years'},
 {'source': 'Deadline',
  'headline': 'Harrison Butker Responds To ESPYs Diss By Serena Williams And Quinta Brunson',
  'time': '2024-13-07 10:15',
  'body': 'The Kansas City Chiefs kicker spoke to NBC News for his rebuttal.'},
 {'source': 'New York Post',
  'headline': 'Smiling Alec Baldwin heads to celebratory dinner after ‘Rust’ involuntary manslaughter charges shockingly tossed ',
  'time': '2024-13-07 09:27',
  'body': 'The “30 Rock” star, 66, smiled with his entourage outside Casa Chimayo restaurant in Santa Fe.'}]



#scroller code
welcome_scroller = WelcomeScroller('Welcome to Valafar Lab', screen_info, screen_width, scrollspeed=2)
headlines_scroller = HeadlineScroller(headlines, screen, 0, screen_height - screen_height // 2, screen_width // 2, screen_height // 2)

#gpu graph code
plt.style.use('dark_background')

gpu_plot00 = GPUPlot()
gpu_plot01 = GPUPlot()

gpu_monitor00 = GPUMonitor()
gpu_monitor00.start_monitoring()
gpu_monitor01 = GPUMonitor()
gpu_monitor01.start_monitoring()

# main  loop
clock = pygame.time.Clock()
update_interval = 5000 #5 sec
running = True

gpu_thread00 = threading.Thread(target=gpu_monitoring_thread, args=(gpu_monitor00, gpu_plot00, update_interval, running))
gpu_thread00.start()

gpu_thread01 = threading.Thread(target=gpu_monitoring_thread, args=(gpu_monitor01, gpu_plot01, update_interval, running))
gpu_thread01.start()



#main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

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
