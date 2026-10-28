# X-COP — source reading

Read 2026-10-28: Ettori et al. 2019 (A&A 621, A39; arXiv:1805.00035, via ar5iv), Eckert et al. 2022 (A&A 662, A123), Ghizzardi et al. 2020 (arXiv:2007.01084), the X-COP data page and the full data archive.

## Ettori et al. 2019 (hydrostatic mass profiles)

- Four tables: **Table 1** masses at reference radii from the backward method with an NFW model; **Table 2** systematic differences of the forward method and other models relative to backward-NFW (as sample medians and quartiles); Table 3 best-fit parameters; Table 4 χ² values.
- **Per-cluster forward-method mass profiles are not tabulated in the paper.**
- Stellar mass is modelled: an NFW-shaped profile (concentration 2.9) normalised by a stellar-to-gas relation (Gonzalez et al. 2013).
- The paper's data-availability line points to `astro.unige.ch/xcop`, which on 2026-10-28 redirects to the university home page (dead link).

## Eckert et al. 2022, "The gravitational field of X-COP galaxy clusters"

- Hydrostatic mass from X-ray and SZ data by three approaches, including a **non-parametric log-normal-mixture reconstruction** with minimal assumptions on the mass-profile shape.
- **Stars measured, not modelled**, for five clusters (A644, A1795, A2029, A2142, A2319): the central galaxy from multi-Gaussian expansion and Jeans modelling, satellites from photometry with background subtraction.
- Compares total and baryonic accelerations directly.
- The authors' `hydromass` Python package is public.

## Data page and archive

Data page: https://dominiqueeckert.wixsite.com/xcop/data. **No licence stated**; it asks that these papers be cited (re-read 2026-10-28): thermodynamic profiles, Ghirardini et al. 2018; mass profiles, Ettori et al. 2018; gas mass and gas fraction, Eckert et al. 2018; metal abundance profiles, Ghizzardi et al. 2020; Hydra A, De Grandi et al. 2016; A2142, Tchernin et al. 2016; A2319, Ghirardini et al. 2017; RXC 1825, Clavico et al. 2019. The stellar-mass files are not listed separately; their header names them as the profiles used in Ghizzardi et al. 2020.

The whole release is one archive, linked from the page (Switch Drive public share `j3WUOYXWgv9Jbnz`), read 2026-10-28:

| File | Bytes | SHA-256 | Last modified (server) |
|---|---|---|---|
| `allfiles.tar.gz` | 315 080 566 | `0edf5038b419b70d070b73b22f4801e27f318b0854db61eec52142c27c140d94` | 2025-09-08 |

271 entries; one folder per cluster (A85, A644, A1644, A1795, A2029, A2142, A2255, A2319, A3158, A3266, RXC1825, ZW1215). Per cluster, among others:

- **`<cluster>_hydro_mass.fits`**: 100 radii (kpc), total mass with errors for the **forward method** (`M_FORW`, `EM_FORW`) and for NFW, Einasto, isothermal and Burkert models (plus a Hernquist error column). Header comment: hydrostatic mass profiles for various mass models.
- **`<cluster>_fgas_profile.fits`**: radius in units of R500; NFW total mass, **gas mass with lower and upper bounds** (`MGAS`, `MGAS_LO`, `MGAS_HI`), and gas fraction.
- **`<cluster>_mstar.fits`** (7 clusters only: A85, A644, A1795, A2029, A2142, A2319, ZW1215): radius in units of R500, **cumulative stellar mass** with statistical and cosmic-variance bounds, from Ghizzardi et al. 2020. No stellar file for A1644, A2255, A3158, A3266, RXC1825.
- A FITS master table (separate link) with cluster properties, including R500, needed to convert R/R500 to kpc.

**The non-parametric mass profiles of Eckert et al. 2022 are not in the release.**

## Ghizzardi et al. 2020 stellar masses (arXiv:2007.01084, read via ar5iv)

Photometric stellar masses of member galaxies above 10⁹ M☉, with statistical subtraction of foreground and background galaxies; **central galaxy included, intracluster light excluded**. The authors note that published estimates of the intracluster-light share of total cluster light range from about 10 % to about 50 % and adopt the larger value as a conservative case in their own analysis.

## Consequences for the Atlas

- The amended D-005 (2026-10-28: Eckert et al. 2022 non-parametric masses) **cannot be built from public data**: those profiles are not released. D-005 was amended again on 2026-10-28 accordingly (see `docs/decisions.md`).
- What the public release **does** support: forward-method masses (no assumed shape for the potential) for all 12 clusters; measured gas mass for all 12; **measured stellar mass for 7** (not 5); intracluster light as a natural named assumption with a published range (≈10–50 % of cluster light, read here; the underlying studies to be read at source before use).
- Licence: none stated; per D-004 the archive is not committed. The package records the share address and the hash above, and the pipeline verifies them on each build.

## Archive details read during conversion (2026-10-28)

- `MGAS_LO`/`MGAS_HI` are one-sigma errors; `MSTAR_SMOOTHED` `MSTAR_LO`/`MSTAR_HI` are bounds (total uncertainty); `MSTAR_RAW` gives statistical and cosmic-variance errors separately on an R/R500 grid.
- The gas and stellar files carry `R500` and `M500` header keywords. For A644, A2029 and A2319 these differ from Ettori et al. 2019 Table 1 (1250, 1414, 1368 kpc against 1230, 1423, 1346); for the other nine they are equal. Known issue #19.
- Ettori et al. 2019 Table 1 also gives redshift, c200, R200 and M200 per cluster; its concentration is defined with Δ = 200 (eq. 3). Lin et al. 2004 (arXiv:astro-ph/0402308) define their galaxy concentration (c = 2.90 +0.21/−0.22) relative to r200, from galaxy number counts excluding the central galaxy.
