"""Tests for hex2base64."""

import unittest
import hex2base64

class Hex2base64Test(unittest.TestCase):

  def testNumToB64Char(self):
      cases = {
              0: 'A',
              10: 'K',
              25: 'Z',
              26: 'a',
              30: 'e',
              51: 'z',
              52: '0',
              61: '9',
              62: '+',
              63: '/',
      }
      for i, o in cases.iteritems():
          self.assertEqual(hex2base64.numToB64Char(i), o)

  def testB64CharToNum(self):
      cases = {
              'A': 0,
              'K': 10,
              'Z': 25,
              'a': 26,
              'e': 30,
              'z': 51,
              '0': 52,
              '9': 61,
              '+': 62,
              '/': 63,
      }
      for i, o in cases.iteritems():
          self.assertEqual(hex2base64.b64CharToNum(i), o)

  def testNumToB64CharError(self):
      with self.assertRaises(TypeError):
          hex2base64.numToB64Char("42")
      with self.assertRaises(ValueError):
          hex2base64.numToB64Char(-1)
      with self.assertRaises(ValueError):
          hex2base64.numToB64Char(64)

  def testHex2String(self):
      cases = {
              "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d": "I'm killing your brain like a poisonous mushroom",
              "746865206b696420646f6e277420706c6179": "the kid don't play",
      }
      for i, o in cases.iteritems():
          self.assertEqual(hex2base64.hex2str(i), o)

  def testString2Hex(self):
      cases = {
              "I'm killing your brain like a poisonous mushroom": "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d",
              "the kid don't play": "746865206b696420646f6e277420706c6179",
      }
      for i, o in cases.iteritems():
          self.assertEqual(hex2base64.str2hex(i), o)

  def testHex2Base64(self):
      cases = {
              "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d": "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t",
              "706c6561737572652e": "cGxlYXN1cmUu",
              "6c6561737572652e": "bGVhc3VyZS4=",
              "6561737572652e": "ZWFzdXJlLg==",
              "61737572652e": "YXN1cmUu",
              "737572652e": "c3VyZS4=",
      }
      for i, o in cases.iteritems():
          self.assertEqual(hex2base64.hex2base64(i), o)

  def testStr2Base64(self):
      cases = {
              "I'm killing your brain like a poisonous mushroom": "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t",
              "pleasure.": "cGxlYXN1cmUu",
              "leasure.": "bGVhc3VyZS4=",
              "easure.": "ZWFzdXJlLg==",
              "asure.": "YXN1cmUu",
              "sure.": "c3VyZS4=",
      }
      for i, o in cases.iteritems():
          self.assertEqual(hex2base64.str2base64(i), o)

  def testBase642Str(self):
      cases = {
              "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t": "I'm killing your brain like a poisonous mushroom",
              "cGxlYXN1cmUu": "pleasure.",
              "bGVhc3VyZS4=": "leasure.",
              "ZWFzdXJlLg==": "easure.",
              "YXN1cmUu": "asure.",
              "c3VyZS4=": "sure.",
      }
      for i, o in cases.iteritems():
          self.assertEqual(hex2base64.base642str(i), o)


if __name__ == '__main__':
  unittest.main()
