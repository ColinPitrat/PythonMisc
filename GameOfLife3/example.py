import itertools

class GameOfLife:
  def __init__(self, rows, cols):
    self.area = [0]*rows*cols
    self.cols = cols
    self.rows = rows

  def idx(self, x, y):
    return self.rows * (x%self.cols) + (y%self.rows)

  def get(self, x, y):
    return self.area[self.idx(x, y)]

  def setAlive(self, x, y):
    self.area[self.idx(x,y)] = 1

  def countN(self, x, y):
    result = 0
    for (dx, dy) in itertools.product([-1, 0, 1], [-1, 0, 1]):
        result += self.area[self.idx(x+dx,y+dy)]
    return result - self.area[self.idx(x, y)]

  def willLive(self, x, y):
    count = self.countN(x, y)
    isAlive = self.get(x, y)
    return (isAlive and count > 1 and count < 4) or (not isAlive and count == 3)
