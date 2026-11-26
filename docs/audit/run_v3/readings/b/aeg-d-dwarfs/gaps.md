# Gaps found in the method and the sources (reader B)

No row was marked "method incomplete" or "unreadable": every row could be computed. These are the places where the method was unclear, contradicted itself, or where a locator was wrong.

1. **Andromeda XVI (m000013), distance: no column named.** MartinezVazquez 2017, Table 8 (p.18), row And XVI prints four RRL moduli: PWR 23.70, LMRB03 23.73, LMRC03 23.70 and FOBE 23.75. Neither the method nor the locator says which column to use. I used PWR (23.70), because the paper itself says it adopts the PWR distances as final (p.18 text; the abstract also gives 23.70). The method should name the column.
2. **Antlia II (m000024), modulus for m_V,0: unclear which one.** §3.4's route "M_V + (m − M) used by the paper" points me to the modulus in Ji 2021, the paper that gives M_V. That is 20.6 (Table 1, p.7, cited there to Torrealba 2019). But the rows.json locator for apparent_magnitude names Vivas 2022 (S104), whose modulus is 20.47. I used 20.6. If 20.47 is meant, L_V and g_bar both go up by a factor of 10^(0.4×0.13) ≈ 1.127. The M_V value itself is not in Vivas 2022 at all. The method's word "(cited)" is not defined.
3. **Higgs 2021 ellipticity is in a different table than the locator says (And XVIII m000015, Leo T m000047).** Both the locator and the method text say r_h and ε come from Table 3, but Table 3 has no ellipticity. I read ε from Table 2 on the same page (p.16, column e). The method also does not say that Higgs' Sérsic R_s is a semi-major radius. The paper measures its profiles along the semi-major axis (SMA), which agrees with the "semi-major" convention.
4. **Per-system "Read from" text in METHOD.md contradicts rows.json for σ.**
   - Andromeda XVIII says "Kvasova 2024 (arXiv 1112.1067v3), p9, Table 3, row And XVIII, column σLOS". That is Tollerud's locator text. Kvasova's value is in Table 2 (p.7) and Table 4 (p.11).
   - Leo T and Ursa Major I say "Geha 2026 (arXiv 0706.0516v2), p9, Table 3". The supplied file is 2602.10200v2, and the values are in Table A1, pp.32–34.
   - Ursa Minor quotes "σv 8.7+0.3−0.3 … arXiv 2002.09503v2 p.9 Table 3". That paper is not supplied. The locator's Geha 2026 Table A1 gives 8.86, and I used 8.86.
   - Fornax names Hendricks "arXiv 0811.0118v1"; the supplied file is 1408.5597v1. The value 11.84 is at the locator (p.5, §2.1).
   - Andromeda XI, XII and XIX (not among my rows) also cite mismatched arXiv IDs.
   In every case I used the rows.json locator.
5. **Kvasova 2024 Table 2: column layout is ambiguous.** In the extracted text the kinematic values do not line up clearly with the "38 stars" column. The value 10.0 (+1.1 −1.0) km/s was confirmed against Table 4, row "This work" (Nmem 38), and the §4.1 text, which quotes the 56-member/PAndAS9654-excluded values.
6. **Fornax (m000038), which radius.** Wang 2019 Table 1's Sérsic column prints both "Sersic r_s" (16.4′) and "2D Half-light r_h" (20.1′). The method says "half-light radius", and tex line 106 is the 2D half-light row, so I used 20.1′. Wang does not state the axis, so semi-major is assumed per D-052. The ellipticity (0.31) is from the same column, tex line 97 and PDF p.4.
7. **Ellipticity in Muñoz 2018 Table 5.** The method does not name the ellipticity column for UMi and UMa I. I used the Sérsic-fit ellipticity in the same row of Table 5 (0.55 and 0.57).
8. **Υ_V beyond the table range.** The MW rows span [Fe/H] −2.29 to +0.22. Hydrus I (−2.52), Boötes III (−2.34) and UMa I (−2.56) take the end value (M/L)1 = 1.931 at −2.29 (flag beyond_source_range), as §3.5 says.
9. **Rounding.** I applied the §3 rounding: R_h, D, L_V and M_gas to 6 significant figures, and m_V,0 to 4 decimals, before step 8.
10. **Boötes III.** I read the distance as a modulus (18.43) as the per-system table says; Li 2026 also prints 48.5 kpc. The Moskowitz 1-Plummer Rh,1c (33.03′) is circularised, so ε (0.33) is not used.
