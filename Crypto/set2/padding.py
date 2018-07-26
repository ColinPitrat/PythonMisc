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

