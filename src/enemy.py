import pygame
import random
from . import spritesheet

class Enemy:
    def __init__(self, x, y, name=None, width=0, height=0, stage=1):
        # General information
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.name = name
        self.stage = stage

        # Stats
        self.max_health = 10
        self.health = self.max_health
        self.speed_x = 3
        self.speed_y = 3
        self.direction = [-1, 1]
        self.direction_x = self.direction[random.randint(0, 1)]
        self.direction_y = self.direction[random.randint(0, 1)]
        self.range = 20
        self.shot_speed = 1
        self.tear_size = 1
        
        # State
        self.spawned = False
        self.dead = False
        self.transformation = False
        self.invincible = False
        self.hurt = False
        self.shooting = False
        self.shooting_direction = None

        # Sides hitbox
        self.left_side = pygame.Rect(self.x, self.y+self.height//2-1, self.width//2, 2)
        self.right_side = pygame.Rect(self.x+self.width//2, self.y+self.height//2-1, self.width//2, 2)
        self.top_side = pygame.Rect(self.x+self.width//2-1, self.y, 2, self.height//2)
        self.bottom_side = pygame.Rect(self.x+self.width//2-1, self.y+self.height//2, 2, self.height//2)
        self.sides = [self.left_side, self.right_side, self.top_side, self.bottom_side]

        # Cooldown tracking
        self.shooting_cooldown = 1000
        self.cooldown_tracker = 0
        self.counter = 0

        # Animation
        self.flip = 1
        self.death_animation = False
        self.death_animation_duration = 0
        self.animation_backwards = 1
        self.angle = 0
        self.frame_duration = 60
        self.frame = 0
        self.body_frame = 0
        self.head_frame = 0
        self.row = 0

        # Animation updates
        self.last_update_time = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.last_hit = pygame.time.get_ticks()
        self.last_wobble_tick = pygame.time.get_ticks()
        self.last_body_animation = pygame.time.get_ticks()
        self.last_animation_frame = pygame.time.get_ticks()

    def draw(self, window):
        if self.hurt:
            self.hurtSpriteOverlay(self.sprite)
        
        window.blit(self.sprite, (self.x + self.width//2 - self.sprite.get_width()//2, self.y + self.height//2 - self.sprite.get_height()//2))
        
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height), 1)

    def update(self, character, map):
        self.sidesUpdate()
        self.updateChild()
        current_time = pygame.time.get_ticks()
        if not self.dead:
            self.move(map, current_time, character)

        if self.dead:
            if not self.death_animation:
                map.current_room.enemies.remove(self)

        if not character.dead:
            if map.checkCollision(character, self):
                if not character.damage_taken_cooldown:
                    character.hit()

        if self.shooting and current_time - self.last_shot >= 500:
            self.shooting = False

        if self.hurt and current_time - self.last_hit >= 100:
            self.hurt = False
        
        if self.death_animation and current_time - self.last_hit >= self.death_animation_duration:
            self.death_animation = False

        self.enemyBehaviour(current_time, map)

    def shoot(self, map, direction, amount):
        map.createTears(direction, self, type="hostile", amount=amount)
        self.shooting = True

    def hit(self, damage):
        if not self.dead:
            self.hurt = True
            self.last_hit = pygame.time.get_ticks()
            if self.health > 0:
                self.health -= 1 * damage
                if self.health <= 0:
                    self.dead = True
                    self.death_animation = True

    def sidesUpdate(self):
        self.left_side = pygame.Rect(self.x, self.y+self.height//2-10, self.width//2, 20)
        self.right_side = pygame.Rect(self.x+self.width//2, self.y+self.height//2-10, self.width//2, 20)
        self.top_side = pygame.Rect(self.x+self.width//2-10, self.y, 20, self.height//2)
        self.bottom_side = pygame.Rect(self.x+self.width//2-10, self.y+self.height//2, 20, self.height//2)
        self.sides = [self.left_side, self.right_side, self.top_side, self.bottom_side]

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
    
    def spriteWobble(self, sprite):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_wobble_tick >= 50:
            self.counter += 1 * self.flip
            self.last_wobble_tick = current_time

            if self.counter >= 4 or self.counter <= 0:
                self.flip *= -1

        sprite = pygame.transform.scale(sprite, (sprite.get_width() + 10*self.counter/4, sprite.get_height() - 10*self.counter/4)).convert_alpha()

        return sprite
    
    def distanceCalculator(self, map, character):
        delta_x = (map.player_info[0] + map.player_info[2]//2) - (character.x + character.width//2)
        delta_y = (map.player_info[1] + map.player_info[3]//2) - (character.y + character.height//2)

        distance = (delta_x**2 + delta_y**2)**(1/2)

        return distance
    
    def enemyCollision(self, map, character):
        for enemy in map.current_room.enemies:
            if map.checkCollision(self.bottom_side, enemy.top_side):
                self.y -= self.speed_x
            if map.checkCollision(self.top_side, enemy.bottom_side):
                self.y += self.speed_x
            if map.checkCollision(self.left_side, enemy.right_side):
                self.x += self.speed_y
            if map.checkCollision(self.right_side, enemy.left_side):
                self.x -= self.speed_y

        if map.checkCollision(self.bottom_side, character.top_side):
                self.y -= self.speed_x
        if map.checkCollision(self.top_side, character.bottom_side):
            self.y += self.speed_x
        if map.checkCollision(self.left_side, character.right_side):
            self.x += self.speed_y
        if map.checkCollision(self.right_side, character.left_side):
            self.x -= self.speed_y

    def hurtSpriteOverlay(self, sprite):
        colour_image = pygame.Surface(sprite.get_size()).convert_alpha()
        colour_image.fill((255, 120, 120))
        sprite = sprite.blit(colour_image, (0,0), special_flags=pygame.BLEND_RGBA_MULT)