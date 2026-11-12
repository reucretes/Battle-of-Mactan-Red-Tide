import pygame
import sys
import settings as st

from ast import main
from character_select import CharacterSelect
from character import Character
from menu import Menu
from enemy import Enemy
from zombie_manager import ZombieManager
from win_screen import WinScreen
from defeat_screen import DefeatScreen
from arrow import Arrow
from blood_effect import BloodEffect
from story_intro import StoryIntro
from pause_menu import PauseMenu
from gem import Gem

pygame.init()
pygame.mixer.init()

# WAVE TEXT
font = pygame.font.SysFont(None, 50)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

w, h = screen.get_size()
clock = pygame.time.Clock()

st.SCREEN_CENTER_Y = h // 2

black_overlay = pygame.Surface((w, h))
black_overlay.set_alpha(180)
black_overlay.fill((0, 0, 0))

# BACKGROUND MUSIC
main_sound = pygame.mixer.music.load("soundfile/main_sound.MP3")
pygame.mixer.music.set_volume(0.4)  
pygame.mixer.music.play(-1)

# SOUND EFFECTS
click_sound = pygame.mixer.Sound("soundfile/click.MP3")
wave_sound = pygame.mixer.Sound("soundfile/wave.MP3")
victory_sound = pygame.mixer.Sound("soundfile/victory.MP3")
defeat_sound = pygame.mixer.Sound("soundfile/defeat.MP3")
arrow_hit_sound = pygame.mixer.Sound("soundfile/arrow_hit.MP3") 
sword_hit_sound = pygame.mixer.Sound("soundfile/sword_hit.MP3")
normal_zombie_spawn_sound = pygame.mixer.Sound("soundfile/normal_spawn.WAV")
runner_zombie_spawn_sound = pygame.mixer.Sound("soundfile/runner_spawn.MP3")
armored_zombie_spawn_sound = pygame.mixer.Sound("soundfile/armored_spawn.MP3")
boss_zombie_spawn_sound = pygame.mixer.Sound("soundfile/boss_spawn.MP3")

gem_spawn_sound = pygame.mixer.Sound("soundfile/gem_spawn.WAV")
gem_pickup_sound = pygame.mixer.Sound("soundfile/gem_pickup.MP3")
normal_zombie_spawn_sound.set_volume(0.6)
runner_zombie_spawn_sound.set_volume(0.6)
armored_zombie_spawn_sound.set_volume(0.6) 
boss_zombie_spawn_sound.set_volume(0.6)

# IPAPASA NATIN ITO SA ZOMBIE MANAGER
zombie_spawn_sounds = {
    "normal": normal_zombie_spawn_sound,
    "runner": runner_zombie_spawn_sound,
    "armored": armored_zombie_spawn_sound,
    "boss": boss_zombie_spawn_sound
}

# adjust volume levels for each sound effect:
arrow_hit_sound.set_volume(0.6)
sword_hit_sound.set_volume(0.6)
gem_spawn_sound.set_volume(0.9)
gem_pickup_sound.set_volume(0.9)

menu = Menu(screen)
result = menu.run()
if result == "start":
    click_sound.play()

selector = CharacterSelect(screen, click_sound)

pause_menu = PauseMenu(screen)

ground_y = h // 2 + st.START_Y_OFFSET

player = Character(st.START_X, ground_y, st)
zombies = ZombieManager(st, zombie_spawn_sounds)

state = st.MENU
music_on = True

paused = False
music_on = True

# WORLD SETTINGS
WORLD_WIDTH = 3000
camera_x = 0

# MAP SYSTEM
selected_map = None
game_bg = None

# WAVE SYSTEM
current_wave = 1

wave_transition = False    

wave_anim_timer = 0
wave_alpha = 0
wave_scale = 0.5
wave_intro_active = True
wave_intro_finished = False

game_won = False

pygame.mixer.music.fadeout(500)

print("Loading animations... Please wait.")
for zombie_type in ["normal", "runner", "armored", "boss"]:
    Enemy(-9999, -9999, st, zombie_type)
print("All animations loaded successfully!")

try:
    StoryIntro(screen).run()
except StopIteration:
    pass

#HIRAYA ARROW
arrows = []
blood_effects = []

