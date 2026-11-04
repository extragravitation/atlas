# aeg-d-dwarfs/v2: reproduction test (draft; frozen on merge, before conversion)

**Status: draft, revision 3, for JvH's approval.** Written 2026-11-04, before `convert.py` for v2 exists. No v2 value has been computed.
- Revision 2 answered the first independent review (`docs/sources/readings/step-d-2026-11-04/dwarfs-review-1.md`).
- Revision 3 answers the second (`dwarfs-review-2.md`, "the review") and applies D-099.

On merge, this file's SHA-256 goes into `v2/sources.json`. It is not edited after merge. If the test fails, v2 does not ship and the failure is published; the test is not changed to pass (operating rule 5; D-005).

**Depends on:**
- data standard 2.5.1 (D-093, D-095, D-099 rule 1);
- D-096 (defer to the source's stated choices);
- D-097 (when D-025 excludes a system);
- D-098 (D-096 rule 2 for the same data points only; three classes for D-097);
- D-099 (sources that count; the classes made mechanical).

D-099 (PR #148) is merged before this test is frozen.

## Purpose

v2 re-issues `aeg-d-dwarfs/v1` (standard 2.0.0) under standard 2.5.1 (D-083, D-084). It:
- adds the uncertainty terms read at source in step A (`docs/sources/readings/step-a-2026-11-04/dwarfs-adjudication.md`, "the adjudication");
- adds the half-light radius, ellipticity and distance errors that v1 did not carry;
- applies D-096 to D-099 to every system.

**Values change only where D-096 requires it,** and each change is listed with its source quotation. v2 sets `x_value_change_ruling = D-096` if any value changes. v1 stays published and unchanged; the frozen audit samples v1's rows.

## Rules applied

1. **Scope of D-096 (D-098).** D-096 rule 1 chooses among the values offered by the source that D-038 and the other value rulings select. It does not choose the source.
   - **Conflicts go to JvH before conversion.** The second reading (item 11) may find a source's stated preference that conflicts with an earlier value ruling (for example D-052, D-055, D-061 item 4 or D-062). Each such conflict is listed and brought to JvH **before the first conversion run**. The converter is not run until it is ruled. No conflict is resolved after v2 values exist.
2. **D-096 rule 1, preferred values.** Known case: Phoenix II (`aeg-s-000394`).
   - **The source's values.** Fritz et al. 2019 (arXiv 1805.07350v4, `spec_v1_ref1_arx.tex`, e-print SHA-256 `41cad1cd…`) print two values in Table 4:
     - 9.5 (+6.8/−4.4) km/s at l. 446;
     - 11.0 (+9.4/−5.3) km/s at l. 452.
   - **The preference.** The caption (l. 436) reads: "Above the line we show the values calculated from all possible members, below those from the certain members. We indicate in bold which determination we prefer". The bold row is 11.0.
     - l. 393: "our preferred set of values are those derived when excluding this star".
     - l. 546 (conclusions) gives 11.0 "for the preferred membership selection".
   - **The abstract (l. 75) prints 9.5.** This is recorded so the reader does not raise it as a conflict: the table's bold mark and the conclusions state the preference.
   - **In v2 the default is 11.0 (+9.4/−5.3).** The 9.5 value becomes an appended alternative row:
     - `role = alternative`, `alternative_of` = the Phoenix II default, `plotted = false`, `not_plotted_reason = alternative_value`;
     - its g columns are bit-for-bit equal to v1 `aeg-d-dwarfs/v1/m000051`.
   - **The D-038 2B coding.** v1's σ coding (`v1/reading/sigma_rules_rows_v3.csv`, `phoenix_2`, `v2`) filed the certain-members value as "subset (D-038 2B)". D-098 reads 2B as covering multi-population fits only.
   - **D-038 1A for the new default** is decided by v1's frozen step: `v1/reproduction/apply_sigma_rules_v3.py`, which passes a value whose coding has `coverage = beyond_rh`.
     - The `phoenix_2`/`v2` coding row has `coverage = beyond_rh`, from Fritz Table 2 col. 4 (the certain members at 0.57, 1.78, 1.71, 1.82 and 1.54 R_half).
     - This is D-038 1A's "as the source states it". v1 has no D-051 member-table computation for Phoenix II (no row in any `v1/reading/coverage_config*.csv`), so none is run.
     - **If the new default fails 1A or any other plotting rule,** Phoenix II is recorded, not plotted. The 9.5 value is not promoted to default.
   - Fritz l. 415 ("does not depend significantly on which set of members is considered") is quoted in the result.
3. **D-096 rule 2, excluded data (D-098 rule 1).** It changes an input only where the Atlas computes from the same data points the source excluded.
   - For this dataset that means only the D-051 coverage computation from a source's per-star member table. It uses only the stars the source states it used for the chosen value.
   - A printed σ, radius, distance or magnitude already reflects the source's exclusions and is not changed by rule 2.
4. **D-097 classes (D-098 rule 2; D-099 rule 4).** The second reading (item 11) classes every statement about equilibrium, binding or tides in the sources that count.
   - **Sources that count (D-098 rule 3; D-099 rule 2):**
     - the paper whose σ is used (for rows taken from Geha et al. 2026, that re-analysis);
     - the structure original;
     - the source the Atlas takes the distance from.

     Magnitude, gas, metallicity and compilation papers do not count.
   - **Possibility:** the source hedges the state itself with "may", "might", "could", "possibly" or "perhaps". **Plotted,** with the quotation in `notes`.
   - **Finding:** any other statement or conclusion, in the source's own words or by citing others, that the system is out of equilibrium, unbound, being tidally disrupted or tidally disturbed. It includes "likely", "unlikely to be", "suggest", "support" and "consistent with".
     - **Excluded:** `plotted = false`, `not_plotted_reason = other`, the quotation in `notes`, and a row in `data/registry/excluded.csv` (item 8).
   - **Neither:** tidal tails, stripping, extension or mass loss mentioned on their own, or orbital remarks. Recorded in the reading only.
   - **Several statements:** any finding in any source that counts makes the system a finding.
   - **Known findings, by ruling (D-097 rule 1; D-099 rule 4):**
     - **Andromeda XXVII** (`aeg-s-000365`). Collins et al. 2013 (arXiv 1302.6590, `M31dsphsv3.tex`, l. 1423–1427): "Andromeda XXVII (And XXVII) is a somewhat unusual object as it is currently undergoing tidal disruption, spreading its constituent stars into a large stellar stream … As such, it is unlikely to be in virial equilibrium, if it remains bound at all." l. 1439, "may no longer be a gravitationally bound system", is also recorded.
     - **Antlia II** (`aeg-s-000367`). Ji et al. 2021 (`main-arxiv.tex`, l. 104, abstract): "Overall, the new kinematic measurements support a tidal disruption scenario for the origin of these large and extended dwarf spheroidal galaxies."
     - The second reading confirms each at source. A disagreement goes to JvH before the first conversion run, and the ruling stands until then.
   - Excluded systems' values are unchanged. They stay visible on their own pages (D-097 rule 5).
5. **Sizes of uncertainty terms: one rule for every row, applied at source in this test.**
   - A size is `given` only when the source states it for these systems, or for a class it names that contains them, for the method or quantity as the package uses it.
   - A size the source states for its own analysis, for one test case, or for systems other than those the row covers is `not_given_by_source`. The note quotes the statement.
   - The wording gives the kind:
     - "up to", "at most" or "better than" → `upper_bound`;
     - a published lower and upper value of a parameter → `range`;
     - a printed ± error, a "typical" value or a plain value → `as_released`.
   - The statuses and kinds in item 7 are fixed by this test. The second reading confirms the scope of each stated size (item 11). A disagreement goes to JvH before conversion, never after.
6. **Two-sided sizes.** Where a size varies by row and has two sides, `size_column` names the `_hi` (or `_high`) column.
   - The column of the same stem ending `_lo` (or `_low`) holds the other side.
   - Both sides are used by the registry formula and the views.
   - Item 7 checks that every row filled in one is filled in the other.

## The test

Applied to the v2 tables, with v1 at commit `5dc4091` as the reference.

### A. Values

1. **Rows.**
   - v2 has v1's 64 measurement rows, in v1's order, with the same `measurement_id` stem and `system_id`.
   - Alternative rows created by D-096 are appended after them, with new sequential `measurement_id`s.
   - `r_kpc` equals v1's on every row not listed under item 3.
2. **Measurements table.** On every row not listed under item 3, the following are bit-for-bit equal to v1's: `g_obs`, `g_bar`, `g_bar_stars`, `g_bar_gas_cold`, `g_obs_err_*` and `g_bar_err_*`.
   - **Every other v1 measurements column is unchanged,** except:
     - `plotted`, `not_plotted_reason` and `notes`, as rule 4 and item 8 require;
     - `role` and `alternative_of`, for D-096 rows;
     - `assumptions` and `flags`, which gain the D-038 1A assumption and the `star_count_weighting` flag (item 9);
     - `x_dwarfs_flags`, which may gain `distance_inherited` (item 9);
     - every column of the rows listed under item 3.
   - **New measurements columns are only these:**
     - `g_bar_err_point_lo/hi` (item 5);
     - `err_level`, `err_level_status`, `g_bar_err_level` and `g_bar_err_level_status` (item 5);
     - the extension columns of item 6;
     - `x_dwarfs_binary_screening` (item 9).
2a. **Observables table.**
   - v1's observable rows are kept, in v1's order, with v1's values. Their IDs differ only in the dataset prefix.
   - **Allowed changes:**
     - `err_lo`, `err_hi` and `source_ref` on `half_light_radius`, `structural_param` and `distance` rows (item 6);
     - the added columns `err_level` and `err_level_status` (item 5).
   - New observable rows are appended after v1's last, only for values that item 3 introduces (for example Phoenix II's 11.0 km/s).
2b. **Systems table.**
   - Unchanged, except the fields that record a system's default and plotting status, for systems listed under item 3 or excluded under rule 4.
   - No new systems columns.
3. **Changed values.** Every row whose values differ from v1 is listed in `REPRODUCTION_RESULT.md` with:
   - the rule of D-096 that changed it, and the line of the second reading that records it;
   - the source quotation and location;
   - the old and new inputs, and the old and new `r_kpc`;
   - for D-096 rule 2 changes, the data points dropped;
   - the result of the existing plotting rules on the new value (rule 2).

   Phoenix II is one such row. A change not in the second reading, or not traceable to D-096, is a fail.
4. **Arithmetic.** g_obs and g_bar recomputed from the stored inputs agree with the stored values to 10⁻⁹ (as v1 test 3).

### B. Uncertainties (standard 2.5.1; §2a, §3 and §7a as in 2.4.0; §12 as in 2.5.1)

5. **Error columns.**
   - **`g_obs_err_*`** hold the σ error only, as in v1. The column description says that each pipeline's per-star velocity floors are inside it: the source folds them into its σ error, and they cannot be separated (term `velocity_error_model`).
   - **`g_bar_err_*` keep v1's values.** For five systems, v1 folded the paper's modulus into the magnitude error in quadrature (`v1/reproduction/inputs_v2.py` `MAG_OVERRIDE`):

     | System | ID | Modulus error (mag) |
     |---|---|---|
     | Andromeda VI | `aeg-s-000347` | 0.07 |
     | Andromeda VII | `aeg-s-000348` | 0.10 |
     | Phoenix | `aeg-s-000393` | 0.1 |
     | Leo T | `aeg-s-000390` | 0.2 |
     | Tucana | `aeg-s-000402` | 0.16 |

     - **Why the modulus does not belong in the error.** The magnitude is rebuilt as m = M_V + μ_paper. Under the D-061 and D-053 pairing, M_V is the paper's own, derived with that same μ_paper, so μ_paper cancels. The second reading confirms at source, for each of the five, that the M_V used was derived with the modulus used. If one was not, it goes to JvH before conversion.
     - **`g_bar_err_point_lo/hi` are added on every row:**
       - on these five rows, the M_V error alone, propagated as v1 propagates the total;
       - on Leo T, empty, because de Jong et al. 2008 print M_V without an error (term `g_bar_point_leo_t`, `not_given_by_source`);
       - on the other 59 rows, equal to `g_bar_err_*`.
     - The column descriptions say all of this. No §7a row is added for the modulus, because it moves neither axis.
   - **Confidence levels** are set from the second reading (item 11), never assumed:
     - **σ:** `err_level` and `err_level_status` per row, from the level each σ source states. Examples:
       - "If resolved, we quote the 1-sigma errors" (Geha et al. 2026 l. 741) → 0.683, `stated`;
       - "the 95th percentile of the posterior" → 0.95, `stated`;
       - "the values at the 90-th percentile" (Fritz l. 388) → 0.90, `stated`.

       Where the σ source states no level, `err_level` is empty and the status is `not_given_by_source`.
     - **Andromeda XII** (`aeg-s-000352`; D-062): `err_level` is empty and `err_level_status = not_given_by_source`, unconditionally.
       - The limit is the upper end of Collins et al. 2013's two-sided interval, 0.0 (+4.0) km/s. On a `limit = upper` row, `err_level` is the level of the limit (standard §3), and no limit level is stated.
       - The note gives Collins's 1σ wording as the second reading finds it and says that this is the upper end of a two-sided interval.
       - The flag `limit_from_1sigma_upper_error` stays in `x_dwarfs_flags`.
     - **Magnitudes:** `g_bar_err_level` and `g_bar_err_level_status` per row, the same way, from the level each magnitude source states.
6. **Half-light radius, ellipticity and distance errors** are added wherever the original prints them.
   - **In the observables** (`half_light_radius`, `structural_param` and `distance`, `err_lo`/`err_hi`), with `no_uncertainty` noted in `source_ref` where the original prints none.
   - **In new measurements extension columns** (standard §12 as in 2.5.1):
     - `x_dwarfs_rh_err_lo_arcmin`, `x_dwarfs_rh_err_hi_arcmin`: the printed r_h error carried to the circularised R_h with ε fixed;
     - `x_dwarfs_ellipticity`: the ε used in R_h = a√(1 − ε), or 0 where the radius is printed circularised;
     - `x_dwarfs_ellipticity_err_lo`, `x_dwarfs_ellipticity_err_hi`: its printed errors;
     - `x_dwarfs_eps_used`: 1 where a√(1 − ε) is used, else 0;
     - `x_dwarfs_rh_semimajor_assumed`: 1 on rows flagged `rh_semimajor_assumed`, else 0;
     - `x_dwarfs_distance_err_lo_kpc`, `x_dwarfs_distance_err_hi_kpc`;
     - `x_dwarfs_gbar_stars_distance_exponent`: −2 on rows flagged `mv_distance_independent`, else 0.
   - Error columns are empty where the original prints no error.
   - **Checked against v1.** The R_h and ε errors are compared with v1's own double reading (`v1/reading/structure_values_all.csv`, `err_minus`/`err_plus`). A difference is resolved at source before conversion.
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly the rows below.
   - Each cites its source at the location given in the adjudication or this test, and `covariance` is `not_published`.
   - Rows marked "per system" are one row for each system named, with `term_id` `<stem>_<system_id>`, a single `system_id` in `applies_to`, and the scale shown.
   - Given sizes that vary by row are `as_released`. Each original's stated level is recorded in the observables' `err_level` (item 5).

**Shape and direction**

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `half_light_radius` | point | * | both | given | `size_column` `x_dwarfs_rh_err_hi_arcmin` (rule 6), `as_released` | `dw_rhalf_wolf` | §2a rule 7: g_obs ∝ 1/R_h, g_bar ∝ 1/R_h² (stars and gas); left out of both point columns |
| `half_light_radius_<system_id>` | point | per system: each whose structural original prints no R_h error | both | not_given_by_source | — | `dw_rhalf_wolf` | from the second reading; v1's observables show examples (Andromeda VI, Antlia II, Tucana V) |
| `ellipticity` | point | * | both | given | `size_column` `x_dwarfs_ellipticity_err_hi` (rule 6), `as_released` | `dw_ellipticity` | enters only where `x_dwarfs_eps_used` = 1 |
| `ellipticity_<system_id>` | point | per system: each with `x_dwarfs_eps_used` = 1 whose original prints no ε error | both | not_given_by_source | — | `dw_ellipticity` | from the second reading |
| `ellipticity_radial_variation` | system | * | both | not_given_by_source | — | `dw_ellipticity` | "Some galaxies show changes in the position angle and/or ellipticity with radius and the current LVDB format does not account for this" (Pace 2025 §5, l. 699); Sculptor 0.23–0.49 by subsample (Muñoz 2018) |
| `rh_convention_profile` | system | * | both | not_given_by_source | — | `dw_rh_circularised` | profile family, and semi-major or circularised convention (flag `rh_semimajor_assumed`); effect by the formula below (D-052 item 2) |
| `deprojection_4_3` | dataset | * | both | given | `size_lo` 1.305, `size_hi` 1.352, `size_unit` r½/R_h, `range` | `dw_rhalf_wolf` | a parameter term (§2a rule 4). Wolf et al. 2010 Appendix table (l. 1793–1800): Plummer 1.305 to Sérsic n = 8 1.352; "accurate to better than 2%" (l. 150–152). 4/3 is the default |
| `distance` | system | * | both | given | `size_column` `x_dwarfs_distance_err_hi_kpc` (rule 6), `as_released` | `dw_distance` | g_obs ∝ 1/D; g_bar_stars ∝ D^e with e from `x_dwarfs_gbar_stars_distance_exponent` (0, or −2 for Boötes III, D-061 item 2); gas ∝ D⁰ (adjudication F1) |
| `distance_<system_id>` | system | per system: each whose distance source prints no error | both | not_given_by_source | — | `dw_distance` | for example Antlia II: Vivas et al. 2022 give a 5.4 kpc dispersion and a ~13 kpc gradient (l. 264–266), quoted in the note |
| `distance_calibration_savino` | dataset | the systems whose distance source is Savino et al. 2022 | both | given | `size_value` 0.035, `size_unit` fraction of D, `as_released` | `dw_distance` | see below |
| `distance_calibration_other` | dataset | * | both | not_given_by_source | — | `dw_distance` | Carlin et al. 2017's anchor modulus has no error (l. 114); Higgs et al. 2021's TRGB calibration states none (l. 361); Medina et al. 2018 (1802.01581v1, `ms.tex`, e-print SHA-256 `3108c7bf…`, l. 266) gives 1.8 % and ~3.6 % for assumed metallicity offsets of ±0.5 and ±1.0 dex, a conditional test, not an error |

`distance_calibration_savino` note:
- Savino §7 (Conclusions), l. 1244: "Through extensive tests we quantified our typical systematic uncertainties to be ∼3.5%".
- **Possible overlap.** Savino §5 (l. 952) says the quoted intervals "have been computed to account for our uncertain knowledge of the RR Lyrae metallicity, pulsation parameters, and of the adopted PWZ calibration". It does not say whether the 3.5 % overlaps them.
- The note says so. Views show the term beside the error bars, never added in.

**Velocities and the estimator**

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `velocity_error_model` | dataset | * | g_obs | not_given_by_source | — | — | per-star floors inside each source's σ error; effect on σ not stated: Geha 2026 k_v 1.4, floor 1.1 km/s (l. 420); Tollerud 2012 2.2 km/s (l. 268); Heiger 2024 1 km/s (l. 109); Kvasova 2024 1.49 km/s (l. 260); Collins 2013 mask offsets (l. 571–573) |
| `binaries` | system | * | g_obs | not_given_by_source | — | — | Wolf l. 1212–1214: "up to ∼20%" in σ, only "in the smallest dSphs" (citing Minor 2010); rule 5. Screening per row in `x_dwarfs_binary_screening` (item 9) |
| `membership` | system | * | g_obs | not_given_by_source | — | — | Tollerud's "few-percent level" applies to its own systems only (rule 5) |
| `rotation` | system | * | g_obs | not_given_by_source | — | — | Pace 2025 §5 |
| `light_weighting` | dataset | * | g_obs | not_given_by_source | — | `dw_member_sample_sigma` | member-sample σ taken as the light-weighted σ (D-038 1A) |
| `estimator_normalisation` | dataset | * | g_obs | not_given_by_source | — | `dw_equilibrium` | Wolf's "±10%" is a band drawn for the classical dSphs (l. 922–927), not a stated error for these systems (rule 5) |
| `anisotropy_profile` | dataset | * | g_obs | not_given_by_source | — | `dw_equilibrium` | Wolf l. 990–992: "the errors on M_half increased by roughly 0.05 dex when the (rather extreme) second β(r) form was used". This is the error of Wolf's own Jeans analysis, so rule 5 gives no size. The estimator-normalisation and anisotropy terms both describe the estimator; no source states their correlation |

**Light and gas**

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `g_bar_point_leo_t` | point | `aeg-s-000390` | g_bar | not_given_by_source | — | — | de Jong 2008 M_V printed without an error (item 5) |
| `luminosity_function_martin` | dataset | the systems whose photometry original is Martin et al. 2016 | g_bar | not_given_by_source | — | — | Martin l. 385: "A test performed by assuming that And I is instead…", with ∼0.2 mag brighter for an 8-Gyr population. A one-galaxy test, so rule 5 gives no size. The "0.29 ± 0.11 magnitudes fainter" comparison with the literature is quoted too |
| `luminosity_function_other` | dataset | * | g_bar | not_given_by_source | — | — | IMF and population assumed in other sources' luminosity functions: Muñoz 2018 "assuming a Salpeter initial mass function" (l. 416) |
| `band_transformation` | dataset | * | g_bar | not_given_by_source | — | — | Muñoz l. 468 (Jordi 2006); Martin l. 379 (Ibata 2007); Richstein; Leo T (D-055 item 7) |
| `extinction` | system | * | g_bar | not_given_by_source | — | — | Martin l. 377; Higgs l. 221–222; Pace App. A l. 800 |
| `solar_magnitude` | dataset | * | g_bar | not_given_by_source | — | — | 4.85 (McLaughlin & van der Marel 2005); Carlin and Richstein use 4.83 |
| `stellar_ml` | dataset | * | g_bar | given | `size_column` `x_dwarfs_upsilon_v_high` (rule 6, companion `x_dwarfs_upsilon_v_low`), `range` | `dw_stellar_ml` | the D-060 envelope |
| `helium_factor` | dataset | * | g_bar | not_given_by_source | — | — | 1.33 (Lelli et al. 2016) |
| `gas_inside_rhalf_aeg-s-000390` | system | `aeg-s-000390` | g_bar | not_given_by_source | — | `dw_gas_half_total` | Leo T: half the total HI mass (flag `gas_half_total`) |
| `gas_inside_rhalf_aeg-s-000393` | system | `aeg-s-000393` | g_bar | not_given_by_source | — | `dw_gas_half_total` | Phoenix: as above |
| `hi_flux` | system | * | g_bar | not_given_by_source | — | — | Putman 2021's HI mass errors "are from the distance errors shown" (MRT Note 4), so they are part of `distance` and cancel in g_bar. No flux error is stated. Phoenix's "confusion with Galactic emission" (Note 22) is quoted |
| `hi_limit_assumptions` | dataset | * | g_bar | not_given_by_source | — | — | 5σ limits with a fixed 10 km/s width (Putman l. 176) and an assumed central concentration (l. 166); limits enter g_bar as zero |
| `molecular_ionised_gas` | dataset | * | g_bar | not_given_by_source | — | — | `not_addressed` in v1's `x_baryon_inventory` |
| `heterogeneity` | dataset | * | both | not_given_by_source | — | — | "there will be systematics in the LVDB" (Pace §5) |

   - **List-valued `applies_to`.** "The systems whose …" are written as semicolon lists of `system_id`s (standard §7a), taken from the distance and magnitude observables' `source_ref`.
   - **Not rows, with reasons:**
     - **Equilibrium and sphericity** are assumptions (§2a rule 4; registry `dw_equilibrium`), not uncertainty terms.
     - **The modulus folded in by v1** moves neither axis (item 5).
     - **Savino's RR Lyrae metallicity prior** (0.06 mag) is inside the printed intervals (l. 952).
     - **Inherited host distances** are a flag, not a term (item 9).
   - **Registry.** Every `dw_*` entry named on a v2 row or in this table gains an `aeg-d-dwarfs/v2` dataset entry: `dw_equilibrium`, `dw_rhalf_wolf`, `dw_rh_circularised`, `dw_distance`, `dw_magnitude_modulus`, `dw_gas_half_total`, `dw_hi_distance_rescaled` and `dw_stellar_ml`, plus two new entries:
     - **`dw_member_sample_sigma`** (D-038 1A): "member-sample σ taken as representative of the light-weighted σ". Not adjustable, no effects.
     - **`dw_ellipticity`**: the ε used in R_h = a√(1 − ε). Not adjustable.

     **Effects formulas.** One assumption per formula, each with a numeric parameter p and default p0. At p = p0 every formula returns the stored value. Here e = `x_dwarfs_ellipticity`, u = `x_dwarfs_eps_used`, s = `x_dwarfs_rh_semimajor_assumed`, and k = `x_dwarfs_gbar_stars_distance_exponent`.

     | Assumption | p | p0 | g_obs | g_bar_stars and g_bar_gas_cold |
     |---|---|---|---|---|
     | `dw_rhalf_wolf` | r½ scaled by p, against 4/3 R_h | 1 | `g_obs * p0 / p` | each `* (p0 / p)^2` |
     | `dw_distance` | D scaled by p | 1 | `g_obs * p0 / p` | stars `* (p / p0)^k`; gas unchanged |
     | `dw_ellipticity` | shift in ε | 0 | `g_obs * sqrt((1 - e - u*p0) / (1 - e - u*p))` | each `* (1 - e - u*p0) / (1 - e - u*p)` |
     | `dw_rh_circularised` | from semi-major (0) to circularised (1) reading of r_h | 0 | `g_obs * (1 - e)^(s*(p - p0)/2)` | each `* (1 - e)^(s*(p - p0))` |

     - In each case `g_bar` = `g_bar_stars` + `g_bar_gas_cold` after the change.
     - The `half_light_radius` term uses the `dw_rhalf_wolf` formula with p = R_h′/R_h.
     - The `deprojection_4_3` term uses it with p = (r½/R_h)/(4/3).
   - **Checked before the freeze.** A dummy package (v1's tables with this test's new columns, and a terms table with exactly these rows) passed `validate_v22` and `validate_v24` with 0 problems on 2026-11-04. The dummy registry added `dw_member_sample_sigma` and `dw_ellipticity`.
   - **Checked again on the real tables (item 12).** Every two-sided `size_column` has its companion filled on the same rows (rule 6).

### C. Structure and flags

8. **Plotting.**
   - **D-097 findings** are `plotted = false`, `not_plotted_reason = other`, with the quotation in `notes`. Each has a row in `data/registry/excluded.csv`, with the columns of standard §5:
     - `system`: the system_id;
     - `dataset`: `aeg-d-dwarfs/v2`;
     - `reason`: "D-097 finding: " and the quotation;
     - `citation`: bibcode and location.
   - The file, and the site's display of each excluded system's quotation and reason on its page, are built in a separate pull request, merged before the first conversion run.
   - **D-097 possibilities** are plotted, with the quotation in `notes`. Each is checked against the reading.
   - **D-096 alternatives** are `plotted = false`, `not_plotted_reason = alternative_value`.
   - **Rows listed under item 3** are plotted as the existing rules decide for the new value (rule 2).
   - **Every other row** is plotted as in v1.
9. **Named items v1 omitted.**
   - **D-038 1A.** `dw_member_sample_sigma` is added to `assumptions`, and the §11 flag `star_count_weighting` to `flags`, on every row whose σ passed D-038 1A in v1's coding. These are the rows whose selected value has `coverage = beyond_rh` or a passing D-051 table check (`v1/reading/sigma_selection_v3.csv`, by v1's frozen `apply_sigma_rules_v3.py`), plus Phoenix II's new default if it passes (rule 2).
   - **Binary screening.** A per-row extension column `x_dwarfs_binary_screening` records, as D-025 asks, whether the σ source states multi-epoch screening for binaries. It is a closed list:
     - `multi_epoch_stated`;
     - `no_multi_epoch_stated` (the source says it has no multi-epoch data);
     - `not_stated`.

     The values come from the second reading, which starts from `v1/reading/sigma_values.csv` `binaries`.
   - **Inherited distances.** The flag `distance_inherited` goes in `x_dwarfs_flags` (it is not in the §11 list) on every system whose distance source gives its host's distance. The count is reported, possibly zero.
