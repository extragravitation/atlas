# aeg-d-kids1000-rar/v1 — reproduction test (frozen before conversion)

Written 2026-10-28, **before `convert.py` exists**. Disclosure: while reading the source on 2026-10-28, the values of two released files (`Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt` and `Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt`) were seen in full, and the release README was read. Nothing below depends on those values: every criterion is a rule, not a number chosen to fit them. This file's SHA-256 is recorded in `sources.json`; it is not edited after the first conversion run. If the test fails, the outcome is recorded and handled under D-019; the test is not changed to pass.

## What can be reproduced, and what cannot

Brouwer et al. 2021 (A&A 650, A113; arXiv:2106.11677) **publishes no tables of g_obs or g_bar**; the numbers exist only in figures and in the released files. So, unlike SPARC, there is no independent published table to reproduce. What the source does publish is the exact recipe (release README, and paper eq. 7):

- g_bar: the first column of each RAR file, in m s⁻² (the bin's mean baryonic acceleration).
- g_obs = 4 G ΔΣ_t / bias × [pc/m], with **G = 4.52 × 10⁻³⁰ pc³ M☉⁻¹ s⁻²** and **[pc/m] = 3.086 × 10¹⁶** as stated in the README; error[g_obs] = 4 G error[ΔΣ_t] / bias × [pc/m].
- Covariance: covariance[corrected] = covariance / bias, with the bias column of the covariance file.

**This test therefore establishes that the package follows the authors' documented method exactly. It does not independently verify the authors' published figures.** The dataset page states this limitation.

## Files in scope

From `brouwer2021_rar.tar` (SHA-256 in `sources.json`), the three RAR results shown in the paper's Fig. 4 for isolated lenses: KiDS-bright (`Fig-4-5-C1_RAR-KiDS-isolated_*`), KiDS-bright with the authors' hot-gas estimate added to g_bar (`Fig-4_RAR-KiDS-isolated_hotgas_*`), and GAMA (`Fig-4-C1_RAR-GAMA-isolated_*`), each with its covariance file. macOS metadata entries (`._*`) are ignored.

## The test

1. **Completeness.** Every data row of each in-scope ESD file appears exactly once in `tables/measurements.ecsv`, and nothing else does.
2. **g_bar.** Each row's g_bar equals the file's first column (relative tolerance 1e-12).
3. **g_obs and its error, against the README recipe with the README's own constants.** |Δ log10 g_obs| ≤ 0.001 dex and the same for the error. The package uses precise physical constants (IAU/CODATA via astropy); the README rounds G to three figures, so the two differ by much less than 0.001 dex but not by zero.
4. **Covariance.** For every pair in each covariance file, the package's covariance equals (4 G [pc/m])² × covariance / bias, with the package's constants, to relative 1e-9; the matrix is symmetric; its diagonal is positive.
5. **Constants.** The package's 4 G [pc/m] factor agrees with the README's 4 × 4.52e-30 × 3.086e16 to within 0.25 %.

**Pass** = all five hold.
