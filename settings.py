import pygame
import os

# STATES
MENU = "menu"
GAME = "game"
PAUSE = "pause"
SETTINGS_MENU = "settings"

# MENU BACKGROUND (FIX)
MENU_BG = "images/ui/bg_4.png"

# MAPS
GAME_MAP = "images/maps/bg1.png"

# PLAYER SETTINGS
START_X = 300
START_Y_OFFSET = 290 # to downshift the player to the ground level
SCREEN_CENTER_Y = 0
GROUND_Y = 650  

PLAYER_SPEED = 3
PLAYER_RUN_SPEED = 4
GRAVITY = 0.5
JUMP_POWER = -14

ANIMATION_SPEED = 0.15

VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720