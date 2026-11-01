# Screening S9 — cluster names in A9 and stellar-mass records (part 2)

Prepared 2026-10-31 by Claude (AI assistance, disclosed). Exploratory source-reading record; not a data package.

**What this file holds.** For each record: the citation, the URL(s) read, the table read, and every cluster name with its redshift exactly as printed in that table. No masses, fractions, ratios, velocity dispersions or other results are recorded here, even where the same table prints them.

**How it was read.** Each paper's arXiv abstract page (`https://arxiv.org/abs/<id>`) was read to confirm title, journal reference and DOI. The arXiv LaTeX source (`https://arxiv.org/e-print/<id>`) was downloaded and the sample table's name and redshift columns were extracted by script, then spot-checked against the source lines. The SHA-256 given is of the downloaded e-print file. VizieR/CDS (`cdsarc`, `vizier.cds.unistra.fr`), the GAVO mirror (`dc.g-vo.org`), `aanda.org`, `academic.oup.com` and `sdss.org` were refused by this session's network proxy, so **no VizieR ReadMe or table was read** for any record.

**Rendering conventions.** LaTeX was rendered to plain text: `$-$` and `$+$` to `-` and `+`, `~` to a space, `$\pm$` to `±`, and runs of spaces in names collapsed to one. Nothing else was changed. "Below z = 0.30" means strictly less than 0.30, using the printed redshift. Where a table prints a velocity (cz) instead of z, the count uses z ≈ cz/c and says so.

## Summary

| Record | Clusters named | Below z = 0.30 | Table read |
|---|---|---|---|
| C20a Rines+2013 HeCS | 58 | 58 | Table 1 |
| C20c Logan+2022 CHeCS | 44 | 44 | Table 1 |
| C20d Pizzardo+2021 CIRS+HeCS | 129 (71 CIRS + 58 HeCS) | 129 | CIRS table + HeCS table |
| C21a Rines+2003 CAIRNS I | 9 (8 CAIRNS + A194) | 9 (cz) | Table 1 |
| C21b Rines+2004 CAIRNS II | 9 | 9 (cz) | Table 1 |
| C22 van der Marel+2000 CNOC1 | 16 (from Carlberg+1996, Table 1; the paper itself prints no list) | 8 | Carlberg+1996 Table 1 |
| C24a Biviano & Girardi 2003 2dFGRS | 43 | 43 (cz) | Table 1 |
| C26 Mamon+2019 WINGS | 54 **not identified by name**; parent list of 73 from Cava+2017 | 73 (parent) | Cava+2017 Table 1 |
| C29a Liu+2024 eRASS1 | 22 | 12 | Table 1 |
| C29b CHEX-MATE kinematics 2025 | 75 (+2 extra clusters, +3 sub-component rows) | 59 of the 75 | Table A.1 |
| S9a Zhang+2016 DES X-ray clusters | 106 | 30 | BCG table |
| S10b Chiu+2018 SPT 91 | 91 | 6 | Table 1 |
| S15a Bellstedt+2016 BCGs | 123 with a BCG stellar mass | 34 | Appendix BCG results table |
| S15c Erfanianfar+2019 | **not read** (catalogue hosted outside the paper; host blocked) | — | — |


## C20a — Rines, Geller, Diaferio & Kurtz 2013, ApJ 767, 15 (2013ApJ...767...15R)

**URLs read:**
- https://arxiv.org/abs/1209.3786 (title, DOI 10.1088/0004-637X/767/1/15)
- https://arxiv.org/e-print/1209.3786 (SHA-256 293f6e9dca6764ba1bb97f40d2f6eb284e000172aea665e08eb907d7246c05a5)

**Table/file read:** Table 1, "HeCS Basic Properties" (file `rine0917v2astroph.tex`); columns Name and z_⊙.

**Name — z_⊙** (58):

- A267 — 0.2291
- Zw1478 — 0.1027
- A646 — 0.1273
- A655 — 0.1271
- A667 — 0.1452
- A689 — 0.2789
- A697 — 0.2812
- A750 — 0.1640
- MS0906 — 0.1767
- A773 — 0.2173
- A795 — 0.1374
- Zw2701 — 0.2160
- A963 — 0.2041
- A980 — 0.1555
- Zw3146 — 0.2894
- A990 — 0.1416
- Zw3179 — 0.1422
- A1033 — 0.1220
- A1068 — 0.1386
- A1132 — 0.1351
- A1201 — 0.1671
- A1204 — 0.1706
- A1235 — 0.1030
- A1246 — 0.1921
- A1302 — 0.1152
- A1361 — 0.1159
- A1366 — 0.1160
- A1413 — 0.1412
- A1423 — 0.2142
- A1437 — 0.1333
- A1553 — 0.1668
- A1682 — 0.2272
- A1689 — 0.1842
- A1758 — 0.2760
- A1763 — 0.2312
- A1835 — 0.2506
- A1902 — 0.1623
- A1918 — 0.1388
- A1914 — 0.1660
- A1930 — 0.1308
- A1978 — 0.1459
- A2009 — 0.1522
- RXJ1504 — 0.2168
- A2034 — 0.1132
- A2050 — 0.1191
- A2055 — 0.1023
- A2069 — 0.1139
- A2111 — 0.2291
- A2187 — 0.1829
- A2219 — 0.2257
- Zw8197 — 0.1132
- A2259 — 0.1605
- RXJ1720 — 0.1604
- A2261 — 0.2242
- RXJ2129 — 0.2339
- A2396 — 0.1919
- A2631 — 0.2765
- A2645 — 0.2509

**Count below z = 0.30:** 58 of 58.


## C20c — Logan et al. 2022, A&A 665, A124 (2022A&A...665A.124L)

**URLs read:**
- https://arxiv.org/abs/2202.08569 (jref A&A 665, A124 (2022))
- https://arxiv.org/e-print/2202.08569 (SHA-256 ee98e85a1a8a44de2258cf9f9fb1ec786091b1066a94687dffa3534acb792af4)

**Table/file read:** Table 1 `table.samplesummary`, "Summary of sample" (file `checs50-aa.tex`); columns Cluster, Short name, z (spectroscopic).

**Cluster (Short name) — z** (44):

