# ECC签名 fail

import hashlib
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Util.number import long_to_bytes, bytes_to_long
import os

KEY_SIZE = 256

# Select SHA-256 as the hash function
HASH_FUNCTION = hashlib.sha256

# Define constants used in the signature and verification process
P = ECC._Curve.p
ORDER = ECC._Curve.order
Gx = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
Gy = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

# Convert the generator to Montgomery form
MONTGOMERY_GENERATOR = ECC.generate.to_montgomery()

# Generate a new ECC key pair
key = ECC.generate(curve='P-256')

# Get the private key and public key
private_key = key.d
public_key = key.public_key().export_key(format='DER')


def bytes_to_point(b: bytes) -> ECC.EccPoint:
    x = bytes_to_long(b[:KEY_SIZE])
    y = bytes_to_long(b[KEY_SIZE:])
    return ECC.EccPoint(curve=ECC.curves.NIST256, x=x, y=y)


def point_to_bytes(p: ECC.EccPoint) -> bytes:
    x = long_to_bytes(p.x, KEY_SIZE)
    y = long_to_bytes(p.y, KEY_SIZE)
    return x + y


def hash_to_point(message: bytes) -> ECC.EccPoint:
    while True:
        # Compute the hash of the message
        h = HASH_FUNCTION(message).digest()

        # Convert the hash to an ECC point
        p = bytes_to_point(h)

        # Check if the point is on the curve
        if p.curve.validate_point(p.x, p.y):
            break

    return p


def sign(private_key: int, message: bytes) -> bytes:
    # Compute the hash of the message
    h = SHA256.new(message)

    # Convert the hash to an ECC point
    p = hash_to_point(h.digest())

    # Get the Montgomery form of the point
    p_montgomery = p.to_montgomery()

    # Generate a random nonce
    k = int.from_bytes(os.urandom(KEY_SIZE), 'big')

    # Compute the nonce point
    R = ECC.NIST256.generator * k

    # Compute the x-coordinate of R in Montgomery form
    R_x = long_to_bytes(R.x, KEY_SIZE)

    # Compute the scalar s
    s = (bytes_to_long(h.digest()) + private_key * bytes_to_long(R_x) * bytes_to_long(p_montgomery.x)) % ORDER

    # Convert s to Montgomery form
    s_montgomery = pow(2, 256 * 2, ORDER)

    # Compute the signature
    signature = point_to_bytes(R) + long_to_bytes(s * s_montgomery % ORDER, KEY_SIZE)

    return signature


def verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
    # Convert the public key to an ECC object
    key = ECC.import_key(public_key)

    # Compute the hash of the message
    h = SHA256.new(message)

    # Decode the signature
    R = bytes_to_point(signature[:KEY_SIZE * 2])
    s = bytes_to_long(signature[KEY_SIZE * 2:])

    # Compute the x-coordinate of R in Montgomery form
    R_x = long_to_bytes(R.x, KEY_SIZE)
    R_x_montgomery = pow(bytes_to_long(R_x), ORDER - 2, ORDER)

    # Compute v1 and v2
    v1 = ECC.NIST256.generator * (s * R_x_montgomery % ORDER)
    v2 = key.pointQ * (bytes_to_long(h.digest()) * R_x_montgomery % ORDER)

    # Compute the point v
    v = v1 + v2

    # Check that v is equal to R
    return v.x == R.x and v.y == R.y


# Sign the message
signature = sign(private_key, b'hello world')

# Verify the signature
result = verify(public_key, b'hello world', signature)
print(result)
