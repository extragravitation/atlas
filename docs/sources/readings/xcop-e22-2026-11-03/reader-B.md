# Reader B report: Eckert et al. 2022 (X-COP v2, Atlas step A, D-089)

**Bottom line:** the candidate arXiv id in the brief (2205.01123) is the wrong paper. The paper is **arXiv:2205.01110v1**. Read as published there, it does not describe any release of g_obs or g_bar tables. The only things it says are released are the `hydromass` code, the mock-data generator and the earlier 2019 X-COP products.

## Header

- **Reader:** Reader B
- **Date:** 2026-11-03
- **Working directory:** /tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/e22_readerB
- **Identifying the paper:** I checked https://arxiv.org/abs/2205.01123 and it does not match. Its title is "Constraints on dark matter self-interaction from the internal density profiles of X-COP galaxy clusters" (Eckert, Ettori, Robertson, Massey, Pointecouteau, Harvey, McCarthy), journal ref "A&A 666, A41 (2022)", DOI 10.1051/0004-6361/202243205. That is the companion "Paper II". I did not download it. A search of arxiv.org found the correct id, **2205.01110**: title "The gravitational field of X-COP galaxy clusters"; authors Eckert, D.; Ettori, S.; Pointecouteau, E.; van der Burg, R. F. J.; Loubser, S. I.; journal ref "A&A 662, A123 (2022)"; DOI 10.1051/0004-6361/202142507. Only a v1 exists (2 May 2022), with the comment "Accepted for publication in A&A".

**Sources read:**

| Source | arXiv id, version | Main .tex | SHA-256 of e-print |
|---|---|---|---|
| Eckert et al. 2022, A&A 662, A123 (the paper) | 2205.01110v1 | `hydromass.tex` (727 lines; SHA-256 of the .tex is fdf040686a41eee38be2b9a2feb28c1c97b0b8cc0a4c8a7aa78785947cfa5cb1) | 18fc2e8025f56c716a864e5ef9436cccb5f0be05cff7a0f004aedd4605e5c7d8 |
| Loubser et al. 2020, MNRAS 496, 1857 (BCG method; cited as `loubser20`) | 2006.05706v1 | `BCG_v3_withoutBold.tex` | ded65c6d1457b3183ee21b573bf426bf5ddfd20575fc39f429eb0e887dd9044c |
| van der Burg et al. 2015, A&A 577, A19 (satellite method; cited as `vdb15`) | 1412.2137v2 | `paper_publisher.tex` | 17fd10bfdf5ab6ec9f374385f73663a15677b31eefeec97440da6a3614d5ea5d |
| Ghizzardi et al. 2021, A&A 646, A92 (X-COP satellite stellar-mass profiles; cited as `ghizzardi21`) | 2007.01084v1 | `xcop-metallicity.tex` | 88c8e91c036077e2ca660cd029943d576df1462daae914d3e58aa24169c5a9e8 |

- I opened none of the shared data files, nothing from drive.switch.ch, and no data products outside the papers. Nothing downloaded was executed.
- Unless stated otherwise, every location below refers to `hydromass.tex` in 2205.01110v1. Many lines in it are whole paragraphs, so a line number points to a paragraph.

---

## A. Sample

**1. Clusters analysed, and which have the complete baryon budget**

- **All 12 are analysed.** L342: "to analyze the gravitational field of the 12 X-COP clusters". Table 1 (`tab:master`, L324–335) lists A85, A644, A1644, A1795, A2029, A2142, A2255, A2319, A3158, A3266, RXC1825 and Zw1215.
- **Five have the complete budget.** L402 (Sect. 4.3): "for a subset of systems (A644, A1795, A2029, A2142, and A2319) we have access to precise measurements of the stellar mass profiles of the cluster's BCG \citep{loubser20} and of the cumulative stellar mass of satellite galaxies \citep{vdb15}. Therefore, with the exception of a potential contribution of intracluster light (ICL) we have direct measurements of the mass profiles of all the baryonic components (gas, BCG, and satellites)."
- The same five are named for the BCG at L103 ("For the BCGs of A644, A1795, A2029, A2142, and A2319, we used stellar mass distributions from \citet{loubser20}") and for the satellites at L114 ("the same five clusters (A644, A1795, A2029, A2142, and A2319)").
- **The RAR uses only these five.** L518: "we provided a detailed reconstruction of the RAR in a subset of five systems (see Fig. \ref{fig:rar})". L541: "in the five systems for which the baryonic content can be completely characterized".

**2. Radial range**

- Sample-wide: L528, "over the radial range $[0.01-2]R_{500}$". L512: "the entire radial range of interest ($[0.01-2]R_{500}$...)". L38 (abstract): "over two decades in radius".
- NP method: L342, "we restrict specifically to the radii corresponding to the existing spectral and SZ data points to avoid extrapolating". L263: "we evaluate it at the radii of the observed data and present them in the form of data points".
- BCG stellar profile: L404, "can be estimated only within a limited radial range out to $\sim50$ kpc".
- Satellite profile fit: L408, "beyond the BCG ($R>100$ kpc)".
- **No per-cluster radial range is given in the text or tables.** The per-cluster appendix figures (L558–723) presumably show it, but I could not read their values from the source.

**3. Clusters excluded or treated differently**

