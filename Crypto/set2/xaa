def numToB64Char(num):
    if not isinstance(num, int):
        raise TypeError("Invalid input type for numToB64Char: %s (%s)" % (num, type(num)))
    if num < 0:
        raise ValueError("Invalid B64 num: %s" % num)
    if num < 26:
        return chr(ord('A') + num)
    if num < 52:
        return chr(ord('a') + (num-26))
    if num < 62:
        return chr(ord('0') + (num-52))
    if num == 62:
        return '+'
    if num == 63:
        return '/'
    raise ValueError("Invalid B64 num: %s" % num)

def b64CharToNum(char):
    if char >= 'A' and char <= 'Z':
        return ord(char) - ord('A')
    if char >= 'a' and char <= 'z':
        return ord(char) - ord('a') + 26
    if char >= '0' and char <= '9':
        return ord(char) - ord('0') + 52
    if char == '+':
        return 62
    if char == '/':
        return 63
    raise ValueError("Invalid B64 char: %s" % char)

def hex2str(content):
    result = ""
    for i in range(len(content)/2):
        hexbyte = content[2*i:2*(i+1)]
        byte = int(hexbyte, 16)
        result += chr(byte)
    return result

def str2hex(content):
    return "".join([c.encode("hex") for c in content])

def hex2base64(content):
    result = ""
    bit_idx = 0
    while bit_idx < len(content)*4:
        byte_idx = bit_idx / 8
        shift = bit_idx % 8
        byte1 = int(content[2*byte_idx:2*(byte_idx+1)], 16)
        try:
            byte2 = int(content[2*(byte_idx+1):2*(byte_idx+2)], 16)
        except:
            byte2 = 0
        if shift > 2:
            val = (byte1 << (shift-2)) | (byte2 >> (8-shift+2))
        else:
            val = byte1 >> (2-shift)
        val = val & 0x3F
        result += numToB64Char(val)
        bit_idx += 6
    padding = len(result)%4 
    if padding != 0:
        result += '=' * (4-padding)
    return result

def str2base64(content):
    return hex2base64(str2hex(content))

def base642str(content):
    result = ""
    bit_idx = 0
    b1 = 0
    b2 = 0
    for c in content:
        if c == '=':
            break
        if bit_idx == 0:
            b1 = b64CharToNum(c) << 2
        if bit_idx == 6:
            b1 |= b64CharToNum(c) >> 4
            b2 = b64CharToNum(c) << 4
        if bit_idx == 4:
            b1 = b2
            b1 |= b64CharToNum(c) >> 2
            b2 = b64CharToNum(c) << 6
        if bit_idx == 2:
            b1 = b2
            b1 |= b64CharToNum(c)
        if bit_idx != 0:
            result += chr(b1 & 0xFF)
        bit_idx = (bit_idx + 6) % 8
    return result
