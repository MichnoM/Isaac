import pygame
from . import spritesheet
from settings import window_width, window_height

isaac_walking_sprites = pygame.image.load('sprites/isaacWalking.png')
isaac_head_sprites = pygame.image.load('sprites/isaacHead.png')
isaac_hurt_sprites = pygame.image.load('sprites/isaacHurt.png')

isaac_hurt_spritesheet = spritesheet.SpriteSheet(isaac_hurt_sprites)
isaac_walking_spritesheet = spritesheet.SpriteSheet(isaac_walking_sprites)
isaac_head_spritesheet = spritesheet.SpriteSheet(isaac_head_sprites)

class Player:
    def __init__(self, x, y, width=32, height=32):
        self.health = 5
        self.max_health = 5
        self.speed = 5
        self.attack_speed = 2
        self.damage = 4
        self.range = 5
        self.luck = 0
        self.size = 2
        self.damage_multiplier = 1
        self.shot_speed = 1
        self.tear_size = 1
        self.tear_amount = 1

        self.x = x
        self.y = y
        self.width = width * self.size
        self.height = height * self.size
        self.x -= self.width//2
        self.y -= self.height//2
        self.previous_size = self.size

        self.bombs = 0
        self.keys = 0
        self.coins = 0

        self.items = []

        self.stationary = True
        self.body_frame = 0
        self.head_frame = 0
        self.collision = False
        self.dead = False
        self.hurt = False
        self.pickup_item = False
        self.pickup_pickup = False
        self.door_collision = False
        self.doorframe_collision = [False, False, False, False]

        self.shooting_cooldown = False
        self.damage_taken_cooldown = False

        self.head_animation_duration = 100
        self.body_animation_duration = 100
        self.hurt_animation_duration = 500
        self.pickup_item_duration = 1000
        self.pickup_pickup_duration = 500
        self.body_animation_cooldown = False
        self.head_animation = False

    def __str__(self):
        return f"max_health: {self.max_health}, health: {self.health}, speed: {self.speed}, attack_speed: {self.attack_speed}, damage: {self.damage}, range: {self.range}, luck: {self.luck}, size: {self.size}"

    def draw(self, window):
        if not (self.hurt or self.dead or self.pickup_item):
            body_sprite = isaac_walking_spritesheet.get_image(self.body_frame, 32, 32, scale=self.size)
            head_sprite = isaac_head_spritesheet.get_image(self.head_frame, 32, 32, scale=self.size)
            window.blit(body_sprite, (self.x + self.width//2 - body_sprite.get_width()//2, self.y + self.height//2 - body_sprite.get_height()//6))
            window.blit(head_sprite, (self.x + self.width//2 - head_sprite.get_width()//2, self.y - head_sprite.get_height()//10))

        else:
            if self.hurt:
                hurt_sprite = isaac_hurt_spritesheet.get_image(1, 36, 33, scale=self.size)

            if self.dead:
                hurt_sprite = isaac_hurt_spritesheet.get_image(2, 36, 33, scale=self.size)

            if self.pickup_item or self.pickup_pickup:
                hurt_sprite = isaac_hurt_spritesheet.get_image(3, 36, 33, scale=self.size)

            window.blit(hurt_sprite, (self.x, self.y))

        # pygame.draw.rect(window, (0, 0, 255), (self.x, self.y, self.width, self.height), 1)

    def update(self):
        self.left_side = pygame.Rect(self.x, self.y+self.height//2-1, self.width//2, 2)
        self.right_side = pygame.Rect(self.x+self.width//2, self.y+self.height//2-1, self.width//2, 2)
        self.top_side = pygame.Rect(self.x+self.width//2-1, self.y, 2, self.height//2)
        self.bottom_side = pygame.Rect(self.x+self.width//2-1, self.y+self.height//2, 2, self.height//2)
        self.sides = [self.left_side, self.right_side, self.top_side, self.bottom_side]
        
        self.door_collision = False
        self.doorframe_collision = [False, False, False, False]
        if self.stationary:
            if not self.head_animation:
                self.head_frame = 0
            self.body_frame = 0
        self.stationary = True

    def hit(self):
        if not self.damage_taken_cooldown:
            if self.health > 0:
                self.hurt = True
                self.hurt_interaction = True
                self.health -= 1
                if self.health <= 0:
                    self.dead = True
            self.damage_taken_cooldown = True

    def bodyAnimation(self, direction):
        if type(direction) == "tuple":
            if direction[0] == -1 and (direction[1] <= 1 or direction[0] >= -1):
                direction = "left"
            if direction[0] == 1 and (direction[1] <= 1 or direction[0] >= -1):
                direction = "right"
            if direction[1] == -1 and (direction[0] <= 1 or direction[0] >= -1):
                direction = "up"
            if direction[1] == 1 and (direction[0] <= 1 or direction[0] >= -1):
                direction = "down"
            

        if direction == "left":
            if self.body_frame <= 19:
                self.body_frame = 20
            if not self.body_animation_cooldown:
                self.body_frame += 1
                self.body_animation_cooldown = True
            if self.body_frame > 29:
                self.body_frame = 20

        if direction == "right":
            if self.body_frame <= 9:
                self.body_frame = 10
            if not self.body_animation_cooldown:
                self.body_frame += 1
                self.body_animation_cooldown = True
            if self.body_frame > 19:
                self.body_frame = 10

        if direction == "up" or direction == "down":
            if not self.body_animation_cooldown:
                self.body_frame += 1
                self.body_animation_cooldown = True
            if self.body_frame > 9:
                self.body_frame = 0

    def headAnimation(self, direction):
        if not self.head_animation:
            if direction == "left":
                self.head_frame = 6
            if direction == "right":
                self.head_frame = 2
            if direction == "up":
                self.head_frame = 4
            if direction == "down":
                self.head_frame = 0

    def walk(self, direction, map):
        self.stationary = False
        if direction == "left":
            if not map.checkCollision(self, map.left_wall) or (self.door_collision and not map.current_room.enemies):
                if not self.doorframe_collision[3]:
                    self.x -= self.speed
                if map.checkCollision(self, map.left_wall) and not (self.door_collision and not map.current_room.enemies):
                    self.x = map.left_wall.x + map.left_wall.width

        if direction == "right":
            if not map.checkCollision(self, map.right_wall) or (self.door_collision and not map.current_room.enemies):
                if not self.doorframe_collision[1]:
                    self.x += self.speed
                if map.checkCollision(self, map.right_wall) and not (self.door_collision and not map.current_room.enemies):
                    self.x = map.right_wall.x - self.width

        if direction == "up":
            if not map.checkCollision(self, map.upper_wall) or (self.door_collision and not map.current_room.enemies):
                if not self.doorframe_collision[0]:
                    self.y -= self.speed
                if map.checkCollision(self, map.upper_wall) and not (self.door_collision and not map.current_room.enemies):
                    self.y = map.upper_wall.y + map.upper_wall.height

        if direction == "down":
            if not map.checkCollision(self, map.bottom_wall) or (self.door_collision and not map.current_room.enemies):
                if not self.doorframe_collision[2]:
                    self.y += self.speed
                if map.checkCollision(self, map.bottom_wall) and not (self.door_collision and not map.current_room.enemies):
                    self.y = map.bottom_wall.y - self.height

    def shoot(self, direction, map):
        self.headAnimation(direction)
        self.shootingAnimation(direction)
        if not self.shooting_cooldown:
            map.createTears(direction, self, amount=self.tear_amount)
            self.shooting_cooldown = True

    def shootingAnimation(self, direction):
        if not self.shooting_cooldown:
            if direction == "left":
                self.head_frame = 7
            if direction == "right":
                self.head_frame = 3
            if direction == "up":
                self.head_frame = 5
            if direction == "down":
                self.head_frame = 1
            self.head_animation = True

    def doorframeCollision(self, room):
        self.door_collision = True
        for door in room.doors:
            if door.localisation == 1 or door.localisation == 3:
                if self.y < 40 or self.y + self.height > window_height - 40:
                    if self.x < door.x:
                        self.doorframe_collision[3] = True
                    if self.x + self.width > door.x + door.width:
                        self.doorframe_collision[1] = True

            if door.localisation == 2 or door.localisation == 4: 
                if self.x < 40 or self.x + self.width > window_width - 40:
                    if self.y < door.y:
                        self.doorframe_collision[0] = True
                    if self.y + self.height > door.y + door.height:
                        self.doorframe_collision[2] = True