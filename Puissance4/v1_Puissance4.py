#!/usr/bin/python2
import pygame, random, math, time, sys

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

r_col = range(0, nb_colonnes)
r_lig = range(0, nb_lignes)
r_col_rev = range(max_colonnes, -1, -1)
r_lig_rev = range(max_lignes, -1, -1)
r_1_3 = range(1, 3)
r_diag = range(-(nb_lignes-4), nb_colonnes+nb_lignes-4)

#############
# Variables #
#############
position = 0
plateau = []
for i in r_col:
    plateau.append([])
    for j in r_lig:
        plateau[i].append(0)
player = 1

computer = [False, True, True]
fini = False
quitter = False

#############
# Fonctions #
#############

def reset():
    global fini, plateau
    for i in r_col:
        for j in r_lig:
            plateau[i][j] = 0
    fini = False

def otherCouleur(couleur):
    if couleur == 1:
        return 2
    if couleur == 2:
        return 1
    return couleur

def affichePlateau():
    for j in r_lig:
        ligne = ""
        for i in r_col:
            ligne = "%s %s" % (ligne, plateau[i][j])
        print(ligne)

def gagnant(verbose = False):
    global nb_colonnes, nb_lignes, plateau, fini
    places = [ 0, 0, 0 ]
    count3 = [ 0, 0, 0 ]
    count2 = [ 0, 0, 0 ]
    # Verticales
    if verbose:
        print(" ==== Verticales ==== ")
    for i in r_col:
        count = 0
        couleur = 0
        for j in r_lig_rev:
            if plateau[i][j] == couleur:
                count += 1
            else:
                # 2 ou 3 pions alignes verticalement n'est utile que si il y a une place pour un quatrieme
                if count == 2 and plateau[i][j] == 0 and j > 0:
                    count2[couleur] += 1
                if count == 3 and plateau[i][j] == 0:
                    count3[couleur] += 1
                couleur = plateau[i][j]
                count = 1
            # Une colonne s'arrete des qu'on trouve une case vide
            if couleur == 0:
                break
            if count == 4:
                fini = True
                return (couleur, 1000000)
            if i == 2 or i == 4:
                places[couleur] += 1
            elif i == 3:
                places[couleur] += 3
    # Horizontales
    if verbose:
        print(" ==== Horizontales ==== ")
    for j in r_lig:
        count = [0, 0, 0]
        succ = 0
        potentiel = 0
        couleur = -1
        prev_couleur = 0
        for i in r_col:
            if j == 5 and verbose:
                print("plateau[%s][%s]: %s - count: [%s, %s, %s] - potentiel: %s" % (i, j, plateau[i][j], count[0], count[1], count[2], potentiel))
            if plateau[i][j] == couleur:
                count[couleur] += 1
                succ += 1
                if couleur == 0:
                    potentiel += 1
                if j == 5 and verbose:
                    print("  +1 %s: count[%s] = %s - potentiel = %s" % (couleur, couleur, count[couleur], potentiel))
            else:
                succ = 1
                nv_coul = plateau[i][j]
                if nv_coul != 0:
                    # Entre dans une couleur: on verifie si on a un alignement
                    c = otherCouleur(nv_coul)
                    if j == 5 and verbose:
                        print("  test: count[%s] = %s - count[%s] = %s - potentiel = %s" % (0, count[0], c, count[c], potentiel))
                    if count[c] >= 3 and count[0] >= 1:
                        count3[c] += 1
                        if j == 5 and verbose:
                            print("  count3[%s] = %s" % (c, count3[c]))
                    if count[c] == 2 and count[0] >= 2:
                        count2[c] += 1
                        if j == 5 and verbose:
                            print("  count2[%s] = %s" % (c, count2[c]))
                    if couleur == 0:
                        # Passe de vide a une couleur: le compteur d'emplacement vides passe a potentiel
                        count[0] = potentiel
                    elif nv_coul != prev_couleur:
                        potentiel = 0
                if nv_coul != 0 and prev_couleur != nv_coul:
                    if j == 5 and verbose:
                        print("  chgCoul: nv_coul = %s - prev_couleur = %s" % (nv_coul, prev_couleur))
                    if prev_couleur != 0:
                        count[prev_couleur] = 0
                    count[nv_coul] = 1
                    prev_couleur = nv_coul
                else:
                    count[nv_coul] += 1
                if nv_coul == 0:
                    potentiel = 1
                couleur = nv_coul
            if succ == 4 and couleur != 0:
                fini = True
                return (couleur, 1000000)
        for c in r_1_3:
            if count[c] >= 3 and count[0] >= 1:
                count3[c] += 1
                if j == 5 and verbose:
                    print("  eol: count3[%s] = %s" % (c, count3[c]))
            if count[c] == 2 and count[0] >= 2:
                count2[c] += 1
                if j == 5 and verbose:
                    print("  eol: count2[%s] = %s" % (c, count2[c]))
    #      -2-1 0 1 2 3 4 5 6 7 8
    #  0        X X X Z X X X   Y
    #  1        X X Z X X X X Y
    #  2        X Z X X X X Z
    #  3        Z X X X X Z X
    #  4      Y X X X X Z X X
    #  5    Y   X X X Z X X X
    #       - - - - - - - - - - -    <--- Largeur totale a considerer: nb_colonnes + 2*(nb_lignes - 4)
    # Diagonales montantes
    if verbose:
        print(" ==== Diagonales montantes ==== ")
    for k in r_diag:
        count = [0, 0, 0]
        succ = 0
        potentiel = 0
        couleur = -1
        prev_couleur = 0
        for l in r_lig:
            j = max_lignes - l
            i = k + l
            if i < 0:
                continue
            if i >= nb_colonnes:
                break
            if verbose:
                print("plateau[%s][%s]: %s - count: [%s, %s, %s] - potentiel: %s" % (i, j, plateau[i][j], count[0], count[1], count[2], potentiel))
            if plateau[i][j] == couleur:
                count[couleur] += 1
                succ += 1
                if couleur == 0:
                    potentiel += 1
            else:
                nv_coul = plateau[i][j]
                succ = 1
                if nv_coul != 0:
                    # Entre dans une couleur: on verifie si on a un alignement
                    c = otherCouleur(nv_coul)
                    if verbose:
                        print("  chgCoul: count[%s] = %s - potentiel: %s" % (c, count[c], potentiel))
                    if count[c] >= 3 and count[0] >= 1:
                        count3[c] += 1
                    if count[c] == 2 and count[0] >= 2:
                        count2[c] += 1
                    if couleur == 0:
                        # Passe de vide a une couleur: le compteur d'emplacement vides passe a potentiel
                        count[0] = potentiel
                    elif nv_coul != prev_couleur:
                        potentiel = 0
                if nv_coul != 0 and prev_couleur != nv_coul:
                    if prev_couleur != 0:
                        count[prev_couleur] = 0
                    count[nv_coul] = 1
                    prev_couleur = nv_coul
                else:
                    count[nv_coul] += 1
                if nv_coul == 0:
                    potentiel += 1
                couleur = nv_coul
            if succ == 4 and couleur != 0:
                fini = True
                return (couleur, 1000000)
        for c in r_1_3:
            if count[c] >= 3 and count[0] >= 1:
                count3[c] += 1
                if verbose:
                    print("  eol: count3[%s] = %s" % (c, count3[c]))
            if count[c] == 2 and count[0] >= 2:
                count2[c] += 1
                if verbose:
                    print("  eol: count2[%s] = %s" % (c, count2[c]))
    # Diagonales descendantes
    if verbose:
        print(" ==== Diagonales descendantes ==== ")
    for k in r_diag:
        count = [0, 0, 0]
        succ = 0
        potentiel = 0
        couleur = -1
        prev_couleur = 0
        for j in r_lig:
            i = k + j
            if i < 0:
                continue
            if i >= nb_colonnes:
                break
            if verbose:
                print("plateau[%s][%s]: %s - count: [%s, %s, %s] - potentiel: %s" % (i, j, plateau[i][j], count[0], count[1], count[2], potentiel))
            if plateau[i][j] == couleur:
                count[couleur] += 1
                succ += 1
                if couleur == 0:
                    potentiel += 1
            else:
                nv_coul = plateau[i][j]
                succ = 1
                if nv_coul != 0:
                    # Entre dans une couleur: on verifie si on a un alignement
                    c = otherCouleur(nv_coul)
                    if verbose:
                        print("  chgCoul: count[%s] = %s - potentiel: %s" % (c, count[c], potentiel))
                    if count[c] >= 3 and count[0] >= 1:
                        count3[c] += 1
                    if count[c] == 2 and count[0] >= 2:
                        count2[c] += 1
                    if couleur == 0:
                        # Passe de vide a une couleur: le compteur d'emplacement vides passe a potentiel
                        count[0] = potentiel
                    elif nv_coul != prev_couleur:
                        potentiel = 0
                if nv_coul != 0 and prev_couleur != nv_coul:
                    if prev_couleur != 0:
                        count[prev_couleur] = 0
                    count[nv_coul] = 1
                    prev_couleur = nv_coul
                else:
                    count[nv_coul] += 1
                if nv_coul == 0:
                    potentiel += 1
                couleur = nv_coul
            if succ == 4 and couleur != 0:
                fini = True
                return (couleur, 1000000)
        for c in r_1_3:
            if count[c] >= 3 and count[0] >= 1:
                count3[c] += 1
                if verbose:
                    print("  eol: count3[%s] = %s" % (c, count3[c]))
            if count[c] == 2 and count[0] >= 2:
                count2[c] += 1
                if verbose:
                    print("  eol: count2[%s] = %s" % (c, count2[c]))
    # Calcul du score final
    score = 100*(count3[1]-count3[2])+10*(count2[1]-count2[2])+places[1]-places[2]
    if score > 0:
        return (1, score)
    elif score < 0:
        return (2, -score)
    return (0, 0)

