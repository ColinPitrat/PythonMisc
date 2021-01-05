# -*- coding: utf8 -*-

# Visualisation du paradoxe de Simpson.
# En rouge et vert les cas où le paradoxe ne se produit pas.
# En blanc les cas où il se produit.
#
# L'approche est un peu bizarre puisqu'on fait varier le nombre de cas dans
# chaque catégorie (par exemple Homme/Placébo/Guéri ou
# Femme/Médicament/Non-guéri) entre 1 et M pour une valeur de M donnée.
#
# Ce n'est pas super logique puisque cela signifie que la taille de population
# varie selon le pixel considéré ... Une meilleure approche serait de faire la
# même chose pour une population de taille N fixe.

import pygame
import math
import time

##############
# Constantes #
##############

resolution = largeur, hauteur = 2500, 1400
resolution = largeur, hauteur = 1600, 1000

noir = 0, 0, 0
gris = 50, 50, 50
gris_sombre = 25, 25, 25
rouge = 255, 0, 0
rouge_sombre = 127, 0, 0
vert = 0, 255, 0
vert_sombre = 0, 127, 0
bleu = 0, 0, 255
cyan = 0, 255, 255
magenta = 255, 0, 255
jaune = 255, 255, 0
blanc = 255, 255, 255

def increment(stats, categorie):
    if not categorie in stats:
        stats[categorie] = 0
    stats[categorie] += 1

def afficheStats(stats):
    total = 0
    for k, v in stats.iteritems():
        total += v
    for k, v in stats.iteritems():
        print("%s: %s (%s%%)" % (k, v, 100.0*v/total))
    print("Total: %s" % total)

class SimpsonGraph(object):

    def __init__(self, M, zoom):
        self.M = M
        self.M2 = M**2
        self.M3 = M**3
        self.zoom = zoom
        cote = zoom*(M**4)
        self.surface = pygame.Surface((cote, cote))
        self.reset()

    def reset(self):
        print("Representation graphique du paradoxe de Simpson pour M=%s - zoom=%s" % (self.M, self.zoom))
        self.begin = time.time()
        self.surface.fill(noir)
        self.stats = {}
        self.a1 = 1
        self.a2 = 1
        self.b1 = 1
        self.b2 = 1
        self.c1 = 1
        self.c2 = 1

    def computeStep(self):
        if self.a1 > self.M:
            # Computed everything already
            return
        # Statistiques globales:
        #            | Gueri | Non-gueri |
        # Placebo    |     A |         B |
        # Medicament |     C |         D |
        #
        # Hommes:
        #            | Gueri | Non-gueri |
        # Placebo    |    a1 |        b1 |
        # Medicament |    c1 |        d1 |
        #
        # Femmes:
        #            | Gueri | Non-gueri |
        # Placebo    |    a2 |        b2 |
        # Medicament |    c2 |        d2 |
        for c1 in range(1, self.M+1):
            for c2 in range(1, self.M+1):
                for d1 in range(1, self.M+1):
                    for d2 in range(1, self.M+1):
                        x = self.zoom*((self.a1-1)*self.M3 + (self.b1-1)*self.M2 + (c1-1)*self.M + (d1-1))
                        y = self.zoom*((self.a2-1)*self.M3 + (self.b2-1)*self.M2 + (c2-1)*self.M + (d2-1))
                        a1 = 1.0*self.a1
                        b1 = 1.0*self.b1
                        c1 = 1.0*c1
                        d1 = 1.0*d1
                        a2 = 1.0*self.a2
                        b2 = 1.0*self.b2
                        c2 = 1.0*c2
                        d2 = 1.0*d2
                        A = a1+a2
                        B = b1+b2
                        C = c1+c2
                        D = d1+d2
                        #print("x=%s, y=%s - A/B = %s - C/D = %s - a1/b1 = %s - c1/d1 = %s - a2/b2 = %s - c2/d2 = %s" % (x, y, A/B, C/D, a1/b1, c1/d1, a2/b2, c2/d2))
                        # Le placebo est globalement meilleur que le medicament
                        if A/B > C/D:
                            # Et de meme pour les sous populations
                            if a1/b1 > c1/d1 and a2/b2 > c2/d2:
                                pygame.draw.rect(self.surface, rouge_sombre, (x, y, self.zoom+1, self.zoom+1), 0)
                                increment(self.stats, "Rouge")
                            # Mais pas pour les sous populations
                            elif a1/b1 < c1/d1 and a2/b2 < c2/d2:
                                #print("x=%s, y=%s - A/B = %s - C/D = %s - a1/b1 = %s - c1/d1 = %s - a2/b2 = %s - c2/d2 = %s" % (x, y, A/B, C/D, a1/b1, c1/d1, a2/b2, c2/d2))
                                pygame.draw.rect(self.surface, blanc, (x, y, self.zoom+1, self.zoom+1), 0)
                                increment(self.stats, "Blanc 1")
                            # Cas 'ininteressant'
                            else:
                                pygame.draw.rect(self.surface, gris_sombre, (x, y, self.zoom+1, self.zoom+1), 0)
                                increment(self.stats, "Gris 1")
                        # Le medicament est globalement meilleur que le placebo
                        elif A/B < C/D:
                            # Et de meme pour les sous populations
                            if a1/b1 < c1/d1 and a2/b2 < c2/d2:
                                pygame.draw.rect(self.surface, vert_sombre, (x, y, self.zoom+1, self.zoom+1), 0)
                                increment(self.stats, "Vert")
                            # Mais pas pour les sous populations
                            elif a1/b1 > c1/d1 and a2/b2 > c2/d2:
                                #print("x=%s, y=%s - A/B = %s - C/D = %s - a1/b1 = %s - c1/d1 = %s - a2/b2 = %s - c2/d2 = %s" % (x, y, A/B, C/D, a1/b1, c1/d1, a2/b2, c2/d2))
                                pygame.draw.rect(self.surface, blanc, (x, y, self.zoom+1, self.zoom+1), 0)
                                increment(self.stats, "Blanc 2")
                            # Cas 'ininteressant'
                            else:
                                pygame.draw.rect(self.surface, gris_sombre, (x, y, self.zoom+1, self.zoom+1), 0)
                                increment(self.stats, "Gris 2")
                        # Egalite: cas 'ininteressant'
                        else:
                            pygame.draw.rect(self.surface, gris_sombre, (x, y, self.zoom+1, self.zoom+1), 0)
                            increment(self.stats, "Gris 3")
        self.b2 += 1
        if self.b2 > self.M:
            self.b2 = 1
            self.b1 += 1
            if self.b1 > self.M:
                self.b1 = 1
                self.a2 += 1
                if self.a2 > self.M:
                    self.a2 = 1
                    self.a1 += 1
                    if self.a1 > self.M:
                        end = time.time()
                        print("Finished in %s seconds" % (end - self.begin))
                        afficheStats(self.stats)

