# Reader A notes: aeg-d-strong-lensing_v1

Read only the packet at `/home/claude/audit_v2/packets/aeg-d-strong-lensing_v1/`. No downloads were needed: every record named in a locator (R5, R10, R13, R26, R28) was already in `sources/`. PDFs were converted to text with `pdftotext -layout` into my scratchpad.

## Main finding: method incomplete for every row

The method is `methods_page.txt` (it has no strong-lens formula), `REPRODUCTION.md`, `A6S_PRECEDENCE.md` and `descriptor.json`. Together they define:
- g_obs = G M_E / R_E²
- g_bar = G (M* + M_gas)(<R_E) / R_E²
- M_E = θ_E² c² D_s D_l / (4 G D_ls)
- R_E = θ_E D_l

None of them gives a numerical value for G, c, the solar mass in kg, or the length of a kpc or Mpc in metres. They point to the frozen code `aeg.lensing`, which is not in the packet. The brief says a constant the method does not state makes the step "method incomplete". So all 10 rows have status `method incomplete`, with g_obs and g_bar left empty.

What can be computed without constants is in `code/intermediates.csv` and in each row's notes:
- M_E where the source prints it;
- the Sérsic fraction;
- M*(<R_E) and M_bar(<R_E);
- the ratio M_E / M_bar, which equals g_obs/g_bar for the S4TM and SNL-0 rows.

For the SLACS rows, even the ratio needs c³/(G H0), because M_E has to be computed from θ_E.

If the maintainers want readers to reproduce m s⁻² values, the method should state G, c, M_sun, kpc and Mpc in SI, and the distance integral it uses (or that it uses astropy's FlatLambdaCDM).

## Steps where I made a judgement

1. **Gas term.** I used 0.12 % of M*(<R_E) for hot gas and 0 for cold gas. These are the registered defaults of `a6s_gas_in_RE` in `descriptor.json` (x_baryon_inventory). The methods page says only "default", with no number.
2. **Gas for SNL-0.** In R28, footnote 3 (p.7) the authors assume the gas inside R_E is negligible. A6S_PRECEDENCE §3.4 names ESO 325-G004 as an example of a "system-level statement". The method does not say whether this assumption overrides the registered term. If it gives zero gas, M_bar is 0.12 % lower. I used 0.12 %.
3. **S4TM profile fraction.** I used n = 4 (de Vaucouleurs, as Table 1 states), with b_n defined by P(2n, b_n) = ½ (b_4 = 7.66925). R_eff and b_SIE are both in the intermediate-axis convention, so I used their ratio as is. The method does not say whether to circularise.
4. **S4TM M_E.** I used the printed log M_Ein (Table 2, column 7), as REPRODUCTION.md says ("the default record's M_E as printed").
5. **SLACS stellar mass.** This is Grillo et al. 2009, MChaBC2 (BC03, Chabrier, R ≤ R_Ein). Grillo's thetaE equals R5's bSIE for all four systems, and both papers adopt (Ωm, ΩΛ, H0) = (0.3, 0.7, 70), so the apertures match. The masses are printed as integers in units of 10¹⁰ M_sun, which is coarse: about ±10 % rounding at the 5–6 level.
6. **SNL-0 radius.** R_E would be θ_E D_l with WMAP7 (H0 = 70.4, Ωm = 0.272). The source's zl is 0.0347 (CMB frame), and it also gives a heliocentric 0.0339. It prints D_l = 142 Mpc, 0.687 kpc/arcsec and R_Ein = 1.96 kpc. The method does not say which redshift to use. I would use the one labelled zl (0.0347), because that is the one the source used for D_l.
7. **SNL-0 stellar mass.** L_r,Ein × (M*/L_r)_MW (Kroupa), from Newman et al. 2017 Table 1. Both are inside θ_Ein = 2.85″, the same as R28's R_Ein.

Not verified: any uncertainty propagation (not asked for), and the frozen `aeg.lensing` code (not in the packet).
