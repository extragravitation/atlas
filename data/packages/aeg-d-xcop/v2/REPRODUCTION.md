# aeg-d-xcop/v2: reproduction test, part A (source reproduction)

**Status: draft for JvH's approval. Frozen on merge, before any value in the source files is read.**

Written 2026-11-03 under D-089. No value in the two source archives has been read:

- **Seen:** file names, sizes, FITS extension names, column names and units (TTYPE, TUNIT), and row counts.
- **Opened by nobody:** the `<cluster>_BCG.txt` files, which are about 50 lines each.

If a check fails, the failure is published and the test is not changed to pass (operating rule 5). Under D-019 a package may still ship with the affected rows flagged, if JvH rules so.

**Part B** (structure under data standard 2.4.0: the observables table, the uncertainty-terms table, descriptor fields, and an independent second reading) is written and frozen after standard 2.4.0 (plan step B). Part B reads no source value, so writing it later does not compromise this freeze.

## 1. Sources

Both archives were shared by D. Eckert on 2026-11-03 and retrieved the same day.

| Archive | URL | Bytes | SHA-256 |
|---|---|---|---|
| `data_E22.tar.gz` | https://drive.switch.ch/index.php/s/nKxwcKwftb3Esjc/download | 161 298 | `ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d` |
| `mbar.tar.gz` | https://drive.switch.ch/index.php/s/tzaoqQEnNm8Y3jb/download | 157 262 | `0420a7edba60da7f2df6aa4f38cbb21135ab50949d579176a8c893bab712c496` |

