import random
from . import door
from . import enemy
from . import item as itemClass
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
        self.empty = False
        self.amount_of_items = amount_of_items
        self.doors = []
        self.items = []
        self.enemies = []
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

    def enemiesSpawn(self, number_of_enemies, character, boundaries):
        for i in range(0, number_of_enemies):
            spawn_x = random.randint(boundaries[0].width + 100, boundaries[1].x - 100)
            spawn_y = random.randint(boundaries[2].height + 100, boundaries[3].y - 100)
            if spawn_x == character.x or spawn_y == character.y:
                for j in range(100):
                    spawn_x = random.randint(boundaries[0].width + 100, boundaries[1].x - 100)
                    spawn_y = random.randint(boundaries[2].height + 100, boundaries[3].y - 100)
            else:
                self.enemies.append(enemy.Enemy(spawn_x, spawn_y, 50, 50))

    def itemsSpawn(self, item_list):
        for i in range(self.amount_of_items):
            random_int = random.randint(0, len(item_list) - 1)
            random_item = item_list[random_int]
            self.items.append(itemClass.Item(random_item[0], random_item[1]))

        for item_id, item in enumerate(self.items):
            if self.amount_of_items != 1:
                if self.amount_of_items % 2 == 0:
                    item.x = ((window_width//2 + item.width*1.5) - (self.amount_of_items * (item.width*2))) + 200*item_id
                else:
                    item.x = ((window_width//2 + item.width*1.5) - (self.amount_of_items * (item.width*2))) + 200*item_id