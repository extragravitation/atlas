# Gaps

No row was marked "method incomplete" or "unreadable". g_obs and g_bar were computed for all 170 rows. The points below are about locators and wording. None of them changed a value.

1. **The locator omits Inc and e_Inc.** METHOD §2 and §4 say the galaxy's row of SPARC_Lelli2016c.mrt gives Inc and e_Inc. The rows.json locator for that row names only "D, e_D and f_D". I read Inc and e_Inc from the same row (whitespace tokens 6 and 7) and marked them at_locator = no. They are used only for the §4 uncertainty, not for g_obs or g_bar.
2. **Vbul for rows with no bulge.** 108 rows list no Vbul input. In every one of them the file has Vbul = 0.00 (bytes 54-59), so 0 was used, as METHOD §2 says. All 62 rows that do list Vbul have a non-zero Vbul.
3. **Negative Vgas.** 15 rows have negative Vgas: m000316, m001782, m002098, m000810, m001062, m001578, m001608, m001781, m002078, m000817, m002528, m002672, m002949, m002131, m001406. The sign was kept as METHOD §3 step 3 says. This matches SPARC.tex eq. 2 (l. 195) and l. 197.
4. **Wrong section number in source_ref (2 rows).** The source_ref cites "§3.4" for the exponential gas-profile assumption. The text is in §3.3, SPARC.tex l. 199, and the paper has no §3.4. The rows.json note already records this.
5. **Placeholders in source_ref.** Some source_ref strings contain "[value]" in place of Υ, f_D and H0. The values come from METHOD §1 and the files instead: Υ_disk = 0.5 and Υ_bul = 0.7; f_D from S2; H0 = 73 from the S2 header Note (2) and SPARC.tex l. 121.
6. **Checks that passed, for the record.**
   - The SHA-256 hashes of all three files, and of SPARC.tex, match sources.json.
   - The cited lines of SPARC.tex (l. 29, 113-121, 199, 261, 307, 312) say what METHOD §1 claims.
   - In all 3391 mass-model data lines, reading by byte position gives the same values as splitting on white space.
   - For every row, the S1 ID matches the row's system name, and the S2 row number matches the locator.
   - For every row, D in S1 equals D in S2.
7. **Not computed.** The §4 uncertainties were not computed, because the brief's output columns ask only for g_obs and g_bar. The §4 formula for g_obs cites arXiv:1610.08981 eq. 2, which is not among the supplied files, so I could not check that citation.