def removePion(col):
    global player
    removed = False
    for i in r_lig:
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
    for lig in r_lig_rev:
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
    for i in r_col:
        if plateau[i][0] == 0:
            fini = False
    return placed

def trouveMeilleurePosition(joueur, joueurCourant, depth):
#print("  "*depth + "tMP(%s, %s, %s)" % (joueur, joueurCourant, depth))
    score = 0
    bestMove = [ 0, -1000000 ]
    worstMove = [ 0, 1000000 ]
    for c in r_col:
        placed = placePion(c, joueurCourant)
        if placed:
            (g, l) = gagnant()
#print("  "*depth + "  placed = %s - gagnant = (%s, %s)" % (c, g, l))
            if l == 1000000:
                removePion(c)
                if g == joueur:
                    return [c, 1000000]
                else:
                    return [c, -1000000]
            if g != joueur:
                l = -l
            if depth <= profondeur_recherche:
                (p, score) = trouveMeilleurePosition(joueur, otherCouleur(joueurCourant), depth+1)
                if score > bestMove[1]:
                    bestMove = [c, score]
                if score < worstMove[1]:
                    worstMove = [c, score]
            else:
                if l > bestMove[1]:
                    bestMove = [c, l]
                elif l < worstMove[1]:
                    worstMove = [c, l]
