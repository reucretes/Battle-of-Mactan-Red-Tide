import pygame


class CharacterSelect:

    def __init__(self, screen, click_sound):

        self.screen = screen
        self.click_sound = click_sound
        self.width, self.height = screen.get_size()

        # BACKGROUND
        self.bg = pygame.image.load("images/ui/character_bg.png").convert()
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

        # Optional dark overlay
        self.overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 0))

        # LOAD CHARACTER IMAGES
        self.lapu_img = pygame.image.load("images/ui/lapu.png").convert_alpha()
        self.hiraya_img = pygame.image.load("images/ui/hiraya.png").convert_alpha()

        # Resize for UI
        self.lapu_img = pygame.transform.scale(self.lapu_img, (500, 700))
        self.hiraya_img = pygame.transform.scale(self.hiraya_img, (500, 700))

        # CLICK AREAS
        self.lapu_rect = self.lapu_img.get_rect(
            center=(self.width * 0.3, self.height // 2 + 60)
        )

        self.hiraya_rect = self.hiraya_img.get_rect(
            center=(self.width * 0.7, self.height // 2 + 60)
        )

        # FONTS
        self.font = pygame.font.SysFont(None, 50)
        self.title_font = pygame.font.SysFont(None, 90)

        self.selected_character = None

    def run(self):

        while self.selected_character is None:

            # DRAW BACKGROUND
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.overlay, (0, 0))

            # TITLE

            title = self.title_font.render(
                "  ",
                True,
                (255, 255, 255)
            )

            title_rect = title.get_rect(center=(self.width // 2, 80))
            self.screen.blit(title, title_rect)

            # MOUSE POSITION
            mouse = pygame.mouse.get_pos()

            # DRAW CHARACTERS

            self.draw_character(
                self.lapu_img,
                self.lapu_rect,
                "  ",
                mouse
            )

            self.draw_character(
                self.hiraya_img,
                self.hiraya_rect,
                " ",
                mouse
            )

            pygame.display.flip()

            # EVENTS
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.lapu_rect.collidepoint(mouse):
                        self.click_sound.play()
                        self.selected_character = "lapulapu"

                    if self.hiraya_rect.collidepoint(mouse):
                        self.click_sound.play()
                        self.selected_character = "hiraya"

        return self.selected_character

    def draw_character(self, image, rect, name, mouse):

        hovered = rect.collidepoint(mouse)

    # HOVER ANIMATION
        if hovered:

            scale = 1.08  # bigger when hovered

            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)

            animated_img = pygame.transform.smoothscale(
                image,
                (new_width, new_height)
            )

            animated_rect = animated_img.get_rect(center=rect.center)

            self.screen.blit(animated_img, animated_rect)

        else:
            self.screen.blit(image, rect)

    # NAME TEXT
        text = self.font.render(name, True, (255, 255, 255))

        text_rect = text.get_rect(
            center=(rect.centerx, rect.bottom + 30)
        )

        self.screen.blit(text, text_rect)