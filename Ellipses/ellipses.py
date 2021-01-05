# -*- coding: utf-8 -*-
import pygame

# Une forme de généralisation des ellipses.
# On choisit un ensemble de "foyers" (clic droit) et un point sur la forme à
# tracer (clic gauche).
#
# Par exemple: 
#  - un premier clic droit désigne le centre A d'un cercle. Un clic gauche qui
# suit permet alors de désigner un point M sur le cercle et donc de déduire le
# rayon R du cercle. Le programme trace alors le cercle de centre A et passant
# par M (qui a donc un rayon R).
#  - deux clics droits désignent les foyers A et B d'une ellipse. Un clic
# gauche désigne un point M sur l'ellipse à tracer. Le programme trace alors
# l'ellipse de foyers A et B passant par M, c'est à dire l'ensemble des points
# N tels que d(A,N)+d(B,N) = d(A,M)+d(B,M) où d() désigne la distance entre les
# deux points.
#  - d'une manière générale, n clics droits désignent n points A_n. Le clic
# gauche désigne un point M sur la figure à tracer. La figure sera l'ensemble
# des points N tels que sum(i=0..n, d(A_i,N)) = sum(i=0..n, d(A_i,M))

##############
# Constantes #
##############

resolution = largeur, hauteur = 600, 600

noir = 0, 0, 0
rouge = 255, 0, 0
vert = 0, 255, 0
bleu = 0, 0, 255
cyan = 0, 255, 255
magenta = 255, 0, 255
jaune = 255, 255, 0
blanc = 255, 255, 255

def distance(p1, p2):
    return ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5

def somme_distances(points, point):
    d = 0
    for p in points:
        d += distance(p, point)
    return d

def dessine(ecran, points, point, epsilon):
    print("Dessine commence")
    pygame.draw.rect(ecran, blanc, (0, 0, largeur, hauteur), 0)
    if point:
        rayon = somme_distances(points, point)
        print("Rayon = %s" % rayon)
        for x in range(0, largeur):
            for y in range(0, hauteur):
                SD = somme_distances(points, (x, y))
                if abs(somme_distances(points, (x, y)) - rayon) < epsilon:
                    pygame.draw.rect(ecran, bleu, (x, y, 2, 2), 0)
        pygame.draw.circle(ecran, magenta, (point[0], point[1]), epsilon)
    for p in points:
        pygame.draw.circle(ecran, rouge, (p[0], p[1]), epsilon)
    pygame.display.flip()
    print("Dessine fini")

def main():
    pygame.init()

    ecran = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Generalisation des ellipses")

    points = []
    point = None
    quitter = False
    epsilon = 5
    change = True
    while not quitter:
        # Boucle d'evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitter = True
                if event.key == pygame.K_r:
                    points = []
                    point = None
                    epsilon = 5
                    change = True
                if event.key == pygame.K_p:
                    change = True
                    epsilon += 1
                    print("Epsilon = %s" % epsilon)
                if event.key == pygame.K_m:
                    change = True
                    epsilon -= 1
                    print("Epsilon = %s" % epsilon)
            if event.type == pygame.MOUSEBUTTONDOWN:
                change = True
                x = event.pos[0]
                y = event.pos[1]
                if pygame.mouse.get_pressed()[0]:
                  points.append((x, y))
                if pygame.mouse.get_pressed()[2]:
                  point = (x, y)
        if change:
            dessine(ecran, points, point, epsilon)
            change = False


if __name__ == '__main__':
    main()
