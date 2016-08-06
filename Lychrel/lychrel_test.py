import unittest
import lychrel



class TestReverseNumber(unittest.TestCase):

   def test_reverse_1_is_1(self):
      self.assertEqual(1, lychrel.reverse(1, 10))

   def test_reverse_12_is_21(self):
      self.assertEqual(12, lychrel.reverse(21, 10))

   def test_reverse_493_is_394(self):
      self.assertEqual(493, lychrel.reverse(394, 10))

   def test_reverse_100_is_1(self):
      self.assertEqual(1, lychrel.reverse(100, 10))

   def test_reverse_negative_returns_0(self):
      self.assertEqual(0, lychrel.reverse(-100, 10))

   def test_reverse_throw_TypeError_if_given_float(self):
      with self.assertRaises(TypeError):
         lychrel.reverse(3.1415, 10)

   def test_reverse_throw_TypeError_if_given_string(self):
      with self.assertRaises(TypeError):
         lychrel.reverse("test", 10)

   def test_reverse_1A_is_A1(self):
      self.assertEqual(0xA1, lychrel.reverse(0x1A, 16))

   def test_reverse_E9ABC_is_CBA9E(self):
      self.assertEqual(0xCBA9E, lychrel.reverse(0xE9ABC, 16))

   def test_reverse_10111_is_11101(self):
      self.assertEqual(0b11101, lychrel.reverse(0b10111, 2))

   # TODO: test with invalid inputs for base



class TestLychrelStep(unittest.TestCase):

   def test_lychrel_step_63_is_99(self):
      self.assertEqual(99, lychrel.lychrel_step(63, 10))

   def test_lychrel_step_121_is_242(self):
      self.assertEqual(242, lychrel.lychrel_step(121, 10))

   def test_lychrel_step_74_is_121(self):
      self.assertEqual(121, lychrel.lychrel_step(74, 10))

   def test_lychrel_step_39_is_132(self):
      self.assertEqual(132, lychrel.lychrel_step(39, 10))

   def test_lychrel_step_1A_is_BB(self):
      self.assertEqual(0xBB, lychrel.lychrel_step(0x1A, 16))

   def test_lychrel_step_2F_is_121(self):
      self.assertEqual(0x121, lychrel.lychrel_step(0x2F, 16))

   def test_lychrel_step_BF_is_1BA(self):
      self.assertEqual(0x1BA, lychrel.lychrel_step(0xBF, 16))

   def test_lychrel_step_10110_is_100011(self):
      self.assertEqual(0b100011, lychrel.lychrel_step(0b10110, 2))

   # TODO: test with invalid inputs for base



class TestLychrelLoop(unittest.TestCase):

   def test_lychrel_loop_11_is_11(self):
      self.assertEqual([11], lychrel.lychrel_loop(11, 10))

   def test_lychrel_loop_12_is_12_33(self):
      self.assertEqual([12, 33], lychrel.lychrel_loop(12, 10))

   def test_lychrel_loop_39_is_39_132_363(self):
      self.assertEqual([39, 132, 363], lychrel.lychrel_loop(39, 10))

   def test_lychrel_loop_1A_is_1A_BB(self):
      self.assertEqual([0x1A, 0xBB], lychrel.lychrel_loop(0x1A, 16))

   def test_lychrel_loop_BF_is_BF_1BA_C6B_etc(self):
      self.assertEqual([0xBF, 0x1BA, 0xC6B, 0x17D7, 0x9548, 0x119A1, 0x2C2B2, 0x57574, 0x9EAE9], lychrel.lychrel_loop(0xBF, 16))

   def test_lychrel_loop_10011_is_10011_101100_etc(self):
      self.assertEqual([0b10011, 0b101100, 0b111001, 0b1100000, 0b1100011], lychrel.lychrel_loop(0b10011, 2))

   # TODO: test with invalid inputs for base



class TestLychrelNum(unittest.TestCase):

   def test_lychrel_num_11_is_0(self):
      self.assertEqual(0, lychrel.lychrel_num(11, 10))

   def test_lychrel_num_12_is_1(self):
      self.assertEqual(1, lychrel.lychrel_num(12, 10))

   def test_lychrel_num_39_is_2(self):
      self.assertEqual(2, lychrel.lychrel_num(39, 10))

   def test_lychrel_num_193_is_8(self):
      self.assertEqual(8, lychrel.lychrel_num(193, 10))

   def test_lychrel_num_1F_is_2(self):
      self.assertEqual(2, lychrel.lychrel_num(0x1F, 16))

   def test_lychrel_num_BF_is_2(self):
      self.assertEqual(8, lychrel.lychrel_num(0xBF, 16))

   def test_lychrel_num_1000_is_1(self):
      self.assertEqual(1, lychrel.lychrel_num(0b100, 2))

   def test_lychrel_num_1011_is_2(self):
      self.assertEqual(2, lychrel.lychrel_num(0b1011, 2))

   def test_lychrel_num_10100_is_2(self):
      self.assertEqual(5, lychrel.lychrel_num(0b10100, 2))

   # TODO: test with invalid inputs for base



class TestLychrelCandidates(unittest.TestCase):

   def test_lychrel_candidate_11_in_1_step_is_false(self):
      self.assertEqual(False, lychrel.lychrel_candidate(11, 1, 10))

   def test_lychrel_candidate_12_is_false(self):
      self.assertEqual(False, lychrel.lychrel_candidate(12, 2, 10))

   def test_lychrel_candidate_39_is_false(self):
      self.assertEqual(False, lychrel.lychrel_candidate(39, 3, 10))

   def test_lychrel_candidate_193_is_false(self):
      self.assertEqual(False, lychrel.lychrel_candidate(193, 9, 10))

   def test_lychrel_candidate_196_is_true(self):
      self.assertEqual(True, lychrel.lychrel_candidate(196, 1000, 10))

   def test_lychrel_candidate_879_is_true(self):
      self.assertEqual(True, lychrel.lychrel_candidate(879, 1000, 10))

   def test_lychrel_candidate_1997_is_true(self):
      self.assertEqual(True, lychrel.lychrel_candidate(1997, 1000, 10))

   def test_lychrel_candidate_BF_is_false(self):
      self.assertEqual(False, lychrel.lychrel_candidate(0xBF, 1000, 16))

   def test_lychrel_candidate_19D_is_true(self):
      self.assertEqual(True, lychrel.lychrel_candidate(0x19D, 1000, 16))

   def test_lychrel_candidate_10100_is_false(self):
      self.assertEqual(False, lychrel.lychrel_candidate(0b10100, 1000, 2))

   def test_lychrel_candidate_10110_is_true(self):
      self.assertEqual(True, lychrel.lychrel_candidate(0b10110, 1000, 2))

   # TODO: test with invalid inputs for base



if __name__ == '__main__':
   unittest.main()
