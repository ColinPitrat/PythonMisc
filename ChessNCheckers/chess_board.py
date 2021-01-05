import board
import math
import os
import pygame


class Move(object):

    def __init__(self, start, end, taken, moved):
        self.start = start
        self.end = end
        self.taken = taken
        self.moved = moved

    def __str__(self):
        return "%s, %s, %s, %s" % (self.start, self.end, self.taken, self.moved)

    def __repr__(self):
        return "%s, %s, %s, %s" % (self.start, self.end, self.taken, self.moved)


class ChessPiece(board.Piece):

    def __init__(self, style_path, name, color, pos):
        super().__init__(name, pos)
        self._color = color
        self._surface = pygame.image.load(os.path.join(style_path, '%s%s.png' % (name.lower(), color)))
        self._moved = 0

    def attacking(self, board):
        return self.possible_moves(board)

    def valid_moves(self, board):
        result = self.possible_moves(board)
        #print("Possible moves: %s" % result)
        # Remove positions where the king would be taken
        to_remove = set()
        for pos in result:
            board.move_piece(self, pos, simulate=True)
            if board.checked(self._color):
                to_remove.add(pos)
            board.undo_move(simulate=True)
        return result.difference(to_remove)

    def move(self, pos, count=1):
        self._moved += count
        self._pos = pos

    def position(self):
        return self._pos


class Bishop(ChessPiece):

    def __init__(self, style_path, color, pos):
        super().__init__(style_path, 'Bishop', color, pos)

    def letter(self):
        return 'B'

    def possible_moves(self, board):
        result = set()
        pos = self._pos
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        blocked = [False] * 4
        for dist in range(1, 8):
            for i, direc in enumerate(directions):
                if blocked[i]:
                    continue
                occupier = board.at((pos[0]+dist*direc[0], pos[1]+dist*direc[1]), invalid=True)
                if occupier:
                    blocked[i] = True
                    if occupier != True and occupier._color != self._color:
                        result.add((pos[0]+dist*direc[0], pos[1]+dist*direc[1]))
                else:
                    result.add((pos[0]+dist*direc[0], pos[1]+dist*direc[1]))
        return result


class King(ChessPiece):

    def __init__(self, style_path, color, pos):
        super().__init__(style_path, 'King', color, pos)

    def letter(self):
        return 'K'

    def attacking(self, board):
        # Do not include castling to not recurse
        return self.possible_moves(board, include_castling=False)

    def possible_moves(self, board, include_castling=True):
        result = set()
        pos = self._pos
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                dest = board.at((pos[0]+dx, pos[1]+dy), invalid=True)
                if not dest or (dest != True and dest._color != self._color):
                    result.add((pos[0]+dx, pos[1]+dy))
        # Castling:
        # - King & Rook must not have moved
        if self._moved or not include_castling:
            return result
        r1 = board.at((0, pos[1]))
        r2 = board.at((7, pos[1]))
        for r in [r1, r2]:
            if not r:
                continue
            if r._moved:
                continue
            # - No piece between King & Rook
            blocked = False
            for i in (list(range(r._pos[0]+1, self._pos[0])) +
                    list(range(self._pos[0]+1, r._pos[0]))):
                if board.at((i, pos[1])):
                    blocked = True
                    break
            if blocked:
                continue
            # - King not in check and not passing through or landing on attacked square
            direction = int(math.copysign(1, r._pos[0]-self._pos[0]))
            attacked = False
            opponent = 'W' if self._color == 'B' else 'B'
            attacked_squares = board.attacked(opponent)
            for dx in (0, 1, 2):
                if (pos[0] + dx*direction, pos[1]) in attacked_squares:
                    attacked = True
            if attacked:
                continue
            result.add((pos[0]+2*direction, pos[1]))
        return result


