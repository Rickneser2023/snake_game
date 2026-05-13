import pygame
import sys
import os
from settings import WIDTH, HEIGHT, FPS, BG_COLOR, TILE_SIZE
from snake import Snake
from food import Food
from level_manager import LevelManager
from save_system import SaveSystem
from ui import UI
from menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Pro - Nivel Infinito")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Sistemas
        self.save_data = SaveSystem.load_game()
        self.highscore = self.save_data.get("highscore", 0)
        
        self.level_manager = LevelManager()
        self.snake = Snake()
        self.food = Food(self.snake.body, self.level_manager.obstacles)
        self.ui = UI()
        self.menu = Menu(self.screen)
        
        self.score = 0
        self.paused = False
        self.running = True

    def reset_game(self):
        self.score = 0
        self.snake.reset()
        self.level_manager.reset()
        self.food = Food(self.snake.body, self.level_manager.obstacles)
        self.paused = False

    def run(self):
        while self.running:
            # Mostrar Menú Principal
            choice = self.menu.main_menu(self.highscore)
            if choice == "START":
                self.game_loop()

    def game_loop(self):
        self.reset_game()
        game_active = True
        
        while game_active:
            # 1. Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if event.key == pygame.K_ESCAPE:
                        game_active = False
                    
                    self.snake.handle_input(pygame.key.get_pressed())

            if not self.paused:
                # 2. Lógica
                self.snake.update()

                # Colisión con comida
                if self.snake.body[0] == self.food.position:
                    self.score += 1
                    self.snake.grow_pending = True
                    self.level_manager.update(self.score)
                    self.food = Food(self.snake.body, self.level_manager.obstacles)
                    
                    # Auto-guardado de record
                    if self.score > self.highscore:
                        self.highscore = self.score
                        SaveSystem.update_highscore(self.highscore)

                # Colisión con paredes, obstáculos o cuerpo
                if self.snake.check_collision(self.level_manager.obstacles):
                    # Guardar progreso antes de morir
                    SaveSystem.save_game({
                        "level": self.level_manager.level,
                        "score": self.score,
                        "highscore": self.highscore
                    })
                    
                    # Pantalla Game Over
                    result = self.menu.game_over(self.score, self.highscore)
                    if result == "RESTART":
                        self.reset_game()
                    else:
                        game_active = False

            # 3. Dibujado
            self.screen.fill(BG_COLOR)
            
            # Dibujar cuadrícula tenue (opcional, para estilo retro)
            for x in range(0, WIDTH, TILE_SIZE):
                pygame.draw.line(self.screen, (30, 30, 40), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, TILE_SIZE):
                pygame.draw.line(self.screen, (30, 30, 40), (0, y), (WIDTH, y))

            for obs in self.level_manager.obstacles:
                obs.draw(self.screen)
                
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            self.ui.draw_hud(self.screen, self.score, self.highscore, self.level_manager.level)
            
            if self.paused:
                self.ui.draw_pause(self.screen)

            pygame.display.flip()
            self.clock.tick(self.level_manager.speed)

if __name__ == "__main__":
    game = Game()
    game.run()
