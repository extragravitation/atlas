# Adjudication log: aeg-d-dwarfs/v1 sigma readings, 38 disputed pairs

Adjudicated 2026-10-30 against `reading/SIGMA_READING_BRIEF.md`. Each disputed number was checked in the paper on the sheet, at the cited location. Figure labels were checked as page images. Only the 38 pairs' PDFs were opened. Nothing was computed. Output: `adjudicated.csv`, 245 rows.

## Conventions applied (clarifications of the brief)

1. `limit_level` is the level as printed, in short form: "95%", "99.5%", "68%", "90th percentile", "95th percentile", "2σ", "98.3%". It is "not stated" when a limit has no printed level.
2. `limit` is `upper` or `lower` as printed. A printed lower bound is recorded as `lower`.
3. A value printed as "0.0" with errors is a value, not a limit.
4. Printed digits are kept exactly. A quantity printed with different digits in two places gets two rows (brief rule 1). The same digits printed in several places give one row listing every location, including when a later mention drops the uncertainty.
5. Predictions, assumed values and simulation outputs printed as values for the system are recorded and labelled in `estimator`. Inputs to mock tests are left out.
6. When one printed number is stated to hold for two estimators (e.g. "in both models"), each estimator gets its own row, because the brief lists with and without a gradient as separate values. When the same digits are printed for differently described samples and the paper does not say they are one value, each gets its own row.
7. Binned-profile values are recorded, with the bin named in `sample`.
8. Geha 2026 arXiv 2602.10202 Table A1 col. (15) prints no level. The method text defines unresolved limits as "the 95th percentile of the posterior distribution", so the level is "95th percentile". Geha 2026 ApJ 999 140 Table A1 note (17) prints "upper 95% confidence limit", so the level is "95%".
9. Rows the readers agreed on (after normalisation) were not re-checked. Their `checked_page` is blank.

## Per pair

