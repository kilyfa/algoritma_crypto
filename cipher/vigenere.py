def clean_text(text):
    return ''.join([c.upper() for c in text if c.isalpha()])

def encrypt(plain_text, key):
    plain_text = clean_text(plain_text)
    key = clean_text(key)
    cipher_text = ''
    for i in range(len(plain_text)):
        shift = ord(key[i % len(key)]) - ord('A')
        ch = chr(((ord(plain_text[i]) - ord('A') + shift) % 26) + ord('A'))
        cipher_text += ch
    return cipher_text

def decrypt(cipher_text, key):
    cipher_text = clean_text(cipher_text)
    key = clean_text(key)
    plain_text = ''
    for i in range(len(cipher_text)):
        shift = ord(key[i % len(key)]) - ord('A')
        ch = chr(((ord(cipher_text[i]) - ord('A') - shift + 26) % 26) + ord('A'))
        plain_text += ch
    return plain_text
