# aeg-d-kids1000-rar/v2: reproduction result

**Result: PASS.** All fifteen items of the frozen test `REPRODUCTION_REV3.md` (SHA-256 `57ae39ae…ae7e`, `data/frozen/kids-v2-test-rev3.json`) hold. Item 12 was checked against a copy of the release built from the public mirror; against the canonical tarball it is decided by CI, which runs the same check in `convert.py` on every build (see item 12).

## The first frozen test's item 11 failed (item 15; D-103 rule 2)

- The first frozen v2 test, `REPRODUCTION.md` (SHA-256 `b44f5a58…190b`), allowed exactly one D-096 finding: the hot-gas variant.
- Its second reading found another. The source leaves KiDS-bright rows 1–8, beyond its isolation limit, out of its tests of analytical models (Brouwer et al. 2021, l. 508, 748, 821). Under that test, **item 11 failed.**
- JvH ruled D-103 (2026-11-05): D-096 rule 2 applies, no value changes, and the test is re-issued. `REPRODUCTION_REV3.md` was written and frozen by ruling **before any v2 value existed**. The first test stays unedited.
- The other items of the first test are scored here as `REPRODUCTION_REV3.md` restates them.
- **D-096 rule 4 counts:** 8 rows change plotting status under D-096 rule 2 (D-103: KiDS-bright rows 1–8), and 15 under D-096 rule 3 (the hot-gas variant). **No value changes.** 22 of 45 rows are plotted (v1: 45).

## Item by item

The scored run was the first complete run of `convert.py`, on 2026-11-05, with the release copy described under item 12. The mechanical checks are `reproduction/score.py`; its output is `reproduction/score.json`.

1. **Rows: pass.** 45 rows; row k has v1 row k's sample and `source_ref`.
2. **Values unchanged: pass.**
   - `g_obs`, `g_obs_err_lo`, `g_obs_err_hi`, `g_bar` and the four `x_kids1000_rar_*` columns are bit-for-bit equal to v1 on all 45 rows (identical float64, compared by hex).
   - Every other v1 column is unchanged apart from the prefix of `measurement_id`. The v1 columns that changed are the allowed ones: `flags`, `assumptions`, `gas_hot_status` (hot-gas rows; item 9), `notes`, `role`, `plotted`, `not_plotted_reason` and `alternative_of`.
   - `method` keeps v1's text. Item 7 asks for the built-in term K6 to be stated in the method text; it is stated in the `method` column's description, so that item 2 holds.
