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
margin = 5
max_depth = [ 5 , 9 ]

screen = pygame.display.set_mode([plateau.get_width(), plateau.get_height()+2*infos_height+margin])
pygame.display.set_caption("Morpion")

blanc = 255, 255, 255
rouge = 255, 0, 0

#############
# Variables #
#############
quitter = False
parties = 1
infos = ""
additionalInfos = ""
explain = False

# True to play against computer
IA = [True, True]
lettres = [ 'X', 'O' ]
playing = 0

# Really depends on the board picture
x_margin = 4
y_margin = 4
x_step = 102
y_step = 102

origin = pygame.Rect(0, 0, 0, 0)
boardPlaces = [ ]
boardState = [ [ 0, 0, 0 ], [ 0, 0, 0], [0, 0, 0] ]

errorSound = pygame.mixer.Sound("ressources/Error.ogg")
police = pygame.font.SysFont("arial", infos_height);

# Initialize board rectangles
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
    # Check lines
    for i in range(0, 3):
        lineElt = boardState[i][0]
        if lineElt != 0 and lineElt == boardState[i][1] and lineElt == boardState[i][2]:
            return lineElt
    # Check columns
    for j in range(0, 3):
        lineElt = boardState[0][j]
        if lineElt != 0 and lineElt == boardState[1][j] and lineElt == boardState[2][j]:
            return lineElt
    # Check diagonals
    lineElt = boardState[0][0]
    if lineElt != 0 and lineElt == boardState[1][1] and lineElt == boardState[2][2]:
        return lineElt
    lineElt = boardState[0][2]
    if lineElt != 0 and lineElt == boardState[1][1] and lineElt == boardState[2][0]:
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

def placeBest(player, toPlay, depth):
    global lettres
    if explain:
        print("placeBest(%s, %s, %s)" % (player, toPlay, depth))
    bestMove = [-1, -1, -2]
    worstMove = [-1, -1, 2]
    if depth <= max_depth[player]:
        for i in range(0, 3):
            for j in range(0, 3):
                if boardState[i][j] == 0:
                    boardState[i][j] = lettres[toPlay]
                    if explain:
                        displayBoard()
                    if winner() != 0:
                        boardState[i][j] = 0
                        if winner() == lettres[player]:
                            if explain:
                                print("This is a winning path !")
                            return (i, j, 1)
                        else:
                            if explain:
                                print("This is a loosing path !")
                            return (i, j, -1)
                    else:
                        result = placeBest(player, otherPlayer(toPlay), depth+1)
                        if explain:
                            print("Returned %s" % list(result))
                        if result[2] > bestMove[2]:
                            bestMove = [i, j, result[2]]
                        if result[2] < worstMove[2]:
                            worstMove = [i, j, result[2]]
                    boardState[i][j] = 0
    if bestMove[2] == -2 and worstMove[2] == 2:
        # N'a pas aboutit a un gagnant ou un perdant: match nul ou issue incertaine
        return (-1, -1, 0)
    if player == toPlay:
        # Ne devrait pas se produire: un resultat 'normal' est entre -1 et 1 et devrait donc modifier a la fois worstMove et bestMove
        if bestMove[2] == -2:
            return worstMove
        return bestMove
    else:
        # Ne devrait pas se produire: un resultat 'normal' est entre -1 et 1 et devrait donc modifier a la fois worstMove et bestMove
        if worstMove[2] == 2:
            return bestMove
        return worstMove

def computerPlays():
    global playing, boardState, additionalInfos
    if not finished():
        # This is what the program plays anyway, but if we don't hardcode it it's taking a few seconds !
        if empty():
            boardState[0][0] = lettres[playing]
            additionalInfos = " - Should be a tie"
        else:
            (i, j, s) = placeBest(playing, playing, 0)
            if explain:
                print("Choose (%s, %s) with score %s" % (i, j, s))
            if s == 1:
                additionalInfos = " - %s should win" % lettres[playing]
            elif s == -1:
                additionalInfos = " - %s should win" % lettres[otherPlayer(playing)]
            else:
                additionalInfos = " - Should be a tie"
            boardState[i][j] = lettres[playing]
        playing = otherPlayer(playing)

# Callback for when a click occurs
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

def drawBoard():
    screen.blit(plateau, origin)
    for i in range(0, 3):
        for j in range(0,3):
            if boardState[i][j] == 'X':
                screen.blit(croix, boardPlaces[i][j])
            elif boardState[i][j] == 'O':
                screen.blit(rond, boardPlaces[i][j])
    infos_s = police.render(infos, True, rouge)
    infos2_s = police.render("IA1: %s (%s) - IA2: %s (%s)" % (IA[0], max_depth[0], IA[1], max_depth[1]), True, rouge)
    screen.fill(blanc, (0, plateau.get_height(), plateau.get_width(), 2*infos_height+margin))
    screen.blit(infos_s, (0, plateau.get_height()))
    screen.blit(infos2_s, (0, plateau.get_height()+infos_height))
    pygame.display.flip()

pygame.mixer.music.load("ressources/Music.ogg")
pygame.mixer.music.set_volume(1.0)
#pygame.mixer.music.play(-1, 0.0)

# Profiling
import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()
# Main loop of the game
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
            if event.key == pygame.K_e:
                explain = not explain
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

    if IA[playing] and not finished():
        infos = "Computing ..."
    elif finished():
        if winner() == 0:
            infos = "It's a tie !"
        else:
            infos = "%s won !" % winner()
        if parties == 10:
            quitter = True
        else:
            resetBoard()
            parties += 1
    else:
        infos = "%s to play" % lettres[playing]
    if not finished():
        infos += additionalInfos
    drawBoard()

    if IA[playing]:
        computerPlays()
pygame.mixer.music.stop()
pygame.quit()
# Profiling
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
