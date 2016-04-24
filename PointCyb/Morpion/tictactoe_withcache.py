#!/usr/bin/python2
import sys, pygame, random, time
pygame.init()

##############
# Constantes #
##############
board_size = 300
square_size = board_size / 3

infos_height = 20
infos_lines = 3
margin = 5
max_depth = [ 9 , 9 ]

screen = pygame.display.set_mode([board_size, board_size+infos_lines*infos_height+margin])
pygame.display.set_caption("Tic-tac-toe")

blanc = 255, 255, 255
rouge = 255, 0, 0
bleu = 0, 0, 255
noir = 0, 0, 0

#############
# Variables #
#############
quitter = False
autoRestart = False
parties = 0
infos = ""
additionalInfos = ""

# True pour que l'ordinateur joue ce joueur
IA = [False, True]
lettres = [ 'X', 'O' ]
scores = [ 0, 0 ]
playing = 0
r_0_3 = range(0, 3)
r_0_2 = range(0, 2)

bestMoves = {}
boardState = [ [ 0, 0, 0 ], [ 0, 0, 0], [0, 0, 0] ]

#errorSound = pygame.mixer.Sound("ressources/Error.ogg")
police = pygame.font.SysFont("arial", infos_height);

def resetBoard():
    global additionalInfos, boardState
    for i in range(0, 3):
        for j in range(0, 3):
            boardState[i][j] = 0
    additionalInfos = ""
    drawBoard()

def winner():
    for i in r_0_3:
        # Verifie les lignes
        lineElt = boardState[i][0]
        if lineElt == boardState[i][1] and lineElt == boardState[i][2] and lineElt != 0:
            return lineElt
        # Verifie les colonnes
        lineElt = boardState[0][i]
        if lineElt == boardState[1][i] and lineElt == boardState[2][i] and lineElt != 0:
            return lineElt
    # Verifie les diagonales
    lineElt = boardState[0][0]
    if lineElt == boardState[1][1] and lineElt == boardState[2][2] and lineElt != 0:
        return lineElt
    lineElt = boardState[0][2]
    if lineElt == boardState[1][1] and lineElt == boardState[2][0] and lineElt != 0:
        return lineElt
    return 0

def empty():
    for i in range(0, 3):
        for j in range(0, 3):
            if boardState[i][j] != 0:
                return False
    return True

def finished():
    if winner() != 0:
        return True
    for i in range(0, 3):
        for j in range(0, 3):
            if boardState[i][j] == 0:
                return False
    return True

def boardString():
    b = ""
    for i in range(0, 3):
        for j in range(0, 3):
            b += "%s" % boardState[i][j]
    return b

def displayBoard():
    for i in range(0, 3):
        print("-------------")
        for j in range(0, 3):
            b = boardState[i][j]
            if b == 0:
                b = '.'
            print("| %s" % b),
        print("|")
        #print("| %s | %s | %s" % (boardState[i][0], boardState[i][1], boardState[i][2]))
    print("-------------")
    print("")

def otherPlayer(player):
    return (player + 1) % 2

# Retourne True si le plateau est symetrique par rapport a l'axe vertical central
def symV():
    if boardState[0][0] != boardState[0][2]:
        return False
    if boardState[1][0] != boardState[1][2]:
        return False
    if boardState[2][0] != boardState[2][2]:
        return False
    return True

# Retourne True si le plateau est symetrique par rapport a l'axe horizontal central
def symH():
    if boardState[0][0] != boardState[2][0]:
        return False
    if boardState[0][1] != boardState[2][1]:
        return False
    if boardState[0][2] != boardState[2][2]:
        return False
    return True

# Retourne True si le plateau est symetrique par rapport a l'axe diagonal descendant
def symD1():
    if boardState[0][1] != boardState[1][0]:
        return False
    if boardState[0][2] != boardState[2][0]:
        return False
    if boardState[1][2] != boardState[2][1]:
        return False
    return True

# Retourne True si le plateau est symetrique par rapport a l'axe diagonal montant
def symD2():
    if boardState[0][1] != boardState[1][2]:
        return False
    if boardState[0][0] != boardState[2][2]:
        return False
    if boardState[1][0] != boardState[2][1]:
        return False
    return True

# Retourne le meilleur coup a jouer pour le joueur toPlay a la profondeur "depth", le coup que l'on explore etant celui du joueur "player"
def placeBest(player, toPlay, depth):
    global lettres
    if depth < 0:
        print("Depth: %s" % depth)
        displayBoard()
    bestMove = [-1, -1, -3]
    worstMove = [-1, -1, 3]
    w = winner()
    if w != 0:
        if w == lettres[player]:
            return (-1, -1, 2-0.1*depth)
        else:
            return (-1, -1, -2+0.1*depth)
    rgi = r_0_3
    rgj = r_0_3
    if symH():
        rgi = r_0_2
    if symV():
        rgj = r_0_2
    sD1 = symD1()
    sD2 = symD2()
    if depth <= max_depth[player]:
        for i in rgi:
            for j in rgj:
                if sD1 and j < i:
                    continue
                if sD2 and 2-j < i:
                    continue
                if boardState[i][j] == 0:
                    boardState[i][j] = lettres[toPlay]
                    result = placeBest(player, otherPlayer(toPlay), depth+1)
                    if result[2] > bestMove[2]:
                        bestMove = [i, j, result[2]]
                    if result[2] < worstMove[2]:
                        worstMove = [i, j, result[2]]
                    boardState[i][j] = 0
    if bestMove[2] == -3 and worstMove[2] == 3:
        # N'a pas aboutit a un gagnant ou un perdant: match nul ou issue incertaine
        return (-1, -1, 0)
    if player == toPlay:
        return bestMove
    else:
        return worstMove

