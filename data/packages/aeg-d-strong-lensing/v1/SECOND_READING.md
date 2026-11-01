# aeg-d-strong-lensing/v1: second reading and reproduction tests

Run 2026-11-01. Method in `REPRODUCTION.md` (frozen, D-065); readings and adjudication in `reading/`. Claude (Anthropic, Claude Opus 5.5) wrote the conversion and the test scripts and ran them; AI assistance is disclosed. JvH has not reviewed this run.

## Result

| Test | Result |
|---|---|
| 1. Second reading against the sources | **FAIL: 1107 of 1111** packaged input numbers pass (1097 found in both readings, 10 adjudicated at source with the adjudication cited). The 4 that fail are below. `checks/second_reading.csv` |
| 2. Transcription | **PASS:** 5927 of 5927 table values equal the adjudicated readings (`checks/transcription.csv`). |
| 3. Arithmetic integrity | **PASS:** 1178 recomputations from the stored columns agree to 10⁻⁹, in memory and again on the table read back (run inside `convert.py`). They cover M_E where computed, R_E, the L × Υ products, f(<R_E), M*(<R_E), g_obs, g_bar_stars, each gas component and g_bar. |
| 4. Code | **PASS:** `pipeline/tests/test_lensing.py` (frozen) and the full pipeline suite, 197 passed; the converter's own synthetic tests (`pipeline/tests/test_a6_convert.py`, 26) are part of it. |

Under REPRODUCTION.md, the package passes only if tests 1–4 all hold. **Test 1, version 2, failed** on 4 numbers, and that failure stays on record here. The test was not changed. The 4 numbers were R32's R_E errors in kpc, which only reader A had recorded. An independent second reader then read R32 Table 1 (`reading/readings/second-reader-r32.csv`) and found the same values: ±0.09 kpc and ±0.37 kpc.
- **Test 1, version 3**, adds that reading and nothing else: **PASS, 1111 of 1111.**
- The version 2 output is kept as `checks/second_reading_v2.csv`.

### The 4 numbers that fail test 1

They are the printed errors of R32's Einstein radius in kpc (Smith et al. 2020, Table 1, row R_Ein):

| System | Value | Reader A | Reader B |
|---|---|---|---|
| J1436+4943 | 4.72 ± **0.09** kpc | 4.72, 0.09, 0.09 | "R_Ein = 4.72 kpc (theta_Ein)", no error recorded |
| J1701+3722 | 3.71 ± **0.37** kpc | 3.71, 0.37, 0.37 | "R_Ein = 3.71 kpc (theta_Ein)", no error recorded |

- The adjudicated rows record "both readers agree (scope spelling differs)", which is true of the values but not of the errors.
- The adjudication table (`reading/adjudication.md` §4) prints "4.72 ± 0.09 kpc" and "3.71 ± 0.37 kpc", but no settlement at source is recorded for the errors. The test's rule, written before it was run, accepts a one-reader number only where the adjudicated row says it was settled or verified at source.
- **What these numbers do.** They are stored as the errors of the `einstein_radius` observables of the two MaNGA lenses. They do not enter g_obs, g_bar or their errors: R_E is the coordinate, and errors are carried at fixed R_E (REPRODUCTION.md, Uncertainties).
- **Next step:** a targeted re-read of R32 Table 1 (R_Ein errors) by reader B or by JvH. Then test 1 is run again, and the re-read is recorded, as was done for aeg-d-dwarfs/v1.

## How test 1 was run

- **Packaged numbers.** These are every number of every adjudicated row that enters the tables (the observables: value and printed errors). They also include the numbers that enter only measurement columns: H0 and Ω_m of each observed-side record, and the printed Salpeter conversions used for the IMF top (R29 α = 1.55, R32 α ≈ 1.65, R30 ÷ 0.61).
- **Readings.**
  - Readers A and B: `reading/readings/reader-{a,b}-{block1,block2,block3,supplement}.csv`. They read independently, in separate folders, without the conversion code.
  - SNL-1's R61 values (L_F814W 2.52 ± 0.04 × 10¹⁰ L⊙ inside 2.38″; Υ_ref 2.75, Kroupa, no printed error): the adjudicator read these at source (`reading/gas/adjudication_gas.md` §1), and a further second reader confirmed them (`reading/readings/second-reader-r61-snl1.csv`; D-076 item 3).
- **Matching.** A number counts as found in a reading if it is among the values and errors that reader recorded for the same record and system. It may appear as printed or in base units after the reader's own unit scaling. Matching is by record and system, not by quantity name, because the readers named some quantities differently. This is a limitation: a number could in principle match another quantity of the same system and record.

**Adjudicated at source (10 numbers).** Each is settled in `reading/adjudication.md` §2:
- J0403−0239 (R29): M_E error 0.4. "adopted error 0.4 (statistical 0.23)"; both readers recorded 0.23.
- J0403−0239 (R29): z_l 0.06569 and z_s 0.19130. One-reader extras (A), verified at source.
- NGC 6505 (R30): θ_E errors ±0.001. B missed the printed error.
- NGC 6505 (R30): M_E 1.53 × 10¹¹ and the alternative z_l 0.041 ± 0.001. One-reader extras (A), verified at source.

**Script versions (disclosed).**
- **Test 1, version 2.** The first run is kept in `checks/second_reading_v1.csv`: 1109 of 1115. It contained one script defect and one converter defect.
  - *Script defect:* a record-level number (a printed Salpeter conversion) was looked up only under the readers' "(record)" rows. Reader A had filed the conversions under the systems they apply to. Version 2 looks such numbers up among all of that reader's rows for the record. R29 α = 1.55, R30 0.61 and R32 1.65 are now found in both readings.
  - *Converter defect:* R26's 2.2″ spectroscopic (M/L) aperture for SNL-1, an alternative record, had been packaged as an alternative `einstein_radius` observable. It is not an Einstein radius. `convert.py` now keeps apertures of stellar-side alternatives in the alternative's note only. That removed 4 alternative observables (630, not 634). No default value, g_obs or g_bar changed.
  - The 4 R32 failures are the same in both runs.
- **Test 2, version 2.** The first run is kept in `checks/transcription_v1.csv`: 5736 of 5927. One script defect: an empty text cell reads back as None, so the 191 dimensionless redshift rows (unit "") were counted as unequal. No value changed.

## Released files (additional check, run inside `convert.py`)

- Every tier-1 number used is found in its system's row of the released file, hash-verified by `aeg.fetch`: **972 of 972** (`checks/released_files.csv`).
  - VizieR J/ApJ/682/964 tables 4–5 (SLACS V);
  - VizieR J/A+A/501/461 (R13);
  - IOP tables of R10 (S4TM) and R20 (SL2S III).
- A fresh VizieR export differs in its raw bytes (request time) but matched the recorded content hash (2026-11-01).

## Reported, not pass/fail

See `RESULT_SUMMARY.md` for the summary statistics.
- §2.4 formula check: `checks/formula_check.ecsv`.
- D-075 item 5 profile-step check: `checks/profile_step.ecsv`.
- Overlap between surveys: `checks/overlap.csv`, none.

## Disclosure

While building the released-file check, the converter's author saw a few rows of R7 Table 4 in the terminal. These included R7's f*,Ein columns (lensing-based stellar fractions, which the Atlas does not use). None was recorded or used.
