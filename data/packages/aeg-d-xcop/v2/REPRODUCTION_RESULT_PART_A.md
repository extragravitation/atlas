# aeg-d-xcop/v2: reproduction test, part A — result

**Run** 2026-11-03, after the test was frozen (#128 merged as `777fece`; test SHA-256 `c7c949a0…c4c1` recorded in `data/frozen/xcop-v2-part-a.json` by #131). The archives' values were first read after that.

**Code:** `check_part_a.py` in this folder, run on the two archives listed in the test (§1). Machine-readable result: `result_part_a.json` (check outcomes, ratios and fitted parameters; no source rows, per D-090 rule 5). Implementation choices that the test text leaves open are listed in the JSON (`implementation_notes`) and below.

**Independent check:** an independent agent re-implemented A1–A5, A8 and A9 from the test text alone, without seeing this code or this result. Its report is `docs/sources/readings/xcop-e22-2026-11-03/result-recomputation.md`; agreement is stated in the last section.

**The test is not changed after this result (operating rule 5).**

## Summary

| Check | Kind | Outcome |
|---|---|---|
| A1 Completeness and structure | pass/fail | **Fail.** Row counts of four `gbar_gobs` files differ from the test's "exactly 21" (the test's error; see below). Everything else passes. |
| A2 g_bar = gas + file's stars | pass/fail | **Fail.** No variant passes for all five clusters. Variant (b)(i) reproduces four clusters to 0.1 %; A644 deviates by up to 32 % in every variant. |
| A3 stage-2 condition | pass/fail | **Fail.** The `GP_mass.fits` grid is too coarse (δ > 0.05) at the innermost 1–3 testable rows of every cluster. The gas part also fails because A2 failed. |
| A4 Table 4 | pass/fail | **Fail.** 39 of 45 entries within tolerance (convention (a), as the rule requires when A2 selects none). |
| A5 R500 | reported | Ratios to Table 1: 0.92 to 1.03. |
| A6 Stellar functional form | decision rule | **Undetermined.** Neither model reproduces M_STAR to the 10⁻³ required; rms 2.7×10⁻³ to 3.2×10⁻². |
| A7 Model dependence | reported | GP/Einasto at R500: 0.97 to 1.04. |
| A8 Stage-1 checks | pass/fail | **Fail.** A3158 has negative total mass at 6 rows inside the inferred source range. The other six pass. |
| A9 Stellar normalisation | reported | 1.86 to 2.42 against Ghizzardi's spherical M★,500. |

