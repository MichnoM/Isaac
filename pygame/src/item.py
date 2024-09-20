import pygame
from settings import window_width, window_height
from . import map

item_sprite = pygame.image.load("sprites/item.png")
item_sprite = pygame.transform.scale(item_sprite, (50, 50))

key_sprite = pygame.image.load("sprites/key.png")
bomb_sprite = pygame.image.load("sprites/bomb.png")
coin_sprite = pygame.image.load("sprites/coin.png")
heart_sprite = pygame.image.load("sprites/heart.png")

key_sprite = pygame.transform.scale(key_sprite, (28, 40))
bomb_sprite = pygame.transform.scale(bomb_sprite, (40, 42))
coin_sprite = pygame.transform.scale(coin_sprite, (36, 26))
heart_sprite = pygame.transform.scale(heart_sprite, (32, 26))

class Item(object):
    def __init__(self, name, stats, values, x = window_width//2 - 25, y = window_height//2 - 25, width=50, height=50, type="item"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stats = stats
        self.values = values
        self.used = False
        self.picked = False
        self.type = type
        self.name = name

        self.centre_x = self.x + self.width//2
        self.centre_y = self.y + self.height//2

        self.pickups = ["key", "bomb", "coin", "heart"]

    def __str__(self):
        return f"name: {self.name} stats: {self.stats}, values: {self.values}"

    def draw(self, window):
        sprite = item_sprite
        if self.name == "key":
            sprite = key_sprite
        if self.name == "bomb":
            sprite = bomb_sprite
        if self.name == "coin":
            sprite = coin_sprite
        if self.name == "heart":
            sprite = heart_sprite
        window.blit(sprite, (self.centre_x - sprite.get_width()//2, self.centre_y - sprite.get_height()//2))

    def update(self, character, map):
        self.centre_x = self.x + self.width//2
        self.centre_y = self.y + self.height//2

        if self.picked:
            self.x = character.x + character.width//2 - self.width//2
            self.y = character.y - character.height//2
            self.centre_x = self.x + self.width//2
            self.centre_y = self.y + self.height//2

        if self.type == "item":
            if self.used and not character.pickup_item:
                if self in map.current_room.items:
                    map.current_room.items.remove(self)
        
        if self.type == "pickup":
            if self.used and not character.pickup_pickup:
                if self in map.current_room.pickups:
                    map.current_room.pickups.remove(self)

    def effect(self, character):
        if not self.used:
            if self.type == "item":
                character.items.append(self.name)
            for i, stat in enumerate(self.stats):
                if self.type == "item":
                    if not (stat == "max_health" and character.max_health >= 8):
                        if stat != "":
                            setattr(character, stat, getattr(character, stat) + self.values[i])
                        self.used = True
                if self.type == "pickup":
                    if self.name == "key":
                        if character.keys < 99:
                            setattr(character, stat, getattr(character, stat) + self.values[i])
                        self.used = True
                    if self.name == "bomb":
                        if character.bombs < 99:
                            setattr(character, stat, getattr(character, stat) + self.values[i])
                        self.used = True
                    if self.name == "coin":
                        if character.coins < 99:
                            setattr(character, stat, getattr(character, stat) + self.values[i])
                        self.used = True
                    if self.name == "heart":
                        if character.health < character.max_health:
                            setattr(character, stat, getattr(character, stat) + self.values[i])
                            self.used = True
                    
    def pickup(self, character):
        if self.type == "item":
            if not character.pickup_item:
                character.pickup_item = True
                self.picked = True
                self.effect(character)
        if self.type == "pickup":
            # if not character.pickup_pickup:
            #     if not (self.name == "key" or self.name == "bomb" or self.name == "coin" or self.name == "heart"):
            #         character.pickup_pickup = True
            #         self.picked = True
            self.effect(character)
