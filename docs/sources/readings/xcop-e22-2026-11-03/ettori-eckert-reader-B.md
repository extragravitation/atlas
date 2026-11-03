# Reader B report: Ettori & Eckert, arXiv 2112.07554

**Reader:** Reader B
**Date:** 2026-11-03

**Sources read**

| Source | arXiv id / version | Main .tex | SHA-256 of e-print |
|---|---|---|---|
| Ettori, S. & Eckert, D., "Tracing the non-thermal pressure and hydrostatic bias in galaxy clusters" | 2112.07554 v1. This is the only version: "[v1] Tue, 14 Dec 2021 17:00:07 UTC (194 KB)". | `p_nt_b_aa.tex` (447 lines), plus `p_nt_b_aa.bbl` | `ef5cbd0a2d19b62428c362cfcbf973c3bdf928a3e8c6a36a547a6e9431a6e840` |

- The title and authors match the abs page.
- **Journal reference** (abs page): "A&A 657, L1 (2022)". DOI 10.1051/0004-6361/202142638.
- The e-print is a gzip tarball containing `p_nt_b_aa.tex`, `p_nt_b_aa.bbl`, `aa.cls`, `aa.bst` and three figure PDFs: `A1795_p_nt.pdf`, `ai_bb.pdf` and `vturb_bias.pdf`. The figure PDFs contain no text that can be extracted (pdftotext returns nothing), so I took figure content from the captions only.
- I read no other paper. Paper I (2205.01110) and 2205.01123 are **not cited** in this paper; the bibliography has 31 entries and neither is among them. So under the brief's rule I did not download them and have no SHA-256 for them. I did not open any cited method paper (see Doubts D1).
- All locations below are line numbers in `p_nt_b_aa.tex` unless marked `.bbl`.

**Overall finding, stated once.** This paper is a 4-page Letter that models non-thermal pressure. It contains no g_obs or g_bar profiles, no BCG or satellite modelling, no radial acceleration relation and no data release. It was written before Paper I, and it builds on the 2019 X-COP products (Ettori+2019, Eckert+2019, Ghirardini+2019), not on the 2022 analysis. What it gives for the Atlas is:
- a per-cluster non-thermal pressure fraction α at R500 and R200, with model parameters (Table 1);
- a stated median radial scaling of the bias into the core.

Most items in the brief are therefore "Not stated".

---

## A0. Relation to Paper I

- **No relation stated.** Paper I (Eckert et al. 2022, arXiv 2205.01110) and 2205.01123 are not cited anywhere (bibliography, `.bbl` lines 1–166). The paper went on arXiv on 2021-12-14, before both.
- **What it takes from earlier X-COP work instead:**
  - The thermal-only mass profile: "the `thermal-only' gravitational mass profile \citep[described in][]{ettori19}" (l. 182). `ettori19` is Ettori et al. 2019, A&A 621, A39 (`.bbl` l. 42–45).
  - The clumping-corrected gas mass: "the gas mass profile previously corrected for some gas clumping … (see the discussion on the recovered thermodynamic profiles in \citealt{ghirardini19} and Sect.~5.1 in \citealt{eckert19} …)" (l. 183–184).
  - The universal gas fraction: "we adopt the measurements of this universal gas fraction presented and discussed in our previous work \citep[see e.g. Sect. 3.1 in][]{eckert19}: $f_{g, U} (R_{500}) = 0.131 \pm 0.009$ and $f_{g, U} (R_{200}) = 0.134 \pm 0.007$." (l. 173–174)
  - The polytropic description: "As we have shown in \cite{ghirardini19poly}, a polytropic function … is a very good representation for the thermal gas distribution" (l. 137).
- **Cosmology:** "All the measurements quoted in the present analysis have been made assuming $H_0 = 70$ km s$^{-1}$ Mpc$^{-1}$ and $\Omega_{\rm m} = 0.3$." (l. 104)
- **What it does differently from Eckert+2019:** "In \cite{eckert19}, a model for $\alpha$ (instead of $P_{NT}$) -- presented in \cite{nelson14} … -- is adopted … In the present work, we suggest adopting a modelization of the non-thermal pressure as directly proportional to the electron density" (l. 177–179). On consistency: "All our estimates are consistent with the results presented in \cite{eckert19}." (l. 303)

