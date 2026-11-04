# aeg-d-gc-baumgardt/v2: reproduction test (draft; frozen on merge, before conversion)

**Status: draft, revision 3, for JvH's approval.**
- Revision 2 answered review 1 (`docs/sources/readings/step-d-2026-11-04/gc-review-1.md`) and applied D-098.
- Revision 3 answers review 2 (`gc-review-2.md`) and applies D-099 and standard 2.5.1.
- Written 2026-11-04, before `convert.py` for v2 exists. No v2 value has been computed.
- On merge, this file's SHA-256 goes into `v2/sources.json`, and the file is not edited after merge.
- If the test fails, v2 does not ship and the failure is published. The test is not changed to pass (operating rule 5; D-005).

**Depends on:**
- data standard 2.5.1 (D-099 rule 1: extension columns may hold §7a sizes and formula inputs);
- D-087 (`model_dependence`);
- D-096 (defer to the source's stated choices);
- D-097 (when D-025 excludes a system);
- D-098 (D-096 rule 2 applies only to the same data points; three classes; NGC 2298 and Pal 5);
- D-099 (the classes made mechanical; the distance source that counts; Harris's dynamical-parallax anchors). D-099 must be merged before this test.

## Purpose

v2 re-issues `aeg-d-gc-baumgardt/v1` (standard 2.0.0) under standard 2.5.1 (D-083, D-084). It:
- adds the uncertainty terms read at source in step A (`docs/sources/readings/step-a-2026-11-04/gc-adjudication.md`, "the adjudication");
- applies D-087, D-096, D-097, D-098 and D-099 to every cluster;
- corrects the registry locations found in step A (adjudication F7).

**Values change only where D-096 requires it,** and each change is listed with its source quotation. v2 then sets `x_value_change_ruling = D-096`.

**What carries over:** v1 stays published and unchanged. D-046 (Pal 1, the failed King-fit test) and D-047 (Harris-only clusters recorded, not plotted) carry over unchanged.

## Rules applied

1. **D-096 rule 2, excluded data (as clarified by D-098 rule 1).** It changes a value only where the Atlas computes from the data points the source excluded.
   - **NGC 6715 (M54).** Baumgardt 2017 (B17; arXiv 1609.08794v1, l. 586–589): "We have therefore neglected all data points beyond 200'' in the dynamical analysis of this cluster", because the sample "includes stars from the Sagittarius dwarf galaxy". The cut is a radius, so it carries over to v1's binning. It is a ruled input (D-098 rule 1).
   - **How the cut is applied.**
     - v1 stores each line-of-sight bin's mean radius ⟨r⟩ (`x_gc_baumgardt_r_arcsec`), not its star radii.
     - v2 drops every M54 bin of the RV code with ⟨r⟩ > 200″. On v1's bins these are the bins at 269.01″, 410.12″ and 679.1″, leaving 13 of 16.
     - Since only ⟨r⟩ is stored, two bins may straddle 200″. The bin at 170.92″ may hold stars beyond 200″; it is kept, and they cannot be removed. The bin at 269.01″ may hold stars inside 200″; it is dropped, and they are lost.
     - The row's note and a known issue (item 9) say so.
   - **Re-inference is expected.** v1's code (`aeg.dispersion`) infers bin edges from the remaining radii. The outer edge of the 170.92″ bin therefore moves inward, and the light weights of all 13 bins change. This is part of the change, not a separate one.
   - **NGC 2298 and Pal 5 are not D-096 changes** (D-098 rule 1). BH18 dropped the outermost point of its own 2018 profiles. v1 uses the updated `veldis.html` bins, which are different, and in which σ falls outward. Their values are not changed; their plotting is (rule 2).
   - **After the M54 cut,** D-036's coverage rule (≥ 0.80) and the ≥ 2-bin rule apply as usual. If M54 then fails, its row stays, with `plotted = false` and `not_plotted_reason = coverage_below_threshold`.
2. **D-097, with the classes of D-098 rule 2 and D-099 rule 4.** A statement is classed by its wording, about the system's state:
   - **possibility:** the state is hedged with "may", "might", "could", "possibly" or "perhaps";
   - **finding:** any other statement or conclusion, in the source's own words or by citing others, that the system is out of equilibrium, unbound, being tidally disrupted or tidally disturbed. It includes "likely", "unlikely to be", "suggest", "support" and "consistent with";
   - **neither:** tidal tails, stripping, extension or mass loss mentioned on their own.
   - **Several statements:** any finding in any source that counts makes the system a finding (D-099 rule 4).
   - **Sources that count** (D-098 rule 3; D-099 rule 2):
     - the system's dispersion source as used. For the RV code (pooled data) these are the re-analysis papers behind it (B17, BH18, B19), not the pooled literature papers;
     - its structure original, McLaughlin & van der Marel 2005 (MvdM);
     - its distance source, Harris 2010, the source the Atlas takes the value from. The papers behind the compilation are not sources that count.
   - **NGC 2298 and Pal 5 are findings by ruling** (D-098 rule 4; D-099 rule 4). BH18 (arXiv 1804.08359v2, l. 226–227): "NGC~2298 and Pal~5 have velocity dispersion profiles which increase towards the outer parts, which could be due to the ongoing tidal disruption of these clusters". "Could" hedges the link to the profile; the disruption is stated as ongoing. The second reading confirms this at source (item 11).
   - **What an excluded system's rows get.** The excluded systems are NGC 2298, Pal 5 and any further finding the frozen reading lists. Every row of an excluded system gets:
     - `plotted = false`;
     - `role = alternative` and `alternative_of` empty, by v1's convention (`convert.py` l. 250: `is_default = (s.default is c and s.plotted)`);
     - `not_plotted_reason = other` on rows that v1 plotted. Rows already unplotted keep v1's reason;
     - in `notes`, the quotation with its location and "D-097 finding (D-098, D-099)".

     Their values are unchanged.
   - **Any possibility** stays plotted, with the quotation in `notes`.
   - **The exclusion register.** Every excluded system has exactly one row in `data/registry/excluded.csv`, with the columns that standard §5 names: `system` (the `system_id`), `dataset` (`aeg-d-gc-baumgardt/v2`), `reason` ("D-097 finding (D-098, D-099): " followed by the quotation) and `citation` (paper, arXiv version, file and line). The file is created if it does not exist.
3. **D-087.** `model_dependence` is `none` on every row; v1 has `observable_form` on every row.
   - All 79 rows come from binned profiles. Refused and fitted candidates never became rows.
   - The King (1966) light profiles interpolate well-sampled surface-brightness data and are used only as weights.
4. **D-096 rule 1** (preferred values) and **rule 3** (fiducial baselines) are applied wherever the frozen reading finds them, and only there.
5. **D-099 rule 3, Harris's dynamical-parallax anchors.**
   - Harris (2010, arXiv 1012.3224v1, `Harris.tex` l. 125–127) builds its M_V(HB) calibration partly from "dynamical parallax from combined solutions to radial velocity and proper motion dispersions (Rees 1996; McLaughlin et al.~2006; van de Ven et al.~2006; van den Bosch et al.~2006)".
   - Harris does not name the clusters. The second reader identifies them at source, from those four papers (item 11).
   - Each such cluster's rows carry that quotation in `notes`, with "D-036 #6 not triggered (D-099 rule 3)". Nothing else changes.

## Order of work (against steering)

1. **Exclusion display.** Before the first v2 conversion run, a separate site pull request makes system pages show the rows of `data/registry/excluded.csv`: the reason with its quotation, and the citation.
2. **The second reading.**
   - The second reader (item 11) completes the reading before the first v2 conversion run.
   - The reader has no access to v1's g values, `convert.py` or any v2 table.
   - The reading is written to three files in `v2/reading/`:
     - `d096_d097.csv`: D-096 and D-097 fields, and the D-099 rule 3 anchors;
     - `err_levels.csv`: confidence levels per dispersion dataset code;
     - `binary_screening.csv`: the screening value per dispersion dataset code.
3. **Ruled outcomes in the reading files.** The outcomes of D-098 and D-099 are written into `d096_d097.csv` as ruled inputs, marked `ruled`:
   - the M54 cut (> 200″, the three bins listed in rule 1);
   - NGC 2298 and Pal 5 as findings.

   If the reader disagrees with one, the dissent is recorded in `v2/reading/resolutions.md` and reported to JvH before conversion. The ruled value stays in the file unless JvH rules otherwise.
4. **Other disagreements** between the reading and this test's expectations are resolved at source, before conversion. They are resolved by a session with no access to v1's g values or any v2 value. Each resolution is recorded in `resolutions.md`, and the reading files are updated to match.
5. **Freezing the reading.** The SHA-256 of the four files goes into `data/frozen/gc-v2-reading.json`, by a pull request merged before the first conversion run.
6. **Conversion.** `convert.py` applies changes, exclusions, levels, notes and screening values **only** from the frozen reading files. It contains no system-specific rule of its own.

## The test

Applied to the v2 tables, with v1 at commit `5dc4091` as the reference.
- **"Changed rows"** are the rows the frozen reading lists under D-096. Expected: the M54 row, `m000067`.
- **"Excluded systems"** are the systems it lists as D-097 findings. Expected: NGC 2298 (`aeg-s-000212`, row `m000009`) and Pal 5 (`aeg-s-000322`, row `m000078`).

### A. Values and tables

1. **Rows.** v2 has exactly v1's 79 measurement rows, in v1's order.
   - Row k has v1 row k's `system_id` and `x_gc_baumgardt_dataset`.
   - Row k has the same `measurement_id` apart from the prefix (`v1` → `v2`).
   - Excluded systems keep their rows.
2. **What may change, by table.** Each table is compared with v1's by ID, after the prefix `v1` → `v2` in every ID.
   - **Measurements** (`measurements.ecsv`).
     - **Unchanged values.** On every row that is not a changed row, these are bit-for-bit equal to v1's:
       - `g_obs`, `g_obs_err_lo` and `g_obs_err_hi`;
       - `g_bar`, `g_bar_err_lo`, `g_bar_err_hi` and `g_bar_stars`;
       - `r_kpc`;
       - every v1 `x_gc_baumgardt_*` column.
     - **On changed rows,** these are also unchanged: `g_bar`, `g_bar_err_*`, `g_bar_stars`, `r_kpc`, `x_gc_baumgardt_r_h_pc`, `_l_v`, `_ml_v`, `_ml_v_salpeter` and `_distance_kpc`.
     - **Every other v1 column is unchanged,** except:
       - IDs: the `measurement_id` prefix, and the observable IDs in `observed_from`, `baryonic_from` and `alternative_of`;
       - `model_dependence` (rule 3);
       - on rows of excluded systems: `plotted`, `role`, `alternative_of`, `not_plotted_reason` and `notes` (rule 2);
       - on changed rows: `observed_from` (the dropped bins removed), `notes` (the D-096 note), and the values listed in item 3. If M54 fails coverage, also `plotted`, `role` and `not_plotted_reason`, as rule 1 says;
       - `notes` on rows with a possibility quotation or a D-099 rule 3 anchor note;
       - `flags` and `notes` on rows given `no_uncertainty` by item 6;
       - `assumptions`, which gains the new registry IDs of item 7 on every row;
       - `baryonic_from`, which gains the row's V_t observable ID (item 9).
     - **New columns** are allowed only as listed in items 5, 6, 7 and 9.
   - **Systems** (`systems.ecsv`).
     - **Unchanged:** every v1 column is unchanged, except `properties`.
     - **New column:** `x_gc_baumgardt_ebv_mag` (item 9).
     - **In `properties`, only these keys may change:**
       - for excluded systems: `status` (`recorded`) and `reasons_not_plotted` (the D-097 reason);
       - for M54: `candidates.RV.coverage`, `candidates.RV.n_bins` and `candidates.RV.sigma_rms_km_s`, as recomputed by item 3. If M54 then fails coverage, also `status` and `reasons_not_plotted`.
   - **Observables** (`observables.ecsv`).
     - **Unchanged:** every v1 row keeps every v1 value, except:
       - `err_level` and `err_level_status`, which are added to the `sigma_los` rows (item 5);
       - the R_h, W₀ and r₀ errors, which are unchanged but also copied to item 6's columns.
     - **New rows:** the new `apparent_magnitude` rows (item 9) are appended after `o003182`, numbered on from `o003183` in systems-table order.
     - **No other row is added or removed.**
3. **Changed values.** The changed rows are exactly those of the frozen reading. Each is listed in `REPRODUCTION_RESULT.md` with:
   - the rule of D-096 that changed it;
   - the source quotation and location;
   - the bins dropped (by observable ID and ⟨r⟩);
   - the old and new σ, σ errors, coverage and bin count, and the old and new g_obs and its errors.
   - **Check:** the new σ, its errors, coverage and bin count equal `aeg.dispersion` (v1's frozen code, with `aeg.king66` weights) run on v1's bins minus the dropped bins, to a relative 10⁻⁹.
   - **A change not traceable to the frozen reading is a fail. So is a listed change that is missing.**
4. **Arithmetic.** g_obs and g_bar are recomputed from the stored σ, r½, L_V and Υ_V, by v1's formulas and `astropy.constants.G`. They agree with the stored values to a relative 10⁻⁹ on every row.

### B. Uncertainties (standard 2.5.1 §2a, §3, §7a)

5. **Error columns and confidence levels.**
   - `g_obs_err_*` hold the light-weighted σ error only (point = system, one value per cluster), as in v1. No g_obs point columns are added, because these totals are point-scale only.
   - **`err_level` and `err_level_status` are set per dispersion dataset code,** from `v2/reading/err_levels.csv`. Expected, from step A and review 2:

     | Code | Expected | Basis |
     |---|---|---|
     | RV | `stated`, 0.683 | "the $1\sigma$ upper and lower error bars" (BH18 Table 3 caption, `veldis_tab.tex`). The bounds use B17's likelihood-ratio criterion (adjudication F5). The "plus updates" method is not described |
     | K18 | `stated`, 0.68 | "the 16th and 84th percentiles" (K18 l. 282) |
     | D21 | `stated`, 0.68 | "the interval between the 16-th and 84-th percentile" (D21, arXiv 2105.02246, l. 418) |
     | L13 | `not_given_by_source` | no level stated (Reader A G11) |
     | F13 | `not_given_by_source` | "sigma-clipped standard deviation of these 1,000 velocity dispersions" (F13, arXiv 1304.4176, l. 352): a spread of simulations, not a stated confidence level |
     | L15 | `not_given_by_source` | no level found in step A |

     Where the frozen reading records a level that step A did not find, the reading governs, and the result says so. The same values go on the `sigma_los` observables of each code.
   - **`g_bar_err_*`** hold the population M/L error, as in v1. `g_bar_err_level` = 0.683 and `g_bar_err_level_status = stated`: "The 1{sigma} error in BC/ChD" (MvdM, `J_ApJS_161_304_clusters.vot`, field `e_(M/L)1`).
   - **This error mixes scales:** a dataset-scale age term with a system-scale [Fe/H] term (F6). So:
     - `g_bar_err_point_*` are empty;
     - the term `g_bar_point` records that the source gives no point-scale part;
     - the term `ml_population` records the mixed term (item 7).
6. **New per-row size columns** (measurements extension columns; standard 2.5.1 §12 allows them as §7a sizes). Each is copied from v1's observables or v1's sources without change:
   - `x_gc_baumgardt_log_rh_err_lo`, `_hi` (dex): MvdM's R_h errors, from the `half_light_radius` observable;
   - `x_gc_baumgardt_w0_err_lo`, `_hi`: MvdM's W₀ errors, from the `structural_param` observables;
   - `x_gc_baumgardt_r0_err_lo`, `_hi` (arcsec): MvdM's r₀ errors, from the `structural_param` observables;
   - `x_gc_baumgardt_ml_v_err` (M☉/L☉): the `e_(M/L)1` value, from the `stellar_ml_population` observable;
   - `x_gc_baumgardt_vt_scatter_mag`: 0.22, 0.45 or 0.70 mag by the cluster's Harris V_t.
     - The ranges are BSH20's "V< 8", "8 < V < 11" and "V>11".
     - The Atlas assigns V_t = 8 and V_t = 11 to the middle range.
     - BSH20 does not say whose magnitudes define the ranges; the Atlas uses Harris's V_t.
   - **A row whose source prints no error** gets an empty value in that column, the flag `no_uncertainty`, and the column's name in `notes`.
   - **Each column's header** names the term that uses it (item 7).
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly the rows below.
   - Each cites its source at the location given, in the adjudication or the step A readings.
   - `covariance` is `not_published` on every row.
   - **One sizing rule for every row.** A size is `given` only where the source states it for these systems or for a class that contains them. Otherwise the row is `not_given_by_source`, and any figure the source gives elsewhere goes in the note.
   - **Not uncertainty terms (§2a rule 4):** equilibrium, spherical symmetry and the estimator are assumptions in the registry (`gc_equilibrium`, `gc_rhalf_wolf`), as in v1.

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `half_light_radius` | point | * | both | given | `size_column` `x_gc_baumgardt_log_rh_err_hi` (lower side in `_lo`), dex, `one_sigma` | `gc_rh_measured` | §2a rule 7: g_obs ∝ 1/R_h, g_bar ∝ 1/R_h²; left out of both point columns. MvdM's errors are "χ² within 1 of the global minimum" (l. 2187–2190). Correlated with `king_w0` and `king_r0` (one fit; covariance not published) |
| `king_w0` | system | * | g_obs | given | `size_column` `x_gc_baumgardt_w0_err_hi` (lower in `_lo`), `one_sigma` ("Upper/Lower 1{sigma} error in WO", MvdM models VOT) | — | moves the light weights; effect not computed in v2 |
| `king_r0` | system | * | g_obs | given | `size_column` `x_gc_baumgardt_r0_err_hi` (lower in `_lo`), `one_sigma` | — | as `king_w0` |
| `king_wilson_family` | system | * | both | not_given_by_source | — | — | MvdM: Wilson models are "associated with slightly larger projected half-intensity radii $R_c$ and smaller half-light radii $R_h$" (l. 2703–2705); no size stated for Galactic clusters |
| `centre_position` | system | * | g_obs | not_given_by_source | — | — | Harris: centres "uncertain to typically 1-2 arcseconds" (l. 94); effect on σ not stated |
| `distance_hb_zero_point` | dataset | * | g_obs | given | 0.049 mag, `as_released` | `gc_distance_hb` | Harris 2010 l. 148; Harris does not say what its ± means. R_Sun and L_V move together, so g_bar is unchanged (F1). Correlated with `distance_hb_slope` (one fit; correlation not published). The calibration includes dynamical parallaxes (l. 125–127); D-036 #6 is not triggered (D-099 rule 3; rule 5) |
| `distance_hb_slope` | dataset | * | g_obs | given | 0.033 mag per dex of [Fe/H], `as_released` | `gc_distance_hb_slope` | Harris 2010 l. 148; the shift in M_V(HB) is the slope change × `metallicity_feh`. Correlated with `distance_hb_zero_point` |
| `distance_hb_scatter` | system | * | g_obs | given | 0.11 mag, `as_released` | `gc_distance_hb` | Harris 2010 l. 152, the rms about the calibration |
| `reddening` | system | * | both | given_by_other_source | 0.10 (fraction of E(B−V)), `as_released` | `gc_reddening` | "the average errors on … the reddening (10 %)" (Lützgendorf et al. 2013, l. 489). This is L13's description of Harris (1996), not read at source, applied here to the 2010 edition; the kind of error is not stated. Moves R_Sun only, so g_obs ∝ 1/D and g_bar ∝ 1/D² (F1). Uses each cluster's `x_gc_baumgardt_ebv_mag` (item 9) |
| `extinction_law_rv` | dataset | * | both | not_given_by_source | — | `gc_extinction_rv` | R_V = 3.1 fixed ("$A_V=3.1\,E(B-V)$", MvdM l. 1212 in arXiv astro-ph/0605132v1); no range stated by Harris or MvdM; acts as `reddening` |
| `integrated_magnitude` | system | * | g_bar | given_by_other_source | `size_column` `x_gc_baumgardt_vt_scatter_mag`, `upper_bound` | `gc_luminosity_vt` | BSH20 (arXiv 2009.09611v1, `paper.tex`, Table `tab:comp`, l. 266): the "standard deviation around the mean" of the differences from Harris (2010). It bounds the Harris error from above only because BSH20 calls the estimates "more or less independent of each other" (l. 254). It excludes the mean offsets (+0.03, +0.01 and −0.25 mag); the −0.25 mag offset for V > 11 is a systematic shift this row does not carry. Moves g_bar only (F1) |
| `solar_magnitude` | dataset | * | g_bar | not_given_by_source | — | — | M_V,⊙ = 4.85 (MvdM) |
| `g_bar_point` | point | * | g_bar | not_given_by_source | — | — | item 5 |
| `ml_population` | system | * | g_bar | given | `size_column` `x_gc_baumgardt_ml_v_err`, `one_sigma` | `gc_ml_scale` | MvdM `e_(M/L)1`. It mixes a dataset-scale age term (13 ± 2 Gyr for every cluster) with a system-scale [Fe/H] term (± 0.2 dex), not split by MvdM (F6). Labelling it `system` is a simplification, and the result says so. It is already inside `g_bar_err_lo/hi`, so it is not added again. As a fraction for `gc_ml_scale`: `x_gc_baumgardt_ml_v_err / x_gc_baumgardt_ml_v` |
| `pop_synthesis_code` | dataset | * | g_bar | given | 0.10 (fraction of Υ_V), `as_released` | `gc_ml_scale` | MvdM l. 1357–1359: "although there are some exceptions, these differences are generally slight: at the level of … $\la 10\%$ in $\Upsilon_V$". The hedge means this is not an upper bound |
| `stellar_ml` | dataset | * | g_bar | given | `size_column` `x_gc_baumgardt_ml_v_salpeter` (upper end), `range` | `gc_stellar_ml` | The registry range. Upper end: each cluster's Salpeter value, in the column. Lower end: 0.53 × `x_gc_baumgardt_ml_v`, from the registry's `range_basis.min` (Kruijssen & Mieske 2009; D-039), not from a column. MvdM's models build in about 30 % mass loss (MvdM Fig. 4); MvdM used Harris (1996) [Fe/H] (F8) |
| `estimator_normalisation` | dataset | * | g_obs | not_given_by_source | — | — | Wolf et al. 2010 shows "±10% variation about the predicted relation" (l. 927) as guide lines in a figure for classical dwarf spheroidals, not as a stated accuracy; none is stated for clusters |
| `anisotropy_profile` | dataset | * | g_obs | not_given_by_source | — | — | Wolf l. 966–976 gives 0.05 dex "in cases where extended kinematics are not available", from the dEs and Es, "to allow for a range of $\beta$ profiles". These rows have ≥ 80 % light coverage, so the condition does not describe them |
| `deprojection_4_3` | dataset | * | both | given | 0.02, `upper_bound` | `gc_rhalf_wolf` | Wolf: "$\rhalf/\Rhalf \simeq 4/3$ is accurate to better than 2\% for most surface brightness profiles used to describe observed stellar systems" (l. 1829); for King (1962) profiles, l. 1814–1818. v1 uses King (1966) (F8). An assumption with a stated accuracy (§2a rule 4) |
| `light_weighting` | dataset | * | g_obs | not_given_by_source | — | — | bins covering ≥ 80 % of the light, against Wolf's whole-system average (F8) |
| `binaries` | system | * | g_obs | not_given_by_source | — | — | BH18 names Pal 13, Arp 2 and Ter 3 as possibly inflated (l. 228–233). K18 gives +0.3 and +0.6 km/s for binary fractions of 5 % and 10 % in its own NGC 6121 data (l. 330), not for these profiles |
| `membership_contamination` | system | * | g_obs | not_given_by_source | — | — | non-members "removed iteratively" (BH18 l. 206) |
| `rotation` | system | * | g_obs | not_given_by_source | — | — | |
| `tracer_mass` | system | * | g_obs | not_given_by_source | — | — | K18 states "≲5%" in σ between its main-sequence samples and literature giant profiles, for NGC 3201 and NGC 6121 only (l. 344). The RV code is mostly giants (BH18 l. 185) |
| `rv_zero_points` | system | * | g_obs | not_given_by_source | — | — | shifts "usually less than 1 km/sec" (BH18 l. 199); effect on σ not stated |
| `ellipticity` | system | * | both | not_given_by_source | — | — | |
| `heterogeneity` | dataset | * | both | not_given_by_source | — | — | the "plus updates" values are not documented; they differ slightly from BH18's printed table (F8) |

   - **Registry update for v2** (`data/assumptions.json`). Every `gc_*` entry gains an `aeg-d-gc-baumgardt/v2` dataset entry; v1's entries stay as published. Where an entry below has effects, its v2 default is numeric. The formula leaves every value unchanged at the default and depends on one cause only. In the formulas, `E` stands for `system.x_gc_baumgardt_ebv_mag` and `[Fe/H]` for `system.metallicity_feh`.
     - **Unchanged except for the v2 entry:** `gc_equilibrium`, `gc_light_model` and `gc_gas_absent`. Their v1 defaults are kept, with no effects.
     - **`gc_distance_hb`.**
       - p = the shift in M_V(HB), in mag; default 0.
       - g_obs, `g_obs_err_lo` and `g_obs_err_hi` × 10^(0.2 (p − p0)).
       - g_bar is unchanged.
       - Used by `distance_hb_zero_point` and `distance_hb_scatter`.
       - It gains the F7 locations.
     - **`gc_distance_hb_slope` (new).** p = the change in the calibration slope, in mag per dex; default 0. The same columns × 10^(0.2 (p − p0) [Fe/H]).
     - **`gc_reddening` (new).**
       - p = the fractional change in E(B−V); default 0. With A_V = 3.1 E(B−V) (MvdM l. 1212), Δμ₀ = −3.1 (p − p0) E.
       - g_obs and its errors × 10^(0.62 (p − p0) E).
       - g_bar, `g_bar_stars` and `g_bar_err_*` × 10^(1.24 (p − p0) E).
     - **`gc_extinction_rv` (new).**
       - p = R_V; default 3.1. Δμ₀ = −(p − p0) E.
       - g_obs and its errors × 10^(0.2 (p − p0) E).
       - g_bar, `g_bar_stars` and `g_bar_err_*` × 10^(0.4 (p − p0) E).
     - **`gc_rh_measured` (new).**
       - p = the shift in log₁₀ R_h, in dex; default 0.
       - g_obs and its errors × 10^(−(p − p0)).
       - g_bar, `g_bar_stars` and `g_bar_err_*` × 10^(−2 (p − p0)).
     - **`gc_rhalf_wolf`.**
       - p = r½/R_h; v2 default 1.3333333333333333 (the 4/3 of v1, made numeric).
       - g_obs and its errors × p0/p.
       - g_bar, `g_bar_stars` and `g_bar_err_*` × (p0/p)^2.
     - **`gc_luminosity_vt` (new).**
       - Role `baryonic_inference`: L_V from Harris V_t.
       - p = the shift in V_t, in mag; default 0.
       - g_bar, `g_bar_stars` and `g_bar_err_*` × 10^(−0.4 (p − p0)).
     - **`gc_ml_scale` (new).**
       - p = the fractional change in Υ_V; default 0.
       - g_bar, `g_bar_stars` and `g_bar_err_*` × (1 + p)/(1 + p0).
     - **`gc_stellar_ml`.** v1's range slider and formulas are carried over unchanged. It gains the F7 correction: KM09's table is `tab:pred` in arXiv v1.
     - **Not sliders.** Only `gc_stellar_ml` is `adjustable`, as in v1. Making any other entry a slider needs a ruling.
   - **Check (part of this item).** For every `gc_*` v2 entry with effects:
     - every formula parses;
     - it names only `p`, `p0`, existing row columns or `system.<column>`;
     - evaluated at p = p0 on every v2 row, it leaves every affected column unchanged to a relative 10⁻¹².
   - **Second reading of term sizes.** Step A's two concordant readings serve as the D-031 second reading for the sizes in this table.

### C. Structure and flags

8. **Plotting.**
   - Plotting is as v1, plus rule 1's effect on M54 and rule 2's exclusions.
   - D-096 alternatives found by the reading are `plotted = false`, with `not_plotted_reason = alternative_value`.
   - MW-PAL1 stays recorded, not plotted (D-046).
   - **Notes:**
     - every row of an excluded system has its quotation in `notes`;
     - every possibility in the frozen reading has its quotation in that system's rows' `notes`.
   - **Exclusion register:** `data/registry/excluded.csv` has exactly one row per excluded system of this dataset, with the columns of rule 2.
   - **Site check, mechanical.** In the built site, the HTML of each excluded system's page contains its quotation and the citation, as stored in `excluded.csv`. The search is for exact text, after HTML entities are decoded and whitespace is collapsed.
   - **Counts published with the result:**
     - rows changed under D-096;
     - systems excluded under D-097;
     - possibilities recorded;
     - rows with a D-099 rule 3 anchor note.
9. **Named items v1 omitted.**
   - **Binary screening flag.** A per-row extension column `x_gc_baumgardt_binary_screening`, a closed list, set per dispersion dataset code from `v2/reading/binary_screening.csv`:
     - `multi_epoch_stated`: the source states that stars with multiple velocities are tested and removed. Expected for RV: "Stars where the individual measurements had a less than 5\% probability to be compatible with a constant radial velocity were removed" (BH18 l. 203–204). This applies only to stars with more than one measurement; the note says so.
     - `integrated_light`: the dispersion comes from integrated-light spectra, where screening of individual stars does not apply.
     - `not_stated`: otherwise.
   - **New observables,** from `mwgc.dat` (Harris 2010), for every system with a measurement row: `apparent_magnitude` (V_t, band V). It is used by `integrated_magnitude`, to assign `x_gc_baumgardt_vt_scatter_mag`, and as an input to L_V. So its ID joins each row's `baryonic_from`.
   - **E(B−V).** It has no §4a quantity, so it goes in a systems extension column, `x_gc_baumgardt_ebv_mag` (mag), from `mwgc.dat`. The column's header names Harris 2010 and the `gc_reddening` and `gc_extinction_rv` formulas that read it.
   - **Registry corrections (F7):**
     - the KM09 table is `tab:pred` in arXiv v1;
     - MvdM's R_h is in Table 11 (`tab:struc`), and W₀ and r₀ are in Table 10.
   - **Sources.** `v2/sources.json` lists every v1 source still used, and adds BSH20:
     - arXiv 2009.09611v1, e-print SHA-256 `0e1a2b34d587ba8dacfc0ddd243e534ac15e22c3ea4b72d0606b0340dcf636b2` (as read in step A by Reader B);
     - its licence as stated on its arXiv listing at retrieval;
     - `redistributable` set from that licence.
   - **Known issues.** One exists, linked from the dataset page, for each of:
     - the M54 bins that may straddle 200″ (170.92″ and 269.01″; rule 1);
     - the Harris calibration's dynamical-parallax anchors and D-099 rule 3.
10. **Descriptor.**
    - `standard_version` is `2.5.1`.
    - `x_value_change_ruling` is `D-096` if item 3 lists any row.
    - Other fields are as v1, updated.
    - `x_second_reading` points to `SECOND_READING.md` and the four frozen reading files.
11. **Second reading (D-031 item 3).** An independent reader works without access to `convert.py`, v1's g values or any v2 table. For every cluster with a measurement row, the reader records:
    - **D-096 fields:** whether its dispersion source, its structure source (MvdM) or Harris 2010 marks a preferred value, excludes data, or names a fiducial baseline, with quote and location. For an exclusion: whether the Atlas computes from the same data points (D-098 rule 1), and if so, which v1 bins (by observable ID and ⟨r⟩) are dropped.
    - **D-097 field:** every statement in the sources that count (rule 2) about equilibrium, binding or tides. Each is classed under rule 2 as finding, possibility or neither, with the quote and location. The ruled findings (NGC 2298, Pal 5) are confirmed at source.
    - **D-099 rule 3 anchors:** the clusters whose dynamical parallaxes the four papers cited at Harris l. 125–127 give, read at source in those papers.
    - **Confidence levels:** for each dispersion dataset code, the level as printed, with quote and location (item 5), in `err_levels.csv`.
    - **Binary screening:** the value for each dispersion dataset code (item 9), in `binary_screening.csv`.
    - **Pass:** the package equals the frozen reading files on every field they hold. Any mismatch is a fail.
12. **Standard and site.**
    - `python -m aeg.validate data/packages/aeg-d-gc-baumgardt/v2` passes under 2.5.1;
    - the site builds;
    - `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes.
13. **v1 untouched.** Every file in `aeg-d-gc-baumgardt/v1/` has the checksum it had at commit `5dc4091`.

**Pass** = all thirteen hold. Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right.
- v1's test 2 result (FAIL, Pal 1; D-046). It stands for v1 and is not re-run.
- MvdM's use of Harris (1996) [Fe/H] behind M/L₁ (F8). It is stated in the `stellar_ml` term's note.
- Statements in the pooled literature RV papers and in the papers behind Harris 2010. These are not sources that count (D-098 rule 3; D-099 rule 2).
