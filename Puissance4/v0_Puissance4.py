#!/usr/bin/python2
import pygame, random, math, time
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 700, 700
resolution = largeur, hauteur = 700, 700

noir = 0, 0, 0
rouge = 255, 0, 0
jaune = 255, 255, 0
bleu = 0, 0, 255
blanc = 255, 255, 255

nb_colonnes = 7
nb_lignes = 6
max_colonnes = nb_colonnes - 1
max_lignes = nb_lignes - 1

profondeur_recherche = 2

rayon = min((largeur / (2*nb_colonnes)), (hauteur / (2*(nb_lignes+1))))
v_remainder = max(hauteur - 2*rayon * (nb_lignes+1), 0)
v_remainder += 2*rayon
h_remainder = max(largeur - 2*rayon * nb_colonnes, 0)
margin = rayon / 10
rayon -= margin

errorSound = pygame.mixer.Sound("Error.ogg")
police = pygame.font.SysFont("arial", 50);

#############
# Variables #
#############
position = 0
plateau = []
alignements = []
for i in range(0, nb_colonnes):
    plateau.append([])
    alignements.append([])
    for j in range(0, nb_lignes):
        plateau[i].append(0)
        alignements[i].append([0, 0, 0, 0])
player = 1

computer = [False, True, True]
fini = False

#############
# Fonctions #
#############

def reset():
    global fini, plateau
    for i in range(0, nb_colonnes):
        for j in range(0, nb_lignes):
            plateau[i][j] = 0
            alignements[i][j] = [0, 0, 0, 0]
    fini = False

def gagnant3():
    score = 0
    couleur = 1
    for i in range(0, nb_colonnes):
        for j in range(0, nb_lignes):
            if plateau[i][j] != 0:
                if plateau[i][j] == couleur:
                    score += j*i
                else:
                    score -= j*i
    if score >= 0:
        return (couleur, score)
    else:
        return (2, -score)

def gagnant2():
    global nb_colonnes, nb_lignes, plateau, fini
    count3 = [ 0, 0, 0 ]
    count2 = [ 0, 0, 0 ]
    # Verticales
    for i in range(0, nb_colonnes):
        count = 0
        couleur = 0
        for j in range(max_lignes, -1, -1):
            if plateau[i][j] == couleur:
                count += 1
            else:
                # 3 pions alignes verticalement n'est utile que si il y a une place pour un quatrieme
                if plateau[i][j] == 0 and plateau[i][j-1] == 0 and count == 2:
                    count2[couleur] += 1
                if plateau[i][j] == 0 and count == 3:
                    count3[couleur] += 1
                couleur = plateau[i][j]
                count = 1
            if count == 4 and couleur != 0:
                fini = True
                return (couleur, 10000)
            # Une colonne s'arrete des qu'on trouve une case vide
            if couleur == 0:
                break
    # Horizontales
    for j in range(0, nb_lignes):
        count = 0
        potentiel = [ 0, 0, 0]
        couleur = -1
        for i in range(0, nb_colonnes):
            if plateau[i][j] == couleur:
                if couleur == 0:
                    for c in range(1,3):
                        potentiel[c] += 1
                else:
                    count += 1
                    couleur = plateau[i][j]
            else:
                nv_coul = plateau[i][j]
                if nv_coul != 0:
                    if couleur != 0:
                        if count == 3 and potentiel[couleur] >= 1:
                            count3[couleur] += 1
                        if count == 2 and potentiel[couleur] >= 2:
                            count2[couleur] += 1
                        for c in range(0,2):
                            potentiel[c] = 0
                    else:
                        potentiel[(nv_coul+1)%2] = 0
                else:
                    potentiel[(couleur+1)%2] = 1
                couleur = nv_coul
            if count == 4 and couleur != 0:
                fini = True
                return (couleur, 10000)
    #           X X X Z X X X   Y
    #           X X Z X X X X Y
    #           X Z X X X X Z
    #           Z X X X X Z X
    #         Y X X X X Z X X
    #       Y   X X X Z X X X
    #       - - - - - - - - - - -    <--- Largeur totale a considerer: nb_colonnes + 2*(nb_lignes - 4)
    # Diagonales montantes
    for k in range(-(nb_lignes-4), nb_colonnes+nb_lignes-4):
        count = 0
        couleur = 0
        for j in range(0, nb_lignes):
            i = k + j
            if i < 0:
                continue
            if i >= nb_colonnes:
                break
            if plateau[i][j] == couleur:
                count += 1
            else:
                if count == 3:
                    count3[couleur] += 1
                couleur = plateau[i][j]
                count = 1
            if count == 4 and couleur != 0:
                fini = True
                return (couleur, 0)
    # Diagonales descendantes
    for k in range(-(nb_lignes-4), nb_colonnes+nb_lignes-4):
        count = 0
        couleur = 0
        for j in range(0, nb_lignes):
            i = max_lignes + k - j
            if i < 0:
                continue
            if i >= nb_colonnes:
                break
            if plateau[i][j] == couleur:
                count += 1
            else:
                if count == 3:
                    count3[couleur] += 1
                couleur = plateau[i][j]
                count = 1
            if count == 4 and couleur != 0:
                fini = True
                return (couleur, 0)
    if count3[1] > count3[2]:
        return (1, 100*(count3[1]-count3[2])+10*(count2[1]-count2[2])+1)
    elif count3[2] > count3[1]:
        return (1, 100*(count3[2]-count3[1])+10*(count2[2]-count2[1])+1)
    return (0, 0)