## A. Sample

**1. Which clusters.** The X-COP objects: "the observed thermodynamic profiles recovered for the objects in our {\it XMM-Newton} Cluster Outskirts Project (X-COP) sample \citep{xcop}" (l. 46).
- Table 1 lists 12 clusters (l. 261–272): A1644, A1795, A2029, A2142, A2255, A2319, A3158, A3266, A644, A85, RXC1825, ZW1215.
- "Complete baryon budget" (hot gas, central galaxy, satellites): **not stated**. The only baryons modelled are gas, through f_gas. Stars enter only as a statistical correction inside the simulated universal fraction: "$f_{g, U} = f_{\rm b, sims} - f_{\rm star, stat}$" (l. 172).

**2. Radial range.**
- The constraints are at two radii: "at (at least) two given points ($R_{500}$ and $R_{200}$, from the thermal mass profile, $M_T$)" (l. 227).
- γ is measured "in the radial range $[0.3, 1.6] R_{500}$" (Table 1 footnote, l. 275).
- Fig. 2 shows α(r) as a function of radius for A1795 only (l. 287).
- The Fig. 3 inset shows the median b versus radius (l. 399–400).
- No per-cluster radial range of the input profiles is stated.

**3. Exclusions or different treatment.**
- No cluster is excluded. All 12 appear in Table 1.
- Five clusters are treated as having no solution: "For five clusters, the constraints on $\alpha$ are consistent with zero: three of them have an estimated $F_i > 1$ at $R_{500}$ and/or $R_{200}$, implying a negative hydrostatic bias." (l. 304–305) In Table 1 these rows show "-" for $P_{0NT}/P_{0T}$ and β: A1644, A3266, A644, RXC1825 and ZW1215.
- **No criterion for "morphologically disturbed" is given.** The only related statements are:
  - "less than few per cent in relaxed systems but comparable to the effect induced from turbulent and bulk motions in disturbed ones" (l. 75–76; about simulations);
  - "confirming that our bright local systems are, on average, relaxed (i.e. closer to the assumption of a spherically symmetric gas distribution in hydrostatic equilibrium with the underlying gravitational potential), as they were selected at origin." (l. 382–383)

## B. g_obs

**4. How the total mass is obtained.** The hydrostatic equation with total pressure:
- "$\frac{1}{\rho_{\rm gas}} \frac{dP_{\rm tot}}{dr} = -\frac{d\phi}{dr} = - \frac{G M_{\rm tot}}{r^2}$" with "$P_{\rm tot} = P_T +P_{NT}$" (l. 62–66).
- The relation between the two masses: "$M_{\rm tot} = M_T \frac{1 +A}{1 - \alpha}$" (l. 85), with "$\alpha = P_{NT}/P_{\rm tot}$" and "$A = P_{\rm tot} \frac{d\alpha/dr}{d P_T/dr}$" (l. 90–91).
- The thermal-only mass M_T is taken from Ettori+2019 (l. 182).
- The true mass is fixed by requiring the gas fraction to equal the universal value: "The total true mass is then recovered by comparing $f_{g, U}$ to the observed $f_{g, T}$" (l. 182).
- The paper contains no log-normal mixture or other non-parametric mass method.

**5. Reconstructions presented.** No Einasto, NFW, non-parametric or baryon-subtracted mass profiles are presented. What is presented is Table 1 (l. 256–279), which gives, per cluster:
- α500/α200 from E19;
- F500/F200;
- γ;
- $P_{0NT}/P_{0T}$;
- β;
- α500/α200 from this work.

The model is "$P_{NT} = P_{0NT} \, (n/n_0)^{\beta}$" (l. 141) and "$P_T = P_{0T} \, (n/n_0)^{\gamma}$" (l. 138).

**6. Input data.**
- From the abstract: "the X-ray (and Sunayev-Zel'dovich) derived radial profiles of the X-COP galaxy clusters" (l. 25).
- From the conclusions: "the X-COP results on the radial profiles of the gas density, temperature, and pressure" (l. 410).

