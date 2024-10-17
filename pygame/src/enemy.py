import pygame
import random
from . import spritesheet

fistula_sprites = pygame.image.load("sprites/fistula.png")
fistula_spritesheet = spritesheet.SpriteSheet(fistula_sprites)

body_walking_sprites = pygame.image.load('sprites/isaacWalking.png')
gaper_head_sprites = pygame.image.load('sprites/gaperHead.png')

body_walking_spritesheet = spritesheet.SpriteSheet(body_walking_sprites)
gaper_head_spritesheet = spritesheet.SpriteSheet(gaper_head_sprites)

haunt_sprites = pygame.image.load("sprites/theHaunt.png")
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
        self.transformation = False
        self.invincible = False
        self.angle = 0
        self.hurt = False
        self.counter = 0
        self.flip = 1
        self.death_animation = False
        self.death_animation_duration = 0
        self.statsAssign()

    def draw(self, window):
        if self.type == "regular":
            if self.name == "gaper":
                sprite = body_walking_spritesheet.get_image(self.body_frame, 32, 32, scale=2)
                head_sprite = gaper_head_spritesheet.get_image(1, 32, 32, scale=2)
                sprite.blit(head_sprite, (self.x + self.width//2 - head_sprite.get_width()//2, self.y - head_sprite.get_height()//10))

            # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height), 1)

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

                sprite = pygame.transform.scale(sprite, (self.width, self.height)).convert_alpha()
                sprite = pygame.transform.rotate(sprite, self.angle).convert_alpha()

            if self.name == "the haunt":
                sprite = haunt_spritesheet.get_image(self.frame, 84, 79, scale=3, row=self.row)
                if not self.stage == 2:
                    sprite = self.spriteWobble(sprite)
            
        if self.hurt:
            colour_image = pygame.Surface(sprite.get_size()).convert_alpha()
            colour_image.fill((255, 120, 120))
            sprite.blit(colour_image, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        
        window.blit(sprite, (self.x + self.width//2 - sprite.get_width()//2, self.y + self.height//2 - sprite.get_height()//2))
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height), 1)

    def update(self, character, map):
        current_time = pygame.time.get_ticks()
        if not self.dead:
            self.move(map)

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

        self.bossBehaviour(current_time, map)
        self.enemyBehaviour(current_time)

    def move(self, map):
        if self.type == "regular":
            if self.name == "gaper":
                x_block, y_block = self.boundaryBlock(map.walls)
                delta_x = map.player_coordinates[0] - self.x
                delta_y = map.player_coordinates[1] - self.y

                distance = (delta_x**2 + delta_y**2)**(1/2)

                if distance != 0:
                    self.direction_x = delta_x / distance
                    self.direction_y = delta_y / distance
                else:
                    self.direction_x = 0
                    self.direction_y = 0

                self.x += self.speed_x * self.direction_x
                self.y += self.speed_y * self.direction_y

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
                self.width = 200
                self.height = 200
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
                    self.width = 250
                    self.height = 250
                self.speed_x = 5
                self.max_health = 22
                self.health == self.max_health
            self.x -= self.width//2
            self.y -= self.height//2
        
        if self.type == "regular":
            if self.name == "gaper":
                self.width = 64
                self.height = 64

            else:
                self.width = 50
                self.height = 50

    def bossBehaviour(self, current_time, map):
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
            if self.dead:
                if self.stage == 1:
                    amount_of_splits = 4
                if self.stage == 2:
                    amount_of_splits = 2
                if self.stage == 3:
                    amount_of_splits = 0
                for i in range(amount_of_splits):
                    map.current_room.enemies.append(Enemy(self.x - 25 + i*50, self.y, type="boss", name="fistula", width=self.width-100//self.stage, height=self.height-100//self.stage, stage=self.stage + 1))

    def spriteWobble(self, sprite):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_wobble_tick >= 50:
            self.counter += 1 * self.flip
            self.last_wobble_tick = current_time

            if self.counter >= 4 or self.counter <= 0:
                self.flip *= -1

        sprite = pygame.transform.scale(sprite, (sprite.get_width() + 10*self.counter/4, sprite.get_height() - 10*self.counter/4)).convert_alpha()
        return sprite
    
    def enemyBehaviour(self, current_time):
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

                self.bodyAnimation(direction, current_time)

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

