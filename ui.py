import pygame
from settings import WIDTH, HEIGHT, TEXT_COLOR, UI_ACCENT, HUD_HEIGHT, COMBO_WINDOW_FRAMES, get_font

class UI:
    @staticmethod
    def draw_hud(surface, score, highscore, level, combo=0, combo_timer=0,
                 is_ghost=False, ghost_timer=0, is_slow=False, slow_timer=0):
        sw = surface.get_width()
        font_small = get_font(22)
        font_label = get_font(14)
        
        # Fondo del HUD con gradiente sutil
        for i in range(HUD_HEIGHT):
            alpha = int(210 * (1 - i / HUD_HEIGHT))
            s = pygame.Surface((sw, 1))
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
        draw_stat(sw // 2 - 35, "NIVEL", level, UI_ACCENT)
        draw_stat(sw - 150, "RECORD", highscore, TEXT_COLOR)

        # Línea decorativa inferior
        pygame.draw.line(surface, UI_ACCENT, (0, HUD_HEIGHT), (sw, HUD_HEIGHT), 1)

        if combo > 1 and combo_timer > 0:
            combo_txt = font_small.render(f"COMBO x{combo}", True, (255, 180, 80))
            surface.blit(combo_txt, (sw // 2 - combo_txt.get_width() // 2, 34))
            bar_w = 140
            bar_h = 6
            ratio = max(combo_timer / COMBO_WINDOW_FRAMES, 0)
            bar_x = sw // 2 - bar_w // 2
            bar_y = 54
            pygame.draw.rect(surface, (40, 40, 55), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
            pygame.draw.rect(surface, (255, 180, 80), (bar_x, bar_y, int(bar_w * ratio), bar_h), border_radius=3)

        # Efectos activos
        y_pos = 34
        if is_ghost:
            ghost_txt = font_small.render(f"FANTASMA: {ghost_timer//60}s", True, (147, 112, 219))
            surface.blit(ghost_txt, (10, y_pos))
            y_pos += 22
        if is_slow:
            slow_txt = font_small.render(f"TIEMPO LENTO: {slow_timer//60}s", True, (0, 255, 255))
            surface.blit(slow_txt, (10, y_pos))

    @staticmethod
    def draw_pause(surface):
        overlay = pygame.Surface(surface.get_size())
        overlay.set_alpha(160)
        overlay.fill((10, 10, 20))
        surface.blit(overlay, (0, 0))
        
        font_big = get_font(80)
        txt = font_big.render("PAUSA", True, UI_ACCENT)
        # Sombra
        shadow = font_big.render("PAUSA", True, (0, 0, 0))
        
        rect = txt.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 20))
        surface.blit(shadow, (rect.x + 4, rect.y + 4))
        surface.blit(txt, rect)
        
        font_msg = get_font(24)
        msg = font_msg.render("Presiona 'P' para continuar", True, (200, 200, 200))
        msg_rect = msg.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 50))
        surface.blit(msg, msg_rect)
