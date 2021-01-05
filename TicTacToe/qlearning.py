#!/usr/bin/python
# -*- coding: utf8 -*-"

import collections
import itertools
import os
import pickle
import random

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# Because we can't pickle a lambda
def dd_float():
    return collections.defaultdict(float)

# Discount factor
discount_factor = 0.95

# A reward just for going further in the game
playing_reward = 0.05

# Exploration rate base
exploration_base = 100
min_exploration_rate = 0.01

# Learning rate base
learning_base = 100
min_learning_rate = 0.01

# Frequency at which stats are displayed
nb_games_for_stats = 100
# Frequency at which model is saved
nb_games_for_save = 100

epsilon = 1e-10

all_actions = [(x, y) for x, y in itertools.product(range(3), range(3))]


# Returns a string representing the board.
def board_to_state(board):
    return "".join(["%s" % v for line in board.boardState for v in line])

def explorationRate(games):
    #return max(min_exploration_rate, 1.0*exploration_base/(exploration_base+games))
    return min_exploration_rate

def learningRate(games):
    return max(min_learning_rate, 1.0*learning_base/(learning_base+games))
    #return min_learning_rate

def validActions(board):
    return [(x, y) for x, y in all_actions if board.boardState[x][y] == 0]



class QValuesTabular(object):

    FILENAME = "q_learning_tab_%s.pkl"

    def __init__(self, player):
        self.player = player
        self.filename = self.FILENAME % self.player
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.q_values = pickle.load(f)
                print("Loaded %s" % self.filename)
        else:
            self.q_values = collections.defaultdict(dd_float)

    def at_state(self, state):
        return self.q_values[state]

    def at_state_action(self, state, action):
        return self.q_values[state][action]

    def adjust_state_action(self, state, action, target, learning_rate):
        delta = learning_rate * (target - self.q_values[state][action])
        #print("State %s, action %s - Learnt %s - Adding %s to %s => " % (state, action, learnt_value, delta, self.q_values.at_state_action(state, action)), end='')
        self.q_values[state][action] += delta
        #print(self.q_values.at_state_action(state, action))

    def save_model(self):
        # TODO: Save more state than just the values (e.g #games to not reset learning & exploration rates)
        with open(self.filename, 'wb') as f:
            pickle.dump(self.q_values, f)
        print("Saved state to %s" % self.filename)


class QValuesNeuralNet(object):

    FILENAME = "q_learning_nn_%s.dat"

    def __init__(self, player):
        self.player = player
        self.filename = self.FILENAME % self.player
        if os.path.exists(self.filename):
            self.model = keras.models.load_model(self.filename)
            print("Loaded %s" % self.filename)
        else:
            self.model = self.build_model()
        print(self.model.summary())

    def build_model(self):
        model = keras.Sequential([
            # The input is the state: -1 for O, 0 for empty and 1 for X
            layers.Dense(10, activation='relu', input_shape=[9]),
            layers.Dense(10, activation='relu'),
            layers.Dense(10, activation='relu'),
            layers.Dense(10, activation='relu'),
            # The output layer has 9 outputs: one per cell that can be played
            layers.Dense(9),
        ])

        optimizer = keras.optimizers.RMSprop(0.001)

        model.compile(
            loss='mse',
            optimizer=optimizer,
            metrics=['mae', 'mse'])

        return model

    def letter_to_idx(self, letter):
        if letter == 'X':
            return 1.0
        if letter == 'O':
            return -1.0
        return 0.0

    def state_to_input(self, state):
        return [self.letter_to_idx(c) for c in state]

    def action_to_index(self, action):
        return action[0]+action[1]*3

    def predict_at_state(self, state):
        inp = self.state_to_input(state)
        return self.model.predict([inp])[0]

    def at_state(self, state):
        pred = self.predict_at_state(state)
        result = {}
        for i in range(3):
            for j in range(3):
                result[(i,j)] = pred[i+3*j]
        return result

    def at_state_action(self, state, action):
        out = self.state_to_input(state)
        idx = self.action_to_index(action)
        return out[idx]

    def adjust_state_action(self, state, action, target, learning_rate):
        objective = self.predict_at_state(state)
        objective[self.action_to_index(action)] = target
        inp = np.array(self.state_to_input(state)).reshape(1,9)
        out = objective.reshape(1,9)
        self.model.fit(inp, out, epochs=1, verbose=0)

    def save_model(self):
        self.model.save(self.filename)
        print("Saved state to %s" % self.filename)


