import cbc
import oracle

def parse(args):
    result = {}
    for token in args.split('&'):
        parts = token.split('=')
        if len(parts) < 2:
            continue
        result[parts[0]] = parts[1]
    return result

def profile_for(address):
    address = address.replace('=', '').replace('&', '')
    return "email=%s&uid=10&role=user" % address

def encryptProfile(address, key):
    profile = profile_for(address)
    return cbc.cipherAES128ECB(profile, key)

def decryptProfile(encrypted, key):
    return parse(cbc.decipherAES128ECB(encrypted, key))

key = oracle.generate_key(16)

ep1 = encryptProfile('fo@bar.comadmin', key)
print(len(ep1))
print(cbc.decipherAES128ECB(ep1[0:16], key))
print(cbc.decipherAES128ECB(ep1[16:32], key))
print(cbc.decipherAES128ECB(ep1[32:48], key))
ep2 = encryptProfile('fo123@bar.com', key)
print(len(ep2))
print(cbc.decipherAES128ECB(ep2[0:16], key))
print(cbc.decipherAES128ECB(ep2[16:32], key))
print(cbc.decipherAES128ECB(ep2[32:48], key))
ep = ep2[0:32] + ep1[16:32]
print(len(ep))
print(cbc.decipherAES128ECB(ep[0:16], key))
print(cbc.decipherAES128ECB(ep[16:32], key))
print(cbc.decipherAES128ECB(ep[32:48], key))
print(cbc.decipherAES128ECB(ep, key))
print(decryptProfile(ep, key))