- ZwCl 0755.8+5408 (Zw1478) — 0.1027
- Abell 0655 (A655) — 0.1271
- Abell 0697 (A697) — 0.2812
- MS 0906.5+1110 (MS0906) — 0.1767
- Abell 0773 (A773) — 0.2173
- Abell 0795 (A795) — 0.1374
- ZwCl 0949.6+5207 (Zw2701) — 0.2160
- Abell 0963 (A963) — 0.2041
- Abell 0980 (A980) — 0.1555
- ZwCl 1021.0+0426 (Zw3146) — 0.2894
- Abell 0990 (A990) — 0.1416
- ZwCl 1023.3+1257 (Zw3179) — 0.1422
- Abell 1033 (A1033) — 0.1220
- Abell 1068 (A1068) — 0.1386
- Abell 1132 (A1132) — 0.1351
- Abell 1201 (A1201) — 0.1671
- Abell 1204 (A1204) — 0.1706
- Abell 1235 (A1235) — 0.1030
- Abell 1246 (A1246) — 0.1921
- Abell 1302 (A1302) — 0.1152
- Abell 1413 (A1413) — 0.1412
- Abell 1423 (A1423) — 0.2142
- Abell 1437 (A1437) — 0.1333
- Abell 1553 (A1553) — 0.1668
- Abell 1682 (A1682) — 0.2272
- Abell 1689 (A1689) — 0.1842
- Abell 1763 (A1763) — 0.2312
- Abell 1835 (A1835) — 0.2506
- Abell 1918 (A1918) — 0.1388
- Abell 1914 (A1914) — 0.1660
- Abell 1930 (A1930) — 0.1308
- Abell 1978 (A1978) — 0.1459
- Abell 2009 (A2009) — 0.1522
- RXCJ 1504.1-0248 (RXJ1504) — 0.2168
- Abell 2034 (A2034) — 0.1132
- Abell 2050 (A2050) — 0.1191
- Abell 2069 (A2069) — 0.1139
- Abell 2111 (A2111) — 0.2291
- Abell 2219 (A2219) — 0.2257
- ZwCl 1717.9+5636 (Zw8197) — 0.1132
- Abell 2259 (A2259) — 0.1605
- RXCJ 1720+2638 (RXJ1720) — 0.1604
- Abell 2261 (A2261) — 0.2242
- RXCJ 2129+0005 (RXJ2129) — 0.2339

**Count below z = 0.30:** 44 of 44.


## C20d — Pizzardo et al. 2021, A&A 646, A105 (2021A&A...646A.105P)

**URLs read:**
- https://arxiv.org/abs/2005.11562 (jref A&A 646, A105 (2021))
- https://arxiv.org/e-print/2005.11562 (SHA-256 fd354e9738eb75d59b3701fbe54c01bef92e6c05080a04f9e0aaade4a009d505)

**Table/file read:** Tables `CIRSsample` ("CIRS clusters") and `HeCS sample` ("HeCS clusters") (file `38481corr.tex`); columns cluster and z.

**Notes:** 71 + 58 = 129, matching the abstract. The HeCS table is split into low-mass and high-mass halves; the order is kept. Names are printed with zero-padding (e.g. A0646), unlike C20a.

**CIRS: cluster — z** (71):

- A0085 — 0.055
- A0119 — 0.044
- A0160 — 0.043
- A0168 — 0.045
- A0295 — 0.042
- A0602 — 0.060
- A0671 — 0.050
- A0757 — 0.051
- A0779 — 0.023
- A0954 — 0.096
- A0957 — 0.046
- A0971 — 0.092
- A1035A — 0.068
- A1035B — 0.078
- A1066 — 0.069
- A1142 — 0.036
- A1173 — 0.076
- A1190 — 0.076
- A1205 — 0.076
- A1291A — 0.051
- A1291B — 0.059
- A1314 — 0.033
- A1377 — 0.052
- A1424 — 0.075
- A1436 — 0.064
- A1552 — 0.086
- A1650 — 0.084
- A1663 — 0.084
- A1728 — 0.089
- A1750 — 0.085
- A1767 — 0.071
- A1773 — 0.078
- A1809 — 0.079
- A1885 — 0.089
- A2061 — 0.077
- A2064 — 0.074
- A2067 — 0.077
- A2110 — 0.097
- A2124 — 0.066
- A2142 — 0.089
- A2149 — 0.065
- A2169 — 0.058
- A2175 — 0.096
- A2197 — 0.030
- A2199 — 0.031
- A2244 — 0.099
- A2245 — 0.088
- A2249 — 0.085
- A2255 — 0.080
- A2399 — 0.058
- A2428 — 0.084
- A2593 — 0.042
- A2670 — 0.076
- MKW04 — 0.020
- MKW08 — 0.027
- MKW11 — 0.023
- MS1306 — 0.083
- NGC4325 — 0.025
- NGC6107 — 0.032
- NGC6338 — 0.029
- RXCJ1022p3830 — 0.054
- RXCJ1053p5450 — 0.073
- RXCJ1115p5426 — 0.069
- RXCJ1210p0523 — 0.077
- RXCJ1326p0013 — 0.084
- RXCJ1351p4622 — 0.063
- RXCJ2214p1350 — 0.026
- RXJ0137 — 0.041
- SHK352 — 0.049
- Zw1215p0400 — 0.077
- Zw1665 — 0.030

**HeCS: cluster — z** (58):

- A0646 — 0.127
- A0655 — 0.127
- A0667 — 0.145
- A0689 — 0.279
- A0750 — 0.164
- A0990 — 0.141
- A1033 — 0.122
- A1068 — 0.138
- A1132 — 0.135
- A1201 — 0.167
- A1204 — 0.170
- A1235 — 0.103
- A1302 — 0.116
- A1361 — 0.116
- A1366 — 0.116
- A1423 — 0.214
- A1902 — 0.163
- A1918 — 0.140
- A1930 — 0.131
- A1978 — 0.146
- A2055 — 0.103
- A2187 — 0.183
- A2259 — 0.160
- A2261 — 0.225
- RXJ1720 — 0.160
- RXJ2129 — 0.234
- Zw1478 — 0.103
- Zw3179 — 0.142
- Zw8197 — 0.113
- A0267 — 0.229
- A0697 — 0.282
- A0773 — 0.218
- A0795 — 0.137
- A0963 — 0.204
- A0980 — 0.156
- A1246 — 0.192
- A1413 — 0.141
- A1437 — 0.133
- A1553 — 0.167
- A1682 — 0.227
- A1689 — 0.184
- A1758 — 0.276
- A1763 — 0.231
- A1835 — 0.252
- A1914 — 0.166
- A2009 — 0.152
- A2034 — 0.113
- A2050 — 0.119
- A2069 — 0.114
- A2111 — 0.230
- A2219 — 0.226
- A2396 — 0.192
- A2631 — 0.277
- A2645 — 0.251
- MS0906 — 0.177
- RXJ1504 — 0.216
- Zw2701 — 0.215
- Zw3146 — 0.290

**Count below z = 0.30:** 129 of 129.


## C21a — Rines, Geller, Kurtz & Diaferio 2003, AJ 126, 2152 (2003AJ....126.2152R), CAIRNS I

**URLs read:**
- https://arxiv.org/abs/astro-ph/0306538 (jref Astron.J.126:2152,2003)
- https://arxiv.org/e-print/astro-ph/0306538 (SHA-256 4f0148f19d0beb07c73c6d626b2cccf8bfc011d5fcc4cca5f9333df69bda9418)

**Table/file read:** Table 1, "CAIRNS Basic Properties" (file `Rines.tex`); columns Cluster and cz_⊙ (km s⁻¹).

**Notes:** **No z column is printed; the table gives heliocentric cz in km s⁻¹, which is recorded here as printed.** The 8 CAIRNS clusters are listed above a rule. A194 is listed below it as a ninth system that lies in the A168 survey region. Commented-out rows in the source (A193, A426, A2063, A2107, A2147, A2657) are not printed and are not listed.

