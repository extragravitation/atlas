# Coverage of A9 clusters by stellar-mass records (S9)

- **Date:** 2026-10-31
- **Inputs:** `screening-A9/final.csv`, `screening-A9/reader-a-block1.md`, `reader-a-block2.md`, `reader-b-block1.md`, `reader-b-block2.md`; `screening-S9/final.csv`, `screening-S9/reader-a.md`, `reader-b.md`. No other source was read and no paper was fetched.
- **Names and redshifts only.** This file records cluster names, redshifts as printed in the readings, record numbers and decision codes. It records no mass, fraction, ratio or result.

## Method

1. Took every A9 row whose final code is E or E-pair. Where reader A and reader B numbered a record differently, it is written `A-id/B-id` (e.g. C9d/C9e), as in `final.csv`.
2. Took cluster names from that record's two readings ("Observed side" and "Notes" columns). Where another row's note says a named cluster belongs to this record (e.g. "A209 overlaps C1a"), the cluster is listed with that record and flagged **[via note in row X]**. Gas-only E-pair records (C3a, C9h/C9i, C15a, C15c) are marked "gas side, no L/O". They are listed against a cluster only where a reading names that cluster in them or names them as its pairing.
3. Redshifts are copied from the A9 readings with the row they come from. Where the A9 readings print none, a redshift printed in the S9 readings is used and marked "(S9 reading)".
4. Exclusions: redshift 0.30 or above, and clusters the readings say their source calls merging (A10). Where a record states how many clusters fall below 0.3 and which ones, the others are taken to be at 0.3 or above.
5. Stellar-mass records: every S-row whose "Clusters covered" column (either reader) names the cluster, with its final code from `screening-S9/final.csv`. "Yes" means at least one E record names the cluster **and** the reading says it gives a stellar mass for it. E records that name a cluster but show no stellar mass for it (S12b's dash entries) do not count.
6. The five X-COP clusters were added as instructed (part C).

## Coverage table

Row codes: L = lensing, O = member-galaxy dynamics.

| Cluster | z (as printed; source row) | A9 records (code, row L/O) | Stellar-mass records naming it (code) | Covered by an E stellar record? (yes / pending P / no) |
|---|---|---|---|---|
| A1689 | 0.183 (C9b, reader A; C9a, reader B) | C9a (E, L); C9b (E, L); C9c (E, L); C9d/C9e (E, L); C9e/C9f (E, L); C9f/C9g (E, L); C9g/C9h (E, L); C9h/C9i (E-pair, gas side, no L/O); C11a (E, L); C11b (E, L); C12c (E-pair, L) | S4a (P; named by reader B only); S4d (P); S6 (X; named by reader A only); S13e (P; core map only) | pending P |
| A2261 | 0.225 (C5a, both readers) | C5a (E, L); C11a (E, L); C1a and C1b (E, L) [via note in C5a, reader A: "Overlaps C1a/C1b"]; C3a (E-pair, gas side; named as pairing in C5a) | S4a (P; reader B only); S8a (E; BCG only) | yes (BCG only) |
| A2142 | 0.09 (C28a, reader A); 0.090 (C28a, reader B) | C11a (E, L); C28a (E, O) | S4b (E); S4c (X); S5 (X; listed by reader A); S11 (X; reader A example); S12a (P); S12b (E) | yes |
| A2390 | 0.228 (C14a, both readers; C14b, reader A) | C11a (E, L); C14a (E-pair, L); C14b (E-pair, L) | S3b (X; reader B: X-ray only, no stellar mass for it); S6 (X; reader A only); S16a (X); S16b (X; "same 15 CNOC1") | no |
| Hydra A | 0.0538 (C11b, reader A; C13g, both readers) | C11b (E, L); C13g (E, L) | none | no |
| A478 | 0.0881 (C11b, reader A; C13g, both readers) | C11b (E, L); C13f (E, L); C13g (E, L) | S3b (X; written "A0478"/"Abell 0478"; reader B: X-ray only, no stellar mass) | no |
| A1835 | 0.252 (C12f, reader A) | C11b (E, L); C12f (E-pair, L) | none | no |
| A1703 | 0.281 (C10a, reader A; C10a is an X record) | C9e/C9f (E, L); C11c (E-pair, L) | none | no |
| A2204 | 0.152 (C12f, reader A) | C12f (E-pair, L) | none | no |
| Coma | ~0.024 (C13a, reader A); 0.024 (C13a, reader B); ≈ 0.023 (C23c, reader A) | C13a (E-pair, L); C23a (E-pair, O); C23b (E-pair, O); C23c (E, O); C21a (E-pair, O) [via note in C21a, reader B: "Includes Coma and A2199"]; C21b (E-pair; reader B row O, reader A baryonic side) [inferred: "8 CAIRNS clusters plus A194"] | S4b (E); S4c (X); S13a (X) | yes |
| A209 | ~0.2 (C13c, reader A); 0.2 (C13c, reader B) | C13c (E-pair, L); C1a (E, L) [via note in C13c, reader A: "A209 overlaps C1a"]; C3a (E-pair, gas side; named as pairing in C13c, reader B) | S6 (X; reader A only); S8a (E; BCG only); S8d (E) | yes |
| A383 | 0.187 (C13h, reader B) | C13h (E, L); C1a and C1b (E, L) [via note in C13h, reader B: "Overlaps C1a–C1b"]; C3a (E-pair, gas side; named as pairing in C13h) | S4a (P; reader B only); S8a (E; BCG only) | yes (BCG only) |
| RX J2129.7+0005 | "below 0.3" (C4a, reader A: "1 below 0.3 (RX J2129.7+0005)"); no number printed against the name | C4a (E, L; reader B lists it as "RX J2129" in C4b, the VizieR half of the same record) | S4a (P; "RXJ2129.6+0005", reader B only); S8a (E; "RXJ2129+0005", BCG only) | yes (BCG only) **[uncertain match: suffix .7 vs .6 vs none; not MACS J2129-07]** |
| A2199 | ≈ 0.03 (C21d, reader B; C21d is an X record) | C21c (E-pair, O; "A2199 supercluster"); C21a (E-pair, O) [via note in C21a, reader B]; C21b (E-pair) [inferred, as for Coma] | S4b (E); S4c (X); S5 (X; reader A only) | yes |
| A2197 | not stated | C21c (E-pair, O; named only for X-ray luminosities of its components; reader B: the system is "A2199+A2197+group") | S5 (X; reader A only) | no **[uncertain: part of the A2199 supercluster, not a separate profile]** |
| A194 | not stated | C21b (E-pair; reader B: "9 systems (8 CAIRNS clusters plus A194)", row O; reader A: baryonic side, observed side reused from C21a) | none | no |
| A1644 (X-COP) | not stated in A9 readings; 0.0473 (S12a, both readers; S9 reading); 0.04691 (S1b, both readers; S9 reading) | none (no A9 E/E-pair record names it) | S1a (P; named, but both readers say no mass profile for it); S1b (P; galaxy-level only, QS4); S2a (X; reader A lists it, reader B found no target match); S12a (P; no stellar mass for it); S12b (E; dash, no stellar mass for it) | pending P (S1b only, QS4) |
| A2255 (X-COP) | not stated in A9 readings; 0.0809 (S12a; S9 reading); 0.0800 (S2b, S4b, S4c; S9 readings); 0.080 (S13f; S9 reading) | none | S2a (X; reader A only); S2b (X); S4b (E); S4c (X); S5 (X); S12a (P; no stellar mass for it); S12b (E; dash); S13f (P); S19 (P) | yes (S4b) |
| A3158 (X-COP) | not stated in A9 readings; 0.059 (S12a); 0.05947 (S1b) (S9 readings) | none | S1a (P); S1b (P); S2a (X; reader A only); S12a (P; no stellar mass for it); S12b (E; dash) | pending P (S1a; S1b) |
| A3266 (X-COP) | not stated in A9 readings; 0.0589 (S12a); 0.05915 (S1b); 0.0594 (S2b) (S9 readings) | none | S1a (P); S1b (P); S2a (X; reader A only); S2b (X); S12a (P; no stellar mass for it); S12b (E; dash) | pending P (S1a; S1b) |
| RXC1825 (X-COP) | not stated in A9 readings; 0.065 (S12a; S9 reading) | none | S12a (P; no stellar mass for it); S12b (E; dash) | no |

Notes on the table:
- **S12b is coded E but gives no stellar mass for any of the five X-COP clusters** (both readers). It is listed because it names them, and it is not counted as coverage.
- **"BCG only":** S8a is E for the BCG component only. Three clusters (A2261, A383, RX J2129) are "yes" only through S8a.
- **Name forms treated as the same cluster:** A478 = A0478 = Abell 0478; A209 = Abell 209; A383 = Abell 383; A2261 = Abell 2261; A1689 = Abell 1689; RXC1825 = RXC J1825. RX J2129.7+0005 = RXJ2129.6+0005 = RXJ2129+0005 is flagged above as uncertain.
- **Possible gaps in the "no" and "pending" verdicts.** Several S records hold cluster lists that the readers did not read by name: S1c (48 WINGS clusters), S4a (reader A did not read names), S7a (XXL), S9a (106 XCS), S9b (134 redMaPPer), S10b (91 SPT), S15a (132 clusters, including Abell), S15c (416 CODEX), S18c (COSMOS). Of these, S9a, S10b, S15a and S15c are E. A cluster marked "no" or "pending" could still appear in one of them.
- **Kind:** A2142's C28a reading (reader B) notes substructures, with merging status unverified; the source is not reported as calling it merging, so it is kept. S19's dataset title calls A2255 a "post-merger cluster". That is an S9 reading, not an A9 source, so A2255 stays because part C requires it. It is flagged for the A10 kind check.
- **Not listed because their A9 records are not E or E-pair:** A611, MS2137, A963, A2537, A2667 (C8a, C8c: P); A2465 (C13d: X, A10); MS 0440 (C13e: P); AS1063 (C17a, C17b, C27b: P); AC 114 (C17c: P).

## Exclusions

**By redshift (0.30 or above): 23 clusters** named in E/E-pair records:
MACS J0416 (0.396, C15f), MACS J0717 (0.55, C5e), MACS J0647 (0.59, C15c), MACS J1149 (no z in A9 readings; 0.544 in S8a, 0.543 in S14c), RX J2248 / AS1063 (0.35, C27b; named in C1a, reader A), MACS J1206 (0.439, C5b; 0.44, C5c/C27a), MACS J2129.4-0741 (0.589, C5f), MACS J0329, J0429, J1115, J1311 and RX J1347 (C4a: only RX J2129 is below 0.3; S8a also prints 0.450, 0.399, 0.352, 0.494, 0.451), MACS J1931.8-2635 (0.35, C19a), A370 (0.375, C10a), Cl0024+17 (0.395, C10a), SDSS J1446+3032, J1531+3414, J2111−0115 (C11c: only A1703 is below 0.3), A1351 and A1995 (0.32, C13b), MS1008.1-1224 (0.302, C13j), Cl J120958.9+495352 (0.902, C15b), SPT-CL J0546-5345 (1.07, C19b).
MACS J1149's exclusion rests only on the S9 redshift. RX J1347 is excluded both by the C4a statement and by S8a.

**By kind (A10): 0 additional.** The merging clusters that appear in E/E-pair records (A370, MACS J0416, MACS J0717, AS1063) are already excluded by redshift. A2465 appears only in an X record (C13d).

## Summary

| Count | Clusters |
|---|---|
| Clusters listed | **21** (16 from A9 E/E-pair records + 5 X-COP) |
| With E stellar coverage | **8**: A2261, A2142, Coma, A209, A383, RX J2129.7+0005, A2199, A2255 (for 3 of these, A2261, A383 and RX J2129, the only E record is the BCG-only S8a) |
| Pending only (P) | **4**: A1689, A1644, A3158, A3266 |
| None | **9**: A2390, Hydra A, A478, A1835, A1703, A2204, A2197, A194, RXC1825 |
| Excluded | 23 by redshift ≥ 0.30; 0 by kind alone |

## A9 E/E-pair records whose clusters could not be named (names not in the readings)

| Record (final code, row) | What the readings give |
|---|---|
| C1a (E, L) | 20 CLASH clusters, z 0.187–0.686, 5 below 0.3. Named in the row: MACS J0416, J1149, J0717, J0647 (all excluded by z) and RX J2248 (excluded). A209, A2261 and A383 are tied to C1a by notes in other rows; the other 2 of the 5 below 0.3 are not named. |
| C1b (E, L) | Same 20 clusters as C1a; same naming situation. |
| C1c (E, L) | 25 CLASH clusters, z range not transcribed; only MACS J0647 is tied to it (C15c). |
| C3a (E-pair, gas side) | 25 CLASH clusters (its Table 1); not named in the readings. A209, A2261, A383 and RX J2129 name it as their pairing. |
| C6a (E-pair, L) | 20 LoCuSS cluster cores, z 0.15–0.30; per-cluster z not transcribed. |
| C6b/C6c (E-pair, L) | 50 clusters, stacked, 0.15 < z < 0.3. |
| C6c/C6d (E-pair, L) | 50 LoCuSS clusters, 0.15 ≤ z ≤ 0.3. |
| C7a (E-pair, L) | 28 SGAS clusters; z range unverified. |
| C7b (E-pair, L) | 37 SGAS clusters; z range not transcribed. |
| C12d (E-pair, L) | 11 X-ray-luminous clusters, z 0.21 ± 0.04. |
| C12e (E-pair, L) | 7 400d clusters, z 0.39–0.94 (all excluded by z in any case). |
| C15a (E-pair, gas side; row O is X) | 14 CNOC clusters, 0.17 < z < 0.55. |
| C18c (E-pair, L) | 136 XXL groups and clusters, 0.031 ≤ z ≤ 1.033. |
| C18d (E-pair, L) | 39 APEX-SZ clusters, z 0.1–0.83 (reader B). |
| C20a (E, O) | 58 HeCS clusters, 0.1 < z < 0.3. |
| C20c (E, O) | 44 CHeCS clusters, 0.1 < z < 0.3. |
| C20d (E-pair, O) | 129 CIRS + HeCS clusters, 0.01 < z < 0.30. |
| C21a (E-pair, O) | 8 CAIRNS clusters; Coma and A2199 named (reader B note); 6 not named. |
| C21b (E-pair) | 9 systems (8 CAIRNS + A194); 6 CAIRNS clusters not named. |
| C22/C22a (E-pair, O) | 16 CNOC1 clusters, stacked; z range unverified. |
| C24a (E-pair, O) | 43 2dFGRS clusters, stacked; z range unverified. |
| C26/C26a (E-pair, O) | 54 WINGS clusters in 3 stacks; 0.04 < z < 0.07 (reader B). |
| C29a (E, O) | 22 eRASS1 clusters, z 0.077–0.768, 12 below 0.3. |
| C29b (E, O) | 75 CHEX-MATE clusters; 0.05 < z < 0.6 (tiers); number below 0.3 unverified. |

24 records in all.
