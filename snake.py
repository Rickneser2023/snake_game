import pygame
import math
from settings import TILE_SIZE, SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, SNAKE_TAIL_COLOR, WIDTH, HEIGHT

class Snake:
    def __init__(self):
        self.reset()
        self.animation_offset = 0

    def reset(self):
        self.body = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        self.grow_pending = 0
        self.is_ghost = False
        self.ghost_timer = 0
        self.animation_offset = 0

    def handle_input(self, key):
        key_to_direction = {
            pygame.K_UP: "UP",
            pygame.K_w: "UP",
            pygame.K_DOWN: "DOWN",
            pygame.K_s: "DOWN",
            pygame.K_LEFT: "LEFT",
            pygame.K_a: "LEFT",
            pygame.K_RIGHT: "RIGHT",
            pygame.K_d: "RIGHT",
        }
        new_direction = key_to_direction.get(key)
        if not new_direction:
            return

        opposite = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
        }
        if new_direction != opposite[self.next_direction]:
            self.next_direction = new_direction

    def update(self):
        self.direction = self.next_direction
        head = list(self.body[0])

        if self.direction == "UP":
            head[1] -= TILE_SIZE
        elif self.direction == "DOWN":
            head[1] += TILE_SIZE
        elif self.direction == "LEFT":
            head[0] -= TILE_SIZE
        elif self.direction == "RIGHT":
            head[0] += TILE_SIZE

        self.body.insert(0, head)
        if self.grow_pending == 0:
            self.body.pop()
        else:
            self.grow_pending -= 1
            
        if self.is_ghost:
            self.ghost_timer -= 1
            if self.ghost_timer <= 0:
                self.is_ghost = False
                self.ghost_timer = 0
        
        self.animation_offset += 0.2

    def cut_tail(self):
        if len(self.body) > 3:
            new_len = max(3, len(self.body) // 2)
            self.body = self.body[:new_len]

    def check_collision(self, obstacles):
        head = self.body[0]
        
        # Paredes
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
            
        if self.is_ghost:
            return False
        
        # Propio cuerpo
        if head in self.body[1:]:
            return True
            
        # Obstáculos
        if head in [ob.position for ob in obstacles]:
            return True
            
        return False

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            # Calcular color degradado
            ratio = i / len(self.body)
            r = int(SNAKE_HEAD_COLOR[0] * (1 - ratio) + SNAKE_TAIL_COLOR[0] * ratio)
            g = int(SNAKE_HEAD_COLOR[1] * (1 - ratio) + SNAKE_TAIL_COLOR[1] * ratio)
            b = int(SNAKE_HEAD_COLOR[2] * (1 - ratio) + SNAKE_TAIL_COLOR[2] * ratio)
            color = (r, g, b)
            
            if self.is_ghost:
                color = (147, 112, 219) # Purple color for ghost mode

            rect = pygame.Rect(segment[0], segment[1], TILE_SIZE, TILE_SIZE)
            
            # Dibujar segmento con bordes redondeados
            pygame.draw.rect(surface, color, rect, border_radius=TILE_SIZE // 3)
            
            # Efecto de brillo en la cabeza
            if i == 0:
                glow_size = TILE_SIZE + int(math.sin(self.animation_offset) * 4)
                glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*color, 50), (glow_size, glow_size), glow_size)
                surface.blit(glow_surf, (rect.centerx - glow_size, rect.centery - glow_size))

                # Ojos
                eye_color = (255, 255, 255)
                eye_size = 3
                pupil_color = (0, 0, 0)
                
                if self.direction in ["RIGHT", "LEFT"]:
                    # Ojo 1
                    pygame.draw.circle(surface, eye_color, (rect.centerx, rect.top + 6), eye_size + 1)
                    pygame.draw.circle(surface, pupil_color, (rect.centerx + (2 if self.direction == "RIGHT" else -2), rect.top + 6), eye_size - 1)
                    # Ojo 2
                    pygame.draw.circle(surface, eye_color, (rect.centerx, rect.bottom - 6), eye_size + 1)
                    pygame.draw.circle(surface, pupil_color, (rect.centerx + (2 if self.direction == "RIGHT" else -2), rect.bottom - 6), eye_size - 1)
                else:
                    # Ojo 1
                    pygame.draw.circle(surface, eye_color, (rect.left + 6, rect.centery), eye_size + 1)
                    pygame.draw.circle(surface, pupil_color, (rect.left + 6, rect.centery + (2 if self.direction == "DOWN" else -2)), eye_size - 1)
                    # Ojo 2
                    pygame.draw.circle(surface, eye_color, (rect.right - 6, rect.centery), eye_size + 1)
                    pygame.draw.circle(surface, pupil_color, (rect.right - 6, rect.centery + (2 if self.direction == "DOWN" else -2)), eye_size - 1)
