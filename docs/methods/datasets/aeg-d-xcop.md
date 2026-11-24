# X-COP galaxy clusters (aeg-d-xcop/v3): how each row is computed

This text is complete for every row of `tables/measurements.ecsv`. The code is `v3/convert.py`. Where this text and the code differ, the error is in this text; please report it.

## 1. What the source releases

Eckert et al. 2022 release g_obs and g_bar themselves, for five clusters, in `data_E22.tar.gz`. Each cluster has a file `<cluster>/gbar_gobs_<cluster>.fits`, for A644, A1795, A2029, A2142 and A2319. The Atlas converts nothing.

## 2. Inputs per row

**One row of the measurements table is one row of a cluster's FITS table,** counted from 1. The `source_ref` gives the file and the row.

**Columns of the FITS table:**

| Column | Content | Unit |
|---|---|---|
| `RADIUS` | three-dimensional radius | kpc |
| `GOBS` | the source's non-parametric hydrostatic g_obs | m s⁻² |
| `GOBS_ERR_LO`, `GOBS_ERR_HI` | its errors, read as error magnitudes (`reading/error_form.md`) | m s⁻² |
| `GBAR` | g_bar: gas, central galaxy and satellites, as one total | m s⁻² |
| `GBAR_ERR` | its error, an error magnitude | m s⁻² |

**Units:** the file states them. The Atlas checks that `RADIUS` is in kpc and the four accelerations in m s⁻². No unit is converted.

## 3. Steps

1. r = `RADIUS`, g_obs = `GOBS`, g_bar = `GBAR`, all unchanged.
2. Every row of the five files is plotted.
3. **The seven other X-COP clusters** have no stellar data and no released accelerations. They are recorded as systems with no rows (part B rule 2).

## 4. Background

g_obs = G M_HSE(<r) / r² (Eckert et al. 2022, l. 453). The hydrostatic mass comes from the source's non-parametric reconstruction (§3.4, l. 263). The Atlas uses the released values and does not redo this step.
