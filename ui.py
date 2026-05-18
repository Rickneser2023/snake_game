import pygame
from settings import WIDTH, TEXT_COLOR, UI_ACCENT, get_font

class UI:
    @staticmethod
    def draw_hud(surface, score, highscore, level, is_ghost=False, ghost_timer=0, is_slow=False, slow_timer=0):
        font_small = get_font(22)
        font_label = get_font(14)
        
        # Fondo del HUD con gradiente sutil
        hud_height = 50
        for i in range(hud_height):
            alpha = int(200 * (1 - i/hud_height))
            s = pygame.Surface((WIDTH, 1))
            s.set_alpha(alpha)
            s.fill((0, 0, 0))
            surface.blit(s, (0, i))

        # Renderizar textos
        def draw_stat(x, label, value, color):
            lbl_img = font_label.render(label, True, (150, 150, 150))
            val_img = font_small.render(str(value), True, color)
            surface.blit(lbl_img, (x, 5))
            surface.blit(val_img, (x, 20))

        draw_stat(30, "PUNTOS", score, TEXT_COLOR)
        draw_stat(WIDTH // 2 - 40, "NIVEL", level, UI_ACCENT)
        draw_stat(WIDTH - 150, "RECORD", highscore, TEXT_COLOR)

        # Línea decorativa inferior
        pygame.draw.line(surface, UI_ACCENT, (0, hud_height), (WIDTH, hud_height), 1)

        # Efectos activos
        y_pos = hud_height + 10
        if is_ghost:
            ghost_txt = font_small.render(f"FANTASMA: {ghost_timer//60}s", True, (147, 112, 219))
            surface.blit(ghost_txt, (10, y_pos))
            y_pos += 25
        if is_slow:
            slow_txt = font_small.render(f"TIEMPO LENTO: {slow_timer//60}s", True, (0, 255, 255))
            surface.blit(slow_txt, (10, y_pos))

    @staticmethod
    def draw_pause(surface):
        overlay = pygame.Surface((WIDTH, 600))
        overlay.set_alpha(160)
        overlay.fill((10, 10, 20))
        surface.blit(overlay, (0, 0))
        
        font_big = get_font(80)
        txt = font_big.render("PAUSA", True, UI_ACCENT)
        # Sombra
        shadow = font_big.render("PAUSA", True, (0, 0, 0))
        
        rect = txt.get_rect(center=(WIDTH//2, 300))
        surface.blit(shadow, (rect.x + 4, rect.y + 4))
        surface.blit(txt, rect)
        
        font_msg = get_font(24)
        msg = font_msg.render("Presiona 'P' para continuar", True, (200, 200, 200))
        msg_rect = msg.get_rect(center=(WIDTH//2, 380))
        surface.blit(msg, msg_rect)
