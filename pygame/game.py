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
        self.damage = 1

    def draw(self, window):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        # HITBOX VISUALISATION
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        # ---------------------------------------------------
        sprite = sprite_sheet.get_image(self.frame)
        window.blit(sprite, (self.x, self.y))

    def hit(self):
        if self.health > 0:
            self.health -= 1
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
        self.direction = 1
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = 10

    def draw(self, window):
        self.move()
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.x + self.width > 770 or self.x < 30:
            self.direction *= -1
            self.vel_x = random.randint(0, 4) * self.direction
            self.vel_y = random.randint(0, 4) * self.direction
            if self.vel_x == 0 and self.vel_y == 0:
                self.vel_x = random.randint(2, 4) * self.direction
                self.vel_y = random.randint(2, 4) * self.direction

        if self.y + self.height > 550 or self.y < 50:
            self.direction *= -1
            self.vel_x = random.randint(0, 4) * self.direction
            self.vel_y = random.randint(0, 4) * self.direction
            if self.vel_x == 0 and self.vel_y == 0:
                self.vel_x = random.randint(2, 4) * self.direction
                self.vel_y = random.randint(2, 4) * self.direction

        self.x += self.vel_x
        self.y += self.vel_y

    def hit(self):
        if self.health > 0:
            self.health -= 1 * isaac.damage
            if self.health <= 0:
                enemies.pop(enemies.index(enemy))
        print('enemy hit!')

def redrawGameWindow():
    window.blit(background, (0, 0))
    isaac.draw(window)
    for tear in tears:
        tear.draw(window)
    for enemy in enemies:
        enemy.draw(window)
    window.blit(healthbar, (-360 + 45 * isaac.health, 10))

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
    if object1.x + object1.width > object2.x and object1.x < object2.x + object2.width:
        if object1.y + object1.height > object2.y and object1.y < object2.y + object2.height:
            return True
    return False

cooldown_reset_event = pygame.USEREVENT + 1
damage_cooldown_reset_event = pygame.USEREVENT + 2

on_cooldown = False
damage_cooldown = False

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == cooldown_reset_event:
            on_cooldown = False
            pygame.time.set_timer(cooldown_reset_event, 0)
        if event.type == damage_cooldown_reset_event:
            damage_cooldown = False
            pygame.time.set_timer(damage_cooldown_reset_event, 0)

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

    keys = pygame.key.get_pressed()

    if isaac.dead == False:
        if keys[pygame.K_a] and isaac.x > isaac.vel and isaac.collision == False:
            isaac.x -= isaac.vel
            isaac.stationary = False
            isaac.frame = 2
        if keys[pygame.K_d] and isaac.x < window_width - isaac.width - isaac.vel and isaac.collision == False:
            isaac.x += isaac.vel
            isaac.stationary = False
            isaac.frame = 3
        if keys[pygame.K_s] and isaac.y < window_height - isaac.height - 50 and isaac.collision == False:
            isaac.y += isaac.vel
            isaac.frame = 0
        if keys[pygame.K_w] and isaac.y > isaac.vel and isaac.collision == False:
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