# Reader B report: Eckert et al. 2022b (Paper II), arXiv 2205.01123, for X-COP v2 (Atlas step A, D-089)

**Header**
- Reader: **Reader B**
- Date: 2026-11-03
- Sources read:
  1. **Paper II**: arXiv **2205.01123 v1**. The abstract page lists only v1, submitted 2 May 2022, journal reference A&A 666, A41 (2022). Title and authors confirmed: "Constraints on dark matter self-interaction from the internal density profiles of X-COP galaxy clusters", by D. Eckert, S. Ettori, A. Robertson, R. Massey, E. Pointecouteau, D. Harvey and I. G. McCarthy. The main file is `einasto.tex` (268 lines). It pulls in `tab2.tex` (Table 2, 20 lines), and I also read `einasto.bbl`. E-print SHA-256: `a138d88fec5d3b7627eeb9657d663c30f9aae7a12ce3e968edf08bba07503fcb`. I read the whole paper. I also pulled the text labels out of the figure PDFs, but only the labels.
  2. **Paper I**, for a few specific line references only: arXiv **2205.01110 v1**, "The gravitational field of X-COP galaxy clusters". Main file `hydromass.tex`. E-print SHA-256: `18fc2e8025f56c716a864e5ef9436cccb5f0be05cff7a0f004aedd4605e5c7d8`. I did not read it in full; I used a grep for the Paper II links and read lines 56, 190, 342 and 393.
- I read no other method papers. Paper II hands every g_bar and method question on to Paper I.
- I opened no shared data files. I did not read the published A&A version, because only arxiv.org and GitHub are reachable. The arXiv text calls the paper "this Letter".
- Working directory: `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/e22b_readerB`. Sources are in `src2/` and `src1/`.

**Main finding:** Paper II has **no g_bar content at all**. It has no baryon decomposition, no radial acceleration relation, no non-parametric profiles, no NFW results, no satellites, no intracluster light and no mass-to-light ratio. It fits **one Einasto profile to the total hydrostatic mass** of each of the 12 clusters. What it gives for g_obs is Table 2: M500 from the Einasto fit, r_s, ρ_s, μ=1/α, the centroid shift w, and the fitted radial range. All g_bar material has to come from Paper I.

---

## A0. Relation to Paper I

