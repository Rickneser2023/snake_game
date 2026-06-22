import pygame
import sys
from settings import WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR, UI_ACCENT, get_font

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.font_title = get_font(80)
        self.font_msg = get_font(30)
        self.font_action = get_font(24)
        self.font_small = get_font(18)

    def draw_button(self, text, y_pos, color):
        txt_surf = self.font_action.render(text, True, color)
        rect = txt_surf.get_rect(center=(self.surface.get_width() // 2, y_pos))
        self.surface.blit(txt_surf, rect)
        return rect

    def main_menu(self, highscore, present=None, toggle_fullscreen=None):
        while True:
            sw = self.surface.get_width()
            sh = self.surface.get_height()
            self.surface.fill(BG_COLOR)
            
            title = self.font_title.render("SNAKE PRO", True, UI_ACCENT)
            title_rect = title.get_rect(center=(sw // 2, 120))
            self.surface.blit(title, title_rect)

            high_txt = self.font_msg.render(f"Mejor Puntaje: {highscore}", True, TEXT_COLOR)
            high_rect = high_txt.get_rect(center=(sw // 2, 220))
            self.surface.blit(high_txt, high_rect)

            subtitle = self.font_small.render("Come, crece y sobrevive al caos procedural", True, (180, 180, 190))
            self.surface.blit(subtitle, subtitle.get_rect(center=(sw // 2, 270)))

            self.draw_button("Presiona ENTER para Jugar", 375, (255, 255, 255))
            self.draw_button("Presiona ESC para Salir", 420, (200, 200, 200))
            self.draw_button("Presiona F11 para Pantalla Completa", 465, (180, 220, 255))
            controls = self.font_small.render("Controles: flechas o WASD | P: pausa | ESC: volver", True, (150, 150, 160))
            self.surface.blit(controls, controls.get_rect(center=(sw // 2, sh - 35)))

            if present:
                present()
            else:
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11 and toggle_fullscreen:
                        toggle_fullscreen()
                        break
                    if event.key == pygame.K_RETURN:
                        return "START"
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def game_over(self, score, highscore, level, best_combo, foods_eaten, present=None, toggle_fullscreen=None):
        while True:
            sw = self.surface.get_width()
            sh = self.surface.get_height()
            # Fondo oscuro semi-transparente
            overlay = pygame.Surface((sw, sh))
            overlay.set_alpha(180)
            overlay.fill((20, 0, 0))
            self.surface.blit(overlay, (0, 0))

            title = self.font_title.render("GAME OVER", True, (255, 50, 50))
            title_rect = title.get_rect(center=(sw // 2, 120))
            self.surface.blit(title, title_rect)

            score_txt = self.font_msg.render(f"Puntaje Final: {score}", True, TEXT_COLOR)
            self.surface.blit(score_txt, score_txt.get_rect(center=(sw // 2, 215)))

            if score >= highscore and score > 0:
                new_record = self.font_msg.render("¡NUEVO RECORD!", True, UI_ACCENT)
                self.surface.blit(new_record, new_record.get_rect(center=(sw // 2, 255)))

            stats = [
                f"Nivel alcanzado: {level}",
                f"Comida comida: {foods_eaten}",
                f"Mejor combo: x{best_combo}",
            ]
            y = 315
            for line in stats:
                stat_img = self.font_small.render(line, True, (210, 210, 220))
                self.surface.blit(stat_img, stat_img.get_rect(center=(sw // 2, y)))
                y += 22

            self.draw_button("Presiona ENTER para Reiniciar", 425, (255, 255, 255))
            self.draw_button("Presiona ESC para Menú", 470, (200, 200, 200))
            self.draw_button("Presiona F11 para Pantalla Completa", 515, (180, 220, 255))

            if present:
                present()
            else:
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11 and toggle_fullscreen:
                        toggle_fullscreen()
                        break
                    if event.key == pygame.K_RETURN:
                        return "RESTART"
                    if event.key == pygame.K_ESCAPE:
                        return "MENU"
