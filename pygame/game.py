import pygame
import random
import src
from src.items import item_list
from settings import window_width, window_height
import src.projectile

pygame.init()

window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Game")

clock = pygame.time.Clock()
                
def redrawGameWindow():
    map.draw(window)
    for room in rooms:
        if room.room_index == current_room:
            room.draw(window)
            for item in room.items:
                item.draw(window)
            for door in room.doors:
                door.draw(window)
    for enemy in enemies:
        enemy.draw(window)
    isaac.draw(window)
    for tear in tears:
        tear.draw(window)
    isaac.drawHealthbar(window)
    if debug_mode:
        pygame.draw.line(window, (0, 0, 255), (window_width//2, window_height), (window_width//2, 0))
        pygame.draw.line(window, (0, 0, 255), (0, window_height//2), (window_width, window_height//2))
    if pause:
        pygame.draw.rect(window, "black", (window_width//4, window_height//4, window_width//2, window_height//2))

    pygame.display.update()

def checkCollision(object1, object2, mode = 1):
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

def enemiesSpawn(number_of_enemies):
    for i in range(0, number_of_enemies):
        spawn_x = random.randint(map.left_wall.width + 100, map.right_wall.x - 100)
        spawn_y = random.randint(map.upper_wall.height + 100, map.bottom_wall.y - 100)
        if spawn_x == isaac.x or spawn_y == isaac.y:
            for j in range(100):
                spawn_x = random.randint(map.left_wall.width, map.right_wall.x)
                spawn_y = random.randint(map.upper_wall.height, map.bottom_wall.y)
        else:
            enemies.append(src.enemy.Enemy(spawn_x, spawn_y, 50, 50, map.walls))

def itemsSpawn():
    for room in rooms:
        for i in range(room.amount_of_items):
            random_int = random.randint(0, len(item_list) - 1)
            random_item = item_list[random_int]
            room.items.append(src.item.Item(random_item[0], random_item[1]))

        for item_id, item in enumerate(room.items):
            if not item.hide:
                if room.amount_of_items != 1:
                    if room.amount_of_items % 2 == 0:
                        item.x = ((window_width//2 + item.width*1.5) - (room.amount_of_items * (item.width*2))) + 200*item_id
                    else:
                        item.x = ((window_width//2 + item.width*1.5) - (room.amount_of_items * (item.width*2))) + 200*item_id

cooldown_reset_event = pygame.USEREVENT + 1
damage_cooldown_reset_event = pygame.USEREVENT + 2
custom_sprite_event = pygame.USEREVENT + 3

on_cooldown = False
damage_cooldown = False
src.player.custom_sprite = False

debug_mode = True

# MAIN LOOP
# |-----------------------------------------------------------------------------------|
map = src.mapClass.Map(window_width, window_height)
isaac = src.player.Player(window_width//2 - 28, window_height//2 - 33)
rooms = map.rooms
tears = []
enemies = []
items = []
current_room = [5, 5]

itemsSpawn()

if debug_mode:
    for x in range(len(map.layout)):
        print(map.layout[x])
    for object in map.rooms:
        print(object)

run = True
pause = False
while run:
    clock.tick(60)

    isaac.stationary = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key ==  pygame.K_ESCAPE:
                if pause:
                    pause = False
                else:
                    pause = True

        if event.type == cooldown_reset_event:
            on_cooldown = False
            pygame.time.set_timer(cooldown_reset_event, 0)
        if event.type == damage_cooldown_reset_event:
            damage_cooldown = False
            pygame.time.set_timer(damage_cooldown_reset_event, 0)
        if event.type == custom_sprite_event:
            src.player.custom_sprite = False
            pygame.time.set_timer(custom_sprite_event, 0)

    for tear in tears:
        if tear.x < window_width and tear.x > 0 and tear.y < window_height and tear.y > 0:
            if tear.direction == "up":
                tear.y -= tear.speed
            elif tear.direction == "down":
                tear.y += tear.speed
            elif tear.direction == "left":
                tear.x -= tear.speed
            elif tear.direction == "right":
                tear.x += tear.speed
        else:
            tears.pop(tears.index(tear))

        for enemy in enemies:
            if checkCollision(tear, enemy):
                tears.pop(tears.index(tear))
                enemy.hit()
            if enemy.dead:
                enemies.pop(enemies.index(enemy))

    for enemy in enemies:
        if checkCollision(isaac, enemy):
            if not damage_cooldown:
                isaac.hit()
                damage_cooldown = True
                pygame.time.set_timer(damage_cooldown_reset_event, 1000)
                if not isaac.dead:
                    src.player.custom_sprite = True
                    pygame.time.set_timer(custom_sprite_event, 1000)


    for room in rooms:
        if room.room_index == [5, 5]:
            room.visited = True

        for door in room.doors:
            if enemies:
                door.closed = True
            else:
                door.closed = False

            if map.layout[room.room_x][room.room_y] == 2 and len(room.doors) == 1:
                door.is_treasure = True
            if map.layout[room.room_x][room.room_y] == 3 and len(room.doors) == 1:
                door.is_boss = True

            for i in range(4):
                if door.localisation == 1:
                    if map.layout[room.room_x - 1][room.room_y] == 2:
                        door.is_treasure = True
                    if map.layout[room.room_x - 1][room.room_y] == 3:
                        door.is_boss = True

                if door.localisation == 2:
                    if map.layout[room.room_x][room.room_y + 1] == 2:
                        door.is_treasure = True
                    if map.layout[room.room_x][room.room_y + 1] == 3:
                        door.is_boss = True

                if door.localisation == 3:
                    if map.layout[room.room_x + 1][room.room_y] == 2:
                        door.is_treasure = True
                    if map.layout[room.room_x + 1][room.room_y] == 3:
                        door.is_boss = True
                        
                if door.localisation == 4:
                    if map.layout[room.room_x][room.room_y - 1] == 2:
                        door.is_treasure = True
                    if map.layout[room.room_x][room.room_y - 1] == 3:
                        door.is_boss = True

        if room.room_index == current_room:
            if not room.visited:
                for door in room.doors:
                    door.closing = True
                if room.room_type == 1:
                    enemiesSpawn(room.number_of_enemies)
                    room.visited = True
                if room.room_type == 3:
                    enemies.append(src.enemy.Enemy(400, 400, 200, 200, map.walls))
                    room.visited = True

            if checkCollision(isaac, room.doors):
                door_collision = True
            else:
                door_collision = False

            for item in room.items:
                if enemies:
                    item.hide = True
                else:
                    item.hide = False
                
                if checkCollision(isaac, item):
                    item.effect(isaac)
                    room.items.remove(item)

            if isaac.y <= 0:
                isaac.x = window_width//2 - isaac.width//2
                isaac.y = window_height - 100
                current_room[0] -= 1
            if isaac.x >= window_width:
                isaac.x = 100 - isaac.width//2
                isaac.y = window_height//2 - isaac.height//2
                current_room[1] += 1
            if isaac.y >= window_height:
                isaac.x = window_width//2 - isaac.width//2
                isaac.y = 100 - isaac.height//2
                current_room[0] += 1
            if isaac.x <= 0:
                isaac.x = window_width - 100
                isaac.y = window_height//2 - isaac.height//2
                current_room[1] -= 1
    print(pause)
    keys = pygame.key.get_pressed()
    if isaac.dead == False:
        if keys[pygame.K_a]:
            if not checkCollision(isaac, map.left_wall) or door_collision and not enemies:
                isaac.x -= isaac.speed
            if not keys[pygame.K_d]:
                isaac.stationary = False
            isaac.frame = 2
        if keys[pygame.K_d]:
            if not checkCollision(isaac, map.right_wall) or door_collision and not enemies:
                isaac.x += isaac.speed
            if not keys[pygame.K_a]:
                isaac.stationary = False
            isaac.frame = 3
        if keys[pygame.K_s]:
            if not checkCollision(isaac, map.bottom_wall) or door_collision and not enemies:
                isaac.y += isaac.speed
            if not keys[pygame.K_w]:
                isaac.stationary = False
            if not (keys[pygame.K_w] and keys[pygame.K_s]):
                isaac.frame = 0
        if keys[pygame.K_w]:
            if not checkCollision(isaac, map.upper_wall) or door_collision and not enemies:
                isaac.y -= isaac.speed
            if not keys[pygame.K_s]:
                isaac.stationary = False
            if not (keys[pygame.K_w] and keys[pygame.K_s]):
                isaac.frame = 1
        if isaac.stationary:
            isaac.frame = 0

        if keys[pygame.K_UP]:
            isaac.frame = 1
            if not on_cooldown:
                tears.append(src.projectile.Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "up"))
                on_cooldown = True
                pygame.time.set_timer(cooldown_reset_event, 1000//isaac.attack_speed)

        elif keys[pygame.K_DOWN]:
            isaac.frame = 0
            if not on_cooldown:
                tears.append(src.projectile.Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "down"))
                on_cooldown = True
                pygame.time.set_timer(cooldown_reset_event, 1000//isaac.attack_speed)

        elif keys[pygame.K_LEFT]:
            isaac.frame = 2
            if not on_cooldown:
                tears.append(src.projectile.Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "left"))
                on_cooldown = True
                pygame.time.set_timer(cooldown_reset_event, 1000//isaac.attack_speed)

        elif keys[pygame.K_RIGHT]:
            isaac.frame = 3
            if not on_cooldown:
                tears.append(src.projectile.Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "right"))
                on_cooldown = True
                pygame.time.set_timer(cooldown_reset_event, 1000//isaac.attack_speed)

        if debug_mode == True:
            if keys[pygame.K_SPACE]:
                enemies = []
            if keys[pygame.K_z]:
                for x in range(11):
                    for y in range(11):
                        if map.layout[x][y] == 2:
                            current_room = [x, y]
                            break
            if keys[pygame.K_x]:
                for x in range(11):
                    for y in range(11):
                        if map.layout[x][y] == 3:
                            current_room = [x, y]
                            break
    redrawGameWindow()

pygame.quit()