# Reader B notes: aeg-d-dwarfs_v1

All 10 rows: status `method incomplete`. g_obs is computed for all 10; g_bar for none.

## Why g_bar is not computed (all rows)

The written method (methods_page.txt, REPRODUCTION.md, D048_KIND_BASIS.md, descriptor.json, sources.json) gives
g_bar = G (½ L_V Υ_V + M_gas(<r½)) / r½², but states **no numeric value for G**, none for the solar mass in kg, and none for the parsec in metres. The brief says an unstated constant means "method incomplete", so g_bar is left empty. The intermediate baryonic masses are in `code/results.json` (`M_bar_half_Msun`, `rhalf_kpc`) for anyone who wants to compare once constants are fixed.

## g_obs and unit definitions

g_obs = 3σ²/r½, with r½ = 4/3 R_h and R_h = a√(1−ε) (REPRODUCTION.md; D-025). To convert to m s⁻² I used only unit definitions: 1 km = 1000 m, 1 pc = 648000/π au, 1 au = 149 597 870 700 m (IAU exact definitions). The method does not state these. I treated them as unit definitions, not physical constants. Arcminutes go to radians exactly, and distances use D = 10^(μ/5+1) pc.

## Other method gaps and judgement calls

1. **[Fe/H] for Υ_V.** The descriptor says the metallicity comes from the "spectroscopic original (D-057) or the dispersion paper (D-059)". The packet does not include D-057 or D-059, so the D-057 source is unknown.
   - Tollerud 2012 (And III, IX, XV, XVI) prints no [Fe/H], so Υ_V cannot be determined for these.
   - Geha 2026 (CVn II) prints no system mean, only per-star values; computing a mean is an unspecified step. Diagnostic only: [Fe/H] = −2.12 (Muñoz 2018 Table 1) gives Υ = 1.903.
   - Koch 2007 (Leo I) gives −1.31 on the CG97 scale and −1.61 on the ZW84 scale. The method names no scale. Υ is 1.942 at −1.31, 1.873 at −1.61 and 1.899 at −1.45 (Muñoz value).
   - Gregory 2019 (Tucana) only quotes F09's −1.95, which gives Υ = 1.879. Saviane's −1.82 would give 1.869.
   - Collins 2013 (And XII, XXIII) gives −2.2, which gives Υ = 1.9158.
   - Cerny 2026 (Draco II) gives [Fe/H]model = −2.94. This is below the MvdM05 minimum of −2.29, so Υ = 1.931, flagged `beyond_source_range`.
2. **Υ_V interpolation.** I used MvdM05 (M/L)₁ over the 148 `MW-` rows. All are at logAge 10.11, and (M/L)₁ is single-valued in [Fe/H], which I checked in code. Values are rounded to the printed precision (2 dp for [Fe/H], 3 dp for M/L) before linear interpolation.
3. **Solar M_V.** It is +4.85, read from MvdM05 (arXiv:astro-ph/0605132v1, p. 22). That paper was not in the packet; see the downloads below.
4. **Tucana R_h.** Saviane 1996 Table 5 gives Re = 205 pc as the "effective geometric radius", assuming 870 kpc. The abstract modulus 24.69 corresponds to 867 kpc. Following the locator ("Re … pc at (m-M)0 …, as an angle"), I converted Re to an angle using μ = 24.69, then to pc at Bernard's 24.74, which gives 209.78 pc.
   - A geometric radius is already circularised, so I did not apply √(1−ε). The method does not cover this case, and D-053 and D-058 are not in the packet.
   - If Re were instead treated as semi-major with ε = 0.48, g_obs would be about 1.39 times larger. The value is in the values.csv notes.
