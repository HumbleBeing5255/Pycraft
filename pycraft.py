import sys
import pygame as pg
from collections import deque
pg.init()
clock=pg.time.Clock()
scw,sch,bls=1000,700,20
world_width=100
xspeed_pl,yspeed_pl,stand,mid_x,mid_y,block_list=0,0,True,scw//2,sch//2,deque([])
white=(255,255,255)
black=(0,0,0)
xofs=0
font=pg.font.Font(None,50)
mouse_down=False
screen=pg.display.set_mode((scw,sch))
block_rect=pg.rect.Rect(0,0,bls,bls)
block_surface=pg.transform.scale(pg.image.load("dirt_block.jpg").convert(),(bls,bls))
for h in range(world_width*-1,world_width):
    for v in range(1//bls,(sch//bls)+1):
        if v*bls<=mid_y:
            block_list.append([0,h*bls,v*bls])
        else:
            block_list.append([1,h*bls,v*bls])
def block_render():
    global mouse_down
    for i in range(len(block_list)):
        keys=pg.key.get_pressed()
        if keys[pg.K_a]:
            block_list[i][1]+=5
        if keys[pg.K_d]:
            block_list[i][1]-=5
        if abs(block_list[i][1])<550:
            if block_list[i][0]!=0:
                screen.blit(block_surface,(block_list[i][1]+mid_x-(bls/2),block_list[i][2]))
            block_rect.topleft=(block_list[i][1]+mid_x-(bls/2),block_list[i][2])
            if block_rect.collidepoint(pg.mouse.get_pos()):
                pg.draw.rect(screen,black,block_rect,2)
                if mouse_down:
                    if block_list[i][0]==0:
                        block_list[i][0]=1
                    elif block_list[i][0]==1:
                        block_list[i][0]=0
                    mouse_down=False
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
    screen.fill((0,200,255))
    block_render()
    ms_text=font.render(str(pg.time.get_ticks()-start_time),True,white)
    screen.blit(ms_text,(20,20))
    pg.display.flip()
    clock.tick(30)