class QLearningPlayer(object):

    def __init__(self, player, kind='tabular'):
        self.games = 0
        self.player = player
        self.kind = kind
        if kind == 'tabular':
            self.q_values = QValuesTabular(self.player)
        elif kind == 'neuralnet':
            self.q_values = QValuesNeuralNet(self.player)
        else:
            raise ValueError('Unknown kind "%s"' % kind)
        self.history = []
        self.summary = collections.defaultdict(int)

    def name(self):
        return "QLearning"

    def description(self):
        return "%s (%s)" % (self.name(), self.kind)

    def stronger(self):
        pass

    def weaker(self):
        pass

    # Fait jouer l'ordinateur
    def computerPlays(self, board, additionalInfos):
        board_state = board_to_state(board)
        if self.history:
            # Record the resulting state from previous play
            self.history[-1] = (self.history[-1][0], self.history[-1][1], board_state)
        to_play = None
        # If we don't want to explore, play the (supposed) best move
        if random.random() > explorationRate(self.games):
            to_play = self.findBestAction(board_state, validActions(board))
            self.summary['best'] += 1
        # Otherwise play a valid random move
        if not to_play:
            to_play = self.pickRandom2(board)
            self.summary['random'] += 1
        board.boardState[to_play[0]][to_play[1]] = board.lettres[board.playing]
        self.history.append((board_state, to_play, None))

    # Whether the game was won (score = 1), lost (score = -1) or draw (score = 0)
    def outcome(self, score):
        global discount_factor
        self.games += 1
        last_play = True
        if score < 0:
            self.summary['lost'] += 1
        elif score == 0:
            self.summary['draw'] += 1
        else:
            self.summary['won'] += 1
        #for (state, played, next_state) in reversed(self.history):
        # Ideally this should be done just after playing, but this is equivalent
        # and allow to easily compare with the optimized version with the reversed
        for (state, played, next_state) in self.history:
            if last_play:
                learnt_value = score
            else:
                learnt_value = playing_reward
                next_values = list(self.q_values.at_state(next_state).values())
                if next_values:
                    learnt_value += max(next_values)
            self.q_values.adjust_state_action(state, played, learnt_value, learningRate(self.games))
        self.history = []
        if self.games % nb_games_for_stats == 0:
            print("Learning rate = %s - Exploration = %s" % (learningRate(self.games), explorationRate(self.games)))
            print("%s (playing %s) - Games: %s - Random: %s - Best: %s - Won: %s - Lost: %s - Draw: %s" % (self.kind, self.player, self.games, self.summary['random'], self.summary['best'], self.summary['won'], self.summary['lost'], self.summary['draw']))
            self.summary.clear()
        if self.games % nb_games_for_save == 0:
            self.q_values.save_model()

    def findBestAction(self, board_state, valid_actions):
        maxValue = None
        bestAction = None
        for action, value in self.q_values.at_state(board_state).items():
            #print("Action %s at %s has value %s" % (action, board_state, value))
            # Just ignore invalid actions as our NeuralNet can predict anything ...
            if action not in valid_actions:
                #print("Skipping %s at %s - it's not valid" % (action, board_state))
                continue
            if maxValue is None or value > maxValue:
                maxValue = value
                bestAction = action
        #print("Choose to play at %s" % (bestAction,))
        return bestAction

    def findBestAction2(self, board_state, valid_actions):
        actions = []
        values = []
        minV, maxV = None, None
        for action, value in self.q_values[board_state].items():
            # Just ignore invalid actions as our NeuralNet can predict anything ...
            if action not in valid_actions:
                continue
            actions.append(action)
            values.append(value)
            if minV is None or value < minV:
                minV = value
        values = [v - minV + epsilon for v in values]
        #for action, value in zip(actions, values):
        #    print("Action %s at %s has value %s" % (action, board_state, value))
        # Translate values to all be positive, with the min having a probability of
        # epsilon to be taken
        if not actions:
            return None
        #coup = len([x for x in board_state if x != '0'])
        #print("Coup %s: %s ---> %s" % (coup, len(values), values))
        chosen = random.choices(actions, values)[0]
        #print("Choose to play at %s" % (chosen,))
        return chosen

    def pickRandom(self, board):
        return random.choice(validActions(board))

    def pickRandom2(self, board):
        board_state = board_to_state(board)
        # Favors actions that have never been tried from this state
        candidates = [(x, y) for x, y in validActions(board) if (x,y) not in self.q_values.at_state(board_state)]
        if candidates:
            return random.choice(candidates)
        return self.pickRandom(board)

    def pickRandomStupid(self, board):
        while True:
            to_play = (random.randint(0, 2), random.randint(0, 2))
            if board.boardState[to_play[0]][to_play[1]] == 0:
                return to_play
