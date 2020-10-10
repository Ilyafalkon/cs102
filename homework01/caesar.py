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
    for char in plaintext :
        char_index = ord(char)
        char_possible_indexes = list(range(65, 91)) 
        char_possible_indexes.extend(range(65, 91))
        char_possible_indexes.extend(range(97, 123))
        char_possible_indexes.extend(range(97, 123))
        if ( char_index in char_possible_indexes ) :
            char_index = char_possible_indexes[char_possible_indexes.index(char_index)+shift%26]
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
    for char in ciphertext :
        char_index = ord(char)
        char_possible_indexes = list(range(65, 91)) 
        char_possible_indexes.extend(range(65, 91))
        char_possible_indexes.extend(range(97, 123))
        char_possible_indexes.extend(range(97, 123))
        char_possible_indexes.reverse()
        if ( char_index in char_possible_indexes ) :
            char_index = char_possible_indexes[char_possible_indexes.index(char_index)+shift%26]
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
