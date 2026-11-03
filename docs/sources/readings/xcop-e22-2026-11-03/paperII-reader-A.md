# Reader A report: Eckert et al. 2022b (Paper II), X-COP v2, Atlas step A (D-089)

**Reader:** Reader A
**Date:** 2026-11-03
**Working directory:** /tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/e22b_readerA

**Sources read**

| Paper | arXiv id / version | Journal (from arXiv jref) | Main .tex | SHA-256 of e-print |
|---|---|---|---|---|
| Paper II: "Constraints on dark matter self-interaction from the internal density profiles of X-COP galaxy clusters". Eckert, Ettori, Robertson, Massey, Pointecouteau, Harvey, McCarthy | 2205.01123 **v1**, the only version (submitted Mon 2 May 2022) | A&A 666, A41 (2022); DOI 10.1051/0004-6361/202243205 | `einasto.tex` (268 lines) plus `tab2.tex` (20 lines, `\input` as Table 2); bibliography `einasto.bbl` | `a138d88fec5d3b7627eeb9657d663c30f9aae7a12ce3e968edf08bba07503fcb` |
| Paper I: "The gravitational field of X-COP galaxy clusters" (targeted grep of cross-references only, not re-read) | 2205.01110 **v1**, the only version | A&A 662, A123 (2022) | `hydromass.tex` (727 lines) | `18fc2e8025f56c716a864e5ef9436cccb5f0be05cff7a0f004aedd4605e5c7d8` |

No shared data files were opened or downloaded. Paper I's arXiv source contains per-cluster subdirectories (`a85/`, `a644/` and so on); I did not open them. The X-COP web page that Paper II cites (wixsite) was not accessed.

**Main finding:** Paper II is a short Letter. It fits **one parametric Einasto model to the total hydrostatic mass** of each of the 12 clusters. It contains **no g_bar, no baryon decomposition, no non-parametric profiles, no NFW results and no radial acceleration relation.** Everything bearing on g_bar is either absent or deferred to Paper I. Its only per-cluster numerical product is Table 2.

---

## A0. Relation to Paper I

**What Paper II says it takes from Paper I**

- **Framework and method:** "In a companion paper (Eckert et al. 2022, hereafter Paper \rom{1}), we presented a general framework to recover the mass profiles of galaxy clusters from X-ray and SZ data under the assumption that the gas is in hydrostatic equilibrium within the DM potential well. Here we apply our framework to recover the parameters of the Einasto functional form by fitting the X-COP data over a wide range in radius" (`einasto.tex` §1, l.61).
- "The methodology adopted to recover the mass profiles from X-ray surface brightness and spectroscopic temperature profiles and SZ pressure profiles is presented in detail in Paper \rom{1}." (§2.2, l.82)
- "For more details on the mass reconstruction technique and a thorough discussion of the associated systematic uncertainties, we refer the reader to Paper \rom{1}." (§2.2, l.103)
- **Hydrostatic equilibrium validity:** "The validity of the assumption of hydrostatic equilibrium (HSE) in the case of the X-COP clusters was discussed in detail in \citet{ettori19,eckert19} and in Paper \rom{1}." (§2.2, l.80)
- **Einasto compared with the non-parametric method:** "In Paper \rom{1} we showed that the Einasto model provides a good representation of the data at hand and closely follows the results obtained with a non-parametric technique that makes no assumption on the shape of the mass profile." (§2.2, l.129)
- **BCG stellar masses:** "The black stars show the measured BCG stellar masses within the same aperture in X-COP clusters (see Paper \rom{1})." (Fig. 3 caption, l.248). Also "compared them with the stellar masses of the BCGs in X-COP clusters \citep[see Paper \rom{1}]{loubser20}" (App. B, l.263).

**Cosmology:** "Throughout the paper, we assume a \emph{Planck} 2015 $\Lambda$CDM cosmology with $\Omega_m=0.308$, $\Omega_\Lambda=0.692$ and $H_0=67.8$ km/s/Mpc" (l.61). Paper I l.56 states the same H_0 and Ω_m (it gives no Ω_Λ). The cosmology is therefore the same.

**What Paper II does differently.** Paper II does not flag these itself; I identified them by comparison with Paper I.

