# Presentation slides and speaking notes

This is a text copy of the nine-slide presentation, updated for numeric ID input. The editable PowerPoint is [here](Symmetric_Algorithm_Presentation.pptx).

## Slide 1

Slide content:

A New Symmetric Algorithm

A custom 16-bit cipher with four rounds

Wahab Yaseen Dawod  1098271

Faisal Saud Al Maamari  1075075

CSE 310   Introduction to Cryptography

Section 101   Dr Moatsum Alawida

Speaking notes:

Wahab: We will explain our four-round cipher, trace one example, and show what happens when we change one bit. Faisal will explain the Python program and the test results. This is a classroom design with a small key, so we do not use it for real data protection.

## Slide 2

Slide content:

Cipher structure

Custom 16-bit block cipher. Four rounds. Ten fixed S-boxes.

Plaintext

Round 1

Round 2

Round 3

Round 4

Ciphertext

Inside each round

Substitute two bytes

Shuffle 16 bits

XOR round key

Key expansion supplies one 16-bit key to each round.

Speaking notes:

Wahab: This is the custom cipher described in our project handout. We borrow S-AES key expansion. Our block encryption follows the handout's four-round substitution, permutation and XOR rules. The block is two bytes. Substitution changes each byte through its selected S-box. Permutation moves bits using a supplied pattern. XOR combines the result with a round key. NumPy creates ten S-boxes and their inverses once with seed 310. Our small wrapper calls the downloaded S-AES module twice for four keys. The report contains the full flowchart and pseudocode.

## Slide 3

Slide content:

Four round keys

Two calls to the S-AES module generate four 16-bit round keys.

| Library call | Input key | Generated key |
| --- | --- | --- |
| 1 | 2D55 | BCE9 |
| 1 | 2D55 | A34A |
| 2 | A34A | 2E64 |
| 2 | A34A | C6A2 |

The second call uses the last key from the first call.

Speaking notes:

Wahab: We reuse Mayank Jain's Simplified AES module for key expansion. Calling SimplifiedAES with secret key 2D55 generates BCE9 and A34A. Then we call it again using A34A as the input key. That gives 2E64 and C6A2. We keep all four generated round keys. The small wrapper only calls the module and converts its state arrays into integers. Each call uses round constants 80 and 30, so the sequence is 80, 30, 80, 30. This is our two-stage schedule for the project. Inside the module, S-AES swaps nibbles, substitutes them and uses XOR. For the manual example, 2D XOR 11 XOR 80 gives BC, and 55 XOR BC gives E9, making first key BCE9. We have included the original module unchanged and its MIT license. Sources: https://github.com/mayank-02/simplified-aes/tree/27c9feaf7a22c9707c524e295cf2a17473d1d42f ; https://www.rose-hulman.edu/~holden/Preprints/s-aes.pdf

## Slide 4

Slide content:

Choosing and using the S-boxes

Each S-box contains all 256 byte values once.

| Round 1 selection | Calculation | Result |
| --- | --- | --- |
| Left box | 48361 mod 10 | S1 |
| Right box | 38717 mod 10 | S7 |
| Left byte 00 | S1, row 0, column 0 | 9D |
| Right byte 10 | S7, row 1, column 0 | D4 |

BCE9 = 48361. Reversing all 16 bits gives 38717.

Speaking notes:

Wahab: We label the S-boxes S0 to S9 to match Python indices. The normal subkey mod 10 selects the left table; its 16-bit reversal mod 10 selects the right. BCE9 selects S1 and S7. Our first numeric ID block is 0010, split into bytes 00 and 10. The high hex digit is the row and the low hex digit is the column. These lookups give 9D and D4, making 9DD4. Inverse S1 maps 9D back to 00. The required formulas can select the same table twice for some keys.

## Slide 5

Slide content:

Worked example

Plaintext 0010, the first numeric ID block. Key 2D55. Values are hexadecimal.

| Round | Input | Substitute | Permute | Key | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | 0010 | 9DD4 | EAB8 | BCE9 | 5651 |
| 2 | 5651 | 514B | 41D3 | A34A | E299 |
| 3 | E299 | 8A45 | 610B | 2E64 | 4F6F |
| 4 | 4F6F | 3173 | CE8C | C6A2 | 082E |

Round 1: EAB8 XOR BCE9 = 5651

Final ciphertext 082E. Decryption returns 0010.

Speaking notes:

