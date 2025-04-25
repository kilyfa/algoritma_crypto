def mod_inverse(a, m):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None

def encrypt_affine(plain, a, b):
    plain = ''.join([c.upper() for c in plain if c.isalpha()])
    return ''.join([chr(((a * (ord(c) - 65) + b) % 26) + 65) for c in plain])

def decrypt_affine(cipher, a, b):
    cipher = ''.join([c.upper() for c in cipher if c.isalpha()])
    a_inv = mod_inverse(a, 26)
    return ''.join([chr(((a_inv * ((ord(c) - 65) - b)) % 26) + 65) for c in cipher])