**Cluster — cz_⊙ [km s⁻¹]** (9):

- A119 — 13268
- A168 — 13395
- A496 — 9900
- A539 — 8717
- A576 — 11510
- A1367 — 6495
- A1656 — 6973
- A2199 — 9101
- A194 — 5341

**Count below z = 0.30:** 9 of 9. The largest printed cz is 13395 km s⁻¹, so z ≈ cz/c ≈ 0.045.


## C21b — Rines, Geller, Diaferio, Kurtz & Jarrett 2004, AJ 128, 1078 (2004AJ....128.1078R), CAIRNS II

**URLs read:**
- https://arxiv.org/abs/astro-ph/0402242 (jref Astron.J.128:1078,2004)
- https://arxiv.org/e-print/astro-ph/0402242 (SHA-256 192aaf8fae047ec1e4ae4f2af16af0dfe141a1097c8ce8783a19c32ca6c35373)

**Table/file read:** Table 1, "CAIRNS Parent Population" (file `Rines.tex`); columns Cluster and cz_⊙ (km s⁻¹).

**Notes:** No z column; cz as printed. These are the same 9 systems as C21a; this table prints "Coma" where C21a prints "A1656". The text says A194 is analysed as a ninth system. A147 and A2197 are named in the text and keywords but are not separate table rows.

**Cluster — cz_⊙ [km s⁻¹]** (9):

- A119 — 13268
- A168 — 13395
- A496 — 9900
- A539 — 8717
- A576 — 11510
- A1367 — 6495
- Coma — 6973
- A2199 — 9101
- A194 — 5341

**Count below z = 0.30:** 9 of 9 (largest printed cz 13395 km s⁻¹).


## C22 — van der Marel, Magorrian, Carlberg, Yee & Ellingson 2000, AJ 119, 2038 (2000AJ....119.2038V), CNOC1

**URLs read:**
- https://arxiv.org/abs/astro-ph/9910494 (DOI 10.1086/301351)
- https://arxiv.org/e-print/astro-ph/9910494 (SHA-256 36b2c37d4bbec27f0451dfde091cfbd13157ff10aeba327f23352c522c27acee)
- https://arxiv.org/abs/astro-ph/9509034 (Carlberg et al. 1996, ApJ 462, 32: the list the paper points to)
- https://arxiv.org/e-print/astro-ph/9509034 (SHA-256 dae70d3fed57266e9c1cc0f98180191aeae0fd9735991b1f783e366d1f603e46)

**Table/file read:** **C22 prints no list of clusters.** It says redshifts were obtained for 16 clusters at z = 0.17–0.55 and refers to "Table 4 of C96 and Table 1 of C97b" for per-cluster quantities. The names below are from Carlberg et al. 1996 (C96), Table 1 `tab:lim`, "Cluster Redshift and Field Limits"; columns Name and z.

**Notes:** C22 excludes MS 0906+11 and MS 1358+62 ("strong binaries") and analyses the galaxies of the remaining 14 clusters as one stacked (ensemble) sample. It gives no per-cluster profiles.

**Name — z (C96 Table 1)** (16):

- A2390 — 0.2280
- MS0016+16 — 0.5466
- MS0302+16 — 0.4246
- MS0440+02 — 0.1965
- MS0451+02 — 0.2011
- MS0451-03 — 0.5392
- MS0839+29 — 0.1928
- MS0906+11 — 0.1705
- MS1006+12 — 0.2605
- MS1008-12 — 0.3062
- MS1224+20 — 0.3255
- MS1231+15 — 0.2348
- MS1358+62 — 0.3290
- MS1455+22 — 0.2568
- MS1512+36 — 0.3726
- MS1621+26 — 0.4274

**Count below z = 0.30:** 8 of 16 (A2390, MS0440+02, MS0451+02, MS0839+29, MS0906+11, MS1006+12, MS1231+15, MS1455+22). MS0906+11 is one of the two that C22 excludes.


## C24a — Biviano & Girardi 2003, ApJ 585, 205 (2003ApJ...585..205B)

**URLs read:**
- https://arxiv.org/abs/astro-ph/0301439 (jref Astrophys.J. 585 (2003) 205-214)
- https://arxiv.org/e-print/astro-ph/0301439 (SHA-256 b09268803175a9078042031160bb452e9cffc3f0f6960387f3b51881c7e59962)

**Table/file read:** Table 1 `tabsample`, "The sample of 43 clusters" (file `abmg.tex`); columns Name and v̄ (km s⁻¹).

**Notes:** **No z column is printed; the table gives the mean velocity v̄ in km s⁻¹, recorded as printed.**

**Name — v̄ [km s⁻¹]** (43):

- ACO 419 — 20499
- ACO 892 — 28130
- ACO 957 — 13648
- ACO 978 — 16371
- ACO 993 — 16368
- ACO 1098 — 20699
- ACO 1308 — 15496
- ACO 1364 — 31681
- ACO 1373 — 38892
- ACO 1750 — 25187
- ACO 2660 — 15968
- ACO 2726 — 18220
- ACO 2734 — 18437
- ACO 2915 — 25877
- ACO 2967 — 33036
- ACO 2981 — 32484
- ACO 3042 — 31161
- ACO 3814 — 35819
- ACO 3837 — 27390
- ACO 4044 — 32917
- ACO 4049 — 17743
- ACO 4053 — 21451
- ACO S246 — 17776
- ACO S301 — 6772
- ACO S340 — 20840
- ACO S983 — 17246
- ACO S1127 — 31259
- APM 171 — 29038
- APM 294 — 39891
- APM 311 — 32608
- APM 416 — 31360
- APM 715 — 21726
- APM 880 — 25126
- EDCC 69 — 6385
- EDCC 129 — 11400
- EDCC 148 — 23395
- EDCC 153 — 17130
- EDCC 155 — 10118
- EDCC 445 — 18511
- EDCC 601 — 29200
- EDCC 623 — 25369
- EDCC 641 — 31236
- EDCC 642 — 32513

**Count below z = 0.30:** 43 of 43. The largest printed v̄ is 39891 km s⁻¹, so z ≈ 0.13.


## C26 — Mamon, Cava, Biviano et al. 2019, A&A 631, A131 (2019A&A...631A.131M), WINGS II

**URLs read:**
- https://arxiv.org/abs/1901.06393 (jref A&A 631, A131 (2019))
- https://arxiv.org/e-print/1901.06393 (SHA-256 063de54a931e6264001f80fb20faf97901f85651179e93785f84076c7bed3081)
- https://arxiv.org/abs/1708.08541 (Cava et al. 2017, A&A 606, A108 = "Paper I")
- https://arxiv.org/e-print/1708.08541 (SHA-256 c3cba02dc6f9199119ca47470e412990ca9ff9337622b6b742d20cce3d60095d)

