import pygame
import random
from . import spritesheet

fistula_sprites = pygame.image.load("sprites/bosses/fistula.png")
fistula_spritesheet = spritesheet.SpriteSheet(fistula_sprites)

body_walking_sprites = pygame.image.load('sprites/enemies/bodyWalking.png')
gaper_head_sprites = pygame.image.load('sprites/enemies/gaperHead.png')
horf_sprites = pygame.image.load('sprites/enemies/horf.png')

body_walking_spritesheet = spritesheet.SpriteSheet(body_walking_sprites)
gaper_head_spritesheet = spritesheet.SpriteSheet(gaper_head_sprites)
horf_spritesheet = spritesheet.SpriteSheet(horf_sprites)

haunt_sprites = pygame.image.load("sprites/bosses/theHaunt.png")
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
        self.max_health = 10
        self.health = self.max_health
        self.cooldown_tracker = 0
        self.dead = False
        self.name = name
        self.stage = stage
        self.frame = 0
        self.body_frame = 0
        self.head_frame = 0
        self.row = 0
        self.frame_duration = 60
        self.shooting = False
        self.shooting_direction = None
        self.shooting_cooldown = 1000
        self.range = 20
        self.shot_speed = 1
        self.tear_size = 1
        self.last_update_time = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.last_hit = pygame.time.get_ticks()
        self.last_wobble_tick = pygame.time.get_ticks()
        self.last_body_animation = pygame.time.get_ticks()
        self.last_animation_frame = pygame.time.get_ticks()
        self.transformation = False
        self.invincible = False
        self.angle = 0
        self.hurt = False
        self.counter = 0
        self.flip = 1
        self.death_animation = False
        self.death_animation_duration = 0
        self.animation_backwards = 1
        self.spawned = False
        self.statsAssign()

        self.left_side = pygame.Rect(self.x, self.y+self.height//2-1, self.width//2, 2)
        self.right_side = pygame.Rect(self.x+self.width//2, self.y+self.height//2-1, self.width//2, 2)
        self.top_side = pygame.Rect(self.x+self.width//2-1, self.y, 2, self.height//2)
        self.bottom_side = pygame.Rect(self.x+self.width//2-1, self.y+self.height//2, 2, self.height//2)
        self.sides = [self.left_side, self.right_side, self.top_side, self.bottom_side]

    def draw(self, window):
        if self.type == "regular":
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

                self.angle -= 0.5
                if self.angle == 0:
                    self.angle = 360

                sprite = pygame.transform.scale(sprite, (self.width * 1.25, self.height * 1.25)).convert_alpha()
                sprite = pygame.transform.rotate(sprite, self.angle).convert_alpha()

            if self.name == "the haunt":
                sprite = haunt_spritesheet.get_image(self.frame, 84, 79, scale=3.5, row=self.row)
                if not self.stage == 2:
                    sprite = self.spriteWobble(sprite)
            
        if self.hurt or self.name == "horf" and self.frame != 0 and self.animation_backwards == 1:
            colour_image = pygame.Surface(sprite.get_size()).convert_alpha()
            colour_image.fill((255, 120, 120))
            sprite.blit(colour_image, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        
        window.blit(sprite, (self.x + self.width//2 - sprite.get_width()//2, self.y + self.height//2 - sprite.get_height()//2))
        
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height), 1)

    def update(self, character, map):
        self.sidesUpdate()
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

    def move(self, map, current_time, character):
        if self.type == "regular":
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

        if self.type == "boss":
            if self.name == "the haunt":
                if self.stage == 1:
                    self.boundaryBlock(map.walls)

                    random_int = random.randint(1, 100)
                    if random_int == 1:
                        self.direction_x *= -1

                    if random_int == 2:
                        self.direction_y *= -1

                    self.x += self.speed_x * self.direction_x
                    self.y += self.speed_y * self.direction_y

                else:
                    x_block, y_block = self.boundaryBlock(map.walls, mode="x")

                    if self.stage == 2:
                        self.y -= 4

                    if self.stage == 3:
                        if x_block:
                            self.direction_x *= -1

                        self.x += self.speed_x * self.direction_x

            if self.name == "fistula":
                x_block, y_block = self.boundaryBlock(map.walls)
                if x_block == True:
                    self.direction_x *= -1
                    self.speed_x = random.randint(1, 4)

                if y_block == True:
                    self.direction_y *= -1
                    self.speed_y = random.randint(1, 4)

                self.x += self.speed_x * self.direction_x
                self.y += self.speed_y * self.direction_y

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

    def statsAssign(self):
        if self.type == "boss":
            if self.name == "the haunt":
                self.width = 150
                self.height = 150
                self.speed_x = 1
                self.speed_y = 1
                self.max_health = 200
                self.health = self.max_health
                self.shot_speed = 2
                self.tear_size = 1.5
                self.shooting_cooldown = 5000
                self.death_animation_duration = 2000

            if self.name == "fistula":
                if self.stage == 1:
                    self.width = 200
                    self.height = 200
                    self.max_health = 60
                    self.health = self.max_health
                if self.stage == 2:
                    self.health = 15
                if self.stage == 3:
                    self.health = 8
                
                self.speed_x = 5

            self.x -= self.width//2
            self.y -= self.height//2
        
        if self.type == "regular":
            if self.name == "gaper":
                self.width = 32
                self.height = 32

            if self.name == "horf":
                self.width = 32*1.5
                self.height = 32*1.5

            else:
                self.width = 50
                self.height = 50

    def enemyBehaviour(self, current_time, map):
        if self.type == "boss":
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
                        map.current_room.enemies.append(Enemy(self.x - 25 + i*50, self.y, type="boss", name="fistula", width=self.width-100//self.stage, height=self.height-100//self.stage, stage=self.stage + 1))
                    self.spawned = True

        if self.type == "regular":
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