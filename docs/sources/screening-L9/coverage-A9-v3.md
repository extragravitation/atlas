# Coverage of A9 clusters by measured stars (stellar mass or printed luminosity), version 3

- **Date:** 2026-10-31. Prepared by Claude (AI assistance, disclosed). Exploratory screening record; not a data package. Matching scripts and the extracted name lists are in `coverage-v3-tools/`.
- **Names and redshifts only.** This file records cluster names, redshifts as printed, record identifiers, decision codes, aperture geometry (projected or 3D) and observed-side channel (L or O). It records no luminosity, mass, fraction, ratio or other result value. Positions were used only inside the matching script and are not reproduced here.
- **Builds on** `screening-S9/coverage-A9-v2.md` (319 clusters below z = 0.30 in non-stacked E/E-pair A9 records). The cluster list, name-matching rules (U1–U6), stacked-only list and stellar-mass classes are taken from v2 unchanged. New: D-071 counts a source's printed cluster luminosity (BCG plus members) as measured stars; the luminosity records screened in `screening-L9/` are added here.
- **Rulings.** QL1 and QL2 were ruled as recommended by D-072 (2026-10-31 20:49 MDT), after this table was started; the **recommended QL2 column is the ruled one**. The strict column is kept to show what the rejected alternative would have cost.
- **Not readable:** the full cluster lists of **LV3** (614 maxBCG clusters; VizieR J/MNRAS/449/2345 only) and of **L5a** beyond the 35 rows printed in the paper (114 in total; CDS J/A+A/423/449 only). CDS, VizieR mirrors (CfA, NAO) and the GAVO mirror all refused the connection from this workspace (connection reset or proxy 403). The arXiv source bundles of both papers were checked and carry no cluster table. LV3 is therefore **not cross-matched**; L5a is cross-matched for its 35 printed rows only.

## Inputs

Repository files (read, not changed):

| File | SHA-256 |
|---|---|
| `docs/sources/screening-S9/coverage-A9-v2.md` | `507ed285defe439a23e2db1fe05ce0e2e7a880f6cdbd23e0154f28e54cac7925` |
| `docs/sources/screening-L9/final.csv` | `ec148ed1f000312361de08903b8aebf8e12b7434d174283b331b297ae695e08c` |
| `docs/sources/screening-L9/adjudication.md` | `e41cdd802f43b18057c1a88661d7c61ba2db25720ee192126c850dfd32f3884f` |
| `docs/sources/screening-L9/reader-a-S.md` | `1aeab018515091fa725226a49b75e1a6e319fb323fac52a97a860b1f45c9ba3f` |
| `docs/sources/screening-L9/reader-a-L1.md` | `b3cd6eed5e633a8f296cd20468103dbc16436162a08c757b38853f3cb6def97a` |
| `docs/sources/screening-L9/reader-a-L2.md` | `a5d680ebd2e4d9e5fbb03a942cca390dc31072e3b675dd7d6b9de3e206b0f707` |
| `docs/sources/screening-L9/reader-b-S.md` | `ae17db2b89c1f1fae50f3d0834c2dad9c7d00270b85bcb797e0830fff404c19a` |
| `docs/sources/screening-L9/reader-b-L1.md` | `a9dfd80af31f05e0b1ef9d6f0103033f74795f0453527997bb305a0cfcd1cfa1` |
| `docs/sources/screening-L9/reader-b-L2.md` | `59e6ce8205dcbe795f628e172a13c4fabbd74d70223fd497a6ee540f5b989858` |
| `docs/sources/screening-A9/final.csv` | `24b81ce9413da659a556b51bbe9c7f23a647be19584f0bc37a0598eb89c498d3` |
| `docs/sources/screening-S9/reader-a.md` | `490c999f6341845c61f0e6c01edefac0d8d31e4901c786c72c8a85097f137afd` |
| `docs/sources/screening-S9/reader-b.md` | `80c258992d2178674ebc341e1dd1b50246c02d4ce560a27cf1f706b85c302877` |

Sources read at arXiv on 2026-10-31 (`curl -sSL https://arxiv.org/pdf/<id>`, then `pdftotext -layout`; only the name, z and position columns were extracted):

| Record | Source | Table read | SHA-256 of the downloaded file |
|---|---|---|---|
| L1 | arXiv:astro-ph/0402308 (PDF) | Table 2, columns Name and z (93 rows) | `671a1f1f031377553330c184b5f135df570a7fbe14c8719e486e3e62b1526830` |
| L2 | arXiv:astro-ph/9907266 (PDF) | Table 2, columns Name and Center (B1950); **no z column** | `6aae392dc07359047b77bfcf0cf82844a1227c9aed75c5d3359f0bd1a5daa9cf` |
| L5a | arXiv:astro-ph/0403354 (PDF) | Table 1, columns Name, Alternative Name, R.A., dec, z (35 printed rows: "the first 35 cluster" of 114) | `9a1ed5f1cfecf626b6cde13c63eea7a093350d5f9c96088a4d32c7b7a5d39dc4` |
| L5a | arXiv:astro-ph/0403354 (e-print source) | checked for a full cluster table: none | `d6b663fefc475a5ce9e3f5ee84ea4a2668c59ba91abd7d89c909ae7465383b5e` |
| L5c | arXiv:astro-ph/0606191 (PDF) | Appendix A, columns Name and z_c (137 rows) | `f9a3caa0c6c663971f93c569df1f0d0b07b724022b841eadb61e6d01585d33a8` |
| LV3 | arXiv:1503.00975 (e-print source) | checked for a cluster table: none (one table of percentile offsets only) | `860b5010705c398030aa93cf50e82ce9cafe926286ed83e7d0785a41e775b79b` |

All other luminosity-record cluster lists (60 or fewer clusters) are taken from the "Clusters covered" column of the L9 readings, as the readings print them.

## Method

