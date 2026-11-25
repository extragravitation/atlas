# Globular clusters (aeg-d-gc-baumgardt/v3): how each row is computed

This text is meant to be complete for every row of `tables/measurements.ecsv`. Its arithmetic, and the selection rules where the tables allow, are checked against every published row by `pipeline/tests/test_methods_text.py`. Whether a reader who does not know the code can follow it is tested only by the independent audit (D-116). A reader with the source files, the locators (`locators.json`) and this page should be able to recompute g_obs and g_bar without the Atlas code. The code that does it is `v1/analysis.py` (with `pipeline/aeg/dispersion.py` and `pipeline/aeg/king66.py`), and `v2/convert.py` for the two v2 changes. Where this text and the code differ, that is an error in this text: please report it.

## 1. Constants and units

| Quantity | Value | Source |
|---|---|---|
| G | 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻² | CODATA 2018, through astropy ≥ 6.1 |
| M☉ | 1.98840987 × 10³⁰ kg | IAU 2015 nominal, through astropy |
| 1 pc | 3.0856775814913673 × 10¹⁶ m | IAU 2015 B2, through astropy |
| M_V,☉ | +4.85 mag | as adopted by McLaughlin & van der Marel 2005 §4.2 ("Lang 1999") |
| 1 rad | 206 264.806″ | |
| km s⁻¹ to m s⁻¹ | × 1000 | |

## 2. Inputs per cluster, and where they are

| Input | Unit | File and place |
|---|---|---|
| Dispersion profile: for each bin, `<r>`, NStar and σ | arcsec, count, km s⁻¹ | `veldis.html`: the velocity-dispersion table. Every row of the cluster with the chosen Type (§3). The cluster's name is printed only on its first row and carries down to the rows below it |
| W₀ and r₀ of the King (1966) fit | dimensionless, arcsec | VizieR J/ApJS/161/304 `models`: the row `MW-<name>` with `Mod = K`, columns `W0/gamma` and `r0` |
| R_h, the projected half-light radius | log₁₀(pc) | the same row, column `Rh` |
| The distance the fit assumed | kpc | the same row, column `Dist` |
| Υ_V, the stellar mass-to-light ratio | M☉/L☉ (V band) | VizieR J/ApJS/161/304 `clusters`: row `MW-<name>`, column `(M/L)1` (Bruzual & Charlot 2003 with a Chabrier disk IMF) |
| R_Sun, the distance | kpc | Harris `mwgc.dat` Part I, column `R_Sun`, the cluster's row |
| M_V,t, the integrated absolute magnitude | mag | Harris `mwgc.dat` Part II, column `M_V,t`, the cluster's row |

**Matching names.** Names are matched across the three sources by `v1/sources_io.norm_name`:
- upper-case the name;
- drop a leading `MW-`;
- remove spaces, hyphens and underscores;
- write `TERZAN<n>` as `TER<n>`.

Then the aliases listed in that function apply: 2MSGC01 / 2MS1 → 2MASSGC01, 2MSGC02 / 2MS2 → 2MASSGC02, DJORG1 → DJOR1, DJORG2 → DJOR2, 1636283 → ESO452SC11, ESOSC06 → ESO280SC06, GRAN3PATCHICK125 → GRAN3, PATCHICK126 → PAT126, SAGITTARIUSII → SGR2 and GRAN1ESO456SC29 → GRAN1. Example: `NGC 104` and `MW-NGC104` are the same cluster.

## 3. Which profile is used

