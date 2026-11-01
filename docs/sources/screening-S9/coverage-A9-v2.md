# Coverage of A9 clusters by stellar-mass records, version 2

- **Date:** 2026-10-31. Prepared by Claude (AI assistance, disclosed). Exploratory screening record; not a data package. Not committed.
- **Names and redshifts only.** This file records cluster names, redshifts as printed (or z = cz/c where a table prints velocities), record identifiers and decision codes. It records no mass, fraction, ratio or result.
- **Supersedes** `coverage-A9.md` (version 1, 21 clusters) for the A9 cluster list. Version 1 could name only the clusters printed in the A9 readings; this version uses the sample tables read at source in `names-A9-part1.md` and `names-A9-part2.md`.
- **Not readable:** the cluster list of **S15c** (Erfanianfar et al. 2019, 416 CODEX-SPIDERS BCGs; the catalogue host was blocked). S15c is E (BCG only); any cluster below could also be in it. S9b (P) also names no cluster in the readings.

## Inputs (all read from files; no web access in this step)

| File | SHA-256 |
|---|---|
| `docs/sources/screening-S9/coverage-A9.md` | `426e11558d8cf98ace91e93c8e75f9e5b72be11ee4f88117f2a7406425adc455` |
| `docs/sources/screening-S9/names-A9-part1.md` | `3e14a93ae09a82a64cc7297c90294f3e2b90e3608f96d0936441aa617f546766` |
| `docs/sources/screening-S9/names-A9-part2.md` | `a809b5d18783d3b486abffd38effe1031a5522c4704ae40d35bea6f75bd7c985` |
| `docs/sources/screening-A9/final.csv` | `24b81ce9413da659a556b51bbe9c7f23a647be19584f0bc37a0598eb89c498d3` |
| `docs/sources/screening-A9/reader-a-block1.md` | `02449c2f6bcb392ee5be0d62f4e621f0405960baf2a54bf61898383fc01eb799` |
| `docs/sources/screening-A9/reader-a-block2.md` | `6327104d788e5b429aa75a22cb6c391c8c3f0144ab6fd98ebdef4cc97a98e4ff` |
| `docs/sources/screening-A9/reader-b-block1.md` | `1a0fc7659857dad937a3265168cb8e0a50757c6ebce310eb55136c62a3cb4bac` |
| `docs/sources/screening-A9/reader-b-block2.md` | `5c5e33f6c8846df4845ee6b69b3e1b71151d3247a96148dcb0a9bf829497bdc5` |
| `docs/sources/screening-S9/final.csv` | `439990121d5f2a4010a1d2de33ab27c02ab9855f93efcc0ab8bdbb13b6c4fb7d` |
| `docs/sources/screening-S9/reader-a.md` | `490c999f6341845c61f0e6c01edefac0d8d31e4901c786c72c8a85097f137afd` |
| `docs/sources/screening-S9/reader-b.md` | `80c258992d2178674ebc341e1dd1b50246c02d4ce560a27cf1f706b85c302877` |

## Method

1. **A9 records.** Every row of `screening-A9/final.csv` with final code E or E-pair. Records numbered differently by the two readers are written `A-id/B-id`, as in `final.csv`. Gas-side E-pair records (C3a, C9h/C9i, C15a) and C21b (K-band light side) are included, since they name their clusters.
2. **Cluster names and redshifts.** From the sample tables in `names-A9-part1.md` and `names-A9-part2.md` (C1a, C1b, C1c, C3a, C6a, C6c/C6d, C7a, C7b, C12d, C12e, C15a, C18c, C18d, C20a, C20c, C20d, C21a, C21b, C29a, C29b; stacked C22, C24a, C26). For the other records, from the A9 readings (row and reader given in the z column). C18c prints bare XLSSC numbers, recorded as "XLSSC nnn"; C29a and C29b names take the "1eRASS" and "PSZ2" prefixes from their column headers.
3. **Redshift cut.** A cluster is kept if a non-stacked E/E-pair source prints z < 0.30, or, where no value is printed, a reading states it is below 0.3 (C4a, C11a, C11b, C11c). For C21a and C21b (cz tables) z = cz/c with c = 299 792.458 km/s; the largest cz (13 395 km/s) gives z ≈ 0.045. No cluster has one A9 source below 0.30 and another at or above it.
4. **Merging.** Clusters a reading says the source calls merging are excluded (A10). Every such cluster in the readings (MACS J0717, MACS J0416, A370, AS1063, A2465, AC 114) is either at z ≥ 0.30 or only in a non-E record, so **no cluster below 0.30 is excluded on kind**. Weaker kind notes (substructure, binary, bimodal, supercluster, groups) are kept and flagged.
5. **Stacked-only records** (C6b/C6c, C22/C22a, C24a, C26/C26a) are listed separately (D-067 item 2). A cluster that is also in a non-stacked record appears in the main table.
6. **Name matching.** Names are normalised for case, spacing, hyphens and zero-padding (Abell 1689 = A1689 = ABELL1689 = Abell1689; ACO n = A n; A S n = AS n; Coma = A1656, as C21a/C21b print the same row as "A1656" and "Coma"; MKW04 = MKW4; Zw1215p0400 = Zw1215+0400; ZwCl = Zw; XLSSC zero-padded). Equivalences printed in a source are applied and not flagged (C20c short names: Zw1478, Zw2701, Zw3146, Zw3179, Zw8197, MS0906, RXJ1504, RXJ1720, RXJ2129; C6a footnotes: Z2701 = ZwCl 0949.6+5207, RX J1720 = RX J1720.1+2638, RX J2129 = RX J2129.6+0005, A 521 = RXC J0454.1−1014). All other equivalences are flagged U1–U6 (list at the end). Matches U5 are **computed from the designations themselves** (J2000 names directly; Zw and MS names precessed from B1950; PSZ2 names converted from Galactic coordinates; astropy 8.0.2), accepted when the separation is within the precision of the coarser designation and printed redshifts differ by ≤ 0.02. No coordinate or alias was taken from memory.
7. **Stellar-mass records.** Only S9 records coded **E or P** in `screening-S9/final.csv` (after D-069) are listed. A record counts for a cluster only if its "Clusters covered" column (either reader) names the cluster **with a stellar mass**; records that name a cluster without one (S12b dashes, S12a, S1a for A1644) are listed as "named, no stellar mass" and do not count. Lists used: S1a (reader B, 42 with mass profiles), S4a (reader B, 37 with stellar masses), S4b, S4d, S8a–S8d, S10a, S12a, S12b, S13c, S13e, S14d from the readings; S9a, S10b, S15a from `names-A9-part2.md`.
8. **Components** (from the S9 readings). "full" = members + BCG, with or without ICL. A component counts if at least one reading states it is included and no reading says it is excluded. Where only one reader states the BCG is included (S4a, S4b, S9b: reader A; reader B "not stated") the entry is marked **full (BCG per reader A only)**. Other labels: BCG only (S8a, S9a, S15a, S15c); not stated (S4d, S8b); members only, BCG by dynamical M/L, not eligible (S12a); BCG + core galaxies, core only (S13e, counted as partial).
9. **Classes.** (a) full coverage by an E record; (b) full coverage only by P records; (c) partial only (BCG only, or core only); (d) none (including clusters named only without a stellar mass, or only by "not stated" records). A **strict variant** treats "full (BCG per reader A only)" as "not stated"; where it changes a class, the Flags column says so.

## Summary

| Class | Clusters (main rule) | Clusters (strict variant) |
|---|---|---|
| (a) full stellar coverage by an E record | **14** | 7 |
| (b) full coverage only by P records | **31** | 6 |
| (c) partial only (BCG only or core only) | **14** | 21 |
| (d) none | **260** | 285 |
| Total distinct clusters, z < 0.30, in non-stacked E/E-pair records | **319** | 319 |

Stacked-only clusters (listed separately, not classified): **102** (most from the C24a and C26 lists).

- **(a)**: A85, A209, A1367, A1650, A2142, A2199, A2255, Coma (A1656), MKW04, MKW08, PSZ2 G266.04-21.25, RXCJ0232.2−4420, RXCJ0516.6−5430, Zw1215p0400.
- **(b)**: A115, A119, A160, A168, A267, A383, A586, A697, A773, A781, A957, A1204, A1413, A1682, A1689, A1763, A1914, A2034, A2069, A2111, A2259, A2261, A2399, A2593, A2631, MS 0906.5+1110, MS 1455.0+2232, NGC4325, RXCJ 1504.1-0248, RXJ1720.1+2638, RXJ2129.6+0005.
- **(c)**: A68, A496, A520, A611, A750, A901, A963, A1423, A1553, A1758, A1835, A2390, A2552, MS 0440.5+0204.
- **(d)**: 260 clusters, of which 66 XLSSC (C18c), 51 PSZ2 (C29b) and 11 1eRASS (C29a) carry designations that no stellar-mass record uses in its readings (see "Gaps").