| What | Quote | Location |
|---|---|---|
| Framework taken from Paper I | "In a companion paper (Eckert et al. 2022, hereafter Paper \rom{1}), we presented a general framework to recover the mass profiles of galaxy clusters from X-ray and SZ data under the assumption that the gas is in hydrostatic equilibrium within the DM potential well. Here we apply our framework to recover the parameters of the Einasto functional form by fitting the X-COP data over a wide range in radius" | einasto.tex §1, l.61 |
| Method and systematics deferred to Paper I | "The methodology adopted to recover the mass profiles from X-ray surface brightness and spectroscopic temperature profiles and SZ pressure profiles is presented in detail in Paper \rom{1}." | §2.2, l.82 |
| | "For more details on the mass reconstruction technique and a thorough discussion of the associated systematic uncertainties, we refer the reader to Paper \rom{1}." | §2.2, l.103 |
| HSE validity | "The validity of the assumption of hydrostatic equilibrium (HSE) in the case of the X-COP clusters was discussed in detail in \citet{ettori19,eckert19} and in Paper \rom{1}." | §2.2, l.80 |
| Einasto compared with the non-parametric method | "In Paper \rom{1} we showed that the Einasto model provides a good representation of the data at hand and closely follows the results obtained with a non-parametric technique that makes no assumption on the shape of the mass profile." | §2.2, l.129 |
| BCG stellar masses | "...compared them with the stellar masses of the BCGs in X-COP clusters \citep[see Paper \rom{1}]{loubser20}" and Fig. B caption: "The black stars show the measured BCG stellar masses within the same aperture in X-COP clusters (see Paper \rom{1})." | App. B, l.263; caption l.248 |
| Cosmology (Paper II) | "Throughout the paper, we assume a \emph{Planck} 2015 $\Lambda$CDM cosmology with $\Omega_m=0.308$, $\Omega_\Lambda=0.692$ and $H_0=67.8$ km/s/Mpc" | §1, l.61 |
| Cosmology (Paper I) | "Planck 2015 $\Lambda$CDM cosmology \citep{planck15_13} with $H_0=67.8$ km/s/Mpc and $\Omega_m=0.308$." The two papers are consistent; Paper I does not state Ω_Λ on this line. | hydromass.tex l.56 |
| **Different parametrisation (Paper II)** | "Following \citet{ettori19}, rather than fitting for the characteristic density $\rho_s$ we optimise for the unitless normalisation $c$ ... with $\Delta=200$ the chosen fit overdensity ... we optimise for $\mu\equiv1/\alpha$ ... four free parameters: the scale radius $r_{s}$, the normalisation $c$, the inverse $\mu$ ... and the integration constant $P_0$." | §2.2, l.105–111 |
| Different parametrisation (Paper I) | "Instead of the scale radius $r_s$ and density normalization $\rho_s$ we optimize for the overdensity radius $R_{200}$ and the concentration $c_{200}=R_{200}/r_{s}$ ... a similar description of the priors on the Einasto model is provided in Paper \rom{2}." | hydromass.tex l.190 |
| Paper I hands the Einasto results to Paper II | "The results obtained with the Einasto model are presented and discussed in Paper \rom{2}." | hydromass.tex l.342 |
| Radial range | Paper II fits each cluster over its own range in units of R200 (Table 2, R_min and R_max). The simulations are fitted over "$0.01 \times R_{200}$ and $R_{200}$". | tab2.tex l.7–18; einasto.tex l.181 |
| Mass at R500 | Paper II tabulates only "$M_{500,Einasto}$", described as "Value of $M_{500}$ and uncertainty from the best-fit Einasto model". It does not compare these with Paper I's NFW masses. | tab2.tex l.3; einasto.tex l.142 |

Paper II says nothing about whether its Einasto runs are the same chains as any Einasto runs in Paper I. Paper I's Einasto fits with baryons separated out (hydromass.tex l.410) are a different model from Paper II's total-mass Einasto fit.

## A. Sample

**1. Clusters analysed.** "We applied our mass profile reconstruction technique to all 12 X-COP systems. The resulting parameters are provided in Table \ref{tab:params}." (§3.1, l.135). The clusters in Table 2 are A85, A644, A1644, A1795, A2029, A2142, A2255, A2319, A3158, A3266, RXC1825 and ZW1215 (tab2.tex l.7–18).

The sample is defined at l.67: "12 massive galaxy clusters in the redshift range $0.04<z<0.1$. The sample contains the most significant SZ detections from the \emph{Planck} PSZ1 catalog \citep{psz1} with the exception of three highly perturbed systems for which the validity of a radially-averaged analysis cannot be guaranteed. For each cluster, a minimum of 5 \emph{XMM-Newton} pointings are available to cover uniformly the gas distribution at least out to $2\times R_{500}$."

On the "complete" baryon budget, Paper II does not list which clusters have one. It says only: "Since measurements of the stellar mass profiles are currently available only for a subset of X-COP systems, in this paper we fitted an Einasto profile to the total gravitational field" (App. B, l.263). For comparison, Paper I l.402 names A644, A1795, A2029, A2142 and A2319; that list is from Paper I, not Paper II.

**2. Radial range per cluster**, from Table 2 (tab2.tex l.7–18), as R_min to R_max in units of R200:

| Cluster | R_min to R_max (R200) |
|---|---|
| A85 | 0.009 to 1.03 |
| A644 | 0.013 to 0.87 |
| A1644 | 0.010 to 1.30 |
| A1795 | 0.012 to 1.29 |
| A2029 | 0.012 to 1.13 |
| A2142 | 0.007 to 1.07 |
| A2255 | 0.028 to 1.24 |
| A2319 | 0.020 to 1.12 |
| A3158 | 0.011 to 1.06 |
| A3266 | 0.009 to 0.92 |
| RXC1825 | 0.013 to 1.19 |
| ZW1215 | 0.013 to 0.94 |

