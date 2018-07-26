import random
import cbc
import hex2base64

consistent_key = 'abcdefghijklmnop'

def generate_key(length):
    result = ""
    for i in range(0, length):
        result += chr(random.randint(0, 255))
    return result

def challenge12encrypt(content):
    return cbc.cipherAES128ECB(content, consistent_key)

def challenge12encrypt2(content):
    suffix = hex2base64.base642str("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
                                   "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
                                   "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
                                   "YnkK")
    content = content + suffix
    return cbc.cipherAES128ECB(content, consistent_key)

def encryption_oracle(content):
    content = '%s%s%s' % (generate_key(random.randint(5,10)), content, generate_key(random.randint(5,10)))
    if random.randint(0,1) == 0:
        return ('ECB', cbc.cipherAES128ECB(content, generate_key(16)))
    return ('CBC', cbc.cipherAES128CBC(content, generate_key(16), generate_key(16)))

def encryption_oracle(content):
    content = '%s%s%s' % (generate_key(random.randint(5,10)), content, generate_key(random.randint(5,10)))
    if random.randint(0,1) == 0:
        return ('ECB', cbc.cipherAES128ECB(content, generate_key(16)))
    return ('CBC', cbc.cipherAES128CBC(content, generate_key(16), generate_key(16)))

def byteHammingDistance(a, b):
    c = a ^ b
    r = c & 0b01010101
    r += (c & 0b10101010) >> 1
    r2 = r & 0b00110011
    r2 += (r & 0b11001100) >> 2
    r = r2 & 0b00001111
    r += (r2 & 0b11110000) >> 4
    return r

def hammingDistance(a, b):
    if len(a) < len(b):
        a, b = b, a
    # b is always the shorter one
    r = 0
    for i in range(0, len(b)):
        r += byteHammingDistance(ord(a[i]), ord(b[i]))
    # Effectively pad b with 0
    for i in range(len(b), len(a)):
        r += byteHammingDistance(ord(a[i]), 0)
    #print("distance between '%s' and '%s': %s" % (a,b,r))
    return r

def usesECB(content):
    score = 0
    for i in range(0, len(content)/16):
        for j in range(i+1, len(content)/16):
            if content[i*16:(i+1)*16] == content[j*16:(j+1)*16]:
                #print('%s & %s' % (i, j))
                score += 1
    print('Score: %s' % score)
    # Score should really be either 0 or n(n+1)/2 but we can be unlucky ...
    if score > len(content)/16:
        return True
    return False

def detect_ECB_or_CBC():
    content = '0' * 160
    real, encrypted = encryption_oracle(content)
    detected = 'ECB' if usesECB(encrypted) else 'CBC'
    #print('Detected = %s - Real = %s' % (detected, real))
    return detected == real

def challenge11():
    total = 0
    success = 0
    for i in range(0, 1000):
        total += 1
        if detect_ECB_or_CBC():
            success += 1
    print("Success: %s / %s (%s%%)" % (success, total, 100.0*success/total))

def discoverBlockSize():
    l1, l2, l3 = 0, 0, 0
    for i in range(0, 50):
        r = challenge12encrypt2('A'*i)
        l = len(r)
        if l1 == 0:
            print("1) For i = %s, l = %s" % (i, l))
            l1 = l
        elif l2 == 0:
            if l != l1:
                print("2) For i = %s, l = %s" % (i, l))
                l2 = len(r)
        elif l3 == 0:
            if l != l2:
                print("3) For i = %s, l = %s" % (i, l))
                l3 = len(r)
        #print('%s -> %s' % (i, hex2base64.str2hex(r)))
    print('Block size = %s (%s-%s confirmation: %s: %s-%s)' % (l2-l1, l2, l1, l3-l2, l3, l2))
    return l2-l1

def verifyUsesECB():
    r = challenge12encrypt2('A'*500)
    if usesECB(r):
        print("OK: Uses ECB")
    else:
        print("*** KO: does not use ECB ***")

def challenge12():
    bs = discoverBlockSize()
    verifyUsesECB()
    result = ""
    bl = 1
    for bl in range(1, 10):
        for i in range(1, 17):
            short_in = 'A' * (bs-i)
            r = challenge12encrypt2(short_in)
            for b in range(0, 255):
                r2 = challenge12encrypt2(short_in + result + chr(b))
                if r[:bl*bs] == r2[:bl*bs]:
                    result += chr(b)
                    break
    print(result)

if __name__ == '__main__':
    #challenge11()
    challenge12()
