#!/usr/bin/python
# -*- coding: utf8 -*-"

import random

r_0_3 = range(0, 3)
r_0_2 = range(0, 2)

class MinimaxPlayer(object):

    def __init__(self, player):
        _ = player
        self.max_depth = 9

    def name(self):
        return "Minimax"

    def description(self):
        return "Minimax (%s)" % self.max_depth

    def stronger(self):
        if self.max_depth < 9:
            self.max_depth += 1

    def weaker(self):
        if self.max_depth > 1:
            self.max_depth -= 1

    # Retourne le meilleur coup a jouer pour le joueur toPlay a la profondeur "depth", le coup que l'on explore etant celui du joueur "player"
    def placeBest(self, board, player, toPlay, depth):
        if depth < 0:
            print("Depth: %s" % depth)
            print(board)
        bestMoves = [-3, [(-1, -1)]]
        worstMoves = [3, [(-1, -1)]]
        w = board.winner()
        if w != 0:
            # Renvoi un score dont le signe indique le vainqueur.
            # Moins il faut de coups pour gagner, meilleur est le score pour le gagnant.
            # Il faut 9 coups au maximum pour terminer la partie donc le score est
            # entre 1.1 et 2 (en valeur absolue).
            if w == board.lettres[player]:
                return ( 2-0.1*depth, [(-1, -1)])
            else:
                return (-2+0.1*depth, [(-1, -1)])
        rgi = r_0_3
        rgj = r_0_3
        if board.symH():
            rgi = r_0_2
        if board.symV():
            rgj = r_0_2
        sD1 = board.symD1()
        sD2 = board.symD2()
        if depth <= self.max_depth:
            for i in rgi:
                for j in rgj:
                    if sD1 and j < i:
                        continue
                    if sD2 and 2-j < i:
                        continue
                    if board.boardState[i][j] == 0:
                        board.boardState[i][j] = board.lettres[toPlay]
                        result = self.placeBest(board, player, board.otherPlayer(toPlay), depth+1)
                        if result[0] > bestMoves[0]:
                            bestMoves = [result[0], [(i, j)]]
                        elif result[0] == bestMoves[0]:
                            bestMoves[1].append((i, j))
                        if result[0] < worstMoves[0]:
                            worstMoves = [result[0], [(i, j)]]
                        elif result[0] == worstMoves[0]:
                            worstMoves[1].append((i, j))
                        board.boardState[i][j] = 0
        if bestMoves[0] == -3 and worstMoves[0] == 3:
            # N'a pas aboutit a un gagnant ou un perdant: match nul ou issue incertaine
            return (0, [(-1, -1)])
        if player == toPlay:
            return bestMoves
        else:
            return worstMoves

    # Fait jouer l'ordinateur
    def computerPlays(self, board, additionalInfos):
        # C'est ce que le programme joue de toute facon pour le premier coup mais sans le hard-coder, il met plusieurs secondes pour le faire !
        if board.empty():
            x = random.choice([0, 2])
            y = random.choice([0, 2])
            board.boardState[x][y] = board.lettres[board.playing]
            additionalInfos = " - Devrait finir en nul"
        else:
            (s, moves) = self.placeBest(board, board.playing, board.playing, 0)
            if s >= 1:
                additionalInfos = " - %s devrait gagner" % board.lettres[board.playing]
            elif s <= -1:
                additionalInfos = " - %s devrait gagner" % board.lettres[board.otherPlayer(board.playing)]
            else:
                additionalInfos = " - Devrait finir en nul"
            (i, j) = random.choice(moves)
            board.boardState[i][j] = board.lettres[board.playing]

    def outcome(self, score):
            pass
