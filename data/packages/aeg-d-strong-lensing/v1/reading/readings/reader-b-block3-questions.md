# Reader B, block 3: answers to the specific questions

Reader B, 2026-10-31. All sources are arXiv PDFs (`curl -sSL https://arxiv.org/pdf/<id>`, `pdftotext -layout`), except R26 Table 1 and R41 Table 1, which come from the IOP `content.cld.iop.org` ascii tables (no user-agent header was sent). MNRAS and A&A were not tried: the inventory records them as refusing. Versions are listed per row in `reading.csv`. Downloads are in `dl/`. The builder script is `scripts/build.py`.

## Q1. R61 (Collier, Smith & Lucey 2018): is the fiducial aperture R_ap the Einstein radius?

**R61 does not say so.** It defines R_ap as the half-image separation from SLC15 (R25):
- Sect. 3, SNL-1: "we adopt a fiducial aperture of Rap = 2.38 arcsec (the half-image separation derived by SLC15)". For SNL-2: "adopted as Rap = 2.21 arcsec" (Table 1: "SLC15, SINFONI–based").
- Table 2 caption: "Masses are measured within the fiducial radius, Rap."
- R61's own HST half image-separations differ from R_ap: 2.43 ± 0.03 arcsec for SNL-1 and 2.30 ± 0.03 arcsec for SNL-2 (Table 1, "this paper, HST–based").

Related facts printed by other sources:
- R25 Sect. 4.1: "For SNL-1 and SNL-2, we approximate REin by half the image separation". R25 Table 2 lists REin = 2.38 and 2.21 arcsec ("0.5×image-separation for SNL-1,2").
- R26 Table 1: θEin = 2.38 and 2.21 arcsec, "Denoted REin by S15".
- R33 Table 1 gives θEin = 2.38 arcsec (Smith et al. 2015). R33 Sect. 4 calls R61's 9.49 × 10^10 M_sun "the projected Einstein mass".

So R_ap numerically equals R25's R_Ein, which R25 defines as an approximation by the half-separation. R61 never states R_ap = R_Ein, and R61's own measured half-separation is larger.

## Q2. R57 (Sonnenfeld et al. 2019, SuGOHI III): which radius does the printed stellar mass refer to?

**Both are printed.** Table 5 has two stellar-mass columns, and its caption reads (arXiv v2): "stellar mass inferred from stellar population synthesis fitting of HSC photometry, ... and stellar population synthesis stellar mass enclosed within an aperture equal to the Einstein radius."
- Column 2, log M∗(Chab), is the total.
- Column 5, log M∗(Chab)(< REin), is inside R_Ein, "obtained assuming a constant M∗ /L throughout the galaxy" (Sect. 3.2).

The readers' dispute is therefore settled: Table 5 prints both. All 23 lenses have z_d ≥ 0.458 (Table 1), so no R57 mass value was transcribed.

## Q3. Do R26 and R29 print a light-profile fit (type, R_e, n)?

- **R26 (Newman et al. 2017): R_e only.**
  - Table 1 prints R_e = 9.8, 3.3 and 5.9 arcsec, "Effective radius in J band. Denoted REff by S15". These values come from S15 (R25), not from an R26 fit.
  - R26 prints no profile type or Sérsic n for the lenses. Its MGE expansions (Sect. 4.2, Fig. 1) appear only in a figure, not in a table.
  - The galfit Sérsic fit for SNL-2's neighbour prints no parameters.
- **R29 (Collier, Smith & Lucey 2018b): partly.**
  - Sect. 3 para 1 gives the type and n: "a smooth inner light profile, well fitted by a Sersic profile with index n ≈ 4" (PS1 imaging). The n is approximate.
  - Sect. 3 para 4 gives R_e: "an effective (half-light) radius of 5.7 arcsec". It is i band, with no error printed.
  - A galfit Sérsic fit was used for the PSF correction, but its parameters are not printed.
  - Note that R29's aperture is its own R_Ein = 1.47 arcsec (half-separation). The R27 default θ_E is 1.49 arcsec.

