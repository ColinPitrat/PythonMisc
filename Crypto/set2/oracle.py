import random
import cbc
import hex2base64
import sys
import time

consistent_key = 'abcdefghijklmnop'
magic_char = '\xFF'

def generate_key(length):
    result = ""
    for i in range(0, length):
        result += chr(random.randint(0, 255))
    return result

def challenge12encrypt(content):
    suffix = hex2base64.base642str("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
                                   "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
                                   "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
                                   "YnkK")
    content = content + suffix
    return cbc.cipherAES128ECB(content, consistent_key)

def challenge14encrypt_with_prefixlength(content):
    suffix = hex2base64.base642str("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
                                   "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
                                   "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
                                   "YnkK")
    prefix = generate_key(random.randint(50, 150))
    content = prefix + content + suffix
    #print("To cipher: %s" % hex2base64.str2hex(content))
    return cbc.cipherAES128ECB(content, consistent_key), len(prefix)

def challenge14encrypt(content):
    return challenge14encrypt_with_prefixlength(content)[0]

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

def discoverBlockSize(oracle):
    l1, l2, l3 = 0, 0, 0
    for i in range(0, 50):
        r = oracle('A'*i)
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

def discoverBlockSize2(oracle):
    lengths = set()
    for i in range(0, 50):
        # We want to be sure to find the min length
        for j in range(0, 50):
            r = oracle('A'*i)
            lengths.add(len(r))
    lengths = sorted(list(lengths))
    dls = []
    prev = lengths[0]
    for l in lengths:
        if l == prev:
            continue
        dls.append(l - prev)
        prev = l
    dls = sorted(list(set(dls)))
    print('Min length = %s - Block size = %s (candidates: %s)' % (lengths[0], dls[0], dls))
    return (lengths[0], dls[0])

def verifyUsesECB(oracle):
    r = oracle('A'*500)
    if usesECB(r):
        print("OK: Uses ECB")
    else:
        print("*** KO: does not use ECB ***")

def challenge12():
    min_l, bs = discoverBlockSize2(challenge12encrypt)
    verifyUsesECB(challenge12encrypt)
    result = ""
    for bl in range(1, 10):
        for i in range(1, 17):
            short_in = 'A' * (bs-i)
            r = challenge12encrypt(short_in)
            for b in range(0, 255):
                r2 = challenge12encrypt(short_in + result + chr(b))
                if r[:bl*bs] == r2[:bl*bs]:
                    result += chr(b)
                    break
    print(result)

def findAAABlock(oracle, bs):
    candidates = {}
    for k in range(0, 100):
        content = oracle(magic_char * 100)
        for i in range(0, len(content)/bs):
            block = content[i*bs:(i+1)*bs]
            for j in range(i+1, len(content)/bs):
                block2 = content[j*bs:(j+1)*bs]
                if block == block2:
                    if block not in candidates:
                        candidates[block] = 0
                    candidates[block] += 1
    winner = ''
    max_score = 0
    for block, score in candidates.iteritems():
        if score > max_score:
            max_score = score
            winner = block
    print("Winner: %s" % hex2base64.str2hex(block))
    return winner

def findFirstBlockAfter(block, content):
    bs = len(block)
    #print("Block length: %s" % bs)
    i = 0
    while content[bs*i:bs*(i+1)] != block:
        i += 1
        if i*bs > len(content):
            print("ERROR: Out of content !")
            return -1
    while content[bs*i:bs*(i+1)] == block:
        i += 1
        if i*bs > len(content):
            print("ERROR: Out of content !")
            return -1
    #print("First block = %s" % i)
    return i

