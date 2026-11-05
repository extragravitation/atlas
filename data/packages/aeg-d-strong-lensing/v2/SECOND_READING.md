# aeg-d-strong-lensing/v2: second reading

The v2 second reading (frozen test item 11; D-031 item 3) was done before the first v2 conversion. The reader had no access to `convert.py`, v1's g values or any v2 table. The main session's resolutions of the reader's six calls were added without access to any g value. The reading was frozen by hash in `data/frozen/lenses-v2-reading.json`, through the pull request merged on 2026-11-05 (#171).

**Files** (in `reading/`):
- `d096.csv`: the D-096 fields (preferred values, excluded data, fiducial baselines) for every source used, with quote and location. No D-096 case was found.
- `theta_class.csv`: per measurement row, the rule 5 class (A, B, no θ_E error, aperture), the fractional θ_E error as printed, and its quote and location.
- `profiles.csv`: per system with a light-profile row, the profile the source prints, or "none printed".
- `err_levels.csv`: per source and side, the confidence level of each error used, as stated.
- `distance.csv`: per source, the adopted H0 and any alternative it tests (for a named paper, its abstract headline value), and any peculiar-velocity or redshift-frame statement with its size and the quantity it is stated in.
- `baryon_inventory.csv`: per source, what it states about a central black hole, gas and dust inside R_E.
- `resolutions.md`: the reader's findings and disagreements, and the six resolutions.

**What the converter takes from it.** `convert.py` takes θ_E classes and fractions, light profiles, confidence levels, the H0 and distance cross-checks and the black-hole inventory only from these files, and refuses to run if any file differs from its freeze record. Values that do not change are carried over from v1, whose own second reading (1 496 of 1 496 numbers, version 5; `../v1/SECOND_READING.md`) still stands for them.

**Comparison.** The package is compared with these files field by field in `REPRODUCTION_RESULT.md` (item 11), by `reproduction/score.py`.

**Step A.** The term sizes of item 7 rest on step A's two concordant readings (A and B) and the corrections of review 1 checked at source (`docs/sources/readings/step-a-2026-11-04/`), which serve as the D-031 second reading for those sizes.
