import pygame
from . import enemy
from . import spritesheet
from .enemies import regulars

body_walking_sprites = pygame.image.load('sprites/enemies/bodyWalking.png')
gaper_head_sprites = pygame.image.load('sprites/enemies/gaperHead.png')
horf_sprites = pygame.image.load('sprites/enemies/horf.png')

body_walking_spritesheet = spritesheet.SpriteSheet(body_walking_sprites)
gaper_head_spritesheet = spritesheet.SpriteSheet(gaper_head_sprites)
horf_spritesheet = spritesheet.SpriteSheet(horf_sprites)

class Regular(enemy.Enemy):
    def __init__(self, x, y, name):
        super().__init__(x, y)

        self.name = name
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.type = "regular"

        self.sprite = None

        self.statsAssign()
        self.updateChild()

    def updateChild(self):
        if self.name == "gaper":
            scale = 2
            sprite = pygame.Surface((32*scale, 32*scale), pygame.SRCALPHA)
            body_sprite = body_walking_spritesheet.get_image(self.body_frame, 32, 32, scale=2)
            head_sprite = gaper_head_spritesheet.get_image(1, 32, 32, scale=scale)
            sprite.blit(body_sprite, (0,body_sprite.get_height()//3))
            sprite.blit(head_sprite, (0,-head_sprite.get_height()//8))

        if self.name == "horf":
            scale = 2.5
            sprite = horf_spritesheet.get_image(self.frame, 32, 32, scale=scale)
            if self.frame != 0 and self.animation_backwards == 1:
                self.hurtSpriteOverlay(sprite)

        self.sprite = sprite

    def move(self, map, current_time, character):
        self.enemyCollision(map, character)
        if self.name == "gaper":
            self.speed_x = 3
            self.speed_y = 3
            x_block, y_block = self.boundaryBlock(map.walls)
            delta_x = (map.player_info[0] + map.player_info[2]//2) - (self.x + self.width//2)
            delta_y = (map.player_info[1] + map.player_info[3]//2) - (self.y + self.height//2)

            distance = (delta_x**2 + delta_y**2)**(0.5)

            if distance != 0:
                self.direction_x = delta_x / distance
                self.direction_y = delta_y / distance
            else:
                self.direction_x = 0
                self.direction_y = 0

            self.x += self.speed_x * self.direction_x
            self.y += self.speed_y * self.direction_y

        if self.name == "horf":
            if not self.shooting:
                if current_time - self.last_wobble_tick >= 40:
                    self.counter += 1
                    self.last_wobble_tick = current_time

                    if self.counter >= 4 or self.counter <= 0:
                        self.flip *= -1
                
                self.x += 2 * self.flip

    def enemyBehaviour(self, current_time, map):
        if self.name == "gaper":
            if abs(self.direction_x) > abs(self.direction_y):
                if self.direction_x < 0:
                    direction = "left"
                if self.direction_x > 0:
                    direction = "right"

            else:
                if self.direction_y > 0:
                    direction = "down"
                if self.direction_y < 0:
                    direction = "up"

            if self.direction_x == 0 and self.direction_y == 0:
                direction = "down"

            self.bodyAnimation(direction, current_time)

        if self.name == "horf":
            if current_time - self.last_shot >= self.shooting_cooldown:
                distance = self.distanceCalculator(map, self)
                if distance <= 400:
                    self.shoot(map, "player", 1)
                    self.last_shot = current_time

            if not self.shooting:
                frames = [0]
                self.animation_backwards = 1
            else:
                frames = [1, 2, 3]

            if current_time - self.last_animation_frame >= self.frame_duration:
                if self.frame == frames[-1] and self.frame != 0:
                    self.animation_backwards *= -1
                    self.frame -= 1
                    
                if self.frame < frames[-1]:
                    self.frame += 1 * self.animation_backwards
                    if self.frame < 0:
                        self.frame = 0

                self.last_animation_frame = current_time

    def bodyAnimation(self, direction, current_time):
        if current_time - self.last_body_animation > 100:
            self.body_frame += 1
            self.last_body_animation = current_time

        if direction == "left":
            if self.body_frame <= 19:
                self.body_frame = 20

            if self.body_frame > 29:
                self.body_frame = 20

        if direction == "right":
            if self.body_frame <= 9:
                self.body_frame = 10

            if self.body_frame > 19:
                self.body_frame = 10

        if direction == "up" or direction == "down":
            if self.body_frame > 9:
                self.body_frame = 0

    def statsAssign(self):
        for i in regulars:
            if self.name == i[0]:
                for j, stat in enumerate(i[1]):
                    setattr(self, stat, i[2][j])