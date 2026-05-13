import pygame
import sys
from settings import WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR, UI_ACCENT, get_font

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.font_title = get_font(80)
        self.font_msg = get_font(30)

    def draw_button(self, text, y_pos, color):
        txt_surf = self.font_msg.render(text, True, color)
        rect = txt_surf.get_rect(center=(WIDTH // 2, y_pos))
        self.surface.blit(txt_surf, rect)
        return rect

    def main_menu(self, highscore):
        while True:
            self.surface.fill(BG_COLOR)
            
            title = self.font_title.render("SNAKE PRO", True, UI_ACCENT)
            title_rect = title.get_rect(center=(WIDTH // 2, 150))
            self.surface.blit(title, title_rect)

            high_txt = self.font_msg.render(f"Mejor Puntaje: {highscore}", True, TEXT_COLOR)
            high_rect = high_txt.get_rect(center=(WIDTH // 2, 250))
            self.surface.blit(high_txt, high_rect)

            start_rect = self.draw_button("Presiona ENTER para Jugar", 400, (255, 255, 255))
            exit_rect = self.draw_button("Presiona ESC para Salir", 450, (200, 200, 200))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "START"
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def game_over(self, score, highscore):
        while True:
            # Fondo oscuro semi-transparente
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(5) # Para efecto de desvanecimiento gradual
            overlay.fill((20, 0, 0))
            self.surface.blit(overlay, (0, 0))

            title = self.font_title.render("GAME OVER", True, (255, 50, 50))
            title_rect = title.get_rect(center=(WIDTH // 2, 150))
            self.surface.blit(title, title_rect)

            score_txt = self.font_msg.render(f"Puntaje Final: {score}", True, TEXT_COLOR)
            self.surface.blit(score_txt, score_txt.get_rect(center=(WIDTH // 2, 250)))

            if score >= highscore and score > 0:
                new_record = self.font_msg.render("¡NUEVO RECORD!", True, UI_ACCENT)
                self.surface.blit(new_record, new_record.get_rect(center=(WIDTH // 2, 300)))

            self.draw_button("Presiona ENTER para Reiniciar", 400, (255, 255, 255))
            self.draw_button("Presiona ESC para Menú", 450, (200, 200, 200))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "RESTART"
                    if event.key == pygame.K_ESCAPE:
                        return "MENU"
