import pygame
import os


pygame.font.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 1200, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
COLOR_INACTIVE = "#ccc0c1"
COLOR_ACTIVE = "#e0d5d6"
COLOR_LIST_INACTIVE = "#939491"
COLOR_LIST_ACTIVE = "#a8a8a6"

# Ships
RED_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "red_inv.png")), (195, 140))
GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "green_inv.png")), (70, 50))
BLUE_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "blue_inv.png")), (70, 50))
PINK_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pink_inv.png")), (150, 80))
ORANGE_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "orange_inv.png")), (45, 45))
YELLOW_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "invader.png")), (130, 90))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
PINK_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_pink.png"))
ORANGE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_orange.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Bonuses
SHIELD_BONUS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "shield_bonus.png")), (50, 50))
HEALTH_BONUS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "health_bonus.png")), (50, 50))
SLOW_BONUS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "slow_bonus.png")), (50, 50))
LIVES_BONUS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "lives_bonus.png")), (50, 50))

# Sound and Pause
SOUND_OFF_ICON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sound_off.png")), (100, 100))
SOUND_ON_ICON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sound_on.png")), (100, 100))
PAUSE_ICON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pause2.png")), (200, 200))
SETTINGS_ICON = pygame.image.load(os.path.join("assets", "settings_icon.png"))

# Extra img
ALIEN = pygame.image.load(os.path.join("assets", "alien.png"))
SCENE = pygame.image.load(os.path.join("assets", "scene.png"))
ROCKET = pygame.image.load(os.path.join("assets", "rocket.png"))
AWARD = pygame.transform.scale(pygame.image.load(os.path.join("assets", "award.png")), (50, 40))
PLANET = pygame.image.load(os.path.join("assets", "planet.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Sounds
GAME_MUSIC = pygame.mixer.Sound("sfx/game_sound.mp3")

# Player data
PLAYER_SPEED_VALUES = {
            'Slow': 3.5,
            'Medium': 4.25,
            'Fast': 5
        }

PLAYER_BULLET_SPEED_VALUES = {
            'Slow': 4,
            'Medium': 5,
            'Fast': 6
        }

# Enemy data
COLOR_MAP = {
            "red": (RED_SPACE_SHIP, RED_LASER),
            "green": (GREEN_SPACE_SHIP, GREEN_LASER),
            "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
            "pink": (PINK_SPACE_SHIP, PINK_LASER),
            "orange": (ORANGE_SPACE_SHIP, ORANGE_LASER)
        }

LASER_OFFSETS = {
        RED_SPACE_SHIP: (48, 45),
        ORANGE_SPACE_SHIP: (-27, 0),
        PINK_SPACE_SHIP: (25, 5),
        "default": (-15, 0)
    }

POINTS_EARNED = {
        "red": 150,
        "blue": 200,
        "green": 250,
        "orange": 300,
        "pink": 350,
    }

SHOOT_TIMING = {
            "red": (2, 40),
            "blue": (2, 0),
            "green": (1, 20),
            "orange": (2, 20),
            "pink": (2, 15)
        }

COLLIDE_DAMAGE = {
            "green": 20,
            "orange": 20,
            "default": 10
        }

ENEMY_SPEED_VALUES = {
            'Slow': 0.75,
            'Medium': 1,
            'Fast': 1.25
        }

ENEMY_BULLET_SPEED_VALUES = {
            'Slow': 3.5,
            'Medium': 5,
            'Fast': 6.5
        }

# Level data
ENEMY_COLORS_BY_LEVELS = {
            1: ["red"],
            2: ["red", "blue"],
            3: ["red", "blue", "green"],
            4: ["red", "blue", "green", "orange"],
            5: ["red", "blue", "green", "orange", "pink"]
        }

SPAWN_OFFSETS = {
                "red": 210,
                "pink": 210,
                "default": 100
            }

# Bonus data
BONUS_TYPES = {
        "health": HEALTH_BONUS,
        "lives": LIVES_BONUS,
        "slow": SLOW_BONUS,
        "shield": SHIELD_BONUS
    }