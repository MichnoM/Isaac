import pygame
import spritesheet
import random

pygame.init()

window_width = 1280
window_height = 800
window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Game")

isaac_sprites = pygame.image.load('sprites/Isaac.png')
tear_sprites = pygame.image.load('sprites/tear.png')
background = pygame.image.load('sprites/background.png')
background = pygame.transform.scale(background, (window_width, window_height))
healthbar = pygame.image.load('sprites/HealthBar.png')
healthbar = pygame.transform.scale(healthbar, (360, 60))

sprite_sheet = spritesheet.SpriteSheet(isaac_sprites)
tear_spritesheet = spritesheet.SpriteSheet(tear_sprites)

clock = pygame.time.Clock()

class Player(object):
    def __init__(self, x, y, width=56, height=66):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stationary = True
        self.frame = 0
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collision = False
        self.dead = False

        self.health = 5
        self.vel = 5
        self.attack_speed = 5
        self.damage = 10

    def draw(self, window):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        # HITBOX VISUALISATION
        #pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        # ---------------------------------------------------
        if not custom_sprite:
            sprite = sprite_sheet.get_image(self.frame)
            window.blit(sprite, (self.x, self.y))
        else:
            self.frame = 4
            sprite = sprite_sheet.get_image(self.frame)
            window.blit(sprite, (self.x, self.y))

    def hit(self):
        if self.health > 0:
            self.health -= 1
            self.frame = 4
            if self.health <= 0:
                self.dead = True
                self.frame = 5

