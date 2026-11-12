import pygame
import os

class Character:

    def __init__(self, x, y, settings, character_type="lapulapu"):

        self.x = float(x)
        self.y = float(y)

        self.settings = settings

        # CHARACTER TYPE
        self.character_type = character_type

        if self.character_type == "lapulapu":
            self.weapon_type = "sword"
            self.attack_damage = 250
            self.attack_range = 200
            
            # --- LAPU-LAPU'S UNIQUE HEALTH ---
            self.max_health = 1500  
            self.health = 1500

        else:
            self.weapon_type = "spear"
            self.attack_damage = 250
            self.attack_range = 800
            
            # --- HIRAYA'S UNIQUE HEALTH ---
            self.max_health = 1000 
            self.health = 1000

        # PLAYER SETTINGS
        self.base_width = 170
        self.base_height = 200
        self.velocity_y = 0

        self.is_jumping = False
        self.facing_right = True

        self.frame_index = 0
        self.current_action = "idle"

        # ATTACK
        self.is_attacking = False
        self.attack_timer = 0
        self.arrow_spawned = False
        self.has_hit = False
        self.has_jump_hit = False
        
# SOUND EFFECTS

        if self.character_type == "lapulapu":
            self.sfx_run = pygame.mixer.Sound("soundfile/lapu_run.MP3")
            self.sfx_jump = pygame.mixer.Sound("soundfile/lapu_jump.MP3")
            self.sfx_attack = pygame.mixer.Sound("soundfile/lapu_attack.MP3")
            self.sfx_hit = pygame.mixer.Sound("soundfile/lapu_attack_zombie.MP3")

        else:
            self.sfx_run = pygame.mixer.Sound("soundfile/hiraya_run.MP3")
            self.sfx_jump = pygame.mixer.Sound("soundfile/hiraya_jump.MP3")
            self.sfx_attack = pygame.mixer.Sound("soundfile/hiraya_attack.MP3")
            self.sfx_hit = pygame.mixer.Sound("soundfile/hiraya_attack_zombie.MP3")

        self.sfx_run.set_volume(0.6)
        self.sfx_jump.set_volume(0.6)
        self.sfx_attack.set_volume(0.6)
        self.sfx_hit.set_volume(0.7)

        self.run_sound_playing = False

        # HIRAYA ARROW IMAGE
        if self.character_type == "hiraya":

            self.arrow_image = pygame.image.load(
                "images/arrow.png"
            ).convert_alpha()

            self.arrow_image = pygame.transform.scale(
                self.arrow_image,
                (150, 70)
            )
        
        self.BAR_WIDTH = 400
        self.BAR_HEIGHT = 80
        self.FILL_HEIGHT = 50

        # Load and scale ONCE sa __init__
        self.health_ui_bg = pygame.image.load("images/ui/health_bg.png").convert_alpha()
        self.health_ui_bg = pygame.transform.scale(self.health_ui_bg, (self.BAR_WIDTH, self.BAR_HEIGHT))

        self.health_ui_frame = pygame.image.load("images/ui/health_frame.png").convert_alpha()
        self.health_ui_frame = pygame.transform.scale(self.health_ui_frame, (self.BAR_WIDTH, self.BAR_HEIGHT))
        
        self.health_ui_fill = pygame.image.load("images/ui/health_fill.png").convert_alpha()

        self.health_font = pygame.font.SysFont(None, 40)
        # LOAD ANIMATIONS
        self.animations = self.load_animations()

    # LOAD FRAMES

    def load_frames(self, folder):

        frames = []

        if not os.path.exists(folder):
            return frames

        for file in sorted(os.listdir(folder)):

            if file.endswith(".png"):

                img = pygame.image.load(
                    os.path.join(folder, file)
                ).convert_alpha()

                img = pygame.transform.scale(
                    img,
                    (self.base_width, self.base_height)
                )

                frames.append(img)

        return frames

    # LOAD ANIMATIONS

    def load_animations(self):

        base = f"images/{self.character_type}"

        return {

            "idle":
                self.load_frames(f"{base}/idle"),

            "run":
                self.load_frames(f"{base}/run"),

            "jump":
                self.load_frames(f"{base}/jump"),

            "attack":
                self.load_frames(f"{base}/attack"),

            "celebrate": self.load_frames(f"{base}/celebrate")
        }

    # UPDATE
    def update(self, keys):

        speed = (
            self.settings.PLAYER_RUN_SPEED
            if keys[pygame.K_LSHIFT]
            else self.settings.PLAYER_SPEED
        )

        moving = False   # MUST BE HERE

        # MOVE RIGHT
        if keys[pygame.K_RIGHT]:
            self.x += speed
            self.facing_right = True
            moving = True

        # MOVE LEFT
        if keys[pygame.K_LEFT]:
            self.x -= speed
            self.facing_right = False
            moving = True

        # RUN SOUND CONTROL
        grounded = self.y >= (
            self.settings.START_Y_OFFSET + self.settings.SCREEN_CENTER_Y
        )

        if moving and grounded:
            if not self.run_sound_playing:
                self.sfx_run.play(-1)
                self.run_sound_playing = True
        elif self.run_sound_playing:
            self.sfx_run.stop()
            self.run_sound_playing = False

        # GRAVITY
        self.velocity_y += self.settings.GRAVITY

        self.y += self.velocity_y

        ground_y = (
            self.settings.START_Y_OFFSET
            + self.settings.SCREEN_CENTER_Y
        )

        if self.y >= ground_y:

            self.y = ground_y
            self.velocity_y = 0
            self.is_jumping = False

        # ATTACK ANIMATION

        if self.is_attacking:

            self.current_action = "attack"

            # --- MOVE THE ARROW DELAY LOGIC HERE ---
            if self.character_type == "hiraya":
                self.attack_timer += 1
                
                # adjust timing here (e.g., 8 to 15 based on animation speed)
                if self.attack_timer == 8:
                    self.arrow_spawned = True

            if self.frame_index >= len(self.animations["attack"]) - 1:

                self.is_attacking = False
                self.frame_index = 0

            return

        # NORMAL ANIMATIONS

        if self.is_jumping:

            self.current_action = "jump"

        elif moving:

            self.current_action = "run"

        else:

            self.current_action = "idle"

    # JUMP
    def jump(self):

        if not self.is_jumping:

            self.velocity_y = self.settings.JUMP_POWER
            self.is_jumping = True
            self.frame_index = 0
            self.has_jump_hit = False 

            self.sfx_jump.play()

    # ATTACK
    def attack(self):

        if self.is_attacking:
            return

        self.is_attacking = True
        self.frame_index = 0

        self.attack_timer = 0
        self.arrow_spawned = False
        self.has_hit = False  # <--- ADD THIS HERE

        self.sfx_attack.play()

    # DAMAGE
    def take_damage(self, amount, player=None):

        self.health -= amount

        if self.health < 0:
            self.health = 0

        if player:
            player.sfx_hit.play()

    # HEAL
    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    # DRAW PLAYER
    def draw(self, screen, camera_x):

        frames = self.animations.get(self.current_action, [])

        if not frames:
            return

        self.frame_index += self.settings.ANIMATION_SPEED

        if self.frame_index >= len(frames):

            if self.current_action == "attack":

                self.frame_index = len(frames) - 1

            else:

                self.frame_index = 0

        frame = frames[int(self.frame_index)]

        # FLIP
        if not self.facing_right:

            frame = pygame.transform.flip(
                frame,
                True,
                False
            )
        #character position relative to camera
        rect = frame.get_rect(
            center=(int(self.x - camera_x), int(self.y))
        )

        screen.blit(frame, rect)

    # HEALTH BAR
    def draw_health_bar(self, screen):

        x = 20
        y = 20

        # health ratio (0 to 1)
        ratio = self.health / self.max_health
        ratio = max(0, min(1, ratio))

        # fill width (inside frame padding)
        fill_width = int((self.BAR_WIDTH - 40) * ratio)

        # draw order (IMPORTANT) - Hindi na kailangan i-scale yung bg at frame!
        screen.blit(self.health_ui_bg, (x, y))

        if fill_width > 0:
            fill = pygame.transform.scale(self.health_ui_fill, (fill_width, self.FILL_HEIGHT))
            screen.blit(fill, (x + 20, y + 15))

        screen.blit(self.health_ui_frame, (x, y))