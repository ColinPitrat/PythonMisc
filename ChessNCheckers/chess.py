import pygame
import chess_board
import random
import time
import collections

class Player(object):

    def __init__(self, board, color):
        self._board = board
        self._color = color
        board.set_player(color, self)
        self._my_turn = False

    def notify_turn(self):
        self._my_turn = True

    def play(self):
        pass


class HumanPlayer(Player):

    def onclick(self, pos):
        if not self._my_turn:
            return
        # Outside of the board
        # TODO: translation of coordinates should be done by the board
        if pos[0] < 14 or pos[0] > 438 or pos[1] < 14 or pos[1] > 438:
            return
        i = (pos[0] - 14)//53
        j = (pos[1] - 14)//53
        # TODO: Move selected info to the player?
        # TODO: Avoid direct usage of self._board
        if self._board._selected:
            if self._board._selected.position() == (i, j):
                self._board._selected = None
            elif (i, j) in self._board._selected.valid_moves(self._board):
                print("Unselect and switch turn.")
                self._my_turn = False
                self._board.move_piece(self._board._selected, (i, j))
                self._board._selected = None
            else:
                # TODO: play an annoying sound + visual annoyance too
                print("Invalid move")
        else:
            # No piece to select
            if not self._board._board[i][j]:
                return
            if self._board._board[i][j]._color == self._color:
                self._board._selected = self._board._board[i][j]


class RandomPlayer(Player):

    def play(self):
        if not self._my_turn:
            return
        pieces = [p for l in self._board._board for p in l if p and p._color == self._color]
        random.shuffle(pieces)
        for p in pieces:
            moves = list(p.valid_moves(self._board))
            if moves:
                random.shuffle(moves)
                self._board.move_piece(p, moves[0])
                self._my_turn = False
                break

    def onclick(self, pos):
        pass


class MinMaxPlayer(Player):

    def __init__(self, board, color, depth):
        super().__init__(board, color)
        self._depth = depth
        self._value = {
            'P': 1,
            'N': 3,
            'B': 3,
            'R': 5,
            'Q': 9,
            'K': 10000,
        }

    def play(self):
        if not self._my_turn:
            return
        _, move = self.simulate(self._color, self._depth)
        #print("I'll move piece at %s to %s" % (move[0], move[1]))
        p = self._board.at(move[0])
        try:
            self._board.move_piece(p, move[1])
        except:
            self._board.print_board()
            self._board.print_history()
            print("Failed to really move %s to %s" % (p, move))
            raise

    def evaluate(self, color):
        pieces = [p for l in self._board._board for p in l]
        score = {'W': 0, 'B': 0}
        for p in pieces:
            if not p:
                continue
            score[p._color] += self._value[p.letter()]
        opponent = 'W' if color == 'B' else 'B'
        return score[color] - score[opponent]

    def simulate(self, color, depth):
        if depth == 0:
            return [self.evaluate(color), None]
        pieces = [p for l in self._board._board for p in l if p and p._color == color]
        # When multiple move are equivalent, this will do a random one
        random.shuffle(pieces)
        best_score = None
        best_move = None
        for p in pieces:
            from_pos = p._pos
            moves = list(p.valid_moves(self._board))
            random.shuffle(moves)
            for move in moves:
                try:
                    self._board.move_piece(p, move, simulate=True)
                except:
                    self._board.print_board()
                    self._board.print_history()
                    print("Failed to simulate move %s to %s" % (p, move))
                    raise
                opponent = 'W' if color == 'B' else 'B'
                if self._board.checked_mate(self._color):
                    score = -10000
                elif self._board.checked_mate(opponent):
                    score = 10000
                # Stale mate is bad for me as well as for opponent
                elif self._board.stale_mate(self._color) or self._board.stale_mate(opponent):
                    score = -5000
                else:
                    score, _ = self.simulate(opponent, depth-1)
                if not best_score or score > best_score:
                    #print("    " * (self._depth - depth) + "  Good move: from %s to %s (score: %s)" % (from_pos, move, score))
                    best_score = score
                    best_move = (from_pos, move)
                try:
                    self._board.undo_move(simulate=True)
                except:
                    self._board.print_board()
                    self._board.print_history()
                    print("Failed to simulate undo: %s" % (self._board._moves[-1], ))
                    raise
        #print("    " * (self._depth - depth) + "Return move: from %s to %s" % (from_pos, best_move))
        return best_score, best_move

    def onclick(self, pos):
        pass


def init_board():
    board = chess_board.ChessBoard()
    #board.set_player('W', HumanPlayer(board, 'W'))
    #board.set_player('W', MinMaxPlayer(board, 'W', 1))
    board.set_player('W', RandomPlayer(board, 'W'))
    #board.set_player('B', HumanPlayer(board, 'B'))
    #board.set_player('B', MinMaxPlayer(board, 'B', 1))
    board.set_player('B', RandomPlayer(board, 'B'))
    board.start_game()
    return board

def enable_profiling():
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    return pr

def profiling_results(pr):
    import pstats
    from io import StringIO
    pr.disable()
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

def main():
    #pr = enable_profiling()
    width, height = 451, 451
    screen = pygame.display.set_mode((width, height))
    exit = False
    paused = False
    board = init_board()
    points = { 'B': 0, 'W': 0}
    results = collections.defaultdict(int)
    while not exit:
        board.assert_consistent()
        board.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit = True
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit = True
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r:
                    board = init_board()
                    paused = False
                if event.key == pygame.K_u:
                    board.undo_move()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board._player[board._whose_turn].onclick(event.pos)
        if not paused:
            board._player[board._whose_turn].play()
            # TODO: Display/sound when checked / checked-mate
            for color in ['W', 'B']:
                opponent = 'W' if color == 'B' else 'B'
                if board.checked_mate(color):
                    print("Checked-mate %s" % color)
                    points[opponent] += 1
                    results['Checked-mate %s' % color] += 1
                    board = init_board()
                    #paused = True
                elif board.stale_mate(color):
                    print("Stale-mate %s" % color)
                    points[color] += .5
                    points[opponent] += .5
                    results['Stale-mate %s' % color] += 1
                    board = init_board()
                    #paused = True
                elif board._last_capture_or_pawn >= 100:
                    print("Auto-invoke 50 move rule")
                    points[color] += .5
                    points[opponent] += .5
                    results['50 moves %s' % color] += 1
                    board = init_board()
                elif board.checked(color):
                    print("Checked %s" % color)
    print("Total: ", sum(results.values()))
    print("Score:")
    for color, score in points.items():
        print(" %s: %s" % (color, score))
    print("")
    for ending, nb in results.items():
        print(" %s: %s" % (ending, nb))
    pygame.quit()
    #profiling_results(pr)

if __name__ == '__main__':
    main()
