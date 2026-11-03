# Reader A report: Eckert et al. 2022 (A&A 662, A123), X-COP v2, Atlas step A (D-089)

**Reader:** Reader A
**Date:** 2026-11-03
**Working directory:** `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/e22_readerA`

**The brief's candidate arXiv id is wrong.**
- 2205.01123 is Eckert, Ettori, Robertson, Massey, Pointecouteau, Harvey & McCarthy, "Constraints on dark matter self-interaction from the internal density profiles of X-COP galaxy clusters", journal reference A&A 666, A41 (2022). That is "Paper II".
- The paper we want is **2205.01110**. I confirmed it on `https://arxiv.org/abs/2205.01110`:
  - title "The gravitational field of X-COP galaxy clusters";
  - authors D. Eckert, S. Ettori, E. Pointecouteau, R. F. J. van der Burg, S. I. Loubser;
  - DOI 10.1051/0004-6361/202142507, journal reference "A&A 662, A123 (2022)";
  - only v1 exists (2 May 2022).

I did not open the shared data files, any data from the paper, the hydromass GitHub repository, or drive.switch.ch. The arXiv listing and search pages were read only to identify papers.

### Sources read

| Role | arXiv id and version | Main .tex | SHA-256 of e-print |
|---|---|---|---|
| Target paper (Eckert+22) | 2205.01110v1 | `hydromass.tex` (727 lines) | `18fc2e8025f56c716a864e5ef9436cccb5f0be05cff7a0f004aedd4605e5c7d8` |
| BCG method (Loubser+20, MNRAS 496, 1857; DOI 10.1093/mnras/staa1682 per the arXiv comments) | 2006.05706v1 (only version) | `BCG_v3_withoutBold.tex` | `ded65c6d1457b3183ee21b573bf426bf5ddfd20575fc39f429eb0e887dd9044c` |
| Satellite method (van der Burg+15, A&A 577, A19) | 1412.2137v2 (latest) | `paper_publisher.tex` | `17fd10bfdf5ab6ec9f374385f73663a15677b31eefeec97440da6a3614d5ea5d` |
| Satellite profiles for X-COP (Ghizzardi+21, A&A 646, A92) | 2007.01084v1 (only version) | `xcop-metallicity.tex` | `88c8e91c036077e2ca660cd029943d576df1462daae914d3e58aa24169c5a9e8` |

- Unless prefixed, line numbers refer to `hydromass.tex` in 2205.01110v1. Other files are written as `Loubser:Lnnn`, `vdB15:Lnnn` and `Ghizzardi:Lnnn`.
- Section numbers are inferred from the order of `\section` commands.
- I read the arXiv v1 text only. The A&A version of record was not reachable (only arXiv and GitHub are allowed) and may differ.

---

## A. Sample

**A1. Clusters analysed, and which have the complete baryon budget**

The 12 clusters are listed in Table 1 (`tab:master`, L324–335): A85, A644, A1644, A1795, A2029, A2142, A2255, A2319, A3158, A3266, RXC1825 and Zw1215.

- L54 (§1): "We apply our technique to the 12 X-COP systems with the aim of comparing NFW and Einasto profiles. For a subset of systems, we use measurements of the gas mass as well as the stellar mass within the brightest cluster galaxy (BCG) and satellite galaxies to break down the gravitational field into its baryonic and DM components."
- **The complete baryon budget covers five clusters: A644, A1795, A2029, A2142 and A2319.**
  - L103 (§2.4.1): "For the BCGs of A644, A1795, A2029, A2142, and A2319, we used stellar mass distributions from \citet{loubser20}."
  - L114 (§2.4.2): "The stellar mass content contained in the satellite population of the same five clusters (A644, A1795, A2029, A2142, and A2319), is probed using $g$- and $r$-band imaging data obtained with MegaCam at the CFHT".
  - L402 (§5.3): "for a subset of systems (A644, A1795, A2029, A2142, and A2319) we have access to precise measurements of the stellar mass profiles of the cluster's BCG \citep{loubser20} and of the cumulative stellar mass of satellite galaxies \citep{vdb15}. Therefore, with the exception of a potential contribution of intracluster light (ICL) we have direct measurements of the mass profiles of all the baryonic components (gas, BCG, and satellites)."
  - L541 (§7): "We studied in detail the relation between observed and baryonic acceleration (RAR) in the five systems for which the baryonic content can be completely characterized".

**A2. Radial range**

- Sample-wide range, L528 (§7): "we have performed a detailed analysis of the gravitational field of X-COP galaxy clusters over the radial range $[0.01-2]R_{500}$". L512 (§6.2) repeats it: "over the entire radial range of interest ($[0.01-2]R_{500}$".
- Abstract, L38: "over two decades in radius".
- The nonparametric (NP) profile is evaluated only at the data radii.
  - L263 (§3.5): "it cannot be extrapolated outside of the fitted range. Thus, for the remainder of the paper we evaluate it at the radii of the observed data and present them in the form of data points rather than continuous models."
  - L342 (§5.1): "we restrict specifically to the radii corresponding to the existing spectral and SZ data points to avoid extrapolating."
- BCG, L404 (§5.3): "the stellar mass profile of the BCG can be estimated only within a limited radial range out to $\sim50$ kpc".
- Satellites, L408: "we fitted the stellar mass profiles beyond the BCG ($R>100$ kpc) with a gNFW profile".
- **Per-cluster inner and outer radii are not given numerically anywhere in the text.** They appear only graphically, in Fig. 1 and Appendix A Figs. A.1–A.11 (L558–722).

**A3. Clusters excluded or treated differently**