- **Seven of the 12 lack a complete stellar inventory**, so they are left out of the decomposition, the baryon fraction and the RAR (L402, L518). The paper gives no reason why these seven lack the data.
- **A3266 and A2029 have new XMM data.** L65: "we add a set of 6 additional \emph{XMM-Newton} pointings that were obtained during AO-17 ... on two clusters (A3266 and A2029)". L70: "With the exception of the two systems with new observations (A3266 and A2029), we employ the publicly available data products presented in \citet{ghirardini19}".
- **A644 and A2319 have no weak-lensing mass for the BCG model.** L109: "For A644 and A2319, we did not have weak lensing masses available from \citet{herbonnet2020} but used the average DM distribution (of the 23 other clusters in \citealt{loubser20}) to calculate the effect of a DM mass component on the best fitting stellar mass-to-light ratio".
- **A2319 is flagged as hydrostatically biased.** L435: "particularly striking in the case of A2319, for which HSE masses are known to be biased low". L502: "a single system that is known to be strongly biased \citep[A2319;][]{ghirardini18}". L512: "with the exception of a system known for its high level of nonthermal pressure support (A2319)". It is not excluded.
- **A2319 and A644 profile shape.** L410: "In the case of A2319 and A644, the mass profile was found to be better described by a Burkert profile, which leads to the curved shape of the DM profiles observed here."
- **A2255 and A644 are morphologically disturbed.** L514: "Some systems (e.g., A2255 and A644) show a larger amount of curvature ... These systems exhibit a somewhat disturbed X-ray morphology ... This effect is likely to be present in A2255, which exhibits a very flat central gas density profile and a substantial offset between the X-ray peak and the position of the BCG \citep[123 kpc,][]{rossetti16}." Neither is excluded in this paper; the exclusion of disturbed systems happens in Paper II.

## B. g_obs

**4. How the total mass profile is obtained**

All methods solve hydrostatic equilibrium. L129: $dP_{gas}/dr = -\rho_{gas} G M_{tot}(<r)/r^2$. L126: "We assume that the ICM is fully thermalized and that the gas pressure locally balances the gravitational force". L122: "parametric mass models (Sect. \ref{sec:massmod}), forward fitting with parametric functions (Sect. \ref{sec:forward}), and nonparametric log-normal mixture reconstruction (Sect. \ref{sec:GP})".

- **(a) Parametric mass models, NFW and Einasto (L170–190).** The HSE equation is integrated into a pressure profile (Eq. `eq:p0`, L173), with "the integration constant $P_0$ is left free while fitting. We set a Gaussian prior on $P_0$ with mean and standard deviation set to the outermost pressure value and its 1-sigma uncertainty" (L176). NFW is L180; Einasto is L186, with α free (L190).
- **(b) Baryons + DM decomposition, five systems only.** L209: $\rho_{tot}=\rho_{DM}+\rho_{gas}+\rho_{\star,BCG}+\rho_{\star,sat}$. L212: "the DM profile $\rho_{DM}$ is described by a mass model (NFW or Einasto) and the contribution of the baryonic components is provided as input."
- **(c) Parametric forward model (L217–224).** A gNFW pressure profile, "with $P_0$, $r_s$, $\alpha$, $\beta,$ and $\gamma$ as free parameters ... The pressure gradient can be computed analytically".
- **(d) Nonparametric log-normal mixture, "NP" (L229–253).** "we describe the 3D temperature profile as a linear combination of a large number $N_{g}$ of log-normal functions" (Eq. `eq:gp`, L232). The setup (L235): "We implement the model with $N_g=200$ and the values of $\mu_i$ logarithmically spaced from the innermost to the outermost data points. We set the values of $\sigma_i$ to the width of the nearest spectroscopic annulus or SZ radial bin". The mass follows from L240: $M(<r) = -\frac{rkT_{3D}}{G\mu m_p}(\partial\log T/\partial\log r + \partial\log n_{gas}/\partial\log r)$.
- **Gas density in all methods.** L142: "modeled using the nonparametric multi-scale approach implemented in \citet{eckert20}", as a sum of King functions (L145–156).
- **Sampler.** L259–261: NUTS/HMC in PyMC3, "four parallel HMC chains with 2,000 tuning steps and 2,000 samples each".

**5. Which method gives g_obs for the RAR**

- L453: $g_{obs}(r) = GM_{HSE}(<r)/r^2$.
- L458: "For the observed acceleration we consider both the nonparametric reconstruction and the results of the Einasto fit to the DM component only. As can be seen in Fig. \ref{fig:rar}, the two methods provide consistent results throughout the entire range."
- Figure caption, L445: "The solid colored curves show the result of the Einasto fit to the baryons+DM model, whereas the individual data points indicate the accelerations computed using the nonparametric log-normal mixture model (NP)."
- The relation is fitted to the NP points. L486: "We fitted the nonparametric points on the $g_{\rm obs}-g_{\rm bar}$ plane". See Doubts D1.

**6. Input data**

- X-ray: XMM-Newton EPIC surface brightness in the [0.7–1.2] keV band, using the azimuthal median (L72–74), plus spectroscopic temperatures in annuli (L76).
- SZ: Planck MILCA y-map, deprojected to a 3D pressure profile, with the covariance matrix propagated (L80–97).
- Joint fit, L165: "constructing a joint likelihood comparing the 3D model pressure to the SZ pressure and the spectroscopic-like temperature profile to the X-ray temperatures". The spectroscopic-like weighting follows Mazzotta (L161) and is PSF-convolved (L165).