The column description reads "Lower and upper bounds of the fitting range as a fraction of $R_{200}$" (l.142–143). Paper II does not give R200 values in kpc.

**3. Exclusions and different treatment**
- A2319, for HSE: "With the exception of one peculiar system for which there is clear evidence of a breakdown of hydrostatic equilibrium \citep[A2319,][]{ghirardini18}" (l.80).
- Outliers: "three systems (A2319, A644, and A2255) exhibiting larger values of $\alpha$ ($\gtrsim 0.5$)" (l.135). Also: "A closer look at these systems shows that they are all unrelaxed systems with large deviations from spherical symmetry." (l.152)
- The criterion for "morphologically disturbed". The paper never defines the phrase directly. It uses it at l.45 ("After removing morphologically disturbed systems") and at l.227 ("...all of which appear morphologically disturbed, as indicated by a large centroid shift"). The operational criterion is the centroid shift w, Eq. at l.155: $w = \frac{1}{R_{500}} \sqrt{\frac{1}{N-1}\sum_{i=1}^N (\Delta_i - \Delta_{500})^2}$, measured on "[0.7-1.2] keV mosaic images", with "$N$ apertures of decreasing radius $R_i$, with $R_1=R_{500}$" (l.152). Three thresholds appear:
  - "Most studies ... place the boundary between relaxed and unrelaxed systems in the range $w=0.01-0.02$. We can see that all the quoted outliers exhibit values of $w$ greater than $0.02$" (l.161).
  - **The selection:** "To avoid the potential impact of miscentering and hydrostatic bias, we selected a subsample of X-ray regular systems with $w<0.015$. This subsample excludes four objects with high centroid shifts, for which the offset between the X-ray peak and the bottom of the gravitational potential may be large and thus the value of $\alpha$ may be unreliable." (l.163)
  - The Fig. 2 caption says "$w<0.0015$" (l.148). This conflicts with l.163; see Doubts.
- The paper does not name the four excluded clusters. Reading Table 2, where w is in units of 10⁻³, the ones with w ≥ 15×10⁻³ are A644 (20.97), A2255 (31.40), A2319 (33.08) and A3266 (30.84). That identification is my inference. l.227 says "The subset of 8 X-ray regular systems", and 12 − 4 = 8 matches.
- Reasons the paper gives: "First, the validity of the hydrostatic equilibrium assumption in unrelaxed systems is unclear ... Second, the position of the X-ray centroid may not coincide with the bottom of the potential well ... we expect the reconstructed mass profiles to be substantially flatter than the true profiles, which would bias the reconstructed values of $\alpha$ towards high values." (l.161)
- The excluded clusters are still fitted and tabulated. The exclusion applies only to the population mean of α.

## B. g_obs

**4. How the total mass is obtained.** Paper II uses one method only: a forward fit of a parametric Einasto model, assuming HSE.
- "$\frac{dP_{\rm gas}}{dr} = - \rho_{\rm gas}\frac{GM(<r)}{r^2}$" (Eq. at l.77).
- "The density profile is integrated numerically over the volume to determine the cumulative model mass as a function of radius, $M_{\rm mod}(<r)$. The gas density profile is described as a linear combination of King functions \citep{eckert20} and fitted jointly to the X-ray surface brightness profile. The hydrostatic equilibrium equation Eq. \ref{eq:hse} is then integrated to predict the 3D pressure profile" (l.91).
- The pressure integral at l.94 runs from r to r₀, "with $r_0$ the outermost radius of the SZ pressure profile and $P_0\equiv P(r_0)$ the integration constant ... the model pressure is projected along the line of sight and convolved with the instrumental PSF to predict the expected spectroscopic temperature profile." (l.103)
- Code: "The code ... includes a wide range of effects (non-parametric gas density deprojection, PSF convolution, spectroscopic temperature weights, and profile covariance matrices) into an efficient Bayesian optimisation framework ... Python package \texttt{hydromass}" (l.82).
- Sampler: "No U-Turn Sampler (NUTS) as implemented in \texttt{PyMC3} ... Four independent chains ... each with 1,000 tuning steps and 1,000 output samples." (l.129)
- **The non-parametric log-normal mixture is not used or presented in Paper II.** It is mentioned once, as a Paper I result (l.129).

