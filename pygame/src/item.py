import pygame
from settings import window_width, window_height
from . import map

class Item(object):
    def __init__(self, stats, values, x = window_width//2 - 25, y = window_height//2 - 25):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.stats = stats
        self.values = values
        self.hide = True
        self.used = False
        self.picked = False

    def __str__(self):
        return f"stats: {self.stats}, values: {self.values}"

    def draw(self, window):
        if not self.hide:
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def effect(self, character):
        if not self.used:
            for i, stat in enumerate(self.stats):
                if not (stat == "max_health" and character.max_health >= 8):
                    setattr(character, stat, getattr(character, stat) + self.values[i])
                    self.used = True

    def pickup(self, character):
        if not self.hide:
            if not character.pickup_item:
                character.pickup_item = True
                self.picked = True
                self.effect(character)

    def update(self, character, map):
        if not map.current_room.empty:
            self.hide = True
        else:
            self.hide = False

        if self.picked:
            self.x = character.x + character.width//2 - self.width//2
            self.y = character.y - character.height//2

        if self.used and not character.pickup_item:
            if self in map.current_room.items:
                map.current_room.items.remove(self)