# Verifie si il y a un gagnant et met a jour le score
def checkWinner():
    global parties
    if finished():
        w = winner()
        if lettres[0] == w:
            scores[0] += 1
        elif lettres[1] == w:
            scores[1] += 1
        parties += 1

# Fait jouer l'ordinateur
def computerPlays():
    global playing, boardState, additionalInfos
    # C'est ce que le programme joue de toute facon pour le premier coup mais sans le hard-coder, il met plusieurs secondes pour le faire !
    if empty():
        boardState[0][0] = lettres[playing]
        additionalInfos = " - Should be a tie"
    else:
        b = "%s_%s" % (playing, boardString())
        (i, j, s) = (-1, -1, -1)
        if b in bestMoves:
            (i, j, s) = bestMoves[b]
        else:
            (i, j, s) = placeBest(playing, playing, 0)
            bestMoves[b] = (i, j, s)
        if s >= 1:
            additionalInfos = " - %s should win" % lettres[playing]
        elif s <= -1:
            additionalInfos = " - %s should win" % lettres[otherPlayer(playing)]
        else:
            additionalInfos = " - Should be a tie"
        boardState[i][j] = lettres[playing]
    playing = otherPlayer(playing)
    checkWinner()

# Gere le clic de souris
def mouse_clicked(x, y):
    global playing
    if finished() or IA[playing]:
        #errorSound.play()
        return
    x_min = margin
    y_min = margin
    i = 0
    col = -1
    row = -1
    while i < 3:
        if x > x_min and x < x_min + square_size:
            col = i
        if y > y_min and y < y_min + square_size:
            row = i
        i += 1
        x_min += square_size + margin
        y_min += square_size + margin
    if col == -1 or row == -1:
        return
    if boardState[row][col] == 0:
        boardState[row][col] = lettres[playing]
    else:
        #errorSound.play()
        return
    playing = otherPlayer(playing)
    checkWinner()

# Gere l'affichage
def drawBoard():
    screen.fill(blanc)
    for i in range(0, 3):
        pygame.draw.line(screen, noir, (margin, i*square_size), (board_size - margin, i*square_size))
    for i in range(0, 3):
        pygame.draw.line(screen, noir, (i*square_size, margin), (i*square_size, board_size - margin))
    for i in range(0, 3):
        for j in range(0,3):
            if boardState[i][j] == 'X':
                pygame.draw.rect(screen, bleu, pygame.Rect(j*square_size + 2*margin, i*square_size + 2*margin, square_size-4*margin, square_size-4*margin))
            elif boardState[i][j] == 'O':
                pygame.draw.circle(screen, rouge, (j*square_size + square_size/2, i*square_size + square_size/2), square_size/2 - 2*margin)
    J1 = "Humain"
    J2 = "Humain"
    if IA[0]:
            J1 = "IA (%s)" % max_depth[0]
    if IA[1]:
            J2 = "IA (%s)" % max_depth[1]
    infos_s = police.render(infos, True, rouge)
    infos2_s = police.render("Joueur 1: %s/%s (%s)" % (scores[0], parties, J1), True, bleu)
    infos3_s = police.render("Joueur 2: %s/%s (%s)" % (scores[1], parties, J2), True, rouge)
    screen.blit(infos_s, (0, board_size))
    screen.blit(infos2_s, (0, board_size+infos_height))
    screen.blit(infos3_s, (0, board_size+2*infos_height))
    pygame.display.flip()

# Boucle principale du jeu
while not quitter:
#    pygame.mouse.set_visible(True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            if event.key == pygame.K_r:
                if event.mod == pygame.KMOD_SHIFT or event.mod == pygame.KMOD_LSHIFT or event.mod == pygame.KMOD_RSHIFT:
                    autoRestart = not autoRestart
                else:
                    resetBoard()
            if event.key == pygame.K_F1:
                IA[0] = not IA[0]
                additionalInfos = ""
            if event.key == pygame.K_F2:
                IA[1] = not IA[1]
                additionalInfos = ""
            if event.key == pygame.K_u:
                if event.mod == pygame.KMOD_SHIFT or event.mod == pygame.KMOD_LSHIFT or event.mod == pygame.KMOD_RSHIFT:
                    if max_depth[0] < 9:
                        max_depth[0] += 1
                else:
                    if max_depth[0] > 1:
                        max_depth[0] -= 1
                # Reinitialise le cache pour "perdre" l'intelligence acquise avec un niveau de recherche different
                bestMoves = {}
            if event.key == pygame.K_d:
                if event.mod == pygame.KMOD_SHIFT or event.mod == pygame.KMOD_LSHIFT or event.mod == pygame.KMOD_RSHIFT:
                    if max_depth[1] < 9:
                        max_depth[1] += 1
                else:
                    if max_depth[1] > 1:
                        max_depth[1] -= 1
                # Reinitialise le cache pour "perdre" l'intelligence acquise avec un niveau de recherche different
                bestMoves = {}
            if event.key == pygame.K_b:
                print("Best moves (%s):" % len(bestMoves))
                print(bestMoves)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked(event.pos[0], event.pos[1])

    f = finished()
    if IA[playing] and not f:
        infos = "Computing ..."
    elif f:
        w = winner()
        if w == 0:
            infos = "It's a tie !"
        else:
            infos = "%s won !" % w
    else:
        infos = "%s to play" % lettres[playing]
    if not f:
        infos += additionalInfos
    drawBoard()

    if IA[playing] and not f:
        computerPlays()
    if f and autoRestart:
        resetBoard()

pygame.quit()
