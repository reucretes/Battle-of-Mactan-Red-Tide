import pygame
import settings as st


class Menu:

    def __init__(self, screen):

        self.screen = screen
        self.width, self.height = screen.get_size()

        # BACKGROUND
        self.bg = pygame.image.load(st.MENU_BG).convert()
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

        # START BUTTON IMAGE
        self.start_img = pygame.image.load(
            "images/ui/start_button.png"
        ).convert_alpha()

        # Resize button
        self.start_img = pygame.transform.scale(
            self.start_img,
            (260, 180)
        )

        # Hover version
        self.start_hover = pygame.transform.scale(
            self.start_img,
            (240, 160)
        )

        # Button position
        self.start_rect = self.start_img.get_rect(
            center=(self.width // 2, self.height * 0.63)
        )

        self.choice = None

    # MAIN LOOP
    def run(self):

        while self.choice is None:

            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    mouse = pygame.mouse.get_pos()

                    if self.start_rect.collidepoint(mouse):
                        self.choice = "start"

        return self.choice

    # DRAW MENU
    def draw(self):

        # Background
        self.screen.blit(self.bg, (0, 0))

        mouse = pygame.mouse.get_pos()

        # HOVER EFFECT
        if self.start_rect.collidepoint(mouse):

            hover_rect = self.start_hover.get_rect(
                center=self.start_rect.center
            )

            self.screen.blit(self.start_hover, hover_rect)

        else:
            self.screen.blit(self.start_img, self.start_rect)

        