**Consequences, by the frozen rules:**
- **R2 (units):** not accepted, because A4 failed. The units question goes to the authors; no other units are tried.
- **R1 convention downstream:** (a), because A2 selected none.
- **A8 stage 2 (#129) is blocked**, by A3 and by A8's stage-1 check. The questions go to the authors; any change is a JvH ruling; the checks and thresholds are never changed.
- **v2's plotted rows** are the source's own `gbar_gobs` values (§5), which no check modifies. Their publication still waits for the authors' consent (D-090 rule 5).

## A1. Completeness and structure — fail

- Archive SHA-256: both match §1.
- Members: both archives match §1 exactly. Member SHA-256 values are in the JSON.
- Units: RADIUS in kpc, accelerations in m/s², as listed.
- All GBAR, GOBS and error values are finite; GBAR and GOBS are positive.
- The Einasto files are byte-identical across the two archives.
- **Row counts:** A644 19, A1795 21, A2029 22, A2142 20, A2319 27 (109 rows in all). The test says each file has "exactly 21 rows".

**This failure is the test's error, not the source's.** Before freezing, the FITS row counts were seen (test §1, l. 10), but the test generalised one file's count to all five. §5's "105 rows" is wrong for the same reason: the five files hold 109. The intent of §5 is "the rows of the five `gbar_gobs` files"; the count is recorded here as a correction and is not edited into the frozen text.

## A2. Is g_bar gas plus the file's stars? — fail

Median ratio GBAR / [G (gas + M_STAR)/r²], and max |ratio − 1|, per variant:

| Cluster | (a)(i) | (a)(ii) | (b)(i) | (b)(ii) |
|---|---|---|---|---|
| A644 | 0.953, 0.29 | 0.995, 0.32 | 0.978, 0.32 | 0.997, 0.32 |
| A1795 | 0.977, 0.027 | 1.020, 0.035 | **1.0002, 0.0007** | 1.022, 0.035 |
| A2029 | 0.977, 0.025 | 1.019, 0.020 | **1.0002, 0.0005** | 1.021, 0.023 |
| A2142 | 0.974, 0.031 | 1.014, 0.016 | **1.0001, 0.0009** | 1.017, 0.019 |
| A2319 | 0.972, 0.031 | 1.011, 0.015 | **1.0002, 0.0008** | 1.013, 0.015 |

- **What is established:** for A1795, A2029, A2142 and A2319, GBAR is the Einasto file's gas plus its M_STAR, read at R_OUT, to better than 0.1 % on every row.
- **What fails:** for A644, the ratio runs smoothly from 1.32 at the innermost row to 0.96 at the outermost, in every variant. A644's GBAR was not built from the shared Einasto file's gas and stars. The reading of Paper II infers A644 among the clusters it leaves out of some analyses (readings §3b); this is noted, not used as an explanation. **Question for the authors.**

## A3. Stage-2 condition — fail

- **Grid step.** `GP_mass.fits` radii are close to linearly spaced, so ln(R_OUT/R_IN) falls from 0.49 at the first rows to 0.01 at the last. Testable rows with δ > 0.05: A644 1 of 19, A1795 3 of 21, A2029 3 of 22, A2142 3 of 20, A2319 2 of 27; the largest is 0.087 (A2142). By l. 145, the condition fails.
- **Gas part:** fails for every cluster because A2 failed (l. 151).
- **Total-mass part, as computed:** every cluster meets both the median and the per-row criterion. Medians over 0.05–2 R500: A644 0.989, A1795 0.988, A2029 0.983, A2142 0.989, A2319 0.983; largest |ratio − 1| 0.089.
- **Gas part, as computed** (it fails by rule, reported for the authors): medians 0.99 to 1.02; A644 has 3 rows outside 0.10 + a (largest 0.28), the others none.
- **Einasto diagnostic** (GOBS against the Einasto file's MASS): medians 0.966 to 0.988; largest |ratio − 1| 0.15 to 0.34.
- **RADIUS ranges** in units of Table 1's R500: A644 0.046–1.24, A1795 0.049–2.11, A2029 0.052–1.99, A2142 0.033–1.91, A2319 0.064–1.75.

**The rule's effect, stated once.** l. 145 fails the whole condition when any testable row is too coarse, rather than setting those rows aside. It was written that way before the data were seen and is not changed.

## A4. Table 4 — fail (39 of 45)

Convention (a). FGAS values are all ≤ 1 and are read as fractions (×100). Entries outside tolerance (Atlas against Table 4 ± error):

| Cluster | Entry | Atlas | Table 4 |
|---|---|---|---|
| A644 | f_gas,2500 | 7.95 | 7.7 ± 0.1 |
| A644 | f_gas,200 | 15.46 | 16.9 ± 1.2 |
| A1795 | f_gas,2500 | 9.78 | 9.6 ± 0.1 |
| A2319 | f_gas,2500 | 9.75 | 9.2 ± 0.1 |
| A2319 | f_gas,200 | 23.70 | 24.9 ± 0.5 |
| A2319 | f_bar,200 | 25.16 | 26.4 ± 1.0 |

All other entries, including all 15 f★ entries, are within tolerance. Full values, the MGAS/MASS secondary estimates and the Table 1 R500 variant are in the JSON.

## A5. R500 — reported

R500 from the Einasto MASS (R3), against Table 1: A644 1284 / 1398 (0.919), A1795 1147 / 1160 (0.989), A2029 1383 / 1340 (1.032), A2142 1493 / 1453 (1.027), A2319 1401 / 1424 (0.984) kpc.

## A6. Functional form of the stellar mass — undetermined

| Cluster | rms(3D), rms(2D) at (0.64, 1.63) | at (0.72, 1.64) | Fitted R200 (3D) / Table 1 R200 |
|---|---|---|---|
| A644 | 2.6×10⁻², 3.1×10⁻² | 2.6×10⁻², 3.2×10⁻² | 615 / 2125 kpc |
| A1795 | 8.1×10⁻³, 1.1×10⁻² | 8.2×10⁻³, 1.1×10⁻² | 190 / 1746 kpc |
| A2029 | 1.4×10⁻², 1.8×10⁻² | 1.5×10⁻², 1.9×10⁻² | 412 / 2006 kpc |
| A2142 | 1.9×10⁻², 2.4×10⁻² | 2.0×10⁻², 2.5×10⁻² | 816 / 2253 kpc |
| A2319 | 2.7×10⁻³, 3.9×10⁻³ | 2.8×10⁻³, 4.0×10⁻³ | 229 / 2176 kpc |

- No fit reaches 10⁻³, so every verdict is "undetermined", and so is the overall verdict. The question goes to the authors (#124).
- A global optimiser (differential evolution) on A2319 and A1795 found the same minima. The residuals alternate in sign from row to row, so M_STAR is not the smooth model output the test assumed (l. 176).
- The fitted satellite R200 values are 4–9 times smaller than Table 1's, so the fitted forms do not describe the satellites as the test framed them.

## A7. Model dependence of the total mass — reported

At R500 from R3: GP/Einasto 1.033, 0.969, 1.042, 0.986, 0.994 (A644, A1795, A2029, A2142, A2319). Against Table 1's M500 (at Table 1's R500): GP 0.80, 0.94, 1.15, 1.07, 0.95; Einasto 0.78, 0.97, 1.10, 1.09, 0.95. These become the system-scale "choice of mass model" term in Part B. They are never applied as a correction.

## A8. Stage-1 checks — fail (A3158)

- All seven files have 200 rows.
- **A3158:** MASS is negative at rows 12–17 (midpoints 17.9–30.5 kpc, 0.016–0.027 × R500), inside the inferred 0.01–2 R500 range. MGAS is positive there. **Question for the authors**, together with the source range itself.
- The other six pass.
- **Reported only:**
  - outward decreases of MASS inside the range: A85 0, A1644 32, A2255 24, A3158 13, A3266 8, RXC1825 0, ZW1215 19 rows; MGAS: none;
  - |FGAS − MGAS/MASS| over all 200 rows: median below 2×10⁻⁴ in every cluster; maxima from 0.09 to 33 occur where MASS is near zero, outside the inferred range. Inside it, the maxima are at most 0.36 (A3158), per the independent recomputation.
  - Outside the range (no effect on the check): the five complete clusters' `GP_mass.fits` also have negative MASS below about 15 kpc, and A1795's last row has MGAS greater than MASS.
- Midpoint ranges run from about 0.001 to 2.0–2.9 × R500, so every file extends beyond 0.01–2 R500 on both sides.

## A9. Stellar normalisation — reported

M_STAR(<R500) / Ghizzardi M★,500: A644 2.04, A1795 1.86, A2029 2.42, A2142 2.27, A2319 2.25. With the fitted Sérsic term removed: 1.51 to 2.05, nearly the same for every fit. The pre-stated expectations were about 1 (spherical, same basis) and about 1.33 (projected). The tension stated before the run (1.9–2.7, from the published tables) is confirmed in the files. Never used to correct anything; flagged to the authors with #124.

## Exploratory, not the test's outcome

These were run after the result above, to help the authors' questions. They change nothing.
- **A4 under convention (b),** the one A2 shows to be right for four clusters: A1795, A2029 and A2142 reproduce all nine Table 4 entries; A644 misses 3 and A2319 misses 4 (38 of 45 overall).
- So the A4 misses concentrate in A644 and A2319, the two clusters with source caveats (A644 in A2 above; A2319's hydrostatic caveat, E22 l. 435, l. 502).

## Agreement with the independent recomputation

The independent recomputation (`result-recomputation.md`) agrees on every outcome: A1, A2, A3, A4 and A8 fail for the same reasons; the A2 variant table, R_Δ, A5, the six A4 misses, the A3 medians and maximum δ, A3158's rows 12–17 and the A9 ratios agree to the digits printed. It did not run A6 or A7.
- Its A3 gas column reports max(|ratio − 1| − a), not the margin against 0.10 + a. Read that way, its A1795 "+0.015" is within the per-row criterion, as here; A644's +0.21 exceeds it, as here (3 rows).
- Its |FGAS − MGAS/MASS| maxima are inside the source range; this file's were over all rows. Both are now stated.

## What this establishes, and what it does not

**Established:**
- The archives and members are as recorded, and the Einasto files are identical in both.
- For A1795, A2029, A2142 and A2319, the released g_bar is the Einasto file's gas plus its M_STAR, at R_OUT.
- The 2021 non-parametric total masses agree with GOBS for all five clusters within the test's total-mass thresholds, as computed.
- The stellar masses in the files are about twice Ghizzardi's spherical values at R500.

**Not established:**
- How A644's GBAR was built.
- The units and R_Δ definition behind Table 4 (R2 not accepted).
- The functional form, and the projection, of the stellar term.
- Anything about plotting the seven clusters, which stays blocked.

## Questions for the authors (batched with the "v2 is up" note)

1. A644: which gas and stellar profiles give the released GBAR?
2. Table 4: which R_Δ and which mass profile were used?
3. M_STAR: how was it computed, and is it a sphere or a cylinder?
4. The normalisation against Ghizzardi et al. 2021 (A9).
5. A3158: the negative masses at 18–30 kpc; and the valid radial range of each `GP_mass.fits`.
6. The confidence level of the released errors.

## Implementation choices (the test leaves these open)

As listed in `implementation_notes` in the JSON:
- log–log interpolation uses only rows with r > 0 and a positive quantity;
- FGAS read as a fraction because every value is ≤ 1;
- A6 used 12 starting points per model with stated bounds, and b_n from Ciotti & Bertin 1999;
- the 2D gNFW mass is tabulated numerically;
- A8 "inside the source's range" uses midpoints.

None of these changes a pass/fail outcome above, except possibly A6, which is cross-checked with a global optimiser.
