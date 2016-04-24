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

couleurs = [ rouge, vert, bleu, cyan, magenta, jaune ]

nombre_pas = 1000000
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
cur_pos = None
next_pos = None

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

# Profiling
import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()
#####################
# Boucle principale #
#####################
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

    # Fait avancer l'ivrogne
    for i in range(0, pas_par_boucle):
      if pas == 0:
        first_pos=(largeur/2, hauteur/2)
        cur_pos = first_pos
        pas = pas + 1
      elif pas < nombre_pas:
        dx = dy = 0
        while dx == 0 and dy == 0:
            if random.randint(0,1) == 1:
              dx = taille_pas * random.randint(-1, 1)
            else:
              dy = taille_pas * random.randint(-1, 1)
        new_pos = (cur_pos[0] + dx, cur_pos[1] + dy)
        pygame.draw.line(plan, couleur, cur_pos, new_pos)
        prev_distance = math.sqrt((cur_pos[0] - first_pos[0]) ** 2 + (cur_pos[1] - first_pos[1]) ** 2)
        distance = math.sqrt((new_pos[0] - first_pos[0]) ** 2 + (new_pos[1] - first_pos[1]) ** 2)
        pygame.draw.line(courbe, couleur, (origin_x + echelle_x*(pas - 1), origin_y - echelle_y * prev_distance), (origin_x + echelle_x*pas, origin_y - echelle_y * distance))
        pas = pas + 1
        cur_pos = new_pos
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

# Profiling
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
