import random
import hex2base64
import padding
import cbc

input_strings = [
        'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
        'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
        'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
        'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
        'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
        'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
        'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
        'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
        'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
        'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93',
]

key =""

def generate_key(length):
    result = ""
    for i in range(0, length):
        result += chr(random.randint(0, 255))
    return result

def escapeString(content):
    for i in range(0, 32):
        content = content.replace(chr(i), hex(i).replace("0x", "\\x"))
    for i in range(128, 256):
        content = content.replace(chr(i), hex(i).replace("0x", "\\x"))
    return content

def encrypt(content):
    global key
    choice = padding.pkcs7_pad(hex2base64.base642str(content), 16)
    print("Encrypting %s" % escapeString(choice))
    key = generate_key(16)
    iv = generate_key(16)
    result = cbc.cipherAES128CBC(choice, key, iv)
    return result, iv

def chooseAndEncrypt():
    return encrypt(random.choice(input_strings))

def validPadding(content, iv):
    result = cbc.decipherAES128CBC(content, key, iv)
    print("Decrypting %s" % escapeString(result))
    try:
        result = padding.pkcs7_unpad(result)
        return True
    except ValueError:
        return False



def patchChar(content, index, newvalue):
    return content[0:index] + newvalue + content[index+1:]

def xorChar(content, index, operand):
    return content[0:index] + chr(ord(content[index]) ^ operand) + content[index+1:]

def findPadding(r, iv):
    # Break the padding if != 1
    r = xorChar(r, len(r)-18, 2)
    r = xorChar(r, len(r)-19, 1)
    for i in range(0, 255):
        d = xorChar(r, len(r)-17, i)
        if validPadding(d, iv):
            return i ^ 1
    return None

if False:
    print("")
    for s in input_strings:
        print(hex2base64.base642str(s))
    print("")

    for s in input_strings:
        print("=====")
        r, iv = encrypt(s)
        p = findPadding(r, iv)
        print("Padding: %s" % p)

        print("R : %s" % hex2base64.str2hex(r))
        print("Found: %s" % chr(findChar(r2, iv, len(r)-p)))

        print("")
        print("Valid: %s" % validPadding(r, iv))
        r = xorChar(r, len(r)-17, 1)
        print("Valid: %s" % validPadding(r, iv))

r, iv = chooseAndEncrypt()
pad = findPadding(r, iv)
print("Padding: %s" % pad)
c = "%s" % chr(pad)
p = r
for i in range(1, 16):
    for b in range(1, 255):
        d = xorChar(p, len(p)-17-i, b)
        if validPadding(d, iv):
            p = patchChar(p, len(p)-i, chr(b))
            c = chr(b) + c
            break
    print("Result: %s" % escapeString(c))