- A3266 and A2029 have new data.
  - L65: "we add a set of 6 additional \emph{XMM-Newton} pointings that were obtained during AO-17 (observation ID 082365, PI: Eckert) on two clusters (A3266 and A2029) to homogenize the data set."
  - L70: "With the exception of the two systems with new observations (A3266 and A2029), we employ the publicly available data products presented in \citet{ghirardini19}".
- A644 and A2319 had no weak-lensing mass for the BCG modelling. L109: "For A644 and A2319, we did not have weak lensing masses available from \citet{herbonnet2020} but used the average DM distribution (of the 23 other clusters in \citealt{loubser20}) to calculate the effect of a DM mass component on the best fitting stellar mass-to-light ratio".
- A2319 is treated as hydrostatically biased.
  - L435: "This effect is particularly striking in the case of A2319, for which HSE masses are known to be biased low".
  - L502: "with the exception of a single system that is known to be strongly biased \citep[A2319;][]{ghirardini18}".
  - It is not excluded from the RAR.
- A2319 and A644 used a Burkert-like DM shape. L410: "In the case of A2319 and A644, the mass profile was found to be better described by a Burkert profile, which leads to the curved shape of the DM profiles observed here."
- A2255 and A644 show curvature and possible miscentering. L514: "Some systems (e.g., A2255 and A644) show a larger amount of curvature in their mass profiles ... it is possible that the X-ray peak does not trace exactly the bottom of the potential well. This effect is likely to be present in A2255, which exhibits ... a substantial offset between the X-ray peak and the position of the BCG \citep[123 kpc,][]{rossetti16}."
- **No cluster is excluded from the 12-cluster mass analysis.** The 7 clusters without stellar data are left out of g_bar and the RAR (L518: "in a subset of five systems").

---

## B. g_obs

**B4. How the total mass profile is obtained**

All methods share hydrostatic equilibrium and a joint X-ray/SZ forward fit.
- L129 (§3.1), Eq. hse: `\frac{dP_{\rm gas}}{dr} = -\rho_{\rm gas}\frac{GM_{\rm tot}(<r)}{r^2}`.
- L140: "We use three complementary approaches to model the radial temperature and pressure profiles and reconstruct $M_{HSE}$ ... We adopt a forward modeling approach in which the model 3D quantities are projected along the line of sight and compared to the projected data."
- Gas density, L142: "The gas density profile is modeled using the nonparametric multi-scale approach implemented in \citet{eckert20}", a sum of King profiles (L145–156).

The methods:
1. **Parametric mass models, NFW and Einasto** (§3.2, L170–190). This is a "backward" integration of HSE (Eq. p0, L173): "This method is based on the ``backward'' approach introduced by \citet{ettori10}, with the notable difference that the integration constant $P_0$ is left free while fitting." (L176). Einasto α is free (L190).
2. **Baryons + DM decomposition** (L207–212): "we attempt to model the gravitational field as the sum of baryonic and DM profiles ... the DM profile $\rho_{DM}$ is described by a mass model (NFW or Einasto) and the contribution of the baryonic components is provided as input." L402: "the cumulative mass of the baryonic components is added as a fixed component to the mass profile at every radii."
3. **Parametric forward model** (§3.3, L217–224). The pressure is a gNFW function (Eq. gnfw), "The pressure gradient can be computed analytically from the reconstructed functional form to recover the mass profile from Eq. \ref{eq:hse}."
4. **Nonparametric log-normal mixture (NP)** (§3.4, L229–253).
   - L229: "we describe the 3D temperature profile as a linear combination of a large number $N_{g}$ of log-normal functions".
   - L235: "We implement the model with $N_g=200$ and the values of $\mu_i$ logarithmically spaced from the innermost to the outermost data points. We set the values of $\sigma_i$ to the width of the nearest spectroscopic annulus or SZ radial bin".
   - Mass, L240: `M(<r) = -\frac{rkT_{3D}(r)}{G\mu m_p}\left(\frac{\partial \log T_{3D}}{\partial \log r} + \frac{\partial\log n_{\rm gas}}{\partial\log r}\right)`.
- Sampling, L259–261: NUTS in PyMC3, "four parallel HMC chains with 2,000 tuning steps and 2,000 samples each."

**B5. Which method gives the RAR g_obs**

- L458 (§5.5): "For the observed acceleration we consider both the nonparametric reconstruction and the results of the Einasto fit to the DM component only. As can be seen in Fig. \ref{fig:rar}, the two methods provide consistent results throughout the entire range."
- Fig. 9 caption, L445: "The solid colored curves show the result of the Einasto fit to the baryons+DM model, whereas the individual data points indicate the accelerations computed using the nonparametric log-normal mixture model (NP)."
- The fitted RAR model uses NP only. L486: "We fitted the nonparametric points on the $g_{\rm obs}-g_{\rm bar}$ plane".
- L366: "the results obtained with the NP method are used as a benchmark of the local gravitational field because the method is fully data driven."

**B6. Input data**

- X-ray surface brightness, L72: "We extracted count images from the clean event files in the [0.7-1.2] keV band"; azimuthal median (L74).
- X-ray spectroscopic temperature, L76: annular spectra fitted with APEC.
- Projection of the model temperature (Mazzotta weighting), Eq. mazzotta, L161.
- SZ, L80–97: *Planck* MILCA y-map, "Our SZ map has a spatial resolution of 7~arcmin" (L81). The 3D pressure profile comes from PSF deconvolution and deprojection (L97).
- Joint likelihood, L165: "constructing a joint likelihood comparing the 3D model pressure to the SZ pressure and the spectroscopic-like temperature profile to the X-ray temperatures \citep[see Eq. 2 of ][]{ettori19}."

