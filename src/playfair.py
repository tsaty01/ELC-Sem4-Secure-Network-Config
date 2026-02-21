"""Playfair cipher implementation."""

from pathlib import Path

KEY_FILE = "playfair_key.txt"

def _generate_playfair_grid(key: str) -> str:
    """Helper function to build the 25-character Playfair grid."""
    # Clean the key: uppercase, keep only letters, treat J as I
    clean_key = "".join(filter(str.isalpha, key.upper())).replace("J", "I")
    
    grid = ""
    # Standard alphabet without J
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    
    # Add unique letters from the key, then fill with remaining alphabet
    for char in clean_key + alphabet:
        if len(grid) == 25:
            break
        if char not in grid:
            grid += char
            
    return grid


def playfair_encrypt(plaintext: str, key: str) -> str:
    grid = _generate_playfair_grid(key)
    
    text = "".join(filter(str.isalpha, plaintext.upper())).replace("J", "I")
    pairs = []
    i = 0
    while i < len(text):
        if i == len(text) - 1:
            pairs.append(text[i] + 'X')
            i += 1
        elif text[i] == text[i+1]:
            pairs.append(text[i] + 'X')
            i += 1
        else:
            pairs.append(text[i] + text[i+1])
            i += 2
            
    result = ""
    for a, b in pairs:
        row_a, col_a = divmod(grid.index(a), 5)
        row_b, col_b = divmod(grid.index(b), 5)
        
        # Rule 1: Same Row - Shift right
        if row_a == row_b:
            result += grid[row_a * 5 + (col_a + 1) % 5]
            result += grid[row_b * 5 + (col_b + 1) % 5]
            
        # Rule 2: Same Column - Shift down
        elif col_a == col_b:
            result += grid[((row_a + 1) % 5) * 5 + col_a]
            result += grid[((row_b + 1) % 5) * 5 + col_b]
            
        # Rule 3: Rectangle - Swap corners horizontally
        else:
            result += grid[row_a * 5 + col_b]
            result += grid[row_b * 5 + col_a]
            
    return result


def playfair_decrypt(ciphertext: str, key: str) -> str:
    # Decryption assumes the ciphertext is already correctly formatted
    grid = _generate_playfair_grid(key)
    result = ""
    
    # Process ciphertext in pairs
    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i]
        b = ciphertext[i+1]
        
        row_a, col_a = divmod(grid.index(a), 5)
        row_b, col_b = divmod(grid.index(b), 5)
        
        # Reverse Rule 1: Same Row - Shift left
        if row_a == row_b:
            result += grid[row_a * 5 + (col_a - 1) % 5]
            result += grid[row_b * 5 + (col_b - 1) % 5]
            
        # Reverse Rule 2: Same Column - Shift up
        elif col_a == col_b:
            result += grid[((row_a - 1) % 5) * 5 + col_a]
            result += grid[((row_b - 1) % 5) * 5 + col_b]
            
        # Reverse Rule 3: Rectangle - Swap corners horizontally (Exactly the same as encryption)
        else:
            result += grid[row_a * 5 + col_b]
            result += grid[row_b * 5 + col_a]
            
    return result

def playfair_load_key() -> str:
    with Path(KEY_FILE).open() as f:
        return f.readline().strip()

def playfair_save_key(key: str) -> None:
    with Path(KEY_FILE).open("w") as f:
        f.write(key)