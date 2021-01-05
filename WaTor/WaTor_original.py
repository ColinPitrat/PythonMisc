#!/usr/bin/python2

# Wa-Tor: https://en.wikipedia.org/wiki/Wa-Tor

import pygame, random, numpy
import pygame.gfxdraw

# Profiling
import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()

pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 256, 256

noir = 0, 0, 0
rouge = 255, 0, 0
vert = 0, 255, 0
bleu = 0, 0, 255
cyan = 0, 255, 255
magenta = 255, 0, 255
jaune = 255, 255, 0
blanc = 255, 255, 255

cote_cellule = 1
marge = 0

largeur_reseau, hauteur_reseau = largeur/cote_cellule, hauteur/cote_cellule

reseau = []

delaiReproductionPoissons = 10
delaiReproductionRequins = 50
energieRequins = 20
energieParTour = 1
energiePoisson = 5

# Valeurs de l'article de Dewdney (avec un +1 sur delai & energie car je decremente avant):
# http://home.cc.gatech.edu/biocs1/uploads/2/wator_dewdney.pdf
delaiReproductionPoissons = 4
delaiReproductionRequins = 11
energieRequins = 4
energieParTour = 1
energiePoisson = 5

deplacements = [(-1, 0), (0, -1), (1, 0), (0, 1)]

def combinaisons(l):
    if len(l) == 0:
        return []
    if len(l) == 1:
        return [l]
    result = []
    for e in l:
        l2 = list(l)
        l2.remove(e)
        subs = combinaisons(l2)
        for s in subs:
            result.append([e] + s)
    return result

combi_deplacements = combinaisons(deplacements)
nb_deplacements = len(combi_deplacements)


randoms = numpy.random.randint(nb_deplacements, size=1000000)
randidx = 0
max_randidx = len(randoms)


def cell_at(r, x, y):
  return r[x % largeur_reseau][y % hauteur_reseau]

def set_cell_at(r, x, y, v):
  r[x % largeur_reseau][y % hauteur_reseau] = v

class Habitant(object):

    def __init__(self, x, y, delaiReproduction):
        self.x = x
        self.y = y
        self.delaiReproduction = delaiReproduction
        self.reproduction = delaiReproduction

    def move(self):
        raise "Unimplemented method"

    def type(self):
        raise "Unimplemented method"

    def couleur(self):
        raise "Unimplemented method"


class Poisson(Habitant):

    def __init__(self, x, y):
        Habitant.__init__(self, x, y, delaiReproductionPoissons)

    def move(self):
        global reseau, randidx
        self.reproduction -= 1
        idx = randoms[randidx]
        deplacements = combi_deplacements[idx]
        randidx += 1
        if randidx >= max_randidx:
            randidx = 0
        # Se deplace au hasard si possible
        for (dx, dy) in deplacements:
            if cell_at(reseau, self.x+dx, self.y+dy) is None:
                if self.reproduction <= 0:
                    set_cell_at(reseau, self.x, self.y, Poisson(self.x, self.y))
                    self.reproduction = self.delaiReproduction
                else:
                    set_cell_at(reseau, self.x, self.y, None)
                self.x += dx
                self.y += dy
                set_cell_at(reseau, self.x, self.y, self)
                return

        # Aucun mouvement possible

    def type(self):
        return "Poisson"

    def couleur(self):
        return vert


class Requin(Habitant):

    def __init__(self, x, y):
        Habitant.__init__(self, x, y, delaiReproductionRequins)
        self.energie = energieRequins

    def move(self):
        global reseau, randidx
        self.reproduction -= 1
        self.energie -= energieParTour
        if self.energie == 0: # Mort du requin
            set_cell_at(reseau, self.x, self.y, None)
            return
        idx = randoms[randidx]
        deplacements = combi_deplacements[idx]
        randidx += 1
        if randidx >= max_randidx:
            randidx = 0

        # Essaie d'abord de manger si possible
        for (dx, dy) in deplacements:
            cell = cell_at(reseau, self.x+dx,self.y+dy)
            if cell is not None and cell.type() == "Poisson":
                set_cell_at(reseau, self.x, self.y, None)
                if self.reproduction <= 0:
                    set_cell_at(reseau, self.x, self.y, Requin(self.x, self.y))
                    self.reproduction = self.delaiReproduction
                self.x += dx
                self.y += dy
                set_cell_at(reseau, self.x, self.y, self)
                self.energie += energiePoisson
                if self.energie > energieRequins:
                    self.energie = energieRequins
                return

        # Sinon se deplace au hasard si possible
        for (dx, dy) in deplacements:
            if cell_at(reseau,self.x+dx,self.y+dy) is None:
                set_cell_at(reseau, self.x, self.y, None)
                if self.reproduction <= 0:
                    set_cell_at(reseau,self.x,self.y, Requin(self.x, self.y))
                    self.reproduction = self.delaiReproduction
                self.x += dx
                self.y += dy
                set_cell_at(reseau,self.x,self.y, self)
                return

        # Aucun mouvement possible

    def type(self):
        return "Requin"

    def couleur(self):
        return bleu



