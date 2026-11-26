# Gaps: aeg-d-sparc/v3, reader B

g_obs and g_bar: none. Every one of the 170 rows could be computed by following METHOD.md §1 to §3 alone. No value was unreadable. Every MassModels data row named in rows.json holds the galaxy given as `system`. Every SPARC Table 1 row number in the locators matches that galaxy's name. Every f_D code agrees with the method text in its source_ref.

Checks run:
- File hashes match sources.json (S1, S2, S3, and SPARC.tex inside S3).
- Reading MassModels_Lelli2016c.mrt by its header's byte positions gives the same values as splitting on white space, for all 3391 data rows. There are 3391 data rows, starting at file line 26.
- SPARC_Lelli2016c.mrt has 175 data rows, starting at file line 99, each with 19 white-space fields. It was read by splitting on white space, as METHOD §2 says.
- The SPARC.tex line citations were checked and found where stated. l. 29 has Υ★ ≃ 0.5, l. 261 has Υ_bul = 1.4 Υ_disk, l. 307 and l. 312 have 0.5 and 0.7, l. 113–121 are §2.2, and l. 199 has the 1.33 factor and the exponential gas profile for D512-2, D564-8 and D631-7.

Places where the locators or the method text are incomplete. None of these affects g_obs or g_bar.
1. **Inc and e_Inc have no locator.** METHOD §4 uses them for δg_obs, but no input in rows.json names them. I read them from the galaxy's SPARC Table 1 row (white-space fields 6 and 7) and marked them at_locator = no.
2. **Vbul for rows without a bulge is not listed.** METHOD §2 says so on purpose. I read the file value, which is 0.00 in every such row, used it, and marked it at_locator = no.
3. **R has no column locator.** The row-level locator (`where: {row}`) is the only thing that points to it. I counted it as at the locator.
4. **e_Vobs is missing from the §2 input table**, although §4 uses it and rows.json lists it with Vobs.
5. **A section reference in rows m000015 (D564-8) and m000034 (D631-7) is wrong.** Their source_ref cites "§3.4" for the exponential gas profile, but the statement is in §3.3, l. 199. rows.json already records this as known issue #222.
6. **The method does not say whether blank lines count as data rows.** The data sections contain no blank lines, so this has no effect here.
7. **15 rows have negative Vgas.** METHOD §3 step 3 says to keep the sign, and I did. Each such row is noted in values.csv.

Items that are only for the record:
- D in the mass-model file was not compared row by row with Table 1 beyond the script's check. No difference was found for these 170 rows.
- The uncertainties in §4 were not computed, because the brief asks only for g_obs and g_bar.
