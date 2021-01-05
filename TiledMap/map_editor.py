import pygame
import random
import os
import sys
from pygame.locals import *

pygame.init()

width, height = 1280, 1024
screen = pygame.display.set_mode((width, height))

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
map_path = os.path.join(resource_path, 'maps') # The map folder path
image_path = os.path.join(resource_path, 'images') # The image folder path


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


MAP_WIDTH=50
MAP_HEIGHT=50

def random_map():
    result = Map()
    result.generate(MAP_WIDTH, MAP_HEIGHT)
    return result

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

def save_map(landmap):
    with open(os.path.join(map_path, 'map.txt'), "w") as f:
        f.write('\n'.join(['T' + '#'.join([','.join(cell) for cell in row]) for row in landmap._tiles]) + '\n')
        f.write('\n'.join(['O%s,%s,%s' % (o[0], o[1], o[2]) for o in landmap._objects]) + '\n')

def load_tiles(with_alpha = True):
    tiles = pygame.image.load(os.path.join(image_path, 'tiles_snow.png'))#.convert_alpha()
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

BORDER=20
MARGIN=10

dy = 0
ddy = 0
max_y = 0
margins = True
labels = True
alpha = True

def move_down(ddy, surface):
    global dy
    dy += ddy
    if dy < 0:
      dy = 0
    if dy > max_y - surface.get_height() + BORDER:
      dy = max_y - surface.get_height() + BORDER

LABEL_HEIGHT=14
def show_tiles(surface, tiles):
    global dy, ddy, max_y, margins, labels, alpha, selected, to_select
    surface.fill((50, 50, 50))
    x, y = BORDER, BORDER
    max_line_y = 0
    margin = MARGIN if margins else 0
    for name in sorted(tiles.keys()):
        sprite = tiles[name]
        if x + sprite.get_width() > surface.get_width() - BORDER:
            x = BORDER
            y += max_line_y + margin + LABEL_HEIGHT
            max_line_y = 0
        if name == selected:
            pygame.draw.rect(surface, (0, 0, 0), (x, y-dy-LABEL_HEIGHT, sprite.get_width(), sprite.get_height()+LABEL_HEIGHT))
        tile_rect = surface.blit(sprite, (x, y-dy))
        if to_select and tile_rect.collidepoint(to_select):
            selected = name
            to_select = None
        if labels:
            label = font.render(name, True, (255, 255, 255))
            surface.blit(label, (x, y-dy-LABEL_HEIGHT))
        x += sprite.get_width() + margin
        max_line_y = max(max_line_y, sprite.get_height())
        max_y = y + max_line_y

    move_down(ddy, surface)

