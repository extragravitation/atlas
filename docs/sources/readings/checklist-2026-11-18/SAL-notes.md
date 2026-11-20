# SAL reading notes: Salucci 2019, A&ARv 27, 2 (arXiv 1811.08843v2)

Reader: SAL. Brief: `brief.md` in this folder (committed 2026-11-18).
PDF sha256 first 16 checked: `be94f7b54b7675ed` (matches the brief).

## Pages read

- PDF pages 1–56, every page, in `/home/claude/reviews/1811.08843.txt` (pdftotext layout), including all figure captions, tables and footnotes. Page 57 (the end of section 12, Acknowledgements) and the reference list are outside the range. I did not use them.
- Figure pages opened in the PDF to read labels the text extraction misses: 4 (Fig. 1), 15 (Fig. 5), 28 (Fig. 9), 33–34 (Figs. 11–12), 35 (Fig. 13), 37 (Fig. 14), 38–41 (Figs. 15–18), 45 (Fig. 20), 46 (Fig. 21), 48 (Fig. 23), 49 (Fig. 24), 50–51 (Figs. 25–26), 53–54 (Figs. 27–28). Figs. 13, 17 and 21 were rasterised at 300–400 dpi to read the panel labels.

### Pages not readable as text, and how I handled them

- **Fig. 13 (p. 35):** the panel labels are only in the image. At 300 dpi they read 2841, 3992, 7331, 2998, 2903, 3198, 2403, 6503, 5585, 1560, 3109, D154. The review prints no catalogue prefix. In the CSV I record them as "read as NGC xxxx / DDO 154". **That prefix is my reading of the label and was not checked at source** (Bottema and Pestaña 2015 was not opened).
- **Fig. 17 (p. 40):** the legend and point labels are only in the image. They read IC 2574, NGC 2366, Ho I, Ho II, DDO 154, DDO 53, M81dwB, DG1, DG2, DDO 210, DDO 101 and Haro 36. The review does not say what DG1 and DG2 are, so they have `channel = unclear` and that is noted in the CSV. Whether they are real galaxies was not checked at source.
- **Fig. 21 (p. 46):** the 16 ATLAS3D panel names are only in the image. All 16 are legible.
- **Figs. 8, 22 and 23 (pp. 27, 47, 48):** the axis text comes out garbled in the extraction. I read them from the PDF. They contain only sample names (ATLAS3D, SLACS), which are covered by `type` rows.
- **Equations:** several are garbled in the text (Eqs. 3, 5, 6, 14, 17–21, 29–36). None of them is needed to identify an item, and no values were taken from equations.
- The extraction breaks some words across lines with a hyphen. Where a quote spans such a break, the CSV quote is de-hyphenated to match the PDF. Every quote was checked by script against the text pages (whitespace and line-break hyphens normalised), and every quote is under 15 words.

## Routes close to the boundary (not a direct observed-pull versus detected-matter comparison)

- **Cusp versus core / inner logarithmic density slope** (pp. 32–41, 50–52): this is the shape of the inferred residual profile. Examples are the LITTLE THINGS slope <alpha> = -0.32 (Fig. 17), the dSph slope method and Schwarzschild fits of Fornax and Sculptor, and the cored-versus-NFW fit-quality comparisons in SPARC, GHASP, Bottema and Pestaña, NGC 5005 and the Milky Way.
- **Model-profile families** (section 6, pp. 23–26): BT-URC, NFW, Burkert, pseudo-isothermal, fermionic, Zhao and feedback-transformed. These are fitting forms, not measurements.
- **Halo-parameter scaling relations:** the constant r0·rho0 (p. 53), core radius against disk scale length (p. 41), rho0 against r0 (pp. 34, 36), the compactness correlation (Figs. 16, 28), and the pressure-like quantity rho·V² at r0 (p. 55). All of them are built from fitted parameters of the residual component, not from g_obs and g_bar directly.
- **NFW concentration compared with simulations** (Milky Way c = 20 ± 2, p. 37; GHASP, p. 36): this compares fitted parameters with model predictions.
- **Fundamental plane and its tilt** (pp. 42–43): this tests stellar M/L variation inside Re. The review says it is "not directly related" to the unseen component.
- **IMF variation** (Fig. 23 and Tortora 2018, p. 48; De Masi 2018 chemistry, p. 48): this changes the stellar M/L and therefore g_bar. It sits at the boundary as an input systematic.
- **Stellar-to-halo mass relation** (p. 54): it is mentioned and the review does not enter it.
- **Local density at the solar radius and the Milky Way escape speed** (p. 11): these are quoted only as inputs to direct-detection rates.
- **Diversity of rotation-curve shapes at fixed Vmax** (pp. 38, 40): the review compares profile shapes in physical units with shapes in double-normalised units.
- **Stacking and coadding of rotation curves** (pp. 6, 29–30, 38, 40): this is a way to build population averages, and a content-type question for the Atlas.

