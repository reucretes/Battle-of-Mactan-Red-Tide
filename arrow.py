import pygame

class Arrow:

    def __init__(self, x, y, facing_right, image):

        self.x = x
        self.y = y

        self.speed = 15

        self.image = image
        self.facing_right = facing_right

        if not facing_right:
            self.image = pygame.transform.flip(
                self.image,
                True,
                False
            )

    def update(self):

        if self.facing_right:
            self.x += self.speed
        else:
            self.x -= self.speed

    def draw(self, screen, camera_x):

        screen.blit(
            self.image,
            (
                self.x - camera_x,
                self.y
            )
        )

    def get_rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height()
        )