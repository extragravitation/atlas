# aeg-d-gc-baumgardt/v2: reproduction test (draft; frozen on merge, before conversion)

**Status: draft, for JvH's approval.** Written 2026-11-04, before `convert.py` for v2 exists. No v2 value has been computed. On merge, this file's SHA-256 goes into `v2/sources.json`, and it is not edited after the first v2 conversion run. If the test fails, v2 does not ship and the failure is published; the test is not changed to pass (operating rule 5; D-005).

**Depends on:**
- data standard 2.5.0;
- D-087 (`model_dependence`);
- D-096 (defer to the source's stated choices);
- D-097 (when D-025 excludes a system).

## Purpose

v2 re-issues `aeg-d-gc-baumgardt/v1` (standard 2.0.0) under standard 2.5.0 (D-083, D-084). It:
- adds the uncertainty terms read at source in step A (`docs/sources/readings/step-a-2026-11-04/gc-adjudication.md`, "the adjudication");
- applies D-087, D-096 and D-097 to every cluster;
- corrects the registry locations found in step A (adjudication F7).

**Values change only where D-096 requires it,** and each change is listed with its source quotation. v2 then sets `x_value_change_ruling = D-096`. v1 stays published and unchanged, and D-046 (Pal 1, the failed King-fit test) carries over unchanged.

## Rules applied

1. **D-096 rule 2, excluded data.** Known cases:
   - **NGC 6715 (M54).** Baumgardt 2017 (arXiv 1609.08794v1, l. 586–589): "We have therefore neglected all data points beyond 200'' in the dynamical analysis of this cluster", because the sample "includes stars from the Sagittarius dwarf galaxy". v2 drops M54's bins beyond 200″.
   - **NGC 2298 and Pal 5.** Baumgardt & Hilker 2018 (arXiv 1804.08359v2, l. 226–228): "We therefore neglected the outermost data point of their velocity dispersion profiles in our fits." v2 drops each cluster's outermost line-of-sight bin.
   - After dropping, D-036's coverage rule (≥ 0.80) and the ≥ 2-bin rule apply as usual. A cluster that then fails is `plotted = false` with `not_plotted_reason = coverage_below_threshold`, as v1's rules require.
2. **D-097.** NGC 2298 and Pal 5 are a "possibility" ("could be due to the ongoing tidal disruption"): plotted, with the quotation in `notes`. Any "finding" the second reading records excludes the cluster (recorded, not plotted, `not_plotted_reason = other`, in `excluded.csv`).
3. **D-087.** `model_dependence` = `none` on every row: the King (1966) light profiles interpolate well-sampled surface-brightness data and are used only as weights. A row where a fitted profile stands in for binned dispersion data would be `observable_form`; v1 has none (every plotted value uses binned profiles).
4. **D-096 rule 1** (preferred values) and **rule 3** (fiducial baselines) are applied wherever the second reading finds them.

## The test

Applied to the v2 tables, with v1 at commit `5dc4091` as the reference.

### A. Values

1. **Rows.** v2 has v1's 79 measurement rows, in v1's order, with the same `system_id` and `x_gc_baumgardt_dataset`.
2. **Unchanged values.** On every row not listed under item 3, `g_obs`, `g_bar`, `g_obs_err_*`, `g_bar_err_*` and the `x_gc_baumgardt_*` values are bit-for-bit equal to v1's.
3. **Changed values.** Every changed row is listed in `REPRODUCTION_RESULT.md` with:
   - the rule of D-096 that changed it;
   - the source quotation and location;
   - the bins dropped;
   - the old and new σ, coverage and bin count.
   - M54, NGC 2298 and Pal 5 are expected to be listed. A change not traceable to D-096 is a fail.
4. **Arithmetic.** g_obs and g_bar recomputed from the stored inputs, by v1's frozen code (`aeg.dispersion`, `aeg.king66`), agree with the stored values to 10⁻⁹.

### B. Uncertainties (standard 2.4.0 §2a, §3, §7a)

5. **Error columns.**
   - `g_obs_err_*` hold the light-weighted σ error only (point = system for one value per cluster). `err_level` = 0.683, `err_level_status = stated`: "the $1\sigma$ upper and lower error bars" (BH18 Table 3 caption). The note records B17's likelihood-ratio criterion (adjudication F5).
   - `g_bar_err_*` hold the population M/L error, which mixes a dataset-scale age term with a system-scale [Fe/H] term (F6). So `g_bar_err_point_*` are empty, and a `point` term with `not_given_by_source` records that the source gives no point-scale part.
6. **R_h and King errors** stay in the observables as in v1 (`half_light_radius`, `structural_param`).
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly these rows. Each cites its source at the location in the adjudication, and `covariance` is `not_published`.

| term_id | scale | applies_to | moves | status | size | Note |
|---|---|---|---|---|---|---|
| `half_light_radius` | point | * | both | given | from the R_h observables' errors (§2a rule 7) | g_obs ∝ 1/R_h, g_bar ∝ 1/R_h²; left out of the point columns |
| `king_weights` | system | * | g_obs | given | from the W₀ and r₀ observables' errors | through the light weights; effect not computed in v2 |
| `distance_hb_zero_point` | dataset | * | g_obs | given | 0.049 mag, `one_sigma` | Harris 2010 l. 148; R_Sun and L_V move together, so g_bar is unchanged (F1) |
| `distance_hb_scatter` | system | * | g_obs | given | 0.11 mag, `one_sigma` | Harris 2010 l. 152, the rms about the calibration |
| `reddening` | system | * | both | given_by_other_source | 0.10, `as_released` | "the average errors on … the reddening (10 %)" (Lützgendorf et al. 2013, describing Harris 1996); moves R_Sun only (F1) |
| `integrated_magnitude` | system | * | g_bar | given_by_other_source | `size_column` `x_gc_baumgardt_vt_scatter_mag` (0.22, 0.45 or 0.70 mag by V_t range), `upper_bound` | Baumgardt, Sollima & Hilker 2020 Table "tab:comp": the scatter between two measurements bounds the Harris error from above (F2) |
| `solar_magnitude` | dataset | * | g_bar | not_given_by_source | — | 4.85 (MvdM 2005) |
| `g_bar_point` | point | * | g_bar | not_given_by_source | — | item 5 |
| `pop_synthesis_code` | dataset | * | g_bar | given | 0.10, `upper_bound` | MvdM l. 1358 "≲10%" |
| `stellar_ml` | dataset | * | g_bar | given | the registry range (IMF up to Salpeter; dissolution down to 0.53×), `range` | `assumption_id` `gc_stellar_ml` |
| `mass_loss_models` | dataset | * | g_bar | not_given_by_source | — | about 30 % built in (MvdM Fig. 4) |
| `estimator_normalisation` | dataset | * | g_obs | given | 0.10, `as_released` | Wolf et al. 2010, for dwarf spheroidals; its accuracy for clusters is not stated |
| `anisotropy_profile` | dataset | * | g_obs | given | 0.05 dex, `as_released` | Wolf l. 974, on the mass |
| `deprojection_4_3` | dataset | * | both | given | 0.02, `upper_bound` | Wolf, for King (1962); v1 uses King (1966) |
| `binaries` | system | * | g_obs | not_given_by_source | — | BH18: about 50 % for Pal 13; others not stated |
| `membership_contamination` | system | * | g_obs | not_given_by_source | — | B17 3σ clipping |
| `rotation` | system | * | g_obs | not_given_by_source | — | |
| `tracer_mass` | system | * | g_obs | given | 0.05, `upper_bound` | K18 "≲5%", for NGC 3201 and NGC 6121 |
| `rv_zero_points` | system | * | g_obs | not_given_by_source | — | shifts "usually less than 1 km/sec" (BH18); effect on σ not stated |
| `light_weighting` | dataset | * | g_obs | not_given_by_source | — | bins covering ≥ 80 % of the light, against Wolf's whole-system average |
| `ellipticity` | system | * | both | not_given_by_source | — | |
| `heterogeneity` | dataset | * | both | not_given_by_source | — | "plus updates" values not documented |

   - The registry entry `gc_distance_hb` gives each cause's effect from F1. The calibration terms move g_obs ∝ 1/D only; reddening moves both.
   - `x_gc_baumgardt_vt_scatter_mag` is a new measurements extension column. It is assigned from each cluster's Harris V_t by the three ranges of BSH20 (V < 8; 8–11; > 11).

### C. Structure and flags

8. **Plotting.** As v1, plus the effects of rules 1 and 2. D-096 alternatives are `plotted = false`, `not_plotted_reason = alternative_value`. MW-PAL1 stays recorded, not plotted (D-046).
9. **Named items v1 omitted.**
   - A per-row extension column `x_gc_baumgardt_binary_screening` records BH18's stated multi-epoch screening, "less than 5% probability" (D-025).
   - The registry corrections of F7: the KM09 table is `tab:pred` in arXiv v1; MvdM's R_h is in Table 11.
10. **Descriptor.** `standard_version` `2.5.0`; `x_value_change_ruling` `D-096` if item 3 lists any row; other fields as v1, updated.
11. **Second reading (D-031 item 3).** An independent reader, with no access to the conversion code or the v2 tables, records, for every cluster:
    - **D-096 fields:** whether its dispersion source (BH18, B17, B19, K18 or the integral-field papers, as listed on `veldis.html`), its structure source (MvdM 2005) or Harris 2010 marks a preferred value or excludes data, with quote and location;
    - **D-097 field:** every statement in those sources about equilibrium, binding or tides, classified as a "finding" or a "possibility", with the quote;
    - the bins dropped under rule 1.
    - **Pass:** the package matches the reading. Disagreements are resolved at source; one resolved against the package is a fail.
    - The counts of D-096 changes and D-097 exclusions are published with the result.
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
