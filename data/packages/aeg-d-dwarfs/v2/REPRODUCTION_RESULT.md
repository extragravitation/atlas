# aeg-d-dwarfs/v2: reproduction result

**Result: PASS.** All thirteen items of the frozen test hold.
- **Test:** `REPRODUCTION.md`, SHA-256 `395460b84359dc10de812fd3c86791832f17575c531272b0b457a7c4c75c020e` (freeze record `data/frozen/dwarfs-v2-test.json`, merged in #149).
- **Reading:** `reading/resolved.csv`, frozen in `data/frozen/dwarfs-v2-reading.json` (merged in #157).
- **Run:** 2026-11-05, one scored conversion run by `convert.py`, scored by `reproduction/score.py` (output `reproduction/score.json`) and, for item 12's page check, `reproduction/page_check.py` (`reproduction/page_check.json`).
- **Reference:** v1 at commit `5dc4091`.

## Counts the test asks for

- **D-096 changes:** 2 rows, Phoenix II and Fornax. Both were ruled before conversion (D-098 rule 5; D-101).
- **D-097 classes, the 64 systems with rows:** 8 findings (recorded, not plotted), 14 possibilities (plotted, with the quotation), 42 with no relevant statement. Andromeda XIII, which has no row, is "none" in the reading too.
- **D-097 statements in the reading:** 29 classed finding, 49 possibility and 126 neither (counted over all statements, including those in sources that do not decide a class).
- **Plotted defaults:** 56 of 64. The 8 not plotted are the D-097 findings.

## Item by item

1. **Rows: pass.** 64 rows in v1's order, with v1's `measurement_id` stems and `system_id`s. Two alternative rows are appended: `m000065` (Fornax, exponential radius) and `m000066` (Phoenix II, all-members σ). `r_kpc` differs from v1 only on Fornax.
2. **Measurements, observables, systems: pass.**
   - On the 62 unchanged rows, `g_obs`, `g_bar`, `g_bar_stars`, `g_bar_gas_cold` and all four error columns are bit-for-bit equal to v1. Every other v1 column is unchanged except the allowed ones.
   - The alternative rows' g columns, `r_kpc`, σ and R_h are bit-for-bit equal to v1's defaults for those systems (`m000038`, `m000051`).
   - The new measurement columns are exactly those item 2 lists.
   - **2a.** v1's 586 observables are kept in order with v1's values; only `err_lo`, `err_hi` and `source_ref` on half-light-radius, ellipticity and distance rows change, plus the two level columns. Two observables are appended, both for item 3 values: Phoenix II's σ = 11.0 km/s (`o000587`) and Fornax's Sérsic r_h = 20.1′ (`o000588`).
   - **2b.** Systems are unchanged apart from `properties` (status) on the eight excluded systems. No new columns.
3. **Changed values: pass.** The rows whose values differ from v1 are exactly the two listed, and both are recorded as ruled changes in the reading.

   | | Phoenix II (`aeg-s-000394`) | Fornax (`aeg-s-000381`) |
   |---|---|---|
   | Rule | D-096 rule 1 (D-098 rule 5) | D-096 rule 1 (D-101) |
   | Reading line | `d096_preferred`, role sigma, resolution `ruled` | `d096_preferred` and `d096_conflict`, role structure, `ruled` |
   | Source | Fritz et al. 2019, Table 4 caption l. 436: "We indicate in bold which determination we prefer"; bold row l. 452. l. 415: σ "does not depend significantly on which set of members is considered" | Wang et al. 2019, `Fornax_main.tex` l. 333: "found that Sersic model gives the best fit to the data while other models seem to fail to capture the complex light profile shape of Fornax" |
   | Old input | σ = 9.5 (+6.8/−4.4) km/s | r_h = 19.8′ (exponential); R_h = 16.4471′ |
   | New input | σ = 11.0 (+9.4/−5.3) km/s | r_h = 20.1′ (Sérsic); R_h = 16.6963′ (ε = 0.31 fixed) |
   | `r_kpc` | 0.0380669, unchanged | 0.9093999 → 0.9231788 |
   | g_obs (m s⁻²) | 2.305 × 10⁻¹⁰ → 3.090 × 10⁻¹⁰ | 1.499 × 10⁻¹¹ → 1.476 × 10⁻¹¹ |
   | g_bar (m s⁻²) | 8.869 × 10⁻¹⁴, unchanged | 3.491 × 10⁻¹² → 3.388 × 10⁻¹² |
   | Data points dropped | none (rule 1, not rule 2) | none |
   | Plotting rules on the new value | D-038 1A by v1's coding (`coverage = beyond_rh`, Fritz Table 2): passes; plotted | D-038 1A with D-051, recomputed by v1's frozen member rule (Hendricks 2014) and `aeg.coverage` with a_h = 20.1′: 327 of 340 members beyond r_h (96.2 %), max r/r_h 2.36; passes; plotted |

   The source centre, position angle and ellipticity for the Fornax coverage are v1's (`reading/structure_values.csv`); only a_h changed.
4. **Arithmetic: pass.** g_obs and g_bar recomputed from the stored inputs agree to 2.2 × 10⁻¹⁶ (limit 10⁻⁹).
5. **Error columns and levels: pass.**
   - `g_bar_err_point_lo/hi`: on And VI, And VII, Phoenix and Tucana the M_V error alone; on Leo T empty; on every other row equal to the total.
   - Levels from the reading: σ level stated on 33 of 64 rows, magnitude level on 47. And XII has `err_level` empty and `not_given_by_source`, with the flag `limit_from_1sigma_upper_error` kept.
   - The reading confirms for all five modulus systems that the M_V used was derived with the modulus used (Leo T numerically; Tucana by V_T − M_V).
6. **R_h, ellipticity and distance errors: pass.** Every row matches the reading; two-sided columns are filled together. 60 R_h errors agree exactly with v1's own structure reading (`structure_values_all.csv`), and none differs. The other four are And VI, And VII and Fornax (no error printed) and Tucana (printed in pc, 32 pc, converted as the value).
7. **Uncertainty terms and registry: pass.** 34 terms, exactly the frozen table plus its per-system rows: `half_light_radius_` for And VI, And VII and Fornax; `distance_` for Antlia II and Sextans. No `ellipticity_<system>` row is needed (every system using ε prints its error). Six terms are `given`. Every `dw_*` entry gains an `aeg-d-dwarfs/v2` entry, plus `dw_member_sample_sigma` and `dw_ellipticity`. All four effects formulas return the stored values at the default, to 0 relative difference.
8. **Plotting: pass.** The 8 findings are `plotted = false`, `not_plotted_reason = other`, with every finding quotation in `notes`, and one row each in `data/registry/excluded.csv`. The 14 possibilities are plotted as in v1 with their quotations in `notes`. The two alternatives are `alternative_value`. Every other row is plotted as in v1.

   | System | Deciding quotation (first in the reading) |
   |---|---|
   | And XXI | "From the velocity profile, it appears that this system is not in equilibrium…" (Collins 2021) |
   | And XXVII | "…currently undergoing tidal disruption…" (Collins 2013, l. 1423–1427) |
   | Antlia II | "…support a tidal disruption scenario…" (Ji 2021, l. 104) |
   | Boötes I | "…suggest that \BooI\ is experiencing tidal disruption…" (Sandford 2026) |
   | Boötes III | "Bo\"otes III is a Tidally Disrupting Ultra-Faint Dwarf Galaxy…" (Li 2026, title) |
   | Hercules | "…it is likely that Hercules is indeed currently undergoing tidal disruption…" (Ou 2024) |
   | Ursa Major II | "…UMa~II is probably a system that is undergoing severe tidal disruption…" (Muñoz 2018, citing Muñoz 2010) |
   | Willman 1 | "previous studies of W1 found evidence for dynamical disequilibrium…" (Chiu 2026) |
9. **Named items: pass.** `dw_member_sample_sigma` and `star_count_weighting` on all 66 rows: every v1 row's selected σ passed D-038 1A in v1's coding (18 by `coverage = beyond_rh`, 46 by a passing D-051 member table), and Phoenix II's new default passes. Binary screening from the reading: 31 `multi_epoch_stated`, 2 `no_multi_epoch_stated`, 31 `not_stated`. `distance_inherited`: 0 systems.
10. **Descriptor: pass.** `standard_version` 2.5.1; `x_value_change_ruling` D-096.
11. **Second reading: pass.** The package equals `reading/resolved.csv` on every field it holds: D-096 changes, D-097 classes and quotations, σ and magnitude levels, binary screening. The file's SHA-256 equals its freeze record and `sources.json`.
12. **Standard and site: pass.**
    - `python -m aeg.validate data/packages/aeg-d-dwarfs/v2`: passed.
    - `python -m aeg.formula_check`: passed (73 833 evaluations).
    - The site builds (640 pages); `python -m aeg.site_check`: 0 errors.
    - The reproduction ledger's hash check (run in the site build): passed, with this package's entry in `data/reproduction.json`.
    - Each of the 8 excluded systems' built pages contains its `excluded.csv` quotation exactly (HTML unescaped, whitespace collapsed): 8 of 8.
13. **v1 untouched: pass.** All 129 tracked files in `aeg-d-dwarfs/v1/` are byte-identical to commit `5dc4091`, and none was added or removed.

## The `beyond_source_range` count (not tested; explained)

39 rows carry the flag, against the 26 D-060 describes as below the metallicity floor. 26 rows have [Fe/H] below −2.29, the lowest tabulated value. The other 13 have [Fe/H] between −2.29 and −1.80, but `v1/reproduction/upsilon.py` evaluates the range at [Fe/H] ± s (its docstring, l. 13 and 21–23), and for each of them [Fe/H] − s lies below the floor (for example Antlia II, −1.90 − 0.66). The flag marks that the envelope reached the table's end. Both counts are right; they count different things. The flag itself is unchanged.

## What was and was not verified

- **Verified:** every item above, mechanically, against v1's tables, the frozen reading and the freeze records.
- **Not verified here:** whether the sources' own error sizes are right (not tested, as the test says), and the line numbers the readers recorded beyond what the reading's resolution checked.
- **Noted, not a test item.** The site's dwarf page for an excluded system says no acceleration was computed. For a D-097 finding that is not so: the values are kept in the tables and downloads. The page shows the quotation and reason, as item 12 requires; the wording of the page is a site matter for a later pull request.
- **Columba I.** As the test notes, v1 uses Geha 2026 because no original passes the plotting rules. Fritz 2019's preferred limit (< 16.1 km/s) is not a passing value, so D-096 does not change it.
