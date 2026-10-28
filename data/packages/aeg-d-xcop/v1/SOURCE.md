# aeg-d-xcop/v1 — source

**Source.** X-COP public data release (XMM-Newton Cluster Outskirts Project), one archive linked from the data page https://dominiqueeckert.wixsite.com/xcop/data. Read 2026-10-28. Full reading notes: `docs/sources/xcop.md`.

| File | Bytes | SHA-256 |
|---|---|---|
| `allfiles.tar.gz` | 315 080 566 | `0edf5038b419b70d070b73b22f4801e27f318b0854db61eec52142c27c140d94` |

**Licence.** None stated. The archive is not redistributed (D-004); `sources.json` records its address and hash, and the pipeline verifies both on every build.

**Citation, as the data page requests.** Thermodynamic profiles: Ghirardini et al. 2018. Mass profiles: Ettori et al. 2018 (published 2019, A&A 621, A39; arXiv:1805.00035). Gas mass and gas fraction: Eckert et al. 2018 (arXiv:1805.00034). Metal abundance profiles: Ghizzardi et al. 2020 (arXiv:2007.01084), whose stellar-mass profiles are used here. A2142: Tchernin et al. 2016. A2319: Ghirardini et al. 2017. RXC 1825: Clavico et al. 2019.

## What is used

Twelve clusters (A85, A644, A1644, A1795, A2029, A2142, A2255, A2319, A3158, A3266, RXC1825, ZW1215). Per cluster:

| Quantity | File, extension, columns | Notes |
|---|---|---|
| g_obs | `<cluster>_hydro_mass.fits`, ext 1: `RADIUS` (kpc), `M_FORW`, `EM_FORW` (M☉) | Forward-method hydrostatic mass (no assumed shape for the mass profile), Ettori et al. 2019; 100 radii, 30–3000 kpc; `EM_FORW` is a symmetric one-sigma error |
| g_bar, hot gas | `<cluster>_fgas_profile.fits`, ext `FGAS`: `RADIUS` (R/R500), `MGAS`, `MGAS_LO`, `MGAS_HI` (M☉) | `MGAS_LO`/`MGAS_HI` are one-sigma errors (they are about 1–2 % of `MGAS`), not bounds. Radii converted to kpc with the `R500` keyword in the same file's header |
| g_bar, stars (7 clusters) | `<cluster>_mstar.fits`, ext `MSTAR_SMOOTHED`: `RADIUS` (kpc), `MSTAR`, `MSTAR_LO`, `MSTAR_HI` (M☉) | Header: "Smoothed stellar mass profile used in Ghizzardi et al. 2020 and total uncertainties". `MSTAR_LO`/`MSTAR_HI` are bounds (they bracket `MSTAR`). Central galaxy included, intracluster light excluded (Ghizzardi et al. 2020) |
| g_bar, stars (5 clusters) | Modelled, D-022 item 3 | A1644, A2255, A3158, A3266, RXC1825 have no stellar file |

Not used: the `MSTAR_RAW` extension (R/R500 grid, statistical and cosmic-variance errors given separately; the smoothed extension carries the combined uncertainty); the NFW, Einasto, isothermal and Burkert mass models (each assumes a shape for the mass profile; NFW is used only in the reproduction test); thermodynamic profiles, images and spectra.

## Conversion

- **Rows** are the hydrostatic file's own radii. A radius is converted only if it lies inside the tabulated range of every component used for that cluster (gas file, and stellar file where measured): no profile is extrapolated. This keeps 83–93 of the 100 radii per cluster, 1 065 in all, from 30 kpc out to between 1.4 and 2.3 Mpc.
- **Interpolation.** Gas and stellar masses (and their errors or bounds) are interpolated to each radius linearly in log M against log r.
- **Accelerations.** g = G M(<r) / r² for each mass, with G and M☉ from astropy; g_bar = g_bar,gas + g_bar,stars. g_bar errors: gas and stellar errors added in quadrature, separately below and above; modelled stars carry no error.
- **Modelled stars (D-022 item 3).** M★(<r) ∝ ln(1 + x) − x/(1 + x) with x = r / r_s, r_s = R200 / 2.9; normalised so that M★(<R500) = 0.39 (M500 / 10¹⁴ M☉)^−0.84 × M_gas(<R500), where R500, M500 and R200 are Ettori et al. 2019 Table 1's values and M_gas(<R500) is the gas mass interpolated at that R500 (for all 5 modelled clusters the gas file's header R500 equals Table 1's).
- **Assumptions recorded per row.** `xray_hse_bias` (all rows, adjustable), `icl_fraction` (measured-star rows, adjustable), `stars_cluster_modelled` (modelled-star rows; draft, no slider). Ranges and effects: `data/assumptions.json`, D-022.
- **Cosmology.** As in the source: flat ΛCDM, H0 = 70 km s⁻¹ Mpc⁻¹, Ωm = 0.3 (Ettori et al. 2019 §1).

## Known issue

Archive profiles for A644, A2029 and A2319 differ from Ettori et al. 2019 Table 1 beyond the frozen tolerance; their rows are flagged `reproduction_mismatch` and linked to issue #19 (D-019). See `REPRODUCTION_RESULT.md`.
