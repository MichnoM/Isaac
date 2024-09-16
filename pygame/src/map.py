import pygame
import random
from . import room
from . import enemy
from . import projectile

class Map(object):
    def __init__(self, width, height, wall_thickness = 40):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.wall_thickness = wall_thickness
        self.left_wall = pygame.Rect(0, 0, wall_thickness, height)
        self.right_wall = pygame.Rect(width - wall_thickness, 0, wall_thickness, height)
        self.upper_wall = pygame.Rect(0, 0, width, wall_thickness)
        self.bottom_wall = pygame.Rect(0, height - wall_thickness-20, width, wall_thickness+20)
        self.walls = [self.left_wall, self.right_wall, self.upper_wall, self.bottom_wall]
        self.blocks = []
        self.layout = []
        self.rooms = []
        self.number_of_rooms = 10
        self.current_room_index = [5, 5]
        self.current_room = None
        self.room_change = False
        self.cooldown = 0

        self.mapLayout()
        self.roomCreation()
        self.doorTypeAssign()

        self.background = pygame.image.load('sprites/Background.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def draw(self, window):
        if not self.room_change:
            self.x = 0
            self.y = 0
        else:
            if self.cooldown == 0:
                if self.y > 0:
                    self.y -= 10
                if self.y < 0:
                    self.y += 10
                if self.x > 0:
                    self.x -= 10
                if self.x < 0:
                    self.x += 10
            self.cooldown += 1
            if self.cooldown == 1:
                self.cooldown = 0
        window.blit(self.background, (0, 0))

        for room in self.rooms:
            if room.room_index == self.current_room_index:
                room.draw(window)

    def mapLayout(self):
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
        for j in range(2):
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
                            else:
                                self.layout[row][column] = 3
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
                        self.rooms.append(room.Room(0, room_x, room_y, door_layout, column, 5))
                    if column == 3:
                        self.rooms.append(room.Room(1, room_x, room_y, door_layout, column, 1))
                    door_layout = []

    def doorTypeAssign(self):
        for room in self.rooms:
            for door in room.doors:
                if room.room_type == "treasure":
                    door.type = "treasure"
                if room.room_type == "boss":
                    door.type = "boss"

                for i in range(4):
                    if door.localisation == 1:
                        if self.layout[room.room_x - 1][room.room_y] == 2:
                            door.type = "treasure"
                        if self.layout[room.room_x - 1][room.room_y] == 3:
                            door.type = "boss"

                    if door.localisation == 2:
                        if self.layout[room.room_x][room.room_y + 1] == 2:
                            door.type = "treasure"
                        if self.layout[room.room_x][room.room_y + 1] == 3:
                            door.type = "boss"

                    if door.localisation == 3:
                        if self.layout[room.room_x + 1][room.room_y] == 2:
                            door.type = "treasure"
                        if self.layout[room.room_x + 1][room.room_y] == 3:
                            door.type = "boss"
                            
                    if door.localisation == 4:
                        if self.layout[room.room_x][room.room_y - 1] == 2:
                            door.type = "treasure"
                        if self.layout[room.room_x][room.room_y - 1] == 3:
                            door.type = "boss"

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
                            return True
                else:
                    if object1.x + object1.width <= i.x + i.width and object1.x >= i.x:
                        if object1.y + object1.height <= i.y + i.height and object1.y >= i.y:
                            return True
        else: 
            if mode == 1:
                if object1.x + object1.width > object2.x and object1.x < object2.x + object2.width:
                    if object1.y + object1.height > object2.y and object1.y < object2.y + object2.height:
                        return True
            else:
                if object1.x + object1.width <= object2.x + object2.width and object1.x >= object2.x:
                        if object1.y + object1.height <= object2.y + object2.height and object1.y >= object2.y:
                            return True
        return False
    
    def roomChange(self, character):
        if character.y <= 0:
            character.x = self.width//2 - character.width//2
            character.y = self.height - 100
            self.current_room_index[0] -= 1
            self.room_change = True
            self.y = 200
        if character.x >= self.width:
            character.x = 100 - character.width//2
            character.y = self.height//2 - character.height//2
            self.current_room_index[1] += 1
            self.room_change = True
            self.x = -200
        if character.y >= self.height:
            character.x = self.width//2 - character.width//2
            character.y = 100 - character.height//2
            self.current_room_index[0] += 1
            self.room_change = True
            self.y = -200
        if character.x <= 0:
            character.x = self.width - 100
            character.y = self.height//2 - character.height//2
            self.current_room_index[1] -= 1
            self.room_change = True
            self.x = 200

    def update(self, character):
        self.roomChange(character)
        for room in self.rooms:
            if room.room_index == self.current_room_index:
                self.current_room = room

        for room in self.rooms:
            room.update(character, self)

    def createTears(self, direction, character):
        self.current_room.tears.append(projectile.Projectile(round(character.x + character.width//2), round(character.y + character.height//2), 10, (0,0,0), direction))

    def checkDoorframeCollision(character, room):
        pass