# Error budget (WP2): inventory and options

**Status:** proposal for JvH's ruling (2026-11-01). Nothing is built yet. The inventory is read from the shipped packages' column descriptions and the assumption registry (`data/assumptions.json`) at main `6f62152`. No source paper has been re-read for this document. Items marked *to read at source* are not stated as fact.

## 1. Why this matters

A reader who works on these data will judge the Atlas first by its error bars:
- what each bar includes;
- what it leaves out;
- whether an error shared by many points is drawn as if every point were independent.

An error drawn as independent when it is shared makes a relation look tighter or looser than the data support. That is the most common technical objection to compilations like this one.

## 2. Three scales of uncertainty

Every uncertainty in the Atlas acts at one of three scales. This is a property of the measurement, not a choice.

| Scale | Shared by | Examples |
|---|---|---|
| **Point** | one measurement only | SPARC velocity error; KiDS stacked-signal error; a dispersion's error; θ_E error |
| **System** | every point of one galaxy, cluster or lens | distance; inclination; one galaxy's stellar mass-to-light ratio; one cluster's mass-profile fit |
| **Dataset** | every system in a dataset | stellar-population calibration and IMF; hydrostatic bias; helium factor; cosmology; ICL fraction |

## 3. Inventory: what the shipped error columns contain

Default rows only. The "median" column is the median upper error in dex.

| Dataset | g_obs error: contents (rows with it; median) | g_bar error: contents (rows with it; median) | Scale actually in the bar | Sliders (dataset scale) |
|---|---|---|---|---|
| SPARC | velocity, inclination and distance in quadrature (3 391/3 391; 0.104) | 10 % gas, 25 % stellar, "per source" (3 389/3 391; 0.089) | **Mixed:** g_obs mixes point (velocity) with system (inclination, distance) terms. g_bar is a system-scale Υ scatter drawn on every point. The map's "per point / full" toggle separates the g_obs terms; g_bar has no such split. | ml_disk, ml_bulge; distance and inclination per galaxy |
| X-COP | forward-method mass error (861/861; 0.017) | gas and measured-star errors in quadrature; modelled stars carry none (861/861; 0.004) | Profile points come from one fit per cluster, so neighbouring errors are **correlated**. This is not stated on the figures. The modelled-star rows understate g_bar error. | xray_hse_bias, icl_fraction |
| KiDS-1000 | released stacked-signal error, bias-corrected (45/45; 0.039); full covariance shipped | **none:** "Not given by the source" (0/45) | Point, with covariance. g_bar has no error at all. | none (deprojection and hot gas are fixed assumptions) |
| Strong lensing | M_E error at fixed R_E (56/94; 0.017) | stellar-mass error only, at fixed R_E (57/94; 0.079) | Point. 38 rows lack a g_obs error and 37 a g_bar error (*to read at source* whether the papers print them). Redshift and cosmology terms are not included. | a6s_stellar_imf, a6s_gas_in_RE |
| Globular clusters | dispersion error only (64/64; 0.053) | population M/L_V error only (64/64; 0.035) | Point. Distance (it moves g_obs and g_bar together) and half-light-radius errors are not included. | gc_stellar_ml |
| Dwarf galaxies | printed dispersion error only (57/64; 0.156) | magnitude error only (64/64; 0.108) | Point. Distance and half-light-radius errors are not included. 7 rows without a g_obs error are *to check* (upper limits?). | dw_stellar_ml |

**What a specialist will notice first:**
1. **SPARC g_bar.** A 25 % stellar error is drawn on every point. The source's own file does the same, since `RAR.mrt` gives an error per point. But it is a per-galaxy (and partly whole-dataset) quantity, so the bars do not show that all points of a galaxy move together, and the reader cannot tell.
2. **KiDS g_bar has no error.** The stellar masses of lens galaxies carry a substantial systematic uncertainty. *To read at source:* what Brouwer et al. 2021 state.
3. **X-COP errors are correlated along each profile**, and modelled stars carry no error.
4. **Distance is missing** for globular clusters and dwarfs. A distance error moves g_obs and g_bar together along a fixed direction, which is different from an independent bar on each axis.
5. **Issue #64** (KiDS `no_uncertainty` wording) belongs here.

## 4. Options

### A. Label, don't change (smallest)

- Keep every number.
- State on every error column, legend and tooltip which scale and which terms are in the bar, and which are left out.
- Add an error-budget table to each dataset page.
- **For:** fast; honest about the present state.
- **Against:** the figures still draw shared errors as independent bars. A specialist will still object, now with the Atlas's own table as evidence.

### B. Three-scale error model (recommended)

1. **Data standard 2.2.0.**
   - The g_obs and g_bar error columns hold **point-scale terms only**.
   - System- and dataset-scale terms become **named components** in the assumption registry. Each has a published range and an effect formula, as the sliders already do: distance, inclination, per-galaxy Υ, profile fit, cosmology, calibration.
   - Each term records which axes it moves (g_obs, g_bar or both) and its source.
2. **Figures.**
   - Error bars show point-scale errors.
   - A system-scale term appears, on demand, as a **shift of the whole system along its true direction**. Distance, for example, moves a galaxy's points diagonally, not as separate bars on each axis.
   - Dataset-scale terms are the existing sliders.
   - The map's "per point / full" toggle becomes general across datasets.
3. **Fill gaps only from the sources.**
   - Where a source publishes a term that the package left out, add it, read at source with a quote: for example, KiDS stellar-mass uncertainty, X-COP modelled-star scatter, and distances for globular clusters and dwarfs.
   - Where no source gives it, the Atlas says "not given by the source" on the figure. No error is invented.
4. **Correlations.**
   - Shipped as given where a source provides them: KiDS covariance now, and the X-COP profile covariance if the team supplies it (it could be added to the X-COP note).
   - Otherwise stated as "correlated along the profile, covariance not published".
5. **Each package becomes a new version** (v2), with its own frozen reproduction test. The v1 packages stay published and unchanged.

- **For:** this is the correct statistical model, and the one a specialist expects. It reuses the slider machinery that already computes effects from the data. It invents nothing.
- **Against:**
  - more work: one standard change, six package versions and site changes;
  - each v2 needs its reproduction test frozen first;
  - some gaps stay gaps.

### C. Full Monte Carlo realisations

- Publish, for each dataset, a set of correlated random realisations of all terms (for example 1 000 draws), so a user can propagate any analysis.
- **For:** the most complete.
- **Against:**
  - heavy, and it needs distributions that most sources do not state, so it would mean choosing shapes the sources did not give;
  - it is better done after B, for the datasets whose sources give full error models.

## 5. Recommendation

**B**, in this order:
1. Freeze data standard 2.2.0, the registry terms, and each v2 package's reproduction test before converting.
2. Then the packages, starting with SPARC (most scrutinised) and KiDS (no g_bar error).
3. Then X-COP, the globular clusters, the dwarfs and the lenses.
4. Site changes go with each package.

Option C stays on the backlog.

## 6. Rulings needed

1. Option A, B or C.
2. If B: whether the X-COP note (draft v4) should also ask for the profile covariance. That is a data request, so it falls under the freeze; it costs nothing, but you decide.
3. If B: whether all six packages are in scope for v0.2, or SPARC and KiDS first, with the others following.
