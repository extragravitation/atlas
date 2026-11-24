# aeg-d-sparc/v2 — reproduction test (draft; frozen on merge, before conversion)

**Approved by JvH 2026-11-01 ("approve the SPARC test with the three amendments"); frozen on merge.** Written 2026-11-01 before `convert.py` for v2 exists. No v2 value has been computed. On merge, this file's SHA-256 goes into `v2/sources.json`. It is not edited after the first v2 conversion run. If the test fails, v2 does not ship and the failure is published; the test is not changed to pass (operating rule 5).

## Purpose

v2 re-issues `aeg-d-sparc/v1` (standard 1.2.0) under data standard 2.3.0, in full (D-083, D-084). It adds:
- point-scale error columns, and an uncertainty-terms table naming every shared (system- or dataset-scale) term;
- the 2.0 structure: an observables table, the 2.0 measurement columns, the descriptor fields, and an independent second reading of every number.

It changes **no value**.

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

Also read, from the LaTeX source of Lelli, McGaugh & Schombert 2016 (arXiv:1606.09251, file `SPARC.tex`), §2 and §3.4:
- **Gas:** "We assume a thin disk with a total mass of 1.33 M_HI, where the factor 1.33 considers the contribution of helium." V_gas "is either computed using HI surface density profiles or taken from published mass models". For D512-2, D564-8 and D631-7, "HI surface density profiles are not available, hence we compute V_gas assuming an exponential profile with a scale length of 2 R_d."
- **Molecular gas:** "We neglect the contribution of molecular gas because CO data are not available for most SPARC galaxies. Fortunately, molecules constitute a minor dynamical component …"
- **Stars:** the stellar contribution uses "the observed [3.6] surface brightness profile and extrapolating the exponential fit to R→∞, unless the profile shows a clear truncation". Bulges are decomposed non-parametrically and "linearly extrapolated at R > R_bul". "We assume that the bulge is spherical and the disk has an exponential vertical distribution with scale height z_d = 0.196 R_d^0.633."
- **Units of the components:** V_bul and V_disk are given "for Υ⋆ = 1 M☉/L☉".
- **Sample:** "SPARC is not a statistically complete sample" (§2).

**Assignment of scales (D-083; data standard 2.2.0 §2a).** The source does not use these words. The assignment follows from what each term is.

| Term | What it is | Scale | Moves | Where its size comes from |
|---|---|---|---|---|
| Velocity | δV_obs at each radius | point | g_obs | `e_Vobs` per row (SPARC mass-model table) |
| Inclination | one inclination per galaxy | system | g_obs | `e_Inc` per galaxy (SPARC Table 1) |
| Distance | one distance per galaxy | system | g_obs only (g_bar is distance independent) | `e_D` per galaxy (SPARC Table 1) |
| HI flux calibration | one calibration per galaxy's HI data | system | g_bar (gas) | 10 %, as stated |
| Υ⋆ scatter | variation of the stellar mass-to-light ratio; the source does not say whether between or within galaxies | system (**Atlas assignment**: at 3.6 µm most variation is expected between galaxies, but radial variation within a galaxy is possible and is not separated) | g_bar (stars) | 25 %, as stated |
| Υ⋆ normalisation | the population value adopted for all galaxies | dataset | g_bar (stars) | registry `ml_disk` (0.2–0.7) and `ml_bulge` |
| 3D geometry and molecular gas | vertical structure, bulge flattening, H₂ | system | g_bar | "∼20 % … at small radii", as stated; not quantified per point |
| Point-scale part of g_bar | — | point | g_bar | **none given by the source** |

## The test

Applied to the v2 tables, with v1 at commit `bf5c9ba` as the reference. Numbers in the source tables are compared at their printed precision.

### A. Values unchanged (D-083 item 3)

1. v2 has exactly 3 391 measurement rows. Row k of v2 has the same `system_id`, `r_kpc` and `source_ref` as row k of v1.
2. `g_obs`, `g_bar`, `g_bar_stars`, `g_bar_stars_disk`, `g_bar_stars_bulge` and `g_bar_gas_cold` are **bit-for-bit equal** (identical float64) to v1's.
3. The systems table has the same 175 systems, with values equal to v1's in every v1 column.

### B. Uncertainties (D-083; standard §2a, §3, §7a)

4. **Point-scale g_obs.** For every row, `g_obs_err_point_lo` = `g_obs_err_point_hi` = g_obs · 2 · e_Vobs / V_obs, from the row's own V_obs and e_Vobs, to a relative tolerance of 1e-12.
5. **The decomposition reproduces the source's total.** For every row, (point term)² + (g_obs · 2 δi / tan i)² + (g_obs · δD / D)² equals v1's `g_obs_err_hi`², to a relative tolerance of 1e-9, with the galaxy's δi (in radians) and δD.
6. **g_bar total.**
   - v2's `g_bar_err_lo` and `g_bar_err_hi` equal v1's.
   - (0.10 · g_bar_gas_cold)² + (0.25 · g_bar_stars)² equals v1's `g_bar_err_hi`², to a relative tolerance of 1e-9.
   - `g_bar_err_point_*` are empty on every row.
   - The column descriptions state the scale of each error column.
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly these rows:

