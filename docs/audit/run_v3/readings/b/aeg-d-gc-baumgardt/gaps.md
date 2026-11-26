# Gaps

No row is marked "method incomplete" or "unreadable". All 10 rows were computed, and every input was found where its locator points.

Some wording in the method was ambiguous or short of complete. None of these points changed any value, because each had only one possible reading in these files:

1. **mwgc.dat, ID field.** The method says a row is matched by "the ID (the first field)". But IDs contain a space (for example "NGC 288" and "IC 4499"), so splitting on white space gives "NGC" or "IC". The method does not give the width of the ID field. I used the fixed-width columns 1 to 12 of each data line, which contain only the ID in Parts I to III for every cluster used here.
2. **mwgc.dat, value positions.** The method says to read "by the character positions of its column label", but it does not say how a value lines up with its label: values are not confined to the label's characters. I took the single whitespace-delimited token that overlaps the label's character span. That gave one unambiguous token for R_Sun, M_V,t and V_t in every row.
3. **veldis.html, spacer rows.** The spacer rows are `<tr> <td>&nbsp; </td></tr>`. They have one blank cell, not "no cells" as the method says. I skipped any row with fewer than 7 cells. Their blank first cell would carry the name down anyway, and they carry no Type, so they cannot become bins.
4. **Bin locators in rows.json.** The per-bin locators print `<r> = [value]"`, a placeholder, not the actual radius. Each bin therefore could not be checked against its own locator individually. I checked the count instead: the number of RV rows read for each cluster equals the number of sigma_los inputs listed in rows.json for that row (9, 6, 5, 7, 5, 2, 20, 4, 2, 14).
5. **Default-choice tie-break.** The year tie-break gives no year for `RV`. It is not needed, because `RV` ranks first by rule 1. In all 10 clusters, RV is the only line-of-sight Type present.
6. **Numerical sensitivity.** These are not gaps, just results from the stated numerics (RK4 in ln x, 400 steps per decade, trapezoid projections):
   - Raising the resolution to 3000 steps per decade changes g_obs by at most 5e-5 relative.
   - g_bar is unaffected.
   - log10 x_t reproduces Conc for every row to the printed 2 decimals.
   - NGC 6496 has W0 = 0.30 with Conc = 0.00, an extreme but self-consistent fit.
