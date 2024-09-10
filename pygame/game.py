import pygame
import random
import src
from src.items import item_list
from settings import window_width, window_height, debug_mode
import src.projectile

pygame.init()

window = pygame.display.set_mode((window_width, window_height))
font = pygame.font.SysFont("None", 30)

pygame.display.set_caption("Game")

clock = pygame.time.Clock()
                
def redrawGameWindow():
    map.draw(window)
    for room in map.rooms:
        if room.room_index == map.current_room:
            room.draw(window)
            for item in room.items:
                item.draw(window)
            for door in room.doors:
                door.draw(window)
        for enemy in room.enemies:
            enemy.draw(window)
    isaac.draw(window)
    for tear in tears:
        tear.draw(window)
    isaac.drawHealthbar(window)
    if debug_mode:
        pygame.draw.line(window, (0, 0, 255), (window_width//2, window_height), (window_width//2, 0))
        pygame.draw.line(window, (0, 0, 255), (0, window_height//2), (window_width, window_height//2))
        for wall in map.walls:
            pygame.draw.rect(window, (255, 0, 0), wall, 2)
    if pause:
        label = font.render(f"Damage: {isaac.damage}, Attack Speed: {isaac.attack_speed}, Speed: {isaac.speed}", 1, (255, 255, 255))
        menu = pygame.Surface((window_width//2, window_height//2))
        menu.blit(label, (menu.get_width()//10, menu.get_width()//10))
        window.blit(menu, (window_width//4, window_height//4, window_width//2, window_height//2))

    pygame.display.update()

cooldown_event = pygame.USEREVENT + 1
damage_cooldown_event = pygame.USEREVENT + 2
head_animation_event = pygame.USEREVENT + 3
body_animation_cooldown_event = pygame.USEREVENT + 4
hurt_animation_event = pygame.USEREVENT + 5

on_cooldown = False
damage_cooldown = False
head_animation = False
body_animation_cooldown = False

# MAIN LOOP
# |-----------------------------------------------------------------------------------|
map = src.map.Map(window_width, window_height)
isaac = src.player.Player(window_width//2, window_height//2)
tears = []

if debug_mode:
    isaac.damage = 10
    isaac.speed = 15
    isaac.attack_speed = 5
    for x in range(len(map.layout)):
        print(map.layout[x])
    for object in map.rooms:
        print(object)

run = True
pause = False
while run:
    clock.tick(60)

    isaac.stationary = True
    door_collision = False
    door_frame_collision = [False, False, False, False]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key ==  pygame.K_ESCAPE:
                if pause:
                    pause = False
                else:
                    pause = True

        if event.type == cooldown_event:
            on_cooldown = False
            pygame.time.set_timer(cooldown_event, 0)
        if event.type == damage_cooldown_event:
            damage_cooldown = False
            pygame.time.set_timer(damage_cooldown_event, 0)
        if event.type == head_animation_event:
            head_animation = False
            pygame.time.set_timer(head_animation_event, 0)
        if event.type == body_animation_cooldown_event:
            body_animation_cooldown = False
            pygame.time.set_timer(body_animation_cooldown_event, 0)
        if event.type == hurt_animation_event:
            isaac.hurt = False
            pygame.time.set_timer(hurt_animation_event, 0)

    map.roomChange(isaac)
    if not pause:
        for tear in tears:
            if not map.checkCollision(tear, map.walls):
                tear.move()
            else:
                tear.delete(tears)

        for room in map.rooms:
            if room.room_index == [5, 5]:
                room.visited = True

            for door in room.doors:
                if not room.enemies:
                    door.open()
                else:
                    door.close()
                door.update()

            if room.room_index == map.current_room:
                if not room.enemies:
                    room_empty = True
                else:
                    room_empty = False
                for enemy in room.enemies:
                    enemy.move(map.walls)
                    if enemy.dead:
                        room.enemies.pop(room.enemies.index(enemy))
                    if not isaac.dead:
                        if map.checkCollision(isaac, enemy):
                            if not damage_cooldown:
                                isaac.hit()
                                damage_cooldown = True
                                pygame.time.set_timer(damage_cooldown_event, 1000)
                                pygame.time.set_timer(hurt_animation_event, isaac.hurt_animation_duration)
                                
                    for tear in tears:
                        if map.checkCollision(tear, enemy):
                            tears.pop(tears.index(tear))
                            enemy.hit(isaac.damage)

                if not room.visited:
                    room.itemsSpawn(item_list)
                    if room.room_type != 3:
                        room.enemiesSpawn(room.number_of_enemies, isaac, map.walls)
                        room.visited = True
                    else:
                        room.enemies.append(src.enemy.Enemy(400, 400, 200, 200))
                        room.visited = True

                if map.checkCollision(isaac, room.doors):
                    door_collision = True
                    for door in room.doors:
                        if door.localisation == 1 or door.localisation == 3:
                            if isaac.y < 40 or isaac.y + isaac.height > window_height - 40:
                                if isaac.x < door.x:
                                    door_frame_collision[3] = True
                                if isaac.x + isaac.width > door.x + door.width:
                                    door_frame_collision[1] = True

                        if door.localisation == 2 or door.localisation == 4: 
                            if isaac.x < 40 or isaac.x > window_width - 40:
                                if isaac.y < door.y:
                                    door_frame_collision[0] = True
                                if isaac.y + isaac.height > door.y + door.height:
                                    door_frame_collision[2] = True

                for item in room.items:
                    if room.enemies:
                        item.hide = True
                    else:
                        item.hide = False
                    
                    if not item.hide:
                        if map.checkCollision(isaac, item):
                            item.effect(isaac)
                            room.items.remove(item)

        keys = pygame.key.get_pressed()

        if isaac.dead == False:
            if keys[pygame.K_a]:
                if not keys[pygame.K_d]:
                    if not (keys[pygame.K_w] != keys[pygame.K_s]):
                        if isaac.body_frame <= 19:
                            isaac.body_frame = 20
                        if not body_animation_cooldown:
                            isaac.body_frame += 1
                            body_animation_cooldown = True
                            pygame.time.set_timer(body_animation_cooldown_event, isaac.body_animation_duration)
                        if isaac.body_frame > 29:
                            isaac.body_frame = 20

                    if not map.checkCollision(isaac, map.left_wall) or (door_collision and room_empty):
                        if not door_frame_collision[3]:
                            isaac.x -= isaac.speed
                        if map.checkCollision(isaac, map.left_wall) and not (door_collision and room_empty):
                            isaac.x = map.left_wall.x + map.left_wall.width

                    isaac.stationary = False
                if not head_animation:
                    isaac.head_frame = 6

            if keys[pygame.K_d]:
                if not keys[pygame.K_a]:
                    if not (keys[pygame.K_w] != keys[pygame.K_s]):
                        if isaac.body_frame <= 9:
                            isaac.body_frame = 10
                        if not body_animation_cooldown:
                            isaac.body_frame += 1
                            body_animation_cooldown = True
                            pygame.time.set_timer(body_animation_cooldown_event, isaac.body_animation_duration)
                        if isaac.body_frame > 19:
                            isaac.body_frame = 9

                    if not map.checkCollision(isaac, map.right_wall) or (door_collision and room_empty):
                        if not door_frame_collision[1]:
                            isaac.x += isaac.speed
                        if map.checkCollision(isaac, map.right_wall) and not (door_collision and room_empty):
                            isaac.x = map.right_wall.x - isaac.width

                    isaac.stationary = False
                if not head_animation:
                    isaac.head_frame = 2

            if keys[pygame.K_s]:
                if not keys[pygame.K_w]:
                    if not body_animation_cooldown:
                        isaac.body_frame += 1
                        body_animation_cooldown = True
                        pygame.time.set_timer(body_animation_cooldown_event, isaac.body_animation_duration)
                        if isaac.body_frame > 9:
                            isaac.body_frame = 0

                    if not map.checkCollision(isaac, map.bottom_wall) or (door_collision and room_empty):
                        if not door_frame_collision[2]:
                            isaac.y += isaac.speed
                        if map.checkCollision(isaac, map.bottom_wall) and not (door_collision and room_empty):
                            isaac.y = map.bottom_wall.y - isaac.height

                    isaac.stationary = False
                if not (keys[pygame.K_w] and keys[pygame.K_s]):
                    if not head_animation:
                        isaac.head_frame = 0

            if keys[pygame.K_w]:
                if not keys[pygame.K_s]:
                    if not body_animation_cooldown:
                        isaac.body_frame += 1
                        body_animation_cooldown = True
                        pygame.time.set_timer(body_animation_cooldown_event, isaac.body_animation_duration)
                    if isaac.body_frame > 9:
                        isaac.body_frame = 0

                    if not map.checkCollision(isaac, map.upper_wall) or (door_collision and room_empty):
                        if not door_frame_collision[0]:
                            isaac.y -= isaac.speed
                        if map.checkCollision(isaac, map.upper_wall) and not (door_collision and room_empty):
                            isaac.y = map.upper_wall.y + map.upper_wall.height
                        
                    isaac.stationary = False
                if not (keys[pygame.K_w] and keys[pygame.K_s]):
                    if not head_animation:
                        isaac.head_frame = 4

            if isaac.stationary:
                if not head_animation:
                    isaac.head_frame = 0
                isaac.body_frame = 0

            if keys[pygame.K_UP]:
                if not head_animation:
                    isaac.head_frame = 4
                if not on_cooldown:
                    isaac.head_frame = 5
                    tears.append(src.projectile.Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "up"))
                    on_cooldown = True
                    head_animation = True
                    pygame.time.set_timer(cooldown_event, 1000//isaac.attack_speed)
                    pygame.time.set_timer(head_animation_event, isaac.head_animation_duration)

            elif keys[pygame.K_DOWN]:
                if not head_animation:
                    isaac.head_frame = 0
                if not on_cooldown:
                    isaac.head_frame = 1
                    tears.append(src.projectile.Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "down"))
                    on_cooldown = True
                    head_animation = True
                    pygame.time.set_timer(cooldown_event, 1000//isaac.attack_speed)
                    pygame.time.set_timer(head_animation_event, isaac.head_animation_duration)

            elif keys[pygame.K_LEFT]:
                if not head_animation:
                    isaac.head_frame = 6
                if not on_cooldown:
                    isaac.head_frame = 7
                    tears.append(src.projectile.Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "left"))
                    on_cooldown = True
                    head_animation = True
                    pygame.time.set_timer(cooldown_event, 1000//isaac.attack_speed)
                    pygame.time.set_timer(head_animation_event, isaac.head_animation_duration)

            elif keys[pygame.K_RIGHT]:
                if not head_animation:
                    isaac.head_frame = 2
                if not on_cooldown:
                    isaac.head_frame = 3
                    tears.append(src.projectile.Projectile(round(isaac.x + isaac.width//2), round(isaac.y + isaac.height//2), 10, (0,0,0), "right"))
                    on_cooldown = True
                    head_animation = True
                    pygame.time.set_timer(cooldown_event, 1000//isaac.attack_speed)
                    pygame.time.set_timer(head_animation_event, isaac.head_animation_duration)

        if debug_mode == True:
            if keys[pygame.K_SPACE]:
                for room in map.rooms:
                    room.enemies = []
            if keys[pygame.K_z]:
                for x in range(11):
                    for y in range(11):
                        if map.layout[x][y] == 2:
                            map.current_room = [x, y]
                            break
            if keys[pygame.K_x]:
                for x in range(11):
                    for y in range(11):
                        if map.layout[x][y] == 3:
                            map.current_room = [x, y]
                            break
    redrawGameWindow()

pygame.quit()