Reading of the result, stated once: class (a) rests on four records: S4b (9 of the 14, BCG stated by reader A only), S12b (A85, A2142, Zw1215), S10b (three clusters, all through computed U5 matches) and S8d (A209). Under the strict variant only 7 keep (a): A85, A209, A2142, and four whose match is uncertain (U4/U5).

## Per-cluster table

Sorted by class, then name. "A9 records" lists non-stacked records (final code); stacked records the cluster also appears in follow "stacked:". Flags: U1–U6 = uncertain name match (see the list at the end); "kind" = kind note, cluster kept.

| Class | Cluster | Other name forms | z (as printed; source) | A9 records (code) | Stellar-mass records naming it (code; components; name as printed) | Flags |
|---|---|---|---|---|---|---|
| a | A85 | A0085 | 0.055 (C20d) | C20d (E-pair) · stacked: C26/C26a | S1a (P; full; as "A85"); S4b (E; full (BCG per reader A only); as "A85"); S12a (P; named, no stellar mass for it); S12b (E; full; as "A85") | kind: C28b reader B notes other literature calls A85 merging (titles only); the source is not reported as doing so |
| a | A209 | A 209, ABELL0209, Abell 209 | 0.206 (C1a, C1b, C3a, C12d, C18d); 0.21 (C1c); 0.2060 (C6c/C6d); readings: ~0.2 (reader A); 0.2 (reader B) (C13c) | C1a (E); C1b (E); C1c (E); C3a (E-pair); C6c/C6d (E-pair); C12d (E-pair); C13c (E-pair); C18d (E-pair) | S8a (E; BCG only; as "A209"); S8d (E; full; as "Abell 209") | — |
| a | A1367 | — | 0.0217 [= cz/c, cz 6495 km/s] (C21a, C21b) | C21a (E-pair); C21b (E-pair) | S4b (E; full (BCG per reader A only); as "A1367") | class d if BCG inclusion must be stated by both readers |
| a | A1650 | — | 0.084 (C20d) | C20d (E-pair) | S4b (E; full (BCG per reader A only); as "A1650") | class d if BCG inclusion must be stated by both readers |
| a | A2142 | — | 0.089 (C20d); readings: "z 0.091–0.228 ... all 4 below 0.3" (C11a, reader A); 0.09 (reader A); 0.090 (reader B) (C28a) | C11a (E); C20d (E-pair); C28a (E) | S4b (E; full (BCG per reader A only); as "A2142"); S12a (P; members only (BCG by dynamical M/L, not eligible); as "A2142"); S12b (E; full; as "A2142") | kind: substructure noted (C11a, C28a reader B); merging not stated |
| a | A2199 | — | 0.031 (C20d); 0.0304 [= cz/c, cz 9101 km/s] (C21a, C21b) | C20d (E-pair); C21a (E-pair); C21b (E-pair); C21c (E-pair) | S4b (E; full (BCG per reader A only); as "A2199") | kind: supercluster A2199+A2197+group (C21c); class d if BCG inclusion must be stated by both readers |
| a | A2255 | — | 0.080 (C20d) | C20d (E-pair) | S4b (E; full (BCG per reader A only); as "A2255"); S12a (P; named, no stellar mass for it); S12b (E; named, no stellar mass for it) | kind: an S9 reading (S19 dataset title) calls it "post-merger"; no A9 reading does; A10 check; class d if BCG inclusion must be stated by both readers |
| a | Coma (A1656) | A1656, Coma | 0.0233 [= cz/c, cz 6973 km/s] (C21a, C21b); readings: ~0.024 (reader A); 0.024 (reader B) (C13a); ≈ 0.023 (C23c reader A, citing C23d text) | C13a (E-pair); C21a (E-pair); C21b (E-pair); C23a (E-pair); C23b (E-pair); C23c (E) | S4b (E; full (BCG per reader A only); as "Coma") | kind: infalling groups noted (C13a reader B); merging not stated; class d if BCG inclusion must be stated by both readers |
| a | MKW04 | MKW4 | 0.020 (C20d) | C20d (E-pair) | S4b (E; full (BCG per reader A only); as "MKW4") | class d if BCG inclusion must be stated by both readers |
| a | MKW08 | MKW8 | 0.027 (C20d) | C20d (E-pair) | S4b (E; full (BCG per reader A only); as "MKW8") | class d if BCG inclusion must be stated by both readers |
| a | PSZ2 G266.04-21.25 | SPT-CL J0658-5556, XMMXCSJ065829.1-555641.5 | 0.2965 (C29b) | C29b (E) | S9a (E; BCG only; as "XMMXCSJ065829.1-555641.5"); S10b (E; full; as "SPT-CL J0658-5556") | U5; possibly the same system as "Bullet" (C18d, z 0.297); not testable from files; not merged |
| a | RXCJ0232.2−4420 | SPT-CL J0232-4421 | 0.284 (C18d) | C18d (E-pair) | S10b (E; full; as "SPT-CL J0232-4421") | U5 |
| a | RXCJ0516.6−5430 | ACT-CL-J0516-5430, SPT-CL J0516-5430, XMMXCSJ051636.81-543113.3 | 0.295 (C18d) | C18d (E-pair) | S9a (E; BCG only; as "XMMXCSJ051636.81-543113.3"); S10b (E; full; as "SPT-CL J0516-5430"); S15a (E; BCG only; as "ACT-CL-J0516-5430") | U5 |
| a | Zw1215p0400 | 1eRASS J121741.6+033931, ZW1215, Zw1215, ZwCl1215 | 0.077 (C20d); 0.0773 (C29a) | C20d (E-pair); C29a (E) | S4b (E; full (BCG per reader A only); as "ZwCl1215"); S12a (P; named, no stellar mass for it); S12b (E; full; as "ZW1215") | U4; U5 |
| b | A115 | ABELL0115 | 0.1971 (C6c/C6d) | C6c/C6d (E-pair) | S4a (P; full (BCG per reader A only); as "A115") | class d if BCG inclusion must be stated by both readers |
| b | A119 | A0119 | 0.044 (C20d); 0.0443 [= cz/c, cz 13268 km/s] (C21a, C21b) | C20d (E-pair); C21a (E-pair); C21b (E-pair) · stacked: C26/C26a | S1a (P; full; as "A119") | — |
| b | A160 | A0160 | 0.043 (C20d) | C20d (E-pair) · stacked: C26/C26a | S1a (P; full; as "A160") | — |
| b | A168 | A0168 | 0.045 (C20d); 0.0447 [= cz/c, cz 13395 km/s] (C21a, C21b) | C20d (E-pair); C21a (E-pair); C21b (E-pair) · stacked: C26/C26a | S1a (P; full; as "A168") | — |
| b | A267 | A 267, A0267, ABELL0267 | 0.2300 (C6c/C6d); 0.230 (C12d); 0.2291 (C20a); 0.229 (C20d) | C6c/C6d (E-pair); C12d (E-pair); C20a (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A267") | class d if BCG inclusion must be stated by both readers |
| b | A383 | A 383, ABELL0383, Abell 383 | 0.187 (C1a, C1b, C3a, C12d, C18d); 0.189 (C1c); 0.1883 (C6a, C6c/C6d); readings: 0.187 (C13h, reader B) | C1a (E); C1b (E); C1c (E); C3a (E-pair); C6a (E-pair); C6c/C6d (E-pair); C12d (E-pair); C13h (E); C18d (E-pair) | S4a (P; full (BCG per reader A only); as "A383"); S8a (E; BCG only; as "A383") | class c if BCG inclusion must be stated by both readers |
| b | A586 | ABELL0586 | 0.1710 (C6c/C6d) | C6c/C6d (E-pair) | S4a (P; full (BCG per reader A only); as "A586") | class d if BCG inclusion must be stated by both readers |
| b | A697 | A0697, ABELL0697, Abell 0697 | 0.2820 (C6c/C6d); 0.2812 (C20a, C20c); 0.282 (C20d) | C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A697") | class d if BCG inclusion must be stated by both readers |
| b | A773 | A 773, A0773, ABELL0773, Abell 0773 | 0.2170 (C6a, C6c/C6d); 0.2173 (C20a, C20c); 0.218 (C20d) | C6a (E-pair); C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A773") | class d if BCG inclusion must be stated by both readers |
| b | A781 | ABELL0781 | 0.2984 (C6c/C6d) | C6c/C6d (E-pair) | S4a (P; full (BCG per reader A only); as "A781") | S4a reading prints z 0.30 (A9 source 0.2984); class d if BCG inclusion must be stated by both readers |
| b | A957 | A0957, ACO 957 | 0.046 (C20d) | C20d (E-pair) · stacked: C24a, C26/C26a | S1a (P; full; as "A957") | — |
| b | A1204 | Abell 1204, Abell1204 | 0.1706 (C20a, C20c); 0.170 (C20d) | C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A1204"); S15a (E; BCG only; as "Abell1204") | class c if BCG inclusion must be stated by both readers |
| b | A1413 | A 1413, Abell 1413 | 0.1427 (C6a); 0.1412 (C20a, C20c); 0.141 (C20d) | C6a (E-pair); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A1413") | class d if BCG inclusion must be stated by both readers |
| b | A1682 | ABELL1682, Abell 1682 | 0.2260 (C6c/C6d); 0.2272 (C20a, C20c); 0.227 (C20d) | C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A1682") | class d if BCG inclusion must be stated by both readers |
| b | A1689 | A 1689, ABELL1689, Abell 1689, Abell1689 | 0.1832 (C6a, C6c/C6d); 0.184 (C12d, C20d); 0.183 (C18d); 0.1842 (C20a, C20c); readings: 0.183 (C9b reader A; C9a reader B); "z 0.091–0.228 ... all 4 below 0.3" (C11a, reader A); "all below 0.3" (C11b, reader A) | C6a (E-pair); C6c/C6d (E-pair); C9a (E); C9b (E); C9c (E); C9d/C9e (E); C9e/C9f (E); C9f/C9g (E); C9g/C9h (E); C9h/C9i (E-pair); C11a (E); C11b (E); C12c (E-pair); C12d (E-pair); C18d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A1689"); S4d (P; not stated; as "A1689"); S13e (P; BCG + core galaxies, core only; as "Abell 1689"); S15a (E; BCG only; as "Abell1689") | class c if BCG inclusion must be stated by both readers |
| b | A1763 | A 1763, ABELL1763, Abell 1763 | 0.2279 (C6c/C6d); 0.228 (C12d); 0.2312 (C20a, C20c); 0.231 (C20d) | C6c/C6d (E-pair); C12d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A1763") | class d if BCG inclusion must be stated by both readers |
| b | A1914 | ABELL1914, Abell 1914 | 0.1712 (C6c/C6d); 0.1660 (C20a, C20c); 0.166 (C20d) | C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A1914") | class d if BCG inclusion must be stated by both readers |
| b | A2034 | Abell 2034 | 0.1132 (C20a, C20c); 0.113 (C20d) | C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A2034") | class d if BCG inclusion must be stated by both readers |
| b | A2069 | Abell 2069 | 0.1139 (C20a, C20c); 0.114 (C20d) | C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A2069") | class d if BCG inclusion must be stated by both readers |
| b | A2111 | ABELL2111, Abell 2111 | 0.2290 (C6c/C6d); 0.2291 (C20a, C20c); 0.230 (C20d) | C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A2111") | class d if BCG inclusion must be stated by both readers |
| b | A2259 | Abell 2259 | 0.1605 (C20a, C20c); 0.160 (C20d) | C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A2259") | class d if BCG inclusion must be stated by both readers |
| b | A2261 | ABELL2261, Abell 2261 | 0.224 (C1a, C1b, C3a); 0.225 (C1c, C20d); 0.2240 (C6c/C6d); 0.2242 (C20a, C20c); readings: 0.225 (C5a, both readers); "z 0.091–0.228 ... all 4 below 0.3" (C11a, reader A) | C1a (E); C1b (E); C1c (E); C3a (E-pair); C5a (E); C6c/C6d (E-pair); C11a (E); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A2261"); S8a (E; BCG only; as "A2261") | class c if BCG inclusion must be stated by both readers |
| b | A2399 | — | 0.058 (C20d) | C20d (E-pair) · stacked: C26/C26a | S1a (P; full; as "A2399") | — |
| b | A2593 | — | 0.042 (C20d) | C20d (E-pair) · stacked: C26/C26a | S1a (P; full; as "A2593") | — |
| b | A2631 | ABELL2631, Abell2631 | 0.2779 (C6c/C6d); 0.2765 (C20a); 0.277 (C20d) | C6c/C6d (E-pair); C20a (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "A2631"); S4d (P; not stated; as "A2631"); S15a (E; BCG only; as "Abell2631") | class c if BCG inclusion must be stated by both readers |
| b | MS 0906.5+1110 | MS0906, MS0906+11, MS0906.5+1110, PSZ2 G218.81+35.51, PSZ2 G218.81+35.51 a, PSZ2 G218.81+35.51 b | 0.1709 (C15a); 0.1767 (C20a, C20c); 0.177 (C20d); 0.1663 (C29b); 0.1643 (C29b); 0.1776 (C29b) | C15a (E-pair); C20a (E); C20c (E); C20d (E-pair); C29b (E) · stacked: C22/C22a | S4a (P; full (BCG per reader A only); as "MS0906.5+1110") | U3; U5; kind: C22 calls MS 0906+11 a "strong binary"; PSZ2 G218.81+35.51 is printed with sub-component rows (bimodal) in C29b; class d if BCG inclusion must be stated by both readers |
| b | MS 1455.0+2232 | MS1455+22, MS1455.0+2232, ZwCl1454.8+2233 | 0.2578 (C6c/C6d); 0.2570 (C15a) | C6c/C6d (E-pair); C15a (E-pair) · stacked: C22/C22a | S4a (P; full (BCG per reader A only); as "MS1455.0+2232") | U3; U5; class d if BCG inclusion must be stated by both readers |
| b | NGC4325 | — | 0.025 (C20d) | C20d (E-pair) | S4a (P; full (BCG per reader A only); as "NGC4325") | class d if BCG inclusion must be stated by both readers |
| b | RXCJ 1504.1-0248 | RXCJ1504.1-0248, RXJ1504, RXJ1504-0248 | 0.2153 (C6c/C6d); 0.215 (C18d); 0.2168 (C20a, C20c); 0.216 (C20d) | C6c/C6d (E-pair); C18d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "RXJ1504-0248") | U2; class d if BCG inclusion must be stated by both readers |
| b | RXJ1720.1+2638 | PSZ2 G049.22+30.87, RX J1720, RX-J1720.1+2638, RXCJ 1720+2638, RXJ1720 | 0.1640 (C6a, C6c/C6d); 0.1604 (C20a, C20c); 0.160 (C20d); 0.1606 (C29b) | C6a (E-pair); C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair); C29b (E) | S4a (P; full (BCG per reader A only); as "RXJ1720.1+2638"); S15a (E; BCG only; as "RX-J1720.1+2638") | U5; S4a reading prints z 0.39 for this name (A9 sources 0.160–0.164): z discrepancy in the S9 reading, unverified; class c if BCG inclusion must be stated by both readers |
| b | RXJ2129.6+0005 | ACT-CL-J2129.6+0005, RX J2129, RX J2129.7+0005, RXCJ 2129+0005, RXJ2129, RXJ2129+0005, RXJ2129.7+0005 | 0.234 (C1a, C1b, C1c, C3a, C20d); 0.2350 (C6a, C6c/C6d); 0.2339 (C20a, C20c); readings: "1 below 0.3 (RX J2129.7+0005)" (C4a, reader A); no value printed | C1a (E); C1b (E); C1c (E); C3a (E-pair); C4a (E); C6a (E-pair); C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S4a (P; full (BCG per reader A only); as "RXJ2129.6+0005"); S8a (E; BCG only; as "RXJ2129+0005"); S15a (E; BCG only; as "ACT-CL-J2129.6+0005") | U1; class c if BCG inclusion must be stated by both readers |
| c | A68 | A 68, ABELL0068, Abell68 | 0.2546 (C6a, C6c/C6d); 0.255 (C12d) | C6a (E-pair); C6c/C6d (E-pair); C12d (E-pair) | S15a (E; BCG only; as "Abell68") | — |
| c | A496 | Abell496 | 0.0330 [= cz/c, cz 9900 km/s] (C21a, C21b) | C21a (E-pair); C21b (E-pair) | S4d (P; not stated; as "A496"); S15a (E; BCG only; as "Abell496") | — |
| c | A520 | Abell520 | 0.199 (C18d) | C18d (E-pair) | S15a (E; BCG only; as "Abell520") | kind: no reading assesses it; A10 check advised before packaging |
| c | A611 | A 611, ABELL0611, Abell 611 | 0.288 (C1a, C1b, C3a); 0.29 (C1c); 0.2850 (C6a); 0.2880 (C6c/C6d) | C1a (E); C1b (E); C1c (E); C3a (E-pair); C6a (E-pair); C6c/C6d (E-pair) | S8a (E; BCG only; as "A611") | — |
| c | A750 | A0750, ABELL0750, Abell750 | 0.1630 (C6c/C6d); 0.1640 (C20a); 0.164 (C20d) | C6c/C6d (E-pair); C20a (E); C20d (E-pair) | S15a (E; BCG only; as "Abell750") | — |
| c | A901 | ABELL0901, Abell901 | 0.1634 (C6c/C6d) | C6c/C6d (E-pair) | S15a (E; BCG only; as "Abell901") | — |
| c | A963 | A 963, A0963, ABELL0963, Abell 0963, Abell963 | 0.2050 (C6a, C6c/C6d); 0.206 (C12d); 0.2041 (C20a, C20c); 0.204 (C20d) | C6a (E-pair); C6c/C6d (E-pair); C12d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S15a (E; BCG only; as "Abell963") | — |
| c | A1423 | ABELL1423, Abell 1423, Abell1423 | 0.213 (C1c, C3a); 0.2130 (C6c/C6d); 0.2142 (C20a, C20c); 0.214 (C20d) | C1c (E); C3a (E-pair); C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S8a (E; BCG only; as "A1423") | — |
| c | A1553 | Abell 1553, Abell1553 | 0.1668 (C20a, C20c); 0.167 (C20d) | C20a (E); C20c (E); C20d (E-pair) | S15a (E; BCG only; as "Abell1553") | — |
| c | A1758 | Abell1758 | 0.2760 (C20a); 0.276 (C20d) | C20a (E); C20d (E-pair) | S15a (E; BCG only; as "Abell1758") | possibly the same system as A1758N (C6c/C6d); not merged |
| c | A1835 | A 1835, ABELL1835, Abell 1835, Abell1835 | 0.2528 (C6a, C6c/C6d); 0.253 (C12d, C18d); 0.2506 (C20a, C20c); 0.252 (C20d); readings: "all below 0.3" (C11b, reader A); 0.252 (C12f, reader A) | C6a (E-pair); C6c/C6d (E-pair); C11b (E); C12d (E-pair); C12f (E-pair); C18d (E-pair); C20a (E); C20c (E); C20d (E-pair) | S15a (E; BCG only; as "Abell1835") | — |
| c | A2390 | A 2390, ABELL2390, Abell 2390, Abell2390 | 0.2329 (C6a, C6c/C6d); 0.233 (C12d); 0.2279 (C15a); 0.228 (C18d); readings: "z 0.091–0.228 ... all 4 below 0.3" (C11a, reader A); 0.228 (C14a, both readers); 0.228 (C14b, both readers) | C6a (E-pair); C6c/C6d (E-pair); C11a (E); C12d (E-pair); C14a (E-pair); C14b (E-pair); C15a (E-pair); C18d (E-pair) · stacked: C22/C22a | S15a (E; BCG only; as "Abell2390") | — |
| c | A2552 | ABELL2552, Abell2552 | 0.2998 (C6c/C6d) | C6c/C6d (E-pair) | S15a (E; BCG only; as "Abell2552") | S15a prints z_spec 0.302 (A9 source C6c/C6d 0.2998) |
| c | MS 0440.5+0204 | MS-0440+0204, MS0440+02 | 0.1965 (C15a) | C15a (E-pair) · stacked: C22/C22a | S15a (E; BCG only; as "MS-0440+0204") | U3 |
| d | 1eRASS J004207.1-283154 | — | 0.1075 (C29a) | C29a (E) | — | — |
| d | 1eRASS J073220.0+313748 | PSZ2 G187.53+21.92 | 0.1705 (C29a); 0.1707 (C29b) | C29a (E); C29b (E) | — | U5 |
| d | 1eRASS J073721.1+351739 | — | 0.2094 (C29a) | C29a (E) | — | — |
| d | 1eRASS J080056.9+360324 | — | 0.2866 (C29a) | C29a (E) | — | — |
| d | 1eRASS J082317.9+155700 | — | 0.1529 (C29a) | C29a (E) | — | — |
| d | 1eRASS J084257.5+362208 | PSZ2 G186.37+37.26 | 0.2818 (C29a, C29b) | C29a (E); C29b (E) | — | U5 |
| d | 1eRASS J090131.5+030055 | — | 0.1936 (C29a) | C29a (E) | — | — |
| d | 1eRASS J101703.2+390250 | — | 0.2048 (C29a) | C29a (E) | — | — |
| d | 1eRASS J115518.0+232422 | PSZ2 G226.18+76.79 | 0.1422 (C29a); 0.1415 (C29b) | C29a (E); C29b (E) | — | U5 |
| d | 1eRASS J125922.4-041138 | — | 0.0843 (C29a) | C29a (E) | — | — |
| d | 1eRASS J130252.8-023059 | — | 0.0838 (C29a) | C29a (E) | — | — |
| d | A141 | ABELL0141 | 0.2300 (C6c/C6d) | C6c/C6d (E-pair) | — | — |
| d | A194 | — | 0.0178 [= cz/c, cz 5341 km/s] (C21a, C21b) | C21a (E-pair); C21b (E-pair) | — | — |
| d | A291 | ABELL0291 | 0.1960 (C6c/C6d) | C6c/C6d (E-pair) | — | — |
| d | A295 | A0295 | 0.042 (C20d) | C20d (E-pair) | — | — |
| d | A478 | — | 0.0881 (C11b, reader A); 0.0881 per C13g (C13f, reader A); 0.0881 (C13g, both readers) | C11b (E); C13f (E); C13g (E) | — | — |
| d | A521 | A 521, ABELL0521 | 0.2475 (C6a, C6c/C6d) | C6a (E-pair); C6c/C6d (E-pair) | — | — |
| d | A539 | — | 0.0291 [= cz/c, cz 8717 km/s] (C21a, C21b) | C21a (E-pair); C21b (E-pair) | — | — |
| d | A576 | — | 0.0384 [= cz/c, cz 11510 km/s] (C21a, C21b) | C21a (E-pair); C21b (E-pair) | — | — |
| d | A602 | A0602 | 0.060 (C20d) | C20d (E-pair) · stacked: C26/C26a | — | — |
| d | A646 | A0646 | 0.1273 (C20a); 0.127 (C20d) | C20a (E); C20d (E-pair) | — | — |
| d | A655 | A0655, Abell 0655 | 0.1271 (C20a, C20c); 0.127 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A667 | A0667 | 0.1452 (C20a); 0.145 (C20d) | C20a (E); C20d (E-pair) | — | — |
| d | A671 | A0671 | 0.050 (C20d) | C20d (E-pair) · stacked: C26/C26a | — | — |
| d | A689 | A0689 | 0.2789 (C20a); 0.279 (C20d) | C20a (E); C20d (E-pair) | — | — |
| d | A757 | A0757 | 0.051 (C20d) | C20d (E-pair) | — | — |
| d | A779 | A0779 | 0.023 (C20d) | C20d (E-pair) | — | — |
| d | A795 | A0795, Abell 0795 | 0.1374 (C20a, C20c); 0.137 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A868 | A 868 | 0.1535 (C6a) | C6a (E-pair) | — | — |
| d | A907 | ABELL0907 | 0.1669 (C6c/C6d); 0.153 (C18d) | C6c/C6d (E-pair); C18d (E-pair) | — | — |
| d | A954 | A0954 | 0.096 (C20d) | C20d (E-pair) | — | — |
| d | A971 | A0971 | 0.092 (C20d) | C20d (E-pair) | — | — |
| d | A980 | A0980, Abell 0980 | 0.1555 (C20a, C20c); 0.156 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A990 | A0990, Abell 0990 | 0.1416 (C20a, C20c); 0.141 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1033 | Abell 1033 | 0.1220 (C20a, C20c); 0.122 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1035A | — | 0.068 (C20d) | C20d (E-pair) | — | component row as printed (C20d) |
| d | A1035B | — | 0.078 (C20d) | C20d (E-pair) | — | component row as printed (C20d) |
| d | A1066 | — | 0.069 (C20d) | C20d (E-pair) | — | — |
| d | A1068 | Abell 1068 | 0.1386 (C20a, C20c); 0.138 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1132 | Abell 1132 | 0.1351 (C20a, C20c); 0.135 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1142 | — | 0.036 (C20d) | C20d (E-pair) | — | — |
| d | A1173 | — | 0.076 (C20d) | C20d (E-pair) | — | — |
| d | A1190 | — | 0.076 (C20d) | C20d (E-pair) | — | — |
| d | A1201 | A 1201, Abell 1201 | 0.1688 (C6a); 0.1671 (C20a, C20c); 0.167 (C20d) | C6a (E-pair); C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1205 | — | 0.076 (C20d) | C20d (E-pair) | — | — |
| d | A1235 | Abell 1235 | 0.1030 (C20a, C20c); 0.103 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1246 | Abell 1246 | 0.1921 (C20a, C20c); 0.192 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1291A | — | 0.051 (C20d) | C20d (E-pair) | — | component row as printed (C20d) |
| d | A1291B | — | 0.059 (C20d) | C20d (E-pair) | — | component row as printed (C20d) |
| d | A1302 | Abell 1302 | 0.1152 (C20a, C20c); 0.116 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1314 | — | 0.033 (C20d) | C20d (E-pair) | — | — |
| d | A1361 | — | 0.1159 (C20a); 0.116 (C20d) | C20a (E); C20d (E-pair) | — | — |
| d | A1366 | — | 0.1160 (C20a); 0.116 (C20d) | C20a (E); C20d (E-pair) | — | — |
| d | A1377 | — | 0.052 (C20d) | C20d (E-pair) | — | — |
| d | A1424 | — | 0.075 (C20d) | C20d (E-pair) | — | — |
| d | A1436 | — | 0.064 (C20d) | C20d (E-pair) | — | — |
| d | A1437 | Abell 1437 | 0.1333 (C20a, C20c); 0.133 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1451 | ABELL1451 | 0.1992 (C6c/C6d) | C6c/C6d (E-pair) | — | — |
| d | A1552 | — | 0.086 (C20d) | C20d (E-pair) | — | — |
| d | A1663 | — | 0.084 (C20d) | C20d (E-pair) | — | — |
| d | A1703 | A 1703 | 0.2800 (C6a); 0.277 (C7a); readings: "1 below 0.3 (A1703)" (C11c, reader A) | C6a (E-pair); C7a (E-pair); C9e/C9f (E); C11c (E-pair) | — | — |
| d | A1728 | — | 0.089 (C20d) | C20d (E-pair) | — | — |
| d | A1750 | ACO 1750 | 0.085 (C20d) | C20d (E-pair) · stacked: C24a | — | — |
| d | A1758N | ABELL1758N | 0.2800 (C6c/C6d) | C6c/C6d (E-pair) | — | possibly the same system as A1758 (N component); not merged |
| d | A1767 | — | 0.071 (C20d) | C20d (E-pair) | — | — |
| d | A1773 | — | 0.078 (C20d) | C20d (E-pair) | — | — |
| d | A1809 | — | 0.079 (C20d) | C20d (E-pair) | — | — |
| d | A1885 | — | 0.089 (C20d) | C20d (E-pair) | — | — |
| d | A1902 | — | 0.1623 (C20a); 0.163 (C20d) | C20a (E); C20d (E-pair) | — | — |
| d | A1918 | Abell 1918 | 0.1388 (C20a, C20c); 0.140 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1930 | Abell 1930 | 0.1308 (C20a, C20c); 0.131 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A1978 | Abell 1978 | 0.1459 (C20a, C20c); 0.146 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A2009 | ABELL2009, Abell 2009 | 0.1530 (C6c/C6d); 0.1522 (C20a, C20c); 0.152 (C20d) | C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A2050 | Abell 2050 | 0.1191 (C20a, C20c); 0.119 (C20d) | C20a (E); C20c (E); C20d (E-pair) | S4d (P; not stated; as "A2050") | — |
| d | A2055 | — | 0.1023 (C20a); 0.103 (C20d) | C20a (E); C20d (E-pair) | — | — |
| d | A2061 | — | 0.077 (C20d) | C20d (E-pair) | — | — |
| d | A2064 | — | 0.074 (C20d) | C20d (E-pair) | — | — |
| d | A2067 | — | 0.077 (C20d) | C20d (E-pair) | — | — |
| d | A2110 | — | 0.097 (C20d) | C20d (E-pair) | — | — |
| d | A2124 | — | 0.066 (C20d) | C20d (E-pair) · stacked: C26/C26a | — | — |
| d | A2149 | — | 0.065 (C20d) | C20d (E-pair) · stacked: C26/C26a | — | — |
| d | A2163 | — | 0.203 (C18d) | C18d (E-pair) | — | — |
| d | A2169 | — | 0.058 (C20d) | C20d (E-pair) · stacked: C26/C26a | — | — |
| d | A2175 | — | 0.096 (C20d) | C20d (E-pair) | — | — |
| d | A2187 | — | 0.1829 (C20a); 0.183 (C20d) | C20a (E); C20d (E-pair) | — | — |
| d | A2197 | — | 0.030 (C20d) | C20d (E-pair); C21c (E-pair) | — | kind: part of the A2199 supercluster (C21c); C21c names it only for X-ray of its components |
| d | A2204 | A 2204, ABELL2204 | 0.1524 (C6a, C6c/C6d); 0.152 (C18d); readings: 0.152 (C12f, reader A) | C6a (E-pair); C6c/C6d (E-pair); C12f (E-pair); C18d (E-pair) | — | — |
| d | A2218 | A 2218 | 0.1710 (C6a); 0.171 (C12d) | C6a (E-pair); C12d (E-pair) | — | — |
| d | A2219 | A 2219, ABELL2219, Abell 2219 | 0.2281 (C6a, C6c/C6d); 0.228 (C12d); 0.2257 (C20a, C20c); 0.226 (C20d) | C6a (E-pair); C6c/C6d (E-pair); C12d (E-pair); C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | A2244 | — | 0.099 (C20d) | C20d (E-pair) | — | — |
| d | A2245 | — | 0.088 (C20d) | C20d (E-pair) | — | — |
| d | A2249 | — | 0.085 (C20d) | C20d (E-pair) | — | — |
| d | A2396 | — | 0.1919 (C20a); 0.192 (C20d) | C20a (E); C20d (E-pair) | — | — |
| d | A2428 | — | 0.084 (C20d) | C20d (E-pair) | — | — |
| d | A2485 | ABELL2485 | 0.2472 (C6c/C6d) | C6c/C6d (E-pair) | — | — |
| d | A2537 | ABELL2537 | 0.2966 (C6c/C6d); 0.297 (C18d) | C6c/C6d (E-pair); C18d (E-pair) | — | — |
| d | A2645 | ABELL2645 | 0.2510 (C6c/C6d); 0.2509 (C20a); 0.251 (C20d) | C6c/C6d (E-pair); C20a (E); C20d (E-pair) | — | — |
| d | A2667 | A 2667 | 0.2264 (C6a) | C6a (E-pair) | S4d (P; not stated; as "A2667") | — |
| d | A2670 | — | 0.076 (C20d) | C20d (E-pair) | — | — |
| d | A2697 | ABELL2697 | 0.2320 (C6c/C6d) | C6c/C6d (E-pair) | — | — |
| d | A2813 | ABELL2813 | 0.2924 (C6c/C6d); 0.292 (C18d) | C6c/C6d (E-pair); C18d (E-pair) | — | — |
| d | A3404 | — | 0.167 (C18d) | C18d (E-pair) | — | — |
| d | Bullet | — | 0.297 (C18d) | C18d (E-pair) | — | kind: no reading assesses it; A10 check advised before packaging. Possibly the same system as PSZ2 G266.04-21.25 (C29b, z 0.2965); not testable from files, since "Bullet" carries no coordinates; not merged |
| d | Hydra A | — | 0.0538 (C11b, reader A); 0.0538 (C13g, both readers) | C11b (E); C13g (E) | — | no file gives an Abell number for Hydra A; not matched to any Abell entry |
| d | MKW11 | — | 0.023 (C20d) | C20d (E-pair) | — | — |
| d | MS1306 | — | 0.083 (C20d) | C20d (E-pair) | — | — |
| d | MS 0451.5+0250 | MS0451+02, PSZ2 G195.75-24.32 | 0.2010 (C15a); 0.2007 (C29b) | C15a (E-pair); C29b (E) · stacked: C22/C22a | — | U3; U5 |
| d | MS 0839.8+2938 | MS0839+29 | 0.1928 (C15a) | C15a (E-pair) · stacked: C22/C22a | — | U3 |
| d | MS 1006.0+1202 | MS1006+12 | 0.2605 (C15a) | C15a (E-pair) · stacked: C22/C22a | — | U3 |
| d | NGC6107 | — | 0.032 (C20d) | C20d (E-pair) | — | — |
| d | NGC6338 | — | 0.029 (C20d) | C20d (E-pair) | — | — |
| d | PSZ2 G006.49+50.56 | — | 0.07854 (C29b) | C29b (E) | — | — |
| d | PSZ2 G021.10+33.24 | — | 0.1511 (C29b) | C29b (E) | — | — |
| d | PSZ2 G028.63+50.15 | — | 0.09083 (C29b) | C29b (E) | — | — |
| d | PSZ2 G028.89+60.13 | — | 0.1519 (C29b) | C29b (E) | — | — |
| d | PSZ2 G031.93+78.71 | — | 0.07533 (C29b) | C29b (E) | — | — |
| d | PSZ2 G033.81+77.18 | — | 0.06272 (C29b) | C29b (E) | — | — |
| d | PSZ2 G040.03+74.95 | PSZ2 G040.03+74.95a | 0.07067 (C29b); 0.07558 (C29b) | C29b (E) | — | U6; kind: printed with a sub-component row (bimodal) in C29b |
| d | PSZ2 G040.58+77.12 | — | 0.0754 (C29b) | C29b (E) | — | — |
| d | PSZ2 G041.45+29.10 | — | 0.1771 (C29b) | C29b (E) | — | — |
| d | PSZ2 G042.81+56.61 | — | 0.07225 (C29b) | C29b (E) | — | — |
| d | PSZ2 G044.20+48.66 | — | 0.08987 (C29b) | C29b (E) | — | — |
| d | PSZ2 G046.88+56.48 | — | 0.1137 (C29b) | C29b (E) | — | — |
| d | PSZ2 G048.10+57.16 | — | 0.07782 (C29b) | C29b (E) | — | — |
| d | PSZ2 G049.32+44.37 | — | 0.09606 (C29b) | C29b (E) | — | — |
| d | PSZ2 G050.40+31.17 | — | 0.1605 (C29b) | C29b (E) | — | — |
| d | PSZ2 G053.53+59.52 | — | 0.1136 (C29b) | C29b (E) | — | — |
| d | PSZ2 G055.59+31.85 | — | 0.2255 (C29b) | C29b (E) | — | — |
| d | PSZ2 G056.77+36.32 | — | 0.09696 (C29b) | C29b (E) | — | — |
| d | PSZ2 G057.61+34.93 | — | 0.08492 (C29b) | C29b (E) | — | — |
| d | PSZ2 G057.78+52.32 | — | 0.06628 (C29b) | C29b (E) | — | — |
| d | PSZ2 G066.68+68.44 | — | 0.1625 (C29b) | C29b (E) | — | — |
| d | PSZ2 G067.17+67.46 | — | 0.1667 (C29b) | C29b (E) | — | — |
| d | PSZ2 G067.52+34.75 | — | 0.1822 (C29b) | C29b (E) | — | — |
| d | PSZ2 G071.63+29.78 | — | 0.1575 (C29b) | C29b (E) | — | — |
| d | PSZ2 G072.62+41.46 | — | 0.2255 (C29b) | C29b (E) | — | — |
| d | PSZ2 G073.97-27.82 | — | 0.2282 (C29b) | C29b (E) | — | — |
| d | PSZ2 G075.71+13.51 | — | 0.05455 (C29b) | C29b (E) | — | — |
| d | PSZ2 G077.90-26.63 | — | 0.1449 (C29b) | C29b (E) | — | — |
| d | PSZ2 G080.41-33.24 | — | 0.1101 (C29b) | C29b (E) | — | — |
| d | PSZ2 G092.71+73.46 | — | 0.2317 (C29b) | C29b (E) | — | — |
| d | PSZ2 G105.55+77.21 | — | 0.07242 (C29b) | C29b (E) | — | — |
| d | PSZ2 G107.10+65.32 | — | 0.2772 (C29b) | C29b (E) | — | — |
| d | PSZ2 G113.29-29.69 | — | 0.103 (C29b) | C29b (E) | — | — |
| d | PSZ2 G114.79-33.71 | — | 0.09447 (C29b) | C29b (E) | — | — |
| d | PSZ2 G124.20-36.48 | — | 0.1921 (C29b) | C29b (E) | — | — |
| d | PSZ2 G149.39-36.84 | — | 0.1699 (C29b) | C29b (E) | — | — |
| d | PSZ2 G159.91-73.50 | — | 0.2095 (C29b) | C29b (E) | — | — |
| d | PSZ2 G172.74+65.30 | — | 0.07529 (C29b) | C29b (E) | — | — |
| d | PSZ2 G179.09+60.12 | — | 0.1397 (C29b) | C29b (E) | — | — |
| d | PSZ2 G192.18+56.12 | — | 0.1268 (C29b) | C29b (E) | — | — |
| d | PSZ2 G208.80-30.67 | — | 0.2468 (C29b) | C29b (E) | — | — |
| d | PSZ2 G217.09+40.15 | — | 0.1382 (C29b) | C29b (E) | — | — |
| d | PSZ2 G224.00+69.33 | — | 0.1917 (C29b) | C29b (E) | — | — |
| d | PSZ2 G238.69+63.26 | — | 0.1672 (C29b) | C29b (E) | — | — |
| d | PSZ2 G243.64+67.74 | — | 0.08108 (C29b) | C29b (E) | — | — |
| d | PSZ2 G273.59+63.27 | — | 0.1335 (C29b) | C29b (E) | — | — |
| d | PSZ2 G283.91+73.87 | — | 0.08635 (C29b) | C29b (E) | — | — |
| d | PSZ2 G285.63+72.75 | — | 0.1667 (C29b) | C29b (E) | — | — |
| d | PSZ2 G287.46+81.12 | — | 0.07194 (C29b) | C29b (E) | — | — |
| d | PSZ2 G313.33+61.13 | — | 0.1848 (C29b) | C29b (E) | — | — |
| d | PSZ2 G340.36+60.58 | — | 0.251 (C29b) | C29b (E) | — | — |
| d | RXCJ0019.0−2026 | — | 0.277 (C18d) | C18d (E-pair) | — | — |
| d | RXCJ0437.1+0043 | — | 0.284 (C18d) | C18d (E-pair) | — | — |
| d | RXCJ0528.9−3927 | — | 0.284 (C18d) | C18d (E-pair) | — | — |
| d | RXCJ0532.9−3701 | — | 0.275 (C18d) | C18d (E-pair) | — | — |
| d | RXCJ1022p3830 | — | 0.054 (C20d) | C20d (E-pair) | — | — |
| d | RXCJ1053p5450 | — | 0.073 (C20d) | C20d (E-pair) | — | — |
| d | RXCJ1115p5426 | — | 0.069 (C20d) | C20d (E-pair) | — | — |
| d | RXCJ1210p0523 | — | 0.077 (C20d) | C20d (E-pair) | — | — |
| d | RXCJ1212.3-1816 | — | 0.2690 (C6c/C6d) | C6c/C6d (E-pair) | — | — |
| d | RXCJ1326p0013 | — | 0.084 (C20d) | C20d (E-pair) | — | — |
| d | RXCJ1351p4622 | — | 0.063 (C20d) | C20d (E-pair) | — | — |
| d | RXCJ2014.8−2430 | — | 0.160 (C18d) | C18d (E-pair) | — | — |
| d | RXCJ2102.1-2431 | — | 0.1880 (C6c/C6d) | C6c/C6d (E-pair) | — | — |
| d | RXCJ2151.0−0736 | — | 0.284 (C18d) | C18d (E-pair) | — | — |
| d | RXCJ2214p1350 | — | 0.026 (C20d) | C20d (E-pair) | — | — |
| d | RXCJ2337.6+0016 | PSZ2 G087.03-57.37 | 0.278 (C18d); 0.2761 (C29b) | C18d (E-pair); C29b (E) | — | U5 |
| d | RXJ0137 | — | 0.041 (C20d) | C20d (E-pair) | — | — |
| d | SDSS J0928+2031 | — | 0.1920±0.0009 (C7b) | C7b (E-pair) | — | — |
| d | SDSS J1207+5254 | — | 0.275±0.003 (C7b) | C7b (E-pair) | — | — |
| d | SDSS J1336−0331 | — | 0.17637±0.00003 (C7b) | C7b (E-pair) | — | — |
| d | SDSS J1604+2244 | — | 0.286±0.004 (C7b) | C7b (E-pair) | — | — |
| d | SHK352 | — | 0.049 (C20d) | C20d (E-pair) | — | — |
| d | XLSSC 008 | — | 0.299 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 011 | — | 0.054 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 021 | — | 0.085 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 022 | — | 0.293 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 025 | — | 0.265 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 027 | — | 0.295 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 028 | — | 0.297 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 035 | — | 0.174 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 041 | — | 0.142 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 044 | — | 0.263 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 050 | — | 0.140 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 051 | — | 0.279 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 052 | — | 0.056 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 054 | — | 0.054 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 055 | — | 0.232 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 057 | — | 0.153 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 060 | — | 0.139 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 061 | — | 0.259 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 062 | — | 0.059 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 075 | — | 0.211 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 077 | — | 0.202 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 079 | — | 0.194 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 087 | — | 0.141 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 088 | — | 0.295 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 090 | — | 0.141 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 091 | — | 0.186 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 095 | — | 0.138 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 098 | — | 0.297 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 103 | — | 0.233 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 104 | — | 0.294 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 108 | — | 0.254 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 112 | — | 0.139 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 114 | — | 0.234 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 117 | — | 0.298 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 123 | — | 0.194 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 137 | — | 0.290 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 138 | — | 0.140 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 139 | — | 0.216 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 140 | — | 0.294 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 141 | — | 0.196 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 146 | — | 0.254 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 147 | — | 0.031 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 148 | — | 0.294 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 149 | — | 0.292 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 150 | — | 0.292 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 151 | — | 0.189 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 152 | — | 0.205 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 154 | — | 0.179 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 162 | — | 0.138 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 163 | — | 0.283 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 165 | — | 0.180 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 166 | — | 0.158 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 167 | — | 0.298 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 168 | — | 0.295 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 171 | — | 0.044 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 174 | — | 0.235 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 176 | — | 0.141 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 177 | — | 0.211 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 180 | — | 0.289 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 182 | — | 0.174 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 189 | — | 0.204 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 190 | — | 0.070 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 191 | — | 0.054 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 193 | — | 0.203 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 201 | — | 0.138 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | XLSSC 202 | — | 0.292 (C18c) | C18c (E-pair) | — | kind: C18c readers note many XXL systems are groups (A8 question) |
| d | Zw1665 | — | 0.030 (C20d) | C20d (E-pair) | — | — |
| d | ZwCl0104.4+0048 | — | 0.2540 (C6c/C6d) | C6c/C6d (E-pair) | — | — |
| d | ZwCl0857.9+2107 | — | 0.2347 (C6c/C6d) | C6c/C6d (E-pair) | — | — |
| d | ZwCl1231.4+1007 | — | 0.2290 (C6c/C6d) | C6c/C6d (E-pair) | — | candidate match to RXJ1234.2+0947 (S4a, P, z 0.23) at 5.2 arcmin after precession, beyond designation precision: not accepted (would be class b) |
| d | ZwCl1459.4+4240 | — | 0.2897 (C6c/C6d) | C6c/C6d (E-pair) | — | — |
| d | ZwCl 0755.8+5408 | Zw1478 | 0.1027 (C20a, C20c); 0.103 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | ZwCl 0949.6+5207 | Z2701, Zw2701, ZwCl0949.6+5207 | 0.2140 (C6a, C6c/C6d); 0.2160 (C20a, C20c); 0.215 (C20d) | C6a (E-pair); C6c/C6d (E-pair); C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | ZwCl 1021.0+0426 | RXCJ1023.6+0411, Zw3146, ZwCl1021.0+0426 | 0.2906 (C6c/C6d); 0.280 (C18d); 0.2894 (C20a, C20c); 0.290 (C20d) | C6c/C6d (E-pair); C18d (E-pair); C20a (E); C20c (E); C20d (E-pair) | — | U5 |
| d | ZwCl 1023.3+1257 | Zw3179 | 0.1422 (C20a, C20c); 0.142 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |
| d | ZwCl 1717.9+5636 | Zw8197 | 0.1132 (C20a, C20c); 0.113 (C20d) | C20a (E); C20c (E); C20d (E-pair) | — | — |

