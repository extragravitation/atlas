# Atlas data standard

**Version 1.0.0 — FROZEN 2026-10-28 (decision D-015).** Packages state the version they follow. Changes follow section 0. Nothing enters `data/packages/` that does not follow a frozen version of this standard.

The standard is written so that each of the four v0.1 sources (SPARC, KiDS-1000 RAR, X-COP, CLASH lensing) fits without special cases. The source readings that shaped it are in `docs/sources/`.

## 0. Versioning

The standard uses semantic versioning, MAJOR.MINOR.PATCH. Every change gets a decision-log entry and a changelog line.

| Change | Example | Version step |
|---|---|---|
| **Patch**: wording or clarification with no effect on any file | Rewording a description | 1.0.0 → 1.0.1 |
| **Minor**: additive and backward-compatible; every package valid under the old version stays valid | New optional column; new value in a closed list; new extension rule | 1.0.x → 1.1.0 |
| **Major**: breaking; some valid package would become invalid, or a column would change meaning | Renaming, removing or retyping a column; changing a unit; changing what a column means; making an optional column required | 1.x → 2.0.0 |

A package following an older version stays valid under it. A package is never edited to follow a newer version; it is re-issued as a new dataset version (D-006).

## 1. Package layout

One folder per dataset version: `data/packages/<dataset>/<version>/`, e.g. `data/packages/aeg-d-sparc/v1/`.

| Path | Content | Committed? |
|---|---|---|
| `datapackage.json` | Frictionless Data Package descriptor: name, version, standard version, title, licence, sources, contributors, resources | yes |
| `SOURCE.md` | What was read at source: addresses, dates, licence text or its absence, citation, method summary, link to `docs/sources/<name>.md` | yes |
| `sources.json` | Every source file: address, file name, bytes, SHA-256, retrieval date, redistributable (true/false) | yes |
| `REPRODUCTION.md` | Published numbers the package must reproduce, and the tolerance. **Committed, with its hash in `sources.json`, before `convert.py` is first run** | yes |
| `convert.py` | Fetches sources (verifying hashes), converts, writes `tables/` | yes |
| `tables/measurements.ecsv` | Section 3 | yes |
| `tables/systems.ecsv` | Section 4 (omitted for population-only datasets) | yes |
| `tables/covariance.ecsv` | Section 5, where the source provides covariance | yes |
| `tests/` | Reproduction, schema and assumption tests | yes |
| `checksums.sha256` | SHA-256 of every committed file in the package | yes |
| `source/` | Downloaded source files | **never** (`.gitignore`) |

## 2. Table format: ECSV

All tables are **ECSV 1.0** (Enhanced Character Separated Values, the astropy community format), **comma-delimited**. Each file starts with a commented YAML header; below it the data are ordinary CSV.

Every column's header entry carries:
- `name`, `datatype`;
- `unit` (where the quantity has one), in the units of section 2a;
- `description`, one sentence in the Technical vocabulary;
- `meta: {ucd: …}`, a UCD from the IVOA UCD1+ controlled vocabulary **version 1.6 (2024-12-18)**, validated automatically against that list.

The file-level header carries `meta` with the dataset ID and version and the standard version.

Plain CSV and Parquet copies are generated at build time for downloads and the site. They are never committed and never edited by hand.

### 2a. Units and conventions

| Quantity | Unit | Notes |
|---|---|---|
| Accelerations (g_obs, g_bar and components) | m s⁻² | Stored linear, never logged |
| Radius | kpc | Physical, not comoving; projected or three-dimensional stated per row (`r_kind`) |
| Mass | M☉ (`solMass`) | |
| Velocity | km s⁻¹ | Source-derived columns only |
| Distance | Mpc | |

- Values that depend on the Hubble constant are stored as the source gives them, with the source's assumed H0 (or h) in `datapackage.json`. **No silent rescaling.** Any rescaling is a named assumption.
- Uncertainties: lower and upper one-sigma bounds as separate columns (`_err_lo`, `_err_hi`), both non-negative. Symmetric errors repeat the value. A missing uncertainty is an empty cell plus the `no_uncertainty` flag, never zero.
- Signs: components of g_bar keep their sign (e.g. SPARC gas contributions are negative at some radii). A component's acceleration is V·|V|/R, not V²/R.
- Missing values: empty cell. Never a sentinel number such as −999.

