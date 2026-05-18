import pygame
import sys
import os
from settings import (WIDTH, HEIGHT, FPS, BG_COLOR, TILE_SIZE, 
                      FOOD_COLOR, PARTICLE_COLOR, SHAKE_INTENSITY_SMALL, 
                      SHAKE_INTENSITY_LARGE, SHAKE_DURATION, DATA_DIR, UI_ACCENT)
from snake import Snake
from food import Food
from level_manager import LevelManager
from save_system import SaveSystem
from ui import UI
from menu import Menu
from effects import ParticleManager, ScreenShake, FloatingText
from powerups import PowerUpManager
import random

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Pro - Nivel Infinito")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Asegurar que el directorio de datos existe
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            
        # Sistemas
        self.save_data = SaveSystem.load_game()
        self.highscore = self.save_data.get("highscore", 0)
        
        self.level_manager = LevelManager()
        self.snake = Snake()
        self.food = Food(self.snake.body, self.level_manager.obstacles)
        self.powerups = PowerUpManager()
        self.ui = UI()
        self.menu = Menu(self.screen)
        
        # Efectos
        self.particles = ParticleManager()
        self.shake = ScreenShake()
        self.floating_texts = []
        
        self.score = 0
        self.paused = False
        self.running = True

    def reset_game(self):
        self.score = 0
        self.snake.reset()
        self.level_manager.reset()
        self.food = Food(self.snake.body, self.level_manager.obstacles)
        self.powerups = PowerUpManager()
        self.particles = ParticleManager()
        self.floating_texts = []
        self.paused = False
        self.is_slow_mode = False
        self.slow_mode_timer = 0

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
                self.particles.update()
                self.powerups.update()
                
                # Spawn aleatorio de powerups
                if self.powerups.active_powerup is None and random.random() < 0.002:
                    self.powerups.spawn_powerup(self.snake.body, self.level_manager.obstacles)
                
                # Gestionar timer de slow mode
                if getattr(self, 'is_slow_mode', False):
                    self.slow_mode_timer -= 1
                    if self.slow_mode_timer <= 0:
                        self.is_slow_mode = False
                        # Recalcular velocidad basada en el nivel
                        from settings import INITIAL_SPEED, SPEED_INCREMENT, MAX_SPEED
                        self.level_manager.speed = min(INITIAL_SPEED + (self.level_manager.level - 1) * SPEED_INCREMENT, MAX_SPEED)

                for ft in self.floating_texts[:]:
                    ft.update()
                    if ft.life <= 0:
                        self.floating_texts.remove(ft)

                # Colisión con comida
                if self.snake.body[0] == self.food.position:
                    self.score += 1
                    self.snake.grow_pending += 1
                    
                    # Efectos al comer
                    self.particles.emit(self.food.position[0] + TILE_SIZE//2, 
                                       self.food.position[1] + TILE_SIZE//2, 
                                       FOOD_COLOR)
                    self.shake.trigger(SHAKE_INTENSITY_SMALL, 5)
                    self.floating_texts.append(FloatingText(self.snake.body[0][0], self.snake.body[0][1], "+1", (255,255,255), pygame.font.SysFont("Consolas", 20, bold=True)))
                    
                    level_up = self.level_manager.update(self.score)
                    if level_up:
                        self.floating_texts.append(FloatingText(WIDTH//2 - 50, HEIGHT//2, "¡NIVEL UP!", UI_ACCENT, pygame.font.SysFont("Consolas", 40, bold=True)))
                    
                    self.food = Food(self.snake.body, self.level_manager.obstacles)
                    
                    # Auto-guardado de record
                    if self.score > self.highscore:
                        self.highscore = self.score
                        SaveSystem.update_highscore(self.highscore)

                # Colision con powerup
                if self.powerups.active_powerup and self.snake.body[0] == self.powerups.active_powerup.position:
                    p = self.powerups.active_powerup
                    self.particles.emit(p.position[0] + TILE_SIZE//2, p.position[1] + TILE_SIZE//2, p.color)
                    
                    if p.type == "GOLD":
                        self.score += 3
                        self.snake.grow_pending += 2
                        self.floating_texts.append(FloatingText(self.snake.body[0][0], self.snake.body[0][1], "+3", p.color, pygame.font.SysFont("Consolas", 20, bold=True)))
                    elif p.type == "SLOW":
                        self.is_slow_mode = True
                        from settings import POWERUP_DURATION_FRAMES
                        self.slow_mode_timer = POWERUP_DURATION_FRAMES
                        self.level_manager.speed = max(5, self.level_manager.speed - 10)
                        self.floating_texts.append(FloatingText(self.snake.body[0][0], self.snake.body[0][1], "SLOW!", p.color, pygame.font.SysFont("Consolas", 20, bold=True)))
                    elif p.type == "GHOST":
                        self.snake.is_ghost = True
                        from settings import POWERUP_DURATION_FRAMES
                        self.snake.ghost_timer = POWERUP_DURATION_FRAMES
                        self.floating_texts.append(FloatingText(self.snake.body[0][0], self.snake.body[0][1], "GHOST!", p.color, pygame.font.SysFont("Consolas", 20, bold=True)))
                    elif p.type == "SCISSORS":
                        self.snake.cut_tail()
                        self.floating_texts.append(FloatingText(self.snake.body[0][0], self.snake.body[0][1], "CUT!", p.color, pygame.font.SysFont("Consolas", 20, bold=True)))
                        
                    self.powerups.active_powerup = None
                    self.shake.trigger(SHAKE_INTENSITY_SMALL, 5)

                # Colisión con paredes, obstáculos o cuerpo
                if self.snake.check_collision(self.level_manager.obstacles):
                    # Efecto de muerte
                    self.particles.emit(self.snake.body[0][0], self.snake.body[0][1], (255, 0, 0), count=30)
                    self.shake.trigger(SHAKE_INTENSITY_LARGE, 20)
                    
                    # Guardar progreso antes de morir
                    SaveSystem.save_game({
                        "level": self.level_manager.level,
                        "score": self.score,
                        "highscore": self.highscore
                    })
                    
                    # Esperar un momento para ver la explosión
                    pygame.display.flip()
                    pygame.time.delay(500)
                    
                    # Pantalla Game Over
                    result = self.menu.game_over(self.score, self.highscore)
                    if result == "RESTART":
                        self.reset_game()
                    else:
                        game_active = False

            # 3. Dibujado
            # Aplicar Screen Shake
            shake_offset = self.shake.get_offset()
            
            self.screen.fill(BG_COLOR)
            
            # Dibujar cuadrícula tenue (con movimiento sutil)
            grid_offset = (pygame.time.get_ticks() // 100) % TILE_SIZE
            for x in range(shake_offset[0], WIDTH + TILE_SIZE, TILE_SIZE):
                pygame.draw.line(self.screen, (25, 25, 35), (x, 0), (x, HEIGHT))
            for y in range(shake_offset[1], HEIGHT + TILE_SIZE, TILE_SIZE):
                pygame.draw.line(self.screen, (25, 25, 35), (0, y), (WIDTH, y))

            # Dibujar elementos del juego con el offset de la cámara
            temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            
            for obs in self.level_manager.obstacles:
                obs.draw(self.screen)
                
            self.food.draw(self.screen)
            self.powerups.draw(self.screen)
            self.snake.draw(self.screen)
            self.particles.draw(self.screen)
            for ft in self.floating_texts:
                ft.draw(self.screen)
            
            self.ui.draw_hud(self.screen, self.score, self.highscore, self.level_manager.level, 
                             self.snake.is_ghost, getattr(self.snake, 'ghost_timer', 0), 
                             getattr(self, 'is_slow_mode', False), getattr(self, 'slow_mode_timer', 0))
            
            if self.paused:
                self.ui.draw_pause(self.screen)

            # Blit final con offset de shake (aplicado manualmente a los dibujos o vía superficie)
            # Nota: Para simplificar, ya moví el fondo. Los elementos se dibujan en coordenadas reales.
            # Un enfoque más profesional sería dibujar todo en una superficie y blitearla con el offset.
            
            pygame.display.flip()
            self.clock.tick(self.level_manager.speed)

if __name__ == "__main__":
    game = Game()
    game.run()
