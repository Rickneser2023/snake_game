import pygame
import os

# Pantalla
WIDTH = 800
HEIGHT = 600
FPS = 60
TILE_SIZE = 20

# Colores (Paleta Moderna)
BG_COLOR = (15, 15, 25)
SNAKE_HEAD_COLOR = (0, 255, 150)
SNAKE_BODY_COLOR = (0, 200, 100)
SNAKE_TAIL_COLOR = (0, 150, 80)
FOOD_COLOR = (255, 50, 50)
FOOD_GLOW = (255, 100, 100)
POWERUP_GOLD_COLOR = (255, 215, 0)
POWERUP_SLOW_COLOR = (0, 255, 255)
POWERUP_GHOST_COLOR = (147, 112, 219)
POWERUP_SCISSORS_COLOR = (255, 105, 180)
OBSTACLE_COLOR = (80, 80, 100)
TEXT_COLOR = (240, 240, 240)
UI_ACCENT = (255, 215, 0)
SHADOW_COLOR = (0, 0, 0, 100)
PARTICLE_COLOR = (255, 255, 255)

# Efectos
SHAKE_INTENSITY_SMALL = 3
SHAKE_INTENSITY_LARGE = 8
SHAKE_DURATION = 10
POWERUP_DURATION_FRAMES = 300 # 5 seconds at 60 FPS
POWERUP_SPAWN_CHANCE = 0.003 # Chance por frame para spawnear un powerup
COMBO_WINDOW_FRAMES = 180
HUD_HEIGHT = 72
GRID_COLOR = (25, 25, 35)

# Niveles
POINTS_PER_LEVEL = 5
INITIAL_SPEED = 10
SPEED_INCREMENT = 1.5
MAX_SPEED = 30

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")
SAVE_FILE = os.path.join(DATA_DIR, "save.json")

# Fuentes
pygame.font.init()
def get_font(size):
    return pygame.font.SysFont("Consolas", size, bold=True)