class Knight(ChessPiece):

    def __init__(self, style_path, color, pos):
        super().__init__(style_path, 'Knight', color, pos)

    def letter(self):
        return 'N'

    def possible_moves(self, board):
        result = set()
        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:
                if dx == dy or dx == -dy:
                    continue
                pos = self._pos
                occupier = board.at((pos[0]+dx, pos[1]+dy), invalid=True)
                if not occupier or (occupier != True and occupier._color != self._color):
                    result.add((pos[0]+dx, pos[1]+dy))
        return result


class Pawn(ChessPiece):

    def __init__(self, style_path, color, pos):
        super().__init__(style_path, 'Pawn', color, pos)

    def letter(self):
        return 'P'

    def attacking(self, board):
        direction = 1 if self._color == 'B' else -1
        result = set()
        pos = self._pos
        for dx in [-1, +1]:
            if board.at((pos[0]+dx, pos[1]+direction), invalid=True) == True:
                continue
            result.add((pos[0]+dx, pos[1]+direction))
        return result

    def possible_moves(self, board):
        direction = 1 if self._color == 'B' else -1
        result = set()
        pos = self._pos
        # Moving
        if not board.at((pos[0], pos[1]+direction), invalid=True):
            result.add((pos[0], pos[1]+direction))
            # Moving (first move of the pawn)
            if (((self._color == 'W' and pos[1] == 6) or
                 (self._color == 'B' and pos[1] == 1)) and
                 not board.at((pos[0], pos[1]+2*direction), invalid=True)):
                result.add((pos[0], pos[1]+2*direction))
        # Taking
        for dx in [-1, +1]:
            diag = board.at((pos[0]+dx, pos[1]+direction))
            lat = board.at((pos[0]+dx, pos[1]))
            if diag and diag._color != self._color:
                # Standard taking
                result.add((pos[0]+dx, pos[1]+direction))
            elif (lat and lat._color != self._color and lat._name == 'Pawn' and
                  board._moves[-1].end == lat._pos and
                  board._moves[-1].start[1] - lat._pos[1] in [-2, 2]):
                # Taking "en-passant"
                result.add((pos[0]+dx, pos[1]+direction))
        return result


