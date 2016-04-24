#!/usr/bin/python2
import pygame, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 700, 700

noir = 0
blanc = 255, 255, 255

x0 = largeur/2
y0 = hauteur/2

# Rayon de la base de la courbe
R = 60.0
X_step = 2*R/largeur
Y_step = 1

#############
# Variables #
#############

quitter = False
affiche_infos = False
couleurs = False
draw_y = False
police = pygame.font.SysFont("arial", 18);

A = 5
R0 = 50
# Facteur de perspective
perspective = -1.5
# x et y sont les co-ordonnees a l'ecran (avant l'ajustement au centre)
x = 0
# X et Y sont les co-ordonnees dans le monde en 3D
X = 0

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)

def f(r):
    global A, R0
    v = None
    if R0 >= r:
        v = A*math.sqrt(R0*R0 - r*r)
    return v

def redraw():
    global ecran, noir, X, x
    ecran.fill(noir)
    X = 0
    x = 0

redraw()
#####################
# Boucle principale #
#####################
while quitter == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            if event.key == pygame.K_p:
                perspective += 0.1
                redraw()
            if event.key == pygame.K_m:
                perspective -= 0.1
                redraw()
            if event.key == pygame.K_w:
                if Y_step <= 0.1:
                    Y_step += 0.01
                else:
                    Y_step += 0.1
                redraw()
            if event.key == pygame.K_x:
                if Y_step > 0.15:
                    Y_step -= 0.1
                elif Y_step > 0.015:
                    Y_step -= 0.01
                redraw()
            if event.key == pygame.K_a:
                if A > 1:
                    A -= 1
                redraw()
            if event.key == pygame.K_q:
                A += 1
                redraw()
            if event.key == pygame.K_y:
                draw_y = not draw_y
                redraw()
            if event.key == pygame.K_i:
                affiche_infos = not affiche_infos
                redraw()
            if event.key == pygame.K_c:
                couleurs = not couleurs
                redraw()

    if X < R:
        minimum = 999999
        maximum = -999999
        YMax = math.sqrt(R*R - X*X)
        Y = YMax
        while Y >= -YMax:
            c = f(math.sqrt(X*X + Y*Y))
            if c is not None:
                s = c - perspective*Y
                t = -c - perspective*Y
                coul = 255
                if couleurs:
                  coul = (255/(A*R0) * abs(c)) % 255
                draw_s = False
                draw_t = False
                if s >= maximum:
                    maximum = s
                    draw_s = True
                if s < minimum:
                    minimum = s
                    draw_s = True
                if t >= maximum:
                    maximum = t
                    draw_t = True
                if t < minimum:
                    minimum = t
                    draw_t = True
                if draw_s:
                    pygame.draw.rect(ecran, (255, coul, coul), (x0 + x, y0 + s, 1, 1), 1)
                    pygame.draw.rect(ecran, (255, coul, coul), (x0 - x, y0 + s, 1, 1), 1)
                if draw_t:
                    pygame.draw.rect(ecran, (255, coul, coul), (x0 + x, y0 + t, 1, 1), 1)
                    pygame.draw.rect(ecran, (255, coul, coul), (x0 - x, y0 + t, 1, 1), 1)
            Y = Y - Y_step
        x = x + 1
        X = X + X_step

    if affiche_infos:
        infos = police.render("A=%s - dY=%s - p=%s" % (A, Y_step, perspective), True, blanc)
        ecran.blit(infos, (0, 0))
    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
