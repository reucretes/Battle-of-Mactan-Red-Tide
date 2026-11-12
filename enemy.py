import pygame
import os

import pygame
import os

class Enemy:
    
    _cached_animations = {}

    def __init__(self, x, y, settings, zombie_type="normal"):
        self.x = float(x)
        self.y = float(y)
        self.settings = settings

        self.zombie_type = zombie_type
        if zombie_type == "normal":
            self.anim_folder = "images/enemy_normal/normal"

        elif zombie_type == "runner":
            self.anim_folder = "images/enemy_runner/runner"

        elif zombie_type == "armored":
            self.anim_folder = "images/enemy_armored/armored"

        elif zombie_type == "boss":
            self.anim_folder = "images/enemy_boss/boss"

        # NORMAL
        if zombie_type == "normal":
            self.base_width = 180
            self.base_height = 200

        # RUNNER
        elif zombie_type == "runner":
            self.base_width = 190
            self.base_height = 210

        # ARMORED
        elif zombie_type == "armored":
            self.base_width = 200
            self.base_height = 220

        # BOSS
        elif zombie_type == "boss":
            self.base_width = 350
            self.base_height = 380
        
        # Adjust Y center so feet align perfectly with a 200px tall player
        height_diff = self.base_height - 200
        self.y -= height_diff / 2

        # SET HEALTH BASED ON ZOMBIE TYPE
        if zombie_type == "normal":
            self.max_health = 500
            self.damage = 5     
        elif zombie_type == "runner":
            self.max_health = 500
            self.damage = 10     
        elif zombie_type == "armored":
            self.max_health = 750
            self.damage = 10    
        elif zombie_type == "boss":
            self.max_health = 5000
            self.damage = 30      
            
        self.health = self.max_health

        self.speed = getattr(settings, "ZOMBIE_SPEED", 2)

        self.damage = getattr(settings, "ZOMBIE_DAMAGE", 5)
        self.is_dead = False
        self.death_timer = 0

        self.facing_right = True

        # STATES
        self.state = "walk"
        self.frame_index = 0

        # COMBAT
        self.attack_range = 80

        self.is_attacking = False
        self.attack_cooldown = 0
        self.has_transformed = False

        if zombie_type not in Enemy._cached_animations:
            Enemy._cached_animations[zombie_type] = self.load_animations()
        
        # get the cached animations for this zombie type
        self.animations = Enemy._cached_animations[zombie_type]

    #LOAD 
    def load_frames(self, folder):
        frames = []
        if not os.path.exists(folder):
            return frames

        for file in sorted(os.listdir(folder)):
            if file.endswith(".png"):
                img = pygame.image.load(os.path.join(folder, file)).convert_alpha()
                img = pygame.transform.scale(img, (self.base_width, self.base_height))
                frames.append(img)
        return frames

    def load_animations(self):
        return {
            "walk": self.load_frames(f"{self.anim_folder}_walk"),
            "attack": self.load_frames(f"{self.anim_folder}_attack"),
            "die": self.load_frames(f"{self.anim_folder}_dying"),
            "transform": self.load_frames(f"{self.anim_folder}_transform"),
        }

    #UPDATE 
    def update(self, player):

        distance = abs(player.x - self.x)

        self.facing_right = player.x > self.x

    # cooldown timer
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.is_dead:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

    # ATTACK START
        if (
            distance < self.attack_range + 20
            and self.attack_cooldown == 0
            and not self.is_attacking
        ):

            self.is_attacking = True
            self.state = "attack"
            self.frame_index = 0
            self.has_hit = False
            self.attack_cooldown = 60

    # ATTACK LOGIC
        if self.is_attacking:

    # DEAL DAMAGE ONCE PER ATTACK
            if not hasattr(self, "has_hit"):
                self.has_hit = False
            distance = abs(player.x - self.x)
            vertical = abs(player.y - self.y)

    # GUARANTEED HIT CHECK
            if distance < self.attack_range and vertical < 80 and not self.has_hit:
                
                # CHANGE '5' TO 'self.damage'
                player.take_damage(self.damage) 
                
                self.has_hit = True

    # END ATTACK ANIMATION
            if self.frame_index >= len(self.animations["attack"]) - 1:
                self.is_attacking = False
                self.state = "walk"
                self.frame_index = 0
                self.has_hit = False
            return

    # WALKING
        if distance > self.attack_range:

            direction = 1 if player.x > self.x else -1
            self.x += direction * self.speed
            self.state = "walk"

    def take_damage(self, amount):

        if self.is_dead:
            return

        self.health -= amount

        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.state = "die"
            self.frame_index = 0
            self.death_timer = 20

    #DRAW 
    def draw(self, screen, camera_x):

        # GET FRAMES SAFELY
        frames = self.animations.get(self.state, [])

        if len(frames) == 0:
            return

        # UPDATE ANIMATION
        self.frame_index += self.settings.ANIMATION_SPEED

        # LIMIT FRAME INDEX
        if self.frame_index >= len(frames):
            if self.state == "die":
                self.frame_index = len(frames) - 1  # stop at last frame
            else:
                self.frame_index = 0

        frame = frames[int(self.frame_index)]

        # FLIP DIRECTION
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        rect = frame.get_rect(
            center=(int(self.x - camera_x  + 23), int(self.y))
        )

        screen.blit(frame, rect)