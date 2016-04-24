#!/usr/bin/python2
import pygame, random, math, time
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 700, 700

noir = 0, 0, 0
rouge = 255, 0, 0
blanc = 255, 255, 255

zoom = 4
Largeur = largeur / zoom
Hauteur = hauteur / zoom

#############
# Variables #
#############

couleur = (255, 0, 0)
delta_couleur = (-1, 1, 0)

nombre_marcheurs = 10000
m_x = 0
m_y = 0
reseau = []
for i in range(0, Largeur):
    reseau.append([])
    for j in range(0, Hauteur):
        reseau[i].append(0)

##################
# Initialisation #
##################
taille_croix = 5
ecran = pygame.display.set_mode(resolution)
for i in range (int(Largeur/2) - taille_croix, int(Largeur/2) + taille_croix):
    reseau[i][int(Hauteur/2)] = 1
    pygame.draw.rect(ecran, rouge, (zoom * i, zoom * int(Hauteur/2), zoom, zoom))
for j in range (int(Hauteur/2) - taille_croix, int(Hauteur/2) + taille_croix):
    reseau[int(Largeur/2)][j] = 1
    pygame.draw.rect(ecran, rouge, (zoom * int(Largeur/2), zoom * j, zoom, zoom))

#####################
# Boucle principale #
#####################
quitter = False
finished = False
while quitter != True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True

    if not finished:
        dx = dy = 0
        while dx == 0 and dy == 0:
            if random.randint(0,1) == 1:
                dx = random.randint(-1, 1)
                if m_x + dx < 0:
                    dx += Largeur
                if m_x + dx >= Largeur:
                    dx -= Largeur
            else:
                dy = random.randint(-1, 1)
                if m_y + dy < 0:
                    dy += Hauteur
                if m_y + dy >= Hauteur:
                    dy -= Hauteur
        if reseau[m_x + dx][m_y + dy] == 1:
            reseau[m_x][m_y] = 1
            pygame.draw.rect(ecran, couleur, (zoom * m_x, zoom * m_y, zoom, zoom))
            m_x = 0
            m_y = 0
            if reseau[m_x][m_y] == 1:
                finished = True
            couleur = tuple(x+y for x,y in zip(couleur, delta_couleur))
            print("couleur = ", couleur)
            if couleur == (0, 255, 0):
                delta_couleur = (0, -1, 1)
            if couleur == (0, 0, 255):
                delta_couleur = (1, 0, -1)
            if couleur == (255, 0, 0):
                delta_couleur = (-1, 1, 0)
        else:
            pygame.draw.rect(ecran, noir, (zoom * m_x, zoom * m_y, zoom, zoom))
            pygame.draw.rect(ecran, blanc, (zoom * (m_x + dx), zoom * (m_y + dy), zoom, zoom))
            m_x += dx
            m_y += dy
    
    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
