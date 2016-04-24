#!/usr/bin/python2
import pygame, random, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 400, 200
demilargeur = largeur/2

noir = 0, 0, 0
rouge = 255, 0, 0
blanc = 255, 255, 255

#############
# Variables #
#############
police = pygame.font.SysFont("arial", 15);
minXM = -2
maxXM = 1
minYM = -5.0/4
maxYM = 1.5
minXJ = -2
maxXJ = 2
minYJ = -2
maxYJ = 2
C = complex(-1, 0)
maxIterations = 100
zoom = 1.0
zoomFactor = 2.0
# 0 = Choix d'un point - 1 = zoom - 2 = dezoom
mode = 0

def convergeMandelbrot(C):
    u = C
    for i in range(0, maxIterations):
        u = u**2 + C
        if abs(u) > 2:
            return (int(i*255.0/maxIterations), 0, 255)
    return (0, 0, 0)

def convergeJulia(u):
    global C
    for i in range(0, maxIterations):
        u = u**2 + C
        if abs(u) > 5:
            return (255, 0, int(i*255.0/maxIterations))
    return (0, 0, 0)
        
##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("Ensembles de Mandelbrot et Julia")

quitter = False
yJ = 0
yM = 0
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
                yM = 0
                yJ = 0
            if event.key == pygame.K_p:
                maxIterations *= 2
            if event.key == pygame.K_m:
                maxIterations /= 2
            if event.key == pygame.K_c:
                mode = 0
            if event.key == pygame.K_z:
                mode = 1
            if event.key == pygame.K_d:
                mode = 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if event.pos[0] <= demilargeur:
                    clicX = minXM + 1.0*event.pos[0]/demilargeur*(maxXM-minXM)
                    clicY = minYM + 1.0*(maxYM-minYM)*(hauteur-event.pos[1])/hauteur
                    if mode == 0:
                        C = complex(clicX, clicY)
                        print("Trace l'ensemble de Julia pour C=%s" % C)
                        yJ = 0
                    else:
                        if mode == 1:
                            newLargeur = (maxXM - minXM) / zoomFactor
                            newHauteur = (maxYM - minYM) / zoomFactor
                            zoom *= zoomFactor
                        else:
                            newLargeur = (maxXM - minXM) * zoomFactor
                            newHauteur = (maxYM - minYM) * zoomFactor
                            zoom /= zoomFactor
                        minXM = clicX - newLargeur/2.0
                        maxXM = clicX + newLargeur/2.0
                        minYM = clicY - newHauteur/2.0
                        maxYM = clicY + newHauteur/2.0
                        yM = 0

    if yM < hauteur:
        if yM == 0:
            ecran.fill(noir, (0, 0, demilargeur, hauteur))
        for x in range(0, demilargeur):
                X = minXM + 1.0*x/demilargeur*(maxXM-minXM)
                Y = minYM + 1.0*(maxYM-minYM)*(hauteur-yM)/hauteur
                couleur = convergeMandelbrot(complex(X, Y))
                if couleur:
                    pygame.draw.line(ecran, couleur, (x, yM), (x, yM))
        yM += 1

    if yJ < hauteur:
        if yJ == 0:
            ecran.fill(blanc, (demilargeur, 0, demilargeur, hauteur))
        for x in range(demilargeur, largeur):
                X = minXJ + 1.0*(x-demilargeur)/demilargeur*(maxXJ-minXJ)
                Y = -(minYJ + 1.0*yJ/hauteur*(maxYJ-minYJ))
                couleur = convergeJulia(complex(X, Y))
                if couleur:
                    pygame.draw.line(ecran, couleur, (x, yJ), (x, yJ))
        yJ += 1

    infos = police.render("Iter=%s - Zoom=%s" % (maxIterations, zoom), True, rouge)
    ecran.blit(infos, (0, 0))
    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
