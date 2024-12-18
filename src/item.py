import pygame
from . import spritesheet
from settings import window_width, window_height
from . import map

items_sprites = pygame.image.load("sprites/items/items.png")
shop_items_sprites = pygame.image.load("sprites/items/shopItems.png")

items_spritesheet = spritesheet.SpriteSheet(items_sprites)
shop_items_spritesheet = spritesheet.SpriteSheet(shop_items_sprites)

key_sprite = pygame.image.load("sprites/pickups/key.png")
bomb_sprite = pygame.image.load("sprites/pickups/bomb.png")
coin_sprite = pygame.image.load("sprites/pickups/coin.png")
heart_sprite = pygame.image.load("sprites/pickups/heart.png")

key_sprite = pygame.transform.scale(key_sprite, (28, 40))
bomb_sprite = pygame.transform.scale(bomb_sprite, (40, 42))
coin_sprite = pygame.transform.scale(coin_sprite, (36, 26))
heart_sprite = pygame.transform.scale(heart_sprite, (32, 26))

pygame.init()

font = pygame.font.Font("font/upheavtt.ttf", 40)

class Item:
    def __init__(self, name, stats, values, x = window_width//2 - 25, y = window_height//2 - 25, width=50, height=50, type=None, price = 0, id=None, description=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stats = stats
        self.values = values
        self.used = False
        self.effect_done = False
        self.picked = False
        self.type = type
        self.name = name
        self.price = price
        self.id = id
        self.centre_x = self.x + self.width//2
        self.centre_y = self.y + self.height//2
        self.starting_x = self.x
        self.starting_y = self.y
        self.direction = -1

        self.description = description

        self.pickups = ["key", "bomb", "coin", "heart"]

    def __str__(self):
        return f"type: {self.type}, name: {self.name} stats: {self.stats}, values: {self.values}, price: {self.price}, id: {self.id}"

    def draw(self, window):
        if self.id != None:
            frame, row = self.idToFrame(self.id)
        else:
            frame, row = 0, 0

        if self.type == "shop item":
            self.sprite = shop_items_spritesheet.get_image(frame, 32, 32, 2, row=row)
        else:
            self.sprite = items_spritesheet.get_image(frame, 32, 32, 2, row=row)

        if self.name == "key":
            self.sprite = key_sprite
        if self.name == "bomb":
            self.sprite = bomb_sprite
        if self.name == "coin":
            self.sprite = coin_sprite
        if self.name == "heart":
            self.sprite = heart_sprite
        window.blit(self.sprite, (self.centre_x - self.sprite.get_width()//2, self.centre_y - self.sprite.get_height()//2))

        if self.type == "shop item":
            if not self.picked:
                if self.price == 7 or self.price == 3:
                    colour = (200, 0, 0)
                else:
                    colour = (255, 255, 255)

                price = font.render(f"{self.price} $", 1, colour)
                
                window.blit(price, (self.x, self.y + 50))

    def update(self, character, map):
        self.centre_x = self.x + self.width//2
        self.centre_y = self.y + self.height//2

        if self.picked:
            self.x = character.x + character.width//2 - self.width//2
            self.y = character.y - character.height*2
            self.centre_x = self.x + self.width//2
            self.centre_y = self.y + self.height//2

        if self.type == "item" and not self.used:
            self.pedestalMovement()

        if self.type == "item" or self.type == "shop item":
            if self.used and not character.pickup_item:
                if self in map.current_room.items:
                    map.current_room.items.remove(self)
        
        if self.type == "pickup":
            if self.used and not character.pickup_pickup:
                if self in map.current_room.pickups:
                    map.current_room.pickups.remove(self)

    def effect(self, character):
        if not self.used:
            if self.type == "item" or self.type == "shop item":
                character.items.append(self)

            for i, stat in enumerate(self.stats):
                if self.type == "item" or self.type == "shop item":
                    if not (stat == "max_health" and character.max_health >= 8):
                        if stat != "":
                            if stat == "damage":
                                stat *= character.damage_multiplier
                            setattr(character, stat, getattr(character, stat) + self.values[i])
                        character.coins -= self.price
                        self.used = True

                if self.type == "pickup":
                    if self.name == "key":
                        setattr(character, stat, getattr(character, stat) + self.values[i])
                        self.used = True
                    if self.name == "bomb":
                        setattr(character, stat, getattr(character, stat) + self.values[i])
                        self.used = True
                    if self.name == "coin":
                        setattr(character, stat, getattr(character, stat) + self.values[i])
                        self.used = True
                    if self.name == "heart":
                        if character.health < character.max_health:
                            setattr(character, stat, getattr(character, stat) + self.values[i])
                            self.used = True

                    if getattr(character, stat) >= 100:
                        setattr(character, stat, 99)
                    
    def pickup(self, character):
        if self.type == "item" or self.type == "shop item":
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

    def idToFrame(self, id):
        frame = int(id/5)
        row = id - 5*frame
        return row, frame
    
    def pedestalMovement(self):
        if self.y <= self.starting_y - self.height//4 or self.y >= self.starting_y + self.height//4:
            self.direction *= -1

        self.y += 0.5 * self.direction
