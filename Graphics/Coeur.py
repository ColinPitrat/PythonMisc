#!/usr/bin/python
# -*- coding: utf8 -*-"

import pygame, math
from datetime import datetime, timedelta
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 600, 600

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
noir = 0, 0, 0
pink = 0xc5, 0x65, 0x88
blanc = 255, 255, 255

#####################
# Boucle principale #
#####################
quitter = False
r = 10
w = 10

def reset():
    global t, ecran
    ecran.fill(noir)
    t = 0

reset()
while quitter == False:
    begin = datetime.now()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            if event.key == pygame.K_r:
                reset()

    if t < 2*math.pi:
        x = r*16*math.sin(t)**3 + largeur/2
        y = r*(-13*math.cos(t) + 5*math.cos(2*t) + 2*math.cos(3*t) + math.cos(4*t)) + hauteur/2
        pygame.draw.line(ecran, pink, (largeur/2, hauteur/2), (x, y), w)
        t2 = 0
        while t2 < t:
            x2 = r*16*math.sin(t2)**3 + largeur/2
            y2 = r*(-13*math.cos(t2) + 5*math.cos(2*t2) + 2*math.cos(3*t2) + math.cos(4*t2)) + hauteur/2
            pygame.draw.ellipse(ecran, blanc, (x2-w/2, y2-w/2, w, w), 0)
            t2 += 0.01
        t += 0.01
    while datetime.now() - begin < timedelta(microseconds=10000):
        pass
    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
