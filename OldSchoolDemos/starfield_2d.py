#!/usr/bin/python
# -*- coding: utf8 -*-"

import pygame, random

##############
# Constantes #
##############
resolution = largeur, hauteur = 1600, 1000
vitesse_min, vitesse_max = 10, 300
intensity_min, intensity_max = 100, 255

def reinit_star(star):
    star[0] = largeur
    star[1] = 1.0*random.randint(0, hauteur)
    star[2] = 1.0*random.randint(vitesse_min, vitesse_max)/100
    star[3] = random.randint(intensity_min, intensity_max)

def init_star():
    star = [0, 0, 0, 0]
    reinit_star(star)
    star[0] = 1.0*random.randint(0, largeur)
    return star

def create_stars(n):
    return [init_star() for i in range(0, n)]

def main():
    pygame.init()

    quitter = False
    ecran = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Starfield 2D")
    stars = create_stars(1000)
    while quitter != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitter = True
        for star in stars:
            #print("%s" % star)
            pygame.draw.rect(ecran, (0, 0, 0), (star[0], star[1], 1, 1), 1)
            star[0] -= star[2]
            if star[0] <= 0:
                reinit_star(star)
            color = (star[3], star[3], star[3])
            pygame.draw.rect(ecran, color, (star[0], star[1], 1, 1), 1)
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
