import random
from settings import WIDTH, HEIGHT, TILE_SIZE, INITIAL_SPEED, SPEED_INCREMENT, POINTS_PER_LEVEL, MAX_SPEED
from obstacle import Obstacle

class LevelManager:
    def __init__(self):
        self.level = 1
        self.speed = INITIAL_SPEED
        self.obstacles = []

    def update(self, score):
        new_level = (score // POINTS_PER_LEVEL) + 1
        if new_level > self.level:
            self.level = new_level
            self.speed = min(INITIAL_SPEED + (self.level - 1) * SPEED_INCREMENT, MAX_SPEED)
            self.generate_obstacles()
            return True # Subió de nivel
        return False

    def generate_obstacles(self):
        self.obstacles = []
        # Generar obstáculos aleatorios basados en el nivel
        num_obstacles = min(self.level * 2, 30) 
        for _ in range(num_obstacles):
            while True:
                x = random.randrange(2, (WIDTH // TILE_SIZE) - 2) * TILE_SIZE
                y = random.randrange(2, (HEIGHT // TILE_SIZE) - 2) * TILE_SIZE
                # Evitar el centro para no atrapar a la serpiente al inicio
                if abs(x - WIDTH//2) > 100 or abs(y - HEIGHT//2) > 100:
                    self.obstacles.append(Obstacle(x, y))
                    break

    def reset(self):
        self.level = 1
        self.speed = INITIAL_SPEED
        self.obstacles = []