| term_id | scale | applies_to | moves | status | size | assumption_id |
|---|---|---|---|---|---|---|
| `inclination` | system | * | g_obs | given | size_column `inclination_err_deg`, one_sigma | `inclination` |
| `distance` | system | * | g_obs | given | size_column `distance_err_mpc`, one_sigma | `distance` |
| `hi_flux_calibration` | system | * | g_bar | given | 0.10 (fraction of the gas term), as_released | — |
| `ml_scatter_galaxy` | system | * | g_bar | given | 0.25 (fraction of the stellar term), as_released; its `note` states that the system scale is the Atlas's assignment, that the source does not say whether the 25 % varies between or within galaxies, and that variation within a galaxy is possible | — |
| `ml_disk` | dataset | * | g_bar | given | range 0.2–0.7 M☉/L☉ | `ml_disk` |
| `ml_bulge` | dataset | * | g_bar | given | range as registry `ml_bulge` | `ml_bulge` |
| `geometry_3d_molecular` | system | * | g_bar | given | ~0.20, as_released, "at small radii" | — |
| `g_bar_point` | point | * | g_bar | not_given_by_source | — | — |

   - Every given row cites arXiv:1610.08981 with its section, or SPARC Table 1 for the size columns.
   - `covariance` is `not_published` for every row.

### C. 2.0 structure (D-084)

8. **Observables** (`tables/observables.ecsv`), one row per number the comparison uses:
   - For every measurement row:
     - one `observed` row: `v_rot` = V_obs, with err_lo = err_hi = e_Vobs, unit km/s, at the row's `r_kpc` (`3d`);
     - one `baryonic` `v_circ_component` row each for gas and stellar disc, plus one for the bulge where the galaxy's V_bul is not zero on every row. Each carries the value as released, unit km/s, at the row's `r_kpc`, with the component and (for stars) "Υ = 1 M☉/L☉" named in `source_ref`.
     - one `baryonic` `surface_brightness` row each for the stellar disc and, where present, the bulge: SBdisk and SBbul as released, unit L☉ pc⁻², band [3.6], at the row's `r_kpc`, with steps `photometry;surface_density`. They are the measured photometry from which the source computed V_disk and V_bul. The gas has no released surface density, so its record is the `v_circ_component` row only;
   - For every galaxy: one `distance` row (`observed` side, since g_bar is distance independent), with the SPARC Table 1 value and error, in Mpc.
   - **Steps:**
     - `v_rot`: `rotation_curve`. The intermediate steps differ between the original rotation-curve sources listed per galaxy in SPARC Table 1, so they are not listed.
     - Gas: `hi_21cm;surface_density;helium_factor;potential_from_density`.
     - Stellar components: `photometry;surface_density;potential_from_density`.
   - `evidence_tier` = 1 (released files) on every row.
   - Every measurement's `observed_from` lists exactly its `v_rot` row and its galaxy's `distance` row. Its `baryonic_from` lists exactly its `v_circ_component` and `surface_brightness` rows.
9. **Measurement columns.** On every row:
   - `measured_quantity` = `g_obs`, `limit` = `none`, `role` = `default`, `evidence_tier` = 1;
   - `plotted` = true, as in v1. The quality flag Q is carried as data and is never used to hide rows;
   - `model_dependence` = `observable_form` on every row of D512-2, D564-8 and D631-7, whose gas profile is assumed exponential because no HI surface density is available, with `notes` saying so. On every other row, `model_dependence` = `none`. The source's exponential extrapolation of each stellar profile beyond the last measured radius is stated in `x_baryon_inventory` and in the `geometry_3d_molecular` term's note, not in this label. A rule for this label that applies consistently across all datasets is a separate open issue.
   - The 4 rows flagged `reproduction_mismatch` in v1 (issue #8) carry the same flag.
10. **Descriptor** (`datapackage.json`):
    - `standard_version` `2.3.0`;
    - `x_selection` states SPARC's own selection in the source's words, including "not a statistically complete sample";
    - `x_baryon_inventory` lists:

      | Component | Status | Note |
      |---|---|---|
      | stars | `measured` | [3.6] photometry, Υ assumed |
      | atomic gas | `measured` | `modelled` for D512-2, D564-8, D631-7 |
      | helium | `modelled` | factor 1.33 |
      | molecular gas | `known_unmeasured` | with the source's quote |
      | hot gas | `not_addressed` | |
      | ionised gas | `not_addressed` | |
      | dust | `not_addressed` | |

    - `x_search_log` states that SPARC was admitted by D-005 before search logs existed, and that the A1 search (#48) is pending (D-084 item 4);
    - `x_second_reading` points to `SECOND_READING.md`.
11. **Independent second reading (D-031 item 3).**
    - **Who:** a session with no access to `convert.py`, the package tables or v1.
    - **What it parses:** `MassModels_Lelli2016c.mrt` and `SPARC_Lelli2016c.mrt`, from their headers and the SPARC paper alone. It reports the known header inconsistency of `SPARC_Lelli2016c.mrt` (header 113 bytes; data rows 131 characters) and how it resolved it.
    - **What it writes:** every number the package uses: per row, R, V_obs, e_Vobs, V_gas, V_disk, V_bul and D; per galaxy, D, e_D, Inc, e_Inc and Q.
    - **Pass:** every packaged number equals the second reading.
    - **Disagreements:** each is resolved at source, with the byte position. One resolved against the package is a fail.
12. **Standard and site.**
    - `python -m aeg.validate` passes under 2.3.0;
    - the site builds;
    - `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes.
13. **v1 untouched.** Every file in `aeg-d-sparc/v1/` has the checksum it had at commit `bf5c9ba`.

**Pass** = all thirteen hold. Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right. The Atlas carries them as the source states them.
- The v1 reproduction test against `RAR.mrt`. It applies to v2's values unchanged, because test 1 makes them identical. Its result (FAILED, 4 points, issue #8) carries over, and the same 4 rows are flagged in v2.
