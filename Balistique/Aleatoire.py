#!/usr/bin/python2
import pygame, random, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 800, 600

noir = 0, 0, 0
rouge = 255, 0, 0
blanc = 255, 255, 255

police = pygame.font.SysFont("arial", 20);

#############
# Variables #
#############

X = 0
Y = 0
x = 0
y = 0
v_x = 0
v_y = 0
a_y = 0

echelle = 1.0/100
quitter = False

def reset():
    global ecran, noir, X, Y, x, y, v_x, v_y, a_y
#    ecran.fill(noir)
    X = 0
    Y = hauteur
    x = 0
    y = 0
    v_x = random.randint(300,800)
    v_y = random.randint(500,1000)
    a_y = -10

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("Balistique")

reset()
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
                ecran.fill(noir)
                reset()

    if y >= 0 and X < largeur:
        pygame.draw.rect(ecran, blanc, (X, Y, 1, 1), 1)
        X = echelle * x
        Y = hauteur - echelle * y
        x = x+v_x
        v_y = v_y + a_y
        y = y+v_y
        pygame.draw.rect(ecran, rouge, (X, Y, 1, 1), 1)

        infos = police.render("Vx = %s , Vy = %s, Ay = %s" % (v_x, v_y, a_y), True, rouge)
        ecran.fill(noir, infos.get_rect())
        ecran.blit(infos, (0, 0))
    else:
        reset()

    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