**5. Reconstructions presented**
- **Einasto, total mass**: $\rho_{\rm Einasto}(r) = \rho_s \exp[-\frac{2}{\alpha}((r/r_s)^\alpha - 1)]$ (l.87). The parametrisation is $\rho_s = \frac{\Delta}{3} \frac{c^3}{\log(1 + c) - c / (1 + c)} \rho_c(z)$ with Δ=200 (l.108–111). The tabulated parameters are M500,Einasto (10¹⁴ M☉), r_s (kpc), ρ_s (10⁻²⁷ g/cm³), μ, w (10⁻³), R_min and R_max (R200) (tab2.tex l.3–4). Example row: "A1795 & $4.36_{-0.10}^{+0.12}$ & $323_{-13}^{+16}$ & $23.82_{-2.16}^{+2.06}$ & $4.05_{-0.20}^{+0.24}$ & $2.36\pm0.02$ & 0.012 & 1.29" (tab2.tex l.10). Table 2 does not list the fitted parameter c or P₀.
- The priors (Table 1, l.120–123) are r_s: mean 700, σ 300, range 100–3000 kpc; c: mean 1.8, σ 1.5, range 0–10; μ: mean 5, σ 3, range 0.2–20; P₀: mean P_m, σ dP_m, range P_m ± 2dP_m.
- For each cluster, α is taken from the posterior of μ: "For each system, we used the posterior distribution of $\mu$ to determine the corresponding value of $\alpha$ and its uncertainty." (l.135) Per-cluster α values are shown only in Fig. 2, not tabulated.
- Population results: "$\langle\alpha\rangle=0.22\pm0.04$ ... $\sigma_{\alpha}=0.14_{-0.05}^{+0.10}$" (l.152) and "$\langle\alpha_{\rm rel}\rangle=0.19\pm0.03$ ... $\sigma_{\alpha, rel}=0.06_{-0.03}^{+0.04}$" (l.163).
- **Not presented in Paper II:** NFW, non-parametric, the forward method, and any reconstruction with baryons subtracted. "we fitted an Einasto profile to the total gravitational field" (l.263).

**6. Input data.** "observations of their hot gaseous atmosphere using the X-ray observatory \emph{XMM-Newton}, and of the Sunyaev-Zel'dovich effect using the \emph{Planck} all-sky survey" (l.45). In detail: "reduced data and thermodynamic profiles (gas density and spectroscopic temperature) are publicly available ... \emph{Planck} SZ pressure profiles were derived for all systems following \citet{planck5} from the SZ signal reconstructed using the MILCA algorithm \citep{hurier13}" (l.69). The fit uses X-ray surface brightness, X-ray spectroscopic temperature and SZ pressure (l.82). Fig. 1 also shows "X/SZ temperatures obtained by dividing the SZ pressure by the gas density" (l.100).

**7. 3D and spherical.** M(<r) is a 3D enclosed mass under spherical HSE (l.77, l.91). On sphericity: "while most galaxy clusters should exhibit an elliptical shape, our results are mildly affected by the assumption of spherical symmetry \citep{buote12}" (l.129). The only radius at which a mass is tabulated is R500 (Table 2). The fit overdensity is Δ=200 (l.111). Fig. 1 shows "the fitted location of $R_{500}$" (l.100). No R500 or R200 values are tabulated.

**8. Corrections.** No correction is applied to g_obs. Non-thermal pressure is only simulated as a test (App. A, l.252–258), and there is no correction for hydrostatic bias: "Therefore, we conclude that the hydrostatic assumption has little impact on the results presented here." (l.258)

## C. g_bar

