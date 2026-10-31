# aeg-d-dwarfs/v1: second reading and reproduction tests

Run 2026-10-31. Method in `REPRODUCTION.md`; brief in `reading/SECOND_READING_BRIEF.md`.

## Result

| Test | Result |
|---|---|
| 1. Second reading against the originals | **PASS:** 534 of 534 packaged input numbers are found as printed (`checks/second_reading.csv`). |
| 2. Transcription | **PASS:** 554 of 554 table values equal the checked inputs. |
| 3. Arithmetic integrity | **PASS:** g_obs and g_bar recomputed from the stored columns agree to 10⁻⁹ (run inside `convert.py`). |
| 4. Kind coding | **PASS:** the coding sheet is complete; double-coding agreement 20 of 21, resolved by the rule text (`reading/KINDS_RESULT.md`). |

## Reported, not pass/fail

**D-038 3A consistency (originals against Geha et al. 2026): consistent.** Run 2026-10-31 by `reproduction/check_d038_consistency.py`, committed and hash-frozen (`data/frozen/d038-a5-consistency.json`) before it was run. 13 systems have both an original default and a Geha et al. 2026 value; 10 pairs have two-sided values and give a z-score, 3 are limit pairs. No pair is beyond 2σ; median z = −0.03; largest |z| = 1.8 (Boötes III, against an unrefereed preprint). Per-pair results in `checks/d038_consistency.csv`.

**D-037 reproduction from released per-star velocities: not yet run.** It needs a per-source membership configuration frozen before any velocities are read (issue #24).

## How test 1 was run

**Readers.** Two independent agent sessions read the original papers for 258 sheet rows: 65 systems (And XII's four rows were added after D-062, Leo II's after its distance original was read), each with dispersion, structure, distance and magnitude. They worked with no access to the conversion code, the package tables or the earlier readings. They recorded 946 values, with every printed candidate and the headline marked (`reading/second_reading_{a,b}.csv`).

**First run: 451 of 470** (`checks/second_reading_v1.csv`). The 19 misses are all accounted for below. **No package value was changed.**
- **Defects in the test script, fixed in version 2 and disclosed in the script's docstring:**
  - A modulus stored as "x ± y" was not parsed (12 misses).
  - An ellipticity printed only as an upper limit was compared as 0 (2 misses).
  - Tucana's r_h is printed in pc (205), and the package stores the angle derived from it (1 miss).
- **Targeted re-reads by the same readers** (`reading/second_reading_{a,b}_followup.csv`):
  - Tucana σ = 14.35 (+2.78/−2.32) is printed in the Fig. 5 label of Gregory 2019. The text prints 14.4 (+2.8/−2.3). D-051's duplicate rule ("most digits") selects the figure printing.
  - The Leo T modulus 23.1 ± 0.2 (de Jong 2008 Table 1) had been written only in a note.
  - The And XXVIII modulus 24.55 ± 0.13 (Slater 2015 Table 1) had been written only in a note.

## Disagreements of interpretation (for the outside reader)

These numbers are printed as packaged. The question is how a paper used them.

1. **Which modulus a paper's M_V uses.** And XXVIII (Slater 2015), Aquarius II (Torrealba 2016) and Hydrus I (Koposov 2018):
   - The supplementary two-reader coding (adjudicated, `reading/supplement_final.csv`) recorded the paper's own modulus.
   - The second reader reports that the paper does not say so explicitly.
   - The package uses the paper's own modulus. For Hydrus I the second reader notes that Sec. 3.1 also prints an isochrone distance of about 31 kpc.
2. **Pegasus IV ellipticity** (Cerny 2023) is printed only as an upper limit, < 0.41. Under D-062 the package uses the paper's printed circularised r_h, 1.55′; the second reader found it as printed.
3. **Values printed differently in the same paper** (the D-051/D-055 printing rules decide; the second readers recorded both):
   - Ho 2012 And II, σ 7.8 in the abstract and 7.5 in the conclusions (the package uses the abstract, D-055 item 2).
   - Muñoz 2018 CVn I and CVn II, M_V in the text and in Table 6 (table).
   - Richstein 2024 Tri II, M_V.
   - Koposov 2018 Hydrus I, M_V −4.71 in Table 1 and −4.74 in the text (table).
   - Battaglia 2012 Phoenix, ellipticity 0.3 in Table 1 and 0.28 in the text (table).
4. **Muñoz 2018 Table 1 distances** are a literature compilation and the paper names no source per object. They are used only to undo the paper's own M_V (D-061 item 3).

## And XII (D-062)

Collins 2013 prints σ = 0.0 (+4.0) and calls the dispersion unresolved, without stating a limit. It is plotted as an upper limit at 4.0 km/s, the 1σ upper end, flagged `limit_from_1sigma_upper_error`.

## Leo II

Its distance original, Monelli et al. 2025 (A&A 700, A201), was read from the journal PDF (JvH; sha256 6cf940d5…). Two readers agree on the headline (m−M)₀ = 21.60 ± 0.03 (`reading/residual_reading_{1,2}_leo2.csv`). It enters through the frozen input assembly v2.

## Printed m_V,0 errors (after PR #85)

The input assembly had taken the magnitude error only on the M_V route. For the 25 systems whose paper prints m_V,0 itself, g_bar had no magnitude error. `reproduction/inputs_magerr.py` (frozen before it ran) carries those printed errors from the double-read structure readings. Test 1, version 3, checks them against the second reading: all 50 are found. No g_obs or g_bar value changed; only g_bar's error columns did.

## Not plotted (recorded)

- **And XIII:** no [Fe/H] (D-059).
