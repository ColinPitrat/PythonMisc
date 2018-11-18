#!/usr/bin/python2
import pygame, random

##############
# Constantes #
##############
resolution = largeur, hauteur = 800, 1000
taille_pixel = 10
resolution = largeur, hauteur = 160, 200
taille_pixel = 2
# + 1 pour les cas ou largeur ou hauteur n'est pas un multiple de taille_pixel
resolution_grid = largeur_grid, hauteur_grid = largeur / taille_pixel + 1, hauteur / taille_pixel

TMP_MIN = 0
TMP_MAX = 765

# TODO: code mort ?
def palette_feu():
    result = []
    for r in range(0, 255):
        result.append((r, 0, 0))
    for g in range(0, 255):
        result.append((255, g, 0))
    return result

def create_grids():
    grid = []
    tmp_grid = []
    for x in range(0, largeur_grid):
        grid.append([])
        tmp_grid.append([])
        for y in range(0, hauteur_grid+1):
            grid[x].append(0)
            tmp_grid[x].append(0)
    return grid, tmp_grid

def int_to_col(i):
    if i < 0:
        return (0, 0, 0)
    if i <= 255:
        return (i, 0, 0)
    if i <= 510:
        return (255, i-255, 0)
    if i <= 765:
        return (255, 255, i-510)
    return (255, 255, 255)

def col_to_int(c):
    return c[0] + c[1] + c[2]

def braise(tmp_min, tmp_max):
    return random.randint(tmp_min, tmp_max)

def random_line(grid, tmp_grid):
    tmp_min, tmp_max = TMP_MIN, TMP_MAX
    for x in range(0, largeur_grid):
        if x % 10 == 0:
            a = random.randint(TMP_MIN, TMP_MAX)
            b = random.randint(TMP_MIN, TMP_MAX)
            tmp_min = min(a, b)
            tmp_max = max(a, b)
        grid[x][hauteur_grid] = braise(tmp_min, tmp_max)
        tmp_grid[x][hauteur_grid] = grid[x][hauteur_grid]

def random_update_line(grid, tmp_grid):
    for x in range(0, largeur_grid):
        grid[x][hauteur_grid] += random.randint(0, 250) - 125
        if grid[x][hauteur_grid] < 0:
            grid[x][hauteur_grid] = 0
        if grid[x][hauteur_grid] > 765:
            grid[x][hauteur_grid] = 765
        tmp_grid[x][hauteur_grid] = grid[x][hauteur_grid]

def moyenne(grid, x, y):
    c = 0
    rg = [-1, 0, 1]
    for dx in rg:
        if x+dx > 0 and x+dx < largeur_grid:
            for dy in rg:
                if y+dy > 0 and y+dy <= hauteur_grid:
                    c += grid[x+dx][y+dy]
    return max(c/9-3, 0)

def moyenne_sous(grid, x, y):
    c = 0
    for dx in [-1, 0, 1]:
        for dy in [1]:
            if x+dx > 0 and x+dx < largeur_grid and y+dy > 0 and y+dy <= hauteur_grid:
                c += grid[x+dx][y+dy]
    return c/3

def calcule(grid, tmp_grid):
    for x in range(0, largeur_grid):
        for y in range(0, hauteur_grid):
            tmp_grid[x][y] = moyenne(grid, x, y+1)
    return tmp_grid, grid

def affiche(surface, grid):
    border = 1 if taille_pixel == 1 else 0
    for x in range(0, largeur_grid):
        for y in range(0, hauteur_grid+1):
            pygame.draw.rect(surface, int_to_col(grid[x][y]), (x*taille_pixel, y*taille_pixel, taille_pixel, taille_pixel), border)

def print_grid(grid):
    for y in range(0, hauteur_grid+1):
        line = ""
        for x in range(0, largeur_grid):
            line += "%03d " % grid[x][y]
        print(line)

def main():
    global TMP_MIN, TMP_MAX
    pygame.init()
    quitter = False
    grid, tmp_grid = create_grids()
    ecran = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Effet feu")
    random_line(grid, tmp_grid)
    while quitter != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitter = True
                if event.key == pygame.K_m:
                    TMP_MIN = 0
                    TMP_MAX = 510
                if event.key == pygame.K_p:
                    TMP_MIN = 255
                    TMP_MAX = 765
                if event.key == pygame.K_r:
                    TMP_MIN = 0
                    TMP_MAX = 765
        random_update_line(grid, tmp_grid)
        grid, tmp_grid = calcule(grid, tmp_grid)
        affiche(ecran, grid)
        #print_grid(grid)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    # Profiling
    import cProfile, pstats, StringIO
    pr = cProfile.Profile()
    pr.enable()

    main()

    # Profiling
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()
