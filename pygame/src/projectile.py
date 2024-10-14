import pygame
from . import spritesheet

tear_sprites = pygame.image.load('sprites/Tear.png')

tear_spritesheet = spritesheet.SpriteSheet(tear_sprites)

class Projectile:
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
        self.distance_travelled = 0
        self.pop = False
        self.check = 0
        self.did_hit = False

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)
        window.blit(self.tear_sprite, (self.x - round(self.tear_sprite.get_width()//2), self.y - round(self.tear_sprite.get_height()//2)))

    def update(self, character, map):
        self.move(character.range)
        if map.checkCollision(self, map.walls):
            self.pop = True
        if self.pop:
            for room in map.rooms:
                if self in room.tears:
                    room.tears.remove(self)
        for enemy in map.current_room.enemies:
            if map.checkCollision(self, enemy):
                if not self.did_hit:
                    self.did_hit = True
                    self.pop = True
                    enemy.hit(character.damage)
                
    def move(self, projectile_range):
        if self.distance_travelled < projectile_range*10:
            if self.direction == "up":
                self.y -= self.speed
            elif self.direction == "down":
                self.y += self.speed
            elif self.direction == "left":
                self.x -= self.speed
            elif self.direction == "right":
                self.x += self.speed
            self.distance_travelled += 1
        else:
            if self.check < 5:
                if self.direction == "up":
                    self.y -= self.speed
                elif self.direction == "down":
                    self.y += self.speed
                elif self.direction == "left":
                    self.x -= self.speed
                    self.y += 2*self.check
                elif self.direction == "right":
                    self.x += self.speed
                    self.y += 2*self.check
                self.check += 1
            else:
                self.pop = True

