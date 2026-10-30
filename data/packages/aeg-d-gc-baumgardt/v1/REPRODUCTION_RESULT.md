# aeg-d-gc-baumgardt/v1 — reproduction result

**Test 2 (King 1966 reproduces the published King fits): FAIL.** 152 of 153 rows are within tolerance; MW-PAL1 is outside. Run on 2026-10-30 by `reproduction/test2_king_fits.py`, as frozen in REPRODUCTION.md (hash in `sources.json`). Per-row results are in `checks/test2_king_fits.csv`. As REPRODUCTION.md requires, the conversion has not been run, and tests 1, 3 and 4 have not been run.

| | Concentration c | log R_c (half-power) | log R_h (half-light) |
|---|---|---|---|
| Rows within 0.02 | 153 of 153 | 152 of 153 | 152 of 153 |
| Median \|Δ\| | 0.0022 | 0.0006 dex | 0.0006 dex |
| Largest \|Δ\| | 0.0055 | 0.0623 dex (MW-PAL1) | 0.0620 dex (MW-PAL1) |

## Diagnosis (after the result; does not change it)

For MW-PAL1, the table's scale radius in parsecs (`r0pc` = 0.040) differs by 0.060 dex from its own angular scale radius times its own distance (0.660″ × 10.9 kpc = 0.0349 pc). For the other 152 King rows these agree within 0.0054 dex.

With 0.0349 pc, the frozen code reproduces MW-PAL1's published c, R_c and R_h within 0.003. The published R_c and R_h therefore correspond to the angular radius, and the `r0pc` entry is inconsistent with the rest of the row. This points to the source table, not to `aeg.king66`.

Pal 1 has a single line-of-sight bin in the Baumgardt profiles. Under the frozen D-036 conversion it could not be converted in any case: edges cannot be inferred from one radius.

No dispersion profile has been converted, and no g_obs or g_bar has been computed.

## Status

The package does not ship on this result. Whether and how it proceeds is for JvH to rule, as a logged decision made after the result (D-031 item 2).

**Ruled 2026-10-30 (D-046, after the result):**
- The FAIL stands, permanently.
- The conversion and the remaining tests run as frozen.
- MW-PAL1 is recorded, not plotted.
- The decision goes to the outside reader at the v1.0 review. If the reader does not confirm it, the package stays out of v1.0.

## Test 4 (pre-registered decision on Harris r_c), run 2026-10-30: D-045 reading rejected

Run by `reproduction/test4_harris_rc.py` on the 85 clusters with both a McLaughlin & van der Marel King fit and Harris c and r_c (per cluster: `checks/test4_harris_rc.csv`).

| Comparison | Median \|Δ log\| |
|---|---|
| (a) Harris r_c against King scale radius r₀ | 0.030 dex |
| (b) Harris r_c against half-power radius R_c | 0.003 dex |

Since (a) > (b), Harris r_c is the half-power (observed) core radius, not r₀. As pre-registered, clusters whose only structural model would come from Harris are **recorded, not plotted**, and the question returns to JvH. Also reported: c_Harris − Conc has median +0.000 and standard deviation 0.162.

## Conversion run (no acceleration value looked at)

Under D-045 and D-046 with the test 4 outcome, 64 of 155 clusters have a plottable value. For all 64 the default is the Baumgardt RV profile, which ranks first because the per-star velocities are released (D-038 3B). The rest are recorded with these reasons (a cluster can have several):

- 90: no line-of-sight candidate passing the plotting rules. Of the converted candidates, 15 had coverage below 0.80; 70 had no structural model; 13 had one bin only.
- 36: Harris-only structure (test 4).
- 24: Harris core-collapse flag (`c` or `c:`) with no McLaughlin & van der Marel fit.
- 13: no tabulated population M/L_V.
- 11: no structural model at all.
- 10: no Harris distance (D-042).
- 10: no Harris integrated magnitude.
- 1: A7 (Crater).
- 1: MW-PAL1 (D-046).
- 1: proper motions only.

Integral-field datasets (MUSE, ARGUS) give no star counts. In the precedence ranking they count as 0 stars; this decided no default.

Tests 1 (transcription) and 3 (arithmetic) run when the tables are written. The g_obs and g_bar values have been computed in memory but not looked at, and will not be until JvH rules on the Harris-only clusters.

## D-037 reproduction check (reported, not pass/fail), reconstructed binning

Run by `reproduction/d037_check.py`. Per bin: `checks/d037_rv_bins.csv`; per cluster: `checks/d037_rv_clusters.csv`.

| Clusters | |
|---|---|
| pass | 3 (Crater, Laevens 3, Pal 8) |
| fail | 1 (NGC 6638) |
| not testable | 148 |

**Not testable (148):** membership is not reproduced. Across all clusters, the published RV bins contain 116 544 stars, but the released RV files give 54 067 members (probability > 0.5) and 42 412 after the binary rule. The profiles therefore use velocities that are not in the released files; the database page notes that most VLT/MUSE data are not included. One cluster has no RV file in the release.

**Fail (NGC 6638, one bin of 12 stars):** the published value is 4.40 (−0.88, +1.24) km s⁻¹; the recomputed value is 3.25 [2.57, 4.21] km s⁻¹. The rebuilt mean radius is 69.9″ against 78.7″ published, so the star set probably differs.
