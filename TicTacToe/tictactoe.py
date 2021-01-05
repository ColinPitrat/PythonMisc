#!/usr/bin/python2
import sys, pygame, random, time
import collections
import minimax
import qlearning
import random_total
pygame.init()

##############
# Constantes #
##############
board_size = 300
x_border = 50
y_border = 10
square_size = board_size // 3

infos_height = 20
infos_lines = 3
margin = 5

screen = pygame.display.set_mode([board_size+2*x_border, board_size+infos_lines*infos_height+margin+2*y_border])
pygame.display.set_caption("Tic-tac-toe")

blanc = 255, 255, 255
rouge = 255, 0, 0
bleu = 0, 0, 255
noir = 0, 0, 0

#############
# Variables #
#############
quitter = False
autoRestart = True
wait = False
parties = 0
infos = ""
additionalInfos = ""

# True pour que l'ordinateur joue ce joueur
IA = [qlearning.QLearningPlayer('X', 'neuralnet'), qlearning.QLearningPlayer('O', 'neuralnet')]
#IA = [qlearning.QLearningPlayer('X', 'neuralnet'), random_total.RandomPlayer('O')]
#IA = [random_total.RandomPlayer('X'), qlearning.QLearningPlayer('O', 'neuralnet')]
#IA = [random_total.RandomPlayer('X'), random_total.RandomPlayer('O')]
scores = [ 0, 0 ]
r_0_3 = range(0, 3)
r_0_2 = range(0, 2)

class Board(object):

    def __init__(self):
        self.lettres = [ 'X', 'O' ]
        self.boardState = [ [ 0, 0, 0 ], [ 0, 0, 0], [0, 0, 0] ]
        self.playing = 0

    def empty(self):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.boardState[i][j] != 0:
                    return False
        return True

    def winner(self):
        for i in r_0_3:
            # Verifie les lignes
            lineElt = self.boardState[i][0]
            if lineElt == self.boardState[i][1] and lineElt == self.boardState[i][2] and lineElt != 0:
                return lineElt
            # Verifie les colonnes
            lineElt = self.boardState[0][i]
            if lineElt == self.boardState[1][i] and lineElt == self.boardState[2][i] and lineElt != 0:
                return lineElt
        # Verifie les diagonales
        lineElt = self.boardState[0][0]
        if lineElt == self.boardState[1][1] and lineElt == self.boardState[2][2] and lineElt != 0:
            return lineElt
        lineElt = self.boardState[0][2]
        if lineElt == self.boardState[1][1] and lineElt == self.boardState[2][0] and lineElt != 0:
            return lineElt
        return 0

    def finished(self):
        if board.winner() != 0:
            return True
        for i in range(0, 3):
            for j in range(0, 3):
                if self.boardState[i][j] == 0:
                    return False
        return True

    def __str__(self):
        for i in range(0, 3):
            print("-------------")
            for j in range(0, 3):
                b = self.boardState[i][j]
                if b == 0:
                    b = '.'
                print("| %s" % b),
            print("|")
            #print("| %s | %s | %s" % (self.boardState[i][0], self.boardState[i][1], self.boardState[i][2]))
        print("-------------")
        print("")

    def __repr__(self):
        return self.__str__()

    # Retourne True si le plateau est symetrique par rapport a l'axe vertical central
    def symV(self):
        if self.boardState[0][0] != self.boardState[0][2]:
            return False
        if self.boardState[1][0] != self.boardState[1][2]:
            return False
        if self.boardState[2][0] != self.boardState[2][2]:
            return False
        return True

    # Retourne True si le plateau est symetrique par rapport a l'axe horizontal central
    def symH(self):
        if self.boardState[0][0] != self.boardState[2][0]:
            return False
        if self.boardState[0][1] != self.boardState[2][1]:
            return False
        if self.boardState[0][2] != self.boardState[2][2]:
            return False
        return True

    # Retourne True si le plateau est symetrique par rapport a l'axe diagonal descendant
    def symD1(self):
        if self.boardState[0][1] != self.boardState[1][0]:
            return False
        if self.boardState[0][2] != self.boardState[2][0]:
            return False
        if self.boardState[1][2] != self.boardState[2][1]:
            return False
        return True

    # Retourne True si le plateau est symetrique par rapport a l'axe diagonal montant
    def symD2(self):
        if self.boardState[0][1] != self.boardState[1][2]:
            return False
        if self.boardState[0][0] != self.boardState[2][2]:
            return False
        if self.boardState[1][0] != self.boardState[2][1]:
            return False
        return True

    def otherPlayer(self, player):
        return (player + 1) % 2

    # Verifie si il y a un gagnant et met a jour le score
    def checkWinner(self):
        global parties
        if self.finished():
            w = self.winner()
            if self.lettres[0] == w:
                scores[0] += 1
            elif self.lettres[1] == w:
                scores[1] += 1
            parties += 1


board = Board()

#errorSound = pygame.mixer.Sound("ressources/Error.ogg")
police = pygame.font.SysFont("arial", infos_height);

def resetBoard():
    global additionalInfos, board
    board = Board()
    additionalInfos = ""
    drawBoard()

