def pad(content, blocksize, char):
    while len(content) % blocksize != 0:
        content += char
    return content

def pad2(content, blocksize, char):
    exceed = len(content) % blocksize
    missing = 0
    if exceed > 0:
        missing = blocksize - exceed
    return content + missing * char

def pkcs7_pad(content, blocksize):
    excess = blocksize - (len(content) % blocksize)
    if excess == 0:
        excess = blocksize
    return content + chr(excess) * excess

def pkcs7_unpad(content):
    excess = ord(content[-1])
    for c in content[-excess:]:
        if c != chr(excess):
            raise ValueError("Invalid padding")
    return content[:-excess]
