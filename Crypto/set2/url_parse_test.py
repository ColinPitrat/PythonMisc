"""Tests for url_parse."""

import unittest
import url_parse
import oracle


class UrlParseTest(unittest.TestCase):

  def testUrlParse(self):
      cases = {
              "": {},
              "foo=bar": {
                      'foo': 'bar',
              },
              "foo=bar&baz=qux&zap=zazzle": {
                      'foo': 'bar',
                      'baz': 'qux',
                      'zap': 'zazzle'
              },
      }
      for i, o in cases.iteritems():
          self.assertEqual(url_parse.parse(i), o)

  def testEncode(self):
      cases = {
              "foo@bar.com": "email=foo@bar.com&uid=10&role=user",
              "foo@bar.com&role=admin": "email=foo@bar.comroleadmin&uid=10&role=user",
      }
      for i, o in cases.iteritems():
          self.assertEqual(url_parse.profile_for(i), o)

  def testCryptDecrypt(self):
      cases = {
              "foo@bar.com": {
                      'email': 'foo@bar.com',
                      'uid': '10',
                      'role': 'user',
              },
      }
      for i, o in cases.iteritems():
          key = oracle.generate_key(16)
          self.assertEqual(url_parse.decryptProfile(url_parse.encryptProfile(i, key), key), o)


if __name__ == '__main__':
  unittest.main()
