import pygame
from settings import WIDTH, TEXT_COLOR, UI_ACCENT, get_font

class UI:
    @staticmethod
    def draw_hud(surface, score, highscore, level):
        font_small = get_font(24)
        
        # Fondo del HUD (barra superior semi-transparente)
        hud_bar = pygame.Surface((WIDTH, 40))
        hud_bar.set_alpha(150)
        hud_bar.fill((0, 0, 0))
        surface.blit(hud_bar, (0, 0))

        score_txt = font_small.render(f"Puntos: {score}", True, TEXT_COLOR)
        level_txt = font_small.render(f"Nivel: {level}", True, UI_ACCENT)
        high_txt = font_small.render(f"Record: {highscore}", True, TEXT_COLOR)

        surface.blit(score_txt, (20, 7))
        surface.blit(level_txt, (WIDTH // 2 - 50, 7))
        surface.blit(high_txt, (WIDTH - 200, 7))

    @staticmethod
    def draw_pause(surface):
        overlay = pygame.Surface((WIDTH, 600))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        font_big = get_font(72)
        txt = font_big.render("PAUSA", True, (255, 255, 255))
        rect = txt.get_rect(center=(WIDTH//2, 300))
        surface.blit(txt, rect)