# WAVE IMAGES (ADD HERE)
wave_images = {
    1: pygame.image.load("images/ui/wave1.png").convert_alpha(),
    2: pygame.image.load("images/ui/wave2.png").convert_alpha(),
    3: pygame.image.load("images/ui/wave3.png").convert_alpha(),
    4: pygame.image.load("images/ui/wave4.png").convert_alpha(),
    5: pygame.image.load("images/ui/final_wave.png").convert_alpha()
}

celebrate_images = [
    pygame.image.load("images/celebrate/0.png").convert_alpha(),
    pygame.image.load("images/celebrate/1.png").convert_alpha()
]

# I-scale natin pareho para kasing-laki ng player mo (330x400)
celebrate_images = [pygame.transform.scale(img, (300, 360)) for img in celebrate_images]

wave_ready = False

def start_game():
    pygame.mixer.music.play(-1)

    global camera_x
    global current_wave
    global wave_transition
    global transition_timer
    global game_won
    global game_bg
    global ground_y
    global active_gems
    global zombies_killed

    active_gems.clear()
    zombies_killed = 0

    game_bg = pygame.image.load(st.GAME_MAP).convert()
    game_bg = pygame.transform.scale(game_bg, (WORLD_WIDTH, h))

    current_wave = 1
    game_won = False

    player.x = st.START_X

    ground_y = h // 2 + st.START_Y_OFFSET

    player.y = ground_y
    player.velocity_y = 0
    player.is_jumping = False
    player.health = player.max_health

    zombies.x = 1000
    zombies.y = ground_y

    zombies.frame_index = 0
    zombies.state = "walk"

    camera_x = 0

    setup_wave()

def setup_wave():
    wave_sound.play()

    global current_wave
    global wave_anim_timer, wave_alpha, wave_scale
    global wave_intro_active, wave_intro_finished

    zombies.enemies.clear()
    
    # TRIGGER THE SPAWN POOL MATH
    zombies.generate_pool(current_wave)

    if current_wave == 1:
        zombie_health = 500
        zombie_speed = 3
        zombie_damage = 15
        zombies.max_enemies = 3  # Max alive on screen at once

    elif current_wave == 2:
        zombie_health = 750
        zombie_speed = 4
        zombie_damage = 30
        zombies.max_enemies = 4

    elif current_wave == 3:
        zombie_health = 2000
        zombie_speed = 4
        zombie_damage = 60
        zombies.max_enemies = 4

    elif current_wave == 4:
        zombie_health = 2250
        zombie_speed = 4
        zombie_damage = 90
        zombies.max_enemies = 5

    elif current_wave == 5:
        zombie_health = 500
        zombie_speed = 2.5
        zombie_damage = 150
        zombies.max_enemies = 5

    st.ZOMBIE_HEALTH = zombie_health
    st.ZOMBIE_SPEED = zombie_speed
    st.ZOMBIE_DAMAGE = zombie_damage

    wave_anim_timer = 0
    wave_alpha = 0
    wave_scale = 0.3

    wave_intro_active = True
    wave_intro_finished = False

def reset_game():
    global current_wave, wave_transition, game_won, camera_x

    pygame.mixer.music.play(-1)

    current_wave = 1
    wave_transition = False
    game_won = False
    camera_x = 0

    player.x = st.START_X
    player.y = h // 2 + st.START_Y_OFFSET
    player.health = player.max_health
    player.velocity_y = 0
    player.is_jumping = False

    zombies.enemies.clear()
    zombies.total_spawned = 0
    zombies.total_killed = 0

    setup_wave()

zombies_killed = 0
active_gems = []

is_celebrating = False
celebration_timer = 0
celebrate_frame = 0

running = True

