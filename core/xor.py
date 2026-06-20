def xor(text: bytes, key: bytes) -> bytes:
    return bytes(text[i] ^ key[i % len(key)] for i in range(len(text)))