5. **Tucana M_V.** I used Saviane Table 5 M_V = −9.55 plus its own TRGB modulus 24.69, giving m_V,0 = 15.14, then Bernard μ = 24.74. Saviane's printed V_T = 15.15 differs by 0.01, presumably extinction; I did not use it.
6. **Tucana σ.** I used 14.4 km/s, the final value after removing outlier 37852 (Gregory §3.3, abstract and conclusions). Gregory also prints 16.6 (before the removal), 20.9 (all objects) and 13.3 (after subtracting rotation). I applied the "whole sample" rule as the paper's final membership sample.
7. **And XVI distance.** Martínez-Vázquez 2017 Table 8 prints four RR Lyrae moduli. I used PWR (23.70) because the paper adopts it (p. 17). Savino 2022 prints 23.57 for And XVI, but the locator names MV2017.
8. **Leo I.** μ0 = 22.155, the midpoint of Stetson's 22.06 and 22.25 (as the locator says). Apparent V is −11.78 + 5 log10(254.0 kpc / 10 pc) using Muñoz Table 1 R, so M_V = −11.911 at the adopted distance. σ = 9.9 km/s, the combined GMOS+DEIMOS value from the Koch 2007 arXiv v1. I did not check the published ApJ text against v1.
9. **CVn II.** Same reconstruction: −5.17 + 5 log10(160.0 kpc / 10 pc), then μ0 = 21.02 (Greco §5). I used the modulus, not the rounded "d = 160 kpc", for the size conversion.
10. **Limits.**
    - Draco II: σ < 2.6 km/s, a 95% credible upper limit.
    - And XII: σ = 0.0+4.0 km/s, the formal 1σ upper bound.
    - Both are computed at the limit and noted as `limit`.
11. **Gas.** All ten systems are 5σ upper limits in Putman 2021, so the gas is "absent (measured limit)" and M_gas = 0. The helium factor of 1.33 (descriptor) is therefore not used.
12. **Semi-major radii.** Martin 2016, Muñoz 2018 and Longeard 2018 all use the Martin et al. 2008 likelihood, with r_h along the major axis, so a√(1−ε) was applied. Longeard's ellipticity row label prints as "-" (a lost glyph); it is the row after θ, with value 0.23.

## Downloads (arXiv e-prints, as the brief allows)

| Paper | URL | SHA-256 |
|---|---|---|
| McLaughlin & van der Marel 2005 | https://arxiv.org/pdf/astro-ph/0605132v1 | 8605aae32a4f021f1213f735c3f7f5e84bcae496f3ea49234e1e2e1c00920d22 |
| Koch et al. 2007 (Leo I) | https://arxiv.org/pdf/astro-ph/0611372 (v1) | 6fdfb5b5fcb066c885aba77624e5cbc3327d58baca67cf7dbd75c61000fa5a3c |
| Gregory et al. 2019 (Tucana) | https://arxiv.org/pdf/1902.07228 | 30a451f8ae8804c37f7d7a94e3c9de9c2ecf64fc116351ba53a8164c332422ac |
| Bernard et al. 2009 (Tucana distance) | https://arxiv.org/pdf/0904.4463 | 48354807f724ccdb427831829b2f74a8fea63d6f577c1f271346981f86a600d2 |
| Saviane et al. 1996 (Tucana) | https://arxiv.org/pdf/astro-ph/9601165 | a00ce53f0564da44f12c5819ec2913e6f081d3f82424df4647abf4c0acf7d528 |

The files are in `tmp/`. The arXiv IDs were found through arxiv.org title and author search only.

## Not verified

- Page numbers are PDF page indices, taken from the pdftotext form-feed split. For the arXiv preprints these are preprint pages, not journal pages.
- I did not render page images. Values were read from the pdftotext `-layout` output. Multi-line asymmetric errors were checked by eye, and only central values are used.
- Martin 2016 Table 1 And IX ε prints as 0.00+0.16−0.00; 0.00 is used.

## Isolation

I read only my packet and the five arXiv e-prints listed above. The session scratchpad directory turned out to contain other sessions' files. I listed it once by accident, read none of its contents, and moved all temporary work to `tmp/` inside my own output folder.
