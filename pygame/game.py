import pygame
import spritesheet

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Game")

isaacSprites = pygame.image.load('sprites/Isaac.png')
background = pygame.image.load('sprites/background.png')
background = pygame.transform.scale(background, (window_width, window_height))

sprite_sheet = spritesheet.SpriteSheet(isaacSprites)

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
        self.attack_speed = 1
        self.cooldown_tracker = 0

    def on_cooldown(self):
        self.cooldown_tracker += clock.get_time()
        if self.cooldown_tracker > 400/self.attack_speed:
            self.cooldown_tracker = 0
            return False
        return True

    def draw(self, window):
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

def redrawGameWindow():
    window.blit(background, (0, 0))
    isaac.draw(window)
    for tear in tears:
        tear.draw(window)

    pygame.display.update()

#mainloop
isaac = Player(372, 267, 56, 66)
tears = []
run = True
while run:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    isaac.stationary = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

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

    if keys[pygame.K_UP] and not isaac.on_cooldown():
        tears.append(Projectile(round(isaac.cord_x + isaac.width//2), round(isaac.cord_y + isaac.height//2), 6, (0, 0, 0), "up"))
        isaac.up = True
        isaac.down = False
        isaac.left = False
        isaac.right = False
    elif keys[pygame.K_DOWN] and not isaac.on_cooldown():
        tears.append(Projectile(round(isaac.cord_x + isaac.width//2), round(isaac.cord_y + isaac.height//2), 6, (0, 0, 0), "down"))
        isaac.down = True
        isaac.up = False
        isaac.left = False
        isaac.right = False
    elif keys[pygame.K_LEFT] and not isaac.on_cooldown():
        tears.append(Projectile(round(isaac.cord_x + isaac.width//2), round(isaac.cord_y + isaac.height//2), 6, (0, 0, 0), "left"))
        isaac.left = True
        isaac.up = False
        isaac.down = False
        isaac.right = False
    elif keys[pygame.K_RIGHT] and not isaac.on_cooldown():
        tears.append(Projectile(round(isaac.cord_x + isaac.width//2), round(isaac.cord_y + isaac.height//2), 6, (0, 0, 0), "right"))
        isaac.right = True
        isaac.up = False
        isaac.down = False
        isaac.left = False

    redrawGameWindow()

pygame.quit()