Wahab: This table traces all four rounds for 0010, the first block of either numeric ID. In round 1, the S-boxes give 9DD4. Pattern 1 reads bit positions 6, 8, 1, 2 and so on, giving EAB8. XOR with BCE9 gives 5651. Feed that result into round 2 and repeat with the next pattern and key. The final ciphertext is 082E. The optional decryption check restores 0010 by reversing the round operations. The report includes all eight S-box lookups and a binary XOR calculation. I will hand over to Faisal for the program and results.

## Slide 6

Slide content:

Python libraries

| Library | Calls used | Purpose |
| --- | --- | --- |
| NumPy | permutation(256)<br>argsort(box)<br>frombuffer(data, ">u2") | Create S-boxes and inverses<br>Read 16-bit blocks |
| BitVector | permute(pattern)<br>unpermute(pattern)<br>reverse() | Shuffle and restore bits<br>Reverse subkey bits |
| S-AES module | SimplifiedAES(key) | Generate two round keys |

Our wrapper calls S-AES twice. The remaining code connects the round steps.

Speaking notes:

Faisal: symmetric_cipher.py contains our project logic. saes.py is Mayank Jain's downloaded module, unchanged and supplied with its MIT license. We use its key-expansion methods. NumPy creates S-boxes and inverse tables, and frombuffer reads two-byte numbers. The Python integer method student_id.to_bytes(4, "big") stores the whole ID in four bytes, most significant first. Leading zeros fill 32 bits. BitVector handles permutation and bit reversal. Our code connects these operations into four rounds, CBC and tests. Sources: https://github.com/mayank-02/simplified-aes ; https://docs.python.org/3/library/stdtypes.html#int.to_bytes ; https://numpy.org/doc/stable/reference/generated/numpy.frombuffer.html ; https://engineering.purdue.edu/kak/dist/BitVector-3.5.0.html

## Slide 7

Slide content:

Encrypting both student IDs

| Student | ID | CBC ciphertext |
| --- | --- | --- |
| Wahab | 1098271 | 082E 41B9 |
| Faisal | 1075075 | 082E 0DB4 |

Each numeric ID fills two 16-bit blocks, with leading zeros.

Store the number in four bytes. CBC demonstration IV: 0000.

Speaking notes:

Faisal: The inputs are integers 1098271 and 1075075. Each needs 21 bits. We store each in four bytes and add leading zero bits to fill 32 bits; this preserves the numeric value. Wahab is hexadecimal 0010C21F, giving blocks 0010 and C21F. Faisal is 00106783, giving 0010 and 6783. There is no ASCII conversion and no extra padding byte. CBC XORs each plaintext block with the preceding ciphertext before its four rounds. The first block uses IV 0000. Both IDs have first block 0010, so the same demonstration key and IV produce first ciphertext 082E. The second ciphertexts differ. The fixed IV is for a repeatable example and exposes repeated-prefix patterns.

## Slide 8

Slide content:

One-bit change tests

| Test | Plaintext | Key | Ciphertext | Changed bits |
| --- | --- | --- | --- | --- |
| Original | 0010 | 2D55 | 082E | 0 / 16 |
| Plaintext bit 0 | 0011 | 2D55 | 334E | 7 / 16 |
| Key bit 0 | 0010 | 2D54 | E230 | 9 / 16 |

Plaintext change: 43.75% of output bits change.

Key change: 56.25% of output bits change.

Speaking notes:

Faisal: Bit 0 is the rightmost bit. Keep key 2D55 and change plaintext 0010 to 0011. The output changes from 082E to 334E. Their XOR is 3B60, containing 7 set bits. Next, keep plaintext 0010 and change key 2D55 to 2D54. The ciphertext becomes E230; its XOR with the original is EA1E, with 9 set bits. The percentages are 43.75% and 56.25%. These tests use the raw block cipher, so CBC does not influence the measurement. They are examples, not proof of security.

## Slide 9

Slide content:

Program demonstration and limits

python symmetric_cipher.py

The output shows round keys, both IDs, decryption and one-bit tests.

Only 65,536 possible keys. This is a classroom cipher.

Speaking notes:

Faisal: Run python symmetric_cipher.py in the project folder. The output shows round keys, ciphertext 0x82e, recovered plaintext 0x10, both numeric ID ciphertexts, then 7 and 9 changed bits. Python's 0x prefix means hexadecimal and omits leading zeros: 0x82e is 082E and 0x10 is 0010. We input the full decimal IDs as integers. The built-in to_bytes method stores each number in four bytes and frombuffer splits those bytes into two 16-bit blocks. CBC chains those blocks. The detailed trace is in the report. Keep saes.py beside our program and install the requirements first. Both students answer questions. The cipher follows the handout. S-AES supplies only key expansion through two calls, with K2 fed into the second call. The small key and two avalanche examples do not establish security.
