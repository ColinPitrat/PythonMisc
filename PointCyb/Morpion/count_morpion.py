#!/usr/bin/python2
import sys, pygame, random, time
pygame.init()

##############
# Constantes #
##############
plateau = pygame.image.load("ressources/plateau.png")
croix = pygame.image.load("ressources/croix.png")
rond = pygame.image.load("ressources/rond.png")
infos_height = 20
infos_lines = 3
margin = 5
max_depth = [ 9 , 9 ]

print("%s - %s" % (plateau.get_width(), plateau.get_height()))
screen = pygame.display.set_mode([plateau.get_width(), plateau.get_height()+infos_lines*infos_height+margin])
pygame.display.set_caption("Morpion")

blanc = 255, 255, 255
rouge = 255, 0, 0
bleu = 0, 0, 255

#############
# Variables #
#############
quitter = False
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
nbsteps = 0
nbparties = 0

# Parametres dependant de l'image du plateau
x_margin = 4
y_margin = 4
x_step = 102
y_step = 102

origin = pygame.Rect(0, 0, 0, 0)
boardPlaces = [ ]
boardState = [ [ 0, 0, 0 ], [ 0, 0, 0], [0, 0, 0] ]

errorSound = pygame.mixer.Sound("ressources/Error.ogg")
police = pygame.font.SysFont("arial", infos_height);

# Initialise les rectangles correspondant aux positions du plateau
for i in range(0, 3):
    line = []
    for j in range(0, 3):
        line.append(pygame.Rect((x_step + x_margin)*j + x_margin, (y_step + y_margin)*i + y_margin, x_step, y_step))
    boardPlaces.append(line)

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

def displayBoard():
    for i in range(0, 3):
        print("------------")
        print("%s | %s | %s" % (boardState[i][0], boardState[i][1], boardState[i][2]))
    print("------------")
    print("")

def otherPlayer(player):
    return (player + 1) % 2

def symV():
    for i in r_0_3:
        if boardState[i][0] != boardState[i][2]:
            return False
    return True

def symH():
    for j in r_0_3:
        if boardState[0][j] != boardState[2][j]:
            return False
    return True

def symD1():
    if boardState[0][1] != boardState[1][0]:
        return False
    if boardState[0][2] != boardState[2][0]:
        return False
    if boardState[1][2] != boardState[2][1]:
        return False
    return True

def symD2():
    if boardState[0][1] != boardState[1][2]:
        return False
    if boardState[0][0] != boardState[2][2]:
        return False
    if boardState[1][0] != boardState[2][1]:
        return False
    return True

def placeBest(player, toPlay, depth):
    global lettres, nbsteps, nbparties
    bestMove = [-1, -1, -3]
    worstMove = [-1, -1, 3]
    played = False
    w = winner()
    if w != 0:
        nbparties += 1
        return (-1, -1, 0)
    rgi = r_0_3
    rgj = r_0_3
    if symH():
        rgi = r_0_2
    if symV():
        rgj = r_0_2
    sD1 = symD1()
    sD2 = symD2()
    if depth == 1:
        if symH():
            print("H symetry:")
            displayBoard()
        if symV():
            print("V symetry:")
            displayBoard()
        if symD1():
            print("D1 symetry:")
            displayBoard()
        if symD2():
            print("D2 symetry:")
            displayBoard()
    if depth <= max_depth[player]:
        for i in rgi:
            for j in rgj:
                if sD1 and j < i:
                    continue
                if sD2 and 2-j < i:
                    continue
                if boardState[i][j] == 0:
                    played = True
                    nbsteps += 1
                    boardState[i][j] = lettres[toPlay]
#                        if w == lettres[player]:
#                            nbparties += 1
#                            return (i, j, 2-0.1*depth)
#                        else:
#                            nbparties += 1
#                            return (i, j, -2+0.1*depth)
#                    else:
                    result = placeBest(player, otherPlayer(toPlay), depth+1)
#                        if result[2] > bestMove[2]:
#                            bestMove = [i, j, result[2]]
#                        if result[2] < worstMove[2]:
#                            worstMove = [i, j, result[2]]
                    boardState[i][j] = 0
    if not played:
        nbparties += 1
    #if bestMove[2] == -3 and worstMove[2] == 3:
        # N'a pas aboutit a un gagnant ou un perdant: match nul ou issue incertaine
    return (-1, -1, 0)
    #if player == toPlay:
    #    return bestMove
    #else:
    #    return worstMove

def checkWinner():
    global parties
    if finished():
        w = winner()
        if lettres[0] == w:
            scores[0] += 1
        elif lettres[1] == w:
            scores[1] += 1
        parties += 1

def computerPlays():
    global playing, boardState, additionalInfos
    # C'est ce que le programme joue de toute facon pour le premier coup mais sans le hard-coder, il met plusieurs secondes pour le faire !
    if empty():
        boardState[0][0] = lettres[playing]
        additionalInfos = " - Should be a tie"
    else:
        (i, j, s) = placeBest(playing, playing, 0)
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
        errorSound.play()
        return
    x_min = x_margin
    y_min = y_margin
    i = 0
    col = -1
    row = -1
    while i < 3:
        if x > x_min and x < x_min + x_step:
            col = i
        if y > y_min and y < y_min + y_step:
            row = i
        i += 1
        x_min += x_step + x_margin
        y_min += y_step + y_margin
    if col == -1 or row == -1:
        return
    if boardState[row][col] == 0:
        boardState[row][col] = lettres[playing]
    else:
        errorSound.play()
        return
    playing = otherPlayer(playing)
    checkWinner()

def drawBoard():
    screen.blit(plateau, origin)
    for i in range(0, 3):
        for j in range(0,3):
            if boardState[i][j] == 'X':
                screen.blit(croix, boardPlaces[i][j])
            elif boardState[i][j] == 'O':
                screen.blit(rond, boardPlaces[i][j])
    J1 = "Humain"
    J2 = "Humain"
    if IA[0]:
            J1 = "IA (%s)" % max_depth[0]
    if IA[1]:
            J2 = "IA (%s)" % max_depth[1]
    infos_s = police.render(infos, True, rouge)
    infos2_s = police.render("Joueur 1: %s/%s (%s)" % (scores[0], parties, J1), True, bleu)
    infos3_s = police.render("Joueur 2: %s/%s (%s)" % (scores[1], parties, J2), True, rouge)
    screen.fill(blanc, (0, plateau.get_height(), plateau.get_width(), infos_lines*infos_height+margin))
    screen.blit(infos_s, (0, plateau.get_height()))
    screen.blit(infos2_s, (0, plateau.get_height()+infos_height))
    screen.blit(infos3_s, (0, plateau.get_height()+2*infos_height))
    pygame.display.flip()

pygame.mixer.music.load("ressources/Music.ogg")
pygame.mixer.music.set_volume(1.0)
#pygame.mixer.music.play(-1, 0.0)

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
            if event.key == pygame.K_d:
                if event.mod == pygame.KMOD_SHIFT or event.mod == pygame.KMOD_LSHIFT or event.mod == pygame.KMOD_RSHIFT:
                    if max_depth[1] < 9:
                        max_depth[1] += 1
                else:
                    if max_depth[1] > 1:
                        max_depth[1] -= 1
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

    if empty():
        placeBest(playing, playing, 0)
        print("Parties: %s" % nbparties)
        print("Etapes: %s" % nbsteps)
    break
    #if IA[playing] and not f:
    #    computerPlays()
pygame.mixer.music.stop()
pygame.quit()
