# -*- coding: utf-8 -*-

import pygame
import math
import datetime

##############
# Constantes #
##############

resolution = largeur, hauteur = 2500, 1400

noir = 0, 0, 0
rouge = 255, 0, 0
vert = 0, 255, 0
bleu = 0, 0, 255
cyan = 0, 255, 255
magenta = 255, 0, 255
jaune = 255, 255, 0
blanc = 255, 255, 255


class Position(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def carre_distance(self, other):
        return (self.x-other.x)**2 + (self.y-other.y)**2

    def distance(self, other):
        return math.sqrt(self.carre_distance(other))

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)


class Corps(object):

    def __init__(self, name, position, vitesse, masse, diametre, couleur, trace):
        self._name = name
        self._pos = position
        self._masse = masse
        self._taille = diametre
        self._vitesse = vitesse
        self._couleur = couleur
        self._trace = trace


masse_soleil = 1.9891e30
masse_mercure = 3.3011e23
masse_venus = 4.8685e24
masse_terre = 5.9736e24
masse_lune = 7.3477e22
masse_mars = 641.85e21
masse_jupiter = 1.8986e27
masse_saturne = 568.46e24
masse_uranus = 8.6810e25
masse_neptune = 102.43e24

rayon_soleil = 696342000
rayon_mercure = 2439700
rayon_venus = 6051800
rayon_terre = 6378137
rayon_lune = 1737400
rayon_mars = 3396200
rayon_jupiter = 71492000
rayon_saturne = 60268000
rayon_uranus = 25559000
rayon_neptune = 24764000

# TODO: A corriger a partir des ephemerides
# TODO: Decalage a introduire: [ratio*largeur/2, ratio*hauteur/2]
p0_soleil = Position(0, 0)
# TODO: Syntax p + p
p0_mercure = Position(0, p0_soleil.y+46001272000)
p0_venus = Position(0, p0_soleil.y+107476259000)
p0_terre = Position(0, p0_soleil.y+147098074000)
p0_lune = Position(0, p0_terre.y+363104000)
p0_mars = Position(0, p0_soleil.y+206644545000)
p0_jupiter = Position(0, p0_soleil.y+740520000000)
p0_saturne = Position(0, p0_soleil.y+1349823615000)
p0_uranus = Position(0, p0_soleil.y+2734998229000)
p0_neptune = Position(0, p0_soleil.y+4452940833000)
v0_soleil = [-17, 0]
#v0_soleil = [-0.4, 0]
v0_mercure = [59980, 0]
v0_venus = [35260, 0]
v0_terre = [30287, 0]
v0_lune = [v0_terre[0]+1052, 0]
v0_mars = [26499, 0]
v0_jupiter = [13720, 0]
v0_saturne = [10183, 0]
v0_uranus = [7128, 0]
v0_neptune = [5479, 0]

G = 6.6742e-11

def zoom_mercure():
    """Zoom sur l'orbite de Mercure."""
    ratio = (4.1*p0_mercure.y) / min(largeur, hauteur)
    decalage = Position(largeur/2, hauteur/2)
    return ratio, decalage

def zoom_terre():
    """Zoom sur l'orbite de la Terre."""
    ratio = (2.1*p0_terre.y) / min(largeur, hauteur)
    decalage = Position(largeur/2, hauteur/2)
    return ratio, decalage

def zoom_terre_lune():
    """Zoom sur une petite partie de l'orbite de la Terre, pour voir le mouvement Terre-Lune."""
    ratio = (0.5*p0_terre.y) / min(largeur, hauteur)
    decalage = Position(0, -1.5*hauteur)
    return ratio, decalage

def zoom_mars():
    """Zoom sur l'orbite de Mars."""
    ratio = (3.1*p0_mars.y) / min(largeur, hauteur)
    decalage = Position(largeur/2, hauteur/2)
    return ratio, decalage

def zoom_systeme():
    """Vision globale du système solaire."""
    ratio = (2.1*p0_neptune.y) / min(largeur, hauteur)
    decalage = Position(largeur/2, hauteur/2)
    return ratio, decalage