def gagnant():
    global nb_colonnes, nb_lignes, plateau, fini
    for i in range(0, nb_colonnes):
        for j in range(0, nb_lignes):
            couleur = plateau[i][j]
            if couleur == 0:
                continue
#            gagnant = [ True, True, True, True, True, True, True, True ]
            gagnant = [ True, True, True, True, False, False, False, False ]
            for k in range(0, 4):
                if i+k >= nb_colonnes:
#                    gagnant[7] = False
                    gagnant[0] = False
                    gagnant[1] = False
                if j+k >= nb_lignes:
                    gagnant[1] = False
                    gagnant[2] = False
                    gagnant[3] = False
                if i-k < 0:
                    gagnant[3] = False
#                    gagnant[4] = False
#                    gagnant[5] = False
#                if j-k < 0:
#                    gagnant[5] = False
#                    gagnant[6] = False
#                    gagnant[7] = False
                if gagnant[0] == True:
                    if plateau[i+k][j] != couleur:
                        gagnant[0] = False
                if gagnant[1] == True:
                    if plateau[i+k][j+k] != couleur:
                        gagnant[1] = False
                if gagnant[2] == True:
                    if plateau[i][j+k] != couleur:
                        gagnant[2] = False
                if gagnant[3] == True:
                    if plateau[i-k][j+k] != couleur:
                        gagnant[3] = False
#                if gagnant[4] == True:
#                    if plateau[i-k][j] != couleur:
#                        gagnant[4] = False
#                if gagnant[5] == True:
#                    if plateau[i-k][j-k] != couleur:
#                        gagnant[5] = False
#                if gagnant[6] == True:
#                    if plateau[i][j-k] != couleur:
#                        gagnant[6] = False
#                if gagnant[7] == True:
#                    if plateau[i+k][j-k] != couleur:
#                        gagnant[7] = False
#            for k in range(0, 8):
            for k in range(0, 4):
                if gagnant[k]:
                    fini = True
                    return couleur
    return 0

def removePion(col):
    global player
    removed = False
    for i in range(0, nb_lignes):
        if plateau[col][i] != 0:
            plateau[col][i] = 0
            removed = True
            break
    return removed

def placePion(col, ply):
    global player
    placed = False
    if col < 0 or col >= nb_colonnes:
        return False
    for lig in range(max_lignes, -1, -1):
        if plateau[col][lig] == 0:
            plateau[col][lig] = ply
            """
            # Alignement horizontal
            if lig > 0 and alignement[col][lig-1] == ply:
                alignement[col][lig][0] += alignement[col][lig-1][0]
            if lig < max_lignes and alignement[col][lig+1] == ply:
                alignement[col][lig][0] += alignement[col][lig+1][0]
            # Alignement diagonal 'montant'
            if col > 0 and lig > 0 and alignement[col-1][lig-1] == ply:
                alignement[col][lig][1] += alignement[col-1][lig-1][1]
            if col < max_colonnes and lig < max_lignes and alignement[col+1][lig+1] == ply:
                alignement[col][lig][1] += alignement[col+1][lig+1][1]
            # Alignement vertical
            if col > 0 and alignement[col-1][lig] == ply:
                alignement[col][lig][2] += alignement[col-1][lig][2]
            if col < max_colonnes and alignement[col+1][lig] == ply:
                alignement[col][lig][2] += alignement[col+1][lig][2]
            # Alignement diagonal 'descendant'
            if col > 0 and lig < max_lignes and alignement[col-1][lig+1] == ply:
                alignement[col][lig][3] += alignement[col-1][lig+1][3]
            if col < max_colonnes and lig > 0 and alignement[col+1][lig-1] == ply:
                alignement[col][lig][3] += alignement[col+1][lig-1][3]
            """
            placed = True
            break
    return placed

def placePionAndMore(col):
    global player, fini
    placed = False
    if placePion(col, player):
        player = (player % 2) + 1
        placed = True
    fini = True
    for i in range(0, nb_colonnes):
        if plateau[i][0] == 0:
            fini = False
    return placed

