import pygame
import os

class BloodEffect:

    _cached_frames = {}

    def __init__(self, x, y, settings):

        self.x = x
        self.y = y
        self.settings = settings

        self.frame_index = 0
        self.finished = False

        if not BloodEffect._cached_frames:
            BloodEffect._cached_frames = self.load_frames("images/blood")

        # LOAD ANIMATION FRAMES
        self.frames = BloodEffect._cached_frames

    def load_frames(self, folder):

        frames = []
        if not os.path.exists(folder):
            return frames

        for file in sorted(os.listdir(folder)):
            if file.endswith(".png"):

                img = pygame.image.load(
                    os.path.join(folder, file)
                ).convert_alpha()

                # INCREASE THE SIZE HERE
                img = pygame.transform.scale(img, (150, 150)) 
                frames.append(img)

        return frames

    def update(self):

        self.frame_index += 0.3

        if self.frame_index >= len(self.frames):
            self.finished = True

    def draw(self, screen, camera_x):

        if self.finished or not self.frames:
            return

        frame = self.frames[int(self.frame_index)]

        rect = frame.get_rect(
            center=(self.x - camera_x, self.y)
        )

        screen.blit(frame, rect)