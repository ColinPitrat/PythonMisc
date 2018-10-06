"""Tests for cbc."""

import unittest
import cbc

class CbcTest(unittest.TestCase):

  def testCipherDecipherAES128ECB(self):
      cases = [
              ("This is a random string to cipher and decipher.", "YELLOW SUBMARINE"),
              ("And here is another one, just to have more than one.", "ENIRAMBUS WOLLEY"),
      ]
      for (msg, key) in cases:
          crypted = cbc.cipherAES128ECB(msg, key)
          self.assertNotEqual(crypted, msg)
          decrypted = cbc.decipherAES128ECB(crypted, key)
          self.assertEqual(msg, decrypted)

  def testCipherDecipherAES128CBC(self):
      cases = [
              ("This is a random string to cipher and decipher.", "YELLOW SUBMARINE", 'abcdefghijkl'),
              ("And here is another one, just to have more than one.", "ENIRAMBUS WOLLEY", '0000000000000000'),
      ]
      for (msg, key, iv) in cases:
          crypted = cbc.cipherAES128CBC(msg, key, iv)
          self.assertNotEqual(crypted, msg)
          decrypted = cbc.decipherAES128CBC(crypted, key, iv)
          self.assertEqual(msg, decrypted)

  def testXorStr(self):
      cases = {
              ("abcde", "abcde"): "\x00\x00\x00\x00\x00",
              ("abcde", "\x00\x00\x00\x00\x00"): "abcde",
              ("abcdef", "abc"): "\x00\x00\x00def",
      }
      for i, o in cases.iteritems():
          self.assertEqual(cbc.xorStr(*i), o)


if __name__ == '__main__':
  unittest.main()