def main():
    pygame.init()

    ecran = pygame.display.set_mode(resolution)
    police = pygame.font.SysFont("arial", 15)
    pygame.display.set_caption("Systeme terre-lune-soleil")

    ratio, decalage = zoom_systeme()

    Soleil = Corps("Soleil", p0_soleil, v0_soleil, masse_soleil, 2*rayon_soleil, jaune, vert)
    Mercure = Corps("Mercure", p0_mercure, v0_mercure, masse_mercure, 2*rayon_mercure, rouge, magenta)
    Venus = Corps("Venus", p0_venus, v0_venus, masse_venus, 2*rayon_venus, bleu, cyan)
    Terre = Corps("Terre", p0_terre, v0_terre, masse_terre, 2*rayon_terre, cyan, bleu)
    Lune = Corps("Lune", p0_lune, v0_lune, masse_lune, 2*rayon_lune, blanc, jaune)
    Mars = Corps("Mars", p0_mars, v0_mars, masse_mars, 2*rayon_mars, rouge, magenta)
    Jupiter = Corps("Jupiter", p0_jupiter, v0_jupiter, masse_jupiter, 2*rayon_jupiter, rouge, rouge)
    Saturne = Corps("Saturne", p0_saturne, v0_saturne, masse_saturne, 2*rayon_saturne, jaune, jaune)
    Uranus = Corps("Uranus", p0_uranus, v0_uranus, masse_uranus, 2*rayon_uranus, blanc, blanc)
    Neptune = Corps("Neptune", p0_neptune, v0_neptune, masse_neptune, 2*rayon_neptune, bleu, bleu)
    corps = [Soleil, Mercure, Venus, Terre, Lune, Mars, Jupiter, Saturne, Uranus, Neptune]
    quitter = False
    pause = False
    d_t = 3600*24 / 24
    delta = datetime.timedelta(seconds=d_t)
    time = datetime.datetime(year=1897, month=6, day=29, hour=12)
    #d_t = 3600*24 / 240
    while not quitter:
        # Boucle d'evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitter = True
                if event.key == pygame.K_p:
                    pause = not pause
                # TODO: Ameliorer en trancant sur une surface immense et en n'en affichant qu'une partie
                if event.key == pygame.K_UP:
                    ecran.scroll(0, 10)
                    decalage.y += 10
                if event.key == pygame.K_DOWN:
                    ecran.scroll(0, -10)
                    decalage.y -= 10
                if event.key == pygame.K_LEFT:
                    ecran.scroll(10, 0)
                    decalage.x += 10
                if event.key == pygame.K_RIGHT:
                    ecran.scroll(-10, 0)
                    decalage.x -= 10
        if pause:
            continue

        # Efface les corps existants / affiche la trace
        for c in corps:
            pygame.draw.circle(ecran, c._trace, (int(c._pos.x/ratio+decalage.x), int(c._pos.y/ratio+decalage.y)), int(c._taille/ratio))

        # Actions des corps les uns sur les autres
        for c1 in corps:
            accel = [0, 0]
            for c2 in corps:
                if c1 != c2:
                    accel_tot = -G*c2._masse/c1._pos.carre_distance(c2._pos)
                    d = c1._pos.distance(c2._pos)
                    accel[0] += accel_tot*((c1._pos.x-c2._pos.x)/d)
                    accel[1] += accel_tot*((c1._pos.y-c2._pos.y)/d)
            c1._vitesse[0] += accel[0] * d_t
            c1._vitesse[1] += accel[1] * d_t

        # Mouvement des corps
        for c in corps:
            c._pos.x += c._vitesse[0]*d_t
            c._pos.y += c._vitesse[1]*d_t
            # TODO: Trace
            pygame.draw.circle(ecran, c._couleur, (int(c._pos.x/ratio+decalage.x), int(c._pos.y/ratio+decalage.y)), int(c._taille/ratio))

        time += delta
        if time == datetime.datetime(year=1898, month=6, day=29, hour=12):
            for c in corps:
                print("%s: pos%s vit%s" % (c._name, c._pos, tuple(c._vitesse)))

        pygame.display.flip()


if __name__ == '__main__':
    main()
