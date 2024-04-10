
import pygame as pg

clock = pg.time.Clock()

FPS = 30

frames = ["frame1", "frame2", "frame3", "frame4"]


# x=0
# while True:
#     x = x%len(frames)
#     print(frames[x])
#     x+=1

x = 0
then = 0
current_frame = 0

while True:
    clock.tick(FPS)
    now = pg.time.get_ticks()
    if now - then > 200:
        # print(frames[current_frame])
        print(current_frame)
        current_frame = (current_frame + 1) % 4
    #     print(now)
    #     then = now
    # print(pg.time.get_ticks())

