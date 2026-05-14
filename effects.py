import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 1.0  # Vida de 0 a 1
        self.decay = random.uniform(0.02, 0.05)
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        self.size = max(0, self.size - 0.1)

    def draw(self, surface):
        if self.life > 0:
            alpha = int(self.life * 255)
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
            surface.blit(s, (self.x - self.size, self.y - self.size))

class ParticleManager:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

class ScreenShake:
    def __init__(self):
        self.intensity = 0
        self.duration = 0

    def trigger(self, intensity, duration):
        self.intensity = intensity
        self.duration = duration

    def get_offset(self):
        if self.duration > 0:
            self.duration -= 1
            x = random.randint(-self.intensity, self.intensity)
            y = random.randint(-self.intensity, self.intensity)
            return x, y
        return 0, 0

class FloatingText:
    def __init__(self, x, y, text, color, font):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.life = 1.0
        self.vy = -1.0

    def update(self):
        self.y += self.vy
        self.life -= 0.02

    def draw(self, surface):
        if self.life > 0:
            alpha = int(self.life * 255)
            img = self.font.render(self.text, True, self.color)
            img.set_alpha(alpha)
            surface.blit(img, (self.x, self.y))
