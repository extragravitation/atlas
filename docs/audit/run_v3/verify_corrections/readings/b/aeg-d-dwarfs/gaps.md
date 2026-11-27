# Gaps: aeg-d-dwarfs/v3 audit, reader B

Method incomplete: none. Unreadable: none. I computed all 5 rows in rows.json from values I read in files/.

## Ambiguities and observations (none of them blocked a computation)

1. **The Higgs et al. 2021 ellipticity is not defined as 1 − b/a.** This affects Andromeda XVIII, Andromeda XXVIII and Leo T. METHOD.md §2 defines ε = 1 − b/a. The per-system table and the rows.json locator take ε from Higgs 2021 Table 2, column `e`. Higgs defines `e` on p. 11 (eq. 4) from intensity-weighted second moments: e = sqrt((σxx − σyy)² + σxy²) / (σyy + σxx). The paper does not say this equals 1 − b/a. I used the column as the method names it. R_h = r_h √(1 − e) therefore depends on reading the moment ellipticity as 1 − b/a.
2. **The Putman 2021 locator names a column the file does not have.** The locator names column `galaxy_as_printed`. The MRT file apjabe391t1_mrt.txt has no such column; the name column is `Galaxy` (bytes 1–17). I found the rows by the names the methods page gives: "Andromeda XVIII" (line 192), "Andromeda XXVIII" (line 153), "Antlia 2" (line 129) and "Leo T" (line 145). Eridanus IV is not in the file (only "Eridanus 3" and "Eridanus II" are). This agrees with the methods page.
3. **The modulus μ in the L_V formula.** The method says μ is "the modulus of the package distance D". All five package distances are printed as moduli, so I used each printed modulus directly. Recomputing μ from D after rounding D to 6 significant figures changes L_V by less than 1e-6 in relative terms.
4. **The order of rounding is not fully stated.** "R_h (arcmin) to six significant figures" does not say whether to round before or after circularising. I rounded the circularised R_h. The effect is below 1e-6 relative.
5. **The Leo T σ is not strictly a "global" dispersion.** §2 asks for the global line-of-sight dispersion. Geha 2026 Table A1, column 14, is the dispersion of stars inside 2 r_eff (table note). I used it as the per-system table directs.
6. **The Leo T M_V has no printed uncertainty.** de Jong 2008 Table 1 prints M_V = −8.0 with no error, and the text gives "M_V,total ≃ −8.0". I used −8.0.
7. **The Eridanus IV package modulus has a compound error.** Cerny 2021 Table 1 prints m − M as 19.42 (+0.01 −0.08) ± 0.1. I used the central value 19.42. Heiger 2024 Table 1 prints the same 19.42.
8. **Eridanus IV [Fe/H] is outside the M/L table.** Its [Fe/H] of −2.87 is below the lowest MW-row [Fe/H] in the McLaughlin & van der Marel table (−2.29). Per §3 step 5, I used the end value (M/L)1 = 1.931 and flagged the row beyond_source_range.
9. **rows.json has no gas entry for Eridanus IV.** This is consistent with the methods page ("Not in Putman et al. 2021 Table 1: no gas term").
