# aeg-d-dwarfs/v2: reproduction test (draft; frozen on merge, before conversion)

**Status: draft, for JvH's approval.** Written 2026-11-04, before `convert.py` for v2 exists. No v2 value has been computed. On merge, this file's SHA-256 goes into `v2/sources.json`, and it is not edited after the first v2 conversion run. If the test fails, v2 does not ship and the failure is published; the test is not changed to pass (operating rule 5; D-005).

**Depends on** data standard 2.5.0 (D-095), D-096 (defer to the source's stated choices) and D-097 (when D-025 excludes a system).

## Purpose

v2 re-issues `aeg-d-dwarfs/v1` (standard 2.0.0) under standard 2.5.0 (D-083, D-084). It:
- adds the uncertainty terms read at source in step A (`docs/sources/readings/step-a-2026-11-04/dwarfs-adjudication.md`, "the adjudication");
- adds the half-light radius and ellipticity errors that v1 omitted;
- applies D-096 and D-097 to every system.

**Values change only where D-096 requires it,** and each change is listed with its source quotation. v2 therefore sets `x_value_change_ruling = D-096` if any value changes. v1 stays published and unchanged; the frozen audit samples v1's rows.

## Rules applied

1. **D-038's specific rules come first.** Second moment where given (2A), whole-sample value for multi-population fits (2B), binary-corrected re-analyses as alternatives (2C), originals before Geha et al. 2026 (3A). D-096 decides only where these do not. Where they conflict, the conflict is listed in the result and brought to JvH. It is not resolved by the converter.
2. **D-096 rule 1, preferred values.** Known case: Phoenix II. Fritz et al. 2019 (arXiv 1805.07350v4, Table 4) print 9.5 (+6.8/−4.4) km/s "from all possible members" and 11.0 (+9.4/−5.3) km/s "from the certain members", and mark the latter in bold as preferred (caption, l. 436; l. 393). In v2 the default is 11.0 (+9.4/−5.3), and 9.5 is an alternative row (`role = alternative`, `plotted = false`, `not_plotted_reason = alternative_value`).
3. **D-096 rule 2, excluded data.** Applied wherever a σ, structure, distance or photometry source excludes data from its own analysis of the quantity used.
4. **D-097, out of equilibrium.** Known cases: And XXVII, where Collins et al. 2013 says "unlikely to be in virial equilibrium, if it remains bound at all"; and Antlia 2, whose kinematics Ji et al. 2021 say "support a tidal disruption scenario". Both are `plotted = false`, `not_plotted_reason = other`, with the quotation in `notes`, and are listed in `data/registry/excluded.csv`. Their values are unchanged.

## The test

Applied to the v2 tables, with v1 at commit `5dc4091` as the reference.

### A. Values

1. **Rows.**
   - v2 has v1's 64 measurement rows, in v1's order, with the same `system_id` and `r_kpc`.
   - Alternative rows created by D-096 are appended after them.
2. **Unchanged values.** On every row not listed under item 3, `g_obs`, `g_bar`, `g_bar_stars`, `g_bar_gas_cold`, `g_obs_err_*` and `g_bar_err_*` are bit-for-bit equal to v1's.
3. **Changed values.** Every row whose values differ from v1 is listed in `REPRODUCTION_RESULT.md` with:
   - the rule of D-096 that changed it;
   - the source quotation and location;
   - the old and new inputs.
   - Phoenix II is one such row.
   - A change not traceable to D-096 is a fail.
4. **Arithmetic.** g_obs and g_bar recomputed from the stored inputs agree with the stored values to 10⁻⁹ (as v1 test 3).

### B. Uncertainties (standard 2.4.0 §2a, §3, §7a)

5. **Error columns.**
   - `g_obs_err_*` hold the σ error only, and `g_bar_err_*` the magnitude error only, as in v1.
   - For the five systems whose magnitude was rebuilt with a distance modulus (D-061; flag `mv_modulus_assumed`), v1 folded the modulus error into `g_bar_err_*`. Distance does not move the stellar g_bar under these formulas (finding F1 of the adjudication). So v2 keeps v1's totals and adds `g_bar_err_point_*` without the modulus term, and the column descriptions say so.
   - The σ upper-limit rows keep their limit levels in `err_level`.
   - Their g_bar errors are one-sigma, so `g_bar_err_level` = 0.683 and `g_bar_err_level_status = stated` on those rows.
6. **Half-light radius and ellipticity errors** are added to the observables (`half_light_radius` and `structural_param`, `err_lo`/`err_hi`) wherever the structural original prints them. The second reading records them. Where an original prints none, the observable says so in its `source_ref`.
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly these rows. Each cites its source at the location given in the adjudication, and `covariance` is `not_published`.

| term_id | scale | applies_to | moves | status | size | Note |
|---|---|---|---|---|---|---|
| `half_light_radius` | point | * | both | given | from the observables' R_h and ε errors (§2a rule 7) | registry formula: g_obs ∝ 1/R_h, stellar g_bar ∝ 1/R_h²; left out of the point columns |
| `distance` | system | * | g_obs | given | `size_column` `x_dwarfs_distance_err_hi_kpc` (a measurements extension column, with `x_dwarfs_distance_err_lo_kpc` beside it, both copied from the distance observables; empty where the original prints none) | g_bar is unchanged except for Boötes III (D-061 item 2), as the registry formula states (F1) |
| `distance_calibration_savino` | dataset | the 21 Savino et al. 2022 systems | g_obs | given | 0.035, `as_released` | "∼3.5%" systematic (Savino §6) |
| `estimator_normalisation` | dataset | * | g_obs | given | 0.10, `as_released` | Wolf et al. 2010 "±10%" (l. 927) |
| `anisotropy_profile` | dataset | * | g_obs | given | 0.05 dex, `as_released` | Wolf l. 974, on the mass |
| `deprojection_4_3` | dataset | * | both | given | 0.02, `upper_bound` | Wolf l. 152 "better than 2%" |
| `binaries` | system | * | g_obs | not_given_by_source | — | Wolf cites up to ∼20 % for the smallest systems; per-system screening is recorded (item 9) |
| `membership` | system | * | g_obs | not_given_by_source | — | Tollerud "few-percent level" |
| `light_weighting` | dataset | * | g_obs | not_given_by_source | — | member-sample σ taken as the light-weighted σ (D-038 1A) |
| `rotation` | system | * | g_obs | not_given_by_source | — | Pace 2025 §5 |
| `rh_convention_profile` | system | * | both | not_given_by_source | — | profile family and semi-major or circularised convention (flag `rh_semimajor_assumed`) |
| `luminosity_function_martin` | dataset | the Martin et al. 2016 photometry systems | g_bar | given | 0.2 mag, `as_released` | assumed population age (Martin l. 385) |
| `extinction` | system | * | g_bar | not_given_by_source | — | |
| `solar_magnitude` | dataset | * | g_bar | not_given_by_source | — | 4.85 (McLaughlin & van der Marel 2005); others use 4.83 |
| `stellar_ml` | dataset | * | g_bar | given | `size_column` `x_dwarfs_upsilon_v_low/high` (measurements), `range` | the D-060 envelope; `assumption_id` `dw_stellar_ml` |
| `helium_factor` | dataset | * | g_bar | not_given_by_source | — | 1.33 (Lelli et al. 2016) |
| `gas_inside_rhalf` | system | Leo T; Phoenix | g_bar | not_given_by_source | — | half the total (flag `gas_half_total`) |
| `heterogeneity` | dataset | * | both | not_given_by_source | — | "there will be systematics in the LVDB" (Pace §5) |

   - "the 21 Savino et al. 2022 systems" and "the Martin et al. 2016 photometry systems" are written as semicolon lists of `system_id`s (standard 2.4.0 §7a).
   - **The registry entry `dw_distance`** gets the net effect: g_obs ∝ 1/D, g_bar unchanged, except Boötes III, g_bar ∝ 1/D².

### C. Structure and flags

8. **Plotting.**
   - D-097's excluded systems are `plotted = false`, `not_plotted_reason = other`, with the quotation, and are in `excluded.csv`.
   - D-096's alternatives are `plotted = false`, `not_plotted_reason = alternative_value`.
   - Every other row is plotted, as in v1.
9. **Named items v1 omitted.**
   - The D-038 1A assumption is added to each row's `assumptions` and to the registry.
   - A per-row extension column `x_dwarfs_binary_screening` records the source's stated binary treatment, from `reading/sigma_values.csv`, as D-025 asks.
   - The `distance_inherited` flag is set on every system whose distance original is its host's, as REPRODUCTION v1 required. The count is reported, possibly zero.
10. **Descriptor.** `standard_version` `2.5.0`; `x_value_change_ruling` `D-096` if item 3 lists any row; the other 2.0 descriptor fields as v1, updated.
11. **Second reading (D-031 item 3).** An independent reader, with no access to the conversion code or the v2 tables, records, for every system:
    - R_h and ε errors as printed, with quote and location;
    - **D-096 fields:** whether each σ, structure, distance or photometry source marks a preferred value or excludes data, with quote and location;
    - **D-097 field:** every statement in the system's own sources about equilibrium, binding or tides, classified as a "finding" (excludes) or a "possibility" (plotted, quoted), with the quote.
    - **Pass:** the package matches the reading on every field. Disagreements are resolved at source; one resolved against the package is a fail.
    - The counts of D-096 changes and D-097 exclusions are published with the result.
12. **Standard and site.**
    - `python -m aeg.validate` passes under 2.5.0;
    - the site builds;
    - `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes.
13. **v1 untouched.** Every file in `aeg-d-dwarfs/v1/` has the checksum it had at commit `5dc4091`.

**Pass** = all thirteen hold. Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right.
- The v1 tests, which stand for v1. For unchanged rows they carry over, because item 2 makes those rows identical.
- The `beyond_source_range` count (39 against D-060's 26 below the metallicity floor). It is reported with the result and explained; the flag itself is unchanged.
