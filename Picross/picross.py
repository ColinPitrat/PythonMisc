#!/usr/bin/python
# -*- coding: utf8 -*-"

import copy
from enum import Enum

CELL_UNKNOWN = "??"
CELL_EMPTY = "⬜"
CELL_FULL = "⬛"

class Cell(Enum):
  UNKNOWN = 1
  EMPTY = 2
  FULL = 3

  def __str__(self):
    if self == Cell.UNKNOWN:
      return CELL_UNKNOWN
    elif self == Cell.EMPTY:
      return CELL_EMPTY
    elif self == Cell.FULL:
      return CELL_FULL
    else:
      raise ValueError("Unexpected cell value: %s" % c)


def line_str(row):
  return "".join([str(c) for c in row])

def _faster_options(content, size):
  needed = sum(content) + len([x for x in content if x != 0]) - 1
  if needed > size:
    return []
  pattern = []
  for c in content:
    pattern += [Cell.FULL] * c + [Cell.EMPTY]
  pattern = pattern[:-1]
  to_fill = size-len(pattern)
  result = []
  for i in range(to_fill+1):
    result.append([Cell.EMPTY]*i + pattern + [Cell.EMPTY]*(to_fill-i))
  return result

def options(content, size, current, full=False):
  if not full and all([x == Cell.UNKNOWN for x in current]):
    return _faster_options(content, size)
  needed = sum(content) + len([x for x in content if x != 0]) - 1
  result = []
  if needed <= 0:
    if any([x == Cell.FULL for x in current]):
      return []
    return [[Cell.EMPTY] * size]
  shift = 0
  while needed <= size:
    prefix = [Cell.EMPTY] * shift + [Cell.FULL] * content[0]
    compatible = True
    for i in range(len(prefix)):
      if current[i] != Cell.UNKNOWN and prefix[i] != current[i]:
        compatible = False
        break
    if compatible:
      # It's OK to not have an empty cell after if there's no more content
      if len(content) > 1:
        prefix += [Cell.EMPTY]
      for option in options(content[1:], size - len(prefix), current[len(prefix):], full):
        result.append(prefix + option)
    shift += 1
    needed += 1
  return result

def signature(line):
  result = []
  current = 0
  # Add an empty cell to count last pattern in case the line ends with a full one
  for c in line + [Cell.EMPTY]:
    if c == Cell.FULL:
      current += 1
    elif current != 0:
      result.append(current)
      current = 0
  return result


class Picross(object):

  def __init__(self, size, verticals, horizontals):
    assert len(verticals) == size
    assert len(horizontals) == size
    assert sum([y for x in verticals for y in x]) == sum([y for x in horizontals for y in x])
    self._size = size
    self._verticals = verticals
    self._horizontals = horizontals
    self._rows = [[Cell.UNKNOWN for i in range(size)] for j in range(size)]
    self._columns = [[Cell.UNKNOWN for i in range(size)] for j in range(size)]

  def set(self, x, y, c):
    self._rows[y][x] = c
    self._columns[x][y] = c

  def __str__(self):
    result = ""
    for row in self._rows:
      result += line_str(row) + "\n"
    return result

  def long_valid(self):
    for (y, row) in enumerate(self._rows):
      opts = options(self._horizontals[y], len(row), row)
      # Only keep options compatible with what we know
      for i in range(len(row)):
        if self._rows[y][i] != Cell.UNKNOWN:
          opts = [o for o in opts if o[i] == self._rows[y][i]]
      if not opts:
        return False
    for (x, column) in enumerate(self._columns):
      opts = options(self._verticals[x], len(column), column)
      # Only keep options compatible with what we know
      for i in range(len(column)):
        if self._columns[x][i] != Cell.UNKNOWN:
          opts = [o for o in opts if o[i] == self._columns[x][i]]
      if not opts:
        return False
    return True

  def valid(self):
    for (y, row) in enumerate(self._rows):
      if all([c != Cell.UNKNOWN for c in self._rows[y]]):
        if signature(self._rows[y]) != self._horizontals[y]:
          return False
    for (x, column) in enumerate(self._columns):
      if all([c != Cell.UNKNOWN for c in self._columns[x]]):
        if signature(self._columns[x]) != self._verticals[x]:
          return False
    return True

  def backtrack(self):
    result = []
    if not self.valid():
        return []
    for (y, row) in enumerate(self._rows):
      for x in range(len(row)):
        if self._rows[y][x] == Cell.UNKNOWN:
          self.set(x, y, Cell.FULL)
          result += self.backtrack()
          self.set(x, y, Cell.EMPTY)
          result += self.backtrack()
          self.set(x, y, Cell.UNKNOWN)
          return result
    print(self)
    return [copy.deepcopy(self)]

  def serialize(self, filename):
    with open(filename, "w") as f:
      for (y, row) in enumerate(self._rows):
        for x in range(len(row)):
          val = self._rows[y][x]
          if val != Cell.UNKNOWN:
            c = "picross.Cell.FULL" if val == Cell.FULL else "picross.Cell.EMPTY"
            f.write("p.set(%d, %d, %s)\n" % (x, y, c))

  def complete(self):
    return not any([c == Cell.UNKNOWN for row in self._rows for c in row])

  def solve(self):
    progress = True
    while progress:
      print("Doing rows")
      progress = False
      for (y, row) in enumerate(self._rows):
        print(" - row %d: %s" % (y, self._horizontals[y]))
        print(self)
        opts = options(self._horizontals[y], len(row), row)
        # Only keep options compatible with what we know
        for i in range(len(row)):
          if self._rows[y][i] != Cell.UNKNOWN:
            opts = [o for o in opts if o[i] == self._rows[y][i]]
        if not opts:
          raise RuntimeError("No option for row %d" % y)
        for i in range(len(row)):
          if self._rows[y][i] != Cell.UNKNOWN:
            continue
          val = opts[0][i]
          for o in opts:
              if o[i] != val:
                val = Cell.UNKNOWN
                break
          if val != Cell.UNKNOWN:
            self.set(i, y, val)
            progress = True
      print("Doing columns")
      for (x, column) in enumerate(self._columns):
        print(" - column %d: %s" % (x, self._verticals[x]))
        print(self)
        opts = options(self._verticals[x], len(column), column)
        # Only keep options compatible with what we know
        for i in range(len(column)):
          if self._columns[x][i] != Cell.UNKNOWN:
            opts = [o for o in opts if o[i] == self._columns[x][i]]
        if not opts:
          raise RuntimeError("No option for col %x" % x)
        for i in range(len(column)):
          if self._columns[x][i] != Cell.UNKNOWN:
            continue
          val = opts[0][i]
          for o in opts:
              if o[i] != val:
                val = Cell.UNKNOWN
                break
          if val != Cell.UNKNOWN:
            self.set(x, i, val)
            progress = True
      self.serialize("intermediate_result.txt")
      if self.complete():
        break
    print(self)
    if not self.complete():
      print("Now backtracking...")
      all_results = self.backtrack()
      print("*****************")
      print("* Full results: *")
      print("*****************")
      for r in all_results:
        print(r)
