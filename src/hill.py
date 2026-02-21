import math
from pathlib import Path

import numpy as np

KEY_FILE = "hill_key.txt"

def hill_encrypt(plaintext: str, key: str) -> str:
    key = "".join(filter(str.isalpha, key.upper()))
    
    n = math.isqrt(len(key))
    assert n * n == len(key), "Key length must be a perfect square."

    k_matrix = np.zeros((n, n), dtype=int)
    for i, char in enumerate(key):
        k_matrix[i // n][i % n] = ord(char) - ord('A')

    det_k = round(np.linalg.det(k_matrix)) % 26
    
    # Enforce strict invertibility modulo 26
    assert math.gcd(det_k, 26) == 1, f"Key matrix determinant ({det_k}) is not coprime with 26. Use a different key."
    
    # Clean and pad plaintext so it divides evenly by n
    text = "".join(filter(str.isalpha, plaintext.upper()))
    if len(text) % n != 0:
        text += 'X' * (n - (len(text) % n))

    result = ""
    # Process the text in chunks of size n
    for i in range(0, len(text), n):
        block = text[i:i+n]
        p_matrix = np.array([ord(char) - ord('A') for char in block])
        e_matrix = (k_matrix @ p_matrix) % 26
        
        for val in e_matrix:
            result += chr(int(val) + ord('A'))

    return result


def hill_decrypt(ciphertext: str, key: str) -> str:
    key = "".join(filter(str.isalpha, key.upper()))
    
    n = math.isqrt(len(key))
    assert n * n == len(key), "Key length must be a perfect square."

    k_matrix = np.zeros((n, n), dtype=int)
    for i, char in enumerate(key):
        k_matrix[i // n][i % n] = ord(char) - ord('A')

    # Calculate Determinant and check invertibility
    det_f = round(np.linalg.det(k_matrix))
    det_k = det_f % 26
    assert math.gcd(det_k, 26) == 1, f"Key matrix is not invertible mod 26 (det={det_k})."

    # Find Modular Multiplicative Inverse
    det_inv = pow(det_k, -1, 26)

    # Calculate Adjugate Matrix
    adj_k = np.round(np.linalg.inv(k_matrix) * det_f).astype(int)

    # Calculate True Inverse Matrix Modulo 26
    inv_k = (adj_k * det_inv) % 26
    inv_k = (inv_k + 26) % 26

    text = "".join(filter(str.isalpha, ciphertext.upper()))
    assert len(text) % n == 0, "Ciphertext length must be a multiple of the matrix size."

    result = ""
    # Process the ciphertext in chunks of size n
    for i in range(0, len(text), n):
        block = text[i:i+n]
        c_matrix = np.array([ord(char) - ord('A') for char in block])
        d_matrix = (inv_k @ c_matrix) % 26
        
        for val in d_matrix:
            result += chr(int(val) + ord('A'))

    return result


def hill_load_key() -> str:
    with Path(KEY_FILE).open() as f:
        return f.readline().strip()

def hill_save_key(key: str) -> None:
    with Path(KEY_FILE).open("w") as f:
        f.write(key)