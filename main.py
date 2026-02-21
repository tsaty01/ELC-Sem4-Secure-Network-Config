import argparse
from pathlib import Path

from src.bench import run_decryption_benchmark, run_encryption_benchmark
from src.caesar import caesar_decrypt, caesar_encrypt, caesar_load_key, caesar_save_key
from src.hill import hill_decrypt, hill_encrypt, hill_load_key, hill_save_key
from src.playfair import (
    playfair_decrypt,
    playfair_encrypt,
    playfair_load_key,
    playfair_save_key,
)


def main():
    parser = argparse.ArgumentParser(description="Cryptographic Cipher Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    caesar_parser = subparsers.add_parser("caesar", help="use Caesar Cipher")
    caesar_parser.add_argument("--encrypt", action="store_true", help="Encrypt the input text")
    caesar_parser.add_argument("--decrypt", action="store_true", help="Decrypt the input text")
    caesar_parser.add_argument("--input", type=argparse.FileType('r'), help="Input file to perform the operation on")

    playfair_parser = subparsers.add_parser("playfair", help="use Playfair Cipher")
    playfair_parser.add_argument("--encrypt", action="store_true", help="Encrypt the input text")
    playfair_parser.add_argument("--decrypt", action="store_true", help="Decrypt the input text")
    playfair_parser.add_argument("--input", type=argparse.FileType('r'), help="Input file to perform the operation on")

    hill_parser = subparsers.add_parser("hill", help="use Hill Cipher")
    hill_parser.add_argument("--encrypt", action="store_true", help="Encrypt the input text")
    hill_parser.add_argument("--decrypt", action="store_true", help="Decrypt the input text")
    hill_parser.add_argument("--input", type=argparse.FileType('r'), help="Input file to perform the operation on")

    subparsers.add_parser("bench", help="Benchmark ciphers and generate a graph")

    args = parser.parse_args()

    if args.command == "bench":
        run_encryption_benchmark()
        run_decryption_benchmark()
        return

    if not args.command:
        parser.print_help()
        return

    result = ""
    text = None
    output_file = None
    if args.input:
        text = args.input.read()
        output_file = f"{args.command}_output.txt"

    if args.command == "caesar":
        if args.encrypt:
            if not text:
                text = input("[CAESAR] Enter plaintext to encrypt: ")
            shift = int(input("[CAESAR] Enter shift value: "))
            result = caesar_encrypt(text, shift)
            caesar_save_key(shift)
        elif args.decrypt:
            if not text:
                text = input("[CAESAR] Enter ciphertext to decrypt: ")
            shift = caesar_load_key()
            result = caesar_decrypt(text, shift)
    elif args.command == "playfair":
        if args.encrypt:
            if not text:
                text = input("[PLAYFAIR] Enter plaintext to encrypt: ")
            key = input("[PLAYFAIR] Enter key (only alpha): ")
            result = playfair_encrypt(text, key)
            playfair_save_key(key)
        elif args.decrypt:
            if not text:
                text = input("[PLAYFAIR] Enter ciphertext to decrypt: ")
            key = playfair_load_key()
            result = playfair_decrypt(text, key)
    elif args.command == "hill":
        try:
            if args.encrypt:
                if not text:
                    text = input("[HILL] Enter plaintext to encrypt: ")
                key = input("[HILL] Enter key (only alpha, perfect square length): ")
                result = hill_encrypt(text, key)
                hill_save_key(key)
            elif args.decrypt:
                if not text:
                    text = input("[HILL] Enter ciphertext to decrypt: ")
                key = hill_load_key()
                result = hill_decrypt(text, key)
        except Exception as e:
            print(f"Error: {e}")
            raise
            return

    if output_file:
        with Path(output_file).open("w") as f:
            f.write(result)
    else:
        print(f"Output: {result}")

if __name__ == "__main__":
    main()