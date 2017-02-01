#!/usr/bin/python
# -*- coding: utf8 -*-"

import unittest
import example

class TestGOL(unittest.TestCase):

   def test_peek_cell_in_the_middle(self):
      grid = example.GOLGrid(10, 10)
      grid.set_alive(5,5)
      self.assertEqual(0, grid.safe_peek_cell(4, 5))
      self.assertEqual(0, grid.safe_peek_cell(5, 4))
      self.assertEqual(1, grid.safe_peek_cell(5, 5))

   def test_peek_cell_on_the_horizontal_side(self):
      grid = example.GOLGrid(10, 10)
      grid.set_alive(0,0)
      grid.set_alive(9,1)
      self.assertEqual(1, grid.safe_peek_cell(0, 0))
      self.assertEqual(0, grid.safe_peek_cell(-1, 0))
      # We loop on the X dimension
      self.assertEqual(1, grid.safe_peek_cell(-1, 1))
      self.assertEqual(1, grid.safe_peek_cell(10, 0))

   def test_peek_cell_on_the_vertical_side(self):
      grid = example.GOLGrid(10, 10)
      grid.set_alive(0,0)
      grid.set_alive(1,9)
      self.assertEqual(1, grid.safe_peek_cell(0, 0))
      # We do not loop on the Y dimension
      self.assertEqual(0, grid.safe_peek_cell(1, -1))
      self.assertEqual(0, grid.safe_peek_cell(0, 10))

   def test_count_live_in_the_middle(self):
      grid = example.GOLGrid(10, 10)
      grid.set_alive(5,5)
      self.assertEqual(1, grid.count_live_neighbors(4, 5))
      self.assertEqual(1, grid.count_live_neighbors(5, 4))
      self.assertEqual(0, grid.count_live_neighbors(5, 5))


if __name__ == '__main__':
   unittest.main()
