# Selection protocol, v1.0 coverage (draft, D-028)

**Status: draft, 2026-10-29. Not frozen.** Written before any new data are converted and without plotting any candidate. Once JvH approves it, it is **frozen by hash on the protected `main` branch** (`data/taxonomy.json`, with GitHub's push time as the first timestamp) before the search in §3 starts, and **deposited on Zenodo** for an outside timestamp before the first new conversion (TAXONOMY §6.8). Changes after the freeze go to the deviations register (§9).

The general rules are in `docs/plans/TAXONOMY.md` §6. This document adds what §6 leaves to be written in advance: eligibility per cell, the search procedure, the method rulings each cell needs, and the dates.

## 1. Rules common to every cell

A dataset is eligible if all of the following hold:
1. **Both sides.** It gives, per system, per radius or per stacked bin, the observed side (the observables, or a quantity derived from them) and the baryonic side (the observed components, or the quantities they are computed from), or another eligible dataset supplies the missing side for the same systems (recorded as a pairing).
2. **Machine-readable and public**, or supplied by the authors on request. Values read off figures are never used.
3. **Not circular.** The observed side does not come from a scaling relation (D-029). Fitted forms are allowed and labelled with `model_dependence`.
4. **Terms.** Its licence is read per record; it is redistributed only if permitted, otherwise fetched by address and verified by hash (D-004, D-029).
5. **Independence.** Data independent of datasets already included, or a re-reduction recorded as such, with a precedence rule for default views (D-029).
6. **Distance or redshift** is given per system or per bin (D-033).
7. **Statuses.** Each baryon component can be classed measured, modelled or absent (D-034).

## 2. Eligibility per cell

Additions to §1, written before any candidate is examined. "N" is the minimum number of systems for a cell to be filled by a sample; case-study cells take single systems.

| Cell | Kind × tracer | Observed side must be | Baryonic side must be | N | Form |
|---|---|---|---|---|---|
| A0·orbits | Solar System × planetary orbits | A published bound on an anomalous acceleration from ephemeris fits, with method | Known masses as used in the fit | — | Limit |
| A1·orbits | Wide binaries × orbits | Per-pair separations and relative velocities (projected or 3D) from Gaia, as released by each team | Per-star photometry or masses, with the mass–magnitude relation named | — | Case study: each team's released sample as a named alternative (D-028) |
| A2·random | Open clusters × random motions | Internal velocity dispersion (radial-velocity or proper-motion), measured | Stellar mass from counts or photometry | 5 | Single aperture or profile; the source's equilibrium statement recorded |
| A3·random | Globular clusters × random motions | Velocity-dispersion values or binned profiles measured from stellar velocities; not a dynamical mass alone | Luminosity, or a luminosity profile, with a stellar-population mass-to-light ratio (registered); a dynamical M/L is not a baryonic input | 20 | Profile or single aperture |
| A4·rotation | Late-type and irregular × rotation | Rotation curves per radius | Stellar (photometric) and gas (HI) components per radius | 10 | Profile |
| A4/A6·weak lensing | Isolated galaxies, stacked × weak lensing | ΔΣ or g_obs per bin, with covariance | Stellar and gas masses per bin | — | Population average |
| A5·random | Dwarf spheroidal and ultra-faint × random motions | Velocity dispersion (global, at a stated radius, or a profile); upper limits kept as limits | Luminosity and half-light radius; registered mass-to-light ratio; gas recorded if measured | 10 | Single aperture or profile |
| A6·rotation | Early-type × HI rings or discs | Ring rotation velocity at stated radius | Stellar photometry | 5 | Single radius or profile |
| A6·random | Early-type × stellar kinematics | Dispersion or circular-velocity profiles (model-derived allowed, labelled) | Stellar photometry with a named mass-to-light method | 10 | Profile or aperture |
| A6·orbits | Early-type × globular clusters or planetary nebulae | Released individual or binned tracer velocities | Stellar photometry | 5 | Profile |
| A6·hot gas | Early-type × X-ray | Hydrostatic mass profiles | Gas and stellar profiles | 5 | Profile |
| A6·strong lensing | Early-type × strong lensing | Mass within the Einstein radius | Stellar mass from photometry, IMF named | 20 | Single aperture (projected) |
| A7·any | Unusual configurations | Per-object data, either tracer | Per-object components | 1 | Case study |
| A8·hot gas | Groups × X-ray | Hydrostatic mass profiles | Gas profiles; stars if available | 5 | Profile |
| A8·weak lensing | Groups × weak lensing | Per-system or stacked ΔΣ profiles | Gas and stellar masses on comparable radii | 5 | Profile or average |
| A9·orbits | Clusters × member galaxies | Caustic or Jeans mass profiles from member velocities | Gas (and stars) for the same clusters, possibly from a paired dataset | 5 | Profile |
| A9·hot gas | Clusters × X-ray | Hydrostatic mass profiles | Gas and stellar profiles | 5 | Profile |
| A9·lensing | Clusters × weak/strong lensing | Binned profiles, or quantities evaluated from fits (labelled) | Gas profiles for the same clusters; stars if available | 5 | Profile (projected) |
| A10·maps | Colliding clusters × lensing and X-ray | Lensing mass (κ) maps as files with coordinates | X-ray maps of the same cluster | 1 | Map, case study |
| Epoch | z ≳ 0.3, any kind | As the kind's cell | As the kind's cell | — | Declared a gap for v1.0 (D-033) |

## 3. Search procedure (per cell)

Run once per cell, on a recorded date, and logged in `docs/sources/search-log-<cell>.md`:
1. **ADS:** the query strings for the cell, recorded verbatim (kind terms, tracer terms, and "data release" or "catalogue"), refereed papers since 1990.
2. **VizieR:** keyword search for the kind and tracer.
3. **Zenodo and GitHub:** keyword search for the kind and tracer with "data".
4. **Citations:** the data papers cited by eligible datasets, and recent reviews of the kind.
5. **Log:** every record found, screened and excluded, with the reason; counts in the style of a PRISMA flow (identified, screened, eligible, included).

Eligibility is decided from metadata, data documentation and methods sections only (TAXONOMY §6.4). The 2026-10-28 and 2026-10-29 surveys are starting points, not the search.

## 4. Inclusion and ranking

Every eligible dataset is included. Where two datasets reduce the same observations, the one shown by default is chosen by: deepest observables released; then independence of the reduction; then number of systems; then licence. Both remain in the record.

## 5. Method rulings needed, with deadlines

Each must be ruled before the data-freeze date (§6). Under D-031, JvH rules at least one in three method decisions before seeing Claude's recommendation.

| Ruling | Needed for | Proposed deadline |
|---|---|---|
| D-025: turning dispersions into g_obs (estimator at a radius, Jeans profiles, or both, labelled) | A2, A3, A5, A6·random | Before the A3 and A5 searches end |
| Stellar mass-to-light ratio for star clusters and dwarfs: defaults and ranges, read at source | A2, A3, A5 | With D-025 |
| Projection for lensing: baryons projected, or lensing deprojected (per dataset) | A6·strong, A8·lensing, A9·lensing | Before the first lensing package |
| Wide-binary case study: what is shown (per-team samples, the shared base catalogue, or both) | A1 | Before the A1 search ends |
| Maps: how co-registered maps are shown and what is computed from them | A10 | Before the A10 package |
| Solar System limit: which published bound, and how a limit is drawn | A0 | Before the A0 package |

## 6. Dates

- **Search window:** from the freeze of this protocol on `main` until the data-freeze date.
- **Data-freeze date:** set at the freeze. Proposed: 8 weeks after the freeze. Datasets found or released later go to the next version.
- **Data requests:** held by JvH (2026-10-29) until the public cells are built. A request's 8-week clock (§6.5 of TAXONOMY) starts when it is sent; cells waiting on requests stay open past the data-freeze date only for the requests' answers.

## 7. Order of work

1. Release-gate cells: A3, A5, A0.
2. A6 (strong lensing first), A9 lensing and member galaxies.
3. A4 second disc set, A10 maps, A1 case study.
4. A2, A7, A8.

## 8. What is frozen

This document, TAXONOMY §2–§7, the kinds list, and the hashes of both, in `data/taxonomy.json`, committed to protected `main` before the search starts; the Zenodo deposit before the first conversion records the same hashes.

## 9. Deviations register

Empty. Each entry: date, cell, what changed, why, and the data seen at the time.