## Per-record summary

Counts are distinct clusters (main rule; strict-variant (a) in brackets where it differs). "Named" counts the clusters the record names in the sources used here; "z ≥ 0.30" are excluded by the epoch cut (D-066).

| A9 record | Code | Side / row | Named | z ≥ 0.30 | z < 0.30 | (a) | (b) | (c) | (d) |
|---|---|---|---|---|---|---|---|---|---|
| C1a | E | L | 20 | 15 | 5 | 1 | 3 | 1 | 0 |
| C1b | E | L | 20 | 15 | 5 | 1 | 3 | 1 | 0 |
| C1c | E | L | 25 | 19 | 6 | 1 | 3 | 2 | 0 |
| C3a | E-pair | gas side | 25 | 19 | 6 | 1 | 3 | 2 | 0 |
| C4a | E | L | 8 | 7 | 1 | 0 | 1 | 0 | 0 |
| C5a | E | L | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C5b | E | L | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| C5c | E | L | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| C5f | E | L | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| C6a | E-pair | L | 20 | 0 | 20 | 0 | 6 | 5 | 9 |
| C6c/C6d | E-pair | L | 50 | 0 | 50 | 1 | 18 | 9 | 22 |
| C7a | E-pair | L | 27 | 26 | 1 | 0 | 0 | 0 | 1 |
| C7b | E-pair | L | 37 | 33 | 4 | 0 | 0 | 0 | 4 |
| C9a | E | L | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C9b | E | L | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C9c | E | L | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C9d/C9e | E | L | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C9e/C9f | E | L | 5 | 3 | 2 | 0 | 1 | 0 | 1 |
| C9f/C9g | E | L | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C9g/C9h | E | L | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C9h/C9i | E-pair | gas side | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C11a | E | L | 4 | 0 | 4 | 1 | 2 | 1 | 0 |
| C11b | E | L | 4 | 0 | 4 | 0 | 1 | 1 | 2 |
| C11c | E-pair | L | 4 | 3 | 1 | 0 | 0 | 0 | 1 |
| C12c | E-pair | L | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C12d | E-pair | L | 11 | 0 | 11 | 1 | 4 | 4 | 2 |
| C12e | E-pair | L | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| C12f | E-pair | L | 2 | 0 | 2 | 0 | 0 | 1 | 1 |
| C13a | E-pair | L | 1 | 0 | 1 | 1 [0] | 0 | 0 | 0 |
| C13b | E-pair | L | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| C13c | E-pair | L | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| C13f | E | L | 1 | 0 | 1 | 0 | 0 | 0 | 1 |
| C13g | E | L | 2 | 0 | 2 | 0 | 0 | 0 | 2 |
| C13h | E | L | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C13j | E | L | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| C14a | E-pair | L | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| C14b | E-pair | L | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| C15a | E-pair | gas side | 14 | 7 | 7 | 0 | 2 | 2 | 3 |
| C15b | E | L | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| C15c | E-pair | L | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| C18c | E-pair | L | 136 | 70 | 66 | 0 | 0 | 0 | 66 |
| C18d | E-pair | L | 39 | 15 | 24 | 3 | 3 | 3 | 15 |
| C19a | E-pair | L | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| C19b | E-pair | L | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| C20a | E | O | 58 | 0 | 58 | 0 | 19 | 6 | 33 |
| C20c | E | O | 44 | 0 | 44 | 0 | 17 | 4 | 23 |
| C20d | E-pair | O | 129 | 0 | 129 | 8 [3] | 26 | 6 | 89 |
| C21a | E-pair | O | 9 | 0 | 9 | 3 [0] | 2 | 1 | 3 |
| C21b | E-pair | K-band light side; observed side reused from C21a | 9 | 0 | 9 | 3 [0] | 2 | 1 | 3 |
| C21c | E-pair | O | 2 | 0 | 2 | 1 [0] | 0 | 0 | 1 |
| C23a | E-pair | O | 1 | 0 | 1 | 1 [0] | 0 | 0 | 0 |
| C23b | E-pair | O | 1 | 0 | 1 | 1 [0] | 0 | 0 | 0 |
| C23c | E | O | 1 | 0 | 1 | 1 [0] | 0 | 0 | 0 |
| C27a | E-pair | L | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| C28a | E | O | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| C29a | E | O | 22 | 10 | 12 | 1 | 0 | 0 | 11 |
| C29b | E | O | 77 | 18 | 59 | 1 | 2 | 0 | 56 |

