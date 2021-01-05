import pygame
import random
import os
import sys
from pygame.locals import *

pygame.init()

width, height = 1024, 768
screen = pygame.display.set_mode((width, height))

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path

persos = pygame.image.load(os.path.join(image_path, 'perso.png')).convert_alpha()

COLS=3
ROWS=4

perso = [None] * (COLS*ROWS)
for i in range(COLS):
  for j in range(ROWS):
    perso[COLS*j+i] = pygame.Surface((32, 36), flags=HWSURFACE | SRCALPHA)
    perso[COLS*j+i].blit(persos, (0, 0), area=(32*i, 36*j, 32, 36))

NB_FRAMES=100

exit = False
moving = False
orient = 2
# Sprite 1 is the "rest" one. Adding NB_FRAMES-1 ensures the sprite is animated
# when moving no matter how small the movement is.
frame = 2*NB_FRAMES-1
pos = [100, 100]
while not exit:
    screen.fill(0)

    screen.blit(perso[orient*3 + (frame // NB_FRAMES) % 3], (pos[0], pos[1]))

    pygame.display.flip()
    if moving:
        frame += 1
        if frame % 10 == 0:
            if orient == 0:
              pos[1] -= 1
            elif orient == 1:
              pos[0] += 1
            elif orient == 2:
              pos[1] += 1
            elif orient == 3:
              pos[0] -= 1

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit = True
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
            if event.key == pygame.K_UP:
                orient = 0
                moving = True
            if event.key == pygame.K_DOWN:
                orient = 2
                moving = True
            if event.key == pygame.K_LEFT:
                orient = 3
                moving = True
            if event.key == pygame.K_RIGHT:
                orient = 1
                moving = True
        if event.type==pygame.KEYUP:
            if ((event.key == pygame.K_UP and orient == 0) or
                (event.key == pygame.K_DOWN and orient == 2) or
                (event.key == pygame.K_LEFT and orient == 3) or
                (event.key == pygame.K_RIGHT and orient == 1)):
                   moving = False
                   frame = 2*NB_FRAMES-1

pygame.quit()
