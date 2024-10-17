import pygame
from settings import debug_mode
from . import spritesheet
import globals

_circle_cache = {}

healthbar = pygame.image.load('sprites/healthBar.png')
healthbar_empty = pygame.image.load('sprites/healthBarEmpty.png')
pickups = pygame.image.load('sprites/pickupsGui.png')
boss_healthbar_sprite = pygame.image.load("sprites/bossHealthBar.png")
boss_healthbar_spritesheet = spritesheet.SpriteSheet(boss_healthbar_sprite)

healthbar = pygame.transform.scale(healthbar, (360, 45))
healthbar_empty = pygame.transform.scale(healthbar_empty, (360, 45))
pickups = pygame.transform.scale(pickups, (60*0.75, 210*0.75))

pygame.init()

font = pygame.font.Font("font/upheavtt.ttf", 40)

class Gui:
    def __init__(self):
        self.width = globals.window_width
        self.height = globals.window_height
        self.last_healthbar_frame = pygame.time.get_ticks()

    def draw(self, window, character, pause, map):
        gui = pygame.Surface((self.width, self.height))
        gui.fill((1, 1, 1))
        gui.set_colorkey((1, 1, 1))
        self.drawHealthbar(window, character)
        self.drawBossHealthBar(window, map.current_room.enemies)
        gui.blit(pickups, (0, 100))
        gui.blit(self.render(f"{character.coins}", font), (60*0.75, 103))
        gui.blit(self.render(f"{character.bombs}", font), (60*0.75, 153))
        gui.blit(self.render(f"{character.keys}", font), (60*0.75, 203))
        # if debug_mode:
        #     pygame.draw.line(gui, (0, 0, 255), (self.width//2, self.height), (self.width//2, 0))
        #     pygame.draw.line(gui, (0, 0, 255), (0, self.height//2), (self.width, self.height//2))

        if pause:
            label = font.render(f"Damage: {character.damage}, Attack Speed: {character.attack_speed}, Speed: {character.speed}", 1, (255, 255, 255))
            menu = pygame.Surface((self.width//2, self.height//2))
            menu.fill((0, 0, 0))
            menu.blit(label, (menu.get_width()//10, menu.get_width()//10))
            gui.blit(menu, (self.width//4, self.height//4, self.width//2, self.height//2))

        window.blit(gui, (0, 0))
        self.update()

    def drawHealthbar(self, window, character):
        window.blit(healthbar_empty, (-360 + 45 * character.max_health, 10))
        window.blit(healthbar, (-360 + 45 * character.health, 10))

    def drawBossHealthBar(self, window, enemies):
        current_time = pygame.time.get_ticks()
        for enemy in enemies:
            if enemy.type == "boss":
                scale = 3
                ratio = enemy.health / enemy.max_health
                
                sprite = boss_healthbar_spritesheet.get_image(0, 132, 32, scale, row=1)
                current_health = boss_healthbar_spritesheet.get_image(0, 132, 32, 3)
                current_health = current_health.subsurface(18*scale, 0, 110*scale * ratio, 32*scale)

                colour_image = pygame.Surface(current_health.get_size()).convert_alpha()
                if not enemy.hurt:
                    colour_image.fill((255, 0, 0))
                else:
                    colour_image.fill((200, 0, 0))
                    if current_time - self.last_healthbar_frame >= 40:
                        colour_image.fill((255, 0, 0))
                        self.last_healthbar_frame = current_time
                current_health.blit(colour_image, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

                # current_health = current_health.subsurface((0, 0, current_health.get_width() * ratio, current_health.get_height()))

                window.blit(sprite, (self.width//2 - sprite.get_width()//2, self.height - self.height//8))
                window.blit(current_health, (self.width//2 - sprite.get_width()//2 + 18*scale, self.height - self.height//8))

    def update(self):
        self.width = globals.window_width
        self.height = globals.window_height

    def _circlepoints(self, r):
        r = int(round(r))
        if r in _circle_cache:
            return _circle_cache[r]
        x, y, e = r, 0, 1 - r
        _circle_cache[r] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points

    def render(self, text, font, gfcolor=(255, 255, 255), ocolor=(0, 0, 0), opx=4):
        textsurface = font.render(text, True, gfcolor).convert_alpha()
        w = textsurface.get_width() + 2 * opx
        h = font.get_height()

        osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

        for dx, dy in self._circlepoints(opx):
            surf.blit(osurf, (dx + opx, dy + opx))

        surf.blit(textsurface, (opx, opx))
        return surf