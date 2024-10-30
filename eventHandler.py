import pygame
from settings import window_width, window_height, debug_mode
import globals

cooldown_event = pygame.USEREVENT + 1
damage_taken_cooldown_event = pygame.USEREVENT + 2
head_animation_event = pygame.USEREVENT + 3
body_animation_cooldown_event = pygame.USEREVENT + 4
hurt_animation_event = pygame.USEREVENT + 5
pickup_item_event = pygame.USEREVENT + 6
pickup_pickup_event = pygame.USEREVENT + 7
room_change_event = pygame.USEREVENT + 8

class eventHandler:
    def __init__(self, map, character, window, monitor_size, background, menu):
        self.map = map
        self.character = character
        self.run = True
        self.pause = False
        self.main_menu = True
        self.debug_mode = debug_mode
        self.window = window
        self.monitor_size = monitor_size
        self.fullscreen = False
        self.background = background
        self.title_menu = menu
        self.menu = self.title_menu
        self.current_button = 1

        self.map_change_check = False
        self.cooldown_check = False
        self.head_animation_check = False
        self.body_animation_check = False
        self.damage_taken_check = False
        self.hurt_animation_check = False
        self.pickup_item_check = False
        self.pickup_pickup_check = False

    def eventHandling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_ESCAPE:
                    if not self.map.room_change:
                        if self.pause:
                            self.pause = False
                        else:
                            self.current_button = 1
                            self.pause = True

                if event.key == pygame.K_UP:
                    if self.pause:
                        self.current_button -= 1
                        if self.current_button < 0:
                            self.current_button = 2

                if event.key == pygame.K_DOWN:
                    if self.pause:
                        self.current_button += 1
                        if self.current_button > 2:
                            self.current_button = 0

                if event.key == pygame.K_RETURN:
                    if self.pause:
                        if self.current_button == 1:
                            self.pause = not self.pause
                        if self.current_button == 2:
                            self.run = False

                    if self.main_menu:
                        self.main_menu = not self.main_menu

                if event.key == pygame.K_SPACE:
                    if self.main_menu:
                        self.main_menu = not self.main_menu
                            
                if event.key == pygame.K_f:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.window = pygame.display.set_mode(self.monitor_size, pygame.SCALED | pygame.FULLSCREEN)
                        globals.window_width = self.window.get_width()
                        globals.window_height = self.window.get_height()
                        self.background = pygame.transform.scale(self.background, (globals.window_width, globals.window_height))
                        self.menu = pygame.transform.smoothscale(self.title_menu.copy(), (globals.window_width, globals.window_height))
                    else:
                        self.window = pygame.display.set_mode((window_width, window_height), pygame.SCALED)
                        globals.window_width = self.window.get_width()
                        globals.window_height = self.window.get_height()
                        self.background = pygame.transform.scale(self.background, (globals.window_width, globals.window_height))
                        self.menu = pygame.transform.smoothscale(self.title_menu.copy(), (globals.window_width, globals.window_height))

                if event.key == pygame.K_b:
                    self.debug_mode = not self.debug_mode

            if event.type == cooldown_event:
                self.character.shooting_cooldown = False
                self.cooldown_check = False
                pygame.time.set_timer(cooldown_event, 0)
                
            if event.type == damage_taken_cooldown_event:
                self.character.damage_taken_cooldown = False
                self.damage_taken_check = False
                pygame.time.set_timer(damage_taken_cooldown_event, 0)

            if event.type == head_animation_event:
                self.character.head_animation = False
                self.head_animation_check = False
                pygame.time.set_timer(head_animation_event, 0)

            if event.type == body_animation_cooldown_event:
                self.character.body_animation_cooldown = False
                self.body_animation_check = False
                pygame.time.set_timer(body_animation_cooldown_event, 0)

            if event.type == hurt_animation_event:
                self.character.hurt = False
                self.character.hurt_interaction = False
                self.hurt_animation_check = False
                pygame.time.set_timer(hurt_animation_event, 0)

            if event.type == pickup_item_event:
                self.character.pickup_item = False
                self.pickup_item_check = False
                pygame.time.set_timer(pickup_item_event, 0)

            if event.type == pickup_pickup_event:
                self.character.pickup_pickup = False
                self.pickup_pickup_check = False
                pygame.time.set_timer(pickup_pickup_event, 0)

            if event.type == room_change_event:
                self.map.room_change = False
                self.map_change_check = False
                pygame.time.set_timer(room_change_event, 0)\
                
        if not self.pause:
            if self.character.shooting_cooldown:
                if not self.cooldown_check:
                    pygame.time.set_timer(cooldown_event, 1000//self.character.attack_speed)
                    self.cooldown_check = True
                
            if self.character.head_animation:
                if not self.head_animation_check:
                    pygame.time.set_timer(head_animation_event, self.character.head_animation_duration)
                    self.head_animation_check = True

            if self.character.body_animation_cooldown:
                if not self.body_animation_check:
                    pygame.time.set_timer(body_animation_cooldown_event, self.character.body_animation_duration)
                    self.body_animation_check = True

            if self.character.damage_taken_cooldown:
                if not self.damage_taken_check:
                    pygame.time.set_timer(damage_taken_cooldown_event, 1000)
                    self.damage_taken_check = True

            if self.character.hurt:
                if not self.hurt_animation_check:
                    pygame.time.set_timer(hurt_animation_event, self.character.hurt_animation_duration)
                    self.hurt_animation_check = True

            if self.character.pickup_item:
                if not self.pickup_item_check:
                    pygame.time.set_timer(pickup_item_event, self.character.pickup_item_duration)
                    self.pickup_item_check = True

            if self.character.pickup_pickup:
                if not self.pickup_pickup_check:
                    pygame.time.set_timer(pickup_pickup_event, self.character.pickup_pickup_duration)
                    self.pickup_pickup_check = True

            if self.map.room_change:
                if not self.map_change_check:
                    pygame.time.set_timer(room_change_event, 400)
                    self.map_change_check = True

        return self.run, self.pause, self.window, self.background, self.current_button, self.main_menu, self.menu, self.debug_mode