## 3. Measurements table (`tables/measurements.ecsv`)

One row per measurement.

| Column | Type | Unit | UCD | Required | Meaning |
|---|---|---|---|---|---|
| `measurement_id` | string | | `meta.id;meta.main` | yes | `aeg-d-<name>/v<N>/m000001`, sequential within the package version |
| `system_id` | string | | `meta.id` | for systems | `aeg-s-000001`; empty for population measurements |
| `kind` | string (closed list) | | `meta.code` | yes | `profile_point`, `system_value`, `population_bin` |
| `channel` | string (closed list) | | `meta.code` | yes | `dynamics`, `lensing` |
| `method_class` | string (closed list) | | `meta.code.class` | yes | `kinematic`, `hydrostatic`, `lensing` |
| `method` | string | | `meta.note` | yes | Source method, e.g. `X-ray+SZ hydrostatic, forward method` |
| `r_kpc` | float64 | kpc | `phys.size.radius` | if defined | Empty where the source bins by another quantity |
| `r_kind` | string (closed list) | | `meta.code` | if `r_kpc` | `3d`, `projected` |
| `g_obs` | float64 | m / s2 | `phys.acceleration` | yes | Observed acceleration |
| `g_obs_err_lo`, `g_obs_err_hi` | float64 | m / s2 | `stat.error;phys.acceleration` | if available | Lower and upper one-sigma bounds |
| `g_bar` | float64 | m / s2 | `phys.acceleration;meta.modelled` | yes | Newtonian acceleration from detected baryons, at catalogue defaults |
| `g_bar_err_lo`, `g_bar_err_hi` | float64 | m / s2 | `stat.error;phys.acceleration` | if available | Bounds |
| `g_bar_stars`, `g_bar_gas_cold`, `g_bar_gas_hot` | float64 | m / s2 | `phys.acceleration;meta.modelled` | where separable | Components at catalogue defaults |
| `stars_status`, `gas_cold_status`, `gas_hot_status` | string (closed list) | | `meta.code` | yes | `measured`, `modelled`, `absent`, `not_separable` |
| `assumptions` | string | | `meta.note` | yes | Semicolon-separated assumption IDs (section 6) affecting this row, each with its catalogue value |
| `adjustable` | string | | `meta.note` | yes | Assumption IDs whose sliders can change this row; empty if none |
| `quality_source` | string | | `meta.code.qual` | no | The source's own quality label, verbatim. Shown; never used to hide data by default |
| `source_ref` | string | | `meta.ref` | yes | Pointer to the source row or file |
| `flags` | string | | `meta.code` | no | Semicolon-separated values from the closed list in section 7 |

`meta.modelled` on g_bar records what g_bar is: the Newtonian prediction from detected matter, as distinct from the observed g_obs.

Rules:
- g_bar is always Newtonian, from detected baryons, at the catalogue's default assumptions. Slider effects are computed from the stored components and the registry formula (section 6), never stored as extra rows.
- If components are not separable (KiDS), stellar-mass sliders do not apply; the source's own systematic range is shown instead.

## 4. Systems

Global registry `data/registry/systems.csv` (ID, primary name, first dataset version, assignment date; rules enforced by `python -m aeg.check`). The registry is a small editorial file and stays plain CSV. Per package, `tables/systems.ecsv`:

| Column | Unit | UCD | Meaning |
|---|---|---|---|
| `system_id` | | `meta.id;meta.main` | From the registry; new systems are added to it in the same pull request |
| `name_in_source` | | `meta.id` | Name exactly as the source writes it |
| `class_in_source` | | `src.class` | Class label as the source gives it; never the Atlas's verdict |
| `distance_mpc` | Mpc | `pos.distance` | As given by the source |
| `distance_err_mpc` | Mpc | `stat.error;pos.distance` | As given by the source |
| `distance_method` | | `meta.code` | As given by the source |
| `ra_deg`, `dec_deg` | deg | `pos.eq.ra`, `pos.eq.dec` | Where the source gives them |
| `properties` | | `meta.note` | JSON object of other source-given properties, units in the key names (e.g. `"inclination_deg"`, `"r500_kpc"`) |