class Queen(ChessPiece):

    def __init__(self, style_path, color, pos):
        super().__init__(style_path, 'Queen', color, pos)

    def letter(self):
        return 'Q'

    def possible_moves(self, board):
        result = set()
        pos = self._pos
        directions = [(1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]
        blocked = [False] * 8
        for dist in range(1, 8):
            for i, direc in enumerate(directions):
                if blocked[i]:
                    continue
                occupier = board.at((pos[0]+dist*direc[0], pos[1]+dist*direc[1]), invalid=True)
                if occupier:
                    blocked[i] = True
                    if occupier != True and occupier._color != self._color:
                        result.add((pos[0]+dist*direc[0], pos[1]+dist*direc[1]))
                else:
                    result.add((pos[0]+dist*direc[0], pos[1]+dist*direc[1]))
        return result


class Rook(ChessPiece):

    def __init__(self, style_path, color, pos):
        super().__init__(style_path, 'Rook', color, pos)

    def letter(self):
        return 'R'

    def possible_moves(self, board):
        result = set()
        pos = self._pos
        directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
        blocked = [False] * 8
        for dist in range(1, 8):
            for i, direc in enumerate(directions):
                if blocked[i]:
                    continue
                occupier = board.at((pos[0]+dist*direc[0], pos[1]+dist*direc[1]), invalid=True)
                if occupier:
                    blocked[i] = True
                    if occupier != True and occupier._color != self._color:
                        result.add((pos[0]+dist*direc[0], pos[1]+dist*direc[1]))
                else:
                    result.add((pos[0]+dist*direc[0], pos[1]+dist*direc[1]))
        return result


class ChessBoard(board.Board):

    def __init__(self):
        super().__init__(8, 8)
        current_path = os.path.dirname(__file__)
        resources_path = os.path.join(current_path, 'resources')
        # TODO: Allow to configure the pieces to use
        self._style_path = os.path.join(resources_path, 'simple')
        for i in range(8):
            self.add_piece(Pawn, 'B', (i, 1))
            self.add_piece(Pawn, 'W', (i, 6))
        for (i, c) in [(0, 'B'), (7, 'W')]:
            self.add_piece(Rook, c, (0, i))
            self.add_piece(Rook, c, (7, i))
            self.add_piece(Knight, c, (1, i))
            self.add_piece(Knight, c, (6, i))
            self.add_piece(Bishop, c, (2, i))
            self.add_piece(Bishop, c, (5, i))
            self.add_piece(Queen, c, (3, i))
            self.add_piece(King, c, (4, i))
        self._selected = None
        self._moves = []
        self._board_surface = pygame.image.load(os.path.join(resources_path, 'board.png'))
        self._square_surface = {}
        for c in ['B', 'W']:
            self._square_surface[c] = pygame.image.load(os.path.join(self._style_path, 'square%s.png' % c))
        self._whose_turn = 'W'
        self._player = {}
        # For fifty move rules (https://en.wikipedia.org/wiki/Fifty-move_rule)
        self._last_capture_or_pawn = 0

    def assert_consistent(self):
        for i in range(self._width):
            for j in range(self._height):
                piece = self._board[i][j]
                if piece:
                    assert piece.position() == (i, j), "%s at (%s, %s) thinks it's at %s" % (piece._name, i, j, piece.position())
        for m in self._moves:
            assert m.start, "Found move with no start position: %s" % '\n'.join(['%s' % x for x in self._moves])
            assert m.end, "Found move with no end position: %s" % '\n'.join(['%s' % x for x in self._moves])

    def set_player(self, color, player):
        self._player[color] = player

    def start_game(self):
        # next_turn will switch _whose_turn
        self._whose_turn = 'B'
        self.next_turn()

    def next_turn(self, simulate=False):
        self._whose_turn = 'B' if self._whose_turn == 'W' else 'W'
        if not simulate:
            #print("Switch turn to %s" % self._whose_turn)
            self._player[self._whose_turn].notify_turn()

    def add_piece(self, kind, color, pos):
        assert self.at(pos, invalid=True) == None, "Trying to add a piece at (%s, %s) which is not free" % pos
        self._board[pos[0]][pos[1]] = kind(self._style_path, color, pos)

    def remove_piece(self, pos):
        assert self.at(pos) != None, "Trying to remove a piece from (%s, %s) where there's none." % pos
        self._board[pos[0]][pos[1]] = None

    def print_board(self):
        print("-" + "---"*8)
        for i in range(8):
            print("|", end="")
            for j in range(8):
                p = self.at((j, i))
                if p:
                    print("%s%s" % (p.letter(), p._color), end="")
                else:
                    print("  ", end="")
                print("|", end="")
            print("")
            print("-" + "---"*8)

    def print_history(self):
        print("(From, To, Taken, Moved)")
        [print(move) for move in self._moves]

    def move_piece(self, piece, pos, simulate=False):
        # Note: we assume the move is valid.
        if not simulate:
            self._last_capture_or_pawn += 1
        #    self.print_board()
        #    print("move_piece %s (%s) from %s to %s" % (piece._name, piece._color, piece._pos, pos))
        taken = []
        if self._board[pos[0]][pos[1]]:
            taken.append(self._board[pos[0]][pos[1]])
        # Taking "en passant" for a pawn moving diagonally
        if piece._name == 'Pawn' and pos[1] != piece.position()[1] and not self.at(pos):
            taken.append(self._board[pos[0]][piece.position()[1]])
            self._board[pos[0]][piece.position()[1]] = 0
        # Castling
        moved = []
        if piece._name == 'King' and abs(pos[0] - piece.position()[0]) == 2:
            direction = int(math.copysign(1, pos[0] - piece.position()[0]))
            x = 7 if direction == 1 else 0
            r = self._board[x][piece.position()[1]]
            self._board[r.position()[0]][r.position()[1]] = None
            self._board[pos[0]-direction][pos[1]] = r
            moved.append((r.position(), (pos[0]-direction, pos[1])))
            r.move((pos[0]-direction, pos[1]))
        # TODO: promotions
        self._moves.append(Move(piece.position(), pos, taken, moved))
        self._board[piece.position()[0]][piece.position()[1]] = None
        self._board[pos[0]][pos[1]] = piece
        piece.move(pos)
        if piece._name == 'Pawn' or taken:
            self._last_capture_or_pawn = 0
        self.next_turn(simulate)

    def undo_move(self, simulate=False):
        if not self._moves:
            return
        # TODO: undo promotions
        last_move = self._moves.pop()
        piece = self._board[last_move.end[0]][last_move.end[1]]
        if not piece:
            print("Invalid last move: %s" % (last_move,))
        piece.move(last_move.start, -1)
        self._board[last_move.start[0]][last_move.start[1]] = piece
        self._board[last_move.end[0]][last_move.end[1]] = None
        # Undo taking
        for taken in last_move.taken:
            self._board[taken.position()[0]][taken.position()[1]] = taken
        # Undo side moves (Castling)
        for moved in last_move.moved:
            moved_piece = self._board[moved[1][0]][moved[1][1]]
            moved_piece.move(moved[0], -1)
            self._board[moved[0][0]][moved[0][1]] = moved_piece
            self._board[moved[1][0]][moved[1][1]] = None
        self.next_turn(simulate)

    def attacked(self, color):
        """Returns all the squares attacked by a piece of color 'color'."""
        result = set()
        for i in range(self._width):
            for j in range(self._height):
                pos = (i,j)
                if self.at(pos) and self.at(pos)._color == color:
                    result.update(self.at(pos).attacking(self))
        return set(result)

    def checked(self, color):
        opponent = 'W' if color == 'B' else 'B'
        king = None
        # TODO: Index pieces by color & name
        for i in range(self._width):
            for j in range(self._height):
                piece = self.at((i, j))
                if piece and piece._color == color and piece.name() == 'King':
                    king = piece
                    break
            if king:
                break
        assert king, "Couldn't find %s King" % color
        return king.position() in self.attacked(opponent)

    def mate(self, color):
        for i in range(self._width):
            for j in range(self._height):
                piece = self._board[i][j]
                if piece and piece._color == color and piece.valid_moves(self):
                        return False
        return True

    def stale_mate(self, color):
        if self.checked(color):
            return False
        return self.mate(color)

    def checked_mate(self, color):
        if not self.checked(color):
            return False
        return self.mate(color)

    def at(self, pos, invalid=None):
        if pos[0] < 0 or pos[0] >= self._width:
            return invalid
        if pos[1] < 0 or pos[1] >= self._height:
            return invalid
        return self._board[pos[0]][pos[1]]

    def draw(self, surface):
        surface.blit(self._board_surface, (0, 0))
        col = ['W', 'B']
        idx = 0
        for i in range(self._width):
            for j in range(self._height):
                surface.blit(self._square_surface[col[idx%2]], (53*i+14, 53*j+14))
                idx += 1
                if self._selected and self._selected.position() == (i, j):
                    pygame.draw.rect(surface, (255, 0, 0), (53*i+14, 53*j+14, 53, 53), 1)
                if self._board[i][j]:
                    self._board[i][j].draw(surface, (53*i+14, 53*j+14))
            idx += 1
        if self._selected:
            for pos in self._selected.valid_moves(self):
                pygame.draw.circle(surface, (0, 0, 255), (53*pos[0]+14+26, 53*pos[1]+14+26), 5)
        for pos in self.attacked('W'):
            pygame.draw.circle(surface, (0, 200, 0), (53*pos[0]+14+43, 53*pos[1]+14+43), 5)
        for pos in self.attacked('B'):
            pygame.draw.circle(surface, (200, 0, 0), (53*pos[0]+14+10, 53*pos[1]+14+43), 5)
