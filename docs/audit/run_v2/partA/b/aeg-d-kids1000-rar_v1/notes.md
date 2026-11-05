# Reader B notes: aeg-d-kids1000-rar_v1

## Scope and isolation
- Read only the packet (`rows.csv`, `method/`, `sources/brouwer2021_rar_members/`). No arXiv e-print downloaded; no web access used.
- Member hashes (SHA-256, computed here): Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt 5343d81c…78a9; Fig-4-C1_RAR-GAMA-isolated_Nobins.txt b6134252…70d74; Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt 5f81078…928fe; README.txt b3680580…8645.
- "data row N" taken as the N-th non-comment line (file line N+1, after the `#` header). Each file has exactly 15 data rows.

## Why every row is "method incomplete"
The written method (methods_page.txt and SOURCE.md) says:
- g_obs = 4 G ΔΣ (singular isothermal sphere deprojection);
- g_bar = point mass of stars plus cold gas within the measurement radius; stars and cold gas are not separately released;
- units carry h70, with h = 0.7 taken "as the source does".

Missing steps:
1. **No value of G and no unit conversion.** ΔΣ is printed in h70 M☉ pc⁻². To get m s⁻² you need G and either M☉ and pc in SI, or G in pc-based units and pc in metres. The method gives none of these. The brief forbids taking constants from anywhere other than the method.
2. **Bias correction not stated for ΔΣ.** The methods page says only that the g_obs *uncertainty* is "bias-corrected, as released". It does not say whether ESD_t is divided by the released `bias(1+K)` column before applying 4GΔΣ. The README says it "should always be applied", but the README is a source, not the method. The correction is about 1.5 %.
3. **No rule for g_bar from the release.** The method defines g_bar physically (M★ + M_cold gas as a point mass), but those masses are not released. The method never says g_bar is to be read from the released first column, `Radius(m/s^2)`. The README describes that column only as "the mean projected distance from the lens center; … in meter-per-second-squared for the RAR data". It does not call it g_bar.

## Other observations (for the coordinator)
- **The hotgas file.** Rows m000019, m000021 and m000028 come from `Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt`. The filename suggests the g_bar binning includes a hot-gas term. The method's g_bar definition (stars + cold gas only) does not mention hot gas, and neither the method nor the README explains the hotgas file. If the Atlas uses this file, the method text does not describe what g_bar contains.
- **The first column holds bin values, not sample means.** It is identical, digit for digit, across all three files (KiDS, GAMA and KiDS-hotgas) and is log-spaced (ratio ≈ 1.764). That points to bin centres, not per-sample means as the README's word "mean" implies. The covmatrix headers label it `Radius[i](mps2/h70)`, so the g_bar axis itself scales with h70. The method does not say how h enters g_bar.
- **Unit typo in the README.** The README prints `G[pc^3/(Msun*s^2)] = 4.52e-30 pc^2/(Msun*s^2)`. The bracketed unit (pc³) and the trailing unit (pc²) disagree. Only pc³ M☉⁻¹ s⁻² is dimensionally right with the extra factor [pc/m].
- **The h70 convention.** ESD_t is printed in h70 M☉ pc⁻². With h = 0.7, h70 = 1 and the value is used as printed. The method states h = 0.7, so this step is covered.

## Supplementary computation (not the audit result)
`supplementary_readme_constants.csv` gives g_obs from the README's Eq. 7 (G = 4.52e-30 pc³ M☉⁻¹ s⁻², pc/m = 3.086e16, ESD_t / bias). Next to it is the printed first column, taken as g_bar. It is there only so the coordinator can see what follows if the README constants are adopted into the method. It breaks the brief's rule on constants and must not be compared as reader output. `values.csv` is the audit result.

## Inputs recorded
Per measurement: `Radius` (col 1), `ESD_t` (col 2), `error` (col 4) and `bias` (col 5), exactly as printed. `error` is recorded for completeness; neither accelerations nor statuses depend on it.
