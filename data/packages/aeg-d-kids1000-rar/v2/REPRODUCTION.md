# aeg-d-kids1000-rar/v2: reproduction test (draft; frozen on merge, before conversion)

**Status: draft, revision 2, for JvH's approval.** Revision 2 answers an independent review (`docs/sources/readings/step-d-2026-11-04/kids-review-1.md`). Written 2026-11-04, before `convert.py` for v2 exists. No v2 value has been computed. On merge, this file's SHA-256 goes into `v2/sources.json`, and it is not edited after the first v2 conversion run. If the test fails, v2 does not ship and the failure is published; the test is not changed to pass (operating rule 5; D-005).

**Depends on** data standard 2.5.0 (D-095), for the quantity `acceleration_released`, and on D-096 (defer to the source's stated choices).

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
2. `g_obs`, `g_obs_err_lo`, `g_obs_err_hi` and `g_bar` are **bit-for-bit equal** (identical float64) to v1's. So are the four `x_kids1000_rar_*` columns. **Every other v1 column is unchanged**, except `flags` (test 6), `assumptions` (test 7), and the role, status and plotting columns set in test 9.
3. `tables/covariance.ecsv` is identical to v1's, apart from the `measurement_id` prefix (`v1` → `v2`).

### B. Uncertainties (standard 2.4.0 and 2.5.0; §2a, §3, §7a)

4. **g_obs error.**
   - `g_obs_err_lo` and `g_obs_err_hi` are K1 only (point scale), as in v1. The column descriptions say so.
   - `err_level` is 0.683 and `err_level_status` is `stated`, citing the README ("1-sigma").
   - No point-scale columns are added, because the totals are already point-scale only.
5. **g_bar as the bin coordinate.**
   - Every row has `g_bar_basis = bin_coordinate`. `g_bar_err_*` and `g_bar_err_point_*` are empty.
   - `g_bar_bin_lo` and `g_bar_bin_hi` hold the edges of the source's bin k: 10^(−15 + (k−1)·Δ) and 10^(−15 + k·Δ) m s⁻², with Δ = log₁₀(5×10⁻¹²/10⁻¹⁵)/15 ≈ 0.2466, for row k (1 to 15) of each file, to a relative tolerance of 1e-12. The source states these bins in general (§2.1, l. 174). That the hot-gas file uses the same edges is the Atlas's inference, stated in its rows' `notes`.
   - **Check:** every released g_bar lies inside its row's bin. A row outside its bin is a fail. This check is not blind: the step A reading already found that the released values fall inside these bins (`uncertainty-readings.md` §1.1).
6. **The `no_uncertainty` flag is removed.** In v1 it referred to g_bar only (#64). Under §3, `g_bar_basis = bin_coordinate` now states the reason exactly (no point error by construction), so #64 is resolved in v2. `source_quality_low` stays on the same 16 rows as v1. For the hot-gas rows this carries v1's use of the KiDS-bright g_bar limit, which may under-flag them, because the source's limit is a radius (R > 0.3 h70⁻¹ Mpc, App. A l. 748). This is disclosed in the K13 term's note and opened as a known issue; the flags are not changed in a no-change re-issue.
7. **Uncertainty terms.** `tables/uncertainty_terms.ecsv` contains exactly these rows.
   - Each cites Brouwer et al. 2021 at the location in `uncertainty-readings.md` §1, and `covariance` is `not_published` on every row. (K1's covariance is in `tables/covariance.ecsv`; K1 is in the error columns, so it has no row, §7a.)
   - Every row's `note` names the sample(s) it applies to: KiDS-bright, GAMA, the hot-gas variant, or all.

| term_id | Reading | scale | applies_to | moves | status | size | in_error_columns |
|---|---|---|---|---|---|---|---|
| `esd_to_gobs_conversion` | K2 | point | * | g_obs | given | 0.1 dex, `as_released`; `note`: added by the paper to every RAR error bar; the combination with the released error is not stated; all samples | `no` |
| `shear_calibration` | K4 | dataset | * | g_obs | not_given_by_source | — (`note`: the correction μ ≈ 0.014 is applied; its uncertainty is not stated) | — |
| `source_redshift_calibration` | K5 | dataset | * | g_obs | not_given_by_source | — (`note`: "percent-level", as stated) | — |
| `random_subtraction` | K7 | dataset | * | g_obs | not_given_by_source | — (`note`: the subtracted random-point profile is described as "only 1.85 ± 0.75 %" of the signal; KiDS-bright) | — |
| `stellar_mass_per_lens_kids` | K8 | dataset | * | both | given | 0.12 dex, `one_sigma`; `note`: KiDS-bright only; acts through bin assignment, not as an error on a bin's g_bar, so it also moves g_obs; the source also tested 0.29 dex and states its conclusions do not change | — |
| `stellar_mass_per_lens_gama` | — | dataset | * | both | not_given_by_source | — (`note`: GAMA stellar masses are Taylor et al. 2011; this paper states no per-lens scatter for them) | — |
| `stellar_mass_systematic` | K9 | dataset | * | both | given | 0.2 dex, `as_released`; `note`: the authors re-ran the analysis with shifted masses, moving lenses between bins, so the effect is not a shift of g_bar (D-021); all samples | — |
| `gama_normalisation` | K10 | dataset | * | g_bar | not_given_by_source | — (`note`: KiDS-bright masses were shifted by +0.056 dex to the GAMA mean; the uncertainty of that shift is not stated) | — |
| `cold_gas_relation` | K11 | dataset | * | g_bar | not_given_by_source | — | — |
| `isolation_satellites` | K13 | dataset | * | g_obs | given | 0.30 (fraction of ΔΣ), `as_released`, one-sided upward, from the source's MICE test; `note`: KiDS-bright rows below about 10⁻¹³ m s⁻², flagged `source_quality_low`; the hot-gas rows' flags follow v1 and may under-flag (test 6) | — |
| `cosmology_h70` | K15 | dataset | * | both | not_given_by_source | — | — |

   - **Not uncertainty terms (§2a rule 4):** the point-mass baryon model (K14) and the SIS deprojection (K3) are assumptions. They are entries in the registry and in each row's `assumptions` (`deproj_lensing=sis` as in v1, plus `baryons_point_mass`). The stellar population model and IMF (BC03, Chabrier; §3.3, l. 349 and 362) are stated in `x_baryon_inventory`.
   - **Built-in terms** (K6, the lens photometric redshift inside Σ_crit) are stated in the measurement `method` text.

### C. 2.0 structure (D-084)

8. **Observables** (`tables/observables.ecsv`), for every measurement row:
   - one `observed` row: `delta_sigma` = ESD_t, with `err_lo` = `err_hi` = the released `error`, unit `solMass / pc2` (with h = 0.7, as the source; stated in the descriptor), steps `shapes;shear;excess_surface_density`;
   - one `baryonic` row: `acceleration_released` = the released g_bar, unit `m / s2`, steps `photometry`, with `source_ref` naming the file and row, and stating the source's further steps: "per-lens stellar mass (SPS fit) plus cold gas (Boselli et al. 2014 relation), as a point mass, binned in g_bar (Brouwer et al. 2021 §2.1, §3.3, §4.3)". For the hot-gas variant it adds: "plus an assumed isothermal hot-gas halo with M_gas = M★ within 100 h70⁻¹ kpc, 'only a rough order of magnitude estimate' (§5.2, l. 512)".
   - `evidence_tier` = 1 on every row. `observed_from` and `baryonic_from` list exactly these two rows.
9. **Measurement columns**, on every row:
   - `measured_quantity` = `g_obs`, `limit` = `none`, `evidence_tier` = 1, `kind` = `population_bin` (as v1);
   - `model_dependence` = `total_mass_form`, because the SIS deprojection assumes a density profile for the total mass (D-087; K3). The assumed baryon forms (point mass; the hot-gas halo) are stated in `notes` and the inventory;
   - `stars_status`, `gas_cold_status` and `gas_hot_status` as v1, except that the hot-gas variant rows get `gas_hot_status = modelled` (D-034): their g_bar includes a gas component that is assumed, not detected. This is stated in their `notes`;
   - **KiDS-bright and GAMA rows:** `role` = `default`, `plotted` = true;
   - **Hot-gas variant rows:** `role` = `alternative`, `alternative_of` = the KiDS-bright row with the same bin index, `plotted` = false, `not_plotted_reason` = `alternative_value`.
     - D-014 names the variant an "alternative baseline".
     - The pairing by bin index is formal: the variant was binned on its own g_bar, so its bin k holds different lenses from the KiDS-bright bin k. Its `notes` say so.
     - Ruled under D-096 rule 3: the source calls stars plus cold gas its "fiducial estimate" and the variant "only a rough order of magnitude estimate". This changes what the site shows (v1 drew all 45 rows); the dataset page states it.
10. **Descriptor** (`datapackage.json`):
    - `standard_version` `2.5.0`;
    - `x_selection`, per sample, with the bin definitions (§9):
      - KiDS-bright: z_ANN < 0.5 and m_r < 20.0, isolated (§3.3);
      - GAMA: nQ ≥ 3 and m_r,Petro < 19.8, isolated (§3.2);
      - the 15 logarithmic g_bar bins of §2.1;
    - `x_precedence`: stars plus cold gas is the source's "fiducial estimate" (§4.3, l. 421); the hot-gas variant is the alternative;
    - `x_baryon_inventory`:

      | Component | Status | Note |
      |---|---|---|
      | stars | `measured` | per sample: KiDS-bright, 9-band LePhare SPS (BC03, Chabrier), normalised to GAMA (K10); GAMA, Taylor et al. 2011 ugrizZY SPS (BC03, Chabrier) |
      | cold gas | `modelled` | Boselli et al. 2014 scaling relation (K11) |
      | hot gas | `known_unmeasured` | "a secure lower limit on g_bar" (§4.3, l. 421); one released alternative with an assumed halo |
      | cool and warm (ionised) gas, dust | `known_unmeasured` | discussed by the source and not counted (§4.3, l. 419; §5.2, l. 512) |
      | remnants | `not_addressed` | |

    - `x_search_log`: admitted by D-005 before search logs existed;
    - `x_second_reading`: points to `SECOND_READING.md`.
11. **Independent second reading (D-031 item 3).**
    - **Who:** a session with no access to `convert.py`, the package tables or v1.
    - **What it parses:** the three RAR files and their covariance files, from the README and the paper alone.
    - **What it writes:** every number the package uses (g_bar, ESD_t, ESD_x, error and bias, per row) and the covariance values.
    - It also derives the bin edges from §2.1 independently.
    - **D-096 fields.** It records whether the source or README marks a preferred value, excludes data, or names a fiducial baseline, for every file used. Any finding beyond the hot-gas variant (already applied) is a fail of this test, because this version may not change values: the test is then revised, by ruling, to a value-changing version under D-096 rule 5.
    - **Pass:** every packaged number equals the second reading, at the printed precision. A disagreement is resolved at source; one resolved against the package is a fail.
12. **The README's provenance.** The README was read from a public mirror (`uncertainty-readings.md` §1), whose SHA-256 is `b3680580696c5dbf5671c700d5e8f90fbfd1dc614fa7e3e07b2f66d1624e8645`. The canonical tarball (hash in `v1/sources.json`) is not reachable from the workspace, so this is checked by CI as the first step of the conversion: the tarball's README member must have exactly this hash. **A mismatch is a fail**, because tests 4 and 8 rest on the README's wording.
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