**Table/file read:** **C26 does not name its 54 clusters.** Its only sample table, "Stacked clusters", gives stacked quantities. Its text says: 73 WINGS clusters (Paper I), minus 15 irregular ones, leaves 58 regular; of these, the 54 with N_m ≥ 30 members within R_200 are used. The names below are the **parent list of 73** from Cava et al. 2017, Table 1 `tab:clusters`, "WINGS cluster properties" (file `paper1.tex`); columns Id and z̄.

**Notes:** The 54-cluster subset is not reconstructed here. Doing so would mean applying the selection to tabulated values, and it is ambiguous: 16 rows have P_DS < 0.05 against the 15 "irregular" stated, and the N_m column counts all members, not only those within R_200. To name the 54 we need the authors' list or a ruling on the reconstruction.

**Id — z̄ (Cava+2017 Table 1, all 73)** (73):

- A85 — 0.055
- A119 — 0.044
- A133 — 0.056
- A147 — 0.044
- A151 — 0.053
- A160 — 0.044
- A168 — 0.045
- A193 — 0.048
- A376 — 0.048
- A500 — 0.068
- A548b — 0.043
- A602 — 0.060
- A671 — 0.050
- A754 — 0.055
- A780 — 0.055
- A957 — 0.045
- A970 — 0.059
- A1069 — 0.065
- A1291 — 0.054
- A1631a — 0.046
- A1644 — 0.047
- A1668 — 0.064
- A1736 — 0.046
- A1795 — 0.063
- A1831 — 0.063
- A1983 — 0.045
- A1991 — 0.058
- A2107 — 0.042
- A2124 — 0.066
- A2149 — 0.065
- A2169 — 0.058
- A2256 — 0.058
- A2271 — 0.057
- A2382 — 0.064
- A2399 — 0.058
- A2415 — 0.058
- A2457 — 0.059
- A2572a — 0.039
- A2589 — 0.041
- A2593 — 0.041
- A2622 — 0.061
- A2626 — 0.057
- A2657 — 0.040
- A2717 — 0.049
- A2734 — 0.061
- A3128 — 0.060
- A3158 — 0.059
- A3266 — 0.059
- A3376 — 0.046
- A3395 — 0.050
- A3490 — 0.069
- A3497 — 0.068
- A3528a — 0.054
- A3528b — 0.054
- A3530 — 0.054
- A3532 — 0.055
- A3556 — 0.048
- A3558 — 0.047
- A3560 — 0.049
- A3667 — 0.055
- A3716 — 0.045
- A3809 — 0.063
- A3880 — 0.058
- A4059 — 0.049
- IIZW108 — 0.048
- MKW3s — 0.045
- RX0058 — 0.048
- RX1022 — 0.054
- RX1740 — 0.044
- Z1261 — 0.065
- Z2844 — 0.050
- Z8338 — 0.049
- Z8852 — 0.041

**Count below z = 0.30:** 73 of 73 (parent list); by implication all 54 used clusters are below 0.30.


## C29a — Liu et al. 2024, A&A 692, A253 (2024A&A...692A.253L)

**URLs read:**
- https://arxiv.org/abs/2411.09735 (jref A&A 692, A253 (2024))
- https://arxiv.org/e-print/2411.09735 (SHA-256 dae53e94223621ae0023a7d9185b94eb27bf08f956a1cbeb775d442b8c6fdad2)

**Table/file read:** Table 1 `tab:Cluster`, "Properties of the 22 selected clusters" (file `eROClusters.tex`); columns 1eRASS Cluster and z_spec.

**Notes:** The table's name column is headed "1eRASS Cluster" and the entries print only the J-designation, so the full names read "1eRASS J…" (as used in the figure captions).

**1eRASS Cluster — z_spec** (22):

- J004049.8-440743 — 0.3493
- J004207.1-283154 — 0.1075
- J024339.2-483339 — 0.4983
- J034656.2-543854 — 0.5286
- J043817.8-541917 — 0.4218
- J052806.2-525951 — 0.7681
- J055942.9-524851 — 0.6087
- J073220.0+313748 — 0.1705
- J073721.1+351739 — 0.2094
- J080056.9+360324 — 0.2866
- J082317.9+155700 — 0.1529
- J084257.5+362208 — 0.2818
- J090131.5+030055 — 0.1936
- J101703.2+390250 — 0.2048
- J115518.0+232422 — 0.1422
- J121741.6+033931 — 0.0773
- J125922.4-041138 — 0.0843
- J130252.8-023059 — 0.0838
- J213056.8-645842 — 0.3163
- J213536.8-572622 — 0.4268
- J213800.9-600758 — 0.3188
- J235137.0-545253 — 0.3838

**Count below z = 0.30:** 12 of 22.


## C29b — "CHEX-MATE: exploring the kinematical properties of Planck galaxy clusters", A&A 699, A88 (2025) (2025A&A...699A..88P)

**URLs read:**
- https://arxiv.org/abs/2505.03708 (jref A&A 699, A88 (2025))
- https://arxiv.org/e-print/2505.03708 (SHA-256 50ceaf03c0b132d9a3e115a1e68dee501d9ab34402f14fc35090790df389ed7d)

**Table/file read:** Appendix table `tab:results` (four continued parts; file `aa.tex`); columns "PSZ2 name" and z. Rows were joined across line breaks before extraction. Commented-out rows (e.g. G262.27-35.38, G080.16+57.65, G099.48+55.60) are not printed and are excluded.

**Notes:** The table has 80 printed rows: the 75 sample clusters; 2 extra clusters that the appendix says were also run despite having fewer than 50 members (PSZ2G113.91-37.01 at z 0.3677, PSZ2G083.29-31.03 at z 0.4102); and 3 sub-component rows for the bimodal systems (G040.03+74.95a; G218.81+35.51 a and b). Names are printed without the "PSZ2 " prefix, which the column header supplies.

**PSZ2 name — z (all 80 printed rows)** (80):

