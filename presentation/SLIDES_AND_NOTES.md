# Presentation slides and speaking notes

This is a text copy of the nine-slide presentation. The editable PowerPoint is [here](Symmetric_Algorithm_Presentation.pptx). Slide text and tables come from the exported deck; speaking notes come from its current saved presentation.

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
| Left byte 31 | S1, row 3, column 1 | 63 |
| Right byte 30 | S7, row 3, column 0 | 09 |

BCE9 = 48361. Reversing all 16 bits gives 38717.

Speaking notes:

Wahab: We label the S-boxes S0 to S9 so the names match Python indices. Convert the subkey normally and take mod 10 for the left side. Reverse all 16 key bits and take mod 10 for the right side. Leading zeros are included. For BCE9 this selects S1 and S7. The input block 3130 splits into 31 and 30. The first hex digit chooses the row and the second chooses the column. Their lookups give 63 and 09. An inverse table undoes a lookup: inverse S1 maps 63 back to 31. The formula may select the same box twice for some keys; we follow the two required mod 10 calculations.

## Slide 5

Slide content:

Worked example

Plaintext 3130 (ASCII “10”). Key 2D55. All values are hexadecimal.

| Round | Input | Substitute | Permute | Key | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | 3130 | 6309 | 5542 | BCE9 | E9AB |
| 2 | E9AB | FB6D | 7FD5 | A34A | DC9F |
| 3 | DC9F | 315D | 845F | 2E64 | AA3B |
| 4 | AA3B | 11E6 | 6788 | C6A2 | A12A |

Round 1: 5542 XOR BCE9 = E9AB

Final ciphertext A12A. Decryption returns 3130.

Speaking notes:

Wahab: This table is the full four-round trace. In round 1, substitution gives 6309. Pattern 1 reads its bits in the order 6, 8, 1, 2 and so on, giving 5542. XOR with BCE9 gives E9AB. Feed that into round 2, then repeat. The final output is A12A. To decrypt, start at round 4: XOR its key, undo the permutation, then use inverse S-boxes. This restores 3130. The report shows the binary XOR and all eight S-box lookups. I will now hand over to Faisal for the program and results.

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

Faisal: Our project-specific file is symmetric_cipher.py. The other Python file, saes.py, is Mayank Jain's downloaded module, unchanged and supplied with its MIT license. We use its key-expansion method, rather than its encryption method. NumPy creates S-boxes, builds inverse tables and reads paired ID bytes into 16-bit blocks. In frombuffer, >u2 means a two-byte unsigned number with the most significant byte first. BitVector performs permutation, inverse permutation and bit reversal. Our code joins these library operations into the required four rounds and handles CBC and tests. Sources: https://github.com/mayank-02/simplified-aes ; https://numpy.org/doc/stable/reference/generated/numpy.frombuffer.html ; https://engineering.purdue.edu/kak/dist/BitVector-3.5.0.html

## Slide 7

Slide content:

Encrypting both student IDs

| Student | ID | CBC ciphertext |
| --- | --- | --- |
| Wahab | 1098271 | A12A 8120 54BF 1711 |
| Faisal | 1075075 | A12A 41E4 6DDE AC05 |

ASCII encoding keeps all seven digits. Two bytes form each block.

One padding byte 01. CBC uses demonstration IV 0000.

Speaking notes:

Faisal: An ID is longer than one 16-bit block. We keep the entire ID as ASCII text and take two characters at a time. Wahab becomes blocks 3130, 3938, 3237 and 3101. Faisal becomes 3130, 3735, 3037 and 3501. The final 01 is one padding byte. CBC XORs each plaintext block with the preceding ciphertext before encryption. The first block uses IV 0000. Both IDs start with 10, so using the same demonstration key and IV gives the same first ciphertext block. Later blocks differ. The fixed IV makes this demonstration repeatable and exposes why repeated IVs leak patterns. We would not reuse it for real data protection.

## Slide 8

Slide content:

One-bit change tests

| Test | Plaintext | Key | Ciphertext | Changed bits |
| --- | --- | --- | --- | --- |
| Original | 3130 | 2D55 | A12A | 0 / 16 |
| Plaintext bit 0 | 3131 | 2D55 | 899C | 7 / 16 |
| Key bit 0 | 3130 | 2D54 | F0F7 | 9 / 16 |

Plaintext change: 43.75% of output bits change.

Key change: 56.25% of output bits change.

Speaking notes:

Faisal: Bit 0 is the rightmost bit. For diffusion, keep key 2D55 and change plaintext 3130 to 3131. The output changes from A12A to 899C. XORing the ciphertexts gives 28B6, with 7 set bits. For key sensitivity, keep plaintext 3130 and change key 2D55 to 2D54. The output is F0F7, 9 bits different from the original. The two percentages are 43.75 and 56.25. These tests use the raw block cipher, so CBC does not affect the measurements. They show the effect for these examples and do not establish security.

## Slide 9

Slide content:

Program demonstration and limits

python symmetric_cipher.py

The output shows round keys, both IDs, decryption and one-bit tests.

Only 65,536 possible keys. This is a classroom cipher.

Speaking notes:

Faisal: Run python symmetric_cipher.py in the project folder. The output shows the four round keys, ciphertext 0xa12a, decrypted 0x3130, both encrypted IDs, then 7 and 9 changed output bits for the two one-bit tests. Python's 0x prefix means hexadecimal, so 0xa12a and A12A are the same value. The detailed round trace is in the report. The if __name__ == "__main__" line runs this demonstration only when the file is executed directly. It is separate from the cipher. Keep saes.py beside our program and install the requirements first. Both: answer questions together. The full cipher is the handout's custom design. S-AES supplies only key expansion. We use two calls, with K2 as the second input. The seven-digit IDs need one padding byte 01. CBC handles the complete IDs. The small key and example avalanche results do not establish security.
