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

couleurs = [ blanc, rouge, vert, bleu, cyan, magenta, jaune ]

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


# Le numero de l'automate est de la forme: a b c d e f g h i
# Pour le voisinage suivant du point e:
# i h g
# f e d
# c b a
def reinit(num_automate):
  global transition, reseau, largeur_reseau, hauteur_reseau, ecran, noir, random_conf
  ecran.fill(noir)
  pygame.display.flip()
  # Cree la table de transition a partir du numero de l'automate
  transition = [None] * max_voisinages
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
  print("Automate %s %s" % (num_automate, bin(num_automate)))


def num_game_of_life():
  num = 0
  for nb in range(0, max_voisinages):
    alives = bin(nb).count('1')
    if (nb & 0b10000) != 0: # La cellule est vivante
        if alives == 3 or alives == 4: # 2 ou 3 cellules vivantes en plus d'elle
            print("Alive and stay alive for %s" % bin(nb))
            num += nb_etats**nb
    else: # La cellule est morte
        if alives == 3: # 3 cellules vivantes autour d'elle
            print("Dead and become alive for %s" % bin(nb))
            num += nb_etats**nb
  print("Game of life is: %s" % num)
  return num


def num_seeds():
  num = 0
  for nb in range(0, max_voisinages):
    alives = bin(nb).count('1')
    if (nb & 0b10000) != 0: # La cellule est vivante
        if alives == 3: # 2 cellules vivantes en plus d'elle
            print("Alive and stay alive for %s" % bin(nb))
            num += nb_etats**nb
    else: # La cellule est morte
        if alives == 2: # 2 cellules vivantes autour d'elle
            print("Dead and become alive for %s" % bin(nb))
            num += nb_etats**nb
  print("Seeds is: %s" % num)
  return num


#num_automate = num_game_of_life()
num_automate = num_seeds()
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
          tmp_reseau[x][y] = transition[nb]
      reseau, tmp_reseau = tmp_reseau, reseau

    ecran.fill(noir)
    # Affiche le resultat
    y = 0
    for x in range(0, largeur_reseau):
      for y in range(0, hauteur_reseau):
        if reseau[x][y] == 1:
          pygame.gfxdraw.box(ecran, (cote_cellule*x + marge, cote_cellule*y + marge, cote_cellule - marge, cote_cellule - marge), blanc)

    if pause:
      infos = police.render("Paused", True, rouge)
      pygame.gfxdraw.box(ecran, (largeur - infos.get_width(), hauteur - infos.get_height(), infos.get_width(), infos.get_height()), noir)
      ecran.blit(infos, (largeur - infos.get_width(), hauteur - infos.get_height()))

    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
