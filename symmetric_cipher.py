"""Four-round student cipher. Run: python symmetric_cipher.py
Install the two libraries first: python -m pip install -r requirements.txt
"""
import numpy as np
from BitVector import BitVector
# Unchanged MIT-licensed module from https://github.com/mayank-02/simplified-aes
# Bundled as saes.py with its original license in SAES_LICENSE.txt.
from saes import SimplifiedAES

# NumPy builds ten reproducible 8-bit S-boxes and their inverse tables.
rng = np.random.default_rng(310)
SBOXES = [rng.permutation(256) for _ in range(10)]
INVERSES = [np.argsort(box) for box in SBOXES]
PATTERNS = [
    [6, 8, 1, 2, 4, 3, 5, 7, 12, 16, 9, 10, 14, 15, 13, 11],
    [9, 10, 1, 3, 5, 7, 11, 13, 2, 4, 6, 8, 12, 14, 15, 16],
    [3, 5, 7, 9, 11, 13, 15, 1, 2, 4, 6, 8, 10, 12, 14, 16],
    [16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
]
PATTERNS = [[position - 1 for position in row] for row in PATTERNS]


def expand_key(key):
    """Call the S-AES module twice, feeding K2 into the second call."""
    keys = []
    for _ in range(2):
        library = SimplifiedAES(key)  # The module performs key expansion here.
        keys += [library.state_to_int(library.round1_key),
                 library.state_to_int(library.round2_key)]
        key = keys[-1]
    return keys


def box_indices(subkey):
    bits = BitVector(intVal=subkey, size=16)
    reversed_bits = bits.reverse()
    reversed_key = int(reversed_bits)
    return subkey % 10, reversed_key % 10


def substitute(block, boxes, left_index, right_index):
    left_byte = block >> 8
    left_box = boxes[left_index]
    left = int(left_box[left_byte])

    right_byte = block & 255
    right_box = boxes[right_index]
    right = int(right_box[right_byte])

    return (left << 8) | right


def encrypt_block(block, key):
    for pattern, subkey in zip(PATTERNS, expand_key(key)):
        a, b = box_indices(subkey)
        block = substitute(block, SBOXES, a, b)
        block = int(BitVector(intVal=block, size=16).permute(pattern))
        block = block ^ subkey
    return block


def decrypt_block(block, key):
    keys = expand_key(key)
    for round_number in range(3, -1, -1):
        subkey = keys[round_number]
        a, b = box_indices(subkey)
        shuffled = BitVector(intVal=block ^ subkey, size=16)
        block = substitute(int(shuffled.unpermute(PATTERNS[round_number])), INVERSES, a, b)
    return block


def encrypt_id(student_id, key, iv=0):
    """Encrypt a numeric student ID as two 16-bit blocks."""
    data = student_id.to_bytes(4, "big")  # Keep the whole number; pad on the left.
    ciphertext = []
    previous = iv
    for block in np.frombuffer(data, dtype=">u2"):  # Read pairs of bytes.
        previous = encrypt_block(int(block) ^ previous, key)
        ciphertext.append(previous)
    return ciphertext


if __name__ == "__main__":
    key, plaintext = 0x2D55, 0x0010  # First 16-bit block of either numeric ID.
    original = encrypt_block(plaintext, key)
    print("Round keys:", [hex(k) for k in expand_key(key)])
    print("Ciphertext:", hex(original))
    print("Decrypted:", hex(decrypt_block(original, key)))

    for student_id in [1098271, 1075075]:
        print(student_id, [hex(c) for c in encrypt_id(student_id, key)])

    for label, p, k in [("Plaintext bit 0", plaintext ^ 1, key), ("Key bit 0", plaintext, key ^ 1)]:
        changed = encrypt_block(p, k)
        count = (original ^ changed).bit_count()
        print(label, hex(changed), count, "/ 16 bits changed")
