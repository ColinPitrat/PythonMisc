#!/usr/bin/python2

# Automates cellulaires a en dimension 2
# Problemes:
#  - beaucoup trop lent a initialiser pour nb_etats > 2
#  - les nombres representants les automates sont enormes meme pour 2 etats (jusqu'a 300 chiffres)
#  - la plupart des automates sont ininteressants
#  - il faut ecrire des methodes pour generer les nombres pour les configurations connues

# Le numero decrivant une transition est de la forme: a b c d e f g h i en base nb_etats
# pour le voisinage suivant du point e:
# i h g
# f e d
# c b a

import pygame, random
import pygame.gfxdraw
import numpy

# Profiling
import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()

pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 800, 800

noir = 0, 0, 0
rouge = 255, 0, 0
vert = 0, 255, 0
bleu = 0, 0, 255
cyan = 0, 255, 255
magenta = 255, 0, 255
jaune = 255, 255, 0
blanc = 255, 255, 255

couleurs = [ blanc, bleu, vert, rouge, cyan, magenta, jaune ]

# Avec un voisinage de 8 cellules plus la cellule elle meme, pour 2 etats, on a
# un maximum de 2^9 = 512 configuration de voisinage possible, Soit 2^512
# automates possibles
nb_etats = 2
max_voisinages = nb_etats**10
max_num_automate = nb_etats**max_voisinages

cote_cellule = 5
marge = 1

largeur_reseau, hauteur_reseau = largeur/cote_cellule, hauteur/cote_cellule

reseau = []
tmp_reseau = []

#############
# Variables #
#############

quitter = False
pause = False
step = False
random_conf = True
show_info = True

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
police = pygame.font.SysFont("arial", 20);
pygame.display.set_caption("Automates cellulaires - dimension 2")

def init():
  global reseau, tmp_reseau, largeur_reseau, hauteur_reseau
  # Cree la table de l'automate
  for x in range(0, largeur_reseau):
    reseau.append([])
    tmp_reseau.append([])
    for y in range(0, hauteur_reseau):
      reseau[x].append(0)
      tmp_reseau[x].append(0)


def reinit():
  global reseau, largeur_reseau, hauteur_reseau, ecran, noir, random_conf
  ecran.fill(noir)
  pygame.display.flip()

  # Cree la configuration initiale
  for x in range(0, largeur_reseau):
    for y in range(0, hauteur_reseau):
      if random_conf:
        reseau[x][y] = (random.randint(0, 1))
      else:
        reseau[x][y] = 0


def describe_automate(automate):
  print("Automate %s" % (automate))


#################################################
# Calcul les transitions d'automates classiques #
#################################################

def nb_states_in_voisinage(state, nb):
    num = 0
    while nb > 0:
        if nb % nb_etats == state:
            num += 1
        nb = nb / nb_etats
    return num

def is_self_in_state(state, nb):
    return ((nb / (nb_etats ** 4)) % nb_etats) == state

# Necessite 2 etats au moins
def make_game_of_life():
  result = []
  for nb in range(0, max_voisinages):
    alives = nb_states_in_voisinage(1, nb)
    if is_self_in_state(1, nb): # La cellule est vivante
        if alives == 3 or alives == 4: # 2 ou 3 cellules vivantes en plus d'elle
            #print("Alive and stay alive for %s" % bin(nb))
            result.append(1)
        else:
            result.append(0)
    else: # La cellule est morte
        if alives == 3: # 3 cellules vivantes autour d'elle
            #print("Dead and become alive for %s" % bin(nb))
            result.append(1)
        else:
            result.append(0)
  #print("Game of life is: %s" % result)
  return result


# Necessite 2 etats au moins
def make_seeds():
  result = []
  for nb in range(0, max_voisinages):
    #alives = bin(nb).count('1')
    alives = nb_states_in_voisinage(1, nb)
    if is_self_in_state(1, nb): # La cellule est vivante
        if alives == 3: # 2 cellules vivantes en plus d'elle
            #print("Alive and stay alive for %s" % bin(nb))
            result.append(1)
        else:
            result.append(0)
    else: # La cellule est morte
        if alives == 2: # 2 cellules vivantes autour d'elle
            #print("Dead and become alive for %s" % bin(nb))
            result.append(1)
        else:
            result.append(0)
  #print("Seeds is: %s" % result)
  return result

# Necessite 2 etats au moins
def make_life_without_death():
  result = []
  for nb in range(0, max_voisinages):
    alives = nb_states_in_voisinage(1, nb)
    if is_self_in_state(1, nb): # La cellule est vivante
        result.append(1)
    else: # La cellule est morte
        if alives == 3: # 3 cellules vivantes autour d'elle
            #print("Dead and become alive for %s" % bin(nb))
            result.append(1)
        else:
            result.append(0)
  #print("Life without death is: %s" % result)
  return result

