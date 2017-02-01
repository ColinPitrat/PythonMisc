#!/usr/bin/python
# -*- coding: utf8 -*-"

import unittest
import example
import numpy

class TestGOL(unittest.TestCase):

   def test_sum_cells_around(self):
      g = example.GOL(10, 10)
      self.assertEqual(0, g.sum_cells_around(0, 3, 3))

   def test_nb_neighbors(self):
      g = example.GOL(10, 10)
      g.set_alive(5, 5)
      self.assertEqual(0, g.nb_neighbors(5, 5))
      self.assertEqual(1, g.nb_neighbors(5, 4))
      self.assertEqual(1, g.nb_neighbors(4, 5))

   def test_nb_neighbors_edges(self):
      g = example.GOL(10, 10)
      g.set_alive(0, 0)
      g.set_alive(0, 9)
      g.set_alive(9, 0)
      self.assertEqual(3, g.nb_neighbors(9, 9))

   def test_next_status(self):
      g = example.GOL(10, 10)
      self.assertEqual(0, g.next_status(0, 0))
      self.assertEqual(0, g.next_status(0, 2))
      self.assertEqual(1, g.next_status(0, 3))
      self.assertEqual(0, g.next_status(0, 5))
      self.assertEqual(0, g.next_status(1, 0))
      self.assertEqual(1, g.next_status(1, 2))
      self.assertEqual(1, g.next_status(1, 3))
      self.assertEqual(0, g.next_status(1, 5))

   def test_next_generation(self):
      g = example.GOL(5, 5)
      g.set_alive(2, 1)
      g.set_alive(2, 2)
      g.set_alive(2, 3)
      g.next_generation()
      expected = numpy.zeros((5, 5))
      expected[2][1] = 1
      expected[2][2] = 1
      expected[2][3] = 1
      self.assertTrue((expected == g.map_).all())

if __name__ == '__main__':
   unittest.main()
