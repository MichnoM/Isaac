import pygame
from . import spritesheet

tear_sprites = pygame.image.load('sprites/tear.png')

tear_spritesheet = spritesheet.SpriteSheet(tear_sprites)

class Projectile:
    def __init__(self, x, y, radius, colour, direction, type="friendly", character=None):
        self.x = x
        self.y = y
        self.starting_x = x
        self.starting_y = y
        self.radius = radius
        self.colour = colour
        self.speed = 8
        self.direction = direction
        self.width = self.radius * 2
        self.height = self.radius * 2
        self.distance_travelled = 0
        self.pop = False
        self.check = 0
        self.did_hit = False
        self.updated = False
        self.type = type
        self.character = character
        self.size = character.tear_size
        self.directionConverter(self.direction)

    def draw(self, window):
        if self.type == "friendly":
            sprite = tear_spritesheet.get_image(0, 130, 130, 0.2*self.size)
        else:
            sprite = tear_spritesheet.get_image(1, 130, 130, 0.2*self.size)
        
        window.blit(sprite, (self.x - round(sprite.get_width()//2), self.y - round(sprite.get_height()//2)))

    def update(self, character, map):
        if not self.updated:
            self.speed *= self.character.shot_speed
            self.updated = True
        self.move(self.character.range)
        if map.checkCollision(self, map.walls):
            self.pop = True
        if self.pop:
            for room in map.rooms:
                if self in room.tears:
                    room.tears.remove(self)
        for enemy in map.current_room.enemies:
            if map.checkCollision(self, enemy) and self.type == "friendly" and not enemy.invincible:
                if not self.did_hit:
                    self.did_hit = True
                    self.pop = True
                    enemy.hit(self.character.damage)

        if map.checkCollision(self, character) and self.type == "hostile":
            if not self.did_hit:
                self.did_hit = True
                self.pop = True
                character.hit()
                
    def move(self, projectile_range):
        if self.distance_travelled < projectile_range*50:
            self.x += self.speed * self.direction[0]
            self.y += self.speed * self.direction[1]
            self.distance_travelled += self.speed
        else:
            if self.check < 5:
                if self.direction[1] < 0:
                    self.y -= self.speed
                elif self.direction[1] > 0:
                    self.y += self.speed
                elif self.direction[0] < 0:
                    self.x -= self.speed
                    self.y += 2*self.check
                elif self.direction[0] > 0:
                    self.x += self.speed
                    self.y += 2*self.check
                self.check += 1
            else:
                self.pop = True

    def directionConverter(self, direction):
        if direction == "up":
            self.direction = [0, -1]
        if direction == "down":
            self.direction = [0, 1]
        if direction == "left":
            self.direction = [-1, 0]
        if direction == "right":
            self.direction = [1, 0]