**7. Spherical 3D masses, and at which radii.**
- The masses are at overdensities: "$\Delta = M_{\Delta} / (4/3 \pi \rho_{cz} R_{\Delta}^3$)" (l. 100).
- Spherical symmetry is implied: "closer to the assumption of a spherically symmetric gas distribution in hydrostatic equilibrium" (l. 382). That is the only explicit mention.
- Radii: R500 and R200.

**8. Corrections to g_obs.** This is the paper's subject.
- The correction is $M_{\rm tot} = M_T (1+A)/(1-\alpha)$ (l. 85). Bias is defined by "$M_{\Delta, T} =  (1-b) M_{\Delta, \rm tot}$" (l. 97) and "$b = \frac{\alpha \beta}{(1-\alpha) \gamma +\alpha \beta}$" (l. 155).
- Per-cluster α values at R500/R200 are in Table 1, last column (l. 261–272). Examples:
  - A2319: "$54.4^{+11.8}_{-7.3} / 67.4^{+12.5}_{-10.7}$" (l. 266);
  - A1795: "$6.6^{+3.8}_{-2.0} / 8.0^{+12.6}_{-5.6}$" (l. 262).
- Per-cluster b is **not tabulated**. Only the distribution is given: "80% of the objects with $b<0.17$ and 50% with $b<0.03$ at $R_{500}$" (l. 381).
- **On the core:** "we estimated a median correction on the bias $b$, estimated at different radii, in the X-COP sample (see inset in Fig.~\ref{fig:vturb_bias}) and obtain $b(0.1 R_{500}) \approx 0.5 b(R_{500})$, with a general increase in the bias moving outwards." (l. 376–377)
- No corrected mass profiles or corrected M500 values are given.

## C. g_bar

**9. Gas.**
- The gas mass comes from earlier work, with a clumping correction: "the gas mass profile previously corrected for some gas clumping that might bias the gas density reconstruction (see … \citealt{ghirardini19} and Sect.~5.1 in \citealt{eckert19} …)" (l. 183–184).
- The paper's own constants: "$\mu \approx 0.6$ and $\mu_e \approx 1.16$" (l. 69).

**10. Central galaxy (BCG):** not stated.

**11. Satellites:** not stated.

**12. Intracluster light:** not stated.

**13. Other baryons.** Only the simulated statistical stellar fraction removed from f_b inside f_{g,U} (l. 172). This is not a baryon component of any cluster.

**14. Is g_bar a 3D enclosed-mass acceleration?** Not stated as such. f_gas = M_g/M_tot at R_Δ (l. 187) implies an enclosed gas mass, but the paper presents no g_bar.

