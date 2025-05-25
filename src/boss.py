import pygame
import random
from . import enemy
from . import spritesheet
from .enemies import bosses

fistula_sprites = pygame.image.load("sprites/bosses/fistula.png")
fistula_spritesheet = spritesheet.SpriteSheet(fistula_sprites)

haunt_sprites = pygame.image.load("sprites/bosses/theHaunt.png")
haunt_spritesheet = spritesheet.SpriteSheet(haunt_sprites)

class Boss(enemy.Enemy):
    def __init__(self, x, y, name, width=50, height=50, stage=1):
        super().__init__(x, y)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stage = stage
        self.name = name
        self.type = "boss"
        
        self.sprite = None

        self.x -= self.width//2
        self.y -= self.height//2

        self.statsAssign()
        self.updateChild()

    def updateChild(self):
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

            self.angle -= 0.5
            if self.angle == 0:
                self.angle = 360

            sprite = pygame.transform.scale(sprite, (self.width * 1.25, self.height * 1.25)).convert_alpha()
            sprite = pygame.transform.rotate(sprite, self.angle).convert_alpha()

        if self.name == "the haunt":
            sprite = haunt_spritesheet.get_image(self.frame, 84, 79, scale=3.5, row=self.row)
            if not self.stage == 2:
                sprite = self.spriteWobble(sprite)

        self.sprite = sprite

    def move(self, map, current_time, character):
        if self.name == "the haunt":
            if self.stage == 1:
                self.boundaryBlock(map.walls)

                random_int = random.randint(1, 100)
                if random_int == 1:
                    self.direction_x *= -1

                if random_int == 2:
                    self.direction_y *= -1

                self.x += self.speed_x * self.direction_x * map.dt * map.dt_speed_constant
                self.y += self.speed_y * self.direction_y * map.dt * map.dt_speed_constant

            else:
                x_block, y_block = self.boundaryBlock(map.walls, mode="x")

                if self.stage == 2:
                    self.y -= 4

                if self.stage == 3:
                    if x_block:
                        self.direction_x *= -1

                    self.x += self.speed_x * self.direction_x * map.dt * map.dt_speed_constant

        if self.name == "fistula":
            x_block, y_block = self.boundaryBlock(map.walls)
            if x_block == True:
                self.direction_x *= -1
                self.speed_x = random.randint(2, 4)

            if y_block == True:
                self.direction_y *= -1
                self.speed_y = random.randint(2, 4)

            self.x += self.speed_x * self.direction_x * map.dt * map.dt_speed_constant
            self.y += self.speed_y * self.direction_y * map.dt * map.dt_speed_constant

    def enemyBehaviour(self, current_time, map):
        if self.name == "the haunt":
            self.shooting_direction = "down"
            if self.health <= 100:
                if self.stage == 1:
                    self.stage = 2
                    self.speed_x = 6

            if self.y < 10 and self.stage == 2:
                self.stage = 3
                self.y = 10

            if self.stage == 1:
                self.row = 0
                frames = [0, 1, 2]

            if self.stage == 2:
                self.transformation = True
                self.invincible = True
                self.row = 0
                frames = [3, 4]
                    
            if self.stage == 3:
                if self.row == 0:
                    self.row = 1
                    self.frame = 0
                frames = [0, 1, 2, 3, 4]
                if self.row == 3:
                    self.transformation = False
                    self.invincible = False
                    if not self.shooting:
                        frames = [0]
                    else:
                        frames = [1, 2, 3]

            if current_time - self.last_update_time >= self.frame_duration:
                if self.frame < frames[-1]:
                    self.frame += 1
                else:
                    if not self.shooting:
                        self.frame = frames[0]
                        if self.row == 1 or self.row == 2:
                            self.row += 1
                            if self.row == 2:
                                self.last_shot = current_time

                self.last_update_time = current_time

            if self.stage == 3:
                if current_time - self.last_shot >= self.shooting_cooldown and not self.transformation and not self.dead:
                    self.shoot(map, "down", 3)
                    self.last_shot = current_time
                    self.shooting_cooldown = random.randint(3000, 8000)

            if self.dead:
                self.row = 3
                self.frame = 4

        if self.name == "fistula":
            if self.dead and not self.spawned:
                if self.stage == 1:
                    amount_of_splits = 4
                if self.stage == 2:
                    amount_of_splits = 2
                if self.stage == 3:
                    amount_of_splits = 0
                for i in range(amount_of_splits):
                    map.current_room.enemies.append(Boss(self.x - 25 + i*50, self.y, name="fistula", width=self.width-100//self.stage, height=self.height-100//self.stage, stage=self.stage + 1))
                self.spawned = True


    def statsAssign(self):
        for i in bosses:
            if self.stage == 1:
                if self.name == i[0]:
                    for j, stat in enumerate(i[1]):
                        setattr(self, stat, i[2][j])