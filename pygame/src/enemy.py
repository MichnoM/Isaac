import pygame
import random
from . import spritesheet

fistula_sprites = pygame.image.load("sprites/fistula.png")
fistula_spritesheet = spritesheet.SpriteSheet(fistula_sprites)

class Enemy:
    def __init__(self, x, y, type="regular", name=None, width=0, height=0, stage=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.speed_x = 3
        self.speed_y = 3
        self.direction_x = 1
        self.direction_y = 1
        self.health = 10
        self.cooldown_tracker = 0
        self.direction = random.randint(1, 4)
        self.dead = False
        self.name = name
        self.stage = stage
        self.statsAssign()

    def draw(self, window):
        if self.type == "regular":
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y, self.width, self.height))

        if self.type == "boss":
            if self.name == "fistula":
                if self.stage == 1:
                    frame = 0
                if self.stage == 2:
                    frame = 1
                if self.stage == 3:
                    frame = 2
                sprite = fistula_spritesheet.get_image(frame, 76, 70)

                if frame == 1:
                    sprite = sprite.subsurface(17, 14, 41, 44)
                if frame == 2:
                    sprite = sprite.subsurface(21, 19, 34, 31)

                sprite = pygame.transform.scale(sprite, (self.width, self.height)).convert_alpha()
                window.blit(sprite, (self.x, self.y))

            if self.name == "the haunt":
                pygame.draw.rect(window, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def update(self, character, map):
        self.move(map.walls)
        if self.dead:
            if self.name == "fistula":
                if self.stage == 1:
                    amount_of_splits = 4
                if self.stage == 2:
                    amount_of_splits = 2
                if self.stage == 3:
                    amount_of_splits = 0
                for i in range(amount_of_splits):
                    map.current_room.enemies.append(Enemy(self.x - 25 + i*50, self.y, type="boss", name="fistula", width=self.width-100//self.stage, height=self.height-100//self.stage, stage=self.stage + 1))

            map.current_room.enemies.remove(self)

        if not character.dead:
            if map.checkCollision(character, self):
                if not character.damage_taken_cooldown:
                    character.hit()

        if self.name == "the haunt":
            if self.health <= 100:
                if not self.stage == 2:
                    self.stage = 2
                    self.speed_x = 6


    def move(self, boundary):
        if self.type == "regular" or self.name == "fistula":
            if self.x + self.width >= boundary[1].x or self.x <= boundary[0].x + boundary[0].width:
                if self.x + self.width >= boundary[1].x:
                    self.x = boundary[1].x - self.width
                else:
                    self.x = boundary[0].x + boundary[0].width

                self.direction_x *= -1
                self.speed_x = random.randint(1, 4) * self.direction_x

            if self.y + self.height >= boundary[3].y or self.y <= boundary[2].y + boundary[2].height:
                if self.y + self.height >= boundary[3].y:
                    self.y = boundary[3].y - self.height
                else:
                    self.y = boundary[2].y + boundary[2].height

                self.direction_y *= -1
                self.speed_y = random.randint(1, 4) * self.direction_y

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
            if self.name == "the haunt":
                if self.stage == 1:
                    if self.x + self.width >= boundary[1].x or self.x <= boundary[0].x + boundary[0].width:
                        if self.x + self.width >= boundary[1].x:
                            self.x = boundary[1].x - self.width
                        else:
                            self.x = boundary[0].x + boundary[0].width

                        self.direction_x *= -1
                        self.speed_x = random.randint(1, 4) * self.direction_x

                    if self.y + self.height >= boundary[3].y or self.y <= boundary[2].y + boundary[2].height:
                        if self.y + self.height >= boundary[3].y:
                            self.y = boundary[3].y - self.height
                        else:
                            self.y = boundary[2].y + boundary[2].height

                        self.direction_y *= -1
                        self.speed_y = random.randint(1, 4) * self.direction_y

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

                else:
                    if self.y > 10:
                        self.y -= 4
                    else:
                        self.y = 10
                        if self.x + self.width >= boundary[1].x:
                            self.speed_x *= -1
                        if self.x <= boundary[0].x + boundary[0].width:
                            self.speed_x *= -1
                        self.x += 1 * self.speed_x

    def hit(self, damage):
        if self.health > 0:
            self.health -= 1 * damage
            if self.health <= 0:
                self.dead = True

    def statsAssign(self):
        if self.type == "boss":
            if self.name == "the haunt":
                self.width = 200
                self.height = 200
                self.speed_x = 3
                self.health = 200
            if self.name == "fistula":
                if self.stage == 1:
                    self.width = 250
                    self.height = 250
                self.speed_x = 5
                self.health == 22
            self.x -= self.width//2
            self.y -= self.height//2
        else:
            self.width = 50
            self.height = 50