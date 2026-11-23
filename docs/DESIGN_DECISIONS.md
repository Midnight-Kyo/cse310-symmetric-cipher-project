# Design decisions

This document explains the implemented choices and their reasons. It separates the handout's requirements from decisions made while preparing this project.

## Cipher structure

The handout specifies a 16-bit block, a 16-bit master key, four rounds, two byte substitutions per round, a bit permutation and XOR with a round key. The program connects those operations directly. It does not call the third-party module's encryption or decryption methods.

The full design is a custom symmetric block cipher. Only its key expansion comes from S-AES. There is no extra key XOR before the first round and no AES MixColumns or ShiftRows operation in this project cipher.

## Key expansion

Standard AES uses larger keys, while the handout asks for four 16-bit subkeys using an AES method. No exact 16-bit schedule was supplied. We chose educational S-AES key expansion because it works with a 16-bit master key and can be explained by hand.

The final program imports Mayank Jain's unchanged `SimplifiedAES` class. Its constructor generates two new round keys. We call it twice, feeding the last generated key into the second call:

| Call | Input | New round keys |
| --- | --- | --- |
| 1 | `2D55` | `BCE9`, `A34A` |
| 2 | `A34A` | `2E64`, `C6A2` |

Each library call uses constants `80` and `30`. The combined sequence is therefore `80, 30, 80, 30`. Calling twice with the original key would repeat the first pair, so that is not what the program does.

This choice reuses a ready-made implementation and leaves a small wrapper to collect the four keys. The module returns keys in a nibble-state representation; its own `state_to_int` method converts them to the integers used by our program.

An earlier draft implemented a four-round extension with a hand-written function. At the user's request, it was replaced with the two-call module approach. The report, trace, ID outputs and avalanche tests were recalculated together. The current result file is the reference; older draft outputs are obsolete.

## S-boxes

The detailed handout description uses a four-bit row and a four-bit column to select an eight-bit output. We implement this as a 16 by 16 table containing 256 byte values. Each byte S-box is a permutation, which permits an inverse lookup.

NumPy's `Generator.permutation(256)` creates each of the ten tables. `argsort` constructs its inverse. Seed `310` makes the public tables reproducible. It is not the secret key and does not make this a cryptographically secure random generator. The tables stay fixed across keys, blocks and tests. The verification tool confirms all ten tables differ.

The S-AES module has a separate, fixed four-bit S-box for key expansion. That small table is distinct from the ten eight-bit encryption S-boxes.

## S-box selection

The left index is the 16-bit subkey modulo 10. The right index is the bit-reversed 16-bit subkey modulo 10. BitVector preserves leading zeros during reversal. Indices run from 0 to 9, matching Python.

The two specified formulas can produce the same index. We do not introduce a rule forcing the indices to differ, because that would change the handout's selection method.

## Permutation direction

The four patterns are copied from the handout. The implemented convention is: the second row lists source positions to read into output positions 1 through 16. Thus pattern 1 begins by reading input positions 6, 8, 1 and 2.

We subtract one to translate the handout's positions into Python's zero-based indices. BitVector's `permute` performs the shuffle. This source-position convention is stated in the report because the handout's wording does not fully define the direction.

## Full student IDs and CBC

The IDs are numeric inputs: `1098271` and `1075075`. Each needs 21 bits, so it cannot fit in one 16-bit block. The built-in integer method `student_id.to_bytes(4, "big")` stores the complete number in four bytes, with leading zero bits to fill 32 bits. The left padding does not change its numeric value.

`np.frombuffer(data, dtype=">u2")` reads those bytes as two 16-bit values, most significant first. Wahab becomes `0010 C21F`; Faisal becomes `0010 6783`. Recombining the two blocks recovers the original integer. This helper accepts the unsigned numbers that fit in four bytes; it is scoped to the IDs in this assignment.

At the user's request on 23 November, this numeric representation replaced the earlier ASCII representation. The current code, worked trace, ID ciphertexts and bit tests were recalculated together. The handout specifies the IDs and 16-bit blocks but does not prescribe their binary formatting.

The handout introduces CBC, so we use `C_i = E_K(P_i XOR C_(i-1))`, with the IV as `C_0`. The IV is `0000` for this repeatable demonstration. Both numeric IDs have the first block `0010`, so the reused key and IV yield the same first ciphertext block. Their second blocks differ. This illustrates the pattern leakage from IV reuse.

## One-bit tests

The tests operate on a raw 16-bit block so that CBC chaining does not obscure the cipher's own response. Bit 0 is the rightmost bit. We flip it once in the plaintext, then separately once in the key. XORing the original and changed ciphertexts identifies different bit positions; Python's `bit_count()` counts them.

The plaintext change alters 7/16 output bits (43.75%); the key change alters 9/16 (56.25%). The report presents these as individual examples of diffusion and key sensitivity, rather than a proof of general cryptographic strength.

## Keeping the student code readable

The user wanted code they could explain during the presentation, and stated that the instructor permits libraries. NumPy handles table creation, inverse construction and reading byte pairs. BitVector handles bit shuffling and reversal. The downloaded S-AES module performs the key calculations.

The project-specific program keeps the custom round order, S-box choice, CBC chaining and tests visible. Detailed trace-printing and elaborate console formatting were removed from the cipher function. The manual trace remains in the report and JSON records. Verification tooling is stored separately so it does not make the demonstration program harder to follow.

## Limits

A 16-bit key has only 65,536 possibilities. The block size is also very small. Random permutation S-boxes have not undergone a security analysis, the demonstration IV is reused, and two avalanche examples are insufficient to evaluate security. This implementation is for the course exercise and is unsuitable for protecting real data.
