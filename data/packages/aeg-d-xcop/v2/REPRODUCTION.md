# aeg-d-xcop/v2: reproduction test, part A (source reproduction)

**Status: draft, revision 4, for JvH's approval.** It is frozen only after D-090 is ruled, because A3 and A8 rest on it. On merge, this file's SHA-256 is recorded in `data/frozen/xcop-v2-part-a.json`. The archives' values are read only after that.

**Written** 2026-11-03 under D-089, then revised after an independent review of revision 1 (`docs/sources/readings/xcop-e22-2026-11-03/test-review.md`). Revision 3 put A8 in two stages. Revision 4 answers a second independent review, of revision 3 (`test-review-2.md` in the same folder).

**Seen so far: no value in the two source archives has been read.** What has been seen:
- archive sizes and SHA-256;
- member names, sizes and dates (`tar -tv`);
- FITS extension names, column names, units (TTYPE and TUNIT) and row counts.

The `<cluster>_BCG.txt` files (about 50 lines each) have not been opened.

**If a check fails,** the failure is published and the test is not changed to pass (operating rule 5).

**Part B** covers structure under data standard 2.4.0: the observables table, the uncertainty-terms table, the descriptor fields, and an independent second reading. It is written and frozen after standard 2.4.0 (plan step B). Part B reads no source value.

## 1. Sources

Both archives were shared by D. Eckert on 2026-11-03 and retrieved the same day.

| Archive | URL | Bytes | SHA-256 |
|---|---|---|---|
| `data_E22.tar.gz` | https://drive.switch.ch/index.php/s/nKxwcKwftb3Esjc/download | 161 298 | `ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d` |
| `mbar.tar.gz` | https://drive.switch.ch/index.php/s/tzaoqQEnNm8Y3jb/download | 157 262 | `0420a7edba60da7f2df6aa4f38cbb21135ab50949d579176a8c893bab712c496` |