Notes: C4a names 8 clusters (reader B, C4b) and states that only RX J2129.7+0005 is below 0.3. C9e/C9f and C11c name clusters above 0.3 whose redshifts come from other rows (C10a, C1a; the C11c statement). C12e, C5b, C5c, C5f, C13b, C13j, C15b, C15c, C19a, C19b and C27a have no cluster below 0.30. C29b: 80 printed rows (75 sample clusters, 2 extra clusters, 3 sub-component rows); 59 sample clusters are below 0.30 and the sub-component rows are counted with their parent.

**Records with the most clusters in class (a):** C20d 8 (strict 3); C18d 3; C21a 3 (strict 0); C21b 3 (strict 0).

## Stacked-only records (D-067 item 2): clusters not plotted individually

Clusters below z = 0.30 in each stacked record, as printed. A dagger (†) marks a cluster that also appears in a non-stacked record and so has a row in the main table. Stellar coverage is not classified here.

- **C6b/C6c** (E-pair; Okabe et al. 2013, stacked shear of 50 LoCuSS clusters, 0.15 < z < 0.3). **No cluster list is printed** (names-A9-part1). The same 50 names are in C6c/C6d, but this paper does not say so in a table, so none is attributed to it.
- **C22/C22a** (E-pair; van der Marel et al. 2000, CNOC1 ensemble). The paper prints no list; names from Carlberg et al. 1996 Table 1. 8 of 16 below 0.30; the paper excludes MS 0906+11 and MS 1358+62 from the stack.
  - A2390†, MS0440+02†, MS0451+02†, MS0839+29†, MS0906+11†, MS1006+12†, MS1231+15, MS1455+22† (8; 7 †)