#print("  "*depth + "  bM / wM = (%s, %s)" % (bestMove, worstMove))
            removePion(c)
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

test = False
if len(sys.argv) > 1:
    test = True
    if sys.argv[1] == 'hori1':
        plateau[3][5] = 1
        plateau[4][5] = 1
        plateau[5][5] = 1
        plateau[6][5] = 1
    elif sys.argv[1] == 'hori2':
        plateau[0][5] = 1
        plateau[1][5] = 1
        plateau[2][5] = 1
        plateau[3][5] = 1
    elif sys.argv[1] == 'hori3':
        plateau[3][2] = 1
        plateau[4][2] = 1
        plateau[5][2] = 1
        plateau[6][2] = 1
    elif sys.argv[1] == 'hori4':
        plateau[0][2] = 1
        plateau[1][2] = 1
        plateau[2][2] = 1
        plateau[3][2] = 1
    elif sys.argv[1] == 'hori5':
        plateau[3][0] = 1
        plateau[4][0] = 1
        plateau[5][0] = 1
        plateau[6][0] = 1
    elif sys.argv[1] == 'hori6':
        plateau[0][0] = 1
        plateau[1][0] = 1
        plateau[2][0] = 1
        plateau[3][0] = 1
    elif sys.argv[1] == 'vert1':
        plateau[6][2] = 1
        plateau[6][3] = 1
        plateau[6][4] = 1
        plateau[6][5] = 1
    elif sys.argv[1] == 'vert2':
        plateau[6][0] = 1
        plateau[6][1] = 1
        plateau[6][2] = 1
        plateau[6][3] = 1
        plateau[6][4] = 2
        plateau[6][5] = 2
    elif sys.argv[1] == 'vert3':
        plateau[3][2] = 1
        plateau[3][3] = 1
        plateau[3][4] = 1
        plateau[3][5] = 1
    elif sys.argv[1] == 'vert4':
        plateau[3][0] = 1
        plateau[3][1] = 1
        plateau[3][2] = 1
        plateau[3][3] = 1
        plateau[3][4] = 2
        plateau[3][5] = 2
    elif sys.argv[1] == 'vert5':
        plateau[0][2] = 1
        plateau[0][3] = 1
        plateau[0][4] = 1
        plateau[0][5] = 1
    elif sys.argv[1] == 'vert6':
        plateau[0][0] = 1
        plateau[0][1] = 1
        plateau[0][2] = 1
        plateau[0][3] = 1
        plateau[0][4] = 2
        plateau[0][5] = 2
    elif sys.argv[1] == 'mont1':
        plateau[3][5] = 1
        plateau[4][4] = 1
        plateau[5][3] = 1
        plateau[6][2] = 1
    elif sys.argv[1] == 'mont2':
        plateau[3][4] = 1
        plateau[4][3] = 1
        plateau[5][2] = 1
        plateau[6][1] = 1
    elif sys.argv[1] == 'mont3':
        plateau[3][3] = 1
        plateau[4][2] = 1
        plateau[5][1] = 1
        plateau[6][0] = 1
    elif sys.argv[1] == 'mont4':
        plateau[0][5] = 1
        plateau[1][4] = 1
        plateau[2][3] = 1
        plateau[3][2] = 1
    elif sys.argv[1] == 'mont5':
        plateau[0][4] = 1
        plateau[1][3] = 1
        plateau[2][2] = 1
        plateau[3][1] = 1
    elif sys.argv[1] == 'mont6':
        plateau[0][3] = 1
        plateau[1][2] = 1
        plateau[2][1] = 1
        plateau[3][0] = 1
    elif sys.argv[1] == 'desc1':
        plateau[6][5] = 1
        plateau[5][4] = 1
        plateau[4][3] = 1
        plateau[3][2] = 1
    elif sys.argv[1] == 'desc2':
        plateau[6][4] = 1
        plateau[5][3] = 1
        plateau[4][2] = 1
        plateau[3][1] = 1
    elif sys.argv[1] == 'desc3':
        plateau[6][3] = 1
        plateau[5][2] = 1
        plateau[4][1] = 1
        plateau[3][0] = 1
    elif sys.argv[1] == 'desc4':
        plateau[3][5] = 1
        plateau[2][4] = 1
        plateau[1][3] = 1
        plateau[0][2] = 1
    elif sys.argv[1] == 'desc5':
        plateau[3][4] = 1
        plateau[2][3] = 1
        plateau[1][2] = 1
        plateau[0][1] = 1
    elif sys.argv[1] == 'desc6':
        plateau[3][3] = 1
        plateau[2][2] = 1
        plateau[1][1] = 1
        plateau[0][0] = 1
    elif sys.argv[1] == 'mixh1':
        plateau[6][5] = 0
        plateau[5][5] = 0
        plateau[4][5] = 2
        plateau[3][5] = 0
        plateau[2][5] = 0
        plateau[1][5] = 1
        plateau[0][5] = 1
    elif sys.argv[1] == 'mixh2':
        plateau[6][5] = 0
        plateau[5][5] = 0
        plateau[4][5] = 2
        plateau[3][5] = 0
        plateau[2][5] = 1
        plateau[1][5] = 1
        plateau[0][5] = 0
    elif sys.argv[1] == 'mixh3':
        plateau[6][5] = 0
        plateau[5][5] = 0
        plateau[4][5] = 2
        plateau[3][5] = 1
        plateau[2][5] = 1
        plateau[1][5] = 0
        plateau[0][5] = 0
    elif sys.argv[1] == 'mixh4':
        plateau[6][5] = 0
        plateau[5][5] = 0
        plateau[4][5] = 2
        plateau[3][5] = 1
        plateau[2][5] = 1
        plateau[1][5] = 1
        plateau[0][5] = 0
    elif sys.argv[1] == 'mixh5':
        plateau[6][5] = 1
        plateau[5][5] = 0
        plateau[4][5] = 1
        plateau[3][5] = 1
        plateau[2][5] = 2
        plateau[1][5] = 0
        plateau[0][5] = 0
    elif sys.argv[1] == 'mixh6':
        plateau[6][5] = 0
        plateau[5][5] = 0
        plateau[4][5] = 2
        plateau[3][5] = 1
        plateau[2][5] = 1
        plateau[1][5] = 0
        plateau[0][5] = 1
    elif sys.argv[1] == 'mixh7':
        plateau[6][5] = 1
        plateau[5][5] = 0
        plateau[4][5] = 2
        plateau[3][5] = 0
        plateau[2][5] = 2
        plateau[1][5] = 1
        plateau[0][5] = 2
    elif sys.argv[1] == 'mixh8':
        plateau[6][5] = 0
        plateau[5][5] = 1
        plateau[4][5] = 1
        plateau[3][5] = 1
        plateau[2][5] = 2
        plateau[1][5] = 0
        plateau[0][5] = 0
    elif sys.argv[1] == 'mixv1':
        plateau[0][5] = 1
        plateau[0][4] = 1
    elif sys.argv[1] == 'mixv2':
        plateau[0][5] = 1
        plateau[0][4] = 1
        plateau[0][3] = 1
    elif sys.argv[1] == 'mixv3':
        plateau[0][5] = 1
        plateau[0][4] = 1
        plateau[0][3] = 1
        plateau[0][2] = 2
    elif sys.argv[1] == 'mixv4':
        plateau[0][5] = 1
        plateau[0][4] = 1
        plateau[0][3] = 2
    elif sys.argv[1] == 'mixm1':
        plateau[3][5] = 1
        plateau[4][4] = 1
        plateau[5][3] = 1
        plateau[6][2] = 0
    elif sys.argv[1] == 'mixm2':
        plateau[2][5] = 0
        plateau[3][4] = 1
        plateau[4][3] = 1
        plateau[5][2] = 1
        plateau[6][1] = 2
    elif sys.argv[1] == 'mixm3':
        plateau[2][5] = 1
        plateau[3][4] = 0
        plateau[4][3] = 0
        plateau[5][2] = 1
        plateau[6][1] = 2
    elif sys.argv[1] == 'mixm4':
        plateau[2][5] = 1
        plateau[3][4] = 2
        plateau[4][3] = 0
        plateau[5][2] = 2
        plateau[6][1] = 2
    elif sys.argv[1] == 'mixm5':
        plateau[0][5] = 0
        plateau[1][4] = 1
        plateau[2][3] = 1
        plateau[3][2] = 0
        plateau[4][1] = 2
    elif sys.argv[1] == 'mixm6':
        plateau[0][3] = 2
        plateau[1][2] = 0
        plateau[2][1] = 2
        plateau[3][0] = 2
    elif sys.argv[1] == 'mixm7':
        plateau[0][3] = 1
        plateau[1][2] = 0
        plateau[2][1] = 0
        plateau[3][0] = 1
    elif sys.argv[1] == 'mixm8':
        plateau[0][5] = 2
        plateau[1][4] = 0
        plateau[2][3] = 1
        plateau[3][2] = 0
        plateau[4][1] = 1
        plateau[5][0] = 2
    elif sys.argv[1] == 'mixd1':
        plateau[6][5] = 1
        plateau[5][4] = 1
        plateau[4][3] = 1
        plateau[3][2] = 0
        plateau[2][1] = 2
    elif sys.argv[1] == 'mixd2':
        plateau[6][4] = 2
        plateau[5][3] = 0
        plateau[4][2] = 0
        plateau[3][1] = 2
    elif sys.argv[1] == 'mixd3':
        plateau[3][5] = 1
        plateau[2][4] = 0
        plateau[1][3] = 1
        plateau[0][2] = 0
    elif sys.argv[1] == 'mixd4':
        plateau[4][5] = 1
        plateau[3][4] = 0
        plateau[2][3] = 1
        plateau[1][2] = 0
        plateau[0][1] = 2
    elif sys.argv[1] == 'mixd5':
        plateau[5][5] = 2
        plateau[4][4] = 0
        plateau[3][3] = 1
        plateau[2][2] = 0
        plateau[1][1] = 1
        plateau[0][0] = 2
    elif sys.argv[1] == 'mixd6':
        plateau[5][5] = 1
        plateau[4][4] = 1
        plateau[3][3] = 0
        plateau[2][2] = 1
        plateau[1][1] = 1
        plateau[0][0] = 0
    elif sys.argv[1] == 'gagne1':
