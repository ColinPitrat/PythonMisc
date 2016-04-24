#!/usr/bin/python2
# La parabole de securite enveloppe toutes les trajectoires possibles d'un boulet tire depuis un canon avec une force donnee. 
# En dehors de cette parabole, une cible ne peut etre atteinte
# Le point le plus lointain qui puisse etre atteint l'est pour l'angle alpha = pi/4 = 0.7854
# En effet (x0 = 0, y0 = 0):
#  y'' = -g ; y' = -g*t + v0y ; y = -g/2*t^2 + v0y*t + y0 = -g/2*t^2 + v0y*t
#  x'' = 0 ; x' = v0x ; x = v0x*t + x0 = v0x*t
#  => t = x / (v0 * cos(alpha)
#  => y = -g/(2*v0*cos(alpha)) * x^2 + tan(alpha) * x = x*(-g/(2*v0*cos(alpha)) * x + tan(alpha))
# 2 solutions: x = 0 (point de depart) et x = 2*v^2/g * cos(alpha)*sin(alpha)
# Pour v donne, x est maximal pour alpha = pi/4. En effet:
#  f(x) = cos(x)*sin(x) est maximal pour f'(x) = cos^2(x) - sin^2(x) = 2*cos^2(x) - 1 = 0 => cos^2(x) = 1/2 => cos(x) = sqrt(2)/2 => x = pi/4
# ou encore x = 2*v^2/g * cos(alpha)*sin(alpha) = v^2/g * sin(2*alpha) maximal pour sin(2*alpha) = 1, soit alpha = pi/4
# cf http://fr.wikipedia.org/wiki/Port%C3%A9e_(balistique)
import pygame, random, math, time
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 800, 600

noir = 0, 0, 0
rouge = 255, 0, 0
vert = 0, 255, 0
bleu = 0, 0, 255
cyan = 0, 255, 255
magenta = 255, 0, 255
jaune = 255, 255, 0
blanc = 255, 255, 255

police = pygame.font.SysFont("arial", 20);

#############
# Variables #
#############

t = 0
X = 0
Y = 0
x = 0
y = 0
v = 800
alpha = 0
deltaAlpha = 0.02
alpha = math.pi/2.0
deltaAlpha = -0.02
v_x = 0
v_y = 0
a_y = 0

echelle = 1.0/100
quitter = False

def reset():
    global ecran, noir, X, Y, x, y, v_x, v_y, a_y, alpha, t
#    ecran.fill(noir)
    t = 0
    X = 0
    Y = hauteur
    x = 0
    y = 0
    v_x = v*math.cos(alpha)
    v_y = v*math.sin(alpha)
    a_y = -9.81

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
                alpha = 0
                reset()

    if y >= 0 and X < largeur:
        t += 1
        if abs(v_y) <= abs(a_y):
            pygame.draw.rect(ecran, magenta, (X-1, Y-1, 3, 3))
        else:
            if abs(alpha - math.pi/4) <= abs(deltaAlpha):
                pygame.draw.rect(ecran, bleu, (X, Y, 1, 1), 1)
            elif alpha < math.pi/4:
                pygame.draw.rect(ecran, vert, (X, Y, 1, 1), 1)
            else:
                pygame.draw.rect(ecran, blanc, (X, Y, 1, 1), 1)
        X = echelle * x
        Y = hauteur - echelle * y
        x = x+v_x
        v_y = v_y + a_y
        y = y+v_y
        V = math.sqrt(v_x*v_x + v_y*v_y)
        pygame.draw.rect(ecran, rouge, (X, Y, 1, 1), 1)

        infos = police.render("V = %s, Vx = %s , Vy = %s, Ay = %s, alpha = %s" % (V, v_x, v_y, a_y, alpha), True, rouge)

        # Affiche les courbes de vitesses (absolue, composante en X, composante en Y)
#        pygame.draw.rect(ecran, cyan,    (t, hauteur/2-hauteur/2*V  /v+infos.get_height(), 1, 1), 1)
#        pygame.draw.rect(ecran, magenta, (t, hauteur/2-hauteur/2*v_x/v+infos.get_height(), 1, 1), 1)
#        pygame.draw.rect(ecran, jaune,   (t, hauteur/2-hauteur/2*v_y/v+infos.get_height(), 1, 1), 1)

        ecran.fill(noir, (0, 0, largeur, infos.get_height()))
        ecran.blit(infos, (0, 0))
    else:
        if alpha >= 0 and alpha <= math.pi/2:
            alpha += deltaAlpha
            reset()

    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
