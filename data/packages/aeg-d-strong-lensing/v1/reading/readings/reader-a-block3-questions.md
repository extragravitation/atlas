# Reader A, block 3: answers to the specific questions

Reader A, 2026-10-31. Sources were opened from arXiv PDFs (version as marked in `reading.csv`), plus the VizieR table J/ApJ/845/157 from the vizier.cfa.harvard.edu mirror. Every quote below was checked by script against the `pdftotext` output of the file named. Superscripts are written with `^`, and `...` marks omitted words.

## Q1. R61 (Collier, Smith & Lucey 2018, arXiv:1709.01931v1): is the fiducial aperture R_ap the Einstein radius?

**R61 does not say that it is.** R61 defines R_ap as the half-image separation from SLC15 (R25), and its own HST half-image separations are different numbers.

- Sect. 3 (SNL-1): "we adopt a fiducial aperture of Rap = 2.38 arcsec (the half-image separation derived by SLC15)".
- Sect. 3 (SNL-2): "we measure the magnitudes within a fiducial radius, in this case adopted as Rap = 2.21 arcsec".
- Table 1, row "Fiducial aperture, Rap (arcsec)": 2.38 and 2.21, with the note "SLC15, SINFONI–based". The row "Half image-separation (arcsec)" gives 2.43 ± 0.03 and 2.30 ± 0.03, with the note "this paper, HST–based".
- Sect. 4: "we extract the mass enclosed within the fiducial radius (Rap , from Table 1)". The Table 2 caption reads: "Masses are measured within the fiducial radius, Rap".
- R61 does not print an Einstein radius of its own for either lens.

The SLC15 side (R25, arXiv:1503.02661v1) says:
- Sect. 4: "For SNL-1 and SNL-2, we approximate REin by half the image separation".
- Table 2, row "REin [arcsec]": 2.85, 2.38, 2.21, with the note "0.5×image-separation for SNL-1,2".

So R_ap is numerically R25's R_Ein, and R25 calls that an approximation by the half-separation. R_ap is not R61's own Einstein radius, and R61 does not state that the two are equal. For comparison, R33 (Poci & Smith 2022) Table 1 lists θEin = 2.38″ (citing Smith et al. 2015) next to "Total mass log10(M/M⊙) 10.98, Collier et al. (2018)".

## Q2. R57 (Sonnenfeld et al. 2019, SuGOHI III, arXiv:1904.10465v2): which radius does the printed stellar mass refer to?

**Both are printed.** Table 5 has one column for the total stellar mass and one for the stellar mass inside the Einstein radius.

- Table 5 caption: "stellar mass inferred from stellar population synthesis fitting of HSC photometry, Einstein radius in physical units, total projected mass enclosed within the Einstein radius, and stellar population synthesis stellar mass enclosed within an aperture equal to the Einstein radius."
- Column headers: `log M∗(Chab)` (total) and `log M∗(Chab) (< REin)`.
- Sect. 3.2: "the stellar mass enclosed within REin , obtained assuming a constant M∗ /L throughout the galaxy."
- The Einstein radius is "the circularised radius of the elliptical isodensity curve that encloses an average surface mass density equal to the lensing critical density" (Sect. 3.1). It comes from R57's own SIE model.

Both screening readers were partly right. All 23 lenses have printed z_d ≥ 0.458 (Table 1), so no mass values were read.

## Q3. Do R26 and R29 print a light-profile fit (type, R_e, n) for their lens?