- G049.22+30.87 — 0.1606
- G226.18+76.79 — 0.1415
- G053.53+59.52 — 0.1136
- G056.77+36.32 — 0.09696
- G042.81+56.61 — 0.07225
- G033.81+77.18 — 0.06272
- G041.45+29.10 — 0.1771
- G238.69+63.26 — 0.1672
- G080.41-33.24 — 0.1101
- G048.10+57.16 — 0.07782
- G287.46+81.12 — 0.07194
- G031.93+78.71 — 0.07533
- G067.17+67.46 — 0.1667
- G006.49+50.56 — 0.07854
- G124.20-36.48 — 0.1921
- G021.10+33.24 — 0.1511
- G044.20+48.66 — 0.08987
- G075.71+13.51 — 0.05455
- G324.04+48.79 — 0.4505
- G284.41+52.45 — 0.4399
- G349.46-59.95 — 0.3465
- G008.94-81.22 — 0.3064
- G266.04-21.25 — 0.2965
- G107.10+65.32 — 0.2772
- G340.36+60.58 — 0.251
- G072.62+41.46 — 0.2255
- G055.59+31.85 — 0.2255
- G159.91-73.50 — 0.2095
- G195.75-24.32 — 0.2007
- G313.33+61.13 — 0.1848
- G208.80-30.67 — 0.2468
- G172.98-53.55 — 0.374
- G205.93-39.46 — 0.4409
- G273.59+63.27 — 0.1335
- G057.61+34.93 — 0.08492
- G046.88+56.48 — 0.1137
- G243.64+67.74 — 0.08108
- G008.31-64.74 — 0.3153
- G285.63+72.75 — 0.1667
- G077.90-26.63 — 0.1449
- G114.79-33.71 — 0.09447
- G224.00+69.33 — 0.1917
- G113.91-37.01 — 0.3677
- G067.52+34.75 — 0.1822
- G113.29-29.69 — 0.103
- G192.18+56.12 — 0.1268
- G179.09+60.12 — 0.1397
- G283.91+73.87 — 0.08635
- G149.39-36.84 — 0.1699
- G040.03+74.95 — 0.07067
- G040.03+74.95a — 0.07558
- G217.09+40.15 — 0.1382
- G172.74+65.30 — 0.07529
- G105.55+77.21 — 0.07242
- G066.68+68.44 — 0.1625
- G050.40+31.17 — 0.1605
- G057.78+52.32 — 0.06628
- G040.58+77.12 — 0.0754
- G028.63+50.15 — 0.09083
- G186.37+37.26 — 0.2818
- G228.16+75.20 — 0.5423
- G286.98+32.90 — 0.386
- G028.89+60.13 — 0.1519
- G087.03-57.37 — 0.2761
- G071.63+29.78 — 0.1575
- G073.97-27.82 — 0.2282
- G092.71+73.46 — 0.2317
- G187.53+21.92 — 0.1707
- G278.58+39.16 — 0.3063
- G218.81+35.51 — 0.1663
- G218.81+35.51 a — 0.1643
- G218.81+35.51 b — 0.1776
- G049.32+44.37 — 0.09606
- G046.10+27.18 — 0.3878
- G262.73-40.92 — 0.4218
- G206.45+13.89 — 0.4054
- G083.29-31.03 — 0.4102
- G201.50-27.31 — 0.539
- G057.25-45.34 — 0.3977
- G111.61-45.71 — 0.5477

**Count below z = 0.30:** 59 of the 75 sample clusters; 0 of the 2 extras; 3 of the 3 sub-component rows (62 of the 80 rows).


## S9a — Zhang et al. 2016, ApJ 816, 98 (2016ApJ...816...98Z; VizieR 2016yCat..18160098Z)

**URLs read:**
- https://arxiv.org/abs/1504.02983 (DOI 10.3847/0004-637X/816/2/98)
- https://arxiv.org/e-print/1504.02983 (SHA-256 c7b533f07bf5f2b9a862f2e38d2362a01953fef64d9da1df84df3d9de3322c28)

**Table/file read:** BCG table `tbl:bcgs` (file `table_bcg.tex`, input to `bcg_evolution.tex`); columns Cluster Name and Cluster Redshift. Each row also carries a BCG stellar mass, which is not recorded here.

**Notes:** The VizieR catalogue 2016yCat..18160098Z was not read because the host is blocked. The arXiv table has 106 numbered rows (1–106).

**Cluster Name — Cluster Redshift** (106):

