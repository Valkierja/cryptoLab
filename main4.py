import hashlib

# 用于示例的待加密明文
message = "Hello World"

# 创建SHA-1哈希对象
sha1 = hashlib.sha1()

# 将消息添加到哈希对象
sha1.update(message.encode())

# 计算哈希值
hash_value = sha1.hexdigest()

# 输出哈希值
print(hash_value)