- **Parametrisation.** Paper II: "Following \citet{ettori19}, rather than fitting for the characteristic density $\rho_s$ we optimise for the unitless normalisation $c$ … with $\Delta=200$ … we optimise for $\mu\equiv1/\alpha$ … our model includes four free parameters: the scale radius $r_{s}$, the normalisation $c$, the inverse $\mu$ … and the integration constant $P_0$" (l.105–111). Paper I instead says: "Instead of the scale radius $r_s$ and density normalization $\rho_s$ we optimize for the overdensity radius $R_{200}$ and the concentration $c_{200}=R_{200}/r_{s}$ … a similar description of the priors on the Einasto model is provided in Paper \rom{2}" (`hydromass.tex` l.190).
- **Mass fitted.** Paper II fits the total mass only: "in this paper we fitted an Einasto profile to the total gravitational field" (l.263). Paper I additionally decomposes the mass into baryons and the dark-matter term for 5 systems (`hydromass.tex` l.402).
- **Radial range.** Paper II gives a per-cluster fitting range in units of R_200 (Table 2). Paper I quotes "$[0.01-2]R_{500}$" (`hydromass.tex` l.512).
- **Masses.** Paper II tabulates "$M_{500,Einasto}$" (`tab2.tex` l.3). Paper II does not say how these relate to Paper I's M500 values.

## A. Sample

**1. Clusters analysed.** All 12: "We applied our mass profile reconstruction technique to all 12 X-COP systems." (§3.1, l.135). Table 2 lists A85, A644, A1644, A1795, A2029, A2142, A2255, A2319, A3158, A3266, RXC1825 and ZW1215 (`tab2.tex` l.7–18).

Sample definition: "a set of 12 massive galaxy clusters in the redshift range $0.04<z<0.1$. The sample contains the most significant SZ detections from the \emph{Planck} PSZ1 catalog \citep{psz1} with the exception of three highly perturbed systems for which the validity of a radially-averaged analysis cannot be guaranteed." (§2.1, l.67)

Complete baryon budget: **not identified in Paper II.** It says only: "Since measurements of the stellar mass profiles are currently available only for a subset of X-COP systems, in this paper we fitted an Einasto profile to the total gravitational field" (App. B, l.263). It does not name the subset. Paper I names it as A644, A1795, A2029, A2142 and A2319 (`hydromass.tex` l.402).

**2. Radial range.** Coverage: "For each cluster, a minimum of 5 \emph{XMM-Newton} pointings are available to cover uniformly the gas distribution at least out to $2\times R_{500}$." (l.67)

Fitting range per cluster, from Table 2 columns $R_{\rm min}$ and $R_{\rm max}$ in units of $R_{200}$ (`tab2.tex` l.3–4; column description l.143: "Lower and upper bounds of the fitting range as a fraction of $R_{200}$"):

| Cluster | R_min/R200 | R_max/R200 | tab2.tex line |
|---|---|---|---|
| A85 | 0.009 | 1.03 | 7 |
| A644 | 0.013 | 0.87 | 8 |
| A1644 | 0.010 | 1.30 | 9 |
| A1795 | 0.012 | 1.29 | 10 |
| A2029 | 0.012 | 1.13 | 11 |
| A2142 | 0.007 | 1.07 | 12 |
| A2255 | 0.028 | 1.24 | 13 |
| A2319 | 0.020 | 1.12 | 14 |
| A3158 | 0.011 | 1.06 | 15 |
| A3266 | 0.009 | 0.92 | 16 |
| RXC1825 | 0.013 | 1.19 | 17 |
| ZW1215 | 0.013 | 0.94 | 18 |

Also: "well represented by an Einasto model over more than two decades in radius" (l.225). Paper II does not tabulate R_200 in kpc.

**3. Exclusions and different treatment**

