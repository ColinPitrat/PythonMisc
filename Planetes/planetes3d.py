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

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def carre_distance(self, other):
        return (self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2

    def distance(self, other):
        return math.sqrt(self.carre_distance(other))

    def __str__(self):
        return "(%s, %s, %s)" % (self.x, self.y, self.z)


class Corps(object):

    def __init__(self, name, position, vitesse, masse, diametre, couleur, trace):
        self._name = name
        self._pos = position
        self._masse = masse
        self._taille = diametre
        self._vitesse = vitesse
        self._couleur = couleur
        self._trace = trace


masse_soleil = 1.98855e30
masse_mercure = 3.3011e23
masse_venus = 4.8675e24
masse_terre = 5.97237e24
masse_lune = 7.342e22
masse_mars = 6.4171e23
masse_jupiter = 1.8982e27
masse_saturne = 5.6834e26
masse_uranus = 8.6810e25
masse_neptune = 1.0243e26

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
p0_soleil = Position(992681496.739200, 70398818.0067215, 2216636.38337567)
# TODO: Syntax p + p
p0_mercure = Position(49380079459.2802, 14241521455.1545, 2536963889.71312)
p0_venus = Position(81946474380.0193, -64369613677.8244, -34096537393.1433)
p0_terre = Position(25747629293.9908, -137607068800.190, -59725875994.0898)
p0_lune = Position(p0_terre.x-16470250.3596576, p0_terre.y+358077908.180965, p0_terre.z+178283080.729064)
p0_mars = Position(-244850004252.896, 27593592152.0310, 19330638480.2682)
p0_jupiter = Position(-787463907684.725, 168931700682.005, 91645880283.7390)
p0_saturne = Position(-740058782663.621, -1207735549729.54, -466799428701.107)
p0_uranus = Position(-1450255731709.32, -2218351876501.55, -951029717065.071)
p0_neptune = Position(657202451310.559, 4095117111566.13, 1659812729575.99)
v0_soleil = [0000.729748066150916, 0011.9097740688431, 0005.10725574999813]
v0_mercure = [-22975.0000067609, 42534.9111126741, 25101.5031758128]
v0_venus = [23171.0368891155, 24191.3965080077, 9406.61390814358]
v0_terre = [28917.5292511539, 4361.19205342266, 1893.55152590164]
v0_lune = [v0_terre[0]-981.430804599795, v0_terre[1]-31.5996121108727, v0_terre[2]-95.0083624125734]
v0_mars = [-2295.26242720580, -19972.1719385533, -9097.49512859968]
v0_jupiter = [-3235.16524153528, -11129.8961768755, -4692.74939907665]
v0_saturne = [7853.32180659251, -4343.35768403540, -2129.64973131718]
v0_uranus = [5784.32799941912, -3474.20125389939, -1603.78055731200]
v0_neptune = [-5407.50121294795, 0723.356213112248, 0430.644132604786]

G = 6.67408e-11

def main():
    pygame.init()

    ecran = pygame.display.set_mode(resolution)
    police = pygame.font.SysFont("arial", 15)
    pygame.display.set_caption("Systeme terre-lune-soleil")

    #ratio = (2.1*p0_terre.distance(p0_soleil)) / min(largeur, hauteur)
    #decalage = Position(largeur/2, hauteur/2, 0)
    #ratio = (3.1*p0_mercure.distance(p0_soleil)) / min(largeur, hauteur)
    #decalage = Position(largeur/2, hauteur/2, 0)
    #ratio = (0.5*p0_terre.distance(p0_soleil)) / min(largeur, hauteur)
    #decalage = Position(0, -1.0*hauteur, 0)
    #ratio = (2.1*p0_mars.distance(p0_soleil)) / min(largeur, hauteur)
    #decalage = Position(largeur/2, hauteur/2, 0)
    ratio = (2.1*p0_neptune.distance(p0_soleil)) / min(largeur, hauteur)
    decalage = Position(largeur/2, hauteur/2, 0)
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
    #corps = [Soleil, Mercure, Venus, Terre, Lune, Mars]
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
                # TODO: Ameliorere en trancant sur une surface immense et en n'en affichant qu'une partie
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
            accel = [0, 0, 0]
            for c2 in corps:
                if c1 != c2:
                    accel_tot = -G*c2._masse/c1._pos.carre_distance(c2._pos)
                    d = c1._pos.distance(c2._pos)
                    accel[0] += accel_tot*((c1._pos.x-c2._pos.x)/d)
                    accel[1] += accel_tot*((c1._pos.y-c2._pos.y)/d)
                    accel[2] += accel_tot*((c1._pos.z-c2._pos.z)/d)
            c1._vitesse[0] += accel[0] * d_t
            c1._vitesse[1] += accel[1] * d_t
            c1._vitesse[2] += accel[2] * d_t

        # Mouvement des corps
        for c in corps:
            c._pos.x += c._vitesse[0]*d_t
            c._pos.y += c._vitesse[1]*d_t
            c._pos.z += c._vitesse[2]*d_t
            # TODO: Trace
            pygame.draw.circle(ecran, c._couleur, (int(c._pos.x/ratio+decalage.x), int(c._pos.y/ratio+decalage.y)), int(c._taille/ratio))

        time += delta
        if time == datetime.datetime(year=1898, month=6, day=29, hour=12):
            for c in corps:
                print("%s: pos%s vit%s" % (c._name, c._pos, tuple(c._vitesse)))

        pygame.display.flip()


if __name__ == '__main__':
    main()