def challenge14():
    begin = time.time()
    min_l, bs = discoverBlockSize2(challenge14encrypt)
    verifyUsesECB(challenge14encrypt)
    aaa_block = findAAABlock(challenge14encrypt, bs)
    result = ""
    min_retries, tot_retries, max_retries = 0, 0, 0
    nb_chars = 0
    for bl in range(1, 10):
        for i in range(1, 17):
            retries = 0
            progressed = False
            short_in = magic_char * (3*bs-i)
            results = {}
            collisions = []
            while not progressed:
                for b in range(0, 255):
                    if b == magic_char:
                        continue
                    # Increase chances of detecting collisions
                    for d in range(0, 20):
                        r2, pl = challenge14encrypt_with_prefixlength(short_in + result + chr(b))
                        #print('R2: %s' % hex2base64.str2hex(r2))
                        fbi = findFirstBlockAfter(aaa_block, r2)
                        if fbi < 0:
                            continue
                        blocks = r2[fbi*bs:(fbi+bl)*bs]
                        # Collision means that the added letter falls at the beginning of a block
                        if blocks in collisions or (blocks in results and results[blocks][0] != b):
                            collisions.append(blocks)
                            #print("%s with pl %s collides" % (chr(b), pl))
                        results[blocks] = (b, pl)
                        #print('Result[%s] = (%s (%s), %s)' % (hex2base64.str2hex(blocks), chr(b), b, pl))
                for c in collisions:
                    results.pop(c, None)
                # Increase chances of hitting the right value
                for i in range(0, 20):
                    r = challenge14encrypt(short_in)
                    #print('R: %s' % hex2base64.str2hex(r))
                    nfbi = findFirstBlockAfter(aaa_block, r)
                    candidate = r[nfbi*bs:(nfbi+bl)*bs]
                    #print('Candidate %s' % (hex2base64.str2hex(candidate)))
                    if candidate in results:
                        # Not sure why this happens sometimes ...
                        # Had to add the 'while not progressed' stuff becaues of this.
                        if results[candidate][0] < 240:
                            result += chr(results[candidate][0])
                            progressed = True
                        else:
                            print('Invalid char: %s (current: %s)' % (results[candidate][0], result))
                        break
                retries += 1
            nb_chars += 1
            tot_retries += retries
            min_retries = min(retries, min_retries)
            max_retries = max(retries, max_retries)
            #print("Result: %s (%s)" % (result, hex2base64.str2hex(result)))
            sys.stdout.write(result[-1])
            sys.stdout.flush()
    end = time.time()
    print(" ========== ")
    print(result)
    print("Retries per char (min/avg/max): %s/%s/%s" % (min_retries, 1.0*tot_retries/nb_chars, max_retries))
    print("Found %s chars in %s seconds." % (nb_chars, end - begin))

def testEncoding():
    message = magic_char * 15 + 'R'
    toencode = ['9883f56eddefb349538d97b95eae2c80'
                'ef16ca0d363f00432d1a6d68e6d7d6da'
                '37dc3f88ee613c0374d87e4a3be12d96'
                '15c32d4a0fc188922c547e11ead23fca'
                'c4c92c123404e6c82973fe8037f0c4ed'
                '75ffffffffffffffffffffffffffffff'
                'ffffffffffffffffffffffffffffffff'
                'ffffffffffffffffffffffffffffff52'
                '02526f6c6c696e2720696e206d792035'
                '2e300a57697468206d79207261672d74'
                '6f7020646f776e20736f206d79206861'
                '69722063616e20626c6f770a54686520'
                '6769726c696573206f6e207374616e64'
                '627920776176696e67206a7573742074'
                '6f207361792068690a44696420796f75'
                '2073746f703f204e6f2c2049206a7573'
                '742064726f76652062790a']
    # Expect 'bae1c74ff5c04a14fff6244360623f9b'
    #for token in toencode:
    #    print(hex2base64.str2hex(cbc.cipherAES128ECB(hex2base64.hex2str(token), consistent_key)))
    print(hex2base64.str2hex(cbc.cipherAES128ECB(hex2base64.hex2str('ffffffffffffffffffffffffffff5200'), consistent_key)))
    print(hex2base64.str2hex(cbc.cipherAES128ECB(hex2base64.hex2str('ffffffffffffffffffffffffffff5203'), consistent_key)))

if __name__ == '__main__':
    #challenge11()
    #challenge12()
    challenge14()
    #testEncoding()
