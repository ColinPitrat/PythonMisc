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
map_path = os.path.join(resource_path, 'maps') # The map folder path

tiles = pygame.image.load(os.path.join(image_path, 'tiles.png')).convert_alpha()
persos = pygame.image.load(os.path.join(image_path, 'perso.png')).convert_alpha()

class Map(object):

    def generate(self, width, height):
        self._width = width
        self._height = height
        self._tiles = [
            [
                ['grass%s' % random.randint(0, 15)]
                for i in range(2*height)
            ]
            for j in range(width)
        ]
        self._objects = []

    def height_pixels(self):
        return self._height * 32 + 16

    def width_pixels(self):
        return self._width * 64 + 32


def load_map():
    landmap = Map()
    landmap._tiles = []
    landmap._objects = []
    with open(os.path.join(map_path, 'map.txt')) as f:
        for l in f.readlines():
            if l[0] == "T":
                landmap._tiles.append([])
                l = l[1:]
                for n in l.split('#'):
                    landmap._tiles[-1].append([])
                    for t in n.split(','):
                        t = t.strip()
                        if t:
                            landmap._tiles[-1][-1].append(t)
            elif l[0] == "O":
                l = l[1:].split(',')
                landmap._objects.append([l[0], int(l[1]), int(l[2])])
    landmap._width = len(landmap._tiles)
    landmap._height = len(landmap._tiles[0])//2
    return landmap


def load_tiles(with_alpha = True):
    tiles = pygame.image.load(os.path.join(image_path, 'tiles.png'))#.convert_alpha()
    result = {}
    with open(os.path.join(image_path, 'tiles.txt')) as f:
        for desc in f.readlines():
            if desc[0] == '#':
                continue
            elems = desc.split(',')
            flags = HWSURFACE
            if with_alpha:
                flags |= SRCALPHA
            if elems[0] == '%ASSEMBLE':
                name = elems[1]
                w, h = int(elems[2]), int(elems[3])
                result[name] = pygame.Surface((w, h), flags=flags)
                nb_components = (len(elems)-4)/3
                for i in range(nb_components):
                    idx=4+3*i
                    c_name = elems[idx]
                    c_x, c_y = int(elems[idx+1]), int(elems[idx+2])
                    result[name].blit(result[c_name], (c_x, c_y))
            elif elems[0] == '%REMOVE':
                name = elems[1].strip()
                del result[name]
            else:
                x, y, w, h = int(elems[1]), int(elems[2]), int(elems[3]), int(elems[4])
                result[elems[0]] = pygame.Surface((w, h), flags=flags)
                result[elems[0]].blit(tiles, (0, 0), area=(x, y, w, h))
    return result


P_COLS=3
P_ROWS=4

perso = [None] * (P_COLS*P_ROWS)
for i in range(P_COLS):
  for j in range(P_ROWS):
    perso[P_COLS*j+i] = pygame.Surface((32, 36), flags=HWSURFACE | SRCALPHA)
    perso[P_COLS*j+i].blit(persos, (0, 0), area=(32*i, 36*j, 32, 36))

MAP_WIDTH=50
MAP_HEIGHT=50

landmap = load_map()
tiles = load_tiles()

NB_FRAMES=10
SPEED=2

def constrain(value, lower, higher):
    if value < lower:
        return lower
    if value > higher:
        return higher
    return value

exit = False
moving = False
orient = 2
# Sprite 1 is the "rest" one. Adding NB_FRAMES-1 ensures the sprite is animated
# when moving no matter how small the movement is.
frame = 2*NB_FRAMES-1
pos = [0, 0]
perso_pos = [512, 384]
dpos = [0, 0]
fps_frame_count = 0
fps_last_tick = pygame.time.get_ticks()
while not exit:
    screen.fill(0)
    for j in range(0, 2*landmap._height):
      for i in range(0, landmap._width):
        offset = 32 if j%2 == 1 else 0
        for t in landmap._tiles[i][j]:
            screen.blit(tiles[t], (64*i + offset - pos[0],16*j - pos[1]))
    perso_pos[0] = constrain(perso_pos[0] + dpos[0], 32, 3200-perso[0].get_width())
    pos[0] = constrain(perso_pos[0] - 512, 32, 3200-1024)
    perso_pos[1] = constrain(perso_pos[1] + dpos[1], 16, 1600-perso[0].get_height())
    pos[1] = constrain(perso_pos[1] - 384, 16, 1600-768)
    for o in landmap._objects:
        screen.blit(tiles[o[0]], (o[1] - pos[0], o[2] - pos[1]))

    screen.blit(perso[orient*3 + (frame // NB_FRAMES) % 3], (perso_pos[0] - pos[0], perso_pos[1] - pos[1]))

    pygame.display.flip()
    fps_frame_count += 1
    if fps_frame_count % 100 == 0:
        new_tick = pygame.time.get_ticks()
        print("FPS=%s" % (1000*fps_frame_count/(new_tick - fps_last_tick)))
        fps_frame_count = 0
        fps_last_tick = new_tick
    if moving:
        frame += 1

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit = True
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
            if event.key == pygame.K_UP:
                dpos[0] = 0
                dpos[1] = -SPEED
                orient = 0
                moving = True
            if event.key == pygame.K_DOWN:
                dpos[0] = 0
                dpos[1] = SPEED
                orient = 2
                moving = True
            if event.key == pygame.K_LEFT:
                dpos[0] = -SPEED
                dpos[1] = 0
                orient = 3
                moving = True
            if event.key == pygame.K_RIGHT:
                dpos[0] = SPEED
                dpos[1] = 0
                orient = 1
                moving = True
        if event.type==pygame.KEYUP:
            if ((event.key == pygame.K_UP and orient == 0) or
                (event.key == pygame.K_DOWN and orient == 2) or
                (event.key == pygame.K_LEFT and orient == 3) or
                (event.key == pygame.K_RIGHT and orient == 1)):
                   moving = False
                   frame = 2*NB_FRAMES-1
                   dpos[0] = 0
                   dpos[1] = 0

pygame.quit()
