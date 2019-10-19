#!/usr/bin/python
# -*- coding: utf8 -*-"

import picross
import ownd

# Example from https://en.wikipedia.org/wiki/Nonogram
p = picross.Picross(11,
      [[0], [9], [9], [2, 2], [2, 2], [4], [4], [0], [0], [0], [0]],
      [[0], [4], [6], [2, 2], [2, 2], [6], [4], [2], [2], [2], [0]])

p = ownd.p

def main():
  print(p)
  assert p.long_valid()
  p.solve()

if __name__ == "__main__":
  main()
