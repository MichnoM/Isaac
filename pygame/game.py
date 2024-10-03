import pygame
import src
from src.items import item_list, pickup_list, shop_items
from settings import window_width, window_height, debug_mode
import eventHandler

pygame.init()

window = pygame.display.set_mode((window_width, window_height))
gui = src.gui.Gui()
pygame.display.set_caption("Game")

clock = pygame.time.Clock()
                
def redrawGameWindow():
    background = pygame.Surface((window_width, window_height))
    screen = pygame.Surface((window_width, window_height))
    map.draw(screen)
    isaac.draw(screen)
    window.blit(background, (0, 0))
    window.blit(screen, (map.x, map.y))
    gui.draw(window, isaac, pause)

    pygame.display.update()

# MAIN LOOP
# |-----------------------------------------------------------------------------------|
map = src.map.Map(window_width, window_height)
isaac = src.player.Player(window_width//2, window_height//2)
event_handler = eventHandler.eventHandler(map, isaac)

if debug_mode:
    isaac.damage = 10
    isaac.speed = 15
    isaac.attack_speed = 5
    isaac.luck = 4
    isaac.items.append("piggy bank")
    for x in range(len(map.layout)):
        print(map.layout[x])
    for object in map.rooms:
        print(object)
        for door in object.doors:
            print(door.type)

run = True
pause = False
while run:
    clock.tick(60)

    run, pause = event_handler.eventHandling()

    if not pause:
        map.update(isaac)
        isaac.update()
            
        if not map.room_change:
            for room in map.rooms:
                if room == map.current_room:
                    if not room.visited:
                        room.enemiesSpawn(room.number_of_enemies, isaac, map.walls)
                        room.visited = True
                        
                    if not room.items_spawned:
                        if room.room_type == "treasure" or room.room_type == "boss":
                            if not room.enemies:
                                room.itemsSpawn("item", isaac)
                        else:
                            room.itemsSpawn("shop item", isaac)

                    if (not room.pickups_spawned) and not room.enemies and room.room_type == "regular" and not room.spawn_room:
                        room.itemsSpawn("pickup", isaac)
                    
                    for item in room.items:
                        if map.checkCollision(isaac, item):
                            item.pickup(isaac)
                    for pickup in room.pickups:
                        if map.checkCollision(isaac, pickup):
                            pickup.pickup(isaac)

                    for door in room.doors:
                        if map.checkCollision(isaac, door):
                            if not door.closed:
                                isaac.doorframeCollision(room)
                            if door.locked and isaac.keys > 0:
                                isaac.keys -= 1
                                door.locked = False
                        
            keys = pygame.key.get_pressed()
            if isaac.dead == False:
                if keys[pygame.K_a]:
                    if not keys[pygame.K_d]:
                        isaac.walk("left", map)
                        if not (keys[pygame.K_w] != keys[pygame.K_s]):
                            isaac.bodyAnimation("left")
                        isaac.headAnimation("left")

                if keys[pygame.K_d]:
                    if not keys[pygame.K_a]:
                        isaac.walk("right", map)
                        if not (keys[pygame.K_w] != keys[pygame.K_s]):
                            isaac.bodyAnimation("right")
                        isaac.headAnimation("right")

                if keys[pygame.K_s]:
                    if not keys[pygame.K_w]:
                        isaac.walk("down", map)
                        isaac.bodyAnimation("down")
                        isaac.headAnimation("down")

                if keys[pygame.K_w]:
                    if not keys[pygame.K_s]:
                        isaac.walk("up", map)
                        isaac.bodyAnimation("up")
                        isaac.headAnimation("up")

                if keys[pygame.K_UP]:
                    isaac.shoot("up", map)

                elif keys[pygame.K_DOWN]:
                    isaac.shoot("down", map)

                elif keys[pygame.K_LEFT]:
                    isaac.shoot("left", map)

                elif keys[pygame.K_RIGHT]:
                    isaac.shoot("right", map)

            if debug_mode == True:
                if keys[pygame.K_SPACE]:
                    for room in map.rooms:
                        room.enemies = []
                if keys[pygame.K_z]:
                    for x in range(11):
                        for y in range(11):
                            if map.layout[x][y] == 2:
                                map.current_room_index = [x, y]
                                break
                if keys[pygame.K_x]:
                    for x in range(11):
                        for y in range(11):
                            if map.layout[x][y] == 3:
                                map.current_room_index = [x, y]
                                break
                if keys[pygame.K_c]:
                    for x in range(11):
                        for y in range(11):
                            if map.layout[x][y] == 4:
                                map.current_room_index = [x, y]
                                break
                            
    redrawGameWindow()

pygame.quit()