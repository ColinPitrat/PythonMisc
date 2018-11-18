#!/usr/bin/python2
import pygame, random, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 1280, 800
taille_pixel = 4
resolution = largeur, hauteur = 160, 100
taille_pixel = 1
resolution = largeur, hauteur = 1600, 1000
taille_pixel = 10
# + 1 pour les cas ou largeur ou hauteur n'est pas un multiple de taille_pixel
resolution_grid = largeur_grid, hauteur_grid = largeur / taille_pixel + 1, hauteur / taille_pixel

def int_to_col(i):
    if i < 0:
        return (0, 0, 0)
    if i <= 255:
        return (i, i, 0)
    if i <= 510:
        return (255, 510-i, 0)
    if i <= 765:
        return (765-i, 0, i-510)
    if i <= 1020:
        return (0, i-765, 1020-i)
    return (255, 255, 255)

def palette_plasma():
    palette = [(0, 0, 0)] * 256
    for x in range(0, 64):
        palette[x] = (4*x, 4*x, 0)
        palette[x+64] = (252, 252-4*x, 0)
        palette[x+128] = (252-4*x, 0, 4*x)
        palette[x+192] = (0, 4*x, 252-4*x)
    palette.append((255, 255, 255))
    return palette

def palette_monochrome():
    palette = [(0, 0, 0)] * 256
    for x in range(0, 256):
        palette[x] = (x, x, x)
    palette.append((255, 255, 255))
    return palette

palette = palette_plasma()
PI = 3.141592654
cosTbl = [0]*256
for i in range(0, 256):
    cosTbl[i] = int((math.cos(i*360.0/256 * PI/180)*32)+32)

t1, t2, t3, t4 = 0, 0, 0, 0
p1, p2, p3, p4 = 0, 0, 0, 0

#def cosTbl(i):
#    return int(256*math.cos(i*360.0/256 * PI/180))

def affiche(surface):
    global t1, t2, t3, t4, p1, p2, p3, p4
    border = 1 if taille_pixel == 1 else 0
    t1 = p1
    t2 = p2
    for y in range(0, hauteur_grid):
        t3 = p3
        t4 = p4
        line = ""
        j = cosTbl[t1] + cosTbl[t2]
        for x in range(0, largeur_grid):
            i = j + cosTbl[t3] + cosTbl[t4]
            #i = int(cosTbl[t4])
            #line += "%03d " % i
            col = palette[i]
            pygame.draw.rect(surface, col, (x*taille_pixel, y*taille_pixel, taille_pixel, taille_pixel), border)
            t3 = (t3 - 1) % 256
            t4 = (t4 + 4) % 256
        t1 = (t1 - 4) % 256
        t2 = (t2 + 2) % 256
        #print(line)
    p1 = (p1 + 1) % 256
    p2 = (p2 + 4) % 256
    p3 = (p3 + 1) % 256
    p4 = (p4 - 4) % 256

def main():
    quitter = False
    ecran = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Plasma")
    while quitter != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitter = True
        affiche(ecran)
        pygame.display.flip()

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

###############
# Terminaison #
###############
pygame.quit()