#2 1 0 2 0 0 0
#2 2 0 2 0 0 0
#1 1 0 1 0 0 0
#2 2 0 2 0 0 0
#1 1 0 2 0 1 0
#1 1 2 2 0 1 1
        plateau[0][0] = 2
        plateau[1][0] = 1
        plateau[3][0] = 2

        plateau[0][1] = 2
        plateau[1][1] = 2
        plateau[3][1] = 2

        plateau[0][2] = 1
        plateau[1][2] = 1
        plateau[3][2] = 1

        plateau[0][3] = 2
        plateau[1][3] = 2
        plateau[3][3] = 2

        plateau[0][4] = 1
        plateau[1][4] = 1
        plateau[3][4] = 2
        plateau[5][4] = 1

        plateau[0][5] = 1
        plateau[1][5] = 1
        plateau[2][5] = 2
        plateau[3][5] = 2
        plateau[5][5] = 1
        plateau[6][5] = 1
    else:
        print("Error: Unknown test case '%s'" % sys.argv[1])
        sys.exit(1)
    verbose = False
    fast = False
    if len(sys.argv) > 2: 
        if sys.argv[2] == 'verbose':
            verbose = True
        elif sys.argv[2] == 'fast':
            fast = True
    g = gagnant(verbose)
    print("Gagnant: (%s, %s)" % g)
    if fast:
        if g[0] == 1 and g[1] == 1000000:
            print("Joueur %s gagne !" % player)
        elif g[0] == 2 and g[1] == 1000000:
            print("Joueur %s gagne !" % player)
        sys.exit(0)

