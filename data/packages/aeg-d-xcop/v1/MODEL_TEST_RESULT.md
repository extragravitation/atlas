# aeg-d-xcop/v1 — result of the modelled-star test (D-023)

**Result: validated range r/R500 = 0.1445 to 1.3798** (first run, 2026-10-28). `MODEL_TEST.md` (SHA-256 `2283eba3…`, frozen at commit `0b4e304`) unchanged.

Applied to the 7 clusters with measured stars, the prescription reproduces their g_bar within 10 % (median absolute deviation) from 0.145 R500 outwards, to the last grid point covered by at least 5 clusters. Inside 0.145 R500 it fails, increasingly towards the centre (74 % at 0.027 R500), as expected from a profile that leaves out the central galaxy. Outside 0.2 R500 the median deviation is 4 % or less.

## Cut applied to the 5 modelled clusters

| Cluster | Rows kept | Rows removed | Innermost kept radius |
|---|---|---|---|
| A1644 | 49 | 38 | 153 kpc |
| A2255 | 49 | 42 | 176 kpc |
| A3158 | 48 | 44 | 168 kpc |
| A3266 | 44 | 41 | 212 kpc |
| RXC1825 | 49 | 39 | 160 kpc |

All removed rows lie inside 0.145 R500 or beyond 1.38 R500. The 7 clusters with measured stars are not cut. The package has 861 measurements.

## D(x): median over the covering clusters of |g_bar,model / g_bar − 1|

| r/R500 | Clusters covering | D (%) | Outcome |
|---|---|---|---|
| 0.0250 | 4 | — | not evaluated (fewer than 5 clusters) |
| 0.0272 | 7 | 74.4 | fail |
| 0.0295 | 7 | 71.5 | fail |
| 0.0321 | 7 | 68.4 | fail |
| 0.0349 | 7 | 65.2 | fail |
| 0.0380 | 7 | 61.7 | fail |
| 0.0413 | 7 | 58.0 | fail |
| 0.0449 | 7 | 54.2 | fail |
| 0.0488 | 7 | 50.3 | fail |
| 0.0530 | 7 | 46.5 | fail |
| 0.0577 | 7 | 42.7 | fail |
| 0.0627 | 7 | 39.0 | fail |
| 0.0681 | 7 | 35.6 | fail |
| 0.0741 | 7 | 32.4 | fail |
| 0.0805 | 7 | 29.1 | fail |
| 0.0876 | 7 | 26.0 | fail |
| 0.0952 | 7 | 22.4 | fail |
| 0.1035 | 7 | 18.3 | fail |
| 0.1125 | 7 | 16.4 | fail |
| 0.1223 | 7 | 14.7 | fail |
| 0.1330 | 7 | 12.7 | fail |
| 0.1445 | 7 | 9.9 | pass |
| 0.1571 | 7 | 7.7 | pass |
| 0.1708 | 7 | 6.1 | pass |
| 0.1857 | 7 | 4.9 | pass |
| 0.2019 | 7 | 4.0 | pass |
| 0.2195 | 7 | 3.8 | pass |
| 0.2386 | 7 | 3.5 | pass |
| 0.2594 | 7 | 2.7 | pass |
| 0.2820 | 7 | 1.7 | pass |
| 0.3066 | 7 | 2.0 | pass |
| 0.3333 | 7 | 1.6 | pass |
| 0.3624 | 7 | 1.1 | pass |
| 0.3940 | 7 | 1.4 | pass |
| 0.4283 | 7 | 1.9 | pass |
| 0.4656 | 7 | 2.0 | pass |
| 0.5062 | 7 | 2.0 | pass |
| 0.5503 | 7 | 1.6 | pass |
| 0.5983 | 7 | 1.5 | pass |
| 0.6504 | 7 | 1.3 | pass |
| 0.7071 | 7 | 1.1 | pass |
| 0.7687 | 7 | 1.5 | pass |
| 0.8357 | 7 | 2.0 | pass |
| 0.9086 | 7 | 2.2 | pass |
| 0.9878 | 7 | 2.0 | pass |
| 1.0738 | 6 | 2.0 | pass |
| 1.1674 | 6 | 2.3 | pass |
| 1.2692 | 5 | 1.7 | pass |
| 1.3798 | 5 | 1.6 | pass |
| 1.5000 | 4 | — | not evaluated (fewer than 5 clusters) |

**Recomputed independently** of `convert.py` by `tests/test_model_test.py` (from the package tables and the archive's gas files); the test also checks that every modelled row lies inside the range and that the measured clusters are uncut.

**What this does not show.** The test is on clusters with measured stars, which are not the same clusters; it shows the prescription works on average for this sample, not for each modelled cluster. Inside the range, the modelled clusters still carry no stellar uncertainty in g_bar, and no slider (D-022).
