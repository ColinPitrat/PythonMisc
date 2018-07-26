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


if __name__ == '__main__':
  unittest.main()
