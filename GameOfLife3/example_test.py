#!/usr/bin/python
# -*- coding: utf8 -*-"

import unittest
import example

class TestGameOfLife(unittest.TestCase):

   def test_setAlive_and_get(self):
      g = example.GameOfLife(10, 10)
      g.setAlive(1, 1)
      g.setAlive(9, 9)
      self.assertEqual(0, g.get(0, 0))
      self.assertEqual(1, g.get(1, 1))
      self.assertEqual(1, g.get(-1, -1))

   def testRowsCols(self):
      g = example.GameOfLife(10, 1)
      g.setAlive(5, 1)
      self.assertEqual(0, g.get(1, 5))
      self.assertEqual(1, g.get(5, 1))

   def testCountN(self):
     g = example.GameOfLife(10, 10)
     self.assertEqual(0, g.countN(5,5))

     g.setAlive(5, 5)
     self.assertEqual(0, g.countN(5,5))
     g.setAlive(4, 5)
     self.assertEqual(1, g.countN(5,5))
     g.setAlive(6, 5)
     self.assertEqual(2, g.countN(5,5))

     g.setAlive(5, 6)
     self.assertEqual(3, g.countN(5,5))
     g.setAlive(4, 6)
     self.assertEqual(4, g.countN(5,5))
     g.setAlive(6, 6)
     self.assertEqual(5, g.countN(5,5))

     g.setAlive(5, 4)
     self.assertEqual(6, g.countN(5,5))
     g.setAlive(4, 4)
     self.assertEqual(7, g.countN(5,5))
     g.setAlive(6, 4)
     self.assertEqual(8, g.countN(5,5))

   def testWillLiveAlreadyLiving(self):
     g = example.GameOfLife(10, 10)
     g.setAlive(3, 3)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(3, 2)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(3, 4)
     self.assertTrue(g.willLive(3, 3))
     g.setAlive(2, 3)
     self.assertTrue(g.willLive(3, 3))
     g.setAlive(2, 2)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(2, 4)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(4, 2)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(4, 3)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(4, 4)
     self.assertFalse(g.willLive(3, 3))

   def testWillLiveDeadCell(self):
     g = example.GameOfLife(10, 10)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(3, 2)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(3, 4)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(2, 3)
     self.assertTrue(g.willLive(3, 3))
     g.setAlive(2, 2)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(2, 4)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(4, 2)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(4, 3)
     self.assertFalse(g.willLive(3, 3))
     g.setAlive(4, 4)
     self.assertFalse(g.willLive(3, 3))

   def test_idx(self):
      g = example.GameOfLife(10, 10)
      self.assertEqual(14, g.idx(31, 24))


if __name__ == '__main__':
   unittest.main()
