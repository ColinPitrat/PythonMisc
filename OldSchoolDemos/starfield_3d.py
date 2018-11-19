#!/usr/bin/python
# -*- coding: utf8 -*-"

import pygame, random

##############
# Constantes #
##############
resolution = largeur, hauteur = 1600, 1000
vitesse_min, vitesse_max = 300, 300
intensity_min, intensity_max = 1, 10
focale = 100
profondeur = 1000

def reinit_star(star):
    star[0] = 1.0*random.randint(-largeur*profondeur/focale, largeur*profondeur/focale)
    star[1] = 1.0*random.randint(-hauteur*profondeur/focale, hauteur*profondeur/focale)
    star[2] = 1.0*profondeur
    star[3] = 1.0*random.randint(vitesse_min, vitesse_max)/100
    star[4] = 1.0*random.randint(intensity_min, intensity_max)

def init_star():
    star = [0, 0, 0, 0, 0]
    reinit_star(star)
    star[2] = 1.0*random.randint(focale, profondeur)
    return star

def create_stars(n):
    return [init_star() for i in range(0, n)]

def main():
    pygame.init()

    quitter = False
    ecran = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Starfield 3D")
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
            # x' = z'*x/z 
            x, y = star[0]*focale/star[2] + largeur/2, star[1]*100/star[2] + hauteur/2
            # intensity is 1/z^2
            pygame.draw.rect(ecran, (0, 0, 0), (x, y, 1, 1), 1)
            star[2] -= star[3]
            if star[2] <= 0 or x < 0 or y < 0 or x > largeur or y > hauteur:
                reinit_star(star)
            x, y = star[0]*focale/star[2] + largeur/2, star[1]*100/star[2] + hauteur/2
            # The right formula would be in 1/z^2 but this means the stars are almost invisible until they come very close
            i = int(255.0*(profondeur-star[2])/(profondeur-focale))
            i = max(min(i, 255), 0)
            pygame.draw.rect(ecran, (i, i, i), (x, y, 1, 1), 1)
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