## D. Uncertainties

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | Provided? |
|---|---|---|---|---|---|---|---|
| E1 | Statistical error on α (non-thermal fraction) | "The quoted errors are at $1 \sigma$ c.l., and the quoted errors on $\alpha$ are obtained from 100 Monte Carlo runs by propagating the statistical errors on the observed gas density and pressure profiles, and the observed gas fractions." | Table 1 footnote, l. 276–277 | Per cluster at R500 and R200, e.g. A2142 "$19.9^{+2.9}_{-2.3} / 23.4^{+7.6}_{-5.6}$" | point (two radii per cluster) | g_obs (if corrected) | Paper, Table 1 |
| E2 | Universal gas fraction f_{g,U} (simulation-based prior) | "$f_{g, U} (R_{500}) = 0.131 \pm 0.009$ and $f_{g, U} (R_{200}) = 0.134 \pm 0.007$"; "although a universal mean gas fraction has to be imposed on all the systems" | l. 174; l. 309 | ±0.009 / ±0.007. Effect shown qualitatively: "$\alpha$ increases as $F$ decreases" (l. 245). Example: b = 0.38 would require f_{g,U}(R500) "62\% of the adopted value of 0.13" (l. 422–423) | dataset | g_obs | Paper (values); effect via Eq. f1f2 / Fig. 1 only |
| E3 | Gas-fraction ratio F = f_{g,U}/f_{g,T} | Table 1 column "$F_{500} / F_{200}$" | l. 260–272 | e.g. A2319 "$0.693 \pm 0.056 / 0.565 \pm 0.041$" | point (two radii) | g_obs | Paper, Table 1 |
| E4 | Effective polytropic index γ | "the effective polytropic index, $\gamma$, measured in the radial range $[0.3, 1.6] R_{500}$" | l. 275 | per cluster, e.g. A644 "$1.356 \pm 0.118$" | system | g_obs | Paper, Table 1 |
| E5 | Gas clumping / systematics on f_{g,T} | "corrected for some gas clumping that might bias the gas density reconstruction (see … Sect.~5.1 in \citealt{eckert19} on the systematic uncertainties affecting $f_{g, T}$)" | l. 183–184 | not stated here | not stated | g_bar (gas), and g_obs through F | Referred to Eckert+2019 |
| E6 | Radius-conversion factor C_f | "In the present analysis, because we do not use the profiles in numerical simulations, we assume $C_f = 1$." | l. 224 | not stated | dataset | g_obs | Assumption only |
| E7 | p0 and β constant with radius | "if we assume that the unknowns $p_0 = P_{0T}/P_{0NT}$ and $\beta$ do not vary with radius (though this assumption can also be relaxed once more measurements of $F_i$ are available)" | l. 231–232 | not stated | system | g_obs | Assumption only |
| E8 | Choice of P_NT model (method choice) | "All our estimates are consistent with the results presented in \cite{eckert19}." | l. 303 | E19 versus this work, side by side in Table 1 columns 2 and 7 | system | g_obs | Paper, Table 1 |
| E9 | Acceleration bias (temporal velocity variations) | "have been shown in \cite{nelson14} to be less than few per cent in relaxed systems but comparable to the effect induced from turbulent and bulk motions in disturbed ones, with a contribution that spans values between 40 and 20 per cent of the non-thermal pressure support moving outwards" | l. 75–77 | "few per cent" (relaxed); "40 and 20 per cent" of P_NT support (simulations) | not stated | g_obs | Literature statement; not applied separately |
| E10 | Radial behaviour of the bias into the core | "$b(0.1 R_{500}) \approx 0.5 b(R_{500})$, with a general increase in the bias moving outwards" | l. 377 | median factor ≈0.5 at 0.1 R500 | dataset (median) | g_obs | Fig. 3 inset only (median, 1st/3rd quartiles, l. 400); no numbers |
| E11 | Hydrostatic bias distribution in X-COP | "80\% of the objects with $b<0.17$ and 50\% with $b<0.03$ at $R_{500}$" | l. 381 (also abstract, l. 30) | 0.17 (80 %), 0.03 (50 %) | dataset | g_obs | Paper text; Fig. 3 |
| E12 | Cosmology | "$H_0 = 70$ … $\Omega_{\rm m} = 0.3$" | l. 104 | fixed | dataset | both (via R_Δ) | Stated |
| E13 | Mean molecular weights | "$\mu \approx 0.6$ and $\mu_e \approx 1.16$" | l. 69 | fixed | dataset | both | Stated |

**Correlations between radii:** not discussed or provided for any term. The only joint treatment is the 100 Monte Carlo runs in E1.

**Brief's examples:**
- **Hydrostatic bias:** E1–E11.
- **M/L or IMF:** not stated.
- **Calibration:** not stated.
- **Choice of method:** E8.
- **Non-parametric prior or regularisation:** not applicable; no such method is in the paper.

## E. Radial acceleration relation as presented

**15–17.** Not stated. The paper contains no g_obs–g_bar plot, binning, fitted relation or scatter, and no comparison with galaxies.

**Stated conclusions about accounts (recorded only):**
- "an assumed dark-matter gravitation field" (l. 45).
- Keyword "cosmology: dark matter" (l. 34).
- "All these values are below the amount of bias required to reconcile the observed cluster number count in the cosmological framework set from {\it Planck}." (l. 31)
- "the value of $b=0.38 (\pm 0.03)$ required to reconcile the measurements of the cosmic microwave background anisotropies with the SZ-based cluster number count from {\it Planck} data" (l. 419–420).
- "Overall, these distributions of the hydrostatic bias, $b$, at $R_{500}$ are in good agreement with the mean values of about 10-20 per cent obtained in hydrodynamical simulations" (l. 389–390).

## F. Data availability

