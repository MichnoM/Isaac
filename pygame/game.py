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
last_update = pygame.time.get_ticks()

class Player(object):
    def __init__(self, cord_x, cord_y, width=56, height=66):
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.stationary = True
        self.attack_speed = 5
        self.frame = 0

    def draw(self, window):
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

class Projectile(object):
    def __init__(self, x, y, radius, colour, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.vel = 8
        self.direction = direction

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)
        tear_sprite = tear_spritesheet.get_image(0, 130, 130, 0.2)
        window.blit(tear_sprite, (self.x - round(tear_sprite.get_width()//2), self.y - round(tear_sprite.get_height()//2)))

class Enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # self.end = end
        self.vel_x = 3
        self.vel_y = 3
        # self.path = [self.x, self.end]
        self.direction = 1
        self.enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.move()
        pygame.draw.rect(window, (0, 255, 0), self.enemy_rect)

    def move(self):
        if self.enemy_rect.left <= 20 or self.enemy_rect.right >= 780:
            self.direction *= -1
            self.vel_x = random.randint(0, 8) * self.direction
            self.vel_y = random.randint(0, 8) * self.direction
            if self.vel_x == 0 and self.vel_y == 0:
                self.vel_x = random.randint(2, 8) * self.direction
                self.vel_y = random.randint(2, 8) * self.direction

        if self.enemy_rect.top <= 20 or self.enemy_rect.bottom >= 580:
            self.direction *= -1
            self.vel_x = random.randint(0, 8) * self.direction
            self.vel_y = random.randint(0, 8) * self.direction
            if self.vel_x == 0 and self.vel_y == 0:
                self.vel_x = random.randint(2, 8) * self.direction
                self.vel_y = random.randint(2, 8) * self.direction

        self.enemy_rect.left += self.vel_x
        self.enemy_rect.top += self.vel_y
            # if last_update - current_time > 2000:
            #     self.direction *= -1
            #     self.vel = random.randint(2,8) * self.direction

def redrawGameWindow():
    window.blit(background, (0, 0))
    isaac.draw(window)
    for tear in tears:
        tear.draw(window)
    enemy1.draw(window)

    pygame.display.update()

on_cooldown_event = pygame.USEREVENT + 1
custom_sprite_event = pygame.USEREVENT + 2

on_cooldown = False
custom_sprite_event = False

#mainloop
isaac = Player(372, 267, 56, 66)
tears = []
enemy1 = Enemy(100, 100, 50, 50)

run = True
while run:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    isaac.stationary = True

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
        if tear.x < window_width and tear.x > 0:
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

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and isaac.cord_x > isaac.vel:
        isaac.cord_x -= isaac.vel
        isaac.right = False
        isaac.up = False
        isaac.down = False
        isaac.stationary = False
        isaac.left = True
    if keys[pygame.K_d] and isaac.cord_x < window_width - isaac.width - isaac.vel:
        isaac.cord_x += isaac.vel
        isaac.left = False
        isaac.up = False
        isaac.down = False
        isaac.stationary = False
        isaac.right = True
    if keys[pygame.K_s] and isaac.cord_y < window_height - isaac.height - isaac.vel:
        isaac.cord_y += isaac.vel
        isaac.up = False
        isaac.left = False
        isaac.right = False
        isaac.stationary = False
        isaac.down = True
    if keys[pygame.K_w] and isaac.cord_y > isaac.vel:
        isaac.cord_y -= isaac.vel
        isaac.down = False
        isaac.left = False
        isaac.right = False
        isaac.stationary = False
        isaac.up = True
    if isaac.stationary:
        isaac.up = False
        isaac.down = False
        isaac.left = False
        isaac.right = False

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