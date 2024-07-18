import pygame


# Headlines scroller class
class HeadlineScroller:
    def __init__(self, api, headlines, screen, subscreen_x_start, subscreen_y_start, sub_screen_width, sub_screen_height, scroll_speed=1, titlefont_size=26, body_font_size=19,subfont_size=17, title_color=(255, 255, 255), source_color=(0, 122, 204), date_color=(99,176,227)):
        self.api = api
        self.headlines = headlines
        self.num_headlines = len(headlines)

        self.subsurface_rect = pygame.Rect(subscreen_x_start, subscreen_y_start, sub_screen_width, sub_screen_height)
        self.subsurface = screen.subsurface(self.subsurface_rect)

        self.max_left = 0  # The length of the longest headline
        self.scroll_speed = scroll_speed

        self.x = self.subsurface_rect.width
        self.sub_screen_height = sub_screen_height 

        self.headline_font = pygame.font.Font(pygame.font.match_font('ubuntusansmono'), titlefont_size)
        self.sub_font = pygame.font.Font(pygame.font.match_font('ubuntusansmono'), subfont_size)
        self.body_font = pygame.font.Font(pygame.font.match_font('ubuntusansmono'), body_font_size)
        self.y_padding = sub_screen_height // len(headlines)
        self.headline_col = title_color
        self.date_col = date_color
        self.source_col = source_color

    def update(self):
        self.x -= self.scroll_speed
        if self.x <= -self.max_left:  # Reset position when pad screen
            self.headlines = self.api.get_stories()
            self.x = self.subsurface_rect.width

    def draw(self):
        #self.subsurface.fill((0, 0, 255))  # Clear subsurface each frame
        x = self.x
        for i, headline in enumerate(self.headlines):
            headline_text = self.headline_font.render(headline["headline"], True, self.headline_col)
            source_text = self.sub_font.render(headline["source"], True, self.source_col)
            time_text = self.sub_font.render(headline["time"], True, self.date_col)
            body_text = self.body_font.render(headline["body"], True, self.headline_col)

            self.max_left = max(body_text.get_width(), headline_text.get_width(), self.max_left)

            self.subsurface.blit(headline_text, (x, i * self.y_padding + 15))
            self.subsurface.blit(body_text, (x, i * self.y_padding + 5*(headline_text.get_height() // 4) + 15))
            self.subsurface.blit(source_text, (x, i * self.y_padding + 8*(headline_text.get_height() // 4) + 15))
            self.subsurface.blit(time_text, (x + 250, i * self.y_padding + 8*(headline_text.get_height() // 4) + 15))

