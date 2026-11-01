# Reader B, block 1 (SLACS): questions and unsettled points

Date: 2026-10-31. Output: `reading.csv` (2088 rows), built by `build_reading.py` from the files in `dl/` (copies printed strings only; no arithmetic on values).

## Sources opened

| Record | What | Route | Version |
|---|---|---|---|
| R5 | VizieR J/ApJ/682/964 table4, table5, notes | vizier.cfa.harvard.edu `asu-txt` | VizieR |
| R5 | Bolton et al. 2008, arXiv:0805.1931 | arXiv PDF | arXiv v1 |
| R7 | IOP apj326624t3, t4 (Tables 3, 4) | content.cld.iop.org | MRT |
| R7 | Auger et al. 2009, arXiv:0911.2471 | arXiv PDF | arXiv v1 |
| R13 | VizieR J/A+A/501/461/lens (Tables 1 and 4) | vizier.cfa.harvard.edu `asu-txt` | VizieR |
| R13 | Grillo et al. 2009, arXiv:0904.3282 | arXiv PDF | arXiv v2 |
| R13 | Grillo et al. 2008 letter, arXiv:0712.0680 (Tables 1, 2 read from the rendered page 4) | arXiv PDF | arXiv v1 |
| R49 | Grillo et al. 2010: IOP apj327635t1; arXiv:0912.0744 | IOP; arXiv | MRT; arXiv v1 |
| R49 | Eichner et al. 2012, arXiv:1209.2140 (Table 9 read from the rendered page 16) | arXiv PDF | arXiv v1 |
| R66 | Sonnenfeld et al. 2012: IOP apj430577t1–t9; arXiv:1111.4215 | IOP; arXiv | MRT; arXiv v3 |

vizier.idia.ac.za refused the connection (proxy 403); the CfA mirror's `Cat`/ReadMe pages redirect to CDS (unreachable), but its `asu-txt` export works and prints the column descriptions. File SHA-256 values of every download are in `dl_sha256.txt`.

## Counts

- SLACS V-modelled lenses: 63 systems (R5 table5). Printed z_l (R5 zFG) below 0.30: **54**. Above: J0008−0004, J0157−0056, J0216−0813, J0330−0020, J0737+3216, J0903+4116, J0935−0003, J1100+5329, J1525+3327.
- Of the 54, six are not in R13 (no default stellar mass): J0841+3824 (R5 morphology L), J0955+0101 (L), J1032+5322 (L), J1103+5322 (U), J1251−0208 (L), J1432+6317 (L). R13 restricts itself to early types.
- J1538+5817 (z_l 0.1428), J1430+4105 (0.2850), J0946+1006 (0.2219): all three are in R5 table5 and in R13 (membership checked; was "not checked" in the inventory). All below 0.30. They also appear in the V-modelled scope rows.

## The four specific questions

1. **R61 R_ap = R_E?** Not in my scopes; not read.
2. **R57 stellar-mass radius?** Not in my scopes; not read.
3. **R26, R29 light profile?** Not in my scopes; not read.
4. **Gas candidates in my scopes.** Inventory §4 lists one in my scopes: R49, Eichner et al. 2012 (J1430+4105). At source (arXiv v1, Sect. 4.2, last paragraph): "this gas needs to be incorporated in either the dark matter or the de Vaucouleurs component"; same paragraph: "the uncertainty of our mass estimates due to the neglected gas is ≈ 10%". It cites Young et al. (2011) M(H2) ≤ 10⁹ M⊙ (less than 1% of the masses derived) and Sanderson et al. (2003) for hot gas up to 10% of the total mass in centres. It is a statement for ellipticals and groups in general, applied to this system; it is not a measurement inside θ_E. No other system-level gas statement found in R5, R7, R13, R49 (Grillo 2010) or R66. R5 Sect. 5.2 has a general sentence only (SIE success "requires that the dark-matter component and any significant gas mass be well aligned with the stellar spheroid").

## Not settled by the rules (facts for the comparison, not rulings)

