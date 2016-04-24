#!/usr/bin/python2
import pygame, random, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 200, 200

noir = 0, 0, 0
rouge = 255, 0, 0
blanc = 255, 255, 255

#############
# Variables #
#############
police = pygame.font.SysFont("arial", 15);
minX = -3.0/2
maxX = 3.0/2
minY = -3.0/2
maxY = 3.0/2
C = complex(0.32, 0.043)
C = complex(-0.122561, 0.744862)
C = complex(0.34, 0.07)
C = complex(-0.35, -0.63125)
C = complex(-1, 0)
maxIterations = 100
zoom = 1.0

ensembleDivergent = []
ensembleConvergent0 = []
ensembleConvergent = []

def converge(u):
    global C, ensembleConvergent, ensembleConvergent0, ensembleDivergent
    for i in range(0, maxIterations):
        u = u**2 + C
        if abs(u) < 0.1:
            return (0, 0, 0)
        if abs(u) > 10:
            return (0, 0, 255)
    return (255, 0, 0)
        
##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("Ensemble de Julia")

quitter = False
y = 0
#####################
# Boucle principale #
#####################
while quitter != True:
    # Boucle d'evenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            if event.key == pygame.K_r:
                C = complex(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
                print("C = %s" % C)
                y = 0
            if event.key == pygame.K_c:
                y = 1
            if event.key == pygame.K_p:
                maxIterations *= 2
            if event.key == pygame.K_m:
                maxIterations /= 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                centerX = minX + 1.0*event.pos[0]/largeur*(maxX-minX)
                centerY = maxY - 1.0*event.pos[1]/hauteur*(maxY-minY)
                print("Zoom current (%s, %s, %s, %s) - clicked (%s, %s) = (%s, %s)" % (minX, maxX, minY, maxY, event.pos[0], event.pos[1], centerX, centerY))
                newLargeur = (maxX - minX) / 10.0
                newHauteur = (maxY - minY) / 10.0
                minX = centerX - newLargeur/2.0
                maxX = centerX + newLargeur/2.0
                minY = centerY - newHauteur/2.0
                maxY = centerY + newHauteur/2.0
                zoom *= 10.0
                print("Zoom (%s, %s) => (%s, %s) (%s, %s)" % (centerX, centerY, minX, minY, maxX, maxY))
                y = 0
            if pygame.mouse.get_pressed()[2]:
                centerX = minX + 1.0*event.pos[0]/largeur*(maxX-minX)
                centerY = maxY - 1.0*event.pos[1]/hauteur*(maxY-minY)
                print("Zoom current (%s, %s, %s, %s) - clicked (%s, %s) = (%s, %s)" % (minX, maxX, minY, maxY, event.pos[0], event.pos[1], centerX, centerY))
                newLargeur = (maxX - minX) * 10
                newHauteur = (maxY - minY) * 10
                minX = centerX - newLargeur/2
                maxX = centerX + newLargeur/2
                minY = centerY - newHauteur/2
                maxY = centerY + newHauteur/2
                zoom /= 10.0
                print("Dezoom (%s, %s) => (%s, %s) (%s, %s)" % (centerX, centerY, minX, minY, maxX, maxY))
                y = 0

    if y < hauteur:
        if y == 0:
            ecran.fill(noir)
        for x in range(0, largeur):
                X = minX + 1.0*x/largeur*(maxX-minX)
                Y = maxY - 1.0*y/hauteur*(maxY-minY)
                couleur = converge(complex(X, Y))
                if couleur:
                    pygame.draw.line(ecran, couleur, (x, y), (x, y))
        infos = police.render("C=%s - Iter=%s - Zoom=%s" % (C, maxIterations, zoom), True, rouge)
        ecran.blit(infos, (0, 0))
        pygame.display.flip()
        y += 1

###############
# Terminaison #
###############
pygame.quit()
