# X-COP — source reading

Read 2026-10-28: Ettori et al. 2019 (A&A 621, A39; arXiv:1805.00035, via ar5iv), Eckert et al. 2022 (A&A 662, A123), and the X-COP data page.

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

## Data page

The current X-COP data page (https://dominiqueeckert.wixsite.com/xcop/data) offers per-cluster thermodynamic profiles, **mass profiles, gas mass, gas fraction**, density profiles, SZ profiles, and **stellar mass profiles** (Ghizzardi et al. 2020, added August 2020), plus a FITS master table, as one download. **No licence stated**; it asks that the listed papers be cited. Which method produced the released mass profiles is not stated on the page; this needs the download itself.

## Consequences for the Atlas

- Ettori et al. 2019 alone **cannot** supply forward-method profiles: the D-005 plan needs a different X-COP source.
- **Better source:** Eckert et al. 2022's non-parametric mass reconstruction with measured stellar masses. It is less model-dependent than the forward method and replaces the modelled stellar mass with a measurement for five clusters. Proposed for a ruling as a D-005 amendment.
- Next step: download the X-COP archive (needs JvH's permission) and confirm which mass method and stellar products it contains, then hash and record it.
