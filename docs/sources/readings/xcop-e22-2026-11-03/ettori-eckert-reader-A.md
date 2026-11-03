# Reader A report: Ettori & Eckert 2022 (arXiv 2112.07554), read for X-COP v2

**Bottom line:** this paper adds almost nothing to g_obs or g_bar. It is a 6-page A&A Letter that models non-thermal pressure. It gives that pressure only as α = P_NT/P_tot at R500 and R200 for each of the 12 X-COP clusters, plus the model parameters (Table 1). It has no mass profiles and no Einasto, NFW or non-parametric reconstructions. It has nothing on the central galaxy, the satellites or intracluster light, and no radial acceleration relation. It releases no data and gives no table of R500 or M500. It predates Paper I (2205.01110) and 2205.01123 and cites neither. It cannot be one of the "2022 papers" that refined the core treatment in the sense of a new mass reconstruction. Its only statement about the core concerns the radial shape of the bias (item 8 and D).

## Header
- **Reader:** Reader A
- **Date:** 2026-11-03
- **Source read:** arXiv 2112.07554, version **v1**. It is the only version: the submission history lists only v1 (Tue, 14 Dec 2021 17:00:07 UTC).
  - Title: "Tracing the non-thermal pressure and hydrostatic bias in galaxy clusters"
  - Authors: S. Ettori, D. Eckert
  - Journal reference on the abs page: **A&A 657, L1 (2022)**; DOI 10.1051/0004-6361/202142638
  - Comments field: "6 pages, 3 figures. Accepted for publication in A&A Letters"
  - E-print SHA-256: `ef5cbd0a2d19b62428c362cfcbf973c3bdf928a3e8c6a36a547a6e9431a6e840`
  - Main file `p_nt_b_aa.tex` (447 lines), SHA-256 `c20d6303a6ea020003781040ba25303e312d5c1f463cb9830962e2d8f993ca4c`
  - Bibliography `p_nt_b_aa.bbl`, SHA-256 `86ca26539c5c7035f0f28ab826b69144fa7f785bcad374b19b495c38c08847a6`
  - Figure files `ai_bb.pdf`, `A1795_p_nt.pdf` and `vturb_bias.pdf` were rendered and looked at. They are part of the paper.
- **Not read:** Paper I (2205.01110) and 2205.01123, because this paper does not refer to them. No cited method paper was needed, because the paper itself contains no g_obs or g_bar reconstruction. No data files were opened.
- **Line numbers:** all quotes come from `p_nt_b_aa.tex`, with line numbers as in the e-print.

## A0. Relation to Paper I
- The paper does not refer to Paper I (Eckert et al. 2022, 2205.01110) or to 2205.01123. The .bbl has neither (checked all entries).
- **Where its inputs come from instead:**
  - The thermal-only mass is from Ettori et al. 2019. Line 182: "the observed $f_{g, T}$, which is based on the `thermal-only' gravitational mass profile \citep[described in][]{ettori19}" (`ettori19` = Ettori et al. 2019, A&A 621, A39; .bbl line 45).
  - The gas profiles are from Ghirardini et al. 2019 and Eckert et al. 2019 (lines 183–184).
  - The universal gas fraction is from Eckert et al. 2019. Lines 173–174: "we adopt the measurements of this universal gas fraction presented and discussed in our previous work \citep[see e.g. Sect. 3.1 in][]{eckert19}: $f_{g, U} (R_{500}) = 0.131 \pm 0.009$ and $f_{g, U} (R_{200}) = 0.134 \pm 0.007$."
- **Cosmology**, Sect. 2, line 104: "All the measurements quoted in the present analysis have been made assuming $H_0 = 70$ km s$^{-1}$ Mpc$^{-1}$ and $\Omega_{\rm m} = 0.3$." Lines 102–103 describe it as flat ("in a flat Universe with $\Omega_{\rm m} = 1 - \Lambda$").
- **What it does differently from Eckert et al. 2019**, lines 177–180: "In \cite{eckert19}, a model for $\alpha$ … presented in \cite{nelson14} … is adopted and solved iteratively in its two free parameters (a third scale parameter is maintained fixed). In the present work, we suggest adopting a modelization of the non-thermal pressure as directly proportional to the electron density". The new model is $P_{NT} = P_{0NT} \, (n/n_0)^{\beta}$ (line 141).

