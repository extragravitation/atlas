# aeg-d-xcop/v1 — test of the modelled-star prescription (frozen before it is run)

Written 2026-10-28 under D-023, **before the prescription has been compared with any measured stellar profile**. Disclosure: before this file was written, the share of g_bar contributed by stars had been looked at for all 12 clusters (measured stars: 68–92 % at 30 kpc, 34–49 % at 100 kpc, 15–21 % at 200 kpc; modelled: 33–62 % at 30 kpc), and the ratio g_obs/g_bar at 30 kpc (4–12 measured, 20–90 modelled). No comparison of modelled with measured stars was made. This file's SHA-256 is recorded in `sources.json`. The test is not changed after it has run.

## Purpose

The 5 clusters without measured stars (A1644, A2255, A3158, A3266, RXC1825) take their stellar mass from the prescription of D-022 item 3. Its rows ship only at radii where the same prescription, applied to the 7 clusters with measured stars, reproduces their g_bar.

## Procedure

1. For each of the 7 clusters with measured stars (A85, A644, A1795, A2029, A2142, A2319, ZW1215), at each of its rows in the package (before any cut), compute the modelled stellar mass exactly as for the 5 modelled clusters: NFW shape with r_s = R200 / 2.9, normalised so that M★(<R500) = 0.39 (M500 / 10¹⁴ M☉)^−0.84 × M_gas(<R500), with R500, M500 and R200 from Ettori et al. 2019 Table 1 and M_gas(<R500) interpolated from the gas file as in `convert.py`.
2. g_bar,model = g_bar,gas + G M★,model(<r) / r². Deviation d = g_bar,model / g_bar − 1, where g_bar is the package's value with measured stars.
3. Scaled radius x = r / R500 (Table 1). Grid: 50 values of x spaced evenly in log x from 0.025 to 1.5. For each cluster, d is interpolated linearly in log x onto the grid points inside that cluster's own range of x; no extrapolation.
4. At each grid point covered by **at least 5** of the 7 clusters: statistic D(x) = median over those clusters of |d|. The point **passes** if D(x) ≤ 0.10.
5. **Validated range** [x_min, x_max]: x_max is the largest grid point covered by at least 5 clusters; x_min is the smallest grid point such that every covered grid point from x_min to x_max passes. If x_max itself fails, there is no validated range.
6. **Cut.** A row of the 5 modelled clusters ships only if x_min ≤ r / R500 (Table 1) ≤ x_max. If there is no validated range, no row of the 5 modelled clusters ships; the clusters stay in the registry and in `systems.ecsv`, and the dataset page says why.

## Recorded

`MODEL_TEST_RESULT.md` gives D(x), the number of clusters covering each grid point, pass or fail, the validated range, and the number of modelled rows kept and removed per cluster, whatever the outcome. The 10 % tolerance is a judgement call (D-023), set inside the hydrostatic-bias range already allowed (0 to 20 %).
