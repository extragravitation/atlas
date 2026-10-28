# aeg-d-xcop/v1 — reproduction result

**Result: FAILED** for 3 of 12 clusters (first run, 2026-10-28). `REPRODUCTION.md` (SHA-256 `a49cb132…`) unchanged. Conversion integrity passes exactly, so the package may ship under D-019 with the affected rows flagged (known issue #19).

| Check | Outcome |
|---|---|
| Frozen-file hash | pass |
| 1. Coverage: exactly the 12 clusters; stellar profiles for exactly A85, A644, A1795, A2029, A2142, A2319, ZW1215 | pass |
| 2. Archive NFW mass at 0.5, 1 and 1.5 Mpc within 1.5 % of Table 1 (36 checks) | **31 pass, 5 fail** (A644 at all three radii; A2319 at 1 and 1.5 Mpc) |
| 3a. Archive NFW mass at Table 1 R500 within 1.5 % of M500 (12 checks) | **10 pass, 2 fail** (A644, A2319) |
| 3b. Gas file's NFW mass at R/R500 = 1 within 1.5 % of M500 (12 checks) | **9 pass, 3 fail** (A644, A2029, A2319) |
| 4. Conversion integrity, 1 065 rows, relative 1e-9, recomputed from the archive independently of `convert.py` | pass |

## Numbers: archive relative to Ettori et al. 2019 Table 1 (%)

| Cluster | NFW at 0.5 Mpc | 1 Mpc | 1.5 Mpc | NFW at R500 vs M500 | Gas file at R/R500 = 1 vs M500 | Header R500 (kpc) vs Table 1 |
|---|---|---|---|---|---|---|
| A85 | +0.5 | +0.0 | +0.1 | −0.0 | −0.1 | 1235 = 1235 |
| **A644** | **+2.1** | **+3.4** | **+4.2** | **+3.5** | **+4.8** | **1250 vs 1230** |
| A1644 | +0.3 | +0.1 | +0.1 | +0.1 | +0.2 | 1054 = 1054 |
| A1795 | −0.1 | +0.1 | +0.1 | −0.0 | −0.0 | 1153 = 1153 |
| **A2029** | +0.1 | −0.8 | −1.4 | −1.4 | **−2.0** | **1414 vs 1423** |
| A2142 | −0.1 | −0.0 | −0.1 | −0.0 | −0.1 | 1424 = 1424 |
| A2255 | +0.5 | −0.0 | +0.2 | −0.1 | −0.2 | 1196 = 1196 |
| **A2319** | +1.2 | **+2.7** | **+3.8** | **+3.5** | **+5.0** | **1368 vs 1346** |
| A3158 | +0.4 | −0.1 | +0.0 | −0.0 | −0.1 | 1123 = 1123 |
| A3266 | +0.2 | +0.0 | −0.1 | −0.1 | −0.1 | 1430 = 1430 |
| RXC1825 | −0.0 | +0.0 | −0.0 | +0.1 | +0.2 | 1105 = 1105 |
| ZW1215 | +0.2 | +0.2 | +0.0 | +0.1 | +0.2 | 1358 = 1358 |

Nine clusters match within 0.5 %. The three that fail are exactly the three whose file headers carry an R500 different from Table 1's, and for each of them both the hydrostatic and the gas file agree with their own header R500 and M500 within 0.1 %. That points to a revised analysis in the archive for these clusters; this is a hypothesis, put to the X-COP team (issue #19).

**Handling (D-019).** The failing checks are kept unchanged as strict expected failures; a lock test requires that exactly these 10 fail and that the flagged rows are exactly every row of A644, A2029 and A2319 (264 rows, flag `reproduction_mismatch`, `known_issues = #19`). Gas radii are converted with each file's own header R500, so the converted values do not depend on which R500 is right; what is not established is that the archive's profiles for these clusters are the published ones.

## Reported, not pass/fail (as frozen)

Forward method relative to backward NFW, (M_forward / M_NFW − 1), median with 1st and 3rd quartiles over the archive's 12 clusters, against Ettori et al. 2019 Table 2 (13 clusters including Hydra A):

| Radius | Archive, 12 clusters | Table 2, 13 clusters |
|---|---|---|
| 0.5 Mpc | +3.6 % (+2.0 / +5.6) | +0.6 % (−1.1 / +3.3) |
| 1 Mpc | +0.4 % (−2.4 / +2.3) | −2.0 % (−5.9 / +1.4) |
| 1.5 Mpc | −1.9 % (−5.1 / +1.8) | −4.6 % (−7.9 / +1.3) |
| R500 (Table 1) | −2.3 % (−8.4 / +1.6) | −4.7 % (−10.9 / −0.5) |

The archive's medians sit 2.4 to 3.0 percentage points above Table 2's at every radius. Hydra A's absence and the three revised clusters may account for part of this; it cannot be resolved from the public files and is included in the question to the X-COP team. R200 was not computed (it would need a choice of method not specified in `REPRODUCTION.md`).
