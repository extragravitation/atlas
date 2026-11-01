# Reader B, part S (GAS_AND_SUPPLEMENT_BRIEF v2, items 1–5): open points

Output: `supplement_reading.csv` (297 rows). Downloads in `dl/` (arXiv PDFs and text, VizieR TSV `r13_lens.tsv` sha256 268594681ba975375ee95bdd1ef649c018115d99c38bce0c6e4df2f40c51de0f, IOP R7 tables t1–t5). Build script: `scripts/build.py`.

## Settled at source
- **R29 cosmology:** H0 = 70.4, Ωm = 0.272, ΩΛ = 0.728 (WMAP7), from §4. The word "flat" is not printed.
- **SNL-1, R25:** no stellar mass is printed. It prints L_Ein = 4.3 ± 0.1 ×10¹⁰ L☉,J inside R_Ein = 2.38″ (half the image separation), Υref = 1.47 ± 0.12 (J band, Maraston 2005, Kroupa, assumed age 10 ± 1 Gyr), and the alternative Υref = 1.46 ± 0.18 (CvD12 6dF age fits, Table 3d).
- **SNL-1, R26:** covers SNL-1. It prints no stellar mass, but gives L_r,Ein = 1.62 ± 0.05 ×10¹⁰ L☉,r inside θEin = 2.38″ and (M∗/Lr)MW = 3.93 ± 0.20 (Kroupa; SPS models descended from CvD12, fit to IMACS spectra).
- **R13:** 48 of 57 lenses have a printed z_l < 0.30. The totals are VizieR MChaBC/MSalBC, with E_ = upper (+) and e_ = lower (−) errors, checked against paper Table 4 for J0008−0004 and J0029−0055. R_e is R13's θe: the de Vaucouleurs fit on F814W, in Table 1, which cites Bolton et al. 2008a (R5).
- **R7:** 74 Table 4 lenses have a Table 3 z_lens < 0.30. No error is printed on log M_Ein. 54 of them are in the adjudicated SLACS set; 20 are not, and those are flagged in the note.
- **Salpeter conversions:**
  - R29: α = 1.55.
  - R32: α ≈ 1.65.
  - R30: divide by 0.61 (stellar mass; 0.63 is for SFR).
  - R10 (FSPS: Conroy, Gunn & White 2009; Conroy & Gunn 2010): not printed.
  - R20 (BC03): not printed. BC03 prints only the mass-return fractions at 10 Gyr (Salpeter 31%, Chabrier 48%) and an M/L_V plot.

## Questions
1. **Quantities outside the READING_BRIEF list.** I used `OL`, `L_Ein`, `ML_pop` and `salpeter_conversion` because part S asks for things the list has no name for. Should they be renamed?
2. **R7 scope.** Should the 20 R7 lenses below 0.30 that are outside the adjudicated SLACS set be kept? They include the SLACS IX new models.
3. **SNL-1 default.** R25 (J band, M05) and R26 (r band, CvD12-descended) give two luminosity × M/L routes at the same 2.38″ aperture. Which one is the default, given that R33 (the MGE) is the inventory default?
4. **R26 cosmology.** R26 states no cosmology (it adopts S15 distances). Its L_r,Ein note says "distance error not included".
5. **R32 extraction.** The extraction also contains "α & 1.6" in §5. This is likely "α ≳ 1.6", but the glyph was not verified against the rendered PDF.
6. **Not read.** The R9 Fig. 9 Salpeter masses (figure only) and the journal versions (MNRAS/A&A pages; arXiv was used). The VizieR R7 tables timed out, so I used the IOP ascii tables instead.
