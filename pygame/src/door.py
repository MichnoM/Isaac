import pygame
from . import spritesheet

door_sprites = pygame.image.load('sprites/Doors.png')
door_spritesheet = spritesheet.SpriteSheet(door_sprites)
treasure_door = pygame.image.load("sprites/TreasureDoors.png")
treasure_door = pygame.transform.scale(treasure_door, (51*2, 40*2))
boss_door = pygame.image.load("sprites/BossDoors.png")
boss_door_spritesheet = spritesheet.SpriteSheet(boss_door)

class Door(object):
    def __init__(self, x, y, width, height, localisation):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.localisation = localisation
        self.closed = False
        self.closing = False
        self.opening = False
        self.cooldown = 0
        self.cooldown2 = 0
        self.frame = 0
        self.frame2 = 0
        self.is_treasure = False
        self.is_boss = False

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, localisation: {self.localisation}"

    def draw(self, window):
        if self.cooldown >= 1:
            self.cooldown += 1
        if self.cooldown >= 6 and self.cooldown <= 20:
            self.cooldown = 0
        if self.cooldown == 0:
            self.frame += 1
            self.cooldown = 1
        if self.frame + 1 >= 13:
            self.cooldown = 30

        if self.cooldown2 >= 1:
            self.cooldown2 += 1
        if self.cooldown2 >= 6 and self.cooldown2 <= 20:
            self.cooldown2 = 0
        if self.cooldown2 == 0:
            self.frame2 += 1
            self.cooldown2 = 1
        if self.frame2 + 1 >= 11:
            self.cooldown2 = 30
            
        if self.localisation == 1:
            if self.is_boss:
                sprite3 = boss_door_spritesheet.get_image(self.frame2, 63, 41, 2)
                window.blit(sprite3, (self.x - self.width//2 - 12, self.y - 12))
            else:
                sprite = door_spritesheet.get_image(self.frame, 51, 35, 2)
                window.blit(sprite, (self.x - self.width//2, self.y))
                if self.is_treasure:
                    sprite2 = treasure_door
                    window.blit(sprite2, (self.x - self.width//2, self.y - 10))

        if self.localisation == 2:
            if self.is_boss:
                sprite3 = boss_door_spritesheet.get_image(self.frame2, 63, 41, 2, rotation_angle = 270)
                window.blit(sprite3, (self.x, self.y - self.height//2 - 12))
            else:
                sprite = door_spritesheet.get_image(self.frame, 51, 35, 2, rotation_angle = 270)
                window.blit(sprite, (self.x, self.y - self.height//2))
                if self.is_treasure:
                    sprite2 = treasure_door
                    sprite2 = pygame.transform.rotate(sprite2, 270)
                    window.blit(sprite2, (self.x, self.y - self.height//2))

        if self.localisation == 3:
            if self.is_boss:
                sprite3 = boss_door_spritesheet.get_image(self.frame2, 63, 41, 2, rotation_angle = 180)
                window.blit(sprite3, (self.x - self.width//2 - 12, self.y))
            else:
                sprite = door_spritesheet.get_image(self.frame, 51, 35, 2, rotation_angle = 180)
                window.blit(sprite, (self.x - self.width//2, self.y))
                if self.is_treasure:
                    sprite2 = treasure_door
                    sprite2 = pygame.transform.rotate(sprite2, 180)
                    window.blit(sprite2, (self.x - self.width//2, self.y))

        if self.localisation == 4:
            if self.is_boss:
                sprite3 = boss_door_spritesheet.get_image(self.frame2, 63, 41, 2, rotation_angle = 90)
                window.blit(sprite3, (self.x - 12, self.y - self.height//2 - 12))
            else:
                sprite = door_spritesheet.get_image(self.frame, 51, 35, 2, rotation_angle = 90)
                window.blit(sprite, (self.x - 3, self.y - self.height//2))
                if self.is_treasure:
                    sprite2 = treasure_door
                    sprite2 = pygame.transform.rotate(sprite2, 90)
                    window.blit(sprite2, (self.x - 12, self.y - self.height//2))