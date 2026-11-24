# SPARC rotation curves (aeg-d-sparc/v3): how each row is computed

This text is complete for every row of `tables/measurements.ecsv`. The code is `v1/convert.py`, carried unchanged in value through v2 and v3. Where this text and the code differ, the error is in this text; please report it.

## 1. Constants and units

- **Unit conversion:** 1 (km s⁻¹)² kpc⁻¹ = 3.2407792894443656 × 10⁻¹⁴ m s⁻². This uses 1 kpc = 3.0856775814913673 × 10¹⁹ m (IAU 2015 B2, through astropy ≥ 6.1).
- **Mass-to-light ratios at 3.6 µm:** Υ_disk = 0.5 and Υ_bul = 0.7 M☉/L☉. These are the catalogue defaults, "as suggested by SPS models" (Lelli, McGaugh & Schombert 2016; arXiv:1606.09251).
- **Helium:** V_gas already includes the factor 1.33 for helium (SPARC Table 2, note 2). Nothing is added.

## 2. Inputs per row

**One row of the measurements table is one data row** of `MassModels_Lelli2016c.mrt`, in file order. The `source_ref` gives its number, counting data rows from 1 after the byte-by-byte header.

**From that row:**

| Column | Quantity | Unit |
|---|---|---|
| `R` | radius in the disc plane | kpc |
| `Vobs` | observed rotation velocity | km s⁻¹ |
| `Vgas` | gas contribution, for Υ = 1 and including helium | km s⁻¹ |
| `Vdisk` | stellar disc contribution, for Υ = 1 | km s⁻¹ |
| `Vbul` | stellar bulge contribution, for Υ = 1 (0 where there is no bulge) | km s⁻¹ |

**The galaxy's row of `SPARC_Lelli2016c.mrt`** gives the distance, inclination and their errors. These are used only for the uncertainty (§4).

**Rows used:** every data row is used, and no row is cut.

## 3. Steps

With C = 3.2407792894443656 × 10⁻¹⁴:

1. g_obs = Vobs² / R × C.
2. g_bar_stars = (0.5 Vdisk |Vdisk| + 0.7 Vbul |Vbul|) / R × C.
3. g_bar_gas_cold = Vgas |Vgas| / R × C. The sign is kept: a negative V|V| lowers g_bar (source eq. 2).
4. g_bar = g_bar_stars + g_bar_gas_cold.

## 4. Uncertainties shown with a row

These do not enter g_obs or g_bar.

- **g_obs:** δg_obs = g_obs √[(2 e_Vobs/Vobs)² + (2 δi / tan i)² + (δD/D)²] (arXiv:1610.08981 eq. 2). The inclination and its error are in radians.
- **Point-scale g_obs error:** g_obs × 2 e_Vobs / Vobs, the velocity part only.
- **g_bar:** √[(0.10 g_bar_gas)² + (0.25 g_bar_stars)²].