**R26 (Newman et al. 2017, arXiv:1612.00065v2; VizieR J/ApJ/845/157): no usable profile fit.**
- It prints R_e only, as "Effective radius in J band. Denoted REff by S15" (Table 1). The values are 9.8″, 3.3″ and 5.9″ for SNL-0, -1 and -2, taken from S15 (R25). There is no Sérsic index and no profile type for these.
- A multi-Gaussian expansion is used for the dynamics ("JAM requires that the projected luminosity density be expressed via multi-gaussian expansions", Sect. 4.2). It is shown only as isophotes in Fig. 1, with no component values.
- Galfit Sérsic fits were made only to estimate the SNL-2 neighbour's light (Sect. 3), and no parameters are printed.
- Fact relevant to aperture matching for SNL-0: R26 measures the r-band luminosity "within a circular aperture with radius θEin" (Sect. 3), with θEin = 2.85″ ("Denoted REin by S15"). R28 (Smith & Lucey 2013) Table 3 prints REin = 2.85″ from the same Smith et al. (2005) SIS model. The two radii are numerically the same printed number.

**R29 (Collier, Smith & Lucey 2018b, arXiv:1803.07082v1): partly.**
- Type and index: "a smooth inner light profile, well fitted by a Sersic profile with index n ≈ 4" (Sect. 3, para 1; Pan-STARRS PS1). n is printed as approximate, with no error.
- R_e: "an effective (half-light) radius of 5.7 arcsec" (Sect. 3, para 4; PS1 i band), with no error. The source does not say which fit produced it.
- A galfit Sérsic model was used for the PSF correction, but its parameters are not printed.
- R29's luminosity aperture is its own REin = 1.47 ± 0.03″ (half the image separation). R27, the observed default, prints REin = 1.49″ (peak pixel, PyAutoLens on HST), so the two radii differ.

## Q4. Gas candidates in packaging-inventory §4 (all in my scopes, or scope "gas")

All are in `reading.csv` with quantity `gas`. Only the R28 and R25 statements explicitly mention gas within the Einstein radius. Both are assumptions ("assume ... negligible", "are neglected"), not measurements.

| System / kind | Record | Quote (as read) | Location |
|---|---|---|---|
| ESO 325-G004 (SNL-0) | R28 | "We assume the gas mass projected within the Einstein radius is negligible." | Smith & Lucey 2013, footnote 3 (arXiv v1) |
| SNL-0, SNL-1, SNL-2 | R25 | "Other possible non-stellar mass contributions within the Einstein radius, e.g. gas and central black holes, are neglected." | Smith, Lucey & Conroy 2015, Sect. 4 (arXiv v1) |
| J1436+4943, J1701+3722 | R32 | "(and in principle from a central black hole, gas, etc but these are expected to be negligible)" | Smith et al. 2020, Sect. 5, para 3 (arXiv v1) |
| MG2016+112 | R35 | "showing no evidence for hot X-ray gas" (Chandra, cited Chartas et al. 2001) | Koopmans & Treu 2002, Sect. 1 (arXiv v2) |
| SNL-1 | R61 | "This suggests the presence of a small cold ISM disc." (dust within the central ~1″; no mass) | Collier et al. 2018, Sect. 3 |
| SNL-1 | R26 | "nebular emission in SNL-1, which is likely driven by the presence of warm gas" (no mass) | Newman et al. 2017, Sect. 6.2 |
| J0403−0239 | R29 | "both are contaminated by gas emission, to different extent" (Hα, Hβ in the Einstein-aperture spectrum; no mass) | Collier et al. 2018b, Sect. 4 |
| NGC 6505 | R30 | "Henry et al. (1995) find evidence in X-ray emission that the galaxy is part of a small group" (nothing inside θE) | O'Riordan et al. 2025, Sect. 4.3 (arXiv v1) |
| elliptical galaxies | R31 | "In most cases, the gas content in elliptical galaxies can be safely neglected" | Wang et al. 2026, Sect. 1, para 1 (arXiv v1) |
| early-type galaxies | R37 | "Other baryonic components, hot and cold gas or dust, are known to contribute a small fraction to the net baryon budget in these systems (Roberts & Haynes 1994)." | Ferreras, Saha & Burles 2008, Sect. 3 (arXiv v1) |
| SDSS J1430+4105 / kind | R49 | gas "needs to be incorporated in either the dark matter or the de Vaucouleurs component"; "the uncertainty of our mass estimates due to the neglected gas is ≈ 10%" | Eichner et al. 2012, Sect. 4.2 (arXiv v1) |
| SLACS (R8, X) | R8 | "any gas is effectively treated as dark matter" | Auger et al. 2010, Sect. 2 (arXiv v1) |
| elliptical galaxies (R64, X) | R64 | "X-ray observations show that the residual gas is a small fraction of the stellar mass" | Treu et al. 2010, Sect. 2 (arXiv v1) |

