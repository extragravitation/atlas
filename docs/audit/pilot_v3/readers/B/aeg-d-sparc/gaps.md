# Method gaps (audit packet B, aeg-d-sparc/v3)

No row needed "method incomplete" for g_obs or g_bar. The steps below I had to infer or guess, even where I am confident of the result.

1. **Where data rows start.** The method says to count data rows "from 1 after the byte-by-byte header". The header goes on past the column table into notes. I took data row 1 to be the first line after the last dashed separator (MassModels file line 26; SPARC Table 1 file line 99) and skipped blank lines. The galaxy names (NGC1090, NGC5985) match the systems in rows.json, which supports this reading.
2. **How to read the columns of SPARC Table 1 (S2).** The byte-by-byte header does not match the data. The header says lines are at most 113 bytes, but the data lines are 131 bytes. Reading by the stated byte ranges gives garbage (for example, D comes out as "4  37."). I read by whitespace tokens instead: 19 tokens per line, in header order. The method does not say how to read this file. For the MassModels file (S1), the byte ranges match the data, and I checked them against a whitespace split.
3. **How to find the galaxy's row in Table 1.** The method says "the galaxy's row" but does not say how to find it. I used the row number in rows.json (42, 86) and checked that the galaxy name matches.
4. **Which distance to use.** Both files give D (MassModels 37.0 / 39.7, and Table 1 37.00 / 39.70). §4 does not say which D goes into δD/D. I used Table 1, as §2 implies. The two agree for these rows. D does not enter g_obs or g_bar.
5. **What δi and δD are.** I took them to be the e_Inc and e_D columns of Table 1 ("mean error"). The method does not name the columns. Inclination and e_Inc are not in the rows.json locator. I read them from the same Table 1 row.
6. **Naming in the g_bar uncertainty.** The §4 formula uses "g_bar_gas", but §3 defines "g_bar_gas_cold". I took them to be the same thing. Whether to take the absolute value does not matter, because the term is squared.
7. **The δg_obs formula cannot be checked here.** It is cited to arXiv:1610.08981 eq. 2, which is not in the packet. I applied it as written. The uncertainties are in the notes only and do not enter g_obs or g_bar.
8. **Rounding and output precision.** The method does not say how many digits to give or how to round. I report 11 significant figures, from full double precision.
9. **Locator and packet mismatches (not method steps, but they affect how the inputs are located).**
   - sources.json gives S3's file as `arxiv/1606.09251v1.tar.gz`. It is at `files/1606.09251v1.tar.gz`. Its SHA-256 matches, and SPARC.tex inside it matches the stated hash 51504da7…
   - The rows.json source_ref strings still hold unfilled placeholders: "Υ = [value]", "f_D= [value]", "H0 = [value]". The values are f_D = 1 and H0 = 73 (S2 Note (2); S3 l.121), and Υ_disk = 0.5 and Υ_bul = 0.7 (from the method).
   - rows.json lists SBdisk and SBbul as inputs, but the method uses neither.
   - The method quotes "as suggested by SPS models" for Υ = 0.5/0.7. In SPARC.tex (l.263) that phrase supports Υ_bul = 1.4 Υ_disk, not the value 0.5 itself.
10. **Checks that passed.** All three file hashes match sources.json. S3 l.113 is the §2.2 heading, and the H0 = 73 Hubble-flow text is at l.121. The helium factor 1.33 is at l.199. "source eq. 2" matches the second equation in SPARC.tex (l.194, the V_bar equation with |V|V).
