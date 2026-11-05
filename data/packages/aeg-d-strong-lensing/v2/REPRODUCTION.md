# aeg-d-strong-lensing/v2: reproduction test (draft; frozen on merge, before conversion)

**Status: draft, revision 1, for review and then JvH's approval.**
- Written 2026-11-05, before `convert.py` for v2 exists. No v2 value has been computed, and no g value of v1 was opened to write it.
- On merge, this file's SHA-256 goes into `data/frozen/lenses-v2-test.json`, and the file is not edited after merge.
- If the test fails, v2 does not ship and the failure is published. The test is not changed to pass (operating rule 5; D-005).

**Depends on:**
- data standard 2.5.1 (§2a rule 7, from D-093; §12 as clarified by D-099 rule 1);
- D-064 item 4 as replaced by D-094 (distance enters at first order, g_obs/g_bar ∝ 1/D);
- D-087 (`model_dependence`);
- D-096 and D-098 rule 1 (defer to the source's stated choices; exclusions only for the same data points);
- the frozen precedence rule `docs/methods/A6S_PRECEDENCE.md` (D-065) and the rulings D-066, D-075 and D-076, which v1 applied.

**Open items for JvH, to be ruled before this test is frozen:** O1 (the central black hole) and O2 (the θ_E term's profile where the source prints none). See the end of this file. The test is written with the recommended answer to each; a different ruling changes only the rows named there.

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
   - The second reading records, for every source used (R5, R13, R10, R9, R20, R21, R25, R26, R28, R29, R30, R32, R61), whether it marks a preferred value or names a fiducial baseline among the values it prints, with quote and location.
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
   - **Expected rows of this kind ("class A"):**
     - SLACS (48 rows; M_E computed from R5's θ_E);
     - SL2S (2 rows; computed from R20's θ_E);
     - MaNGA J1436+4943 and J1701+3722 (R32 prints M_E and θ_E; the M_E error is the θ_E error, "the error reflecting the variation between models" (main.tex l. 176) and "we impose a 10 per cent error on θ_Ein" (l. 261));
     - NGC 6505 (R30; θ_E error stated as a lower bound, l. 798, l. 813; M_E printed without error).
   - **Rows where the printed M_E error is not a θ_E error alone ("class B")** keep it on g_obs, as in v1, and get no separate θ_E term, so nothing is counted twice:
     - SNL-0: the 4 % reflects "the difference between SIS- and MFL-model masses" (R28 lensz_arXiv.tex l. 317–325), and θ_E (2.85″) has no printed error;
     - J0403−0239: the 2 % "dominated by the measurement of R_Ein" plus about 3 % for ellipticity, revised "to ∼4 per cent" (R29 newlens.tex l. 210). The parts are not separable.
   - **Rows where θ_E has no printed error:** S4TM (37 rows; R10 prints neither a θ_E nor an M_E error). R9's 0.5 % was derived for R9's own models (ms_v2.tex l. 138), so under the sizing rule it is not a size for R10's models; it goes in the note.
   - **SNL-1 and SNL-2** use a mass inside the aperture R_ap (R61 Table 2), which has no printed error. Rule 7 does not apply (its "no error of its own" clause). Their printed mass errors stay on g_obs.
   - **The reading decides each row's class at source:** whether the source defines M_E as the mass inside the radius of mean convergence 1, and whether its stated error is a θ_E error alone. Where the reading differs from the expectation above, the reading governs, and the result says so.
6. **Distance (D-094).** Distance moves g_obs at first order. The stellar g_bar is distance-free at fixed Ω_m: M* ∝ D_L², R_E² ∝ D_A², and both scale as H0⁻².
   - **H0** enters exactly as g_obs ∝ H0 (all distances ∝ 1/H0 at fixed Ω_m), with R_E ∝ 1/H0. The formula is the corrected registry entry `a6s_source_cosmology` (item 7).
   - **Peculiar velocity and the redshift frame** enter through the lens distance only. Their size is taken as each source states it, as a fractional change in the lensing mass-to-light ratio, and applied to g_obs (`a6s_lens_distance`, item 7).

## Order of work (against steering)

1. **The second reading** (item 11) is completed before the first v2 conversion run, by a reader with no access to v1's g values, `convert.py` or any v2 table. It writes to `v2/reading/`:
   - `d096.csv`: D-096 fields per source, with quote and location;
   - `theta_class.csv`: per measurement row, the rule 5 class (A, B, no θ_E error, aperture), the fractional θ_E error as printed (lower and upper), and its quote and location;
   - `profiles.csv`: per class A row, the light profile the source prints for the stellar mass inside R_E (form, R_e, n, and which paper and table), or "none printed";
   - `err_levels.csv`: per source, the confidence level of each error used, as stated;
   - `distance.csv`: per source, any statement of an H0, peculiar-velocity or redshift-frame effect, with its size as stated.
2. **Disagreements** with step A, or with this test's expectations, are resolved at source by a session with no access to any g value, and recorded in `v2/reading/resolutions.md`. A conflict under rule 1 goes to JvH.
3. **Freezing the reading.** The SHA-256 of every reading file goes into `data/frozen/lenses-v2-reading.json`, by a pull request merged before the first conversion run.
4. **Conversion.** `convert.py` takes D-096 changes, θ_E classes and sizes, profiles, confidence levels and distance sizes **only** from the frozen reading files. It contains no system-specific rule of its own. It reuses v1's frozen code (`aeg.lensing`, frozen with v1) for every computed quantity.

## The test

Applied to the v2 tables, with v1 at commit `5dc4091` as the reference.

### A. Values and tables

1. **Rows.** v2 has exactly v1's 147 measurement rows (94 defaults, 53 alternatives), in v1's order, and v1's 212 systems. Row k has v1 row k's `system_id`, `role`, `alternative_of` (prefix changed) and `x_strong_lensing_scope`, and the same `measurement_id` apart from the prefix (`v1` → `v2`).
2. **What may change, by table.** Each table is compared with v1's by ID, after the prefix `v1` → `v2` in every ID.
   - **Measurements.**
     - **Bit-for-bit equal to v1 on every row:** `g_obs`, `g_bar`, `g_bar_stars`, `g_bar_gas_cold`, `g_bar_gas_hot`, `r_kpc`, `g_bar_err_lo`, `g_bar_err_hi`, and every v1 `x_strong_lensing_*` column. The only exception is a row changed under rule 1 by ruling.
     - **`g_obs_err_lo` and `g_obs_err_hi`:**
       - on class A rows, empty (rule 5). The θ_E error is in the term `theta_e` (item 7);
       - on every other row, bit-for-bit equal to v1.
     - **Every other v1 column is unchanged,** except:
       - IDs: the `measurement_id` prefix, and the observable IDs in `observed_from`, `baryonic_from` and `alternative_of`;
       - `notes` on class A rows ("θ_E error carried by g_bar, standard §2a rule 7; term theta_e") and on rows given a reading note;
       - `assumptions`, which gains the new registry IDs of item 7 on every row.
     - **New columns,** and only these:
       - `g_obs_err_point_lo/hi` and `g_bar_err_point_lo/hi` (item 5);
       - `err_level`, `err_level_status`, `g_bar_err_level` and `g_bar_err_level_status` (item 5);
       - the extension columns of item 6.
   - **Systems.** Every v1 column is unchanged, except `properties` where a reading note is added. No new column.
   - **Observables.** Every v1 row keeps every v1 value. `err_level` and `err_level_status` are added (item 5). No row is added or removed.
3. **Changed values.** Expected: none. If the frozen reading lists a D-096 change and JvH has ruled it, each changed row is listed in `REPRODUCTION_RESULT.md` with the rule, the quotation and location, and the old and new values. A change not traceable to the frozen reading and a ruling is a fail. So is a listed change that is missing.
4. **Arithmetic.**
   - M_E (where computed), R_E, f(<R_E), M*(<R_E), g_obs and g_bar are recomputed from the stored inputs by `aeg.lensing` (frozen with v1). They agree with the stored values to a relative 10⁻⁹.
   - The new column `x_strong_lensing_dlngbar_dlntheta` (item 6) is recomputed the same way and agrees to a relative 10⁻⁶.

### B. Uncertainties (standard 2.5.1 §2a, §3, §7a)

5. **Error columns and confidence levels.** One value per lens, so point and system scale coincide (§2a; readers A and B).
   - **`g_obs_err_point_*`** equal `g_obs_err_*` on every row.
   - **`g_bar_err_point_*`** equal `g_bar_err_*` on every row except the two MaNGA lenses. There, they hold the L_Ein error alone (R32 Table 2: 6.72 ± 0.10 and 5.56 ± 0.35), propagated as v1 does. This is because v1's `g_bar_err_*` there also contain the shared Υ_ref (±0.26), which is a dataset-scale term (F4; §2a rule 1). Their header says so (§2a rule 6).
   - **Confidence levels**, per source, from `v2/reading/err_levels.csv`. Expected, from step A:

     | Source | Side | Expected | Basis |
     |---|---|---|---|
     | R5 (SLACS θ_E) | g_bar via term `theta_e` | `not_given_by_source` | "a 2% RMS fractional error" (ms_arxiv.tex l. 972–975): an RMS, no level stated |
     | R13 (SLACS M*) | g_bar | `stated`, 0.683 | "The mass estimates (with 1 σ error bars)" (plain.txt l. 2975, figure caption) |
     | R20 (SL2S) | both | `stated`, 0.68 | "68% credible intervals (1-σ uncertainties)" (sl2s-rm-pdflatex.tex l. 462) |
     | R10 (S4TM) | both | no error printed | `no_uncertainty`, as v1 |
     | R26, R28 (SNL-0) | both | `not_given_by_source` | |
     | R61 (SNL-1, SNL-2) | both | `not_given_by_source` | |
     | R29 (J0403) | both | `not_given_by_source` | |
     | R32 (MaNGA) | g_bar | `not_given_by_source` | the "2σ interval" (main.tex l. 276–277) is for Υ_ref, a dataset term, not for the point error |
     | R30 (NGC 6505) | both | `not_given_by_source` | lower bounds (l. 798) |

     Where the frozen reading records a level that step A did not find, the reading governs, and the result says so.
6. **New per-row extension columns** (standard 2.5.1 §12). Each header names the term or formula that uses it:
   - `x_strong_lensing_theta_e_err_frac_lo`, `_hi`: the fractional θ_E error on class A rows, from `theta_class.csv`. SLACS: 0.02 both sides, R5's adopted RMS. Empty elsewhere.
   - `x_strong_lensing_dlngbar_dlntheta`: on class A rows, d ln g_bar / d ln θ_E at fixed redshifts and cosmology. It equals −2 + d ln f(<R_E)/d ln R_E, from the profile in `profiles.csv`, by central difference (step 10⁻⁴ in ln R_E) of the frozen `aeg.lensing.sersic_projected_fraction`. Where M*(<R_E) is L(<R_E) × Υ, the same profile is used for L. Where no profile is printed, see O2.
   - `x_strong_lensing_lens_distance_frac`: the fractional change in the lensing mass-to-light ratio a source states for peculiar velocity or the redshift frame (`distance.csv`). Empty where none is stated.
   - **Empty values:** a row whose source gives no size gets an empty value, and the column name goes in `notes`. The flag `no_uncertainty` is used only as in v1.
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly the rows below.
   - Each cites its source at the location given (the adjudication, or readers A and B).
   - `covariance` is `not_published` on every row.
   - **One sizing rule for every row.** A size is `given` only where the source states it for these systems, or for a class that contains them. Otherwise the row is `not_given_by_source`, and any figure the source gives elsewhere goes in the note.
   - **Not uncertainty terms (§2a rule 4):** general-relativistic lensing (`a6s_gr_lensing`), the projected cylinder (`a6s_projected_cylinder`) and spectroscopic redshifts (`a6s_redshifts_spectroscopic`) are registry assumptions, as in v1.
   - **Subset lists.** Where `applies_to` names a survey ("SLACS", "S4TM", "SL2S", "SNELLS", "MaNGA"), it is the semicolon list of the `system_id`s of that survey's default rows (`x_strong_lensing_scope`), in systems-table order.

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `theta_e` | point | * | g_bar | given | `size_column` `x_strong_lensing_theta_e_err_frac_hi` (lower in `_lo`), `as_released` | `a6s_theta_e` | §2a rule 7, class A rows only (rule 5). Moves g_bar and the coordinate R_E; g_obs = π G Σ_cr is unchanged. SLACS: R5's adopted "2% RMS" (l. 972–975); R13 used "a conservative 5%" (plain.txt l. 1669–1671); SL2S adopts 3 % (F3). SL2S: R20's 68 % intervals, including its 3 % systematic. MaNGA: R32 l. 176 and l. 261. Kinds differ by source: see `err_levels.csv` |
| `theta_e_ngc6505` | point | `aeg-s-000509` (NGC 6505) | g_bar | given | 0.0004 (0.001″ of 2.500″), `lower_bound` | `a6s_theta_e` | "should therefore be considered lower-bounds which only account for measurement uncertainty" (R30 ms.tex l. 798; θ_E l. 813) |
| `lens_model_systematic_ngc6505` | system | `aeg-s-000509` | g_obs | not_given_by_source | — | — | R30 §4.3: the systematic dominates but is not sized; M_E printed without error (l. 778) |
| `lens_model_profile` | system | * | g_obs | not_given_by_source | — | — | "the Einstein radius parameter … becomes somewhat dependent on the assumed mass model" for asymmetric images (R5 l. 843–848); slope effects (R9 l. 398–400) |
| `sie_axis_convention` | dataset | S4TM | g_obs | given | 0.01, `upper_bound` | — | "accurate to < 1% on average" (R9 ms_v2.tex l. 117) |
| `external_shear` | dataset | S4TM | g_obs | given | 0.02, `as_released` | — | R10 models omit shear; R9: "The overall fractional discrepancy is on the level of 2%", "about 4%" in mocks (l. 388) |
| `external_convergence` | system | * | g_obs | not_given_by_source | — | — | "no more than a few percent" (R9 l. 386) |
| `line_of_sight_snl0` | system | `aeg-s-000503` (SNL-0) | g_obs | given_by_other_source | 0.02, `as_released` | — | "∼2 per cent for a z = 2 source (Taruya et al. 2002)" (R28 l. 320–322) |
| `lens_light_subtraction` | dataset | S4TM | g_obs | not_given_by_source | — | — | R10 l. 291–292 |
| `aperture_radius_snl12` | dataset | `aeg-s-000504;aeg-s-000505` (SNL-1, SNL-2) | both | not_given_by_source | — | — | R_ap against the HST half-separation: 2 % and 4 % larger (R61 Table 1 l. 151, 156); a difference, not an error |
| `companion_snl2` | system | `aeg-s-000505` (SNL-2) | g_obs | not_given_by_source | — | — | "tension between the measured and predicted flux ratios" (R61 l. 317); SLC15's 8–16 % superseded |
| `redshift_measurement` | system | * | both | not_given_by_source | — | — | No redshift errors printed except R30 (row below) |
| `redshift_ngc6505` | system | `aeg-s-000509` | g_obs | given | z_l ± 0.00003 (`size_lo`) and z_s ± 0.003 (`size_hi`), `as_released` | — | R30 l. 639, 698; effect not computed in v2 |
| `cosmology_h0` | dataset | * | g_obs | not_given_by_source | — | `a6s_source_cosmology` | Exact formula (item 7). Sources stating no H0 effect: SLACS, S4TM, SL2S, NGC 6505 |
| `cosmology_h0_snells` | dataset | SNELLS | g_obs | given | 0.05, `as_released` | `a6s_source_cosmology` | "Adopting H0 = 67 … rather than H0 = 70 … would yield smaller α by ∼5 per cent" (R25 l. 862–863) |
| `cosmology_h0_j0403` | system | `aeg-s-000506` (J0403−0239) | g_obs | given | 0.04, `as_released` | `a6s_source_cosmology` | "α would be 4 per cent lower, due to the variation in H0" (R29 l. 241) |
| `cosmology_h0_manga` | dataset | MaNGA | g_obs | given | 0.035, `as_released` | `a6s_source_cosmology` | "would increase α by 3.5 per cent" (R32 l. 293) |
| `cosmology_omega_m` | dataset | * | g_obs | not_given_by_source | — | — | Ω_m as stated per source (`x_strong_lensing_om`); flags `cosmology_named_only`, `flatness_not_stated` as v1 |
| `lens_distance` | system | * | g_obs | given | `size_column` `x_strong_lensing_lens_distance_frac`, `as_released` | `a6s_lens_distance` | Peculiar velocity and redshift frame. Expected sizes: SNL-0 0.03–0.04 ("3–4%", R26 snells.tex l. 139); SNELLS up to 0.05 ("up to 5 per cent in α", R25 l. 864–865). NGC 6505: z = 0.041 ± 0.001 against 0.04243 (R30 l. 790), carried as v1's alternative row. Empty elsewhere |
| `aperture_factor_slacs` | dataset | SLACS | g_bar | not_given_by_source | — | — | "⟨f_ap⟩ = 0.36 ± 0.01" is a sample mean (R13 l. 1701–1705); "the stellar mass is traced by the light distribution" |
| `r_eff_profile` | point | * | g_bar | not_given_by_source | — | — | R_e errors: SLACS 3.5 % adopted (R5 l. 1072–1076); SL2S CFHT 30 %, HST 10 % (R20 l. 354–359); S4TM none (R10 l. 386); effect through f(<R_E) not computed in v2 |
| `sps_templates_slacs` | dataset | SLACS | g_bar | not_given_by_source | — | — | solar-metallicity, dust-free templates (R13 l. 914–916, 1060–1064); Maraston pair kept as alternatives |
| `sps_systematic_s4tm` | dataset | S4TM | g_bar | given | 0.5 dex, `as_released` | — | "around 0.5 dex" between lower- and upper-bound models (R9 l. 424–425) |
| `sps_template_sl2s` | dataset | SL2S | g_bar | given | 0.06 dex, `as_released` | — | R20 l. 740; bias 0.01 dex |
| `luminosity_corrections_manga` | dataset | MaNGA (`aeg-s-000507;aeg-s-000508`) | g_bar | not_given_by_source | — | — | extinction, band-shift and PSF corrections carry no stated error (R32 l. 270–272; F5) |
| `upsilon_ref_manga` | dataset | MaNGA | g_bar | given | 2.41–3.46, `range` | — | "The full range in Υ_ref spanned by these models is 2.41–3.46; our calculations adopt this as the 2σ interval" (R32 l. 276–277). One value for both lenses (F4); left out of `g_bar_err_point_*` |
| `pop_model_family_j0403` | system | `aeg-s-000506` | g_bar | given | 0.10, `as_released` | — | Maraston models: "α would increase by 10 per cent" (R29 l. 241) |
| `pop_age_j0403` | system | `aeg-s-000506` | g_bar | given | 0.14, `as_released` | — | 8.5 Gyr: "α would have increased by 14 per cent" (R29 l. 208) |
| `pop_model_family_manga` | dataset | MaNGA | g_bar | given | 0.12, `as_released` | — | "using Maraston models for Υ_ref would increase α by ∼12 per cent" (R32 l. 282) |
| `alpha_fe` | dataset | * | g_bar | not_given_by_source | — | — | SLC15 "∼4 per cent" in J-band Υ; SL13 2–3 % in I-band; not for the bands v1 uses |
| `stellar_imf` | dataset | * | g_bar | given | `size_column` `x_strong_lensing_mstar_top_msun` (upper end), `range` | `a6s_stellar_imf` | v1's slider, unchanged. Lower end: the printed Chabrier/Kroupa value |
| `gas_in_re` | dataset | * | g_bar | given_by_other_source | `size_column` `x_strong_lensing_gas_hot_frac_max` (hot; cold in `_cold_frac_max`), `range` | `a6s_gas_in_RE` | v1's registered term (D-076 item 1); the sources call gas negligible (R28 l. 496; R25 l. 769; R32 l. 274) |
| `neighbour_light_snl2` | system | `aeg-s-000505` | g_bar | given | 0.015, `as_released` | — | "only 1.5%, a minor effect that we neglect" (R26 l. 141) |
| `internal_dust_snl1` | system | `aeg-s-000504` | g_bar | not_given_by_source | — | — | R61 l. 313 |
| `lensed_source_light` | dataset | * | g_bar | not_given_by_source | — | — | "not affected in any significant way" (R13) |
| `solar_magnitude` | dataset | * | g_bar | not_given_by_source | — | — | 4.066 (F814W), 4.64 (r, AB), 4.534 and 4.53 (i), as each source states |
| `aperture_shape` | dataset | * | both | not_given_by_source | — | — | circular disk for M* against the SIE's elliptical critical curve, "expressed as in an 'effective' axisymmetric model" (R13 l. 1646–1651) |
| `central_black_hole` | system | * | g_bar | not_given_by_source | — | — | **O1.** Inside M_E; not detected matter. SNL-0 "2 per cent of M_Ein" expected (R28 §4); NGC 6505 "(0.57 +0.68/−0.31)%" (R30 l. 778); "∼1.4 × 10⁹ M⊙" (R25 l. 772–773) |

   - **Registry update for v2** (`data/assumptions.json`). Every `a6s_*` entry gains an `aeg-d-strong-lensing/v2` dataset entry; v1's entries stay as published. Every formula leaves every value unchanged at the default.
     - **`a6s_source_cosmology`** (corrected, D-094 rule 4).
       - p = H0 / H0_source; default 1.
       - `g_obs`, `g_obs_err_*` and `g_obs_err_point_*` × p / p0.
       - `r_kpc` × p0 / p.
       - g_bar is unchanged.
       - Its v2 note replaces v1's "does not depend on it to first order" with D-094's text.
     - **`a6s_theta_e` (new).**
       - p = θ_E / θ_E,printed; default 1.
       - `g_bar`, `g_bar_stars`, `g_bar_gas_cold`, `g_bar_gas_hot`, `g_bar_err_*` and `g_bar_err_point_*` × (p / p0)^`x_strong_lensing_dlngbar_dlntheta`.
       - `r_kpc` × p / p0.
       - g_obs is unchanged.
     - **`a6s_lens_distance` (new).**
       - p = the fractional change in the lensing mass-to-light ratio; default 0.
       - `g_obs`, `g_obs_err_*` and `g_obs_err_point_*` × (1 + p) / (1 + p0).
     - **`a6s_stellar_imf` and `a6s_gas_in_RE`:** carried over unchanged, with v2 entries. They are the only sliders, as in v1. Making any other entry a slider needs a ruling.
     - **Unchanged except for the v2 entry:** `a6s_gr_lensing`, `a6s_projected_cylinder`, `a6s_redshifts_spectroscopic`, `a6s_mstar_population` and `a6s_mstar_profile`.
   - **Check (part of this item).** For every `a6s_*` v2 entry with effects:
     - every formula parses;
     - it names only `p`, `p0`, existing row columns or `system.<column>`;
     - evaluated at p = p0 on every v2 row where every column it names is filled, it leaves every affected column unchanged to a relative 10⁻¹².
     - **Rows where a named column is empty** are those with no θ_E term (`x_strong_lensing_dlngbar_dlntheta` empty: rows outside class A, and O2). The formula is not applied to them. None of them lists `a6s_theta_e` in `adjustable`, and their count is published with the result.
   - **Second reading of term sizes.** Step A's two concordant readings (A and B) serve as the D-031 second reading for the sizes in this table.

### C. Structure and flags

8. **Plotting.** As v1: the same 94 rows plotted, and the same 53 alternatives `plotted = false`, `not_plotted_reason = alternative_value`. The only exception is a rule 1 change by ruling. The epoch-gap systems (D-066) stay recorded, not plotted.
9. **Named items v1 omitted.**
   - **The F1 correction** is stated on the dataset page and in a known issue: v1 carried the θ_E error on g_obs "at fixed R_E" (`convert.py` l. 48–49).
   - **The F2 correction** (D-094) is stated the same way, in the same known issue or its own.
   - **NGC 6505's lower bounds** (F5) are stated in the row's `notes`.
   - **Sources.** `v2/sources.json` lists every v1 source still used, with v1's hashes.
10. **Descriptor.**
    - `standard_version` is `2.5.1`.
    - `x_value_change_ruling` is set only if item 3 lists a row.
    - `x_second_reading` points to `SECOND_READING.md` and the frozen reading files.
    - Other fields are as v1, updated.
11. **Second reading (D-031 item 3).** One independent reader, as in the order of work, writes the five files listed there.
    - **Pass:** the package equals the frozen reading files on every field they hold. Any mismatch is a fail.
12. **Standard and site.**
    - `python -m aeg.validate data/packages/aeg-d-strong-lensing/v2` passes under 2.5.1;
    - the formula check passes;
    - `PYTHONPATH=pipeline python -m pytest -q pipeline/tests/test_lensing.py` passes;
    - the site builds;
    - `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes.
13. **v1 untouched.** Every file in `aeg-d-strong-lensing/v1/` has the checksum it had at commit `5dc4091`.

**Pass** = all thirteen hold. Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right.
- v1's tests 1–4 (PASS). They stand for v1 and are not re-run.
- The θ_E term's effect where no profile is printed (O2), and the R_e error's effect through f(<R_E) (`r_eff_profile`). Both are listed, not computed.
- The epoch-gap systems (z_l ≥ 0.30), which carry no measurement rows.

## Checked before freezing (draft, 2026-11-05)

A mock package was built from v1's tables plus every column this test adds, and from the 38 terms above with their survey lists (SLACS 48, S4TM 37, SL2S 2, SNELLS 3, MaNGA 2 systems). The new registry entries were added in memory only.
- `validate_v22` and `validate_v24` at 2.5.1 report 0 problems.
- The three new formulas parse, name only existing columns, and leave every value unchanged at the default on every row where their inputs are filled.
- No g value was printed or looked at. The mock and its script are not committed.

## Open items for JvH (before freezing)

- **O1. The central black hole.** It sits inside M_E, so it is part of g_obs. No source measures it as detected matter: the sizes quoted are expectations from scaling relations (SNL-0, SLC15) or an estimate (NGC 6505). Whether it counts as a detected baryon is a definitional question, not a source statement (adjudication F5).
  - **Recommend:** it is not detected matter. It stays out of g_bar, and the term `central_black_hole` lists its possible size as `not_given_by_source` on g_bar. This matches the baseline: "Newtonian gravity acting on detected baryonic matter".
  - **Alternative:** add it to g_bar where a source gives a size (SNL-0, NGC 6505). That would change two g_bar values and need D-096-style handling.
- **O2. The θ_E term where the source prints no light profile.** §2a rule 7 says such a profile "comes from the source or from a registered assumption".
  - **Recommend:** where `profiles.csv` records "none printed", `x_strong_lensing_dlngbar_dlntheta` is empty and the row's `notes` say the effect is not computed in v2. This adds no assumption.
  - **Alternative:** register a de Vaucouleurs profile with the source's printed R_e as an assumption for those rows. That needs a ruling and a published range.
  - **Expected scope:** possibly the MaNGA and NGC 6505 rows; the SLACS and SL2S rows have printed R_e (R5; R20).
