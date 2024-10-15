import pygame
import random
from . import spritesheet

fistula_sprites = pygame.image.load("sprites/fistula.png")
fistula_spritesheet = spritesheet.SpriteSheet(fistula_sprites)

haunt_sprites = pygame.image.load("sprites/the haunt.png")
haunt_spritesheet = spritesheet.SpriteSheet(haunt_sprites)

class Enemy:
    def __init__(self, x, y, type="regular", name=None, width=0, height=0, stage=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.speed_x = 3
        self.speed_y = 3
        self.direction = [-1, 1]
        self.direction_x = self.direction[random.randint(0, 1)]
        self.direction_y = self.direction[random.randint(0, 1)]
        self.health = 10
        self.cooldown_tracker = 0
        self.dead = False
        self.name = name
        self.stage = stage
        self.frame = 0
        self.row = 0
        self.frame_duration = 60
        self.shooting = False
        self.last_update_time = pygame.time.get_ticks()
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

            if self.name == "the haunt":
                sprite = haunt_spritesheet.get_image(self.frame, 84, 79, scale=3, row=self.row)
            
            window.blit(sprite, (self.x + self.width//2 - sprite.get_width()//2, self.y + self.height//2 - sprite.get_height()//2))
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height), 1)

    def update(self, character, map):
        current_time = pygame.time.get_ticks()
        self.move(map.walls)
        if self.dead:
            map.current_room.enemies.remove(self)

        if not character.dead:
            if map.checkCollision(character, self):
                if not character.damage_taken_cooldown:
                    character.hit()

        self.bossBehaviour(current_time, map)

    def move(self, boundary):
        if self.type == "regular" or self.name == "fistula":
            x_block, y_block = self.boundaryBlock(boundary)
            if x_block == True:
                self.direction_x *= -1
                self.speed_x = random.randint(1, 4)

            if y_block == True:
                self.direction_y *= -1
                self.speed_y = random.randint(1, 4)

            self.x += self.speed_x * self.direction_x
            self.y += self.speed_y * self.direction_y

        if self.type == "boss":
            if self.name == "the haunt":
                if self.stage == 1:
                    self.boundaryBlock(boundary)

                    random_int = random.randint(1, 100)
                    if random_int == 1:
                        self.direction_x *= -1

                    if random_int == 2:
                        self.direction_y *= -1

                    self.x += self.speed_x * self.direction_x
                    self.y += self.speed_y * self.direction_y

                else:
                    x_block, y_block = self.boundaryBlock(boundary, mode="x")
                    if self.y > 10:
                        self.stage = 2
                        self.y -= 4
                    else:
                        self.stage = 3
                        self.y = 10
                        if x_block:
                            self.direction_x *= -1

                        self.x += self.speed_x * self.direction_x

    def boundaryBlock(self, boundary, mode=None):
        x = False
        y = False
        if mode == "x" or mode == None:
            if self.x + self.width >= boundary[1].x or self.x <= boundary[0].x + boundary[0].width:
                if self.x + self.width >= boundary[1].x:
                    self.x = boundary[1].x - self.width
                else:
                    self.x = boundary[0].x + boundary[0].width

                x = True
        if mode == "y" or mode == None:
            if self.y + self.height >= boundary[3].y or self.y <= boundary[2].y + boundary[2].height:
                if self.y + self.height >= boundary[3].y:
                    self.y = boundary[3].y - self.height
                else:
                    self.y = boundary[2].y + boundary[2].height

                y = True

        return x, y

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
                self.speed_x = 1
                self.speed_y = 1
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

    def bossBehaviour(self, current_time, map):
        if self.name == "the haunt":
            if self.health <= 100:
                if self.stage == 1:
                    self.stage = 2
                    self.speed_x = 6

            if self.stage == 1:
                self.row = 0
                frames = [0, 1, 2]

            if self.stage == 2:
                self.row = 0
                frames = [3, 4]
                    
            if self.stage == 3:
                if self.row == 0:
                    self.row = 1
                    self.frame = 0
                frames = [0, 1, 2, 3, 4]
                if self.row == 3:
                    frames = [0]

            if current_time - self.last_update_time >= self.frame_duration:
                if self.frame < frames[-1]:
                    self.frame += 1
                else:
                    self.frame = frames[0]
                    if self.row == 1 or self.row == 2:
                        self.row += 1

                self.last_update_time = current_time

        if self.name == "fistula":
            if self.dead:
                if self.stage == 1:
                    amount_of_splits = 4
                if self.stage == 2:
                    amount_of_splits = 2
                if self.stage == 3:
                    amount_of_splits = 0
                for i in range(amount_of_splits):
                    map.current_room.enemies.append(Enemy(self.x - 25 + i*50, self.y, type="boss", name="fistula", width=self.width-100//self.stage, height=self.height-100//self.stage, stage=self.stage + 1))