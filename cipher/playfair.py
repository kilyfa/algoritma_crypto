def create_matrix(key):
    key = ''.join(dict.fromkeys(key.upper().replace('J', 'I')))
    matrix = []
    for c in key:
        if c not in matrix:
            matrix.append(c)
    for c in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if c not in matrix:
            matrix.append(c)
    return [matrix[i*5:i*5+5] for i in range(5)]

def locate(char, matrix):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)

def process_digraphs(text):
    text = text.upper().replace('J', 'I')
    text = ''.join([c for c in text if c.isalpha()])
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) and text[i+1] != a else 'X'
        if i+1 < len(text) and text[i+1] == a:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    if len(text) % 2:
        pairs.append((text[-1], 'X'))
    return pairs

def encrypt_playfair(text, key):
    matrix = create_matrix(key)
    pairs = process_digraphs(text)
    cipher = ''
    for a, b in pairs:
        row1, col1 = locate(a, matrix)
        row2, col2 = locate(b, matrix)
        if row1 == row2:
            cipher += matrix[row1][(col1+1)%5] + matrix[row2][(col2+1)%5]
        elif col1 == col2:
            cipher += matrix[(row1+1)%5][col1] + matrix[(row2+1)%5][col2]
        else:
            cipher += matrix[row1][col2] + matrix[row2][col1]
    return cipher

def decrypt_playfair(text, key):
    matrix = create_matrix(key)
    pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    plain = ''
    for pair in pairs:
        a, b = pair
        row1, col1 = locate(a, matrix)
        row2, col2 = locate(b, matrix)
        if row1 == row2:
            plain += matrix[row1][(col1-1)%5] + matrix[row2][(col2-1)%5]
        elif col1 == col2:
            plain += matrix[(row1-1)%5][col1] + matrix[(row2-1)%5][col2]
        else:
            plain += matrix[row1][col2] + matrix[row2][col1]
    return plain