9. **Gas.** The paper gives only the gas density model used inside the HSE fit: "linear combination of King functions \citep{eckert20} and fitted jointly to the X-ray surface brightness profile" (l.91). It reports no gas mass profile and no gas mass.
10. **BCG.** There is no method and no M/L in Paper II. It reports only an aperture comparison: "the BCG stellar masses within 100 kpc radius for the CDM and SIDM1 cases as well as the X-COP BCG stellar masses within the same aperture" (l.263), shown in the Fig. B right panel (axis label "M*,BCG (<100 kpc) [M☉]"; values not tabulated). The source is "\citep[see Paper \rom{1}]{loubser20}" (l.263). In a test it scales "the stellar mass of the BCG by a conservative factor of 2 in the upward and downward directions" (l.265). The method, Υ*, and 3D versus projected are not stated in Paper II. Paper I l.103–111 covers them (MGE, Jeans anisotropic, Υ*DYN), but I did not read those lines for this report beyond the grep hits.
11. **Satellites.** Not stated.
12. **Intracluster light.** Not stated.
13. **Other baryons.** Not stated, apart from the simulation side: "total mass (DM + baryons)" (l.181) and "gas + stars" (l.263).
14. **g_bar as a 3D enclosed-mass acceleration.** Not applicable: Paper II computes no g_bar.

## D. Uncertainties

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | Provided? |
|---|---|---|---|---|---|---|---|
| E1 | Statistical posterior on Einasto parameters and M500 | "Parameter values and uncertainties for the Einasto parameters $r_s$, $\rho_s$, and $\mu=1/\alpha$"; "Value of $M_{500}$ and uncertainty from the best-fit Einasto model" | l.142; tab2.tex | Per cluster, asymmetric. M500: e.g. A85 ±0.08, ZW1215 −0.32/+0.30 (10¹⁴ M☉). Confidence level not stated in the caption; Fig. 1 shows "$1\sigma$" | system (a parametric profile, so errors are correlated across radii through the parameters) | g_obs | Table 2 gives marginals only. Covariance between parameters is shown only for A1795 (Fig. 1 corner plot: "the posterior distributions of the fitted Einasto model parameters and the covariance between them", l.100). No profile covariance is given |
| E2 | Hydrostatic bias, overall | "the HSE assumption is valid at the $\lesssim20\%$ level out to $R_{200}$" | l.80 | ≲20% | dataset (stated for the sample) | g_obs | No correction applied |
| E3 | HSE breakdown in A2319 | "one peculiar system for which there is clear evidence of a breakdown of hydrostatic equilibrium \citep[A2319,][]{ghirardini18}" | l.80 | Not quantified | system | g_obs | No |
| E4 | Non-thermal pressure, effect on profile shape | "the HSE assumption typically overestimates $\alpha$ by $2-8\%$ depending on the assumed non-thermal pressure profile and the true value of $\alpha$, corresponding to differences of 0.01 for $\alpha_{\rm True}=0.18$" | App. A, l.258 | 2–8% on α (0.01 at α=0.18). Profiles from Nelson+14 and Angelinelli+20 | dataset (fiducial cluster, radially varying P_NT) | g_obs (shape) | Fig. A left panel only; no correction |
| E5 | Method accuracy on a mock | "the code was found to reproduce the input mass profile with an accuracy better than 3\%" | l.82 | <3% | dataset (method) | g_obs | No |
| E6 | Prior choice | "the posterior distributions are much narrower than the prior and clearly pull away from it, therefore the results of this paper weakly depend on the choice of the prior. Using uniform priors over the range given in Table \ref{tab:priors} also returns similar results and uncertainties" | l.111 | Not quantified | dataset | g_obs | Priors in Table 1 |
| E7 | P₀ boundary condition | "for $P_0$ we set a Gaussian prior with mean and standard deviation equal to the outermost SZ pressure value and its uncertainty" | l.111 | dP_m (per cluster, not given) | system | g_obs | No |
| E8 | Spherical symmetry | "our results are mildly affected by the assumption of spherical symmetry \citep{buote12}" | l.129 | Not quantified | system | g_obs | No |
| E9 | Miscentering in unrelaxed clusters | "In case our profiles are miscentered ... we expect the reconstructed mass profiles to be substantially flatter than the true profiles, which would bias the reconstructed values of $\alpha$ towards high values." | l.161 | Not quantified | system (the 4 clusters with high w) | g_obs (inner shape) | w given in Table 2 |
| E10 | BCG stellar mass, effect on fitted α | "modified the stellar mass of the BCG by a conservative factor of 2 ... For an input value $\alpha=0.18$ the retrieved value of $\alpha$ changes by $\pm0.02$" | App. B, l.265 | Factor 2 in mass gives ±0.02 in α | dataset (fiducial test) | Total-profile shape. This is the baryon part of the total mass, not a g_bar input | No |
| E11 | Profile covariance in the fit | "...and profile covariance matrices) into an efficient Bayesian optimisation framework" | l.82 | Not stated | point (correlations between data radii are used in the fit) | g_obs | Not provided in the paper |
| E12 | Uncertainty on centroid shift w | Table 2, e.g. "$3.85\pm0.02$" | tab2.tex | ±0.01 to 0.26 (10⁻³) | system | Neither (selection only) | Table 2 |

