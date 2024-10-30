import sys
import pygame as pg
from collections import deque
pg.init()
clock=pg.time.Clock()
scw,sch,bls=1000,700,40
world_width=100
xspeed_pl,yspeed_pl,stand,mouse_down,mid_x,mid_y,block_list,block_list_y,xofs,white,black=0,0,True,False,scw//2,sch//2,deque([]),deque([]),0,(255,255,255),(0,0,0)
font=pg.font.Font(None,50)
screen=pg.display.set_mode((scw,sch))
block_rect=pg.rect.Rect(0,0,bls,bls)
player_rect=pg.rect.Rect(mid_x,mid_y-bls*4,bls*0.9,bls*1.8)
player_surface=pg.transform.scale(pg.image.load("Steve.webp"),(player_rect.width,player_rect.height))
dirt_block_surface=pg.transform.scale(pg.image.load("dirt_block.jpg").convert(),(bls,bls))
stone_block_surface=pg.transform.scale(pg.image.load("stone_block.jpg").convert(),(bls,bls))
def block_render():
    global mouse_down,xofs,yspeed_pl,stand,xofs
    for h in range(len(block_list)):
        if abs(block_list[h][0][1]+xofs)<550:
            for v in range(len(block_list[0])):
                block_rect.topleft=(block_list[h][v][1]+xofs+mid_x-(bls//2),block_list[h][v][2]+bls)
                if block_list[h][v][0]!=0:
                    if block_list[h][v][0]==1:
                        screen.blit(dirt_block_surface,(block_list[h][v][1]+xofs+mid_x-(bls//2),block_list[h][v][2]+bls))
                    elif block_list[h][v][0]==2:
                        screen.blit(stone_block_surface,(block_list[h][v][1]+xofs+mid_x-(bls//2),block_list[h][v][2]+bls))
                    if player_rect.colliderect(block_rect):
                        if player_rect.bottom>block_rect.top:
                            player_rect.y=block_rect.y-player_rect.height+1
                            yspeed_pl=0
                            stand=True
                if block_rect.collidepoint(pg.mouse.get_pos()):
                    pg.draw.rect(screen,black,block_rect,2)
                    if mouse_down:
                        if block_list[h][v][0] == 0:
                            block_list[h][v][0] = 1
                        elif block_list[h][v][0] == 1:
                            block_list[h][v][0] = 0
                        elif block_list[h][v][0] == 2:
                            block_list[h][v][0] = 0
                        mouse_down = False
def player_render():
    global stand,yspeed_pl,xofs
    yspeed_pl-=0.3
    player_rect.y-=yspeed_pl
    keys = pg.key.get_pressed()
    if stand:
        if keys[pg.K_SPACE]:
            player_rect.y-=1
            yspeed_pl = 6
            stand = False
            print("Jump")
    if keys[pg.K_a]:
        xofs += 2
    if keys[pg.K_d]:
        xofs -= 2
    screen.blit(player_surface,player_rect)
    pg.draw.rect(screen,black,player_rect,2)
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