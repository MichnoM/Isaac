from . import door
from settings import window_width, window_height
class Room(object):
    def __init__(self, number_of_enemies, room_x, room_y, door_placement, room_type, amount_of_items = 0):
        self.number_of_enemies = number_of_enemies
        self.room_x = room_x
        self.room_y = room_y
        self.room_index = [room_x, room_y]
        self.door_placement = door_placement
        self.room_type = room_type
        self.visited = False
        self.amount_of_items = amount_of_items
        self.doors = []
        self.items = []
        self.doorsPlacement(door_placement)

    def __str__(self):
        return f"no of enemies: {self.number_of_enemies}, x: {self.room_x}, y: {self.room_y}, door placement: {self.door_placement}, type: {self.room_type}, items: {self.items}"

    def draw(self, window):
        for door in self.doors:
            door.draw(window)

    def doorsPlacement(self, door_placement):
        for i in door_placement:
            if i == 1 or i == 3:
                width = 50
                height = 65
                if i == 1:
                    x = window_width//2 - width//2
                    y = 0
                    self.doors.append(door.Door(x, y, width, height, 1))
                else:
                    x = window_width//2 - width//2
                    y = window_height - height
                    self.doors.append(door.Door(x, y, width, height, 3))
            elif i == 2 or i == 4:
                width = 65
                height = 50
                if i == 2:
                    x = window_width - width
                    y = window_height//2 - height//2
                    self.doors.append(door.Door(x, y, width, height, 2))
                else:
                    x = 0
                    y = window_height//2 - height//2
                    self.doors.append(door.Door(x, y, width, height, 4))