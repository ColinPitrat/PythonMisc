import cbc
import hex2base64
import oracle
import padding

aes_key = oracle.generate_key(16)
my_iv = oracle.generate_key(16)

def encryptURL(content):
    prefix = "comment1=cooking%20MCs;userdata="
    suffix = ";comment2=%20like%20a%20pound%20of%20bacon"
    content = content.replace(';', '%3B').replace('=', '%3D')
    #iv = oracle.generate_key(16)
    iv = my_iv
    return iv, cbc.cipherAES128CBC(padding.pkcs7_pad(prefix + content + suffix, 16), aes_key, iv)

def isAdminDecrypted(content):
    for var in content.split(';'):
        tokens = var.split('=')
        if len(tokens) != 2:
            continue
        if tokens[0] == 'admin' and tokens[1] == 'true':
            return True
    return False

def isAdmin(content, iv):
    decrypted = cbc.decipherAES128CBC(content, aes_key, iv)
    return isAdminDecrypted(decrypted)

def patchChar(content, index, newvalue):
    return content[0:index] + newvalue + content[index+1:]

def xorChar(content, index, operand):
    return content[0:index] + chr(ord(content[index]) ^ operand) + content[index+1:]

data = "_admin_true"
iv, result = encryptURL(data)

print(hex2base64.str2hex(result))
print(cbc.decipherAES128CBC(result, aes_key, iv))

# From _ (111011) to ; (1011111)
#  111011
# 1011111
# 1100100 (0x64)
result = xorChar(result, 16, 0x64)
# From _ (111011) to = (1100001)
#  111101
# 1011111
# 1100010 (0x62)
result = xorChar(result, 22, 0x62)
print("=====")
print(hex2base64.str2hex(result))
print(cbc.decipherAES128CBC(result, aes_key, iv))

print("Is admin: %s" % isAdmin(result, iv))
