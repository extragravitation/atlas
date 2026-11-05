# aeg-d-gc-baumgardt/v2: second reading

The v2 second reading (frozen test item 11; D-031 item 3) was done before the first v2 conversion. The reader had no access to `convert.py`, v1's g values or any v2 table. It was frozen by hash in `data/frozen/gc-v2-reading.json`, through the pull request merged on 2026-11-04 (#157).

**Files** (in `reading/`):
- `d096_d097.csv`: the D-096 fields (preferred values, excluded data, fiducial baselines) and the D-097 statements and classes for every cluster with a measurement row, and the D-099 rule 3 anchors.
- `err_levels.csv`: the confidence level per dispersion dataset code, and for g_bar.
- `binary_screening.csv`: the binary-screening value per dispersion dataset code.
- `resolutions.md`: dissent and disagreements, with how each was settled.
- `BRIEF.md`: the reader's brief. The three `manifest_*.csv` files are v1's rows, observables and systems, without g values.

**What the converter takes from it.** `convert.py` applies changes, exclusions, possibilities, anchor notes, confidence levels and screening values only from these files. Values that do not change are carried over from v1, whose own second reading (3 535 of 3 535 numbers; `../v1/SECOND_READING.md`) still stands for them.

**Comparison.** The package is compared with these files field by field in `REPRODUCTION_RESULT.md` (item 11).
