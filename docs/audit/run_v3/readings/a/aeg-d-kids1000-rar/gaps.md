# Gaps

Method incomplete: none. Unreadable values: none.

For all 10 measurements in rows.json, METHOD.md was enough to compute g_obs and g_bar. Every input was found at the place its locator gives (member, data row, column). Archive and member SHA-256 hashes match sources.json, and RAR_paper_Brouwer_4.tex matches the hash in the S2 note.

Observations (none of these blocks a computation):

1. METHOD.md §2 says "the README says column 1 is the baryonic acceleration of the bin". README.txt actually says: "Radius(Mpc or m/s^2): The mean projected distance from the lens center; in Megaparsec for the rotation curve data, or in meter-per-second-squared for the RAR data." So the README describes column 1 as a "mean" in m/s^2, not as g_bar or as a midpoint. For the 10 rows checked, the released values equal the arithmetic midpoints of the §2.1 bins (to the 5 printed digits), as METHOD.md says. The wording that attributes this to the README is inaccurate.
2. The S2 locator line 174 is correct: it is §2.1 ("Mass measurements with weak gravitational lensing", under §2 Theory) and gives "15 logarithmic bins between 1e-15 < g_bar < 5e-12 m s^-2". The quotes at l. 508 and l. 595 were also found as cited.
3. Each data file has a header line, so data row k is file line k+1. The locators count data rows, as METHOD.md states.
4. The 0.1 dex conversion term lives in tables/uncertainty_terms.ecsv, which is not in this folder. It was not needed for g_obs or g_bar and was not checked.