- XMMXCSJ003545.5-431758.6 — 0.650 ± 0.002
- XMMXCSJ003548.1-432232.8 — 0.630 ± 0.002
- XMMXCSJ021442.21-043315.3 — 0.142 ± 0.001
- XMMXCSJ021547.28-045031.4 — 0.955 ± 0.108
- XMMXCSJ021611.69-041422.8 — 0.154 ± 0.001
- XMMXCSJ021735.7-051315.8 — 0.646 ± 0.002
- XMMXCSJ021807.88-054557.3 — 0.689 ± 0.002
- XMMXCSJ021826.0-045942.7 — 0.873 ± 0.002
- XMMXCSJ021833.0-050101.5 — 0.874 ± 0.002
- XMMXCSJ021837.90-054037.0 — 0.317 ± 0.001
- XMMXCSJ021843.7-053253.3 — 0.381 ± 0.001
- XMMXCSJ021914.5-045053.2 — 0.222 ± 0.001
- XMMXCSJ021940.78-055043.7 — 0.729 ± 0.002
- XMMXCSJ021944.3-045326.8 — 0.332 ± 0.001
- XMMXCSJ022154.83-054519.0 — 0.258 ± 0.001
- XMMXCSJ022204.5-043246.3 — 0.315 ± 0.001
- XMMXCSJ022233.02-045803.5 — 0.839 ± 0.002
- XMMXCSJ022302.5-043619.6 — 1.260 ± 0.085
- XMMXCSJ022318.3-051209.8 — 0.332 ± 0.001
- XMMXCSJ022318.37-052707.6 — 0.211 ± 0.001
- XMMXCSJ022347.50-025134.4 — 0.185 ± 0.007
- XMMXCSJ022350.88-053643.9 — 0.500 ± 0.002
- XMMXCSJ022356.32-030556.8 — 0.300 ± 0.010
- XMMXCSJ022357.6-043519.7 — 0.572 ± 0.002
- XMMXCSJ022401.1-050542.2 — 0.327 ± 0.001
- XMMXCSJ022433.9-041442.7 — 0.262 ± 0.001
- XMMXCSJ022512.2-062307.9 — 0.204 ± 0.001
- XMMXCSJ022512.31-053112.3 — 0.294 ± 0.001
- XMMXCSJ022524.7-044043.9 — 0.267 ± 0.001
- XMMXCSJ022529.8-041432.7 — 0.143 ± 0.001
- XMMXCSJ022532.42-035502.4 — 0.771 ± 0.002
- XMMXCSJ022549.02-055339.3 — 0.232 ± 0.001
- XMMXCSJ022559.68-024932.4 — 0.305 ± 0.017
- XMMXCSJ022632.5-054651.9 — 0.445 ± 0.026
- XMMXCSJ022634.75-040408.0 — 0.346 ± 0.001
- XMMXCSJ022722.82-032147.3 — 0.360 ± 0.016
- XMMXCSJ022726.4-043206.8 — 0.309 ± 0.001
- XMMXCSJ022740.4-045129.9 — 0.295 ± 0.001
- XMMXCSJ022802.85-045101.1 — 0.297 ± 0.001
- XMMXCSJ022808.41-053553.2 — 0.192 ± 0.001
- XMMXCSJ022827.3-042542.5 — 0.433 ± 0.001
- XMMXCSJ022829.83-031257.2 — 0.370 ± 0.000
- XMMXCSJ023052.5-045128.7 — 0.590 ± 0.002
- XMMXCSJ033151.23-274936.2 — 0.676 ± 0.002
- XMMXCSJ034004.0-283150.6 — 0.262 ± 0.001
- XMMXCSJ034025.95-284025.4 — 0.067 ± 0.001
- XMMXCSJ034026.03-282835.8 — 0.375 ± 0.007
- XMMXCSJ041646.0-552510.4 — 0.410 ± 0.008
- XMMXCSJ042017.8-503155.0 — 0.470 ± 0.015
- XMMXCSJ042226.36-514029.7 — 0.575 ± 0.039
- XMMXCSJ043218.04-610356.5 — 0.435 ± 0.021
- XMMXCSJ043318.93-614013.7 — 0.545 ± 0.007
- XMMXCSJ043706.81-541413.0 — 0.505 ± 0.006
- XMMXCSJ043708.09-542908.8 — 0.565 ± 0.041
- XMMXCSJ043818.09-541917.5 — 0.475 ± 0.005
- XMMXCSJ043940.82-542412.9 — 0.700 ± 0.015
- XMMXCSJ045421.2-531531.1 — 0.325 ± 0.028
- XMMXCSJ045506.1-532343.2 — 0.435 ± 0.019
- XMMXCSJ051141.31-515420.8 — 0.724 ± 0.028
- XMMXCSJ051636.81-543113.3 — 0.295 ± 0.001
- XMMXCSJ065829.1-555641.5 — 0.297 ± 0.001
- XMMXCSJ065860.0-560926.8 — 0.335 ± 0.015
- XMMXCSJ095737.12+023426.0 — 0.373 ± 0.001
- XMMXCSJ095823.49+024920.2 — 0.343 ± 0.001
- XMMXCSJ095846.90+021550.8 — 0.771 ± 0.002
- XMMXCSJ095924.73+014615.7 — 0.124 ± 0.001
- XMMXCSJ095931.63+022657.2 — 0.356 ± 0.001
- XMMXCSJ095944.68+023619.8 — 0.343 ± 0.001
- XMMXCSJ095947.18+025529.1 — 0.126 ± 0.001
- XMMXCSJ095951.46+014051.8 — 0.373 ± 0.001
- XMMXCSJ100021.72+022329.3 — 0.221 ± 0.001
- XMMXCSJ100027.26+022135.9 — 0.221 ± 0.001
- XMMXCSJ100043.28+014608.0 — 0.346 ± 0.001
- XMMXCSJ100047.16+015917.0 — 0.438 ± 0.001
- XMMXCSJ100109.18+013336.0 — 0.435 ± 0.002
- XMMXCSJ100141.74+022538.0 — 0.120 ± 0.001
- XMMXCSJ100142.56+014059.4 — 0.218 ± 0.001
- XMMXCSJ100201.42+021334.2 — 0.838 ± 0.002
- XMMXCSJ232737.63-541610.0 — 1.005 ± 0.096
- XMMXCSJ232810.21-555015.8 — 0.890 ± 0.035
- XMMXCSJ232900.4-533931.7 — 0.255 ± 0.004
- XMMXCSJ233000.57-543706.4 — 0.176 ± 0.001
- XMMXCSJ233003.40-541415.6 — 0.415 ± 0.011
- XMMXCSJ233037.38-554340.2 — 0.330 ± 0.017
- XMMXCSJ233135.2-562754.1 — 0.185 ± 0.005
- XMMXCSJ233204.99-551242.8 — 0.305 ± 0.014
- XMMXCSJ233215.97-544205.3 — 0.360 ± 0.022
- XMMXCSJ233331.89-554753.4 — 1.195 ± 0.065
- XMMXCSJ233346.00-553826.9 — 0.780 ± 0.000
- XMMXCSJ233406.45-554710.8 — 0.775 ± 0.000
- XMMXCSJ233421.4-541054.6 — 0.365 ± 0.017
- XMMXCSJ233429.10-543618.3 — 0.450 ± 0.009
- XMMXCSJ233528.43-543501.1 — 0.870 ± 0.118
- XMMXCSJ233637.1-524408.2 — 0.560 ± 0.011
- XMMXCSJ233706.8-541911.5 — 0.505 ± 0.008
- XMMXCSJ233745.46-562758.5 — 0.380 ± 0.018
- XMMXCSJ233836.3-543740.3 — 0.375 ± 0.006
- XMMXCSJ234119.2-560400.2 — 0.475 ± 0.014
- XMMXCSJ234142.5-555747.7 — 0.200 ± 0.005
- XMMXCSJ234145.4-564000.7 — 0.495 ± 0.009
- XMMXCSJ234201.2-553253.8 — 0.555 ± 0.005
- XMMXCSJ234231.5-562106.8 — 0.415 ± 0.027
- XMMXCSJ234448.2-561728.2 — 0.650 ± 0.006
- XMMXCSJ234730.8-553320.5 — 0.395 ± 0.025
- XMMXCSJ235009.5-551957.9 — 0.420 ± 0.015
- XMMXCSJ235059.5-552206.1 — 0.140 ± 0.006

**Count below z = 0.30:** 30 of 106. XMMXCSJ022356.32-030556.8, printed as 0.300 ± 0.010, is not counted.


## S10b — Chiu et al. 2018, MNRAS 478, 3072 (2018MNRAS.478.3072C)

**URLs read:**
- https://arxiv.org/abs/1711.00917 (DOI 10.1093/mnras/sty1284)
- https://arxiv.org/e-print/1711.00917 (SHA-256 4b663fd65a77d76ebe68ffc317181b0e3633c7f1507060ba7c45bfcb3f3e9f23)

**Table/file read:** Table `tab:sample` (file `xvp.master.tex`); columns Name and redshift. Its name column is identical, row for row, to `tab:measurements` (file `xvp.measurement.tex`), which carries the per-cluster stellar masses (not recorded here).

**Name — z** (91):

