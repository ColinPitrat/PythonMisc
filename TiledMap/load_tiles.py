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

tiles = pygame.image.load(os.path.join(image_path, 'tiles.png')).convert_alpha()

COLS=16
# Lines 0 & 1 contain grass & path
ROWS=2
tile = [None] * (COLS*(ROWS+1))
for i in range(COLS):
  for j in range(ROWS):
    tile[COLS*j+i] = pygame.Surface((64, 32), flags=HWSURFACE | SRCALPHA)
    tile[COLS*j+i].blit(tiles, (0, 0), area=(64*i, 32*j, 64, 32))

# Lines 19 contains water
for i in range(COLS):
  tile[COLS*ROWS+i] = pygame.Surface((64, 32), flags=HWSURFACE | SRCALPHA)
  tile[COLS*ROWS+i].blit(tiles, (0, 0), area=(64*i, 32*19, 64, 32))

# 2 rows of objects + 16 trees
NB_OBJECTS=2*COLS+16
objects_sprites = [None] * NB_OBJECTS
# Lines 8 & 9 contain chests & barriers
# Lines 10 & 11 contain plants
for i in range(COLS):
  for j in range(2):
      objects_sprites[j*COLS+i] = pygame.Surface((64, 64), flags=HWSURFACE | SRCALPHA)
      objects_sprites[j*COLS+i].blit(tiles, (0, 0), area=(64*i, 32*8+64*j, 64, 64))
# Lines 31 -> 41 contain trees of different sizes
for i in range(4):
  objects_sprites[2*COLS+i] = pygame.Surface((128, 128), flags=HWSURFACE | SRCALPHA)
  objects_sprites[2*COLS+i].blit(tiles, (0, 0), area=(128*i, 32*31, 128, 128))
  objects_sprites[2*COLS+4+i] = pygame.Surface((128, 196), flags=HWSURFACE | SRCALPHA)
  objects_sprites[2*COLS+4+i].blit(tiles, (0, 0), area=(512+128*i, 32*36, 128, 196))
  objects_sprites[2*COLS+8+i] = pygame.Surface((128, 196), flags=HWSURFACE | SRCALPHA)
  objects_sprites[2*COLS+8+i].blit(tiles, (0, 0), area=(128*i, 32*31, 128, 196))
  objects_sprites[2*COLS+12+i] = pygame.Surface((128, 160), flags=HWSURFACE | SRCALPHA)
  objects_sprites[2*COLS+12+i].blit(tiles, (0, 0), area=(512+128*i, 32*37, 128, 160))

bridge_sprites = [None] * COLS
# Lines 20 & 21 contains bridges
for i in range(COLS):
  bridge_sprites[i] = pygame.Surface((64, 64), flags=HWSURFACE | SRCALPHA)
  bridge_sprites[i].blit(tiles, (0, 0), area=(64*i, 32*20, 64, 64))

MAP_WIDTH=50
MAP_HEIGHT=50

# Purely random map, looks foolish ...
random_landmap = [random.randint(0, len(tile)-1) for i in range(2*MAP_WIDTH*MAP_HEIGHT)]

# Create a grass only map
landmap = [
    random.randint(0, COLS-1) for i in range(2*MAP_WIDTH*MAP_HEIGHT)
]

# Create a diagonal path
for i in range(MAP_WIDTH):
    landmap[2*i*MAP_WIDTH+i] = random.randint(COLS+4, COLS+7)
    landmap[(2*i+1)*MAP_WIDTH+i] = random.randint(COLS+4, COLS+7)
    landmap[2*i*MAP_WIDTH+i+1] = random.randint(COLS+4, COLS+7)
    if i+1 < MAP_WIDTH:
        landmap[(2*i+1)*MAP_WIDTH+i+1] = random.randint(COLS+4, COLS+7)
    landmap[2*i*MAP_WIDTH+i+2] = random.randint(COLS+4, COLS+7)
    if i+2 < MAP_WIDTH:
        landmap[(2*i+1)*MAP_WIDTH+i+2] = random.randint(COLS+4, COLS+7)

# Create a lake
for i in range(10):
  for j in range(10):
    landmap[(5+j)*MAP_WIDTH + 22 + i] = random.randint(2*COLS, 3*COLS-1)

NB_OBJECTS_ON_MAP=100
objects = [(
        random.randint(0, MAP_WIDTH*64),
        random.randint(0, MAP_HEIGHT*32),
        random.randint(0, len(objects_sprites)-1)
        ) for i in range(0, NB_OBJECTS_ON_MAP)]

LEN_BRIDGE=20
bridge_map = [random.randint(2,7)*2 for i in range(2*LEN_BRIDGE)]

exit = False
pos = [0, 0]
dpos = [0, 0]
while not exit:
    screen.fill(0)
    idx = 0
    for i in range(-1, MAP_WIDTH):
      for j in range(-1, MAP_HEIGHT):
        screen.blit(tile[landmap[i+2*j*MAP_WIDTH]], (64*i - pos[0],32*j - pos[1]))
        screen.blit(tile[landmap[i+(2*j+1)*MAP_WIDTH]], (64*i + 32 - pos[0],32*j + 16 - pos[1]))
    pos[0] += dpos[0]
    if pos[0] < 0:
        pos[0] = 0
    if pos[0] >= 3200-1024:
        pos[0] = 3200-1024
    pos[1] += dpos[1]
    if pos[1] < 0:
        pos[1] = 0
    if pos[1] >= 1600-768:
        pos[1] = 1600-768
    for o in objects:
        screen.blit(objects_sprites[o[2]], (o[0] - pos[0], o[1] - pos[1]))
    # Draw a bridge
    screen.blit(bridge_sprites[0], (64*3 - pos[0], 32*7 - pos[1]))
    screen.blit(bridge_sprites[4], (64*3 + 32 - pos[0], 32*7 + 16 - pos[1]))
    for i in range(1, LEN_BRIDGE):
        screen.blit(bridge_sprites[bridge_map[2*i]], (64*(3+i) - pos[0], 32*(7+i) - pos[1]))
        screen.blit(bridge_sprites[bridge_map[2*i+1]], (64*(3+i) + 32 - pos[0], 32*(7+i) + 16 - pos[1]))
    screen.blit(bridge_sprites[2], (64*(3+LEN_BRIDGE) - pos[0], 32*(7+LEN_BRIDGE) - pos[1]))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit = True
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
            if event.key == pygame.K_UP:
                if dpos[1] > -5:
                    dpos[1] -= 1
            if event.key == pygame.K_DOWN:
                if dpos[1] < 5:
                    dpos[1] += 1
            if event.key == pygame.K_LEFT:
                if dpos[0] > -5:
                    dpos[0] -= 1
            if event.key == pygame.K_RIGHT:
                if dpos[0] < 5:
                    dpos[0] += 1

pygame.quit()
