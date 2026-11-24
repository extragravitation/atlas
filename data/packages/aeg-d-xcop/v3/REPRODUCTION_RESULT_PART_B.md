# aeg-d-xcop/v2: reproduction test, part B — result

**PASS.** All thirteen items of the frozen part B test hold (`REPRODUCTION_PART_B.md`, SHA-256 `89640ef17b7d58d8ecca2002bfe6e24eabc61898d769f7e4c199266f85ea115d`, frozen in `data/frozen/xcop-v2-part-b.json`). Part A's result stands beside it, unchanged (D-091).

**Run** 2026-11-05 by `reproduction/score.py`, once, mechanically, after the second reading was frozen (`data/frozen/xcop-v2-reading.json`) and the off-repo `values.csv` was verified against its recorded hash. Machine-readable outcomes: `reproduction/result_part_b.json`.

**Consent gate (D-090 rule 5).** This file, the JSON and every log of the run hold outcomes, counts, hashes and booleans only, never a row value. The v2 tables are not committed (`.gitignore`); `checksums.sha256` holds their hashes.

**Build-only fix, disclosed.** The first scoring run (`reproduction/result_part_b_run1.json`, kept) failed item 12 on two errors in the scoring procedure, not in the package: build 1's site had been built before a later edit to `sources.json` (its `licence` text), so two download files were stale; and build 2's site check was run with the v2 tables present, so it looked for v2 downloads that build 2 correctly does not have. The procedure was corrected (build 1 rebuilt after the last package edit; `score.py` moves the v2 tables aside while checking build 2) and the score run again. No package file, value or rule changed between the runs. Items 1–11 and 13 have identical outcomes in both runs; item 12 differs only in those two site checks.

## Summary

| Item | Outcome | One line |
|---|---|---|
| 1 Rows | **pass** | 109 rows in file order (A644 19, A1795 21, A2029 22, A2142 20, A2319 27), v1's system IDs, `m000001`–`m000109`, profile_point / dynamics / hydrostatic. |
| 2 Values | **pass** | `r_kpc`, `g_obs`, `g_bar` equal RADIUS, GOBS, GBAR of the reader's `values.csv` bit for bit on 109 of 109 rows; component columns empty; statuses `not_separable` (stars, hot gas), cold gas as v1. |
| 3 Changed values | **pass** | The reading names no exclusion; no row is recorded and not plotted. v2 is not compared with v1 (D-090 rule 1). |
| 4 Arithmetic | **pass** | 109 of 109 rows equal their two observables exactly. |
| 5 Errors and levels | **pass** | Error form from `error_form.md`: magnitudes (not undetermined). 109 of 109 rows carry the error columns as item 5 sets them; `g_bar_err_point_*` empty; levels `not_given_by_source` on both sides. |
| 6 Extension columns | **pass** | All columns present with headers; α as printed (unit "as printed (per cent inferred, not stated)"), w in 10⁻³ as printed; A7 ratios at stored precision; `x_xcop_mass_model_frac` recomputed equal to A644 0.2241, A1795 0.0617, A2029 0.1459, A2142 0.0852, A2319 0.0518; no rule-1 column. |
| 7 Terms and registry | **pass** | Exactly the 22 terms; `bcg_ml_extra_mass_model` applies to A644 and A2319 (from the reading); `xray_hse_bias` v2 entry (five formulas, 0–0.2, E22 l. 502 and l. 539); `xcop_hse_equilibrium`, `xcop_spherical` added; no v2 entry for `icl_fraction` or `stars_cluster_modelled`. |
| 8 Tables | **pass** | 218 observables with the item 8 steps and source texts; 12 systems with Table 1 values only in `properties`; all 109 rows plotted, default; no `no_uncertainty` flag. |
| 9 Named items | **pass** | D-092 note and flag on A644's 19 rows only, and both layers on its page; A2319's 7 statements on its 27 rows in file order, and both sentences on its page; stellar-projection note with the A9 ratios on every row; hydrostatic sentences on the dataset page; the seven "Recorded, not plotted" pages state the register's reason, not D-097 wording; known issues #124, #129, #136, #178 (A3158), #179 (D-091 erratum). |
| 10 Descriptor | **pass** | Standard 2.5.1; `x_publication` `awaiting_authors_consent`; `x_value_change_ruling` D-090 with both sentences on the page; `x_precedence`, `x_second_reading`, `x_baryon_inventory` as item 10; `sources.json` with both archives (hashes, member hashes, "not stated; asked (#19)", not redistributable) and five e-prints with bytes and SHA-256. |
| 11 Second reading | **pass** | All eight pairs agree. |
| 12 Standard and site | **pass** | Build 1 (local, tables present): `aeg.validate` passes, `aeg.formula_check` passes with the v2 entry on 109 rows, `site_check` 0 errors, page texts present. Build 2 (as deployed): no v2 table tracked (the tables are ignored), `site_check` 0 errors, v1 current with the rule-5 sentence, no v2 page, map point or download. Log check: 14 captured local logs, 0 hits for 1 467 search strings. |
| 13 v1 untouched | **pass** | No file of `aeg-d-xcop/v1/` differs from commit `5dc4091`. |

## Where each item ran

- **Locally only** (need the off-repo `values.csv` or the v2 tables): items 2, 4, 5 and 11, build 1 of item 12, and the log check. Items 1, 3 and 6–10 also read the local tables.
- **In CI as well:** build 2 (the deployed site is built from the repository, which holds no v2 table), item 13, and the determinism check: CI regenerates the tables from the fetched archives and compares `checksums.sha256` with the committed file. Locally, two conversions gave identical table hashes.
- **The log check** covered the local logs of the converter, fetch, validator, formula check, pipeline and package tests, both site builds, both site checks and `npm test`. The captured CI log of this pull request is searched the same way once CI has run; the outcome is reported on the pull request.
- Until the authors confirm, the package is reproducible from the public archives plus `convert.py`, not from the repository alone (part B item 12).

## Not tested here

As the test lists: the source's error sizes; part A's checks; the questions with the authors (A644's GBAR, Table 4 units, the stellar projection, A3158's negative masses, the valid radial range, the meaning of the error columns); the seven clusters' g_bar and stage 2 (#129); the X-COP v2 audit (D-090 rule 3).

## Published (D-106)

- **Published 2026-11-05** under D-106 (JvH: "publish the site and then forward them links to it for their review"), replacing D-090 rule 5's waiting period. The authors are told the same day, with links and the `03c` questions, and their wishes are followed.
- **What changed at publication:**
  - the v2 tables are committed, and the ignore rule for them is removed;
  - `x_publication` is `published` in the descriptor;
  - the reproduction ledger has its v2 entry;
  - the descriptor's description and licence-status text no longer say the version waits for the authors;
  - `sources.json` status, `convert.py` docstring and one print line are updated.
- **Determinism.** `aeg.fetch` followed by `convert.py` reproduced the four table hashes in the `checksums.sha256` committed by #180, byte for byte. Only the metadata files' hashes change.
- **What did not change:** no value, row, rule or test. This section is the only addition to this file. The scored outcomes above stand.
- **The archives are still not committed** (D-004). Only the derived rows and their observables are published.
