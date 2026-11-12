import pygame
import sys

class StoryIntro:

    def __init__(self, screen):

        self.screen = screen
        self.width, self.height = screen.get_size()

        self.font = pygame.font.Font(None, 42)

        # SCENES
        self.scenes = [

            (
                "images/story/scene1.png",
                "The island of Zamal lives in a completely harmonious state, being one with \nnature, and finding peace within its vicinity."
            ),

            (
                "images/story/scene2.png",
                "Amidst the joy and cheers of the island’s people, a fleet of five great ships. \nOf which all were worn, but somehow, it approached the shore, as if operated fine."
            ),

            (
                "images/story/scene3.png",
                "As the fleet came, tides turned red, and the skies darkened its hue. \nThe atmosphere fills the lungs of those who witnessed its arrival. A strangling \nair wraps around their neck and completely overshadows their minds."
            ),

            (
                "images/story/scene4.png",
                "Boats rush to crash on land while the ships halt on their tracks. \nThe invaders come out… they looked pale, nightmarish to say. \nOne would feel their evergrowing bloodlust, absolute terror."
            ),

            (
                "images/story/scene5.png",
                "The invaders then began attacking the people that were in a complete state \nof terror. The undead tore them up, violently tearing the people limb by limb, \neating out the flesh from their bones."
            ),

            (
                "images/story/scene6.png",
                "A closer glance reveals these creatures to be undead, with no mind and soul, \nmuch likely animated... \nPerhaps this could cause the extinction of the island."
            ),

            (
                "images/story/scene7.png",
                "Lapu-Lapu refuses this destruction. He decides to retaliate and \nannihilate all who would cause destruction to his sanctum."
            ),

            (
                "images/story/scene8.png",
                "Slowly, Lapu-Lapu’s sanctum crumbles. His people being ravaged \nby these creatures, the people who he cherished and protected. \nHe unknowingly loses hope."  
            ),

            (
                "images/story/scene9.png",
                "Seemingly out of nowhere, an arrow pierces through Lapu-Lapu’s enemies.\nIt was Hiraya who shot the creatures. Hiraya is devastated as much as \nLapu-Lapu is;they fought and fought nonetheless."
            ),

            (
                "images/story/scene10.png",
                "The tandem fought endlessly, slaying these creatures of pure \nterror all while being outnumbered"
            ),

            (
                "images/story/scene11.png",
                "Hiraya swore to avenge her family, slain before her eyes."
            ),

            (
                "images/story/scene12.png",
                "Lapu-Lapu plans to uncover the truth and root cause of all this destruction."
            )

        ]

        self.images = []

        for img_path, _ in self.scenes:

            img = pygame.image.load(img_path).convert()

            img = pygame.transform.scale(
                img,
                (self.width, self.height)
            )

            self.images.append(img)

        self.scene_index = 0

        self.current_text = ""
        self.char_index = 0

        self.typing_speed = 2
        self.timer = 0

        self.wait_timer = 0
        self.waiting_next = False

        # STORY MUSIC
        self.story_music = pygame.mixer.Sound(
            "soundfile/story_music.MP3"
        )
        self.story_music.set_volume(0.8)

        # TRANSITION EFFECTS
        self.fade_alpha = 255
        self.fading_in = True

        # CINEMATIC ZOOM
        self.zoom_scale = 1.0
            

    def run(self):
        self.story_music.play()
        clock = pygame.time.Clock()
        timer = 0 

        while True:
            timer += 1 # Ngayon, tama na ang timer

            # 2. ISA LANG DAPAT ANG EVENT LOOP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Instant skip gamit ang '0'
                    if event.key == pygame.K_0:
                        self.story_music.stop()
                        return
                    
                    # Next scene gamit ang SPACE
                    if event.key == pygame.K_SPACE:

                        text = self.scenes[self.scene_index][1]

                        # Kung nagta-type pa
                        if not self.waiting_next:

                            self.current_text = text
                            self.char_index = len(text)
                            self.waiting_next = True

                        # Kung tapos na ang text
                        else:
                            if self.scene_index >= len(self.scenes) - 1:
                                self.story_music.stop()
                                return

                            self.fade_out()
                            self.next_scene()

            # 3. Text auto-progress logic (Kung gusto mong kusa syang mag-skip pagtagal)
            # Kung ayaw mo naman ng auto-skip, pwede mong tanggalin ang if timer > 300
            if timer > 300: 
                timer = 0
                # Kung gusto mong kusa syang mag-next, tawagin ang self.next_scene() dito

            # --- Dito na ilalagay ang drawing logic (yung zoom, blit, etc.) ---
            image = self.images[self.scene_index]
            
            # CINEMATIC SLOW ZOOM
            self.zoom_scale += 0.0002
            if self.zoom_scale > 1.2: self.zoom_scale = 1.2
            new_w = int(self.width * self.zoom_scale)
            new_h = int(self.height * self.zoom_scale)
            zoomed = pygame.transform.smoothscale(image, (new_w, new_h))
            rect = zoomed.get_rect(center=(self.width // 2, self.height // 2))
            
            self.screen.blit(zoomed, rect)
            
            # ... (itira mo yung overlay, fade logic, update_typing, at draw_text_box dito)
            
            # FADE IN EFFECT
            if self.fading_in:
                fade_surface = pygame.Surface((self.width, self.height))
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
                self.fade_alpha -= 8
                if self.fade_alpha <= 0:
                    self.fade_alpha = 0
                    self.fading_in = False

            self.update_typing()
            self.draw_text_box()

            pygame.display.flip()
            clock.tick(60) # Huwag kalimutan ang clock.tick!

    def update_typing(self):

        if self.waiting_next:
            return

        self.timer += 1

        if self.timer >= self.typing_speed:

            self.timer = 0

            text = self.scenes[self.scene_index][1]

            if self.char_index < len(text):

                self.current_text += text[self.char_index]

                self.char_index += 1

            else:

                self.waiting_next = True

    def next_scene(self):

        self.scene_index += 1

        # STORY FINISHED
        if self.scene_index >= len(self.scenes):
            self.story_music.stop()   # STOP STORY MUSIC
            return False

        self.current_text = ""
        self.char_index = 0
        self.waiting_next = False

        return True
    
    def fade_out(self):
        clock = pygame.time.Clock()

        fade = pygame.Surface(
            (self.width, self.height)
        )

        fade.fill((0, 0, 0))

        for alpha in range(0, 255, 10):

            fade.set_alpha(alpha)

            image = self.images[self.scene_index]

            self.screen.blit(image, (0, 0))
            self.screen.blit(fade, (0, 0))

            pygame.display.flip()
            clock.tick(60)

        self.fade_alpha = 255
        self.fading_in = True
        self.zoom_scale = 1.0

    def draw_text_box(self):

        box = pygame.Surface(
            (self.width - 100, 170),
            pygame.SRCALPHA
        )

        box.fill((0, 0, 0, 180))

        self.screen.blit(
            box,
            (50, self.height - 220)
        )
        
        # divide the current text into lines based on newline characters
        lines = self.current_text.split("\n")
        
        # this will be the starting y position for the first line of text
        y_offset = self.height - 200

        for line in lines:
            text_surface = self.font.render(
                line,
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                text_surface,
                (80, y_offset)
            )
            
            # add 40 pixels to the y_offset for the next line
            y_offset += 40  

        if self.waiting_next:

            hint = self.font.render(
                "Press SPACE to continue...",
                True,
                (255, 255, 0)
            )

            self.screen.blit(
                hint,
                (80, self.height - 95)
            )