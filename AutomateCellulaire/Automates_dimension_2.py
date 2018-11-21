#!/usr/bin/python2

# Automates cellulaires a en dimension 2
# Problemes:
#  - beaucoup trop lent a initialiser pour nb_etats > 2
#  - les nombres representants les automates sont enormes meme pour 2 etats (jusqu'a 300 chiffres)
#  - la plupart des automates sont ininteressants
#  - il faut ecrire des methodes pour generer les nombres pour les configurations connues

import pygame, random, math
import pygame.gfxdraw
pygame.init()

# Profiling
import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()
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
nb_etats = 3
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
num_automate = random.randint(0, max_num_automate)
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


def compute_transition(nb):
    digit_value = nb_etats**nb
    transition[nb] = (num_automate / digit_value) % nb_etats


# Le numero de l'automate est de la forme: a b c d e f g h i
# Pour le voisinage suivant du point e:
# i h g
# f e d
# c b a
def reinit(num_automate):
  global transition, reseau, largeur_reseau, hauteur_reseau, ecran, noir, random_conf
  precompute_transitions = False
  ecran.fill(noir)
  pygame.display.flip()
  # Cree la table de transition a partir du numero de l'automate
  transition = [None] * max_voisinages
  if precompute_transitions:
    digit_value = 1
    for nb in range(0, max_voisinages):
      if (nb % 1000) == 0:
          print("nb = %s" % nb)
      digit_value *= nb_etats
      transition[nb] = (num_automate / digit_value) % nb_etats
      #if ((num_automate / digit_value) % nb_etats):
      #    print("Alive for %s" % bin(nb))

  # Cree la configuration initiale
  for x in range(0, largeur_reseau):
    for y in range(0, hauteur_reseau):
      if random_conf:
        reseau[x][y] = (random.randint(0, 1))
      else:
        reseau[x][y] = 0


def describe_automate(num_automate):
  print("Automate %s" % (num_automate))


#############################################
# Calcul les nombres d'automates classiques #
#############################################

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
def num_game_of_life():
  num = 0
  for nb in range(0, max_voisinages):
    #alives = bin(nb).count('1')
    alives = nb_states_in_voisinage(1, nb)
    if is_self_in_state(1, nb): # La cellul est vivante
        if alives == 3 or alives == 4: # 2 ou 3 cellules vivantes en plus d'elle
            print("Alive and stay alive for %s" % bin(nb))
            num += nb_etats**nb
    else: # La cellule est morte
        if alives == 3: # 3 cellules vivantes autour d'elle
            print("Dead and become alive for %s" % bin(nb))
            num += nb_etats**nb
  print("Game of life is: %s" % num)
  return num


# Necessite 2 etats au moins
def num_seeds():
  num = 0
  for nb in range(0, max_voisinages):
    #alives = bin(nb).count('1')
    alives = nb_states_in_voisinage(1, nb)
    if is_self_in_state(1, nb): # La cellule est vivante
        if alives == 3: # 2 cellules vivantes en plus d'elle
            print("Alive and stay alive for %s" % bin(nb))
            num += nb_etats**nb
    else: # La cellule est morte
        if alives == 2: # 2 cellules vivantes autour d'elle
            print("Dead and become alive for %s" % bin(nb))
            num += nb_etats**nb
  print("Seeds is: %s" % num)
  return num

# Necessite 3 etats au moins - 0 est morte, 1 est vivant, 2 est mourrant
def num_brian_brain():
  num = 0
  for nb in range(0, max_voisinages):
    alives = nb_states_in_voisinage(1, nb)
    if is_self_in_state(0, nb): # La cellule est morte, ell ne nait que si elle a 2 voisines
        if alives == 2: # 2 cellules vivantes
            num += nb_etats**nb
    # Si la cellule est mourrante, elle sera morte ensuite donc on n'ajoute rien a num
    elif is_self_in_state(1, nb): # La cellule est vivante, elle sera mourrante
        num += 2*(nb_etats**nb)
  print("Brian is: %s" % num)
  return num


#num_automate = num_game_of_life()
#num_automate = num_seeds()
#num_automate = num_brian_brain()
#####################
# Boucle principale #
#####################
init()
reinit(num_automate)
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
                num_automate = (num_automate + 1) % max_num_automate
                describe_automate(num_automate)
                reinit(num_automate);
            elif event.key == pygame.K_m:
                num_automate = (num_automate - 1) % max_num_automate
                describe_automate(num_automate)
                reinit(num_automate)
            elif event.key == pygame.K_n:
                num_automate = random.randint(0, max_num_automate)
                describe_automate(num_automate)
                reinit(num_automate)
            elif event.key == pygame.K_r:
                random_conf = not random_conf
                reinit(num_automate)
            elif event.key == pygame.K_c:
                reinit(num_automate);
            elif event.key == pygame.K_i:
                show_info = not show_info
            elif event.key == pygame.K_SPACE:
                pause = not pause

    # Calcul de la generation suivante
    if not pause:
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