## Test cases the review names as contested

- p. 16: vertical-dispersion disk M/L (DiskMass) "can be subject to relevant biases (Hessman 2017)".
- p. 16: reference velocities Vflat, Vlast, W50 and Vmax are called "very biased".
- p. 22: dynamical against SED disk masses differ by about 0.15 dex, which the review calls large for mass modelling.
- p. 29: the baryonic Tully–Fisher slope "strongly depends on the vagueness in the definition of the reference velocity Vflat (Brook et al. 2016)".
- pp. 32–33: individual rotation curves and the cusp. "A debate has arisen on the level of the observational support" for the cusped profile. The review cites de Blok et al. 2001 to Adams et al. 2014.
- p. 36: the Milky Way. The available kinematics "is not able to discriminate between the cored and a cusped" profile (Catena and Ullio).
- p. 37: Milky Way circular-velocity compilation. "Notice measurements with huge uncertainty" (Fig. 14).
- p. 43: ellipticals. Tracers often fail to cover 1/3–3 Re.
- p. 46: Poci et al. 2017 slope variations are "in some contrast with previous works".
- p. 47: Alabi et al. 2018 globular-cluster fractions "seem in contradiction" with the r^-2.1 total-density results.
- p. 41: globular clusters and planetary nebulae as halo tracers have a "totally unknown dynamical state".
- p. 51: dSph Jeans analysis. There are "views that this investigation … cannot resolve in these objects the cusp/core issue" (Walker et al. 2009b, Strigari et al. 2008, Bonnivard et al. 2015, Strigari et al. 2018). The slope method's intrinsic bias is examined by Strigari et al. 2018. Breddels et al. 2013 find NFW "only marginally allowed in Sculptor".
- p. 25: "transformed" (feedback) profiles. The review disputes whether such a transformation can have happened in every galaxy.
- p. 5: the author declares a personal bias and excludes alternative theories from the review. I record this only because it bounds what the review tests: no confrontation with any account other than particle models appears in pp. 1–56.

## Row counts by item_kind

| item_kind | rows | of which `mentioned, not used as a test` |
|:--|--:|--:|
| system | 63 | 2 |
| type | 59 | 7 |
| route | 43 | 3 |
| outside | 11 | 10 |
| **total** | **176** | **22** |

The system rows include 12 Fig. 13 panels, 12 Fig. 17 labels, 16 Fig. 21 panels and 8 classical dSphs (Fig. 25). By channel: dynamics 145, lensing 6, both 5, neither 13, unclear 7. No cluster-scale system is used as a test anywhere in pp. 1–56. Clusters appear only as the environment of UDGs (p. 13), as "the biggest structures" in the list of untreated evidence (p. 3), and as the environments of comparison ETGs in Fig. 24 (Coma, Abell 262).

## scan_names.py

Command run: `python3 -I scan_names.py 1811.08843 SAL`. Result: 23 names found, 1 not in the CSV.

### Scan false matches

- `M3.6` (p. 27): the 3.6 µm absolute magnitude symbol in Eq. 39 (`M3.6 = (9.5 ± 0.3) log Vflat + …`). It is not a Messier object.

Matches the scan finds that are covered in the CSV, though they are not objects:
- `Virgo` (p. 8): this is "LIGO-Virgo", the gravitational-wave detector. It is covered inside the `outside` row on gravitational waves and is not the Virgo cluster.
- `Galaxy` (pp. 2, 5, 26, 36, 43): only p. 36 means the Milky Way, and it is covered by the Milky Way rows. The others are titles ("Galaxy Disks") or survey names ("SAMI Galaxy Survey", "6dF Galaxy Survey"), each covered by its own row.
- `Gaia` (p. 14): this is a survey, and it is named in the dSph stellar-density route row.
- `Milky Way` (p. 12): the isothermal-sphere velocity distribution assumed for direct detection. It sits within the p. 11–12 `mentioned` rows.