10. **Descriptor.**
    - `standard_version` `2.5.1`;
    - `x_value_change_ruling` `D-096` if item 3 lists any row;
    - the other 2.0 descriptor fields as v1, updated.

    The column descriptions state what items 5 and 6 say.
11. **Second reading (D-031 item 3; D-097 rule 4), done before conversion.** Two independent readers, with no access to the conversion code or any v2 table, each record, for every system:
    - the R_h and ε errors as printed, with quote and location;
    - the confidence level each σ and magnitude source states for its errors or limits, with quote;
    - **D-096 fields:** whether each σ, structure, distance or photometry source marks a preferred value, or excludes data points the Atlas computes from (rule 3), with quote and location;
    - any conflict between a stated preference and an earlier value ruling (rule 1);
    - **D-097 field:** every statement about equilibrium, binding or tides in the sources that count, classed as finding, possibility or neither (rule 4), with the quote;
    - the binary-screening class (item 9), and whether the distance is inherited from the host;
    - for the five systems in item 5, whether the M_V used was derived with the modulus used;
    - confirmation of the scope of each stated size in item 7 (rule 5).

    **Before the first conversion run:**
    - both readings are complete and committed;
    - the two readings are compared with each other, with the step A readings and with v1's structure reading (item 6);
    - every disagreement is resolved at source by a session that has seen no v2 value (none exists yet), and recorded with its resolution;
    - conflicts under rules 1, 4 and 5 are ruled by JvH;
    - the SHA-256 of the resolved reading file is recorded in `v2/sources.json`.

    The converter takes D-096 changes, D-097 classes, confidence levels and binary-screening classes only from that file.

    **Pass:** the package equals the hashed reading on every field. Any mismatch is a fail.

    The counts of D-096 changes and of D-097 findings, possibilities and "neither" statements are published with the result.
12. **Standard and site.**
    - `python -m aeg.validate data/packages/aeg-d-dwarfs/v2` passes under 2.5.1;
    - `python -m aeg.formula_check` passes;
    - the site builds;
    - `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes;
    - the built HTML page of each excluded system contains its quotation exactly as in `excluded.csv`, checked by a text search of the built page (D-097 rule 5).
13. **v1 untouched.** Every file in `aeg-d-dwarfs/v1/` has the checksum it had at commit `5dc4091`.

**Pass** = all thirteen hold (items 2a and 2b are part of item 2). Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right.
- The v1 tests, which stand for v1. For unchanged rows they carry over, because item 2 makes those rows identical.
- The `beyond_source_range` count (39 against D-060's 26 below the metallicity floor). It is reported with the result and explained; the flag itself is unchanged.
- **Columba I.** v1 uses Geha 2026 because no original passes the existing plotting rules. Fritz 2019's preferred limit (< 16.1 km/s) is not a passing value, so D-096 does not change that. The second reading records it.
