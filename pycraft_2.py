import sys
import pygame as pg
from collections import deque
pg.init()
clock=pg.time.Clock()
scw,sch,bls=1000,700,30
world_width=100
xspeed_pl,yspeed_pl,stand,mouse_down,mid_x,mid_y,block_list,block_list_y,xofs,white,black=0,0,True,False,scw//2,sch//2,deque([]),deque([]),0,(255,255,255),(0,0,0)
font=pg.font.Font(None,50)
collide_foot=pg.USEREVENT+1
collide_head=pg.USEREVENT+2
collide_left=pg.USEREVENT+3
collide_right=pg.USEREVENT+4
screen=pg.display.set_mode((scw,sch))
block_rect=pg.rect.Rect(0,0,bls,bls)
player_rect=pg.rect.Rect(mid_x,mid_y-bls*2,bls*0.8,bls*1.6)
player_surface=pg.transform.scale(pg.image.load("Steve.webp"),(player_rect.width,player_rect.height))
block_surface=pg.transform.scale(pg.image.load("dirt_block.jpg").convert(),(bls,bls))
for h in range(world_width*-1,world_width):
    block_list_y=[]
    for v in range(-1,(sch//bls)-1):
        if v*bls>=mid_y:
            block_list_y.append([1,h*bls,v*bls])
        else:
            block_list_y.append([0,h*bls,v*bls])
    block_list.append(block_list_y)
def block_render():
    global mouse_down,xofs,yspeed_pl,stand
    for h in range(len(block_list)):
        if abs(block_list[h][0][1]+xofs)<550:
            for v in range(len(block_list[0])):
                if block_list[h][v][0]!=0:
                    screen.blit(block_surface,(block_list[h][v][1]+xofs+mid_x-(bls//2),block_list[h][v][2]+bls))
                    if player_rect.colliderect(block_rect):
                        pass

                        #This is where I would put the collision detection (from bottom, top, left and right)

                block_rect.topleft = (block_list[h][v][1]+xofs+mid_x-(bls//2),block_list[h][v][2]+bls)
                if block_rect.collidepoint(pg.mouse.get_pos()):
                    pg.draw.rect(screen,black,block_rect,2)
                    if mouse_down:
                        if block_list[h][v][0] == 0:
                            block_list[h][v][0] = 1
                        elif block_list[h][v][0] == 1:
                            block_list[h][v][0] = 0
                        mouse_down = False
def player_render():
    global stand,yspeed_pl,xofs
    player_rect.y-=yspeed_pl
    yspeed_pl-=0.

    #This is where I would handle the collisions

    keys = pg.key.get_pressed()
    if stand:
        if keys == pg.K_SPACE:
            yspeed_pl = 10
            stand = False
            print("jump")
    if keys[pg.K_a]:
        xofs += 5
    if keys[pg.K_d]:
        xofs -= 5
    screen.blit(player_surface,player_rect.topleft)
while True:
    start_time=pg.time.get_ticks()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type==pg.MOUSEBUTTONDOWN:
            mouse_down=True
        if event.type==pg.MOUSEBUTTONUP:
            mouse_down=False
    screen.fill((0,150,255))
    block_render()
    player_render()
    ms_text=font.render(str(pg.time.get_ticks()-start_time),True,white)
    screen.blit(ms_text,(20,20))
    pg.display.flip()
    clock.tick(60)