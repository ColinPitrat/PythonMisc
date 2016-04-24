#!/usr/bin/python2
import pygame, random, math
import pygame.gfxdraw
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 1300, 640

noir = 0, 0, 0
rouge = 255, 0, 0
bleu = 0, 0, 255
blanc = 255, 255, 255

lignes_par_boucle = 5
cote_cellule = 5
marge = 1

largeur_reseau, hauteur_reseau = largeur/cote_cellule, hauteur/cote_cellule

reseau = []
pattern = []
pattern_gauche = [ 1 ]
pattern_milieu = []
pattern_droite = []
for i in range(0, largeur_reseau/2):
    pattern_gauche.append(0)
    pattern_milieu.append(0)
    pattern_droite.append(0)
pattern_milieu.append(1)
for i in range(0, largeur_reseau/2 - 1):
    pattern_gauche.append(0)
    pattern_milieu.append(0)
    pattern_droite.append(0)
pattern_droite.append(1)
#pattern_regulier = [ 1, 0 ]
pattern_regulier = [ 1, 1, 0, 0 ]
#pattern_regulier = [ 1, 1, 1, 0, 1, 0, 1, 1 ]
#pattern_regulier = [ 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1 ]
#pattern_regulier = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
#pattern_regulier = [ 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1 ]

#############
# Variables #
#############

quitter = False
ligne_courante = 0
#num_automate = 110
#num_automate = 156
num_automate = 184
something_changed = False
random_conf = True
show_info = True

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
police = pygame.font.SysFont("arial", 20);
pygame.display.set_caption("Automate cellulaire - dimension 1")

def init():
  global reseau, largeur_reseau, hauteur_reseau
  # Cree la table de l'automate
  for x in range(0, largeur_reseau):
    reseau.append([])
    for y in range(0, hauteur_reseau):
      reseau[x].append(0)


def reinit(num_automate, random_configuration = True, clear = True):
  global ligne_courante, transition, reseau, largeur_reseau, hauteur_reseau, ecran, noir, random_conf
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
  i = 0
  for x in range(0, largeur_reseau):
    if random_conf:
      reseau[x][0] = (random.randint(0, 1))
    else:
      reseau[x][0] = pattern[i%len(pattern)]
      i = i + 1

def print_values():
    global reseau
    plus_petit_chiffre = 0
    for y in range(0, hauteur_reseau):
        valeur = 0
        for x in range(0, largeur_reseau):
            valeur = 2*valeur+reseau[x][y]
            if reseau[x][y] != 0 and x > plus_petit_chiffre:
              plus_petit_chiffre = x
        valeur = valeur / 2**(largeur_reseau - plus_petit_chiffre - 1)
        print("%s: %s" % (y, valeur))


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
            if pygame.mouse.get_pressed()[0]:
              reseau[event.pos[0]/cote_cellule][0] = 1
              ligne_courante = 0
            if pygame.mouse.get_pressed()[2]:
              reseau[event.pos[0]/cote_cellule][0] = 0
              ligne_courante = 0
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
                pattern = pattern_regulier
                random_conf = False
                reinit(num_automate, clear = False)
            elif event.key == pygame.K_i:
                show_info = not show_info
            elif event.key == pygame.K_a:
                random_conf = False
                pattern = pattern_gauche
                reinit(num_automate, clear = False)
            elif event.key == pygame.K_z:
                random_conf = False
                pattern = pattern_milieu
                reinit(num_automate, clear = False)
            elif event.key == pygame.K_e:
                random_conf = False
                pattern = pattern_droite
                reinit(num_automate, clear = False)
            elif event.key == pygame.K_d:
                print_values()
            elif event.key == pygame.K_SPACE:
                reinit(num_automate, clear = False);

    # Calcul de la ligne suivante
    something_changed = False
    for i in range(0, lignes_par_boucle):
      if ligne_courante < hauteur_reseau-1:
        something_changed = True
        ligne_courante = ligne_courante + 1
        for x in range(0, largeur_reseau):
          if x > 0:
            a0 = reseau[x-1][ligne_courante-1]
          else:
            a0 = reseau[largeur_reseau-1][ligne_courante-1]
          a1 = reseau[x][ligne_courante-1]
          if x < largeur_reseau-1:
            a2 = reseau[x+1][ligne_courante-1]
          else:
            a2 = reseau[0][ligne_courante-1]
          reseau[x][ligne_courante] = transition[a0][a1][a2]

    if something_changed:
      ecran.fill(noir)
      # Affiche le resultat
      y = 0
      for x in range(0, largeur_reseau):
        for y in range(0, hauteur_reseau):
          if reseau[x][y] == 1:
            pygame.gfxdraw.box(ecran, (cote_cellule*x + marge, cote_cellule*y + marge, cote_cellule - marge, cote_cellule - marge), blanc)
      if show_info:
        automate_desc = "%s %s %s %s %s %s %s %s" % (transition[1][1][1], transition[1][1][0], transition[1][0][1], transition[1][0][0], transition[0][1][1], transition[0][1][0], transition[0][0][1], transition[0][0][0])
        infos = police.render("# %s - %s" % (num_automate, automate_desc), True, rouge)
        pygame.gfxdraw.box(ecran, (largeur - infos.get_width(), hauteur - infos.get_height(), infos.get_width(), infos.get_height()), noir)
        ecran.blit(infos, (largeur - infos.get_width(), hauteur - infos.get_height()))

    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
