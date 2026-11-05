# aeg-d-strong-lensing/v2: reproduction result

**Result: PASS.** All 13 items of the frozen test hold.

- **Test:** `REPRODUCTION.md`, SHA-256 `49dc59c46e6cae4841f7833bfc50165b95dd3969f9b84157cbf96b45be66ab5a`, frozen in `data/frozen/lenses-v2-test.json` (#166).
- **Second reading:** `reading/`, frozen in `data/frozen/lenses-v2-reading.json` (#171), with the main session's six resolutions.
- **Scored run:** one complete conversion, 2026-11-05 14:28 UTC (`convert.py`, SHA-256 `e0466a8a…87f9`), from an empty `tables/` folder; scored once at 14:30 UTC by `reproduction/score.py --site site/dist --fetch-abstracts`, output in `reproduction/score.json`. No code in `convert.py` or `score.py` was changed after the run.
- **Before the scored run:** `convert.py` was run during development to check structure only (the validator, `check_formulas.py`, the site build). No g value was printed or inspected; v2 copies v1's values, so there was nothing to tune. The black-hole components were then moved from the hand-written descriptor into `convert.py`, so that they come from the frozen reading, before the scored run.

## Counts

| What | Count |
|---|---|
| Measurement rows (defaults, alternatives) | 147 (94, 53), as v1 |
| Rows with changed values (D-096) | 0 |
| Class A rows: θ_E error carried by g_bar | 107 (SLACS 96, SL2S 6, MaNGA 2, NGC 6505 2, J0403−0239 1) |
| Of these, with the θ_E fraction column filled | 105 (NGC 6505's lower bound is the term `theta_e_ngc6505`) |
| Of these, effect on g_bar not computed (no printed profile, D-104 rule 3) | 5 (MaNGA 2, NGC 6505 2, J0403−0239 1) |
| Rows with `x_strong_lensing_dlngbar_dlntheta` | 139 (SLACS 96, S4TM 37, SL2S 6) |
| New observables (R5 de Vaucouleurs R_e, SLACS) | 48, `o000631` to `o000678` |
| Uncertainty terms | 44 |
| Rows plotted | 94, as v1 |

## Items

1. **Rows: PASS.** 147 rows (94 defaults, 53 alternatives) in v1's order, each with v1's `system_id`, `role`, `alternative_of` and scope, and the same ID apart from the prefix. 212 systems.
2. **What may change: PASS.** Every v1 column was compared on every row after the prefix change. The only differences are the ones the test allows:
   - `g_obs_err_lo/hi`, empty on the 107 class A rows;
   - IDs;
   - `baryonic_from`, which gains the SLACS R_e observables;
   - `notes` on class A rows and on SNL-1 and SNL-2;
   - `assumptions`, which gains `a6s_theta_e` and `a6s_lens_distance`;
   - `flags`, which gains `no_uncertainty` on class A rows.

   The 19 new columns are exactly those of items 5 and 6. Systems are unchanged. The 630 v1 observables are unchanged apart from the prefix and the two empty level columns. The 48 new observables are appended from `o000631`, each named in its system's rows.
3. **Changed values: PASS.** None expected and none found. The 39 rows of `d096.csv` are all "no", and the 37 value columns are bit-for-bit equal to v1 on every row. There is no `x_value_change_ruling`.
4. **Arithmetic: PASS.**
   - 1 178 recomputations with v1's frozen test-3 code (`aeg.lensing`) agree to 10⁻⁹. They cover M_E, R_E, L × M/L, f(<R_E), M*(<R_E), g_obs, g_bar and its components.
   - `dlngbar_dlntheta` agrees to 10⁻⁶ on 139 rows.
   - `g_bar_stars_ref` agrees to 10⁻¹² on 147 rows.
5. **Error columns and levels: PASS.**
   - The point columns equal the error columns everywhere except the two MaNGA lenses. There, `g_bar_err_point_*` hold the L_Ein error alone, recomputed from the observables.
   - Levels, from `err_levels.csv`:
     - R13 g_bar: `stated` 0.683 (all 96 SLACS rows);
     - R20, R26, R29, R30 and R32 g_bar: `not_given_by_source`;
     - R28 and R61 g_obs: `not_given_by_source`;
     - empty where the column is empty (class A g_obs; S4TM both sides).
   - R20's g_bar level was left to the reading, which records `not_given_by_source`. R32's combined `g_bar_err_*` is `not_given_by_source`: one component (L_Ein) has no stated level, although the reading finds an implied 1σ for the Υ_ref component (reading 3.6).
6. **New extension columns: PASS.**
   - θ_E fractions on 105 class A rows (SLACS 0.02). They are empty on NGC 6505 and outside class A.
   - Profile columns on the 96 SLACS rows. `dlngbar_dlntheta` is filled exactly where a profile is printed.
   - The single-system sizes are on J0403−0239 (0.03), SNL-0 (0.02) and SNL-2 (0.015).
   - `r_eff_err_frac` on the six SL2S rows: 0.30 for the CFHT R_e (defaults), 0.10 for the HST R_e (alternatives).
   - Every header names its term or formula and says what an empty value means.
7. **Uncertainty terms and registry: PASS.**
   - The 44 terms match the frozen table in scale, `applies_to` (built from the scopes in systems-table order), moves, status, size, size kind, unit, assumption, `in_error_columns` and covariance.
   - Every `a6s_*` entry has a v2 registry entry, appended:
     - `a6s_source_cosmology` corrected (D-094);
     - `a6s_theta_e` and `a6s_lens_distance` new, at the end of the list, so gas comes before θ_E;
     - the gas formula reads `x_strong_lensing_g_bar_stars_ref`;
     - `a6s_stellar_imf` copied.
   - `check_formulas.py`: 23 726 Python/JavaScript evaluations, 0 problems.
     - Rows not evaluated: `a6s_theta_e` 8 (the 5 class A rows without a profile, and SNL-0, SNL-1, SNL-2); `a6s_stellar_imf` 3 (SNELLS, no Salpeter top); others 0.
     - **Disclosed reading of "every column it names is filled":** an effect on a column that is empty in the row (for example `g_obs_err_*` on class A rows) is left out, because that column stays empty. The entry is then evaluated if every column its remaining effects name is filled. Read strictly, H0 and lens distance would be evaluated on only the 3 SNELLS rows (the only rows with `g_obs_err_*` filled). Read this way, they are evaluated on all 147 rows.
8. **Plotting: PASS.** 94 rows plotted, and the 53 alternatives `plotted = false` with `alternative_value`, as v1.
9. **Named items: PASS.**
   - F1 and F2 are stated on the dataset page (the descriptor description) and in known issue #139.
   - NGC 6505's lower-bound note is on both of its rows.
   - The black hole is recorded as two inventory components, built from `baryon_inventory.csv`.
   - The 28 v1 sources are carried with v1's hashes.
   - The three abstract pages were fetched at scoring; all three hashes match item 9.
   - The built v2 dataset page contains "θ_E error stated; effect on g_bar not computed" (HTML unescaped).
10. **Descriptor: PASS.**
    - `standard_version` is 2.5.1.
    - `x_second_reading` points to `SECOND_READING.md`, the seven reading files and the freeze record.
    - The inventory is v1's six components plus the two black-hole components.
    - `x_previous_version`, `x_reproduction` and `x_known_issues` are added.
11. **Second reading: PASS.**
    - The reading files are unchanged since freezing.
    - Classes: A 107, no θ_E error 37, aperture 2, B 1, as `theta_class.csv`.
    - θ_E, fractions, profiles, levels, H0 values, the peculiar-velocity size and the black-hole statuses equal the reading.
    - The SNELLS pair is R25's own comparison, 67 against 70 (resolution 5). R25's adopted 70.4 is in the term note.
12. **Standard and site: PASS.**
    - `aeg.validate` passes on the package under 2.5.1.
    - `check_formulas.py` and `aeg.formula_check` pass.
    - `test_lensing.py`: 14 passed.
    - The site builds (643 pages), and `aeg.site_check` reports 0 errors.
    - The ledger hash check passes: the reproduction page builds with this entry, and `sources.json` records the test's hash.
13. **v1 untouched: PASS.** All 75 files of `aeg-d-strong-lensing/v1/` are identical to commit `5dc4091`.

## What was and wasn't verified

- **Verified mechanically:** everything above, by `score.py` reading the tables, the frozen reading and v1, independently of `convert.py`.
- **Disclosed reading of the test:**
  - `check_formulas.py`'s rule for empty affected columns (item 7, above).
  - The SNELLS H0 pair 67/70 follows resolution 5, as the frozen test states it.
  - The three abstract pages are kept under `reference_pages` in `sources.json`, not under `sources`. A change to arXiv's page layout therefore cannot stop the CI fetch. `score.py --fetch-abstracts` checks them by hash, or, if the page has changed, by the quoted H0.
- **Corrected in the result, not in the data:**
  - Test item 4 gives the basis for `total_mass_form` on SNL-1 and SNL-2 as the half-image-separation approximation. That does not hold at source (reading 2.2). Their masses come from full lens models inside R_ap (R61 l. 209). The value `total_mass_form` is unchanged. The row notes give the corrected reason (resolution 2).
  - The test's "R61 Table 2 l. 151" is Table 1 (reading 3.3). The term note says so.
- **Known issue opened:** #174, for SNL-1's stated gas and for J0403−0239's nebular emission and dust (resolutions 3 and 4), to be handled in the next version.
- **Site changes:** v2 has no checks or reading of its own for v1's values, so the lens dataset and system pages now read v1's readings, checks and test summary from v1 (`evidenceVersion` in `site/src/lib/lensing.mjs`). They also say so. The system pages also show where the θ_E error is carried, and the D-104 rule 3 line where it applies.
- **Not verified here, as the test states:** whether the sources' error sizes are right; the θ_E effect where no profile is printed; NGC 6505's redshift-error effects; and the R_e error's effect through f(<R_E). v1's tests 1–4 were not re-run.
- **After scoring:** the ledger entry was written with this result. The site was then rebuilt and checked again, and `convert.py` was run again to refresh `checksums.sha256` with the result files. The tables were byte-identical to the scored run.