#############
# Variables #
#############

quitter = False
pause = False
random_conf = False
show_info = True
show_courbe = False

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
police = pygame.font.SysFont("arial", 20);
pygame.display.set_caption("Automates cellulaires - dimension 2")

def init():
  global reseau, largeur_reseau, hauteur_reseau
  # Cree la table de l'automate
  for x in range(0, largeur_reseau):
    reseau.append([])
    for y in range(0, hauteur_reseau):
      reseau[x].append(None)


historique_requins = []
historique_poissons = []

def reinit():
  global reseau, largeur_reseau, hauteur_reseau, ecran, noir, random_conf, historique_requins, historique_poissons
  ecran.fill(noir)
  pygame.display.flip()

  # Cree la configuration initiale
  for x in range(0, largeur_reseau):
    for y in range(0, hauteur_reseau):
      if random_conf:
        v = random.randint(0, 5)
        if v == 0:
          reseau[x][y] = Requin(x, y)
        elif v == 1:
          reseau[x][y] = Poisson(x, y)
        else:
          reseau[x][y] = None
      else:
        reseau[x][y] = None

  historique_poissons = []
  historique_requins = []


#####################
# Boucle principale #
#####################
init()
reinit()
reseau[128][128] = Poisson(128, 128)
i = 0
while quitter != True:
    # Boucle d'evenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            x = event.pos[0]/cote_cellule
            y = event.pos[1]/cote_cellule
            if x < largeur_reseau and y < hauteur_reseau:
              if pygame.mouse.get_pressed()[0]:
                reseau[x][y] = Requin(x, y)
              if pygame.mouse.get_pressed()[2]:
                reseau[x][y] = Poisson(x, y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            elif event.key == pygame.K_r:
                random_conf = not random_conf
                reinit()
            elif event.key == pygame.K_n:
                reinit()
            elif event.key == pygame.K_c:
                show_courbe = not show_courbe
            elif event.key == pygame.K_i:
                show_info = not show_info
            elif event.key == pygame.K_SPACE:
                pause = not pause

    nb_requins = 0
    nb_poissons = 0
    # Calcul de la generation suivante
    if not pause:
      for x in range(0, largeur_reseau):
        for y in range(0, hauteur_reseau):
          if reseau[x][y] is not None:
            t = reseau[x][y].type()
            if t == "Poisson":
                nb_poissons += 1
            elif t == "Requin":
                nb_requins += 1
            reseau[x][y].move()
      historique_requins.append(nb_requins)
      historique_poissons.append(nb_poissons)

    ecran.fill(noir)
    # Affiche le resultat
    if show_courbe:
      max_x = max(len(historique_requins), 1)
      max_y = max(max(historique_requins), max(historique_poissons), 1)
      x_scale = 1.0*largeur / max_x
      y_scale = 1.0*hauteur / max_y
      x = 0
      for r in historique_requins:
          x += 1
          pygame.gfxdraw.box(ecran, (x*x_scale, hauteur-int(r*y_scale), 2, 2), bleu)
      x = 0
      for p in historique_poissons:
          x += 1
          pygame.gfxdraw.box(ecran, (x*x_scale, hauteur-int(p*y_scale), 2, 2), vert)
    else:
        y = 0
        for x in range(0, largeur_reseau):
          for y in range(0, hauteur_reseau):
            if reseau[x][y] is not None:
              pygame.gfxdraw.box(ecran, (cote_cellule*x + marge, cote_cellule*y + marge, cote_cellule - marge, cote_cellule - marge), reseau[x][y].couleur())

    infos = police.render("Requins: %s - Poissons: %s" % (nb_requins, nb_poissons), True, rouge)
    pygame.gfxdraw.box(ecran, (largeur - infos.get_width(), hauteur - infos.get_height(), infos.get_width(), infos.get_height()), noir)
    ecran.blit(infos, (largeur - infos.get_width(), hauteur - infos.get_height()))

    pygame.display.flip()

    i += 1
    if i == 50:
        reseau[128][128] = Requin(128, 128)
    if i == 1000:
        quitter = True

###############
# Terminaison #
###############
pygame.quit()

# Profiling
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