class Projectile(object):
    def __init__(self, x, y, radius, colour, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.vel = 8
        self.direction = direction
        self.tear_sprite = tear_spritesheet.get_image(0, 130, 130, 0.2)
        self.width = self.radius * 2
        self.height = self.radius * 2

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)
        window.blit(self.tear_sprite, (self.x - round(self.tear_sprite.get_width()//2), self.y - round(self.tear_sprite.get_height()//2)))

class Enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel_x = 3
        self.vel_y = 3
        self.direction_x = 1
        self.direction_y = 1
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = 10
        self.cooldown_tracker = 0
        self.direction = random.randint(1, 4)

    def draw(self, window):
        self.move()
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y, self.width, self.height))
        #pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.cooldown_tracker >= 1:
            self.cooldown_tracker += 1
        if self.cooldown_tracker == 10:
            self.cooldown_tracker = 0
        if self.x + self.width >= map.right_wall.x or self.x <= map.left_wall.x + map.left_wall.width:
            if self.cooldown_tracker == 0:
                self.direction_x *= -1
                self.vel_x = random.randint(1, 4) * self.direction_x
                self.cooldown_tracker = 1

        if self.y + self.height >= map.bottom_wall.y or self.y <= map.upper_wall.y + map.upper_wall.height:
            if self.cooldown_tracker == 0:
                self.direction_y *= -1
                self.vel_y = random.randint(1, 4) * self.direction_y
                self.cooldown_tracker = 1

        if self.direction == 1:
            self.x += 1 * self.vel_x
            self.y += 1 * self.vel_y
        elif self.direction == 2:
            self.x -= 1 * self.vel_x
            self.y -= 1 * self.vel_y
        elif self.direction == 3:
            self.x += 1 * self.vel_x
            self.y -= 1 * self.vel_y
        else:
            self.x -= 1 * self.vel_x
            self.y += 1 * self.vel_y

    def hit(self):
        if self.health > 0:
            self.health -= 1 * isaac.damage
            if self.health <= 0:
                enemies.pop(enemies.index(enemy))

class Map(object):
    def __init__(self, width, height, thickness = 40):
        self.width = width
        self.height = height
        self.thickness = thickness
        self.left_wall = pygame.Rect(0, 0, thickness, height)
        self.right_wall = pygame.Rect(window_width - thickness, 0, thickness, height)
        self.upper_wall = pygame.Rect(0, 0, width, thickness)
        self.bottom_wall = pygame.Rect(0, window_height - thickness-20, width, thickness+20)
        self.walls = [self.left_wall, self.right_wall, self.upper_wall, self.bottom_wall]

    def draw(self, window):
        for wall in self.walls:
            pygame.draw.rect(window, (255, 0, 0), wall, 2)

class Level(object):
    def __init__(self, number_of_enemies, number_of_doors, level_number):
        self.number_of_enemies = number_of_enemies
        self.number_of_doors = number_of_doors
        self.level_number = level_number
        self.previous_door = ""
        self.doors = []
        self.createDoors()
        self.enemiesSpawn()

    def draw(self, window):
        for door in self.doors:
            pygame.draw.rect(window, (0, 0, 0), (door.x, door.y, door.width, door.height))

    def createDoors(self):
        # number_of_doors = random.randint(1, 4)
        door_placement_check = []
        door_placement = 0
        if self.previous_door == 0:
            for i in range(0, self.number_of_doors):
                door_placement = random.randint(1, 4)
                if door_placement not in door_placement_check:
                    door_placement_check.append(door_placement)
                else:
                    for i in range(0, 100):
                        door_placement = random.randint(1, 4)
                        if door_placement not in door_placement_check:
                            door_placement_check.append(door_placement)
                            break
        else:
            for i in range(0, self.number_of_doors - 1):
                if i == 0:
                    door_placement = self.previous_door
                else:
                    door_placement = random.randint(1, 4)
                if door_placement not in door_placement_check:
                    door_placement_check.append(door_placement)
                else:
                    for i in range(0, 100):
                        door_placement = random.randint(1, 4)
                        if door_placement not in door_placement_check:
                            door_placement_check.append(door_placement)
                            break
                
        if door_placement == 1 or door_placement == 3:
            width = 50
            height = 65
            if door_placement == 1:
                x = window_width//2 - width//2
                y = 0
                self.doors.append(Doors(x, y, width, height, "up"))
            else:
                x = window_width//2 - width//2
                y = window_height - height
                self.doors.append(Doors(x, y, width, height, "up"))
        elif door_placement == 2 or door_placement == 4:
            width = 50
            height = 50
            if door_placement == 2:
                x = window_width - width
                y = window_height//2 - height//2
                self.doors.append(Doors(x, y, width, height, "up"))
            else:
                x = 0
                y = window_height//2 - height//2
                self.doors.append(Doors(x, y, width, height, "up"))
            
    def enemiesSpawn(self):
        # self.number_of_enemies = random.randint(1, 3)
        for i in range(0, self.number_of_enemies):
            spawn_x = random.randint(map.left_wall.width + 100, map.right_wall.x - 100)
            spawn_y = random.randint(map.upper_wall.height + 100, map.bottom_wall.y - 100)
            if spawn_x == isaac.x or spawn_y == isaac.y:
                spawn_x = random.randint(map.left_wall.width, map.right_wall.x)
                spawn_y = random.randint(map.upper_wall.height, map.bottom_wall.y)
                enemies.append(Enemy(spawn_x, spawn_y, 50, 50))
            else:
                enemies.append(Enemy(spawn_x, spawn_y, 50, 50))

class Doors(object):
    def __init__(self, x, y, width, height, localisation):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.localisation = localisation
        self.createDoor()

    def createDoor(self):
        pygame.Rect(self.x, self.y, self.width, self.height)

def redrawGameWindow():
    window.blit(background, (0, 0))
    map.draw(window)
    isaac.draw(window)
    for tear in tears:
        tear.draw(window)
    for enemy in enemies:
        enemy.draw(window)
    levels[level_number].draw(window)
    window.blit(healthbar, (-360 + 45 * isaac.health, 10))

    pygame.display.update()

def checkCollision(object1, object2):
    if object1.x + object1.width > object2.x and object1.x < object2.x + object2.width:
        if object1.y + object1.height > object2.y and object1.y < object2.y + object2.height:
            return True
    return False

cooldown_reset_event = pygame.USEREVENT + 1
damage_cooldown_reset_event = pygame.USEREVENT + 2
custom_sprite_event = pygame.USEREVENT + 3

on_cooldown = False
damage_cooldown = False
custom_sprite = False

# MAIN LOOP
# |-----------------------------------------------------------------------------------|
map = Map(window_width, window_height)
isaac = Player(372, 267, 56, 66)
levels = []
tears = []
enemies = []
level0 = Level(0, 4, 0)
level_number = 0
levels.append(level0)

run = True
while run:
    clock.tick(60)

    isaac.stationary = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == cooldown_reset_event:
            on_cooldown = False
            pygame.time.set_timer(cooldown_reset_event, 0)
        if event.type == damage_cooldown_reset_event:
            damage_cooldown = False
            pygame.time.set_timer(damage_cooldown_reset_event, 0)
        if event.type == custom_sprite_event:
            custom_sprite = False
            pygame.time.set_timer(custom_sprite_event, 0)

    for tear in tears:
        if tear.x < window_width and tear.x > 0 and tear.y < window_height and tear.y > 0:
            if tear.direction == "up":
                tear.y -= tear.vel
            elif tear.direction == "down":
                tear.y += tear.vel
            elif tear.direction == "left":
                tear.x -= tear.vel
            elif tear.direction == "right":
                tear.x += tear.vel
        else:
            tears.pop(tears.index(tear))

        for enemy in enemies:
            if checkCollision(tear, enemy):
                tears.pop(tears.index(tear))
                enemy.hit()

    for enemy in enemies:
        if checkCollision(isaac, enemy):
            if not damage_cooldown:
                isaac.hit()
                damage_cooldown = True
                pygame.time.set_timer(damage_cooldown_reset_event, 1000)
                if not isaac.dead:
                    custom_sprite = True
                    pygame.time.set_timer(custom_sprite_event, 1000)

    for level in levels:
        for doors in level.doors:
            if checkCollision(isaac, doors) and not enemies:
                level.previous_door = doors.localisation
                level_number += 1
                levels.append(Level(random.randint(1, 6), random.randint(1, 4), level_number))

    keys = pygame.key.get_pressed()

    if isaac.dead == False:
        if keys[pygame.K_a]:
            if not checkCollision(isaac, map.left_wall):
                isaac.x -= isaac.vel
            isaac.stationary = False
            isaac.frame = 2
        if keys[pygame.K_d]:
            if not checkCollision(isaac, map.right_wall):
                isaac.x += isaac.vel
            isaac.stationary = False
            isaac.frame = 3
        if keys[pygame.K_s]:
            if not checkCollision(isaac, map.bottom_wall):
                isaac.y += isaac.vel
            isaac.stationary = False
            isaac.frame = 0
        if keys[pygame.K_w]:
            if not checkCollision(isaac, map.upper_wall):
                isaac.y -= isaac.vel
            isaac.stationary = False
            isaac.frame = 1
        if isaac.stationary:
            isaac.frame = 0

        if keys[pygame.K_UP]:
            isaac.frame = 1
            if not on_cooldown:
                tears.append(Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "up"))
                on_cooldown = True
                pygame.time.set_timer(cooldown_reset_event, 1000//isaac.attack_speed)

        elif keys[pygame.K_DOWN]:
            isaac.frame = 0
            if not on_cooldown:
                tears.append(Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "down"))
                on_cooldown = True
                pygame.time.set_timer(cooldown_reset_event, 1000//isaac.attack_speed)

        elif keys[pygame.K_LEFT]:
            isaac.frame = 2
            if not on_cooldown:
                tears.append(Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "left"))
                on_cooldown = True
                pygame.time.set_timer(cooldown_reset_event, 1000//isaac.attack_speed)

        elif keys[pygame.K_RIGHT]:
            isaac.frame = 3
            if not on_cooldown:
                tears.append(Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "right"))
                on_cooldown = True
                pygame.time.set_timer(cooldown_reset_event, 1000//isaac.attack_speed)

    redrawGameWindow()

pygame.quit()