Cross-identifications (`data/registry/crossids.csv`: `system_id`, `catalogue`, `identifier`) are added when a second dataset names the same system. A match is never made by name alone without a recorded position check.

## 5. Covariance (`tables/covariance.ecsv`)

| Column | Unit | UCD | Meaning |
|---|---|---|---|
| `measurement_id_i`, `measurement_id_j` | | `meta.id` | The pair |
| `quantity` | | `meta.code` | `g_obs` |
| `covariance` | m2 / s4 | `stat.covariance;phys.acceleration` | Converted with the same formula as the values |

Only where the source provides covariance.

## 6. Assumption registry (`data/assumptions.json`)

One entry per named assumption, shared across datasets.

| Field | Meaning |
|---|---|
| `id` | e.g. `ml_disk`, `ml_bulge`, `distance`, `inclination`, `xray_hse_bias`, `stars_cluster_modelled`, `icl_fraction`, `deproj_lensing` |
| `name_technical`, `name_plain` | Both vocabularies |
| `applies_to` | Dataset versions |
| `parameter` | Name, unit, catalogue default per dataset (with reference), published range (with references, each read at source) |
| `effects` | For each affected column, a **formula** in the expression language below |
| `adjustable` | true for sliders; false for assumptions shown but fixed |
| `status` | `draft` until default and range are read at source; only `confirmed` assumptions may drive a slider |

**Formula expression language (D-014).** One formula per effect, written once and executed by both the pipeline (Python) and the site (JavaScript) from the same text. Allowed: numbers; the parameter `p` and its default `p0`; column names of the same row; `+ - * /`, `^` for powers; parentheses; functions `sqrt`, `abs`, `sin`, `cos`, `deg2rad`. Nothing else: no loops, no conditionals, no other rows. Example (SPARC distance, g_obs at fixed angle): `g_obs * p0 / p`.

Both evaluators are tested on every measurement and every adjustable assumption at its default and range ends; results must agree to a relative tolerance of 1e-12.

## 7. Validation (automated; fails the build)

1. Every source file matches its recorded SHA-256 and size.
2. `REPRODUCTION.md`'s hash in `sources.json` matches the file, and git history shows it committed before the first commit containing `tables/`.
3. Reproduction tests pass within the frozen tolerances.
4. Every table reads as ECSV with astropy; every column has the required unit, datatype, description and UCD; every UCD is valid against the UCD1+ list v1.6.
5. Schema: required columns present; closed lists respected; units as section 2a; no sentinel values; error bounds non-negative.
6. IDs: measurement IDs well-formed, unique, sequential; every `system_id` exists in the registry.
7. Physical sanity (warnings that need an acknowledged note, not silent fixes): g_obs and g_bar positive where the source implies they must be; values within 10⁻¹⁶ to 10⁻⁶ m s⁻².
8. Every assumption named in `assumptions` or `adjustable` exists in the registry; every `adjustable` one is `confirmed`.
9. Slider formulas: changing each assumption changes only rows listing it in `adjustable`, exactly as its formula says; the Python and JavaScript evaluators agree (section 6).
10. Licence: if any source is not redistributable, no file from it is committed and the release archive excludes it.
11. Closed list of `flags`: `no_uncertainty`, `beyond_source_range`, `inner_resolution_limited`, `source_quality_low`. Adding a value is a minor version change.
12. Extension columns (section 8) are named correctly and carry unit (where applicable), description and a valid UCD.

## 8. Extension columns

A dataset may carry extra source-specific columns in any of its tables without a change to the standard, named `x_<dataset short name>_<name>` (e.g. `x_sparc_q` for the SPARC quality flag in its raw form). Rules:
- They carry the same header information as core columns (section 2).
- They are validated for naming and header completeness only.
- The core site, the sliders and cross-dataset views never depend on them.
- If an extension column proves generally useful, it is promoted to a core column by a minor version, and the extension remains in existing packages unchanged.