- **Line of sight only.** Only line-of-sight Types are converted: `RV`, `F13`, `L13`, `L15`, `K18`, `D21`, `C22` and `G22` (the page's legend). Proper-motion Types (`W15`, `C21`, `H21`, `VB21`, `LI22`, `T22`, `P22`) are recorded as observables and never enter g_obs.
- **Candidates.** Each line-of-sight Type a cluster has is one candidate profile. Its rows, sorted by `<r>`, are its bins.
- **Plotting rules.** A candidate can be plotted only if it has at least two bins and its light coverage (§4, step 4) is at least 0.80.
- **Default among candidates that pass:**
  1. `RV` first;
  2. then the larger total NStar (a Type that prints no NStar counts as 0);
  3. then the later year of the Type's code: F13 and L13 are 2013, L15 2015, K18 2018, D21 2021, C22 and G22 2022.
- **Other candidates.** The rest are alternative rows (`role = alternative`). Candidates that fail the plotting rules are also alternative rows, with `not_plotted_reason = coverage_below_threshold`.
- **In practice.** Every default row in v3 uses Type `RV`.

## 4. Steps

1. **King (1966) model** from W₀ and r₀, the lowered isothermal sphere in McLaughlin & van der Marel's dimensionless form, with x = r/r₀:
   - **density:** ρ(W) ∝ e^W erf(√W) − √(4W/π) (1 + 2W/3);
   - **Poisson equation:** (1/x²) d/dx (x² dW/dx) = −9 ρ(W)/ρ(W₀), with W(0) = W₀ and dW/dx(0) = 0;
   - **tidal radius:** x_t is where W first reaches 0.
   - **The Atlas's numerics:** fourth-order Runge–Kutta in ln x, 400 steps per decade from x = 10⁻⁶, the tidal radius by linear interpolation of the sign change of W, and the trapezoidal rule for projections.
   - Any integration accurate to about 10⁻⁴ in the light fractions gives the same g_obs well within the audit tolerance.
2. **Projected (cylinder) light fraction** inside a projected radius R:
   - L_cyl(R) = L(<R) + ∫_R^{r_t} 4π r² ρ(r) [1 − √(1 − R²/r²)] dr, where L(<r) is the 3D light inside r (light follows ρ);
   - divide by the total light L(<r_t). This gives F(R), which is 0 at R = 0 and 1 at R = r_t.
   - R is in arcsec, the unit of r₀.
3. **Bin edges.** The page gives only each bin's mean radius `<r>`, so the edges are inferred from the sorted radii r₁ < … < r_n:
   - the first edge is 0;
   - each inner edge is the midpoint (r_i + r_{i+1})/2;
   - the last edge is r_n + (r_n − r_{n−1})/2.
4. **Weights and coverage.**
   - Each bin's weight is w_i = F(edge_{i+1}) − F(edge_i).
   - The coverage is Σ w_i. A bin beyond r_t contributes only the light inside r_t.
5. **Light-weighted dispersion:** ⟨σ²⟩ = Σ w_i σ_i² / Σ w_i, and σ = √⟨σ²⟩ in km s⁻¹ (column `x_gc_baumgardt_sigma`).
6. **Half-light radius at the Harris distance:** R_h = 10^Rh × R_Sun / Dist, in pc (column `x_gc_baumgardt_r_h_pc`).
7. **3D half-light radius:** r½ = (4/3) R_h (Wolf et al. 2010; registered assumption `gc_rhalf_wolf`).
8. **Luminosity:** L_V = 10^(−0.4 (M_V,t − 4.85)) in L☉ (column `x_gc_baumgardt_l_v`).
9. **Accelerations,** with σ in m s⁻¹ and r½ in m:
   - **g_obs** = 3 σ² / r½;
   - **g_bar** = G × (½ L_V Υ_V M☉) / r½².
   - No gas term: globular clusters are taken as gas-free (registered assumption `gc_gas_absent`).

## 5. The two v2 changes (D-096, D-097)

- **NGC 6715 (M54):** the `RV` bins with `<r>` greater than 200″ are dropped before steps 3 to 5. Baumgardt 2017 states: "We have therefore neglected all data points beyond 200'' in the dynamical analysis of this cluster" (arXiv 1609.08794v1, l. 588–589).
- **NGC 2298 and Pal 5:** computed as above, but recorded and not plotted. Their rows have `role = alternative` and `not_plotted_reason = other`, because their sources describe them as possibly out of equilibrium (`data/registry/excluded.csv`). The rows keep their g_obs and g_bar.

## 6. Clusters with no McLaughlin & van der Marel fit (alternative and recorded rows only)

No default row in v3 takes this path. It is used only for recorded clusters.
- **Model:** Harris Part III `c` and `r_c` are read as log₁₀(r_t/r₀) and r₀, in arcmin × 60 = arcsec. W₀ is the value whose King (1966) model has that c.
- **Radius:** R_h = r_h (Harris Part III, arcmin) × 60 / 206 264.806 × R_Sun × 1000, in pc.
- **Refused:** a `c` carrying a core-collapse flag (`c` or `c:`) is not used.

## 7. Not plotted, by rule

- **Crater (Laevens I):** recorded only; its classification is disputed (D-038 4A).
- **Pal 1:** recorded only, because the source's structural parameters are internally inconsistent (D-046).
- **Any cluster lacking one input of §2:** recorded, with the missing input named in `notes`.

## 8. Uncertainties shown with a row

These do not enter g_obs or g_bar.
- **Shifts of ⟨σ²⟩:**
  - **lower:** d_lo = √Σ (w_i/Σw × [σ_i² − max(σ_i − Δσ Low, 0)²])²;
  - **upper:** d_hi = √Σ (w_i/Σw × [(σ_i + Δσ Up)² − σ_i²])².
- **σ errors:** err_lo = σ − √(⟨σ²⟩ − d_lo) and err_hi = √(⟨σ²⟩ + d_hi) − σ (columns `x_gc_baumgardt_sigma_err_lo` and `_hi`).
- **g_obs errors:** g_obs_err_lo = g_obs × [1 − ((σ − err_lo)/σ)²] and g_obs_err_hi = g_obs × [((σ + err_hi)/σ)² − 1].
- **Other terms:** the system- and dataset-scale terms are listed in `tables/uncertainty_terms.ecsv`.
