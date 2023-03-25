# 导入必要的库
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import serialization, hashes

# 生成椭圆曲线密钥对
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# 加密明文
message = b"Hello World"
signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))

# 验证签名是否有效
try:
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    print("Signature is valid")
except:
    print("Signature is invalid")