Terms I looked for and did not find: X-ray or SZ calibration (temperature calibration, cross-calibration); the M/L or IMF for g_bar; the choice of method as a systematic on mass (Paper II uses one method only); the regularisation of the non-parametric method; the uncertainty on redshift or cosmology; and the confidence level of the Table 2 errors.

These are not g terms, but I record them: the population intrinsic scatter of α (l.152, 163); the α–σ/m interpolation method, "Similar constraints ... (linear interpolation, cubic spline, or second-order polynomial)" (l.210); and the statistical uncertainty of the simulation means, "can safely be ignored" (l.210).

## E. The radial acceleration relation

15–17. Not present. Paper II has no g_obs-versus-g_bar plot, no binning, no fitted relation, and no comparison of scatter with galaxies.

As stated only, the paper's conclusions are about the Einasto α and the self-interaction cross section of the account it tests: "$\alpha\approx 0.18 + 0.20 ( (\sigma/m)/(\mbox{1 cm$^2$/g)})^{0.63}$" (l.229); "$\alpha_0=0.178$, $\alpha_1=0.20$, and $\gamma=0.63$" (l.203); "$\frac{\sigma}{m} < 0.19$ cm²/g ... (95\% confidence level)" (l.207). The paper also says: "The hydrostatic mass profiles of the 12 X-COP galaxy clusters are well represented by an Einasto model over more than two decades in radius." (l.225)

## F. Data availability

18. There are two statements:
- "the reduced data and thermodynamic profiles (gas density and spectroscopic temperature) are publicly available\footnote{\href{https://dominiqueeckert.wixsite.com/xcop}{...}}" (l.69)
- "The code is publicly available in the form of the Python package \texttt{hydromass}\footnote{\href{https://github.com/domeckert/hydromass}{...}}" (l.82)

No licence or terms are stated. No data release specific to Paper II is stated.

19. Nothing is said about released g_obs or g_bar tables.

20. The 12-cluster mass reconstructions appear only as Table 2's Einasto parameters and M500. The paper does not mention releasing posterior chains or profiles.

## G. Differences from Ettori et al. 2019 and the 2019 archive

- Parametrisation follows Ettori et al. 2019: "Following \citet{ettori19}, rather than fitting for the characteristic density $\rho_s$ we optimise for the unitless normalisation $c$" (l.105).
- Cored models for the outliers: "in \citet{ettori19} the mass profiles of these same systems were found to be better represented by models exhibiting a central core (Burkert, non-singular isothermal sphere)" (l.152).
- From Paper I, not Paper II: Ettori et al. 2019 fixed μ=5, whereas the new analysis leaves α free (hydromass.tex l.190).
- Paper II gives no per-cluster R500, no redshifts, and no comparison with the 2019 masses or the 2019 archive. The only per-cluster mass is M500,Einasto (Table 2):

