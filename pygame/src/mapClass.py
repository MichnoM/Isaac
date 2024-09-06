import pygame
import random
from . import room

class Map(object):
    def __init__(self, width, height, wall_thickness = 40):
        self.width = width
        self.height = height
        self.wall_thickness = wall_thickness
        self.left_wall = pygame.Rect(0, 0, wall_thickness, height)
        self.right_wall = pygame.Rect(width - wall_thickness, 0, wall_thickness, height)
        self.upper_wall = pygame.Rect(0, 0, width, wall_thickness)
        self.bottom_wall = pygame.Rect(0, height - wall_thickness-20, width, wall_thickness+20)
        self.walls = [self.left_wall, self.right_wall, self.upper_wall, self.bottom_wall]
        self.layout = []
        self.rooms = []
        self.number_of_rooms = 10
        self.mapLayout()
        self.roomCreation()

        self.background = pygame.image.load('sprites/Background.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def draw(self, window):
        window.blit(self.background, (0, 0))

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