import random
from enemy import Enemy

class ZombieManager:

    def __init__(self, settings, sounds=None):

        self.settings = settings
        self.sounds = sounds
        self.enemies = []

        self.spawn_timer = 0
        self.spawn_delay = 120  # Base delay between spawns
        self.max_enemies = 5    # Max allowed on screen at the exact same time
        self.sound_cooldown = 0

        self.total_spawned = 0
        self.total_killed = 0

        self.wave_spawn_limit = 0
        self.spawn_pool = []    # Holds the shuffled deck of zombies

    # CREATES THE EXACT ZOMBIE MIX PER WAVE
    def generate_pool(self, current_wave):
        
        self.spawn_pool = []

        if current_wave == 1:
            self.spawn_pool.extend(["normal"] * 10)

        elif current_wave == 2:
            self.spawn_pool.extend(["runner"] * 9 + ["normal"] * 6)

        elif current_wave == 3:
            # armored = sword zombie
            self.spawn_pool.extend(["armored"] * 6 + ["runner"] * 4 + ["normal"] * 3)

        elif current_wave == 4:
            self.spawn_pool.extend(["armored"] * 3 + ["runner"] * 3 + ["normal"] * 4)

        elif current_wave == 5:
            # boss = magellan
            self.spawn_pool.extend(["boss"] * 1 + ["normal"] * 4 + ["runner"] * 3 + ["armored"] * 2)

        # Shuffle the list so they spawn randomly!
        random.shuffle(self.spawn_pool)

        self.wave_spawn_limit = len(self.spawn_pool)
        self.total_spawned = 0
        self.total_killed = 0

    # SPAWN ZOMBIE FROM THE POOL
    def spawn_enemy(self, player_x):

        # If pool is empty, stop spawning
        if not self.spawn_pool:
            return

        side = random.choice(["left", "right"])

        if side == "left":
            spawn_x = random.randint(-300, -100)
        else:
            world_width = 3000 
            spawn_x = world_width + random.randint(100, 300)

        # Spawn height based on our previous fix
        spawn_y = self.settings.SCREEN_CENTER_Y + self.settings.START_Y_OFFSET

        # Draw the next zombie from the shuffled deck
        zombie_type = self.spawn_pool.pop()

        enemy = Enemy(spawn_x, spawn_y, self.settings, zombie_type)

        self.enemies.append(enemy)
        self.total_spawned += 1

        if self.sounds and zombie_type in self.sounds:
            if self.sound_cooldown == 0:
                self.sounds[zombie_type].play()
                self.sound_cooldown = 90

    # UPDATE
    def update(self, player, current_wave):

        self.spawn_timer += 1
        if self.sound_cooldown > 0:
            self.sound_cooldown -= 1

        # Check timer, max on-screen limit, and if the pool still has zombies
        if (
            self.spawn_timer >= self.spawn_delay
            and len(self.enemies) < self.max_enemies
            and len(self.spawn_pool) > 0
        ):

            self.spawn_enemy(player.x)
            
            # Reset timer with random offset so spawns stagger unpredictably
            self.spawn_timer = random.randint(0, 60)

        # Update enemies
        alive_enemies = []

        for enemy in self.enemies:

            enemy.update(player)

            if enemy.is_dead and enemy.death_timer <= 0:
                self.total_killed += 1
                continue

            else:
                alive_enemies.append(enemy)

        self.enemies = alive_enemies
        player.zombie_list = self.enemies

    # DRAW
    def draw(self, screen, camera_x):

        for enemy in self.enemies:
            enemy.draw(screen, camera_x)