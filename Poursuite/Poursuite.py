#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Un "jeu" de poursuite. Les deux points se déplacent toujours à la même
# vitesse.
# Le point bleu décrit simplement un cercle.
# Le point violet se déplace toujours en direction du point bleu.

import pygame, random, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 1600, 1000

noir = 0, 0, 0
rouge = 255, 0, 0
vert = 0, 255, 0
bleu = 0, 0, 255
cyan = 0, 255, 255
magenta = 255, 0, 255
jaune = 255, 255, 0
blanc = 255, 255, 255

couleurs = [ rouge, vert, bleu, cyan, magenta, jaune ]

nombre_pas = 250000
taille_pas = 1
marge = 10

#############
# Variables #
#############
quitter = False
cible = None
ancienne_cible = None
centre = None
t = 0
rayon = None
suiveur = None
ancien_suiveur = None
plan = None
police = pygame.font.SysFont("arial", 30);

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("Poursuite")

def reset():
   global cible, centre, t, rayon, suiveur, plan, ancienne_cible, ancien_suiveur
   plan = pygame.Surface(resolution)
   rayon = random.randint(0, min(largeur, hauteur)/2)
   centre = [random.randint(rayon, largeur - rayon), random.randint(rayon, hauteur - rayon)]
   cible = [centre[0], centre[1]-rayon]
   suiveur = [random.randint(0, largeur), random.randint(0, hauteur)]
   ancien_suiveur = None
   ancienne_cible = None
   t = 0
   plan.fill(noir)

def distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx*dx + dy*dy)

def roundPoint(point):
   return [int(point[0]), int(point[1])]

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
                reset()

    if ancienne_cible is not None:
       pygame.draw.line(plan, bleu, roundPoint(ancienne_cible), roundPoint(cible))
    if ancien_suiveur is not None:
       pygame.draw.line(plan, magenta, roundPoint(ancien_suiveur), roundPoint(suiveur))
    # Fait avancer la cible
    #dx = centre[0] - cible[0]
    #dy = centre[1] - cible[1]
    #d = math.sqrt(dx*dx + dy*dy)
    #print("Cible: %s - Centre: %s - dx = %s - dy = %s - d = %s" % (cible, centre, dx, dy, d)) 
    #dx = dx/d
    #dy = dy/d
    ancienne_cible = cible
    #cible[0] += dy
    #cible[1] -= dx
    t += 1.0
    cible[0] = centre[0] + rayon*math.cos(t/rayon)
    cible[1] = centre[1] + rayon*math.sin(t/rayon)
    print("Cible: %s - t = %s - cos(t) = %s - sin(t) = %s" % (cible, t, math.cos(t/rayon), math.sin(t/rayon)))

    # Fait avancer le suiveur
    dx = ancienne_cible[0] - suiveur[0]
    dy = ancienne_cible[1] - suiveur[1]
    d = math.sqrt(dx*dx + dy*dy)
    print("Cible: %s - Suiveur: %s - dx = %s - dy = %s - d = %s" % (cible, suiveur, dx, dy, d))
    dx = dx/d
    dy = dy/d
    ancien_suiveur = suiveur
    suiveur[0] += dx
    suiveur[1] += dy

    print("Ancienne cible: %s" % ancienne_cible)
    print("Cible: %s" % cible)
    pygame.draw.line(plan, blanc, roundPoint(ancienne_cible), roundPoint(cible))
    print("Ancienne suiveur: %s" % ancien_suiveur)
    print("Suiveur: %s" % suiveur)
    pygame.draw.line(plan, jaune, roundPoint(ancien_suiveur), roundPoint(suiveur))

    ecran.blit(plan, (0, 0))
    infos = police.render("d = %s" % distance(cible, suiveur), True, blanc)
    ecran.blit(infos, (0, 0))
    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
