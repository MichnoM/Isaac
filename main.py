import pygame
import src
from settings import window_width, window_height, debug_mode
import eventHandler
import globals

pygame.init()

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
window = pygame.display.set_mode((window_width, window_height), pygame.SCALED)
gui = src.gui.Gui()
pygame.display.set_caption("The Binding of Isaac")

font = pygame.sysfont.SysFont("arial", 40, True)

shading = pygame.image.load("sprites/shade.png")
shading = pygame.transform.scale(shading, (window_width*1.1, window_height*1.15)).convert_alpha()
shading.set_alpha(240)

title_menu = pygame.image.load("sprites/ui/titleMenu.png")
title_menu = pygame.transform.scale(title_menu, (globals.window_width, globals.window_height)).convert_alpha()

background = pygame.Surface((globals.window_width, globals.window_height), pygame.SRCALPHA)
screen = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

clock = pygame.time.Clock()
                
def redrawGameWindow():
    if not main_menu:
        window.blit(background, (0, 0))
        map.draw(screen)
        screen.blit(shading, (-60, -55))
        for room in map.rooms:
            for pickup in room.pickups:
                pickup.draw(screen)
        isaac.draw(screen)
        for room in map.rooms:
            for item in room.items:
                item.draw(screen)
            for enemy in room.enemies:
                enemy.draw(screen)
            for tear in room.tears:
                tear.draw(screen)

        background.fill((15,15,15))
        window.blit(screen, (map.x, map.y))
        gui.draw(window, isaac, pause, map, current_button, debug_mode)
        # fps = gui.render(f"{round(clock.get_fps())}", font)
        # window.blit(fps, (globals.window_width - 50, 0))
    else:
        window.blit(title_menu, (0, 0))

    pygame.display.update()

# MAIN LOOP
# |-----------------------------------------------------------------------------------|
map = src.map.Map(window_width, window_height)
isaac = src.player.Player(window_width//2, window_height//2)
event_handler = eventHandler.eventHandler(map, isaac, window, monitor_size, background, title_menu)

if debug_mode:
    isaac.damage = 10
    isaac.speed = 15
    isaac.attack_speed = 5
    isaac.luck = 4
    isaac.coins = 50
    isaac.shot_speed += 0.3
    isaac.range = 10
    isaac.size = 1

run = True
pause = False
main_menu = True

while run:
    clock.tick(60)
    run, pause, window, background, current_button, main_menu, title_menu, debug_mode = event_handler.eventHandling()
    globals.window_width = window.get_width()
    globals.window_height = window.get_height()

    if not pause and not main_menu:
        map.update(isaac)
        isaac.update()
            
        if not map.room_change:
            for room in map.rooms:
                if room == map.current_room:
                    if not room.visited:
                        room.enemiesSpawn(room.number_of_enemies, isaac, map.walls)
                        room.visited = True
                    
                    if not room.items_spawned:
                        if room.type == "treasure" or room.type == "boss":
                            if not room.enemies:
                                room.itemsSpawn("item", isaac, map)
                        else:
                            room.itemsSpawn("shop item", isaac, map)

                    if (not room.pickups_spawned) and not room.enemies and room.type == "regular" and not room.spawn_room:
                        room.itemsSpawn("pickup", isaac, map)
                    
                    for item in room.items:
                        if map.checkCollision(isaac, item):
                            if room.type == "shop":
                                if isaac.coins >= item.price:
                                    item.pickup(isaac)
                            else:
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

            # CHEATS
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

                if keys[pygame.K_v]:
                    for x in range(len(map.layout)):
                        print(map.layout[x])
                    for object in map.rooms:
                        print(object)
                        for item in object.items:
                            print(item)
                        for pickup in object.pickups:
                            print(pickup)
                
                if keys[pygame.K_b]:
                    print(isaac.items)
                    print(isaac.x, isaac.y)
                            
    redrawGameWindow()

pygame.quit()