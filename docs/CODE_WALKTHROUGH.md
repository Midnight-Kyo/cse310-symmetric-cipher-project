# Code walkthrough

This guide explains the current [project program](../symmetric_cipher.py). It implements a custom 16-bit cipher from the handout. The downloaded [saes.py](../saes.py) performs key expansion only. Its own encryption methods are not used by our cipher.

One byte is eight bits. One project block is sixteen bits, or two bytes. `0x` marks a hexadecimal number; `0x82e` and `082E` represent the same value. Leading zeros fill the four-digit block display.

## Imports

```python
import numpy as np
from BitVector import BitVector
from saes import SimplifiedAES
```

NumPy builds tables and reads ID bytes into blocks. BitVector rearranges bits. `SimplifiedAES` is the third-party key-expansion implementation bundled in the repository.

## S-box generation

```python
rng = np.random.default_rng(310)
SBOXES = [rng.permutation(256) for _ in range(10)]
INVERSES = [np.argsort(box) for box in SBOXES]
```

The fixed seed repeats the same public tables each run. It is separate from the encryption key. `permutation(256)` shuffles all byte values without repetition. We create ten tables. `argsort` produces the inverse tables: if a table maps `31` to `63`, its inverse maps `63` back to `31`.

The four `PATTERNS` lists come from the handout. The subtraction below changes positions numbered 1–16 into Python positions 0–15:

```python
PATTERNS = [[position - 1 for position in row] for row in PATTERNS]
```

## Key expansion

```python
def expand_key(key):
    keys = []
    for _ in range(2):
        library = SimplifiedAES(key)
        keys += [library.state_to_int(library.round1_key),
                 library.state_to_int(library.round2_key)]
        key = keys[-1]
    return keys
```

Start an empty list and call the module twice. Each call generates two keys. The module's `state_to_int` converts its key representation into an ordinary integer. `keys[-1]` is the last key generated; it becomes the second call's input.

For input `2D55`, call 1 gives `BCE9, A34A`. Call 2 uses `A34A` and gives `2E64, C6A2`. Each call restarts constants `80, 30`. This is our documented adaptation to the assignment's four-key requirement.

## S-box selection

```python
def box_indices(subkey):
    reversed_key = int(BitVector(intVal=subkey, size=16).reverse())
    return subkey % 10, reversed_key % 10
```

BitVector reverses the sixteen bits, including leading zeros. Modulo 10 selects an index from 0–9. The normal subkey selects the left table; its reversed bits select the right table.

## Substitution

```python
def substitute(block, boxes, left_index, right_index):
    left = int(boxes[left_index][block >> 8])
    right = int(boxes[right_index][block & 255])
    return (left << 8) | right
```

`block >> 8` gets the left byte. `block & 255` gets the right byte. Each byte is replaced using its selected S-box, then the final line joins the replacement bytes. In the first round, `0010` splits into `00` and `10`; S1 and S7 give `9D` and `D4`, making `9DD4`.

## Encrypting one block

```python
def encrypt_block(block, key):
    for pattern, subkey in zip(PATTERNS, expand_key(key)):
        a, b = box_indices(subkey)
        block = substitute(block, SBOXES, a, b)
        block = int(BitVector(intVal=block, size=16).permute(pattern))
        block = block ^ subkey
    return block
```

1. `zip` pairs each of the four patterns with its round key, giving four loop passes.
2. `box_indices` selects the left and right S-boxes.
3. `substitute` replaces the two bytes.
4. BitVector shuffles the sixteen bits using the current pattern. `int` returns the result as a number.
5. `^` XORs the shuffled block with the round key. Equal bits give 0; different bits give 1.
6. The updated block enters the next round. After four rounds, the returned block is the ciphertext.

A presentation explanation: “Each round selects two S-boxes, substitutes the bytes, shuffles the bits and XORs the result with its round key. We repeat that four times.”

## Decrypting one block

```python
def decrypt_block(block, key):
    keys = expand_key(key)
    for round_number in range(3, -1, -1):
        subkey = keys[round_number]
        a, b = box_indices(subkey)
        shuffled = BitVector(intVal=block ^ subkey, size=16)
        block = substitute(int(shuffled.unpermute(PATTERNS[round_number])), INVERSES, a, b)
    return block
```

The loop uses positions 3, 2, 1, 0, meaning rounds 4 back to 1. XOR the key again, undo the permutation, then use inverse S-boxes. The result recovers the plaintext.

## Encrypting a complete ID

```python
def encrypt_id(student_id, key, iv=0):
    """Encrypt a numeric student ID as two 16-bit blocks."""
    data = student_id.to_bytes(4, "big")  # Keep the whole number; pad on the left.
    ciphertext = []
    previous = iv
    for block in np.frombuffer(data, dtype=">u2"):  # Read pairs of bytes.
        previous = encrypt_block(int(block) ^ previous, key)
        ciphertext.append(previous)
    return ciphertext
```

The input is the entire ID as an integer. `student_id.to_bytes(4, "big")` writes that number in four bytes, most significant byte first. Leading zero bits fill the 32-bit space. This is numeric formatting, with no ASCII conversion and no extra padding byte.

For Wahab, `1098271` is hexadecimal `0010C21F`; the two blocks are `0010` and `C21F`. Faisal's `1075075` is `00106783`, giving `0010` and `6783`. We do not split the decimal digits into pairs.

`ciphertext` stores the results. `previous` initially holds demonstration IV `0000`. NumPy's `>u2` reads pairs of bytes as 16-bit unsigned numbers, most significant byte first.

Before the four rounds, XOR the current block with the preceding ciphertext. The first block uses the IV instead. Save each completed ciphertext for the next block. This is CBC chaining.

```text
Block 1: 0010 XOR 0000 = 0010; encrypt to 082E.
Block 2: C21F XOR 082E = CA31; encrypt to 41B9.
```

The returned list contains two encrypted blocks. Decrypting them and recombining the recovered numeric blocks gives the complete original ID.

## The demonstration section

`if __name__ == "__main__":` runs the demonstration when this file is executed directly. Importing its functions does not automatically run the demo. This condition contributes nothing to encryption.

The demo chooses key `2D55` and plaintext `0010` (the first numeric ID block), prints the round keys, encrypts and decrypts the example, then encrypts both complete IDs. `hex()` only formats output.

For the tests, `plaintext ^ 1` flips the plaintext's rightmost bit, while `key ^ 1` flips the key's rightmost bit. Each changed case is encrypted separately. The expression below counts differing output positions:

```python
count = (original ^ changed).bit_count()
```

The results are 7 changed bits for the plaintext test and 9 for the key test. The report computes the percentages as `changed bits / 16 * 100`.
