import pygame
import sys


class WinScreen:

    def __init__(self, screen):

        self.screen = screen
        self.width, self.height = screen.get_size()

        # BACKGROUND
        self.bg = pygame.image.load(
            "images/ui/win_screen.png"
        ).convert()

        self.bg = pygame.transform.scale(
            self.bg,
            (self.width, self.height)
        )

        #BUTTON IMAGES
        self.restart_img = pygame.image.load(
            "images/ui/restart.png"
        ).convert_alpha()

        self.quit_img = pygame.image.load(
            "images/ui/quit.png"
        ).convert_alpha()

        # Resize
        self.restart_img = pygame.transform.scale(
            self.restart_img,
            (260, 150)
        )

        self.quit_img = pygame.transform.scale(
            self.quit_img,
            (260, 150)
        )

        # BUTTON POSITIONS
        self.restart_rect = self.restart_img.get_rect(
            center=(self.width // 2, self.height * 0.64)
        )

        self.quit_rect = self.quit_img.get_rect(
            center=(self.width // 2, self.height * 0.78)
        )

        self.choice = None

    # MAIN LOOP
    def run(self):

        while self.choice is None:

            self.draw()

            pygame.display.flip()

            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        if self.restart_rect.collidepoint(mouse):
                            self.choice = "restart"

                        if self.quit_rect.collidepoint(mouse):
                            self.choice = "quit"

        return self.choice

    # DRAW
    def draw(self):

        self.screen.blit(self.bg, (0, 0))

        mouse = pygame.mouse.get_pos()

        self.draw_button(
            self.restart_img,
            self.restart_rect,
            mouse
        )

        self.draw_button(
            self.quit_img,
            self.quit_rect,
            mouse
        )

    # BUTTON HOVER EFFECT
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