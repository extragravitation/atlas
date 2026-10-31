# Adjudication log: aeg-d-dwarfs/v1 second-reading disagreements

Every disagreement was settled on the page image (Read with `pages`; 300 dpi crops for Fornax Table 6 and LGS 3 Table 7). No value was decided by plausibility. Agreed rows were carried over from Reading 1 without re-checking unless they were on a page already open.

## Pairs

1. draco_1 / Armandroff 1995: "about 10 km s-1" (Aaronson & Olszewski 1987, 1988) is printed on p.2131. Added; R2 omitted it. 5 rows.
2. fornax_1 / Mateo 1991: Table 6 (p.920) prints sigma_BW and sigma_W for rejection iterations 1 to 4. All 8 are recorded and labelled INTERMEDIATE; R1 recorded only iteration 4. Table 9 fits are labelled MODEL FIT, and the Table 11 (p.923) locations are added to the 10.5 ± 2.0 and 13.7 ± 2.3 rows. 20 rows.
3. leo_2 / Vogt 1995: values agree. The confidence level of the 9.3 limit is not printed (pp.152, 158), so `limit_level` is blank with a note. R1 wrote "not stated": a format deviation. 3 rows.
4. m_032 / Bender 1996: Fig. 3 caption (p.L126) prints sigma = 85 km s-1, a Gaussian fit to the LOSVD core. Added and labelled MODEL FIT; R2 omitted it. 36 rows.
5. sextans_1 / Suntzeff 1993: the Summary (p.225) prints 6.2 ± 2.6 for each metallicity group. Added; R2 omitted it. R2's v_s = 7.4 ± 1.2 (p.224) is excluded because the paper calls it a King-model "scale" velocity and says it "does not use the observed velocity dispersion". This is a judgment; R2 is counted with 1 inclusion error. Both readers missed "the observed value of 6 km s-1" (p.224), which is added. 12 rows.
6. ursa_minor_1 / Armandroff 1995: "about 10 km s-1" on p.2131. Added; R2 omitted it. 8 rows.
7. lgs_3 magnitude / Lee 1995: A_R = 0.07 and A_I = 0.05 are printed on p.1130. Added; R2 omitted them. Both readers missed the 7 smaller-aperture V values in Table 7 (p.1136), which are added. 16 rows.
8. phoenix_1 magnitude / van de Rydt 1991: E(V-I) = 0.027 is printed on p.133 and gets its own row. R2 had it only in a note. 8 rows.

## Error counts (value errors; shared omissions counted separately)

| Reader | Omissions | Wrong inclusions | Format deviations | Total own errors |
|---|---|---|---|---|
| Reading 1 | 6 (Fornax Table 6, iterations 1 to 3) | 0 | 1 (Leo II limit_level) | 6 + 1 format |
| Reading 2 | 7 (Draco 1, UMi 1, M32 1, Sextans 1, LGS 3 2, Phoenix 1) | 1 (Sextans v_s) | 0 | 8 |
| Both (shared) | 8 (Sextans "6" 1; LGS 3 Table 7 V 7) | 0 | 0 | 8 |

## Judgment calls for JvH's review

- Same digits from different estimators (Fornax iteration 3: sigma_BW = sigma_W = 12.5) are kept as 2 rows. The "one row per same digits" rule was applied only to the same value reprinted.
- M32: the "central" 92 ± 5 (abstract, Sec. 3) and the Table 1 value at r = -0.23 (92 ± 5) are kept as 2 rows, because the paper does not identify them as one value.
- Excluded as not measured dispersions of the system: Fornax Table 8 mu_int^2 in (km/s)^2; Leo II predictions of 7 to 15 and 2.5 km s-1 (p.152); Sextans Table 10 simulated sigma_obs and the 2.1 km s-1 simulation input; M32 "sigma ~ 150-200 km s-1" model threshold; Sextans and Fornax v_s.
