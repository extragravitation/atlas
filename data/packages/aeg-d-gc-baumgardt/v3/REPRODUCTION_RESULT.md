# aeg-d-gc-baumgardt/v2: reproduction result

**Result: PASS.** All 13 items of the frozen test hold, with one disclosure on item 12. On its first attempt the site build stopped on a site component bug, not on the package; see item 12.

- **Test:** `REPRODUCTION.md`, SHA-256 `4bb0d6da0bf00bab5be644588d68006ee419fc43d5a361f04c53a6e6ec5585e4`, frozen in `data/frozen/gc-v2-test.json` (#150, #151).
- **Second reading:** `reading/`, frozen in `data/frozen/gc-v2-reading.json` (#157).
- **Scored run:** one complete conversion, 2026-11-05 12:46 UTC (`convert.py`), scored by `reproduction/score.py`, with the output in `reproduction/score.json`. No code in `convert.py` was changed after the run.

## Counts (item 8)

| What | Count |
|---|---|
| Rows changed under D-096 | 1 (M54, `m000067`) |
| Systems excluded under D-097 | 2 (NGC 2298, Pal 5) |
| Possibilities recorded | 0 |
| Rows with a D-099 rule 3 anchor note | 10 (9 clusters; NGC 5139 has 2 rows) |
| Rows plotted | 62 of 79 (v1: 64) |

## The one changed value (item 3)

**M54 (NGC 6715), `aeg-d-gc-baumgardt/v2/m000067`.**
- **Rule:** D-096 rule 2, as clarified by D-098 rule 1.
- **Source:** Baumgardt 2017 (B17), arXiv 1609.08794v1, `paper.tex` l. 588–589: "We have therefore neglected all data points beyond 200'' in the dynamical analysis of this cluster."
- **Bins dropped:** `o002481` (⟨r⟩ = 269.01″), `o002482` (410.12″) and `o002483` (679.1″). 13 of 16 bins are kept.
- **Known issue #159:** the bins at 170.92″ and 269.01″ may straddle 200″, because only each bin's mean radius is stored.

| | v1 | v2 |
|---|---|---|
| σ (km/s) | 12.3164 (−0.2720 / +0.3209) | 12.7373 (−0.2892 / +0.3410) |
| Light coverage | 1.000 | 0.907 |
| Bins | 16 | 13 |
| g_obs (m s⁻²) | 1.7486 × 10⁻⁹ (−0.0764 / +0.0923 × 10⁻⁹) | 1.8701 × 10⁻⁹ (−0.0840 / +0.1015 × 10⁻⁹) |
| Plotted | yes | yes (coverage ≥ 0.80, ≥ 2 bins) |

**Check:** `aeg.dispersion` with `aeg.king66` weights (v1's frozen code), run on v1's bins minus the three dropped bins, gives the same σ, errors, coverage and bin count, to a relative 10⁻⁹. Before applying the change, the converter confirmed that this code on all 16 bins reproduces v1's σ and coverage exactly. No other row's values changed.

## Items

1. **Rows: PASS.** There are 79 rows, in v1's order, with v1's `system_id` and dataset code, and the same `measurement_id` apart from the prefix. The excluded systems keep their rows.
2. **What may change: PASS.** Every v1 column was compared on every row, after the ID prefix change.
   - **Measurements.** Only the listed exceptions differ:
     - `model_dependence`, now `none` on every row;
     - `assumptions`, which gains the six new registry IDs;
     - `baryonic_from`, which gains each row's V_t observable;
     - on M54: `observed_from`, `notes` and the item 3 values;
     - on the excluded rows: plotting, role, `alternative_of`, reason and notes;
     - anchor notes.
   - **New measurement columns** are only those of items 5, 6 and 9.
   - **Systems:** only `properties` changes (the excluded systems' status and reasons, and M54's RV candidate coverage, σ and bin count), plus the new column `x_gc_baumgardt_ebv_mag`.
   - **Observables:** all 3 182 v1 rows are unchanged apart from the ID prefix and the new level columns. 71 V_t rows are appended from `o003183`, in systems-table order.
3. **Changed values: PASS.** The changed rows are exactly the frozen reading's: M54 only. See above.
4. **Arithmetic: PASS.** g_obs and g_bar, recomputed from the stored σ, r½, L_V and Υ_V with `astropy.constants.G`, agree on all 79 rows. The largest relative difference is 3 × 10⁻¹⁶.
5. **Error columns and confidence levels: PASS.** Levels come from `reading/err_levels.csv`, on all 79 rows and on every `sigma_los` observable of those codes, and match the test's expected table:

   | Code | Level |
   |---|---|
   | RV | 0.683, stated |
   | K18 | 0.68, stated |
   | D21 | 0.68, stated |
   | L13 | not given by the source |
   | F13 | not given by the source |
   | L15 | not given by the source |

   - The g_bar level is 0.683, stated (MvdM `e_(M/L)1`).
   - `g_bar_err_point_lo/hi` are present and empty. No g_obs point columns are added.
   - C22 and G22 have `sigma_los` observables but no measurement rows and no reading row, so their level columns are empty.
6. **Size columns: PASS.**
   - The R_h, W₀ and r₀ errors and `e_(M/L)1` are copied from v1's observables on all 79 rows. Every row's source prints them, so no row needed `no_uncertainty`.
   - `x_gc_baumgardt_vt_scatter_mag` is assigned from Harris V_t: 0.22 mag below 8, 0.45 mag from 8 to 11, 0.70 mag above 11.
   - Each size column's header names its term.
7. **Uncertainty terms and registry: PASS.**
   - **Terms:** the 27 terms are as frozen (term_id, scale, moves, status, size, kind, assumption), with `applies_to = *` and `covariance = not_published`.
   - **Registry:** every `gc_*` entry has an `aeg-d-gc-baumgardt/v2` entry, and v1's entries are unchanged. Six entries are new: `gc_distance_hb_slope`, `gc_reddening`, `gc_extinction_rv`, `gc_rh_measured`, `gc_luminosity_vt` and `gc_ml_scale`.
   - **Formulas:** every formula parses and names only `p`, `p0`, existing columns or `system.<column>`. At p = p0, all 3 634 evaluations leave the values unchanged to 10⁻¹².
   - **Sliders:** only `gc_stellar_ml` is adjustable, with v1's range and formulas.
8. **Plotting: PASS.**
   - **Plotting:** as v1, except that NGC 2298 (`m000009`) and Pal 5 (`m000078`) are recorded, not plotted. Each is `role = alternative`, with `not_plotted_reason = other` and BH18 l. 226–227 quoted in `notes`. M54 stays plotted, and MW-PAL1 stays recorded (D-046).
   - **Exclusion register:** `data/registry/excluded.csv` has exactly one row per excluded system.
   - **Site check:** both pages contain their quotation and citation, as an exact-text search after decoding HTML entities and collapsing whitespace.
9. **Named items: PASS.**
   - **Binary screening:** set per code from `reading/binary_screening.csv`: RV and K18 `multi_epoch_stated`; L13, F13 and L15 `integrated_light`; D21 `not_stated`.
   - **New V_t and E(B−V) data:** 71 V_t observables, and E(B−V) in `x_gc_baumgardt_ebv_mag`, whose header names Harris 2010 and both formulas.
   - **Corrections (F7):** KM09 `tab:pred`, in `gc_stellar_ml` v2; MvdM Table 10 for W₀ and r₀ and Table 11 for R_h, in `gc_light_model` v2.
   - **Sources:** `sources.json` lists v1's sources and BSH20, with its e-print hash `0e1a2b34…36b2`. Its licence is the arXiv non-exclusive distribution licence 1.0, as shown on the arXiv listing (read 2026-11-05), so `redistributable = false`.
   - **Known issues:** #159 (the M54 bins) and #160 (the Harris dynamical-parallax anchors).
10. **Descriptor: PASS.** `standard_version` is 2.5.1, `x_value_change_ruling` is D-096, and `x_second_reading` names `SECOND_READING.md` and the four frozen reading files.
11. **Package equals the frozen reading: PASS.** The D-096 change, the D-097 exclusions (no possibilities), the D-099 anchors, the levels and the screening values equal the reading, field by field. The reading files still have their frozen hashes.
12. **Standard and site: PASS, with one disclosure.**
    - `python -m aeg.validate data/packages/aeg-d-gc-baumgardt/v2` passes.
    - `aeg.formula_check` passes.
    - `aeg.site_check` reports 0 errors (188 541 values, 21 783 links).
    - The site builds, including the reproduction ledger's hash check (a ledger entry was added in `data/reproduction.json`).
    - **Disclosure:** the first build failed. `site/src/components/UncertaintyTerms.astro` rendered every term's note through the two-layer `L` component, which refuses empty text, and two frozen terms (`rotation`, `ellipticity`) have no note. The component now omits an empty note. This is a site change; the package was not changed.
13. **v1 untouched: PASS.** All 23 committed v1 files are identical to commit `5dc4091`.

## What was and wasn't verified

- **Verified mechanically:** every item above, by `reproduction/score.py`, which re-reads v1, the frozen reading and the v2 tables independently of `convert.py`; by the validator, the formula check, `aeg.check` (pass) and pytest (216 passed); and by the site build and site check.
- **Not re-verified here:** the term sizes and quotations, which step A's two readers read at source and two reviews checked; and v1's own values, whose second reading (3 535 of 3 535) carries over.
- **Not looked at:** no plot of the v2 values was made or inspected before scoring.

## Build fix after scoring (2026-11-05; disclosed, no value changed)

- **What failed:** CI's source fetch. The `sources.json` entry for Baumgardt, Sollima & Hilker 2020 had no `bytes` field and no fetchable file name.
- **The fix:** the entry now names the arXiv e-print as a fetched file (`bsh20/2009.09611v1.eprint`, 2 103 132 bytes, SHA-256 unchanged).
- **What changes:** only `sources.json` and `checksums.sha256`. Scoring is unchanged, as with the site-component fix JvH accepted for item 12 ("item 12 pass", 2026-11-05).
