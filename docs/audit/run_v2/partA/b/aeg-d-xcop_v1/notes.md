# Reader B — aeg-d-xcop_v1 notes

## What I read
- Method: `method/SOURCE.md` (aeg-d-xcop/v1), used as the written method. The methods page's X-COP paragraph describes a different conversion (Eckert et al. 2022 released accelerations, D-089/D-090, "five with stellar data"); it does not match this package (v1, source = X-COP `allfiles.tar.gz`, 12 clusters, modelled stars for 5). I followed SOURCE.md, since it is the package's own method file. Flag: the methods page and the v1 package method disagree.
- Source: `allfiles.tar.gz` from the packet; extracted only `*_hydro_mass.fits`, `*_fgas_profile.fits`, `*_mstar.fits` into `extract/`.
- Ettori et al. 2019 Table 1 is not in `sources/`; downloaded the arXiv e-print as allowed:
  - URL: https://arxiv.org/e-print/1805.00035
  - SHA-256: `3bc07668cc877920ac05ca955c88d80d15aad19a11d9fd7286e25c396d658733`
  - Table 1 (`\label{tab:mass}`) read from `mass_xcop.tex` lines 315 (A1644), 319 (A2255), 322 (A3266), 324 (RXC1825). Values in Mpc and 1e14 Msun, converted Mpc -> kpc by x1000.

## Steps followed
1. r = `RADIUS` (kpc) and `M_FORW` (Msun) from `HYDRO_MASS` extension at the given row. g_obs = G M_FORW / r^2, hydrostatic bias at its default b = 0.
2. Gas: `FGAS` extension, `RADIUS` (R/R500) x header `R500` (kpc), `MGAS`; linear interpolation in log M vs log r (numpy interp on log10 values).
3. Stars, measured (A85, A644, A1795, A2029, A2142, A2319, ZW1215): `MSTAR_SMOOTHED` `RADIUS` (kpc), `MSTAR`; same interpolation.
4. Stars, modelled (A1644, A2255, A3266, RXC1825 in this packet): M*(<r) = K[ln(1+x) - x/(1+x)], x = r/r_s, r_s = R200/2.9, K from M*(<R500) = 0.39 (M500/1e14)^-0.84 x M_gas(<R500), with M_gas(<R500) interpolated from the gas file at Table 1's R500. Table 1 R500 equals the gas header R500 for all four, as SOURCE.md states.
5. g_bar = G (M_gas + M*) / r^2.
- Constants: G = 6.6743e-11 m^3 kg^-1 s^-2 (CODATA 2022) and M_sun = 1.988409870698051e30 kg from astropy 8.0.2, as the method says. kpc -> m (3.085677581491367e19) from astropy.units; the method does not state this conversion explicitly, but it is a unit definition rather than a physical constant, so I did not mark it incomplete.

## Judgement calls
- **Row numbering.** "row N" taken as 1-based. Evidence: A85 row 86 would be 0-based index 86, which lies outside the gas file's tabulated range (A85 valid 0-based indices are 1..85 under the no-extrapolation rule), so it could not ship; 1-based index 85 is the last valid one. With 1-based rows, all 44 radii are inside every component's range and all modelled-star rows are inside the D-023 cut (0.145-1.38 R500). Per-cluster counts of in-range radii sum to 1 065, matching SOURCE.md.
- **Interpolation edge cases.** None of the 44 radii needed extrapolation.
- `inputs.csv` gives the hydro row values and the two tabulated rows bracketing each interpolation (gas at r, stars at r, and gas at R500 for modelled clusters), as stored (float32, shortest representation).
- Only central values were computed; the brief asks for g_obs and g_bar, not their errors.

## Not verified
- I did not check the archive hash myself (the brief says the packet sources were already checked).
- The 0.39 (M500/1e14)^-0.84 prescription and r_s = R200/2.9 are taken as written in SOURCE.md (D-022 item 3); I did not trace them to their own published origin, which SOURCE.md does not cite.
