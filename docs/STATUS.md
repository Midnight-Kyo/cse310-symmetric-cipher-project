# Current project status

Repository prepared on 23 November 2026. The implementation and report preserve the final version prepared on 17 November 2026; publication does not change the algorithm or its results.

## Completed

- A four-round encryption implementation, its inverse and CBC handling for both seven-digit student IDs.
- Ten fixed 8-bit S-boxes and all ten inverse tables.
- Two calls to the downloaded S-AES key-expansion module for four round keys.
- A six-page Word report and a matching PDF with the flowchart, pseudocode, full four-round worked example, ID results and one-bit tests.
- Nine presentation slides, speaker notes and a plain-text copy of the slides.
- A code walkthrough, decision record, source attribution and rubric map.
- Expected console output, full result records and a portable verification tool.

## Verification

The verification tool checks all ten S-boxes and 2,560 inverse entries; all four permutation patterns; 512 deterministic plaintext/key pairs against an independent reference implementation; encryption/decryption recovery; all 65,536 plaintext outputs under the example key for uniqueness; both complete ID results; and both one-bit tests.

It also checks the recorded results, the project-source checksum, the unchanged third-party source and the submission archive. The GitHub Actions workflow runs these checks on Python 3.12. Its latest run is the public record of the server-side result.

The PowerPoint archive has nine slides, six native tables and speaker notes. It passed package, slide geometry, font-policy and re-import checks. These checks are separate from visual review and do not claim a live classroom presentation took place.

## Not yet confirmed

- The instructor has not supplied or approved a specific 16-bit adaptation of AES key expansion in this conversation. The two-call S-AES approach is explicitly our design choice.
- The handout does not fully define how to adapt standard AES key expansion to a 16-bit master key or disambiguate the direction of its permutation tables. Our conventions are documented.
- The nine-slide presentation still needs to be delivered by both students. Speaking notes are preparation material, not evidence of delivery.
- No Blackboard submission, submission receipt or professor grading has been recorded.
- The original `Project+Rurbric.docx` was available for the earlier review but could not be found at publication time. The requirements file is a structured transcription of its contents. Its example S-box images were retained from the original extraction.

## Submission files versus repository context

The supplied [ZIP](../submission/Symmetric_Project_Files.zip) contains exactly:

1. `Symmetric_Algorithm_Report.docx`: the written evidence for the flowchart, pseudocode, trace and tests.
2. `symmetric_cipher.py`: the project program required by the rubric.
3. `requirements.txt`: the two dependency versions needed to run it.
4. `saes.py`: the third-party module imported by the program.
5. `SAES_LICENSE.txt`: the original license notice supplied with that module.

The [presentation](../presentation/Symmetric_Algorithm_Presentation.pptx) is separate and is also required by the rubric. The report PDF is a readable copy of the same report. The remaining repository documentation and verification files explain and check the work; they are not additional university submission requirements.

Historical scratch folders, installed dependency trees, unrelated Lab 1 work and temporary QA files are outside this repository. The current deliverables and the meaningful design history are preserved here.

The original names and IDs are included at the user's explicit request for this public repository.
