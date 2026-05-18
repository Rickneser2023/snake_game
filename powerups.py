import pygame
import random
import math
from settings import (TILE_SIZE, WIDTH, HEIGHT, 
                      POWERUP_GOLD_COLOR, POWERUP_SLOW_COLOR, 
                      POWERUP_GHOST_COLOR, POWERUP_SCISSORS_COLOR)

class PowerUp:
    def __init__(self, p_type, color, snake_body, obstacles):
        self.type = p_type
        self.color = color
        self.position = self.generate_position(snake_body, obstacles)
        self.animation_offset = random.uniform(0, 10)
        self.life_timer = 600 # lasts 10 seconds on screen before disappearing

    def generate_position(self, snake_body, obstacles):
        while True:
            x = random.randrange(0, WIDTH // TILE_SIZE) * TILE_SIZE
            y = random.randrange(0, HEIGHT // TILE_SIZE) * TILE_SIZE
            pos = [x, y]
            if pos not in snake_body and pos not in [ob.position for ob in obstacles]:
                return pos

    def update(self):
        self.life_timer -= 1

    def draw(self, surface):
        self.animation_offset += 0.15
        pulse = math.sin(self.animation_offset) * 4
        
        rect = pygame.Rect(self.position[0], self.position[1], TILE_SIZE, TILE_SIZE)
        
        # Glow
        glow_size = (TILE_SIZE // 2) + 6 + pulse
        glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.color, 80), (glow_size, glow_size), glow_size)
        surface.blit(glow_surf, (rect.centerx - glow_size, rect.centery - glow_size))
        
        # Shape depending on type
        if self.type == "GOLD":
            pygame.draw.polygon(surface, self.color, [
                (rect.centerx, rect.top - pulse),
                (rect.right + pulse, rect.centery),
                (rect.centerx, rect.bottom + pulse),
                (rect.left - pulse, rect.centery)
            ])
        elif self.type == "SLOW":
            pygame.draw.polygon(surface, self.color, [
                (rect.left, rect.top), (rect.right, rect.top),
                (rect.centerx, rect.centery),
                (rect.left, rect.bottom), (rect.right, rect.bottom)
            ])
        elif self.type == "GHOST":
            pygame.draw.circle(surface, self.color, rect.center, int((TILE_SIZE // 2) + pulse/2))
            pygame.draw.rect(surface, self.color, (rect.left - pulse/2, rect.centery, TILE_SIZE + pulse, TILE_SIZE//2 + pulse/2))
            # Eyes for ghost
            pygame.draw.circle(surface, (255,255,255), (rect.centerx - 4, rect.centery - 2), 2)
            pygame.draw.circle(surface, (255,255,255), (rect.centerx + 4, rect.centery - 2), 2)
        elif self.type == "SCISSORS":
            pygame.draw.line(surface, self.color, rect.topleft, rect.bottomright, 4)
            pygame.draw.line(surface, self.color, rect.topright, rect.bottomleft, 4)

class PowerUpManager:
    def __init__(self):
        self.active_powerup = None
        
    def spawn_powerup(self, snake_body, obstacles):
        if self.active_powerup is None:
            p_type = random.choice(["GOLD", "SLOW", "GHOST", "SCISSORS"])
            colors = {
                "GOLD": POWERUP_GOLD_COLOR,
                "SLOW": POWERUP_SLOW_COLOR,
                "GHOST": POWERUP_GHOST_COLOR,
                "SCISSORS": POWERUP_SCISSORS_COLOR
            }
            self.active_powerup = PowerUp(p_type, colors[p_type], snake_body, obstacles)

    def update(self):
        if self.active_powerup:
            self.active_powerup.update()
            if self.active_powerup.life_timer <= 0:
                self.active_powerup = None
                
    def draw(self, surface):
        if self.active_powerup:
            self.active_powerup.draw(surface)
