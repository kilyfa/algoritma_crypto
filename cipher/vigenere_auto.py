def bersihkan(teks):
    return ''.join([c.upper() for c in teks if c.isalpha()])

def encrypt_autokey(plain, key):
    plain = bersihkan(plain)
    key = bersihkan(key) + plain
    cipher = []
    for i, c in enumerate(plain):
        shift = ord(key[i]) - ord('A')
        ch = chr(((ord(c) - ord('A') + shift) % 26) + ord('A'))
        cipher.append(ch)
    return ''.join(cipher)

def decrypt_autokey(cipher, key):
    cipher = bersihkan(cipher)
    key = bersihkan(key)
    plain = []
    for i, c in enumerate(cipher):
        shift = ord(key[i]) - ord('A')
        ch = chr(((ord(c) - ord('A') - shift + 26) % 26) + ord('A'))
        plain.append(ch)
        key += ch
    return ''.join(plain)