3. **Covariance: pass.** 675 entries, identical to v1 apart from the prefix.
4. **g_obs error: pass.** K1 only, as v1; `err_level` 0.683, `err_level_status` stated (README "1-sigma"); no point-scale columns.
5. **g_bar as the bin coordinate: pass.** `g_bar_basis = bin_coordinate`, empty g_bar errors, bin edges equal to 10^(−15 + (k−1)Δ) and 10^(−15 + kΔ) within 1e-12, every g_bar inside its bin, and the hot-gas rows' notes state that their use of these edges is the Atlas's inference.
6. **Flags and known issues: pass.** `no_uncertainty` removed (#64's subject is now `g_bar_basis`); `source_quality_low` on the same 16 rows as v1. Known issues opened and linked in `known_issues.json`: #168 (the hot-gas rows may be under-flagged) and #169 (the limit written as both 0.3 and 3 h70⁻¹ Mpc, as the source prints it).
7. **Uncertainty terms: pass.** Exactly the eleven rows of the table, with `covariance = not_published`, citations and locations. Registry entries for v2: `deproj_lensing`, `hot_gas_halo` (as v1) and the new `baryons_point_mass` (K14). Each row's `assumptions` lists them as specified.
8. **Observables: pass.** 90 rows, two per measurement: `delta_sigma` (ESD_t, the released error, 0.683 stated) and `acceleration_released` (g_bar, described as the bin's arithmetic midpoint, with the source's steps; for the hot-gas rows, the assumed halo).
9. **Measurement columns: pass.**
   - All rows: `measured_quantity` g_obs, `limit` none, tier 1, `population_bin`, `model_dependence` total_mass_form; statuses as v1, except `gas_hot_status = modelled` on the hot-gas rows.
   - GAMA and KiDS-bright rows 9–15: default, plotted.
   - KiDS-bright rows 1–8: default, not plotted, `other`, with the three quotations, the source's reason and the D-103 sentence in `notes`.
   - Hot-gas rows: alternatives of the KiDS-bright row with the same bin index, not plotted, `alternative_value`.
   - The dataset page states both choices and why ("What is plotted"). No `excluded.csv` rows: these are bins, not systems.
10. **Descriptor: pass.** Standard 2.5.1; no `x_value_change_ruling` (D-103 rule 1: no value changes); `x_selection`, `x_precedence` (with D-103), `x_baryon_inventory` (stars measured, cold gas modelled, hot gas known but unmeasured, cool and warm gas and dust known but unmeasured, remnants not addressed), `x_search_log` and `x_second_reading`.
11. **Second reading: pass.**
    - Every packaged number equals the frozen reading by the named pairs: 0 mismatches over 45 rows. The bin edges agree within 1e-12.
    - `convert.py` regenerated the covariance reading with the frozen parser into the gitignored `source/reading/`. Its SHA-256 equals the frozen `off_repo` hash, and so does the regenerated second-reading CSV.
    - The packaged covariance equals that reading's covariance, divided by column 7 (`bias_product`) and converted as v1: 0 mismatches over 675 entries.
    - Plotting statuses match the reading's two findings (the hot-gas variant; KiDS-bright rows 1–8).
12. **Release provenance: pass here; decided in CI against the canonical tarball.**
    - `convert.py` checks, before writing any table, that each of the seven release members used has the SHA-256 listed in the frozen `reading/kids-d096.md`, and stops otherwise.
    - The canonical tarball (`kids.strw.leidenuniv.nl`) is refused by this workspace's proxy. So the scored run used a tar assembled from the same mirror the second reading used (`rstpier/EFF_G_GALAXIES` at `7606a21d…`), in the gitignored `source/` folder. All seven members matched, as they must, since the reading was made from those files.
    - In CI, `aeg.fetch` downloads the canonical tarball (hash `73adc2d4…8733`, as v1) and `convert.py` runs the same check on its members. CI also requires the rebuilt tables to equal the committed ones. **If either fails, item 12 fails. If CI cannot reach the tarball, the test is blocked, not scored, and v2 is not published.** The pull request's `packages` check records the outcome.
13. **Standard and site: pass.** `python -m aeg.validate data/packages/aeg-d-kids1000-rar/v2` passes under 2.5.1; `python -m aeg.formula_check` passes; the site builds (642 pages); `aeg.site_check` reports 0 errors; the reproduction ledger (`data/reproduction.json`) records the test's SHA-256, which the build verifies against the file and `sources.json`. `aeg.check` passes; pytest: 216 passed.
14. **v1 untouched: pass.** `git diff 5dc4091 -- data/packages/aeg-d-kids1000-rar/v1` is empty.
15. **Reporting: pass.** This file states the first test's item 11 failure, the ruling, and the D-096 rule 4 counts above.

## What was and was not verified

- **Verified:** every item above by script or command; the two hash checks that `convert.py` performs (seven release members; the regenerated readings).
- **Not verified here:**
  - the canonical tarball itself, which this workspace cannot reach (item 12, decided in CI);
  - the rendered dataset page by eye: it was checked by text search of the built HTML.
- **Disclosed:** the first run of `score.py` stopped on a bug in the scorer itself (it passed a text buffer where astropy expects a string). The scorer was fixed and run once. The conversion was not re-run or changed.
