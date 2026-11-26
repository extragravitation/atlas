# Gaps

Method incomplete: none. All 10 rows could be computed from METHOD.md alone.
Unreadable values: none.

Observations. None of these changed any value.

1. veldis.html spacer rows. These are `<tr> <td>&nbsp; </td></tr>`: they have one blank cell, not "no cells" as METHOD.md says. I skipped any row with fewer than 7 cells. No data row has fewer than 7 cells, so no bin is affected.
2. mwgc.dat column reading. METHOD.md says to read by "the character positions of its column label" but does not say how a value that is only partly under the label is handled. The values are right-aligned and only partly lie under the label. I took the single whitespace-delimited token that overlaps the label's character span. For every value used, exactly one token overlapped, so the reading is unambiguous.
3. File paths and hashes in sources.json. S5 and S7 are listed as `mvdm05/J_ApJS_161_304_*.vot`, but in this folder they are `files/J_ApJS_161_304_*.vot`. Their whole-file SHA-256 values do not match sources.json:
   - clusters: 99beb657...
   - models: c637c20e...
   
   The files record request_date 2026-11-25, not the 2026-10-30 retrieval. Their `content_sha256` from `<RESOURCE` does match sources.json (619b71cf..., 3109d33f...), which fits sources.json's own note that a re-export changes only the header lines. veldis.html and mwgc.dat match their listed SHA-256.
4. rows.json sigma locators give `<r> = [value]` placeholders, not the bin radii. The bins were found by cluster and Type RV, as METHOD.md §2 says. The number of RV bins found matches the number of sigma_los inputs in rows.json for every row.
5. Profile choice. For all 10 clusters, RV is the only line-of-sight Type on the page, and it passes the plotting rules: at least 2 bins, and coverage from 0.926 (IC 4499) to 1.000. So the §3 default is RV, as rows.json says. The §3 tie-break for Types from the same year (C22 vs G22, F13 vs L13) is not fully specified, but no row here needs it.
6. Check of the King model. log10 x_t reproduces the models-table Conc to the printed 2 decimals for all 10 clusters. A second, independent integrator (scipy solve_ivp plus adaptive quad) changes g_obs by at most 5e-5 (relative).
