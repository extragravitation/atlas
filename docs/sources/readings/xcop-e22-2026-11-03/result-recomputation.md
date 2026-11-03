# Independent recomputation of X-COP v2 test part A, 2026-11-03

An independent agent wrote this report. It re-implemented A1–A5, A8 and A9 from the frozen test text, without seeing the Atlas's code or result. The report follows verbatim.

**Bottom line:** A1 fails, A2 fails (no variant passes for all five clusters, so none is selected), A4 fails (39 of 45), the A3 stage-2 condition fails, and the A8 stage-1 check fails for A3158. I wrote all the code from the test text alone. I did not open check_part_a.py, xcop2res/, a6probe/, ax/ or bx/.

**Test text used.** The local `origin/main` ref is out of date (it is still at #29), so I read the text at the remote main head `8cdbd4b`. Its SHA-256 is `c7c949a0…c4c1`, which matches `data/frozen/xcop-v2-part-a.json`. The file on disk is identical.

**Working files.** Data extracted to `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/indep_check/{a,b}`. My code is in `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/indep_check/code/check.py`. Constants (G, M☉, kpc) come from astropy. Cosmology: flat, H₀ 67.8, Ω_m 0.308.

## A1: FAIL
- **Archive hashes:** both SHA-256 values and byte sizes match §1.
- **Members and columns:** as listed in §1. The extension and column names in the FITS files match.
- **`gbar_gobs` row counts:** only A1795 has 21 rows. This is the failure.

| Cluster | Rows | RADIUS range (kpc) | RADIUS range (× Table 1 R500) |
|---|---|---|---|
| A644 | **19** | 64.2–1734.8 | 0.046–1.241 |
| A1795 | 21 | 57.3–2447.1 | 0.049–2.110 |
| A2029 | **22** | 69.3–2668.8 | 0.052–1.992 |
| A2142 | **20** | 48.1–2777.3 | 0.033–1.911 |
| A2319 | **27** | 90.9–2496.7 | 0.064–1.753 |

- **Units:** RADIUS is in kpc and all accelerations are in m/s² (from TUNIT).
- **Values:** every value is finite, and every GBAR and GOBS is positive.
- **Einasto files:** the five pairs across the two archives are byte-identical.

## A2: FAIL, no variant selected
Every row was testable in every variant.

| Variant | A644 median / max\|r−1\| | A1795 | A2029 | A2142 | A2319 |
|---|---|---|---|---|---|
| (a)(i) | 0.9528 / 0.291 ✗ | 0.9767 / 0.027 ✗ | 0.9772 / 0.025 ✗ | 0.9742 / 0.031 ✗ | 0.9720 / 0.031 ✗ |
| (a)(ii) | 0.9946 / 0.316 ✗ | 1.0198 / 0.035 ✓ | 1.0186 / 0.020 ✓ | 1.0139 / 0.016 ✓ | 1.0112 / 0.015 ✓ |
| (b)(i) | 0.9777 / 0.316 ✗ | 1.0002 / 0.0007 ✓ | 1.0002 / 0.0005 ✓ | 1.0001 / 0.0009 ✓ | 1.0002 / 0.0008 ✓ |
| (b)(ii) | 0.9970 / 0.322 ✗ | 1.0218 / 0.035 ✗ | 1.0210 / 0.023 ✗ | 1.0165 / 0.019 ✓ | 1.0128 / 0.015 ✓ |

- **What the table shows (reported only):** for four clusters, variant (b)(i) reproduces GBAR to within 0.1 %. A644 fails every variant.
- **A644 under (b)(i):** the ratio falls smoothly from 1.32 at 64 kpc to 0.96 at 1735 kpc. So A644's GBAR is not this file's gas plus stars.
- **Convention for later checks:** because nothing is selected, convention (a) (R_REF) is used from here on, as the text prescribes.

## R3/A5 (convention (a), Einasto MASS at R_REF)
Each density crossing was unique and inside the grid.

| Cluster | R2500 (kpc) | R500 (kpc) | R200 (kpc) | R500 / Table 1 R500,TOT |
|---|---|---|---|---|
| A644 | 644.1 | 1284.1 | 1811.0 | 0.919 |
| A1795 | 540.0 | 1147.0 | 1672.8 | 0.989 |
| A2029 | 633.9 | 1382.6 | 2047.8 | 1.032 |
| A2142 | 607.9 | 1492.5 | 2341.2 | 1.027 |
| A2319 | 666.1 | 1400.8 | 2018.0 | 0.984 |

## A4: FAIL, 39 of 45 within tolerance (24 within 0.1 percentage point)
- **FGAS units:** I read FGAS as a dimensionless fraction (values 0.06–0.25) and multiplied by 100. FGAS and 100·MGAS/MASS agree to about 0.01 percentage point at every R_Δ.
- **The six failures:**

| Cluster | Entry | Atlas (%) | Table 4 (%) | Difference |
|---|---|---|---|---|
| A644 | f_gas,2500 | 7.949 | 7.7±0.1 | +0.25 |
| A644 | f_gas,200 | 15.46 | 16.9±1.2 | −1.44 |
| A1795 | f_gas,2500 | 9.775 | 9.6±0.1 | +0.175 |
| A2319 | f_gas,2500 | 9.752 | 9.2±0.1 | +0.55 |
| A2319 | f_gas,200 | 23.70 | 24.9±0.5 | −1.20 |
| A2319 | f_bar,200 | 25.16 | 26.4±1.0 | −1.24 |

- **f★:** all 15 entries pass, each within 0.11 percentage point.
- **Reported variant at Table 1's R500,TOT:**

| Cluster | f_gas (%) | Table 4 f_gas,500 (%) |
|---|---|---|
| A644 | 12.97 | 12.8 |
| A1795 | 13.51 | 13.4 |
| A2029 | 14.49 | 14.4 |
| A2142 | 14.16 | 14.1 |
| A2319 | 17.33 | 17.0 |

## A3 stage-2 condition: FAIL
There are no rows with R_IN = 0 in the `GP_mass.fits` files. Every `gbar_gobs` row is testable.

| Cluster | Max δ | Total: rows (in range) | Total: median, median(a) | Total: result | Gas: rows (in range) | Gas: median, median(a) | Gas: result |
|---|---|---|---|---|---|---|---|
| A644 | **0.061** | 19 (18) | 0.989, 0.031 | pass | 18 (18) | 1.023, 0.031 | fail (A2; also rows: worst \|r−1\|−a = +0.21) |
| A1795 | **0.074** | 21 (19) | 0.988, 0.037 | pass | 19 (18) | 0.993, 0.036 | fail (A2; also rows: +0.015) |
| A2029 | **0.072** | 22 (22) | 0.983, 0.036 | pass | 18 (18) | 0.993, 0.033 | fail (A2 only) |
| A2142 | **0.087** | 20 (19) | 0.989, 0.034 | pass | 18 (18) | 1.001, 0.033 | fail (A2 only) |
| A2319 | **0.061** | 27 (27) | 0.983, 0.034 | pass | 22 (22) | 1.004, 0.031 | fail (A2 only) |

- **Total-mass part:** taken alone, every row is within 0.10 + a, and ratio_tot lies between 0.91 and 1.003.
- **Why the condition fails:** two things fail it independently.
  - Every cluster has δ > 0.05 on its innermost one to five testable rows.
  - A2 failed, so the gas part fails for every cluster by rule.
- **Gas numbers:** these used M_STAR at R_REF. They are reported only, because the gas part fails anyway.
- **Diagnostic, GOBS against the Einasto MASS:** median ratios 0.966–0.988, with max |r−1| between 0.15 (A644) and 0.34 (A2142).

## A8 stage 1: FAIL (A3158)
- **Rows:** all seven files have 200 rows and no R_IN = 0 rows.
- **Positivity:** MASS and MGAS are positive on every in-range row for A85, A1644, A2255, A3266, RXC1825 and ZW1215.
- **A3158 fails:** MASS is negative on rows 12–17 (0-based). Their midpoints are 17.9–30.5 kpc (0.016–0.027 R500), and MASS runs from −7.1×10¹⁰ to −2.6×10¹¹ M☉. MGAS is positive on those rows.
- **Reported only, outward MASS decreases inside the range:**

| Cluster | A85 | A1644 | A2255 | A3158 | A3266 | RXC1825 | ZW1215 |
|---|---|---|---|---|---|---|---|
| Rows | 0 | 32 | 24 | 13 | 8 | 0 | 19 |

  There are no outward MGAS decreases.
- **Reported only, max |FGAS − MGAS/MASS|:** up to 0.36 (A3158), 0.19 (ZW1215) and 0.16 (A2255).
- **Outside the source range (no effect on the check):** the five complete clusters' `GP_mass.fits` also have negative MASS below about 15 kpc. A1795's last row has MGAS greater than MASS.

## A9 (R500 from R3, convention (a))

| Cluster | M_STAR(<R500) (M☉) | Ratio to Ghizzardi M★,500 |
|---|---|---|
| A644 | 7.55×10¹² | 2.04 |
| A1795 | 5.60×10¹² | 1.86 |
| A2029 | 1.58×10¹³ | 2.42 |
| A2142 | 1.58×10¹³ | 2.27 |
| A2319 | 1.15×10¹³ | 2.25 |

## Choices where the text left an option open
1. **Interpolation:** linear in log y against log r for every quantity, including FGAS and M_STAR. At R_Δ, f★ is the interpolated M_STAR divided by the interpolated MASS. A value is untestable if it falls outside the grid or either bracketing value is ≤ 0. This never happened at any tested radius.
2. **A2 testable rows:** a RADIUS inside both files' label grids.
3. **A3 usable midpoint:** any row with R_IN > 0. The δ > 0.05 rule is read as failing the whole condition. Both medians use Table 1 R500 × [0.05, 2], inclusive.
4. **A3 gas without an A2 selection:** M_STAR at R_REF (convention (a)), for reporting only.
5. **A8 "inside the range":** a row whose midpoint lies in [0.01, 2] × Table 1 R500,TOT, inclusive.
6. **A4 tolerance:** quoted error + 0.05 percentage point for all three quantities, with a tiny floating-point allowance at the boundary.

## Not done
- A6 was skipped as instructed, so the Sérsic-subtracted A9 variant was not computed.
- The A7 ratios were not computed.
- The `_BCG.txt` files were not opened.

**Next step:** compare these numbers line by line with the original run. The first things to reconcile are the A1 row counts, the A644 failure in A2, and A3158's negative-mass rows.