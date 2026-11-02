# aeg-d-sparc/v2 — reproduction test (draft; frozen on merge, before conversion)

**Status: draft for JvH's review**, written 2026-11-01 before `convert.py` for v2 exists. On merge, this file's SHA-256 goes into `v2/sources.json`. It is not edited after the first v2 conversion run. If the test fails, v2 does not ship and the failure is published; the test is not changed to pass (operating rule 5).

## Purpose

v2 re-issues `aeg-d-sparc/v1` under data standard 2.2.0 (D-083). It changes **only the uncertainties**:
- it adds point-scale error columns;
- it adds an uncertainty-terms table that names every shared (system- or dataset-scale) term.

Under D-083 item 3, every observed and baryonic value must be identical to v1. v1 stays published and unchanged.

## What the source says about the uncertainties (read at source 2026-11-01)

Read from the LaTeX source of Lelli, McGaugh, Schombert & Pawlowski 2017 (arXiv:1610.08981, file `RARarXiv.tex`), §2.1.1–2.1.2 and §3.2.

- **g_obs.**
  - Eq. 2 gives δg_obs = g_obs √[(2δV_obs/V_obs)² + (2δi/tan i)² + (δD/D)²].
  - "The errors on the rotation velocity (δV_obs), disk inclination (δi), and galaxy distance (δD) are described in Paper I."
- **g_bar.**
  - "The uncertainty on g_bar is estimated considering a typical 10% error on the HI flux calibration and a 25% scatter on Υ⋆."
  - "Uncertainties in the Spitzer photometric calibration are negligible."
  - "g_bar is distance independent because both V_bar² and R linearly vary with D."
  - The mean error on g_bar is "a lower limit because it neglects uncertainties due to the adopted 3D geometry (vertical disk structure and bulge flattening) and the possible (minor) contribution of molecular gas … This may add another ∼20% uncertainty to points at small radii."
- **Scatter discussion (§3.2):** "We assume relatively small variations in Υ⋆ (0.11 dex)".

**Assignment of scales (D-083; data standard 2.2.0 §2a).** The source does not use these words. The assignment follows from what each term is.

| Term | What it is | Scale | Moves | Where its size comes from |
|---|---|---|---|---|
| Velocity | δV_obs at each radius | point | g_obs | `e_Vobs` per row (SPARC mass-model table) |
| Inclination | one inclination per galaxy | system | g_obs | `e_Inc` per galaxy (SPARC Table 1) |
| Distance | one distance per galaxy | system | g_obs only (g_bar is distance independent) | `e_D` per galaxy (SPARC Table 1) |
| HI flux calibration | one calibration per galaxy's HI data | system | g_bar (gas) | 10 %, as stated |
| Υ⋆ scatter | galaxy-to-galaxy variation of the stellar mass-to-light ratio | system | g_bar (stars) | 25 %, as stated |
| Υ⋆ normalisation | the population value adopted for all galaxies | dataset | g_bar (stars) | registry `ml_disk` (0.2–0.7) and `ml_bulge` |
| 3D geometry and molecular gas | vertical structure, bulge flattening, H₂ | system | g_bar | "∼20 % … at small radii", as stated; not quantified per point |
| Point-scale part of g_bar | — | point | g_bar | **none given by the source** |

## The test

Applied to the v2 tables, with v1 at commit `bf5c9ba` (main at the time of writing) as the reference.

1. **Values unchanged (D-083 item 3).**
   - v2 has exactly 3 391 measurement rows. Row k of v2 has the same `system_id`, `r_kpc` and `source_ref` as row k of v1.
   - `g_obs`, `g_bar` and every `g_bar_*` component column are **bit-for-bit equal** (identical float64) to v1's.
   - The systems table is identical to v1's, apart from the dataset version in identifiers.
2. **Point-scale g_obs.** For every row, `g_obs_err_point_lo` = `g_obs_err_point_hi` = g_obs · 2 · e_Vobs / V_obs, computed from the row's own `x_sparc_v_obs` and `x_sparc_e_v_obs`, to a relative tolerance of 1e-12.
3. **The decomposition reproduces the source's total.** For every row, (point term)² + (g_obs · 2 δi / tan i)² + (g_obs · δD / D)² equals v1's `g_obs_err_hi`², to a relative tolerance of 1e-9. δi and δD are the galaxy's `inclination_err_deg` (in radians) and `distance_err_mpc`.
4. **g_bar total unchanged.**
   - v2 keeps `g_bar_err_lo` and `g_bar_err_hi` equal to v1's. Their column descriptions say they are system-scale.
   - (0.10 · g_bar_gas_cold)² + (0.25 · g_bar_stars)² equals v1's `g_bar_err_hi`², to a relative tolerance of 1e-9.
   - `g_bar_err_point_*` are empty on every row.
5. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly these rows:

| term_id | scale | applies_to | moves | status | size | assumption_id |
|---|---|---|---|---|---|---|
| `inclination` | system | * | g_obs | given | size_column `inclination_err_deg`, one_sigma | `inclination` |
| `distance` | system | * | g_obs | given | size_column `distance_err_mpc`, one_sigma | `distance` |
| `hi_flux_calibration` | system | * | g_bar | given | 0.10 (fraction of the gas term), as_released | — |
| `ml_scatter_galaxy` | system | * | g_bar | given | 0.25 (fraction of the stellar term), as_released | — |
| `ml_disk` | dataset | * | g_bar | given | range 0.2–0.7 M☉/L☉ | `ml_disk` |
| `ml_bulge` | dataset | * | g_bar | given | range as registry `ml_bulge` | `ml_bulge` |
| `geometry_3d_molecular` | system | * | g_bar | given | ~0.20, as_released, "at small radii" | — |
| `g_bar_point` | point | * | g_bar | not_given_by_source | — | — |

   - Every given row cites arXiv:1610.08981 with its section, or SPARC Table 1 for the size columns.
   - `covariance` is `not_published` for every row.
6. **Standard.** `python -m aeg.validate` passes under 2.2.0, and the site builds with `aeg.site_check` at 0 errors.
7. **v1 untouched.** Every file in `aeg-d-sparc/v1/` has the checksum it had at commit `bf5c9ba`.

**Pass** = all seven hold. Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right. The Atlas carries them as the source states them.
- The v1 reproduction test against `RAR.mrt`. It applies to v2's values unchanged, because test 1 makes them identical. Its result (FAILED, 4 points, issue #8) carries over, and the same 4 rows are flagged in v2.