- **C24a** (E-pair; Biviano & Girardi 2003, 43 2dFGRS clusters). Table prints mean velocity; z = v/c, largest 39 891 km/s gives z ≈ 0.133; all 43 below 0.30.
  - ACO 419, ACO 892, ACO 957†, ACO 978, ACO 993, ACO 1098, ACO 1308, ACO 1364, ACO 1373, ACO 1750†, ACO 2660, ACO 2726, ACO 2734, ACO 2915, ACO 2967, ACO 2981, ACO 3042, ACO 3814, ACO 3837, ACO 4044, ACO 4049, ACO 4053, ACO S246, ACO S301, ACO S340, ACO S983, ACO S1127, APM 171, APM 294, APM 311, APM 416, APM 715, APM 880, EDCC 69, EDCC 129, EDCC 148, EDCC 153, EDCC 155, EDCC 445, EDCC 601, EDCC 623, EDCC 641, EDCC 642 (43; 2 †)
- **C26/C26a** (E-pair; Mamon et al. 2019, 54 WINGS clusters in 3 stacks). **The 54 are not named**; listed is the parent list of 73 (Cava et al. 2017), all below 0.30. Superset of the clusters used.
  - A85†, A119†, A133, A147, A151, A160†, A168†, A193, A376, A500, A548b, A602†, A671†, A754, A780, A957†, A970, A1069, A1291, A1631a, A1644, A1668, A1736, A1795, A1831, A1983, A1991, A2107, A2124†, A2149†, A2169†, A2256, A2271, A2382, A2399†, A2415, A2457, A2572a, A2589, A2593†, A2622, A2626, A2657, A2717, A2734, A3128, A3158, A3266, A3376, A3395, A3490, A3497, A3528a, A3528b, A3530, A3532, A3556, A3558, A3560, A3667, A3716, A3809, A3880, A4059, IIZW108, MKW3s, RX0058, RX1022, RX1740, Z1261, Z2844, Z8338, Z8852 (73; 12 †)

