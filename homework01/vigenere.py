def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    char_possible_indexes = list(range(ord("a"), ord("z") + 1))
    char_possible_indexes.extend(range(ord("a"), ord("z") + 1))
    char_possible_indexes.extend(range(ord("A"), ord("Z") + 1))
    char_possible_indexes.extend(range(ord("A"), ord("Z") + 1))
    char_indexes = list(range(ord("A"), ord("Z") + 1))
    char_indexes.extend(range(ord("a"), ord("z") + 1))
    shift_for_char = list(range(26))
    shift_for_char.extend(range(26))
    shift = dict(zip(char_indexes, shift_for_char))
    keyword += "."
    i = 0
    for char in plaintext:
        if keyword[i] == ".":
            i = 0
        char_index = ord(char)
        if char_index in shift:
            char_index = char_possible_indexes[
                char_possible_indexes.index(char_index) + shift[ord(keyword[i])]
            ]
        char = chr(char_index)
        ciphertext += char
        i = i + 1
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    char_possible_indexes = list(range(ord("a"), ord("z") + 1))
    char_possible_indexes.extend(range(ord("a"), ord("z") + 1))
    char_possible_indexes.extend(range(ord("A"), ord("Z") + 1))
    char_possible_indexes.extend(range(ord("A"), ord("Z") + 1))
    char_possible_indexes.reverse()
    char_indexes = list(range(ord("A"), ord("Z") + 1))
    char_indexes.extend(range(ord("a"), ord("z") + 1))
    shift_for_char = list(range(26))
    shift_for_char.extend(range(26))
    shift = dict(zip(char_indexes, shift_for_char))
    keyword += "."
    i = 0
    for char in ciphertext:
        if keyword[i] == ".":
            i = 0
        char_index = ord(char)
        if char_index in shift:
            char_index = char_possible_indexes[
                char_possible_indexes.index(char_index) + shift[ord(keyword[i])]
            ]
        char = chr(char_index)
        plaintext += char
        i = i + 1
    return plaintext
