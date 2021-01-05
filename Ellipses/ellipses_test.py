#!/usr/bin/python
# -*- coding: utf8 -*-"

import unittest
import ellipses

class TestPosition(unittest.TestCase):

   def test_distance(self):
      cases = {
        ((0, 0), (1, 0), 1),
        ((0, 0), (0, 1), 1),
        ((0, 0), (3, 4), 5),
        ((1, 2), (4, 6), 5),
        ((4, 6), (1, 2), 5),
      }
      for c in cases:
        d = ellipses.distance(c[0], c[1])
        self.assertEqual(d, c[2], 'La distance entre %s et %s est %s, attendait %s' % (c[0], c[1], d, c[2]))

   def test_somme_distances(self):
      cases = {
        (((0, 1), (1, 0), (2, 1)), (1, 1), 3),
      }
      for c in cases:
        d = ellipses.somme_distances(c[0], c[1])
        self.assertEqual(d, c[2], 'La somme des distances entre %s et %s est %s, attendait %s' % (c[0], c[1], d, c[2]))


if __name__ == '__main__':
   unittest.main()
