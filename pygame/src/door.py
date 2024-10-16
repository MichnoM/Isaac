import pygame
from . import spritesheet
from settings import window_width, window_height

door_sprites = pygame.image.load('sprites/doors.png')
door_spritesheet = spritesheet.SpriteSheet(door_sprites)
treasure_door = pygame.image.load("sprites/treasureDoors.png")
treasure_door = pygame.transform.scale(treasure_door, (51*2, 40*2))
boss_door = pygame.image.load("sprites/bossDoors.png")
boss_door_spritesheet = spritesheet.SpriteSheet(boss_door)

class Door:
    def __init__(self, x, y, width, height, localisation, type="regular"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.localisation = localisation
        self.type = type
        self.closed = False
        self.locked = False
        self.frame = 0
        self.sprite = None
        self.animating = False
        self.animation_speed = 20
        self.door_frames = []
        self.last_update_time = pygame.time.get_ticks()
        self.createDoorFrames()

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, localisation: {self.localisation}"
    
    def draw(self, window):
        for i in range(4):
            if self.localisation == i + 1:
                door_centre_x = self.x + self.width//2
                door_centre_y = self.y + self.height//2
                if self.type == "boss":
                    self.sprite = boss_door_spritesheet.get_image(self.frame, 63, 41, 2, rotation_angle = i*-90)
                else:
                    self.sprite = door_spritesheet.get_image(self.frame, 51, 35, 2, rotation_angle = i*-90)
                window.blit(self.sprite, (door_centre_x - self.sprite.get_width()//2, door_centre_y - self.sprite.get_height()//2))
                if self.type == "treasure":
                    sprite = pygame.transform.rotate(treasure_door, i*-90)
                    if self.localisation == 1:
                        door_centre_y -= 10
                    if self.localisation == 4:
                        door_centre_x -= 10
                    window.blit(sprite, (door_centre_x - self.sprite.get_width()//2, door_centre_y - self.sprite.get_height()//2))
        # for frame in self.door_frames:
        #     pygame.draw.rect(window, (200, 200, 200), frame)
    
    def update(self, map):
        if self.localisation == 1:
            self.x = window_width//2 - self.width//2
        if self.localisation == 2:
            self.x = window_width - self.width
            self.y = window_height//2 - self.height//2
        if self.localisation == 3:
            self.x = window_width//2 - self.width//2
            self.y = window_height - self.height
        if self.localisation == 4:
            self.y = window_height//2 - self.height//2

        if map.current_room.enemies:
            self.close()
        else:
            if not self.locked:
                self.open()

        current_time = pygame.time.get_ticks()

        if self.type == "boss":
            frames = 15
        elif self.type == "shop":
            frames = 14
        else:
            frames = 13

        if self.animating:
            if current_time - self.last_update_time > self.animation_speed:
                self.last_update_time = current_time

                if self.closed:
                    if self.frame < frames - 1:
                        self.frame += 1
                    else:
                        self.animating = False
                else:
                    if self.frame > 0:
                        self.frame -= 1
                    else:
                        self.animating = False

    def open(self):
        if self.closed:
            self.animating = True
            self.closed = False

    def close(self):
        if not self.closed:
            self.animating = True
            self.closed = True

    def createDoorFrames(self):
        top_frame = pygame.Rect(self.x, self.y, 30, 1)
        right_frame = pygame.Rect(self.x + self.width, self.y, 1, 30)
        bottom_frame = pygame.Rect(self.x, self.y + self.height, 30, 1)
        left_frame = pygame.Rect(self.x, self.y, 1, 30)
        self.door_frames = [top_frame, right_frame, bottom_frame, left_frame]

        for i in range(4):
            if self.localisation == i + 1:
                if i < 2:
                    self.door_frames.pop(i+2)
                else:
                    self.door_frames.pop(i-2)