| # | Pair | What differed | What the paper shows | Resolution |
|---|---|---|---|---|
| 0 | andromeda_11, Tollerud 2012 | r1 blank row; r2 0.0 ± 3.7 | Fig. 14(c), p19, prints σ_LOS = 0.0 ± 3.7; Table 3 prints "···" | r2 row; blank row dropped. r1 wrong |
| 1 | andromeda_12, Tollerud 2012 | r1 blank row; r2 1.0 ± 11.0 | Fig. 15(c), p20, prints σ_LOS = 1.0 ± 11.0 | r2 row. r1 wrong |
| 2 | andromeda_19, Collins 2020 | r1 has 7.79 +1.73 −1.52 | Fig. 6, p8, prints it once (differs from 7.8 in text) | Keep. r2 wrong |
| 3 | andromeda_22, Chapman 2013 | Level wording only | "99.5% confidence" (p4, p6); "95% confidence" (p5) | Normalised. Formatting only |
| 4 | andromeda_22, Tollerud 2012 | r2 has 3.5 +4.2 −2.5 | Fig. 23(c), p28, prints it (differs from Table 3, 3.54) | Keep. r1 wrong |
| 5 | aquarius_3, Cerny 2025 | r1 has 3.51 and 1.61; level wording | Fig. 4, p11, prints "σv < 1.61 (68% u.l.)" and "< 3.51 (95% u.l.)" | Keep both; levels normalised. r2 wrong |
| 6 | aquarius_3, Geha 2602.10202 | "95th percentile" vs "95%" | Table A1, p17; method p4: "95th percentile of the posterior" | "95th percentile". Formatting only |
| 7 | bootes_1, Sandford 2026 | r2 has 5.1 (no error), ~10 and ~4 | p2 prints σv = 5.1 (J21, same digits as the p16 value); p18 prints "(∼10 vs. ∼4 km s−1)" for L22 bins | 5.1 merged into the J21 row; ~10 and ~4 kept. r1 wrong (2 missed), r2 wrong (duplicate row) |
| 8 | bootes_2, Geha ApJ 999 | r1 has 1.9 +0.8 −0.6 | Sect. 9.2, p27, prints it (Table A1 has 1.92) | Keep. r2 wrong |
| 9 | bootes_3, Li 2026 | r1 has 1.7, 2.12, 3.52, 5.64 | p27 prints σv = 1.7; p17 prints simulated σv for three halo masses | Keep all four (simulation outputs labelled). r2 wrong |
| 10 | canes_venatici_1, Geha ApJ 999 | r1 has 7.7 ± 0.4 | Fig. 16, p23, prints σv = 7.7 ± 0.4 | Keep. r2 wrong |
| 11 | carina_1, Munoz 2006 | r1 has 10.2 | Sect. 3.2, p5, prints σ = 10.2 for stars beyond 0.6 r_lim | Keep. r2 wrong |
| 12 | draco_2, Cerny 2026 | Level wording only | "95% credible level", p38 and p49 | "95%". Formatting only |
| 13 | draco_2, Geha ApJ 999 | r1 has < 2.6 | Sect. 9.2, p27, and Fig. 16, p23, print < 2.6 with no level (Table A1 has 2.64) | Keep, level "not stated". r2 wrong |
| 14 | draco_2, Geha 2602.10202 | "95th percentile" vs "95%" | As #6 | "95th percentile". Formatting only |
| 15 | eridanus_2, Li 2017 | r2 has 7.0 +1.2 −1.0 | Fig. 7, p9 (gradient model), prints it | Keep. r1 wrong |
| 16 | grus_1, Chiti 2022 | Level "not stated" vs blank | p14: < 9.8 with no level | "not stated". Formatting only |
| 17 | hercules_1, Ou 2024 | r2 splits 6.0 into two rows; r2 has 8.0 +1.4 −2.0 | 6.0 is printed for the CF sample (p10) and for the wider velocity window (p14, p20); p20 prints Longeard 8.0 | Two 6.0 rows plus 8.0. r1 wrong |
| 18 | hydra_2, Geha 2602.10202 | As #6 | As #6 | "95th percentile". Formatting only |
| 19 | hydrus_1, Koposov 2018 | r1 has 2.7 | Abstract (p1) and Sect. 6 (p18) print 2.7 (Table 1 has 2.69) | Keep. r2 wrong |
| 20 | leo_1, Mateo 2008 | r2 has ~9 | Sect. 4.1, p14, prints "(∼ 9 km/s)" | Keep. r1 wrong |
| 21 | leo_5, Jenkins 2021 | r2 has 2.3 +3.2 −1.6 twice | Same digits, same Collins 2017 value, on p2, p17, p21 | One row. r2 wrong |
| 22 | pegasus_3, Kim 2016 | Level "not stated" vs blank | p8: < 0.3 with no level | "not stated". Formatting only |
| 23 | reticulum_2, Minor 2019 | r1 has ~3 | p6 prints "apparent velocity dispersion of ∼ 3 km/s"; the same page also prints "most probable intrinsic dispersion of 3 km/s" | Keep r1 row (location corrected to p6); add the second as an adjudicator row. r2 wrong; both readers missed the second |
| 24 | reticulum_3, Fritz 2019 | Level wording only | Table 3 caption, p12: "90-th percentile of the pPDFs" | "90th percentile". Formatting only |
| 25 | sagittarius_1, Frinchaboy 2012 | r1 9.6 ± 0.4; r2 9.60 ± 0.40 | 9.6 ± 0.4 on p3, p14, p28; 9.60 ± 0.40 on p8 | Two rows. Both wrong (each kept one) |
| 26 | segue_1, Martinez 2011 | r1 has lower bound 1 (98.3%) | Sect. 7, p14: "larger than 1 km s−1 at the 98.3% confidence level" | Keep, `lower`. r2 wrong |
| 27 | segue_2, Geha 2602.10202 | As #6 | Table A1, p18 | "95th percentile". Formatting only |
| 28 | segue_2, Kirby 2013 | r2 has 0.5 | Sect. 1, p2: expected dispersion without dark matter, 0.5 | Keep, labelled as prediction. r1 wrong |
| 29 | sextans_1, Battaglia 2011 | r1 has 7.6 ± 1.1 and 8.6 ± 1.4 | Sect. 5, p11, prints both | Keep. r2 wrong |
| 30 | sextans_1, Tolstoy 2025 | r1 has two 8.3 rows, r2 one | p12: 8.3 +0.3 −0.3 "in both models" (with and without gradient) | Two rows. r2 wrong |
| 31 | triangulum_2, Buttry 2022 | r1 has 1.6 and 4 | p9–10: posterior peak at σv = 1.6; p4: "we use σ_TriII = 4 km s−1" | Keep both, labelled. r2 wrong |
| 32 | triangulum_2, Kirby 2017 | r1 has 9.1 +3.9 −2.0 | Sect. 3.4, p7, prints it | Keep. r2 wrong |
| 33 | tucana_1, Gregory 2019 | r1 has 14.35 +2.78 −2.32 | Fig. 5, p7, prints it | Keep. r2 wrong |
| 34 | tucana_1, Taibi 2020 | r1 has 21 and ~15 | Sect. 5, p8, prints both | Keep. r2 wrong |
| 35 | tucana_4, Simon 2020 | `limit` lower vs blank | p8: "at 2σ … larger than 2.7 km s−1" | `lower`, "2σ". Formatting only |
| 36 | ursa_major_1, Simon 2007 | Level "not stated" vs blank | p12: σ < 3.4 with no level | "not stated". Formatting only |
| 37 | willman_1, Chiu 2026 | r1 has 4.74 +1.49 −1.34 | Fig. 4, p9 (enlarged), prints it | Keep. r2 wrong |

## Counts

Difference instances, by kind:

| Kind | Instances | Pairs |
|---|---|---|
| Formatting only (level wording or limit column) | 15 | 12 (11 formatting-only, plus pair 5) |
| Duplicate printing with different digits, one printing missed | 13 | 11 |
| Same digits: merged vs split, or recorded twice | 4 | 4 (pairs 7, 17, 21, 30) |
| Value missed by one reader | 21 (r1 7, r2 14) | 15 |
| Misread digit | 0 | 0 |
| Value missed by both (adjudicator addition) | 1 | 1 (pair 23) |

Pairs where each reader's set of numbers was wrong in substance (formatting excluded):

- r1 wrong in 9 of 38 pairs: 0, 1, 4, 7, 15, 17, 20, 25, 28.
- r2 wrong in 20 of 38 pairs: 2, 5, 7, 8, 9, 10, 11, 13, 19, 21, 23, 25, 26, 29, 30, 31, 32, 33, 34, 37.
- Both wrong in 2 pairs: 7 and 25. Pair 23's adjudicator row is not counted against either reader.
- r1 right in substance in 29 pairs; r2 right in substance in 18 pairs.

Row-level errors: r1 11 (7 missed values, 3 missed duplicate printings, 1 merge); r2 27 (14 missed values, 10 missed duplicate printings, 3 same-digit handling).

Formatting-only pairs, by which reader's form matched the normalised form: r1 in 8 (6, 14, 16, 18, 22, 27, 35, 36), r2 in 2 (3, 12), and neither in 1 (24). In pair 5, r2's level form matched.

Unresolved pairs: none.
