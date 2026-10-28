# aeg-d-xcop/v1 — reproduction test (frozen before conversion)

Written 2026-10-28, **before `convert.py` exists**. Disclosure: on 2026-10-28 the archive was opened to list its contents and read the column headers of three files (`A1795_hydro_mass.fits`, `A1795_mstar.fits`, `A1795_fgas_profile.fits`); no profile values were read. The reference numbers below are transcribed from Ettori et al. 2019 (A&A 621, A39; arXiv:1805.00035), Table 1, read at source the same day. This file's SHA-256 is recorded in `sources.json`. Failures are handled under D-019; the test is not changed to pass.

## Reference: Ettori et al. 2019, Table 1 (backward method, NFW model; units 10¹⁴ M☉ and Mpc)

| Cluster | M(<0.5 Mpc) | M(<1 Mpc) | M(<1.5 Mpc) | R500 | M500 |
|---|---|---|---|---|---|
| A85 | 1.94 ± 0.02 | 4.53 ± 0.08 | 6.81 ± 0.18 | 1.235 ± 0.013 | 5.65 ± 0.18 |
| A644 | 2.36 ± 0.09 | 4.74 ± 0.26 | 6.59 ± 0.45 | 1.230 ± 0.035 | 5.66 ± 0.48 |
| A1644 | 1.15 ± 0.02 | 3.24 ± 0.10 | 5.47 ± 0.26 | 1.054 ± 0.020 | 3.48 ± 0.20 |
| A1795 | 1.95 ± 0.02 | 4.06 ± 0.08 | 5.77 ± 0.15 | 1.153 ± 0.012 | 4.63 ± 0.14 |
| A2029 | 2.78 ± 0.03 | 6.25 ± 0.13 | 9.24 ± 0.26 | 1.423 ± 0.019 | 8.82 ± 0.35 |
| A2142 | 2.48 ± 0.02 | 6.08 ± 0.09 | 9.44 ± 0.19 | 1.424 ± 0.014 | 8.95 ± 0.26 |
| A2255 | 1.39 ± 0.06 | 4.08 ± 0.11 | 7.10 ± 0.36 | 1.196 ± 0.026 | 5.26 ± 0.34 |
| A2319 | 2.61 ± 0.08 | 5.58 ± 0.12 | 8.01 ± 0.25 | 1.346 ± 0.017 | 7.31 ± 0.28 |
| A3158 | 1.59 ± 0.02 | 3.76 ± 0.09 | 5.70 ± 0.21 | 1.123 ± 0.016 | 4.26 ± 0.18 |
| A3266 | 2.02 ± 0.05 | 5.57 ± 0.15 | 9.32 ± 0.39 | 1.430 ± 0.031 | 8.80 ± 0.57 |
| RXC1825 | 1.64 ± 0.02 | 3.69 ± 0.07 | 5.46 ± 0.15 | 1.105 ± 0.012 | 4.08 ± 0.13 |
| ZW1215 | 1.93 ± 0.03 | 5.22 ± 0.15 | 8.61 ± 0.39 | 1.358 ± 0.031 | 7.66 ± 0.52 |

Table 1 also lists Hydra A, which is not in the public archive and is out of scope.

## The test (pass/fail)

1. **Coverage.** The package has exactly these 12 clusters; stellar-mass profiles are present for exactly A85, A644, A1795, A2029, A2142, A2319 and ZW1215, and absent for the other five.
2. **The archive is the paper's analysis.** For each cluster, the archive's NFW mass profile (`M_NFW` in `<cluster>_hydro_mass.fits`, interpolated linearly in log M against log r) at 500, 1000 and 1500 kpc agrees with the Table 1 values within 1.5 %.
3. **R500 is consistent.** For each cluster, the archive's NFW mass at r = R500 (Table 1, in kpc) agrees with Table 1's M500 within 1.5 %, and the gas-fraction file's `M_NFW` at R/R500 = 1 agrees with Table 1's M500 within 1.5 %. (Together these confirm that the archive's R/R500 radii use Table 1's R500.)
4. **Conversion integrity.** For every measurement: g_obs = G M_forward(<r) / r², g_bar,gas = G M_gas(<r) / r² and, where measured, g_bar,stars = G M_star(<r) / r², each equal to the same expression evaluated from the archive's columns at that radius (relative 1e-9; interpolation as in test 2 where the archive grid differs).

The 1.5 % tolerance covers the three-significant-figure rounding of Table 1 (≤ 0.5 %) plus interpolation on smooth profiles. It is comparable to the smallest quoted 1σ errors (about 0.8 %) and well below most of them (up to about 7 %).

## Reported, not pass/fail (decided before conversion)

Ettori et al. 2019 Table 2 gives, for the forward method relative to backward NFW, the sample median (and quartiles) of (M_forward / M_NFW − 1): +0.6 % (−1.1/+3.3) at 0.5 Mpc, −2.0 % (−5.9/+1.4) at 1 Mpc, −4.6 % (−7.9/+1.3) at 1.5 Mpc, −4.7 % (−10.9/−0.5) at R500, +1.2 % (−5.4/+8.1) at R200. The paper's sample includes Hydra A, which the archive does not, so these medians cannot be reproduced exactly. The package's 12-cluster values are **reported** next to them in `REPRODUCTION_RESULT.md`, without a pass/fail threshold.
