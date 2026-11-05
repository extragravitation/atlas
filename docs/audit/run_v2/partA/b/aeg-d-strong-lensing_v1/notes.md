# Reader B notes: aeg-d-strong-lensing_v1

## Status
All 10 rows are `method incomplete`. g_obs and g_bar are left empty in values.csv.

## Why: constants are missing from the method
The brief says to use only the constants stated in the method. The method has three parts: methods_page.txt, REPRODUCTION.md, the two precedence files and descriptor.json. None of them gives a numerical value for:
- G. It is needed for g_obs = G M_E / R_E², for g_bar, and for M_E = θ_E² c² D_s D_l / (4 G D_ls).
- c. It is needed for the angular-diameter distances (Hubble distance c/H0) and for M_E.
- M_sun in kg, and the Mpc or kpc in metres. Without them, masses printed in M_sun and radii in kpc cannot be converted to m s⁻².

The method sends these steps to the frozen `aeg.lensing` functions (`einstein_mass_msun`, `einstein_radius_kpc`, `projected_acceleration`, `sersic_projected_fraction`), but that code is not in the packet.

## What I did anyway (diagnostic only, not method-sourced)
- Every input was read at source (inputs.csv).
- `code/compute.py` follows the written formulas. It uses astropy constants (CODATA 2018 G and c, IAU 2015 M_sun, astropy pc), which are not from the method.
- The results are in `conditional_values.csv`: M_E, R_E, M*(<R_E), f_deV, and conditional g_obs and g_bar. They are not submitted values.
- Sanity checks against the sources' own printed numbers:
  - SLACS: computed log M_E matches R7 (Auger+2009 Table 4) to 0.01 dex for all four systems, and R_E (kpc) matches R7's r_Ein to within 0.02 kpc.
  - SNL-0: R_E = 1.959 kpc, against R28's printed 2.85″ × 0.687 kpc/″ = 1.958 kpc.

## Other steps I was unsure of, with the choices I made
1. **Distance integral.** "Flat, source cosmology" is stated. I used flat FRW with radiation neglected, Ω_Λ = 1 − Ω_m (equal to the printed Ω_Λ in all three sources), and D_ls = (D_C(z_s) − D_C(z_l))/(1+z_s). The radiation treatment is not stated.
2. **Sérsic or de Vaucouleurs fraction.** I used f = P(2n, b_n (R/R_e)^{1/n}) with n = 4. b_n is solved exactly from f(R_e) = ½, as REPRODUCTION test 4 implies (b_4 = 7.66925). The input is circular R = θ_E = b_SIE with R_e = R_eff. Both are in the intermediate-axis convention in S4TM (Table 1 note; Table 2 note). The method does not say how ellipticity is handled, so I took both as circular radii.
3. **SNL-0 lens redshift.** R28 Table 3 prints z = 0.0339 (heliocentric) and z_l = 0.0347 (CMB frame). I used z_l = 0.0347, the one with the symbol. The method does not say which. Using 0.0339 would lower R_E by about 2% and raise both g values by about 5%.
4. **SNL-0 stellar mass.** It is R26 L_r,Ein × (M*/L_r)_MW (Kroupa) = 2.84e10 × 4.04 M_sun. This assumes R26's luminosity aperture θ_Ein = 2.85″ is the same cylinder as R28's REin = 2.85″, which it is as printed. R26's luminosity uses its own distance from the Hubble flow. Its cosmology is not stated in R26 (sources.json says R25 supplies it), and I did not reconcile it.
5. **SLACS stellar mass.** It is R13 MChaBC2 as printed. These are integers in units of 10^10 M_sun (5 or 6), so the rounding is up to about 10%. R13's thetaE equals R5's bSIE for all four systems, so the cylinders match.
6. **S4TM stellar mass.** It is the printed total log M*^Chab × f(<R_E). For J1101+1523, θ_E (1.18″) is larger than R_eff (0.89″).
7. **Gas.** I added the hot-gas term of 0.12 % of M*(<R_E), with cold gas at 0, from descriptor.json x_baryon_inventory. That is a method file, but the value derives from reading/gas/adjudication_gas.md, which is not in the packet. For SNL-0, R28 states (footnote 3, PDF p.7) "We assume the gas mass projected within the Einstein radius is negligible". REPRODUCTION.md says a system-level statement takes precedence, but descriptor.json applies the registered term to all systems. I applied 0.12 % uniformly. The difference is 0.12 % in g_bar.
8. **IMF.** I used the defaults: Chabrier for SLACS (BC03) and S4TM, Kroupa for SNL-0. Salpeter tops were not computed.
9. **J1040+3626.** Its R10 Table 1 classification is "E-U-A". The table note does not define multiplicity code "U". This is recorded only; it does not affect the computation.

No arXiv downloads were needed; all sources were in the packet.