Additional statements found while reading (not in §4):
- R41 (Leier et al. 2011, Sect. 4): "The gas contents of our lens sample – mostly early type galaxies – is expected to be small." The paper adds that for Q2237 (the bulge of a spiral) and B1600 "one can indeed expect deviations".
- R27: no gas statement for J0403−0239. The only related statement is about dust: "signs of irregular patchy dust obscuration".

Literature on the kind, now read. None of these makes a statement about gas inside an Einstein radius.
- **Young et al. 2011** (arXiv:1102.4633v2), abstract: "The overall CO detection rate is 56/259 = 0.22 ±0.03"; "a few extremely CO-rich early-type galaxies with H2 masses ≳ 10^9 M⊙".
- **Serra et al. 2012** (arXiv:1111.4241v1), abstract: "We detect H I in ∼ 40 percent of all ETGs outside the Virgo galaxy cluster". The H I comes as "small discs (M(H I)< 10^8 M ), which are confined within the stellar body", or as large discs or rings of up to 5 × 10^9 M⊙ extending to tens of kpc.
- **Mathews & Brighenti 2003** (arXiv:astro-ph/0309553v1):
  - Sect. 2: "the total mass of hot gas in massive E galaxies varies up to at least several 10^10 M⊙ or about ≲ 1 percent of the total stellar mass". This is for the whole galaxy.
  - Sect. 5: "the mass of hot gas is usually negligible".
  - Sect. 7.2: molecular discs "of mass 10^7 − 10^9 M⊙" in a small number of E galaxies.
  - Sect. 7.3: dust "within ∼ 1 kpc of the center ... with associated gas masses 10^4 − 10^7 M⊙".
- **Diehl & Statler 2007** (arXiv:astro-ph/0606215v2): no gas-mass statement found. Its "X-ray gas fractions range from 57% to 100%" is, in context, the gas share of the X-ray emission. That is my reading of the context, not a mass fraction.
- **Roberts & Haynes 1994**: not located and not opened.

## Matters the rules did not settle

1. **Stellar mass printed only as luminosity × M/L.** R26 (SNL-0), R61 (SNL-2), R29 (J0403) and R32 (MaNGA) print the luminosity inside the aperture and the reference M*/L, but not their product. The brief's quantity list has no luminosity or M/L entry. Both factors are recorded under `mstar`, with notes "factor 1 of 2" and "factor 2 of 2". I did not compute the product.
2. **R29's printed "aperture stellar mass" is not a stellar-population mass.** M_Ein^* = 8.63 ± 0.54 × 10^10 M⊙ is the lensing mass minus an EAGLE dark-matter estimate. It is recorded and flagged. Using it as g_bar would be circular.
3. **R33 (SNL-1 stellar default) prints no stellar mass inside θEin.** It prints:
   - the MGE in Table A1: 11 Gaussians, each with Σ*, µ, σ and q, but no printed share of light or mass;
   - intrinsic (de-projected) masses: log M* = 11.23 within r_max and 11.01 within R_e, with no errors.

   All are recorded. Under REPRODUCTION.md this case needs a frozen MGE routine.
