import numpy as np

from cipher.affine import mod_inverse

def mod26_inv(matrix):
    det = int(round(np.linalg.det(matrix)))
    det_inv = mod_inverse(det % 26, 26)
    if det_inv is None:
        raise ValueError("Matrix is not invertible")
    adjugate = np.round(det * np.linalg.inv(matrix)).astype(int) % 26
    return (det_inv * adjugate) % 26

def prepare_text(text, block_size):
    text = ''.join([c.upper() for c in text if c.isalpha()])
    while len(text) % block_size != 0:
        text += 'X'
    return text

def text_to_matrix(text, size):
    return np.array([[ord(c) - 65 for c in text[i:i+size]] for i in range(0, len(text), size)])

def matrix_to_text(matrix):
    return ''.join([chr(c % 26 + 65) for row in matrix for c in row])

def encrypt_hill(text, key_matrix):
    size = key_matrix.shape[0]
    text = prepare_text(text, size)
    text_matrix = text_to_matrix(text, size)
    result = (np.dot(text_matrix, key_matrix) % 26)
    return matrix_to_text(result)

def decrypt_hill(cipher, key_matrix):
    size = key_matrix.shape[0]
    cipher_matrix = text_to_matrix(cipher, size)
    key_inv = mod26_inv(key_matrix)
    result = (np.dot(cipher_matrix, key_inv) % 26)
    return matrix_to_text(result)
