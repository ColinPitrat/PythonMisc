import bitflipping
import cbc
import unittest

class BitFlippingTest(unittest.TestCase):

    def testEncryptURL(self):
        cases = {
                "data": "comment1=cooking%20MCs;userdata=data;comment2=%20like%20a%20pound%20of%20bacon\x02\x02",
                "mydata": "comment1=cooking%20MCs;userdata=mydata;comment2=%20like%20a%20pound%20of%20bacon\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10",
                "mydata;admin=true": "comment1=cooking%20MCs;userdata=mydata%3Badmin%3Dtrue;comment2=%20like%20a%20pound%20of%20bacon\x01",
        }
        for i, o in cases.iteritems():
            iv, encrypted = bitflipping.encryptURL(i)
            result = cbc.decipherAES128CBC(encrypted, bitflipping.aes_key, iv)
            self.assertEqual(result, o)

    def testIsAdminDecrypted(self):
        cases = {
                "": False,

                "admin": False,
                "admin;userdata=true": False,
                "admin=true=false": False,

                "userdata=true": False,
                "userdata=toto;comment=false": False,

                "admin=true": True,
                "admin=false": False,
                "userdata=toto;admin=true": True,
                "userdata=toto;admin=false": False,
                "admin=true;comment=titi": True,
                "admin=false;comment=titi": False,
                "userdata=toto;admin=true;comment=titi": True,
                "userdata=toto;admin=false;comment=titi": False,
        }
        for i, o in cases.iteritems():
            self.assertEqual(bitflipping.isAdminDecrypted(i), o)


if __name__ == '__main__':
    unittest.main()