**7. Spherical (3D) or not, and at which radii**

- **Spherical, 3D enclosed mass.** L133: "$M_{\rm tot}(<r)$ the total (Newtonian) mass enclosed within a radius $r$"; L97: "We assumed spherical symmetry". The models are 3D and projected for comparison with data. L140: "We adopt a forward modeling approach in which the model 3D quantities are projected along the line of sight and compared to the projected data."
- **NP radii.** NP is evaluated at the spectral-bin and SZ-bin radii. L277 (Fig. 1 caption): "NP results evaluated at the radius of the X-ray spectroscopic measurements (labeled ``NP Spectral bins," blue) and the SZ pressure data (``NP SZ bins," red)".

**8. Corrections in g_obs**

- **No non-thermal pressure correction is applied.** L126 says "fully thermalized", and the HSE equation (L129) contains gas pressure only.
- Non-thermal pressure is discussed only as a possible bias (L435, L502; see D, E4).
- **PSF correction is applied.** L190: "by correcting for the telescope's PSF".
- **Clumping is handled through the azimuthal median.** L74: "used the azimuthal median technique \citep{eckert15} to remove the contribution of unresolved gas clumps".

## C. g_bar

**9. Gas**

- L456: $g_{bar}(r)=G(M_{gas}(<r)+M_{\star,BCG}(<r)+M_{\star,sat}(<r))/r^2$.
- The gas density profile comes from the multiscale King-function deprojection of the X-ray emissivity (L142–156).
- **Not stated in this paper:** how emissivity is converted to n_e or ρ_gas (the value of μ, the n_e/n_H ratio, any abundance dependence), and how M_gas is integrated.

**10. Central galaxy (BCG)**

- **Method.** L105: "We used the multi-Gaussian expansion (MGE) method, as implemented by \citet{cappellari2002}, to obtain the stellar mass distributions from the $r$-band imaging".
- **Deprojection.** L107: "the deprojection from surface density to intrinsic density was performed for the axisymmetric case using the Jeans anisotropic method (\citealt{cappellari2008}) assuming a constant stellar mass-to-light ratio, $\Upsilon_{* \rm DYN}$. We assumed an inclination of $i$ = 90$\degr$".
- **Free parameters.** L107: there are "only two free parameters: (i) the stellar velocity anisotropy ($\beta_{z}$) and (ii) the stellar mass-to-light ratio ($\Upsilon_{* \rm DYN}$)", fitted to the stellar kinematics. "We use this best fitting stellar mass-to-light ratio to derive the enclosed stellar mass of the BCG within spheres of different radii."
- **Source of the M/L.** It is dynamical: fitted to the BCG kinematics in Loubser et al. 2020, not taken from stellar populations or an IMF. Loubser20 L139: "The stellar mass-to-light ratio from dynamics, $\Upsilon_{\star \rm DYN}$, is determined in the rest-frame $r$-band."
- **Values, from Loubser20 (Eckert22 does not quote them).**
  - ★+CEN+DM fits (Loubser20 Table, L522/525/528): Abell 1795 "3.34$\pm$0.09", Abell 2029 "6.59$\pm$0.11", Abell 2142 "5.90$\pm$0.14".
  - A644 and A2319 were not fitted with DM. Loubser20 L458: "for Abell 644 and 2319 we do not model the case with dark matter included". Their ★ / ★+CEN values (Loubser20 L930, L947) are "A644 & --0.07 & 6.81 & 6.11 & --0.08 & 6.71 & 5.82" and "A2319 & --0.11 & 6.28 & 7.62 & --0.38 & 6.23 & 6.52".
  - Eckert22 L109 says that for these two the effect of a DM component was taken from the average of the other clusters: "the best fitting $\Upsilon_{* \rm DYN}$ decrease by 8.3 $\pm$ 2.9 per cent on average". The final Υ values used for A644 and A2319 are not stated.
- **3D result, then Sérsic.** The result is a 3D enclosed mass within spheres (L107). It is then refitted with a 3D Sérsic density form. L404: "we fitted the BCG stellar mass using a S\'ersic functional form" (equation at L406).
- **Deprojection detail, Loubser20 L358:** "the MGE surface density can be deprojected analytically \citep{Monnet1992} ... Although this deprojection is non-unique".

**11. Satellites**

- **Method.** L114: ugri photometry; "The stellar mass-to-light ratios ... are obtained using spectral energy distribution fitting of these aperture fluxes. For this we assume the stellar population libraries from \citet{bruzual03}, an exponentially declining star-formation history, and a \citet{chabrier03} initial mass function."
- **Interlopers.** L116: removed by "statistical subtraction of sources observed in the COSMOS field", with cosmic variance estimated "using \citet{moster11}".
- **Profile treatment.** L408: "the cumulative stellar mass profiles of the satellite galaxies are quite noisy and not smooth ... we fitted the stellar mass profiles beyond the BCG ($R>100$ kpc) with a gNFW profile with shape parameters fixed to \citet{vdb15}, and used the resulting functional form as input for our mass reconstruction code."
- **Projected or deprojected: Eckert22 does not say** whether the fitted profiles are projected, or how they were deprojected. The method papers say:
  - Ghizzardi21 L715: "the cumulative stellar masses plotted in Fig. \ref{fig:mstarprof} are derived by integrating within a projected radius. To derive the stellar mass enclosed within a sphere of radius $R_{500}$, we perform a correction assuming a gNFW for the galaxy distribution (see vdB15), with a concentration parameter $c = 0.72$ and a slope $\alpha=1.64$. We find that 75$\%$ of the mass obtained integrating along the line of sight lies within the sphere with radius $R_{500}$."
  - vdB15 L338–340 gives the gNFW form $\rho=\rho_0/((r/R_s)^\alpha(1+r/R_s)^{3-\alpha})$, "We project the generalised NFW profile numerically along the line-of-sight."
  - vdB15 Table `tab:nfwpars` (L279), "All" row: stellar-mass density $c=0.64^{+0.49+0.73}_{-0.21-0.33}$, $\alpha=1.63^{+0.06+0.09}_{-0.25-0.17}$; number density for $M_\star>10^{10}$, $c=0.72^{+0.31+0.31}_{-0.19-0.28}$, $\alpha=1.64^{+0.06+0.08}_{-0.16-0.06}$.
- **BCG in the profile.** Ghizzardi21 L711: "the BCG is included in our mass computation, while the Intra-Cluster Light (hereafter ICL) is not." Eckert22 avoids it only by fitting at R>100 kpc (see Doubts).

**12. Intracluster light: not included.** L410: "Intracluster light, which is not included in our analysis ... the contribution of ICL to the total baryon budget is expected to be small \citep[$<5\%$; e.g.,][]{gonzalez07}." Also L402.

**13. Other baryons.** None are included. The equation at L456 has gas, BCG and satellites only. Cold gas, dust and a BCG black hole are not included in g_bar. The black hole appears only inside the BCG dynamical model (L107).

**14. Is g_bar a 3D enclosed-mass acceleration?** Yes, as written: L456 uses $M(<r)/r^2$ for each component, and the BCG masses are "within spheres of different radii" (L107). For the satellites, the 3D status rests on the gNFW 3D form; the deprojection step is not described in Eckert22.

## D. Uncertainties

Scale codes: **P** = point (varies with radius), **S** = system (one cluster), **D** = dataset (all clusters).

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | Provided by paper/data? |
|---|---|---|---|---|---|---|---|
| E1 | Statistical posterior on HSE mass | "run four parallel HMC chains ... combined to measure the posterior distributions" | L261 | Not stated numerically for the real data (shown as error bars in the figures) | P | g_obs | Error bars in the figures. Correlations between radii of the NP mass are not discussed. |
| E2 | SZ correlated noise | "The induced correlation between the points of the $y$-profile is accounted for and propagated through the covariance matrix of the profile." / "used to compute the covariance matrix of the 3D pressure profile" | L91, L97 | Not stated | P (correlated) | g_obs | Covariance is used in the fit. Its release is not stated. |
| E3 | NP method accuracy (mocks) | "The nonparametric technique follows the true profile with minimal bias (<5\%) but somewhat higher uncertainties"; T3D "scatter of $\sim5\%$" | L309, L307 | <5% bias; about 5% scatter (temperature) | P (larger at the edges: "uncertainties are higher at the inner and outer edges") | g_obs | Mock test only |
| E4 | Hydrostatic (non-thermal) bias | "predict to be in the range $5-30\%$ at $R_{500}$"; "X-COP hydrostatic masses are 10-15\% lower than weak lensing estimates"; "(7\% at $R_{500}$, 10\% at $R_{200}$)"; "our measurements are mildly biased ($<10\%$) out to $R_{500}$. The HSE assumption is likely to be a poorer approximation beyond this point." Also L311 "hydrostatic bias \citep[10-20\%..." and L435 "deviations from HSE are low, at the level of $6-10\%$, with the notable exception of A2319"; "At $R_{200}$ our baryon fractions exceed the cosmic value by 10-20\%"; abstract "($10-20\%$)" | L502, L311, L435, L38, L539 | 5–30% (simulations); 10–15% (vs WL); <10% within R500; 10–20% at R200 | P (grows with radius, L502), S (A2319 singled out), also stated as a sample-level number | g_obs (biased low) | Discussed only; no correction applied |
| E5 | Gas / temperature inhomogeneities | "temperature inhomogeneities \citep[$\sim10\%$,][]{rasia14}"; "we conclude that the impact of gas inhomogeneities is small ($<10\%$)" | L311, L504 | about 10%; <10% | Not stated (inner <10 kpc multi-temperature noted) | g_obs (via T, n); the paper notes densities would be "biased toward high" values, which would also touch g_bar, but it draws no g_bar conclusion | Discussed only |
| E6 | XMM effective-area calibration | "effective area calibration \citep[$15\%$,][]{schellenberger15}"; "reaches $\sim20\%$ for 10 keV plasma ... our masses at fixed radii would be underestimated by a similar amount"; "mostly affects the regions located inside $0.5 R_{500}$" | L311, L506 | 15%; up to about 20% at 10 keV | D (instrument), P (mostly <0.5 R500, temperature-dependent) | g_obs | Discussed only |
| E7 | Combined systematics | "we estimate that the systematic uncertainties associated with each of the effects discussed here amount to $10-20\%$" | L508 | 10–20% each | Not stated | g_obs | Discussed only |
| E8 | Overall mass accuracy (from baryon fraction) | "our mass profiles are accurate at the $\lesssim 20\%$ level throughout the range considered here" | L435 | ≲20% | Not stated | g_obs | Discussed only |
| E9 | Choice of method | "median masses in the range $[0.05-2]R_{500}$ being within 3\% of one another"; "the relative difference between NFW and NP points being less than 10\% at all radii"; "scatter is minimal in the radial range [0.2-1]$R_{500}$, where all the methods converge within less than 10\%"; "the scatter of the NFW values relative to the NP points is nearly twice as large" (outskirts); Forward has "excess mass" in the innermost region | L373 | 3% (medians); <10% | P (largest in the core and outskirts), S (individual shapes differ) | g_obs | Fig. 3/4 ratios; not tabulated per cluster |
| E10 | Parametric-model bias (mocks) | "NFW reconstruction ... bias of at most 3\%"; "Einasto exceeding the true mass by about 6\% on average" | L309, L311 | ≤3% (NFW); about 6% (Einasto) | P | g_obs | Mock test only |
| E11 | Prior / regularisation in NP | "For large values of $N_g$ the model is essentially independent of the choice of $N_g$ and $\mu_i$, whereas the standard deviations $\sigma_i$ act as effective smoothing scales." ($\sigma_i$ set to bin width) | L235 | Not quantified | P | g_obs | Not tested in the paper; the priors on $G_i$ are not stated |
| E12 | Priors on parametric fits | Table `tab:priors`: $R_{200}$ 2000±1000 kpc, $c_{200}$ 4±4, $P_0$ $P_m\pm dP_m$; "weakly informative ... whilst not biasing the resulting posteriors" | L190–203 | as in the table | S | g_obs (NFW/Einasto) | Stated; the impact is not quantified |
| E13 | Change vs E19 (PSF modelling etc.) | Table `tab:mass_ratio`: mean $M_{hydromass}/M_{E19}$ = 1.08, 1.01, 0.96, 0.93 at Δ = 2500, 1000, 500, 200; "the difference, however, is always within 10\%" | L344–356 | ≤10% | P (radius-dependent), sample average | g_obs | Table (sample mean/median only) |
| E14 | Miscentring | "it is possible that the X-ray peak does not trace exactly the bottom of the potential well ... offset ... (123 kpc)" for A2255 | L514 | 123 kpc offset (A2255) | S, inner P | g_obs (core shape) | Discussed only |
| E15 | BCG M/L uncertainty (weak-lensing DM mass, concentration) | "the observational errors on $M_{\rm DM}$ and $R_{200}$ ... are by far the dominant uncertainty. We derived the errors ... by incorporating the 1$\sigma$ errors on the weak lensing masses as well as a $\pm$ 10 per cent uncertainty on the calculated value for the concentration parameter. The uncertainties on the stellar mass profiles are therefore constant with radius." | L111 | ±10% on concentration plus 1σ WL errors; the resulting BCG-mass error is not stated | S ("constant with radius") | g_bar | The per-BCG error on Υ is in Loubser20 (e.g. 3.34±0.09) |
| E16 | BCG photometry / kinematics | "surface brightness measurement are accurate at the level of $< 0.25$ mag arcsec$^{-2}$, and our stellar kinematic measurement errors are $\pm4.7$ per cent on average"; dynamical modelling "robust against the DM distribution profile ... as well as against assumptions regarding the black hole" | L111 | <0.25 mag arcsec⁻²; ±4.7% | S | g_bar | Stated |
| E17 | BCG M/L, DM-inclusion shift (A644, A2319) | "the best fitting $\Upsilon_{* \rm DYN}$ decrease by 8.3 $\pm$ 2.9 per cent on average" | L109 | 8.3±2.9% | S (the two clusters); the correction is a sample average | g_bar | Stated |
| E18 | BCG JAM alignment (method paper) | "changing our cylindrically-aligned JAM models to spherically-aligned JAM models, results in the best-fitting $\Upsilon_{\star \rm DYN}$ parameters changing by up to $\sim$ 15 per cent" | Loubser20 L547 | up to about 15% | S | g_bar | Not discussed in Eckert22 |
| E19 | BCG MGE fit quality (method paper) | "average mean absolute deviation of 10.2 per cent" | Loubser20 L774 | 10.2% | S | g_bar | Not discussed in Eckert22 |
| E20 | Satellite photometric / cosmic variance | "We also accounted for field-to-field (often called “cosmic”) variance ... We estimate this uncertainty using \citet{moster11}" | L116 | Not stated in Eckert22 | S (field background) | g_bar | Ghizzardi21 L714 shows statistical and cosmic-variance terms separately (figure only) |
| E21 | Satellite IMF / SPS | "a \citet{chabrier03} initial mass function" | L114 | No IMF systematic stated in Eckert22. Ghizzardi21 L749: Salpeter gives values "that exceed by a factor $ \sim 2$"; L923: "we may be underestimating stellar masses by as much as 60\%" | D | g_bar | Not discussed in Eckert22 |
| E22 | Total stellar fraction errors | Table `tab:fbar`, e.g. A644 $f_{\star,500}$ "$1.3\pm0.5$"; A2029 $f_{\star,2500}$ "$2.8\pm0.9$" (percent) | L417–429 | about 30–40% relative on f_star | S per Δ | g_bar | Table (at R2500/R500/R200 only) |
| E23 | ICL omitted | "the contribution of ICL to the total baryon budget is expected to be small \citep[$<5\%$" | L410 | <5% | Not stated | g_bar (one-sided) | Discussed only |
| E24 | Sérsic / gNFW smoothing of stellar inputs | The BCG is refitted with a Sérsic profile (L404) and the satellites with a gNFW with shapes "fixed to \citet{vdb15}" (L408) | L404, L408 | Not stated | S | g_bar | Not quantified |
| E25 | Cosmology | "we assume a Planck 2015 $\Lambda$CDM cosmology ... $H_0=67.8$ km/s/Mpc and $\Omega_m=0.308$"; E19 comparison "converted into the same cosmology" | L56, L347 | n/a | D | both | Stated |
| E26 | Intrinsic scatter of cluster RAR (fit result, not an error term) | "intrinsic scatter $\sigma_{\ln g_{\rm obs}}=0.21\pm0.02$" | L486 | 0.21±0.02 (ln) | D | g_obs | Stated |

**Correlations:**
- Correlations between radii are discussed only for the SZ y-profile and pressure (E2).
- Parameter correlations (NFW M–c) are discussed at L263 and L381.
- No correlation matrix of g_obs or g_bar between radii is described as provided.
- Nothing is said about correlations between the NP "spectral-bin" points and "SZ-bin" points, or about the shared stellar terms (E15, E20–E24), which are system-wide by construction.

## E. The RAR as presented

**15. How g_obs is plotted against g_bar**
- There is no binning. Fig. `fig:rar` (L440–447) shows per-cluster NP data points and per-cluster Einasto curves, against McGaugh et al. 2016 with "the associated 0.06 dex scatter" and a one-to-one line.
- Accelerations are given in m s⁻² (L465).
- The Fig. 8 left panel (L474) adds "the best fit to the NP data with the model that describes two transitions ... and its corresponding $1\sigma$ error envelope. The dotted line shows the classical MOND relation."

**16. Fitted relation**
- Model, L480: $g_{obs} = g_{bar}(1+g_1/g_{bar})^{\alpha_1}(1+g_2/g_{bar})^{\alpha_2-\alpha_1}$.
- Fitted parameters, L486: "$g_{1} = 2.3_{-0.8}^{+1.2}\times 10^{-10}$ m s$^{-2}$ and $g_2 = 1.2_{-0.7}^{+0.9}\times 10^{-11}$ m s$^{-2}$ ... $\alpha_1=1.4_{-0.5}^{+0.7}$ and $\alpha_2=-1.2_{-0.7}^{+0.9}$".
- Comparison relation (McGaugh+16, Eq. `eq:mcgaugh`, L461–465), with "$g_{\dagger}=1.2\times10^{-10}$ m s$^{-2}$".
- Not stated: the fitting likelihood, the treatment of errors on g_bar, and how the clusters are weighted.

**17. Scatter and the comparison with galaxies**
- Scatter: L486, "intrinsic scatter $\sigma_{\ln g_{\rm obs}}=0.21\pm0.02$"; L522, "our clusters indeed define their own RAR with a scatter $\sigma_{\ln g}=0.21$".
- L465: "At high acceleration ($g>10^{-10}$ m s$^{-2}$), the baryonic acceleration induced by the stellar mass of the BCG dominates ... The observed acceleration is up to 5 times higher than expected".
- L467: "Around $g_{\rm bar}\sim2\times 10^{-11}$ m s$^{-2}$ we observe another change of regime ... Our systems eventually catch up with the \citet{mcgaugh16} RAR in the outermost regions, although the slope of the relation is widely different."
- L541: "the observed acceleration exceeding the expected value by a factor of $\sim5$ around $g_{\rm bar}=2\times10^{-11}$ m s$^{-2}$".
- The paper's interpretive claims about accounts (L467, L477, L488–493, L518–524) are recorded here as stated, without evaluation.

## F. Data availability

**18. What is released**
- L56: "The codes developed in the framework of this project are made publicly available. In particular, we release our mass reconstruction code in the form of an easy-to-use Python package named \texttt{hydromass}. Our \emph{XMM-Newton} mock data generator can be downloaded from GitHub."
- Footnote URLs: https://github.com/domeckert/hydromass (L122) and https://github.com/domeckert/xmm_simulator (L299).
- Earlier products: L70 footnote, https://dominiqueeckert.wixsite.com/xcop ("publicly available data products presented in \citet{ghirardini19}").
- **No licence or terms are stated** for the code or data.

**19. Released g_obs and g_bar tables:** the paper says nothing. It does not mention any released table, file, column, units for a table, error convention or confidence level. The only stated confidence levels are for figures and fits: "68\% interval" (L370), "$1\sigma$ contours" (L370) and "$1\sigma$ error envelope" (L474).

**20. The 12-cluster mass reconstructions**
- They were produced with all four methods (L342).
- Table 1 gives the NFW "TOT" results for all 12 (below).
- Per-cluster plots are in Appendix A (L558–723).
- No release of the reconstructed profiles is stated.

## G. Differences from Ettori et al. 2019 (E19) and the 2019 archive

- **PSF modelling.** L344: "the main difference with respect to our previous analysis is the implementation of a modeling scheme for the PSF ... Our new masses are slightly higher inside $R_{2500}$ and slightly lower inside $R_{200}$; the difference, however, is always within 10\% ... we conclude that the NFW concentrations given in E19 were slightly underestimated."
- **Einasto index.** L190: "in the Einasto case we leave the Einasto index $\alpha$ free, whereas previously its value was fixed to $1/\alpha\equiv\mu=5$".
- **Mass ratios, Table `tab:mass_ratio` (L347–357):**

| Overdensity | 2500 | 1000 | 500 | 200 |
|---|---|---|---|---|
| mean(M_hydromass/M_E19) | 1.08 | 1.01 | 0.96 | 0.93 |
| median(M_hydromass/M_E19) | 1.05 | 1.02 | 0.95 | 0.90 |

  The caption says: "For consistency, the masses estimated here were converted into the same cosmology as that used in E19."
- **New data.** A3266 and A2029 have new AO-17 data (L65, L70).
- **Gas density method.** L277 compares the multiscale method "to the L1 regularization results presented in \citet{ghirardini19} and publicly released by the X-COP team".
- **Cosmology.** Planck 2015, H0 = 67.8, Ωm = 0.308 (L56). E19's cosmology is not restated.
- **Redshifts.** No difference from 2019 is stated.
- **Table 1 (`tab:master`, L324–335).** Values are verbatim. The caption (L316) says: "The columns labeled ``DM'' refer to the NFW fits to the DM only for the five systems with complete information on the baryonic components ..., whereas the ``TOT'' subscripts refer to the fits of the total gravitational field with an NFW model ... In this case, the quoted total mass is computed from the sum of DM and baryonic density profiles."

| Cluster | z | N_H (10²⁰ cm⁻²) | R500,TOT (kpc) | M500,TOT (10¹⁴ M☉) | M200,TOT | c200,TOT | M200,DM | c200,DM |
|---|---|---|---|---|---|---|---|---|
| A85 | 0.0555 | 2.8 | 1214 −4/+4 | 5.03 −0.05/+0.05 | 7.04 −0.07/+0.08 | 4.708 −0.044/+0.042 | – | – |
| A644 | 0.0704 | 7.5 | 1398 −16/+16 | 7.80 −0.27/+0.26 | 10.97 −0.43/+0.45 | 4.597 −0.156/+0.163 | 10.98 −0.41/+0.45 | 4.458 −0.169/+0.171 |
| A1644 | 0.0473 | 4.1 | 1031 −10/+11 | 3.06 −0.09/+0.09 | 4.93 −0.20/+0.21 | 2.548 −0.135/+0.140 | – | – |
| A1795 | 0.0622 | 1.2 | 1160 −6/+6 | 4.42 −0.07/+0.07 | 6.04 −0.11/+0.11 | 5.454 −0.076/+0.072 | 6.82 −0.13/+0.13 | 4.510 −0.072/+0.074 |
| A2029 | 0.0766 | 3.2 | 1340 −9/+9 | 6.91 −0.14/+0.14 | 9.29 −0.21/+0.22 | 5.929 −0.101/+0.102 | 11.67 −0.28/+0.29 | 4.185 −0.091/+0.093 |
| A2142 | 0.09 | 3.8 | 1453 −9/+9 | 8.93 −0.16/+0.17 | 13.33 −0.30/+0.32 | 3.440 −0.070/+0.076 | 13.94 −0.31/+0.30 | 3.046 −0.074/+0.076 |
| A2255 | 0.0809 | 2.5 | 1202 −16/+17 | 5.01 −0.20/+0.22 | 8.94 −0.56/+0.66 | 1.800 −0.180/+0.193 | – | – |
| A2319 | 0.0557 | 3.2 | 1424 −4/+5 | 8.12 −0.08/+0.08 | 11.61 −0.14/+0.14 | 4.233 −0.070/+0.068 | 12.16 −0.14/+0.15 | 4.098 −0.079/+0.079 |
| A3158 | 0.059 | 1.4 | 1146 −11/+12 | 4.25 −0.13/+0.14 | 6.46 −0.25/+0.28 | 3.178 −0.146/+0.145 | – | – |
| A3266 | 0.0589 | 1.6 | 1381 −10/+10 | 7.43 −0.15/+0.16 | 12.22 −0.36/+0.41 | 2.352 −0.098/+0.097 | – | – |
| RXC1825 | 0.065 | 9.4 | 1109 −8/+9 | 3.88 −0.08/+0.09 | 5.66 −0.17/+0.18 | 3.807 −0.159/+0.165 | – | – |
| Zw1215 | 0.0766 | 1.7 | 1346 −21/+21 | 7.00 −0.32/+0.35 | 11.44 −0.70/+0.76 | 2.413 −0.148/+0.155 | – | – |

- **Baryon fractions, Table `tab:fbar` (L416–431).** Values are in percent, for the five complete systems at R2500, R500 and R200. For example, A1795: f_gas,500 "13.4±0.3", f_star,500 "1.3±0.5", f_bar,500 "14.7±0.7". The full table is at L424–428.

---

## Not stated (what I looked for, and where)

Searched across all of `hydromass.tex` (text, captions, tables and appendix), grepping for: release, available, github, CDS, zenodo, licen, confidence, 68%, correlat, covarian, gas mass, μ m_p.

- **Releases:**
  - Any release of g_obs or g_bar tables, columns, file names, units, error type or confidence level.
  - Any licence or terms for `hydromass` or the data.
  - Any release of the 12-cluster profiles.
- **Gas mass:**
  - Conversion from emissivity to n_e to ρ_gas (μ, n_e/n_H, abundances).
  - The gas-mass error budget.
- **g_obs inputs and correlations:**
  - Per-cluster radial limits in numbers.
  - The prior on the NP coefficients G_i.
  - Covariance or correlation of the NP g_obs between radii, or between the spectral-bin and SZ-bin points.
- **RAR fit:**
  - The fit likelihood, and whether the g_bar uncertainty enters the fit or the error bars.
  - Which clusters or points enter the RAR fit beyond "the NP points" (by implication the five).
- **Stellar mass:**
  - The final Υ values used for each BCG; Eckert22 gives none (I took them from Loubser20).
  - Which vdB15 gNFW parameter set was used ("shape parameters fixed to \citet{vdb15}", L408).
  - Whether the satellite profiles fitted are projected, and how they were deprojected.
  - An IMF or stellar-population systematic for either stellar component.
- **Earlier data and cross-checks:**
  - Changes in redshift or R500 relative to the 2019 archive, beyond the mass-ratio table.
  - Lensing as a separate channel. The paper uses weak lensing only as a comparison for the hydrostatic bias (L502) and as an input to the BCG dark-matter term (L107).

## Doubts (ambiguities, my inferences, and internal disagreements)

**Within the paper, and between the paper and its method sources**

1. **Which Einasto fit gives g_obs.** L458 says the Einasto fit "to the DM component only". The Fig. `fig:rar` caption (L445) says "Einasto fit to the baryons+DM model". My inference: the plotted g_obs curve is total (DM + baryons) from the decomposition fit, but the text wording differs.
2. **Where the baryon fraction reaches the cosmic value.**
   - The abstract (L38) says it "reaches the cosmic value at $R_{200}$ and slightly exceeds it beyond this point".
   - L435 says "Inside $R_{500}$ our estimated baryon fraction is equal to the cosmic value, and even slightly exceeds it beyond this point".
   - L539 says the systems "reach the cosmic baryon fraction at the virial radius".
3. **Baryon depletion range.** L435 gives "$0.2-0.5 R_{500}$"; L539 gives "$[0.1-0.5]R_{500}$".
4. **Hydrostatic bias from Eckert et al. 2019.** L435 quotes "$6-10\%$"; L502 quotes "7\% at $R_{500}$, 10\% at $R_{200}$". Within the paper's own conclusions, L502 gives "<10% out to R500", while L435 and L539 give 10–20% at R200.
5. **Location of the factor-5 excess.** L465 places it in the regime below $10^{-10}$ ("up to 5 times higher"); L541 places it "around $g_{\rm bar}=2\times10^{-11}$".
6. **Table 1 caption.** "TOT ... fits of the total gravitational field with an NFW model" is followed by "the quoted total mass is computed from the sum of DM and baryonic density profiles". It is unclear whether, for the five complete systems, M500,TOT and R500,TOT come from the total-NFW fit or from the DM + baryons fit.
7. **Caption of `tab:mass_ratio`.** It says "Ratio between the masses published in E19 ($M_{\rm E19}$) and our new results", but the rows are $M_{hydromass}/M_{E19}$. The text (L344) agrees with hydromass/E19.
8. **Possible BCG double counting (my inference).** Ghizzardi21 L711 says the satellite cumulative profiles include the BCG. Eckert22 fits the satellites only at R>100 kpc with a fixed-shape gNFW. Whether the BCG light is removed from the satellite normalisation is not stated. vdB15 (L216) subtracted BCGs with GALFIT for its own profiles.
9. **Which "gNFW" applies to the satellites.** Eckert22 L408 refers to "a generalized NFW profile (see Eq. \ref{eq:gnfw})", which is the five-parameter pressure form (L220). vdB15 uses the two-parameter form at its L338. Which vdB15 parameters were adopted is not stated: the stellar-mass-density fit (c=0.64, α=1.63) or the number-density fit used by Ghizzardi21 (c=0.72, α=1.64).
10. **Mixed stellar-mass bases.** The BCG mass uses a dynamical, r-band Υ (no IMF assumption); the satellites use SED fitting with a Chabrier IMF (L114). The paper does not discuss this difference.
11. **Why five clusters.** Ghizzardi21 Table (L549–561) has satellite stellar masses for 7 X-COP clusters (A1795, A85, A644, A2319, ZW1215, A2029, A2142). Eckert22 uses the 5 that also have Loubser20 BCG models. That last step is my inference; Eckert22 gives no reason why A85 and Zw1215 are absent.
12. **Small inconsistency in vdB15.** Its text (L342) gives α = 1.64^{+0.04+0.08}_{-0.16-0.06}, while its table (L279) gives 1.64^{+0.06+0.08}_{-0.16-0.06}.
13. **Version risk.** I read arXiv v1, labelled "Accepted for publication in A&A". The A&A version of record (662, A123) may differ, and I did not consult it.
14. **Typographical artefact.** L44, `\section{Introduction}a`, contains a stray "a". It does not affect content.

**Scale assignments (my judgement)**

15. "Point / system / dataset" in table D is my reading, except where the paper says it: E15 is "constant with radius", and E4 is "expected to increase with distance". The E22 relative sizes (about 30–40%) are my arithmetic on the table values, not a stated number.

**Brief, memory and next step**

16. **The brief's candidate id is wrong.** Reader A may have used 2205.01123 (Paper II, A&A 666, A41). If so, our reports will differ at the root.
17. **Memory used.** I drew nothing from the user's memory store beyond the standing project rules. There is nothing new to save.
18. **Next step.** The comparing party checks that Reader A used 2205.01110v1 (e-print SHA-256 18fc2e80…c7d8), then settles items 1, 6 and 9 above at source. Item 9 decides which satellite profile shape enters g_bar.