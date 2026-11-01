# Part S: questions and notes (reader A, 2026-11-01)

Output: `supplement_reading.csv` (248 rows). Transcription only. Nothing was computed. The only operation on any value was a selection filter on the printed z_l (< 0.30).

## Sources opened (SHA-256 of the file as downloaded)
| Source | Route | SHA-256 |
|---|---|---|
| R29 arXiv:1803.07082v1 | arxiv.org/pdf | 240f01b5b90632642a38029702b4fd663df9e035b0826941b14f535fc6bdd604 |
| R25 arXiv:1503.02661v1 | arxiv.org/pdf | b6d67d236133a9e7d4e80d22f2d027748a8d32539e5877d5395c96ed8ea89d0e |
| R26 arXiv:1612.00065v2 | arxiv.org/pdf | 542370972c06f894fa4f16658a2aee698a3e01410ea8652ee52e36f19febcff9 |
| R26 VizieR J/ApJ/845/157/table1 (asu-tsv, all columns) | vizier.cfa.harvard.edu | e431f41b6807a6e13ae495e6b4318a950af65556f07494e5468560b8783dd674 |
| R13 arXiv:0904.3282 (PDF carries no version stamp; arXiv listing gives v2 per the adjudication) | arxiv.org/pdf | df3746887007595b00e7fb2564ae1e9121e95849c68c04e55d2a06e3324587cf |
| R13 VizieR J/A+A/501/461/lens (asu-tsv, selected columns) | vizier.cfa.harvard.edu | d0dec58aa7ef3531147b37a43530e17ebd9eb419c73e932fe0c5f13c081a37e7 |
| R7 IOP ascii Table 3 (apj326624t3) | content.cld.iop.org | b99bae9b0608718c3c19b5b32ddc6370cac00d7524ae0229967e95914cdf0614 |
| R7 IOP ascii Table 4 (apj326624t4) | content.cld.iop.org | 7c8a3297628bdf31a65082680c3e96e45c2172ddb49160ab10410ddb6d76c66d |
| R7 arXiv:0911.2471v1 (cosmology; spot checks) | arxiv.org/pdf | 31f2d6b38c8143a9d8216a0cdfda3ca95e7f5536d3f784f479f47c01228e1668 |
| R32 arXiv:1911.06338v1 | arxiv.org/pdf | 9c08bcb07a8c21d07e6dcca1d8ce200a98b52fd26148f3324feb0cff046aa02b |
| R30 arXiv:2502.06505v1 | arxiv.org/pdf | 0b593fc45bd284b7906fda3e35323d9779695448da9bcd930978ffdedea41dd6 |
| R10 arXiv:1711.00072v2 | arxiv.org/pdf | 062808fc803780906933f5c6e7d21f3b613ed2f6b91c7c5a8d7e25cfea5e42b5 |
| R9 arXiv:1407.2240v2 | arxiv.org/pdf | f53c4026d226980310117105c9b92b482996bc5803788246bc0c109575165481 |
| R20 arXiv:1307.4764v1 | arxiv.org/pdf | 95dd93ea5ee9d303ea63c0ef2a5bc4c7df6debdeea8ae3fdb6531b471d40d4d1 |
| Conroy, Gunn & White 2009, ApJ 699, 486, arXiv:0809.4261v2 | arxiv.org/pdf | c836faafe6223ef990942f896f5cf1cb360b93a91e425aec3d7c568674014598 |
| Conroy & Gunn 2010, ApJ 712, 833, arXiv:0911.3151v1 | arxiv.org/pdf | 704a7a0c67b04f1c76b5df85173b4f0434cc069315cc59520c81f8fea174135e |
| Bruzual & Charlot 2003, MNRAS 344, 1000, arXiv:astro-ph/0309134v1 | arxiv.org/pdf | 072998f68479ea6c604fe62f6dd1d3a13d478d788ea767546deb12d20b89391f |

The arXiv ids of the three model papers were found on arxiv.org (abs pages and the author search). Each was confirmed by the title and journal reference on its abs page against the reference lists of R9 and R20. export.arxiv.org was refused by the workspace proxy, so it was not used.

## Open points

