#!/usr/bin/python
# -*- coding: utf8 -*-"

import itertools
import random

all_actions = [(x, y) for x, y in itertools.product(range(3), range(3))]

def validActions(board):
    return [(x, y) for x, y in all_actions if board.boardState[x][y] == 0]

class RandomPlayer(object):

    def __init__(self, player):
        _ = player

    def name(self):
        return "Random"

    def description(self):
        return "Random"

    def stronger(self):
        pass

    def weaker(self):
        pass

    def computerPlays(self, board, additionalInfos):
        chosen = random.choice(validActions(board))
        board.boardState[chosen[0]][chosen[1]] = board.lettres[board.playing]

    def outcome(self, score):
        pass
