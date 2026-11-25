# Strong lenses (aeg-d-strong-lensing/v3): how each row is computed

This text is meant to be complete for every row of `tables/measurements.ecsv`. Its arithmetic, and the selection rules where the tables allow, are checked against every published row by `pipeline/tests/test_methods_text.py`. Whether a reader who does not know the code can follow it is tested only by the independent audit (D-116). The code is `v1/convert.py` with `pipeline/aeg/lensing.py`, carried unchanged in value through v2 and v3. Where this text and the code differ, the error is in this text; please report it.

**Record numbers.** Sources are named here by the record numbers of the A6 reading (R5, R10 and so on). Each entry in `sources.json` gives its record in the field `record`. For example, R5 is S1, S2, S9 and S29, and R13 is S3 and S10.

A row's `source_ref` reads "observed Rm; stellar Rn": the observed side comes from record Rm, the stellar side from record Rn. Its locator rule names the observables rows the row uses, and each of those has its own `source_ref` and locator, with the table and column.

**Within a table,** the row is the lens's own row, by the name the source prints.

## 1. Constants and units

| Quantity | Value | Source |
|---|---|---|
| G | 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻² | CODATA 2018 (stated in code) |
| M☉ | 1.98840987 × 10³⁰ kg | IAU 2015 nominal (stated in code) |
| 1 pc | 3.0856775814913673 × 10¹⁶ m; 1 kpc = 10³ pc, 1 Mpc = 10⁶ pc | IAU 2015 B2 |
| c | 299 792 458 m s⁻¹ | exact |
| 1″ | π / (180 × 3600) rad; angles enter every formula in radians | |
| H₀ | km s⁻¹ Mpc⁻¹ → s⁻¹: H₀ × 10³ / (10⁶ pc in m) | |

## 2. Steps

1. **Distances,** in a flat ΛCDM cosmology with the H₀ and Ω_m the source states (§3), radiation neglected:
   - E(z) = √(Ω_m (1+z)³ + 1 − Ω_m);
   - D_C(z) = (c/H₀) ∫₀^z dz′ / E(z′), by Simpson's rule with 2000 intervals; any accurate integral gives the same result;
   - D_l = D_C(z_l) / (1 + z_l) and D_s = D_C(z_s) / (1 + z_s);
   - D_ls = (D_C(z_s) − D_C(z_l)) / (1 + z_s).
2. **Einstein radius:** R_E = θ_E D_l, in kpc. Where the source prints R_E in kpc (R32), the printed value is used.
3. **Einstein mass:**
   - **Printed:** where the observed record prints M_E, it is used as printed, converting log₁₀ values where the source prints them so.
   - **Printed aperture mass:** where the record prints a mass inside an aperture and the aperture is taken as the Einstein radius (R61, for SNL-1 and SNL-2), that mass and aperture are used.
   - **Computed:** otherwise M_E = θ_E² c² D_s D_l / (4 G D_ls).
   - **θ_E** is the SIE Einstein radius exactly as printed: `bSIE` (R5), `b_SIE` (R10), or the record's own column. It is used with no axis-ratio correction.
4. **Stellar mass inside R_E,** by the route in §3:
   - **printed inside R_E:** used as printed, in the unit the table states; R13's `MChaBC2` is in units of 10¹⁰ M☉. It is used at the precision printed;
   - **profile:**
     - M★(<R_E) = M★,total × f, where f = P(2n, b_n (θ_E / R_e)^(1/n)) is the fraction of a Sérsic profile's light inside a cylinder of radius θ_E;
     - R_e and n are those of the source's light profile, with n = 4 for de Vaucouleurs;
     - P is the regularised lower incomplete gamma function, and b_n solves P(2n, b_n) = ½, to a relative tolerance of 10⁻¹⁰ (b₄ = 7.669249…);
     - θ_E and R_e are both in arcsec, and R_e is used as printed, with no circularisation;
   - **L × Υ:** M★(<R_E) = L(<R_E) × Υ, both printed by the source, with the luminosity inside the same aperture.

   The stellar mass is always at the source's default IMF: Chabrier, or the source's own fixed IMF. The Salpeter value is the upper end of the IMF slider only.
5. **Gas inside R_E** (D-076 item 1; registered term `a6s_gas_in_RE`):
   - **hot gas:** M_gas,hot = 0.0012 × M★(<R_E), with a range of 0.00015 to 0.025;
   - **cold gas:** M_gas,cold = 0 × M★(<R_E), with a range of 0 to 0.02.
   - It is never derived from the observed side.
   - Where a source states that gas is negligible, the registered term still applies, and the source's statement is kept as a quoted assumption (flag `gas_negligible_source_assumption`).
6. **Accelerations in projection** (D-064), with M in M☉ times M☉ in kg, and R_E in m:
   - g_obs = G M_E / R_E²;
   - g_bar = G (M★(<R_E) + M_gas,hot + M_gas,cold) / R_E²;
   - g_bar_stars, g_bar_gas_hot and g_bar_gas_cold are the three terms.

