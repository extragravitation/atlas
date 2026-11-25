# Method gaps (pilot audit, aeg-d-strong-lensing/v3, rows m000021 and m000101)

No step was blocked; both rows computed. Every step below was inferred or taken on trust.

1. **R10 cosmology not checkable.** METHOD.md cites arXiv:1711.00072v2 Sec.1 for H0=70, Om=0.274. That paper is not in the packet, so the values come from METHOD.md and were not checked at source. The R5 cosmology was checked (ms_arxiv.tex l.188-191).
2. **Row-to-source mapping is not in the packet.** rows.json says the row "names its observables" (observed_from / baryonic_from), and METHOD.md cites `locators.json`, `tables/measurements.ecsv` and `adjudicated_inputs.csv`. None of these is in the packet. Lens identity came from the `system` field and the name match.
3. **Lens-name matching across tables.** The names are printed differently: S4TM prints "SDSSJ0757+1956"; table4 has both `SDSS` (full coordinates) and `Name`; Grillo uses `SLACS`. Rows were matched on the short J-name. I took this to be what "by the name the source prints" means.
4. **Units of MChaBC2.** The value is printed as an integer (9) in units of 1e10 Msun, taken from the VizieR column units line. The method does not say how to scale it. The integer rounding (+/-0.5e10, about 5%) is a source limitation.
5. **Which redshifts for R5.** Both table4 (zFG/zBG: 0.2219/0.6085) and Grillo (zl/zs: 0.222/0.609) print redshifts. I followed the method and used table4.
6. **bSIE is an intermediate-axis-normalised SIE radius** (VizieR note). The method uses it directly as theta_E with no axis-ratio correction. I did the same.
7. **R10 route, z_s role.** Because M_E is printed, z_s is not needed for R_E (only D_l is). I used z_s only for the selection rule. The method does not say this explicitly.
8. **R_eff in R10 Table 1 is assumed to be de Vaucouleurs.** Table 1's header does not say so. METHOD.md Sec.3 and sources.json S4 do. I used n=4.
9. **Sersic fraction.** b_n was solved numerically with root-finding (b_4=7.66925). theta_E and R_e were both taken in arcsec, as printed. The ratio is unitless and needs no distance, but the method leaves this implicit. Circular radii were used with no ellipticity (q) correction, which the method does not mention.
10. **Gas term.** I took "0.0012 × M★(<R_E)" to mean M★ inside R_E, in Msun. The cold-gas default of 0 was applied as written.
11. **Spectroscopic-redshift rule.** Neither table carries a flag saying spectroscopic. I relied on the column descriptions: table4 zFG "from SDSS database", zBG "Bolton et al. 2004"; S4 "SDSS spectroscopy" in sources.json. Both rows pass z_l<0.30.
12. **Simpson integration** in comoving distance used n=2000 as stated. H0 was converted to s^-1 with 1 Mpc = 1e6 pc (IAU). This is not written out but is standard.
13. **R_e input listed for m000021 is unused.** R_e (tex l.1821, 2.35 arcsec) is listed as an input, but the "printed inside R_E" route does not use it. Its role (perhaps a check only) is not stated.
14. **File hashes.** The whole-file sha256 of the three VizieR exports differs from sources.json `sha256`, because the export stamps the request time (2026-11-25 here). The `content_sha256` from '#RESOURCE=' matches for all three. The IOP files and the arXiv tarball match `sha256`, and ms_arxiv.tex matches the hash quoted in the S29 note.
15. **Grade/quality filters.** The method states no rule for lens grade (for example the table4 Lens status "A") or for multiple-lens systems. None was applied.