**B7. Spherical (3D) masses, and at which radii**

- They are 3D enclosed masses: $M_{\rm tot}(<r)$, "the total (Newtonian) mass enclosed within a radius $r$" (L133).
- Spherical symmetry is stated for the SZ deprojection, L97: "We assumed spherical symmetry and applied a deconvolution from the Gaussian \emph{Planck} point spread function (PSF) and a geometrical deprojection".
- NP radii, Fig. 1 caption L277: "The data points show the NP results evaluated at the radius of the X-ray spectroscopic measurements (labeled ``NP Spectral bins," blue) and the SZ pressure data (``NP SZ bins," red)." Fig. 3 caption L362 says the same: "at the radii of the X-ray spectral data (circles) and the SZ pressure data (asterisks)".

**B8. Corrections in g_obs**

- No non-thermal pressure correction is applied.
  - L126: "We assume that the ICM is fully thermalized and that the gas pressure locally balances the gravitational force".
  - L453: `g_{\rm obs}(r) = \frac{GM_{\rm HSE}(<r)}{r^2}`.
- Hydrostatic bias is discussed but not applied (see D, E2).
- Corrections that are applied in processing:
  - PSF correction, L190: "by correcting for the telescope's PSF";
  - clump removal by azimuthal median, L74: "used the azimuthal median technique \citep{eckert15} to remove the contribution of unresolved gas clumps".

---

## C. g_bar

**Defining equation**, L456 (§5.5): `g_{\rm bar}(r)=\frac{G(M_{\rm gas}(<r) + M_{\rm \star,BCG}(<r)+M_{\rm \star,sat}(<r))}{r^2}.` L449 describes it as "the acceleration that would be expected in the absence of DM from the sum of the detected baryonic components".

**C9. Gas**

- From the multi-scale King-function fit to the X-ray emissivity (L142–156). L156: "The 3D model is projected onto the line of sight and convolved with the instrumental PSF to create a model for the observed surface brightness. The coefficients $\alpha_k$ are then fitted to the data."
- **Not stated:** the conversion from emissivity to n_e to ρ_gas (cooling function, n_e/n_H, μ), and the explicit gas-mass integral.

**C10. BCG**

- Method, L105: "We used the multi-Gaussian expansion (MGE) method, as implemented by \citet{cappellari2002}, to obtain the stellar mass distributions from the $r$-band imaging."
- Deprojection and dynamics, L107: "the deprojection from surface density to intrinsic density was performed for the axisymmetric case using the Jeans anisotropic method (\citealt{cappellari2008}) assuming a constant stellar mass-to-light ratio, $\Upsilon_{* \rm DYN}$. We assumed an inclination of $i$ = 90$\degr$ ... the BCG mass models include a central mass component for a supermassive black hole, and a DM halo that follows a spherically symmetric NFW profile ... resulting in only two free parameters: (i) the stellar velocity anisotropy ($\beta_{z}$) and (ii) the stellar mass-to-light ratio ($\Upsilon_{* \rm DYN}$) ... We use this best fitting stellar mass-to-light ratio to derive the enclosed stellar mass of the BCG within spheres of different radii."
- **M/L source:** a dynamical fit from Loubser+20. No IMF is assumed.
  - Loubser:L139: "The stellar mass-to-light ratio from dynamics, $\Upsilon_{\star \rm DYN}$, is determined in the rest-frame $r$-band."
  - Loubser Table `DynModsTable` (★+CEN+DM fit) gives Υ★DYN:
    - Abell 1795: 3.34±0.09 (L522);
    - Abell 2029: 6.59±0.11 (L525);
    - Abell 2142: 5.90±0.14 (L528).
  - A644 and A2319 appear only in the ★ and ★+CEN fits (Loubser:L930 and L947): A644 Υ = 6.81 (★) and 6.71 (★+CEN); A2319 Υ = 6.28 and 6.23.
  - Loubser:L458: "for Abell 644 and 2319 we do not model the case with dark matter included ($\star$ + CEN + DM) since no weak lensing masses are available".
  - Eckert+22 does not state the Υ values used for A644 and A2319.
- **3D or not:** the profile is 3D, enclosed within spheres (L107). It is then fitted with a Sérsic-type 3D density (L404–406): "we fitted the BCG stellar mass using a S\'ersic functional form ... $\rho_{BCG}(r) = \rho_0 \exp\{ -b_n ((r/r_e)^{1/n}-1 )\}$."

**C11. Satellites**

- Photometry and M/L, L114: "The stellar mass-to-light ratios that form the basis of the stellar mass measurements are obtained using spectral energy distribution fitting of these aperture fluxes. For this we assume the stellar population libraries from \citet{bruzual03}, an exponentially declining star-formation history, and a \citet{chabrier03} initial mass function."
- Interloper removal, L116: "we clean the galaxy distribution from interlopers ... by performing a statistical subtraction of sources observed in the COSMOS field \citep{muzzin13}."
- Model used, L408: "we fitted the stellar mass profiles beyond the BCG ($R>100$ kpc) with a gNFW profile with shape parameters fixed to \citet{vdb15}, and used the resulting functional form as input".
- **Projected or deprojected:** Eckert+22 does not say. The method paper for X-COP says the profiles are projected. Ghizzardi:L715 (§"Stellar mass profiles"): "the cumulative stellar masses plotted in Fig. \ref{fig:mstarprof} are derived by integrating within a projected radius. To derive the stellar mass enclosed within a sphere of radius $R_{500}$, we perform a correction assuming a gNFW for the galaxy distribution (see vdB15), with a concentration parameter $c = 0.72$ and a slope $\alpha=1.64$. We find that 75$\%$ of the mass obtained integrating along the line of sight lies within the sphere with radius $R_{500}$. We therefore multiply the stellar mass estimates by a factor 0.75."
- vdB15:L340: "We project the generalised NFW profile numerically along the line-of-sight." vdB15:L344 gives the stellar-mass gNFW fit: "$\alpha=1.63^{+0.05+0.09}_{-0.25-0.17}$ and $c=0.64^{+0.49+0.73}_{-0.21-0.33}$". The number-density values for massive galaxies at vdB15:L342 are α=1.64 and c=0.72.
- Ghizzardi:L711: "We point out that the BCG is included in our mass computation, while the Intra-Cluster Light (hereafter ICL) is not."
- Ghizzardi:L700: "we centre clusters on the X-ray centroids, as opposed to the BCGs in vdB15."

**C12. Intracluster light: not included**

- L402: "with the exception of a potential contribution of intracluster light (ICL)".
- L410: "Intracluster light, which is not included in our analysis ... the contribution of ICL to the total baryon budget is expected to be small \citep[$<5\%$; e.g.,][]{gonzalez07}."

**C13. Other baryons**

- None are included in g_bar (see L456).
- The BCG dynamical model contains a black-hole component (L107), but that component is not part of the $M_{\star,BCG}$ in g_bar as written.
- **Not stated:** cold gas, dust, or the black-hole mass in g_bar.

**C14. Is g_bar a 3D enclosed-mass acceleration?**

- As defined, yes. L456 uses $M(<r)/r^2$ for every component, and L402 says "cumulative mass of the baryonic components".
- Gas: 3D (deprojected model).
- BCG: 3D spheres (L107).
- Satellites: the paper does not say that its satellite input is the 3D enclosed mass. See C11 and Doubts D2–D4.

---

## D. Uncertainties

Scales: **point** (varies with radius), **system** (one cluster), **dataset** (all clusters).

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | Provided by paper/data? |
|---|---|---|---|---|---|---|---|
| E1 | Statistical posterior on HSE mass (NP and models) | "The nonparametric technique follows the true profile with minimal bias (<5\%) but somewhat higher uncertainties given the freedom allowed to the model. The uncertainties are higher at the inner and outer edges of the profile, since the temperature gradient cannot be directly constrained there." | §4.3 L309 | Per-radius errors shown only in figures; no number in text | point | g_obs | Posterior errors shown graphically (Figs. 3, 9). Release of per-radius errors: not stated. Correlations between radii: not stated. |
| E2 | SZ noise covariance | "The induced correlation between the points of the $y$-profile is accounted for and propagated through the covariance matrix of the profile." / "used to compute the covariance matrix of the 3D pressure profile." | §2.3 L91, L97 | Not given | point (correlated) | g_obs (through pressure) | Used in the fit (L165). Not stated as released. |
| E3 | Hydrostatic bias, simulations | "mass estimates derived under the hydrostatic assumption are known to be biased toward low values, an effect that various numerical simulations predict to be in the range $5-30\%$ at $R_{500}$" | §6.1 L502 | 5–30% at R500 | system or dataset, radius-dependent | g_obs (low) | Discussed, not corrected (L453) |
| E4 | Hydrostatic bias, vs weak lensing | "we found that X-COP hydrostatic masses are 10-15\% lower than weak lensing estimates \citep{herbonnet2020}." | §6.1 L502 | 10–15% | dataset | g_obs | Not applied |
| E5 | Hydrostatic bias, from gas fraction | "which was found to be low (7\% at $R_{500}$, 10\% at $R_{200}$)." / "we conclude that our measurements are mildly biased ($<10\%$) out to $R_{500}$. The HSE assumption is likely to be a poorer approximation beyond this point." | §6.1 L502 | 7% (R500), 10% (R200); <10% to R500 | dataset, radius-dependent | g_obs | Not applied |
| E6 | Non-thermal pressure at R200 (from baryon fraction) | "At $R_{200}$ our baryon fractions exceed the cosmic value by 10-20\%, potentially indicating a stronger impact of nonthermal pressure beyond $R_{500}$." Also L539 "mild contribution of nonthermal pressure ($10-20\%$) at $R_{200}$"; L435 "deviations from HSE are low, at the level of $6-10\%$, with the notable exception of A2319" (eckert19) | §5.4 L435; §7 L539 | 10–20% at R200; 6–10% (earlier work) | dataset, radius-dependent | g_obs | Not applied |
| E7 | A2319 strong hydrostatic bias | "with the exception of a single system that is known to be strongly biased \citep[A2319;][]{ghirardini18}" | §6.1 L502 | Not quantified here | system | g_obs | Flag in text only |
| E8 | Gas inhomogeneities / temperature structure | "we conclude that the impact of gas inhomogeneities is small ($<10\%$)" / "temperature inhomogeneities \citep[$\sim10\%$,][]{rasia14}" | §6.1 L504; §4.3 L311 | <10%; ~10% | dataset (point-dependent, notably <10 kpc) | g_obs; density bias would also move g_bar (gas) (inference from "both for the gas density ... and the temperature profiles", L504) | Not applied |
| E9 | XMM effective-area calibration | "effective area calibration \citep[$15\%$,][]{schellenberger15}" / "reaches $\sim20\%$ for 10 keV plasma ... our masses at fixed radii would be underestimated by a similar amount ... mostly affects the regions located inside $0.5 R_{500}$" | §4.3 L311; §6.1 L506 | 15%; ~20% at 10 keV; mainly <0.5 R500 | dataset, radius-dependent | g_obs | Not applied |
| E10 | Combined systematics | "we estimate that the systematic uncertainties associated with each of the effects discussed here amount to $10-20\%$" | §6.1 L508 | 10–20% each | dataset | g_obs | Not applied |
| E11 | Mass profile accuracy overall | "our mass profiles are accurate at the $\lesssim 20\%$ level throughout the range considered here" | §5.4 L435 | ≲20% | dataset | g_obs | Statement only |
| E12 | Reconstruction bias (mock validation) | "with a bias of at most 3\% when adopting the NFW method" / "Einasto exceeding the true mass by about 6\% on average" / NP "minimal bias (<5\%)" | §4.3 L309, L311 | NFW ≤3%; Einasto ~+6%; NP <5% | dataset | g_obs | Statement only |
| E13 | Choice of method | "the median masses in the range $[0.05-2]R_{500}$ being within 3\% of one another" / "the relative difference between NFW and NP points being less than 10\% at all radii" / "scatter is minimal in the radial range [0.2-1]$R_{500}$, where all the methods converge within less than 10\%" / "differences arise primarily in the innermost 100 kpc" | §5.1 L373; §3.5 L263 | 3% (median); <10% | point, system | g_obs | Fig. 4 (median ratio, 68% interval) |
| E14 | NP smoothing / regularisation | "the standard deviations $\sigma_i$ act as effective smoothing scales ... such that fluctuations on scales smaller than the bin size are suppressed" | §3.4 L235 | Not quantified | point | g_obs | Settings stated (N_g=200, σ_i = bin width). Priors on G_i: **not stated** |
| E15 | Priors (parametric) | Table 2: "$R_{200}$ [kpc] & 2000 & 1000 & 300 & 4000", "$c_{200}$ & 4 & 4 & 0 & 15", "$P_0$ & $P_{m}$ & $dP_{m}$ ..."; "We set a Gaussian prior on $P_0$ with mean and standard deviation set to the outermost pressure value and its 1-sigma uncertainty." | §3.2 L176, L199–201 | Prior widths as in table | system | g_obs (NFW/Einasto; P0 also in NP? not stated) | Stated; Einasto priors deferred to Paper II (L190) |
| E16 | Previous-analysis (E19) difference, PSF | Table 3: mean ratio "1.08 & 1.01 & 0.96 & 0.93"; "the difference, however, is always within 10\%" | §5.1 L344, L353–354 | <10% | dataset, radius-dependent | g_obs | Table 3 |
| E17 | Miscentering | "a substantial offset between the X-ray peak and the position of the BCG \citep[123 kpc,][]{rossetti16}. The apparent flat mass distribution in the core of this system may thus be explained by miscentering." | §6.2 L514 | Not quantified (A2255) | system | g_obs (core) | Not applied; A2255 is not in the RAR subset |
| E18 | BCG M/L (Υ★DYN): photometric and kinematic errors, WL-mass dominance | "Our surface brightness measurement are accurate at the level of $< 0.25$ mag arcsec$^{-2}$, and our stellar kinematic measurement errors are $\pm4.7$ per cent on average ... the observational errors on $M_{\rm DM}$ and $R_{200}$ ... are by far the dominant uncertainty. We derived the errors on the best fitting parameters by incorporating the 1$\sigma$ errors on the weak lensing masses as well as a $\pm$ 10 per cent uncertainty on the calculated value for the concentration parameter. The uncertainties on the stellar mass profiles are therefore constant with radius." | §2.4.1 L111 | <0.25 mag arcsec⁻²; ±4.7%; ±10% on c. Loubser per-cluster Υ errors ±0.09–0.14 (Loubser:L522/525/528) | system (constant with radius) | g_bar | Values in Loubser+20, not in Eckert+22 |
| E19 | BCG DM-halo treatment (A644, A2319) | "When a DM mass component is included in the dynamical mass models for the BCGs, the best fitting $\Upsilon_{* \rm DYN}$ decrease by 8.3 $\pm$ 2.9 per cent on average." | §2.4.1 L109 | 8.3±2.9% | system | g_bar | Stated |
| E20 | BCG JAM geometry (method paper only) | "changing our cylindrically-aligned JAM models to spherically-aligned JAM models, results in the best-fitting $\Upsilon_{\star \rm DYN}$ parameters changing by up to $\sim$ 15 per cent" | Loubser:L547 | up to ~15% | system | g_bar | Not discussed in Eckert+22 |
| E21 | BCG extrapolation beyond ~50 kpc (Sérsic fit) | "the stellar mass profile of the BCG can be estimated only within a limited radial range out to $\sim50$ kpc, we fitted the BCG stellar mass using a S\'ersic functional form" | §5.3 L404 | Not quantified | system / point | g_bar | Not quantified |
| E22 | Satellite cosmic (field-to-field) variance | "We also accounted for field-to-field (often called “cosmic”) variance ... We estimate this uncertainty using \citet{moster11}" | §2.4.2 L116; Ghizzardi:L714 | Not given in Eckert+22 | system | g_bar | Shown separately in Ghizzardi Fig. (L705) |
| E23 | Satellite flux / statistical | "For this we bootstrap the flux measurements within their uncertainties, and perform 100 perturbations for each galaxy." | Ghizzardi:L712 | Not given | system / point | g_bar | Method paper |
| E24 | Satellite gNFW smoothing | "the cumulative stellar mass profiles of the satellite galaxies are quite noisy and not smooth ... we fitted the stellar mass profiles beyond the BCG ($R>100$ kpc) with a gNFW profile with shape parameters fixed" | §5.3 L408 | Not quantified | system | g_bar | Not quantified |
| E25 | Satellite projection correction (method paper) | "We find that 75$\%$ of the mass obtained integrating along the line of sight lies within the sphere with radius $R_{500}$." | Ghizzardi:L715 | factor 0.75 at R500 | system | g_bar | Not mentioned in Eckert+22 |
| E26 | Stellar mass systematics / IMF (method paper) | "assuming a \citet{salpeter55}-diet Initial Mass Function (IMF) ... provides values that exceed by a factor $ \sim 2$ those obtained using a \citet{chabrier03} mass function" / "our comparison shows that we may be underestimating stellar masses by as much as 60\%." | Ghizzardi:L749, L923 | factor ~2 (IMF); up to 60% | dataset | g_bar | Not discussed in Eckert+22 |
| E27 | ICL omitted | "the contribution of ICL to the total baryon budget is expected to be small \citep[$<5\%$; e.g.,][]{gonzalez07}" | §5.3 L410 | <5% | dataset | g_bar (low) | Not included |
| E28 | Stellar fraction errors at overdensity radii | Table 4, e.g. A644 "$f_{\star,500}$ ... $1.3\pm0.5$", A2029 "$2.1\pm0.7$" | §5.4 L424–428 | ±0.4–0.9 percentage points | system | g_bar | Table 4 (CL not stated) |
| E29 | Gas-fraction errors | Table 4, e.g. A1795 "$13.4\pm0.3$" ($f_{\rm gas,500}$) | §5.4 L425 | ±0.1–1.2 percentage points | system / point | g_bar | Table 4 |
| E30 | Validity of HSE at large radii | "although the validity of the HSE assumption at large radii is unclear" | §5.1 L373 | Not quantified | point (outskirts) | g_obs | Statement only |

**Correlations between radii.**
- These are discussed only for the SZ input (E2).
- The paper says the BCG stellar-mass uncertainty is "constant with radius" (E18). That implies full correlation across radii for the BCG, but this is my inference.
- No covariance between NP g_obs points is stated as computed or released.
- No covariance between g_obs and g_bar is discussed. Both use the same gas density, but the paper does not discuss this.

---

## E. The radial acceleration relation as presented

**E15. Binning and plotting**

- Fig. 9 (L442–446) plots individual NP points and Einasto curves for the five clusters. No binning is described.
- L451: "The baryonic and observed acceleration were computed locally from the reconstructed profiles".
- Comparison curve, Eq. mcgaugh (L461) with "$g_{\dagger}=1.2\times10^{-10}$ m s$^{-2}$" (L465). The caption cites "the associated 0.06 dex scatter".

**E16. Fitted relation (as published)**

- Eq. model_rar, L480: `g_{\rm obs} = g_{\rm bar} \left(1+\frac{g_1}{g_{\rm bar}} \right)^{\alpha_1} \left(1+\frac{g_2}{g_{\rm bar}} \right)^{\alpha_2-\alpha_1}`.
- L486: "For the two acceleration scales we obtain $g_{1} = 2.3_{-0.8}^{+1.2}\times 10^{-10}$ m s$^{-2}$ and $g_2 = 1.2_{-0.7}^{+0.9}\times 10^{-11}$ m s$^{-2}$ ... The fitted slopes yield $\alpha_1=1.4_{-0.5}^{+0.7}$ and $\alpha_2=-1.2_{-0.7}^{+0.9}$."
- The fit is made to NP points (L486). The confidence level of the parameter intervals is not stated; the Fig. 10 caption mentions a "$1\sigma$ error envelope" (L474).

**E17. Scatter and comparison with galaxies**

- L486: "The model provides an adequate description of the data at hand, with an intrinsic scatter $\sigma_{\ln g_{\rm obs}}=0.21\pm0.02$."
- L522: "While our clusters indeed define their own RAR with a scatter $\sigma_{\ln g}=0.21$".
- L465: "The behavior of the relation is inconsistent with the \citet{mcgaugh16} relation at high statistical significance, even when considering the nonparametric reconstruction only. The observed acceleration is up to 5 times higher than expected".
- L467: "Around $g_{\rm bar}\sim2\times 10^{-11}$ m s$^{-2}$ we observe another change of regime ... Our systems eventually catch up with the \citet{mcgaugh16} RAR in the outermost regions, although the slope of the relation is widely different."
- L541: "with the observed acceleration exceeding the expected value by a factor of $\sim5$ around $g_{\rm bar}=2\times10^{-11}$ m s$^{-2}$."
- L449 reports earlier work: "the normalization of the observed acceleration is higher than what was found in rotationally supported galaxies \citep{chan20,tian20,pradyumna21}".
- §5.6 (L488–493) adds a calculation of the "missing" mass under the McGaugh relation, using Einasto reconstructions. L520: "our observed gravitational acceleration would need to be biased low by about a factor of 2 at $R_{200}$".

---

## F. Data availability

**F18. What is released**

- L56: "The codes developed in the framework of this project are made publicly available. In particular, we release our mass reconstruction code in the form of an easy-to-use Python package named \texttt{hydromass}. Our \emph{XMM-Newton} mock data generator can be downloaded from GitHub."
- L122, footnote: `https://github.com/domeckert/hydromass`.
- L299, footnote: `https://github.com/domeckert/xmm\_simulator`.
- Earlier X-COP products, L70 footnote: `https://dominiqueeckert.wixsite.com/xcop`.
- L531: "which we distribute in the form of the public Python package \texttt{hydromass}".
- **Not stated:** any licence or terms of use, any data-availability section, CDS/VizieR tables, or released g_obs/g_bar tables. There is no "Data availability" section in the arXiv v1 text.

**F19. Contents of released g_obs/g_bar tables**

- **Not stated.** The paper gives no columns, radii, units, error definitions or confidence levels for released tables.
- In-text tables give asymmetric errors without a stated confidence level (Table 1, L324–335) and ± errors without a stated confidence level (Table 4).

**F20. The 12-cluster mass reconstructions**

- Table 1 gives NFW results for all 12: z, N_H, R500,TOT, M500,TOT, M200,TOT, c200,TOT, plus DM-only M200 and c200 for the five clusters.
- Appendix A, Figs. A.1–A.11 (L558–722), plus Fig. 1 for A1795, show per-cluster reconstructions.
- Einasto results are deferred to Paper II, L342: "The results obtained with the Einasto model are presented and discussed in Paper \rom{2}."
- **Not stated:** any release of NP mass profiles for the 12 clusters.

---

## G. Differences from Ettori et al. 2019 (E19) and the 2019 archive

- L190: "We expand on the work of E19 in several ways. First, by correcting for the telescope's PSF ... Second, in the Einasto case we leave the Einasto index $\alpha$ free, whereas previously its value was fixed to $1/\alpha\equiv\mu=5$".
- L344: "Correcting for PSF smearing increases the concentration parameter of the NFW profile, which results in slightly higher masses in the core and lower masses in the outskirts ... Our new masses are slightly higher inside $R_{2500}$ and slightly lower inside $R_{200}$; the difference, however, is always within 10\% ... we conclude that the NFW concentrations given in E19 were slightly underestimated."
- Table 3 (L347–356):
  - caption: "For consistency, the masses estimated here were converted into the same cosmology as that used in E19.";
  - mean M_hydromass/M_E19 = 1.08, 1.01, 0.96, 0.93 at Δ = 2500, 1000, 500, 200;
  - median = 1.05, 1.02, 0.95, 0.90.
- Density method: the multi-scale fit replaces the L1 regularisation of ghirardini19 (Fig. 1 caption, L277).
- New AO-17 data for A3266 and A2029 (L65, L70).
- Cosmology, L56: "Planck 2015 $\Lambda$CDM cosmology ... with $H_0=67.8$ km/s/Mpc and $\Omega_m=0.308$". E19's cosmology is not stated in this paper.
- **Per-cluster R500 and M500** (Table 1, NFW "TOT"; L324–335):

| Cluster | z | R500,TOT [kpc] | M500,TOT [10¹⁴ M☉] | M200,TOT | c200,TOT | M200,DM | c200,DM |
|---|---|---|---|---|---|---|---|
| A85 | 0.0555 | 1214 (−4/+4) | 5.03 (−0.05/+0.05) | 7.04 (−0.07/+0.08) | 4.708 (−0.044/+0.042) | – | – |
| A644 | 0.0704 | 1398 (−16/+16) | 7.80 (−0.27/+0.26) | 10.97 (−0.43/+0.45) | 4.597 (−0.156/+0.163) | 10.98 (−0.41/+0.45) | 4.458 (−0.169/+0.171) |
| A1644 | 0.0473 | 1031 (−10/+11) | 3.06 (−0.09/+0.09) | 4.93 (−0.20/+0.21) | 2.548 (−0.135/+0.140) | – | – |
| A1795 | 0.0622 | 1160 (−6/+6) | 4.42 (−0.07/+0.07) | 6.04 (−0.11/+0.11) | 5.454 (−0.076/+0.072) | 6.82 (−0.13/+0.13) | 4.510 (−0.072/+0.074) |
| A2029 | 0.0766 | 1340 (−9/+9) | 6.91 (−0.14/+0.14) | 9.29 (−0.21/+0.22) | 5.929 (−0.101/+0.102) | 11.67 (−0.28/+0.29) | 4.185 (−0.091/+0.093) |
| A2142 | 0.09 | 1453 (−9/+9) | 8.93 (−0.16/+0.17) | 13.33 (−0.30/+0.32) | 3.440 (−0.070/+0.076) | 13.94 (−0.31/+0.30) | 3.046 (−0.074/+0.076) |
| A2255 | 0.0809 | 1202 (−16/+17) | 5.01 (−0.20/+0.22) | 8.94 (−0.56/+0.66) | 1.800 (−0.180/+0.193) | – | – |
| A2319 | 0.0557 | 1424 (−4/+5) | 8.12 (−0.08/+0.08) | 11.61 (−0.14/+0.14) | 4.233 (−0.070/+0.068) | 12.16 (−0.14/+0.15) | 4.098 (−0.079/+0.079) |
| A3158 | 0.059 | 1146 (−11/+12) | 4.25 (−0.13/+0.14) | 6.46 (−0.25/+0.28) | 3.178 (−0.146/+0.145) | – | – |
| A3266 | 0.0589 | 1381 (−10/+10) | 7.43 (−0.15/+0.16) | 12.22 (−0.36/+0.41) | 2.352 (−0.098/+0.097) | – | – |
| RXC1825 | 0.065 | 1109 (−8/+9) | 3.88 (−0.08/+0.09) | 5.66 (−0.17/+0.18) | 3.807 (−0.159/+0.165) | – | – |
| Zw1215 | 0.0766 | 1346 (−21/+21) | 7.00 (−0.32/+0.35) | 11.44 (−0.70/+0.76) | 2.413 (−0.148/+0.155) | – | – |

Table 1 also lists N_H [10²⁰ cm⁻²]: 2.8, 7.5, 4.1, 1.2, 3.2, 3.8, 2.5, 3.2, 1.4, 1.6, 9.4, 1.7 in the same row order.

- **Not stated:** any change in redshifts or centres relative to E19 or the 2019 archive, and any per-cluster comparison with E19's R500.

---

## Not stated (what I looked for, and where)

Places searched: all of `hydromass.tex`, by full read and by grep for "release", "available", "github", "zenodo", "CDS", "covarian", "correlat", "68", "sigma", "mu".
- Per-cluster numeric radial ranges (inner and outer radius of the NP points).
- Gas-mass conversion constants (μ, n_e/n_H, abundance table used for emissivity) and the M_gas integral.
- Priors on the NP normalisations G_i, and whether the P0 prior applies to NP.
- Confidence level of the Table 1 and Table 4 errors and of the RAR-fit parameter intervals (only the "$1\sigma$ error envelope" in the Fig. 10 caption).
- Covariance between NP radii, and between g_obs and g_bar.
- Any released g_obs/g_bar table (columns, units, errors), licence or terms, or a data-availability section.
- The Υ★DYN values actually adopted for each BCG, in particular A644 and A2319.
- Whether the satellite input to g_bar was deprojected, and how.
- Whether the Loubser+20 (H0=73, Loubser:L139) and vdB15 (H0=70, vdB15:L68) quantities were rescaled to H0=67.8.
- The redshifts and centres used versus E19.
- An explicit statement that the RAR uses all radii of all five clusters, or any radius cut.

---

## Doubts

**D1. The candidate id in the brief is wrong.** 2205.01123 is Paper II (A&A 666, A41). The arXiv abstract of Paper II, seen only on its abs page, says "After removing morphologically disturbed systems". That exclusion applies to Paper II, not to this paper.

**D2. Satellite projection (inference).**
- Eckert+22 calls the satellite input "cumulative stellar mass of satellite galaxies" (L402) and fits a gNFW to it (L408). It never says whether the cumulative profile is projected or 3D.
- The X-COP method paper (Ghizzardi:L715) says its cumulative profiles are projected. It converts to a sphere only at R500, by a factor 0.75.
- Whether Eckert+22 fitted a projected gNFW and then used the 3D form, or treated the projected profile as 3D, is not stated.

**D3. BCG inside the satellite profile.** Ghizzardi:L711 says the BCG is included in its cumulative stellar mass. Eckert+22 fits satellites only at R>100 kpc (L408). Eckert+22 does not say whether the BCG light was removed from the satellite profile, or whether the gNFW fit carries any BCG mass inward.

**D4. Which "gNFW" is meant.**
- L408 says the satellite gNFW is "(see Eq. \ref{eq:gnfw})". That equation is the five-parameter pressure form (L220).
- vdB15's gNFW is ρ ∝ (r/R_s)^−α (1+r/R_s)^−(3−α) (vdB15:L338), with stellar-mass values α=1.63, c=0.64 (vdB15:L344).
- Ghizzardi uses c=0.72, α=1.64 (Ghizzardi:L715), which are vdB15's number-density values for massive galaxies (vdB15:L342).
- Which parameter set Eckert+22 fixed is not stated.

**D5. Wording of the RAR g_obs model.** L458 says "the Einasto fit to the DM component only". The Fig. 9 caption (L445) says "the Einasto fit to the baryons+DM model". My inference is that both mean a DM Einasto plus fixed baryons, giving the total, but the wording differs.

**D6. Table 1 "TOT" for the five clusters.** The caption (L316) says "In this case, the quoted total mass is computed from the sum of DM and baryonic density profiles". It is ambiguous whether this applies to the TOT columns for the five clusters, or whether TOT is the NFW fit to the total field (as the earlier part of the caption says).

**D7. Internal numeric differences in the paper.**
- Baryon depletion range: "$0.2-0.5 R_{500}$" (L435) vs "$[0.1-0.5]R_{500}$" (L539).
- Gas dominance of baryons: "beyond $\sim0.05R_{500}$" (L410, differential) vs "beyond $\sim0.1R_{500}$" (L433, L539, integrated). This may be differential vs cumulative.
- c200: "$3.69_{-0.36}^{+0.39}$" (L383) vs "$3.69\pm0.39$" (L537).
- Factor of 5: "up to 5 times higher" in the regime below 10⁻¹⁰ m s⁻² (L465, L518) vs "a factor of $\sim5$ around $g_{\rm bar}=2\times10^{-11}$" (L541).
- Baryon fraction: "Inside $R_{500}$ our estimated baryon fraction is equal to the cosmic value" (L435) vs the abstract's "reaches the cosmic value at $R_{200}$" (L38).

**D8. BCG errors for A644 and A2319.** L111 says the BCG errors come from weak-lensing mass errors. A644 and A2319 had no weak-lensing masses (L109), and how their errors were set is not stated.

**D9. Cosmology mismatch.** The mixed cosmologies across source papers (67.8 / 73 / 70 km/s/Mpc) may or may not have been harmonised. This is not stated.

**D10. Version of record.** I read only arXiv v1 (2 May 2022). The A&A version may contain a data-availability statement or corrections I could not see.

**D11. A commented-out IMF line.** Ghizzardi:L926 has an IMF statement (Salpeter = 1.74× Chabrier) inside a LaTeX comment line, so it is not in the published text. I used only the live text at L749 (factor ~2).

**D12. Scale assignments are my classification.** In table D, "scale" and the effect on g_bar of gas inhomogeneities (E8) are my judgement from the quoted text. The paper does not classify them.

---

### Items worth remembering (from this run, not from memory)

- The correct arXiv id for Eckert+22 (A&A 662, A123) is 2205.01110v1. 2205.01123 is Paper II, A&A 666, A41. Learned from the arXiv abs pages.