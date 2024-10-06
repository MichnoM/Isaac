import pygame
import random

class Enemy(object):
    def __init__(self, x, y, width, height, type="regular"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.speed_x = 3
        self.speed_y = 3
        self.direction_x = 1
        self.direction_y = 1
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = 10
        self.cooldown_tracker = 0
        self.direction = random.randint(1, 4)
        self.dead = False

    def draw(self, window):
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def update(self, character, map):
        self.move(map.walls)
        if self.dead:
            map.current_room.enemies.pop(map.current_room.enemies.index(self))
        if not character.dead:
            if map.checkCollision(character, self):
                if not character.damage_taken_cooldown:
                    character.hit()

    def move(self, boundary):
        if self.type == "regular":
            if self.cooldown_tracker >= 1:
                self.cooldown_tracker += 1
            if self.cooldown_tracker == 10:
                self.cooldown_tracker = 0
            if self.x + self.width >= boundary[1].x or self.x <= boundary[0].x + boundary[0].width:
                if self.cooldown_tracker == 0:
                    self.direction_x *= -1
                    self.speed_x = random.randint(1, 4) * self.direction_x
                    self.cooldown_tracker = 1

            if self.y + self.height >= boundary[3].y or self.y <= boundary[2].y + boundary[2].height:
                if self.cooldown_tracker == 0:
                    self.direction_y *= -1
                    self.speed_y = random.randint(1, 4) * self.direction_y
                    self.cooldown_tracker = 1

            if self.direction == 1:
                self.x += 1 * self.speed_x
                self.y += 1 * self.speed_y
            elif self.direction == 2:
                self.x -= 1 * self.speed_x
                self.y -= 1 * self.speed_y
            elif self.direction == 3:
                self.x += 1 * self.speed_x
                self.y -= 1 * self.speed_y
            else:
                self.x -= 1 * self.speed_x
                self.y += 1 * self.speed_y

        if self.type == "boss":
            pass

    def hit(self, damage):
        if self.health > 0:
            self.health -= 1 * damage
            if self.health <= 0:
                self.dead = True
