#!/usr/bin/python
# -*- coding: utf8 -*-"

import unittest
import example

class TestFactorielle(unittest.TestCase):

   # TODO: negative numbers ? floats ? strings ? ...
   def test_factorial_0_equal_1(self):
      self.assertEqual(1, example.factorial(0))

   def test_factorial_1_equal_1(self):
      self.assertEqual(1, example.factorial(1))

   def test_factorial_2_equal_2(self):
      self.assertEqual(2, example.factorial(2))

   def test_factorial_3_equal_6(self):
      self.assertEqual(6, example.factorial(3))

   def test_factorial_10_equal_3628800(self):
      self.assertEqual(3628800, example.factorial(10))

if __name__ == '__main__':
   unittest.main()
