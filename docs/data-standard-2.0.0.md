# Atlas data standard

**Version 2.0.0 — FROZEN 2026-10-29** (D-029, D-041; incorporates D-033 to D-039). Frozen by hash in `data/frozen/data-standard-2.0.0.json` before the first 2.0 package was converted; `python -m aeg.check` fails if this file changes. The next change is a new version with its own file and freeze record. Version 1.3.0 is kept unchanged in `docs/data-standard-1.3.0.md`; packages that state 1.x are valid under that text and are never edited (references to "docs/data-standard.md §7" inside 1.x packages mean the 1.3.0 text).

What changed from 1.3.0, in one line: every measurement now keeps **what was observed** (observables table) as well as g_obs and g_bar, and records how it was selected, how strong the evidence is, how much it leans on fitted forms, whether it is plotted and why not, and which value is the default when several exist.

## 0. Versioning

Semantic versioning, MAJOR.MINOR.PATCH, as in 1.x: **patch** = wording with no effect on any file; **minor** = additive and backward-compatible (new optional column, new closed-list value, new ladder step); **major** = breaking (renaming, removing or retyping a column; changing a unit or a meaning; making something required). Every change gets a decision-log entry and a changelog line. A package is never edited to follow a newer version; it is re-issued as a new dataset version (D-006).

## Version history

| Version | Date | Decision | Change |
|---|---|---|---|
| 1.0.0–1.3.0 | 2026-10-28 | D-015, D-018, D-019, D-014 | See `docs/data-standard-1.3.0.md` |
| 2.0.0 | 2026-10-29 | D-029, D-041 (with D-033–D-039) | Observables table; selection, baryon inventory and precedence in the descriptor; evidence tier, model dependence, limits and confidence levels; plotted/not-plotted with reason; default and alternative values; kind and label per system; distance or redshift required and never kinematic; per-star table; frozen checks referenced; second reading recorded |

## 1. Package layout

One folder per dataset version: `data/packages/<dataset>/<version>/`.

| Path | Content | Required |
|---|---|---|
| `datapackage.json` | Descriptor (§9): name, version, standard version, sources, licence per source record, selection, baryon inventory, precedence, frozen checks | yes |
| `SOURCE.md` | What was read at source: addresses, dates, licence text or its absence, citation, method summary, search-log row (`docs/sources/search-log-<cell>.md`) | yes |
| `sources.json` | Every source file: address, file name, bytes, SHA-256, retrieval date, redistributable (true/false), evidence tier | yes |
| `REPRODUCTION.md` | Published numbers the package must reproduce, and the tolerance; committed, with its hash in `sources.json`, before `convert.py` first runs | yes |
| `SECOND_READING.md` | The independent second reading (D-031 item 3): for every number entering the package, the reader, the quote and its location, and any disagreement with the first reading and how it was resolved | yes |
| `convert.py` | Fetches sources (verifying hashes), converts, writes `tables/` | yes |
| `tables/observables.ecsv` | §4 | yes |
| `tables/measurements.ecsv` | §3 | yes |
| `tables/systems.ecsv` | §5 (omitted for population-only datasets) | for systems |
| `tables/stars.ecsv` | §6: released per-star velocities used by the D-037 reproduction check, only if the source may be redistributed (otherwise referenced by hash in `sources.json`) | where used |
| `tables/covariance.ecsv` | §7 | where the source gives covariance |
| `tests/` | Reproduction, schema and assumption tests | yes |
| `checks/` | Results of frozen checks run on this package (D-037 reproduction, D-038 consistency, D-039 cross-check), each with the frozen check's hash | where a check applies |
| `known_issues.json` | Known issues, as 1.2.0 | optional |
| `checksums.sha256` | SHA-256 of every committed file in the package | yes |
| `source/` | Downloaded source files | **never committed** |

## 2. Table format, units and conventions

ECSV 1.0, comma-delimited, with `name`, `datatype`, `unit`, `description` (Technical vocabulary) and `meta: {ucd: …}` (IVOA UCD1+ v1.6, validated) on every column, and the dataset ID, version and standard version in the file header. Plain CSV and Parquet copies are generated at build time, never committed.

| Quantity | Unit | Notes |
|---|---|---|
| Accelerations | m s⁻² | Stored linear |
| Radius | kpc | Physical; `r_kind` = `3d` or `projected` |
| Mass | M☉ (`solMass`) | |
| Velocity, velocity dispersion | km s⁻¹ | |
| Distance | Mpc | |
| Luminosity | L☉ in the stated band (`solLum`), band in the column description and `band` | |
| Surface brightness | mag arcsec⁻² or L☉ pc⁻², as the source gives it | |
| Angles | deg (arcsec where the source does) | |