**18–20.** Not stated. There is no release statement, no column or file description, no URL to data, no mention of `hydromass`, no licence, and nothing about 12-cluster mass reconstructions.
- The only URLs in the paper are instrument and project footnotes: XRISM, X-IFU, Athena and CHEX-MATE (l. 427–430).

## G. Differences from Ettori et al. 2019 / the 2019 public archive

- There are no updated masses, R500, M500 or redshifts, and no per-cluster R500/M500 table.
- The only difference stated is the non-thermal model (l. 177–179) and the resulting α compared with E19 (Table 1 columns 2 and 7). Example, A2319: E19 "$43.6_{-3.6}^{+3.5} / 52.3_{-4.6}^{+3.4}$" versus this work "$54.4^{+11.8}_{-7.3} / 67.4^{+12.5}_{-10.7}$" (l. 266).
- The paper uses the 2019 thermal-only masses (l. 182).

---

## Not stated

Searched across the full `p_nt_b_aa.tex` (all 447 lines read), the `.bbl`, and the figure PDFs (no extractable text). Not found:
- any link to Paper I or 2205.01123;
- "complete" baryon budget;
- BCG, satellites, intracluster light, M/L or IMF;
- the log-normal mixture, Einasto or NFW parameters;
- baryon-subtracted profiles;
- per-cluster R500, M500 or redshift;
- per-cluster b values (only α, plus the parameters to compute b through Eq. b_a);
- corrected M_tot profiles;
- radial ranges of the input profiles;
- a "morphologically disturbed" criterion;
- correlations between radii;
- calibration systematics;
- any g_obs–g_bar relation;
- data release, licence or software.

Grep for "core", "kpc", "clump", "disturb", "relaxed", "available" and "http" found only the lines quoted above.

## Doubts

- **D1. Method papers not opened.** M_T comes from Ettori+2019 (A&A 621, A39) and the clumping-corrected gas from Ghirardini+2019 and Eckert+2019. I did not open them, so how M_T is reconstructed (B4) is known here only as "described in ettori19". Reader A may have read them; any difference between our reports there comes from scope, not reading.
- **D2. Brief premise.** The brief calls Paper II "2205.01123" and suggests this paper may be one of the "2022 papers" that refined the core treatment. This paper is published in 2022 (A&A 657, L1) but predates Paper I and uses the 2019 products. Its only core statement is the median b(0.1 R500) ≈ 0.5 b(R500) (l. 377). Whether Ettori meant this paper is not answerable from the paper.
- **D3. Units of α in Table 1.** Table 1 gives α as values such as 54.4, while α is defined as the fraction P_NT/P_tot (l. 90). I infer the Table 1 values are per cent; the table does not say so.
- **D4. Zero-α rows.** Lower errors with a positive sign, e.g. "$0.0^{+14.6}_{+3.9}$" (A644, l. 269) and "$0.0^{+28.9}_{+9.8}$" (RXC1825, l. 271), are not explained. They are reproduced as published.
- **D5. Which three have F > 1.** The text names no clusters (l. 304). From Table 1, F_i > 1 holds for A1644 (1.023/1.063), A3266 (1.241 at R200) and ZW1215 (1.236/1.457), which is consistent with "three". This identification is my inference.
- **D6. Small mismatches within the paper:**
  - The abstract has "b < 0.2" (50 %) and "0.03 in 50\% … 0.17 in 80\%" (l. 28–30); the body has "0.19" (l. 375) and "$b<0.03$ … $b<0.17$" (l. 381). These may be rounding.
  - The Table 1 header cites "(E19)" while the footnote cites `eckert19` (l. 260, 274). I assume both mean Eckert+2019.
  - Line 385 says "$b = \alpha$ from turbulence", while Eq. b_a (l. 155) gives b = α only when β = γ (l. 158).
- **D7. Spherical symmetry and 3D.** Neither is stated explicitly for the masses. I inferred them from the R_Δ definition (l. 100) and l. 382.
- **D8. The 12 X-COP clusters.** Table 1 lists the 12 X-COP clusters. I did not check whether this matches the 12 in Paper I.

Next step for the comparer: settle D1 against Ettori+2019 if Reader A read it, and confirm D3 (per-cent units) from the published A&A table.