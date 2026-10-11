# Review of the Dido obstruction proofs

Reviewed by Codex, 11 October 2026. The [uploaded PDF](../dido_obstructions.pdf) is preserved byte for byte and is published as a working proof note pending independent mathematical review. Read it with the [hypothesis audit](../dido_audit.pdf) and the [editable proof companion](../impossibility-note.md).

## Assessment

The PDF closely follows the proof source. I checked the smooth positive sphere profile and pole behavior, selected-side collar isometry, exact `8π` area gap, nonlinear local maximality inequality, regular exact-length perturbation, round-sphere and cigar nonattainment arguments, finite-query lemma, and infinitely flat scalar residual.

The sphere construction establishes that selected-side boundary germs cannot universally reconstruct area or strictly rank candidates by area. Both candidates are strictly stable local maxima, yet the larger disk is an admissible competitor proving the smaller disk is nonglobal. No global maximizer is needed for this argument. Global methods using region position, the interior metric, or area integration remain outside the theorem's information restriction.

The exact-perimeter nonattainment arguments preserve the selected-region distinctions. On the round sphere the chosen class permits complementary selected disks, whose areas approach the full sphere while perimeter is held fixed. On the cigar the selected regions are compact polar disks of exact length `2π` with areas tending to infinity. These conclusions concern those stated classes.

The finite-query lemma excludes exact area recovery and a uniform finite absolute-error guarantee for arbitrary smooth metrics in its deterministic point-query model. It does not establish undecidability for symbolic metrics or exclude methods supplied with quantitative global bounds. The infinitely flat residual is an abstract smooth example; its realization in Dido geometry remains open in this note.

## Qualification required in Section 2.1

The zero-energy obstruction requires only an admissible class containing both witness disks. The extension to **positive energies tending to zero** additionally requires that the class contain the small exact-length perturbed disks used in the proof. That requirement holds for the class of all proper smooth selected disks, but does not follow merely from containing the two witnesses; a class consisting of just those two disks would have no positive-energy candidates.

This qualification has been made explicit in Section 2.1 of the editable companion. It should be added to the next PDF edition. The uploaded PDF remains unchanged, so this review accompanies its publication.

## Checks and publication details

The nonlinear stability coefficient evaluates to `0.6834977045450736`, agreeing with the printed value. Direct expansion of the graph formulas gives the stated leading coefficients `-1/2` for the constant length correction, `-3π/4` for area change, and `9π/16` for curvature-variation energy. A separate 4,096-point numerical calculation recovers these limits while enforcing exact length; its method and samples are saved in [obstructions-crosschecks.json](obstructions-crosschecks.json). These floating-point calculations support the analytic derivation and are not certification.

The existing argument audit passed all 19 entries; see [the audit review](dido_audit_review.md) for its provenance and limitations. Passing these entries does not replace mathematical peer review or proof-assistant verification.

The long source path on PDF page 7 is clipped at the right edge. A later build should wrap filenames and replace machine-local paths with public citations. Use these portable references now:

- [Original paper](../dido_merged_2026-09-08.pdf).
- [Exotic-surface paper](../dido_relaxation_exotic_surfaces.pdf), Sections 7.4 and 8.
- `dido_argument_audit.py` in the [reproducibility archive](../dido_exotic_surfaces_reproducibility.zip).
- [Argument audit output](argument-audit.json).
- [Earlier cigar and round-sphere crosschecks](additional-crosschecks.txt).

The PDF's introductory illustration reference is contextual; its analytic proof is self-contained and does not depend on a figure. The hypothesis audit and companion are linked from both the repository README and the website.
