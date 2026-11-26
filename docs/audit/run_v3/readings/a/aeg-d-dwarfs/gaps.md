# Gaps: aeg-d-dwarfs, reader A

No row is marked "method incomplete" or "unreadable". Every input was found and read. The items below are places where the method, the locators or the source files were incomplete or did not agree. Each item says how I resolved it.

## Method incomplete (resolved from the source itself, not by guessing)

1. **Andromeda XVI distance (m000013).** The locator names Martínez-Vázquez 2017, p18, Table 8, row And XVI, but no column. The row prints four moduli: PWR 23.70, LMRB03 23.73, LMRC03 23.70, FOBE 23.75. METHOD.md does not say which one to use. I used PWR 23.70 because the paper says so on p17: "We adopt the distances obtained with the PWR as … final adopted distances". With LMRB03 or FOBE, D would rise by about 1.4% or 2.3% and g_obs would fall by the same fraction. g_bar would not change, because L_V and r½² both scale as D².

2. **Higgs 2021 ellipticity (Andromeda XVIII m000015, Leo T m000047).**
   - The per-system table and the locator put r_h and ε in Higgs p16, Table 3. Table 3 has no ellipticity. The value is the column `e` of **Table 2**, so at_locator is "no".
   - Higgs define `e` from second moments (their eq. 4, after McConnachie & Irwin 2006). They do not define it as 1 − b/a, which is the ε that METHOD.md §2 asks for. The method gives no conversion, so I used `e` unchanged as ε.

## Methods text disagrees with the locators and the supplied files

I followed the locator in rows.json and the file the source ID points to. The σ text in METHOD.md §7 names a different place or paper in these cases:
- **Andromeda XVIII:** the text says "Kvasova 2024 (arXiv 1112.1067v3), p9, Table 3, row And XVIII, column σLOS". That is Tollerud 2012, which prints 9.7 ± 2.3. The locator (S70, Kvasova p7 and p11, Tables 2 and 4, '38 stars') gives **10.0** (+1.1 −1.0), the value I used.
- **Ursa Minor:** the text says "(arXiv 2002.09503v2), p.9 Table 3 (σv 8.7)". That paper is not supplied. The locator (Geha 2026, 2602.10200v2, pp. 32–34, Table A1) gives **8.86**, the value I used.
- **Ursa Major I and Leo T:** the text says "(arXiv 0706.0516v2), p9, Table 3". That paper is not supplied. I used the Geha 2026 Table A1 values at the locator: 7.16 and 6.05.
- **Fornax:** the text says Hendricks 2014 is "arXiv 0811.0118v1". The supplied file and S55 are 1408.5597v1. At the locator (p5, Sec. 2.1) the text prints σ_sys = **11.84** ± 0.45, which I used. Fig. 4 on the same page prints 11.62 ± 0.45.
- **Andromeda XI, XIX and VI** have similar mismatched arXiv IDs in METHOD.md. They are not among the 10 audited rows.

## Locator gaps

- **Antlia II magnitude (m000024).** The rows.json locator for `apparent_magnitude` names only S104 (Vivas 2022), which prints no M_V. METHOD.md §7 names Ji 2021, PDF p7, Table 1, row MV, "plus the modulus the paper uses (cited)". I used M_V = −9.86 and Ji's own modulus µ = 20.6 from the same table (cited there to Torrealba 2019). The package distance is Vivas, µ0 = 20.47, as §3 says.
- **Muñoz 2018 Tables 6 and 1** (Ursa Minor, Ursa Major I, Fornax). The locator gives the tables but no pages. I found Table 6 on PDF p28 and Table 1 on p22.
- **Gas locators.** In rows.json the gas locators read "Putman et al. 2021 Table 1, None", so they name no galaxy. I took the row names from METHOD.md §7, and each was found in the MRT. Leo T is the only detection; the other nine are upper limits.

## Conventions applied as the method states (listed for transparency)

- **Semi-major assumed (D-052 item 2):** Ursa Minor and Ursa Major I (Muñoz re,s), and Fornax (Wang "2D Half-light r_h", Sérsic column, with ε = 0.31 from the same column).
- **Hydrus I:** the method uses the semi-major 7.42′ × √(1 − 0.21) = 6.595′. The paper's own printed circularised value is 6.64′.
- **Values beyond the table range:** for Hydrus I (−2.52), Boötes III (−2.34) and Ursa Major I (−2.56), [Fe/H] is below the lowest MW cluster value (−2.29), so the end value (M/L)1 = 1.931 is used (`beyond_source_range`).
- **Rounding:** the §3 rounding was applied before step 8 (6 significant figures for D, R_h, L_V and M_gas; 4 decimals for m_V,0).

## Source-file integrity

- **VOTable hash.** The file-level SHA-256 of `J_ApJS_161_304_clusters.vot` (99beb657…) does not match sources.json (282ea6da…). The content hash from `<RESOURCE` onward does match the recorded content_sha256 (619b71cf…). The file's request_date is 2026-11-25T16:25:21, not the 2026-10-30 that the sources.json note describes. The data rows are therefore as recorded; only the export header differs.
- **Other files:** every other file matched its recorded SHA-256.

## Other observations (no effect on the arithmetic)

- **Boötes III (m000029):** the source title says it is "Tidally Disrupting". It may belong to the §6 recorded-not-plotted set, but the exclusion register was not supplied, so I could not check.
