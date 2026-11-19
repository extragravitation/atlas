# BZ notes: Banik & Zhao 2022, Symmetry 14, 1331 (arXiv 2110.06936v9)

Reader: BZ. Brief: `brief.md` in this folder (committed 2026-11-18). PDF sha256 first 16 checked: `e4fb17289b3f0ad2` (matches the brief).

## Pages read

- Read: PDF pages 1-77, every page, including figure captions, tables (Tables 1-6) and footnotes. The reference list (pages 78-87) was not read.
- Method: the supplied `pdftotext -layout` file interleaves the two columns, so I also extracted reading-order text with `pdftotext` (no `-layout`) into a scratch file outside the repository and read that. Where this was not enough, I looked at the PDF page image.
- Pages where the extracted text was garbled: 14, 15, 25, 26, 29, 30, 32, 45, 52, 55, 59 and 63. These pages carry figures reproduced from other papers, and the embedded text of those figures is mixed into the main text when extracted.
  - Pages 25, 26, 45, 52 and 63: read from the PDF page image. The galaxy names in the Figure 8 legend on page 25 (NGC 6482, 4649, 4472, 4261, 4125, 1521, 1407, 1332, 720) and in the Figure 9 legend on page 26 (NGC 3626, NGC 2824, UGC 6176) were taken from the images.
  - Pages 14, 15, 29, 30, 32, 55 and 59: the review's own text could be separated from the mixed-in figure text in the reading-order extraction, so I did not view these images. The mixed-in text comes from the source papers (McGaugh et al. 2016 PRL, Brouwer et al. 2021, Famaey & McGaugh 2012, McGaugh 1996, Angus et al. 2007, Di Valentino 2021). I did not record it as part of the review.
- Pages that produced no rows (theory, a figure alone, or scoring prose that adds no new test): 5, 6, 7, 9, 22, 39, 65, 68. Pages 22 and 39 hold only figures (Figure 6 on DF2; Figures 19-20 on bar pattern speed). Those figures are covered by the rows for pages 21 and 38.
- Quote check: every `quote` was checked by script against the extracted text of its page, and each has fewer than 15 words. Ten quotes on pages 25, 45, 52 and 63 fail the script check only because the extraction is garbled there. I checked those ten by eye against the PDF page images.

## Measurement routes near the boundary (not a direct comparison of observed pull with the pull of detected matter)

- Cusp versus core: inner rotation curves of dwarfs rise almost linearly (p17). This is a profile shape, and the review uses it only to discuss inclination and the location of the centre. No separate row.
- Diversity of rotation-curve shapes at fixed flat speed (p17, p66). Recorded as `route` because it is tied to the baryon distribution, but it concerns profile shape.
- Freeman limit (p32) and the exponential profiles of discs (p69): distributions of surface brightness and profile shape, compared with a stability threshold. Recorded as `outside`.
- Spiral-arm counts and the stability of LSB discs (p33-34): these infer disc self-gravity from the arm count or the velocity dispersion and compare it with the stellar mass-to-light ratio. Recorded as `route` (dynamics) because a dynamically inferred disc mass is compared with the stellar mass. They sit close to the boundary.
- Bar strength, bar fraction and bar pattern speed (p34-41): morphology and dynamical friction compared with simulations. Recorded as `outside`.
- Dynamical-friction limits as an indirect probe of extended unseen mass: Sagittarius progenitor (p43), shell spacing (p44), M81 group merging (p51), Hickson compact group lifetimes (p51), NGC 3109 backsplash (p50). Recorded as dynamics rows. None of them measures a pull profile directly.
- Tidal radius and tidal edges (p41-42, Fornax cluster dwarfs, McGaugh & Wolf 2010): self-gravity inferred from size and environment. Recorded as dynamics rows.
- Mass-radius relation of tidal dwarfs versus primordial dwarfs (p45-46): sizes at fixed stellar mass. Recorded as `outside`.
- Abundance matching versus dynamical mass of the Milky Way and M31 (p50), and cluster baryon fraction versus the CMB value (p54): these compare dynamical mass with detected baryons only through a cosmological prior. Recorded as `route`.
- Light-fermion phase-space limit for the residual mass in clusters (p55, 30 clusters): a residual-mass profile compared with a particle-physics bound.
- Lyman-alpha absorber internal properties (p27, p58): channel recorded as `unclear`.
- Satellite planes (p46-48), the local void and the Hubble tension (p58-60), the ISW effect, the Cold Spot, cosmic shear, CMB peaks and the cluster mass function: recorded as `outside`.

