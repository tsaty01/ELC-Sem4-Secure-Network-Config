import random
import string
import time

import matplotlib.pyplot as plt

from src.caesar import caesar_decrypt, caesar_encrypt
from src.hill import hill_decrypt, hill_encrypt
from src.playfair import (
    playfair_decrypt,
    playfair_encrypt,
)


def run_encryption_benchmark():
    print("Running encryptionbenchmarks... This may take a few seconds.")
    sizes = range(1, 20002, 500)
    
    times_caesar = []
    times_playfair = []
    times_hill = []

    # Valid Hill Key (Determinant is 5, coprime to 26)
    hill_key = "DDCF"
    playfair_key = "SECRET"

    for size in sizes:
        # Generate random uppercase string
        test_text = "".join(random.choices(string.ascii_uppercase, k=size))

        # Benchmark Caesar
        start = time.perf_counter()
        caesar_encrypt(test_text, 3)
        times_caesar.append(time.perf_counter() - start)

        # Benchmark Playfair
        start = time.perf_counter()
        playfair_encrypt(test_text, playfair_key)
        times_playfair.append(time.perf_counter() - start)

        # Benchmark Hill
        start = time.perf_counter()
        hill_encrypt(test_text, hill_key)
        times_hill.append(time.perf_counter() - start)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_caesar, marker='o', label='Caesar Cipher', linewidth=2)
    plt.plot(sizes, times_playfair, marker='s', label='Playfair Cipher', linewidth=2)
    plt.plot(sizes, times_hill, marker='^', label='Hill Cipher', linewidth=2)

    plt.title('Cipher Encryption Benchmark')
    plt.xlabel('Plaintext Length (Characters)')
    plt.ylabel('Execution Time (Seconds)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    plt.savefig('benchmark_encryption.png')
    print("Encryption benchmark complete! Graph saved as 'benchmark_encryption.png'.")
    plt.show()

def run_decryption_benchmark():
    print("Running decryption benchmarks... This may take a few seconds.")
    sizes = range(1, 20002, 500)
    
    times_caesar = []
    times_playfair = []
    times_hill = []

    # Valid Hill Key (Determinant is 9, coprime to 26)
    hill_key = "DDCF"
    playfair_key = "SECRET"

    for size in sizes:
        # 1. Generate random uppercase plaintext
        test_text = "".join(random.choices(string.ascii_uppercase, k=size))

        # 2. Pre-encrypt the text so we have valid ciphertext to decrypt
        caesar_cipher_text = caesar_encrypt(test_text, 3)
        playfair_cipher_text = playfair_encrypt(test_text, playfair_key)
        hill_cipher_text = hill_encrypt(test_text, hill_key)

        # 3. Benchmark Caesar Decryption
        start = time.perf_counter()
        caesar_decrypt(caesar_cipher_text, 3)
        times_caesar.append(time.perf_counter() - start)

        # 4. Benchmark Playfair Decryption
        start = time.perf_counter()
        playfair_decrypt(playfair_cipher_text, playfair_key)
        times_playfair.append(time.perf_counter() - start)

        # 5. Benchmark Hill Decryption
        start = time.perf_counter()
        hill_decrypt(hill_cipher_text, hill_key)
        times_hill.append(time.perf_counter() - start)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_caesar, marker='o', label='Caesar Decryption', linewidth=2)
    plt.plot(sizes, times_playfair, marker='s', label='Playfair Decryption', linewidth=2)
    plt.plot(sizes, times_hill, marker='^', label='Hill Decryption', linewidth=2)

    plt.title('Cipher Decryption Benchmark')
    plt.xlabel('Ciphertext Length (Characters)')
    plt.ylabel('Execution Time (Seconds)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    plt.savefig('benchmark_decryption.png')
    print("Decryption benchmark complete! Graph saved as 'benchmark_decryption.png'.")
    plt.show()