## Uncertain name matches

Accepted matches (cluster merged into one row; row flagged):

- **U1 — RX J2129+0005 forms.** RX J2129.7+0005 (C1a, C1b, C1c; C4a) = RX J2129.6+0005 (C6a footnote d, C6c/C6d; S4a) = RXJ2129+0005 (C3a; S8a) = RXCJ 2129+0005 / RXJ2129 (C20a, C20c, C20d) = ACT-CL-J2129.6+0005 (S15a). The RA suffix differs (.7, .6, none) and S15a uses an ACT prefix; all printed redshifts are 0.234–0.235. Carried over from version 1.
- **U2 — RXJ1504-0248** (S4a) = RXCJ1504.1-0248 (C6c/C6d; = RXJ1504 per C20c). Truncated designation; z 0.22 (S4a reading) vs 0.2153–0.2168.
- **U3 — MS truncations.** MS0440+02 (C22) and MS-0440+0204 (S15a) = MS 0440.5+0204 (C15a); MS0451+02, MS0839+29, MS0906+11, MS1006+12, MS1455+22 (C22) = the C15a full designations. Printed redshifts agree to 0.001.
- **U4 — Zw1215.** ZwCl1215 (S4b), ZW1215 (S12b) and Zw1215 (S12a) = Zw1215p0400 (C20d). Truncated designation; z 0.0750 (S4b), 0.0766 (S12a) vs 0.077. "Zw1215" could in principle be a Zwicky catalogue number (C20c uses that style, e.g. Zw1478); the redshifts support the coordinate reading.
- **U5 — matches computed from the designations** (astropy 8.0.2; J2000 names direct, Zw/MS precessed from B1950, PSZ2 from Galactic l, b; tolerance = precision of the coarser designation; |Δz| ≤ 0.02):