| Cluster | M500,Einasto (10¹⁴ M☉) |
|---|---|
| A85 | 6.35 (−0.08/+0.08) |
| A644 | 6.06 (−0.30/+0.30) |
| A1644 | 2.97 (−0.09/+0.09) |
| A1795 | 4.36 (−0.10/+0.12) |
| A2029 | 7.76 (−0.22/+0.21) |
| A2142 | 9.41 (−0.19/+0.20) |
| A2255 | 5.58 (−0.27/+0.29) |
| A2319 | 7.79 (−0.10/+0.09) |
| A3158 | 4.32 (−0.15/+0.14) |
| A3266 | 7.44 (−0.13/+0.14) |
| RXC1825 | 3.93 (−0.09/+0.09) |
| ZW1215 | 6.65 (−0.32/+0.30) |

## Not stated

I searched all of `einasto.tex`, `tab2.tex` and the figure-label text for each item below and did not find it:
- **Gas:** gas mass profiles.
- **BCG:** the method, Υ*, and whether the result is 3D.
- **Satellites, ICL and any baryon budget per cluster.**
- **g_bar and the radial acceleration relation.**
- **Other reconstructions:** NFW and non-parametric.
- **Cluster properties:** R500, R200 in kpc, and redshifts per cluster.
- **Uncertainties:** the confidence level of the Table 2 errors, calibration systematics, and correlation matrices of the profiles.
- **Data and procedure:** the band used for the surface-brightness profile in the mass fit, the names of the 4 excluded clusters, licence terms, the contents of released files, and differences from the 2019 archive.

## Doubts

1. **Threshold conflict.** The text uses w<0.015 (l.163). The Fig. 2 caption uses w<0.0015 (l.148). Table w is in units of 10⁻³, so 0.015 = 15 in table units, which separates 4 clusters and leaves 8, consistent with "four objects" (l.163) and "8 X-ray regular systems" (l.227). The caption value looks like a typo, but that is an inference.
2. **Names of the excluded clusters are my inference** from Table 2: A644, A2255, A2319 and A3266. A3266 is excluded on w (30.84×10⁻³) but is not one of the three α outliers. Its μ=6.45 corresponds to α≈0.155 by my own conversion; the paper does not give this. A1644 (13.76×10⁻³) sits just below the cut.
3. **The upper error on the relaxed-subsample scatter differs:** "$\sigma_{\alpha, rel}=0.06_{-0.03}^{+0.04}$" (l.163) against "$\sigma_\alpha=0.06_{-0.03}^{+0.05}$" (l.227).
4. **ρ_s formula and Table 2.** The ρ_s expression at l.108 uses the NFW-form denominator log(1+c) − c/(1+c) for an Einasto model. I record it as written. Table 2 lists ρ_s, not the fitted c; the conversion is not shown.
5. **"Morphologically disturbed" has no explicit definition.** It is tied to "a large centroid shift" (l.227). Three thresholds coexist: 0.01–0.02 from the literature, >0.02 for the outliers, and <0.015 for the selection.
6. **Confidence level of the Table 2 errors is not stated.** I infer 1σ from the Fig. 1 caption, which covers only A1795's model band.
7. **Versions.** The arXiv text calls itself a "Letter". The commented-out abstract (l.47, not rendered) gives "$\sigma/m < 0.14$ cm$^2$/g (90\% confidence level)", against 0.19 at 95% in the live text. I did not compare against the published A&A 666 A41 version.
8. **The R_min and R_max scaling radius is not given.** They are fractions of R200, but no R200 values or their source (Einasto, Δ=200?) are stated.
9. **Paper I relationship.** I cannot tell from Paper II whether its total-mass Einasto chains are the same runs as Paper I's Einasto results. The parametrisations differ: (r_s, c, μ) in Paper II against (R200, c200) in Paper I.

**Next step:** a third party should compare this with Reader A's report. Every g_bar item (C9–C14) and every radial acceleration relation item (E) has to be taken from Paper I, because Paper II contains none of them.