## A. Sample
1. **Clusters.** Table 1 (lines 256–279) lists 12 clusters: A1644, A1795, A2029, A2142, A2255, A2319, A3158, A3266, A644, A85, RXC1825 and ZW1215.
   - Abstract, line 30: "the X-COP sample that includes relaxed massive nearby systems".
   - There is no baryon-budget completeness classification. The paper never mentions the central galaxy, satellites or a "complete" budget. Stars enter only statistically inside $f_{g,U}$, line 172: "$f_{g, U} = f_{\rm b, sims} - f_{\rm star, stat}$".
2. **Radial range.** The paper does not give a radial range for each cluster.
   - The polytropic index is fitted over a common range. Table 1 footnote, line 275: "the effective polytropic index, $\gamma$, measured in the radial range $[0.3, 1.6] R_{500}$".
   - α is constrained at $R_{500}$ and $R_{200}$, line 227: "at (at least) two given points ($R_{500}$ and $R_{200}$, from the thermal mass profile, $M_T$)".
   - Fig. 2 (A1795) plots α(r) over roughly 100–2000 kpc. This is read off the figure, not stated in the text.
3. **Exclusions.** No cluster is excluded.
   - "Morphologically disturbed" is never defined. "Disturbed" appears only in a reference to simulations, lines 75–76: "less than few per cent in relaxed systems but comparable to the effect induced from turbulent and bulk motions in disturbed ones".
   - Five clusters are treated differently, with no model parameters fitted. Lines 304–305: "For five clusters, the constraints on $\alpha$ are consistent with zero: three of them have an estimated $F_i > 1$ at $R_{500}$ and/or $R_{200}$, implying a negative hydrostatic bias." These are A1644, A3266, A644, RXC1825 and ZW1215: their $P_{0NT}/P_{0T}$ and $\beta$ entries are "-" (lines 261, 268, 269, 271, 272).
   - Relaxation, lines 381–383: "confirming that our bright local systems are, on average, relaxed (i.e. closer to the assumption of a spherically symmetric gas distribution in hydrostatic equilibrium with the underlying gravitational potential), as they were selected at origin."

## B. g_obs
4. **How the total mass is obtained.** No new total-mass profile is reconstructed. The paper takes the "thermal-only" hydrostatic mass $M_T$ from Ettori et al. 2019 (line 182) and writes the relation to the "true" mass.
   - Eq. 2 (lines 62–63): $\frac{1}{\rho_{\rm gas}} \frac{dP_{\rm tot}}{dr} = -\frac{G M_{\rm tot}}{r^2}$
   - Eq. 3 (line 85): $M_{\rm tot} = M_T \frac{1 +A}{1 - \alpha}$, with $\alpha = P_{NT}/P_{tot}$ and $A = P_{tot}(d\alpha/dr)/(dP_T/dr)$ (lines 90–91).
   - The bias, Eq. 6 (line 111): "$b = b(r) = \frac{\alpha(r) +A(r)}{1+A(r)}$". Eq. 10 (line 155): $b = \frac{\beta P_{NT}}{\gamma P_T + \beta P_{NT}}$.
   - The paper does not mention the log-normal mixture, Einasto or NFW.
