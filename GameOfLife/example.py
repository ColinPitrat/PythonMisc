
class GOLGrid(object):

    def __init__(self, width, height):
        self.map_ = [ [0 for x in range(0, height)] for y in range(0, width) ]

    def set_alive(self, x, y):
        self.map_[x][y] = 1

    def pretty_print(self):
        for line in self.map_:
            print line

    def safe_peek_cell(self, x, y):
        if x < 0:
            x += len(self.map_)
        if  x >= len(self.map_):
            x -= len(self.map_)
        if y >= 0 and y < len(self.map_[x]):
            return self.map_[x][y]
        return 0

    def count_live_neighbors(self, x, y):
        result = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                result += self.safe_peek_cell(x+dx, y+dy)
        result -= self.map_[x][y]
        return result


grid = GOLGrid(10, 10)
grid.set_alive(5, 5)
grid.pretty_print()
print(grid.count_live_neighbors(9, 0))