- **A2319:** "With the exception of one peculiar system for which there is clear evidence of a breakdown of hydrostatic equilibrium \citep[A2319,][]{ghirardini18}, the comparison of HSE masses with other techniques … indicate that the HSE assumption is valid at the $\lesssim20\%$ level out to $R_{200}$." (l.80)
- **α outliers:** "three systems (A2319, A644, and A2255) exhibiting larger values of $\alpha$ ($\gtrsim 0.5$)" (l.135). "A closer look at these systems shows that they are all unrelaxed systems with large deviations from spherical symmetry." (l.152)
- **Centroid shift:** "we used the [0.7-1.2] keV mosaic images of our systems to measure their centroid shift $w$ … we define $N$ apertures of decreasing radius $R_i$, with $R_1=R_{500}$, and determine the X-ray centroid $\Delta_i$ within each of them." (l.152). The equation is at l.155: $w = \frac{1}{R_{500}} \sqrt{\frac{1}{N-1}\sum_{i=1}^N (\Delta_i - \Delta_{500})^2}$. N and the aperture radii are not given.
- **Literature boundary:** "Most studies … place the boundary between relaxed and unrelaxed systems in the range $w=0.01-0.02$. We can see that all the quoted outliers exhibit values of $w$ greater than $0.02$, which shows that their X-ray morphology is unrelaxed." (l.161)
- **Exact selection criterion (body text):** "To avoid the potential impact of miscentering and hydrostatic bias, we selected a subsample of X-ray regular systems with $w<0.015$. This subsample excludes four objects with high centroid shifts, for which the offset between the X-ray peak and the bottom of the gravitational potential may be large and thus the value of $\alpha$ may be unreliable." (§3.1, l.163)
- **Figure 2 caption, which conflicts:** "the magenta curve shows the fit to the ``unperturbed'' subsample with $w<0.0015$." (l.148). See Doubts.
- **Conclusion:** "a few outliers with $\alpha\gtrsim 0.5$, all of which appear morphologically disturbed, as indicated by a large centroid shift … The subset of 8 X-ray regular systems with low centroid shift" (l.227).
- **Which four are excluded:** the paper does not name them. My inference from Table 2, where w is in units of 10⁻³, is A644 (20.97), A2255 (31.40), A2319 (33.08) and A3266 (30.84). These are the only values above 15×10⁻³. A1644 (13.76) is kept.
- **Reasons given:** "First, the validity of the hydrostatic equilibrium assumption in unrelaxed systems is unclear … Second, the position of the X-ray centroid may not coincide with the bottom of the potential well … In case our profiles are miscentered … we expect the reconstructed mass profiles to be substantially flatter than the true profiles, which would bias the reconstructed values of $\alpha$ towards high values." (l.161)

## B. g_obs

**4. How the total mass is obtained**

- **Only method used in Paper II: Einasto forward fit through hydrostatic equilibrium.** HSE equation: $\frac{dP_{\rm gas}}{dr} = - \rho_{\rm gas}\frac{GM(<r)}{r^2}$ (l.77). Einasto form at l.87.
- "The density profile is integrated numerically over the volume to determine the cumulative model mass as a function of radius, $M_{\rm mod}(<r)$. The gas density profile is described as a linear combination of King functions \citep{eckert20} and fitted jointly to the X-ray surface brightness profile. The hydrostatic equilibrium equation … is then integrated to predict the 3D pressure profile" (l.91). The pressure equation is at l.94.
- "the model pressure is projected along the line of sight and convolved with the instrumental PSF to predict the expected spectroscopic temperature profile." (l.103)
- **Sampler:** "No U-Turn Sampler (NUTS) as implemented in \texttt{PyMC3} … Four independent chains … each with 1,000 tuning steps and 1,000 output samples." (l.129)
- **Code features:** "non-parametric gas density deprojection, PSF convolution, spectroscopic temperature weights, and profile covariance matrices" (l.82).
- **Non-parametric log-normal mixture:** not used or presented in Paper II. It is mentioned only by reference: "closely follows the results obtained with a non-parametric technique that makes no assumption on the shape of the mass profile" (l.129).

**5. Reconstructions presented**

- **Einasto (total mass, all 12 clusters):** Table 2 (`tab2.tex`). Columns: "$M_{500,Einasto}$ [$10^{14} M_\odot$], $r_{s}$ [kpc], $\rho_{s}$ [$10^{-27}$ g/cm$^3$], $\mu$, $w$ [$10^{-3}$], $R_{\rm min}$, $R_{\rm max}$ [$R_{200}$]" (l.3–4). Column description: "Value of $M_{500}$ and uncertainty from the best-fit Einasto model; Parameter values and uncertainties for the Einasto parameters $r_s$, $\rho_s$, and $\mu=1/\alpha$" (`einasto.tex` l.142).
  - The fitted normalisation c and the fitted P_0 are **not tabulated**.
  - Per-cluster α is shown only in Fig. 2 (`alpha_measurements_nooutl.pdf`); it is not tabulated beyond μ.
- **Einasto priors:** Table 1, "Normal priors on the Einasto fit parameters" (l.114–125):

  | Parameter | Mean | σ | Min | Max |
  |---|---|---|---|---|
  | $r_s$ [kpc] | 700 | 300 | 100 | 3000 |
  | $c$ | 1.8 | 1.5 | 0 | 10 |
  | $\mu$ | 5 | 3 | 0.2 | 20 |
  | $P_0$ | $P_m$ | $dP_m$ | $P_m-2dP_m$ | $P_m+2dP_m$ |

