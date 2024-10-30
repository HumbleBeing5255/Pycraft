import sys
import pygame as pg
from collections import deque
pg.init()
clock = pg.time.Clock()
scw, sch, bls = 1000, 700, 50
world_width = 100
collide_left=False
collide_right=False
xspeed_pl, yspeed_pl, stand, mouse_down, mid_x, mid_y, block_list, block_list_y, xofs,white, black = 0, 0, True, False, scw // 2, sch // 2, deque([]), deque([]),0, (255, 255, 255), (0, 0, 0)
font = pg.font.Font(None, 50)
screen = pg.display.set_mode((scw, sch))
block_rect = pg.rect.Rect(0, 0, bls, bls)
player_rect = pg.rect.Rect(mid_x, mid_y - bls * 4, bls * 0.9, bls * 1.8)
cloud_background=pg.transform.scale(pg.image.load("cloud_background.jpg"), (scw,sch))
player_surface = pg.transform.scale(pg.image.load("Steve.webp"), (player_rect.width, player_rect.height))
dirt_block_surface = pg.transform.scale(pg.image.load("dirt_block.jpg").convert(), (bls, bls))
stone_block_surface = pg.transform.scale(pg.image.load("stone_block.jpg").convert(), (bls, bls))
dirt_item_display=pg.transform.scale(pg.image.load("dirt_item.webp"), (60, 60))
stone_iitem_display=pg.transform.scale(pg.image.load("stone_item.png"), (60, 60))
pickaxe_item_display=pg.transform.scale(pg.image.load("pickaxe_item.jpg"), (60, 60))

# world creation
for h in range(world_width*-1,world_width):
    block_list_y=[]
    for v in range(-1,(sch//bls)):
        if v*bls>=sch/1.5:
            block_list_y.append([2,h*bls,v*bls])
        elif v*bls>=sch/2:
            block_list_y.append([1,h*bls,v*bls])
        else:
            block_list_y.append([0,h*bls,v*bls])
    block_list.append(block_list_y)
print(f"World width: {len(block_list)}\nWorld hight: {len(block_list[0])}")


def block_render():
    global mouse_down, xofs,yspeed_pl, stand, collide_left,collide_right
    for h in range(len(block_list)):
        if abs(block_list[h][0][1] + xofs) < 550:
            for v in range(len(block_list[0])):
                # Finds the top left corner of the block right below the player.
                block_rect.topleft = (block_list[h][v][1] + xofs + mid_x - (bls // 2), block_list[h][v][2] + bls)
                if block_list[h][v][0] != 0:
                    if block_list[h][v][0]==1:
                        screen.blit(dirt_block_surface,(block_list[h][v][1]+xofs+mid_x-(bls//2),block_list[h][v][2]+bls))
                    elif block_list[h][v][0]==2:
                        screen.blit(stone_block_surface,(block_list[h][v][1]+xofs+mid_x-(bls//2),block_list[h][v][2]+bls))

                    # Collisions
                    if player_rect.colliderect(block_rect):
                        # Check how far the player is from the top of the block defined earlier.
                        distance_to_top = player_rect.bottom - block_rect.top


                        # Floor collisions
                        # If the distance is less than or equal to half the block height, adjust the player position
                        if distance_to_top <= bls * 0.5:
                            player_rect.y = block_rect.y - player_rect.height + 1
                            yspeed_pl = 0
                            stand = True

                        # Ceiling Collisions. Implement the same as floor but flipped. You will probably need another version of block_rect to achieve this.

                        # Wall Collisions
                        else:
                            # Nudge the player based on collision on the left or right side
                            if player_rect.right > block_rect.left and player_rect.left < block_rect.left:
                                #player_rect.right = block_rect.left  # Nudge player to the left
                                collide_right=True
                            elif player_rect.left < block_rect.right and player_rect.right > block_rect.right:
                                #player_rect.left = block_rect.right  # Nudge player to the right
                                collide_left=True

                        if distance_to_top>=player_rect.height and abs(player_rect.x-block_rect.x)<bls/1.2 and stand==False:
                            player_rect.y+=abs(yspeed_pl)+1
                            yspeed_pl=0
                            pg.draw.rect(screen,black,block_rect,2)
                if block_rect.collidepoint(pg.mouse.get_pos()):
                    pg.draw.rect(screen, black, block_rect, 2)
                    if mouse_down:
                        if block_list[h][v][0] == 0:
                            block_list[h][v][0] = 1
                        elif block_list[h][v][0] == 1:
                            block_list[h][v][0] = 0
                        elif block_list[h][v][0] == 2:
                            block_list[h][v][0] = 0
                        mouse_down = False


def player_render():
    global stand, yspeed_pl,xofs,collide_left,collide_right
    yspeed_pl -= bls * 0.0065
    player_rect.y -= yspeed_pl
    keys = pg.key.get_pressed()
    if stand:
        if keys[pg.K_SPACE]:
            player_rect.y -= 1
            yspeed_pl = 6
            stand = False
    if keys[pg.K_a]:
        xofs+=4
        if collide_left:
            xofs -= 4
            collide_left=False
    if keys[pg.K_d]:
        xofs-=4
        if collide_right:
            xofs+=4
            collide_right=False
        collide_right=False
    screen.blit(player_surface, player_rect)
    pg.draw.rect(screen, black, player_rect, 2)


# main loop
while True:
    start_time = pg.time.get_ticks()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_down = True
        if event.type == pg.MOUSEBUTTONUP:
            mouse_down = False
    #screen.fill((0, 150, 255))
    screen.blit(cloud_background,(0,0))
    block_render()
    player_render()
    ms_text = font.render(str(pg.time.get_ticks() - start_time), True, white)
    screen.blit(dirt_item_display,(300,sch-dirt_item_display.height))
    screen.blit(stone_iitem_display,(380,sch-stone_iitem_display.height))
    screen.blit(pickaxe_item_display,(220,sch-pickaxe_item_display.height))
    screen.blit(ms_text, (20, 20))
    pg.display.flip()
    clock.tick(60)