**Inputs listed but not used in a row's value.**
- **Salpeter stellar masses** (for example R13's `MSalBC2`): the upper end of the IMF slider only.
- **R5's R_e** on SLACS rows: carried for the profile alternative and for the record.
- **Redshifts, θ_E or masses** that the stellar record also prints (R13 prints its own z_l, z_s and θ_E): not used. The observed record's values are used, as the route table says.
- **z_s on rows whose M_E is printed:** used only for the redshift rule in §4.

## 3. Routes, by record pair

| `source_ref` | Rows | Observed side | R_E | Stellar route | Cosmology (H₀ km s⁻¹ Mpc⁻¹, Ω_m) |
|---|---:|---|---|---|---|
| observed R5; stellar R13 | 48 | θ_E (R5 Table 5 `bSIE`) → M_E computed; z_l and z_s from R5 Table 4 (`zFG`, `zBG`) | computed | printed inside R_E: R13 `MChaBC2` (Chabrier, BC03) | 70, 0.3 (R5), flat |
| observed R10; stellar R10 | 37 | M_E printed (R10 Table 2, log₁₀ M_Ein) | computed from θ_E (Table 2 `b_SIE`) | profile: R10 Table 2 total M★ (Chabrier, log₁₀), de Vaucouleurs R_eff from R10 Table 1 | 70, 0.274 (R10), flat |
| observed R20; stellar R20 | 2 | θ_E (R20 Table 6) → M_E computed; z from R21 Table 2 | computed | profile: R20 Table 7 total M★ (Chabrier), de Vaucouleurs R_eff from R20 Table 4 | 70, 0.3 (R20), flat |
| observed R61; stellar R61 | 2 | M(≤ R_ap) printed (R61 Table 2, adopted mass), with R_ap (Table 1) as the Einstein radius | computed from R_ap | L × Υ: R61 Table 1 L_F814W(≤ R_ap) × the Υ of R61 §5 | 70.4, 0.272 (R61), flat |
| observed R32; stellar R32 | 2 | M_E printed (R32 Table 1) | printed in kpc (R32 Table 1) | L × Υ: R32 Table 1 L_Ein × Υ_ref of R32 §5 | not needed: R32 names its cosmology only |
| observed R28; stellar R26 | 1 | M_E printed (R28 Table 3); z_l in the CMB frame | computed from θ_E (R28 Table 3) | L × Υ: R26 Table 1 L_r,Ein × (M★/L_r)_MW | 70.4, 0.272 (R26 adopts R25's distances), flat |
| observed R29; stellar R29 | 1 | M_E printed (R29 §4), with θ_E the image half-separation (R29 §3); z in the CMB frame (R29 §4) | computed | L × Υ: R29 §4 aperture luminosity × Υ_Ref | 70.4, 0.272 (R29), flat |
| observed R30; stellar R30 | 1 | M_E printed (R30 §3.5) | computed from θ_E (R30 §5) | printed inside R_E: R30 §3.2 M★,Chab | 67.8, 0.308 (R30; flatness not stated, taken as flat) |

**Places.** The table and column of every input are given above and in the locator rules of `locators.json`.

**Cosmology.** Each record's cosmology is read in its own paper; the paper is in `sources.json` under the same record:
- R5: arXiv:0805.1931v1 §1, last paragraph;
- R10: arXiv:1711.00072v2 §1, last paragraph;
- R20: arXiv:1307.4764v1 §1, last paragraph;
- R28: §1, last paragraph;
- R26: adopts the distances of R25, which takes WMAP7 (R25 §1);
- R61: §1;
- R29: §4, paragraph 2 (arXiv v1 p. 3);
- R30: §1.

**Lens names.** Sources print names differently, for example `SDSSJ0946+1006` and `J0946+1006`. A lens is matched across records by its J-coordinate name.

**SLACS errors.** For the SLACS rows (R5) no per-lens θ_E error is printed. The survey-wide adopted error of 2 % (R5 Table 3, §6.1) is used for the uncertainty only.

## 4. Which lenses have a row, and which are plotted

1. **A confirmed lens of early type, by the source's own label:**
   - SLACS (R5): grade A only (`grade A`);
   - R10: a classification beginning with E;
   - a morphology code `E`, or a description naming an elliptical, E/S0 or early-type galaxy.

   Other lenses are recorded in the systems table with the reason (D-063 items 5 and 6).
2. **Spectroscopic redshifts:** the lens and source redshifts are both measured spectroscopically. That is, the source describes them as spectroscopic, or (R29) measured them with MUSE. A redshift the source describes as an estimate, a z_FP or a fundamental-plane value does not count (D-063 item 5).
3. **Redshift cut:** the observed record's printed z_l is below 0.30 (D-066). Lenses at or above it are recorded, with the flag `epoch_gap_v1`.

Lenses that fail any of these rules have no default row.

## 5. Uncertainties shown with a row

These do not enter g_obs or g_bar.

- **Computed M_E:**
  - m_e_lo = M_E [1 − ((θ_E − δθ_lo)/θ_E)²];
  - m_e_hi = M_E [((θ_E + δθ_hi)/θ_E)² − 1].
- **θ_E's error moves to g_bar** on rows where θ_E sets both sides (data standard §2a rule 7; v2 item 2).
- **g_bar error:** the stellar-mass error, scaled the same way as M★.
- **Distance errors** are not added.
- **System- and dataset-scale terms** are in `tables/uncertainty_terms.ecsv`.
