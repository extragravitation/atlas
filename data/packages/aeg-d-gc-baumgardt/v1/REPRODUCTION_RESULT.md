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
