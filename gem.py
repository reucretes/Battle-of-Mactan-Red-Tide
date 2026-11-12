import pygame

class Gem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60  # Adjust this to make the gem bigger or smaller
        self.height = 55
        
        # Load your custom gem image here
        # Make sure you place your image in the images/ui/ folder!
        self.image = pygame.image.load("images/ui/gem.png").convert_alpha()
        
        # Scale the image to fit the width and height
        # We keep this as our "master" image to rotate from
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # --- NEW ROTATION VARIABLES ---
        self.angle = 0
        self.rotation_speed = 3  # Increase for a faster spin, decrease for slower

    def draw(self, screen, camera_x):
        # 1. Update the angle continuously
        self.angle = (self.angle + self.rotation_speed) % 360
        
        # 2. Rotate the original image
        # NOTE: Always rotate the ORIGINAL image, never an already-rotated one. 
        # Rotating an already rotated image repeatedly will distort and destroy it.
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        
        # 3. Get the base bounding box and adjust for the camera
        base_rect = self.get_rect()
        base_rect.x -= camera_x
        
        # 4. Get the new bounding box of the rotated image
        # CRITICAL: Set the center of the new rect to the center of the base rect 
        # to prevent the gem from wobbling as it spins!
        rotated_rect = rotated_image.get_rect(center=base_rect.center)
        
        # 5. Draw the rotated image using its new centered rect
        screen.blit(rotated_image, rotated_rect.topleft)

    def get_rect(self):
        # The -30 lifts the gem slightly off the ground
        return pygame.Rect(self.x, self.y - 30, self.width, self.height)