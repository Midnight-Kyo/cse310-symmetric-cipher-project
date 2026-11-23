# CSE 310 symmetric cipher project

This repository records the current **A New Symmetric Algorithm** project for Introduction to Cryptography, Section 101, Fall 2026/2027, with Dr Moatsum Alawida. It includes the implementation, assignment requirements, report, presentation, results and explanations of the choices made.

| Student | ADU ID |
| --- | --- |
| Wahab Yaseen Dawod | 1098271 |
| Faisal Saud Al Maamari | 1075075 |

The program implements the handout's custom **16-bit, four-round symmetric cipher**. Each round substitutes two bytes, permutes the bits and XORs a round key. A downloaded Simplified AES module supplies key expansion. The full encryption algorithm follows the project handout, rather than the standard AES or DES algorithm.

## Run the program

Use Python 3.11 or later. From the repository folder:

```sh
python -m pip install -r requirements.txt
python symmetric_cipher.py
python tools/verify_project.py --check
```

NumPy 2.3.5 and BitVector 3.5.0 are the installed dependencies. The S-AES module is supplied locally as `saes.py`.

## Start here

| File | Purpose |
| --- | --- |
| [Assignment and rubric](requirements/ASSIGNMENT_AND_RUBRIC.md) | Preserves the supplied requirements and shows where each is covered. |
| [Current status](docs/STATUS.md) | Lists completed work, checks and remaining uncertainties. |
| [Design decisions](docs/DESIGN_DECISIONS.md) | Explains the key schedule, S-boxes, bit convention, ID encoding and CBC choices. |
| [Code walkthrough](docs/CODE_WALKTHROUGH.md) | Explains each function in simple terms with code blocks. |
| [Project program](symmetric_cipher.py) | The small project-specific implementation and demo. |
| [Downloaded S-AES module](saes.py) | Mayank Jain's unchanged third-party implementation; used for key expansion. |
| [Word report](report/Symmetric_Algorithm_Report.docx) / [PDF report](report/Symmetric_Algorithm_Report.pdf) | The six-page report, including flowchart, pseudocode, manual trace and tests. |
| [PowerPoint presentation](presentation/Symmetric_Algorithm_Presentation.pptx) | Nine editable slides with speaker notes. |
| [Slides and speaking notes](presentation/SLIDES_AND_NOTES.md) | A readable text copy of the presentation for GitHub. |
| [Expected output](results/expected_output.txt) / [full results](results/results.json) | Reproducible example outputs and intermediate values. |
| [Verification tool](tools/verify_project.py) | Independent checks and regeneration of the result records. |
| [Student package](submission/Symmetric_Project_Files.zip) | The existing report/code package; the presentation is stored separately above. |
| [Sources and credits](docs/THIRD_PARTY.md) | Records external code, dependency versions, authorship and license scope. |

## Current results

With plaintext `3130` (ASCII `10`) and key `2D55`, the round keys are:

```text
BCE9  A34A  2E64  C6A2
```

| Example | Result |
| --- | --- |
| Encrypt block `3130` | `A12A` |
| Decrypt block `A12A` | `3130` |
| Encrypt ID `1098271` | `A12A 8120 54BF 1711` |
| Encrypt ID `1075075` | `A12A 41E4 6DDE AC05` |
| Flip plaintext bit 0 | `899C`; 7/16 output bits change, or 43.75%. |
| Flip key bit 0 | `F0F7`; 9/16 output bits change, or 56.25%. |

## Important design choice

We call the two-round S-AES key expansion twice. The second call uses the last key from the first call. Each call restarts its constants, so the sequence is **80, 30, 80, 30**. This is our documented adaptation to the handout's four-key requirement. Instructor confirmation of this particular adaptation has not been recorded.

The original rubric DOCX is no longer available at its earlier Downloads path. The repository contains a structured transcription from the handout reviewed during the work, including its original example S-box images. It is labeled as a transcription, rather than presented as the original DOCX.

The project code and materials were prepared with OpenAI Codex assistance. The downloaded `saes.py` has separate authorship and its original MIT license. See [sources and credits](docs/THIRD_PARTY.md).

This is a classroom cipher with a 16-bit key and a fixed demonstration IV. Its two avalanche examples do not establish security. See [design limits](docs/DESIGN_DECISIONS.md#limits).
