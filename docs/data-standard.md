# Atlas data standard

**Version 1.0, DRAFT for ruling (D-015).** Once frozen, this standard changes only by a new version with its own decision-log entry; packages state which version they follow. Nothing in `data/packages/` may be committed before the freeze.

The standard is written so that each of the four v0.1 sources (SPARC, KiDS-1000 RAR, X-COP, CLASH lensing) fits it without special cases. The source readings that shaped it are in `docs/sources/`.

## 1. Package layout

One folder per dataset version: `data/packages/<dataset>/<version>/`, for example `data/packages/aeg-d-sparc/v1/`.

| Path | Content | Committed? |
|---|---|---|
| `datapackage.json` | Frictionless Data Package descriptor: name, version, title, licence, sources, contributors, resources with table schemas | yes |
| `SOURCE.md` | What was read at source: addresses, dates, licence text or its absence, citation, method summary, link to `docs/sources/<name>.md` | yes |
| `sources.json` | Every source file: address, file name, bytes, SHA-256, retrieval date, redistributable (true/false) | yes |
| `REPRODUCTION.md` | Which published numbers the package must reproduce, and the tolerance. **Written and its hash recorded in `sources.json` before `convert.py` is first run** | yes |
| `convert.py` | Fetches sources (verifying hashes), converts, writes `tables/` | yes |
| `tables/measurements.csv` | Section 3 | yes |
| `tables/systems.csv` | Section 4 (omitted for population-only datasets) | yes |
| `tables/covariance.csv` | Section 5, where the source provides covariance | yes |
| `tests/` | Reproduction test, schema test, assumption tests | yes |
| `checksums.sha256` | SHA-256 of every committed file in the package | yes |
| `source/` | Downloaded source files | **never** (`.gitignore`) |

A **released** package version is never edited. Any change is a new version (D-006).

## 2. Units and conventions

| Quantity | Unit | Notes |
|---|---|---|
| Accelerations (g_obs, g_bar and components) | m s⁻² | Stored linear, never logged |
| Radius | kpc | Physical, not comoving. Projected or three-dimensional stated per dataset |
| Mass | M☉ | |
| Velocity | km s⁻¹ | Only in source-derived columns |
| Distance | Mpc | |

- Hubble constant: values that depend on it are stored as the source gives them, with the source's assumed H0 (or h) in `datapackage.json`. **No silent rescaling.** A rescaling, if ever done, is a named assumption.
- Uncertainties: lower and upper one-sigma bounds as separate columns (`_err_lo`, `_err_hi`), both positive. Symmetric errors repeat the value. Missing uncertainty is an empty cell plus a flag, never zero.
- Signs: components of g_bar keep their sign (e.g. SPARC gas contributions are negative at some radii). A component's acceleration is V·|V|/R, not V²/R.
- Missing values: empty cell. Never a sentinel number such as −999.

## 3. Measurements table (`tables/measurements.csv`)

One row per measurement.

| Column | Type | Required | Meaning |
|---|---|---|---|
| `measurement_id` | string | yes | `aeg-d-<name>/v<N>/m000001`, sequential within the package version |
| `system_id` | string | for systems | `aeg-s-000001`; empty for population (Average) measurements |
| `kind` | enum | yes | `profile_point` (one radius in one system), `system_value` (one value per system), `population_bin` (stacked average) |
| `channel` | enum | yes | `dynamics`, `lensing` |
| `method_class` | enum | yes | `kinematic`, `hydrostatic`, `lensing` |
| `method` | string | yes | Source method, e.g. `HI/Halpha rotation curve`, `X-ray+SZ hydrostatic, forward method`, `weak lensing, stacked` |
| `r_kpc` | number | if defined | Radius; empty where the source bins by another quantity (KiDS bins by g_bar) |
| `r_kind` | enum | if `r_kpc` | `3d`, `projected` |
| `g_obs`, `g_obs_err_lo`, `g_obs_err_hi` | number | yes (value) | Observed acceleration and bounds |
| `g_bar`, `g_bar_err_lo`, `g_bar_err_hi` | number | yes (value) | Baryonic acceleration at catalogue defaults, and bounds |
| `g_bar_stars`, `g_bar_gas_cold`, `g_bar_gas_hot` | number | where separable | Components at catalogue defaults; empty where the source does not separate them |
| `stars_status`, `gas_cold_status`, `gas_hot_status` | enum | yes | `measured`, `modelled`, `absent`, `not_separable` |
| `assumptions` | string | yes | Semicolon-separated assumption IDs (section 6) affecting this row, each with its catalogue value, e.g. `ml_disk=source;deproj_lensing=sis` |
| `adjustable` | string | yes | Semicolon-separated assumption IDs whose sliders can change this row; empty if none |
| `quality_source` | string | no | The source's own quality label, verbatim (e.g. SPARC Q). Shown; never used to hide data by default |
| `source_ref` | string | yes | Pointer to the source row or file, e.g. `MassModels_Lelli2016c.mrt:row 1234` |
| `flags` | string | no | Semicolon-separated: `no_uncertainty`, `beyond_source_range`, … (closed list in section 7) |

