# aeg-d-kids1000-rar/v2: reproduction test, re-issue under D-103 (frozen on merge, before conversion)

**Status: draft, revision 3, for JvH's approval.**
- This file re-issues the frozen v2 test (`REPRODUCTION.md`, SHA-256 in `v2/sources.json` once v2 is built) as D-103 rule 2 requires. That file stays as it is, unedited. **This file supersedes it** for the v2 conversion.
- The only changes are those D-103 requires:
  - KiDS-bright rows 1–8 are recorded, not plotted (item 9);
  - item 11 accepts that finding and takes the second reading from frozen files;
  - the g_bar description is corrected by the second reading (items 5 and 8);
  - one known issue is added (item 6);
  - the original test's item 11 is reported as failed (item 15);
  - the standard is 2.5.1.

  Everything else is the original test, unchanged in substance.
- **Freezing.** Written 2026-11-05, before `convert.py` for v2 exists. No v2 value has been computed. On merge, this file's SHA-256 goes into `data/frozen/kids-v2-test-rev3.json`, and the file is not edited after merge.
- **If the test fails,** v2 does not ship and the failure is published. The test is not changed to pass (operating rule 5; D-005).

**Depends on:**
- data standard 2.5.1 (D-095 for `acceleration_released`; D-099 for §12);
- D-096 (defer to the source's stated choices);
- D-098 rule 1 (same data points);
- D-103 (KiDS-bright points beyond the isolation limit).

## Purpose

v2 re-issues `aeg-d-kids1000-rar/v1` (standard 1.2.1) under data standard 2.5.1 in full (D-083, D-084). It adds:
- the uncertainty terms read at source in step A (`docs/sources/uncertainty-readings.md` §1);
- the 2.0 structure: an observables table, the 2.0 measurement columns, the descriptor fields, and an independent second reading.

It changes **no value**. Every g_obs and g_bar is bit-for-bit equal to v1 (D-083 item 3). What changes is which rows are plotted, under D-096 rules 2 and 3 (items 9 and 10). v1 stays published and unchanged.

## What the source says (read at source; full reading in `uncertainty-readings.md` §1)

Brouwer et al. 2021, A&A 650, A113 (arXiv 2106.11677, `RAR_paper_Brouwer_4.tex`), and the release README:
- **g_obs.** g_obs = 4 G ΔΣ / bias. The released `error` is "The 1-sigma error value on ESD_t" (README). The paper adds 0.1 dex to every RAR error bar for the ΔΣ-to-g_obs conversion (§4.4, l. 438). The release omits it, and the combination is not stated (K1, K2).
- **g_bar.** It is the binning coordinate: "15 logarithmic bins between 1×10⁻¹⁵ < g_bar < 5×10⁻¹² m s⁻²" (§2.1, l. 174). It has no point error by construction. **The released value is the arithmetic midpoint of its bin,** (lower edge + upper edge)/2, at the printed precision, and it is identical in all three files. It is a fixed coordinate, not a mean over the lenses. The second reading found this (`v2/reading/kids-bins.md`). It corrects step A's inference ("bin means", `uncertainty-readings.md` §1.1) and changes no value. Per-lens stellar-mass scatter acts through bin assignment (K8). The ±0.2 dex systematic is shown by the authors as a re-run band, not a shift (K9; D-021).
- **Points beyond the isolation limit (D-103).** The source leaves the KiDS-bright points beyond its isolation limit out of every model comparison:
  - "by only using the seven data points within the isolation criterion limit" (l. 508);
  - "we can only use the ESD profile of isolated KiDS-bright lenses within R < 0.3 h70⁻¹ Mpc … g_gal > 7.56×10⁻¹⁴ m s⁻²" (l. 748);
  - "Here we have removed all data points beyond the KiDS isolation limit" (l. 821).

  The reason is that photometric-redshift errors admit non-isolated lenses, which raise ΔΣ by about 30 % beyond 0.3 h70⁻¹ Mpc (l. 748). These are KiDS-bright rows 1–8, whose released g_bar (1.3822×10⁻¹⁵ to 7.3580×10⁻¹⁴) lies below 7.56×10⁻¹⁴. Rows 9–15 (from 1.2982×10⁻¹³) are the "seven data points" kept. GAMA is "still reliable within this region" (l. 489).
- **Alternative baryon baseline.** The released hot-gas variant adds "a nominal gas mass equal to the stellar mass" within 100 h70⁻¹ kpc (Fig. 4 caption, l. 483; K12).

## The test

Applied to the v2 tables, with v1 at commit `5dc4091` as the reference.

### A. Values unchanged (D-083 item 3)

1. v2 has exactly 45 measurement rows. Row k of v2 has the same `x_kids1000_rar_sample` and `source_ref` as row k of v1.
2. `g_obs`, `g_obs_err_lo`, `g_obs_err_hi` and `g_bar` are **bit-for-bit equal** (identical float64) to v1's. So are the four `x_kids1000_rar_*` columns. **Every other v1 column is unchanged**, except `flags` (test 6), `assumptions` (test 7), `notes` on the rows named in test 9, and the role, status and plotting columns set in test 9.
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
   - **A second known issue (D-103 rule 3)** is opened and linked from `known_issues.json`. The source writes the isolation limit as "R < 3 h70⁻¹ Mpc" (l. 508, 821) and as "R < 0.3 h70⁻¹ Mpc" (l. 483, 489, 748). The acceleration threshold (l. 748) and "seven data points" (l. 508) fix the rows either way.
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
   - one `baryonic` row: `acceleration_released` = the released g_bar, unit `m / s2`, steps `photometry`. Its `source_ref` names the file and row and states that the released value is the arithmetic midpoint of the source's §2.1 bin k (item 5; `v2/reading/kids-bins.md`), the coordinate at which the lenses were binned on their own g_bar. It also states the source's further steps: "per-lens stellar mass (SPS fit) plus cold gas (Boselli et al. 2014 relation), as a point mass, binned in g_bar (Brouwer et al. 2021 §2.1, §3.3, §4.3)". For the hot-gas variant it adds: "plus an assumed isothermal hot-gas halo with M_gas = M★ within 100 h70⁻¹ kpc, 'only a rough order of magnitude estimate' (§5.2, l. 512)".
   - `evidence_tier` = 1 on every row. `observed_from` and `baryonic_from` list exactly these two rows.
9. **Measurement columns**, on every row:
   - `measured_quantity` = `g_obs`, `limit` = `none`, `evidence_tier` = 1, `kind` = `population_bin` (as v1);
   - `model_dependence` = `total_mass_form`, because the SIS deprojection assumes a density profile for the total mass (D-087; K3). The assumed baryon forms (point mass; the hot-gas halo) are stated in `notes` and the inventory;
   - `stars_status`, `gas_cold_status` and `gas_hot_status` as v1, except that the hot-gas variant rows get `gas_hot_status = modelled` (D-034): their g_bar includes a gas component that is assumed, not detected. This is stated in their `notes`;
   - **GAMA rows and KiDS-bright rows 9–15:** `role` = `default`, `plotted` = true;
   - **KiDS-bright rows 1–8 (D-103; D-096 rule 2):**
     - `role` = `default`, because there is no other value for these bins;
     - `plotted` = false, `not_plotted_reason` = `other`;
     - `notes` hold the three quotations above (l. 508, 748, 821) with their locations, the reason as the source states it (l. 748), and "D-096 rule 2 (D-103): excluded by the source from its own analysis; recorded, not plotted".
     - The rows stay in the tables and downloads, and the dataset page states the exclusion and why.
     - These are bins of a population, not systems, so they have no rows in `data/registry/excluded.csv` (a register of systems; standard §5).
   - **Hot-gas variant rows:** `role` = `alternative`, `alternative_of` = the KiDS-bright row with the same bin index, `plotted` = false, `not_plotted_reason` = `alternative_value`.
     - D-014 names the variant an "alternative baseline".
     - The pairing by bin index is formal: the variant was binned on its own g_bar, so its bin k holds different lenses from the KiDS-bright bin k. Its `notes` say so.
     - Ruled under D-096 rule 3: the source calls stars plus cold gas its "fiducial estimate" and the variant "only a rough order of magnitude estimate". This changes what the site shows (v1 drew all 45 rows); the dataset page states it.
10. **Descriptor** (`datapackage.json`):
    - `standard_version` `2.5.1`;
    - **no `x_value_change_ruling`.** Under standard 2.5.1 §9 it is for "a new version's values" that differ from the previous version's. Here no value differs (tests 1–3), only plotting does, so §10 item 13 applies unchanged;
    - `x_selection`, per sample, with the bin definitions (§9):
      - KiDS-bright: z_ANN < 0.5 and m_r < 20.0, isolated (§3.3);
      - GAMA: nQ ≥ 3 and m_r,Petro < 19.8, isolated (§3.2);
      - the 15 logarithmic g_bar bins of §2.1;
    - `x_precedence`: stars plus cold gas is the source's "fiducial estimate" (§4.3, l. 421); the hot-gas variant is the alternative; KiDS-bright rows 1–8 are recorded and not plotted under D-103;
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
11. **Independent second reading (D-031 item 3), frozen before conversion.**
    - **Done.** A session with no access to `convert.py`, the package tables or v1 (other than the source URL and hashes in `v1/sources.json`) read the three RAR files, their covariance files, the README and the paper on 2026-11-05.
    - **Where it read them.** The canonical tarball was refused by the workspace proxy and was not worked around. So the files were read from the public GitHub mirror `rstpier/EFF_G_GALAXIES`, folder `KiDS Brouwer Weak Lensing/`, commit `7606a21d5e7118b49ec57aef79d357da87118346`. Their SHA-256s are in `v2/reading/kids-d096.md`.
    - **The reading files.** They are frozen by hash in `data/frozen/kids-v2-reading.json`, in the pull request that adds this test:
      - `v2/reading/kids-second-reading.csv`: g_bar, ESD_t, ESD_x, error and bias for each of the 45 rows, as printed, with the bin edges;
      - `v2/reading/kids-bins.md`: the 15 bin edges derived from §2.1;
      - `v2/reading/kids-d096.md`: the D-096 fields per file, with quotes and locations;
      - `v2/reading/scripts/read.py`: the parser.
    - **The covariance reading is not committed.** `kids-covariance.csv` transcribes the released covariance files in full, and the release is not redistributable (`v1/sources.json`). The freeze record holds its SHA-256 instead. The conversion regenerates it with `read.py` from the fetched release and checks that hash; **a mismatch is a fail**.
    - **D-096 fields.** The reading's findings are exactly:
      - the hot-gas variant as a non-fiducial alternative (already in test 9);
      - KiDS-bright rows 1–8 excluded by the source (D-103; test 9).

      These two are applied and no others. The reading found no preferred value, and no exclusion in GAMA or the README.
    - **Pass:**
      - every packaged number equals the frozen reading, at the printed precision;
      - the packaged covariance equals the regenerated covariance reading, divided by the bias column as the README states and converted to g_obs units as v1 does;
      - each row's plotting status matches the D-096 fields above.

      Any mismatch is a fail.
12. **The README's provenance.** The README was read from a public mirror (`uncertainty-readings.md` §1; again by the second reading, item 11), whose SHA-256 is `b3680580696c5dbf5671c700d5e8f90fbfd1dc614fa7e3e07b2f66d1624e8645`. The canonical tarball (hash in `v1/sources.json`) is not reachable from the workspace, so this is checked by CI as the first step of the conversion: the tarball's README member must have exactly this hash. **A mismatch is a fail**, because tests 4 and 8 rest on the README's wording.
13. **Standard and site.**
    - `PYTHONPATH=pipeline python -m aeg.validate data/packages/aeg-d-kids1000-rar/v2` passes under 2.5.1;
    - the site builds;
    - `aeg.site_check` reports 0 errors;
    - the reproduction ledger's hash check passes.
14. **v1 untouched.** Every file in `aeg-d-kids1000-rar/v1/` has the checksum it had at commit `5dc4091`.
15. **The original test's item 11 is reported as failed** (D-103 rule 2). `REPRODUCTION_RESULT.md` states, before the item-by-item result, that the frozen `REPRODUCTION.md` item 11 failed: its second reading found an exclusion beyond the hot-gas variant. It also states that this re-issue was written by ruling (D-103) before any v2 value existed. The other items of the original test are scored as they are restated here.

## Order of work (against steering)

1. **Second reading:** done and frozen with this test (item 11).
2. **Conversion:**
   - `convert.py` takes the D-096 findings and plotting status only from `v2/reading/kids-d096.md` and this test. It contains no other row-specific rule.
   - CI checks the tarball's README hash (item 12) and the regenerated covariance reading's hash (item 11) before the tables are written.
3. **Scoring.** The first complete conversion is the scored run. A fault found after scoring is published as a fail, with its reason; it is not fixed and re-scored.

**Pass** = all fifteen hold. Anything else is a fail.

## Not tested here

- Whether the source's error sizes are right. The Atlas carries them as stated.
- The v1 reproduction test. It applies to v2's values unchanged, because test 1 makes them identical.
- How K2 combines with K1. That is with the authors (Brouwer email, sent 2026-11-02).
- Whether the KiDS-bright rows 1–8 are right. The Atlas follows the source's own exclusion (D-103) and states it.
