#!/usr/bin/python2
import pygame, random, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 800, 600

noir = 0, 0, 0
rouge = 255, 0, 0
vert = 0, 255, 0
bleu = 0, 0, 255
cyan = 0, 255, 255
magenta = 255, 0, 255
jaune = 255, 255, 0
blanc = 255, 255, 255
b1 = 0, 0, 64
b2 = 0, 0, 128
b3 = 0, 0, 192
b4 = 0, 0, 255
v1 = 0, 64, 0
v2 = 0, 128, 0
v3 = 0, 192, 0
v4 = 0, 255, 0

couleurs = [ b1, b2, b3, b4, v1, v2, v3, v4, b1, b2, b3, b4, v1, v2, v3, v4, b1, b2, b3, b4, v1, v2, v3, v4, b1, b2, b3, b4, v1, v2, v3, v4, b1, b2, b3, b4, v1, v2, v3, v4, b1, b2, b3, b4, v1, v2, v3, v4, b1, b2, b3, b4, v1, v2, v3, v4, b1, b2, b3, b4, v1, v2, v3, v4, rouge ]
#couleurs = [ b1, b2, b3, rouge ]
couleurs = [ b1, b2, b3, b4, v1, v2, v3, v4, rouge ]

nombre_pas = 100000
nb_marcheurs = 64
nb_marcheurs = 3
nb_marcheurs = 8
taille_pas = 5
marge = 10

#############
# Variables #
#############
iteration = 0
couleur = couleurs[iteration]
pas = 0
pas_par_boucle = 1
quitter = False
afficher_courbe = False
police = pygame.font.SysFont("arial", 30);
legende_x = police.render("pas", True, blanc)
legende_y = police.render("d", True, blanc)
infos = police.render("%s / %s" % (pas, nombre_pas), True, blanc)
courbe = None
plan = None
first_pos = None
cur_pos = []
new_pos = []
for i in range(0, nb_marcheurs):
    cur_pos.append((0,0))
    new_pos.append((0,0))

origin_x = marge + legende_y.get_width()
origin_y = hauteur - legende_x.get_height() - marge
echelle_x = 1.0 * (largeur - legende_x.get_width() - marge) / nombre_pas
echelle_y = 1.0 / taille_pas

def init_surfaces():
  global courbe, plan, origin_x, origin_y, largeur, hauteur, marge, blanc, legende_x, legende_y, resolution
  courbe = pygame.Surface(resolution)
  plan = pygame.Surface(resolution)
  pygame.draw.line(courbe, blanc, (origin_x, origin_y), (largeur - marge, origin_y))
  courbe.blit(legende_x, ((largeur - legende_x.get_width())/2, hauteur - legende_x.get_height()))
  pygame.draw.line(courbe, blanc, (origin_x, origin_y), (origin_x, marge + infos.get_height()))
  courbe.blit(legende_y, (0, (hauteur - legende_y.get_height()) / 2))
  for i in range(1,8):
    pygame.draw.line(courbe, blanc, (origin_x, origin_y - 100*i), (origin_x + 5, origin_y - 100*i))

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("La marche de l'ivrogne")
init_surfaces()

#####################
# Boucle principale #
#####################
d_moy = []
while quitter != True:
    # Boucle d'evenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            if event.key == pygame.K_c:
                afficher_courbe = True
            if event.key == pygame.K_p:
                afficher_courbe = False
            if event.key == pygame.K_r:
                iteration = -1
                init_surfaces()
            if event.key == pygame.K_n or event.key == pygame.K_r:
                pas = 0
                iteration = iteration + 1
                couleur = couleurs[iteration % len(couleurs)]
            if event.key == pygame.K_f:
                if pas_par_boucle < 65536:
                  pas_par_boucle = pas_par_boucle * 2
                print("Pas par boucle: " , pas_par_boucle);
            if event.key == pygame.K_s:
                if pas_par_boucle > 1:
                  pas_par_boucle = pas_par_boucle / 2
                print("Pas par boucle: " , pas_par_boucle);

    # Fait avancer les ivrognes, la moyenne et la courbe theorique 
    for i in range(0, pas_par_boucle):
      if pas == 0:
        first_pos=(largeur/2, hauteur/2)
        for m in range(0, nb_marcheurs):
          cur_pos[m] = first_pos
        pas = pas + 1
      elif pas < nombre_pas:
        for m in range(0, nb_marcheurs):
          dx = dy = 0
          while dx == 0 and dy == 0:
            if random.randint(0,1) == 1:
              dx = taille_pas * random.randint(-1, 1)
            else:
              dy = taille_pas * random.randint(-1, 1)
          new_pos[m] = (cur_pos[m][0] + dx, cur_pos[m][1] + dy)
          pygame.draw.line(plan, couleurs[m % len(couleurs)], cur_pos[m], new_pos[m])
          prev_distance = math.sqrt((cur_pos[m][0] - first_pos[0]) ** 2 + (cur_pos[m][1] - first_pos[1]) ** 2)
          distance = math.sqrt((new_pos[m][0] - first_pos[0]) ** 2 + (new_pos[m][1] - first_pos[1]) ** 2)
          pygame.draw.line(courbe, couleurs[m % len(couleurs)], (origin_x + echelle_x*(pas - 1), origin_y - echelle_y * prev_distance), (origin_x + echelle_x*pas, origin_y - echelle_y * distance))
          if m == 0:
            if pas == 1:
              d_moy.append(prev_distance)
            d_moy.append(distance)
          else:
            if pas == 1:
              d_moy[-2] += prev_distance
            d_moy[-1] += distance
          if m == nb_marcheurs - 1:
            if pas == 0:
              d_moy[-2] = d_moy[-2] / nb_marcheurs
            d_moy[-1] = d_moy[-1] / nb_marcheurs
            pygame.draw.line(courbe, couleurs[nb_marcheurs % len(couleurs)], (origin_x + echelle_x*(pas - 1), origin_y - echelle_y * d_moy[-2]), (origin_x + echelle_x*pas, origin_y - echelle_y * d_moy[-1]), 2)
          cur_pos[m] = new_pos[m]
        pygame.draw.line(courbe, blanc, (origin_x + echelle_x*(pas - 1), origin_y - math.sqrt(pas - 1)), (origin_x + echelle_x*pas, origin_y - math.sqrt(pas)), 2)
        pas = pas + 1
      else:
        break
    infos = police.render("%s / %s" % (pas, nombre_pas), True, blanc)

    # Affiche le resultat
    ecran.fill(noir)

    if afficher_courbe:
      ecran.blit(courbe, (0, 0))
    else:
      ecran.blit(plan, (0, 0))

    ecran.blit(infos, (0, 0))
    pygame.display.flip()

###############
# Terminaison #
###############
pygame.quit()