5. **Reconstructions presented.**
   - There is no Einasto, NFW, non-parametric or baryon-subtracted reconstruction.
   - The only tabulated parameters are those of the non-thermal pressure model, in Table 1 (lines 256–279): $\alpha_{500}/\alpha_{200}$ (E19), $F_{500}/F_{200}$, $\gamma$, $P_{0NT}/P_{0T}$, $\beta$ and $\alpha_{500}/\alpha_{200}$ (this work). For example, A1795 (line 262): "$6.6^{+3.8}_{-2.0} / 8.0^{+12.6}_{-5.6}$". A2319 (line 266): "$54.4^{+11.8}_{-7.3} / 67.4^{+12.5}_{-10.7}$".
   - Sample medians, lines 421: "the median estimates of $\beta$ (0.84) and $\gamma$ (1.19) recovered in the X-COP sample".
6. **Input data.**
   - Abstract, line 25: "X-ray (and Sunayev-Zel'dovich) derived radial profiles of the X-COP galaxy clusters".
   - Lines 410–411: "the X-COP results on the radial profiles of the gas density, temperature, and pressure".
7. **3D and radii.** The treatment is spherical through the hydrostatic equation (Eq. 2). α is given at $R_{500}$ and $R_{200}$ (Table 1). Overdensities are defined against the critical density (lines 100–101). The word "3D" is not used.
   - Lines 117–118: "only $M_{T}(R_{\Delta, T})$ is known, and $R_{\Delta, \rm tot}$ has to be inferred."
   - Line 224: "In the present analysis, because we do not use the profiles in numerical simulations, we assume $C_f = 1$."
8. **Correction to g_obs.** This is the whole subject of the paper: the non-thermal pressure correction $M_{tot} = M_T(1+A)/(1-\alpha)$. It is not applied to publish any corrected profile.
   - **Size by cluster:** α at R500 and R200 in Table 1, from 0 (five clusters) up to 54.4/67.4 for A2319.
   - **Sample summary**, line 381: "80\% of the objects with $b<0.17$ and 50\% with $b<0.03$ at $R_{500}$".
   - **Core / radial shape**, lines 376–377: "we estimated a median correction on the bias $b$, estimated at different radii, in the X-COP sample (see inset in Fig.~\ref{fig:vturb_bias}) and obtain $b(0.1 R_{500}) \approx 0.5 b(R_{500})$, with a general increase in the bias moving outwards." The Fig. 3 inset plots the median $b(r)/b(R_{500})$ over 0 to 1 $R_{500}$, with first and third quartiles (caption, line 400).

## C. g_bar
9. **Gas.** The gas mass is taken from earlier work, after a clumping correction. Lines 182–184: "the gas mass profile previously corrected for some gas clumping that might bias the gas density reconstruction (see the discussion on the recovered thermodynamic profiles in \citealt{ghirardini19} and Sect.~5.1 in \citealt{eckert19} on the systematic uncertainties affecting $f_{g, T}$)". Gas density conversion, footnote lines 68–69: "$\mu n_{\rm gas} = \mu_e n$, with $\mu \approx 0.6$ and $\mu_e \approx 1.16$".
10. **Central galaxy (BCG):** not stated.
11. **Satellites:** not stated.
12. **Intracluster light:** not stated.
13. **Other baryons:** only the statistical stellar fraction removed from the simulated baryon fraction (line 172).
14. **Whether g_bar is a 3D enclosed-mass acceleration:** not applicable. The paper builds no g_bar.

