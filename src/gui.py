import pygame
from settings import window_width, window_height, debug_mode
from . import spritesheet
import globals

_circle_cache = {}

pause_screen = pygame.image.load('sprites/ui/pausescreen.png')
pointer_sprite = pygame.image.load('sprites/ui/pauseScreenPointer.png')

healthbar = pygame.image.load('sprites/ui/healthBar.png')
healthbar_empty = pygame.image.load('sprites/ui/healthBarEmpty.png')

pickups = pygame.image.load('sprites/ui/pickupsGui.png')

item_text_background = pygame.image.load('sprites/ui/textBackground.png')

boss_healthbar_sprite = pygame.image.load("sprites/ui/bossHealthBar.png")
boss_healthbar_spritesheet = spritesheet.SpriteSheet(boss_healthbar_sprite)

healthbar = pygame.transform.scale(healthbar, (360, 45))
healthbar_empty = pygame.transform.scale(healthbar_empty, (360, 45))
pickups = pygame.transform.scale(pickups, (60*0.75, 210*0.75))

scale = 3

item_text_background = pygame.transform.scale(item_text_background, (400*scale, 64*scale))
pause_screen = pygame.transform.scale(pause_screen, (pause_screen.get_width()*scale, pause_screen.get_height()*scale))
pointer_sprite = pygame.transform.scale(pointer_sprite, (pointer_sprite.get_width()*scale, pointer_sprite.get_height()*scale))

pygame.init()

font = pygame.font.Font("font/upheavtt.ttf", 40)

gui = pygame.Surface((globals.window_width, globals.window_height), pygame.SRCALPHA)

