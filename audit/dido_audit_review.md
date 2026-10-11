# Review of the Dido hypothesis audit

Reviewed by Codex, 11 October 2026. The uploaded PDF is preserved byte for byte. The audit and companion proof note are working research documents pending independent mathematical review.

## Mathematical assessment

The PDF faithfully presents the source audit's 14 conditions. Its distinctions between smooth attainment, admissibility, compactness, local inverse estimates, and global area comparison agree with the original paper's Section 2, Theorem 4, Conjecture 5, and Section 5.2. I found no material mathematical discrepancy between the uploaded audit and the source notes during this review.

The cusp calculation establishes an exact answer within the stated radial-graph tail class. In the repository's cusp end, the graphs satisfy `f >= 0`, and the horocycle answer applies for `0 < L <= 2π`. It is not a classification of all regions on a completed surface. The Klein-bottle family has `L = 4`, `J = 0`, and selected area `4h` for `0 < h < 3`, within the specified separator class. The cigar and round-sphere conclusions concern exact perimeter and explicitly chosen region classes; they do not contradict the fixed-area perimeter existence theorem.

The sphere witness supports failure of area reconstruction and strict area ranking from the selected-side boundary germ, and failure of a global area-deficit bound that vanishes with `J`. Its two boundary collars are isometric, both candidates are strictly stable local maxima, and their selected areas differ by `8π`. This does not exclude methods using region position, the interior metric, or global variational comparisons. It does not prove general undecidability or that only numerical methods can solve broader formulations.

The fixed-area discussion correctly uses BV compactness, preservation of area in L¹, lower semicontinuity of perimeter, and two-dimensional isoperimetric regularity on a closed smooth surface. Its area constraint is regular at a nonempty smooth boundary, including when the perimeter multiplier is zero. A future standalone edition should add a standard bibliographic reference for this existence and regularity argument.

The infinitely flat residual remains an abstract example; a realization in the Dido curvature problem is not established. The finite-query obstruction has a specified deterministic point-query input model. Neither statement should be generalized beyond those qualifications.

## Verification and its limits

The existing `dido_argument_audit.py --json` was rerun under Python 3.12 with NumPy and SciPy. All 19 entries passed; the output is saved in [argument-audit.json](argument-audit.json). The executed source was verified byte for byte against the published reproducibility archive. Logical entries encode proof dependencies, some analytic entries encode formulas supplied by the source, and sampled entries provide numerical crosschecks. Passing the audit is not an independent proof of the mathematical statements.

The [companion proof note](../impossibility-note.md) supplies the analytic arguments referenced by the PDF, including the explicit sphere profile, collar isometry, nonlinear local maximality inequality, exact-perimeter nonattainment constructions, and finite-query lemma. The [additional crosschecks](additional-crosschecks.txt) preserve the earlier cigar and round-sphere calculations as supporting evidence. This review is not proof-assistant certification or independent human peer review.

## Source and typesetting repairs for a later PDF edition

Page 5 uses machine-local paths, and the long full-source witness path runs beyond the page's right edge. The next PDF build should replace these with portable citations and wrap long filenames. The current uploaded PDF has not been altered; the following mapping makes its sources accessible now:

| Reference in the PDF | Published location |
| --- | --- |
| `/workspace/Dido/dido_merged_2026-09-08.pdf` | [Original paper](../dido_merged_2026-09-08.pdf), Sections 2, 5, and 5.2 |
| `/workspace/Dido/dido_relaxation_exotic_surfaces.pdf` | [Exotic-surface paper](../dido_relaxation_exotic_surfaces.pdf), Sections 6–10 |
| Local full-source witness path | `dido_exotic_surfaces_reproducibility/dido_argument_audit.py` inside the [reproducibility archive](../dido_exotic_surfaces_reproducibility.zip) |
| `impossibility-note.md` | [Companion proof note](../impossibility-note.md), included beside both repository PDF copies |
| Existing 19-check argument audit | [Recorded output](argument-audit.json) and source in the reproducibility archive |

The original papers remain separate references. This audit is a technical companion, not a replacement for their conditional theorems or numerical campaign.

The accompanying [obstruction PDF](../dido_obstructions.pdf) has a separate [proof review](dido_obstructions_review.md), including the perturbation-admissibility qualification for its positive-energy extension.
