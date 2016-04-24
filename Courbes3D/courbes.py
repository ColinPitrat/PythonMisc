#!/usr/bin/python2
import pygame, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 640, 350

noir = 0
blanc = 255, 255, 255

x0 = largeur/2
y0 = hauteur/2

# Rayon de la base de la courbe
R = 60.0
X_step = 2*R/largeur

#############
# Variables #
#############

quitter = False
affiche_infos = False
couleurs = True
draw_y = True
police = pygame.font.SysFont("arial", 18);

# A, L et F sont des parametres de notre fonction
A = -0.4*hauteur
L = 1.0 / 640
F = 0.3
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
    global A, L, F
    v = A*math.exp(-L*r*r)*math.cos(F*r)
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
                L = L / 2
                redraw()
            if event.key == pygame.K_x:
                L = L * 2
                redraw()
            if event.key == pygame.K_a:
                F = F + 0.1
                redraw()
            if event.key == pygame.K_q:
                F = F - 0.1
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

    prev_x = None
    prev_s = None
    if X < R:
        minimum = 999999
        maximum = -minimum
        YMax = math.sqrt(R*R - X*X)
        Y = YMax
        while Y >= -YMax:
            c = f(math.sqrt(X*X + Y*Y))
            s = c - perspective*Y
            coul = 255
            if couleurs:
              coul = (255/A * abs(c)) % 255
            draw = False
            if s >= maximum:
                maximum = s
                draw = True
            if s < minimum:
                minimum = s
                draw = True
            if draw:
                if draw_y and ((x % 20) == 0 or X + X_step >= R) and prev_x is not None:
                    pygame.draw.line(ecran, (255, coul, coul), (x0 + prev_x, y0 + prev_s), (x0 + x, y0 + s), 1)
                    pygame.draw.line(ecran, (255, coul, coul), (x0 - prev_x, y0 + prev_s), (x0 - x, y0 + s), 1)
                else:
                    pygame.draw.rect(ecran, (255, coul, coul), (x0 + x, y0 + s, 1, 1), 1)
                    pygame.draw.rect(ecran, (255, coul, coul), (x0 - x, y0 + s, 1, 1), 1)
                prev_x = x
                prev_s = s
            Y = Y - 1
        x = x + 1
        X = X + X_step

    if affiche_infos:
        infos = police.render("A=%s - L=%s - F=%s - p=%s" % (A, L, F, perspective), True, blanc)
        ecran.blit(infos, (0, 0))
    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
