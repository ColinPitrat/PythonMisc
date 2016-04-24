#!/usr/bin/python2
import pygame, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 700, 500

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
R1 = 30
R2 = 60
R0 = (R1 + R2) / 2
r0 = (R2 - R1) / 2
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
    global A, R0, R1, R2, r0
    v = None
    if r >= R1 and r <= R2:
        v = -A*r0*math.sin(math.acos((r - R0)/r0))
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
        minimum_p = 999999
        maximum_p = -999999
        minimum_n = 999999
        maximum_n = -999999
        YMax = math.sqrt(R*R - X*X)
        Y = YMax
        while Y >= -YMax:
            c = f(math.sqrt(X*X + Y*Y))
            if c is not None:
                s = c - perspective*Y
                t = -c - perspective*Y
                coul = 255
                if couleurs:
                  coul = (255/(A*r0) * abs(c)) % 255
                draw_s = False
                draw_t = False
                if Y >= 0:
                    if s >= maximum_p:
                        maximum_p = s
                        draw_s = True
                    if s < minimum_p:
                        minimum_p = s
                        draw_s = True
                    if t >= maximum_p:
                        maximum_p = t
                        draw_t = True
                    if t < minimum_p:
                        minimum_p = t
                        draw_t = True
                else:
                    if s >= maximum_n and (s >= maximum_p or s < minimum_p):
                        maximum_n = s
                        draw_s = True
                    if s < minimum_n and (s >= maximum_p or s < minimum_p):
                        minimum_n = s
                        draw_s = True
                    if t >= maximum_n and (t >= maximum_p or t < minimum_p):
                        maximum_n = t
                        draw_t = True
                    if t < minimum_n and (t >= maximum_p or t < minimum_p):
                        minimum_n = t
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
