"""Caesar cipher implementation."""

from pathlib import Path

KEY_FILE = "caesar_key.txt"

def caesar_encrypt(text: str, shift: int = 3) -> str:
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def caesar_decrypt(text: str, shift: int = 3) -> str:
    return caesar_encrypt(text, -shift)

def caesar_load_key() -> int:
    with Path(KEY_FILE).open() as f:
        return int(f.readline().strip())

def caesar_save_key(shift: int) -> None:
    with Path(KEY_FILE).open("w") as f:
        f.write(str(shift))
