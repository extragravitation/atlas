# Reader A, stratum aeg-d-xcop_v1: notes

## Method followed
`method/SOURCE.md` (package method file for aeg-d-xcop/v1). The methods page text describes a later X-COP conversion
("five with stellar data", Eckert et al. 2022, D-089/D-090) that does not match this v1 package or this archive; I
followed SOURCE.md, which is the v1 method, and treat the methods page conflict as a documentation finding.

Per row:
- g_obs = G M_FORW / r^2, r = `RADIUS` (kpc) from `<c>_hydro_mass.fits` ext HYDRO_MASS at the located row.
- g_bar,gas = G M_gas(<r) / r^2; M_gas interpolated linearly in log M vs log r from `<c>_fgas_profile.fits` ext FGAS
  (`RADIUS` in R/R500 x header `R500`, `MGAS`).
- g_bar,stars: measured clusters: `MSTAR` from `<c>_mstar.fits` ext MSTAR_SMOOTHED (`RADIUS` kpc), same interpolation.
  Modelled clusters (A1644, A2255, A3266, RXC1825 in this packet): M*(<r) proportional to ln(1+x) - x/(1+x), x = r/r_s,
  r_s = R200/2.9, normalised to M*(<R500) = 0.39 (M500/1e14)^-0.84 M_gas(<R500), with R500, M500, R200 from Ettori et
  al. 2019 Table 1 and M_gas(<R500) interpolated from the gas file at Table 1's R500.
- g_bar = g_bar,gas + g_bar,stars. Constants: G and M_sun from astropy 8.0.2 (CODATA 2022 G = 6.6743e-11; IAU 2015
  M_sun = 1.988409870698051e30 kg); kpc from astropy units. Values in values.csv are printed to 7 significant figures.

## Downloaded
- Ettori et al. 2019 e-print: https://arxiv.org/e-print/1805.00035, SHA-256
  `3bc07668cc877920ac05ca955c88d80d15aad19a11d9fd7286e25c396d658733`. Table 1 = `tab:mass` in `mass_xcop.tex`
  (lines 315-324). Values read as printed (R500, M500, R200 columns).

## Steps I was unsure of (none made a row incomplete)
1. **Row numbering.** Locators say "row N" without saying 0- or 1-based. I read N as the 1-based FITS row. Evidence: for
   A85, row index 0 (30 kpc) lies below the gas grid's first radius (0.02429909 x 1235 = 30.009 kpc) and is excluded by
   the method's range rule; measurement ids then run m000001 (row 2) ... m000085 (row 86), and A644's ids continue at
   m000086 (its row 2, after its excluded row 1), which matches rows.csv (m000087 = A644 row 3). Under 0-based reading
   A85 "row 86" would be outside the kept range. Recommend the method state the convention.
2. **Units of the `R500` header keyword** are not given in the FITS header (comment "NFW R500"). Read as kpc: the
   value 1235.0 for A85 equals Table 1's 1.235 Mpc.
3. **ICL assumption default.** SOURCE.md lists `icl_fraction` as an adjustable assumption on measured-star rows but
   does not give its default; the Conversion section states g_bar = g_bar,gas + g_bar,stars with MSTAR as released, so
   I added nothing for ICL. Likewise `xray_hse_bias` default 0.00 (methods page table) leaves g_obs unchanged. If the
   dataset's default ICL fraction is non-zero and applied to the shipped g_bar, the method is incomplete on that point.
4. **astropy version** is not stated; G and M_sun have not changed value between CODATA 2018 and 2022 in astropy, so no
   effect expected.
5. **D-023 cut** boundary: my own count with the stated cut (0.145 <= r/R500 <= 1.38) gives 859 shipped rows, not 861
   as stated; the ids imply A1644 keeps one more inner row than my cut (boundary/float32 rounding). No packet row is
   outside the cut by my reading; this does not affect any computed value.
6. Interpolation of stellar masses: some adjacent MSTAR_SMOOTHED rows have equal values (2 significant figures printed,
   e.g. 2.02e12); interpolation is then flat, as the method implies.

## Isolation
Worked only in this folder; read only the packet; one arXiv download as allowed by the brief.
