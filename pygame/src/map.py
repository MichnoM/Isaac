import pygame
import random
from . import room
from . import enemy
from . import projectile
from settings import window_width, window_height
import globals

background = pygame.image.load('sprites/background.png')

class Map:
    def __init__(self, width, height, wall_thickness = 40):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.wall_thickness = wall_thickness
        self.blocks = []
        self.layout = []
        self.rooms = []
        self.number_of_rooms = 10
        self.current_room_index = [5, 5]
        self.current_room = None
        self.player_coordinates = []
        self.room_change = False
        self.cooldown = 0
        self.spawned_items = []

        self.mapLayout()
        self.roomCreation()
        self.doorTypeAssign()

    def __str__(self):
        layout = ""
        for x in self.layout:
            layout += f"{x}\n"
        return f"{layout}"

    def draw(self, window):
        if not self.room_change:
            self.x = globals.window_width//2 - self.width//2
            self.y = globals.window_height//2 - self.height//2
        else:
            if self.cooldown == 0:
                if self.y > globals.window_height//2 - self.height//2:
                    self.y -= 10
                if self.y < globals.window_height//2 - self.height//2:
                    self.y += 10
                if self.x > globals.window_width//2 - self.width//2:
                    self.x -= 10
                if self.x < globals.window_width//2 - self.width//2:
                    self.x += 10
            self.cooldown += 1
            if self.cooldown == 1:
                self.cooldown = 0
        sprite = pygame.transform.scale(background, (self.width, self.height))
        window.blit(sprite, (0, 0))

        for room in self.rooms:
            if room.room_index == self.current_room_index:
                for door in room.doors:
                    door.draw(window)

    def update(self, character):
        self.width = window_width
        self.height = window_height
        self.left_wall = pygame.Rect(0, 0, self.wall_thickness, self.height)
        self.right_wall = pygame.Rect(self.width - self.wall_thickness, 0, self.wall_thickness, self.height)
        self.upper_wall = pygame.Rect(0, 0, self.width, self.wall_thickness)
        self.bottom_wall = pygame.Rect(0, self.height - self.wall_thickness-20, self.width, self.wall_thickness+20)
        self.walls = [self.left_wall, self.right_wall, self.upper_wall, self.bottom_wall]
        self.player_coordinates = [character.x, character.y]

        self.roomChange(character)

        for room in self.rooms:
            if room.room_index == self.current_room_index:
                self.current_room = room

        for room in self.rooms:
            room.update(character, self)

        for item in character.items:
            self.itemEffects(item, character)

    def mapLayout(self):
        '''
        Creates the map layout. First it creates an 11x11 matrix filled with zeros and then it assigns room types starting from the centre.
        The rooms have to be adjacent to each other, special rooms can have only one entrance.
        '''
        for row in range(11):
            self.layout.append([])
            for column in range(11):
                self.layout[row].append(0)
        for i in range(self.number_of_rooms):
            if i == 0:
                self.layout[5][5] = 1
            else:
                for j in range(100):
                    row = random.randint(1, 8)
                    column = random.randint(1, 8)
                    if self.layout[row][column] == 0:
                        if self.layout[row-1][column] == 1 or self.layout[row+1][column] == 1 or self.layout[row][column-1] == 1 or self.layout[row][column+1] == 1:
                            self.layout[row][column] = 1
                            break
        for j in range(3):
            for n in range(100):
                    row = random.randint(1, 8)
                    column = random.randint(1, 8)
                    room_check = []
                    room_counter = []
                    if self.layout[row][column] == 0:
                        for i in range(4):
                            if i == 0:
                                room_check.append(self.layout[row-1][column])
                            if i == 1:
                                room_check.append(self.layout[row][column+1])
                            if i == 2:
                                room_check.append(self.layout[row+1][column])
                            if i == 3:
                                room_check.append(self.layout[row][column-1])
                        for z in room_check:
                            if z != 0:
                                room_counter.append(1)
                        if len(room_counter) == 1 and not (2 in room_check or 3 in room_check):
                            if j == 0:
                                self.layout[row][column] = 2
                                break
                            if j == 1:
                                self.layout[row][column] = 3
                                break
                            else:
                                self.layout[row][column] = 4
                                break

    def roomCreation(self):
        room_x = 0
        room_y = 0
        door_layout = []
        for row_id, row in enumerate(self.layout):
            for column_id, column in enumerate(row):
                if column != 0:
                    if self.layout[row_id][column_id - 1] != 0:
                        door_layout.append(4)
                    if self.layout[row_id][column_id + 1] != 0:
                        door_layout.append(2)
                    if self.layout[row_id - 1][column_id] != 0:
                        door_layout.append(1)
                    if self.layout[row_id + 1][column_id] != 0:
                        door_layout.append(3)

                    room_x = row_id
                    room_y = column_id
                    if column == 1:
                        self.rooms.append(room.Room(random.randint(1, 6), room_x, room_y, door_layout, column))
                    if column == 2:
                        self.rooms.append(room.Room(0, room_x, room_y, door_layout, column, 1))
                    if column == 3:
                        self.rooms.append(room.Room(1, room_x, room_y, door_layout, column, 1))
                    if column == 4:
                        self.rooms.append(room.Room(0, room_x, room_y, door_layout, column, 5))
                    door_layout = []

    def doorTypeAssign(self):
        for room in self.rooms:
            for door in room.doors:
                if room.room_type == "treasure":
                    door.type = "treasure"
                if room.room_type == "boss":
                    door.type = "boss"
                if room.room_type == "shop":
                    door.type = "shop"

                for i in range(2, 5):
                    if door.localisation == 1:
                        if self.layout[room.room_x - 1][room.room_y] == i:
                            door.type = i

                    if door.localisation == 2:
                        if self.layout[room.room_x][room.room_y + 1] == i:
                            door.type = i

                    if door.localisation == 3:
                        if self.layout[room.room_x + 1][room.room_y] == i:
                            door.type = i
                            
                    if door.localisation == 4:
                        if self.layout[room.room_x][room.room_y - 1] == i:
                            door.type = i

                if door.type == 2:
                    door.type = "treasure"
                if door.type == 3:
                    door.type = "boss"
                if door.type == 4:
                    door.type = "shop"
                    door.locked = True

    def checkCollision(self, object1, object2, mode = 1):
        '''
        pass
        '''
        # mode == 1 - checks for collision
        # mode == 2 - checks if one object is within another object
        if type(object2) == list:
            for i in object2:
                if mode == 1:
                    if object1.x + object1.width > i.x and object1.x < i.x + i.width:
                        if object1.y + object1.height > i.y and object1.y < i.y + i.height:
                            return object2
                else:
                    if object1.x + object1.width <= i.x + i.width and object1.x >= i.x:
                        if object1.y + object1.height <= i.y + i.height and object1.y >= i.y:
                            return object2
        else: 
            if mode == 1:
                if object1.x + object1.width > object2.x and object1.x < object2.x + object2.width:
                    if object1.y + object1.height > object2.y and object1.y < object2.y + object2.height:
                        return object2
            else:
                if object1.x + object1.width <= object2.x + object2.width and object1.x >= object2.x:
                        if object1.y + object1.height <= object2.y + object2.height and object1.y >= object2.y:
                            return object2
        return False
    
    def roomChange(self, character):
        if character.y <= 0:
            character.x = self.width//2 - character.width//2
            character.y = self.height - 100
            self.current_room_index[0] -= 1
            self.room_change = True
            self.y += 200
        if character.x >= self.width:
            character.x = 100 - character.width//2
            character.y = self.height//2 - character.height//2
            self.current_room_index[1] += 1
            self.room_change = True
            self.x += -200
        if character.y >= self.height:
            character.x = self.width//2 - character.width//2
            character.y = 100 - character.height//2
            self.current_room_index[0] += 1
            self.room_change = True
            self.y += -200
        if character.x <= 0:
            character.x = self.width - 100
            character.y = self.height//2 - character.height//2
            self.current_room_index[1] -= 1
            self.room_change = True
            self.x += 200

    def createTears(self, direction, character, type="friendly", amount=1):
        if direction == "down":
            direction2 = [[-0.25, 1], [0, 1], [0.25, 1]]
        if direction == "up":
            direction2 = [[-0.25, -1], [0, -1], [0.25, -1]]
        if direction == "left":
            direction2 = [[-1, -0.25], [-1, 0], [-1, 0.25]]
        if direction == "right":
            direction2 = [[1, -0.25], [1, 0], [1, 0.25]]

        for i in range(amount):
            x = character.x + character.width//2
            y = character.y + character.height//2
            if direction == "up" or direction == "down":
                if amount == 1:
                    x = character.x + character.width//2
                if amount == 2:
                    x = character.x + character.width//4 + i*30
                if amount == 3:
                    x = character.x + i*30

            if direction == "left" or direction == "right":
                if amount == 1:
                    y = character.y + character.height//2
                if amount == 2:
                    y = character.y + character.height//4 + i*30
                if amount == 3:
                    y = character.y + i*30
                    
            if amount != 3:
                self.current_room.tears.append(projectile.Projectile(x, y, 10, (0,0,0), direction, type, character))
            else:
                self.current_room.tears.append(projectile.Projectile(x, y, 10, (0,0,0), direction2[i], type, character))

    def checkDoorframeCollision(character, room):
        pass

    def itemEffects(self, item, character):
        if item.name == "piggy bank":
            if character.hurt and character.hurt_interaction:
                self.current_room.itemsSpawn("pickup", character, character.x + 60, character.y + 50, "coin")
                character.hurt_interaction = False

        if item.name == "steam sale":
            if not item.effect_done:
                for room in self.rooms:
                    for item in room.items:
                        item.price = item.price//2
                        item.effect_done = True

        if item.name == "mom's key":
            for room in self.rooms:
                room.pickup_quantity = 2
