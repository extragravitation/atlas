# Gaps

Method incomplete: none.
Value unreadable: none.

All 5 rows were computed. Every input was found at the place its locator gives.

## Points where the text was ambiguous (decided as stated; none needed a guess beyond the text)

1. Andromeda XXVIII, m_V,0. In METHOD.md §7 the entry reads "plus the modulus the paper uses (its own, read as above)". "Read as above" could mean the package distance (Savino 2022, 24.36). I used Slater 2015 Table 1 (m − M)0 = 24.55, the paper's own modulus, as the rows.json locator note says explicitly (Slater 2015 p.3, Table 1, rows MV and (m − M)0). If 24.36 were meant instead, m_V,0 would change by 0.19 mag, and g_bar_stars by a factor of 10^(0.4×0.19) ≈ 1.19.
2. Andromeda XVIII, σ. Kvasova 2024 Table 2 (p.7) has a layout where, in the text extraction, the kinematic values look offset from the column headers ("39 stars (57)", "38 stars, (56)", "38 stars, [α/H]"). I took 10.0 km/s as the "38 stars, (56)" value. Three things support this: the p.10 text ("we quote values derived with the exclusion of PAndAS9654 (56 members)"), Table 4 row "This work" (σv = 10.0, Nmem 38), and the other printed value (9.8) sitting under "39 stars (57)".
3. Higgs 2021 (And XVIII, And XXVIII, Leo T). The Rs column of Table 3 is a Sérsic radius, and the paper does not say along which axis it is measured in the table. I treated it as semi-major, as the §7 entries state. The ellipticity is the column "e" of Table 2, defined in Higgs §3 from moments (McConnachie & Irwin 2006). It was taken to be ε = 1 − b/a, as the method assumes; the table itself does not print that definition.
4. Leo T, σ. Geha 2026 Table A1, column (14): the header in the PDF text is garbled ("2r σsys eff"). I used the value in column (14), 6.05 km/s, with errors in columns (15) and (16), as the locator says.
5. Rounding (§3 "Rounding"). I rounded D (kpc), R_h (arcmin), L_V and M_gas to 6 significant figures, and m_V,0 to 4 decimals, before step 8. I computed μ for L_V from the rounded D. The effect is below 1e-5 in relative terms.
6. Eridanus IV, Υ_V. [Fe/H] = −2.87 is below the lowest MW [Fe/H] in the McLaughlin & van der Marel table (−2.29). As §3 step 5 says, I used the end value (M/L)1 = 1.931 and flagged the row beyond_source_range.
7. Upsilon table check. The MW rows have no duplicate [Fe/H] with differing (M/L)1, so the conversion did not stop. All 148 MW rows are at logAge 10.11, and there are 100 unique [Fe/H] values.