4. **R61 masses are inside R_ap, not labelled M_E.** They are recorded under `M_E`, with the note "printed as M(≤Rap)". R_ap and R61's own half-separation are recorded under `aperture`.
5. **Cosmology.**
   - R32 names "Planck Collaboration et al. (2018)" but prints no H0 or Ω_m.
   - R27 (Planck 2018: 67.4, 0.315) and R29 (WMAP7: 70.4, 0.272) differ for the same system.
   - No source states "flat" in words. Ω_Λ is printed where noted.
   - R36 uses H0 = 50 with "several discrete values for Ω0" (KKF98) and H0 = 65 (K00). R41 uses 72 / 0.3 / 0.7.
6. **R28 prints two M_E values and two lens redshifts.**
   - M_E: 1.50 ± 0.06 × 10^11 M⊙ (mass-follows-light, Table 3) and M_Ein^SIS = 1.44 × 10^11 M⊙ (text, no error). R_Ein = 2.85″ has no printed error.
   - z_l: 0.0339 heliocentric and 0.0347 CMB frame. The symbol z_l is attached to the CMB-frame row.
7. **R30 (NGC 6505).**
   - M_E = 1.53 × 10^11 M⊙ has no printed error.
   - Only the Chabrier mass is printed. The Salpeter conversion is given as "dividing ... with a constant factor of 0.61", stated in the context of the central 1.5″ SED fit.
   - Two z_l values are printed: 0.04243 ± 0.00003 (spectroscopic) and 0.041 ± 0.001 (cosmological, corrected for peculiar velocity).
8. **CASTLES scope membership.** R36 is two papers: Keeton, Kochanek & Falco 1998 (17 lenses, Tables 1 and 5) and Kochanek et al. 2000 (30 lenses, Tables 3 and 5). I recorded their union, 34 systems.
   - Neither paper states how z_l was measured.
   - KKF98 prints two estimated z_l (‡): MG 0414+0534 at 0.44 and BRI 0952−0115 at 0.99. K00 prints 0.96 for MG0414 and leaves BRI0952 blank, with z_FP = 0.41.
   - K00 lenses without z_l carry only fundamental-plane estimates. FBQ0951+2635 has z_FP = 0.21 < 0.30, but no measured z_l. I did not read the extended items for it and did not count it.
   - Printed z_l < 0.30:
     - MG 1549+3047 (0.11): no z_s.
     - MG 1654+1346 (0.25).
     - Q2237+030 (0.04): "the bulge of a nearby (z = 0.04) spiral galaxy", so a late-type kind.
   - R41 (Leier et al. 2011, Table 1) contains Q2237 but neither MG1549 nor MG1654. Its stellar mass is printed within 2R_e, not inside R_E.
   - Kind is stated per system only for B0218+357, B1600+434 and Q2237 (late-type) and MG2016+112 (two lens galaxies). For the rest, only sample-level statements exist ("dominated by L∗ early-type galaxies").
9. **SuGOHI kind.** No per-system morphology is printed. HSCJ142449−005321 is "the most probable brightest galaxy of a rich (∼ 50 members) cluster".
10. **Group environments stated.**
    - SNL-0: "dominant member of a small galaxy group, catalogued Abell S0740" (R28).
    - Cosmic Horseshoe: "the LRG lies in a galaxy group" (R60).
    - J0100+1818: "the lens early-type galaxy/group" (R47).
    - NGC 6505: "part of a small group" (R30, citing Henry et al. 1995).
11. **KiDS J0233−3447 z_s** is printed as 2.8230 ± 0.0001 in Table 1 and as 2.823 ± 0.001 in the text. Both are recorded.
12. **Access.**
    - vizier.idia.ac.za refused (proxy 403); vizier.cfa.harvard.edu worked.
    - A guessed content.cld.iop.org path for R43 returned 404. It was not pursued, since R43 has z_l ≈ 0.99. No IOP article pages were opened, and no user-agent was changed.
    - MNRAS and A&A pages were not tried. All other values are from arXiv, at the version marked in `reading.csv`.
