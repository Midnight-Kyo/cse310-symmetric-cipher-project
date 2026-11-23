# Sources and credits

## Project work

The project-specific implementation, report, slides, explanations and verification tooling were prepared with OpenAI Codex assistance at the students' direction. This attribution does not imply that a ready-made library implements the entire custom cipher.

The professor's handout supplies the project structure, bit permutations, S-box selection rules and rubric. The report identifies the students and course. Their names and IDs remain in this public snapshot at the user's explicit request.

## Bundled S-AES module

- Author: Mayank Jain.
- Repository: <https://github.com/mayank-02/simplified-aes>.
- Pinned commit: `27c9feaf7a22c9707c524e295cf2a17473d1d42f`.
- Source: <https://github.com/mayank-02/simplified-aes/blob/27c9feaf7a22c9707c524e295cf2a17473d1d42f/saes.py>.
- Local file: [`../saes.py`](../saes.py), unchanged.
- SHA-256: `33d6da8d52454816bfa9da6d4c6594ac319739e0cb6844c30d277a4e1c3dfc3e`.
- Original MIT license: [`../SAES_LICENSE.txt`](../SAES_LICENSE.txt).

The main program uses the constructor's key expansion and `state_to_int` conversion. The module also contains S-AES encryption/decryption methods; our custom block cipher does not call those methods.

## Installed dependencies

| Dependency | Version | Use | Primary source |
| --- | --- | --- | --- |
| NumPy | 2.3.5 | S-box generation, inverse lookup tables, reading byte pairs | [permutation](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.permutation.html), [argsort](https://numpy.org/doc/stable/reference/generated/numpy.argsort.html), [frombuffer](https://numpy.org/doc/stable/reference/generated/numpy.frombuffer.html) |
| BitVector | 3.5.0 | Permutation and bit reversal | [Author's documentation](https://engineering.purdue.edu/kak/dist/BitVector-3.5.0.html) |

These packages are installed from `requirements.txt`; their installed files are not copied into the repository. They retain their own licenses.

## Educational reference

Joshua Holden's [A Simplified AES Algorithm](https://www.rose-hulman.edu/~holden/Preprints/s-aes.pdf) explains the S-AES key schedule and nibble S-box used in the report. The project handout is the authority for the custom cipher and marking requirements.

## License scope

`SAES_LICENSE.txt` applies to Mayank Jain's bundled module. No new blanket license has been assigned to the students' materials or the university handout. The report, requirement transcription and extracted handout figures retain their respective authorship; the module's MIT notice does not relicense them.
