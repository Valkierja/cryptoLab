# 素性检验

import sympy
from random import randint


def isPrime(n):
    if n <= 1: return False
    if n <= 3: return True

    # 使用费马小定理进行素性测试
    for i in range(5):
        a = randint(2, n - 2)
        if sympy.gcd(a, n) != 1:
            return False
        if pow(a, n - 1, n) != 1:  # (a**(n-1) % n) 可以被 pow(a, n-1, n) 替代
            return False

    # 判断是否为二次探测质数，若不是则返回False
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for i in range(5):
        a = randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for r in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    # 经过费马小定理和二次探测，可以判定这是一个大素数
    return True


if __name__ == '__main__':
    n = 0xe5a111a219c64f841669400f51a54dd4e75184004f0f4d21c6ae182cfb528652a02d6d677a72b564c505b1ed42a0c648dbfe14eb66b04c0d60ba3872826c32e7
    print("test number:")
    print(n)
    print("is prime:", isPrime(n))
    n = 2 ** 1024 + 12345
    print("test number:")
    print(n)
    print("is prime:", isPrime(n))
    n = 2358844673868679381600590880805069763225666654546099466492785129471426300391477638650452104531086818456229111862613934070073736716542800102989402734485431
    print("test number:")
    print(n)
    print("is prime:", isPrime(n))
    n = 1797693134862315913401877703488012355873160854485161786242595650070551723742690779190398182123923740479930496231938852772716192958344125863471868188558560880640307606963134388958815624679643568700740676582198660149194895685976867141660278102823189026692
    print("test number:")
    print(n)
    print("is prime:", isPrime(n))
