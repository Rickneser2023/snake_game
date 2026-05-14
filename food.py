import pygame
import random
import math
from settings import TILE_SIZE, FOOD_COLOR, FOOD_GLOW, WIDTH, HEIGHT

class Food:
    def __init__(self, snake_body, obstacles):
        self.position = self.generate_position(snake_body, obstacles)
        self.animation_offset = random.uniform(0, 10)

    def generate_position(self, snake_body, obstacles):
        while True:
            x = random.randrange(0, WIDTH // TILE_SIZE) * TILE_SIZE
            y = random.randrange(0, HEIGHT // TILE_SIZE) * TILE_SIZE
            pos = [x, y]
            if pos not in snake_body and pos not in [ob.position for ob in obstacles]:
                return pos

    def draw(self, surface):
        self.animation_offset += 0.1
        pulse = math.sin(self.animation_offset) * 3
        
        rect = pygame.Rect(self.position[0], self.position[1], TILE_SIZE, TILE_SIZE)
        
        # Efecto de brillo (Glow)
        glow_size = (TILE_SIZE // 2) + 6 + pulse
        glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*FOOD_COLOR, 80), (glow_size, glow_size), glow_size)
        surface.blit(glow_surf, (rect.centerx - glow_size, rect.centery - glow_size))
        
        # Círculo principal
        pygame.draw.circle(surface, FOOD_COLOR, rect.center, (TILE_SIZE // 2) + pulse/2)
        # Brillo interno
        pygame.draw.circle(surface, (255, 255, 255), rect.center, TILE_SIZE // 4)
