# Method gaps (pilot audit, aeg-d-dwarfs/v3, rows m000053 and m000014)

Steps I had to infer, even where confident:

1. **Ret III m_V,0 route ("M_V + (m-M) used by the paper (own)").** The method does not name the paper or table that M_V comes from. The rows.json locator lists 11 candidate sources and says only "the system's row in the paper that gives its distance modulus". I inferred Drlica-Wagner 2015, **Table 2** (M_V = -3.3), p.17; the locator does not name the table. Because m_V,0 is rebuilt with the same modulus used for L_V, L_V does not depend on distance here. The method does not say this.
2. **Modulus versus printed kpc.** Savino 2022 prints both μ = 24.40 and D = 758.6 kpc. Drlica-Wagner prints m-M = 19.81 (Table 1) and 92 ± 13 kpc (Table 2). §3 says "a modulus is turned into kpc" but does not say which wins when both are printed. I used the modulus. Using 758.6 kpc instead would change And XVII g by about 3e-5 relative.
3. **Rounding order.** The method rounds D (kpc) to 6 significant figures but does not say whether μ for L_V is then recomputed from the rounded D. I used the original μ, which makes a negligible difference. It also does not say whether R_h is rounded before or after circularisation. I rounded after.
4. **Unit of the Ret III r_h.** The column header extracts as "(0 )". I inferred arcmin from the paper's convention and checked it: 2.4′ at 92 kpc = 64 pc, which matches Table 2's r1/2 = 64 ± 24 pc.
5. **Fritz 2019 Table 3 preference.** Bold type (the preferred value) cannot be seen in the text extraction. Ret III appears only once, in the upper block (all possible members), so there was only one value to choose. The method states a preference rule for Phoenix II only.
6. **Collins 2013 Table 4 versus Table 5.** The locator names both tables. σ and [Fe/H] (−1.7) agree, but the [Fe/H] uncertainties differ (±0.2 versus ±0.3). The method does not say which table is primary. The g values are not affected.
7. **"Keep one row per [Fe/H]" in the Υ_V table.** The method does not say which duplicate row to keep. In this file, every duplicate [Fe/H] has the same (M/L)1, so the result is not affected.
8. **Ret III Υ_V is beyond the table.** [Fe/H] = −2.81 is below the table minimum of −2.29, so the end value 1.931 was used (flag beyond_source_range), as §3.5 says. This is not a gap, but it is recorded here.
9. **Upper-limit propagation.** For Ret III, σ is an upper limit (the 90th percentile of the posterior), so g_obs is an upper limit. The method does not say whether g_bar or the ratio carry any limit flag. I left g_bar as a value.
10. **Source inconsistency (not a method gap).** Fritz 2019 p.3 quotes Ret III's modulus as 19.82 ± 0.31 and cites Drlica-Wagner 2015a, but Drlica-Wagner Table 1 prints 19.81. I used 19.81, as the locator says.
11. **Ret III ellipticity.** It is an upper limit (< 0.4) and is unused, because the method treats r_h as circularised. That convention is confirmed by the Table 1 caption ("azimuthally averaged half-light radius").
12. **Martin 2016 r_h axis.** The method says semi-major. I confirmed this from Martin 2016 eq. 5: the elliptical radius is scaled along the major axis.
