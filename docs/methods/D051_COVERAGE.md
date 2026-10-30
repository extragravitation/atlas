# D-051: member coverage from the source's own table, duplicate printings, lower limits — frozen

**Frozen 2026-10-30 (on merge of the pull request that adds it), before any per-star table of an A5 or A7 candidate is opened.** The hashes of this file and of the code that implements it are in `data/frozen/d051-coverage.json`. Any change needs a new version and a logged decision, and applies only to later cases.

## 1. What D-038 1A asks, unchanged

A whole-sample dispersion is plotted only if the member stars used for it reach beyond the half-light radius. Otherwise it is an aperture value: recorded, not plotted.

## 2. Evidence admitted

Either of these two kinds of evidence counts.

**(a) Prose.** The source states it in half-light-radius units (the coding brief, `reading/SIGMA_CODING_BRIEF.md`).

**(b) The source's own per-star member table** (D-051), for papers that release per-star velocities with positions. The steps:

1. **Members.** The members used are those the source states it used for the chosen dispersion. The selection rule is recorded with the source's words and their location (`reading/coverage_config.csv`) before the table is opened.
2. **Radius.** Each member's radius is its elliptical radius. It is computed (`pipeline/aeg/coverage.py`) from the structural original's centre, ellipticity, position angle and semi-major half-light radius. This is the same R_h the plotted point uses, from the two-reader structural reading.
3. **Pass.** The value passes if **at least one member used lies beyond the half-light ellipse** (r_ell / a_h > 1). This is the same contour as the circularised R_h.
4. **Published for every system checked:**
   - the number of members;
   - the number beyond R_h, and the fraction;
   - the largest r_ell / a_h.
   These are published so a reader can judge how representative the sample is. They are not a second threshold.
5. **Not reached.** A table that cannot be reached leaves the value as an aperture value, with the reason "coverage not checkable". It is never guessed.

## 3. Duplicate printings

Several rows of one paper may be marked as the paper's adopted result: the same estimate printed in a table, in the text and in a figure, with different digits. The rule:

1. Use the printing in a table.
2. Among several table printings, or if none is in a table, use the printing with the most significant digits.
3. A remaining tie is listed for JvH.

Papers that give genuinely different estimates without saying which is their result are listed for JvH. The script never chooses by value.

## 4. Lower limits

Lower limits are recorded and never plotted.

## 5. Record kept

The result under D-038 1A with prose evidence only (`reproduction/apply_sigma_rules.py`, giving `reading/sigma_selection.csv`) stays on record. It is published beside the D-051 result (`reproduction/apply_sigma_rules_v2.py`). Both, and this decision, go to the outside reader as an after-result decision.
