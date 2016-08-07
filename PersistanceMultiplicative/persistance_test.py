import unittest
import persistance



class TestEntierEnBase(unittest.TestCase):

   def test_entier_0_a_9_en_base_10_a_36(self):
      for base in range(10, 36):
         for num in range(0, 9):
            self.assertEqual("%s" % num, persistance.entier_en_base(num, base))

   def test_entier_0_a_9999_en_base_2(self):
      for num in range(0, 10000):
         self.assertEqual(bin(num), "0b" + persistance.entier_en_base(num, 2))

   def test_quelques_entiers_en_base_3(self):
      self.assertEqual("1021", persistance.entier_en_base(34, 3))
      self.assertEqual("10201", persistance.entier_en_base(100, 3))
      self.assertEqual("21012", persistance.entier_en_base(194, 3))

   def test_quelques_entiers_en_base_4(self):
      self.assertEqual("1032", persistance.entier_en_base(78, 4))
      self.assertEqual("3210", persistance.entier_en_base(228, 4))

   def test_entier_0_a_9999_en_base_8(self):
      self.assertEqual("0", persistance.entier_en_base(0, 8))
      for num in range(1, 10000):
         self.assertEqual(oct(num), "0" + persistance.entier_en_base(num, 8))

   def test_entier_0_a_9999_en_base_10(self):
      for num in range(0, 10000):
         self.assertEqual("%s" % num, persistance.entier_en_base(num, 10))

   def test_entier_0_a_9999_en_base_16(self):
      for num in range(0, 10000):
         self.assertEqual(hex(num), "0x" + persistance.entier_en_base(num, 16))

   def test_quelques_entiers_en_base_36(self):
      self.assertEqual("a", persistance.entier_en_base(10, 36))
      self.assertEqual("z", persistance.entier_en_base(35, 36))
      self.assertEqual("7az", persistance.entier_en_base(7*36*36+10*36+35, 36))
      self.assertEqual("fw2b", persistance.entier_en_base(15*36*36*36+32*36*36+2*36+11, 36))

   def test_quelques_entiers_negatif_en_base_2_a_36(self):
      for base in range(2, 36):
         for n in range(1, min(10, base)):
            self.assertEqual("-%s" % n, persistance.entier_en_base(-n, base))

   def test_string_raises_TypeError(self):
      with self.assertRaises(TypeError):
         persistance.entier_en_base("toto", 10)

   def test_float_raises_TypeError(self):
      with self.assertRaises(TypeError):
         persistance.entier_en_base(3.14, 10)



class TestProduitChiffres(unittest.TestCase):

   def test_produit_chiffres_chiffre_egal_a_lui_meme_base_2_a_36(self):
      for base in range(2, 36):
         for i in range(0, base):
            self.assertEqual(i, persistance.produit_chiffres(i, base))

   def test_produit_chiffres_1_a_10000_base_2(self):
      que_des_1 = [1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191 ]
      for i in range(1, 10000):
         expect = 0
         if i in que_des_1:
            expect = 1
         self.assertEqual(expect, persistance.produit_chiffres(i, 2))

   def test_produit_chiffres_12345_base_10(self):
      self.assertEqual(5*4*3*2, persistance.produit_chiffres(12345, 10))

   def test_produit_chiffres_37892_base_10(self):
      self.assertEqual(3*7*8*9*2, persistance.produit_chiffres(37892, 10))

   def test_produit_chiffres_AF297_base_16(self):
      self.assertEqual(10*15*2*9*7, persistance.produit_chiffres(0xAF297, 16))

   def test_produit_chiffres_negatif_raise_ValueError(self):
      with self.assertRaises(ValueError):
         persistance.produit_chiffres(-10, 10)

   def test_produit_chiffres_flottant_raise_TypeError(self):
      with self.assertRaises(TypeError):
         persistance.produit_chiffres(3.14, 10)

   def test_produit_chiffres_string_raise_TypeError(self):
      with self.assertRaises(TypeError):
         persistance.produit_chiffres("test", 10)



class TestPersistance(unittest.TestCase):

   def test_persistance_chiffre_egal_0_base_2_a_36(self):
      for base in range(2, 36):
         for i in range(0, base):
            self.assertEqual(0, persistance.persistance(i, base))

   def test_persistance_10_a_24_base_10_egal_1(self):
      for i in range(10, 25):
         self.assertEqual(1, persistance.persistance(i, 10))

   def test_persistance_25_a_29_base_10_egal_2(self):
      for i in range(25, 30):
         self.assertEqual(2, persistance.persistance(i, 10))

   def test_persistance_77_base_10_egal_4(self):
      self.assertEqual(4, persistance.persistance(77, 10))

   def test_persistance_377_base_10_egal_4(self):
      self.assertEqual(4, persistance.persistance(377, 10))

   def test_persistance_2_a_10000_base_2_egal_1(self):
      for i in range(2, 10000):
         self.assertEqual(1, persistance.persistance(i, 2))

   # Toutes les puissances de 2 en base 3 comportent un 0 sauf 2^1, 2^2, 2^3, 2^4 et 2^15
   # (conjecture verifiee tres loin) ce qui reduit la persistance a 1 
   def test_persistance_2_exp_2_a_100_base_3_egal_1(self):
      self.assertEqual(1, persistance.persistance(2**2, 3))
      self.assertEqual(2, persistance.persistance(2**3, 3))
      for i in range(4, 15):
         self.assertEqual(1, persistance.persistance(2**i, 3))
      self.assertEqual(2, persistance.persistance(2**15, 3))
      for i in range(16, 100):
         self.assertEqual(1, persistance.persistance(2**i, 3))

   # 26(base 3) == 222(base 10)
   def test_persistance_222_base_3_egal_3(self):
      self.assertEqual(3, persistance.persistance(26, 3))



class TestGenereNombre(unittest.TestCase):

   def test_genere_0_chiffre(self):
      self.assertEqual(0, persistance.genere_nombre([2, 3, 7], [0, 0, 0], 10))

   def test_genere_moins_de_repetitions_que_de_chiffres(self):
      self.assertEqual(23, persistance.genere_nombre([2, 3, 7], [1, 1], 10))

   def test_genere_plus_de_repetitions_que_de_chiffres(self):
      self.assertEqual(237, persistance.genere_nombre([2, 3, 7], [1, 1, 1, 1], 10))

   def test_genere_223337777_base_10(self):
      self.assertEqual(223337777, persistance.genere_nombre([2, 3, 7], [2, 3, 4], 10))



class TestGenerateCandidates(unittest.TestCase):

   # Pas un super bon test: trop contraignant sur l'order de generation de la sequence
   def test_genere_candidats(self):
      expected = [0, 2, 3, 5, 7, 22, 23, 35, 33, 55, 27, 37, 57, 77, 222, 223, 335, 233, 355, 333, 555, 227, 237, 357, 337, 557, 277, 377, 577, 777,
                  2222, 2223, 3335, 2233, 3355]
      generator = persistance.genere_candidats(0)
      for e, g in zip(expected, generator):
         self.assertEqual(e, g);

   def test_genere_candidats_a_partir_de_3_chiffres(self):
      expected = [222, 223, 335, 233, 355, 333, 555, 227, 237, 357, 337, 557, 277, 377, 577, 777,
                  2222, 2223, 3335, 2233, 3355]
      generator = persistance.genere_candidats(3)
      for e, g in zip(expected, generator):
         self.assertEqual(e, g);



if __name__ == '__main__':
   unittest.main()