##################
# Initialisation #
##################
pygame.init()
errorSound = pygame.mixer.Sound("Error.ogg")
police = pygame.font.SysFont("arial", 50);

ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("Puissance 4")

# Profiling
import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()
#####################
# Boucle principale #
#####################
#while quitter != True:
while fini != True:
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
    for i in r_col:
        for j in r_lig:
            if plateau[i][j] == 0:
                pygame.draw.circle(ecran, noir, (h_remainder+(2*i+1)*(rayon+margin), v_remainder+(2*j+1)*(rayon+margin)), rayon)
            elif plateau[i][j] == 1:
                pygame.draw.circle(ecran, rouge, (h_remainder+(2*i+1)*(rayon+margin), v_remainder+(2*j+1)*(rayon+margin)), rayon)
            elif plateau[i][j] == 2:
                pygame.draw.circle(ecran, jaune, (h_remainder+(2*i+1)*(rayon+margin), v_remainder+(2*j+1)*(rayon+margin)), rayon)
    g = gagnant()
    if g[1] == 1000000:
        print("Joueur %s gagne !" % g[0])
        infos = police.render("Joueur %s gagne !" % g[0], True, jaune)
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
    if test:
        time.sleep(1)
        pygame.quit()
        exit(0)
    if computer[player] and not fini:
        ordinateurJoue()

#time.sleep(5)
affichePlateau()

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
