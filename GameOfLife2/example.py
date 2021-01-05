import numpy
import itertools
import sys
import time

class GOL:

    def __init__(self, width, height):
        self.width_ = width
        self.height_ = height
        self.map_ = numpy.zeros((height, width))

    def set_alive(self, x, y):
        self.map_[y][x] = 1

    def randomize(self):
        self.map_ = numpy.round(numpy.random.rand(self.height_, self.width_)).astype(int)

    def peek_status(self, x, y):
        return  self.map_[y%self.height_][x%self.width_]

    def sum_cells_around(self, result, x, y):
        for (dx, dy) in itertools.product([-1, 0, 1], [-1, 0, 1]):
            result += self.peek_status(x+dx, y+dy)
        return result

    def nb_neighbors(self, x, y):
        return self.sum_cells_around(0, x, y) - self.peek_status(x, y)

    def next_status(self, status, nb_neighbors):
        NEXT_STATUS = [0, 0, status, 1, 0, 0, 0, 0, 0, 0]
        return NEXT_STATUS[int(nb_neighbors)]

    def internal_next_generation(self, map_copy):
        for (x, y) in itertools.product(range(0, self.width_), range(0, self.height_)):
            map_copy[y][x] = self.next_status(self.map_[y][x], self.nb_neighbors(x, y))

    def next_generation(self):
        map_copy = self.map_.copy()
        self.internal_next_generation(map_copy)
        self.map_ = map_copy

    def print_line(self, y):
        CELL_REP = [ ' ', 'X' ]
        for x in range(0, self.width_):
            sys.stdout.write(CELL_REP[int(self.map_[y][x])])

    def pretty_print(self):
        for y in range(0, self.height_):
            self.print_line(y)
            sys.stdout.write('\n')

if False:
    g = GOL(120, 100)
    g.randomize()
    for i in range(0, 100):
        g.pretty_print()
        g.next_generation()
        time.sleep(0.1)
else:
    g2 = GOL(19, 26)
    for x in range(8, 11):
      for y in range(9, 17):
        if x == 9 and (y == 10 or y == 15):
            continue
        g2.set_alive(x, y)
    for i in range(0, 100):
        g2.pretty_print()
        g2.next_generation()
        print(" ===== ")
        time.sleep(0.1)
