# X-COP galaxy clusters (aeg-d-xcop/v3): how each row is computed

This text is meant to be complete for every row of `tables/measurements.ecsv`. Its arithmetic, and the selection rules where the tables allow, are checked against every published row by `pipeline/tests/test_methods_text.py`. Whether a reader who does not know the code can follow it is tested only by the independent audit (D-116). The code is `v3/convert.py`. Where this text and the code differ, the error is in this text; please report it.

## 1. What the source releases

Eckert et al. 2022 release g_obs and g_bar themselves, for five clusters, in `data_E22.tar.gz`. Each cluster has a file `<cluster>/gbar_gobs_<cluster>.fits`, for A644, A1795, A2029, A2142 and A2319. The Atlas converts nothing.

## 2. Inputs per row

**Which file and row.** Unpack `data_E22.tar.gz`. Each cluster's file holds one table, in HDU 1, the first extension after the primary header.
- **Rows:** one row of the measurements table is one row of that table, counted from 1 in the order stored. The `source_ref` gives the file and the row.
- **Measurement identifiers:** they follow the files in the order A644, A1795, A2029, A2142, A2319, with each file's rows in order. A644 has rows m000001 to m000019; A1795 follows with 21 rows, A2029 with 22, A2142 with 20 and A2319 with 27.

**Columns of the table:**

| Column | Content | Unit (as the file writes it) |
|---|---|---|
| `RADIUS` | radius from the cluster centre. The file does not say whether it is three-dimensional; the paper computes g_obs and g_bar at three-dimensional radii (l. 451–456) | kpc |
| `GOBS` | g_obs as released | `m/s^2` |
| `GOBS_ERR_LO`, `GOBS_ERR_HI` | its lower and upper errors | `m/s^2` |
| `GBAR` | g_bar as released: gas, central galaxy and satellites, as one total | `m/s^2` |
| `GBAR_ERR` | its error | `m/s^2` |

**Errors are magnitudes,** positive distances below and above the value, not the bounds themselves. The headers do not say so; it is determined from the values (on all 109 rows both GOBS errors are smaller than GOBS, and GBAR_ERR is smaller than GBAR). The confidence level of the errors is not stated by the source.

**Units:** `m/s^2` is m s⁻². The Atlas checks that `RADIUS` is in kpc and that the five acceleration columns are in m s⁻². No unit is converted.

**Values:** they are stored as 32-bit floats and used as stored.

## 3. Steps

1. r = `RADIUS`, g_obs = `GOBS`, g_bar = `GBAR`, all unchanged.
2. Every row of the five files is plotted.
3. **The seven other X-COP clusters** have no stellar data and no released accelerations. They are recorded as systems with no rows (part B rule 2).

## 4. Background

The paper writes g_obs = G M_HSE(<r) / r² and g_bar = G (M_gas + M★,BCG + M★,sat)(<r) / r² (Eckert et al. 2022, `hydromass.tex` l. 453–456).

**Which method the released GOBS comes from is not stated.** The paper uses two methods for g_obs, a nonparametric reconstruction and an Einasto fit (l. 458), and no sentence or FITS keyword says which one the released column holds. The released files give points at the radii of the data. The paper associates such points with the nonparametric method (l. 263 in §3.5 Optimization, and l. 445), but that is an association, not a statement. The Atlas therefore records no model dependence (`reading/model_form.md`, part B rule 3).

**The central galaxy's stellar mass** in g_bar uses dynamical mass-to-light ratios (§2.4.1 "BCG", l. 101–112).

**Line numbers** count the physical lines of the named file from 1.