# Gere le clic de souris
def mouse_clicked(x, y):
    global board
    if board.finished() or IA[board.playing]:
        #errorSound.play()
        return
    x_min = margin + x_border
    y_min = margin + y_border
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
    if board.boardState[row][col] == 0:
        board.boardState[row][col] = board.lettres[board.playing]
    else:
        #errorSound.play()
        return
    board.playing = board.otherPlayer(board.playing)
    board.checkWinner()

# Gere l'affichage
def drawBoard():
    screen.fill(blanc)
    for i in range(0, 4):
        pygame.draw.line(screen, noir, (x_border, i*square_size + y_border), (board_size + x_border, i*square_size + y_border))
    for i in range(0, 4):
        pygame.draw.line(screen, noir, (i*square_size + x_border, y_border), (i*square_size + x_border, board_size + y_border))
    for i in range(0, 3):
        for j in range(0,3):
            if board.boardState[i][j] == 'X':
                pygame.draw.rect(screen, bleu, pygame.Rect(j*square_size + 2*margin + x_border, i*square_size + 2*margin + y_border, square_size-4*margin, square_size-4*margin))
            elif board.boardState[i][j] == 'O':
                pygame.draw.circle(screen, rouge, (j*square_size + square_size//2 + x_border, i*square_size + square_size//2 + y_border), square_size//2 - 2*margin)
    J1 = "Humain"
    J2 = "Humain"
    if IA[0]:
            J1 = "IA %s" % IA[0].description()
    if IA[1]:
            J2 = "IA %s" % IA[1].description()
    infos_s = police.render(infos, True, rouge)
    infos2_s = police.render("Joueur 1: %s/%s (%s)" % (scores[0], parties, J1), True, bleu)
    infos3_s = police.render("Joueur 2: %s/%s (%s)" % (scores[1], parties, J2), True, rouge)
    screen.blit(infos_s, (0, board_size + 2*y_border))
    screen.blit(infos2_s, (0, board_size + 2*y_border + infos_height))
    screen.blit(infos3_s, (0, board_size + 2*y_border + 2*infos_height))
    pygame.display.flip()

stats = []
games = 0
# Boucle principale du jeu
while not quitter:
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
            if event.key == pygame.K_w:
                wait = not wait
            if event.key == pygame.K_F1:
                if IA[0] is None:
                    IA[0] = minimax.MinimaxPlayer('X')
                elif IA[0].name()[:7] == 'Minimax':
                    IA[0] = qlearning.QLearningPlayer('X', 'neuralnet')
                elif IA[0].name() == 'QLearning':
                    IA[0] = random_total.RandomPlayer('X')
                elif IA[0].name() == 'Random':
                    IA[0] = None
                additionalInfos = ""
            if event.key == pygame.K_F2:
                if IA[1] is None:
                    IA[1] = minimax.MinimaxPlayer('O')
                elif IA[1].name() == 'Minimax':
                    IA[1] = qlearning.QLearningPlayer('O', 'neuralnet')
                elif IA[1].name() == 'QLearning':
                    IA[1] = random_total.RandomPlayer('O')
                elif IA[1].name() == 'Random':
                    IA[1] = None
                additionalInfos = ""
            if event.key == pygame.K_u and IA[0]:
                if (event.mod & pygame.KMOD_SHIFT) or (event.mod & pygame.KMOD_LSHIFT) or (event.mod & pygame.KMOD_RSHIFT):
                    IA[0].stronger()
                else:
                    IA[0].weaker()
            if event.key == pygame.K_d and IA[1]:
                if (event.mod & pygame.KMOD_SHIFT) or (event.mod & pygame.KMOD_LSHIFT) or (event.mod & pygame.KMOD_RSHIFT):
                    IA[1].stronger()
                else:
                    IA[1].weaker()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked(event.pos[0], event.pos[1])

    f = board.finished()
    if IA[board.playing] and not f:
        infos = "Calcule ..."
        IA[board.playing].computerPlays(board, additionalInfos)
        board.playing = board.otherPlayer(board.playing)
        board.checkWinner()
    elif f:
        w = board.winner()
        if w == 0:
            score = 0.0
        elif w == board.playing:
            score = 1.0
        else:
            score = -1.0
        if IA[board.playing]:
            IA[board.playing].outcome(score)
        if IA[board.otherPlayer(board.playing)]:
            IA[board.otherPlayer(board.playing)].outcome(-score)
        if w == 0:
            infos = "Match nul !"
        else:
            infos = "%s gagne !" % w
    else:
        infos = "%s joue" % board.lettres[board.playing]
    if not f:
        infos += additionalInfos

    drawBoard()

    if f and autoRestart:
        if wait:
            time.sleep(0.5)
        if games % 100 == 0:
            if games:
                print("X won: %s - O won: %s - Draw: %s" % (stats[-1]['X'], stats[-1]['O'], stats[-1][0]))
            stats.append(collections.defaultdict(int))
            stats[-1]['Games'] = games
        games += 1
        stats[-1][board.winner()] += 1
        resetBoard()
    if games >= 10000:
        break

with open('data.csv', 'w') as f:
    f.write("Games,X,O,Draw\n")
    for stat in stats:
        f.write(",".join([str(stat[k]) for k in ['Games', 'X', 'O', 0]]))
        f.write("\n")

pygame.quit()
