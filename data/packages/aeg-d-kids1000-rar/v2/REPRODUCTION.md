# aeg-d-kids1000-rar/v2: reproduction test (draft; frozen on merge, before conversion)

**Status: draft, for JvH's approval.** Written 2026-11-04, before `convert.py` for v2 exists. No v2 value has been computed. On merge, this file's SHA-256 goes into `v2/sources.json`, and it is not edited after the first v2 conversion run. If the test fails, the failure is published, and the test is not changed to pass (operating rule 5).

**Depends on** data standard 2.5.0 (D-095, proposed), for the quantity `acceleration_released`. If D-095 is not adopted, this test is revised before freezing.

## Purpose

v2 re-issues `aeg-d-kids1000-rar/v1` (standard 1.2.1) under data standard 2.5.0 in full (D-083, D-084). It adds:
- the uncertainty terms read at source in step A (`docs/sources/uncertainty-readings.md` §1);
- the 2.0 structure: an observables table, the 2.0 measurement columns, the descriptor fields, and an independent second reading.

It changes **no value**. Every g_obs and g_bar is bit-for-bit equal to v1 (D-083 item 3). v1 stays published and unchanged.

## What the source says (read at source; full reading in `uncertainty-readings.md` §1)

Brouwer et al. 2021, A&A 650, A113 (arXiv 2106.11677, `RAR_paper_Brouwer_4.tex`), and the release README:
- **g_obs.** g_obs = 4 G ΔΣ / bias. The released `error` is "The 1-sigma error value on ESD_t" (README). The paper adds 0.1 dex to every RAR error bar for the ΔΣ-to-g_obs conversion (§4.4, l. 438). The release omits it, and the combination is not stated (K1, K2).
- **g_bar.** It is the binning coordinate: "15 logarithmic bins between 1×10⁻¹⁵ < g_bar < 5×10⁻¹² m s⁻²" (§2.1, l. 174). It has no point error by construction. Per-lens stellar-mass scatter acts through bin assignment (K8). The ±0.2 dex systematic is shown by the authors as a re-run band, not a shift (K9; D-021).
- **Alternative baryon baseline.** The released hot-gas variant adds "a nominal gas mass equal to the stellar mass" within 100 h70⁻¹ kpc (Fig. 4 caption, l. 483; K12).

## The test

Applied to the v2 tables, with v1 at commit `5dc4091` as the reference.

### A. Values unchanged (D-083 item 3)

1. v2 has exactly 45 measurement rows. Row k of v2 has the same `x_kids1000_rar_sample` and `source_ref` as row k of v1.
2. `g_obs`, `g_obs_err_lo`, `g_obs_err_hi` and `g_bar` are **bit-for-bit equal** (identical float64) to v1's. So are the four `x_kids1000_rar_*` columns.
3. `tables/covariance.ecsv` is identical to v1's, apart from the `measurement_id` prefix (`v1` → `v2`).

### B. Uncertainties (standard 2.4.0 and 2.5.0; §2a, §3, §7a)

4. **g_obs error.**
   - `g_obs_err_lo` and `g_obs_err_hi` are K1 only (point scale), as in v1. The column descriptions say so.
   - `err_level` is 0.683 and `err_level_status` is `stated`, citing the README ("1-sigma").
   - No point-scale columns are added, because the totals are already point-scale only.
5. **g_bar as the bin coordinate.**
   - Every row has `g_bar_basis = bin_coordinate`. `g_bar_err_*` and `g_bar_err_point_*` are empty.
   - `g_bar_bin_lo` and `g_bar_bin_hi` hold the edges of the source's bin k: 10^(−15 + (k−1)·Δ) and 10^(−15 + k·Δ) m s⁻², with Δ = log₁₀(5×10⁻¹²/10⁻¹⁵)/15, for row k (1 to 15) of each file.
   - **Check:** every released g_bar lies inside its row's bin. A row outside its bin is a fail, and then the bin reading of §2.1 goes to the authors.
