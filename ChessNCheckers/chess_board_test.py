import unittest
import chess_board
import chess

class PawnTest(unittest.TestCase):

    def emptyBoard(self):
        board = chess_board.ChessBoard()
        for i in range(8):
            for j in [0, 1, 6, 7]:
                board.remove_piece((i, j))
        return board

    def startBoard(self):
        board = chess_board.ChessBoard()
        return board

    def testValidMoveAtEnd(self):
        board = self.emptyBoard()
        board.add_piece(chess_board.Pawn, 'B', (5, 7))
        pawn = board.at((5, 7))
        self.assertEqual(set(), pawn.valid_moves(board))

    # move_piece Pawn (B) from (1, 7) to (2, 8)
    # |  |  |  |  |  |  |PW|  |
    # -------------------------
    # |KB|  |  |NB|  |  |  |  |
    # -------------------------
    # |  |  |  |  |  |  |  |  |
    # -------------------------
    # |  |  |  |  |  |  |  |  |
    # -------------------------
    # |  |  |  |  |  |  |  |  |
    # -------------------------
    # |KW|  |  |  |  |  |  |  |
    # -------------------------
    # |  |  |  |  |  |  |  |  |
    # -------------------------
    # |  |PB|NW|PB|  |PB|  |  |
    # -------------------------
    def testValidMoveAtEndWith(self):
        board = self.emptyBoard()
        board.add_piece(chess_board.Pawn, 'W', (6, 0))
        board.add_piece(chess_board.King, 'B', (0, 1))
        board.add_piece(chess_board.Knight, 'B', (3, 1))
        board.add_piece(chess_board.King, 'W', (0, 5))
        board.add_piece(chess_board.Pawn, 'B', (1, 7))
        board.add_piece(chess_board.Pawn, 'B', (3, 7))
        board.add_piece(chess_board.Knight, 'W', (4, 7))
        board.add_piece(chess_board.Pawn, 'B', (5, 7))

        pawn = board.at((1, 7))
        self.assertEqual(set(), pawn.valid_moves(board))

    #|  |  |  |  |  |KB|  |  |
    #-------------------------
    #|  |  |  |  |  |  |  |  |
    #-------------------------
    #|  |  |  |  |  |  |  |  |
    #-------------------------
    #|BW|RW|  |  |  |  |  |  |
    #-------------------------
    #|PB|  |  |  |  |  |  |  |
    #-------------------------
    #|PW|  |  |  |  |  |RB|QW|
    #-------------------------
    #|  |  |KW|  |  |  |  |  |
    #-------------------------
    #|  |  |PB|  |  |  |PB|PB|
    #-------------------------
    #move_piece Queen (W) from (7, 5) to (5, 7)
    #Switch turn to B
    #Possible moves: {(5, 8)}
    def testValidMoveAtEndWithNeighbour(self):
        board = self.emptyBoard()
        board.set_player('W', chess.HumanPlayer(board, 'W'))
        board.set_player('B', chess.HumanPlayer(board, 'B'))
        board.add_piece(chess_board.King, 'B', (5, 0))
        board.add_piece(chess_board.Bishop, 'W', (0, 3))
        board.add_piece(chess_board.Rook, 'W', (1, 3))
        board.add_piece(chess_board.Pawn, 'B', (0, 4))
        board.add_piece(chess_board.Pawn, 'W', (0, 5))
        board.add_piece(chess_board.Rook, 'B', (6, 5))
        board.add_piece(chess_board.Queen, 'W', (7, 5))
        board.add_piece(chess_board.King, 'W', (2, 6))
        board.add_piece(chess_board.Pawn, 'B', (2, 7))
        board.add_piece(chess_board.Pawn, 'B', (6, 7))
        board.add_piece(chess_board.Pawn, 'B', (7, 7))

        pawn = board.at((6, 7))
        queen = board.at((7, 5))
        board.move_piece(queen, (5, 7))
        self.assertEqual(set(), pawn.valid_moves(board))

    #-------------------------
    #|RB|  |  |  |KB|  |NB|  |
    #-------------------------
    #|  |BB|  |PB|  |  |  |RB|
    #-------------------------
    #|  |PB|  |  |PB|  |  |  |
    #-------------------------
    #|PB|  |  |  |  |  |  |PB|
    #-------------------------
    #|  |  |  |  |  |  |  |  |
    #-------------------------
    #|NW|PW|  |PW|  |PW|  |  |
    #-------------------------
    #|PW|  |PW|  |PW|  |PW|PW|
    #-------------------------
    #|  |RW|  |QW|KW|BW|NW|RW|
    #-------------------------
    #Failed to really move None to ((3, 0), (1, 2))
    #Traceback (most recent call last):
    #  File "chess.py", line 223, in <module>
    #    main()
    #  File "chess.py", line 195, in main
    #    board._player[board._whose_turn].play()
    #  File "chess.py", line 97, in play
    #    self._board.move_piece(p, move[1])
    #  File "/home/cpitrat/Perso/PythonMisc/ChessNCheckers/chess_board.py", line 325, in move_piece
    #    if piece._name == 'Pawn' and pos[1] != piece.position()[1] and not self.at(pos):
    #AttributeError: 'NoneType' object has no attribute '_name'
    def testFailingMinMax(self):
        board = self.emptyBoard()
        board.set_player('W', chess.MinMaxPlayer(board, 'W', 2))
        board.set_player('B', chess.HumanPlayer(board, 'B'))
        board.add_piece(chess_board.Rook, 'B', (0, 0))
        board.add_piece(chess_board.King, 'B', (4, 0))
        board.add_piece(chess_board.Knight, 'B', (6, 0))
        board.add_piece(chess_board.Bishop, 'B', (1, 1))
        board.add_piece(chess_board.Pawn, 'B', (3, 1))
        board.add_piece(chess_board.Rook, 'B', (7, 1))
        board.add_piece(chess_board.Pawn, 'B', (1, 2))
        board.add_piece(chess_board.Pawn, 'B', (4, 2))
        board.add_piece(chess_board.Pawn, 'B', (0, 3))
        board.add_piece(chess_board.Pawn, 'B', (7, 3))
        board.add_piece(chess_board.Knight, 'W', (0, 5))
        board.add_piece(chess_board.Pawn, 'W', (1, 5))
        board.add_piece(chess_board.Pawn, 'W', (3, 5))
        board.add_piece(chess_board.Pawn, 'W', (5, 5))
        board.add_piece(chess_board.Pawn, 'W', (0, 6))
        board.add_piece(chess_board.Pawn, 'W', (2, 6))
        board.add_piece(chess_board.Pawn, 'W', (4, 6))
        board.add_piece(chess_board.Pawn, 'W', (6, 6))
        board.add_piece(chess_board.Pawn, 'W', (7, 6))
        board.add_piece(chess_board.Rook, 'W', (1, 7))
        board.add_piece(chess_board.Queen, 'W', (3, 7))
        board.add_piece(chess_board.King, 'W', (4, 7))
        board.add_piece(chess_board.Bishop, 'W', (5, 7))
        board.add_piece(chess_board.Knight, 'W', (6, 7))
        board.add_piece(chess_board.Rook, 'W', (7, 7))

        board._player['W'].play()

    # Invalid last move: (5, 1), (3, 0), [], []
    # -------------------------
    # |RB|  |  |  |KB|BB|NB|RB|
    # -------------------------
    # |PB|PB|  |NB|PB|  |  |PB|
    # -------------------------
    # |  |  |  |PB|  |  |  |  |
    # -------------------------
    # |  |  |PB|  |  |PW|  |  |
    # -------------------------
    # |  |  |  |  |  |  |  |  |
    # -------------------------
    # |  |  |  |PW|  |  |  |  |
    # -------------------------
    # |PW|PW|PW|  |PW|PW|  |PW|
    # -------------------------
    # |RW|NW|BW|QW|KW|BW|  |RW|
    # -------------------------
    # (From, To, Taken, Moved)
    # (6, 6), (6, 4), [<chess_board.Pawn object at 0x7f3d0856b1f0>], []
    # (6, 1), (6, 2), [<chess_board.Pawn object at 0x7f3d0856b190>], []
    # (6, 7), (7, 5), [], []
    # (3, 1), (3, 2), [<chess_board.Pawn object at 0x7f3d08577d00>], []
    # (3, 6), (3, 5), [<chess_board.Pawn object at 0x7f3d08577c40>], []
    # (6, 2), (6, 3), [<chess_board.Pawn object at 0x7f3d0856b190>], []
    # (7, 5), (6, 3), [<chess_board.Pawn object at 0x7f3d0856b190>], []
    # (2, 0), (5, 3), [], []
    # (6, 4), (5, 3), [<chess_board.Bishop object at 0x7f3d0856b610>], []
    # (1, 0), (3, 1), [], []
    # (6, 3), (5, 1), [<chess_board.Pawn object at 0x7f3d08577e80>], []
    # (2, 1), (2, 3), [<chess_board.Pawn object at 0x7f3d08577d30>], []
    # Failed to simulate undo: (2, 1), (2, 3), [<chess_board.Pawn object at 0x7f3d08577d30>], []
    # Traceback (most recent call last):
    #   File "chess.py", line 232, in <module>
    #     main()
    #   File "chess.py", line 198, in main
    #     board._player[board._whose_turn].play()
    #   File "chess.py", line 90, in play
    #     _, move = self.simulate(self._color, self._depth)
    #   File "chess.py", line 146, in simulate
    #     self._board.undo_move(simulate=True)
    #   File "/home/cpitrat/Perso/PythonMisc/ChessNCheckers/chess_board.py", line 377, in undo_move
    #     piece.move(last_move.start, -1)
    # AttributeError: 'NoneType' object has no attribute 'move'
    def testFailure(self):
        board = self.startBoard()
        board.set_player('W', chess.MinMaxPlayer(board, 'W', 2))
        board.set_player('B', chess.HumanPlayer(board, 'B'))
        board.move_piece(board.at((6, 6)), (6, 4))
        board.move_piece(board.at((6, 1)), (6, 2))
        board.move_piece(board.at((6, 7)), (7, 5))
        board.move_piece(board.at((3, 1)), (3, 2))
        board.move_piece(board.at((3, 6)), (3, 5))
        board.move_piece(board.at((6, 2)), (6, 3))
        board.move_piece(board.at((7, 5)), (6, 3))
        board.move_piece(board.at((2, 0)), (5, 3))
        board.move_piece(board.at((6, 4)), (5, 3))
        board.move_piece(board.at((1, 0)), (3, 1))
        board.move_piece(board.at((6, 3)), (5, 1))
        board.move_piece(board.at((2, 1)), (2, 3))
        board.move_piece(board.at((5, 1)), (3, 0))
        board.print_board()

        king = board.at((4, 0))
        self.assertNotIn((2, 0), king.possible_moves(board))
        #board._player['W'].play()


if __name__ == '__main__':
    unittest.main()
