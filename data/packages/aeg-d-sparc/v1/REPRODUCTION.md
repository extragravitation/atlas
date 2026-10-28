# aeg-d-sparc/v1 — reproduction test (frozen before conversion)

Written 2026-10-28, **before `convert.py` exists and before any value of the reference file has been read**. Of the reference file, only its header (column definitions) and total line count (2 707) were seen. This file's SHA-256 is recorded in `sources.json`; it is not edited after the first conversion run. If the test fails, the package does not ship and the failure is published; the test is not changed to pass (operating rule 5).

## Reference

`RAR.mrt` from the SPARC site: "Data Behind Figure 2" of Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836, 152 ("One Law to Rule Them All", arXiv:1610.08981). Columns: log10 g_bar, its error, log10 g_obs, its error (m s⁻², two decimals). No galaxy names or radii.

## What the authors did (read at source, arXiv:1610.08981 §II.1)

- Sample: SPARC late-type galaxies, excluding the 12 with quality flag Q = 3 and the 10 with inclination i < 30°.
- Points: only those with δV_obs / V_obs < 0.1, leaving **2 693 points**.
- g_obs = V_obs² / R.
- g_bar = V_bar² / R with V_bar² = |V_gas|V_gas + Υ_disk |V_disk|V_disk + Υ_bul |V_bul|V_bul (SPARC paper, arXiv:1606.09251, eq. 2), Υ_disk = 0.5 and Υ_bul = 0.7 M☉/L☉ at 3.6 µm.

## The test

Applied to `tables/measurements.ecsv` at catalogue defaults (Υ_disk = 0.5, Υ_bul = 0.7), with the per-galaxy Q and inclination from `tables/systems.ecsv`:

1. **Selection count.** Applying the three selections above yields **exactly 2 693** measurements.
2. **Point-by-point agreement.** Compute log10 g_bar and log10 g_obs for those 2 693 measurements. Every one must be matched one-to-one to a distinct row of `RAR.mrt` with |Δ log10 g_bar| ≤ 0.015 and |Δ log10 g_obs| ≤ 0.015 dex. The 0.015 dex tolerance covers the reference's two-decimal rounding (±0.005) plus small differences in unit constants; it is far below the typical measurement error (≈ 0.1 dex on g_obs, per the paper).
3. **Conversion integrity** (independent of the reference). For every one of the 3 391 SPARC rows: √(g_obs · R) recovers the table's V_obs to within 0.01 km s⁻¹ (the table's last digit); g_bar equals (|V_gas|V_gas + 0.5|V_disk|V_disk + 0.7|V_bul|V_bul)/R computed directly from the table, to a relative tolerance of 1e-9; and g_bar equals the sum of its stored components to the same tolerance.

**Pass** = all three hold. Anything else is a fail.

## Not tested here

- Uncertainties are not part of the pass/fail test. The package's g_obs uncertainty follows the authors' formula (arXiv:1610.08981 eq. 2: velocity, inclination and distance errors combined), and its agreement with the reference's error column is reported, not required.
- Selections are applied **only inside this test**. The package itself contains all 175 galaxies and all points; the source's quality flag is carried as data, never used to hide anything.
