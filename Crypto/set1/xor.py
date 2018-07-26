import hex2base64

alphabet = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
punctuation = ' .,?!;:\'"\n()'
valid = alphabet + alphabet.upper() + digits + punctuation

# French
frequents = 'eaisnrtoludc'
infrequents = 'bfghjkmpqvwxyz'
# English
frequents = 'etaoinshrdlu'
infrequents = 'bcfgjkmpqvwxyz'

def str2hex(content):
    return "".join([c.encode("hex") for c in content])

def hex2str(content):
    result = ""
    for i in range(len(content)/2):
        hexbyte = content[2*i:2*(i+1)]
        byte = int(hexbyte, 16)
        result += chr(byte)
    return result

def xorStr(content, key):
    if len(key) == 0:
        raise ValueError("Empty key !")
    result = ""
    i = 0
    for c in content:
        result += chr(ord(c) ^ ord(key[i]))
        i = (i+1) % len(key)
    return result

def xorHex(content, key):
    return str2hex(xorStr(hex2str(content), hex2str(key)))

def countChars(content):
    stats = {}
    for lc in alphabet:
        stats[lc] = 0
    for c in content:
        lc = c.lower()
        if lc not in alphabet:
            continue
        stats[lc] += 1
    return stats

def englishScore(stats):
    score = 0
    for l1 in infrequents:
        for l2 in frequents:
            if stats[l1] < stats[l2]:
                score += 1
    for i in range(0, len(frequents)):
        for j in range(i, len(frequents)):
            if stats[frequents[i]] > stats[frequents[j]]:
                score += 1
    return score

def textScore(content):
    score = 0
    for c in content:
        if c in valid:
            score += 10
        else:
            score -= 50
    return score

def tryKeysHex(content):
    max_score = -1000000000
    good_key = ""
    result = ""
    for k in range(0, 255): 
        key = "%0.2X" % k
        #print("key: %s" % key)
        attempt = hex2str(xorHex(content, key))
        score = textScore(attempt)
        score += englishScore(countChars(attempt))
        #print("%s -> %s" % (k, score))
        #print("%s\t%s -> %s" % (k, attempt, score))
        if score > max_score:
            #print("%s\t%s -> %s" % (k, attempt, score))
            max_score = score
            result = attempt
            good_key = key
    #print("%s\t%s -> %s" % (good_key, result, max_score))
    #print("%s - %s" % (good_key, max_score))
    return (result, good_key, max_score)

def tryKeysStr(content):
    #print("tryKeysStr(%s)" % content)
    return tryKeysHex(str2hex(content))

def isSingleLetterXor(content):
    result, key, score = tryKeysHex(content)
    if score > 5*len(content):
        #print("Result: %s -> %s", (content, result))
        return True
    return False

def breakMultipleKeyXor(content, keysizes):
    final_result = ""
    final_key = ""
    max_score = 0
    #print("breakMultipleKeyXor(%s)" % content)
    for i in keysizes:
        print("Trying with key of length %s" % i)
        i_score = 0
        i_result = []
        i_key = []
        for j in range(0, i):
            result, key, score = tryKeysStr(content[j::i])
            i_score += score
            i_key.append(key)
            i_result.append(result)
        if i_score > max_score:
            max_score = i_score
            final_key = "".join(i_key)
            final_result = "".join(["".join(x) for x in zip(*i_result)])
            #print("Result: %s (score = %s, key = %s)" % (final_result, max_score, final_key))
    return final_result, final_key, max_score

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

def findKeySizeXor(content):
    min_d = 1000000000
    max_keysize = min(len(content)/10, 50)
    result = []
    for keysize in range(1, max_keysize):
        score = 0
        for i in range(1, 2):
            score += hammingDistance(content[i*keysize:(i+1)*keysize], content[(i+1)*keysize:(i+2)*keysize])
        score = 1.0*score/keysize
        result.append((keysize, score))
    return sorted(result, key=lambda(x): x[1])

def main():
    to_decrypt = ("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")

    cyphered = hex2base64.base642str(to_decrypt)

    keysize_scores = findKeySizeXor(cyphered)

    final_result, final_key, max_score = breakMultipleKeyXor(cyphered, [x[0] for x in keysize_scores[:5]])
    print("Result: %s (score = %s, key = %s)" % (final_result, max_score, hex2str(final_key)))

if __name__ == '__main__':
    main()
