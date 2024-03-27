from encryption.py import *

publicKey = [292547, 32807]
privateKey = [292547, 13163]

print(decrypt(encrypt('Hello, world', publicKey), privateKey))
print(keyCheck(publicKey, privateKey))

print(keyBruteforce(13000, 5, publicKey))
