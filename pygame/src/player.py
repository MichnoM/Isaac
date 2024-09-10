import pygame
from . import spritesheet

isaac_walking_sprites = pygame.image.load('sprites/isaacWalking.png')
isaac_head_sprites = pygame.image.load('sprites/isaacHead.png')
isaac_hurt_sprites = pygame.image.load('sprites/isaacHurt.png')
isaac_hurt_spritesheet = spritesheet.SpriteSheet(isaac_hurt_sprites)
isaac_walking_spritesheet = spritesheet.SpriteSheet(isaac_walking_sprites)
isaac_head_spritesheet = spritesheet.SpriteSheet(isaac_head_sprites)
healthbar = pygame.image.load('sprites/HealthBar.png')
healthbar = pygame.transform.scale(healthbar, (360, 45))
healthbar_empty = pygame.image.load('sprites/HealthBarEmpty.png')
healthbar_empty = pygame.transform.scale(healthbar_empty, (360, 45))

custom_sprite = False

class Player(object):
    def __init__(self, x, y, width=30, height=36):
        self.health = 5
        self.max_health = 5
        self.speed = 5
        self.attack_speed = 2
        self.damage = 2
        self.size = 2
    
        self.x = x
        self.y = y
        self.width = width * self.size
        self.height = height * self.size
        self.center_x = self.x + self.width//2
        self.center_y = self.y + self.height//2
        self.stationary = True
        self.body_frame = 0
        self.head_frame = 0
        self.collision = False
        self.dead = False
        self.hurt = False
        self.x -= self.width//2
        self.y -= self.height//2

        self.head_animation_duration = 200
        self.body_animation_duration = 100
        self.hurt_animation_duration = 500

    def draw(self, window):
        if not (self.hurt or self.dead):
            body_sprite = isaac_walking_spritesheet.get_image(self.body_frame, 20, 15, scale=self.size)
            head_sprite = isaac_head_spritesheet.get_image(self.head_frame, 30, 27, scale=self.size)
            window.blit(body_sprite, (self.x + self.width//2 - body_sprite.get_width()//2, self.y + head_sprite.get_height() - body_sprite.get_height()//2))
            window.blit(head_sprite, (self.x, self.y))

        else:
            if self.hurt:
                hurt_sprite = isaac_hurt_spritesheet.get_image(1, 36, 33, scale=self.size)
            else:
                hurt_sprite = isaac_hurt_spritesheet.get_image(2, 36, 33, scale=self.size)
            window.blit(hurt_sprite, (self.x, self.y))

    def drawHealthbar(self, window):
        window.blit(healthbar_empty, (-360 + 45 * self.max_health, 10))
        window.blit(healthbar, (-360 + 45 * self.health, 10))

    def hit(self):
        if self.health > 0:
            self.hurt = True
            self.health -= 1
            if self.health <= 0:
                self.dead = True
