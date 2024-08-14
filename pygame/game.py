import pygame
import spritesheet
import random

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Game")

isaac_sprites = pygame.image.load('sprites/Isaac.png')
tear_sprites = pygame.image.load('sprites/tear.png')
background = pygame.image.load('sprites/background.png')
background = pygame.transform.scale(background, (window_width, window_height))

sprite_sheet = spritesheet.SpriteSheet(isaac_sprites)
tear_spritesheet = spritesheet.SpriteSheet(tear_sprites)

clock = pygame.time.Clock()

class Player(object):
    def __init__(self, cord_x, cord_y, width=56, height=66):
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.width = width
        self.height = height
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.stationary = True
        self.frame = 0
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.width, self.height)
        self.collision = False
        self.dead = False
        self.cooldown_tracker = 0

        self.health = 5
        self.vel = 5
        self.attack_speed = 5
        self.damage = 1

    def draw(self, window):
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.width, self.height)
        # HITBOX VISUALISATION
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        if not custom_sprite_event:
            if self.left:
                walk_left = sprite_sheet.get_image(2)
                window.blit(walk_left, (self.cord_x, self.cord_y))
            elif isaac.right:
                walk_right = sprite_sheet.get_image(3)
                window.blit(walk_right, (self.cord_x, self.cord_y))
            elif self.up:
                walk_up = sprite_sheet.get_image(1)
                window.blit(walk_up, (self.cord_x, self.cord_y))
            elif self.down:
                walk_down = sprite_sheet.get_image(0)
                window.blit(walk_down, (self.cord_x, self.cord_y))
            elif self.stationary:
                not_moving = sprite_sheet.get_image(0)
                window.blit(not_moving, (self.cord_x, self.cord_y))
        else:
            custom = sprite_sheet.get_image(self.frame)
            window.blit(custom, (self.cord_x, self.cord_y))

    def hit(self):
        if self.health > 0:
            self.health -= 1
            print('hit!')
        else:
            self.dead = True

class Projectile(object):
    def __init__(self, x, y, radius, colour, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.vel = 8
        self.direction = direction
        self.tear_sprite = tear_spritesheet.get_image(0, 130, 130, 0.2)
        self.hitbox = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

    def draw(self, window):
        pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)
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
        self.direction = 1
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = 10

    def draw(self, window):
        self.move()
        pygame.draw.rect(window, (0, 255, 0), self.hitbox, 2)

    def move(self):
        if self.hitbox.x + self.hitbox.width > 770 or self.hitbox.x < 30:
            self.direction *= -1
            self.vel_x = random.randint(0, 4) * self.direction
            self.vel_y = random.randint(0, 4) * self.direction
            if self.vel_x == 0 and self.vel_y == 0:
                self.vel_x = random.randint(2, 4) * self.direction
                self.vel_y = random.randint(2, 4) * self.direction

        if self.hitbox.y + self.hitbox.height > 550 or self.hitbox.y < 50:
            self.direction *= -1
            self.vel_x = random.randint(0, 4) * self.direction
            self.vel_y = random.randint(0, 4) * self.direction
            if self.vel_x == 0 and self.vel_y == 0:
                self.vel_x = random.randint(2, 4) * self.direction
                self.vel_y = random.randint(2, 4) * self.direction

        self.hitbox.x += self.vel_x
        self.hitbox.y += self.vel_y

    def hit(self):
        if self.health > 0:
            self.health -= 1 * isaac.damage
        else:
            enemies.pop(enemies.index(enemy))
        print('enemy hit!')

def redrawGameWindow():
    window.blit(background, (0, 0))
    isaac.draw(window)
    for tear in tears:
        tear.draw(window)
    for enemy in enemies:
        enemy.draw(window)

    pygame.display.update()

def enemiesSpawn():
    number_of_enemies = random.randint(1, 3)
    for i in range(0, number_of_enemies):
        spawn_x = random.randint(100, 700)
        spawn_y = random.randint(100, 500)
        if spawn_x == isaac.hitbox.x or spawn_y == isaac.hitbox.y:
            spawn_x = random.randint(100, 700)
            spawn_y = random.randint(100, 700)
            enemies.append(Enemy(spawn_x, spawn_y, 50, 50))
        else:
            enemies.append(Enemy(spawn_x, spawn_y, 50, 50))

def checkCollision(object1, object2):
    if object1.hitbox.x + object1.hitbox.width > object2.hitbox.x and object1.hitbox.x < object2.hitbox.x + object2.hitbox.width:
        if object1.hitbox.y + object1.hitbox.height > object2.hitbox.y and object1.hitbox.y < object2.hitbox.y + object2.hitbox.height:
            return True
    return False

on_cooldown_event = pygame.USEREVENT + 1 
custom_sprite_event = pygame.USEREVENT + 2

