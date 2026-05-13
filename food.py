import pygame
import random
from settings import TILE_SIZE, FOOD_COLOR, WIDTH, HEIGHT

class Food:
    def __init__(self, snake_body, obstacles):
        self.position = self.generate_position(snake_body, obstacles)

    def generate_position(self, snake_body, obstacles):
        while True:
            x = random.randrange(0, WIDTH // TILE_SIZE) * TILE_SIZE
            y = random.randrange(0, HEIGHT // TILE_SIZE) * TILE_SIZE
            pos = [x, y]
            if pos not in snake_body and pos not in [ob.position for ob in obstacles]:
                return pos

    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], TILE_SIZE, TILE_SIZE)
        # Efecto de brillo para la comida
        pygame.draw.circle(surface, FOOD_COLOR, rect.center, TILE_SIZE // 2)
        pygame.draw.circle(surface, (255, 255, 255), rect.center, TILE_SIZE // 4)
