# Gaps

Method incomplete: none. Unreadable values: none. All 10 measurements in rows.json were computed from METHOD.md §1–§3, and every input was found where its locator says (data rows counted from 1, skipping the single `#` header line).

These points do not block any value, but the method text is inaccurate or relies on something I could not check here:

1. METHOD.md §2 says "the README says column 1 is the baryonic acceleration of the bin". It does not say that. README.txt says: "Radius(Mpc or m/s^2): The mean projected distance from the lens center; in Megaparsec for the rotation curve data, or in meter-per-second-squared for the RAR data." Reading column 1 as g_bar depends on the paper (§2.1, l. 174: R-bins chosen to match 15 logarithmic g_bar bins between 1e-15 and 5e-12 m s^-2). I checked that column 1 equals the arithmetic midpoint of the l. 174 bins to the printed 5 significant figures, for all 15 rows of both the kids_bright and gama files.
2. rows.json cites `v2/reading/kids-bins.md` for the midpoint and sources.json cites `reading/kids-d096.md`. Neither file is in the audit folder, so neither was consulted. The midpoint was checked independently against l. 174.
3. rows.json lists only 10 of the 45 measurements METHOD.md describes (m000001, 04, 05, 07, 09, 31, 33, 35, 41, 45). None is from the hot-gas file, so that file's rows were not computed.
4. The README's G unit is written "pc^2/(Msun*s^2)". It should be pc^3. This has no effect: per METHOD.md §1, the README constants are not used.
5. In the method, g_bar keeps the precision printed in the file (5 significant figures). It is not given to more figures because the source does not carry more.

All checks passed: the archive hashes, the member hashes, and the hash of RAR_paper_Brouwer_4.tex match sources.json. The quoted lines 174, 508 and 595 are at the stated line numbers.