| Name (record, z) | Matched to (record, z) | Separation |
|---|---|---|
| ZwCl1021.0+0426 = Zw3146 (C6c/C6d 0.2906; C20a/C20c/C20d) | RXCJ1023.6+0411 (C18d, 0.280) | 0.2′ (Δz 0.011) |
| ZwCl1454.8+2233 (C6c/C6d, 0.2578) | MS 1455.0+2232 (C15a 0.257; S4a) | 2.9′ |
| RX J1720.1+2638 (C6a, C6c/C6d; C20a/c/d) | PSZ2 G049.22+30.87 (C29b, 0.1606) | 0.8′ |
| MS 0451.5+0250 (C15a, 0.2010) | PSZ2 G195.75-24.32 (C29b, 0.2007) | 2.8′ |
| MS 0906.5+1110 (C15a; MS0906 in C20a/c/d) | PSZ2 G218.81+35.51 and its rows a, b (C29b, 0.1663; 0.1643, 0.1776) | 1.6′ |
| RXCJ2337.6+0016 (C18d, 0.278) | PSZ2 G087.03-57.37 (C29b, 0.2761) | 1.6′ |
| Zw1215p0400 (C20d, 0.077) | 1eRASS J121741.6+033931 (C29a, 0.0773) | 7.0′ (Zw designation precise to 1 min RA) |
| 1eRASS J073220.0+313748 (C29a, 0.1705) | PSZ2 G187.53+21.92 (C29b, 0.1707) | 1.2′ |
| 1eRASS J084257.5+362208 (C29a, 0.2818) | PSZ2 G186.37+37.26 (C29b, 0.2818) | 0.8′ |
| 1eRASS J115518.0+232422 (C29a, 0.1422) | PSZ2 G226.18+76.79 (C29b, 0.1415) | 0.4′ |
| RXCJ0232.2−4420 (C18d, 0.284) | SPT-CL J0232-4421 (S10b, 0.284) | 3.4′ |
| RXCJ0516.6−5430 (C18d, 0.295) | SPT-CL J0516-5430 (S10b), ACT-CL-J0516-5430 (S15a), XMMXCSJ051636.81-543113.3 (S9a) | 0.7–0.9′ |
| PSZ2 G266.04-21.25 (C29b, 0.2965) | SPT-CL J0658-5556 (S10b, 0.296); XMMXCSJ065829.1-555641.5 (S9a, 0.297) | 1.2′; 1.0′ |