Rules:
- g_bar is always Newtonian, from detected baryons, at the catalogue's default assumptions. Slider effects are computed on the site from the stored components and the formula in the assumption registry, never stored as extra rows.
- If g_bar components are not separable (KiDS), the measurement is not adjustable by stellar-mass sliders; the source's own systematic range is shown instead.

## 4. Systems

Global registry `data/registry/systems.csv` (ID, primary name, first dataset version, assignment date; rules enforced by `python -m aeg.check`). Per package, `tables/systems.csv`:

| Column | Meaning |
|---|---|
| `system_id` | From the registry; new systems are added to the registry in the same pull request |
| `name_in_source` | Name exactly as the source writes it |
| `class_in_source` | Class label as the source gives it (e.g. Hubble type, "cluster"); never the Atlas's verdict |
| `distance_mpc`, `distance_err_mpc`, `distance_method` | As given by the source |
| `ra_deg`, `dec_deg` | Where the source gives them; otherwise empty, to be filled from a cross-match recorded in the registry |
| `properties` | JSON object of other source-given properties (e.g. inclination, R500), with units in the key names |

Cross-identifications (`data/registry/crossids.csv`: `system_id`, `catalogue`, `identifier`) are added when a second dataset names the same system. A match is never made by name alone without a recorded position check.

## 5. Covariance (`tables/covariance.csv`)

Long form: `measurement_id_i`, `measurement_id_j`, `quantity` (`g_obs`), `covariance` (m² s⁻⁴). Only where the source provides it; converted with the same formula as the values (e.g. KiDS: the bias correction and the factor 4G applied consistently).

## 6. Assumption registry (`data/assumptions.json`)

One entry per named assumption, shared across datasets.

| Field | Meaning |
|---|---|
| `id` | e.g. `ml_disk`, `ml_bulge`, `distance`, `inclination`, `xray_hse_bias`, `stars_cluster_modelled`, `icl_fraction`, `deproj_lensing` |
| `name_technical`, `name_plain` | Both vocabularies |
| `applies_to` | Dataset versions |
| `formula` | Exactly how each affected column changes with the parameter, in plain mathematics |
| `default` | Per dataset: the source's adopted value, with reference |
| `range` | Published range with references (each read at source) |
| `adjustable` | true for sliders; false for assumptions shown but fixed (e.g. `deproj_lensing`) |
| `status` | `draft` until default and range have been read at source; only `confirmed` assumptions may drive a slider |

## 7. Validation (automated; fails the build)

1. Every source file matches its recorded SHA-256 and size.
2. `REPRODUCTION.md` hash in `sources.json` matches the file, and its git history shows it committed before `convert.py` produced the tables.
3. Reproduction tests pass within the frozen tolerances.
4. Schema: required columns present; types and enums valid; units as section 2; no sentinel values; lower and upper errors non-negative.
5. IDs: measurement IDs well-formed, unique, sequential; every `system_id` exists in the registry.
6. Physical sanity (as warnings that need an acknowledged note, not silent fixes): g_obs and g_bar positive where the source implies they must be; values within 10⁻¹⁶ to 10⁻⁶ m s⁻².
7. Every assumption named in `assumptions` or `adjustable` exists in the registry; every `adjustable` one is `confirmed`.
8. Slider formulas: a test changes each assumption and checks that only rows listing it in `adjustable` change, by exactly the registry formula (MVP acceptance criterion 4).
9. Licence: if `redistributable` is false for any source, no file from that source is committed and the release archive excludes it.
10. Closed lists: `flags` values are from: `no_uncertainty`, `beyond_source_range`, `inner_resolution_limited`, `source_quality_low`. Adding a flag is a standard change.

## 8. Formats for downloads

CSV is canonical and committed. Parquet copies are generated at build time for the site and downloads; they are never committed and never edited by hand.