1. **SNL-1 in R25: no stellar mass is printed.** R25 prints L_Ein (J) = 4.3 ± 0.1 × 10¹⁰ L⊙ inside R_Ein = 2.38″, and a Kroupa Υref = 1.47 ± 0.12 (Maraston 2005, an assumed age of 10 ± 1 Gyr). Any M* would be L × Υ. That is the same Q3 situation as in the adjudication. Υref is an assumed range that is the same for all three lenses. The fitted alternative (CvD12, 6dF) is 1.46 ± 0.18.
2. **SNL-1 in R26: R26 covers SNL-1.** It prints L_r,Ein = 1.62 ± 0.05 × 10¹⁰ L⊙,r inside θEin = 2.38″, taken from S15 (= R25), and a Kroupa (M*/Lr)MW = 3.93 ± 0.20 from IMACS spectra. The spectroscopic aperture has a radius of 2.2″, not θEin. R26 says these "radii are matched within ≤ 8%". The luminosity aperture is R25's half-separation, 2.38″. R61's own HST half-separation (2.43″) is not used by R26. R26 states no cosmology (adjudication Q4).
3. **R13 total masses.** They are printed as integers in units of 10¹⁰ M⊙ with asymmetric errors. The VizieR columns map lower to e_ and upper to E_. I checked this mapping against arXiv Table 4 for J0008−0004 and J0029−0055, and it matches. There are 48 R13 lenses with printed z_l < 0.30. Chabrier pairs with BC03 and Salpeter pairs with BC03, as the brief asks. The M05 columns (Sal-M05, Kro-M05) were downloaded but not transcribed.
4. **R13 R_e is R5's fit.** R13 Table 1 prints θe ("measured by fitting a de Vaucouleurs luminosity profile on the F814W images") and gives "References – Bolton et al. (2008a)", which is R5. So the R_e rows are R5's values as printed by R13. I did not open R5's own table (VizieR J/ApJ/682/964 is reachable on the cfa mirror). Should a reader confirm that R5 prints the same numbers?
5. **R7 scope.** R7 Table 3 has 74 lenses with printed z_lens < 0.30. Of these, 63 have a printed log M_Ein and 11 have "···" (listed with an empty value). Table 3 mixes morphologies (E, S0, S, E/S0 and others). It has no grade column, so grade A and grade B are not separated here. No error is printed on M_Ein. Selection used R7's own z_lens. Cases near the cut can differ between records: for example, J0037−0942 is 0.195 in R7 and 0.196 in R13. I checked every lens that appears in both R7 and R13: none falls on a different side of 0.30 in the two.
6. **R7 cosmology** is printed as "h = 0.7", not as H0 in km s⁻¹ Mpc⁻¹. Recorded as `h`.
7. **Salpeter conversion for R10 (FSPS) and R20 (BC03): "not printed".**
   - Conroy, Gunn & White 2009 never mentions Salpeter outside the introduction. Its reference IMF is Kroupa (2001).
   - Conroy & Gunn 2010 has no "Salpeter" or "Chabrier" in its text.
   - Bruzual & Charlot 2003 shows the IMF effect on M/L_V only as a figure (Fig. 4). Its text prints returned-mass fractions at 10 Gyr (31% Salpeter, 48% Chabrier), and these are not a mass ratio.
   - So Q11 option (a) ("read the model paper where the source prints none") yields no number for either. R20 prints its own Chabrier and Salpeter masses (Table 7), so it may not need one.
   - R10/R9: R9 shows Salpeter masses only in Fig. 9 (graphical).
   - Note, without judging it: R30's factor 0.61 is stated for R30's own Prospector fit. That fit uses "the Flexible Stellar Populations Synthesis (FSPS) code (Conroy et al. 2009; Conroy & Gunn 2010), and a Chabrier (2003) IMF" (arXiv v1 p.3, right column). These are the same two model papers R9 cites, but with a different setup (nonparametric SFH, MILES/MIST). Whether 0.61 may be carried over to R10 is a decision, not a reading.
8. **α for Salpeter is printed by more than one source.** R29 prints 1.55 relative to Kroupa (CvD09 models via ezgal). R25 also prints "a Salpeter IMF (α = 1.55)" (§1). R32 prints "α ≈ 1.65" (approximate; marked in `limit`) relative to its Kroupa Υref (CGW09 via EzGal). R26's 1.53 is a Vazdekis et al. (2012) convention (Fig. 2 caption) and is not recorded as a conversion for R26's own masses.
9. **R29 flatness.** Ω_Λ = 0.728 = 1 − Ω_m is printed. The word "flat" is not.
10. Quantity names `OL`, `h`, `L_in_aperture`, `ML_stellar_pop`, `salpeter_alpha`, `salpeter_factor` and `chab_to_salp_ratio` are not in READING_BRIEF's list. They follow the names used in `adjudicated_inputs.csv` where one exists there.