on_cooldown = False
custom_sprite = False
cooldown_tracker = 0

# MAIN LOOP
# |-----------------------------------------------------------------------------------|
isaac = Player(372, 267, 56, 66)
tears = []
enemies = []
enemiesSpawn()

run = True
while run:
    clock.tick(60)

    isaac.stationary = True
    isaac.collision = False
    cooldown_tracker += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == on_cooldown_event:
            on_cooldown = False
            pygame.time.set_timer(on_cooldown_event, 0)
        if event.type == custom_sprite_event:
            custom_sprite_event = False
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
            if tear.x > enemy.hitbox.x and tear.x < enemy.hitbox.x + enemy.hitbox.width:
                if tear.y > enemy.hitbox.y and tear.y < enemy.hitbox.y + enemy.hitbox.height:
                    tears.pop(tears.index(tear))
                    enemy.hit()

    for enemy in enemies:
        if checkCollision(isaac, enemy):
            if cooldown_tracker > 50:
                isaac.hit()
                cooldown_tracker = 0

    keys = pygame.key.get_pressed()

    if isaac.dead == False:
        if keys[pygame.K_a] and isaac.cord_x > isaac.vel and isaac.collision == False:
            isaac.cord_x -= isaac.vel
            isaac.right = False
            isaac.up = False
            isaac.down = False
            isaac.stationary = False
            isaac.left = True
            isaac.frame = 2
        if keys[pygame.K_d] and isaac.cord_x < window_width - isaac.width - isaac.vel and isaac.collision == False:
            isaac.cord_x += isaac.vel
            isaac.left = False
            isaac.up = False
            isaac.down = False
            isaac.stationary = False
            isaac.right = True
            isaac.frame = 3
        if keys[pygame.K_s] and isaac.cord_y < window_height - isaac.height - 50 and isaac.collision == False:
            isaac.cord_y += isaac.vel
            isaac.up = False
            isaac.left = False
            isaac.right = False
            isaac.stationary = False
            isaac.down = True
            isaac.frame = 0
        if keys[pygame.K_w] and isaac.cord_y > isaac.vel and isaac.collision == False:
            isaac.cord_y -= isaac.vel
            isaac.down = False
            isaac.left = False
            isaac.right = False
            isaac.stationary = False
            isaac.up = True
            isaac.frame = 1
        if isaac.stationary:
            isaac.up = False
            isaac.down = False
            isaac.left = False
            isaac.right = False
            isaac.frame = 0

        if keys[pygame.K_UP]:
            custom_sprite_event = True
            isaac.frame = 1
            pygame.time.set_timer(custom_sprite_event, 200)
            if not on_cooldown:
                tears.append(Projectile(round(isaac.cord_x + isaac.width//2), round(isaac.cord_y + isaac.height//2), 10, (0,0,0), "up"))
                isaac.up = True
                isaac.down = False
                isaac.left = False
                isaac.right = False
                on_cooldown = True
                pygame.time.set_timer(on_cooldown_event, 1000//isaac.attack_speed)
        elif keys[pygame.K_DOWN]:
            custom_sprite_event = True
            isaac.frame = 0
            pygame.time.set_timer(custom_sprite_event, 200)
            if not on_cooldown:
                tears.append(Projectile(round(isaac.cord_x + isaac.width//2), round(isaac.cord_y + isaac.height//2), 10, (0,0,0), "down"))
                isaac.down = True
                isaac.up = False
                isaac.left = False
                isaac.right = False
                on_cooldown = True
                pygame.time.set_timer(on_cooldown_event, 1000//isaac.attack_speed)
        elif keys[pygame.K_LEFT]:
            custom_sprite_event = True
            isaac.frame = 2
            pygame.time.set_timer(custom_sprite_event, 200)
            if not on_cooldown:
                tears.append(Projectile(round(isaac.cord_x + isaac.width//2), round(isaac.cord_y + isaac.height//2), 10, (0,0,0), "left"))
                isaac.left = True
                isaac.up = False
                isaac.down = False
                isaac.right = False
                on_cooldown = True
                pygame.time.set_timer(on_cooldown_event, 1000//isaac.attack_speed)
        elif keys[pygame.K_RIGHT]:
            custom_sprite_event = True
            isaac.frame = 3
            pygame.time.set_timer(custom_sprite_event, 200)
            if not on_cooldown:
                tears.append(Projectile(round(isaac.cord_x + isaac.width//2), round(isaac.cord_y + isaac.height//2), 10, (0,0,0), "right"))
                isaac.right = True
                isaac.up = False
                isaac.down = False
                isaac.left = False
                on_cooldown = True
                pygame.time.set_timer(on_cooldown_event, 1000//isaac.attack_speed)

    redrawGameWindow()

pygame.quit()