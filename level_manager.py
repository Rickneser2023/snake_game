import random
from settings import WIDTH, HEIGHT, TILE_SIZE, INITIAL_SPEED, SPEED_INCREMENT, POINTS_PER_LEVEL, MAX_SPEED
from obstacle import Obstacle

class LevelManager:
    def __init__(self):
        self.level = 1
        self.speed = INITIAL_SPEED
        self.obstacles = []

    def update(self, score, snake_body=None):
        new_level = (score // POINTS_PER_LEVEL) + 1
        if new_level > self.level:
            self.level = new_level
            self.speed = min(INITIAL_SPEED + (self.level - 1) * SPEED_INCREMENT, MAX_SPEED)
            self.generate_obstacles(snake_body)
            return True # Subió de nivel
        return False

    def _occupied_set(self, snake_body=None):
        occupied = set()
        if snake_body:
            occupied.update(tuple(segment) for segment in snake_body)
        return occupied

    def _safe_zone(self, x, y):
        return abs(x - WIDTH // 2) <= 100 and abs(y - HEIGHT // 2) <= 100

    def _add_obstacle(self, x, y, occupied):
        pos = (x, y)
        if pos in occupied:
            return False
        if self._safe_zone(x, y):
            return False
        self.obstacles.append(Obstacle(x, y))
        occupied.add(pos)
        return True

    def generate_obstacles(self, snake_body=None):
        self.obstacles = []
        occupied = self._occupied_set(snake_body)
        cols = WIDTH // TILE_SIZE
        rows = HEIGHT // TILE_SIZE

        # Obstáculos base: escalan con el nivel pero dejan espacio para jugar.
        num_obstacles = min(6 + self.level * 2, 32)
        attempts = 0
        while len(self.obstacles) < num_obstacles and attempts < num_obstacles * 8:
            attempts += 1
            x = random.randrange(2, cols - 2) * TILE_SIZE
            y = random.randrange(2, rows - 2) * TILE_SIZE
            self._add_obstacle(x, y, occupied)

        # Un patrón extra según el nivel para darle personalidad al mapa.
        pattern = self.level % 4
        if pattern == 0:
            x = random.randrange(5, cols - 5) * TILE_SIZE
            gap_y = random.randrange(3, rows - 3)
            for row in range(2, rows - 2):
                if row in (gap_y, gap_y + 1):
                    continue
                self._add_obstacle(x, row * TILE_SIZE, occupied)
        elif pattern == 1:
            y = random.randrange(5, rows - 5) * TILE_SIZE
            gap_x = random.randrange(3, cols - 3)
            for col in range(2, cols - 2):
                if col in (gap_x, gap_x + 1):
                    continue
                self._add_obstacle(col * TILE_SIZE, y, occupied)
        elif pattern == 2:
            # Bloques en esquinas para empujar al jugador al centro.
            for x in range(2, 5):
                for y in range(2, 5):
                    self._add_obstacle(x * TILE_SIZE, y * TILE_SIZE, occupied)
            for x in range(cols - 5, cols - 2):
                for y in range(rows - 5, rows - 2):
                    self._add_obstacle(x * TILE_SIZE, y * TILE_SIZE, occupied)
        else:
            # Dos diagonales cortadas crean rutas estrechas interesantes.
            for i in range(3, min(cols, rows) - 3):
                if i % 2 == 0:
                    self._add_obstacle(i * TILE_SIZE, i * TILE_SIZE, occupied)
                    self._add_obstacle((cols - 1 - i) * TILE_SIZE, i * TILE_SIZE, occupied)

    def reset(self):
        self.level = 1
        self.speed = INITIAL_SPEED
        self.obstacles = []