# Necessite 2 etats au moins
def make_day_and_night():
  result = []
  for nb in range(0, max_voisinages):
    alives = nb_states_in_voisinage(1, nb)
    if is_self_in_state(1, nb): # La cellule est vivante
        if alives == 4 or alives == 5 or alives >= 7: # 3, 4, 6, 7 ou 8 cellules vivantes en plus d'elle
            #print("Alive and stay alive for %s" % bin(nb))
            result.append(1)
        else:
            result.append(0)
    else: # La cellule est morte
        if alives == 3 or alives >= 6: # 3, 6, 7 ou 8 cellules vivantes autour d'elle
            #print("Dead and become alive for %s" % bin(nb))
            result.append(1)
        else:
            result.append(0)
  #print("Day and night is: %s" % result)
  return result


# Necessite 3 etats au moins - 0 est morte, 1 est vivant, 2 est mourrant
def make_brian_brain():
  result = []
  for nb in range(0, max_voisinages):
    alives = nb_states_in_voisinage(1, nb)
    if is_self_in_state(0, nb): # La cellule est morte, ell ne nait que si elle a 2 voisines
        if alives == 2: # 2 cellules vivantes
            result.append(1)
        else:
            result.append(0)
    elif is_self_in_state(1, nb): # La cellule est vivante, elle sera mourrante
        result.append(2)
    # Si la cellule est mourrante, elle sera morte ensuite donc on n'ajoute rien a num
    else:
        result.append(0)
  #print("Brian is: %s" % result)
  return result

# Necessite 2 etats au moins
# Une cellule est vivante a t+1 si elle a un nombre impair de voisins vivant a t
def make_replicator():
  result = []
  for nb in range(0, max_voisinages):
    alives = nb_states_in_voisinage(1, nb)
    if is_self_in_state(0, nb):
        result.append(alives % 2)
    else:
        result.append((alives+1) % 2)
  #print("Replicator is: %s" % result)
  return result

# Necessite 2 etats au moins
# Une cellule est vivante a t+1 si elle a un nombre impair de voisins (incluant elle meme) vivant a t
def make_replicator2():
  result = []
  for nb in range(0, max_voisinages):
    alives = nb_states_in_voisinage(1, nb)
    result.append(alives % 2)
  #print("Replicator is: %s" % result)
  return result

def make_random():
  #return [random.randint(0, nb_etats) for x in range(0, max_voisinages)]
  return numpy.random.randint(nb_etats, size=max_voisinages)

def prev_automate():
  global transition
  for idx in range(-1, -max_voisinages, -1):
      transition[idx] -= 1
      if transition[idx] == -1:
        transition[idx] = nb_etats
      else:
        break

def next_automate():
  global transition
  for idx in range(-1, -max_voisinages, -1):
      transition[idx] += 1
      if transition[idx] == nb_etats:
        transition[idx] = 0
      else:
        break

#transition = make_game_of_life()
#transition = make_life_without_death()
#transition = make_seeds()
#transition = make_brian_brain()
#transition = make_random()
#transition = make_day_and_night()
transition = make_replicator()
#####################
# Boucle principale #
#####################
init()
reinit()
while quitter != True:
    # Boucle d'evenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            x = event.pos[0]/cote_cellule
            y = event.pos[1]/cote_cellule
            if pygame.mouse.get_pressed()[0]:
              reseau[x][y] = 1
            if pygame.mouse.get_pressed()[2]:
              reseau[x][y] = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            elif event.key == pygame.K_p:
                next_automate()
                #describe_automate(transition)
                reinit();
            elif event.key == pygame.K_m:
                prev_automate()
                #describe_automate(transition)
                reinit()
            elif event.key == pygame.K_n:
                transition = make_random()
                #describe_automate(transition)
                reinit()
            elif event.key == pygame.K_r:
                random_conf = not random_conf
                reinit()
            elif event.key == pygame.K_c:
                reinit();
            elif event.key == pygame.K_i:
                show_info = not show_info
            elif event.key == pygame.K_s:
                step = True
            elif event.key == pygame.K_SPACE:
                pause = not pause

    # Calcul de la generation suivante
    if not pause or step:
      step = False
      for x in range(0, largeur_reseau):
        for y in range(0, hauteur_reseau):
          nb = 0
          for dx in range(0, 3):
            for dy in range(0, 3):
                nb *= nb_etats
                nb += reseau[(x+dx-1)%largeur_reseau][(y+dy-1)%hauteur_reseau]
          if transition[nb] is None:
            compute_transition(nb)
          tmp_reseau[x][y] = transition[nb]
      reseau, tmp_reseau = tmp_reseau, reseau

    ecran.fill(noir)
    # Affiche le resultat
    y = 0
    for x in range(0, largeur_reseau):
      for y in range(0, hauteur_reseau):
        if reseau[x][y] > 0:
          pygame.gfxdraw.box(ecran, (cote_cellule*x + marge, cote_cellule*y + marge, cote_cellule - marge, cote_cellule - marge), couleurs[reseau[x][y]-1])

    if pause:
      infos = police.render("Paused", True, rouge)
      pygame.gfxdraw.box(ecran, (largeur - infos.get_width(), hauteur - infos.get_height(), infos.get_width(), infos.get_height()), noir)
      ecran.blit(infos, (largeur - infos.get_width(), hauteur - infos.get_height()))

    pygame.display.flip()

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