- **NFW, non-parametric, and any reconstruction with baryons subtracted:** not presented in Paper II.

**6. Input data**

- X-ray: "\emph{XMM-Newton} data were reduced in a homogeneous way \citep{ghirardini19,eckert19,ettori19} and the reduced data and thermodynamic profiles (gas density and spectroscopic temperature) are publicly available" (l.69).
- SZ: "\emph{Planck} SZ pressure profiles were derived for all systems following \citet{planck5} from the SZ signal reconstructed using the MILCA algorithm \citep{hurier13}." (l.69)
- Inputs to the fit: "X-ray surface brightness and spectroscopic temperature profiles and SZ pressure profiles" (l.82).

**7. Spherical (3D) masses, and at which radii**

- The model is spherical and 3D: the cumulative model mass $M_{\rm mod}(<r)$ is obtained by volume integration (l.91), and "our results are mildly affected by the assumption of spherical symmetry \citep{buote12}" (l.129).
- The only tabulated mass is $M_{500}$ (Table 2). Profiles at other radii are not tabulated; they follow from the Einasto parameters.

**8. Corrections:** none applied. Masses are hydrostatic, with no non-thermal pressure correction. The effect of non-thermal pressure is only tested on a fiducial cluster in Appendix A (l.252–258); see D2.

## C. g_bar

Paper II computes no g_bar.

- **9. Gas:** gas density is "a linear combination of King functions \citep{eckert20} and fitted jointly to the X-ray surface brightness profile" (l.91). It is used only inside the HSE fit. No gas mass profile or gas mass is reported.
- **10. BCG:** used only as a check. "we determined the stellar masses of the BCGs in the simulation runs and compared them with the stellar masses of the BCGs in X-COP clusters \citep[see Paper \rom{1}]{loubser20}. … BCG stellar masses within 100 kpc radius" (l.263). Paper II does not state the method (MGE or Jeans), the M/L, its source, or whether the mass is 3D.
- **11. Satellites:** not mentioned.
- **12. Intracluster light:** not mentioned.
- **13. Other baryons:** none. The simulation comparison uses "gas + stars" in BAHAMAS (l.263), but that refers to simulations, not data.
- **14. g_bar as a 3D enclosed-mass acceleration:** not applicable; Paper II has no g_bar.

## D. Uncertainties

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | Provided by paper or data? |
|---|---|---|---|---|---|---|---|
| E1 | Statistical posterior on Einasto parameters and M500 | "Parameter values and uncertainties for the Einasto parameters $r_s$, $\rho_s$, and $\mu=1/\alpha$"; "in spite of the substantial covariance between the parameters the data at hand are of sufficient quality to determine … $\mu$ with good precision" | l.142; l.135; values in `tab2.tex` l.7–18 | Per cluster, asymmetric (e.g. A1795 $M_{500}=4.36_{-0.10}^{+0.12}$); confidence level not stated | system (parameter-level) | g_obs | Marginal errors in Table 2. Parameter covariance is shown only for A1795 (Fig. 1 corner plot, l.100). No radial covariance. |
| E2 | Hydrostatic bias / non-thermal pressure | "the HSE assumption is valid at the $\lesssim20\%$ level out to $R_{200}$"; "the HSE assumption typically overestimates $\alpha$ by $2-8\%$ … corresponding to differences of 0.01 for $\alpha_{\rm True}=0.18$" | l.80; App. A l.258 | ≲20% on mass (out to R200); 2–8% on α | point in principle ("non-uniform in the cluster's volume", l.252); stated as a bound for the sample | g_obs | Not provided. No correction applied. Tested only on a fiducial cluster with Nelson+14 and Angelinelli+20 non-thermal pressure profiles. |
| E3 | Breakdown of HSE in A2319 | "one peculiar system for which there is clear evidence of a breakdown of hydrostatic equilibrium \citep[A2319,][]{ghirardini18}" | l.80 | not stated | system | g_obs | Not provided |
| E4 | Miscentering in unrelaxed clusters | "we expect the reconstructed mass profiles to be substantially flatter than the true profiles, which would bias the reconstructed values of $\alpha$ towards high values" | l.161; also l.195 | not stated | system | g_obs | Not provided. Handled by excluding w ≥ 0.015. |
| E5 | Reconstruction accuracy on mocks | "the code was found to reproduce the input mass profile with an accuracy better than 3\%" | l.82 | <3% | dataset (method level) | g_obs | Not provided per cluster |
| E6 | Spherical symmetry assumption | "our results are mildly affected by the assumption of spherical symmetry \citep{buote12}" | l.129 | not stated ("mildly") | not stated | g_obs | Not provided |
| E7 | Prior choice on Einasto parameters | "the posterior distributions are much narrower than the prior … the results of this paper weakly depend on the choice of the prior. Using uniform priors over the range given in Table \ref{tab:priors} also returns similar results and uncertainties for all parameters." | l.111 | not quantified | system | g_obs | Priors are given in Table 1 |
| E8 | Outer pressure boundary P_0 | "for $P_0$ we set a Gaussian prior with mean and standard deviation equal to the outermost SZ pressure value and its uncertainty" | l.111 | not stated | system | g_obs | Fitted P_0 values not tabulated |
| E9 | BCG stellar mass (effect on fitted α) | "modified the stellar mass of the BCG by a conservative factor of 2 … For an input value $\alpha=0.18$ the retrieved value of $\alpha$ changes by $\pm0.02$" | App. B l.265 | factor 2 in BCG mass gives ±0.02 in α | system (fiducial test) | concerns baryon modelling; Paper II has no g_bar | Not provided |
| E10 | Choice of model (Einasto compared with non-parametric) | "closely follows the results obtained with a non-parametric technique" | l.129 | not quantified in Paper II | not stated | g_obs | Not in Paper II |
| E11 | Intrinsic population scatter of α (a population statistic, not a measurement error) | "$\langle\alpha\rangle=0.22\pm0.04$, with a substantial intrinsic scatter $\sigma_{\alpha}=0.14_{-0.05}^{+0.10}$"; regular subsample "$\langle\alpha_{\rm rel}\rangle=0.19\pm0.03$ … $\sigma_{\alpha, rel}=0.06_{-0.03}^{+0.04}$" | l.152; l.163 | as quoted | dataset | g_obs shape | Stated in text |
| E12 | Calibration (X-ray or SZ) | not discussed | none | — | — | — | Not stated |

