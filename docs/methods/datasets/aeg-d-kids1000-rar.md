# KiDS-1000 weak-lensing RAR (aeg-d-kids1000-rar/v3): how each row is computed

This text is meant to be complete for every row of `tables/measurements.ecsv`. Its arithmetic, and the selection rules where the tables allow, are checked against every published row by `pipeline/tests/test_methods_text.py`. Whether a reader who does not know the code can follow it is tested only by the independent audit (D-116). The code is `v3/convert.py`, which computes values exactly as v1 did. Where this text and the code differ, the error is in this text; please report it.

## 1. Constants and units

- **Conversion:** 4 G × (1 M☉ pc⁻²) = 4 × 6.67430 × 10⁻¹¹ × 1.98840987 × 10³⁰ kg / (3.0856775814913673 × 10¹⁶ m)², in m s⁻². This uses G from CODATA 2018 and M☉ and the parsec from IAU 2015, through astropy ≥ 6.1.
- **ΔΣ** is released in h₇₀ M☉ pc⁻², with h = 0.7, physical. It is used as released, with no h scaling.
- **The README's constants** (G = 4.52 × 10⁻³⁰ pc³ M☉⁻¹ s⁻², pc = 3.086 × 10¹⁶ m) are not used; the constants above are. The difference is about 0.03 %, far below the audit tolerance.

## 2. Inputs per row

**One row of the measurements table is one data row** of one released ESD file in `brouwer2021_rar.tar`.
- **Data rows:** the lines that do not begin with `#`, counted from 1. Each file has 15 rows of 8 columns, separated by white space.
- **Measurement identifiers:**
  - m000001 to m000015 are `kids_bright` rows 1 to 15;
  - m000016 to m000030 are `kids_bright_hotgas` rows 1 to 15;
  - m000031 to m000045 are `gama` rows 1 to 15.

**The three files:**

| Sample | File | Role |
|---|---|---|
| `kids_bright` | `Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt` | default |
| `gama` | `Fig-4-C1_RAR-GAMA-isolated_Nobins.txt` | default |
| `kids_bright_hotgas` | `Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt` | alternative (D-096 rule 3); g_bar includes the authors' hot-gas estimate |

**From each data row:**

| Column | Content |
|---|---|
| 1 | g_bar, as released. The file's header calls it `Radius(m/s^2)`, and the README (l. 25) describes it as "the mean projected distance from the lens center … in meter-per-second-squared for the RAR data". That it is g_bar comes from the paper: the R-bins were chosen to correspond to 15 logarithmic bins in g_bar (§2.1, l. 174). It equals the arithmetic midpoint of its bin (§4) |
| 2 | ESD_t, the tangential excess surface density ΔΣ, before the bias correction |
| 4 | the 1σ error on ESD_t ("The 1-sigma error value on ESD_t", README) |
| 5 | the bias, (1 + K) |

## 3. Steps

1. g_obs = 4 G ΔΣ / bias, with ΔΣ = column 2 and bias = column 5. This is the README's recipe and eq. 7 of the paper.
2. g_bar = column 1, unchanged.
3. **Plotting:**
   - **KiDS-bright rows 1 to 8** are recorded, not plotted (D-103; D-096 rule 2). They are the points beyond the paper's isolation limit, which the paper leaves out of every model comparison: "by only using the seven data points within the isolation criterion limit" (l. 508). The limit is written as both 0.3 and 3 h₇₀⁻¹ Mpc (known issue #169), and once as an acceleration, g_bar < 10⁻¹³ m s⁻² (l. 595), which would also leave out row 9. The Atlas follows the paper's own count of seven points (l. 508): rows 9 to 15 are kept, by row number.
   - **The hot-gas file's rows** are alternative rows, not plotted.
   - **Every other row is plotted.**

## 4. Uncertainties shown with a row

These do not enter g_obs or g_bar.

- **g_obs error:** 4 G × column 4 / bias, the point-scale one-sigma error.
- **The 0.1 dex conversion term:** the paper adds 0.1 dex for the ΔΣ-to-g_obs conversion. It is the term `esd_to_gobs_conversion` in `tables/uncertainty_terms.ecsv`, not a column error.
- **g_bar:** it is the coordinate of its bin. Its bin edges are 10^(−15 + (k − 1)Δ) and 10^(−15 + kΔ) m s⁻², with Δ = log₁₀(5 × 10⁻¹² / 10⁻¹⁵) / 15 (§2.1, l. 174).
