# Data standard 2.0: observables first (D-029)

**Status: ruled 2026-10-29 (D-029), revised after the methodology review (`docs/reviews/2026-10-29-methodology.md`).** This is the specification; the text is written into `docs/data-standard.md` as version 2.0.0 and frozen before the first 2.0 package.

## 1. The problem

g_obs is not an observation. It is inferred from what was measured, and the inference uses assumptions that are part of what is being tested:

| Tracer | Measured | Turned into g_obs by assuming |
|---|---|---|
| Rotation | Line-of-sight velocities → rotation speed V(r) | Circular orbits in a thin disc; inclination; g = V²/r |
| Random motions | Line-of-sight (and proper-motion) dispersions σ(r) | Dynamical equilibrium; Jeans equations; velocity anisotropy; geometry |
| Hot gas | X-ray (and SZ) temperature T(r), density n_e(r) or pressure | Hydrostatic equilibrium; spherical symmetry; thermal pressure only |
| Weak lensing | Excess surface density ΔΣ(R) | General Relativity's relation between mass and deflection; a deprojection model (e.g. singular isothermal sphere) |
| Strong lensing | Einstein radius, image positions | General Relativity; a lens model; mass in projection |
| Wide binaries | Projected separation and relative velocity | Keplerian orbits; deprojection over orbital elements; masses from luminosity |

Every account must reproduce the observations, but not every account shares these steps. Some modified-gravity theories separate lensing from dynamics; some systems may not be in equilibrium. A record that keeps only g_obs states "the test to pass" in a form that already assumes part of the answer. The charter says: describe observations; never assume a cause.

The baryonic side is the same: g_bar is inferred from surface brightness, gas surface density and X-ray emission through mass-to-light ratios, a helium factor and a geometry.

## 2. The change

**Two layers per measurement, on both sides.**

1. **Observable layer**: the quantity as measured, with the processing steps the source performed (§2f).
2. **Inference layer**: g_obs and g_bar, as now, each linked to the observables it was computed from and to every assumption used, including the non-adjustable ones.

The site's default views (map, pull budget) keep showing g_obs against g_bar: that is the agreed baseline. The record, the downloads and any frozen test are defined on the observables wherever the source releases them.

### 2a. New table `tables/observables.ecsv` (required)

One row per published value of an observable.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `observable_id` | string | | `aeg-d-<name>/v<N>/o000001` |
| `system_id` | string | | As in measurements; empty for population bins |
| `side` | closed list | | `observed` (feeds g_obs) or `baryonic` (feeds g_bar) |
| `quantity` | closed list | | e.g. `v_rot`, `sigma_los`, `sigma_pm`, `temperature_x`, `density_e`, `pressure_e`, `delta_sigma`, `einstein_radius`, `binary_dv_proj`, `binary_sep_proj`, `surface_brightness`, `surface_density_hi`, `luminosity`, `mass_gas`, `mass_star`, `mass_hse`; new values by minor version |
| `value`, `err_lo`, `err_hi` | float64 | per row (`unit`) | As the source gives them |
| `unit` | string | | Astropy unit string |
| `r_kpc`, `r_kind` | | kpc | Where the quantity is a profile |
| `steps` | string | | The processing chain from data to this quantity, as semicolon-separated step IDs from the tracer's ladder (§2f), e.g. `spectra;line_velocities;tilted_ring;inclination;rotation_curve` for a SPARC V(r). Names the last step the source performed and every one before it |
| `limit` | closed list | | `none`, `upper`, `lower` |
| `source_ref` | string | | Pointer to the source row, file and column |

### 2b. Changes to `measurements.ecsv`