bg = pygame.Surface((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.SRCALPHA)

class Gui:
    def __init__(self):
        self.width = globals.window_width
        self.height = globals.window_height
        self.last_healthbar_frame = pygame.time.get_ticks()
        self.item_text_duration = 4000
        self.show_text = False
        self.last_text_time = pygame.time.get_ticks()
        self.item_text_x = -200
        self.frame = 0
        self.last_animation_tick = 0
        self.animation_frame_length = 2
        self.updated = False
        self.check = False
        self.check2 = False
        self.frame_updated = False

    def draw(self, window, character, pause, map, current_button):
        gui.set_colorkey((1,1,1))
        gui.fill((1,1,1))
        self.drawHealthbar(window, character)
        self.drawBossHealthBar(window, map.current_room.enemies)
        self.drawItemDescription(window, character)
        self.drawPickupsCount(window, character)

        if pause:
            sprite = pause_screen.copy()
            pointer = pointer_sprite

            if current_button == 1:
                pointer_x = sprite.get_width()//6 - pointer.get_width()//2
                pointer_y = sprite.get_height()*0.75 - pointer.get_height()//4

            if current_button == 2:
                pointer_x = sprite.get_width()//5
                pointer_y = sprite.get_height()*0.85

            if current_button == 0:
                pointer_x = sprite.get_width()//5 - pointer.get_width()//2
                pointer_y = sprite.get_height()*0.60 - pointer.get_height()//4

            bg.fill((0,0,0))
            bg.set_alpha(180)

            colour = (54, 47, 45)
            speed = font.render(f"{character.speed}", 1, colour)
            attack_speed = font.render(f"{character.attack_speed}", 1, colour)
            damage = font.render(f"{character.damage}", 1, colour)
            range = font.render(f"{character.range}", 1, colour)
            shot_speed = font.render(f"{character.shot_speed}", 1, colour)
            luck = font.render(f"{character.luck}", 1, colour)

            sprite.blit(speed, (88*scale, 46*scale))
            sprite.blit(attack_speed, (86*scale, 62*scale))
            sprite.blit(damage, (88*scale, 80*scale))
            sprite.blit(range, (143*scale, 46*scale))
            sprite.blit(shot_speed, (141*scale, 62*scale))
            sprite.blit(luck, (143*scale, 80*scale))

            sprite.blit(pointer_sprite, (pointer_x, pointer_y))
            gui.blit(sprite, (globals.window_width//2 - sprite.get_width()//2, globals.window_height//2 - sprite.get_height()//2))

            window.blit(bg, (0,0))

        window.blit(gui, (0, 0))
        self.update()

    def drawHealthbar(self, window, character):
        window.blit(healthbar_empty, (-360 + 45 * character.max_health, 10))
        window.blit(healthbar, (-360 + 45 * character.health, 10))

    def drawBossHealthBar(self, window, enemies):
        current_time = pygame.time.get_ticks()
        for enemy in enemies:
            if not enemy.dead:
                if enemy.type == "boss":
                    if not (enemy.name == "fistula" and enemy.stage != 1):
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

                        sprite.blit(current_health, (18*scale, 0))

                        window.blit(sprite, (globals.window_width//2 - sprite.get_width()//2, globals.window_height - self.height//8))

    def drawItemDescription(self, window, character):
        if character.pickup_item:
            self.show_text = True
            if not self.frame_updated:
                self.last_text_time = pygame.time.get_ticks()
                self.frame = 0
                self.frame_updated = True
            if self.updated == False:
                self.last_animation_tick = pygame.time.get_ticks()
                self.updated = True

        else:
            self.frame_updated = False

        if self.show_text == True:
            sprite = item_text_background.copy()

            self.item_text_x = globals.window_width//2 - item_text_background.get_width()//2 - item_text_background.get_width()*0.03
            desired_ending_x = globals.window_width//2 - item_text_background.get_width()//2 - item_text_background.get_width()*0.03 + item_text_background.get_width()

            name_text = self.render(f"{character.items[-1].name}", font)
            name_text = pygame.transform.scale(name_text, (name_text.get_width() * 1.5, name_text.get_height() * 1.5))

            description_text = self.render(f"{character.items[-1].description}", font)
            description_text = pygame.transform.scale(description_text, (description_text.get_width()*0.75, description_text.get_height()*0.75))

            sprite.blit(name_text, (window_width//2 - name_text.get_width()//2, sprite.get_height()//2 - name_text.get_height()//2 - sprite.get_height()*0.03))
            sprite.blit(description_text, (window_width//2 - description_text.get_width()//2, sprite.get_height()//2 + description_text.get_height()))

            if self.frame == 0 or self.frame == 15:
                if self.frame == 0:
                    sprite = sprite.subsurface((380*3, 0, 20*3, sprite.get_height()))
                else:
                    sprite = sprite.subsurface((0, 0, 20*3, sprite.get_height()))
                    self.item_text_x = 380*3

                sprite = pygame.transform.scale(sprite, (sprite.get_width()*4, sprite.get_height()//2))

            if self.frame == 1 or self.frame == 14:
                if self.frame == 1:
                    sprite = sprite.subsurface((300*3, 0, 100*3, sprite.get_height()))
                else:
                    sprite = sprite.subsurface((0, 0, 100*3, sprite.get_height()))
                    self.item_text_x = 300*3

                sprite = pygame.transform.scale(sprite, (sprite.get_width()*2, sprite.get_height()//2))

            if self.frame == 2 or self.frame == 13:
                if self.frame == 2:
                    sprite = sprite.subsurface((200*3, 0, 200*3, sprite.get_height()))
                else:
                    sprite = sprite.subsurface(0, 0, 200*3, sprite.get_height())
                    self.item_text_x = 200*3

                sprite = pygame.transform.scale(sprite, (sprite.get_width()*1.75, sprite.get_height()//2))

            if self.frame == 3 or self.frame == 12:
                if self.frame == 3:
                    sprite = sprite.subsurface((20*3, 0, 380*3, sprite.get_height()))
                else:
                    sprite = sprite.subsurface((0, 0, 380*3, sprite.get_height()))
                    self.item_text_x = 20*3

                sprite = pygame.transform.scale(sprite, (sprite.get_width(), sprite.get_height()//1.5))

            if self.frame == 4 or self.frame == 11:
                sprite = pygame.transform.scale(sprite, (sprite.get_width()*0.7, sprite.get_height()))

            if self.frame == 5 or self.frame == 10:
                sprite = pygame.transform.scale(sprite, (sprite.get_width()*0.8, sprite.get_height()))

            if self.frame == 6 or self.frame == 9:
                sprite = pygame.transform.scale(sprite, (sprite.get_width()*0.9, sprite.get_height()))

            if self.frame >= 4 and self.frame <= 7:
                self.item_text_x = desired_ending_x - sprite.get_width()

            if self.frame >= 0 and self.frame <= 3:
                self.item_text_x = 0

            if self.frame == 8:
                if self.check == False:
                    self.last_text_time = pygame.time.get_ticks()
                    self.check = True

            window.blit(sprite, (self.item_text_x, globals.window_height*0.2 - sprite.get_height()//2))

    def drawPickupsCount(self, window, character):
        gui.blit(pickups, (0, 100))
        gui.blit(self.render(f"{character.coins}", font), (60*0.75, 103))
        gui.blit(self.render(f"{character.bombs}", font), (60*0.75, 153))
        gui.blit(self.render(f"{character.keys}", font), (60*0.75, 203))

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.show_text and current_time - self.last_text_time > self.item_text_duration:
            if self.check2 == False:
                self.frame = 9
                self.check2 = True

        if self.show_text and current_time - self.last_animation_tick > self.animation_frame_length:
            if not self.frame == 8:
                self.frame += 1
                self.last_animation_tick = current_time
                if self.frame == 16:
                    self.show_text = False
                    self.last_text_time = current_time
                    self.frame = 0
                    self.updated = False
                    self.check = False
                    self.check2 = False

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