# aeg-d-strong-lensing/v2: reproduction test (draft; frozen on merge, before conversion)

**Status: draft, revision 3, for JvH's approval.**
- Revision 2 answered review 1 (`docs/sources/readings/step-d-2026-11-05/lenses-review-1.md`): all eleven errors and the weaknesses.
- Revision 3 answers review 2 (`lenses-review-2.md`): all ten errors and the weaknesses. Where a fix needed a call within D-094 and D-104, the text says "applying D-094/D-104".
- Written 2026-11-05, before `convert.py` for v2 exists. No v2 value has been computed, and no g value of v1 was opened to write it.
- On merge, this file's SHA-256 goes into `data/frozen/lenses-v2-test.json`, and the file is not edited after merge.
- If the test fails, v2 does not ship and the failure is published. The test is not changed to pass (operating rule 5; D-005).

**Depends on:**
- data standard 2.5.1 (§2a rule 7, from D-093; §12 as clarified by D-099 rule 1);
- D-064 item 4 as replaced by D-094 (distance enters at first order, g_obs/g_bar ∝ 1/D);
- D-087 (`model_dependence`);
- D-096 and D-098 rule 1 (defer to the source's stated choices; exclusions only for the same data points);
- the frozen precedence rule `docs/methods/A6S_PRECEDENCE.md` (D-065) and the rulings D-066, D-075 and D-076, which v1 applied;
- **D-104 (ruled 2026-11-05 07:05 MDT):** the distance sizes are H0 values, not α shifts (rule 6); the central black hole is not in g_bar (item 9); the θ_E effect is not computed where no light profile is printed (rule 5).

## Purpose

v2 re-issues `aeg-d-strong-lensing/v1` (standard 2.1.0) under standard 2.5.1 (D-083, D-084). It:
- adds the uncertainty terms read at source in step A (`docs/sources/readings/step-a-2026-11-04/lenses-adjudication.md`, "the adjudication"; readers A and B in the same folder);
- moves the Einstein-radius error to the side whose value it changes (adjudication F1; §2a rule 7);
- adds distance (H0, peculiar velocity, redshift frame) as a term on g_obs (F2; D-094);
- carries the shared MaNGA Υ_ref as one term shared by the two lenses (F4);
- records NGC 6505's lower-bound errors (F5).

**No value changes, unless the frozen second reading finds a D-096 case** (rules below). Error columns change only where this test says so. v1 stays published and unchanged.

## Rules applied

1. **D-096 rule 1 (preferred values) and rule 3 (fiducial baselines).**
   - The defaults of v1 were fixed by D-065, D-075 and D-076 before any value was read.
   - The second reading records, for every source used (R5, R13, R10, R9, R20, R21, R25, R26, R27, R28, R29, R30, R32, R61), whether it marks a preferred value or names a fiducial baseline among the values it prints, with quote and location. R27 (Collier et al. 2020) supplies J0403−0239's alternative θ_E and redshift observables and is newer than R29, so a preference stated there could change a default.
   - **Known candidate:** NGC 6505. R30 prints a spectroscopic lens redshift, z = 0.04243 (ms.tex l. 639), and a cosmological redshift, z = 0.041 ± 0.001, after a bulk-flow and peculiar-velocity correction (l. 790). v1 uses 0.04243 as the default and 0.041 as an alternative row. The reading records whether R30 states which one it uses for distances.
   - **Any such preference that differs from a v1 default, or conflicts with D-065, D-075 or D-076, goes to JvH before the first conversion run.** It is never decided after conversion. A value change then sets `x_value_change_ruling = D-096` (standard 2.4.0 §9).
   - Expected: no change.
2. **D-096 rule 2 (excluded data), as limited by D-098 rule 1.** It applies only where the Atlas computes from data points the source excluded. The Atlas computes nothing from per-object data here except M_E from θ_E (SLACS, SL2S) and M*(<R_E) from a printed total and light profile. The reading records any exclusion the sources state for those inputs. Expected: none.
3. **D-097 does not apply.** D-025, which D-097 implements, governs g_obs from a velocity dispersion. Lensing g_obs uses no dispersion and no equilibrium assumption: it rests on `a6s_gr_lensing` and `a6s_projected_cylinder`. Statements about a lens's dynamical state are recorded by the reader in a `note` only, and change nothing.
4. **D-087.** `model_dependence` is unchanged from v1:
   - `total_mass_form` on SNL-1, SNL-2 and J0403−0239, where the half-image-separation (SIS) approximation stands in for a full lens model;
   - `none` elsewhere.

   The reading confirms that the three rows are exactly those whose observed side is a half-image-separation estimate.
5. **§2a rule 7: the Einstein-radius error.**
   - **Where the source's M_E is the mass inside the Einstein radius, with mean convergence 1** (M_E = π Σ_cr R_E²), g_obs = G M_E / R_E² = π G Σ_cr. That depends on the redshifts and the cosmology only, not on θ_E. So a θ_E error does not move g_obs. It moves R_E, and with it g_bar = G M*(<R_E) / R_E², through the radius and through the aperture of M*.
   - **The class applies to every row of a system, alternatives included.** Expected rows of this kind ("class A"), 107 in all:
     - SLACS: 96 rows (48 defaults, 48 alternatives); M_E computed from R5's θ_E;
     - SL2S: 6 rows (2 defaults, 4 alternatives); computed from R20's θ_E;
     - MaNGA J1436+4943 and J1701+3722: 2 rows. R32 prints M_E and θ_E, and the error is the θ_E error: "the error reflecting the variation between models" (main.tex l. 176) and "we impose a 10 per cent error on θ_Ein" (l. 261);
     - NGC 6505: 2 rows (R30; θ_E error stated as a lower bound, l. 798, l. 813; M_E printed without error);
     - J0403−0239: 1 row. R29 adopts "R_Ein as half of the image separation, 1.47 ± 0.03 arcsec" (newlens.tex l. 196) and computes M_Ein "using the symmetric lens equation" (l. 210), which is the mass at mean convergence 1. Its "2 per cent uncertainty dominated by the measurement of R_Ein" (l. 210) is that θ_E error. The further 3 % that "a small ellipticity … increases the mass by" (l. 210) changes M_E at a fixed radius, so it stays on g_obs as its own term (`ellipticity_j0403`, item 7). Nothing is subtracted in quadrature.
   - **Rows where the printed M_E error is not a θ_E error ("class B")** keep it on g_obs, as in v1, and get no separate θ_E term, so nothing is counted twice:
     - SNL-0: the 4 % reflects "the difference between SIS- and MFL-model masses" (R28 lensz_arXiv.tex l. 317–325), and θ_E (2.85″) has no printed error.
   - **Rows where θ_E has no printed error:** S4TM (37 rows; R10 prints neither a θ_E nor an M_E error). R9's 0.5 % was derived for R9's own fits of the SLACS grade-A lenses as a scatter against R5 (ms_v2.tex l. 138), not for R10's models, so under the sizing rule it goes in the note.
   - **SNL-1 and SNL-2** use a mass inside the aperture R_ap (R61 Table 2), which has no printed error. Rule 7 does not apply (its "no error of its own" clause). Their printed mass errors stay on g_obs.
   - **The θ_E effect needs the light profile of M*(<R_E)** (item 6). A **printed profile** means one single-component Sérsic or de Vaucouleurs profile whose R_e and n (n = 4 for de Vaucouleurs) the source prints for that lens. A multi-component fit (for example R30's several Sérsic components, l. 656), or a profile without a printed R_e, counts as "none printed" here. Where the source prints no profile, see "Where no profile is printed" below.
   - **The reading decides each row's class at source:** whether the source defines M_E as the mass inside the radius of mean convergence 1, and whether its stated error is a θ_E error alone. Where the reading differs from the expectation above, the reading governs, and the result says so.
   - **Where no profile is printed (D-104 rule 3).** Where `profiles.csv` records "none printed" for a class A row, `x_strong_lensing_dlngbar_dlntheta` is empty and the θ_E effect on g_bar is not computed in v2. `x_strong_lensing_theta_e_err_frac_lo/hi` stay filled with the stated error. The dataset page and the row's view say "θ_E error stated; effect on g_bar not computed". This adds no assumption.
     - Expected scope: the two MaNGA rows (R32 prints θ_Eff but no profile form), NGC 6505 (R30 describes a "complex and varying isophotal structure" fitted with several Sérsic components) and J0403−0239 (the reading decides).
     - A registered de Vaucouleurs profile is rejected: it would contradict R30 and is not stated by R32.
     - **A later option, needing a ruling:** since d ln M*(<R)/d ln R = 2 Σ(R)/Σ̄(<R), the exponent lies in [−2, 0] with no profile at all, provided the surface density does not rise outward at R_E. It is not used in v2.
6. **Distance (D-094; sizes by D-104 rule 1).** Distance moves g_obs at first order. The stellar g_bar is distance-free at fixed Ω_m: M* ∝ D_L², R_E² ∝ D_A², and both scale as H0⁻².
   - **H0** enters exactly: g_obs ∝ H0 (all distances ∝ 1/H0 at fixed Ω_m), with R_E ∝ 1/H0 and g_bar unchanged. The formula is the corrected registry entry `a6s_source_cosmology` (item 7). **H0 terms are sized in the parameter's own unit (km s⁻¹ Mpc⁻¹)**, as the pair of H0 values the source names: its adopted H0 and the alternative it tests. The term's p comes from that pair alone, p = H0_alt / H0_adopted (item 7); no row column enters it (applying D-094/D-104).
     - **Where the source names a paper instead of printing a number** (D-075 item 4), the value is that paper's headline H0 as printed in its abstract. These were read at source for this revision (arXiv abstract pages, hashes in item 9) and are written into the terms table:
       - Planck Collaboration 2016 (A&A 594, A13; arXiv 1502.01589, "Planck 2015 results. XIII"): "H0= (67.8 +/- 0.9) km/s/Mpc";
       - Planck Collaboration 2018 (arXiv 1807.06209): "Hubble constant $H_0 = (67.4\pm 0.5)$km/s/Mpc";
       - Bennett et al. 2014 (ApJ 794, 135; arXiv 1406.1718): "a best-fit Hubble constant of 69.6+/-0.7 km/s/Mpc".
     - The exact formula then gives the effect.
     - The source's percentage is a shift in α, the ratio (M_Ein − M_DM)/(Υ_ref L_Ein) (R29 l. 206; R32 l. 288; R25 l. 613), which subtracts a modelled mass (M_DM in the source's notation). It is recorded in the term's note, labelled as α, and is not applied to g_obs.
   - **Peculiar velocity and the redshift frame** enter through the lens distance D_l. The formula `a6s_lens_distance` (item 7) uses p, the fractional change in D_l: g_obs ∝ 1/D_l and r ∝ D_l, with g_bar unchanged. g_obs = π G Σ_cr ∝ D_s / (D_l D_ls) is close to 1/D_l only when D_s ≫ D_l; that holds for the systems sized here (SNELLS, NGC 6505), and the note says so. **The only size used as a g_obs size is R26's**: "The lensing M/L is proportional to distance … we include an uncertainty corresponding to a 500 km s⁻¹ peculiar velocity (3-4%)" (snells.tex l. 139), stated for the SNELLS lenses. Because R26 states the M/L as proportional to distance, its 3–4 % is the fractional distance change. It is applied as a shift of ±size_hi (±4 %) in D_l; the source states 3–4 %, and `size_lo` records the lower end (applying D-094/D-104). R25's "shifts of up to 5 per cent in α" (snellsI_arxiv.tex l. 864) is an α shift and goes in the note only.
   - This clarifies the sizes listed in D-094 rule 2; it does not reverse D-094.

## Order of work (against steering)

1. **The second reading** (item 11) is completed before the first v2 conversion run, by a reader with no access to v1's g values, `convert.py` or any v2 table. It writes to `v2/reading/`:
   - `d096.csv`: D-096 fields per source, with quote and location;
   - `theta_class.csv`: per measurement row, the rule 5 class (A, B, no θ_E error, aperture), the fractional θ_E error as printed (lower and upper), and its quote and location;
   - `profiles.csv`: per system with any row whose M*(<R_E) uses a light profile (class A, S4TM, SL2S), the profile the source prints (form, R_e, n, and which paper and table), or "none printed";
   - `err_levels.csv`: per source and side, the confidence level of each error used, as stated, with quote and location;
   - `distance.csv`: per source, the adopted H0 and any alternative H0 it tests, confirming the values written into item 7 (for a named paper, its abstract headline value), and any statement of a peculiar-velocity or redshift-frame effect with its size and the quantity it is stated in (lensing M/L, α, or other);
   - `baryon_inventory.csv`: per source, what it states about a central black hole, gas and dust inside R_E, with quote and location (item 9).
   - `theta_class.csv` also records, for SLACS, whether R13's M*(≤R_E) errors already include the θ_E error (R13 l. 1669–1671 states its 5 % for the lensing masses). If they do, the result says so, and the `theta_e` term's note states the overlap.
2. **Disagreements** with step A, or with this test's expectations, are resolved at source by a session with no access to any g value, and recorded in `v2/reading/resolutions.md`. A conflict under rule 1 goes to JvH.
3. **Freezing the reading.** The SHA-256 of every reading file goes into `data/frozen/lenses-v2-reading.json`, by a pull request merged before the first conversion run.
4. **Conversion.** `convert.py` takes D-096 changes, θ_E classes and sizes, profiles, confidence levels, distance sizes and inventory statements **only** from the frozen reading files. It contains no system-specific rule of its own. It reuses v1's frozen code (`aeg.lensing`, frozen with v1) for every computed quantity.

## The test

Applied to the v2 tables, with v1 at commit `5dc4091` as the reference.

### A. Values and tables

1. **Rows.** v2 has exactly v1's 147 measurement rows (94 defaults, 53 alternatives), in v1's order, and v1's 212 systems. Row k has v1 row k's `system_id`, `role`, `alternative_of` (prefix changed) and `x_strong_lensing_scope`, and the same `measurement_id` apart from the prefix (`v1` → `v2`).
2. **What may change, by table.** Each table is compared with v1's by ID, after the prefix `v1` → `v2` in every ID.
   - **Measurements.**
     - **Bit-for-bit equal to v1 on every row:** `g_obs`, `g_bar`, `g_bar_stars`, `g_bar_gas_cold`, `g_bar_gas_hot`, `r_kpc`, `g_bar_err_lo`, `g_bar_err_hi`, and every v1 `x_strong_lensing_*` column. The only exception is a row changed under rule 1 by ruling.
     - **`g_obs_err_lo` and `g_obs_err_hi`:**
       - on class A rows, empty (rule 5), with the flag `no_uncertainty` as standard §2 requires: no point error is stated for g_obs on these rows. The θ_E error is in the term `theta_e` or `theta_e_ngc6505` (item 7), and the column description says why the cell is empty (§2a rule 7);
       - on every other row, bit-for-bit equal to v1.
     - **Every other v1 column is unchanged,** except:
       - IDs: the `measurement_id` prefix, and the observable IDs in `observed_from`, `baryonic_from` and `alternative_of`;
       - `baryonic_from`, which gains the IDs of the profile observables appended under "Observables" below;
       - `notes` on class A rows ("θ_E error carried by g_bar, standard §2a rule 7; term theta_e"), on rows given a reading note, and on rows where the θ_E effect is not computed (rule 5);
       - `assumptions`, which gains the new registry IDs of item 7 on every row;
       - `flags` on class A rows, which gain `no_uncertainty` where v1 lacks it (NGC 6505's two rows already carry it in v1).
     - **New columns,** and only these:
       - `g_obs_err_point_lo/hi` and `g_bar_err_point_lo/hi` (item 5);
       - `err_level`, `err_level_status`, `g_bar_err_level` and `g_bar_err_level_status` (item 5);
       - the extension columns of item 6.
   - **Systems.** Every v1 column is unchanged, except `properties` where a reading note is added. No new column.
   - **"Systems with rows"** in this test means the 94 systems that carry measurement rows (of v1's 212), in systems-table order.
   - **Observables.** Every v1 row keeps every v1 value, and `err_level` and `err_level_status` are added (item 5). **New rows** are appended after v1's last ID (`o000630`), and only for light-profile inputs that `profiles.csv` records for class A rows and v1 did not already hold as observables (for example R5's de Vaucouleurs R_e for SLACS). Each has `side = baryonic`, the quantity, value, unit and source as read, and is named in the row's `baryonic_from` (D-029). No v1 row is removed.
3. **Changed values.** Expected: none. If the frozen reading lists a D-096 change and JvH has ruled it, each changed row is listed in `REPRODUCTION_RESULT.md` with the rule, the quotation and location, and the old and new values. A change not traceable to the frozen reading and a ruling is a fail. So is a listed change that is missing.
4. **Arithmetic.**
   - M_E (where computed), R_E, f(<R_E), M*(<R_E), g_obs and g_bar are recomputed from the stored inputs by `aeg.lensing` (frozen with v1). They agree with the stored values to a relative 10⁻⁹.
   - The new column `x_strong_lensing_dlngbar_dlntheta` (item 6) is recomputed from the stored profile inputs (v1's `x_strong_lensing_r_eff_arcsec` and `_sersic_n`, or the new `x_strong_lensing_theta_profile_*` columns) and agrees to a relative 10⁻⁶.
   - The new column `x_strong_lensing_g_bar_stars_ref` (item 6) equals `g_obs × x_strong_lensing_mstar_re_msun / x_strong_lensing_m_e_msun` to a relative 10⁻¹².

### B. Uncertainties (standard 2.5.1 §2a, §3, §7a)

5. **Error columns and confidence levels.** One value per lens, so point and system scale coincide (§2a; readers A and B).
   - **`g_obs_err_point_*`** equal `g_obs_err_*` on every row (empty on class A rows).
   - **`g_bar_err_point_*`** equal `g_bar_err_*` on every row except the two MaNGA lenses. There, they hold the L_Ein error alone (R32 Table 2), propagated as v1 does, because v1's `g_bar_err_*` there also contain the shared Υ_ref, which is a dataset-scale term (F4; §2a rule 1). Their header says so (§2a rule 6).
   - **Confidence levels, one rule per row.**
     - `err_level` and `err_level_status` describe `g_obs_err_*`; `g_bar_err_level` and `g_bar_err_level_status` describe `g_bar_err_*`.
     - Where the error column is empty (class A g_obs; S4TM), the level and its status are empty. S4TM keeps v1's flag `no_uncertainty`, as v1.
     - Where the column is filled, the level and status come from `v2/reading/err_levels.csv` for that source and side: `stated` with the level, or `not_given_by_source`. A level is never read as 0.683 by default (D-093 rule 1).
     - The confidence level of a term's size (for example R5's θ_E RMS) goes in that term's note, not in these columns.
   - **Expected, from step A (the reading governs):**

     | Source | Column | Expected | Basis |
     |---|---|---|---|
     | R13 (SLACS M*) | g_bar | `stated`, 0.683 | "The mass estimates (with 1 σ error bars)" (plain.txt l. 2975, figure caption) |
     | R20 (SL2S) | g_obs | empty (class A) | |
     | R20 (SL2S) | g_bar | from the reading | l. 462's "68% credible intervals" is for the lens parameters, not M*; the reading reads R20's M* level at source, or records `not_given_by_source` |
     | R26, R28 (SNL-0) | both | `not_given_by_source` | |
     | R61 (SNL-1, SNL-2) | both | `not_given_by_source` | |
     | R29 (J0403) | g_bar | `not_given_by_source` | |
     | R32 (MaNGA) | g_bar | `not_given_by_source` | the "2σ interval" (main.tex l. 276–277) is for Υ_ref, a dataset term, not for the point error |
     | R30 (NGC 6505) | g_bar | `not_given_by_source` | |

     Where the frozen reading records a level that step A did not find, the reading governs, and the result says so.
6. **New per-row extension columns** (standard 2.5.1 §12). Each header names the term or formula that uses it, and says what an empty value means.
   - `x_strong_lensing_theta_e_err_frac_lo`, `_hi`: the fractional θ_E error on class A rows, from `theta_class.csv`. SLACS: 0.02 both sides, R5's adopted RMS. **Empty on NGC 6505** (its lower bound is the separate term `theta_e_ngc6505`, so nothing is counted twice) and on every row outside class A. `_hi` is named by the term `theta_e`; `_lo` is its companion, as in the globular-cluster `stellar_ml` row (D-099 rule 1 covers the column the term names).
   - `x_strong_lensing_theta_profile_form`, `_r_e_arcsec`, `_n`: the light profile from `profiles.csv`, on rows whose v1 profile columns are empty. Expected for SLACS: R5's printed effective radius and profile form, which the reading confirms at source. Empty where none is printed.
   - `x_strong_lensing_dlngbar_dlntheta`: d ln g_bar / d ln θ_E at fixed redshifts and cosmology, **on every row with a printed profile** (class A, S4TM and SL2S). It equals −2 + d ln f(<R_E)/d ln R_E, from the profile (v1's columns or the new ones), by central difference (step 10⁻⁴ in ln R_E) of the frozen `aeg.lensing.sersic_projected_fraction`. Where M*(<R_E) is L(<R_E) × Υ, the same profile is used for L. Empty where no profile is printed (rule 5).
   - `x_strong_lensing_g_bar_stars_ref`: G M*(<R_E)/R_E² at the source's population, computed as in item 4. It is what the v2 gas formula scales (item 7), so that the gas term no longer reads g_obs.
   - `x_strong_lensing_mass_ellipticity_frac`: 0.03 on J0403−0239 only (R29 l. 210, "increases the mass by 3 per cent"; one-sided, upward); empty elsewhere. Named by `ellipticity_j0403`.
   - `x_strong_lensing_los_frac`: 0.02 on SNL-0 only (R28 l. 320–322); empty elsewhere. Named by `line_of_sight_snl0`.
   - `x_strong_lensing_neighbour_light_frac`: 0.015 on SNL-2 only (R26 l. 141); empty elsewhere. Named by `neighbour_light_snl2`.
   - `x_strong_lensing_r_eff_err_frac`: on SL2S rows, 0.10 where the reading records HST imaging and 0.30 where it records CFHT (R20 l. 354–359); empty elsewhere. Named by `r_eff_sl2s`.
   - **The site reads only the `_hi` column of a pair** (D-099 rule 1 covers the column a term names). An asymmetric θ_E error (SL2S) is therefore shown in views by its upper side; the `_lo` column is in the tables and downloads.
   - **Empty values** mean the source gives no size or no profile. The column header says so; `notes` are not changed for this reason.
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly the rows below.
   - Each cites its source at the location given, verified against the e-prints read in step A.
   - `covariance` is `not_published` on every row.
   - **One sizing rule for every row.** A size is `given` only where the source states it for these systems, or for a class that contains them. Otherwise the row is `not_given_by_source`, and any figure the source gives elsewhere goes in the note. R9's 2 % external-shear figure is `given` for S4TM because R10, the S4TM source, defers to it: "a minor effect as quantified in Shu15" (ms_arxiv_v2.tex l. 308–309). R9's 0.5 % (rule 5) has no such link to R10's models.
   - **`size_unit`** is given on every `given` row: "fraction" for fractional sizes, "dex", "arcsec", "km s-1 Mpc-1", or the unit stated.
   - **`in_error_columns`** is empty on `theta_e` and `theta_e_ngc6505` (§2a rule 7 rows).
   - **Not uncertainty terms (§2a rule 4):** general-relativistic lensing (`a6s_gr_lensing`), the projected cylinder (`a6s_projected_cylinder`) and spectroscopic redshifts (`a6s_redshifts_spectroscopic`) are registry assumptions, as in v1. The central black hole is in the baryon inventory (item 9), not in this table.
   - **`applies_to`.** A survey name below stands for the semicolon list of the `system_id`s of the systems whose rows carry the matching `x_strong_lensing_scope` value: "SLACS" = `SLACS V-modelled lenses`; "S4TM" = `S4TM lenses`; "SL2S" = `SL2S III sample`; "SNELLS" = `SNL-0 (ESO 325-G004)`, `SNL-1 (ESO 286-G022)`, `SNL-2`; "MaNGA" = `MaNGA J1436+4943`, `MaNGA J1701+3722`; NGC 6505 = `Euclid NGC 6505` (`aeg-s-000509`); J0403 = `MNELLS J0403-0239` (`aeg-s-000506`). **"Every lens system with rows except X"** means the semicolon list of the `system_id`s of the systems with rows (item 2), minus X. Lists are in systems-table order. A listed subset always has `scale = dataset` (§7a, 2.4.0). A single system has the scale stated. **A term with `applies_to = *` and a `size_column` filled on one system only** has `in_error_columns = no`; an empty cell means no size is given for that row.

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `theta_e` | point | * | g_bar | given | `size_column` `x_strong_lensing_theta_e_err_frac_hi` (lower in `_lo`), `as_released`, fraction | `a6s_theta_e` | §2a rule 7, class A rows only (rule 5); the column is empty elsewhere, including NGC 6505. Moves g_bar and the coordinate R_E; g_obs = π G Σ_cr is unchanged. SLACS: R5's adopted "2% RMS fractional error" (ms_arxiv.tex l. 972–975), no level stated; R13 used "a conservative 5%" (plain.txt l. 1669–1671); R9 0.5 % (ms_v2.tex l. 138) and SL2S's 3 % in the note (F3). SL2S: R20's 68 % intervals including its 3 % systematic (sl2s-rm-pdflatex.tex l. 462, 477–478). MaNGA: R32 l. 176 and l. 261. J0403: ±0.03″ of 1.47″ (R29 l. 196) |
| `theta_e_ngc6505` | point | `aeg-s-000509` | g_bar | given | 0.0004 (0.001″ of 2.500″), `lower_bound`, fraction | `a6s_theta_e` | "should therefore be considered lower-bounds which only account for measurement uncertainty" (R30 ms.tex l. 798; θ_E l. 813). The θ_E effect is not computed where no profile is printed (rule 5) |
| `ellipticity_j0403` | point | * | g_obs | given | `size_column` `x_strong_lensing_mass_ellipticity_frac` (J0403 only), `as_released`, fraction | — | `in_error_columns = no`; one-sided, upward. "Including a small ellipticity (e ≈ 0.1 as measured from galfit) increases the mass by 3 per cent" (R29 newlens.tex l. 210); a change in M_E at fixed radius. R29's revised "∼4 per cent" total is not used, to avoid counting the 2 % θ_E part twice |
| `lens_model_profile` | dataset | every lens system with rows except SNL-0, SNL-1 and SNL-2 | g_bar | not_given_by_source | — | `a6s_theta_e` | Changes the fitted θ_E, so it moves g_bar and R_E (F1): "the Einstein radius parameter … becomes somewhat dependent on the assumed mass model" for asymmetric images (R5 l. 843–848); slope effects (R9 l. 398–400). NGC 6505: R30 §4.3, where the model systematic dominates the stated lower bounds but is not sized (l. 798); M_E printed without error (l. 778). Not SNL-0, whose SIS-against-MFL difference is already in its g_obs error (class B), and not SNL-1 or SNL-2 (apertures) |
| `sie_axis_convention` | dataset | SLACS; S4TM | g_bar | not_given_by_source | — | `a6s_theta_e` | Both use the b_SIE intermediate-axis convention (R9 ms_v2.tex l. 117). R9's "accurate to < 1%" is the accuracy of Huterer's conversion relation, not the size of the convention difference |
| `external_shear` | dataset | S4TM | g_bar | given | 0.02, `as_released`, fraction | `a6s_theta_e` | R9 compares "the resulted Einstein radii" with and without shear: "The overall fractional discrepancy is on the level of 2%" (R9 l. 388); "about 4%" in mocks. R10 omits shear "as quantified in Shu15" (R10 l. 308–309) |
| `external_convergence` | dataset | every lens system with rows except SNL-0 | g_obs | not_given_by_source | — | — | Changes M_E at a fixed radius: "no more than a few percent" (R9 l. 386). SNL-0's is the next row |
| `line_of_sight_snl0` | point | * | g_obs | given | `size_column` `x_strong_lensing_los_frac` (SNL-0 only), `as_released`, fraction | — | `in_error_columns = no` (the validator requires `point` and `given` for that form; R28 states the size itself, citing Taruya et al. 2002). "∼2 per cent for a z = 2 source (Taruya et al. 2002)" (R28 l. 320–322) |
| `lens_light_subtraction` | dataset | S4TM | g_bar | not_given_by_source | — | `a6s_theta_e` | The B-spline foreground subtraction "could introduce some systematic uncertainties in the lens and source parameters" (R10 l. 290–292) |
| `aperture_radius_snl12` | dataset | `aeg-s-000504;aeg-s-000505` (SNL-1, SNL-2) | both | not_given_by_source | — | — | R_ap against the HST half-separation: 2.38″ and 2.21″ (R61 Table 2 l. 151) against 2.43 ± 0.03″ and 2.30 ± 0.03″ (l. 155); a difference, not an error |
| `companion_snl2` | point | `aeg-s-000505` | g_obs | not_given_by_source | — | — | "tension between the measured and predicted flux ratios" (R61 l. 317); SLC15's 8–16 % superseded |
| `redshift_measurement` | dataset | every lens system with rows except NGC 6505 | both | not_given_by_source | — | — | No redshift errors printed except R30 (rows below) |
| `redshift_lens_ngc6505` | point | `aeg-s-000509` | g_obs | given | 0.00003, `as_released`, redshift | — | z_l (R30 l. 639); effect not computed in v2 |
| `redshift_source_ngc6505` | point | `aeg-s-000509` | g_obs | given | 0.003, `as_released`, redshift | — | z_s (R30 l. 698); effect not computed in v2 |
| `cosmology_h0` | dataset | SLACS; S4TM; SL2S; NGC 6505 | g_obs | not_given_by_source | — | `a6s_source_cosmology` | Exact formula (item 7). These sources test no alternative H0 |
| `cosmology_h0_snells` | dataset | SNELLS | g_obs | given | adopted 70, alternative 67 (`size_lo` 67, `size_hi` 70), `range`, km s-1 Mpc-1 | `a6s_source_cosmology` | p = 67/70, from the term's own pair (applying D-094/D-104). "Adopting $H_0$ = 67 … from the Planck cosmology (Planck Collaboration 2014), rather than … 70 … from WMAP7" (R25 snellsI_arxiv.tex l. 862–863). v1's rows carry 70.4 (WMAP7, R28 and R61), which does not enter p. In α: "would yield smaller α by ∼5 per cent" (l. 863) |
| `cosmology_h0_j0403` | dataset | `aeg-s-000506` | g_obs | given | adopted 70.4, alternative 67.8 (`size_lo` 67.8, `size_hi` 70.4), `range`, km s-1 Mpc-1 | `a6s_source_cosmology` | p = 67.8/70.4 (applying D-094/D-104). Adopted 70.4 (R29 l. 210). Alternative: "If we had prescribed the [Planck Collaboration 2016] cosmology" (l. 241); that paper is A&A 594, A13 (arXiv 1502.01589), whose abstract gives "H0= (67.8 +/- 0.9) km/s/Mpc". In α: "4 per cent lower, due to the variation in H0" (l. 241) |
| `cosmology_h0_manga` | dataset | MaNGA | g_obs | given | adopted 67.4, alternative 69.6 (`size_lo` 67.4, `size_hi` 69.6), `range`, km s-1 Mpc-1 | `a6s_source_cosmology` | p = 69.6/67.4 (applying D-094/D-104). Adopted: "We adopt the cosmological parameters from" Planck Collaboration 2018 (R32 main.tex l. 100–101); arXiv 1807.06209 abstract: "$H_0 = (67.4\pm 0.5)$km/s/Mpc". Alternative: Bennett et al. 2014 (l. 293); arXiv 1406.1718 abstract: "69.6+/-0.7 km/s/Mpc". v1's MaNGA rows have no `x_strong_lensing_h0`, which does not enter p. In α: "would increase α by 3.5 per cent" (l. 293) |
| `cosmology_omega_m` | dataset | * | g_obs | not_given_by_source | — | — | Ω_m as stated per source (`x_strong_lensing_om`); flags `cosmology_named_only`, `flatness_not_stated` as v1 |
| `lens_distance_snl0` | system | `aeg-s-000503` | g_obs | given | 0.03–0.04 (`size_lo`, `size_hi`), `as_released`, fraction of D_l; applied as a shift of ±size_hi | `a6s_lens_distance` | "an uncertainty corresponding to a 500 km s⁻¹ peculiar velocity (3-4%)" (R26 snells.tex l. 139). In α: "up to 5 per cent" (R25 l. 864) |
| `lens_distance_snl1` | system | `aeg-s-000504` | g_obs | given | 0.03–0.04, `as_released`, fraction of D_l; applied as a shift of ±size_hi | `a6s_lens_distance` | As SNL-0 (R26 l. 139 covers the three SNELLS lenses of its Table 1) |
| `lens_distance_snl2` | system | `aeg-s-000505` | g_obs | given | 0.03–0.04, `as_released`, fraction of D_l; applied as a shift of ±size_hi | `a6s_lens_distance` | As SNL-0 |
| `lens_distance_ngc6505` | system | `aeg-s-000509` | g_obs | given | z 0.04243 (spectroscopic, l. 639) against 0.041 ± 0.001 (cosmological) (`size_lo` 0.040, `size_hi` 0.04243), `range`, redshift | `a6s_lens_distance` | "On top of the bulk flow peculiar velocities of individual galaxies are typically present at the $150\,\kms$ level. Combining these two effects results in a cosmological redshift of $z=0.041\pm0.001$" (R30 ms.tex l. 790). Effect not computed in v2 (applying D-094/D-104). v1's alternative row (z = 0.041) stays as it is |
| `lens_distance_other` | dataset | every lens system with rows except SNELLS and NGC 6505 | g_obs | not_given_by_source | — | `a6s_lens_distance` | No peculiar-velocity or frame effect stated |
| `aperture_factor_slacs` | dataset | SLACS | g_bar | not_given_by_source | — | — | "⟨f_ap⟩ = 0.36 ± 0.01" is a sample mean (R13 l. 1701–1705); "the stellar mass is traced by the light distribution" |
| `r_eff_slacs` | dataset | SLACS | g_bar | given | 0.035, `as_released`, fraction | — | R_e error adopted by R5 (l. 1072–1076); its effect through f(<R_E) is not computed in v2 |
| `r_eff_sl2s` | point | * | g_bar | given | `size_column` `x_strong_lensing_r_eff_err_frac` (SL2S rows only: HST 0.10, CFHT 0.30), `as_released`, fraction | — | `in_error_columns = no`. R20 l. 354–359; the reading records which imaging each lens uses; effect not computed in v2 |
| `r_eff_s4tm` | dataset | S4TM | g_bar | not_given_by_source | — | — | No R_e error printed (R10 l. 386) |
| `sps_templates_slacs` | dataset | SLACS | g_bar | not_given_by_source | — | — | solar-metallicity, dust-free templates (R13 l. 914–916, 1060–1064); Maraston pair kept as alternatives |
| `sps_systematic_s4tm` | dataset | S4TM | g_bar | given | 0.5, `as_released`, dex | — | "around 0.5 dex" between the lower- and upper-bound models (R9 l. 424–425) |
| `sps_template_sl2s` | dataset | SL2S | g_bar | given | 0.06, `as_released`, dex | — | R20 l. 740; bias 0.01 dex |
| `luminosity_corrections_manga` | dataset | MaNGA | g_bar | not_given_by_source | — | — | extinction, band-shift and PSF corrections carry no stated error (R32 l. 270–272; F5) |
| `upsilon_ref_manga` | dataset | MaNGA | g_bar | given | 2.41–3.46, `range`, solar units | — | "The full range in Υ_ref spanned by these models is 2.41–3.46; our calculations adopt this as the 2σ interval" (R32 l. 276–277). One value for both lenses (F4); left out of `g_bar_err_point_*` |
| `pop_model_family_j0403` | system | `aeg-s-000506` | g_bar | not_given_by_source | — | — | Stated only in α, which subtracts a modelled mass, so it is not a g_bar size (D-104 rule 1's reason; applying D-094/D-104). In α: Maraston models: "α would increase by 10 per cent" (R29 l. 241) |
| `pop_age_j0403` | system | `aeg-s-000506` | g_bar | not_given_by_source | — | — | As above. In α: 8.5 Gyr: "α would have increased by 14 per cent" (R29 l. 241) |
| `pop_model_family_manga` | dataset | MaNGA | g_bar | not_given_by_source | — | — | As above. In α: "using Maraston models for Υ_ref would increase α by ∼12 per cent" (R32 l. 293) |
| `alpha_fe` | dataset | * | g_bar | not_given_by_source | — | — | SLC15 "∼4 per cent" in J-band Υ; SL13 2–3 % in I-band; not for the bands v1 uses |
| `stellar_imf` | dataset | * | g_bar | given | `size_column` `x_strong_lensing_mstar_top_msun` (upper end), `range`, M☉ | `a6s_stellar_imf` | v1's slider, unchanged. Lower end: the printed Chabrier/Kroupa value |
| `gas_in_re` | dataset | * | g_bar | given_by_other_source | `size_column` `x_strong_lensing_gas_hot_frac_max` (hot; cold in `_cold_frac_max`), `range`, fraction of M*(<R_E) | `a6s_gas_in_RE` | v1's registered term (D-076 item 1); the sources call gas negligible (R28 l. 496; R25 l. 769; R32 l. 274) |
| `neighbour_light_snl2` | point | * | g_bar | given | `size_column` `x_strong_lensing_neighbour_light_frac` (SNL-2 only), `as_released`, fraction | — | `in_error_columns = no`. "only 1.5%, a minor effect that we neglect" (R26 l. 141) |
| `internal_dust_snl1` | point | `aeg-s-000504` | g_bar | not_given_by_source | — | — | R61 l. 313 |
| `lensed_source_light` | dataset | * | g_bar | not_given_by_source | — | — | "not affected in any significant way" (R13) |
| `solar_magnitude` | dataset | * | g_bar | not_given_by_source | — | — | 4.066 (F814W), 4.64 (r, AB), 4.534 and 4.53 (i), as each source states |
| `aperture_shape` | dataset | * | both | not_given_by_source | — | — | circular disk for M* against the SIE's elliptical critical curve, "expressed as in an 'effective' axisymmetric model" (R13 l. 1646–1651) |

   - **Registry update for v2** (`data/assumptions.json`). Every `a6s_*` entry gains an `aeg-d-strong-lensing/v2` dataset entry; v1's entries stay as published.
     - **`a6s_source_cosmology`** (corrected, D-094 rule 4). p = H0_alt / H0_adopted, computed from the term's own pair in km s⁻¹ Mpc⁻¹ (item 7); numeric `default` = 1. No row column enters p (applying D-094/D-104). `role` = uncertainty-term formula; `not_adjustable_reason` = "the effect of a stated H0 pair; making it a slider needs a ruling".
       - `g_obs`, `g_obs_err_*` and `g_obs_err_point_*` × p / p0.
       - `r_kpc` × p0 / p.
       - g_bar and its components are unchanged.
       - Its v2 note replaces v1's "does not depend on it to first order" with D-094's text.
     - **`a6s_theta_e` (new).** p = θ_E / θ_E,printed; numeric `default` = 1; `role` = uncertainty-term formula; `not_adjustable_reason` = "the effect of a stated θ_E error; not a slider".
       - `g_bar`, `g_bar_stars`, `g_bar_gas_cold`, `g_bar_gas_hot`, `x_strong_lensing_g_bar_stars_ref`, `g_bar_err_*` and `g_bar_err_point_*` × (p / p0)^`x_strong_lensing_dlngbar_dlntheta`.
       - `r_kpc` × p / p0.
       - g_obs is unchanged.
       - It is a log-linear (first-order) approximation in ln θ_E. That is adequate at 2 %; at J1701's 10 % the second-order term is not computed, and the note says so.
     - **`a6s_lens_distance` (new).** p = the fractional change in D_l; numeric `default` = 0; `role` and `not_adjustable_reason` as for `a6s_theta_e`.
       - `g_obs`, `g_obs_err_*` and `g_obs_err_point_*` × (1 + p0) / (1 + p).
       - `r_kpc` × (1 + p) / (1 + p0).
       - g_bar is unchanged.
       - It assumes D_s ≫ D_l (rule 6); the note says so.
     - **`a6s_gas_in_RE`** (v2 formula). v1's formula uses `g_obs × x_strong_lensing_mstar_re_msun / x_strong_lensing_m_e_msun` for G M*(<R_E)/R_E². The v2 formula uses `x_strong_lensing_g_bar_stars_ref` instead, which has the same value at every default (item 4), so the gas term does not move with H0 or the lens distance and follows θ_E. The fractions and range are v1's.
     - **`a6s_stellar_imf`:** carried over unchanged, with a v2 entry. It and `a6s_gas_in_RE` are the only sliders, as in v1. Making any other entry a slider needs a ruling.
     - **Unchanged except for the v2 entry:** `a6s_gr_lensing`, `a6s_projected_cylinder`, `a6s_redshifts_spectroscopic`, `a6s_mstar_population` and `a6s_mstar_profile`.
   - **Check (part of this item).** A script committed with the conversion, `v2/reproduction/check_formulas.py`, runs the checks of `pipeline/aeg/formula_check.py` on **every** `a6s_*` v2 entry with effects, not only those listed in `adjustable`:
     - every formula parses and names only `p`, `p0`, existing row columns or `system.<column>`;
     - Python (`pipeline/aeg/formula.py`) and JavaScript (`site/src/formula.mjs`) agree to a relative 10⁻¹² on every value it evaluates;
     - evaluated at p = p0 on every v2 row where every column it names is filled, it leaves every affected column unchanged to a relative 10⁻¹²;
     - **combined:**
       - applying all v2 entries in registry order at their defaults leaves every column unchanged;
       - with only `a6s_source_cosmology` or only `a6s_lens_distance` moved to the end of a stated size, `g_bar`, `g_bar_stars`, `g_bar_gas_cold` and `g_bar_gas_hot` are unchanged;
       - with only `a6s_theta_e` moved, `g_obs` is unchanged, and `g_bar` equals `g_bar_stars + g_bar_gas_cold + g_bar_gas_hot` after all entries;
       - with H0 or the lens distance moved together with `a6s_stellar_imf` or `a6s_gas_in_RE` at each end of its range, g_bar equals its value with the slider alone;
     - **rows where a named column is empty** (for `a6s_theta_e`: rows without `x_strong_lensing_dlngbar_dlntheta`, that is, without a printed profile) are not evaluated for that entry. S4TM and SL2S rows, which have a printed profile, are evaluated. No row lists `a6s_theta_e` in `adjustable`, and the count of rows not evaluated is published with the result.
   - **Second reading of term sizes.** Step A's two concordant readings (A and B), with the corrections of review 1 checked at source, serve as the D-031 second reading for the sizes in this table.

### C. Structure and flags

8. **Plotting.** As v1: the same 94 rows plotted, and the same 53 alternatives `plotted = false`, `not_plotted_reason = alternative_value`. The only exception is a rule 1 change by ruling. The epoch-gap systems (D-066) stay recorded, not plotted.
9. **Named items v1 omitted.**
   - **The F1 correction** is stated on the dataset page and in a known issue: v1 carried the θ_E error on g_obs "at fixed R_E" (`convert.py` l. 48–49).
   - **The F2 correction** (D-094) is stated the same way, in the same known issue or its own.
   - **NGC 6505's lower bounds** (F5) are stated in the row's `notes`.
   - **The dataset page** contains the line "θ_E error stated; effect on g_bar not computed" for the rows of rule 5's "no profile printed" case (D-104 rule 3), checked by a text search of the built page (HTML unescaped).
   - **The central black hole (D-104 rule 2).** It is not added to g_bar. Every size the sources quote comes from an M_BH–σ scaling of the lens's own velocity dispersion (R28 l. 691–693; R30 l. 778; R25 l. 772–773), so adding it would take an input from the system's own kinematics (D-036 #6), whatever "detected baryon" is taken to mean. R28 sizes it at "2 per cent of M_Ein" (l. 693); as a share of M*, and so of g_bar, it is larger, and the dataset page says so. Because each inventory component has one status, it is recorded in the descriptor's `x_baryon_inventory` as two components (applying D-094/D-104):
     - "central black hole (SNELLS, MaNGA and NGC 6505 sources)": status `stated_negligible`, with the quotes: R25 ("Other possible non-stellar mass contributions within the Einstein radius, e.g. gas and central black holes, are neglected", l. 769), R28 ("We neglected the extra mass that would be contributed by a central super-massive black hole", l. 691), R30 ("Since this corresponds to only (0.57 +0.68/−0.31)% of the mass within the Einstein radius, we do not include it", l. 778), R32 ("in principle from a central black hole, gas, etc but these are expected to be negligible", l. 274);
     - "central black hole (other sources)": status `not_addressed`, listing those sources, as `baryon_inventory.csv` records.
   - **Sources.** `v2/sources.json` lists every v1 source still used, with v1's hashes, and the three arXiv abstract pages read on 2026-11-05 for H0 values (rule 6), with their hashes and licences: 1502.01589 (`d85fc462fcabf12405ff913a587196bf78b1e1a35b235de8812f49a4662f9cb9`), 1807.06209 (`17256f2d1adbc17162eb3d0e29bf1a547d6dfb131efe3231d2d32abfc72429fa`) and 1406.1718 (`4f18ff396491283c7e0fce47b2010caae4ab0c6ab5344a1efabcb924f1f78008`). These are the pages as served on that date; the conversion records the hash it fetches, and a different page is resolved by checking that the quoted H0 is unchanged.
10. **Descriptor.**
    - `standard_version` is `2.5.1`.
    - `x_value_change_ruling` is set only if item 3 lists a row.
    - `x_second_reading` points to `SECOND_READING.md` and the frozen reading files.
    - `x_baryon_inventory` gains the two black-hole components (item 9).
    - Other fields are as v1, updated.
11. **Second reading (D-031 item 3).** One independent reader, as in the order of work, writes the six files listed there.
    - **Pass:** the package equals the frozen reading files on every field they hold. Any mismatch is a fail.
12. **Standard and site.**
    - `PYTHONPATH=pipeline python -m aeg.validate data/packages/aeg-d-strong-lensing/v2` passes under 2.5.1 (the full `validate()`, not only the 2.2.0 and 2.4.0 checks);
    - `v2/reproduction/check_formulas.py` (item 7) and `PYTHONPATH=pipeline python -m aeg.formula_check` pass;
    - `PYTHONPATH=pipeline python -m pytest -q pipeline/tests/test_lensing.py` passes;
    - the site builds;
    - `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes.
13. **v1 untouched.** Every file in `aeg-d-strong-lensing/v1/` has the checksum it had at commit `5dc4091`.

**Pass** = all thirteen hold. Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right.
- v1's tests 1–4 (PASS). They stand for v1 and are not re-run.
- The θ_E term's effect where no profile is printed (rule 5), the redshift-error effects for NGC 6505, and the R_e error's effect through f(<R_E). All are listed, not computed.
- The epoch-gap systems (z_l ≥ 0.30), which carry no measurement rows.

## Checked before freezing (revision 3, 2026-11-05)

A mock package was built from v1's tables, plus every column this test adds (including the four new single-system size columns and the `no_uncertainty` flag on class A rows), and the 44 terms above with their system lists (SLACS 48, S4TM 37, SL2S 2, SNELLS 3, MaNGA 2 systems). The new registry entries, and the v2 gas formula on `x_strong_lensing_g_bar_stars_ref`, were added in memory only.
- **Validator:** `validate_v22` and `validate_v24` at 2.5.1 report 0 problems. The full `validate()` was not run on the mock, because the mock has no descriptor, sources or checksums; item 12 runs it on the real package.
- **The four v2 formulas** (`a6s_source_cosmology`, `a6s_gas_in_RE`, `a6s_theta_e`, `a6s_lens_distance`) parse, name only existing columns, and leave every value unchanged at the default on every row where their inputs are filled: 0 problems.
- **The combined checks of item 7:** 0 problems. These were:
  - all four entries in registry order at their defaults;
  - H0 moved alone to each of the three stated pairs (67/70, 67.8/70.4, 69.6/67.4), or the lens distance to ±4 %, with g_bar and its components unchanged;
  - θ_E moved alone (+2 %), with g_obs unchanged and g_bar equal to the sum of its components;
  - H0 or the lens distance moved together with the gas slider at each end of its range, with g_bar equal to its value under the slider alone.
- **H0 values** were read from the arXiv abstract pages (hashes in item 9). No other value was read for this revision.
- **Nothing was looked at:** no g value was printed or inspected. The mock and its script are not committed.
