import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    char_possible_indexes = list(range(ord("a"), ord("z") + 1))
    char_possible_indexes.extend(range(ord("a"), ord("z") + 1))
    char_possible_indexes.extend(range(ord("A"), ord("Z") + 1))
    char_possible_indexes.extend(range(ord("A"), ord("Z") + 1))
    for char in plaintext:
        char_index = ord(char)
        if char_index in char_possible_indexes:
            char_index = char_possible_indexes[char_possible_indexes.index(char_index) + shift % 26]
        char = chr(char_index)
        ciphertext += char

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    char_possible_indexes = list(range(ord("a"), ord("z") + 1))
    char_possible_indexes.extend(range(ord("a"), ord("z") + 1))
    char_possible_indexes.extend(range(ord("A"), ord("Z") + 1))
    char_possible_indexes.extend(range(ord("A"), ord("Z") + 1))
    char_possible_indexes.reverse()
    for char in ciphertext:
        char_index = ord(char)
        if char_index in char_possible_indexes:
            char_index = char_possible_indexes[char_possible_indexes.index(char_index) + shift % 26]
        char = chr(char_index)
        plaintext += char
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