## Q4. Gas candidates in inventory §4 (quotes and locations)

All quotes are at most 15 words. Rows are in `reading.csv` (quantity `gas`).

| Candidate | Statement read at source | Location |
|---|---|---|
| R28, SNL-0 | "We assume the gas mass projected within the Einstein radius is negligible." | arXiv 1306.4983v1, footnote 3 (Sect. 2.3). An assumption. |
| R25, SNL-0/1/2 | "non-stellar mass contributions within the Einstein radius, e.g. gas ... are neglected." | arXiv 1503.02661v1, Sect. 4.2 para 1. The full sentence adds "and central black holes". An assumption. |
| R32, J1436+4943 and J1701+3722 | "a central black hole, gas, etc but these are expected to be negligible" | arXiv 1911.06338v1, Sect. 5 para 3. An expectation. |
| R35, MG2016+112 | "showing no evidence for hot X-ray gas (Chartas et al. 2001)" | arXiv astro-ph/0201017v2, Sect. 1 para 2. This refutes a claimed "dark cluster", not gas inside θ_E. The system is outside block-3 scopes. |
| R61, SNL-1 | "This suggests the presence of a small cold ISM disc." | arXiv 1709.01931v1, Sect. 3 (SNL-1) para 1. Dust within ~1 arcsec; not quantified. |
| R26, SNL-1 | "nebular emission in SNL-1, which is likely driven by the presence of warm gas" | arXiv 1612.00065v2, Sect. 6 (SDSS-stack comparison). No mass. |
| R29, J0403−0239 | "both are contaminated by gas emission, to different extent" | arXiv 1803.07082v1, Sect. 4 para 6. Also "weak H α and H β emission" (Sect. 3). No mass. |
| R30, NGC 6505 | X-ray mention only: "observed in Henry et al. (1995, X-rays)". Sect. 4.3: X-rays suggest "the galaxy is part of a small group". | arXiv 2502.06505v1, Sect. 1 and Sect. 4.3. No statement inside θ_E. |
| R31 (kind) | "In most cases, the gas content in elliptical galaxies can be safely neglected" | arXiv 2603.26894v1, Sect. 1 para 1. Not quantified. |
| R37 (kind) | "Other baryonic components, hot and cold gas or dust, are known to contribute a small fraction" | arXiv 0710.3159v1, Sect. 3 para 1, continuing "... to the net baryon budget ... (Roberts & Haynes 1994)". Not quantified. |
| R49 (J1430+4105) | "The hot gas component ... can contribute up to 10% of the total mass in the centre" | arXiv 1209.2140v1, Sect. 4.2 para 2. It also cites Young et al. 2011: M(H2) ⩽ 10^9 M_sun, "less than 1% of the total galaxy masses derived here". It concludes "uncertainty of our mass estimates due to the neglected gas is ≈ 10%". |
| R8 (X) | "any gas is effectively treated as dark matter" | arXiv 1007.2880v1, Sect. 2.3 para 1. A modelling convention. |
| R64 (X) | "X-ray observations show that the residual gas is a small fraction of the stellar mass" | arXiv 0911.3392v1, Sect. 2.1, which cites Mathews & Brighenti 2003 and Humphrey et al. 2006. |
| Young et al. 2011 | "The overall CO detection rate is 56/259 = 0.22 ±0.03". A few CO-rich ETGs have H2 masses ≳ 10^9 M_sun. | arXiv 1102.4633v2, abstract. Whole-galaxy figures; nothing about an Einstein radius. |
| Serra et al. 2012 | HI is detected in ~40 percent of non-Virgo ETGs. "small discs (M(H I)< 10^8 M ), which are confined within the stellar body" | arXiv 1111.4241v1, abstract. |
| Mathews & Brighenti 2003 | The total hot gas is "about <∼ 1 percent of the total stellar mass" (up to several 10^10 M_sun). | arXiv astro-ph/0309553v1, Sect. 1 (p. 4). This is a whole-galaxy total; the gas mass increases outward. |
| Diehl & Statler 2007 | No gas-mass or gas-fraction statement found. | arXiv astro-ph/0606215v2. The text was keyword-searched, not read in full. |
| Roberts & Haynes 1994 | Not read. The inventory did not locate it; it is cited only through R37. | — |

