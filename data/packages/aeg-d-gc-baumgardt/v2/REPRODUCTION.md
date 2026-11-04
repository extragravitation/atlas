# aeg-d-gc-baumgardt/v2: reproduction test (draft; frozen on merge, before conversion)

**Status: draft, revision 2, for JvH's approval.** Revision 2 answers an independent review (`docs/sources/readings/step-d-2026-11-04/gc-review-1.md`) and applies D-098. Written 2026-11-04, before `convert.py` for v2 exists. No v2 value has been computed. On merge, this file's SHA-256 goes into `v2/sources.json`, and it is not edited after the first v2 conversion run. If the test fails, v2 does not ship and the failure is published; the test is not changed to pass (operating rule 5; D-005).

**Depends on:**
- data standard 2.5.0;
- D-087 (`model_dependence`);
- D-096 (defer to the source's stated choices);
- D-097 (when D-025 excludes a system);
- D-098 (D-096 rule 2 applies only to the same data points; three classes for D-097; NGC 2298 and Pal 5).

## Purpose

v2 re-issues `aeg-d-gc-baumgardt/v1` (standard 2.0.0) under standard 2.5.0 (D-083, D-084). It:
- adds the uncertainty terms read at source in step A (`docs/sources/readings/step-a-2026-11-04/gc-adjudication.md`, "the adjudication");
- applies D-087, D-096, D-097 and D-098 to every cluster;
- corrects the registry locations found in step A (adjudication F7).

**Values change only where D-096 requires it,** and each change is listed with its source quotation. v2 then sets `x_value_change_ruling = D-096`. v1 stays published and unchanged. D-046 (Pal 1, the failed King-fit test) and D-047 (Harris-only clusters recorded, not plotted) carry over unchanged.

## Rules applied

1. **D-096 rule 2, excluded data (as clarified by D-098 rule 1).** It changes a value only where the Atlas computes from the data points the source excluded.
   - **NGC 6715 (M54).** Baumgardt 2017 (B17; arXiv 1609.08794v1, l. 586–589): "We have therefore neglected all data points beyond 200'' in the dynamical analysis of this cluster", because the sample "includes stars from the Sagittarius dwarf galaxy". The cut is a radius, so it carries over to v1's binning.
   - **How the cut is applied.** v1 stores each line-of-sight bin's mean radius ⟨r⟩ (`x_gc_baumgardt_r_arcsec`), not its star radii. v2 drops every M54 bin of the RV code with ⟨r⟩ > 200″. On v1's bins these are the bins at 269.01″, 410.12″ and 679.1″, leaving 13 of 16. The bin at 170.92″ keeps any of its stars beyond 200″; v1 has no star radii to remove them. The note says so.
   - **Re-inference is expected.** v1's code (`aeg.dispersion`) infers bin edges from the remaining radii. The outer edge of the 170.92″ bin therefore moves inward, and the light weights of all 13 bins change. This is part of the change, not a separate one.
   - **NGC 2298 and Pal 5 are not D-096 changes** (D-098 rule 1). BH18 dropped the outermost point of its own 2018 profiles. v1 uses the updated `veldis.html` bins, which are different, and in which σ falls outward. Their values are not changed; their plotting is (rule 2).
   - After the M54 cut, D-036's coverage rule (≥ 0.80) and the ≥ 2-bin rule apply as usual. If M54 then fails, its row stays, with `plotted = false` and `not_plotted_reason = coverage_below_threshold`.
2. **D-097 with D-098's three classes.** Classes are decided by what the source says:
   - **finding:** the source states, in its own words or by citing others, that the system *is* out of equilibrium, unbound or being tidally disrupted;
   - **possibility:** that state itself is hedged ("may be disrupting");
   - **neither:** tidal tails, mass loss or tidal extension mentioned on their own.
   - **Sources that count** (D-098 rule 3): the system's dispersion source as used, its structure original and its distance original. For the RV code (pooled data) the dispersion source is the re-analysis papers behind it (B17, BH18, B19), not the pooled literature papers. The structure original is McLaughlin & van der Marel 2005 (MvdM). The distance source is Harris 2010, a compilation; its per-cluster originals are not read, which the result states.
   - **NGC 2298 and Pal 5 are findings** (D-098 rule 4). BH18 (arXiv 1804.08359v2, l. 226–227): "NGC~2298 and Pal~5 have velocity dispersion profiles which increase towards the outer parts, which could be due to the ongoing tidal disruption of these clusters". Every row of both systems is `plotted = false`. Rows that v1 plotted get `not_plotted_reason = other`; rows already unplotted keep v1's reason. `notes` on each row holds the quotation and "D-097 finding (D-098 rule 4)". Their values are unchanged.
   - **Any further finding** in the second reading (item 11) is treated the same way. **Any possibility** stays plotted, with the quotation in `notes`.
   - **The exclusion register.** Every excluded system has one row in `data/registry/excluded.csv`, with the columns of standard §5: `system` (the `system_id`), `dataset` (`aeg-d-gc-baumgardt/v2`), `reason` ("D-097 finding (D-098): " followed by the quotation) and `citation` (paper, arXiv version, file and line). The file is created if it does not exist.
3. **D-087.** `model_dependence` is `none` on every row. v1 has `observable_form` on every row. All 79 rows come from binned profiles: refused and fitted candidates never became rows. The King (1966) light profiles interpolate well-sampled surface-brightness data and are used only as weights.
4. **D-096 rule 1** (preferred values) and **rule 3** (fiducial baselines) are applied wherever the second reading finds them, and only there.

## Order of work (against steering)

1. The second reader (item 11) completes the reading **before the first v2 conversion run**. It writes `v2/reading/d096_d097.csv` and `v2/reading/err_levels.csv`, with no access to v1's g values, `convert.py` or any v2 table.
2. Disagreements between the reading and this test's expectations are resolved at source, before conversion, by a session without access to v1's g values or any v2 value. Each resolution is recorded in `v2/reading/resolutions.md`. A disagreement about NGC 2298, Pal 5 or M54 is recorded but cannot reverse D-098; it is reported to JvH before conversion.
3. The SHA-256 of those three files goes into `data/frozen/gc-v2-reading.json` by a pull request merged before the first conversion run.
4. `convert.py` applies changes and exclusions **only** from the frozen reading files. It contains no system-specific rule of its own.

## The test

Applied to the v2 tables, with v1 at commit `5dc4091` as the reference. "Changed rows" are the rows the frozen reading lists under D-096 (expected: the M54 row only). "Excluded systems" are the systems it lists as D-097 findings (expected: NGC 2298 and Pal 5).

### A. Values

1. **Rows.** v2 has exactly v1's 79 measurement rows, in v1's order. Row k has v1 row k's `system_id` and `x_gc_baumgardt_dataset`, and the same `measurement_id` apart from the prefix (`v1` → `v2`). Excluded systems keep their rows.
2. **Unchanged values.** On every row that is not a changed row, these are bit-for-bit equal to v1's: `g_obs`, `g_obs_err_lo`, `g_obs_err_hi`, `g_bar`, `g_bar_err_lo`, `g_bar_err_hi`, `r_kpc`, and every v1 `x_gc_baumgardt_*` column. On changed rows, `g_bar`, `g_bar_err_*`, `r_kpc`, `x_gc_baumgardt_r_h_pc`, `_l_v`, `_ml_v`, `_ml_v_salpeter` and `_distance_kpc` are also unchanged.
   - **Every other v1 column is unchanged**, except:
     - `measurement_id` (prefix) and the observable IDs in `observed_from` and `baryonic_from` (prefix);
     - `model_dependence` (rule 3);
     - `plotted`, `not_plotted_reason` and `notes` on rows of excluded systems (rule 2), and `notes` on rows with a possibility quotation;
     - on changed rows: `observed_from` (the dropped bins removed), `notes` (the D-096 note), and the values listed in item 3;
     - `assumptions`, if item 7 adds an assumption to every row.
   - New columns are allowed only as listed in items 5, 7 and 9.
3. **Changed values.** The changed rows are exactly those of the frozen reading. Each is listed in `REPRODUCTION_RESULT.md` with:
   - the rule of D-096 that changed it;
   - the source quotation and location;
   - the bins dropped (by observable ID and ⟨r⟩);
   - the old and new σ, σ errors, coverage and bin count, and the old and new g_obs and its errors.
   - **Check:** the new σ, its errors, coverage and bin count equal `aeg.dispersion` (v1's frozen code, with `aeg.king66` weights) run on v1's bins minus the dropped bins, to a relative 10⁻⁹.
   - A change not traceable to the frozen reading is a fail. So is a listed change that is missing.
4. **Arithmetic.** g_obs and g_bar recomputed from the stored σ, r½, L_V and Υ_V, by v1's formulas and `astropy.constants.G`, agree with the stored values to a relative 10⁻⁹ on every row.

### B. Uncertainties (standard 2.4.0 §2a, §3, §7a)

5. **Error columns and confidence levels.**
   - `g_obs_err_*` hold the light-weighted σ error only (point = system for one value per cluster), as in v1. No g_obs point columns are added, because these totals are point-scale only.
   - **`err_level` and `err_level_status` are set per dispersion dataset code,** from `v2/reading/err_levels.csv`. Expected, from step A:

     | Code | Expected | Basis |
     |---|---|---|
     | RV | `stated`, 0.683 | "the $1\sigma$ upper and lower error bars" (BH18 Table 3 caption, `veldis_tab.tex`); the bounds use B17's likelihood-ratio criterion (adjudication F5); the "plus updates" method is not described |
     | K18 | `stated`, 0.68 | "the 16th and 84th percentiles" (K18 l. 282) |
     | D21 | `stated`, 0.68 | "the interval between the 16-th and 84-th percentile" (D21, step A Reader A G11b) |
     | L13 | `not_given_by_source` | no level stated (Reader A G11) |
     | F13 | `not_given_by_source` | "sigma-clipped standard deviation of these 1,000 velocity dispersions": a spread of simulations, not a stated confidence level |
     | L15 | `not_given_by_source` | no level found in step A |

     Where the second reading quotes a level that step A did not find, the reading governs, and the result says so. The same values go on the `sigma_los` observables of each code.
   - `g_bar_err_*` hold the population M/L error, as in v1. `g_bar_err_level` = 0.683 and `g_bar_err_level_status = stated`: "The 1{sigma} error in BC/ChD" (MvdM, `J_ApJS_161_304_clusters.vot`, field `e_(M/L)1`).
   - This error mixes a dataset-scale age term with a system-scale [Fe/H] term (F6). So `g_bar_err_point_*` are empty, the term `g_bar_point` records that the source gives no point-scale part, and the term `ml_population` records the mixed term.
6. **New per-row size columns** (measurements extension columns, standard §12), each copied from v1's observables or v1's sources without change:
   - `x_gc_baumgardt_log_rh_err_lo`, `_hi` (dex): MvdM's R_h errors, from the `half_light_radius` observable;
   - `x_gc_baumgardt_w0_err_lo`, `_hi`: MvdM's W₀ errors; `x_gc_baumgardt_r0_err_lo`, `_hi` (arcsec): MvdM's r₀ errors; both from the `structural_param` observables;
   - `x_gc_baumgardt_ml_v_err` (M☉/L☉): the `e_(M/L)1` value, from the `stellar_ml_population` observable;
   - `x_gc_baumgardt_vt_scatter_mag`: 0.22, 0.45 or 0.70 mag by the cluster's Harris V_t. The ranges are BSH20's "V< 8", "8 < V < 11" and "V>11". The Atlas assigns V_t = 8 and V_t = 11 to the middle range. BSH20 does not say whose magnitudes define the ranges; the Atlas uses Harris's V_t.
   - A row whose source prints no error gets an empty value in that column and the flag `no_uncertainty`, with the column named in `notes`.
   - Standard §12 says core views never depend on extension columns, while §7a (2.4.0) allows a measurements `size_column`. This test reads §7a as allowing an extension column where no core column holds the size. The result records this reading so the standard can settle it.
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly these rows.
   - Each cites its source at the location in the adjudication or the step A readings.
   - `covariance` is `not_published` on every row.
   - Where the table names an `assumption_id`, that registry entry has a non-empty `effects` formula for the term in v2's registry update.
   - **Not uncertainty terms (§2a rule 4):** equilibrium, spherical symmetry and the estimator are assumptions in the registry (`gc_equilibrium`, `gc_rhalf_wolf`), as in v1.

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `half_light_radius` | point | * | both | given | `size_column` `x_gc_baumgardt_log_rh_err_hi` (lower side in `_lo`), dex, `one_sigma` | `gc_rhalf_wolf` | §2a rule 7: g_obs ∝ 1/R_h, g_bar ∝ 1/R_h²; left out of both point columns; MvdM's errors are "χ² within 1 of the global minimum" (l. 2187–2190); correlated with `king_w0` and `king_r0` (one fit; covariance not published) |
| `king_w0` | system | * | g_obs | given | `size_column` `x_gc_baumgardt_w0_err_hi` (lower in `_lo`), `one_sigma` ("Upper/Lower 1{sigma} error in WO", MvdM models VOT) | — | moves the light weights; effect not computed in v2 |
| `king_r0` | system | * | g_obs | given | `size_column` `x_gc_baumgardt_r0_err_hi` (lower in `_lo`), `one_sigma` | — | as `king_w0` |
| `king_wilson_family` | system | * | both | not_given_by_source | — | — | MvdM: Wilson models give "smaller half-light radii $R_h$" (l. 2703–2704); no size stated for Galactic clusters |
| `centre_position` | system | * | g_obs | not_given_by_source | — | — | Harris: centres "uncertain to typically 1-2 arcseconds" (l. 94); effect on σ not stated |
| `distance_hb_zero_point` | dataset | * | g_obs | given | 0.049 mag, `one_sigma` | `gc_distance_hb` | Harris 2010 l. 148; R_Sun and L_V move together, so g_bar is unchanged (F1). Correlated with `distance_hb_slope` (one fit; correlation not published). The calibration includes "dynamical parallax from combined solutions to radial velocity and proper motion dispersions" (Harris §2; Reader A G30): a known issue is opened on this (D-036 #6) |
| `distance_hb_slope` | dataset | * | g_obs | given | 0.033 mag per dex of [Fe/H], `one_sigma` | `gc_distance_hb` | Harris 2010 l. 148; the shift in M_V(HB) is 0.033 × [Fe/H], using `metallicity_feh`; correlated with `distance_hb_zero_point` |
| `distance_hb_scatter` | system | * | g_obs | given | 0.11 mag, `one_sigma` | `gc_distance_hb` | Harris 2010 l. 152, the rms about the calibration |
| `reddening` | system | * | both | given_by_other_source | 0.10 (fraction of E(B−V)), `as_released` | `gc_distance_hb` | "the average errors on … the reddening (10 %)" (Lützgendorf et al. 2013, l. 489): L13's description of Harris (1996), not read at source, applied here to the 2010 edition; the kind of error is not stated. Moves R_Sun only, so g_obs ∝ 1/D and g_bar ∝ 1/D² (F1). Uses each cluster's E(B−V) (item 9) |
| `extinction_law_rv` | dataset | * | both | not_given_by_source | — | `gc_distance_hb` | R_V = 3.1 fixed ("$A_V=3.1\,E(B-V)$", MvdM l. 1212 in arXiv astro-ph/0605132v1); no range stated by Harris or MvdM; acts as `reddening` |
| `integrated_magnitude` | system | * | g_bar | given_by_other_source | `size_column` `x_gc_baumgardt_vt_scatter_mag`, `upper_bound` | `gc_luminosity_vt` | Baumgardt, Sollima & Hilker 2020 (BSH20) Table `tab:comp`, l. 266: the "standard deviation around the mean" of the differences from Harris (2010). It bounds the Harris error from above only because BSH20 calls the estimates "more or less independent of each other" (l. 254). It excludes the mean offsets (+0.03, +0.01 and −0.25 mag); the −0.25 mag offset for V > 11 is a systematic shift this row does not carry. Moves g_bar only (F1) |
| `solar_magnitude` | dataset | * | g_bar | not_given_by_source | — | — | M_V,⊙ = 4.85 (MvdM) |
| `g_bar_point` | point | * | g_bar | not_given_by_source | — | — | item 5 |
| `ml_population` | system | * | g_bar | given | `size_column` `x_gc_baumgardt_ml_v_err`, `one_sigma` | `gc_stellar_ml` | MvdM `e_(M/L)1`; mixes a dataset-scale age term (13 ± 2 Gyr for every cluster) with a system-scale [Fe/H] term (± 0.2 dex), not split by MvdM (F6); already inside `g_bar_err_lo/hi`, so not added again |
| `pop_synthesis_code` | dataset | * | g_bar | given | 0.10, `upper_bound` | `gc_stellar_ml` | MvdM l. 1358, "≲10%" in Υ_V |
| `stellar_ml` | dataset | * | g_bar | given | `size_column` `x_gc_baumgardt_ml_v_salpeter` (upper end), `range` | `gc_stellar_ml` | the registry range: IMF up to Salpeter; dissolution down to 0.53 × `x_gc_baumgardt_ml_v` (lower end, from the registry). MvdM's models build in about 30 % mass loss (MvdM Fig. 4); MvdM used Harris (1996) [Fe/H] (F8) |
| `estimator_normalisation` | dataset | * | g_obs | not_given_by_source | — | `gc_rhalf_wolf` | Wolf et al. 2010 shows "±10% variation about the predicted relation" (l. 927) as guide lines in a figure for classical dwarf spheroidals, not as a stated accuracy; none is stated for clusters |
| `anisotropy_profile` | dataset | * | g_obs | given | 0.05 dex on the mass, `as_released` | `gc_rhalf_wolf` | Wolf l. 974, for dispersion-supported systems in general; its accuracy for these clusters is not stated |
| `deprojection_4_3` | dataset | * | both | given | 0.02, `upper_bound` | `gc_rhalf_wolf` | Wolf, for King (1962) profiles; v1 uses King (1966) (F8). An assumption with a stated accuracy (§2a rule 4) |
| `light_weighting` | dataset | * | g_obs | not_given_by_source | — | — | bins covering ≥ 80 % of the light, against Wolf's whole-system average (F8) |
| `binaries` | system | * | g_obs | not_given_by_source | — | — | BH18 names Pal 13, Arp 2 and Ter 3 as possibly inflated (l. 228–233); K18 gives +0.3 and +0.6 km/s for binary fractions of 5 % and 10 % in its own NGC 6121 data (l. 330), not for these profiles |
| `membership_contamination` | system | * | g_obs | not_given_by_source | — | — | non-members "removed iteratively" (BH18 l. 206) |
| `rotation` | system | * | g_obs | not_given_by_source | — | — | |
| `tracer_mass` | system | * | g_obs | not_given_by_source | — | — | K18 states "≲5%" in σ between its main-sequence samples and literature giant profiles, for NGC 3201 and NGC 6121 only (l. 344); the RV code is mostly giants (BH18 l. 185) |
| `rv_zero_points` | system | * | g_obs | not_given_by_source | — | — | shifts "usually less than 1 km/sec" (BH18 l. 199); effect on σ not stated |
| `ellipticity` | system | * | both | not_given_by_source | — | — | |
| `heterogeneity` | dataset | * | both | not_given_by_source | — | — | the "plus updates" values are not documented; they differ slightly from BH18's printed table (F8) |

   - **Registry update for v2** (`data/assumptions.json`, a new version of each changed entry; v1's entries stay as published):
     - `gc_distance_hb` gains effects formulas, one per cause (F1): calibration terms g_obs ∝ D⁻¹ with g_bar unchanged; `reddening` and `extinction_law_rv` g_obs ∝ D⁻¹ and g_bar ∝ D⁻². It gains the F7 locations.
     - `gc_rhalf_wolf` gains the §2a rule 7 formula for `half_light_radius` (g_obs ∝ R_h⁻¹, g_bar ∝ R_h⁻²) and the effects of the estimator terms.
     - `gc_stellar_ml` gains the formula g_bar ∝ Υ_V, and the F7 correction (KM09's `tab:pred` in arXiv v1).
     - A new entry `gc_luminosity_vt` (role `baryonic_inference`, not adjustable): L_V from Harris V_t; effect g_bar ∝ 10^(−0.4 ΔV_t).
   - **Second reading of term sizes.** Step A's two concordant readings serve as the D-031 second reading for the sizes in this table.

### C. Structure and flags

8. **Plotting.**
   - As v1, plus rule 1's effect on M54 and rule 2's exclusions.
   - D-096 alternatives found by the reading are `plotted = false`, `not_plotted_reason = alternative_value`.
   - MW-PAL1 stays recorded, not plotted (D-046).
   - Every row of an excluded system has its quotation in `notes`. Every possibility found by the reading has its quotation in that system's rows' `notes`.
   - `data/registry/excluded.csv` has exactly one row per excluded system of this dataset, with the columns of rule 2.
   - The built system pages of the excluded systems show the quotation and the reason (checked by looking at the built pages).
   - The counts are published with the result: rows changed under D-096, systems excluded under D-097, and possibilities recorded.
9. **Named items v1 omitted.**
   - **Binary screening flag.** A per-row extension column `x_gc_baumgardt_binary_screening`, closed list, set per dispersion dataset code from the second reading:
     - `multi_epoch_stated`: the source states that stars with multiple velocities are tested and removed. Expected for RV: "Stars where the individual measurements had a less than 5\% probability to be compatible with a constant radial velocity were removed" (BH18 l. 203–204). This applies only to stars with more than one measurement; the note says so.
     - `integrated_light`: the dispersion comes from integrated-light spectra, where screening of individual stars does not apply.
     - `not_stated`: otherwise.
   - **New observables**, from `mwgc.dat` (Harris 2010), for every system with a measurement row: `apparent_magnitude` (V_t, band V), used by `integrated_magnitude` and to assign `x_gc_baumgardt_vt_scatter_mag`. E(B−V) has no §4a quantity, so it goes in the systems `properties` as `ebv_mag`, with the source named, for `reddening`.
   - **Registry corrections (F7):** the KM09 table is `tab:pred` in arXiv v1; MvdM's R_h is in Table 11 (`tab:struc`), W₀ and r₀ in Table 10.
   - **Known issues:** one exists, linked from the dataset page, for each of: the Harris calibration's dynamical-parallax input (`distance_hb_zero_point` note); the M54 bin that straddles 200″ (rule 1).
10. **Descriptor.** `standard_version` `2.5.0`; `x_value_change_ruling` `D-096` if item 3 lists any row; other fields as v1, updated; `x_second_reading` points to `SECOND_READING.md` and the frozen reading files.
11. **Second reading (D-031 item 3).** An independent reader, with no access to `convert.py`, v1's g values or any v2 table, records for every cluster with a measurement row:
    - **D-096 fields:** whether its dispersion source, its structure source (MvdM) or Harris 2010 marks a preferred value, excludes data, or names a fiducial baseline, with quote and location. For an exclusion, whether the Atlas computes from the same data points (D-098 rule 1), and if so, which v1 bins (by observable ID and ⟨r⟩) are dropped.
    - **D-097 field:** every statement in the sources that count (rule 2) about equilibrium, binding or tides, classed as finding, possibility or neither, with the quote and location.
    - **Confidence levels:** for each dispersion dataset code, the level as printed, with quote and location (item 5).
    - **Binary screening:** the value for each dispersion dataset code (item 9).
    - **Pass:** the package matches the frozen reading on every field. Disagreements are resolved at source, as in "Order of work"; one resolved against the package is a fail.
12. **Standard and site.**
    - `python -m aeg.validate` passes under 2.5.0;
    - the site builds;
    - `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes.
13. **v1 untouched.** Every file in `aeg-d-gc-baumgardt/v1/` has the checksum it had at commit `5dc4091`.

**Pass** = all thirteen hold. Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right.
- v1's test 2 result (FAIL, Pal 1; D-046). It stands for v1 and is not re-run.
- MvdM's use of Harris (1996) [Fe/H] behind M/L₁ (F8). It is stated in the `stellar_ml` term's note.
- The per-cluster distance originals behind Harris 2010, which were not read.
- Which v1 rows would change if the pooled literature RV papers were read for D-097. They are not sources that count (D-098 rule 3).
