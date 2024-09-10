import pygame
from . import spritesheet

tear_sprites = pygame.image.load('sprites/Tear.png')
tear_spritesheet = spritesheet.SpriteSheet(tear_sprites)

class Projectile(object):
    def __init__(self, x, y, radius, colour, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.speed = 8
        self.direction = direction
        self.tear_sprite = tear_spritesheet.get_image(0, 130, 130, 0.2)
        self.width = self.radius * 2
        self.height = self.radius * 2

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)
        window.blit(self.tear_sprite, (self.x - round(self.tear_sprite.get_width()//2), self.y - round(self.tear_sprite.get_height()//2)))

    def move(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
    
    def delete(self, list):
        list.pop(list.index(self))