**Radial correlations:** not discussed or provided. The only correlation material is the parameter covariance, "the posterior distributions of the fitted Einasto model parameters and the covariance between them" (Fig. 1 caption, l.100), for A1795 only, plus the code's use of input "profile covariance matrices" (l.82).

The following are simulation-side uncertainties, not on g_obs or g_bar, and are recorded only: AGN feedback energy threshold (l.191), the interpolation method between σ/m values (l.210), and statistical errors of the simulation means "much smaller than the observational errors" (l.210).

## E. Radial acceleration relation

**15–17.** None in Paper II. No g_obs against g_bar plot, no binning, no fitted relation, and no scatter statement about a radial acceleration relation. The only comparison with galaxies is a statement of the CDM expectation: "Their distribution is well represented by an Einasto profile with shape parameter $\alpha\approx0.18$, in the smallest dwarf galaxies or the most massive galaxy clusters alike." (abstract, l.45)

The fitted relations Paper II does publish concern α and σ/m in simulations, recorded as stated: "$\alpha_0=0.178$, $\alpha_1=0.20$, and $\gamma=0.63$" (l.203). The paper's stated conclusion: "$\sigma/m < 0.19 \, {\rm cm}^2/{\rm g,~at~} v_{\mathrm{DM}}\! \approx\!1,000$ (95\% confidence level)" (l.207). These are recorded as published, not evaluated.

## F. Data availability

**18.** Two items are named:

- Reduced data and thermodynamic profiles: "the reduced data and thermodynamic profiles (gas density and spectroscopic temperature) are publicly available\footnote{\href{https://dominiqueeckert.wixsite.com/xcop}{…}}" (l.69).
- Code: "The code is publicly available in the form of the Python package \texttt{hydromass}\footnote{\href{https://github.com/domeckert/hydromass}{…}}" (l.82).

No licence or terms are stated, and no release of mass profiles, g_obs or g_bar tables is mentioned.

**19.** Nothing is said about released g_obs or g_bar tables.

**20.** The only 12-cluster mass product is Table 2: Einasto M500 and parameters. Its confidence level is not stated.

## G. Differences from Ettori et al. 2019 and the 2019 archive