def trouveMeilleurePosition(joueur, joueurCourant, depth):
    print("   "*depth, "tMP (%s, %s, %s)" % (joueur, joueurCourant, depth))
    pos = -1
    score = 0
    bestMove = [ 0, -10000 ]
    worstMove = [ 0, 10000 ]
    if depth <= profondeur_recherche:
        for c in range(0, nb_colonnes):
            placed = placePion(c, joueur)
            if placed:
#            g = gagnant()
#            if g == joueur:
#                removePion(c)
#                return (c, 100)
#            elif g != 0:
#                removePion(c)
#                return (c, 0)
#            elif depth < profondeur_recherche:
                (g, l) = gagnant3()
                print("   "*depth, "%s: g2 () = (%s, %s)" % (c, g, l))
                if l == 10000:
                    removePion(c)
                    if g == joueur:
                        return [c, 10000]
                    else:
                        return [c, -10000]
                else:
                    if l > bestMove[1]:
                        bestMove = [c, l]
                    elif l < worstMove[1]:
                        worstMove = [c, l]
                (p, score) = trouveMeilleurePosition(joueur, (joueurCourant%2)+1, depth+1)
                if score > bestMove[1]:
                    bestMove = [p, score]
                if score < worstMove[1]:
                    worstMove = [p, score]
                removePion(c)
    print("   "*depth, "bM = %s - wM = %s" % (bestMove, worstMove))
    if joueur == joueurCourant:
        return bestMove
    else:
        return worstMove

def ordinateurJoue():
    global player, plateau
    placed = False
    choose = -1
    # Joue en se basant sur l'algorithme min/max
    (c, s) = trouveMeilleurePosition(player, player, 0)
    print("Place un pion en %s (%s)" % (c, s))
    placed = placePionAndMore(c)
    # Sinon place au hasard !
    while not placed:
        choose = random.randint(0, max_colonnes)
        print("Place un pion au hasard en %s" % choose)
        placed = placePionAndMore(choose)

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("Puissance 4")

quitter = False
# Profiling
import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()
#####################
# Boucle principale #
#####################
while quitter != True:
#while fini != True:
    # Boucle d'evenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            if event.key == pygame.K_SPACE:
                if computer[player] == False and not fini:
                    if not placePionAndMore(position):
                        errorSound.play()
            if event.key == pygame.K_LEFT:
                if position > 0:
                    position -= 1
            if event.key == pygame.K_RIGHT:
                if position < max_colonnes:
                    position += 1
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_F1:
                computer[1] = not computer[1]
            if event.key == pygame.K_F2:
                computer[2] = not computer[2]

    # Affichage
    ecran.fill(bleu)
    pygame.draw.rect(ecran, noir, (0, 0, largeur, v_remainder))
    for i in range(0, nb_colonnes):
        for j in range(0, nb_lignes):
            if plateau[i][j] == 0:
                pygame.draw.circle(ecran, noir, (h_remainder+(2*i+1)*(rayon+margin), v_remainder+(2*j+1)*(rayon+margin)), rayon)
            elif plateau[i][j] == 1:
                pygame.draw.circle(ecran, rouge, (h_remainder+(2*i+1)*(rayon+margin), v_remainder+(2*j+1)*(rayon+margin)), rayon)
            elif plateau[i][j] == 2:
                pygame.draw.circle(ecran, jaune, (h_remainder+(2*i+1)*(rayon+margin), v_remainder+(2*j+1)*(rayon+margin)), rayon)
    g = gagnant2()
    if g[0] == 1 and g[1] == 0:
        print("Joueur %s gagne !" % player)
        infos = police.render("Joueur %s gagne !" % player, True, rouge)
        ecran.blit(infos, (0, 0))
    elif g[0] == 2 and g[1] == 0:
        print("Joueur %s gagne !" % player)
        infos = police.render("Joueur %s gagne !" % player, True, jaune)
        ecran.blit(infos, (0, 0))
    elif fini:
        print("Match nul !")
        infos = police.render("Match nul !", True, bleu)
        ecran.blit(infos, (0, 0))
    else:
        if player == 1 and computer[player] == False:
            pygame.draw.circle(ecran, rouge, (h_remainder+(2*position+1)*(rayon+margin), v_remainder-(rayon+margin)), rayon+margin)
        elif player == 2 and computer[player] == False:
            pygame.draw.circle(ecran, jaune, (h_remainder+(2*position+1)*(rayon+margin), v_remainder-(rayon+margin)), rayon+margin)
    pygame.display.flip()
    if computer[player] and not fini:
        ordinateurJoue()

#time.sleep(5)

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
