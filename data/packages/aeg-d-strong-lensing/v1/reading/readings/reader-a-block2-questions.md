# Reader A, block 2: questions and open points

Scopes read: "S4TM lenses" (R10), "SL2S III sample" (R20, redshifts R21), "SL2S V added" (R22), "SL2SJ02176-0513" (R20, alternative R49 = Tu et al. 2009, A&A 501, 475).
Sources: IOP ascii/MRT tables on content.cld.iop.org (recorded as `version = MRT`) and arXiv PDFs (R10 v2, R9 v2, R20 v1, R21 v1, R22 v3, Tu 2009 v1). VizieR was not needed: every table was available from IOP. SHA-256 of every download: `dl/SHA256SUMS.txt`.

## The four specific questions

1. **R61, is R_ap the Einstein radius?** Not answered. R61 is outside block 2's scopes, so I did not open it.
2. **R57, which radius is the stellar mass for?** Not answered, for the same reason.
3. **R26 and R29, light-profile fit?** Not answered, for the same reason.
4. **Gas candidates (inventory §4) in my scopes.** §4 lists no candidate from R10, R20, R21 or R22. Its R49 entry is Eichner et al. 2012, which is not the R49 paper for SL2SJ02176-0513 (that is Tu et al. 2009). I searched the full text of R10, R9, R20, R21, R22 and Tu 2009 for "gas", "HI", "molecular", "ISM" and "dust":
   - None of them makes a statement about gas inside the Einstein radius of any system.
   - The only hits are general remarks on galaxy formation (R21 l. 49; R22 l. 51), Galactic dust extinction (R10 Table 1 note), and Tu 2009 §5 on the group's "intra-cluster gas temperature" (the group, not the lens).
   - So every gas row is recorded as `none`.

## Points the rules did not settle

1. **R20 Table 7: the MRT labels disagree with the paper's columns.** In the MRT (`apj485108t7_mrt.txt`), bytes 37–41 are labelled `logMSalp` and bytes 48–52 `logMChabNIR`. The arXiv v1 Table 7 header gives the order Chab, Chab(NIR), Salp, Salp(NIR). The numbers support the paper: for example, SL2SJ022511-045433 reads 11.57 / 11.59 / 11.81 / 11.84, and for systems with no NIR data bytes 37–41 are blank while bytes 48–52 hold the value about 0.25 dex higher. I assigned the IMF from the paper's header. This needs a ruling, or a check against the journal HTML table, which I could not reach.
2. **R20 Table 6 MRT labels the Einstein-radius column `Reff`.** Its explanation reads "Einstein radius" and the paper's header reads R_Ein. The values match arXiv v1 for all four systems below 0.30. One small mismatch elsewhere: for the external shear of SL2SJ021737 (row `_g_ext`), the MRT gives e_PosAng = 0.9 and the arXiv v1 gives ± 0.1. This value is not packaged.
3. **The stellar-mass aperture is not stated per object:**
   - R10 says "total" only in its abstract ("we have derived the total stellar mass of the S4TM lenses").
   - R20 and R22 do not say total in words. Their SPS fits use the magnitudes of de Vaucouleurs model fits (R20 Table 4 note).
   - I recorded both as read and inferred nothing.
4. **S4TM photometry record.** R10 takes its stellar masses from Shu et al. 2015, ApJ 803, 71 (R9):
   - R9 used HST F814W, FSPS SSPs (tform = 4 Gyr, solar metallicity, no dust) and a core-Sérsic light fit (Brownstein et al. 2014, in prep.). It prints no per-lens core-Sérsic parameters and no per-lens Salpeter masses (Fig. 9 only).
   - The only per-lens light profile printed is R10's own de Vaucouleurs fit: Table 1, R_eff "in the intermediate axis convention", which I recorded. This fit differs from the one behind the masses.
   - Only the Chabrier mass is printed per lens.
5. **R10 prints no errors** on b_SIE, log M_Ein or log M*. The rows are flagged "no error printed".
6. **Flatness.** No record says "flat" in words:
   - R10 prints Ωm = 0.274 and ΩΛ = 0.726.
   - R20, R21, R22 and Tu 2009 print Ωm = 0.3 and ΩΛ = 0.7 (R20 calls it "ΛCDM", R22 "concordance").
   - I recorded the printed values only.
7. **SL2S III sample membership.** I recorded all 56 R20 Table 6 systems, with each grade in `note`, rather than only the 36 grade-A lenses with spectroscopy. Three systems are missing from R21 Table 2 and have no printed z: SL2SJ140533+550231, SL2SJ141917+511729 and SL2SJ142321+572243. Two of the four systems below z = 0.30 are not grade A:
   - SL2SJ221929-001743 is grade B with a fixed PA; R20 says "The best-fit model does not predict multiple images".
   - SL2SJ222012+010606 is grade C; R20 says "probably not strong".
   Whether they belong in the package is a selection question, not a reading question.
8. **R22 updates systems already in R20/R21.** I recorded these under scope "SL2S III sample" with record R22:
   - SL2SJ021801-080247: new z_d = 0.884; R21 printed none.
   - SL2SJ022046-094927: new z_s = 2.61.
   - SL2SJ022648-040610: z_s still not printed.
   - SL2SJ021801 and SL2SJ022046 are upgraded to grade A.
   All three are above z = 0.30.
9. **SL2S V added.** All five new systems have z_d ≥ 0.557, so only identifiers, redshifts and kind were read. None of the five appears in R20 Table 7, so the R20 alternative stellar mass does not exist for them. SL2SJ022708-065445 is described as a "disky early-type galaxy", and SL2SJ020457-110309 is grade B.
10. **SL2SJ02176-0513 (R20 name SL2SJ021737-051329) is at z_l = 0.646 (R21), so only identifiers, redshifts and kind were read.**
    - Tu 2009 prints z_lens = 0.6459 ± 0.0003 in Table 1 and §2.4, but "zlens = 0.656" in its abstract (an internal inconsistency).
    - Tu has a second source at a photometric z_dbl = 2.90 (+0.18/−0.24).
    - Tu says the lens "inhabits a massive galaxy group".
11. **S4TM count.** Of the 40 grade-A lenses (R10 Table 2), 37 have printed z_L below 0.30. The three at or above are SDSSJ0324+0045 (0.3210), SDSSJ0324−0110 (0.4456) and SDSSJ0955+3014 (0.3214). All 40 carry morphology code "E".
