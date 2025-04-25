def encrypt_extended(data: bytes, key: str):
    key_bytes = key.encode()
    return bytes([(data[i] + key_bytes[i % len(key_bytes)]) % 256 for i in range(len(data))])

def decrypt_extended(data: bytes, key: str):
    key_bytes = key.encode()
    return bytes([(data[i] - key_bytes[i % len(key_bytes)]) % 256 for i in range(len(data))])   