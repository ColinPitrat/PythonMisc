#!/usr/bin/python
# -*- coding: utf8 -*-"

import unittest
import planetes
import math

class TestPosition(unittest.TestCase):

   def test_distance(self):
      cases = {
        # point 1, point 2, distance
        ((0, 0), (0, 2), 2),
        ((0, 0), (2, 0), 2),
        ((0, 0), (2, 2), 2*math.sqrt(2)),
        ((2, 0), (2, 2), 2),
        ((1, 1), (2, 2), math.sqrt(2)),
      }
      for c in cases:
        p1 = planetes.Position(c[0][0], c[0][1])
        p2 = planetes.Position(c[1][0], c[1][1])
        self.assertEqual(p1.distance(p2), c[2])
        self.assertEqual(p2.distance(p1), c[2])


if __name__ == '__main__':
   unittest.main()