def main():
    pygame.init()

    ecran = pygame.display.set_mode(resolution)
    police = pygame.font.SysFont("arial", 15)
    pygame.display.set_caption("Paradoxe de Simpson")

    change = True
    quitter = False
    M = 4
    zoom = 1
    graph = None
    dx, dy = 0, 0
    while not quitter:
        # Boucle d'evenements
        # TODO(cpitrat): Afficher infos a propos d'un point quand on le survole avec la souris (ou qu'on clique dessus)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitter = True
                if event.key == pygame.K_p:
                    change = True
                    M += 1
                if event.key == pygame.K_m:
                    if M > 2:
                        change = True
                        M -= 1
                if event.key == pygame.K_z:
                    if event.mod == pygame.KMOD_SHIFT or event.mod == pygame.KMOD_LSHIFT or event.mod == pygame.KMOD_RSHIFT:
                        zoom += 1
                        change = True
                    else:
                        if zoom > 1:
                            zoom -= 1
                            change = True
                if event.key == pygame.K_LEFT:
                    if dx > 0:
                        dx -= M*M
                if event.key == pygame.K_RIGHT:
                    if dx + largeur < graph.surface.get_width():
                        dx += M*M
                if event.key == pygame.K_UP:
                    if dy > 0:
                        dy -= M*M
                if event.key == pygame.K_DOWN:
                    if dy + hauteur < graph.surface.get_height():
                        dy += M*M

        if change:
            change = False
            try:
                graph = SimpsonGraph(M, zoom)
            except:
                # TODO(cpitrat): Message dans l'interface graphique
                print("Impossible de visualiser pour M=%s et zoom=%s" % (M, zoom))

        graph.computeStep()
        ecran.fill(noir)
        ecran.blit(graph.surface, (0, 0), (dx, dy, largeur, hauteur))
        pygame.display.flip()


if __name__ == '__main__':
    main()