- **Parametrisation:** "Following \citet{ettori19}, rather than fitting for the characteristic density $\rho_s$ we optimise for the unitless normalisation $c$" (l.105).
- **Cored models in 2019:** "Incidentally, in \citet{ettori19} the mass profiles of these same systems were found to be better represented by models exhibiting a central core (Burkert, non-singular isothermal sphere)." (l.152)
- **Per-cluster masses:** Table 2 gives $M_{500,Einasto}$ for all 12 clusters (`tab2.tex` l.7–18; e.g. A85 $6.35_{-0.08}^{+0.08}$, A2142 $9.41_{-0.19}^{+0.20}$, in $10^{14} M_\odot$).
- **Not given in Paper II:** R500, R200 and per-cluster redshifts. No statement compares the Table 2 masses with Ettori 2019 or with the 2019 archive.

---

## Not stated

I searched the whole of `einasto.tex`, `tab2.tex` and `einasto.bbl`, using grep for: Paper, non-param, NFW, baryon, gas mass, stellar, ICL/intracluster, satellite, R500/R200, lensing, RAR, acceleration, covariance and systematic. The following are not stated:

- Any g_bar, gas mass profile, satellite mass, ICL, or BCG method, M/L or IMF.
- NFW or non-parametric results.
- A radial acceleration relation.
- Radial covariance.
- The confidence level of the Table 2 errors (Fig. 1 refers to "$1\sigma$ error" only for the A1795 plot, l.129).
- R500 or R200 values, per-cluster redshifts, and fitted c and P_0 values.
- Names of the four excluded clusters, N and the aperture radii used for w, and the uncertainty method behind the w errors.
- Calibration systematics.
- A licence for the code or data.
- Any release of mass tables.
- A list of which clusters have stellar mass profiles.
- Any comparison of the Table 2 M500 values with Paper I or Ettori 2019.
- No bibitem for Paper I exists in `einasto.bbl`; it is cited only as text (l.61).

## Doubts

1. **Selection threshold conflict.** The body text says $w<0.015$ (l.163); the Fig. 2 caption says $w<0.0015$ (l.148). With Table 2's w in units of 10⁻³, only 0.015 gives "four objects" excluded and "8 X-ray regular systems" kept (l.227). The 0.0015 in the caption looks like a typo, but that is my inference. The published A&A version was not checked.
2. **Identity of the four excluded clusters** (A644, A2255, A2319, A3266) is my inference from Table 2. A3266 is excluded by w, but its α is not among the stated outliers (μ = 6.45 in Table 2).
3. **Scatter of the regular subsample is quoted three ways:**
   - abstract: "$\sigma_{\alpha}=0.06$" (l.45);
   - §3.1: "$0.06_{-0.03}^{+0.04}$" (l.163);
   - Conclusion: "$0.06_{-0.03}^{+0.05}$" (l.227).
4. **Table 2 lists ρ_s, but the fit is in c.** Table 2 columns are $\rho_s$ in units of 10⁻²⁷ g/cm³, while the fit is done in c (l.105–111). I assume ρ_s was derived through the l.108 relation. That relation uses the NFW-like factor $c^3/(\log(1+c)-c/(1+c))$, and "log" presumably means the natural log. This is recorded as written, not checked.
5. **Paper I and Paper II use different parametrisations** for the same Einasto form: (R200, c200, α) in Paper I l.190 against (r_s, c, μ, Δ=200) in Paper II. Whether the 12 Einasto fits are identical runs is not stated.
6. **Prior bounds.** Table 1 is titled "Normal priors" but also lists Min and Max. Whether these bound truncated normals is not stated explicitly. l.111 mentions uniform priors over that range as an alternative.
7. **Commented-out earlier draft text** in the source gives different numbers: "$\sigma/m < 0.14$ cm$^2$/g (90\% confidence level)" (l.47, commented out). It is not part of the published text, but it is in the e-print.
8. **Collision-velocity wording.** The abstract says "$v_\mathrm{DM-DM}\sim1,000$ km/s" (l.45); l.207 gives "$v_{\mathrm{DM}}\approx1,000$" with no unit.
9. **Applicability of the HSE bound.** l.80 states that HSE is valid at "≲20%" while excepting A2319, and also cites Ettori 2019 and Eckert 2019. Whether the bound applies to the Paper II fits specifically is not stated.
10. **Reference to the wrong panel.** l.265 says "the analysis presented in the left-hand panel of Fig. \ref{fig:syst}" about the BCG. The BCG comparison is in the right-hand panel (caption l.248), so this looks like an internal panel-reference error.

**Next step:** compare this with Reader B's report. The main points to settle at source are the w threshold (Doubt 1), the excluded-cluster set (Doubt 2), and the confidence level of the Table 2 errors (Not stated). For all g_bar items, the reconciliation should rely on Paper I, because Paper II supplies none.