# aeg-d-xcop/v2: reproduction test, part B (structure, uncertainties, second reading)

**Status: draft, revision 1, for review and JvH's approval.**
- Written 2026-11-05, after part A was run and published (`REPRODUCTION_RESULT_PART_A.md`; D-091), before `convert.py` for v2 exists.
- No value from the shared archives was read to write it. Every number it quotes is either from E22, Paper II or Ettori & Eckert 2022 as read in step A, or from the published part A result.
- On merge, this file's SHA-256 goes into `data/frozen/xcop-v2-part-b.json`, and the file is not edited after merge.
- If the test fails, the failure is published. The test is not changed to pass (operating rule 5; D-005).
- **Part A is frozen and stays as run.** Nothing here re-scores it, and nothing here changes a rule it fixed (D-091 rule 1). Where part A fixed something (§5, A7, A8), part B carries it out.

**Depends on:**
- part A (`REPRODUCTION.md`, revision 6, frozen in `data/frozen/xcop-v2-part-a.json`) and its result with the D-091 erratum;
- D-089 (v2 from Eckert et al. 2022), D-090 (rules 1, 4 and 5), D-091 and D-092 (A644);
- data standard 2.5.1 (D-095 for `acceleration_released`; D-099 for §12);
- D-087 (`model_dependence`), D-093 (confidence levels; §2a rules), D-096 and D-098 rule 1 (defer to the source's stated choices; same data points only).

## Purpose

Part B fixes, before conversion, how the v2 package is built from the source's own released values, and what it must contain:
- the 2.0 structure: measurements, observables, systems, the uncertainty-terms table and the descriptor (D-083, D-084);
- the uncertainty terms read at source in step A (`docs/sources/uncertainty-readings.md` §3, §3b, §3c; the term rows E1–E30 in `readings/xcop-e22-2026-11-03/reader-A.md` and `reader-B.md`);
- the system-scale "choice of mass model" term that part A A7 fixed;
- the handling of the seven clusters without stellar data (part A A8 stage 1; D-090 rule 4);
- an independent second reading, frozen before conversion;
- the consent gate (D-090 rule 5).

**Values are the source's own** (part A §5): g_obs = GOBS and g_bar = GBAR from the five `gbar_gobs_<C>.fits` files. X-COP is the one exception to D-083 item 3 (D-090 rule 1), so v2 is not compared with v1's values.

## Rules applied

1. **Which rows (part A §5; D-091 erratum; D-092).**
   - Every row of the five `gbar_gobs` files is a v2 measurement row: A644 19, A1795 21, A2029 22, A2142 20, A2319 27, **109 rows** (part A result, A1). Part A's "105" and "exactly 21" are the erratum D-091 records; the count here is the files' own.
   - A644's 19 rows are included and carry D-092's note (item 9).
   - **D-096 rule 2 (excluded data), as limited by D-098 rule 1.** If the frozen reading finds that E22 excludes some of these released rows from its own analysis of the radial acceleration relation (for example rows outside the "$[0.01-2]R_{500}$" range of l. 528), those rows are recorded, not plotted, with the quotation in `notes`. Which R500 the source uses for that range is read at source. If the source does not say, the question goes to JvH before conversion; the conversion never chooses.
   - **D-096 rule 1 and rule 3.** The reading records, for E22 and every file used, whether the source marks a preferred value or names a fiducial baseline among the values it releases. The archive releases one GOBS and one GBAR per radius, so no change is expected. A conflict with part A or an earlier ruling goes to JvH before conversion.
2. **The seven clusters without stellar data** (A85, A1644, A2255, A3158, A3266, RXC1825, ZW1215; part A A8 stage 1, D-090 rule 4).
   - **No measurement rows and no observables rows in v2.** Part A left the observables question to part B. They get none, because:
     - no measurement row would cite them (D-029 records the inputs of a row);
     - their only g_bar is a bound below the central value, which standard 2.5.1 cannot hold (part A A8 (a));
     - A8's stage-1 check failed (A3158), so stage 2 is blocked (#129).
   - **Systems table:** all twelve clusters are listed (item 8).
   - **Exclusion register:** each of the seven gets one row in `data/registry/excluded.csv`, with `dataset` = `aeg-d-xcop/v2`, the reason exactly as part A A8 fixed it ("stellar mass not in the source; g_bar bounded below by gas only; recorded under D-090") and the citation "Eckert et al. 2022, A&A 662, A123 (arXiv 2205.01110v1), l. 103, 114, 402".
3. **D-087.** `model_dependence` = `none` on every row: GOBS is the non-parametric reconstruction "evaluate[d] … at the radii of the observed data" (E22 l. 263), the paper's benchmark (l. 366), and GBAR's fitted forms (Sérsic, gNFW) interpolate or extend measured profiles (D-087 item 1). E22 l. 458 says g_obs used "both the nonparametric reconstruction and the results of the Einasto fit to the DM component only". If the reading finds at source that the released GOBS is the Einasto curve, `model_dependence` is `total_mass_form` on those rows; that finding is recorded in the frozen reading, never decided at conversion.
4. **D-097 does not apply.** D-025, which D-097 implements, governs g_obs from a velocity dispersion. The hydrostatic assumption is carried instead as the `hse_bias` and `nonthermal_pressure` terms (item 7). Part A §5 already fixes A2319: plotted, with its hydrostatic-validity quotation on every row (item 9).
5. **The consent gate (D-090 rule 5).** Building, converting and scoring are done in the open. Publishing v2's rows waits for the authors' consent.
   - **Until consent,** v2's tables (`tables/*.ecsv`) are written by `convert.py` but not committed: the conversion pull request adds `data/packages/aeg-d-xcop/v2/tables/` to `.gitignore`. The committed package holds the test, result, reading files, `convert.py`, `sources.json`, `datapackage.json`, the descriptor and `checksums.sha256` (hashes only, no rows).
   - The site loads only committed tables, so v1 stays live on the map, its dataset page and its downloads. The deployed site is built from the repository without running conversions.
   - **v1's dataset page** shows, generated from v2's descriptor key `x_publication` = `awaiting_authors_consent`: "Version 2, built from Eckert et al. 2022, is ready and awaiting the authors' confirmation." v1's files are not edited.
   - **Publication** is a later pull request that commits the tables and sets `x_publication` = `published`. It needs JvH's ruling recording the authors' answer, and `03c` sent first (D-092 rule 4).
   - The result is published like part A's: outcomes, counts and ratios, no rows.

## Order of work (against steering)

1. **The second reading** (item 11) is done before the first v2 conversion run, by a reader with no access to `convert.py`, any v2 table or v1's tables. It writes to `v2/reading/`:
   - `values.json`: the reader's own parse of the five `gbar_gobs_<C>.fits` files (RADIUS, GBAR, GBAR_ERR, GOBS, GOBS_ERR_LO, GOBS_ERR_HI per row), as **hashes only**. The parsed rows are written to the gitignored `v2/source/reading/values.csv`, because the archives are not redistributed (D-004; D-090 rule 5). The file's SHA-256 is recorded under `off_repo` in the freeze record.
   - `error_form.md`: the meaning of the error columns, read from the FITS headers, and if not stated there, decided by the rule in item 5.
   - `d096.csv`: D-096 fields (preferred, excluded, fiducial) per source and file, with quote and location, including E22's stated radial range for the relation and the R500 it is defined with.
   - `err_levels.csv`: the confidence level of GOBS_ERR_* and GBAR_ERR as stated, with quote and location, or `not_given_by_source`.
   - `properties.csv`: per cluster, from the published papers, with quote and location: the centroid shift w and its error (Paper II, arXiv 2205.01123v1, `tab2.tex`); the non-thermal pressure fraction α at R500 and at R200 with its 1σ errors (Ettori & Eckert 2022, arXiv 2112.07554, Table 1, "at $1 \sigma$ c.l.", l. 276).
   - `hse_statements.csv`: every statement in E22 and Paper II about a cluster's hydrostatic validity, with quote and location. These are notes (rule 4), not exclusions.
   - `resolutions.md`.
2. **Disagreements** with step A, part A or this test's expectations are resolved at source by a session with no access to any v2 table, and recorded in `resolutions.md`. A conflict under rule 1 goes to JvH.
3. **Freezing the reading.** The SHA-256 of every committed reading file, and of the off-repo `values.csv`, goes into `data/frozen/xcop-v2-reading.json`, by a pull request merged before the first conversion run.
4. **Conversion.** `convert.py` takes D-096 changes, the error form, confidence levels, cluster properties and hydrostatic notes **only** from the frozen reading files, and its values only from the archives verified by hash (part A §1). It contains no cluster-specific rule of its own, apart from what this test names.

## The test

### A. Values and tables

1. **Rows.** v2 has exactly 109 measurement rows, the rows of the five `gbar_gobs` files in file order (A644, A1795, A2029, A2142, A2319, as in part A §1), with `system_id` from `data/registry/systems.csv` (v1's IDs for these clusters) and `measurement_id` `aeg-d-xcop/v2/m000001` onward. `kind` = `profile_point`, `channel` = dynamics, `method_class` = hydrostatic, as v1.
2. **Values.** On every row, compared with the reader's off-repo `values.csv`:
   - `r_kpc` = RADIUS, `r_kind` as v1;
   - `g_obs` = GOBS and `g_bar` = GBAR, as float64 of the FITS values, bit for bit;
   - the error columns as item 5 sets them;
   - `g_bar_stars`, `g_bar_gas_cold` and `g_bar_gas_hot` are **empty**: the archive releases g_bar as a total. The Einasto files reproduce GBAR for four clusters only (part A A2), so components are not split out in v2. `stars_status` and `gas_hot_status` are `measured` (E22 l. 103–114, 142–156), and `gas_cold_status` is v1's.
3. **Changed values.** Nothing is compared with v1 (D-090 rule 1). Any row recorded and not plotted under rule 1 is listed in the result with the quotation and the source's reason. A plotting change not traceable to the frozen reading is a fail.
4. **Arithmetic.** For each row, `observed_from` and `baryonic_from` name its two observables (item 8), and `g_obs` and `g_bar` equal those observables' values exactly.

### B. Uncertainties (standard 2.5.1 §2a, §3, §7a)

5. **Error columns and confidence levels.**
   - **Error form.** If the FITS headers state what GOBS_ERR_LO, GOBS_ERR_HI and GBAR_ERR are, that governs. If not, the reader decides by this rule, fixed now: the GOBS pair is read as bounds if GOBS_ERR_HI > GOBS on every row, as error magnitudes if GOBS_ERR_HI < GOBS on every row, and otherwise "undetermined"; GBAR_ERR is read as a magnitude if GBAR_ERR < GBAR on every row, and otherwise "undetermined". **Undetermined is a fail of this item**, and the question goes to the authors.
   - **`g_obs_err_lo`, `g_obs_err_hi`** are the magnitudes (GOBS − lower bound and upper bound − GOBS if bounds). **`g_bar_err_lo` = `g_bar_err_hi`** = the GBAR_ERR magnitude.
   - **Scales (§2a rule 6).**
     - `g_obs_err_point_*` = `g_obs_err_*`: GOBS_ERR is the per-radius posterior (E1). Its correlation between radii is not released (term `radial_covariance`).
     - `g_bar_err_point_*` are **empty**: GBAR_ERR mixes point-scale gas errors with the central galaxy's mass-to-light error, which is "constant with radius" (E22 l. 111; E18), a system-scale term. The term `g_bar_point` records that the source gives no point-scale part.
   - **Confidence levels.** `err_level`, `err_level_status`, `g_bar_err_level` and `g_bar_err_level_status` come from `err_levels.csv`. Expected: `not_given_by_source` on both sides (part A §5; question 6 of the part A result). A level is never read as 0.683 by default (D-093 rule 1).
6. **New extension columns** (standard 2.5.1 §12). Each header names the term that uses it and says what an empty value means.
   - **Systems table:** `x_xcop_alpha_nt_r500`, `_r500_err`, `x_xcop_alpha_nt_r200`, `_r200_err` (Ettori & Eckert 2022 Table 1, as fractions; from `properties.csv`; all twelve clusters); `x_xcop_centroid_w`, `_err` (Paper II Table 2; all twelve); `x_xcop_mass_model_frac` (item 7, the five clusters only, empty for the seven).
   - **Measurements table:** `x_xcop_r500_tot_kpc` (Table 1 R500,TOT of the row's cluster, part A §2), used only to state the row's radius in units of R500 in `notes` where rule 1 needs it.
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly the rows below.
   - Each cites its source at the location given, from the step A readings (`reader-A.md`, `reader-B.md`, E1–E30) and §3b–§3c of `uncertainty-readings.md`, which serve as the D-031 second reading of these sizes.
   - `covariance` is `not_published` on every row.
   - **One sizing rule for every row,** as in the dwarf, globular-cluster and lens tests: a size is `given` only where the source states it for these clusters, or for a class that contains them (the X-COP sample). Otherwise the row is `not_given_by_source`, and any figure stated elsewhere goes in the note. `given_by_other_source` is used where the size is stated for these clusters by another paper of the same programme (Ettori & Eckert 2022; Loubser et al. 2020; Ghizzardi et al. 2021).
   - **One exception, fixed by part A:** `mass_model_choice` takes its size from part A A7, which computed it from the source's own two released profiles and fixed it as this term ("These ratios become the system-scale 'choice of mass model' term in v2's uncertainty table", part A l. 202). It is `given`, and its note says it is computed by the Atlas from the source's files, not stated by the source. See open item O2.
   - **`size_unit`** is given on every `given` or `given_by_other_source` row.
   - **`applies_to`.** `*` is every system in the package (twelve). The five clusters with rows are "the five": `aeg-s-000177;aeg-s-000179;aeg-s-000180;aeg-s-000181;aeg-s-000183` (A644, A1795, A2029, A2142, A2319). A listed subset has `scale = dataset` (§7a, 2.4.0), so point- and system-scale rows use `*`; the seven clusters have no measurement rows, so such a term reaches the five only, and any `size_column` is empty for the seven.
   - **Not uncertainty terms (§2a rule 4):** spherical symmetry and hydrostatic equilibrium as the method's assumptions are registry assumptions, as in v1 (`xray_hse_bias` carries the bias; item 7 registry).
   - **Left out, with reasons:** E10's "10–20 % each" (l. 508) summarises the separate effects below, so it would count them twice; E15 (parametric priors) and E17 (miscentering, A2255) concern methods or clusters without rows; E28 and E29 (Table 4 fraction errors) are at overdensity radii, not per row, and are already in GBAR_ERR.

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `radial_covariance` | point | * | g_obs | not_given_by_source | — | — | E1, E2: the SZ covariance is "accounted for and propagated" (E22 l. 91, 97), but no covariance between radii is released |
| `g_bar_point` | point | * | g_bar | not_given_by_source | — | — | Item 5: GBAR_ERR mixes scales; the source gives no point-scale part |
| `np_smoothing` | point | * | g_obs | not_given_by_source | — | — | E14: "fluctuations on scales smaller than the bin size are suppressed" (E22 l. 235) |
| `reconstruction_bias` | dataset | the five | g_obs | given | 0.05, `upper_bound`, fraction | — | E12: the non-parametric technique "follows the true profile with minimal bias (<5\%)" (E22 l. 311), from mock validation of the method on the X-COP setup. NFW ≤ 3 % and Einasto ≈ +6 % in the note |
| `hse_bias` | dataset | the five | g_obs | given | 0.10, `upper_bound`, fraction | `xray_hse_bias` | E5: "we conclude that our measurements are mildly biased ($<10\%$) out to $R_{500}$. The HSE assumption is likely to be a poorer approximation beyond this point" (E22 l. 502). Larger beyond R500: 10–20 % at R200 (l. 539; E6). In the note: simulations "5-30\%" at R500 (E3, l. 502); 10–15 % below weak lensing (E4, l. 502); A2319 "known to be strongly biased" (E7, l. 502). One-sided: hydrostatic g_obs is biased low. Never applied as a correction |
| `nonthermal_pressure` | system | * | g_obs | given_by_other_source | `size_column` `x_xcop_alpha_nt_r500` (R200 value in `x_xcop_alpha_nt_r200`), `as_released`, fraction of total pressure | — | Ettori & Eckert 2022 Table 1, "at $1 \sigma$ c.l." (l. 276); computed from the 2019 thermal-only masses (l. 182), so it is another analysis of the same clusters. Median trend: "$b(0.1 R_{500}) \approx 0.5 b(R_{500})$" (l. 377). Overlaps `hse_bias`; the two are not added. Never applied as a correction (§3c) |
| `gas_inhomogeneity` | dataset | the five | g_obs | given | 0.10, `upper_bound`, fraction | — | E8: "the impact of gas inhomogeneities is small ($<10\%$)" (E22 l. 504); temperature inhomogeneities "$\sim10\%$" (l. 311). Would also move the gas mass, and so g_bar; that effect is not stated |
| `xmm_calibration` | dataset | the five | g_obs | given | 0.15, `as_released`, fraction | — | E9: "effective area calibration (15\%)" (E22 l. 311); "reaches $\sim20\%$ for 10 keV plasma … mostly affects the regions located inside $0.5 R_{500}$" (l. 506) |
| `mass_model_choice` | system | * | g_obs | given | `size_column` `x_xcop_mass_model_frac`, `as_released`, fraction | — | Part A A7 (fixed there as this term): \|GP/Einasto − 1\| at R500 from R3, per cluster: A644 0.033, A1795 0.031, A2029 0.042, A2142 0.014, A2319 0.006 (part A result, A7). Computed by the Atlas from the source's two released profiles, not stated by the source. E22's sample statement in the note: methods "within 3\%" in median over [0.05–2]R500 and NFW against NP "less than 10\% at all radii" (l. 373). Paper II's Einasto against NFW M500 in the note (§3b). Never applied as a correction |
| `hse_validity_outskirts` | point | * | g_obs | not_given_by_source | — | — | E30: "although the validity of the HSE assumption at large radii is unclear" (E22 l. 373) |
| `cosmology` | dataset | * | both | not_given_by_source | — | — | E22 adopts H0 = 67.8, Ω_m = 0.308 (l. 56); its central-galaxy and satellite sources assume H0 = 73 and 70, and harmonisation is not stated (§3.2 item 3). No alternative is tested by the source; the distance dependence is not computed in v2 |
| `gas_density_conversion` | dataset | the five | g_bar | not_given_by_source | — | — | The conversion from X-ray emissivity to gas density is not stated (§3.1) |
| `bcg_ml` | system | * | g_bar | not_given_by_source | — | — | E18: dynamical mass-to-light ratio; its error is dominated by the weak-lensing mass and "constant with radius" (E22 l. 111). Photometry "$< 0.25$ mag arcsec$^{-2}$" and kinematics "$\pm4.7$ per cent" are inputs, not the size of this term |
| `bcg_dm_component` | dataset | `aeg-s-000177;aeg-s-000183` (A644, A2319) | g_bar | given | 0.083, `as_released`, fraction | — | E19: "When a DM mass component is included in the dynamical mass models for the BCGs, the best fitting $\Upsilon_{* \rm DYN}$ decrease by 8.3 $\pm$ 2.9 per cent on average" (E22 l. 109). For A644 and A2319, which had no weak-lensing mass, "the average DM distribution (of the 23 other clusters …)" was used (l. 109; reader B). An average; the reading confirms the systems |
| `bcg_jam_geometry` | dataset | the five | g_bar | given_by_other_source | 0.15, `upper_bound`, fraction | — | E20: "changing our cylindrically-aligned JAM models to spherically-aligned JAM models, results in the best-fitting $\Upsilon_{\star \rm DYN}$ parameters changing by up to $\sim$ 15 per cent" (Loubser et al. 2020, l. 547) |
| `bcg_sersic_extrapolation` | system | * | g_bar | not_given_by_source | — | — | E21: measured "only within a limited radial range out to $\sim50$ kpc", then a Sérsic form (E22 l. 404) |
| `satellite_cosmic_variance` | system | * | g_bar | not_given_by_source | — | — | E22 term: estimated with Moster et al. 2011 (E22 l. 116); shown separately by Ghizzardi (l. 705), no size stated in E22 |
| `satellite_flux` | system | * | g_bar | not_given_by_source | — | — | E23: bootstrap of the fluxes (Ghizzardi l. 712); no size stated |
| `satellite_gnfw_smoothing` | system | * | g_bar | not_given_by_source | — | — | E24: the profiles are "quite noisy and not smooth" and fitted beyond 100 kpc with a gNFW of fixed shape (E22 l. 408); which parameter set is not stated (§3.2 item 1) |
| `satellite_projection` | system | * | g_bar | not_given_by_source | — | — | E25: whether the satellite profile was deprojected is not stated (§3.2 item 1; #124). Ghizzardi: "75$\%$ of the mass obtained integrating along the line of sight lies within the sphere with radius $R_{500}$" (l. 715). Part A A6 (undetermined) and A9 (1.86–2.42 against Ghizzardi's spherical masses) in the note and on every row (item 9) |
| `satellite_imf` | dataset | the five | g_bar | given_by_other_source | 0.60, `upper_bound`, fraction | — | E26: "our comparison shows that we may be underestimating stellar masses by as much as 60\%" (Ghizzardi et al. 2021). A Salpeter IMF gives a factor ∼2 (in the note). One-sided, upward |
| `icl_omitted` | dataset | the five | g_bar | given | 0.05, `upper_bound`, fraction of the baryon budget | — | E27: "the contribution of ICL to the total baryon budget is expected to be small ($<5\%$)" (E22 l. 410). One-sided, upward. Replaces v1's `icl_fraction` slider in v2 (item 7 registry; open item O3) |

   - **Registry update for v2** (`data/assumptions.json`).
     - **`xray_hse_bias`** gains an `aeg-d-xcop/v2` entry with v1's formula on `g_obs`, `g_obs_err_lo`, `g_obs_err_hi` and `g_obs_err_point_*`, v1's default 0 and range 0–0.2. It stays the one slider (open item O3). The check of item 12 runs it.
     - **`icl_fraction`** gets no v2 entry: its v1 formula scales `g_bar_stars`, which v2 does not have (item 2). Its effect is stated by the term `icl_omitted`.
     - **`stars_cluster_modelled`** (v1, draft) gets no v2 entry: v2's stars come from the source.
     - New entries: none.

### C. Structure and flags

8. **Tables.**
   - **Observables** (`tables/observables.ecsv`), two per measurement row:
     - `observed`, `acceleration_released` = GOBS, unit `m / s2`, with the error columns of item 5, steps `xray;projected_t_and_density;deprojected_profiles;hydrostatic_mass;newtonian_g`; `source_ref` names the file and row and states "non-parametric hydrostatic reconstruction evaluated at the radii of the data (E22 §3.4, l. 263); g_obs = G M_HSE(<r)/r² (l. 453)".
     - `baryonic`, `acceleration_released` = GBAR, unit `m / s2`, with GBAR_ERR, steps `xray;deprojection;mass;photometry;stellar_ml;newtonian_g`; `source_ref` names the file and row and states "G (M_gas + M★,BCG + M★,sat)(<r)/r² (E22 l. 456); ICL excluded (l. 410)".
     - `r_kpc` = RADIUS; `err_level` and `err_level_status` as item 5.
   - **Systems** (`tables/systems.ecsv`): all twelve clusters, v1's `system_id`s, `taxonomy_kind` and `kind_label` as v1, `redshift` from part A §2 (Table 1), the item 6 columns, and `properties` holding Table 1's R500,TOT, M500,TOT and M200,TOT (part A §2) and a `status`: `plotted` for the five, `recorded_not_plotted` for the seven (rule 2).
   - **Plotting.** All 109 rows `plotted = true`, `role = default`, except rows recorded and not plotted under rule 1 by the frozen reading (`not_plotted_reason = other`, quotation in `notes`). No alternative rows.
9. **Named items.**
   - **A644 (D-092).** Every A644 row's `notes` and its system page carry D-092's expert-layer note exactly; the page also carries the plain-layer note. Both are checked by a text search of the built page (HTML unescaped). The row flag `reproduction_mismatch` and known issue #136.
   - **A2319 (part A §5).** Every A2319 row's `notes` carries the hydrostatic-validity quotation from the frozen `hse_statements.csv` (E22 l. 435, l. 502; Paper II l. 80).
   - **Stellar projection (part A §5).** Every row's `notes` states "stellar projection: undetermined (part A, A6); stellar normalisation against Ghizzardi et al. 2021: <the cluster's A9 ratio> (part A, A9)", with the A9 ratios as published: A644 2.04, A1795 1.86, A2029 2.42, A2142 2.27, A2319 2.25. Known issue #124.
   - **Centroid shift (part A §5)** is in the systems columns of item 6 (continuous, never a label).
   - **Known issues** (`known_issues.json`): #136 (A644); #124 (projection); #129 (stage 2 blocked); a new issue for A3158's negative masses at 18–30 kpc (part A A8), on the system only; and the D-091 erratum, linked from the result.
   - **Exclusion page text.** The seven clusters' "Recorded, not plotted" text on their system pages states the register's reason, not D-097's equilibrium wording. Checked by a text search of each built page, once v2 is published (before that, the register rows exist but the pages show v1).
10. **Descriptor.**
    - `standard_version` `2.5.1`;
    - `x_publication` `awaiting_authors_consent` (rule 5);
    - `x_value_change_ruling`: not set, because rule 1 (D-090) exempts X-COP from the v1 comparison; `x_precedence` cites D-089 and D-090 rule 1;
    - `x_second_reading` points to `SECOND_READING.md` and the frozen reading files;
    - `x_baryon_inventory`: hot gas `measured`; central galaxy `measured`; satellites `measured`; intracluster light `stated_negligible` (E22 l. 410, quoted); cold gas as v1.
    - `sources.json` lists both archives with part A's hashes (and their members' hashes, recorded at conversion as part A §1 says), E22, Paper II and Ettori & Eckert 2022 with their e-print hashes, licence "not stated; asked (#19)" for the archives, and `redistributable: false` for the archives.
11. **Second reading (D-031 item 3).** One independent reader, as in the order of work.
    - **Pass:** the package equals the frozen reading on every field it holds: `values.csv` against `r_kpc`, `g_obs`, `g_bar` and the observables' values (bit for bit); the error form and magnitudes against the error columns; `err_levels.csv` against the level columns; `properties.csv` against the item 6 columns; `d096.csv` against the plotting of rule 1. Any mismatch is a fail.
12. **Standard and site,** run with the tables present locally (they are not committed; rule 5):
    - `PYTHONPATH=pipeline python -m aeg.validate data/packages/aeg-d-xcop/v2` passes under 2.5.1;
    - `PYTHONPATH=pipeline python -m aeg.formula_check` passes, including `xray_hse_bias`'s v2 entry;
    - the site builds, and `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes;
    - `git ls-files data/packages/aeg-d-xcop/v2/tables` is empty (rule 5);
    - the built page of X-COP v1's dataset shows the rule 5 sentence (text search, HTML unescaped).
13. **v1 untouched.** Every file in `aeg-d-xcop/v1/` has the checksum it had at commit `5dc4091`.

**Pass** = all thirteen hold. Anything else is a fail. Part A's result stands beside it, unchanged.

## Not tested here

- Whether the source's error sizes are right.
- Part A's checks. They stand as run (D-091).
- How A644's GBAR was built, the units and R_Δ behind Table 4, the stellar projection, and A3158's negative masses: all with the authors (part A result, questions 1–6).
- The seven clusters' g_bar, and stage 2 (#129).
- The X-COP v2 audit (D-090 rule 3), written and frozen after v2 ships.

## Open items for JvH before this test is frozen

- **O1. Observables for the seven clusters.** Part A left this to part B. **Recommended: none in v2** (rule 2), because no row would cite them, their only g_bar is a bound the standard cannot hold, and stage 2 is blocked. The alternative, writing their 200-row gas and total-mass profiles as observables with no measurement rows, would publish values from privately shared files with no use on the site.
- **O2. The `mass_model_choice` size** is computed by the Atlas (part A A7), where the one sizing rule asks for a size the source states. **Recommended: keep it**, because part A, frozen, fixed it as this term, and the note says plainly how it was computed. The alternative is `given` 0.10 from E22's sample statement (l. 373), with the A7 ratios in the note.
- **O3. Sliders.** **Recommended:** `xray_hse_bias` carries over as v1's one slider on g_obs; `icl_fraction` does not, because v2 has no stellar component to scale (item 2), and E22 states ICL as below 5 % (term `icl_omitted`). Dropping a v1 slider changes what the site lets readers do, so it needs a ruling.
- **O4. Rule 1's radial range.** If the reading finds E22's "[0.01–2]R500" is an exclusion of released rows from its relation, rows beyond it (part A shows A1795 reaching 2.11 × Table 1's R500, A2029 1.99) are recorded, not plotted. **Recommended:** accept that outcome mechanically if the source states it and names its R500; otherwise put it to JvH with the quote before conversion.

## Checked before freezing (revision 1, 2026-11-05)

A mock package was built with placeholder values (not data): 109 measurement rows over the five clusters with the item 5 columns (`g_bar_err_point_*` empty; levels empty with status `not_given_by_source`), the twelve systems with the item 6 columns, and the 22 terms above parsed from this file.
- **Validator:** `validate_v22` and `validate_v24` at 2.5.1 report 0 problems. The full `validate()` was not run on the mock, because it has no descriptor, observables, sources or checksums; item 12 runs it on the real package.
- **Not exercised:** the `xray_hse_bias` v2 registry entry (item 12 runs `formula_check` on it), the site text checks and the consent gate.
- **No archive value was read for this revision.** Every quoted number comes from E22, Paper II or Ettori & Eckert 2022 as read in step A, or from the published part A result. The mock and its script are not committed.
