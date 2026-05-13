import pygame
from settings import TILE_SIZE, SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, WIDTH, HEIGHT

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        self.grow_pending = False

    def handle_input(self, keys):
        if keys[pygame.K_UP] and self.direction != "DOWN":
            self.next_direction = "UP"
        if keys[pygame.K_DOWN] and self.direction != "UP":
            self.next_direction = "DOWN"
        if keys[pygame.K_LEFT] and self.direction != "RIGHT":
            self.next_direction = "LEFT"
        if keys[pygame.K_RIGHT] and self.direction != "LEFT":
            self.next_direction = "RIGHT"

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
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def check_collision(self, obstacles):
        head = self.body[0]
        
        # Paredes
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        
        # Propio cuerpo
        if head in self.body[1:]:
            return True
            
        # Obstáculos
        if head in [ob.position for ob in obstacles]:
            return True
            
        return False

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            rect = pygame.Rect(segment[0], segment[1], TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, color, rect, border_radius=4)
            # Ojos si es la cabeza
            if i == 0:
                eye_size = 4
                if self.direction in ["RIGHT", "LEFT"]:
                    pygame.draw.circle(surface, (0,0,0), (rect.centerx, rect.top + 6), eye_size)
                    pygame.draw.circle(surface, (0,0,0), (rect.centerx, rect.bottom - 6), eye_size)
                else:
                    pygame.draw.circle(surface, (0,0,0), (rect.left + 6, rect.centery), eye_size)
                    pygame.draw.circle(surface, (0,0,0), (rect.right - 6, rect.centery), eye_size)
