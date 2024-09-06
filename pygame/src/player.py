import pygame
from . import spritesheet

isaac_sprites = pygame.image.load('sprites/Isaac.png')
isaac_spritesheet = spritesheet.SpriteSheet(isaac_sprites)
healthbar = pygame.image.load('sprites/HealthBar.png')
healthbar = pygame.transform.scale(healthbar, (360, 45))
healthbar_empty = pygame.image.load('sprites/HealthBarEmpty.png')
healthbar_empty = pygame.transform.scale(healthbar_empty, (360, 45))

custom_sprite = False

class Player(object):
    def __init__(self, x, y, width=56, height=66):
        self.health = 5
        self.max_health = 5
        self.speed = 15
        self.attack_speed = 5
        self.damage = 10
        self.size = 1
    
        self.x = x
        self.y = y
        self.width = width * self.size
        self.height = height * self.size
        self.stationary = True
        self.frame = 0
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collision = False
        self.dead = False

    def draw(self, window):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if not custom_sprite:
            sprite = isaac_spritesheet.get_image(self.frame, scale=self.size)
            window.blit(sprite, (self.x, self.y))
        else:
            self.frame = 4
            sprite = isaac_spritesheet.get_image(self.frame, scale=self.size)
            window.blit(sprite, (self.x, self.y))

    def drawHealthbar(self, window):
        window.blit(healthbar_empty, (-360 + 45 * self.max_health, 10))
        window.blit(healthbar, (-360 + 45 * self.health, 10))

    def hit(self):
        if self.health > 0:
            self.health -= 1
            self.frame = 4
            if self.health <= 0:
                self.dead = True
                self.frame = 5