1. **Cluster list.** The 319 clusters of v2, with v2's name forms, redshifts, A9 records and stellar-mass entries copied unchanged. Stacked-only clusters (v2, D-067 item 2) are not classified here either.
2. **Luminosity records.** Every row of `screening-L9/final.csv` coded **E** (L1, L5a, L5c, L9, S2b, S3a, S3b, S16b) or **P** (L2, L4, L8, L10, L23b, LV3, S4b, S4d, S6, S10a). How each counts:

   | Records | Final code | Recommended QL2 | Strict QL2 | Basis |
   |---|---|---|---|---|
   | L1, L5a, L5c, L9, S2b, S3b, S16b | E | full | full | final.csv |
   | S3a | E (QL1) | full | full | final.csv; QL1 recommended |
   | L10, L23b | P (QL1) | full | full | QL1 recommended (sum of the source's own printed components) |
   | L2, L8, LV3, S6 | P (QL2) | **full** (BCG by method) | does not count | QL2 (i) |
   | L4, S4b, S4d | P (QL2) | does not count | does not count | QL2 (ii): analytic Schechter total, members only |
   | S10a | P (QL4) | does not count | does not count | observed-frame magnitudes |

   Records that do not count are still listed in the per-cluster table, marked "does not count". The S4b and S4d rows here are their **luminosity** routes; their stellar-mass routes (S9) are unchanged from v2.
3. **Geometry of the stars** (projected or 3D), from `final.csv` and the L9 readings: **3D** for L1 and S2b (the source's own NFW deprojection, QL5) and L4; **projected** for L2, L5a, L5c, L8, L9, L10, L23b, LV3, S3a, S3b, S6, S16b (L5c: "no deprojection stated", reader B; "apparently projected", reader A); not stated for S4b, S4d, S10a. For the S9 stellar-mass records that give class (a) in v2, from the S9 readings: S10b **3D** ("deprojection correction", reader B); S12b **3D** (M⋆,500 "with a projection correction", reader B); S4b and S8d **not stated**.
4. **Name matching.** v2's normalisation (case, spacing, zero-padding, Abell/ACO = A, A S n = AS n, ZwCl = Zw, MKW0n = MKWn, XLSSC zero-padded) and v2's name forms are used as they stand. Added for these lists: L2's "S n" = AS n; an alternative name printed in the same source row is applied without a flag (L5a prints Abell numbers beside 12 RXC names). "MKW4s" is kept distinct from MKW4 (L1 and L4 print both).
5. **Coordinate matching (v2 rule U5).** Applied to every luminosity-record entry that did not match by name and has a coordinate designation or printed position (L5a positions, J2000; L2 centres, B1950, precessed with astropy 8.0.2 FK4 → FK5; RXC, RXJ, ACT-CL designations). Each was compared with every v2 name form that is a coordinate designation (J2000 names direct; Zw and MS from B1950; PSZ2 from Galactic l, b). Accepted when the separation is within the coarser designation's cell (diagonal of its last-digit precision in RA and Dec) **and** the printed redshifts differ by ≤ 0.02. maxBCG-named clusters would have been matched only this way; none could be read (LV3).
6. **Redshift cut.** The A9 redshifts decide (v2). Luminosity entries at z ≥ 0.30 cannot match a v2 row; they are listed in "Gaps" only by count.
7. **Classes per cluster** (as v2, with luminosity added): (a) full stars by an E record (stellar mass per v2, or a counting luminosity record); (b) full stars only by P records (in practice only S9 stellar-mass P records remain, since every luminosity P row is either counted as full or not counted under each variant); (c) partial only; (d) none. Computed for **recommended QL2** and **strict QL2**, each combined with v2's **main** rule for the S9 stellar-mass records. The effect of v2's strict variant ("full (BCG per reader A only)" treated as "not stated") is given as a count.
8. **Observed-side channel and pairing (class (a) only).** For each cluster, the channels of its non-stacked A9 records are taken from v2's per-record table (from the A9 readings): L (lensing) or O (member-galaxy dynamics); C21b counts as O (its observed side is C21a); gas-side records (C3a, C9h/C9i, C15a) carry no channel. A cluster's stars are **pairable with L** if any of its counting star sources is projected and it has an L record, and **pairable with O** if any is 3D and it has an O record. Sources with geometry "not stated" pair with neither.
9. **Script.** Matching and classification ran in Python 3 with `-I` (astropy 8.0.2) from the session scratch folder; scripts and extracted name lists are not committed. Downloads were kept in a separate folder from the scripts.

## Summary

| Class | Recommended QL2 (v2 main) | Strict QL2 (v2 main) | v2 (stellar mass only, main) |
|---|---|---|---|
| (a) full stars by an E record | **116** | **89** | 14 |
| (b) full stars only by P records | **3** | **9** | 31 |
| (c) partial only | **4** | **10** | 14 |
| (d) none | **196** | **211** | 260 |
| Total | 319 | 319 | 319 |

**Under v2's strict variant** (S9 "BCG per reader A only" not counted): recommended QL2 → (a) 116, (b) 2, (c) 4, (d) 197 (**1** cluster changes: NGC4325, b → d). Strict QL2 → (a) 89, (b) 2, (c) 13, (d) 215 (**7** change: A115, A383, A586, A781, A2261, A2631, NGC4325). Class (a) does not change under v2's strict variant in either QL2 reading: every v2 (a) cluster that depends on "BCG per reader A only" (S4b) is also named by a counting luminosity record (L1 or S2b).

**Moved into class (a)** (from v2 main class):

- **Recommended QL2: 102** (28 from b, 10 from c, 64 from d).
  - from (b): A115, A119, A168, A267, A383, A586, A697, A773, A781, A1204, A1413, A1682, A1689, A1763, A1914, A2034, A2069, A2111, A2259, A2261, A2399, A2593, A2631, MS 0906.5+1110, MS 1455.0+2232, RXCJ 1504.1-0248, RXJ1720.1+2638, RXJ2129.6+0005.
  - from (c): A68, A496, A611, A750, A963, A1423, A1835, A2390, A2552, MS 0440.5+0204.
  - from (d): A141, A194, A291, A295, A478, A521, A539, A576, A646, A655, A667, A757, A779, A907, A990, A1066, A1132, A1142, A1205, A1302, A1314, A1366, A1424, A1437, A1451, A1663, A1750, A1767, A1773, A1809, A1918, A2009, A2050, A2149, A2197, A2204, A2219, A2244, A2428, A2485, A2537, A2670, MS 0451.5+0250, MS 0839.8+2938, MS 1006.0+1202, NGC6338, RXCJ1053p5450, RXCJ2102.1-2431, XLSSC 027, 054, 055, 060, 061, 087, 088, 091, 098, 103, 104, 112, ZwCl0857.9+2107, ZwCl1231.4+1007, ZwCl 0949.6+5207, ZwCl 1021.0+0426.
- **Strict QL2: 75** (22 from b, 4 from c, 49 from d): the recommended list less A115, A383, A586, A781, A2261, A2631 (b); A68, A750, A963, A1423, A1835, A2552 (c); A141, A291, A295, A521, A907, A1451, A2009, A2197, A2204, A2219, A2485, A2537, RXCJ2102.1-2431, ZwCl0857.9+2107, ZwCl1231.4+1007 (d). Those 27 rest on S6, L8 or L2 alone.

**Remaining outside (a)** (recommended QL2, v2 main): (b) A160, A957, NGC4325 (S1a or S4a only); (c) A520, A901, A1553, A1758 (S15a BCG only); (d) 196, of which 54 XLSSC, 51 PSZ2 and 11 1eRASS.

**Geometry of the stars and pairing, class (a)** (v2 main rule for the S9 records):

| | Recommended QL2 (116) | Strict QL2 (89) |
|---|---|---|
| Stars projected only | 89 | 61 |
| Stars 3D only | 12 | 20 |
| Stars both projected and 3D | 15 | 7 |
| Stars of "not stated" geometry only | 0 | 1 (A209, S8d) |
| Pairable with lensing (projected stars, L record) only | 55 | 29 |
| Pairable with member dynamics (3D stars, O record) only | 23 | 24 |
| Pairable with both | 1 (Coma) | 0 |
| Geometry does not match the observed side (e.g. projected stars, O records only) | 34 | 32 |
| Not determined (only gas-side A9 records, or geometry not stated) | 3 (MS 0440.5+0204, MS 0839.8+2938, MS 1006.0+1202) | 4 (the same three, and A209) |

Reading of the result, stated once: the jump in class (a) is mostly a name-overlap effect of five large or targeted samples: L5c (27 A9 clusters, 18 of them with no other counting record), S6 (40; 18 sole), L1 (23), L10 (17) and L5a (13 of 35 printed rows). S6, L8 and L2 depend on QL2 and account for the whole difference between the two readings. Thirty-four of the 116 have stars whose geometry does not match any observed-side channel they have: most are C20a/C20d (row O, member dynamics) clusters whose stars come only from projected apertures (L5c, L5a, L10, S6). The XLSSC entries (L9) are XXL systems that the C18c readers note are often groups (A8 question).

## Per-luminosity-record summary

"Named" = distinct v2 clusters the record names (any variant); "sole new (a)" = clusters moved into (a) for which this is the only counting luminosity record.

| Record | Code | Geometry | Clusters in source list | Below z = 0.30 | Named (A9 list) | Sole new (a), rec. QL2 | Sole new (a), strict QL2 |
|---|---|---|---|---|---|---|---|
| L1 | E | 3D | 93 | 93 | 23 | 4 | 8 |
| L2 | P; E rec., X strict | projected | 105 (+ component row A1656b) | all (z ≤ 0.15, §2; no z printed) | 13 | 2 | — |
| L4 | P; does not count | 3D | 8 | 8 | 2 | — | — |
| L5a | E | projected | 114 (35 printed) | 30 of the 35 printed | 13 | 3 | 7 |
| L5c | E | projected | 137 | 137 | 27 | 18 | 18 |
| L8 | P; E rec., X strict | projected | 17 | 17 | 15 | 2 | — |
| L9 | E | projected | 20 | 13 | 12 | 12 | 12 |
| L10 | P; E by QL1 | projected | 20 | 20 | 17 | 5 | 13 |
| L23b | P; E by QL1 | projected | 1 | 1 | 0 | — | — |
| LV3 | P; E rec., X strict | projected | 614 | 614 | **not cross-matched** | — | — |
| S2b | E | 3D | 27 | 27 | 8 | 0 | 0 |
| S3a | E (QL1) | projected | 23 | 23 | 0 | — | — |
| S3b | E | projected | 12 | 12 | 0 | — | — |
| S4b (luminosity route) | P; does not count | not stated | 19 | 19 | 10 | — | — |
| S4d (luminosity route) | P; does not count | not stated | 5 | 5 | 5 | — | — |
| S6 | P; E rec., X strict | projected | 41 (A2697 without K data) | 41 | 41 (40 with luminosity) | 18 | — |
| S10a | P; does not count | not stated | 14 | 1 | 0 | — | — |
| S16b | E | projected | 15 | 7 | 6 | 3 | 5 |

## Per-cluster table

Sorted by class (recommended QL2), then class (strict QL2), then v2 class. Columns 5–8 are copied from v2. "Observed side" = channels of the cluster's non-stacked A9 records (method 8). Luminosity entries give the record, its code under the rulings, its geometry, and the name and z as the source (or reading) prints them. Flags: v2 flags carried over; new flags described under "Uncertain name matches".

| Class (rec. QL2) | Class (strict QL2) | v2 class (main / strict) | Cluster | z (A9 sources, from v2) | A9 records (code) | Observed side | Stellar-mass records (from v2) | Luminosity records naming it (code; geometry; as printed) | Flags |
|---|---|---|---|---|---|---|---|---|---|
| a | a | a / a | A85 | 0.055 (C20d) | C20d (E-pair) · stacked: C26/C26a | O | S1a (P; full; as "A85"); S4b (E; full (BCG per reader A only); as "A85"); S12a (P; named, no stellar mass for it); S12b (E; full; as "A85") | L1 (E; 3D; as "a0085", z 0.0551); L2 (P; E recommended, X strict; projected; as "A85", z not printed); L5a (E; projected; as "RXCJ0041.8-0918", z 0.0520); S2b (E; 3D; as "A85", z 0.0556); S4b (P; X under both, does not count; not stated; as "A85", z 0.0556) | kind: C28b reader B notes other literature calls A85 merging (titles only); the source is not reported as doing so |
| a | a | a / a | A209 | 0.206 (C1a, C1b, C3a, C12d, C18d); 0.21 (C1c); 0.2060 (C6c/C6d); readings: ~0.2 (reader A); 0.2 (reader B) (C13c) | C1a (E); C1b (E); C1c (E); C3a (E-pair); C6c/C6d (E-pair); C12d (E-pair); C13c (E-pair); C18d (E-pair) | L | S8a (E; BCG only; as "A209"); S8d (E; full; as "Abell 209") | L8 (P; E recommended, X strict; projected; as "ABELL0209", z 0.2060); S6 (P; E recommended, X strict; projected; as "Abell0209", z 0.2060) | — |
| a | a | a / d | A1367 | 0.0217 [= cz/c, cz 6495 km/s] (C21a, C21b) | C21a (E-pair); C21b (E-pair) | O | S4b (E; full (BCG per reader A only); as "A1367") | L1 (E; 3D; as "a1367", z 0.0216); S2b (E; 3D; as "A1367", z 0.0216); S4b (P; X under both, does not count; not stated; as "A1367", z 0.0216) | class d if BCG inclusion must be stated by both readers |
| a | a | a / d | A1650 | 0.084 (C20d) | C20d (E-pair) | O | S4b (E; full (BCG per reader A only); as "A1650") | L1 (E; 3D; as "a1650", z 0.0845); L5c (E; projected; as "a1650", z 0.0839); S2b (E; 3D; as "A1650", z 0.0845); S4b (P; X under both, does not count; not stated; as "A1650", z 0.0845) | class d if BCG inclusion must be stated by both readers |
| a | a | a / a | A2142 | 0.089 (C20d); readings: "z 0.091–0.228 ... all 4 below 0.3" (C11a, reader A); 0.09 (reader A); 0.090 (reader B) (C28a) | C11a (E); C20d (E-pair); C28a (E) | L, O | S4b (E; full (BCG per reader A only); as "A2142"); S12a (P; members only (BCG by dynamical M/L, not eligible); as "A2142"); S12b (E; full; as "A2142") | L1 (E; 3D; as "a2142", z 0.0899); S4b (P; X under both, does not count; not stated; as "A2142", z 0.0899) | kind: substructure noted (C11a, C28a reader B); merging not stated |
| a | a | a / d | A2199 | 0.031 (C20d); 0.0304 [= cz/c, cz 9101 km/s] (C21a, C21b) | C20d (E-pair); C21a (E-pair); C21b (E-pair); C21c (E-pair) | O | S4b (E; full (BCG per reader A only); as "A2199") | L1 (E; 3D; as "a2199", z 0.0303); L4 (P; X under both, does not count; 3D; as "A2199", z 0.0302); S4b (P; X under both, does not count; not stated; as "A2199", z 0.0302) | kind: supercluster A2199+A2197+group (C21c); class d if BCG inclusion must be stated by both readers |
| a | a | a / d | A2255 | 0.080 (C20d) | C20d (E-pair) | O | S4b (E; full (BCG per reader A only); as "A2255"); S12a (P; named, no stellar mass for it); S12b (E; named, no stellar mass for it) | L1 (E; 3D; as "a2255", z 0.0806); L5c (E; projected; as "a2255", z 0.0801); S2b (E; 3D; as "A2255", z 0.0800); S4b (P; X under both, does not count; not stated; as "A2255", z 0.0800) | kind: an S9 reading (S19 dataset title) calls it "post-merger"; no A9 reading does; A10 check; class d if BCG inclusion must be stated by both readers |
| a | a | a / d | Coma (A1656) | 0.0233 [= cz/c, cz 6973 km/s] (C21a, C21b); readings: ~0.024 (reader A); 0.024 (reader B) (C13a); ≈ 0.023 (C23c reader A, citing C23d text) | C13a (E-pair); C21a (E-pair); C21b (E-pair); C23a (E-pair); C23b (E-pair); C23c (E) | L, O | S4b (E; full (BCG per reader A only); as "Coma") | L1 (E; 3D; as "a1656", z 0.0232); L2 (P; E recommended, X strict; projected; as "A1656", z not printed); L2 (P; E recommended, X strict; projected; as "A1656b", z not printed); S4b (P; X under both, does not count; not stated; as "Coma", z 0.0232) | kind: infalling groups noted (C13a reader B); merging not stated; class d if BCG inclusion must be stated by both readers; L2 prints a component row "A1656b", counted with this cluster (as U6) |
| a | a | a / d | MKW04 | 0.020 (C20d) | C20d (E-pair) | O | S4b (E; full (BCG per reader A only); as "MKW4") | L1 (E; 3D; as "mkw04", z 0.0200); L2 (P; E recommended, X strict; projected; as "MKW4", z not printed); S4b (P; X under both, does not count; not stated; as "MKW4", z 0.0200) | class d if BCG inclusion must be stated by both readers |
| a | a | a / d | MKW08 | 0.027 (C20d) | C20d (E-pair) | O | S4b (E; full (BCG per reader A only); as "MKW8") | L1 (E; 3D; as "mkw08", z 0.0270); S4b (P; X under both, does not count; not stated; as "MKW8", z 0.0270) | class d if BCG inclusion must be stated by both readers |
| a | a | a / a | PSZ2 G266.04-21.25 | 0.2965 (C29b) | C29b (E) | O | S9a (E; BCG only; as "XMMXCSJ065829.1-555641.5"); S10b (E; full; as "SPT-CL J0658-5556") | — | U5; possibly the same system as "Bullet" (C18d, z 0.297); not testable from files; not merged |
| a | a | a / a | RXCJ0232.2−4420 | 0.284 (C18d) | C18d (E-pair) | L | S10b (E; full; as "SPT-CL J0232-4421") | — | U5 |
| a | a | a / a | RXCJ0516.6−5430 | 0.295 (C18d) | C18d (E-pair) | L | S9a (E; BCG only; as "XMMXCSJ051636.81-543113.3"); S10b (E; full; as "SPT-CL J0516-5430"); S15a (E; BCG only; as "ACT-CL-J0516-5430") | — | U5 |
| a | a | a / a | Zw1215p0400 | 0.077 (C20d); 0.0773 (C29a) | C20d (E-pair); C29a (E) | O | S4b (E; full (BCG per reader A only); as "ZwCl1215"); S12a (P; named, no stellar mass for it); S12b (E; full; as "ZW1215") | S4b (P; X under both, does not count; not stated; as "ZwCl1215", z 0.0750) | U4; U5 |
| a | a | b / b | A119 | 0.044 (C20d); 0.0443 [= cz/c, cz 13268 km/s] (C21a, C21b) | C20d (E-pair); C21a (E-pair); C21b (E-pair) · stacked: C26/C26a | O | S1a (P; full; as "A119") | L1 (E; 3D; as "a0119", z 0.0440); L2 (P; E recommended, X strict; projected; as "A119", z not printed); S2b (E; 3D; as "A119", z 0.0440) | — |
| a | a | b / b | A168 | 0.045 (C20d); 0.0447 [= cz/c, cz 13395 km/s] (C21a, C21b) | C20d (E-pair); C21a (E-pair); C21b (E-pair) · stacked: C26/C26a | O | S1a (P; full; as "A168") | L1 (E; 3D; as "a0168", z 0.0450); L5a (E; projected; as "RXCJ0114.9+0022", z 0.0470); L5c (E; projected; as "a0168", z 0.0450) | — |
| a | a | b / d | A267 | 0.2300 (C6c/C6d); 0.230 (C12d); 0.2291 (C20a); 0.229 (C20d) | C6c/C6d (E-pair); C12d (E-pair); C20a (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A267") | L10 (P; E by QL1; projected; as "A267", z 0.230); L5a (E; projected; as "RXCJ0152.7+0100", z 0.2270); L8 (P; E recommended, X strict; projected; as "ABELL0267", z 0.2300); S6 (P; E recommended, X strict; projected; as "Abell0267", z 0.2300) | class d if BCG inclusion must be stated by both readers |
| a | a | b / d | A697 | 0.2820 (C6c/C6d); 0.2812 (C20a, C20c); 0.282 (C20d) | C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A697") | L5a (E; projected; as "RXCJ0842.9+3621", z 0.2820); L8 (P; E recommended, X strict; projected; as "ABELL0697", z 0.2820); S6 (P; E recommended, X strict; projected; as "Abell0697", z 0.2820) | class d if BCG inclusion must be stated by both readers |
| a | a | b / d | A773 | 0.2170 (C6a, C6c/C6d); 0.2173 (C20a, C20c); 0.218 (C20d) | C6a (E-pair); C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A773") | L10 (P; E by QL1; projected; as "A773", z 0.217); L5a (E; projected; as "RXCJ0917.8+5143", z 0.2170); S6 (P; E recommended, X strict; projected; as "Abell0773", z 0.2170) | class d if BCG inclusion must be stated by both readers |
| a | a | b / c | A1204 | 0.1706 (C20a, C20c); 0.170 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | S4a (P; full (BCG per reader A only); as "A1204"); S15a (E; BCG only; as "Abell1204") | L10 (P; E by QL1; projected; as "A1204", z 0.171) | class c if BCG inclusion must be stated by both readers |
| a | a | b / d | A1413 | 0.1427 (C6a); 0.1412 (C20a, C20c); 0.141 (C20d) | C6a (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A1413") | L10 (P; E by QL1; projected; as "A1413", z 0.143) | class d if BCG inclusion must be stated by both readers |
| a | a | b / d | A1682 | 0.2260 (C6c/C6d); 0.2272 (C20a, C20c); 0.227 (C20d) | C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A1682") | L10 (P; E by QL1; projected; as "A1682", z 0.234); S6 (P; E recommended, X strict; projected; as "Abell1682", z 0.2260) | class d if BCG inclusion must be stated by both readers |
| a | a | b / c | A1689 | 0.1832 (C6a, C6c/C6d); 0.184 (C12d, C20d); 0.183 (C18d); 0.1842 (C20a, C20c); readings: 0.183 (C9b reader A; C9a reader B); "z 0.091–0.228 ... all 4 below 0.3" (C11a, reader A); "all below 0.3" (C11b, reader A) | C6a (E-pair); C6c/C6d (E-pair); C9a (E); C9b (E); C9c (E); C9d/C9e (E); C9e/C9f (E); C9f/C9g (E); C9g/C9h (E); C9h/C9i (E-pair); C11a (E); C11b (E); C12c (E-pair); C12d (E-pair); C18d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A1689"); S4d (P; not stated; as "A1689"); S13e (P; BCG + core galaxies, core only; as "Abell 1689"); S15a (E; BCG only; as "Abell1689") | L10 (P; E by QL1; projected; as "A1689", z 0.183); S4d (P; X under both, does not count; not stated; as "A1689", z 0.1823); S6 (P; E recommended, X strict; projected; as "Abell1689", z 0.1832) | class c if BCG inclusion must be stated by both readers |
| a | a | b / d | A1763 | 0.2279 (C6c/C6d); 0.228 (C12d); 0.2312 (C20a, C20c); 0.231 (C20d) | C6c/C6d (E-pair); C12d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A1763") | L10 (P; E by QL1; projected; as "A1763", z 0.223); S6 (P; E recommended, X strict; projected; as "Abell1763", z 0.2279) | class d if BCG inclusion must be stated by both readers |
| a | a | b / d | A1914 | 0.1712 (C6c/C6d); 0.1660 (C20a, C20c); 0.166 (C20d) | C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A1914") | L10 (P; E by QL1; projected; as "A1914", z 0.171); S6 (P; E recommended, X strict; projected; as "Abell1914", z 0.1712) | class d if BCG inclusion must be stated by both readers |
| a | a | b / d | A2034 | 0.1132 (C20a, C20c); 0.113 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | S4a (P; full (BCG per reader A only); as "A2034") | L10 (P; E by QL1; projected; as "A2034", z 0.113) | class d if BCG inclusion must be stated by both readers |
| a | a | b / d | A2069 | 0.1139 (C20a, C20c); 0.114 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | S4a (P; full (BCG per reader A only); as "A2069") | L10 (P; E by QL1; projected; as "A2069", z 0.116) | class d if BCG inclusion must be stated by both readers |
| a | a | b / d | A2111 | 0.2290 (C6c/C6d); 0.2291 (C20a, C20c); 0.230 (C20d) | C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A2111") | L10 (P; E by QL1; projected; as "A2111", z 0.229); S6 (P; E recommended, X strict; projected; as "Abell2111", z 0.2290) | class d if BCG inclusion must be stated by both readers |
| a | a | b / d | A2259 | 0.1605 (C20a, C20c); 0.160 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | S4a (P; full (BCG per reader A only); as "A2259") | L10 (P; E by QL1; projected; as "A2259", z 0.164); L5c (E; projected; as "a2259", z 0.1600) | class d if BCG inclusion must be stated by both readers |
| a | a | b / b | A2399 | 0.058 (C20d) | C20d (E-pair) · stacked: C26/C26a | O | S1a (P; full; as "A2399") | L5c (E; projected; as "a2399", z 0.0579) | — |
| a | a | b / b | A2593 | 0.042 (C20d) | C20d (E-pair) · stacked: C26/C26a | O | S1a (P; full; as "A2593") | L1 (E; 3D; as "a2593", z 0.0433); L2 (P; E recommended, X strict; projected; as "A2593", z not printed); L5c (E; projected; as "a2593", z 0.0419); S2b (E; 3D; as "A2593", z 0.0433) | — |
| a | a | b / d | MS 0906.5+1110 | 0.1709 (C15a); 0.1767 (C20a, C20c); 0.177 (C20d); 0.1663 (C29b); 0.1643 (C29b); 0.1776 (C29b) | C15a (E-pair); C20a (E); C20c (E); C20d (E-pair); C29b (E) · stacked: C22/C22a | O | S4a (P; full (BCG per reader A only); as "MS0906.5+1110") | L10 (P; E by QL1; projected; as "MS0906.5+1110", z 0.180) | U3; U5; kind: C22 calls MS 0906+11 a "strong binary"; PSZ2 G218.81+35.51 is printed with sub-component rows (bimodal) in C29b; class d if BCG inclusion must be stated by both readers |
| a | a | b / d | MS 1455.0+2232 | 0.2578 (C6c/C6d); 0.2570 (C15a) | C6c/C6d (E-pair); C15a (E-pair) · stacked: C22/C22a | L | S4a (P; full (BCG per reader A only); as "MS1455.0+2232") | L8 (P; E recommended, X strict; projected; as "ZwCl1454.8+2233", z 0.2578); S16b (E; projected; as "MS1455+22", z 0.2570); S6 (P; E recommended, X strict; projected; as "ZwCl1454.8+2233", z 0.2578) | U3; U5; class d if BCG inclusion must be stated by both readers |
| a | a | b / d | RXCJ 1504.1-0248 | 0.2153 (C6c/C6d); 0.215 (C18d); 0.2168 (C20a, C20c); 0.216 (C20d) | C6c/C6d (E-pair); C18d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "RXJ1504-0248") | L10 (P; E by QL1; projected; as "RXJ1504-0248", z 0.215); S6 (P; E recommended, X strict; projected; as "RXCJ1504.1-0248", z 0.2153) | U2; class d if BCG inclusion must be stated by both readers |
| a | a | b / c | RXJ1720.1+2638 | 0.1640 (C6a, C6c/C6d); 0.1604 (C20a, C20c); 0.160 (C20d); 0.1606 (C29b) | C6a (E-pair); C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair); C29b (E) | L, O | S4a (P; full (BCG per reader A only); as "RXJ1720.1+2638"); S15a (E; BCG only; as "RX-J1720.1+2638") | L10 (P; E by QL1; projected; as "RXJ1720.1+2638", z 0.164); L8 (P; E recommended, X strict; projected; as "RXJ1720.1+2638", z 0.1640); S6 (P; E recommended, X strict; projected; as "RXJ1720.1+2638", z 0.1640) | U5; S4a reading prints z 0.39 for this name (A9 sources 0.160–0.164): z discrepancy in the S9 reading, unverified; class c if BCG inclusion must be stated by both readers |
| a | a | b / c | RXJ2129.6+0005 | 0.234 (C1a, C1b, C1c, C3a, C20d); 0.2350 (C6a, C6c/C6d); 0.2339 (C20a, C20c); readings: "1 below 0.3 (RX J2129.7+0005)" (C4a, reader A); no value printed | C1a (E); C1b (E); C1c (E); C3a (E-pair); C4a (E); C6a (E-pair); C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "RXJ2129.6+0005"); S8a (E; BCG only; as "RXJ2129+0005"); S15a (E; BCG only; as "ACT-CL-J2129.6+0005") | L10 (P; E by QL1; projected; as "RXJ2129.6+0005", z 0.235); L8 (P; E recommended, X strict; projected; as "RXJ2129.6+0005", z 0.2350); S6 (P; E recommended, X strict; projected; as "RXJ2129.6+0005", z 0.2350) | U1; class c if BCG inclusion must be stated by both readers |
| a | a | c / c | A496 | 0.0330 [= cz/c, cz 9900 km/s] (C21a, C21b) | C21a (E-pair); C21b (E-pair) | O | S4d (P; not stated; as "A496"); S15a (E; BCG only; as "Abell496") | L1 (E; 3D; as "a0496", z 0.0328); L2 (P; E recommended, X strict; projected; as "A496", z not printed); S2b (E; 3D; as "A496", z 0.0328); S4d (P; X under both, does not count; not stated; as "A496", z 0.033) | — |
| a | a | c / c | A611 | 0.288 (C1a, C1b, C3a); 0.29 (C1c); 0.2850 (C6a); 0.2880 (C6c/C6d) | C1a (E); C1b (E); C1c (E); C3a (E-pair); C6a (E-pair); C6c/C6d (E-pair) | L | S8a (E; BCG only; as "A611") | L5a (E; projected; as "RXCJ0800.9+3602", z 0.2880); L8 (P; E recommended, X strict; projected; as "ABELL0611", z 0.2880); S6 (P; E recommended, X strict; projected; as "Abell0611", z 0.2880) | — |
| a | a | c / c | A2390 | 0.2329 (C6a, C6c/C6d); 0.233 (C12d); 0.2279 (C15a); 0.228 (C18d); readings: "z 0.091–0.228 ... all 4 below 0.3" (C11a, reader A); 0.228 (C14a, both readers); 0.228 (C14b, both readers) | C6a (E-pair); C6c/C6d (E-pair); C11a (E); C12d (E-pair); C14a (E-pair); C14b (E-pair); C15a (E-pair); C18d (E-pair) · stacked: C22/C22a | L | S15a (E; BCG only; as "Abell2390") | L8 (P; E recommended, X strict; projected; as "ABELL2390", z 0.2329); S16b (E; projected; as "A2390", z 0.2279); S6 (P; E recommended, X strict; projected; as "Abell2390", z 0.2329) | — |
| a | a | c / c | MS 0440.5+0204 | 0.1965 (C15a) | C15a (E-pair) · stacked: C22/C22a | not determined (gas-side record only) | S15a (E; BCG only; as "MS-0440+0204") | S16b (E; projected; as "MS0440+02", z 0.1965) | U3 |
| a | a | d / d | A194 | 0.0178 [= cz/c, cz 5341 km/s] (C21a, C21b) | C21a (E-pair); C21b (E-pair) | O | — | L1 (E; 3D; as "a0194", z 0.0180); L2 (P; E recommended, X strict; projected; as "A194", z not printed) | — |
| a | a | d / d | A478 | 0.0881 (C11b, reader A); 0.0881 per C13g (C13f, reader A); 0.0881 (C13g, both readers) | C11b (E); C13f (E); C13g (E) | L | — | L1 (E; 3D; as "a0478", z 0.0881); L4 (P; X under both, does not count; 3D; as "A478", z 0.09) | — |
| a | a | d / d | A539 | 0.0291 [= cz/c, cz 8717 km/s] (C21a, C21b) | C21a (E-pair); C21b (E-pair) | O | — | L1 (E; 3D; as "a0539", z 0.0288); L2 (P; E recommended, X strict; projected; as "A539", z not printed) | — |
| a | a | d / d | A576 | 0.0384 [= cz/c, cz 11510 km/s] (C21a, C21b) | C21a (E-pair); C21b (E-pair) | O | — | L1 (E; 3D; as "a0576", z 0.0389); L2 (P; E recommended, X strict; projected; as "A576", z not printed) | — |
| a | a | d / d | A646 | 0.1273 (C20a); 0.127 (C20d) | C20a (E); C20d (E-pair) | O | — | L5a (E; projected; as "RXCJ0822.1+4705", z 0.1300); L5c (E; projected; as "a0646", z 0.1266) | — |
| a | a | d / d | A655 | 0.1271 (C20a, C20c); 0.127 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | L5a (E; projected; as "RXCJ0825.4+4707", z 0.1260); L5c (E; projected; as "a0655", z 0.1276) | — |
| a | a | d / d | A667 | 0.1452 (C20a); 0.145 (C20d) | C20a (E); C20d (E-pair) | O | — | L5c (E; projected; as "a0667", z 0.1441) | — |
| a | a | d / d | A757 | 0.051 (C20d) | C20d (E-pair) | O | — | L5a (E; projected; as "RXCJ0913.7+4742", z 0.0510) | — |
| a | a | d / d | A779 | 0.023 (C20d) | C20d (E-pair) | O | — | L1 (E; 3D; as "a0779", z 0.0230) | — |
| a | a | d / d | A990 | 0.1416 (C20a, C20c); 0.141 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | L5a (E; projected; as "RXCJ1023.6+4908", z 0.1440) | — |
| a | a | d / d | A1066 | 0.069 (C20d) | C20d (E-pair) | O | — | L5c (E; projected; as "a1066", z 0.0690) | — |
| a | a | d / d | A1132 | 0.1351 (C20a, C20c); 0.135 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | L5c (E; projected; as "a1132", z 0.1358) | — |
| a | a | d / d | A1142 | 0.036 (C20d) | C20d (E-pair) | O | — | L1 (E; 3D; as "a1142", z 0.0349) | — |
| a | a | d / d | A1205 | 0.076 (C20d) | C20d (E-pair) | O | — | L5c (E; projected; as "a1205", z 0.0761) | — |
| a | a | d / d | A1302 | 0.1152 (C20a, C20c); 0.116 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | L5c (E; projected; as "a1302", z 0.1153) | — |
| a | a | d / d | A1314 | 0.033 (C20d) | C20d (E-pair) | O | — | L1 (E; 3D; as "a1314", z 0.0335); L2 (P; E recommended, X strict; projected; as "A1314", z not printed) | — |
| a | a | d / d | A1366 | 0.1160 (C20a); 0.116 (C20d) | C20a (E); C20d (E-pair) | O | — | L5c (E; projected; as "a1366", z 0.1164) | — |
| a | a | d / d | A1424 | 0.075 (C20d) | C20d (E-pair) | O | — | L5c (E; projected; as "a1424", z 0.0754) | — |
| a | a | d / d | A1437 | 0.1333 (C20a, C20c); 0.133 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | L5c (E; projected; as "a1437", z 0.1341) | — |
| a | a | d / d | A1663 | 0.084 (C20d) | C20d (E-pair) | O | — | L5c (E; projected; as "a1663", z 0.0830) | — |
| a | a | d / d | A1750 | 0.085 (C20d) | C20d (E-pair) · stacked: C24a | O | — | L5c (E; projected; as "a1750", z 0.0858) | — |
| a | a | d / d | A1767 | 0.071 (C20d) | C20d (E-pair) | O | — | L1 (E; 3D; as "a1767", z 0.0701); L5c (E; projected; as "a1767", z 0.0705); S2b (E; 3D; as "A1767", z 0.0701) | — |
| a | a | d / d | A1773 | 0.078 (C20d) | C20d (E-pair) | O | — | L5c (E; projected; as "a1773", z 0.0773) | — |
| a | a | d / d | A1809 | 0.079 (C20d) | C20d (E-pair) | O | — | L5c (E; projected; as "a1809", z 0.0795) | — |
| a | a | d / d | A1918 | 0.1388 (C20a, C20c); 0.140 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | L5c (E; projected; as "a1918", z 0.1402) | — |
| a | a | d / d | A2050 | 0.1191 (C20a, C20c); 0.119 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | S4d (P; not stated; as "A2050") | L5c (E; projected; as "a2050", z 0.1193); S4d (P; X under both, does not count; not stated; as "A2050", z 0.1183) | — |
| a | a | d / d | A2149 | 0.065 (C20d) | C20d (E-pair) · stacked: C26/C26a | O | — | L5c (E; projected; as "a2149", z 0.0650) | — |
| a | a | d / d | A2244 | 0.099 (C20d) | C20d (E-pair) | O | — | L5c (E; projected; as "a2244", z 0.0993) | — |
| a | a | d / d | A2428 | 0.084 (C20d) | C20d (E-pair) | O | — | L5c (E; projected; as "a2428", z 0.0839) | — |
| a | a | d / d | A2670 | 0.076 (C20d) | C20d (E-pair) | O | — | L1 (E; 3D; as "a2670", z 0.0762); L2 (P; E recommended, X strict; projected; as "A2670", z not printed); L5c (E; projected; as "a2670", z 0.0761) | — |
| a | a | d / d | MS 0451.5+0250 | 0.2010 (C15a); 0.2007 (C29b) | C15a (E-pair); C29b (E) · stacked: C22/C22a | O | — | S16b (E; projected; as "MS0451+02", z 0.2010) | U3; U5 |
| a | a | d / d | MS 0839.8+2938 | 0.1928 (C15a) | C15a (E-pair) · stacked: C22/C22a | not determined (gas-side record only) | — | S16b (E; projected; as "MS0839+29", z 0.1928) | U3 |
| a | a | d / d | MS 1006.0+1202 | 0.2605 (C15a) | C15a (E-pair) · stacked: C22/C22a | not determined (gas-side record only) | — | L10 (P; E by QL1; projected; as "MS1006.0+1202", z 0.221); S16b (E; projected; as "MS1006+12", z 0.2605) | U3; L10 reading prints z 0.221 for "MS1006.0+1202" (A9 source C15a 0.2605; S16b 0.2605): z discrepancy in the L10 readings, unverified; exact designation match accepted |
| a | a | d / d | NGC6338 | 0.029 (C20d) | C20d (E-pair) | O | — | L1 (E; 3D; as "ngc6338", z 0.0282) | — |
| a | a | d / d | RXCJ1053p5450 | 0.073 (C20d) | C20d (E-pair) | O | — | L5a (E; projected; as "RXCJ1053.7+5452", z 0.0750) | U5 (L5a RXCJ1053.7+5452: 6.8′ from RXCJ1053p5450 (tolerance 8.7′, Δz 0.002)) |
| a | a | d / d | XLSSC 027 | 0.295 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 027", z 0.295) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 054 | 0.054 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 054", z 0.054) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 055 | 0.232 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 055", z 0.232) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 060 | 0.139 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 060", z 0.139) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 061 | 0.259 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 061", z 0.259) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 087 | 0.141 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 087", z 0.141) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 088 | 0.295 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 088", z 0.295) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 091 | 0.186 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 091", z 0.186) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 098 | 0.297 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 098", z 0.297) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 103 | 0.233 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 103", z 0.233) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 104 | 0.294 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 104", z 0.294) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | XLSSC 112 | 0.139 (C18c) | C18c (E-pair) | L | — | L9 (E; projected; as "XLSSC 112", z 0.139) | kind: C18c readers note many XXL systems are groups (A8 question) |
| a | a | d / d | ZwCl 0949.6+5207 | 0.2140 (C6a, C6c/C6d); 0.2160 (C20a, C20c); 0.215 (C20d) | C6a (E-pair); C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | — | L5a (E; projected; as "RXCJ0952.8+5153", z 0.2140); S6 (P; E recommended, X strict; projected; as "ZwCl0949.6+5207", z 0.2140) | U5 (L5a RXCJ0952.8+5153: 1.2′ from ZwCl 0949.6+5207 (tolerance 1.4′, Δz 0.000)) |
| a | a | d / d | ZwCl 1021.0+0426 | 0.2906 (C6c/C6d); 0.280 (C18d); 0.2894 (C20a, C20c); 0.290 (C20d) | C6c/C6d (E-pair); C18d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | — | L5a (E; projected; as "RXCJ1023.6+0411", z 0.2850); S6 (P; E recommended, X strict; projected; as "ZwCl1021.0+0426", z 0.2906) | U5 |
| a | b | b / d | A115 | 0.1971 (C6c/C6d) | C6c/C6d (E-pair) | L | S4a (P; full (BCG per reader A only); as "A115") | S6 (P; E recommended, X strict; projected; as "Abell0115", z 0.1971) | class d if BCG inclusion must be stated by both readers |
| a | b | b / c | A383 | 0.187 (C1a, C1b, C3a, C12d, C18d); 0.189 (C1c); 0.1883 (C6a, C6c/C6d); readings: 0.187 (C13h, reader B) | C1a (E); C1b (E); C1c (E); C3a (E-pair); C6a (E-pair); C6c/C6d (E-pair); C12d (E-pair); C13h (E); C18d (E-pair) | L | S4a (P; full (BCG per reader A only); as "A383"); S8a (E; BCG only; as "A383") | L8 (P; E recommended, X strict; projected; as "ABELL0383", z 0.1883) | class c if BCG inclusion must be stated by both readers |
| a | b | b / d | A586 | 0.1710 (C6c/C6d) | C6c/C6d (E-pair) | L | S4a (P; full (BCG per reader A only); as "A586") | L8 (P; E recommended, X strict; projected; as "ABELL0586", z 0.1710); S6 (P; E recommended, X strict; projected; as "Abell0586", z 0.1710) | class d if BCG inclusion must be stated by both readers |
| a | b | b / d | A781 | 0.2984 (C6c/C6d) | C6c/C6d (E-pair) | L | S4a (P; full (BCG per reader A only); as "A781") | S6 (P; E recommended, X strict; projected; as "Abell0781", z 0.2984) | S4a reading prints z 0.30 (A9 source 0.2984); class d if BCG inclusion must be stated by both readers |
| a | b | b / c | A2261 | 0.224 (C1a, C1b, C3a); 0.225 (C1c, C20d); 0.2240 (C6c/C6d); 0.2242 (C20a, C20c); readings: 0.225 (C5a, both readers); "z 0.091–0.228 ... all 4 below 0.3" (C11a, reader A) | C1a (E); C1b (E); C1c (E); C3a (E-pair); C5a (E); C6c/C6d (E-pair); C11a (E); C20a (E); C20c (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A2261"); S8a (E; BCG only; as "A2261") | S6 (P; E recommended, X strict; projected; as "Abell2261", z 0.2240) | class c if BCG inclusion must be stated by both readers |
| a | b | b / c | A2631 | 0.2779 (C6c/C6d); 0.2765 (C20a); 0.277 (C20d) | C6c/C6d (E-pair); C20a (E); C20d (E-pair) | L, O | S4a (P; full (BCG per reader A only); as "A2631"); S4d (P; not stated; as "A2631"); S15a (E; BCG only; as "Abell2631") | S4d (P; X under both, does not count; not stated; as "A2631", z 0.273); S6 (P; E recommended, X strict; projected; as "Abell2631", z 0.2779) | class c if BCG inclusion must be stated by both readers |
| a | c | c / c | A68 | 0.2546 (C6a, C6c/C6d); 0.255 (C12d) | C6a (E-pair); C6c/C6d (E-pair); C12d (E-pair) | L | S15a (E; BCG only; as "Abell68") | L8 (P; E recommended, X strict; projected; as "ABELL0068", z 0.2546); S6 (P; E recommended, X strict; projected; as "Abell0068", z 0.2546) | — |
| a | c | c / c | A750 | 0.1630 (C6c/C6d); 0.1640 (C20a); 0.164 (C20d) | C6c/C6d (E-pair); C20a (E); C20d (E-pair) | L, O | S15a (E; BCG only; as "Abell750") | S6 (P; E recommended, X strict; projected; as "Abell0750", z 0.1630) | — |
| a | c | c / c | A963 | 0.2050 (C6a, C6c/C6d); 0.206 (C12d); 0.2041 (C20a, C20c); 0.204 (C20d) | C6a (E-pair); C6c/C6d (E-pair); C12d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S15a (E; BCG only; as "Abell963") | S6 (P; E recommended, X strict; projected; as "Abell0963", z 0.2050) | — |
| a | c | c / c | A1423 | 0.213 (C1c, C3a); 0.2130 (C6c/C6d); 0.2142 (C20a, C20c); 0.214 (C20d) | C1c (E); C3a (E-pair); C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S8a (E; BCG only; as "A1423") | S6 (P; E recommended, X strict; projected; as "Abell1423", z 0.2130) | — |
| a | c | c / c | A1835 | 0.2528 (C6a, C6c/C6d); 0.253 (C12d, C18d); 0.2506 (C20a, C20c); 0.252 (C20d); readings: "all below 0.3" (C11b, reader A); 0.252 (C12f, reader A) | C6a (E-pair); C6c/C6d (E-pair); C11b (E); C12d (E-pair); C12f (E-pair); C18d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | S15a (E; BCG only; as "Abell1835") | L8 (P; E recommended, X strict; projected; as "ABELL1835", z 0.2528); S6 (P; E recommended, X strict; projected; as "Abell1835", z 0.2528) | — |
| a | c | c / c | A2552 | 0.2998 (C6c/C6d) | C6c/C6d (E-pair) | L | S15a (E; BCG only; as "Abell2552") | S6 (P; E recommended, X strict; projected; as "Abell2552", z 0.2998) | S15a prints z_spec 0.302 (A9 source C6c/C6d 0.2998) |
| a | d | d / d | A141 | 0.2300 (C6c/C6d) | C6c/C6d (E-pair) | L | — | S6 (P; E recommended, X strict; projected; as "Abell0141", z 0.2300) | — |
| a | d | d / d | A291 | 0.1960 (C6c/C6d) | C6c/C6d (E-pair) | L | — | L8 (P; E recommended, X strict; projected; as "ABELL0291", z 0.1960); S6 (P; E recommended, X strict; projected; as "Abell0291", z 0.1960) | — |
| a | d | d / d | A295 | 0.042 (C20d) | C20d (E-pair) | O | — | L2 (P; E recommended, X strict; projected; as "A295", z not printed) | — |
| a | d | d / d | A521 | 0.2475 (C6a, C6c/C6d) | C6a (E-pair); C6c/C6d (E-pair) | L | — | S6 (P; E recommended, X strict; projected; as "Abell0521", z 0.2475) | — |
| a | d | d / d | A907 | 0.1669 (C6c/C6d); 0.153 (C18d) | C6c/C6d (E-pair); C18d (E-pair) | L | — | S6 (P; E recommended, X strict; projected; as "Abell0907", z 0.1669) | — |
| a | d | d / d | A1451 | 0.1992 (C6c/C6d) | C6c/C6d (E-pair) | L | — | S6 (P; E recommended, X strict; projected; as "Abell1451", z 0.1992) | — |
| a | d | d / d | A2009 | 0.1530 (C6c/C6d); 0.1522 (C20a, C20c); 0.152 (C20d) | C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | — | S6 (P; E recommended, X strict; projected; as "Abell2009", z 0.1530) | — |
| a | d | d / d | A2197 | 0.030 (C20d) | C20d (E-pair); C21c (E-pair) | O | — | L2 (P; E recommended, X strict; projected; as "A2197", z not printed) | kind: part of the A2199 supercluster (C21c); C21c names it only for X-ray of its components |
| a | d | d / d | A2204 | 0.1524 (C6a, C6c/C6d); 0.152 (C18d); readings: 0.152 (C12f, reader A) | C6a (E-pair); C6c/C6d (E-pair); C12f (E-pair); C18d (E-pair) | L | — | S6 (P; E recommended, X strict; projected; as "Abell2204", z 0.1524) | — |
| a | d | d / d | A2219 | 0.2281 (C6a, C6c/C6d); 0.228 (C12d); 0.2257 (C20a, C20c); 0.226 (C20d) | C6a (E-pair); C6c/C6d (E-pair); C12d (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | — | L8 (P; E recommended, X strict; projected; as "ABELL2219", z 0.2281); S6 (P; E recommended, X strict; projected; as "Abell2219", z 0.2281) | — |
| a | d | d / d | A2485 | 0.2472 (C6c/C6d) | C6c/C6d (E-pair) | L | — | L8 (P; E recommended, X strict; projected; as "ABELL2485", z 0.2472) | — |
| a | d | d / d | A2537 | 0.2966 (C6c/C6d); 0.297 (C18d) | C6c/C6d (E-pair); C18d (E-pair) | L | — | S6 (P; E recommended, X strict; projected; as "Abell2537", z 0.2966) | — |
| a | d | d / d | RXCJ2102.1-2431 | 0.1880 (C6c/C6d) | C6c/C6d (E-pair) | L | — | S6 (P; E recommended, X strict; projected; as "RXCJ2102.1-2431", z 0.1880) | — |
| a | d | d / d | ZwCl0857.9+2107 | 0.2347 (C6c/C6d) | C6c/C6d (E-pair) | L | — | S6 (P; E recommended, X strict; projected; as "ZwCl0857.9+2107", z 0.2347) | — |
| a | d | d / d | ZwCl1231.4+1007 | 0.2290 (C6c/C6d) | C6c/C6d (E-pair) | L | — | S6 (P; E recommended, X strict; projected; as "ZwCl1231.4+1007", z 0.2290) | candidate match to RXJ1234.2+0947 (S4a, P, z 0.23) at 5.2 arcmin after precession, beyond designation precision: not accepted (would be class b) |
| b | b | b / b | A160 | 0.043 (C20d) | C20d (E-pair) · stacked: C26/C26a | O | S1a (P; full; as "A160") | — | — |
| b | b | b / b | A957 | 0.046 (C20d) | C20d (E-pair) · stacked: C24a, C26/C26a | O | S1a (P; full; as "A957") | — | — |
| b | b | b / d | NGC4325 | 0.025 (C20d) | C20d (E-pair) | O | S4a (P; full (BCG per reader A only); as "NGC4325") | — | class d if BCG inclusion must be stated by both readers |
| c | c | c / c | A520 | 0.199 (C18d) | C18d (E-pair) | L | S15a (E; BCG only; as "Abell520") | — | kind: no reading assesses it; A10 check advised before packaging |
| c | c | c / c | A901 | 0.1634 (C6c/C6d) | C6c/C6d (E-pair) | L | S15a (E; BCG only; as "Abell901") | — | — |
| c | c | c / c | A1553 | 0.1668 (C20a, C20c); 0.167 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | S15a (E; BCG only; as "Abell1553") | — | — |
| c | c | c / c | A1758 | 0.2760 (C20a); 0.276 (C20d) | C20a (E); C20d (E-pair) | O | S15a (E; BCG only; as "Abell1758") | — | possibly the same system as A1758N (C6c/C6d); not merged |
| d | d | d / d | 1eRASS J004207.1-283154 | 0.1075 (C29a) | C29a (E) | O | — | — | — |
| d | d | d / d | 1eRASS J073220.0+313748 | 0.1705 (C29a); 0.1707 (C29b) | C29a (E); C29b (E) | O | — | — | U5 |
| d | d | d / d | 1eRASS J073721.1+351739 | 0.2094 (C29a) | C29a (E) | O | — | — | — |
| d | d | d / d | 1eRASS J080056.9+360324 | 0.2866 (C29a) | C29a (E) | O | — | — | — |
| d | d | d / d | 1eRASS J082317.9+155700 | 0.1529 (C29a) | C29a (E) | O | — | — | — |
| d | d | d / d | 1eRASS J084257.5+362208 | 0.2818 (C29a, C29b) | C29a (E); C29b (E) | O | — | — | U5 |
| d | d | d / d | 1eRASS J090131.5+030055 | 0.1936 (C29a) | C29a (E) | O | — | — | — |
| d | d | d / d | 1eRASS J101703.2+390250 | 0.2048 (C29a) | C29a (E) | O | — | — | — |
| d | d | d / d | 1eRASS J115518.0+232422 | 0.1422 (C29a); 0.1415 (C29b) | C29a (E); C29b (E) | O | — | — | U5 |
| d | d | d / d | 1eRASS J125922.4-041138 | 0.0843 (C29a) | C29a (E) | O | — | — | — |
| d | d | d / d | 1eRASS J130252.8-023059 | 0.0838 (C29a) | C29a (E) | O | — | — | — |
| d | d | d / d | A602 | 0.060 (C20d) | C20d (E-pair) · stacked: C26/C26a | O | — | — | — |
| d | d | d / d | A671 | 0.050 (C20d) | C20d (E-pair) · stacked: C26/C26a | O | — | — | — |
| d | d | d / d | A689 | 0.2789 (C20a); 0.279 (C20d) | C20a (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A795 | 0.1374 (C20a, C20c); 0.137 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A868 | 0.1535 (C6a) | C6a (E-pair) | L | — | — | — |
| d | d | d / d | A954 | 0.096 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A971 | 0.092 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A980 | 0.1555 (C20a, C20c); 0.156 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1033 | 0.1220 (C20a, C20c); 0.122 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1035A | 0.068 (C20d) | C20d (E-pair) | O | — | — | component row as printed (C20d) |
| d | d | d / d | A1035B | 0.078 (C20d) | C20d (E-pair) | O | — | — | component row as printed (C20d) |
| d | d | d / d | A1068 | 0.1386 (C20a, C20c); 0.138 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1173 | 0.076 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1190 | 0.076 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1201 | 0.1688 (C6a); 0.1671 (C20a, C20c); 0.167 (C20d) | C6a (E-pair); C20a (E); C20c (E); C20d (E-pair) | L, O | — | — | — |
| d | d | d / d | A1235 | 0.1030 (C20a, C20c); 0.103 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1246 | 0.1921 (C20a, C20c); 0.192 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1291A | 0.051 (C20d) | C20d (E-pair) | O | — | — | component row as printed (C20d) |
| d | d | d / d | A1291B | 0.059 (C20d) | C20d (E-pair) | O | — | — | component row as printed (C20d) |
| d | d | d / d | A1361 | 0.1159 (C20a); 0.116 (C20d) | C20a (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1377 | 0.052 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1436 | 0.064 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1552 | 0.086 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1703 | 0.2800 (C6a); 0.277 (C7a); readings: "1 below 0.3 (A1703)" (C11c, reader A) | C6a (E-pair); C7a (E-pair); C9e/C9f (E); C11c (E-pair) | L | — | — | — |
| d | d | d / d | A1728 | 0.089 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1758N | 0.2800 (C6c/C6d) | C6c/C6d (E-pair) | L | — | — | possibly the same system as A1758 (N component); not merged |
| d | d | d / d | A1885 | 0.089 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1902 | 0.1623 (C20a); 0.163 (C20d) | C20a (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1930 | 0.1308 (C20a, C20c); 0.131 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A1978 | 0.1459 (C20a, C20c); 0.146 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2055 | 0.1023 (C20a); 0.103 (C20d) | C20a (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2061 | 0.077 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2064 | 0.074 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2067 | 0.077 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2110 | 0.097 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2124 | 0.066 (C20d) | C20d (E-pair) · stacked: C26/C26a | O | — | — | — |
| d | d | d / d | A2163 | 0.203 (C18d) | C18d (E-pair) | L | — | — | — |
| d | d | d / d | A2169 | 0.058 (C20d) | C20d (E-pair) · stacked: C26/C26a | O | — | — | — |
| d | d | d / d | A2175 | 0.096 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2187 | 0.1829 (C20a); 0.183 (C20d) | C20a (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2218 | 0.1710 (C6a); 0.171 (C12d) | C6a (E-pair); C12d (E-pair) | L | — | — | — |
| d | d | d / d | A2245 | 0.088 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2249 | 0.085 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2396 | 0.1919 (C20a); 0.192 (C20d) | C20a (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | A2645 | 0.2510 (C6c/C6d); 0.2509 (C20a); 0.251 (C20d) | C6c/C6d (E-pair); C20a (E); C20d (E-pair) | L, O | — | — | — |
| d | d | d / d | A2667 | 0.2264 (C6a) | C6a (E-pair) | L | S4d (P; not stated; as "A2667") | S4d (P; X under both, does not count; not stated; as "A2667", z 0.23) | — |
| d | d | d / d | A2697 | 0.2320 (C6c/C6d) | C6c/C6d (E-pair) | L | — | S6 (P; E recommended, X strict; projected; as "Abell2697", z 0.2320) | S6 names it without a luminosity (no K data, per both readings): does not count |
| d | d | d / d | A2813 | 0.2924 (C6c/C6d); 0.292 (C18d) | C6c/C6d (E-pair); C18d (E-pair) | L | — | — | — |
| d | d | d / d | A3404 | 0.167 (C18d) | C18d (E-pair) | L | — | — | — |
| d | d | d / d | Bullet | 0.297 (C18d) | C18d (E-pair) | L | — | — | kind: no reading assesses it; A10 check advised before packaging. Possibly the same system as PSZ2 G266.04-21.25 (C29b, z 0.2965); not testable from files, since "Bullet" carries no coordinates; not merged |
| d | d | d / d | Hydra A | 0.0538 (C11b, reader A); 0.0538 (C13g, both readers) | C11b (E); C13g (E) | L | — | — | no file gives an Abell number for Hydra A; not matched to any Abell entry |
| d | d | d / d | MKW11 | 0.023 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | MS1306 | 0.083 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | NGC6107 | 0.032 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | PSZ2 G006.49+50.56 | 0.07854 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G021.10+33.24 | 0.1511 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G028.63+50.15 | 0.09083 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G028.89+60.13 | 0.1519 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G031.93+78.71 | 0.07533 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G033.81+77.18 | 0.06272 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G040.03+74.95 | 0.07067 (C29b); 0.07558 (C29b) | C29b (E) | O | — | — | U6; kind: printed with a sub-component row (bimodal) in C29b |
| d | d | d / d | PSZ2 G040.58+77.12 | 0.0754 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G041.45+29.10 | 0.1771 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G042.81+56.61 | 0.07225 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G044.20+48.66 | 0.08987 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G046.88+56.48 | 0.1137 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G048.10+57.16 | 0.07782 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G049.32+44.37 | 0.09606 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G050.40+31.17 | 0.1605 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G053.53+59.52 | 0.1136 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G055.59+31.85 | 0.2255 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G056.77+36.32 | 0.09696 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G057.61+34.93 | 0.08492 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G057.78+52.32 | 0.06628 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G066.68+68.44 | 0.1625 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G067.17+67.46 | 0.1667 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G067.52+34.75 | 0.1822 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G071.63+29.78 | 0.1575 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G072.62+41.46 | 0.2255 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G073.97-27.82 | 0.2282 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G075.71+13.51 | 0.05455 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G077.90-26.63 | 0.1449 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G080.41-33.24 | 0.1101 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G092.71+73.46 | 0.2317 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G105.55+77.21 | 0.07242 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G107.10+65.32 | 0.2772 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G113.29-29.69 | 0.103 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G114.79-33.71 | 0.09447 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G124.20-36.48 | 0.1921 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G149.39-36.84 | 0.1699 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G159.91-73.50 | 0.2095 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G172.74+65.30 | 0.07529 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G179.09+60.12 | 0.1397 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G192.18+56.12 | 0.1268 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G208.80-30.67 | 0.2468 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G217.09+40.15 | 0.1382 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G224.00+69.33 | 0.1917 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G238.69+63.26 | 0.1672 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G243.64+67.74 | 0.08108 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G273.59+63.27 | 0.1335 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G283.91+73.87 | 0.08635 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G285.63+72.75 | 0.1667 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G287.46+81.12 | 0.07194 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G313.33+61.13 | 0.1848 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | PSZ2 G340.36+60.58 | 0.251 (C29b) | C29b (E) | O | — | — | — |
| d | d | d / d | RXCJ0019.0−2026 | 0.277 (C18d) | C18d (E-pair) | L | — | — | — |
| d | d | d / d | RXCJ0437.1+0043 | 0.284 (C18d) | C18d (E-pair) | L | — | — | — |
| d | d | d / d | RXCJ0528.9−3927 | 0.284 (C18d) | C18d (E-pair) | L | — | — | — |
| d | d | d / d | RXCJ0532.9−3701 | 0.275 (C18d) | C18d (E-pair) | L | — | — | — |
| d | d | d / d | RXCJ1022p3830 | 0.054 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | RXCJ1115p5426 | 0.069 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | RXCJ1210p0523 | 0.077 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | RXCJ1212.3-1816 | 0.2690 (C6c/C6d) | C6c/C6d (E-pair) | L | — | — | — |
| d | d | d / d | RXCJ1326p0013 | 0.084 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | RXCJ1351p4622 | 0.063 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | RXCJ2014.8−2430 | 0.160 (C18d) | C18d (E-pair) | L | — | — | — |
| d | d | d / d | RXCJ2151.0−0736 | 0.284 (C18d) | C18d (E-pair) | L | — | — | — |
| d | d | d / d | RXCJ2214p1350 | 0.026 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | RXCJ2337.6+0016 | 0.278 (C18d); 0.2761 (C29b) | C18d (E-pair); C29b (E) | L, O | — | — | U5 |
| d | d | d / d | RXJ0137 | 0.041 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | SDSS J0928+2031 | 0.1920±0.0009 (C7b) | C7b (E-pair) | L | — | — | — |
| d | d | d / d | SDSS J1207+5254 | 0.275±0.003 (C7b) | C7b (E-pair) | L | — | — | — |
| d | d | d / d | SDSS J1336−0331 | 0.17637±0.00003 (C7b) | C7b (E-pair) | L | — | — | — |
| d | d | d / d | SDSS J1604+2244 | 0.286±0.004 (C7b) | C7b (E-pair) | L | — | — | — |
| d | d | d / d | SHK352 | 0.049 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | XLSSC 008 | 0.299 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 011 | 0.054 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 021 | 0.085 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 022 | 0.293 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 025 | 0.265 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 028 | 0.297 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 035 | 0.174 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 041 | 0.142 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 044 | 0.263 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 050 | 0.140 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 051 | 0.279 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 052 | 0.056 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 057 | 0.153 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 062 | 0.059 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 075 | 0.211 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 077 | 0.202 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 079 | 0.194 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 090 | 0.141 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 095 | 0.138 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 108 | 0.254 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 114 | 0.234 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 117 | 0.298 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 123 | 0.194 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 137 | 0.290 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 138 | 0.140 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 139 | 0.216 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 140 | 0.294 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 141 | 0.196 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 146 | 0.254 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 147 | 0.031 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 148 | 0.294 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 149 | 0.292 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 150 | 0.292 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 151 | 0.189 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 152 | 0.205 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 154 | 0.179 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 162 | 0.138 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 163 | 0.283 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 165 | 0.180 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 166 | 0.158 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 167 | 0.298 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 168 | 0.295 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 171 | 0.044 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 174 | 0.235 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 176 | 0.141 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 177 | 0.211 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 180 | 0.289 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 182 | 0.174 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 189 | 0.204 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 190 | 0.070 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 191 | 0.054 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 193 | 0.203 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 201 | 0.138 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | XLSSC 202 | 0.292 (C18c) | C18c (E-pair) | L | — | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | d | d / d | Zw1665 | 0.030 (C20d) | C20d (E-pair) | O | — | — | — |
| d | d | d / d | ZwCl0104.4+0048 | 0.2540 (C6c/C6d) | C6c/C6d (E-pair) | L | — | — | — |
| d | d | d / d | ZwCl1459.4+4240 | 0.2897 (C6c/C6d) | C6c/C6d (E-pair) | L | — | — | — |
| d | d | d / d | ZwCl 0755.8+5408 | 0.1027 (C20a, C20c); 0.103 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | ZwCl 1023.3+1257 | 0.1422 (C20a, C20c); 0.142 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |
| d | d | d / d | ZwCl 1717.9+5636 | 0.1132 (C20a, C20c); 0.113 (C20d) | C20a (E); C20c (E); C20d (E-pair) | O | — | — | — |

## Uncertain name matches

v2's U1–U6 stand and are carried in the Flags column. New in this version:

Accepted (cluster merged into the v2 row; row flagged):

- **U5, computed** (astropy 8.0.2; L5a printed J2000 positions; tolerance = the v2 designation's cell; |Δz| ≤ 0.02):

| Luminosity entry (record, z) | Matched to (v2 form, A9 z) | Separation | Tolerance | Δz |
|---|---|---|---|---|
| RXCJ0952.8+5153 (L5a, 0.2140) | ZwCl 0949.6+5207 (B1950, precessed; 0.2140–0.2160) | 1.2′ | 1.4′ | 0.000 |
| RXCJ1053.7+5452 (L5a, 0.0750) | RXCJ1053p5450 (C20d, 0.073) | 6.8′ | 8.7′ (C20d form precise to 1 min RA) | 0.002 |

- **Exact name matches with a redshift discrepancy** (A9 value used): MS1006.0+1202, L10 reading prints z 0.221 (A9 source C15a 0.2605; S16b 0.2605); unverified, may be a transcription error in the reading. A1682, L10 prints 0.234 (A9 0.226–0.227): within 0.02.
- **Component row:** L2 prints "A1656b" (sample M, Blue) beside A1656; counted with Coma (A1656), as v2 U6.
- **Names via an alternative name printed in the same L5a row** (no flag): RXCJ0041.8-0918 = A0085, RXCJ0114.9+0022 = A0168, RXCJ0152.7+0100 = A0267, RXCJ0800.9+3602 = A0611, RXCJ0822.1+4705 = A0646, RXCJ0825.4+4707 = A0655, RXCJ0842.9+3621 = A0697, RXCJ0913.7+4742 = A0757, RXCJ0917.8+5143 = A0773, RXCJ1023.6+4908 = A0990. RXCJ1023.6+0411 (L5a) matches v2's form of ZwCl 1021.0+0426 by name.

Not merged (no row changed):

- **ABELL0115a** (L8, z 0.1971) and **A115** (C6c/C6d "ABELL0115", 0.1971): a component suffix; not merged. **No class effect:** S6 names "Abell0115" directly (counts under recommended QL2); under strict QL2 neither L8 nor S6 counts.
- **RXCJ0137.2-0912** (L5a, z 0.039) and **RXJ0137** (C20d, 0.041): the C20d name has no declination, so the separation cannot be computed. Not accepted. **If accepted, RXJ0137 moves from (d) to (a) under both QL2 readings** (L5a is E).
- **zw1615** (L1, z 0.0302): a designation with no declination; no v2 row can be tested against it. Not merged.
- **A3395sw** (L1), **MKW4s** (L1, L4), **A548e** (S2b): no v2 row of that name; not merged with A3395, MKW4 or A548.
- No L2 centre (B1950, precessed) lies within 10′ of any v2 coordinate designation, so no L2 cluster was added by coordinates. L2 prints no redshift, so a U5 match from L2 could not have met the Δz test in any case.
- ACT-CL J0235-5121 (S10a, z 0.278): no v2 coordinate designation within 10′ (and S10a does not count).

## Gaps: why (d) is an upper bound

- **LV3 not cross-matched.** 614 maxBCG clusters (0.05 < z < 0.16) with positions and z, VizieR only; the hosts are unreachable from this workspace. maxBCG names carry coordinates, so they could only be matched by computed separation (U5); nothing was guessed. Under recommended QL2, any A9 cluster in LV3 at 0.05–0.16 would move to (a). Under strict QL2 LV3 does not count, so this gap does not affect the strict counts.
- **L5a: 79 of 114 clusters unread.** The paper prints the first 35 rows; the rest are in CDS J/A+A/423/449 only (unreachable). L5a is E under both readings, so this gap can lower (d) under both.
- **L2: no redshifts.** Matches are by Abell name only; the Δz check could not be applied. The readings state the sample is z ≤ 0.15 (§2), consistent with all 13 matched A9 redshifts (all ≤ 0.08).
- **Large lists matched by name only, without positions** (L1, L5c): an A9 cluster known by a coordinate name (PSZ2, 1eRASS, RXC) that is also an Abell cluster in these lists cannot be found from the files, as in v2. The 51 PSZ2 and 11 1eRASS clusters in (d) are the main candidates.
- **XLSSC.** L9 names 13 XLSSC systems below 0.30; 12 are in the C18c list. XLSSC 111 (z 0.299) is not among v2's C18c rows. The two L9 readings disagree on the count below 0.30 (reader A 13, reader B 15); recounting reader B's own list gives 13 (XLSSC 106 is printed at 0.300).
- **A1651** is named by L1, L23b, S2b, S3a and S3b but is in no non-stacked A9 record, so QL1 (L23b, S3a) has no effect on the counts.
- **Channels.** MS 0440.5+0204, MS 0839.8+2938 and MS 1006.0+1202 are in C15a (gas side) and the stacked C22 only, so their observed-side channel is not determined from non-stacked records. The geometry of S4b and S8d stellar masses is not stated in the S9 readings.
- **S15c** (v2) is still unreadable; S9b names no clusters.

## Disclosures

- While locating table columns, three commands displayed more than identifier columns before being narrowed: the header region of L1 Table 2 (first rows, including the T_X and N_obs columns), the first ten rows of L2 Table 2 (including its luminosity columns) and the first 35 rows of L5a Table 2 (luminosity-function fit columns). None of these values was recorded, used or copied into any file.
- Redshifts in this file are copied as printed (v2 for A9 sources; the source tables or L9 readings for luminosity records). They were not checked against journal versions.

## Changes from version 2

- Printed cluster luminosities (D-071) are added as a second route to class (a). Under recommended QL2, class (a) rises from 14 to 116 and class (d) falls from 260 to 196; under strict QL2, to 89 and 211.
- The v2 main/strict split now matters little: class (a) is unchanged by it, because every S4b-only (a) cluster is also in L1.
- No v2 row, name form, redshift or stellar-mass entry was changed.
