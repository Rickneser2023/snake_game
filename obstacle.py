import pygame
from settings import TILE_SIZE, OBSTACLE_COLOR

class Obstacle:
    def __init__(self, x, y):
        self.position = [x, y]

    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, OBSTACLE_COLOR, rect, border_radius=4)
        # Detalle para que parezca un bloque
        pygame.draw.rect(surface, (40, 40, 60), rect, 2, border_radius=4)