- **No silent rescaling.** H0-dependent values keep the source's H0, stated in the descriptor; any rescaling is a named assumption. No conversion between redshift and distance without a registered assumption (D-033).
- **Uncertainties:** lower and upper bounds as separate non-negative columns (`_err_lo`, `_err_hi`). The interval's **confidence level** is in `err_level` (fraction, e.g. 0.683, 0.95); empty means 0.683. A missing uncertainty is an empty cell plus the flag `no_uncertainty`, never zero.
- **Limits:** a value that is a limit has `limit` = `upper` or `lower`, the limit in the value column, its confidence level in `err_level`, and empty error columns. Limits are drawn as arrows and never converted into values.
- **Signs:** g_bar components keep their sign (a component's acceleration is V·|V|/R).
- **Missing values:** empty cell, never a sentinel number.

## 3. Measurements table (`tables/measurements.ecsv`)

One row per measurement of the comparison: one place in one system, or one population bin.

| Column | Type | Unit | Required | Meaning |
|---|---|---|---|---|
| `measurement_id` | string | | yes | `aeg-d-<name>/v<N>/m000001`, sequential |
| `system_id` | string | | for systems | `aeg-s-000001`; empty for population bins |
| `kind` | closed list | | yes | Row type: `profile_point`, `system_value`, `population_bin` |
| `channel` | closed list | | yes | `dynamics`, `lensing` |
| `method_class` | closed list | | yes | `kinematic`, `hydrostatic`, `lensing`, `ephemeris` (new) |
| `method` | string | | yes | Source method in words |
| `r_kpc`, `r_kind` | float64, closed list | kpc | if defined | Radius and whether it is `3d` or `projected` |
| `measured_quantity` | closed list | | yes | `g_obs` (the observed acceleration is measured) or `delta_g` (the difference from the Newtonian prediction is measured directly, as for Solar System bounds) |
| `g_obs`, `g_obs_err_lo`, `g_obs_err_hi` | float64 | m / s2 | `g_obs` required when `measured_quantity = g_obs` | Observed acceleration and bounds |
| `delta_g`, `delta_g_err_lo`, `delta_g_err_hi` | float64 | m / s2 | when `measured_quantity = delta_g` | Measured g_obs − g_bar (signed), as the source gives it, with the source's sign convention in `method` |
| `limit` | closed list | | yes | `none`, `upper`, `lower`: applies to the measured quantity |
| `err_level` | float64 | | no | Confidence level of the interval or limit; empty = 0.683 |
| `g_bar`, `g_bar_err_lo`, `g_bar_err_hi` | float64 | m / s2 | `g_bar` yes | Newtonian acceleration from detected baryons, at catalogue defaults |
| `g_bar_stars`, `g_bar_stars_disk`, `g_bar_stars_bulge`, `g_bar_gas_cold`, `g_bar_gas_hot` | float64 | m / s2 | where separable | Components at catalogue defaults |
| `stars_status`, `gas_cold_status`, `gas_hot_status` | closed list | | yes | `measured`, `modelled`, `absent`, `not_separable` (D-034) |
| `observed_from` | string | | yes | Semicolon-separated `observable_id`s used for the observed side |
| `baryonic_from` | string | | yes | The same for g_bar |
| `model_dependence` | closed list | | yes | `none`, `observable_form` (a functional form fitted to an observable, e.g. fitted dispersion profile, aperture correction), `total_mass_form` (a form assumed for the total mass, e.g. NFW) (D-029) |
| `evidence_tier` | integer | | yes | 1 released files; 2 printed tables or text; 3 digitised figures (D-035) |
| `role` | closed list | | yes | `default` or `alternative` (D-038 §3; §9 `x_precedence`) |
| `alternative_of` | string | | if `role = alternative` | The `measurement_id` (any package) of the default it is an alternative to, or empty if the default is not yet packaged (then `x_precedence` explains) |
| `plotted` | bool | | yes | Whether default views plot the row |
| `not_plotted_reason` | closed list | | if `plotted` is false | `coverage_below_threshold` (D-036 ii), `aperture_uncorrected` (D-036 iii), `central_only` (D-038 1B), `members_within_half_light` (D-038 1A), `proper_motion_only` (D-036), `tier_3` (D-035), `alternative_value` (D-038), `limit_only`, `epoch_gap` (D-033), `kinematic_distance` (D-036 #6), `other` (explained in `notes`) |
| `assumptions` | string | | yes | Semicolon-separated `id=value` for every inference step on both sides, adjustable or not (D-029 2b) |
| `adjustable` | string | | yes | Assumption IDs whose sliders can change the row |
| `quality_source` | string | | no | Source's own quality label, verbatim; never used to hide data by default |
| `source_ref` | string | | yes | Pointer to the source row, file and column |
| `flags` | string | | no | §11 closed list |
| `known_issues` | string | | no | GitHub issue numbers |
| `notes` | string | | no | Short free text where a closed list says `other` |

Rules:
- g_bar is always Newtonian from detected baryons at catalogue defaults; slider effects are computed from stored components and registry formulas, never stored as rows.
- Where `measured_quantity = delta_g`, `g_obs` may be stored as `g_bar + delta_g` for plotting, and is then flagged `derived_from_delta_g`.
- Masses from scaling relations never enter the observed side (D-029). Nothing on either side may be derived from the system's own kinematics or acceleration (D-036 #6): a row that would need such an input is `plotted = false` with the reason, or not converted.

## 4. Observables table (`tables/observables.ecsv`)

One row per published value of what was observed or of a quantity the comparison is computed from (D-029 2a).

| Column | Type | Unit | Required | Meaning |
|---|---|---|---|---|
| `observable_id` | string | | yes | `aeg-d-<name>/v<N>/o000001`, sequential |
| `system_id` | string | | for systems | As in measurements; empty for population bins |
| `side` | closed list | | yes | `observed` (feeds g_obs or delta_g) or `baryonic` (feeds g_bar) |
| `quantity` | closed list | | yes | §4a |
| `value`, `err_lo`, `err_hi` | float64 | per row | yes (errors if given) | As the source gives them |
| `unit` | string | | yes | Astropy unit string |
| `band` | string | | for photometric quantities | Photometric band as the source names it |
| `limit`, `err_level` | as §3 | | yes / no | |
| `r_kpc`, `r_kind` | | kpc | for profiles | Radius of the value; for a bin, its representative radius |
| `r_in_kpc`, `r_out_kpc` | float64 | kpc | for binned profiles | Bin edges as the source gives them; empty if not given (then edges are inferred under D-036 and the measurement is flagged `edges_inferred`) |
| `steps` | string | | yes | Processing steps the source performed, as semicolon-separated step IDs from the tracer's ladder (§4b), ending with the last step the source performed |
| `evidence_tier` | integer | | yes | 1, 2 or 3 |
| `in_text` | bool | | no | True where the value is printed in running text rather than a table (D-038 5A; tier 2) |
| `source_ref` | string | | yes | Pointer to the source row, table, page or figure |

### 4a. Quantities (closed list; new values by minor version)

Observed side: `v_rot`, `sigma_los`, `sigma_los_second_moment` (includes rotation; D-038 2A), `sigma_los_about_rotation`, `sigma_pm`, `velocity_gradient`, `temperature_x`, `density_e`, `pressure_e`, `mass_hse`, `delta_sigma`, `kappa`, `einstein_radius`, `binary_sep_proj`, `binary_dv_proj`, `delta_g_bound`, `extra_mass_bound`, `perihelion_precession_extra`.
Baryonic side: `luminosity`, `apparent_magnitude`, `absolute_magnitude`, `surface_brightness`, `structural_param` (with the parameter named in `source_ref`, e.g. King r_c, r_t; Plummer a; Sérsic R_e, n), `half_light_radius`, `metallicity_feh`, `age`, `stellar_ml_population` (a stellar-population mass-to-light ratio, D-039), `star_formation_history_ml`, `mass_star`, `mass_star_counted` (D-036 #3), `surface_density_hi`, `mass_hi`, `mass_gas`, `mass_gas_limit`, `line_flux_co`, `known_mass` (Solar System bodies, as used in an ephemeris).
Both sides: `distance`, `redshift`.

### 4b. Ladders of processing steps (per tracer)

Step IDs are fixed here; a package lists the ones the source performed, in order. New steps are added by minor version with the first package that needs them.

| Tracer | Ladder |
|---|---|
| Random motions, resolved stars | `spectra` → `stellar_velocities` → `membership` → `binary_treatment` → `dispersion_global` or `dispersion_profile` → (Atlas) `light_weighting` (D-036 ii) → (Atlas) `half_light_estimator` (D-025) |
| Random motions, integrated light | `integrated_spectra` → `aperture_dispersion` → `aperture_correction_global` or `aperture_correction_central` → (Atlas) `half_light_estimator` |
| Random motions, proper motions | `astrometry` → `proper_motions` → `membership` → `dispersion_pm` (recorded, not plotted in v1.0) |
| Rotation | `spectra` → `line_velocities` → `velocity_field` → `tilted_ring` → `inclination` → `pressure_correction` → `rotation_curve` → (Atlas) `centripetal` (g = V²/R) |
| Hot gas | `events` → `spectra` → `projected_t_and_density` → `deprojected_profiles` → `fitted_forms` → `hydrostatic_mass` → (Atlas) `newtonian_g` |
| Weak lensing | `shapes` → `shear` → `excess_surface_density` → `deprojection` → (Atlas) `newtonian_g` |
| Strong lensing | `image_positions` → `lens_model` → `einstein_radius` → `projected_mass` |
| Solar System | `observations` → `ephemeris_fit` → `extra_term_fit` → `bound` |
| Stellar mass | `photometry` → `luminosity` → `structural_model` → (Atlas) `stellar_ml` (D-039); or `star_counts` → `mass_function` → `mass_star_counted` |
| Gas | `hi_21cm` or `co_line` or `xray` → `surface_density` or `mass` → `helium_factor` |

Steps marked (Atlas) are performed by the Atlas with frozen code; all others are the source's.

## 5. Systems table (`tables/systems.ecsv`)

The global registry `data/registry/systems.csv` is unchanged. Per package:

| Column | Unit | Required | Meaning |
|---|---|---|---|
| `system_id` | | yes | From the registry |
| `name_in_source` | | yes | Exactly as the source writes it |
| `class_in_source` | | yes | The source's class label, verbatim |
| `taxonomy_kind` | | yes | Taxonomy kind ID `A0`–`A10` (TAXONOMY.md), assigned by what the system is, never by its measured discrepancy |
| `kind_label` | | yes | The source's kind label where sources agree; otherwise `ambiguous: dwarf galaxy or star cluster` (or the analogous pair), placing the system in A7 (D-036 #7, D-037, D-038 §4) |
| `host` | | where relevant | Host galaxy, as a property; never a filter (D-037) |
| `distance_mpc`, `distance_err_mpc` | Mpc | `distance_mpc` or `redshift` required (D-033) | As the source or a cited independent source gives it |
| `distance_method` | | with distance | As stated by the source of the distance |
| `distance_kinematic` | | yes | True if the distance was derived from the system's own kinematics; such a distance is never used (D-036 #6), so it must be false for any plotted row |
| `distance_ref` | | with distance | Citation of the distance used, when not the dataset's own source |
| `redshift`, `redshift_err` | | see above | As given |
| `ra_deg`, `dec_deg` | deg | where given | |
| `metallicity_feh` | | where given | As the source gives it; continuous; never a classifier |
| `inclination_deg`, `inclination_err_deg` | deg | optional | As 1.1.0 |
| `properties` | | no | JSON of other source-given properties, units in key names |

Cross-identifications: `data/registry/crossids.csv` gains `independent_data` (true or false). Exclusions: `data/registry/excluded.csv` (system, dataset, reason, citation), shown on the site.

## 6. Per-star table (`tables/stars.ecsv`, where used)

For the D-037 reproduction check, when the source releases per-star velocities and permits redistribution.

| Column | Unit | Meaning |
|---|---|---|
| `system_id` | | |
| `star_id_in_source` | | As the source gives it |
| `v_los`, `v_los_err` | km / s | As the source gives them |
| `member`, `p_member` | | The source's flag and/or probability |
| `binary_flag` | | The source's binary or velocity-variable flag |
| `r_proj_kpc` or `r_proj_arcmin` | kpc / arcmin | Projected radius, where given |
| `source_ref` | | Row pointer |

If the source does not permit redistribution, the check reads the source file by hash and nothing is committed.

## 7. Covariance (`tables/covariance.ecsv`)

As 1.x: `measurement_id_i`, `measurement_id_j`, `quantity`, `covariance` (converted with the same formula as the values). Only where the source provides covariance.

## 8. Assumption registry (`data/assumptions.json`)

As 1.3.0 (`id`, both names, `applies_to`, `parameter` with default and published range read at source, `effects` as formulas, `adjustable`, `scope`, `status`), plus:

| Field | Meaning |
|---|---|
| `role` | `observed_inference`, `baryonic_inference` or `selection` (D-029 2c) |
| `range_basis` | For each end of the range, what sets it and where it was read (ranges may be asymmetric, D-039) |
| `evidence` | Evidence bearing on the default read at source after it was set, with its direction (e.g. D-039: cluster mass functions suggest fewer low-mass stars than the default) |
| `not_adjustable_reason` | For fixed steps (e.g. `gr_lensing`, `hydrostatic_equilibrium`, `circular_orbits`): "assumed by the source; not tested by the Atlas" or another stated reason |

Formula language and combination rules: unchanged from 1.3.0 (D-014).

## 9. Descriptor additions (`datapackage.json`)

| Key | Required | Content |
|---|---|---|
| `standard_version` | yes | `2.0.0` |
| `licenses` | yes | Per source record, read at source (CDS records vary); derived tables follow share-alike terms where they apply |
| `x_selection` | yes | The sample's selection as structured entries (`quantity`, `condition`, `value`, `citation`) plus the source's own wording; for population bins, the bin definitions and the lenses' redshift range or distribution (D-029 2d, D-033) |
| `x_baryon_inventory` | yes | One entry per component (stars by population, atomic gas, helium, molecular gas, ionised gas, hot gas, intracluster light, dust, remnants as relevant), each with status `measured`, `modelled`, `known_unmeasured`, `stated_negligible` (quoted), `absent_limit` (a measured upper limit, system-specific), `absent_literature_limit` (the kind's literature limit, D-036 #4) or `not_addressed`, and the citation where it was read |
| `x_precedence` | where any row has `role` | Which dataset is the default for each system and why, under D-038 §3 (originals first; per-star velocities released; most members; most recent; Geha et al. 2026 only where unique) |
| `x_checks` | where a check applies | Each frozen check run on the package: its freeze record (`data/frozen/*.json`), the hash it was run with, and the result file in `checks/` |
| `x_search_log` | yes | The search-log file and row(s) (R numbers) that admitted the dataset |
| `x_second_reading` | yes | Who performed the second reading and when (D-031 item 3); details in `SECOND_READING.md` |

## 10. Validation (automated; fails the build)

All 1.3.0 items, plus:
1. `observables.ecsv` present; IDs well-formed, unique, sequential; `side` and `quantity` in the closed lists; every `steps` entry from the ladder for its tracer.
2. Every `observed_from` and `baryonic_from` ID exists in the package's observables, and the sides match.
3. `model_dependence`, `evidence_tier`, `limit`, `role`, `plotted` present on every row; `not_plotted_reason` present exactly when `plotted` is false; `alternative_of` present when `role = alternative`.
4. Rows with `evidence_tier = 3` are `plotted = false` (D-035: never in default views).
5. A row with `limit` not `none` has empty error columns and a value in the measured quantity.
6. `measured_quantity = g_obs` rows have `g_obs`; `delta_g` rows have `delta_g` (or a limit on it).
7. Systems: `taxonomy_kind` in A0–A10; `kind_label` present; `distance_mpc` or `redshift` present; any plotted row's system has `distance_kinematic = false`; systems whose `kind_label` begins `ambiguous` have `taxonomy_kind = A7`.
8. Descriptor: `x_selection`, `x_baryon_inventory`, `x_search_log`, `x_second_reading` present and well-formed; every baryon component's status from the closed list; `SECOND_READING.md` present.
9. Every assumption in the registry used by a 2.0 package has `role`; adjustable ones have `range_basis`.
10. Results in `checks/` reference a frozen check whose hash matches its freeze record.

## 11. Flags (closed list)

`no_uncertainty`, `beyond_source_range`, `inner_resolution_limited`, `source_quality_low`, `reproduction_mismatch` (1.2.0), and new in 2.0.0: `edges_inferred` (D-036 ii), `value_in_text` (D-038 5A), `assumed_concentration` (an aperture correction that used an assumed rather than measured concentration, A3 §8b), `derived_from_delta_g` (§3), `metallicity_cut_membership` (D-038 4B), `fitted_profile` (D-038 2D), `star_count_weighting` (D-038 1A: member-sample σ taken as representative of the light-weighted σ).

## 12. Extension columns

As 1.3.0: `x_<dataset short name>_<name>`, with full header information; validated for naming and header completeness only; the core site, sliders and cross-dataset views never depend on them.
