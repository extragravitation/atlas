# aeg-d-sparc/v1 — reproduction result

**Result: FAILED** (first run, 2026-10-28, data workflow run 40775853081, tables at commit `efa9f95`).
The frozen test (`REPRODUCTION.md`, SHA-256 `5504a48b…`) is unchanged. Per D-005 condition 1 the package does not ship in this state.

| Check | Required | Found | Outcome |
|---|---|---|---|
| 1. Selection count | 2 693 | 2 696 | fail |
| 2. Point-by-point (one-to-one, ≤ 0.015 dex) | all matched | 1 point with no reference within tolerance (test stops at first failure) | fail |
| 3. Conversion integrity (all 3 391 rows) | exact to table precision | exact | **pass** |
| Frozen-file hash | match | match | pass |

## Diagnosis (exploratory; not part of the test)

Run outside the test, in the browser on the published files, and labelled exploratory. Nothing here changes the result above.

**A. Implementation bug in the test (2 of the 3 extra points).** In F568-3, two points have δV/V exactly 0.1 in the published two-decimal values (10.7/107.0 and 11.7/117.0). The frozen rule is δV/V < 0.1, so they are excluded; the test's floating-point division returned a value a hair below 0.1 and kept them. Comparing in exact arithmetic on the published decimals gives 2 694 selected points.

**B. Residual discrepancy with the reference (after A).** 2 694 selected points against 2 693 reference rows: **2 690 matched one-to-one within 0.015 dex.**
- Our points without a reference counterpart: UGC00128 at R = 53.75 kpc (`m001903`); UGC07524 at R = 2.41 and 10.69 kpc (`m002872`, `m002896`); UGC09133 at R = 77.5 kpc (`m003135`).
- Reference rows without a counterpart: (log g_bar, log g_obs) = (−11.18, −10.66), (−11.22, −10.58), (−11.23, −10.58).
- UGC00128 at 53.75 kpc has no reference row within 0.06 dex: it satisfies every selection the authors describe but is absent from their file.
- The other three mismatches differ by about 0.1 dex. **Hypothesis, not established:** the authors' 2017 file was built from a slightly different version of these galaxies' data than the mass-model file served today. Testing it needs the 2016 archival copy (CDS J/AJ/152/157), which could not be reached on 2026-10-28, or the maintainer's answer.

## Not concluded

- Whether the currently served SPARC file or the 2017 reference is "right" for these points.
- Whether the conversion is at fault for any point: check 3 (exact agreement with the source table for every row) argues against it, but does not prove the reference was built from the same table.

## Next

Pending JvH's ruling: whether to correct implementation bug A (disclosed, with this failed result kept), and how to treat discrepancy B (ask the maintainer; decide on shipping at release, not now).

## Run 2 (2026-10-28, after D-016; data workflow run 40776593585, commit `0402e1b`)

**Result: FAILED**, as diagnosis B predicted. The implementation bug (A) is corrected; `REPRODUCTION.md` unchanged.

| Check | Required | Found | Outcome |
|---|---|---|---|
| 1. Selection count | 2 693 | 2 694 | fail (the one extra point is UGC00128 at 53.75 kpc) |
| 2. Point-by-point | all matched | stops at the first unmatched point | fail |
| 3. Conversion integrity | exact | exact | pass |

Status under D-017: referred to the maintainer; whether SPARC v1 ships is decided at milestone M5.

## Status under D-019 (2026-10-28)

The test result remains **FAILED**. SPARC v1 may ship: conversion integrity is exact. The four measurements are flagged `reproduction_mismatch` and linked to known issue [#8](https://github.com/extragravitation/atlas/issues/8). In the test suite, checks 1 and 2 are unchanged and marked as strict expected failures; `test_known_mismatch_is_exactly_as_documented` fails the build if the discrepancy changes in any way.