- `model_dependence` (closed list): `none` (no fitted functional form between observable and g_obs); `observable_form` (a functional form fitted to a thermodynamic or projected observable, e.g. X-COP's fitted pressure and temperature profiles, or an isothermal lensing deprojection); `total_mass_form` (a functional form assumed for the total mass, e.g. NFW). All three are included, labelled and filterable. Masses from scaling relations are excluded.
- `limit` on g_obs (`none`, `upper`, `lower`), drawn as arrows.
- `evidence_tier` (1 released files; 2 transcribed paper tables; 3 digitised figures), D-035. Default views show tiers 1 and 2.

- `observed_from`: semicolon-separated `observable_id`s used for g_obs.
- `baryonic_from`: the same for g_bar.
- `assumptions` keeps its meaning but must now list **every** inference step, including the background cosmology where it enters (e.g. Σ_crit in lensing), adjustable or not (e.g. `circular_orbits`, `thin_disc`, `hydrostatic_equilibrium`, `spherical_symmetry`, `gr_lensing`, `deproj_sis`, `jeans_isotropic`). Each is a registry entry.

### 2c. Registry

Each assumption gets a `role`: `observed_inference`, `baryonic_inference` or `selection`. Non-adjustable steps are registered with their source and stated status (e.g. "assumed by the source; not tested by the Atlas").

### 2d. Selection (required, in `datapackage.json`)

`x_selection`: the sample's selection criteria as structured entries (quantity, condition, value, citation), plus the source's own wording. Population bins also carry their bin definitions. Reason: where the discrepancy appears depends on which systems were selected, and complete coverage of kinds does not remove that.

### 2e. Baryon inventory (required, in `datapackage.json`)

Status definitions follow D-034: **measured** (the component's distribution is observed in that system; conversion factors are registered assumptions), **modelled** (not observed in that system; inferred from other properties, simulations or an assumed shape), **absent**.

`x_baryon_inventory`: one entry per component (stars by population, atomic gas, helium, molecular gas, ionised gas, hot gas, intracluster light, dust, remnants as relevant), each with a status:

- `measured`, `modelled` (as now);
- `known_unmeasured`: present by the source's or the literature's account, not included in g_bar;
- `stated_negligible`: the source states it is negligible (quoted, with citation);
- `not_addressed`: the source does not discuss it.

Each status cites where it was read. The system page shows the inventory beside the pull budget, so the scope of "detected matter" is explicit. The Atlas never adds a component the source did not measure.

### 2f. Ladders of processing steps (per tracer)

Each tracer has a fixed ladder of step IDs in the standard, from raw data to g_obs. A package declares, per observable, the steps the source performed (`steps`). The ladders are written into the standard with the first package of each tracer; examples:
- rotation: `spectra → line_velocities → velocity_field → tilted_ring → inclination → asymmetric_drift → rotation_curve → g = V²/r`;
- random motions: `spectra → stellar_velocities → membership → binned_dispersion → jeans_or_estimator → mass → g`;
- hot gas: `events → spectra → projected_T_and_density → deprojected_profiles → fitted_forms (if any) → hydrostatic_mass → g`;
- weak lensing: `shapes → shear → excess_surface_density (cosmology) → deprojection → g`.

### 2g. Systems, duplicates and exclusions

- `data/registry/crossids.csv` gains `independent_data` (true or false: whether two datasets use independent observations of the system).
- A frozen precedence rule sets which dataset the default views show when a system appears in several; cross-checks use independent pairs only; coverage counts unique systems.
- `data/registry/excluded.csv`: systems excluded by a source or by the Atlas (e.g. as out of equilibrium), with the reason and citation. Shown on the site.

### 2g′. Distance and redshift (D-033)

`tables/systems.ecsv` requires `redshift` or `distance_mpc` (both where the source gives both), with the method as the source states it. Population bins record the lenses' redshift range or distribution as released (in `x_selection`). Values are as the source gives them; no conversion between redshift and distance without a registered assumption (H0, cosmology).

### 2h. Licences

The licence is recorded per source record, read at source (CDS datasets may be CC BY, an open licence or ODbL; a contributor's own licence appears on the dataset page). Tables derived from share-alike sources follow those terms.

### 2i. Frozen tests

Reproduction and model tests compare at the observable level where the source releases observables, and at the inferred level otherwise; the frozen file states which.

## 3. Versioning and the existing packages

This is a **major** version (2.0.0): the observable table, selection and inventory become required, so a valid 1.3.0 package is not valid under 2.0.0. Packages under 1.3.0 stay valid under 1.3.0 and are never edited.

Ruled: the v1 packages are **not** re-issued before v1.0; they keep their observables as extension columns, and the site reads those. They are re-issued under 2.0.0 after v1.0.

| Package | Observables already kept | To add | Plan |
|---|---|---|---|
| `aeg-d-sparc` | V_obs and error; V_gas, V_disk, V_bul (extension columns) | Surface brightness (SBdisk, SBbul) per radius from the same file; selection; inventory | v2 after v1.0 |
| `aeg-d-kids1000-rar` | ΔΣ (ESD_t, ESD_x), error, bias (extension columns) | Selection (isolation criteria, mass bins); inventory | v2 after v1.0 |
| `aeg-d-xcop` | Hydrostatic, gas and stellar masses (inferred level) | Temperature and density profiles from the same public archive (Ghirardini et al. 2018), with their processing steps; selection; inventory | v2 after v1.0, with a new frozen reproduction test for the added files |

Each re-issue gets its own frozen test before conversion, as for v1. The v1 packages stay published and citable.

## 4. On the site

- System pages gain an **As measured** view: the observables (V(r), σ(r), T(r) and n_e(r), ΔΣ(R)) with their errors, beside the pull budget, and the chain of assumptions from each to g_obs and g_bar.
- Downloads include `observables` as well as `measurements`.
- Methods describes the two layers.

## 5. Ruling

See D-029 in `docs/decisions.md`. Rulings on the draft's questions:
1. The observable layer is required where the source releases observables machine-readable; otherwise the package states that only inferred quantities are released.
2. The v1 packages are not re-issued before v1.0 (reversed from the draft, after the review).
3. Frozen tests compare at the observable level where available.
4. System pages get an "As measured" panel for v1.0.
