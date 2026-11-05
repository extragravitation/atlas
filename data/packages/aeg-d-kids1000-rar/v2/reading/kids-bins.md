# KiDS-1000 RAR: g_bar bin edges, derived independently (second reading, item 11)

Read 2026-11-05. Source: Brouwer et al. 2021, arXiv e-print 2106.11677 (e-print SHA-256 `43bab5e0b439d459bcd95b8cb48e31e82f50b4b7c5b99bc4e0715843821874be`), file `RAR_paper_Brouwer_4.tex` (SHA-256 `45aa25abaa516893a77d365e4f708521cc3879113a34e8b11289220948ff4b19`).

## Statement at source

§2.1 ("Mass measurements with weak gravitational lensing"), l. 174:

> "we chose our $R$-bins such that they corresponded to $15$ logarithmic bins between $1\E{-15} < g\un{bar} < 5\E{-12} \mpss$. For each individual lens the calculation of these $g\un{bar}$-bins was based on the baryonic mass of the galaxy $M\un{gal}$"

## Derivation

Logarithmic bins, equal width in log10 g_bar:

Δ = (log10(5×10⁻¹²) − log10(1×10⁻¹⁵)) / 15 = log10(5000) / 15 = 0.24659800028906792

Edges e_k = 10^(−15 + k·Δ) m s⁻², k = 0 … 15. Bin k (1 … 15) is [e_(k−1), e_k].

| bin k | lower edge (m s⁻²) | upper edge (m s⁻²) | arithmetic midpoint (e_(k−1)+e_k)/2 | released column 1 (all three files, printed) |
|---|---|---|---|---|
| 1 | 1.000000e-15 | 1.764404e-15 | 1.382202e-15 | 1.3822e-15 |
| 2 | 1.764404e-15 | 3.113121e-15 | 2.438762e-15 | 2.4388e-15 |
| 3 | 3.113121e-15 | 5.492803e-15 | 4.302962e-15 | 4.3030e-15 |
| 4 | 5.492803e-15 | 9.691522e-15 | 7.592163e-15 | 7.5922e-15 |
| 5 | 9.691522e-15 | 1.709976e-14 | 1.339564e-14 | 1.3396e-14 |
| 6 | 1.709976e-14 | 3.017088e-14 | 2.363532e-14 | 2.3635e-14 |
| 7 | 3.017088e-14 | 5.323362e-14 | 4.170225e-14 | 4.1702e-14 |
| 8 | 5.323362e-14 | 9.392561e-14 | 7.357961e-14 | 7.3580e-14 |
| 9 | 9.392561e-14 | 1.657227e-13 | 1.298242e-13 | 1.2982e-13 |
| 10 | 1.657227e-13 | 2.924018e-13 | 2.290622e-13 | 2.2906e-13 |
| 11 | 2.924018e-13 | 5.159148e-13 | 4.041583e-13 | 4.0416e-13 |
| 12 | 5.159148e-13 | 9.102821e-13 | 7.130985e-13 | 7.1310e-13 |
| 13 | 9.102821e-13 | 1.606105e-12 | 1.258194e-12 | 1.2582e-12 |
| 14 | 1.606105e-12 | 2.833818e-12 | 2.219962e-12 | 2.2200e-12 |
| 15 | 2.833818e-12 | 5.000000e-12 | 3.916909e-12 | 3.9169e-12 |

Full-precision edges are in `kids-second-reading.csv` (`bin_lo`, `bin_hi`, Python float64 `repr`).

## Checks against the release

1. **Every released g_bar lies strictly inside its row's bin** (row k in bin k), in all three files: 45 of 45.
2. **Column 1 is identical in all three files** (KiDS-bright, GAMA, hot-gas variant), row by row, at printed precision; and the covariance files' `Radius[i]` values (printed to 19 significant digits) are identical across the three covariance files.
3. **Column 1 equals the arithmetic midpoint of the bin edges.** The covariance files' full-precision `Radius[i]` values equal (e_(k−1)+e_k)/2 to a relative difference of at most 2.5e-14 for all 15 bins (e.g. bin 1: release 1.382201932178117638e-15, midpoint 1.3822019321781176e-15). They differ from the geometric bin centre (bin 1: 1.3283e-15) and from the mean of a log-uniform distribution over the bin (bin 1: 1.3462e-15).

## Consequence for the reading (a description finding; no value changes)

- The step A reading (`uncertainty-readings.md` §1.1) inferred that column 1 values "appear to be bin means". The release does not support that inference for a sample-dependent mean: the same 15 values appear in three different lens samples, and they reproduce the linear midpoint of the §2.1 logarithmic bins to float precision. Column 1 is a fixed per-bin coordinate (the arithmetic midpoint of each bin), not a mean over each sample's lenses. The README's wording ("The mean projected distance from the lens center") is radius wording and does not describe this.
- This supports `g_bar_basis = bin_coordinate` (test 5) and supports, from the release itself, the Atlas's inference that the hot-gas file uses the same edges.
- It bears on the `acceleration_released` observable's description (test 8) and on Brouwer-email question 2 (§1.4), which can be closed or reworded. Whether to change any wording is for the main session and JvH.