**Licence.** No licence is stated; it has been asked of the authors (#19). Until it is answered, the archives are fetched at build time and verified by hash, never committed or redistributed (D-004).

**Reference publication.** Eckert, Ettori, Pointecouteau, van der Burg & Loubser 2022, A&A 662, A123 ("E22"). The LaTeX source is arXiv 2205.01110v1, e-print SHA-256 `18fc2e80…c7d8`, file `hydromass.tex`. Reading: `docs/sources/uncertainty-readings.md` §3. Line numbers below refer to that file.

**Archive contents.** These were seen as listed. The member SHA-256 values are recorded in `sources.json` at conversion.

`data_E22.tar.gz`. For each of A644, A1795, A2029, A2142 and A2319 (upper-case folders):

| File | Rows | Columns |
|---|---|---|
| `gbar_gobs_<C>.fits` | 21 | RADIUS [kpc], GBAR, GBAR_ERR, GOBS, GOBS_ERR_LO, GOBS_ERR_HI [m/s^2] |
| `GP_thermo.fits` (extension `THERMODYNAMIC PROFILES`) | 200 | R_IN, R_OUT, R_REF; P_TOT, T3D, TSPEC, NE, K, T_COOL and LAMBDA, each with _LO and _HI. **No units.** |
| `EIN3_bar_mass.fits` (extension `MASS PROFILE`) | 200 | R_IN, R_OUT, R_REF; MASS, M_DM, MGAS and FGAS, each with _LO and _HI; M_STAR (**no error column**). **No units.** |
| `<C>_BCG.txt` | about 50 lines | Not opened |

`mbar.tar.gz`:
- `GP_mass.fits` for all 12 clusters (lower-case folders; extension `MASS PROFILE`, 200 rows). Columns: R_IN, R_OUT; MASS, MGAS and FGAS, each with _LO and _HI. **No R_REF, no stellar mass, no units.**
- The same five `EIN3_bar_mass.fits`, **byte-identical** to those in `data_E22` (same SHA-256).

## 2. Reference values (transcribed from E22)

**Cosmology** (l. 56): flat ΛCDM, H₀ = 67.8 km s⁻¹ Mpc⁻¹, Ω_m = 0.308. The critical density is ρ_c(z) = 3H(z)²/(8πG), with H(z) = H₀ √(Ω_m(1+z)³ + 1 − Ω_m) and G from `astropy.constants`.

**Table 1** (`tab:master`, l. 324–335): redshift z, R500,TOT [kpc] and M500,TOT [10¹⁴ M☉], for the five clusters.

| Cluster | z | R500,TOT | M500,TOT |
|---|---|---|---|
| A644 | 0.0704 | 1398 (−16/+16) | 7.80 (−0.27/+0.26) |
| A1795 | 0.0622 | 1160 (−6/+6) | 4.42 (−0.07/+0.07) |
| A2029 | 0.0766 | 1340 (−9/+9) | 6.91 (−0.14/+0.14) |
| A2142 | 0.09 | 1453 (−9/+9) | 8.93 (−0.16/+0.17) |
| A2319 | 0.0557 | 1424 (−4/+5) | 8.12 (−0.08/+0.08) |

**Table 4** (`tab:fbar`, l. 424–428): per cent, ±quoted error. The caption (l. 417) says "Relative contribution of gas and stars as well as the total baryonic fraction at several overdensity radii". The text (l. 433) defines f_bar(r) = M_bar(<r)/M_tot(<r) for the decomposition analysis (l. 402).

| Cluster | f_gas,2500 | f★,2500 | f_bar,2500 | f_gas,500 | f★,500 | f_bar,500 | f_gas,200 | f★,200 | f_bar,200 |
|---|---|---|---|---|---|---|---|---|---|
| A644 | 7.7±0.1 | 1.2±0.4 | 8.9±0.5 | 12.8±0.6 | 1.3±0.5 | 14.1±1.1 | 16.9±1.2 | 1.5±0.6 | 18.4±1.7 |
| A1795 | 9.6±0.1 | 1.7±0.6 | 11.3±0.6 | 13.4±0.3 | 1.3±0.5 | 14.7±0.7 | 15.8±0.5 | 1.3±0.4 | 17.1±1.0 |
| A2029 | 11.1±0.1 | 2.8±0.9 | 13.8±1.1 | 14.4±0.3 | 2.1±0.7 | 16.5±1.0 | 17.1±0.7 | 2.0±0.7 | 19.1±1.4 |
| A2142 | 12.0±0.1 | 2.3±0.8 | 14.3±0.9 | 14.1±0.2 | 1.7±0.6 | 15.8±0.8 | 14.7±0.5 | 1.5±0.5 | 16.2±1.0 |
| A2319 | 9.2±0.1 | 2.0±0.7 | 11.3±0.8 | 17.0±0.2 | 1.5±0.5 | 18.5±0.7 | 24.9±0.5 | 1.5±0.5 | 26.4±1.0 |

**Defining equations** (l. 453, 456):
- g_obs = G M_HSE(<r)/r²
- g_bar = G (M_gas + M★,BCG + M★,sat)(<r)/r²

## 3. Interpretation rules, fixed now

- **R1. Radius column.** In `EIN3_bar_mass.fits`, the cumulative masses are taken at **R_REF**. In `GP_mass.fits`, which has no R_REF, they are taken at **R_OUT**; for check A3 only, the result at √(R_IN·R_OUT) is also reported. Interpolation between rows is linear in log M against log r.
- **R2. Units of files without TUNIT.** Radii are taken as kpc and masses as M☉. This is accepted only if A4 passes. If A4 fails under these units, no other units are tried; the units question goes to the authors.
- **R3. Overdensity radius.** R_Δ for Δ = 2500, 500 and 200 is computed from each cluster's own `EIN3_bar_mass.fits` MASS profile and its Table 1 redshift. R_Δ is the smallest r at which the mean enclosed density M(<r)/(4/3 π r³) falls to Δ ρ_c(z). Table 1's R500,TOT is used only in the report (A5).
- **R4. Fractions.** f_gas = MGAS/MASS, f★ = M_STAR/MASS and f_bar = (MGAS + M_STAR)/MASS, all at R_Δ, in per cent.

## 4. Checks

**A1. Completeness and structure (pass/fail).**
- Each archive's SHA-256 equals §1.
- The members are exactly those listed in §1.
- Each `gbar_gobs` file has exactly 21 rows and the six columns, with RADIUS in kpc and the accelerations in m/s².
- Every GBAR, GOBS and error value is finite, and GBAR and GOBS are positive.
- `EIN3_bar_mass.fits` is identical in both archives.

**A2. g_bar is built from the stated components (pass/fail).** For every one of the 105 rows:

  |GBAR − G (MGAS + M_STAR)(<RADIUS)/RADIUS²| / GBAR ≤ 0.01

Here MGAS and M_STAR come from the same cluster's `EIN3_bar_mass.fits` (R1, R2). This tests whether the released g_bar is the gas plus the file's stellar mass. A failure is reported per cluster with the median ratio, and investigated in the open. It does not stop the other checks.

**A3. g_obs against the non-parametric mass (reported; no threshold).** For every row, report GOBS / [G MASS(<RADIUS)/RADIUS²], with MASS from the same cluster's `GP_mass.fits` (R1). That file is dated 2021, and the `gbar_gobs` files 2023. The papers give no basis for expecting the two to agree exactly, so no threshold is set.

**A4. Reproduce E22 Table 4 (pass/fail).** For each of the 45 entries (5 clusters × 3 radii × 3 fractions), computed under R1–R4:

  |Atlas − Table 4| ≤ the quoted error

Pass means all 45 entries are within. Also reported, without a threshold: every difference, and how many entries agree within 0.1 percentage point. This check also tests the units assumption R2.

**A5. Overdensity radius (reported).** R500 from R3 is compared with Table 1's R500,TOT for the five clusters, as ratios. E22 does not state that Table 4 uses either one.

**A6. Projection of the stellar mass (decision rule; outcome by the data only).**

This decides whether M_STAR in `EIN3_bar_mass.fits` is enclosed within a sphere (3D) or within a projected cylinder (2D).

- **Fit range.** For each cluster, use the rows with 0.2 R500 ≤ R_REF ≤ 1.5 R500, with R500 from R3. In this range the central galaxy is enclosed whole and the satellites dominate the change in M_STAR.
- **Models.** Fit M_STAR(r) = K + N · S(r), with K ≥ 0 and N > 0 free, using:
  - **(3D)** S(r) = the enclosed mass within a sphere of radius r;
  - **(2D)** S(r) = the mass within a cylinder of radius r, projected along the full line of sight.

  Both are for the generalised NFW density ρ ∝ (r/r_s)^(−α) (1 + r/r_s)^(α−3), with r_s = R200/c, R200 from R3, and the two published parameter sets of van der Burg et al. 2015:
  - (c, α) = (0.64, 1.63), the stellar-mass density fit;
  - (c, α) = (0.72, 1.64), the number-density fit used by Ghizzardi et al. 2021.

  The fit is least squares in log M_STAR, with equal weights.
- **Decision**, per cluster and per parameter set:
  - **3D** if rms(2D)/rms(3D) ≥ 2;
  - **2D** if rms(3D)/rms(2D) ≥ 2;
  - otherwise **undetermined**.
- **Overall result.**
  - "**3D**" or "**2D**" if at least four of the five clusters give the same verdict under both parameter sets.
  - Otherwise "**undetermined**". In that case the question goes to the authors, and v2 carries the stellar term with the projection stated as unknown.

**A7. Model dependence of the total mass (reported).** At R500 from R3, report MASS from `GP_mass.fits` (non-parametric) against MASS from `EIN3_bar_mass.fits` (Einasto plus baryons) for the five clusters, and against Table 1's M500,TOT. These ratios become the system-scale "choice of mass model" term in v2's uncertainty table. They are never applied as a correction.

**A8. Coverage of the 12 clusters (structure only).**
- Each `GP_mass.fits` has 200 rows with positive MASS.
- The seven clusters without stellar data (A85, A1644, A2255, A3158, A3266, RXC1825, ZW1215) **have no M_STAR in any shared file**.
- So, under D-089 rule 1 ("included only where their baryons are stated by the source"), these seven get **no g_bar in v2**. Their total and gas mass profiles are recorded as observables, but they are not plotted on the g_obs–g_bar map. **This is a choice for JvH to confirm when approving this test**, because v1 plotted all 12 clusters.

## 5. What v2 plots (default rows), fixed now

- **Plotted:** the 105 rows of the five `gbar_gobs` files.
  - g_obs = GOBS with GOBS_ERR_LO and GOBS_ERR_HI.
  - g_bar = GBAR with GBAR_ERR.
  - Radii in kpc, as released.
- **Not used for plotted values:** none of the parametric files. They serve only the checks above and the uncertainty terms.
- **Recorded on every row:**
  - the source's centroid shift w, from Paper II Table 2 (§3b of the readings), as a continuous quantity;
  - the source's hydrostatic-validity caveat for A2319 (E22 l. 435, 502), as a quotation.

## 6. What the result establishes

**Establishes:**
- that the released g_obs and g_bar follow the paper's stated definitions (A2);
- that the shared files reproduce the paper's published baryon fractions (A4);
- whether the stellar term is spherical (A6).

**Does not establish:** that the hydrostatic masses are free of bias. That is a stated uncertainty term, not a check.
