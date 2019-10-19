#!/usr/bin/python
# -*- coding: utf8 -*-"

import unittest
import picross

class TestPicross(unittest.TestCase):

   def setUp(self):
      picross.CELL_UNKNOWN = "?"
      picross.CELL_EMPTY = " "
      picross.CELL_FULL = "#"

   def test_empty_grid(self):
      p = picross.Picross(5,
              [[0], [0], [0], [0], [0]],
              [[0], [0], [0], [0], [0]]);
      #self.assertEqual(1, picross.factorial(0))

   def test_not_enough_weights_verticals(self):
      with self.assertRaises(AssertionError):
          p = picross.Picross(5,
                  [[0], [0], [0], [0]],
                  [[0], [0], [0], [0], [0]]);

   def test_not_enough_weights_horizontals(self):
      with self.assertRaises(AssertionError):
          p = picross.Picross(5,
                  [[0], [0], [0], [0], [0]],
                  [[0], [0], [0], [0]]);

   def test_sums_do_not_match(self):
      with self.assertRaises(AssertionError):
          p = picross.Picross(5,
                  [[1], [1], [1], [0], [0]],
                  [[1], [1], [0], [0], [0]]);

   def test_str(self):
      p = picross.Picross(5,
                  [[1], [1], [1], [1], [1]],
                  [[5], [0], [0], [0], [0]]);
      self.assertEqual("?????\n?????\n?????\n?????\n?????\n", str(p))
      for x in range(5):
          p.set(x, 0, picross.Cell.FULL)
      self.assertEqual("#####\n?????\n?????\n?????\n?????\n", str(p))
      for x in range(5):
          p.set(x, 1, picross.Cell.EMPTY)
      self.assertEqual("#####\n     \n?????\n?????\n?????\n", str(p))

   def test_options_0(self):
      self.assertEqual(["     "], [picross.line_str(x) for x in picross.options([0], 5, [picross.Cell.UNKNOWN]*5, full=True)])

   def test_options_full(self):
      self.assertEqual(["#####"], [picross.line_str(x) for x in picross.options([5], 5, [picross.Cell.UNKNOWN]*5, full=True)])

   def test_options_split(self):
      self.assertItemsEqual(["## # ", "##  #", " ## #"], [picross.line_str(x) for x in picross.options([2, 1], 5, [picross.Cell.UNKNOWN]*5, full=True)])

   def test_options_split_with_content(self):
      for full in [False, True]:
          self.assertItemsEqual(["## # ", "##  #"], [picross.line_str(x) for x in picross.options([2, 1], 5, [picross.Cell.FULL] + [picross.Cell.UNKNOWN]*4, full=full)])
          self.assertItemsEqual(["##  #", " ## #"], [picross.line_str(x) for x in picross.options([2, 1], 5, [picross.Cell.UNKNOWN]*4 + [picross.Cell.FULL], full=full)])

   def test_fast_options(self):
      self.assertItemsEqual(["## # ", " ## #"], [picross.line_str(x) for x in picross.options([2, 1], 5, [picross.Cell.UNKNOWN]*5)])

   def test_signature(self):
      # Only the first and last number can be 0 (line starting or ending with no empty cell).
      for (z, a, b, c, d, e, f) in [
          (0, 3, 1, 2, 1, 2, 1),
          (2, 3, 1, 2, 1, 2, 1),
          (0, 5, 4, 6, 7, 9, 8),
          (0, 1, 2, 1, 3, 1, 0),
          (3, 1, 2, 1, 3, 1, 0),
      ]:
          self.assertEqual([a, c, e], picross.signature([picross.Cell.EMPTY] * z +
                      [picross.Cell.FULL] * a + [picross.Cell.EMPTY] * b +
                      [picross.Cell.FULL] * c + [picross.Cell.EMPTY] * d +
                      [picross.Cell.FULL] * e + [picross.Cell.EMPTY] * f
                      ))

   def test_valid(self):
      p = picross.Picross(5,
                  [[1], [1], [1], [1], [1]],
                  [[5], [0], [0], [0], [0]]);
      self.assertTrue(p.valid())
      p.set(0, 0, picross.Cell.FULL)
      p.set(1, 0, picross.Cell.FULL)
      p.set(2, 0, picross.Cell.FULL)
      p.set(3, 0, picross.Cell.FULL)
      p.set(4, 0, picross.Cell.FULL)
      self.assertTrue(p.valid())
      p.set(4, 0, picross.Cell.EMPTY)
      self.assertFalse(p.valid())
      p.set(4, 0, picross.Cell.UNKNOWN)
      self.assertTrue(p.valid())

   def test_long_valid(self):
      p = picross.Picross(5,
                  [[3], [3], [3], [1], [1]],
                  [[3], [0], [5], [0], [3]]);
      self.assertTrue(p.long_valid())
      p.set(0, 0, picross.Cell.FULL)
      self.assertTrue(p.long_valid())
      p.set(1, 0, picross.Cell.FULL)
      self.assertTrue(p.long_valid())
      p.set(2, 0, picross.Cell.FULL)
      self.assertTrue(p.long_valid())
      p.set(3, 0, picross.Cell.FULL)
      self.assertFalse(p.long_valid())
      p.set(2, 0, picross.Cell.EMPTY)
      self.assertFalse(p.long_valid())
      p.set(3, 0, picross.Cell.EMPTY)
      self.assertFalse(p.long_valid())
      p.set(2, 0, picross.Cell.FULL)
      self.assertTrue(p.long_valid())

      p.set(2, 2, picross.Cell.FULL)
      self.assertTrue(p.long_valid())
      p.set(3, 2, picross.Cell.FULL)
      self.assertTrue(p.long_valid())
      p.set(4, 2, picross.Cell.FULL)
      self.assertTrue(p.long_valid())


if __name__ == '__main__':
   unittest.main()
