
# 快速模幂乘算法

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


def fast_modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result


def encrypt(plaintext, public_key):
    modulus = public_key.n
    exponent = public_key.e
    hash = SHA256.new(plaintext.encode("utf-8")).digest()
    m = int.from_bytes(hash, 'big')
    return fast_modular_exponentiation(m, exponent, modulus)


key = RSA.generate(1024, e=65537)
plaintext = "hello"
ciphertext = encrypt(plaintext, key.publickey())
print(ciphertext)