- SPT-CL J0000-5748 — 0.702
- SPT-CL J0013-4906 — 0.406
- SPT-CL J0014-4952 — 0.752
- SPT-CL J0033-6326 — 0.597
- SPT-CL J0037-5047 — 1.026
- SPT-CL J0040-4407 — 0.350
- SPT-CL J0058-6145 — 0.826
- SPT-CL J0102-4603 — 0.722
- SPT-CL J0102-4915 — 0.870
- SPT-CL J0123-4821 — 0.620
- SPT-CL J0142-5032 — 0.730
- SPT-CL J0151-5954 — 1.035
- SPT-CL J0156-5541 — 1.221
- SPT-CL J0200-4852 — 0.498
- SPT-CL J0212-4657 — 0.655
- SPT-CL J0217-5245 — 0.343
- SPT-CL J0232-5257 — 0.556
- SPT-CL J0234-5831 — 0.415
- SPT-CL J0236-4938 — 0.334
- SPT-CL J0243-5930 — 0.635
- SPT-CL J0252-4824 — 0.421
- SPT-CL J0256-5617 — 0.580
- SPT-CL J0304-4401 — 0.458
- SPT-CL J0304-4921 — 0.392
- SPT-CL J0307-5042 — 0.550
- SPT-CL J0307-6225 — 0.579
- SPT-CL J0310-4647 — 0.709
- SPT-CL J0324-6236 — 0.730
- SPT-CL J0330-5228 — 0.442
- SPT-CL J0334-4659 — 0.485
- SPT-CL J0346-5439 — 0.530
- SPT-CL J0348-4515 — 0.358
- SPT-CL J0352-5647 — 0.670
- SPT-CL J0406-4805 — 0.737
- SPT-CL J0411-4819 — 0.424
- SPT-CL J0417-4748 — 0.581
- SPT-CL J0426-5455 — 0.630
- SPT-CL J0438-5419 — 0.421
- SPT-CL J0441-4855 — 0.790
- SPT-CL J0446-5849 — 1.186
- SPT-CL J0449-4901 — 0.792
- SPT-CL J0456-5116 — 0.562
- SPT-CL J0509-5342 — 0.461
- SPT-CL J0528-5300 — 0.768
- SPT-CL J0533-5005 — 0.881
- SPT-CL J0542-4100 — 0.642
- SPT-CL J0546-5345 — 1.066
- SPT-CL J0551-5709 — 0.423
- SPT-CL J0555-6406 — 0.345
- SPT-CL J0559-5249 — 0.609
- SPT-CL J0616-5227 — 0.684
- SPT-CL J0655-5234 — 0.470
- SPT-CL J2031-4037 — 0.342
- SPT-CL J2034-5936 — 0.919
- SPT-CL J2035-5251 — 0.528
- SPT-CL J2043-5035 — 0.723
- SPT-CL J2106-5844 — 1.132
- SPT-CL J2135-5726 — 0.427
- SPT-CL J2145-5644 — 0.480
- SPT-CL J2146-4633 — 0.933
- SPT-CL J2148-6116 — 0.571
- SPT-CL J2218-4519 — 0.650
- SPT-CL J2222-4834 — 0.652
- SPT-CL J2232-5959 — 0.594
- SPT-CL J2233-5339 — 0.480
- SPT-CL J2236-4555 — 1.162
- SPT-CL J2245-6206 — 0.580
- SPT-CL J2248-4431 — 0.351
- SPT-CL J2258-4044 — 0.826
- SPT-CL J2259-6057 — 0.750
- SPT-CL J2301-4023 — 0.730
- SPT-CL J2306-6505 — 0.530
- SPT-CL J2325-4111 — 0.358
- SPT-CL J2331-5051 — 0.576
- SPT-CL J2335-4544 — 0.547
- SPT-CL J2337-5942 — 0.775
- SPT-CL J2341-5119 — 1.003
- SPT-CL J2342-5411 — 1.075
- SPT-CL J2344-4243 — 0.596
- SPT-CL J2345-6405 — 0.937
- SPT-CL J2352-4657 — 0.734
- SPT-CL J2355-5055 — 0.320
- SPT-CL J2359-5009 — 0.775
- SPT-CL J0106-5943 — 0.348
- SPT-CL J2332-5053 — 0.560
- SPT-CL J0232-4421 — 0.284
- SPT-CL J0235-5121 — 0.278
- SPT-CL J0516-5430 — 0.295
- SPT-CL J0522-4818 — 0.296
- SPT-CL J0658-5556 — 0.296
- SPT-CL J2011-5725 — 0.279

**Count below z = 0.30:** 6 of 91.


## S15a — Bellstedt et al. 2016, MNRAS 460, 2862 (VizieR 2017yCat..74602862B)

**URLs read:**
- https://arxiv.org/abs/1605.02736 (DOI 10.1093/mnras/stw1184)
- https://arxiv.org/e-print/1605.02736 (SHA-256 ca98013a000c7c32bf3910ba0a2a3a794efc575c909b0a9648a83824bcb65ae1)

**Table/file read:** Appendix table `BCGClusterResults`, "BCG results" (continued over several parts; file `Bellstedt2016_resubmit.tex`); columns Cluster, z_spec and z_phot. Only rows with a printed "BCG Mass" are listed.

**Notes:** The VizieR catalogue 2017yCat..74602862B was not read because the host is blocked. Table 2 (observational summary) in the arXiv source prints only 5 rows and points to a GitHub repository for the full table, which was not read. The results table has 135 rows with a BCG mass, for 123 distinct cluster names; 12 clusters have two BCG rows (MACS-J0014.3-3022, MACS-J0025.4-1222, ACT-CL-J0232-5257, Abell370, ACT-CL-J0256+0006, MACS-J0257.1-2325, SMACS-J0304.3-4401, MS-0440+0204, MACS-J0553.4-3342, SMACS-J0600.2-2008, Abell1758, MACS-J1347.5-1144), with identical redshifts. Each such cluster is listed once. 8 further rows print no redshift and no BCG mass and are excluded: MACS-J0034.9+0234, MACS-J0110.1+3211, SMACS-J0439-4600, MACS-J0449-2848, SMACS-J0600-4353, MACSJ-0845.4+0327, MACS-J1652.3+5534, RX-J2149.3+0951. With these, 131 names are printed, against the 132 clusters stated in the abstract; the difference was not resolved. Each z is labelled z_spec or z_phot according to the column it is printed in.

**Cluster — z (as printed)** (123):

