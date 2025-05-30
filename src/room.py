import random
from . import door
from . import regular
from . import boss
from . import item as itemClass
from .items import item_list, shop_items, pickup_list
from .enemies import bosses, regulars
from settings import window_width, window_height

class Room:
    def __init__(self, number_of_enemies, room_x, room_y, door_placement, type, amount_of_items = 0):
        self.number_of_enemies = number_of_enemies
        self.room_x = room_x
        self.room_y = room_y
        self.room_index = [room_x, room_y]
        self.door_placement = door_placement
        self.type = type
        self.visited = False
        self.empty = False
        self.spawn_room = False
        self.amount_of_items = amount_of_items
        self.doors = []
        self.items = []
        self.items_spawned = False
        self.pickups = []
        self.pickups_spawned = False
        self.pickup_quantity = 1
        self.enemies = []
        self.enemies_list = []
        self.tears = []
        self.boss_counter = 0
        self.typeAssignment()
        self.doorsPlacement(door_placement)

        self.placeholder = None
        self.pickup_placeholder = None

    def __str__(self):
        return f"enemies: {self.number_of_enemies}, x: {self.room_x}, y: {self.room_y}, door placement: {self.door_placement}, type: {self.type}\n items: {self.items}, pickups: {self.pickups}"

    def draw(self, window):
        pass

    def update(self, character, map):
        # sorting enemies by their y attribute to avoid sprites drawing themselves on top of eachother, now the lowest valued y gets drawn last.
        self.enemies.sort(key=lambda x: x.y)
        if not self.enemies:
            self.empty = True
        else:
            self.empty = False

        for door in self.doors:
            door.update(map)

        for enemy in self.enemies:
            enemy.update(character, map)

        for tear in self.tears:
            tear.update(character, map)

        for item in self.items:
            item.update(character, map)
        
        for pickup in self.pickups:
            pickup.update(character, map)

        # clearing the objects from rooms other than the displayed one, but also saving their states.
        if self.room_index != map.current_room_index:
            if len(self.items) > 0:
                self.items_spawned = False
                self.placeholder = self.items.copy()
                self.items = []
            if len(self.pickups) > 0:
                self.pickups_spawned = False
                self.pickup_placeholder = self.pickups.copy()
                self.pickups = []
            if len(self.enemies) > 0:
                self.visited = False
                self.boss_counter = 0
                self.enemies = []
            if len(self.tears) > 0:
                self.tears = []
    
    def typeAssignment(self):
        if self.type == 1:
            self.type = "regular"

        if self.type == 2:
            self.type = "treasure"

        if self.type == 3:
            self.type = "boss"

        if self.type == 4:
            self.type = "shop"

        if self.room_index == [5, 5]:
            self.spawn_room = True
            self.number_of_enemies = 0

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
        if len(self.enemies_list) == 0:
            if self.type == "regular":
                for i in range(number_of_enemies):
                    random_index = random.randint(0, len(regulars) - 1)
                    random_regular = regulars[random_index]
                    for j in range(100):
                        spawn_x = random.randint(boundaries[0].width + 100, boundaries[1].x - 100)
                        spawn_y = random.randint(boundaries[2].height + 100, boundaries[3].y - 100)
                        if spawn_x not in range(character.x - 100, character.x + 100) or spawn_y not in range(character.y - 100, character.y + 100):
                            break

                    self.enemies_list.append((spawn_x, spawn_y, random_regular[0], "regular"))

            if self.type == "boss":
                random_index = random.randint(0, len(bosses) - 1)
                random_boss = bosses[random_index]
                spawn_x = window_width//2
                spawn_y = window_height//2
                self.enemies_list.append((spawn_x, spawn_y, random_boss[0], "boss"))

        for i in self.enemies_list:
            if i[3] == "regular":
                self.enemies.append(regular.Regular(i[0], i[1], i[2]))
                
            if i[3] == "boss":
                self.enemies.append(boss.Boss(i[0], i[1], i[2]))

    def itemsSpawn(self, type, character, map, x=0, y=0, name = None):
        if name == None:
            if type == "item" or type == "shop item":
                if self.placeholder == None:
                    for i in range(self.amount_of_items):
                        for item in self.items:
                            map.spawned_items.append(item.name)
                        if type == "item":
                            for j in range(100):
                                random_int = random.randint(0, len(item_list) - 1)
                                random_item = item_list[random_int]
                                if random_item[0] not in map.spawned_items:
                                    break

                        if type == "shop item":
                            for j in range(100):
                                random_int = random.randint(0, len(shop_items) - 1)
                                random_item = shop_items[random_int]
                                if random_item[0] not in map.spawned_items:
                                    break

                        if self.type == "shop":
                            discount_chance = random.randint(1, 10)
                            if discount_chance == 1:
                                price = 7
                            else:
                                price = 15
                        else:
                            price = 0

                        x = ((window_width//2 + 50*1.5) - (self.amount_of_items * (50*2))) + 200*i

                        self.items.append(itemClass.Item(random_item[0], random_item[1], random_item[2], x, price=price, type=type, id=random_int, description=random_item[3]))

                else:
                    for item in self.placeholder:
                        self.items.append(item)

                self.items_spawned = True

            if type == "pickup":
                if self.pickup_placeholder == None:
                    if character.luck < 4:
                        chance = random.randint(1, 4 - character.luck)
                    else:
                        chance = 1

                    if chance == 1:
                        random_int = random.randint(0, len(pickup_list) - 1)
                        random_pickup = pickup_list[random_int]
                        for item in character.items:
                            if item.name == "bogo bombs":
                                if random_pickup[0] == "bomb":
                                    self.pickup_quantity = 2
                        for i in range(self.pickup_quantity):
                            self.pickups.append(itemClass.Item(random_pickup[0], random_pickup[1], random_pickup[2], x = window_width//2 - 15 + i*20, y = window_height//2 - 15 + i*5, width=30, height=30, type="pickup"))
                else:
                    for pickup in self.pickup_placeholder:
                        self.pickups.append(pickup)

                self.pickups_spawned = True
        else:
            for i in item_list:
                if name == i[0]:
                    self.items.append(itemClass.Item(i[0], i[1], i[2], x=x, y=y))
                    break
            
            for i in pickup_list:
                if name == i[0]:
                    self.pickups.append(itemClass.Item(i[0], i[1], i[2], x=x, y=y, type="pickup"))