while running:

    delta = clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state != st.GAME:  
                click_sound.play()
        
        if state == st.GAME:
            if event.type == pygame.KEYDOWN:

                # PAUSE SYSTEM
                if event.key == pygame.K_ESCAPE:
                    state = st.PAUSE

                if event.key == pygame.K_SPACE:
                    player.jump()

                if event.key == pygame.K_a:
                    player.attack()

   
    keys = pygame.key.get_pressed()

    # MENU UPDATE
    if state == st.MENU:

        action = menu.run()

        if action == "start":
            click_sound.play()
            
            # --- ADD CHARACTER SELECTION HERE ---
            selector.selected_character = None  # Reset selected character
            character_type = selector.run()
            
            player = Character(
                x = st.START_X,
                y = h // 2 + st.START_Y_OFFSET,
                settings = st,
                character_type = character_type
            )

            state = st.GAME
            start_game()
            
    # PAUSE MENU UPDATE
    elif state == st.PAUSE:

        result, music_on = pause_menu.run(music_on)

        if result == "continue":
            state = st.GAME

        elif result == "home":

            state = st.MENU
            menu = Menu(screen)
            action = menu.run()

            if action == "start":
                
                # --- ADD CHARACTER SELECTION HERE TOO ---
                selector = CharacterSelect(screen, click_sound)
                character_type = selector.run()
                
                player = Character(
                    x = st.START_X,
                    y = h // 2 + st.START_Y_OFFSET,
                    settings = st,
                    character_type = character_type
                )
                
                state = st.GAME
                start_game()

    # GAME UPDATE
    if state == st.GAME and not game_won and not paused:

        if wave_intro_active:

            wave_anim_timer += 1

            if wave_anim_timer < 60:
                wave_alpha = min(255, wave_alpha + 10)
                wave_scale = min(0.8, wave_scale + 0.02)

            elif wave_anim_timer < 120:
                wave_alpha = 255

            else:
                wave_intro_active = False
                wave_intro_finished = True

        player.update(keys)

        # --- NEW DELAYED ARROW SPAWN ---
        if player.character_type == "hiraya" and player.arrow_spawned:
            arrows.append(
                Arrow(
                    player.x + 50 if player.facing_right else player.x - 50,
                    player.y - 50,
                    player.facing_right,
                    player.arrow_image
                )
            )
            # Reset immediately so it only spawns ONE arrow per swing
            player.arrow_spawned = False

        if wave_intro_finished:
            zombies.update(player, current_wave)

            zombies.enemies = [enemy for enemy in zombies.enemies if not (enemy.is_dead and enemy.death_timer <= 0)]

        for arrow in arrows:
            arrow.update()

        # --- PREVENT UPDATING MOVEMENT IF CELEBRATING ---
        # Kapag nagce-celebrate, hindi na natin papayagang bumalik sa "idle" ang animation
        if not is_celebrating:
            player.update(keys)

        # ... (Yung Arrow spawn logic at zombie update mo, hayaan lang sa baba nito) ...

        # --- NEW WAVE & CELEBRATION LOGIC ---
        if (
            zombies.total_spawned >= zombies.wave_spawn_limit
            and len(zombies.enemies) == 0
            and wave_intro_finished
        ):
            # KUNG WAVE 5 ANG NATAPOS (Boss Died)
            if current_wave == 5 and not is_celebrating:
                wave_intro_active = False
                is_celebrating = True
                celebration_timer = 0
                
                pygame.mixer.music.stop()
                victory_sound.play()
                
                # I-force ang player animation sa pag-celebrate
                player.current_action = "celebrate"
                player.frame_index = 0
                
            # KUNG NORMAL WAVE LANG ANG NATAPOS
            elif current_wave < 5:
                current_wave += 1
                setup_wave()

        # --- CELEBRATION TIMER TIMER ---
        if is_celebrating:
            celebration_timer += 1
            
            # Maghihintay ng 180 frames (approx 3 seconds) habang nagpa-play ang animation
            if celebration_timer > 180: 
                win_screen = WinScreen(screen)
                result = win_screen.run()

                if result == "restart":
                    is_celebrating = False
                    reset_game()

                elif result == "quit":
                    is_celebrating = False
                    state = st.MENU
                    menu = Menu(screen)
                    continue

            else:
                setup_wave()

        arrows = [
            arrow for arrow in arrows
            if 0 <= arrow.x <= WORLD_WIDTH
        ]

        for arrow in arrows[:]:

            arrow_rect = arrow.get_rect()   

            for enemy in zombies.enemies:
                
                if enemy.is_dead:
                    continue

                enemy_rect = pygame.Rect(
                    enemy.x - 40,
                    enemy.y - 90,
                    80,
                    180
                )

                if arrow_rect.colliderect(enemy_rect):

                    enemy.take_damage(player.attack_damage)
                    
                    # --- GEM SPAWN LOGIC START ---
                    if enemy.health <= 0:
                        zombies_killed
                        zombies_killed += 1
                        if zombies_killed % 10 == 0:
                            active_gems.append(Gem(enemy.x, enemy.y))
                    
                            gem_spawn_sound.play()
                    arrow_hit_sound.play()

                    # BLOOD EFFECT SPAWN
                    blood_effects.append(
                        BloodEffect(
                            enemy.x + 23,
                            enemy.y,
                            st
                        )
                    )

                    arrows.remove(arrow)
                    break

        for blood in blood_effects:
            blood.update()

        blood_effects = [
            b for b in blood_effects
            if not b.finished
        ]

        collision_dist = 60
        vertical_threshold = 60

        for enemy in zombies.enemies:
            
            if enemy.is_dead:
                    continue

            dx = enemy.x - player.x
            dy = enemy.y - player.y

            if abs(dx) < collision_dist and abs(dy) < vertical_threshold:

                # BLOCK MOVEMENT INTO ENEMY
                if dx > 0 and keys[pygame.K_RIGHT]:
                    player.x = enemy.x - collision_dist

                elif dx < 0 and keys[pygame.K_LEFT]:
                    player.x = enemy.x + collision_dist

        # PLAYER ATTACK
        # Add the character_type check here so Hiraya doesn't use the melee hitbox!
        if player.is_attacking and player.character_type == "lapulapu":

            attack_width = player.attack_range
            attack_height = 140

            # PLAYER CENTER (IMPORTANT)
            px = player.x
            py = player.y

            # CREATE ATTACK BOX IN FRONT ONLY
            if player.facing_right:
                attack_rect = pygame.Rect(
                    px,
                    py - attack_height // 2,
                    attack_width,
                    attack_height
                )
            else:
                attack_rect = pygame.Rect(
                    px - attack_width,
                    py - attack_height // 2,
                    attack_width,
                    attack_height
                )

            for enemy in zombies.enemies:
                
                if enemy.is_dead:
                    continue
                
                ex = enemy.x
                ey = enemy.y

                enemy_rect = pygame.Rect(
                    ex - 40,
                    ey - 90,
                    80,
                    180
                )

                if attack_rect.colliderect(enemy_rect):

                    # CHECK IF THE PLAYER ALREADY HIT SOMETHING THIS SWING
                    if not player.has_hit:
                        enemy.take_damage(player.attack_damage)
                        
                        # --- GEM SPAWN LOGIC START ---
                        if enemy.health <= 0:
                            zombies_killed
                            zombies_killed += 1
                            if zombies_killed % 10 == 0:
                                active_gems.append(Gem(enemy.x, enemy.y))
                        # --- GEM SPAWN LOGIC END ---

                        sword_hit_sound.play()
                    
                    
                        # BLOOD EFFECT SPAWN
                        blood_effects.append(
                            BloodEffect(
                                enemy.x + 23,
                                enemy.y,
                                st
                            )
                        )

                        # SET TO TRUE SO IT DOESN'T TRIGGER AGAIN THIS ANIMATION
                        player.has_hit = True
                        break
            
        # LAPU-LAPU JUMP ATTACK
        # NEW
        if player.is_jumping and player.is_attacking and player.character_type == "lapulapu":

            # Create a hitbox around Lapu-Lapu's body while he is in the air
            jump_rect = pygame.Rect(
                player.x - 50,
                player.y - 100,
                100,
                200
            )

            for enemy in zombies.enemies:
                
                # Ignore dead zombies
                if enemy.is_dead:
                    continue

                enemy_rect = pygame.Rect(
                    enemy.x - 40,
                    enemy.y - 90,
                    80,
                    180
                )

                # If Lapu-Lapu crashes into a zombie while jumping
                if jump_rect.colliderect(enemy_rect):

                    # Make sure he only deals damage once per jump
                    if not player.has_jump_hit:
                        enemy.take_damage(player.attack_damage)
                        
                        # --- GEM SPAWN LOGIC START ---
                        if enemy.health <= 0:
                            zombies_killed
                            zombies_killed += 1
                            if zombies_killed % 10 == 0:
                                active_gems.append(Gem(enemy.x, enemy.y))
                        # --- GEM SPAWN LOGIC END ---

                        sword_hit_sound.play()
                        # BLOOD EFFECT SPAWN
                        blood_effects.append(
                            BloodEffect(
                                enemy.x + 23,
                                enemy.y,
                                st
                            )
                        )

                        player.has_jump_hit = True
                        break
        # --- PLAYER GEM PICKUP LOGIC ---
        # Gumawa ng hitbox para sa player
        player_rect = pygame.Rect(player.x - 50, player.y - 100, 100, 200)
        
        for gem in active_gems[:]:
            if player_rect.colliderect(gem.get_rect()):
                player.heal(250)  # Dagdag buhay sa player (Palitan ang 250 kung gusto mo)
                gem_pickup_sound.play()
                active_gems.remove(gem)
        # -------------------------------

        # PLAYER DEAD
        if player.health <= 0:

            pygame.mixer.music.stop()
            defeat_sound.play()
            pygame.time.delay(1500)

            defeat_screen = DefeatScreen(screen)
            choice = defeat_screen.run()

            if choice == "restart":
                reset_game()
                continue   #CRITICAL

            elif choice == "quit":
                state = st.MENU
                menu = Menu(screen)
                continue    
        
        # LIMIT PLAYER
        player.x = max(0, min(player.x, WORLD_WIDTH))

        # CAMERA FOLLOW
        target_x = player.x - w // 2
        camera_x += (target_x - camera_x) * 0.1

        # LIMIT CAMERA
        camera_x = max(0, min(camera_x, WORLD_WIDTH - w))
        
    # DRAW SYSTEM

    if state == st.MENU:

        menu.draw()

    elif state == st.PAUSE:

    # Draw current game background

        if game_bg:
            screen.blit(game_bg, (-camera_x, 0))

        # Draw entities
        player.draw(screen, camera_x)

        for arrow in arrows:
            arrow.draw(screen, camera_x)
        zombies.draw(screen, camera_x)

        for blood in blood_effects:
            blood.draw(screen, camera_x)

        player.draw_health_bar(screen)

        # Draw pause UI
        pause_menu.draw()

    # GAME DRAW
    elif state == st.GAME:

        # BACKGROUND
        if game_bg:
            screen.blit(game_bg, (int(-camera_x), 0))
        else:
            screen.fill((50, 50, 50))

        # --- DRAW PLAYER OR CELEBRATION IMAGE ---
        # --- DRAW PLAYER OR CELEBRATION ANIMATION ---
        if not is_celebrating:
            # Normal na pag-draw sa player
            player.draw(screen, camera_x)
            
        else:
            # --- CELEBRATION ANIMATION LOGIC ---
            # 1. Bilis ng pagpapalit ng frame (Palitan ang 0.1 kung gusto mong pabilisin o pabagalin)
            celebrate_frame += 0.1 
            
            # 2. I-reset pabalik sa 0 kapag sumobra na sa dami ng pictures (para mag-loop)
            if celebrate_frame >= len(celebrate_images):
                celebrate_frame = 0
                
            # 3. Kunin ang kasalukuyang picture (0 o 1)
            current_image = celebrate_images[int(celebrate_frame)]
            
            # 4. Iharap sa tamang direksyon (Flip kung nakaharap sa kaliwa)
            if not player.facing_right:
                current_image = pygame.transform.flip(current_image, True, False)
                
            # 5. Kunin ang posisyon ng player at i-adjust sa camera
            rect = current_image.get_rect(
                center=(int(player.x - camera_x), int(player.y))
            )
            
            # 6. I-blit (i-draw) sa screen
            screen.blit(current_image, rect)

        # (Ipagpatuloy ang pag-draw ng arrows at zombies sa ibaba nito...)
        for arrow in arrows:
            arrow.draw(screen, int(camera_x))

        # ONLY DRAW ZOMBIE IF ALIVE
        zombies.draw(screen, int(camera_x))
        for blood in blood_effects:
            blood.draw(screen, int(camera_x))
        # DRAW GEMS
        for gem in active_gems:
            gem.draw(screen, int(camera_x))

        # HEALTH BAR
        player.draw_health_bar(screen)

        # TRANSITION OVERLAY

        if wave_intro_active:

            screen.blit(black_overlay, (0, 0))

            img = wave_images.get(current_wave)

            if img:

                size = img.get_size()

                new_size = (
                    int(size[0] * wave_scale),
                    int(size[1] * wave_scale)
                )

                img_scaled = pygame.transform.scale(img, new_size)
                img_scaled.set_alpha(wave_alpha)

                rect = img_scaled.get_rect(center=(w // 2, h // 2))

                screen.blit(img_scaled, rect)

    pygame.display.update()

pygame.quit()
sys.exit()