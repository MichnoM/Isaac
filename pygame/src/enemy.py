import pygame
import random

class Enemy(object):
    def __init__(self, x, y, width, height, movement_boundary):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_x = 3
        self.speed_y = 3
        self.direction_x = 1
        self.direction_y = 1
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = 10
        self.cooldown_tracker = 0
        self.direction = random.randint(1, 4)
        self.dead = False
        self.movement_boundary = movement_boundary

    def draw(self, window):
        self.move()
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def move(self):
        if self.cooldown_tracker >= 1:
            self.cooldown_tracker += 1
        if self.cooldown_tracker == 10:
            self.cooldown_tracker = 0
        if self.x + self.width >= self.movement_boundary[1].x or self.x <= self.movement_boundary[0].x + self.movement_boundary[0].width:
            if self.cooldown_tracker == 0:
                self.direction_x *= -1
                self.speed_x = random.randint(1, 4) * self.direction_x
                self.cooldown_tracker = 1

        if self.y + self.height >= self.movement_boundary[3].y or self.y <= self.movement_boundary[2].y + self.movement_boundary[2].height:
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

    def hit(self, damage):
        if self.health > 0:
            self.health -= 1 * damage
            if self.health <= 0:
                self.dead = True