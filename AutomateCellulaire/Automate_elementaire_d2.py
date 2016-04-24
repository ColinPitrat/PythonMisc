#!/usr/bin/python2
import pygame, random, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 800, 600

noir = 0
blanc = 16777215

lignes_par_boucle = 1

#############
# Variables #
#############

quitter = False
ligne_courante = 0
num_automate = 50
random_conf = True
show_info = True

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("Automate cellulaire - dimension 1")

def init():
  global ecran
  ecran.fill(noir)

def reinit(num_automate, random_configuration = True, clear = True):
  global ligne_courante, transition, largeur, hauteur, ecran, noir, random_conf
  if clear:
    ecran.fill(noir)
    pygame.display.flip()
  ligne_courante = 0
  # Cree la table de transition a partir du numero de l'automate
  transition = []
  for a0 in range(0, 2):
    transition.append([])
    for a1 in range(0, 2):
      transition[a0].append([])
      for a2 in range(0, 2):
        transition[a0][a1].append([])
        bit_value = 2**(a0*4 + a1*2 + a2)
        transition[a0][a1][a2] = (num_automate & bit_value) / bit_value

  # Cree la premiere ligne
  ecran.lock()
  reseau = pygame.surfarray.pixels2d(ecran)
  for x in range(0, largeur):
    if random_conf:
      reseau[x][0] = blanc * random.randint(0, 1)
    else:
      reseau[x][0] = 0
  if not random_conf:
    reseau[0][0] = blanc
  ecran.unlock()

#####################
# Boucle principale #
#####################
init()
reinit(num_automate)
while quitter != True:
    print("A")
    # Boucle d'evenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            elif event.key == pygame.K_p:
                if num_automate < 255:
                  num_automate = num_automate + 1
                reinit(num_automate);
            elif event.key == pygame.K_m:
                if num_automate > 0:
                  num_automate = num_automate - 1
                reinit(num_automate)
            elif event.key == pygame.K_r:
                random_conf = True
                reinit(num_automate, clear = False)
            elif event.key == pygame.K_n:
                random_conf = False
                reinit(num_automate, clear = False)
            elif event.key == pygame.K_i:
                show_info = not show_info
            elif event.key == pygame.K_SPACE:
                reinit(num_automate, clear = False);

    print("B1")
    ecran.lock()
    reseau = pygame.surfarray.pixels2d(ecran)
    reseau /= blanc
    print("B2")
    # Calcul de la ligne suivante
    for i in range(0, lignes_par_boucle):
      if ligne_courante < hauteur-1:
        ligne_courante = ligne_courante + 1
        for x in range(0, largeur):
          if x > 0:
            a0 = reseau[x-1][ligne_courante-1]
          else:
            a0 = reseau[largeur-1][ligne_courante-1]
          a1 = reseau[x-1][ligne_courante-1]
          if x < largeur-1:
            a2 = reseau[x+1][ligne_courante-1]
          else:
            a2 = reseau[0][ligne_courante-1]
          reseau[x][ligne_courante] = transition[a0][a1][a2]
      else:
          break
    reseau *= blanc
    print("B3")
    ecran.unlock()

    print("C")
    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