def get_tile_coordinates(pos, map_pos):
  x = pos[0] + map_pos[0]
  y = pos[1] + map_pos[1]
  dx = x - 64*(x//64)
  dy = y - 32*(y//32)
  if 32-dx > 2*dy:
    # top left quarter
    X = x//32 - 1
    Y = y//16 - 1
  elif dx-32 > 2*dy:
    # top right quarter
    X = x//32
    Y = y//16 - 1
  elif dx+32 < 2*dy:
    # bottom left quarter
    X = x//32 - 1
    Y = y//16
  elif 96-dx < 2*dy:
    # bottom right quarter
    X = x//32
    Y = y//16
  else:
    # middle
    X = 2*(x//64)
    Y = 2*(y//32)
  return (X, Y)

map_pos = [0, 0]
map_dpos = [0, 0]
def show_map(surface, landmap, tiles):
    global to_delete
    surface_rect = surface.fill((0, 0, 0))

    cursor = pygame.mouse.get_pos()

    map_pos[0] += map_dpos[0]
    if map_pos[0] < 0:
        map_pos[0] = 0
    if map_pos[0] >= landmap.width_pixels()-surface.get_width():
        map_pos[0] = landmap.width_pixels()-surface.get_width()
    map_pos[1] += map_dpos[1]
    if map_pos[1] < 0:
        map_pos[1] = 0
    if map_pos[1] >= landmap.height_pixels()-surface.get_height():
        map_pos[1] = landmap.height_pixels()-surface.get_height()

    # Show tiles
    for j in range(0, 2*landmap._height):
      for i in range(0, landmap._width):
        offset = 32 if j%2 == 1 else 0
        for t in landmap._tiles[i][j]:
          tile_rect = surface.blit(tiles[t], (64*i + offset - map_pos[0],16*j - map_pos[1]))
          if tile_rect.collidepoint(cursor) and tiles[t].get_at((cursor[0] - tile_rect.x, cursor[1] - tile_rect.y)).a > 0:
            highlight = pygame.surfarray.make_surface(pygame.surfarray.array3d(tiles[t].copy()).astype(bool).astype(int)*0xFFFFFFFF)
            highlight.set_colorkey((0, 0, 0))
            highlight.set_alpha(64)
            surface.blit(highlight, (64*i + offset - map_pos[0],16*j - map_pos[1]))
          if to_delete and tile_rect.collidepoint(to_delete):
            for k, tname in reversed(list(enumerate(landmap._tiles[i][j]))):
              #print("%s, %s, %s, x=%s, y=%s" % (tname, tile_rect, to_delete, to_delete[0] - tile_rect.x, to_delete[1] - tile_rect.y))
              try:
                if tiles[tname].get_at((to_delete[0] - tile_rect.x, to_delete[1] - tile_rect.y)).a > 0:
                  #print("Delete %s" % tname)
                  del landmap._tiles[i][j][k]
                  to_delete = None
                  break
              except:
                print("Oups")
                pass
    # If nothing was found to delete among all tiles, nothing needs to be
    # deleted.
    to_delete = None

    # Show objects
    for o in landmap._objects:
        surface.blit(tiles[o[0]], (o[1] - map_pos[0], o[2] - map_pos[1]))

    if tiled:
        # Highlight the tile over which the cursor is
        (X, Y) = get_tile_coordinates(cursor, map_pos)
        pygame.draw.rect(surface, (255, 255, 0), (32*X - map_pos[0], 16*Y - map_pos[1], 64, 32), 1)

    if selected and surface_rect.collidepoint(cursor):
        surface.blit(tiles[selected], cursor)

exit = False
font = pygame.font.SysFont("arial", 12);
tiles = load_tiles(alpha)
landmap = load_map()
tiled = True
selected = None
to_select = None
to_delete = None

map_view = pygame.Surface((80*screen.get_width()//100, screen.get_height()))
selector = pygame.Surface((screen.get_width()-map_view.get_width(), screen.get_height()))
while not exit:
    show_map(map_view, landmap, tiles)
    show_tiles(selector, tiles)

    map_rect = screen.blit(map_view, (0, 0))
    selector_rect = screen.blit(selector, (map_view.get_width(), 0))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit = True
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
            if event.key == pygame.K_UP:
                map_dpos[1] = -5
            if event.key == pygame.K_DOWN:
                map_dpos[1] = 5
            if event.key == pygame.K_LEFT:
                map_dpos[0] = -5
            if event.key == pygame.K_RIGHT:
                map_dpos[0] = 5
            if event.key == pygame.K_m:
                margins = not margins
            if event.key == pygame.K_l:
                labels = not labels
            if event.key == pygame.K_a:
                alpha = not alpha
                tiles = load_tiles(alpha)
            if event.key == pygame.K_s:
                save_map(landmap)
                print("Saved map.txt")
            if event.key == pygame.K_t:
                tiled = not tiled
        if event.type==pygame.KEYUP:
            if event.key == pygame.K_UP:
                map_dpos[1] = 0
            if event.key == pygame.K_DOWN:
                map_dpos[1] = 0
            if event.key == pygame.K_LEFT:
                map_dpos[0] = 0
            if event.key == pygame.K_RIGHT:
                map_dpos[0] = 0
        if event.type==pygame.MOUSEBUTTONDOWN:
            if selector_rect.collidepoint(event.pos):
                if event.button == 5:
                    move_down(50, selector)
                if event.button == 4:
                    move_down(-50, selector)
                if event.button == 1:
                    to_select = (event.pos[0]-selector_rect.left, event.pos[1]-selector_rect.top)
            if map_rect.collidepoint(event.pos):
                if event.button == 1 and selected:
                    if tiled:
                        (X, Y) = get_tile_coordinates(event.pos, map_pos)
                        landmap._tiles[X//2][Y].append(selected)
                    else:
                        landmap._objects.append([selected, event.pos[0]-map_rect.left+map_pos[0], event.pos[1]-map_rect.top+map_pos[1]])
                if event.button == 3:
                    to_delete = (event.pos[0]-map_rect.left, event.pos[1]-map_rect.top)

pygame.quit()