**Licence.** None is stated, and it has been asked of the authors (#19). Until it is answered, the archives are fetched at build time and verified by hash. They are never committed or redistributed (D-004).

**Reference publication ("E22").** Eckert, Ettori, Pointecouteau, van der Burg & Loubser 2022, A&A 662, A123. LaTeX source: arXiv 2205.01110v1, e-print SHA-256 `18fc2e80…c7d8`, file `hydromass.tex`. The reading is in `docs/sources/uncertainty-readings.md` §3, §3b and §3c. Line numbers below refer to `hydromass.tex`.

**Members, as listed by `tar -tv`.** The member list is fixed by the archive hash; the individual member SHA-256 values are recorded in `sources.json` at conversion.

- **`data_E22.tar.gz`:** 20 files, each listed with its date.
  - The folders `A644/`, `A1795/`, `A2029/`, `A2142/` and `A2319/` each hold four files:
    - `gbar_gobs_<C>.fits`, dated 2023-04-20;
    - `GP_thermo.fits`, dated 2022-04-25;
    - `EIN3_bar_mass.fits`, dated 2022-05-31;
    - `<C>_BCG.txt`, dated 2022-05-31.
  - `gbar_gobs_<C>.fits`: 21 rows. Columns RADIUS [kpc]; GBAR, GBAR_ERR, GOBS, GOBS_ERR_LO and GOBS_ERR_HI [m/s^2].
  - `GP_thermo.fits` (extension `THERMODYNAMIC PROFILES`): 200 rows. Columns R_IN, R_OUT and R_REF, then P_TOT, T3D, TSPEC, NE, K, T_COOL and LAMBDA, each with _LO and _HI. No units.
  - `EIN3_bar_mass.fits` (extension `MASS PROFILE`): 200 rows. Columns R_IN, R_OUT and R_REF, then MASS, M_DM, MGAS and FGAS, each with _LO and _HI, and M_STAR. **M_STAR has no error column.** No units.
- **`mbar.tar.gz`:** 17 files.
  - `GP_mass.fits` (extension `MASS PROFILE`, 200 rows, dated 2021-09-15) in each of the folders `a85/`, `a644/`, `a1644/`, `a1795/`, `a2029/`, `a2142/`, `a2255/`, `a2319/`, `a3158/`, `a3266/`, `rxc1825/` and `zw1215/`. Columns R_IN and R_OUT, then MASS, MGAS and FGAS, each with _LO and _HI. No R_REF, no stellar mass, no units.
  - `EIN3_bar_mass.fits` (dated 2021-09-16) in `a644/`, `a1795/`, `a2029/`, `a2142/` and `a2319/`. They are expected to be identical to the `data_E22` copies; A1 checks this.

## 2. Reference values (transcribed from E22; transcription independently verified on 2026-11-03)

**Cosmology** (l. 56): "Planck 2015 ΛCDM", with H₀ = 67.8 km s⁻¹ Mpc⁻¹ and Ω_m = 0.308.
- Flatness is an inference: the Planck 2015 baseline is flat, but l. 56 does not say so.
- No radiation term is included (T_CMB = 0).
- ρ_c(z) = 3H(z)²/(8πG), with H(z) = H₀ √(Ω_m(1+z)³ + 1 − Ω_m) and G from `astropy.constants`.

**Table 1** (`tab:master`, l. 324–335). The R500,TOT and M500,TOT values come from NFW fits; the caption is at l. 316. Errors are as printed.

| Cluster | z | R500,TOT [kpc] | M500,TOT [10¹⁴ M☉] | M200,TOT [10¹⁴ M☉] |
|---|---|---|---|---|
| A644 | 0.0704 | 1398 (−16/+16) | 7.80 (−0.27/+0.26) | 10.97 (−0.43/+0.45) |
| A1795 | 0.0622 | 1160 (−6/+6) | 4.42 (−0.07/+0.07) | 6.04 (−0.11/+0.11) |
| A2029 | 0.0766 | 1340 (−9/+9) | 6.91 (−0.14/+0.14) | 9.29 (−0.21/+0.22) |
| A2142 | 0.09 | 1453 (−9/+9) | 8.93 (−0.16/+0.17) | 13.33 (−0.30/+0.32) |
| A2319 | 0.0557 | 1424 (−4/+5) | 8.12 (−0.08/+0.08) | 11.61 (−0.14/+0.14) |

**Table 4** (`tab:fbar`, l. 424–428). Values are in per cent, ± the quoted error. The caption (l. 417) begins "Relative contribution of gas and stars as well as the total baryonic fraction at several overdensity radii…". l. 433 defines f_bar(r) = M_bar(<r)/M_tot(<r).

| Cluster | f_gas,2500 | f★,2500 | f_bar,2500 | f_gas,500 | f★,500 | f_bar,500 | f_gas,200 | f★,200 | f_bar,200 |
|---|---|---|---|---|---|---|---|---|---|
| A644 | 7.7±0.1 | 1.2±0.4 | 8.9±0.5 | 12.8±0.6 | 1.3±0.5 | 14.1±1.1 | 16.9±1.2 | 1.5±0.6 | 18.4±1.7 |
| A1795 | 9.6±0.1 | 1.7±0.6 | 11.3±0.6 | 13.4±0.3 | 1.3±0.5 | 14.7±0.7 | 15.8±0.5 | 1.3±0.4 | 17.1±1.0 |
| A2029 | 11.1±0.1 | 2.8±0.9 | 13.8±1.1 | 14.4±0.3 | 2.1±0.7 | 16.5±1.0 | 17.1±0.7 | 2.0±0.7 | 19.1±1.4 |
| A2142 | 12.0±0.1 | 2.3±0.8 | 14.3±0.9 | 14.1±0.2 | 1.7±0.6 | 15.8±0.8 | 14.7±0.5 | 1.5±0.5 | 16.2±1.0 |
| A2319 | 9.2±0.1 | 2.0±0.7 | 11.3±0.8 | 17.0±0.2 | 1.5±0.5 | 18.5±0.7 | 24.9±0.5 | 1.5±0.5 | 26.4±1.0 |

The table's f_bar is not always f_gas + f★: for A2029, 11.1 + 2.8 ≠ 13.8, and for A2319, 9.2 + 2.0 ≠ 11.3. So each column is taken as its own published estimate.

**Defining equations** (l. 453 and l. 456):
- g_obs = G M_HSE(<r)/r²
- g_bar = G (M_gas + M★,BCG + M★,sat)(<r)/r²

**Published stellar masses for the reported check A9.** Ghizzardi et al. 2021 (arXiv 2007.01084v1), Table 2, M★,500, already corrected to a sphere by their factor 0.75 (l. 715). Units 10¹² M☉:
- A644: 3.70
- A1795: 3.02
- A2029: 6.51
- A2142: 6.97
- A2319: 5.11

## 3. Rules, fixed now

- **R1. Radius convention.** Each 200-row file gives R_IN and R_OUT (and R_REF in the Einasto and thermodynamic files). Which radius the cumulative masses refer to is not stated.
  - Check A2 is run under two conventions: **(a)** masses at R_REF (Einasto file) and R_OUT (non-parametric file, which has no R_REF); **(b)** masses at R_OUT in both files.
  - The convention A2 selects (§4, A2) is then used in A4, A6, A7 and A9. If A2 selects none, convention (a) is used and this is stated. For `GP_mass.fits` both conventions mean R_OUT.
  - **Exception: A3 and A8.** These compare `GP_mass.fits` with the `gbar_gobs` files, and a radius-labelling error alone could move their ratios by several per cent. They use the geometric midpoint √(R_IN·R_OUT) of `GP_mass.fits` and widen their tolerance by the grid step (A3).
  - Interpolation between rows is linear in log M against log r.
  - **There is no extrapolation:** a radius outside a file's grid is reported as untestable.
- **R2. Units of the files without TUNIT.** Radii are taken in kpc and masses in M☉. This is accepted only if A4 passes. If A4 fails under these units, no other units are tried, and the units question goes to the authors.
- **R3. Overdensity radius.**
  - **Definition.** R_Δ (Δ = 2500, 500, 200) is the radius at which M(<r)/(4/3 π r³) = Δ ρ_c(z). It uses the cluster's own Einasto file MASS at the R1 radius, and its Table 1 redshift.
  - **Root-finding.** Linear interpolation in log[mean density] against log r, between the two bracketing rows. The mean enclosed density decreases outward, so the crossing is unique. If there is no crossing inside the grid, the entry is "not computable" and counts as a fail in A4.
  - **Table 1's R500,TOT** (NFW) is used only in the reported variant of A4 and in A5.
- **R4. Fractions at R_Δ, in per cent.**
  - **f_gas:** the file's **FGAS** column is primary. MGAS/MASS is reported as a secondary estimate and cannot turn a fail into a pass.
  - **f★:** M_STAR/MASS. Only central values are tested, because M_STAR has no error column, so the published f★ errors cannot be reproduced from the files.
  - **f_bar:** FGAS + f★.

## 4. Checks

**A1. Completeness and structure (pass/fail).** All of the following must hold:
- the archive SHA-256 values equal §1;
- the members and columns are as listed in §1;
- each `gbar_gobs` file has exactly 21 rows, with RADIUS in kpc and the accelerations in m/s²;
- all GBAR, GOBS and error values are finite;
- GBAR and GOBS are positive;
- the Einasto files in the two archives are identical.

If A1 fails, the other checks still run wherever the files allow, and the failure is reported with them.

**A2. Is g_bar built from gas plus the file's stars? (pass/fail; it also selects the R1 convention).**
- For every row, compute ratio = GBAR / [G (gas + M_STAR)(<RADIUS)/RADIUS²]. M_STAR always comes from the cluster's Einasto file. The gas comes from either:
  - **(i)** MGAS in the Einasto file; or
  - **(ii)** MGAS in the non-parametric `GP_mass.fits`.
- With the two radius conventions of R1, that makes four variants, all reported.
- **A variant passes for a cluster** if |median ratio − 1| ≤ 0.02 over its testable rows, and every testable row has |ratio − 1| ≤ 0.05.
- **A2 passes** if one variant passes for all five clusters. If more than one does, the selected variant is the first passing one in the order (a)(i), (a)(ii), (b)(i), (b)(ii).
- **Reason for the tolerances.** Leaving the stars out changes g_bar by about 10 % near R500 and much more in the core. The tolerances therefore test whether the stars are included, and are not sensitive to the radius-labelling question (about 1.5 % between neighbouring grid radii).
- **Also reported:** each cluster's median ratio under every variant. A fail is investigated in the open; it does not stop the other checks.

**A3. g_obs and gas against the non-parametric profiles (reported; it also fixes whether the seven A8 clusters may ever be plotted).**
A3 does not pass or fail v2. Its **stage-2 condition** is pass/fail.
- **Why.** The seven A8 clusters have only the 2021 `GP_mass.fits` profiles. The five complete clusters have both those and the `gbar_gobs` values. So the five show whether the 2021 profiles agree with the analysis behind GOBS and GBAR, for total mass **and** for gas.
- **Radius.** For each `gbar_gobs` row, `GP_mass.fits` is interpolated (R1) at the geometric midpoint of R_IN and R_OUT. **The grid step** δ of a cluster is the median of ln(R_OUT/R_IN) over its rows. A mass read half a step off, with a local slope d ln M/d ln r ≤ 2, is off by at most δ. So δ is added to every tolerance below. The step is not known now. If δ > 0.05 for any of the five, the condition fails, because the grid is then too coarse to test it.
- **Testable rows.** Rows inside the `GP_mass.fits` grid. A cluster needs at least 10 testable rows for the total-mass part and at least 5 for the gas part, or the condition fails for that cluster.
- **Total mass.** ratio_tot = GOBS / [G MASS_GP(<r)/r²].
- **Gas.** ratio_gas = MGAS_GP(<r) / [GBAR r²/G − M_STAR(<r)]. M_STAR comes from the Einasto file under the A2-selected convention. Only rows where M_STAR < 0.5 GBAR r²/G are used, so that the subtraction cannot become noisy or negative in the star-dominated core.
- **The stage-2 condition**, for every one of the five clusters:
  - |median ratio_tot − 1| ≤ 0.05 + δ, and every testable row has |ratio_tot − 1| ≤ 0.10 + δ;
  - |median ratio_gas − 1| ≤ 0.05 + δ, and every testable row has |ratio_gas − 1| ≤ 0.10 + δ.
- **Reason for the thresholds.** E22 states that its mass methods agree to "less than 10% at all radii" (NFW against NP, l. 373) and "within less than 10%" over 0.2–1 R500 (l. 263). The per-row 0.10 is therefore the paper's own method-agreement scale. The median must sit at half of it, so the seven are plotted only if the 2021 profiles track the 2023 analysis more closely than two different methods are expected to. A2's tighter 0.02 tests something else: whether the stars are included in GBAR, a term of 10 % or more.
- **Also reported:** every ratio; the per-cluster median and maximum; GOBS / [G MASS_EIN3(<r)/r²] from the Einasto file, because E22 says it used "both the nonparametric reconstruction and the results of the Einasto fit" for g_obs (l. 456). A failure can then be told apart from "GOBS is the Einasto curve".
- **If the condition fails,** the seven stay unplotted. The question goes to the authors, their answer is recorded, and any change is a JvH ruling in the decision log. The thresholds above are never changed.

**A4. Reproduce E22 Table 4 (pass/fail).** For each of the 45 entries, computed under R1–R4:
- **f_gas and f_bar:** pass if |Atlas − Table 4| ≤ quoted error + 0.05 percentage point (half a printed unit, for rounding).
- **f★:** pass if |Atlas − Table 4| ≤ quoted error + 0.05. Only the central value is tested (R4).
- **Pass overall:** all 45 entries are within.
- **Also reported:** every difference; the number of entries within 0.1 percentage point; the same comparison with R_Δ taken from Table 1's NFW R500,TOT (Δ = 500 only); and the secondary MGAS/MASS estimate.
- **Stated limitation.** Some quoted errors are 0.1 percentage point, and f_gas changes by about 0.1 percentage point when R_Δ shifts by 2 %. So A4 also tests whether the files' R_Δ matches the paper's. A fail may come from the R_Δ definition rather than the data; it is still reported as a fail.

**A5. Overdensity radius (reported).** R500 from R3 is reported against Table 1's R500,TOT. Table 1's value comes from an NFW fit, and E22 does not say which R_Δ Table 4 uses, so a ratio different from 1 is not an error.

**A6. Functional form of the stellar mass (decision rule; the outcome is decided by the data only).**
- **Question.** Does M_STAR(r) in the Einasto file have the form of an enclosed mass within a sphere (3D), or within a projected cylinder (2D)?
- **Models.** M_STAR is noise-free model output, so the test is exact functional reproduction. Over **all** grid rows of each cluster, fit:

  M_STAR(r) = M_Sérsic(<r; ρ₀, r_e, n) + N · S_X(r; R200, α)

  - **M_Sérsic** is the enclosed 3D mass of E22's central-galaxy density, ρ₀ exp{−b_n((r/r_e)^{1/n} − 1)} (l. 406), with ρ₀, r_e and n free. b_n follows the standard Sérsic convention (Ciotti & Bertin 1999 approximation).
  - **S_X** is the generalised-NFW satellite profile of van der Burg et al. 2015, ρ ∝ (r/r_s)^(−α)(1 + r/r_s)^(α−3), with r_s = R200/c, in one of two forms:
    - X = 3D: the mass enclosed within a sphere;
    - X = 2D: the mass within a cylinder, projected along the full line of sight.
  - **Free:** N > 0 and R200 (with c fixed, so r_s = R200/c).
  - **Fixed:** (c, α), in turn at each of the two published sets: (0.64, 1.63), the stellar-mass-density fit, and (0.72, 1.64), the number-density fit used by Ghizzardi.
  - **Fit:** least squares in ln M_STAR.
- **Verdict, per cluster and parameter set.**
  - "3D" if rms(3D) ≤ 1×10⁻³ and rms(2D) ≥ 5 × rms(3D).
  - "2D" in the mirror case.
  - Otherwise "undetermined".
  - The fitted R200 is reported against Table 1's M200,TOT radius.
- **Overall.** "3D" or "2D" if at least four of the five clusters give that verdict under at least one parameter set and no cluster gives the opposite verdict. Otherwise "undetermined", and the question goes to the authors.
- **Limits.**
  - E22 l. 408 points to its gNFW as "Eq. \ref{eq:gnfw}". That equation (l. 218–222) is a five-parameter **pressure** profile, so the exact form E22 used for the satellites is itself uncertain.
  - **A6 establishes the functional form of M_STAR in the file, not whether its normalisation was deprojected.** A 3D-shaped profile is consistent both with correct deprojection and with a 3D model fitted directly to projected cumulative masses. That question stays with the authors (#124).

**A7. Model dependence of the total mass (reported).** At R500 from R3, report each pair of the following as a ratio, for the five clusters:
- `GP_mass.fits` MASS (non-parametric);
- Einasto-file MASS (Einasto plus baryons);
- Table 1's M500,TOT (NFW; the caption, l. 316, calls it the fit to "DM plus baryons").

These ratios become the system-scale "choice of mass model" term in v2's uncertainty table. They are never applied as a correction.

**A8. The other seven clusters, in two stages (under D-090).**
- **Who they are:** A85, A1644, A2255, A3158, A3266, RXC1825 and ZW1215.
- **What they lack:** they have **no complete stellar budget in E22, and no M_STAR in any shared file**. A85 and ZW1215 do have published satellite stellar masses (Ghizzardi Table 2), but no central-galaxy profile in E22.
- **What they have:** hydrostatic total mass and gas mass profiles in `GP_mass.fits` (2021), which Eckert offered "if you still wish to include the mass profiles for all systems" (email of 2026-11-03).
- **The bound.** E22 defines g_bar as gas plus central galaxy plus satellites (l. 456), each non-negative, and leaves out intracluster light. So G MGAS(<r)/r² is a bound below the source's **central** g_bar for this gas profile. It is not a confidence limit and carries no confidence level.
- **Stage 1, in v2: recorded, not plotted.**
  - The seven are listed in the observables table only, with the reason "stellar mass not in the source". **v2 has no measurement rows for them**, because the current standard cannot hold a g_bar limit.
  - The checks below are run and published in v2's result.
- **Stage 2, in a later dataset version (v3 or after): plotted as lower-limit tracks.** It needs all three of:
  - (a) a data standard (planned for 2.4.0) that allows a bound on g_bar, with errors on g_obs kept, and states that it is a bound on the central value, not a confidence limit;
  - (b) the site requirements below, met and checked in screenshots on desktop and phone;
  - (c) A3's stage-2 condition, and every stage-1 check below, passed.

  Released rows are never changed, so stage 2 is a new version. **Any failed stage-1 check blocks stage 2** until it is resolved in the open. Stage 2 is tracked in issue #129.
- **Site requirements for stage 2**, all fixed now:
  - **Tracks, not points.** The 200-row grid is not tied to the radii of the data, unlike the five clusters' 21 rows. So the seven are drawn as lines, with the g_obs _LO/_HI range as a band.
  - **The arrow's direction** in every view is derived from how that view's quantity changes when g_bar increases at fixed g_obs: horizontal toward higher g_bar on g_obs against g_bar; diagonal (slope −1 in log–log) on g_obs/g_bar or g_obs − g_bar against g_bar; vertical downward on g_obs/g_bar against radius. A view whose quantity does not change monotonically with g_bar leaves the tracks out.
  - **Limit rows are excluded** from population averages, binned summaries, fits and the inputs of every frozen pattern test.
  - **Downloads** carry the limit explicitly on every row.
  - **The arrows and bands are readable without colour.**
- **Rows beyond the source's range** are never drawn. E22 says the NP method "cannot be extrapolated outside of the fitted range" (l. 263) and states its range as 0.01–2 R500 (l. 528). For the seven, rows outside 0.01–2 × Table 1's R500,TOT are flagged `beyond_source_range`. This range is Claude's inference from E22 and is asked of the authors.
- **Stage-1 checks (pass/fail):**
  - **Rows:** each of the seven `GP_mass.fits` has 200 rows, and MASS and MGAS are positive on every row inside the source's range.
  - **Monotonic:** MASS and MGAS do not decrease outward inside the source's range (they are enclosed masses).
- **Reported only:** |FGAS − MGAS/MASS| per row. In broad, skewed posteriors the median of a ratio need not equal the ratio of medians, so a difference here is not an error.

**A9. Stellar normalisation against Ghizzardi et al. 2021 (reported; no threshold).**
- At R500 from R3, report M_STAR(<R500) from the Einasto file divided by Ghizzardi's spherical M★,500 (§2).
- Also report the same ratio with M_Sérsic(<R500) from A6 subtracted, under each parameter set.
- **Expectations, stated before reading the files.** Spherical stellar masses on the same basis would give about 1. Projected masses would give about 1/0.75 ≈ 1.33.
- **Already visible in the published tables** (Claude's arithmetic, on E22 f★,500 × Table 1 M500,TOT against Ghizzardi, no files):
  - A1795: 1.9
  - A644: 2.7
  - A2029: 2.2
  - A2142: 2.2
  - A2319: 2.4

  The central-galaxy methods differ (E22 uses a dynamical mass-to-light ratio; Ghizzardi uses SED fitting with the central galaxy included), so the ratio mixes several effects. It is reported, flagged to the authors with #124, and never used to correct anything.

## 5. What v2 plots (default rows), fixed now

- **Plotted in v2:** the 105 rows of the five `gbar_gobs` files.
  - g_obs = GOBS, with errors GOBS_ERR_LO and GOBS_ERR_HI.
  - g_bar = GBAR, with error GBAR_ERR.
  - Radii in kpc, as released.
- **Error confidence levels.** These are not stated in the files or in E22. They are stated as "not given by the source" until the authors answer, and asked of them with the next note.
- **Parametric files:** used only for the checks and the uncertainty terms.
- **Recorded on every row:**
  - the source's centroid shift w and its error, from Paper II Table 2 (§3b of the readings), as a continuous quantity;
  - the source's hydrostatic-validity caveat for A2319 (E22 l. 435, l. 502), as a quotation.
- **The stellar term's projection** is stated on every row of the five clusters as A6's verdict, or as "undetermined", together with A9's normalisation ratio.
- **The seven A8 clusters** have no rows in v2 (A8 stage 1). If stage 2 is reached, they are added in a new version.

## 6. What the result establishes

**It establishes:**
- whether the released g_bar is gas plus the file's stellar mass (A2);
- whether the files reproduce the paper's published baryon fractions, which also tests the assumed units and the R_Δ definition (A4);
- the functional form of the stellar term (A6);
- whether the 2021 non-parametric total and gas profiles agree with the analysis behind GOBS and GBAR, to within E22's own method-agreement scale (A3).

**It does not establish:**
- whether the stellar normalisation was deprojected (A6, A9);
- the confidence level of the released errors;
- that the 2021 non-parametric run is the analysis behind GOBS (A3 also reports the Einasto alternative);
- the g_bar of the seven A8 clusters. Their gas-only value is only a bound below the central value;
- that the hydrostatic masses are free of bias. That is a stated uncertainty term, not a check.
