# SPARC rotation curves (aeg-d-sparc/v3): how each row is computed

This text is meant to be complete for every row of `tables/measurements.ecsv`. Its arithmetic, and the selection rules where the tables allow, are checked against every published row by `pipeline/tests/test_methods_text.py`. Whether a reader who does not know the code can follow it is tested only by the independent audit (D-116). The code is `v1/convert.py`, carried unchanged in value through v2 and v3. Where this text and the code differ, the error is in this text; please report it.

## 1. Constants and units

- **Unit conversion:** 1 (km s⁻¹)² kpc⁻¹ = 3.2407792894443656 × 10⁻¹⁴ m s⁻². This uses 1 kpc = 3.0856775814913673 × 10¹⁹ m (IAU 2015 B2, through astropy ≥ 6.1).
- **Mass-to-light ratios at 3.6 µm:** Υ_disk = 0.5 and Υ_bul = 0.7 M☉/L☉. In Lelli, McGaugh & Schombert 2016 (arXiv:1606.09251, `SPARC.tex`): Υ★ ≃ 0.5 "as suggested by stellar population models" (abstract, l. 29); Υ_bul = 1.4 Υ_disk (l. 261); and both values adopted together (l. 307 and l. 312).
- **Helium:** V_gas already includes the factor 1.33 for helium (SPARC Table 2, note 2). Nothing is added.

## 2. Inputs per row

**One row of the measurements table is one data row** of `MassModels_Lelli2016c.mrt`, in file order. The `source_ref` gives its number.
- **Counting:** data rows are counted from 1, starting with the first line after the last line of dashes, which ends the header and its notes.
- **Measurement identifiers:** m000001 is data row 1, and so on.
- **Reading the file:** it is read by the byte positions its header gives, which fit its data lines.

**From that row:**

| Column | Quantity | Unit |
|---|---|---|
| `R` | radius in the disc plane | kpc |
| `Vobs` | observed rotation velocity | km s⁻¹ |
| `Vgas` | gas contribution, for Υ = 1 and including helium | km s⁻¹ |
| `Vdisk` | stellar disc contribution, for Υ = 1 | km s⁻¹ |
| `Vbul` | stellar bulge contribution, for Υ = 1 (0 where there is no bulge) | km s⁻¹ |

**The galaxy's row of `SPARC_Lelli2016c.mrt`** gives the distance D and its error e_D, and the inclination Inc and its error e_Inc. These are used only for the uncertainty (§4).
- **Finding the row:** by the galaxy's name, column `Galaxy`. The `source_ref` gives the row number, counting data rows the same way.
- **Reading the file:** its data lines are wider than the byte positions in its header allow (131 against 113 bytes), so the file is read by splitting on white space.
- **Distance:** D is taken from this table. The mass-model file repeats it for each galaxy, and nothing is rescaled.

**Rows used:** every data row is used, and no row is cut.

**Listed but not used in g:** the surface-brightness columns `SBdisk` and `SBbul`, and the distance method `f_D`. They are named in the row's source text for the record. A row with no bulge has `Vbul` = 0, and no Vbul input is listed for it.

## 3. Steps

With C = 3.2407792894443656 × 10⁻¹⁴:

1. g_obs = Vobs² / R × C.
2. g_bar_stars = (0.5 Vdisk |Vdisk| + 0.7 Vbul |Vbul|) / R × C.
3. g_bar_gas_cold = Vgas |Vgas| / R × C. The sign is kept: a negative V|V| lowers g_bar (source eq. 2).
4. g_bar = g_bar_stars + g_bar_gas_cold.

## 4. Uncertainties shown with a row

These do not enter g_obs or g_bar.

- **g_obs:** δg_obs = g_obs √[(2 e_Vobs/Vobs)² + (2 δi / tan i)² + (δD/D)²] (Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836, 152, arXiv:1610.08981, eq. 2; that paper is cited, not supplied). Here δi = e_Inc and δD = e_D, from the galaxy's row; i and δi are in radians.
- **Point-scale g_obs error:** g_obs × 2 e_Vobs / Vobs, the velocity part only.
- **g_bar:** √[(0.10 g_bar_gas_cold)² + (0.25 g_bar_stars)²].
