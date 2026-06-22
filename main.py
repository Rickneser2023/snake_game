import os
import random
import sys

import pygame

from effects import FloatingText, ParticleManager, ScreenShake
from food import Food
from level_manager import LevelManager
from menu import Menu
from powerups import PowerUpManager
from save_system import SaveSystem
from settings import (
    BG_COLOR,
    COMBO_WINDOW_FRAMES,
    DATA_DIR,
    FPS,
    FOOD_COLOR,
    GRID_COLOR,
    HEIGHT,
    POWERUP_SPAWN_CHANCE,
    SHAKE_INTENSITY_LARGE,
    SHAKE_INTENSITY_SMALL,
    TILE_SIZE,
    UI_ACCENT,
    WIDTH,
    get_font,
)
from snake import Snake
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Pro - Nivel Infinito")
        self.fullscreen = False
        self.base_surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_surface = None
        self.display_size = (WIDTH, HEIGHT)
        self._set_display_mode(self.fullscreen)
        self.clock = pygame.time.Clock()

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        self.save_data = SaveSystem.load_game()
        self.highscore = self.save_data.get("highscore", 0)
        self.max_level_reached = self.save_data.get("max_level", 1)
        self.total_games = self.save_data.get("total_games", 0)
        self.best_combo_ever = self.save_data.get("best_combo", 0)
        self.total_foods_eaten = self.save_data.get("foods_eaten", 0)

        self.level_manager = LevelManager()
        self.snake = Snake()
        self.food = Food(self.snake.body, self.level_manager.obstacles)
        self.powerups = PowerUpManager()
        self.ui = UI()
        self.menu = Menu(self.base_surface)

        self.particles = ParticleManager()
        self.shake = ScreenShake()
        self.floating_texts = []

        self.font_small = get_font(20)
        self.font_big = get_font(40)

        self.score = 0
        self.paused = False
        self.running = True
        self.combo_streak = 0
        self.combo_timer = 0
        self.best_combo_this_run = 0
        self.foods_eaten_this_run = 0
        self.powerups_collected = 0
        self.is_slow_mode = False
        self.slow_mode_timer = 0

    def _set_display_mode(self, fullscreen):
        self.fullscreen = fullscreen
        if fullscreen:
            info = pygame.display.Info()
            self.display_size = (info.current_w, info.current_h)
            flags = pygame.FULLSCREEN
        else:
            self.display_size = (WIDTH, HEIGHT)
            flags = pygame.RESIZABLE

        self.display_surface = pygame.display.set_mode(self.display_size, flags)

    def toggle_fullscreen(self):
        self._set_display_mode(not self.fullscreen)

    def _present(self):
        target = self.display_surface
        self.display_size = target.get_size()
        target.fill((0, 0, 0))

        base_w, base_h = WIDTH, HEIGHT
        target_w, target_h = self.display_size
        scale = min(target_w / base_w, target_h / base_h)
        draw_size = (max(1, int(base_w * scale)), max(1, int(base_h * scale)))
        scaled = pygame.transform.smoothscale(self.base_surface, draw_size)
        dest = scaled.get_rect(center=(target_w // 2, target_h // 2))
        target.blit(scaled, dest)
        pygame.display.flip()

    def reset_game(self):
        self.score = 0
        self.snake.reset()
        self.level_manager.reset()
        self.food = Food(self.snake.body, self.level_manager.obstacles)
        self.powerups = PowerUpManager()
        self.particles = ParticleManager()
        self.floating_texts = []
        self.paused = False
        self.combo_streak = 0
        self.combo_timer = 0
        self.best_combo_this_run = 0
        self.foods_eaten_this_run = 0
        self.powerups_collected = 0
        self.is_slow_mode = False
        self.slow_mode_timer = 0

    def _combo_multiplier(self):
        if self.combo_streak >= 8:
            return 3
        if self.combo_streak >= 4:
            return 2
        return 1

    def _register_combo(self):
        if self.combo_timer > 0:
            self.combo_streak += 1
        else:
            self.combo_streak = 1
        self.combo_timer = COMBO_WINDOW_FRAMES
        self.best_combo_this_run = max(self.best_combo_this_run, self.combo_streak)
        self.best_combo_ever = max(self.best_combo_ever, self.best_combo_this_run)

    def _save_run(self):
        data = SaveSystem.record_run(
            self.score,
            self.level_manager.level,
            self.best_combo_this_run,
            self.foods_eaten_this_run,
        )
        self.highscore = data.get("highscore", self.highscore)
        self.max_level_reached = data.get("max_level", self.max_level_reached)
        self.total_games = data.get("total_games", self.total_games)
        self.best_combo_ever = data.get("best_combo", self.best_combo_ever)
        self.total_foods_eaten = data.get("foods_eaten", self.total_foods_eaten)

    def _draw_world(self, shake_offset):
        world = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        world.fill(BG_COLOR)

        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(world, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, TILE_SIZE):
            pygame.draw.line(world, GRID_COLOR, (0, y), (WIDTH, y), 1)

        for obs in self.level_manager.obstacles:
            obs.draw(world)

        self.food.draw(world)
        self.powerups.draw(world)
        self.snake.draw(world)
        self.particles.draw(world)

        for ft in self.floating_texts:
            ft.draw(world)

        self.base_surface.blit(world, shake_offset)

    def run(self):
        while self.running:
            choice = self.menu.main_menu(self.highscore, self._present, self.toggle_fullscreen)
            if choice == "START":
                self.game_loop()

    def game_loop(self):
        self.reset_game()
        game_active = True

        while game_active and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    game_active = False
                elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                    self.display_size = event.size
                    self.display_surface = pygame.display.set_mode(self.display_size, pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                        continue
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:
                        game_active = False
                    elif not self.paused:
                        self.snake.handle_input(event.key)

            if not self.paused:
                self.snake.update()
                self.particles.update()
                self.powerups.update()

                if self.combo_timer > 0:
                    self.combo_timer -= 1
                elif self.combo_streak > 0:
                    self.combo_streak = 0

                spawn_chance = min(
                    POWERUP_SPAWN_CHANCE + (self.level_manager.level * 0.00025),
                    0.01,
                )
                if self.powerups.active_powerup is None and random.random() < spawn_chance:
                    self.powerups.spawn_powerup(self.snake.body, self.level_manager.obstacles)

                if getattr(self, "is_slow_mode", False):
                    self.slow_mode_timer -= 1
                    if self.slow_mode_timer <= 0:
                        self.is_slow_mode = False
                        from settings import INITIAL_SPEED, MAX_SPEED, SPEED_INCREMENT

                        self.level_manager.speed = min(
                            INITIAL_SPEED + (self.level_manager.level - 1) * SPEED_INCREMENT,
                            MAX_SPEED,
                        )

                for ft in self.floating_texts[:]:
                    ft.update()
                    if ft.life <= 0:
                        self.floating_texts.remove(ft)

                if self.snake.body[0] == self.food.position:
                    self.foods_eaten_this_run += 1
                    self._register_combo()
                    points = self._combo_multiplier()
                    self.score += points
                    self.snake.grow_pending += 1

                    self.particles.emit(
                        self.food.position[0] + TILE_SIZE // 2,
                        self.food.position[1] + TILE_SIZE // 2,
                        FOOD_COLOR,
                    )
                    self.shake.trigger(SHAKE_INTENSITY_SMALL, 5)

                    combo_text = f"+{points}"
                    if self.combo_streak > 1:
                        combo_text = f"{combo_text} x{self.combo_streak}"
                    self.floating_texts.append(
                        FloatingText(
                            self.snake.body[0][0],
                            self.snake.body[0][1],
                            combo_text,
                            (255, 255, 255),
                            self.font_small,
                        )
                    )

                    level_up = self.level_manager.update(self.score, self.snake.body)
                    if level_up:
                        self.floating_texts.append(
                            FloatingText(
                                WIDTH // 2 - 70,
                                HEIGHT // 2,
                                "NIVEL UP!",
                                UI_ACCENT,
                                self.font_big,
                            )
                        )

                    self.food = Food(self.snake.body, self.level_manager.obstacles)

                    if self.score > self.highscore:
                        self.highscore = self.score
                        SaveSystem.update_highscore(self.highscore)

                if self.powerups.active_powerup and self.snake.body[0] == self.powerups.active_powerup.position:
                    p = self.powerups.active_powerup
                    self.particles.emit(
                        p.position[0] + TILE_SIZE // 2,
                        p.position[1] + TILE_SIZE // 2,
                        p.color,
                    )
                    self.powerups_collected += 1

                    if p.type == "GOLD":
                        self.score += 3
                        self.snake.grow_pending += 2
                        text = "+3"
                    elif p.type == "SLOW":
                        self.is_slow_mode = True
                        from settings import POWERUP_DURATION_FRAMES

                        self.slow_mode_timer = POWERUP_DURATION_FRAMES
                        self.level_manager.speed = max(5, self.level_manager.speed - 10)
                        text = "SLOW!"
                    elif p.type == "GHOST":
                        self.snake.is_ghost = True
                        from settings import POWERUP_DURATION_FRAMES

                        self.snake.ghost_timer = POWERUP_DURATION_FRAMES
                        text = "GHOST!"
                    else:
                        self.snake.cut_tail()
                        text = "CUT!"

                    self.floating_texts.append(
                        FloatingText(
                            self.snake.body[0][0],
                            self.snake.body[0][1],
                            text,
                            p.color,
                            self.font_small,
                        )
                    )
                    self.powerups.active_powerup = None
                    self.shake.trigger(SHAKE_INTENSITY_SMALL, 5)

                if self.snake.check_collision(self.level_manager.obstacles):
                    self.particles.emit(
                        self.snake.body[0][0],
                        self.snake.body[0][1],
                        (255, 0, 0),
                        count=30,
                    )
                    self.shake.trigger(SHAKE_INTENSITY_LARGE, 20)
                    self._save_run()

                    self._present()
                    pygame.time.delay(350)

                    result = self.menu.game_over(
                        self.score,
                        self.highscore,
                        self.level_manager.level,
                        self.best_combo_this_run,
                        self.foods_eaten_this_run,
                        self._present,
                        self.toggle_fullscreen,
                    )
                    if result == "RESTART":
                        self.reset_game()
                    else:
                        game_active = False

            shake_offset = self.shake.get_offset()
            self.base_surface.fill(BG_COLOR)
            self._draw_world(shake_offset)

            self.ui.draw_hud(
                self.base_surface,
                self.score,
                self.highscore,
                self.level_manager.level,
                self.combo_streak,
                self.combo_timer,
                self.snake.is_ghost,
                getattr(self.snake, "ghost_timer", 0),
                getattr(self, "is_slow_mode", False),
                getattr(self, "slow_mode_timer", 0),
            )

            if self.paused:
                self.ui.draw_pause(self.base_surface)

            self._present()
            self.clock.tick(self.level_manager.speed)


if __name__ == "__main__":
    game = Game()
    game.run()
