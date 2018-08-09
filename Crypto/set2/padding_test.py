import unittest
import padding

class PaddingTest(unittest.TestCase):

  def testPad(self):
      cases = {
              ("YELLOW SUBMARINE", 16, '\x04'): "YELLOW SUBMARINE",
              ("YELLOW SUBMARINE", 20, '\x04'): "YELLOW SUBMARINE\x04\x04\x04\x04",
              ("YELLOW SUBMARINE", 20, 'a'): "YELLOW SUBMARINEaaaa",
              ("YELLOW SUBMARINE", 5, 'a'): "YELLOW SUBMARINEaaaa",
      }
      for i, o in cases.iteritems():
          self.assertEqual(padding.pad(*i), o)

  def testPKCS7Pad(self):
      cases = {
              ("YELLOW SUBMARINE", 16): "YELLOW SUBMARINE\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10",
              ("YELLOW SUBMARIN", 16): "YELLOW SUBMARIN\x01",
              ("YELLOW SUBMA", 16): "YELLOW SUBMA\x04\x04\x04\x04",
              ("ICE ICE BABY", 16): "ICE ICE BABY\x04\x04\x04\x04",
              ("YELLOW SUBMARINE", 20): "YELLOW SUBMARINE\x04\x04\x04\x04",
      }
      for i, o in cases.iteritems():
          self.assertEqual(padding.pkcs7_pad(*i), o)

  def testPKCS7Unpad(self):
      self.assertEqual(padding.pkcs7_unpad("ICE ICE BABY\x04\x04\x04\x04"), "ICE ICE BABY")
      with self.assertRaises(ValueError):
          self.assertEqual(padding.pkcs7_unpad("ICE ICE BABY\x05\x05\x05\x05"), "ICE ICE BABY")
      with self.assertRaises(ValueError):
          self.assertEqual(padding.pkcs7_unpad("ICE ICE BABY\x01\x02\x03\x04"), "ICE ICE BABY")


if __name__ == '__main__':
  unittest.main()