## D. Uncertainties

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | Provided by the paper or data? |
|---|---|---|---|---|---|---|---|
| E1 | Statistical error on α (Monte Carlo) | "the quoted errors on $\alpha$ are obtained from 100 Monte Carlo runs by propagating the statistical errors on the observed gas density and pressure profiles, and the observed gas fractions" | Table 1 footnote, l.276–277 | Per cluster, asymmetric, 1σ (e.g. A1795 $6.6^{+3.8}_{-2.0}$ at R500) | point (at R500 and R200, per cluster) | g_obs (M_tot/M_T) | Paper, Table 1. Correlation between the R500 and R200 values is not discussed. |
| E2 | Error on $F_{500}/F_{200}$ | "$0.942 \pm 0.073 / 0.931 \pm 0.058$" (A1795) | l.262 (Table 1) | ± per cluster, 1σ | point | g_obs (via α) and gas fraction | Paper, Table 1 |
| E3 | Error on polytropic index γ | "$1.090 \pm 0.096$" (A1795); "measured in the radial range $[0.3, 1.6] R_{500}$" | l.262, l.275 | ± per cluster, 1σ | system | g_obs (via α, b) | Paper, Table 1 |
| E4 | $P_{0NT}/P_{0T}$ and β | e.g. "1.79e-02 & 0.937" | l.262 | No uncertainty given | system | g_obs | Paper, point values only |
| E5 | Universal gas fraction (assumed prior) | "$f_{g, U} (R_{500}) = 0.131 \pm 0.009$ and $f_{g, U} (R_{200}) = 0.134 \pm 0.007$"; "a universal mean gas fraction has to be imposed on all the systems" | l.174, l.309 | ±0.009 (R500) and ±0.007 (R200) | dataset | g_obs (α, b) | Paper. Impact "can be easily quantified from Eq.~\ref{eq:f1f2}" (l.242) but no number is given, apart from E6. |
| E6 | Sensitivity to $f_{g,U}$ | "we require $f_{g,U}(R_{500})$ to be 62\% of the adopted value of 0.13 (i.e. a universal gas fraction of about 0.08)" | l.422–423 | Needed to reach b = 0.38 | dataset | g_obs | Paper (stated) |
| E7 | Assumption $C_f = 1$ | "we assume $C_f = 1$" | l.224 | Not quantified | dataset | g_obs, gas fraction | Assumption only |
| E8 | $p_0$ and β constant with radius | "if we assume that the unknowns $p_0 = P_{0T}/P_{0NT}$ and $\beta$ do not vary with radius (though this assumption can also be relaxed …)" | l.232 | Not quantified | system | g_obs | Assumption only |
| E9 | Gas clumping correction and $f_{g,T}$ systematics | "corrected for some gas clumping … Sect.~5.1 in \citealt{eckert19} on the systematic uncertainties affecting $f_{g, T}$" | l.183–184 | Not stated here | not stated | g_bar (gas) and g_obs (via $f_{g,T}$) | Deferred to Eckert et al. 2019 |
| E10 | Hydrostatic bias, sample distribution | "The measured bias in the X-COP sample … is 0.03 in 50\% of the objects and 0.17 in 80\% of them." | l.30; also l.381 | b < 0.03 (50%), < 0.17 (80%) at R500 | dataset (distribution) | g_obs | Paper. b is not tabulated per cluster; the Fig. 3 caption says it is inferred from Eq. 10 using Table 1 (l.396). |
| E11 | Radial shape of the bias toward the core | "$b(0.1 R_{500}) \approx 0.5 b(R_{500})$, with a general increase in the bias moving outwards" | l.377 | ×0.5 at 0.1 R500 (median); Fig. 3 inset shows quartiles | dataset (median) | g_obs | Paper (inset figure only) |
| E12 | Acceleration bias (simulations) | "less than few per cent in relaxed systems but comparable to … turbulent and bulk motions in disturbed ones … between 40 and 20 per cent of the non-thermal pressure support moving outwards" | l.75–77 | As quoted (literature) | not applied | g_obs | Literature only, not applied |
| E13 | Comparison with turbulence upper limits | "$b = \alpha$ from turbulence of about $<$11\%, $<$51\%, and $<$29\% for A85, A1795, and A2029" | l.385 | As quoted, 1σ upper limits | system | g_obs | Paper (from Pinto et al. 2015) |
| E14 | Planck-required bias (reference value) | "the value of $b=0.38 (\pm 0.03)$ required to reconcile … {\it Planck} data" | l.419–420 | 0.38 ± 0.03 | dataset (external) | — | Literature |

- **Confidence level**, l.276: "The quoted errors are at $1 \sigma$ c.l."
- **Not discussed in this paper:** the mass-to-light ratio or IMF, calibration, the choice of mass-reconstruction method, and the priors or regularisation of a non-parametric method.

