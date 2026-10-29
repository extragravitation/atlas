# Data standard 2.0: observables first (draft for ruling, D-029)

**Status: draft, 2026-10-29. Nothing here is ruled.** Proposed with D-029, alongside D-028 (`TAXONOMY.md`). Once ruled, the changes are written into `docs/data-standard.md` as version 2.0.0 and frozen.

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

1. **Observable layer**: the quantity as measured, at the deepest level the source releases.
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
| `level` | closed list | | `measured` (an observable as the source measured it), `reduced` (a profile derived from measurements without a mass model, e.g. a binned dispersion), `inferred` (already a mass or acceleration in the source, e.g. a hydrostatic mass) |
| `source_ref` | string | | Pointer to the source row, file and column |

### 2b. Changes to `measurements.ecsv`

- `observed_from`: semicolon-separated `observable_id`s used for g_obs.
- `baryonic_from`: the same for g_bar.
- `assumptions` keeps its meaning but must now list **every** inference step, adjustable or not (e.g. `circular_orbits`, `thin_disc`, `hydrostatic_equilibrium`, `spherical_symmetry`, `gr_lensing`, `deproj_sis`, `jeans_isotropic`). Each is a registry entry.

### 2c. Registry

Each assumption gets a `role`: `observed_inference`, `baryonic_inference` or `selection`. Non-adjustable steps are registered with their source and stated status (e.g. "assumed by the source; not tested by the Atlas").

### 2d. Selection (required, in `datapackage.json`)

`x_selection`: the sample's selection criteria as structured entries (quantity, condition, value, citation), plus the source's own wording. Population bins also carry their bin definitions. Reason: where the discrepancy appears depends on which systems were selected, and complete coverage of kinds does not remove that.

### 2e. Baryon inventory (required, in `datapackage.json`)

`x_baryon_inventory`: one entry per component (stars by population, atomic gas, helium, molecular gas, ionised gas, hot gas, intracluster light, dust, remnants as relevant), each with a status:

- `measured`, `modelled` (as now);
- `known_unmeasured`: present by the source's or the literature's account, not included in g_bar;
- `stated_negligible`: the source states it is negligible (quoted, with citation);
- `not_addressed`: the source does not discuss it.

Each status cites where it was read. The system page shows the inventory beside the pull budget, so the scope of "detected matter" is explicit. The Atlas never adds a component the source did not measure.

### 2f. Frozen tests

Reproduction and model tests compare at the observable level where the source releases observables, and at the inferred level otherwise; the frozen file states which.

## 3. Versioning and the existing packages

This is a **major** version (2.0.0): the observable table, selection and inventory become required, so a valid 1.3.0 package is not valid under 2.0.0. Packages under 1.3.0 stay valid under 1.3.0 and are never edited.

| Package | Observables already kept | To add | Plan |
|---|---|---|---|
| `aeg-d-sparc` | V_obs and error; V_gas, V_disk, V_bul (extension columns) | Surface brightness (SBdisk, SBbul) per radius from the same file; selection; inventory | Re-issue as v2 under 2.0.0 |
| `aeg-d-kids1000-rar` | ΔΣ (ESD_t, ESD_x), error, bias (extension columns) | Selection (isolation criteria, mass bins); inventory | Re-issue as v2 |
| `aeg-d-xcop` | Hydrostatic, gas and stellar masses (inferred level) | Temperature and density profiles from the same public archive (Ghirardini et al. 2018), at `reduced` level; selection; inventory | Re-issue as v2, with a new frozen reproduction test for the added files |

Each re-issue gets its own frozen test before conversion, as for v1. The v1 packages stay published and citable.

## 4. On the site

- System pages gain an **As measured** view: the observables (V(r), σ(r), T(r) and n_e(r), ΔΣ(R)) with their errors, beside the pull budget, and the chain of assumptions from each to g_obs and g_bar.
- Downloads include `observables` as well as `measurements`.
- Methods describes the two layers.

## 5. Proposed D-029

**Proposed ruling.** Data standard 2.0.0: every package records the observables at the deepest level the source releases, links each g_obs and g_bar to them, and registers every inference step, adjustable or not. Selection criteria and the baryon inventory are required records. Frozen tests compare at the observable level where possible. New packages follow 2.0.0; the three v1 packages are re-issued as v2 before the first public release. Display defaults are unchanged.

**Reason.** g_obs and g_bar are inferences whose steps include assumptions some accounts do not share. Keeping the observables makes the Atlas a test that any account can be checked against, rather than a test stated in one framework's terms. Selection and inventory records make explicit what "detected" and "observed" cover.

**Alternatives.**
- Keep 1.x and add observables as optional extension columns (cheaper; leaves the record framework-dependent where a source's observables are skipped).
- Re-derive every g_obs uniformly from raw data with one Atlas method (most uniform; replaces the sources' expertise with ours and is out of scope).

## 6. Questions for JvH

1. **Required or optional observable layer?** Recommendation: required, with a stated exemption when the source releases only inferred quantities.
2. **Re-issue the three packages before the first public release?** Recommendation: yes. SPARC and KiDS already carry most of what is needed; X-COP needs its thermodynamic profiles added.
3. **Frozen tests at the observable level?** Recommendation: yes, where available.
4. **"As measured" view on system pages for v1.0?** Recommendation: yes, modest: one panel, the observables with errors.
