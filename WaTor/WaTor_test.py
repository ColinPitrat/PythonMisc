#!/usr/bin/python
# -*- coding: utf8 -*-"

import unittest
import WaTor

class TestWaTor(unittest.TestCase):

  def test_powerOf2(self):
    self.assertFalse(WaTor.powerOf2(-2))
    self.assertFalse(WaTor.powerOf2(-1))
    self.assertFalse(WaTor.powerOf2(0))
    for i in range(0, 256):
        self.assertTrue(WaTor.powerOf2(2**i))
    for i in range(1, 256):
        self.assertFalse(WaTor.powerOf2(2**i + 1))
    for i in range(2, 256):
        self.assertFalse(WaTor.powerOf2(2**i + 2))
    self.assertFalse(WaTor.powerOf2(9))
    self.assertFalse(WaTor.powerOf2(18))
    self.assertFalse(WaTor.powerOf2(40))

  def test_powerOf2exponent(self):
    for i in range(0, 256):
        self.assertEqual(i, WaTor.powerOf2exponent(2**i))
    self.assertEqual(1, WaTor.powerOf2exponent(3))
    self.assertEqual(2, WaTor.powerOf2exponent(5))
    self.assertEqual(2, WaTor.powerOf2exponent(7))
    self.assertEqual(3, WaTor.powerOf2exponent(9))
    self.assertEqual(3, WaTor.powerOf2exponent(15))

  def test_size(self):
    wator = WaTor.WaTor(8, 16)
    self.assertEqual(8, wator.width())
    self.assertEqual(16, wator.height())

  def test_idx(self):
    wator = WaTor.WaTor(8, 16)
    self.assertEqual(0, wator.idx(0, 0))
    self.assertEqual(7, wator.idx(7, 0))
    self.assertEqual(0, wator.idx(8, 0))
    self.assertEqual(15, wator.idx(7, 1))
    self.assertEqual(20, wator.idx(4, 2))
    self.assertEqual(76, wator.idx(4, 9))
    self.assertEqual(4, wator.idx(4, 16))
    self.assertEqual(0, wator.idx(8, 16))
    self.assertEqual(21, wator.idx(5, 18))
    self.assertEqual(23, wator.idx(7, 18))
    self.assertEqual(127, wator.idx(7, 15))
    self.assertEqual(127, wator.idx(-1, -1))
    self.assertEqual(119, wator.idx(-1, -2))
    self.assertEqual(111, wator.idx(-1, -3))
    self.assertEqual(126, wator.idx(-2, -1))
    self.assertEqual(118, wator.idx(-2, -2))
    self.assertEqual(110, wator.idx(-2, -3))

  def test_x_in_idx(self):
    wator = WaTor.WaTor(8, 16)
    self.assertEqual(0, wator.x_from_idx(0))
    self.assertEqual(7, wator.x_from_idx(7))
    self.assertEqual(7, wator.x_from_idx(15))
    self.assertEqual(4, wator.x_from_idx(20))
    self.assertEqual(4, wator.x_from_idx(76))
    self.assertEqual(4, wator.x_from_idx(4))
    self.assertEqual(5, wator.x_from_idx(21))
    self.assertEqual(7, wator.x_from_idx(23))
    self.assertEqual(7, wator.x_from_idx(127))

  def test_y_in_idx(self):
    wator = WaTor.WaTor(8, 16)
    self.assertEqual(0, wator.y_from_idx(0))
    self.assertEqual(0, wator.y_from_idx(7))
    self.assertEqual(1, wator.y_from_idx(15))
    self.assertEqual(2, wator.y_from_idx(20))
    self.assertEqual(9, wator.y_from_idx(76))
    self.assertEqual(15, wator.y_from_idx(127))

  def test_add_makes_not_empty(self):
    wator = WaTor.WaTor(8, 16)

    self.assertTrue(wator.is_empty(3, 4))
    wator.add_fish(3, 4)
    self.assertFalse(wator.is_empty(3, 4))

    self.assertTrue(wator.is_empty(5, 4))
    wator.add_shark(5, 4)
    self.assertFalse(wator.is_empty(5, 4))

  def test_move(self):
    wator = WaTor.WaTor(8, 16)

    ox, oy = 3, 4
    wator.add_fish(ox, oy)
    wator.move()
    self.assertTrue(wator.is_empty(ox, oy))
    self.assertFalse(wator.is_empty(ox-1, oy) and wator.is_empty(ox+1, oy) and wator.is_empty(ox, oy-1) and wator.is_empty(ox, oy+1))
    nx, ny = 0, 0
    for (x, y) in [(2, 4), (4, 4), (3, 3), (3, 5)]:
        if not wator.is_empty(x, y):
            nx, ny = x, y
            break
    wator.move()
    self.assertTrue(wator.is_empty(nx, ny))
    self.assertFalse(wator.is_empty(nx-1, ny) and wator.is_empty(nx+1, ny) and wator.is_empty(nx, ny-1) and wator.is_empty(nx, ny+1))


if __name__ == '__main__':
   unittest.main()
