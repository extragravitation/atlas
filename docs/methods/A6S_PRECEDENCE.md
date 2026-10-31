# A6·strong lensing: which values are shown (approved by JvH 2026-10-31 17:43 MDT; frozen by hash, D-065)

Written 2026-10-31 under D-063 item 4 and D-064, before any lensing table has been opened. Sources are the eligible records of search log A6 (`docs/sources/screening-A6S/final.csv`). Once approved, this file is hash-frozen in `data/frozen/` and changes only by a new decision.

## 1. Who is plotted

A system is plotted only if all of these hold. Otherwise it is recorded with the reason.
1. A confirmed galaxy-scale lens in A6 by D-063 item 6. Systems coded A7 "ambiguous" appear in the A7 view.
2. Spectroscopic lens and source redshifts, neither derived with the system's own velocity dispersion (D-063 items 3 and 5).
3. An Einstein mass M_E, or θ_E with both redshifts, from a lens model (D-063 item 2).
4. A stellar mass inside R_E as §3 defines it.

## 2. Observed side: which lens model

1. **Originals first** (as protocol §4 and D-038). The default is the model published by the survey that took the imaging: SLACS V and IX for SLACS; S4TM; BELLS GALLERY; SL2S III and the later SL2S paper for its added systems; Collier et al. 2018 for SNELLS; and so on. Re-models of the same imaging by other teams (for example Etherington et al. 2022, Shajib et al. 2021, Project Dinos) are shown as alternatives.
2. **A full model over the image-separation estimate** (D-063 item 2).
3. **Among a survey's own models:** the most recent, unless a later paper only re-uses the earlier one.
4. **Quantity:** M_E as printed. Where only θ_E is printed, M_E = θ_E² · c² D_s D_l / (4 G D_ls), with the source's own cosmology (D-064 item 4). That is the standard formula, coded and tested before use.

## 3. Baryonic side: which stellar mass

1. **Inside the cylinder.** The stellar mass inside R_E as printed by the source is preferred. Where the source prints only a total mass and its own light-profile fit (for example de Vaucouleurs R_e), the fraction of that profile's projected light inside R_E is computed from the source's own fit. That computation is coded, tested and frozen before use, and the point is flagged `mstar_in_RE_from_profile`.
2. **IMF and model family** (consistent with D-039 item 2). The default is Chabrier or Kroupa, as printed by the source. The Salpeter value printed by the same source sets the top of the range. Where a source prints only one IMF, the range uses the Chabrier-to-Salpeter ratio of the same population model as printed in its model paper, read at source and registered.
3. **Among sources for the same lens:**
   - excluded as default: masses with priors using the lens's own σ (D-063 item 3, so SLACS IX is a flagged alternative only), and lensing or dynamical masses;
   - then, more photometric bands before fewer;
   - then a per-object population fit before a fixed-age, fixed-metallicity scaling;
   - then the most recent.

   Spectroscopic population M/Ls with a named IMF are eligible (D-063 item 1). On this rule, the SLACS default would be Grillo et al. 2009 (SDSS ugriz, three IMFs) or Shu et al. 2015 (single band), whichever ranks first. The ranking is applied by script before any value is read.
4. **Gas** (protocol §1.7; deviation #4). A system-level statement or limit where the source gives one (for example ESO 325-G004). Otherwise a cited, quoted statement for the kind on gas inside the Einstein radius of early-type galaxies, read at source before conversion, with each system marked "absent (literature limit for this kind)". If no such statement is found, the cell returns to JvH.

## 4. Tests frozen with this rule

- **Test 1:** an independent second reading of every packaged input, as for A3 and A5.
- **Test 2:** transcription.
- **Test 3:** arithmetic integrity.
- **Reported, not pass/fail:** where a source prints both M_E and θ_E, the formula of §2.4 is checked against the printed M_E.
