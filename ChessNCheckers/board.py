class Piece(object):

    def __init__(self, name, pos):
        self._name = name
        self._pos = pos

    def draw(self, surface, pos):
        surface.blit(self._surface, pos)

    def name(self):
        return self._name


class Board(object):

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._board = [[None for i in range(self._height)] for j in range(self._width)]
