# Method gaps and reading issues: aeg-d-sparc/v3 pilot audit (reader A)

Source hashes checked against sources.json, and all match: S1 9108994b…, S2 5aa0501f…, S3 tar 792903260…, SPARC.tex 51504da7…
I unpacked S3 into `arx/` inside the packet. My code is in `scripts/audit.py`.

## Method gaps (steps I had to infer, even where I am confident)

1. **Where data-row counting starts (S1).** §2 says to count "from 1 after the byte-by-byte header". The header has the byte table, then Notes (1) to (3), then a dash line. I took the first data row to be file line 26 (CamB, R = 0.16), right after the final dash line, so data row n is file line 25 + n. The method does not say whether the Notes count as part of the header.
2. **How to find "the galaxy's row" in SPARC_Lelli2016c.mrt.** The method does not say how to match a mass-model row to its Table 1 row, either by name (S1 `ID` against S2 `Galaxy`) or by row number. It also does not say how data rows in S2 are counted. I matched by name, counting S2 data rows from file line 99 (CamB) = row 1. The rows I found agree with the locators (42 = NGC1090, 86 = NGC5985).
3. **How to parse the files.** The method does not say. For S1 I used the header's byte positions, and they agree with a whitespace split on all 3391 rows. For S2 the header's byte map does **not** fit the data: the header describes 113 bytes, but every data line is 131 characters long (for example, `D` is not at bytes 14–19). I parsed S2 by splitting on whitespace. Every row has 19 tokens and `Ref.` contains no spaces. This is a reading issue in the source file, and the method does not mention it.
4. **e_Vobs is not in the §2 input table**, but §4 uses it. I read it from the S1 column `e_Vobs` in the same row.
5. **Name mismatch.** §4 uses "g_bar_gas" and §3 defines "g_bar_gas_cold". I assumed they are the same quantity.
6. **Inclination (`Inc`, `e_Inc`)** is needed for §4, but the row locators do not name it. I read it from the same S2 row. Converting it to radians is stated in the method.
7. **Two distances.** S1 has its own `D` column per row (37.0 and 39.7), as well as S2's `D`. The method does not say which one is authoritative, or whether R or the velocities should be rescaled to a distance. I applied no rescaling. In these rows the two values agree.
8. **Output precision and rounding** of g_obs and g_bar are not stated. I report 7 significant figures.
9. **Inputs that the locators list but the method never uses:** `f_D` (distance method), `SBdisk` and `SBbul`. I recorded them but did not use them. For row 669, the locator lists no `Vbul`, but the method needs it. I read `Vbul` = 0.00 from the row.

## Locator / provenance discrepancies (not method gaps)

- sources.json gives S3's file as `arxiv/1606.09251v1.tar.gz`, but it is actually at `files/1606.09251v1.tar.gz`.
- In the rows.json source_ref text, the placeholders "Υ = [value]" and "H0 = [value]" are never filled in. For reference, the S2 header Note (2) gives H0 = 73, and the method gives Υ_disk = 0.5 and Υ_bul = 0.7.
- These S3 line citations checked out: §2.2 is at SPARC.tex l. 113–121, the helium factor 1.33 is at l. 199, and the sign rule (eq. 2, the |V|V form) is at l. 194–196. METHOD's "SPARC Table 2, note 2" matches S1 header Note (2).
- Not checked: the constant C against astropy, and arXiv:1610.08981 (cited in §4, not supplied). I used C exactly as stated.