None of these is a measured gas mass inside an Einstein radius for any system in my scopes. Every statement is an assumption, an expectation, a qualitative spectral remark, or a whole-galaxy figure for the kind. Whether any of them qualifies under §3.4 is a ruling, not a reading.

## Things the rules did not settle

1. **No stellar mass is printed in several defaults.** I recorded the printed factors under `mstar` with a "NOT a stellar mass" note. Each product would be a computation, which the brief forbids.
   - R26 (SNL-0): L_r,Ein and (M*/L_r)_MW.
   - R61 (SNL-2): L_F814W(≤R_ap) and Υref = 2.59, with no error printed.
   - R29 (J0403): L_Ein and Υ_Ref.
   - R32 (MaNGA): L_Ein and Υref.
   - The "stellar masses" that R29 (8.63 × 10^10) and R61 do print are lensing minus EAGLE dark matter. They are not population-based, and I did not record them as `mstar`.
2. **R33 (SNL-1) gives no stellar mass inside θ_Ein.**
   - It prints log M* = 11.01 within R_e and 11.23 within r_max. These are from the "intrinsic enclosed mass profiles" (deprojected), not projected cylinders.
   - The MGE (Table A1, 11 Gaussians) was transcribed in full under `component_share`. No component's share of light or mass is printed as a fraction.
3. **R32 cosmology is stated by name only** ("Planck Collaboration et al. (2018)"), with no H0 or Ω_m printed. The H0 and Om cells are blank.
4. **CASTLES.** Two R36 systems have z_l below 0.30: MG 1549+3047 (0.11, no z_s printed) and MG 1654+1346 (0.25, z_s 1.74).
   - Neither is in R41 (the Leier et al. 2011 Table 1 lists 21 lenses, all with z_L ≥ 0.31 or blank), so there is no default stellar mass for them.
   - R36 prints critical radii only, not Einstein masses. Its stated cosmology is H0 = 50 with several (Ω0, λ0) pairs, with Σcr in h^-1.
   - The R36 z_l and z_s methods are not stated, apart from the footnoted "estimated" lens redshifts (MG0414, BRI0952) and the tentative z_s (HST14176).
5. **R27 θ_E = 1.49 arcsec** ("peak pixel REin") is printed in text with no error and no lens mass profile named. R27 also prints z_s = 0.195, while R29 prints 0.19165.
6. **R28 prints two lens redshifts:** heliocentric 0.0339 and CMB frame 0.0347 (z_l). I recorded the CMB-frame value as z_l.
7. **R30 θ_E has no printed error.** Table 2 says the number of significant figures indicates the uncertainty. R30's Salpeter value is not printed; only a division factor of 0.61 is given, stated for the 1.5-arcsec-aperture mass. R30 states H0 and Ω_m but not flatness.
8. **The Cosmic Horseshoe R60 title prints "J1004+4112"**, while R34 names it SDSS J1148+1930. Both are recorded as printed.
9. **Version labels.** The IOP `_ascii.txt` tables (R26 t1, R41 t1) are labelled `MRT` in the version column, because the brief has no "IOP ascii" option. The R43 IOP tables returned 404 at the paths I tried (`/journals/2041-8205/987/{1,2}/L31/revision1/`), so R43 is from arXiv v2.
10. Every system in the KiDS, Cosmic Horseshoe, J0100+1818 and SuGOHI scopes has z_l > 0.30. Only identifiers, redshifts, methods and kind were read for them.