6. **The `no_uncertainty` flag is removed.** In v1 it referred to g_bar only (#64). `g_bar_basis` now states the reason exactly, so #64 is resolved in v2. `source_quality_low` stays on the same 16 rows.
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly these rows. Each cites Brouwer et al. 2021 at the location in `uncertainty-readings.md` §1, and `covariance` is `not_published`, except K1's, which is `published` (`tables/covariance.ecsv`).

| term_id | Reading | scale | applies_to | moves | status | size | in_error_columns |
|---|---|---|---|---|---|---|---|
| `esd_to_gobs_conversion` | K2 | point | * | g_obs | given | 0.1 dex, `as_released`; `note`: the combination with the released error is not stated | `no` |
| `shear_calibration` | K4 | dataset | * | g_obs | not_given_by_source | — | — |
| `source_redshift_calibration` | K5 | dataset | * | g_obs | not_given_by_source | — (`note`: "percent-level", as stated) | — |
| `random_subtraction` | K7 | dataset | * | g_obs | given | 0.0075 (fraction of the signal), `one_sigma`, around the applied 1.85 % | — |
| `stellar_mass_per_lens` | K8 | dataset | * | g_bar | given | 0.12 dex, `as_released`, with `size_lo` 0.06 and `size_hi` 0.29 (the range the source tested); `note`: acts through bin assignment, not as an error on a bin's g_bar | — |
| `stellar_mass_systematic` | K9 | dataset | * | both | given | 0.2 dex, `as_released`; `note`: the authors re-ran the analysis with shifted masses, moving lenses between bins, so the effect is not a shift of g_bar (D-021) | — |
| `cold_gas_relation` | K11 | dataset | * | g_bar | not_given_by_source | — | — |
| `isolation_satellites` | K13 | point | * | g_obs | given | 0.30 (fraction of ΔΣ), `upper_bound`, one-sided upward; `note`: KiDS-bright below about 10⁻¹³ m s⁻², the rows flagged `source_quality_low` | — |
| `point_mass_baryons` | K14 | dataset | * | g_bar | not_given_by_source | — | — |
| `cosmology_h70` | K15 | dataset | * | both | not_given_by_source | — | — |

   Applied corrections and built-in terms (K6 lens photometric redshift, K7's applied 1.85 %, K10 normalisation to GAMA) are stated in `x_baryon_inventory` and in the measurement `method` text. They add no row beyond `random_subtraction`, whose uncertainty the source gives.

### C. 2.0 structure (D-084)

8. **Observables** (`tables/observables.ecsv`), for every measurement row:
   - one `observed` row: `delta_sigma` = ESD_t, with `err_lo` = `err_hi` = the released `error`, unit as released (h70 M☉ pc⁻²), steps `shapes;shear;excess_surface_density`;
   - one `baryonic` row: `acceleration_released` = the released g_bar, unit m s⁻², steps `photometry`, with `source_ref` naming the file, the row, and "stellar plus cold-gas mass, binned (Brouwer et al. 2021 §2.1, §4.3)". For the hot-gas variant it adds "plus nominal hot gas".
   - `evidence_tier` = 1 on every row. `observed_from` and `baryonic_from` list exactly these two rows.
9. **Measurement columns**, on every row:
   - `measured_quantity` = `g_obs`, `limit` = `none`, `evidence_tier` = 1, `kind` = `population_bin` (as v1);
   - `model_dependence` = `total_mass_form`, because the SIS deprojection assumes a density profile for the total mass (D-087; K3);
   - **KiDS-bright and GAMA rows:** `role` = `default`, `plotted` = true;
   - **Hot-gas variant rows:** `role` = `alternative`, `alternative_of` = the KiDS-bright row with the same bin index, `plotted` = false, `not_plotted_reason` = `alternative_value` (D-038; D-014 names it an alternative baseline). This is a visible change from v1, which drew all 45 rows; the variant stays in the tables and downloads.
10. **Descriptor** (`datapackage.json`):
    - `standard_version` `2.5.0`;
    - `x_selection`: isolated lenses as the source defines them (§3.3), with the lens redshift range stated by the source;
    - `x_baryon_inventory`:

      | Component | Status | Note |
      |---|---|---|
      | stars | `measured` | 9-band photometry, normalised to GAMA (K10) |
      | cold gas | `modelled` | Boselli et al. 2014 scaling relation (K11) |
      | hot gas | `known_unmeasured` | "a secure lower limit on g_bar" (§4.3); one released alternative |
      | ionised gas, dust, remnants | `not_addressed` | |

    - `x_search_log`: admitted by D-005 before search logs existed;
    - `x_second_reading`: points to `SECOND_READING.md`.
11. **Independent second reading (D-031 item 3).**
    - **Who:** a session with no access to `convert.py`, the package tables or v1.
    - **What it parses:** the three RAR files and their covariance files, from the README and the paper alone.
    - **What it writes:** every number the package uses (g_bar, ESD_t, ESD_x, error and bias, per row) and the covariance values.
    - **Pass:** every packaged number equals the second reading. A disagreement is resolved at source; one resolved against the package is a fail.
12. **The README's provenance.** The README was read from a public mirror (`uncertainty-readings.md` §1). The conversion checks that the README member of the canonical tarball (hash in `sources.json`) has SHA-256 `b3680580…8645`. If it differs, the README is re-read from the tarball before conversion, and any change is reported.
13. **Standard and site.**
    - `python -m aeg.validate` passes under 2.5.0;
    - the site builds;
    - `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes.
14. **v1 untouched.** Every file in `aeg-d-kids1000-rar/v1/` has the checksum it had at commit `5dc4091`.

**Pass** = all fourteen hold. Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right. The Atlas carries them as stated.
- The v1 reproduction test. It applies to v2's values unchanged, because test 1 makes them identical.
- How K2 combines with K1. That is with the authors (Brouwer email, sent 2026-11-02).
