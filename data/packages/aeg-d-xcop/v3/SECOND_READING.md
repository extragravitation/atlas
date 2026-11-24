# aeg-d-xcop/v2: second reading

The v2 second reading (part B item 11; D-031 item 3) was done before the first v2 conversion, by an independent reader with no access to `convert.py`, any v2 table or v1's tables. It was resolved and frozen by hash in `data/frozen/xcop-v2-reading.json` (merged before conversion; order of work step 3).

**Files** (in `reading/`):
- `values.json`: the reader's own parse of the five `gbar_gobs_<C>.fits` files, as hashes only (per row and per cluster). The parsed rows are in `source/reading/values.csv`, which is **not committed**: the archives are not redistributed (D-004) and v2 is not published until the authors confirm (D-090 rule 5). Its SHA-256 is recorded under `off_repo` in the freeze record.
- `error_form.md`: the meaning of the error columns. The headers say nothing; part B item 5's rule decides: error magnitudes for GOBS_ERR_LO/HI and GBAR_ERR.
- `model_form.md`: part B rule 3's criterion. No such statement, so `model_dependence` = `none`.
- `d096.csv`: the D-096 fields per source and file under rule 1's explicit-wording criterion. No exclusion, preferred value or fiducial baseline among the released values.
- `err_levels.csv`: the confidence levels, `not_given_by_source` on both sides.
- `properties.csv`: per cluster, the centroid shift w (Paper II Table 2, as printed, 10⁻³) and the non-thermal pressure fraction α at R500 and R200 (Ettori & Eckert 2022, last column, as printed, signs included; unit `inferred_percent`).
- `hse_statements.csv`: every statement on hydrostatic validity in E22 and Paper II, in file order; seven are marked for A2319's notes.
- `bcg_extra_mass_systems.md`: E22 l. 109's "8.3 ± 2.9 per cent" describes A644 and A2319 only.
- `resolutions.md`: agreements, disagreements and how each was settled at source. No rule-1 conflict for JvH.

**What the converter takes from it.** `convert.py` takes the error form, model form, D-096 outcome, confidence levels, cluster properties, A2319's statements and the central-galaxy systems only from these files, and its values only from the archive verified by hash (part A §1).

**Comparison.** The package is compared with these files field by field, by the pairs part B item 11 lists, in `REPRODUCTION_RESULT_PART_B.md`. The comparison with `values.csv` runs locally only, and the result records outcomes and counts, never values.
