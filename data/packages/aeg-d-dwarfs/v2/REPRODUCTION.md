# aeg-d-dwarfs/v2: reproduction test (draft; frozen on merge, before conversion)

**Status: draft, revision 2, for JvH's approval.** Written 2026-11-04, before `convert.py` for v2 exists. No v2 value has been computed. Revision 2 answers the independent review (`docs/sources/readings/step-d-2026-11-04/dwarfs-review-1.md`, "the review") and applies D-098.

On merge, this file's SHA-256 goes into `v2/sources.json`. It is not edited after the first v2 conversion run. If the test fails, v2 does not ship and the failure is published; the test is not changed to pass (operating rule 5; D-005).

**Depends on:**
- data standard 2.5.0 (D-093, D-095);
- D-096 (defer to the source's stated choices);
- D-097 (when D-025 excludes a system);
- D-098 (D-096 rule 2 applies to the same data points only; three classes for D-097). D-098 is merged before this test is frozen.

## Purpose

v2 re-issues `aeg-d-dwarfs/v1` (standard 2.0.0) under standard 2.5.0 (D-083, D-084). It:
- adds the uncertainty terms read at source in step A (`docs/sources/readings/step-a-2026-11-04/dwarfs-adjudication.md`, "the adjudication");
- adds the half-light radius, ellipticity and distance errors that v1 did not carry;
- applies D-096, D-097 and D-098 to every system.

**Values change only where D-096 requires it,** and each change is listed with its source quotation. v2 sets `x_value_change_ruling = D-096` if any value changes. v1 stays published and unchanged; the frozen audit samples v1's rows.

## Rules applied

1. **Which rule chooses what (D-098).** D-038 and the other value rulings choose the source and the kind of value. D-096 rule 1 then chooses among the values that one source offers. No precedence rule is added (D-098 rule 5).
   - Where the second reading (item 11) finds a source's stated preference that conflicts with an earlier value ruling (for example D-052, D-055, D-061 item 4 or D-062), the conflict is listed and brought to JvH **before the first conversion run**. The converter is not run until it is ruled. No conflict is resolved after v2 values exist.
2. **D-096 rule 1, preferred values.** Known case: Phoenix II (`aeg-s-000394`).
   - Fritz et al. 2019 (arXiv 1805.07350v4, `spec_v1_ref1_arx.tex`) print 9.5 (+6.8/−4.4) km/s "calculated from all possible members" (l. 446) and 11.0 (+9.4/−5.3) km/s from "the certain members" (l. 452). The caption says "We indicate in bold which determination we prefer" (l. 436), and the bold row is the certain-members one. l. 393: "our preferred set of values are those derived when excluding this star".
   - In v2 the default is 11.0 (+9.4/−5.3). The 9.5 value is an alternative row: `role = alternative`, `alternative_of` = the Phoenix II default, `plotted = false`, `not_plotted_reason = alternative_value`.
   - v1's σ coding filed the certain-members value as "subset (D-038 2B)". D-098 reads 2B as covering multi-population fits only.
   - The changed default still passes through the existing rules. D-038 1A is re-run under D-051 with the five certain members the source used (Fritz Table 2, R/R_half 0.57, 1.78, 1.71, 1.82 and 1.54), against the R_h of the plotted point (Richstein et al. 2024). Under D-055 item 9 it is run with each fit's centre, and passes only if both pass. The result is published with the members beyond R_h, the fraction and the largest r/R_h (D-051 item 3).
   - Fritz l. 415 ("does not depend significantly on which set of members is considered") is quoted in the result.
3. **D-096 rule 2, excluded data (scope by D-098 rule 1).** It changes an input only where the Atlas itself computes from data points the source excluded.
   - For this dataset that is the D-051 coverage computation from a source's per-star member table. It uses only the stars the source states it used for the chosen value.
   - A printed σ, radius, distance or magnitude already reflects the source's exclusions and is not changed by rule 2.
4. **D-097, out of equilibrium, with D-098's three classes.** The second reading (item 11) classes every statement about equilibrium, binding or tides in the sources that count:
   - **Sources that count** (D-098 rule 3): the paper whose σ is used, the structure original and the distance original. Gas, metallicity and compilation papers do not count.
   - **Finding:** the source presents the state as its conclusion or as established fact: out of equilibrium, unbound, or being tidally disrupted. Graded conclusions count ("likely", "unlikely to be in virial equilibrium", "our data support"). A statement that a system is tidally disturbed counts when it says the system is out of equilibrium or being disrupted. **Excluded:** `plotted = false`, `not_plotted_reason = other`, the quotation in `notes`, and a row in `data/registry/excluded.csv`.
   - **Possibility:** the state itself is hedged, or offered as one option the source does not adopt ("could", "may", "might", "cannot be ruled out"). **Plotted,** with the quotation in `notes`.
   - **Neither:** tidal tails, tidal extension, tidal features or mass loss mentioned on their own, or orbital remarks. Recorded in the reading only.
   - **Known findings:** Andromeda XXVII (`aeg-s-000365`), Collins et al. 2013: "unlikely to be in virial equilibrium, if it remains bound at all". Antlia II (`aeg-s-000367`), Ji et al. 2021: kinematics that "support a tidal disruption scenario" (abstract). Both are examples ruled in D-097.
   - Excluded systems' values are unchanged. They stay visible on their own pages (D-097 rule 5).
5. **Sizes of uncertainty terms: one rule for every row.**
   - A size the source states is used (`given`, with the `size_kind` the wording implies) when the source states it for the method or quantity as the package uses it, without restricting it to systems the row does not cover.
   - If the source restricts it (for example "in the smallest dSphs", or a band drawn for the classical dSphs), the row is `not_given_by_source`, and its note quotes the restricted statement.
   - Wording gives the kind: "up to", "at most", "better than" → `upper_bound`; a published lower and upper value of a parameter → `range`; a "typical" or plain value → `as_released`.
6. **Two-sided sizes.** Where a size varies by row and has two sides, `size_column` names the `_hi` (or `_high`) column. The column of the same stem ending `_lo` (or `_low`) holds the other side. Both sides are used by the registry formula and the views. Item 7 checks that every row filled in one is filled in the other.

## The test

Applied to the v2 tables, with v1 at commit `5dc4091` as the reference.

### A. Values

1. **Rows.**
   - v2 has v1's 64 measurement rows, in v1's order, with the same `measurement_id` stem and `system_id`.
   - Alternative rows created by D-096 are appended after them, with new sequential `measurement_id`s.
   - `r_kpc` equals v1's on every row not listed under item 3.
2. **Unchanged values.** On every row not listed under item 3, `g_obs`, `g_bar`, `g_bar_stars`, `g_bar_gas_cold`, `g_obs_err_*` and `g_bar_err_*` are bit-for-bit equal to v1's.
   - **Every other v1 column is unchanged,** except:
     - `plotted`, `not_plotted_reason` and `notes`, as rule 4 and item 8 require;
     - `role` and `alternative_of`, for D-096 rows;
     - `assumptions` and `flags`, which gain the D-038 1A assumption and the `star_count_weighting` flag (item 9);
     - `x_dwarfs_flags`, which may gain `distance_inherited` (item 9);
     - the columns of the rows listed under item 3.
   - New columns are only those this test names.
3. **Changed values.** Every row whose values differ from v1 is listed in `REPRODUCTION_RESULT.md` with:
   - the rule of D-096 that changed it, and the line of the second reading that records it;
   - the source quotation and location;
   - the old and new inputs, and the old and new `r_kpc`;
   - for D-096 rule 2 changes, the data points dropped;
   - the result of the existing plotting rules on the new value (rule 2).
   - Phoenix II is one such row.
   - A change not in the second reading, or not traceable to D-096, is a fail.
4. **Arithmetic.** g_obs and g_bar recomputed from the stored inputs agree with the stored values to 10⁻⁹ (as v1 test 3).

### B. Uncertainties (standard 2.5.0; §2a, §3 and §7a as in 2.4.0)

5. **Error columns.**
   - **`g_obs_err_*`** hold the σ error only, as in v1. The column description says that the per-star velocity floors of each pipeline are inside it, because the source folds them into its σ error and they cannot be separated (term `velocity_error_model`).
   - **`g_bar_err_*`** keep v1's values. For five systems, v1 folded the modulus of the paper into the magnitude error in quadrature (`reproduction/inputs_v2.py` `MAG_OVERRIDE`): Andromeda VI (`aeg-s-000347`, 0.07 mag), Andromeda VII (`aeg-s-000348`, 0.10), Phoenix (`aeg-s-000393`, 0.1), Leo T (`aeg-s-000390`, 0.2) and Tucana (`aeg-s-000402`, 0.16).
     - That modulus does not belong in the error. The magnitude is rebuilt as m = M_V + μ_paper from an M_V the paper derived with the same μ_paper, so μ_paper cancels.
     - So v2 adds `g_bar_err_point_lo/hi` on every row.
     - On these five rows, the point columns hold the M_V error alone, propagated as v1 propagates the total.
     - On Leo T, de Jong et al. 2008 print M_V without an error. Its point columns are empty, with the term `g_bar_point_leo_t` (`not_given_by_source`).
     - On the other 59 rows, the point columns equal `g_bar_err_*`.
     - The column descriptions say all of this. No §7a row is added for the modulus, because it moves neither axis.
   - **Confidence levels** are set from the second reading (item 11), never assumed:
     - `err_level` and `err_level_status` per row, from the level each σ source states. Examples: "If resolved, we quote the 1-sigma errors" (Geha et al. 2026 l. 741) → 0.683, `stated`; "the 95th percentile of the posterior" → 0.95, `stated`; "the values at the 90-th percentile" (Fritz l. 388) → 0.90, `stated`. Where the σ source states no level, `err_level` is empty and the status is `not_given_by_source`.
     - **Andromeda XII** (`aeg-s-000352`; D-062): the limit is the upper end of Collins et al. 2013's interval, 0.0 (+4.0) km/s, and no limit level is stated. `err_level` = 0.683 with `err_level_status = stated` only if the second reading finds Collins stating that its intervals are 1σ. Otherwise `err_level` is empty and the status is `not_given_by_source`. Either way, the note says that this is the upper end of a two-sided interval, not a one-sided limit at a stated level, and the flag `limit_from_1sigma_upper_error` stays in `x_dwarfs_flags`.
     - `g_bar_err_level` and `g_bar_err_level_status` per row, the same way, from the level each magnitude source states for its magnitude error.
6. **Half-light radius, ellipticity and distance errors** are added wherever the original prints them:
   - in the observables (`half_light_radius`, `structural_param` and `distance`, `err_lo`/`err_hi`), with `no_uncertainty` noted in `source_ref` where the original prints none;
   - in new measurements extension columns: `x_dwarfs_rh_err_lo_arcmin` and `x_dwarfs_rh_err_hi_arcmin` (the printed r_h error carried to the circularised R_h with ε fixed), `x_dwarfs_ellipticity`, `x_dwarfs_ellipticity_err_lo` and `x_dwarfs_ellipticity_err_hi`, and `x_dwarfs_distance_err_lo_kpc` and `x_dwarfs_distance_err_hi_kpc`;
   - empty where the original prints none.
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly the rows below. Each cites its source at the location given in the adjudication or this test, and `covariance` is `not_published`. Rows marked "per system" are one row for each system named, with `term_id` `<stem>_<system_id>`. Their scale is `point` or `system` as shown, and they carry a single `system_id` in `applies_to`.

**Shape and direction**

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `half_light_radius` | point | * | both | given | `size_column` `x_dwarfs_rh_err_hi_arcmin` (rule 6), `one_sigma` or as the second reading records | `dw_rhalf_wolf` | §2a rule 7: g_obs ∝ 1/R_h and g_bar ∝ 1/R_h² (stars and gas); left out of both point columns |
| `half_light_radius_<system_id>` | point | each system whose structural original prints no R_h error | both | not_given_by_source | — | `dw_rhalf_wolf` | from the second reading; for example Andromeda VI, Antlia II and Tucana V in v1's observables |
| `ellipticity` | point | * | both | given | `size_column` `x_dwarfs_ellipticity_err_hi` (rule 6) | `dw_rh_circularised` | enters only where R_h = a√(1 − ε) is used; empty where the radius is printed circularised |
| `ellipticity_<system_id>` | point | each system using a√(1 − ε) whose original prints no ε error | both | not_given_by_source | — | `dw_rh_circularised` | from the second reading |
| `ellipticity_radial_variation` | system | * | both | not_given_by_source | — | `dw_rh_circularised` | ε and position angle "vary with radius" (Pace 2025 §5, l. 699); Sculptor 0.23–0.49 by subsample (Muñoz 2018) |
| `rh_convention_profile` | system | * | both | not_given_by_source | — | `dw_rh_circularised` | profile family, and semi-major or circularised convention (flag `rh_semimajor_assumed`); effect computed by the formula (D-052 item 2) |
| `deprojection_4_3` | dataset | * | both | given | `size_lo` 1.305, `size_hi` 1.352, unit r½/R_h, `range` | `dw_rhalf_wolf` | a parameter term (§2a rule 4): Wolf et al. 2010 Appendix table (l. 1793–1800), Plummer to Sérsic n = 8; "accurate to better than 2%" (l. 150–152); 4/3 is the default |
| `distance` | system | * | both | given | `size_column` `x_dwarfs_distance_err_hi_kpc` (rule 6) | `dw_distance` | g_obs ∝ 1/D. g_bar ∝ D⁰, except on rows flagged `mv_distance_independent` in `x_dwarfs_flags`, where g_bar_stars ∝ D⁻² (Boötes III; D-061 item 2). From the flags, not by name (adjudication F1) |
| `distance_<system_id>` | system | each system whose distance original prints no error | both | not_given_by_source | — | `dw_distance` | for example Antlia II; Vivas et al. 2022 give a 5.4 kpc dispersion and a ~13 kpc gradient (l. 264–266), quoted in the note |
| `distance_calibration_savino` | dataset | the systems whose distance original is Savino et al. 2022 | both | given | 0.035, `as_released` | `dw_distance` | "we quantified our typical systematic uncertainties to be ∼3.5%" (Savino §6, l. 1244). Possible overlap: Savino says the quoted intervals already "account for … the adopted PWZ calibration" (§4, l. 952), and does not say whether the 3.5% overlaps them. The note says so; views show the term beside the error bars, never added in |
| `distance_calibration_other` | dataset | * | both | not_given_by_source | — | `dw_distance` | Carlin et al. 2017's anchor modulus has no error (l. 114); Higgs et al. 2021's TRGB calibration states none (l. 361); Medina et al. 2018 gives a conditional 1.8–3.6 % for metallicity offsets (l. 264), not an error |

**Velocities and the estimator**

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `velocity_error_model` | dataset | * | g_obs | not_given_by_source | — | — | per-star floors inside each source's σ error, effect on σ not stated: Geha 2026 k_v 1.4, floor 1.1 km/s (l. 420); Tollerud 2012 2.2 km/s (l. 268); Heiger 2024 1 km/s (l. 109); Kvasova 2024 1.49 km/s (l. 260); Collins 2013 mask offsets (l. 571–573) |
| `binaries` | system | * | g_obs | not_given_by_source | — | — | Wolf l. 1212–1214: "up to ∼20%" in σ, but only "in the smallest dSphs" (citing Minor 2010), so rule 5 gives no size; screening per system in `x_dwarfs_binary_screening` (item 9) |
| `membership` | system | * | g_obs | not_given_by_source | — | — | Tollerud's "few-percent level" applies to its own systems only (rule 5) |
| `rotation` | system | * | g_obs | not_given_by_source | — | — | Pace 2025 §5 |
| `light_weighting` | dataset | * | g_obs | not_given_by_source | — | the D-038 1A registry entry (item 9) | member-sample σ taken as the light-weighted σ (D-038 1A) |
| `estimator_normalisation` | dataset | * | g_obs | not_given_by_source | — | `dw_equilibrium` | Wolf's "±10%" is a band drawn for the classical dSphs (l. 922–927), not a stated error for all systems (rule 5) |
| `anisotropy_profile` | dataset | * | g_obs | given | 0.05 dex on M_half, `as_released` | `dw_equilibrium` | "the errors on M_half increased by roughly 0.05 dex when the (rather extreme) second β(r) form was used" (Wolf l. 990–992). Assigned to every row by the Atlas: Wolf states it for its own analysis. `correlated_with` `estimator_normalisation` (both describe the estimator; the correlation is not stated by the source) |

**Light and gas**

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `g_bar_point_leo_t` | point | `aeg-s-000390` | g_bar | not_given_by_source | — | — | de Jong 2008 M_V printed without an error (item 5) |
| `luminosity_function_martin` | dataset | the systems whose photometry original is Martin et al. 2016 | g_bar | given | 0.2 mag, `as_released` | — | "an 8-Gyr stellar population does lead to magnitudes that are systematically brighter by ∼0.2 magnitudes" (Martin l. 385); also "0.29 ± 0.11 magnitudes fainter" than the literature, in the note |
| `luminosity_function_other` | dataset | * | g_bar | not_given_by_source | — | — | IMF and population assumed in other sources' luminosity functions: Muñoz 2018 "assuming a Salpeter initial mass function" (l. 416) |
| `band_transformation` | dataset | * | g_bar | not_given_by_source | — | — | Muñoz l. 468 (Jordi 2006); Martin l. 379 (Ibata 2007); Richstein; Leo T (D-055 item 7) |
| `extinction` | system | * | g_bar | not_given_by_source | — | — | Martin l. 377; Higgs l. 221–222; Pace App. A l. 800 |
| `solar_magnitude` | dataset | * | g_bar | not_given_by_source | — | — | 4.85 (McLaughlin & van der Marel 2005); Carlin and Richstein use 4.83 |
| `stellar_ml` | dataset | * | g_bar | given | `size_column` `x_dwarfs_upsilon_v_high` (rule 6), `range` | `dw_stellar_ml` | the D-060 envelope |
| `helium_factor` | dataset | * | g_bar | not_given_by_source | — | — | 1.33 (Lelli et al. 2016) |
| `gas_inside_rhalf_aeg-s-000390` | system | `aeg-s-000390` | g_bar | not_given_by_source | — | `dw_gas_half_total` | Leo T: half the total HI mass (flag `gas_half_total`) |
| `gas_inside_rhalf_aeg-s-000393` | system | `aeg-s-000393` | g_bar | not_given_by_source | — | `dw_gas_half_total` | Phoenix: as above |
| `hi_flux` | system | * | g_bar | not_given_by_source | — | — | Putman 2021's HI mass errors "are from the distance errors shown" (MRT Note 4), so they are part of `distance` and cancel in g_bar; no flux error is stated; Phoenix's "confusion with Galactic emission" (Note 22) quoted |
| `hi_limit_assumptions` | dataset | * | g_bar | not_given_by_source | — | — | 5σ limits with a fixed 10 km/s width (Putman l. 176) and an assumed central concentration (l. 166); limits enter g_bar as zero |
| `molecular_ionised_gas` | dataset | * | g_bar | not_given_by_source | — | — | `not_addressed` in v1's `x_baryon_inventory` |
| `heterogeneity` | dataset | * | both | not_given_by_source | — | — | "there will be systematics in the LVDB" (Pace §5) |

   - "The systems whose …" are written as semicolon lists of `system_id`s (standard §7a), taken from the distance and magnitude observables' `source_ref`.
   - **Not rows, with reasons:**
     - **Equilibrium and sphericity** are assumptions (§2a rule 4; registry `dw_equilibrium`), not uncertainty terms.
     - **The modulus folded in by v1** moves neither axis (item 5).
     - **Savino's RR Lyrae metallicity prior** (0.06 mag) is inside the printed intervals, which "account for our uncertain knowledge of the RR Lyrae metallicity" (l. 952).
     - **Inherited host distances** are a flag, not a term (item 9).
   - **Registry.** The v2 entries of `dw_distance`, `dw_rhalf_wolf` and `dw_rh_circularised` carry the `effects` formulas above. A new entry registers the D-038 1A assumption ("member-sample σ taken as representative of the light-weighted σ").
   - **Checked:** a dummy terms table with these rows passes `validate_v22` and `validate_v24` before conversion (the result reports this). Every two-sided `size_column` has its companion filled on the same rows (rule 6).

### C. Structure and flags

8. **Plotting.**
   - D-097 findings are `plotted = false`, `not_plotted_reason = other`, with the quotation in `notes`. Each has a row in `data/registry/excluded.csv`, with the columns of standard §5: `system` (system_id), `dataset` (`aeg-d-dwarfs/v2`), `reason` ("D-097 finding: " and the quotation) and `citation` (bibcode and location). The file is created if it does not exist.
   - D-097 possibilities are plotted, and their quotation is in `notes`. Each one is checked.
   - D-096 alternatives are `plotted = false`, `not_plotted_reason = alternative_value`.
   - Rows listed under item 3 are plotted as the existing rules decide for the new value (rule 2).
   - Every other row is plotted as in v1.
9. **Named items v1 omitted.**
   - The D-038 1A assumption is added to each row's `assumptions`, and the row gets the §11 flag `star_count_weighting`, where the σ is a member-sample σ.
   - A per-row extension column `x_dwarfs_binary_screening` records, as D-025 asks, whether the σ source states multi-epoch screening for binaries. It is a closed list: `multi_epoch_stated`, `no_multi_epoch_stated` (the source says it has no multi-epoch data) or `not_stated`. The values come from the second reading, which starts from `reading/sigma_values.csv` `binaries`.
   - The flag `distance_inherited` goes in `x_dwarfs_flags` (it is not in the §11 list) on every system whose distance original gives its host's distance. The count is reported, possibly zero.
10. **Descriptor.** `standard_version` `2.5.0`; `x_value_change_ruling` `D-096` if item 3 lists any row; the other 2.0 descriptor fields as v1, updated. The column descriptions state what items 5 and 6 say.
11. **Second reading (D-031 item 3), done before conversion.** An independent reader, with no access to the conversion code or any v2 table, records for every system:
    - the R_h and ε errors as printed, with quote and location;
    - the confidence level each σ and magnitude source states for its errors or limits;
    - **D-096 fields:** whether each σ, structure, distance or photometry source marks a preferred value or excludes data points the Atlas computes from (rule 3), with quote and location;
    - any conflict between a stated preference and an earlier value ruling (rule 1);
    - **D-097 field:** every statement about equilibrium, binding or tides in the sources that count, classed as finding, possibility or neither (rule 4), with the quote;
    - the binary-screening class (item 9) and whether the distance is inherited from the host;
    - the scope of each stated size in item 7 (rule 5).

    **Before the first conversion run:**
    - the reading is complete and committed;
    - disagreements with the step A readings are resolved at source by someone who has seen no v2 value (none exists yet);
    - conflicts under rule 1 are ruled;
    - the reading file's SHA-256 is recorded in `v2/sources.json`.

    The converter takes D-096 changes, D-097 classes, levels and sizes only from that file.

    **Pass:** the package matches the hashed reading on every field. A difference is a fail.

    The counts of D-096 changes and of D-097 findings, possibilities and "neither" statements are published with the result.
12. **Standard and site.**
    - `python -m aeg.validate` passes under 2.5.0;
    - the site builds;
    - `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes;
    - the rendered page of each excluded system shows its quotation and reason (D-097 rule 5), checked by looking at the page.
13. **v1 untouched.** Every file in `aeg-d-dwarfs/v1/` has the checksum it had at commit `5dc4091`.

**Pass** = all thirteen hold. Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right.
- The v1 tests, which stand for v1. For unchanged rows they carry over, because item 2 makes those rows identical.
- The `beyond_source_range` count (39 against D-060's 26 below the metallicity floor). It is reported with the result and explained; the flag itself is unchanged.
- Columba I: v1 uses Geha 2026 because no original passes the plotting rules. Fritz 2019's preferred limit does not change that (rule 1). The second reading records it.