- **U6 — PSZ2 sub-component rows.** G040.03+74.95a and G218.81+35.51 a, b (C29b) are counted with their parent rows.

Not merged (flagged in the rows):

- **A1758** (C20a, C20d; S15a "Abell1758") and **ABELL1758N** (C6c/C6d): possibly one system; kept as two rows.
- **Bullet** (C18d, 0.297) and **PSZ2 G266.04-21.25** (C29b, 0.2965): possibly one system; "Bullet" carries no coordinates, so this cannot be tested from the files.
- **ZwCl1231.4+1007** (C6c/C6d, 0.229) and **RXJ1234.2+0947** (S4a, 0.23): 5.2′ after precession, outside the designation tolerance; not accepted. If accepted, the cluster moves from (d) to (b).
- **Hydra A** (C11b, C13g): no file gives an Abell number; not matched to any Abell entry.
- Stacked lists only: A1291 (C26) vs A1291A/B (C20d); RX1022 (C26) vs RXCJ1022+3830 (C20d). Not merged.

Redshift discrepancies in S9 readings (name match accepted; A9 value used): RXJ1720.1+2638, S4a prints 0.39 (A9 sources 0.160–0.164); A781, S4a prints 0.30 (A9 0.2984); A2552, S15a prints 0.302 (A9 0.2998). Abell 2744 is excluded by its A9 redshift (C18d 0.307) although S14d prints 0.28.

## Gaps: why (d) is an upper bound

- **XLSSC (66 clusters, C18c).** No E/P stellar record uses XLSSC numbers. S9a (106 XMM-XCS BCGs, E, BCG only) and S15c (which, per reader B, includes XMM-XXL BCGs) may overlap, but XCS coordinate names cannot be matched to bare XLSSC numbers without the XXL catalogue coordinates, which no input file gives.
- **PSZ2 (C29b) and 1eRASS (C29a).** Matched only by computed coordinates against other coordinate designations. Abell-named stellar records (S1a, S4a, S4b, S15a) cannot be matched to them from these files, so some C29a/C29b clusters in (d) may have coverage.
- **S15c** list not readable (stated above); **S9b** names not read; **S4a**: reader A did not read names, reader B listed only the 37 rows with stellar masses.
- **Stellar records coded X** (after D-069 and the S9 adjudication) are not listed: S1b, S1c, S2a, S2b, S3a, S3b, S4c, S5, S6, S13a, S13b, S13f, S19 and others.

## Changes from version 1

- Version 1 listed 21 clusters (16 from A9 readings plus 5 X-COP clusters added by instruction). Version 2 lists **319** from A9 records only, because the sample tables were read at source. X-COP clusters are not added: A2255 enters through C20d; A1644, A3158 and A3266 appear only in the stacked C26 parent list; RXC1825 is in no A9 record.
- Codes follow `screening-S9/final.csv` after D-069: S1b, S13f and S19 (galaxy-level or SMF) and S4c (fractions only) are now X and no longer count. Version 1 still listed them.
- Components are now separated. A2261, A383 and RX J2129 were "yes (BCG only)" in version 1 through S8a; they are now (b) through S4a (P), or (c) under the strict variant. A2390 and A1835 move from "no" to (c) through S15a (BCG only). A1689 moves from "pending P" to (b) through S4a.
- Not checked here: whether any of the 319 is called merging by a source not yet read (only the readings were used).
