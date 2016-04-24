#!/usr/bin/python2
import pygame, random, math
import pygame.gfxdraw
pygame.init()

# TODO: Permettre de mettre un etat a une autre valuer que 0 ou 1 avec la souris

##############
# Constantes #
##############
resolution = largeur, hauteur = 1300, 640

noir = 0, 0, 0
rouge = 255, 0, 0
vert = 0, 255, 0
bleu = 0, 0, 255
cyan = 0, 255, 255
magenta = 255, 0, 255
jaune = 255, 255, 0
blanc = 255, 255, 255

couleurs = [ blanc, rouge, vert, bleu, cyan, magenta, jaune ]

lignes_par_boucle = 5
cote_cellule = 5
marge = 1
nb_etats = 5
max_numero = nb_etats**nb_etats**3

largeur_reseau, hauteur_reseau = largeur/cote_cellule, hauteur/cote_cellule

reseau = []
pattern = []
pattern_gauche = [ 1 ]
pattern_milieu = []
pattern_droite = []
pattern_special = []
for i in range(0, largeur_reseau/2):
    pattern_gauche.append(0)
    pattern_milieu.append(0)
    pattern_droite.append(0)
    pattern_special.append(random.randint(1,4))
    pattern_special.append(0)
pattern_milieu.append(1)
for i in range(0, largeur_reseau/2 - 1):
    pattern_gauche.append(0)
    pattern_milieu.append(0)
    pattern_droite.append(0)
pattern_droite.append(1)
pattern_droite = pattern_special
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

# Automates a 2 etats interessants
num_automate = 184
#num_automate = 156

# Automates a 4 etats interessants
num_automate = 0

# Automates a 4 etats interessants
#num_automate = 321400215322013816336846560530223119640
#num_automate = 3*4**48 + 2*4**32 + 4**16 + 3*4**3 + 2*4**2 + 4
num_automate = 587728878999653368369611360649171452298184335468742411882478788175620213147132863771875

something_changed = False
random_conf = True
show_info = True
affichage_normal = True
affiche_etat = 1

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
if nb_etats < 4:
  police = pygame.font.SysFont("arial", 20);
elif nb_etats == 4:
  police = pygame.font.SysFont("arial", 15);
elif nb_etats < 7:
  police = pygame.font.SysFont("arial", 12);
else:
  police = pygame.font.SysFont("arial", 8);

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
  valeur_restante = 0
  for a0 in range(0, nb_etats):
    transition.append([])
    for a1 in range(0, nb_etats):
      transition[a0].append([])
      for a2 in range(0, nb_etats):
        transition[a0][a1].append([])
        digit_value = nb_etats**(a0*(nb_etats**2) + a1*(nb_etats**1) + a2)
        transition[a0][a1][a2] = ((num_automate - valeur_restante) % (nb_etats*digit_value)) / digit_value
        valeur_restante = valeur_restante + (digit_value * transition[a0][a1][a2])

  # Cree la premiere ligne
  i = 0
  for x in range(0, largeur_reseau):
    if random_conf:
      reseau[x][0] = (random.randint(0, nb_etats - 1))
    else:
      reseau[x][0] = pattern[i%len(pattern)]
      i = i + 1

def print_values():
    global reseau
    plus_petit_chiffre = 0
    for y in range(0, hauteur_reseau):
        valeur = 0
        for x in range(0, largeur_reseau):
            valeur = nb_etats*valeur+reseau[x][y]
            if reseau[x][y] != 0 and x > plus_petit_chiffre:
              plus_petit_chiffre = x
        valeur = valeur / nb_etats**(largeur_reseau - plus_petit_chiffre - 1)
        print("%s: %s" % (y, valeur))


#####################
# Boucle principale #
#####################
init()
reinit(num_automate)
while quitter != True:
    something_changed = False

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
                if num_automate < max_numero:
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
            elif event.key == pygame.K_w:
                nb_etats = nb_etats - 1
                reinit(num_automate)
            elif event.key == pygame.K_x:
                nb_etats = nb_etats + 1
                reinit(num_automate)
            elif event.key == pygame.K_c:
                num_automate = random.randint(0, max_numero)
                reinit(num_automate)
            elif event.key == pygame.K_q:
                affichage_normal = True
                something_changed = True
            elif event.key == pygame.K_s:
                affichage_normal = False
                something_changed = True
            elif event.key == pygame.K_f:
                if affiche_etat > 1:
                  affiche_etat = affiche_etat - 1
                  something_changed = True
            elif event.key == pygame.K_g:
                if affiche_etat < nb_etats - 1:
                  affiche_etat = affiche_etat + 1
                  something_changed = True
            elif event.key == pygame.K_SPACE:
                reinit(num_automate, clear = False);

    # Calcul de la ligne suivante
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
          if affichage_normal:
            if reseau[x][y] != 0:
              pygame.gfxdraw.box(ecran, (cote_cellule*x + marge, cote_cellule*y + marge, cote_cellule - marge, cote_cellule - marge), couleurs[reseau[x][y]%len(couleurs)])
          else:
            if reseau[x][y] == affiche_etat:
              pygame.gfxdraw.box(ecran, (cote_cellule*x + marge, cote_cellule*y + marge, cote_cellule - marge, cote_cellule - marge), blanc)
      if show_info:
        automate_desc = ""
        for a0 in range(nb_etats, 0, -1):
          for a1 in range(nb_etats, 0, -1):
            for a2 in range(nb_etats, 0, -1):
              automate_desc = "%s %s" % (automate_desc, transition[a0-1][a1-1][a2-1]) 
        filtre = "normal"
        if not affichage_normal:
          filtre = "%s" % affiche_etat
        if nb_etats > 5:
          infos = police.render("# %s - %se (%s)" % (num_automate, nb_etats, filtre), True, rouge)
        else:
          infos = police.render("# %s - %s - %se (%s)" % (num_automate, automate_desc, nb_etats, filtre), True, rouge)
        pygame.gfxdraw.box(ecran, (largeur - infos.get_width(), hauteur - infos.get_height(), infos.get_width(), infos.get_height()), noir)
        ecran.blit(infos, (largeur - infos.get_width(), hauteur - infos.get_height()))

    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
