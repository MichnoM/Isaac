import pygame
from settings import window_width, window_height

class Item(object):
    def __init__(self, stats, values, x = window_width//2 - 25, y = window_height//2 - 25):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.stats = stats
        self.values = values
        self.hide = False

    def __str__(self):
        return f"stats: {self.stats}, values: {self.values}"

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def effect(self, character):
        if not self.hide:
            for i, stat in enumerate(self.stats):
                if not (stat == "max_health" and character.max_health >= 8):
                    setattr(character, stat, getattr(character, stat) + self.values[i])