- SPT-CL-J0000-5748 — z_spec 0.702
- MACS-J0011.7-1523 — z_spec 0.379
- MACS-J0014.3-3022 — z_spec 0.308
- ACT-CL-J0014.9-0057 — z_spec 0.533
- C1G-J001640.6-130644 — z_phot 0.700
- ACT-CL-J0017.6-0051 — z_spec 0.211
- ACT-CL-J0018.2-0022 — z_phot 0.75
- MACS-J0025.4-1222 — z_spec 0.5843
- MACS-J0032.1+1808 — z_phot 0.398
- MACS-J0033.8-0751 — z_phot 0.3
- MACS-J0034.4+0225 — z_phot 0.35
- MACS-J0035.4-2015 — z_spec 0.352
- Abell68 — z_spec 0.255
- SMACS-J0040.8-4407 — z_phot 0.4
- C1G-J005805.6+003058 — z_spec 0.662
- ACT-CL-J0104.8+0002 — z_spec 0.277
- ACT-CL-J0119.9+0055 — z_phot 0.72
- ACT-CL-J0127.2+0020 — z_spec 0.379
- C1G-J013710.4-103423 — z_phot 0.575
- RX-J0142.0-2131 — z_phot 0.28
- ACT-CL-J0145-5301 — z_spec 0.118
- MACS-J0150.3-1005 — z_spec 0.365
- ACT-CL-J0152.7+0100 — z_spec 0.23
- ACT-CL-J0156.4-0123 — z_phot 0.45
- ACT-CL-J0206.2-0114 — z_spec 0.676
- ACT-CL-J0215-5212 — z_spec 0.48
- ACT-CL-J0223.1-0056 — z_spec 0.663
- ACT-CL-J0218.2-0041 — z_spec 0.672
- ACT-CL-J0219.8+0022 — z_spec 0.537
- ACT-CL-J0219.9+0129 — z_phot 0.35
- ACT-CL-J0221.5-0012 — z_spec 0.589
- ACT-CL-J0232-5257 — z_spec 0.556
- ACT-CL-J0235-5121 — z_spec 0.278
- ACT-CL-J0237-4939 — z_spec 0.334
- Abell370 — z_spec 0.375
- MACS-J0242.5-2132 — z_spec 0.314
- ACT-CL-J0245.8-0042 — z_spec 0.179
- ACT-CL-J0250.1+0008 — z_phot 0.78
- ACT-CL-J0256+0006 — z_spec 0.363
- MACS-J0257.1-2325 — z_spec 0.505
- ACT-CL-J0301.6+0155 — z_spec 0.167
- ACT-CL-J0304-4921 — z_spec 0.392
- SMACS-J0304.3-4401 — z_phot 0.52
- ACT-CL-J0326.8-0043 — z_spec 0.448
- ACT-CL-J0330-5227 — z_spec 0.44
- ACT-CL-J0346-5438 — z_spec 0.53
- ACT-CL-J0348+0029 — z_spec 0.297
- ACT-CL-J0348-0028 — z_spec 0.345
- MACS-J0358.8-2955 — z_spec 0.425
- MACS-J0416.1-2403 — z_spec 0.40
- MACS-J0417.5-1154 — z_spec 0.443
- Abell496 — z_spec 0.0328
- ACT-CL-J0438-5419 — z_spec 0.421
- MS-0440+0204 — z_spec 0.197
- MACS-J0451.6-0305 — z_spec 0.5386
- MACS-J0454.1-0300 — z_spec 0.5377
- Abell520 — z_spec 0.205
- ACT-CL-J0516-5430 — z_spec 0.294
- SPT-CL-J0553-5005 — z_spec 0.881
- SPT-CL-J0546-5345 — z_spec 1.066
- MACS-J0553.4-3342 — z_spec 0.407
- SMACS-J0600.2-2008 — z_phot 0.46
- ACT-CL-J0616-5227 — z_spec 0.684
- ACT-CL-J0641-4949 — z_spec 0.146
- ACT-CL-J0645-5413 — z_spec 0.167
- ACT-CL-J0707-5522 — z_spec 0.296
- SMACS-J0723.3-7327 — z_phot 0.39
- C1G-J080434.9+330509 — z_spec 0.552
- Abell644 — z_spec 0.0704
- MACS-J0850.1+3604 — z_spec 0.378
- Abell750 — z_spec 0.18
- MACS-J0911.2+1746 — z_spec 0.5049
- C1G-J094811.6+290709 — z_spec 0.778
- MACS-J0949.8+1708 — z_spec 0.384
- Abell901 — z_spec 0.170
- Abell963 — z_spec 0.206
- MACS-J1105.7-1014 — z_spec 0.466
- MACS-J1108.8+0906 — z_spec 0.466
- Abell1204 — z_spec 0.171
- MACS-J1115.8+0129 — z_spec 0.355
- MACS-J1206.2-0847 — z_spec 0.439
- Abell1553 — z_spec 0.165
- Abell1634 — z_spec 0.196
- MACS-J1311.0-0311 — z_spec 0.494
- Abell1689 — z_spec 0.183
- Abell1758 — z_spec 0.279
- MACS-J1347.5-1144 — z_spec 0.451
- Abell1835 — z_spec 0.253
- MACS-J1427+44 — z_spec 0.487
- Abell1942 — z_spec 0.224
- Abell1994 — z_spec 0.22
- RX-J1720.1+2638 — z_spec 0.164
- MACS-J1752.0+4440 — z_spec 0.366
- MACS-J1931.8-2634 — z_spec 0.352
- ACT-CL-J2025.2+0030 — z_phot 0.34
- ACT-CL-J2050.5-0055 — z_spec 0.622
- ACT-CL-J2051.1+0056 — z_spec 0.333
- ACT-CL-J2055.4+0105 — z_spec 0.408
- ACT-CL-J2128.4+0135 — z_spec 0.385
- ACT-CL-J2129.6+0005 — z_spec 0.234
- ACT-CL-J2130.1+0045 — z_phot 0.71
- MACS-J2140.1-2339 — z_spec 0.313
- C1G-J214826.3-053312 — z_phot 0.625
- ACT-CL-J2152.9-0114 — z_phot 0.69
- Abell2390 — z_spec 0.233
- Abell3827 — z_spec 0.0993
- MACS-J2211.7-0349 — z_spec 0.396
- MACS-J2214.9-1359 — z_spec 0.5027
- ACT-CL-J2220.7-0042 — z_phot 0.57
- ACT-CL-J2229.2-0004 — z_phot 0.61
- C1G-J223007.6-080949 — z_spec 0.623
- C1G-J223727.5+135523 — z_phot 0.700
- MACS-J2241.8+1732 — z_spec 0.3137
- CL2244 — z_spec 0.328
- MACS-J2248.7-4431 — z_spec 0.3475
- ACT-CL-J2253.3-0031 — z_phot 0.54
- AC114 — z_spec 0.313
- ACT-CL-J2302.5+0002 — z_spec 0.52
- Abell2552 — z_spec 0.302
- C1G-J231215.6+035307 — z_spec 0.648
- C1G-J231520.6+090711 — z_phot 0.725
- Abell2631 — z_spec 0.273
- ACT-CL-J2351.7+0009 — z_phot 0.99

**Count below z = 0.30:** 34 of 123.


## S15c — Erfanianfar et al. 2019, A&A 631, A175 (2019A&A...631A.175E)

**URLs read:**
- https://arxiv.org/abs/1908.01559 (DOI 10.1051/0004-6361/201935375)
- https://arxiv.org/e-print/1908.01559 (SHA-256 03cd9493b9824f28f3d2fb9042d9c501ddbb1f2b26de19332e705c613fe8b121)

**Table/file read:** the paper's only catalogue table, `tb:cor:cha` ("CODEX-SPIDERS DR14 BCGs value-added catalog"), which is a **column description**, not data. It lists CLUS_ID ("The SPIDERS/CODEX identification number"), CLUZSPEC (cluster redshift), and Mass_MEDIAN, among others.

**List not read.** The per-cluster list (416 BCGs, according to the abstract) is published as an SDSS DR14 value-added catalogue (the paper points to http://www.sdss.org/dr14/data_access/vac/). `sdss.org`, `data.sdss.org`, VizieR and the GAVO mirror were all refused by this session's network proxy, so no names or redshifts were read. The paper also uses clusters in COSMOS, AEGIS, CDFS, XMM-CFHTLS and XMM-XXL, but it prints no per-cluster table for them. With 416 entries the list exceeds 150, so only the z < 0.30 names would be recorded. To do that, someone needs to read the SPIDERS BCG VAC FITS file (or a VizieR copy, if one exists) from a host that allows it.

**Count below z = 0.30:** not determined.


## Not verified

- No VizieR ReadMe or table was read for any record; all lists come from the arXiv LaTeX source. Where the arXiv version and the journal version differ, these lists may differ from the published tables. Each journal reference was confirmed only through the arXiv page's jref or DOI.
- C22 and C26 do not print their own cluster lists. The lists recorded for them come from the papers they cite, and in C26's case the list is a superset of the clusters actually used.