## E. Radial acceleration relation
15–17. None. The paper has no g_obs–g_bar plot and no fitted relation. It does not compare clusters with galaxies, except to mention stellar dynamics in ellipticals as a way to constrain the potential (l.166, l.355–356).

**Conclusions, recorded only as stated:**
- Abstract l.31: "All these values are below the amount of bias required to reconcile the observed cluster number count in the cosmological framework set from {\it Planck}."
- Line 45 frames the paper as "non-thermal pressure, which supports the gas in equilibrium within an assumed dark-matter gravitation field". The keywords include "cosmology: dark matter" (l.34).

## F. Data availability
18–20. Nothing is released. The paper does not mention files, URLs, `hydromass`, licences, or g_obs and g_bar tables. It says nothing about the 12 mass reconstructions beyond using the Ettori et al. 2019 thermal-only profiles. The only URLs are instrument and project footnotes (XRISM, X-IFU, Athena, CHEX-MATE; l.427–430).

## G. Differences from Ettori et al. 2019 and the 2019 archive
- The paper does not state any update to masses, R500 values or redshifts. It has no per-cluster table of R500 or M500.
- It compares its α with Eckert et al. 2019 (Table 1, column 2) and states, l.303: "All our estimates are consistent with the results presented in \cite{eckert19}."
- Fig. 2 shows R500 and R200 for A1795 only as vertical lines. No values are given in the text.

## Not stated
I looked for all of the following in the whole `.tex` (including a grep for BCG|satell|stellar|Einasto|NFW|hydromass|available|archive|core|disturb|R500/M500|redshift), the `.bbl` and the three figures. None of them appear:
- per-cluster radial range;
- a definition of "morphologically disturbed";
- BCG, satellite, ICL or M/L treatment;
- Einasto, NFW or log-normal mixture reconstructions;
- per-cluster b values;
- errors on β and $P_{0NT}/P_{0T}$;
- correlations between radii;
- per-cluster R500, M500 or z;
- any data release;
- any reference to Paper I or 2205.01123.

## Doubts
1. **Paper identity.** The brief suggests this paper may be one of the "2022 papers" Ettori mentioned. It was submitted in December 2021, before Paper I, and does not refine any core mass treatment. Whether Ettori meant it is my inference: probably not, in the mass-reconstruction sense.
2. **Units of α in Table 1.** They are not stated. The values (e.g. 54.4, 67.4) look like percent, while the abstract and l.381 give b as fractions (0.03, 0.17). This is an inference.
3. **Table entries with a "+" sign on the lower error.** For example "$0.0^{+14.6}_{+3.9}$" (A644, l.269) and "$0.0^{+28.9}_{+9.8}$" (RXC1825, l.271). The meaning is unclear. Likewise the E19 column has entries with zero upper error, such as "$10.5_{-10.5}^{+0.0}$" (A1644, l.261).
4. **b versus α.** The X-COP b distribution (l.30, l.381, Fig. 3) comes from Eq. 10 using Table 1. Five clusters have no β, so for them b presumably equals 0. Fig. 3 starts at N(<b) ≈ 0.42 at b = 0, about 5/12. This is an inference from the figure.
5. **Internal check, my arithmetic.** l.385–387 says the Pinto et al. limits are "more than two and seven times" the constraints for A2029 and A1795. That matches 29/11.3 and 51/6.6. The "five clusters / three with F>1" statement (l.304) matches Table 1 (F>1: A1644, A3266 at R200, ZW1215).
6. **Section 4 algebra.** Eq. 13 (l.333) sets $P_{NT} = \eta P_T$, and l.340 then says "by requiring that $P_B \equiv P_{NT}$". I report this as written.
7. **Abstract versus text, b < 0.2.** The abstract's "50 per cent … $b < 0.2$" (l.28–29) corresponds to the text's 0.19 (l.375).
8. **Cropped figures.** The figure PDFs are cropped by `trim` in the LaTeX, so the published figures may show less than the files I rendered.