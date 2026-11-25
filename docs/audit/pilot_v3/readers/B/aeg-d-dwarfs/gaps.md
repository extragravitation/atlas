# Method gaps (aeg-d-dwarfs/v3, rows m000053 Reticulum III, m000014 Andromeda XVII)

Every step below had to be inferred. Where I am confident, I say so, but it is still a gap in the written method.

1. **The selection records are missing from the packet.** The σ and [Fe/H] locators point to `v1/reading/sigma_selection_v3.csv`, `sigma_reading_1.csv`, `feh_values.csv` and `feh_reading_1.csv/_d059.csv/_followup.csv`. None of these is in the packet, so the selected value has to be inferred from the page and table lists.
   - Ret III: there is only one candidate value, so this is unambiguous.
   - And XVII σ: Tables 4 and 5 agree on 2.9 km/s, so this is unambiguous.
   - And XVII [Fe/H]: see gap 2.
2. **And XVII [Fe/H]: which column is not stated.** Collins 2013 Table 5 prints both [Fe/H]phot (−1.9) and [Fe/H]spec (−1.7±0.3). Table 4 and the Fig. on p.30 print only the spectroscopic value (−1.7±0.2). I used −1.7 (spectroscopic), because all three cited pages carry it.
   - Effect: with −1.9, Υ_V goes from 1.867 to 1.874, and g_bar goes from 1.76103e-13 to 1.76764e-13 (+0.4%).
3. **Ret III: where M_V comes from.** The route is "M_V + (m−M) used by the paper (own)", and the locator names "the system's row in the paper that gives its distance modulus" (DES 2015 Table 1). That row has no M_V. M_V (−3.3) is in Table 2, same page, same system.
   - The paper is identified only indirectly: the source_ref "names no paper", and the locator lists 11 candidate sources. I took DES 2015 because it gives the distance observable.
4. **Ret III: m_V,0 rebuilt and then converted back.** m_V,0 = M_V + 19.81, then L_V uses μ of the package distance, which is the same 19.81. So L_V depends only on M_V. This is implied, not stated; no ambiguity in the result.
5. **Distance when both a modulus and a kpc value are printed.**
   - Savino Table 5 prints μ = 24.40 and D = 758.6 kpc. DES 2015 prints m−M = 19.81 in Table 1 and 92 kpc in Table 2.
   - The method does not say which to use. I used the modulus that the locator's table gives.
   - Effect for And XVII: < 3e-5 relative.
   - Effect for Ret III: if 92 kpc (Table 2) were used, g_obs would fall by 0.4%.
6. **Rounding order is unclear.** "Rounds R_h (arcmin), D (kpc), L_V and M_gas to six significant figures, and m_V,0 to four decimals, before step 8."
   - It is not stated whether μ for L_V is recomputed from the rounded D, or whether R_h is rounded after circularisation. I applied both roundings after the step that produces each quantity.
   - Effect: about 1e-6 relative.
7. **Circularised radius: ε ignored.** Ret III's convention is "circularised", so ε (< 0.4, an upper limit) is not used. The method does not say how an ε upper limit would be treated for a semi-major radius. That case does not arise here.
8. **Υ_V interpolation details.**
   - "Keep one row per [Fe/H]" does not say which row. In this table, rows with the same rounded [Fe/H] have identical (M/L)1, so the choice is harmless.
   - The method says `Cluster` "begins with 'MW'", while the VOTable values look like "MW-NGC5053". The prefix match is unambiguous.
9. **The gas row name relies on gas_values.csv,** which is not in the packet. I used the row names given in METHOD.md §7 ("Reticulum III", "Andromeda XVII"), which match Putman Table 1 rows exactly. Both are upper limits (`<`), so there is no gas term.
10. **Upper-limit σ (Ret III).** σ < 31.2 is the 90th percentile of the posterior (Table 3 caption). The method says to use the stated value as an upper limit, which I did. That the percentile definition does not matter is inferred.
11. **Page numbering.** "page" is taken as the PDF page number. For Fritz 2019, this equals the printed "page N of 16". The Fritz σ locator lists "page 12; 1": no Ret III σ value appears on p.1 (the abstract gives only Phoenix II's).
12. **The Collins σ locator lists 13 pages** (27; 33; 37; 39; 40; 10; ...) with no row or column. Values differ by table only in their errors (Table A1 "full algorithm": 2.9 +5.0/−2.9, vs Tables 4/5: 2.9 +2.2/−1.9). The central value is the same, so g_obs is unaffected.