1. **R5 θ_E has no per-lens error.** R5 Table 3 gives a formal error of 0.2% and an "adopted empirical error" of 2% for b. Recorded in `note`; `err_*` left blank. R13 assumes 5% on the same angles for its Mtotlen.
2. **R5 cosmology "flat".** R5 (and every other record here) prints Ω_m = 0.3 and Ω_Λ = 0.7 but never says "flat". Recorded as "not stated in words".
3. **R13 aperture.** R13's M*(≤R_Ein) uses R5's θ_Ein (R13 Table 1 cites Bolton et al. 2008a; its θ_Ein column matches R5 bSIE) and an aperture factor f_ap from the de Vaucouleurs θ_e. So R13's cylinder is R5's SIE R_E. Printed f_ap is in each `note`.
4. **R13 2008 letter differs.** The letter's 15 systems use R_Ein from Treu et al. 2006 / Koopmans et al. 2006 (e.g. J0037−0942: 1.47″ vs R5 1.53″), Salpeter BC03 only. I recorded its values as record R13 with "2008 letter" in `note`, since the scope names both papers. Whether they belong in the package is for Claude/JvH. The letter's lensing+dynamics stellar masses (σ-based) were not recorded.
5. **R13 VizieR error columns.** VizieR labels `E_` "upper limit" and `e_` "lower limit"; checked against paper Table 4 (J0008−0004: 48 +8 −29 ↔ 48, 8, 29). Recorded as err_plus = E_, err_minus = e_.
6. **R7 M_E and R5 models.** R7 does not say in a sentence that its r_Ein / M_Ein for the 63 R5 lenses come from the R5 SIE models; it says the 11 new models follow Paper V's method. The inventory's coding (R7 re-uses R5 models) is not confirmed or refuted at source. R7 prints no error on M_Ein.
7. **R7 stellar mass is total, inferred from the table layout.** R7 prints M* and, separately, f*,Ein; it never calls M* "total" in words. R7 masses use a σ–metallicity prior (alternative only, D-063 item 3).
8. **J1538+5817 (R49 default).** Only one IMF (Salpeter) and only a total mass (20 +1 −4 × 10¹⁰ M⊙, in the text, not a table). Light profile: de Vaucouleurs with θ_e = 1.58″, which R49 Table 1 takes from Bolton et al. 2008. R49's own z_s (0.531) is from new NOT spectroscopy; R5's z_s is 0.5312.
9. **J1430+4105 (R49 Eichner alternative).** Table 9 prints M* (10¹¹ M⊙) for three models (A Salpeter solar 6.7; B Chabrier solar 4.4; C Chabrier super-solar 4.0) with **no errors** and no stated aperture. The fit is to SDSS griz. θ_eff = 2.55″ is from Bolton et al. 2008.
10. **J0946+1006 (R66 default).** The SPS masses (Table 8: Comp. 1, Comp. 2, Total; Chabrier and Salpeter) use the **double tPIEMD** light model (Table 3), not the double-Sérsic model (Table 2). R66 prints both. The tPIEMD model has core and truncation radii (r_c, r_t), not R_e and n; the frozen `sersic_projected_fraction` would need the Sérsic model (Table 2), whose components may not correspond to the tPIEMD components the masses were fitted on. Component shares are printed only as F814W magnitudes per component (recorded as `component_share`, unit mag). The `quantity` list has no slot for r_c, r_t; they are in the `note` of the tPIEMD `profile_type` row.
11. **J0946+1006 sources.** R5's θ_E (1.38″) refers to the inner ring (z_s1 = 0.609 in R66; R5 zBG 0.6085). The outer ring has a photometric redshift only (R66 Sect. 3).
12. **R13 Mtotlen.** Recorded as `M_E` (record R13) for reference only; R13 computed it from R5's θ_Ein. It is not the observed default.
13. **Morphology disagreement R5 vs R7.** E.g. J1103+5322 is "U" in R5, "S0/SA" in R7; J0959+4416, J1029+0420, J1420+6019, J1443+0304 are "E" in R5 and "S0" in R7 (both are early-type under R5's definition "elliptical and S0"). Both recorded.