## Test cases the review names as contested between the two sides

- Fits with a galaxy-by-galaxy acceleration scale: Rodrigues et al. 2018 and Marra et al. 2020 against Kroupa et al. 2018a and Chang & Zhou 2019; NGC 3953 singled out (p16).
- A break in the BTFR at high mass (super-spirals, OGC 0139): Ogle et al. against Di Teodoro et al. 2021 (p16).
- Departures from the BTFR at low mass: Mancera Piña et al. 2019, 2020, 2022, including AGC 114905. Inclination is disputed, as for UGC 11919 and Holmberg II (p17).
- Whether the RAR can be reproduced with unseen-mass halos: Dutton et al. 2019 and Paranjape & Sheth 2021 against Ghari et al. 2019b, Tian & Ko 2019 and Desmond 2017b (p18, p24-25).
- Milky Way vertical dynamics: Lisanti et al. 2019 against the north-south asymmetry and non-equilibrium. DiskMass weighting: Angus et al. 2015 against Aniyan et al. and Milgrom 2018b (p19).
- Early dwarf dispersion claims (Gerhard & Spergel 1992) (p20); Carina (p21).
- NGC 1052-DF2: van Dokkum et al. 2018 against Kroupa et al. 2018b, Famaey et al. 2018 and Haghi et al. 2019a (p21-23); DF44 (p23, p29-30); NGC 2419: Ibata et al. 2011 against Sanders 2012 (p23).
- Crater II (p26).
- External field effect in SPARC: Chae et al. 2020b, 2021. The opposite sign of the correlation is predicted in one semi-analytic model (Paranjape & Sheth 2022) (p27).
- Wide binaries: Hernandez et al. 2012, 2019, 2022 against Scarpa et al. 2017, El-Badry 2019, Banik 2019 and Pittordis & Sutherland 2018, 2019 (p28, p71-72).
- Anisotropy of the weak-lensing signal: Schrabback et al. 2021b (p29).
- Fattahi et al. 2018 virial analysis of satellites (p42).
- Sagittarius stream: the review says it is hard to tell the accounts apart (p43). Palomar 5 stream asymmetry: external field, Galactic bar or subhalo (p44).
- NGC 3923 shells: Hernquist & Quinn 1987 against Milgrom 1988a and Bílek et al. 2013 (p44).
- Bullet Cluster against Train Wreck (Abell 520), with line-of-sight chance alignment invoked for each (p54). The Bullet Cluster lensing map with an added collisionless component (p55). The MOG fit (p56).
- El Gordo: Kim et al. 2021b against Asencio et al. 2021 (p57).
- Bar pattern speeds: Fragkoudi et al. 2021 against Roshan et al. 2021b (p40-41).
- LMC group infall as the origin of the satellite plane: Samuel et al. 2021 against Santos-Santos et al. 2021 (p47). The significance of the velocity anti-correlation of satellite pairs: Ibata et al. 2014a against Cautun et al. 2015 (p48).
- NGC 5291 tidal dwarfs: Bournaud et al. 2007 and Gentile et al. 2007 against Flores et al. 2016 (p70).
- Solar System quadrupole: Hees et al. 2014, 2016 (p73).
- Cluster residual mass as undetected baryons: Milgrom 2015b, which the review argues against (p54).

## Scan false matches

`scan_names.py 2110.06936 BZ` found 82 names, with 3 not in the CSV after my rows were added. All three are false matches:

- `M16` (p29): in the reproduced Brouwer et al. 2021 Figure 11 caption, "M16" is shorthand for the McGaugh et al. 2016 RAR fit. It is a reference, not Messier 16.
- `UGC6176satellite.` (p26): a garbling of the `-layout` extraction that joins "UGC6176" from the Figure 9 legend to the word "satellite". UGC 6176 itself is in the CSV (page 25 lenticular row).
- `Virgo` (p2, 11, 64, 67): only in the citation "Virgo & LIGO Collaborations 2017". This is a reference, not the Virgo Cluster.

Also handled: `Andromeda` (p2, p46). On p2 it is the Local Group timing argument, so the name was added to that row. On p46 it appears only in the survey name "Pan-Andromeda Archaeological Survey", which is covered by the M31 satellite plane row.

## Row counts by item_kind

| item_kind | rows |
|:--|--:|
| system | 97 |
| route | 94 |
| outside | 54 |
| type | 37 |
| **total** | **282** |

22 of these rows (17 system, 5 route) begin `mentioned, not used as a test:`.

Channel counts: dynamics 190, neither 62, lensing 19, both 7, unclear 4.
