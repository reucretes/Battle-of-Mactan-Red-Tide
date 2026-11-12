import pygame
import sys
import settings as st

class PauseMenu:

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.bg = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.bg.fill((0, 0, 0, 180))

        self.continue_img = pygame.image.load("images/ui/continue.png").convert_alpha()
        self.home_img = pygame.image.load("images/ui/home.png").convert_alpha()
        self.music_on_img = pygame.image.load("images/ui/music_on.png").convert_alpha()
        self.music_off_img = pygame.image.load("images/ui/music_off.png").convert_alpha()
        self.bg_image = pygame.image.load("images/ui/pause_bg.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))

        self.continue_img = pygame.transform.scale(self.continue_img, (260, 120))
        self.home_img = pygame.transform.scale(self.home_img, (260, 120))
        self.music_on_img = pygame.transform.scale(self.music_on_img, (200, 120))
        self.music_off_img = pygame.transform.scale(self.music_off_img, (200, 120))

        left_x = 490

        self.continue_rect = self.continue_img.get_rect(center=(left_x, self.height//2 - 60))
        self.home_rect = self.home_img.get_rect(center=(left_x, self.height//2 + 60))
        self.music_rect = self.music_on_img.get_rect(center=(left_x, self.height//2 + 190))

        self.choice = None
        self.music_on = True

    def run(self, music_on):

        self.music_on = music_on
        self.choice = None

        while self.choice is None:

            self.draw()

            pygame.display.flip()

            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.continue_rect.collidepoint(mouse):
                        self.choice = "continue"

                    elif self.home_rect.collidepoint(mouse):
                        self.choice = "home"

                    elif self.music_rect.collidepoint(mouse):
                        self.music_on = not self.music_on
                        if self.music_on:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()

        return self.choice, self.music_on

    def draw(self):

        # BACKGROUND IMAGE FIRST
        self.screen.blit(self.bg_image, (0, 0))

        mouse = pygame.mouse.get_pos()

        # BUTTONS
        self.draw_button(self.continue_img, self.continue_rect, mouse)
        self.draw_button(self.home_img, self.home_rect, mouse)

        if self.music_on:
            img = self.music_on_img
        else:
            img = self.music_off_img

        self.draw_button(img, self.music_rect, mouse)

    def draw_button(self, image, rect, mouse):

        hovered = rect.collidepoint(mouse)

        if hovered:

            scale = 1.08

            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)

            hover_img = pygame.transform.smoothscale(
                image,
                (new_width, new_height)
            )

            hover_rect = hover_img.get_rect(
                center=rect.center
            )

            self.screen.blit(hover_img, hover_rect)

        else:
            self.screen.blit(image, rect)