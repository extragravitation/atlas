# X-COP uncertainty terms affecting g_obs and g_bar: independent reading (Reader B)

**Reader:** Reader B
**Date:** 2026-11-02
**Working directory:** `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/readerB`

## Sources read

Each e-print came from `https://arxiv.org/e-print/<id>`. The version is the latest one listed on the arXiv abstract page on 2026-11-02, which is what the e-print endpoint serves.

| arXiv id | Version | Main .tex | SHA-256 of e-print |
|---|---|---|---|
| 1805.00035 (Ettori+2019) | v3 | `mass_xcop.tex` (+ `m_syst.tex`, `m_over.tex`) | `3bc07668cc877920ac05ca955c88d80d15aad19a11d9fd7286e25c396d658733` |
| 1805.00034 (Eckert+2019) | v2 | `NTpressure.tex` (+ `table2.tex`) | `766db09383ff70125677ca0872d6d4b2865e32637cc133c97213222be8427bf0` |
| 1805.00042 (Ghirardini+2019) | v2 | `XCOP_thermo.tex` | `9edb7d25de34b769d7c8591db38bfbc7325c93f0d83d9569a774396c3d8bfa38` |
| 2007.01084 (Ghizzardi+2021) | v1 | `xcop-metallicity.tex` | `88c8e91c036077e2ca660cd029943d576df1462daae914d3e58aa24169c5a9e8` |
| 1309.3565 (Gonzalez+2013; id taken from the eprint field in 2007.01084 `biblio.bib`) | v1 | `ms.tex` | `e582a681d6656c8752ef3d5057701be9087ff26f2c4e5d6f846a2e3895ac15a3` |
| astro-ph/0402308 (Lin+2004) | v3 | `arxiv.tex` | `96e3dc16c07c2a979539684d317868b46e2f8180a988db795f2b4044e19b4d8c` |
| 1708.02954 (Ghirardini+2018, A2319) | v2 | `X-COP-A2319.tex` | `ade2df04fe4305c649bde1c75900310bd97d1cc1d15a4b80d401e2f36105434b` |

## Archive

- File: `allfiles.tar.gz`. Its SHA-256 was re-verified as `0edf5038…0d94`, which matches the brief.
- I listed every member (271 entries). There is no README or other documentation file in the archive.
- I opened these 31 members, reading their headers and values:
  - `<cl>/<cl>_hydro_mass.fits` for all 12 clusters
  - `<cl>/<cl>_fgas_profile.fits` for all 12 clusters
  - `<cl>/<cl>_mstar.fits` for A85, A644, A1795, A2029, A2142, A2319 and ZW1215
- I did not open the `*_Y-PROF-COVMAT_P-PROF-COVMAT.20170830.fits` files. I only saw their names in the listing.
- The Atlas repository files `SOURCE.md` and `convert.py` were read for context only.

## Terms

Abbreviations used in the location column:

| Abbreviation | File |
|---|---|
| E19 | `mass_xcop.tex` |
| Ek19 | `NTpressure.tex` |
| G19 | `XCOP_thermo.tex` |
| Gz | `xcop-metallicity.tex` |
| Go13 | `ms.tex` |
| L04 | `arxiv.tex` |
| G18 | `X-COP-A2319.tex` |

| ID | Term | Verbatim quote (short) | Location | Size as stated | Scale | Moves | In release? |
|---|---|---|---|---|---|---|---|
| X1 | Statistical error on the hydrostatic (forward) mass | "Unless mentioned otherwise, the quoted errors are statistical uncertainties at the $1 \sigma$ confidence level." / "the errors as half the difference between the 84th and 16th percentiles" / forward: "Errors are estimated through a Monte Carlo process." | E19 §1 l.113; §3 l.226–227; G18 §3.4 l.606 | "relative (statistical) median error of $3$ \% at $R_{500}$ and $6$\% at $R_{200}$" (E19 abstract l.48). l.304–305 gives the same kind of figures for backward NFW only ("statistical only… $3, 4, 2$\%; $4, 5, 2$\%; $6, 7, 3$\%"). No separate figure is stated for the forward method. | point as tabulated. It comes from a smooth functional fit, so it is correlated across radii (inference). No covariance is released. | g_obs | `hydro_mass.fits` ext HYDRO_MASS, `EM_FORW`. The header gives no definition of the column. |
| X2 | Planck pressure covariance and intrinsic-scatter nuisance σ_T,int in the likelihood | "(ii) an intrinsic scatter $\sigma_{T,int}$ to account for any tension between X-ray and SZ measurements, and (iii) the covariance matrix $\Sigma_{tot}$ among the data in the \planck\ pressure profile" | E19 §3 l.208–209; G18 App. D l.1219–1286 | σ_T,int per cluster is tabulated for the backward models only (NFW: 0.001–0.079, E19 Table A.1 l.681–693). Not stated for forward. | system (one σ_int per cluster; covariance within a cluster) | g_obs | Marginalised into `EM_FORW` (inference). The covariance files exist in the archive (`*_Y-PROF-COVMAT_P-PROF-COVMAT*.fits`) but were not opened. |
| X3 | X-ray background subtraction systematic | "A systematic error of 5\% of the background value was thus added in quadrature to all our surface brightness measurements." For A3266: "included a systematic error of 30\% in quadrature" | G19 §5.1 l.653; §2.2.4 l.191 | 5% of the background level (A3266: 30%). "At $R_{200}$ the systematic uncertainty is typically 20\% or less of the measured signal" (l.653). G18 A2319 total: "4.18\% and 8.5\% at $R_{500}$ and $R_{200}$" (G18 l.646). | system (one background level per cluster, added at every radius) | both | Folded into the surface-brightness errors, so implicitly in `EM_FORW` and `MGAS_LO`/`MGAS_HI` (inference). Not separable. |
| X4 | Spectral-temperature method systematic | "we estimate the systematic error using the standard deviation of the values measured with all the different methods. This error is then added, in quadrature, to the statistical error" | G18 §4.2.1 l.466–468 (A2319 only) | "between 1.4\% and 9.1\%, apart from the outermost radial point where we measure a value of 19\%" (A2319). Whether this was applied to the 12-cluster X-COP masses: not stated in E19. | point | g_obs | Unknown (see Doubts). |
| X5 | X-ray temperature calibration (XMM-Newton effective area) | "If \emph{Chandra} temperatures are correct, our masses should be underestimated by $\sim15\%$" | Ek19 §5.1 l.262; also G19 §5.1 l.657 | ~15% on temperature and mass. G19 reports X-ray/SZ pressure agreement, except ZW1215, where "the pressure measured by \xmm\ actually {exceeds} the SZ pressure by $\sim20\%$" (l.657). | dataset | g_obs | no |
| X6 | Gas-density cross-calibration | "found an exquisite agreement between the two missions at the level of 2.5\%" | Ek19 §5.1 l.262 | 2.5% | dataset | g_bar (and g_obs through the density) | no |
| X7 | Mass reconstruction method / mass model (forward vs backward NFW, with and without SZ) | "the use of the {forward} method (with or without SZ profiles) introduces a small systematic error … median difference of about 4\% at $R_{500}$, and $<$2\% (1st-3rd quartile: -5.4 / +8.1 \%) at $R_{200}$" | E19 §3.3 l.414–415; Table 2 l.429–435 (`m_syst.tex`) | Forw vs NFW: $-4.7\,(-10.9/-0.5)$% at R500; $+1.2\,(-5.4/+8.1)$% at R200. Forw (no SZ): $-4.2$, $+1.3$. ISO/BUR up to "about 25\%" (l.421). Abstract: "of the order of 5\%" (l.50). | system (one offset per cluster; only the sample distribution is given) | g_obs | Not as an error. `hydro_mass.fits` carries the alternative profiles `M_NFW`/`EM_NFW`, `M_EIN`, `M_ISO`, `M_BUR`, and `EM_HER` (no `M_HER` column). |
| X8 | Non-thermal pressure / hydrostatic bias | "We find a median non-thermal pressure of $5.9_{-3.3}^{+2.9}\%$ and $10.5_{-5.5}^{+4.3}\%$ at $R_{500}$ and $R_{200}$" / "median bias $M_{\rm 500,HSE}/M_{\rm 500,tot}=0.94\pm0.04$" | Ek19 §4.1 l.211; §4.3 l.240; per cluster in `table2.tex` l.8–19 | Per-cluster α at R500 and R200 (e.g. A2319 $43.6$%, $52.3$%; several are upper limits at 90% CL). The mean could rise "from 9\% to 13\% at $R_{500}$" with the missing clusters (l.219). | system (parametric α(r) per cluster, which also varies with radius) | g_obs | no |
| X9 | Other departures from HSE and from sphericity | "this budget of the systematic uncertainties does not include … non-thermal contribution … departures from the hydrostatic equilibrium … or the violation of the assumed sphericity … bias the total mass estimates higher (by 10--30\%) at $r>R_{500}$" | E19 §3.3 l.445–450; Conclusions l.606–610 | 10–30% at r > R500 (l.449), versus "a further 10--20\%" (l.610) | system | g_obs (as stated) | no |
| X10 | Intrinsic scatter of hydrostatic masses about the true mass | "we can estimate the intrinsic scatter of the hydrostatic masses, $\sigma_{M_\text{HE}\|M}=0.15\pm0.08$" | E19 §3.2 l.391–393; abstract l.53 ("0.15 dex") | 0.15 ± 0.08 (dex, per l.53 and l.393) | system | g_obs | no |
| X11 | Relativistic SZ correction | "relativistic corrections could lead to an underestimate of the integrated SZ signal up to 15\% for the hottest clusters … For typical temperatures of $\sim5$ keV at $R_{500}$ and beyond the expected effect is less than 5\%" | G19 §5.1 l.655 | <5% at ≥R500; up to 15% integrated | system (temperature-dependent) | g_obs | no |
| X12 | Gas clumping (residual after azimuthal-median correction) | "introduces a systematic uncertainty of 5-10\% on the true gas mass at $R_{200}$ … Residual clumping … we expect the residual effect to be less than a few percent" | Ek19 §5.1 l.261; method G19 l.189 | 5–10% at R200 if uncorrected; residual "less than a few percent", positive bias | system | g_bar (effect on g_obs not stated) | no |
| X13 | Gas-mass reconstruction accuracy | "measurements of $M_{\rm gas}$ are accurate down to the level of a few percent" | Ek19 §5.1 l.261 | "a few percent" | dataset | g_bar | no |
| X14 | Statistical error on gas mass | Header: "COMMENT Gas mass and hydrostatic gas fraction profile" (no error definition). Paper: "typical statistical uncertainties in $f_{\rm gas,HSE}$ are $\sim5\%$ at $R_{500}$" | `fgas_profile.fits` header; Ek19 §2.2 l.84 | Release values: MGAS_HI/MGAS ≈ 0.3–0.9% at R500. Larger in the innermost row (up to 100% for RXC1825 and 93% for ZW1215). | point as tabulated; correlated (comes from integrating a model profile; inference) | g_bar | `fgas_profile.fits` ext FGAS, `MGAS_LO`/`MGAS_HI`. These are offsets, not bounds (inferred, see Doubts). |
| X15 | Mean molecular weight / composition / metallicity assumption | "$\mu \approx (2 X +0.75 Y +0.56 Z)^{-1} \approx 0.6$ … for a typical metallicity of 0.3 times the solar abundance"; "$n_{\rm e} + n_{\rm p} \approx 1.83 n_{\rm e}$" | E19 §3 l.173, l.182–186 | Effect not stated. Values differ by paper: Ek19 l.84 "$n_e=1.17n_p$ … $\mu=0.61$"; Gz l.529 "$n_{\rm gas}= … 2.21 n_{\rm H}$". | dataset | both | no |
| X16 | Helium sedimentation | "any possible rise in the He abundance by up to about 50 per cent over the cosmic value … induce a bias of a few per cent restricted to the inner ($<R_{2500}$) cluster regions" | Ek19 §5.1 l.263 | a few % inside R2500 | system | both | no |
| X17 | Cosmology (H0, Ωm) | "we adopt the cosmological parameters $H_0=70$ … $\Omega_{\rm m} = … 0.3$" / "the results have a very mild dependence on the adopted cosmology" | E19 §1 l.120–121; Ek19 §1 l.54 | Not stated quantitatively | dataset | both | no |
| X18 | Redshift / distance | "Cluster name, redshift, and signal-to-noise ratio from the PSZ1 catalogue"; emission measure normalisation $\propto 1/[d_A(1+z)]^2$ | G19 Table 1 note l.145; eq. l.199–201 | No redshift error stated; distance effect not stated | system | both | Value only: header `REDSHIFT`, no error |
| X19 | R500 / M500 statistical error (enters the modelled-star normalisation via M500 and R200, and the radius scale) | "ERR_R500 … Statistical uncertainty on NFW R500"; Table 1 "$1.235 \pm 0.013$ … $5.65 \pm 0.18$" | header of all three file types; E19 Table 1 l.313–325 | e.g. A85: ±13 kpc, ±0.178e14 M☉; 1–12% across clusters | system | g_bar (modelled stars) | Header keywords `ERR_R500`, `ERR_M500`. R200 error only in E19 Table 1. |
| X20 | Stellar mass, statistical (flux bootstrap) | "we bootstrap the flux measurements within their uncertainties, and perform 100 perturbations for each galaxy" | Gz §5.1 l.712, l.714 | Release (my reading): mean offset / MSTAR ≈ 4–27% at 0.3–1 R500 | point (cumulative, so correlated across radii: inference) | g_bar | `mstar.fits` MSTAR_RAW `MSTAR_LO`/`MSTAR_HI` (offsets). Header: "The quoted uncertainties are the statistical uncertainties and the cosmic variance (CV) separately." |
| X21 | Stellar mass, field-to-field ("cosmic") variance of the background subtraction | "a systematic uncertainty related to how representative the reference field is … substantial uncertainty due to field-to-field (often called "cosmic") variance" | Gz §5.1 l.713–714 | Release: CV offset / MSTAR ≈ 2–14% | system (one subtraction per cluster; the same COSMOS reference for all clusters) | g_bar | MSTAR_RAW `MSTAR_CV_LO`/`MSTAR_CV_HI` |
| X22 | Stellar "total uncertainty" as released | "COMMENT Smoothed stellar mass profile used in Ghizzardi et al. 2020 and total uncertainties." | `mstar.fits` ext MSTAR_SMOOTHED header | Bounds. Inferred to equal stat ⊕ CV (see Doubts). | as X20 and X21 combined | g_bar | MSTAR_SMOOTHED `MSTAR_LO`/`MSTAR_HI` (bounds) |
| X23 | Projected vs spherical stellar mass | "the cumulative stellar masses … are derived by integrating within a projected radius … 75$\%$ of the mass obtained integrating along the line of sight lies within the sphere with radius $R_{500}$. We therefore multiply the stellar mass estimates by a factor 0.75." | Gz §5.1 l.715 | Factor 0.75 at R500 (gNFW, c = 0.72, α = 1.64). Other radii: not stated. | system (assumed common shape) | g_bar | Correction not applied in the released profiles (inference, see Doubts) |
| X24 | Stellar-mass modelling systematics (SPS, SFH, dust, M/L) | "assuming a systematic discrepancy of $50\%-60\%$ between our measurements and those reported in C18 and L12 seems reasonable" / "we may be underestimating stellar masses by as much as 60\%" | Gz §5.2 l.782–783; §6.3 l.923 | 50–60% (direction: stars underestimated) | dataset | g_bar | no |
| X25 | IMF | "assuming a \citet{salpeter55}-diet … IMF … provides values that exceed by a factor $ \sim 2$ those obtained using a \citet{chabrier03}" (Chabrier is assumed, l.693) | Gz §5.2 l.749 | factor ~2 | dataset | g_bar | no |
| X26 | Intracluster light (excluded from measured stars) | "the BCG is included in our mass computation, while the Intra-Cluster Light … is not." / "about 10\% … about 50\% … We adopt a conservative approach and assume the larger contribution of 50\%" | Gz l.711; §6.3 l.928–930; Ek19 l.146 | 10–50% of total optical emission (Gz). "ICL can account for $\sim20-30\%$ … of the total stellar mass" (Ek19 l.146). | dataset | g_bar | no (excluded) |
| X27 | Galaxy mass limit | "If, instead, we only consider galaxies with $M_{\star}>10^{9}\,\mathrm{M_{\odot}}$, this would account for more than 98\% of the stellar mass" | Gz l.710 (footnote) | <2% missing | dataset | g_bar | no |
| X28 | Centring | "The impact of how these profiles are centred is generally small (the centres differ by at most 2\% of $R_{500}$)." | Gz §5.1 l.700 | centres ≤2% R500 apart; mass effect not quantified | system | g_bar | no |
| X29 | Modelled stars: scatter of the stellar-to-gas relation | "This relation is tight, with an implied intrinsic scatter of 12\%." / "The 17\% scatter about the best fit relation can be explained by … observational uncertainties and 12\% intrinsic scatter" | Go13 abstract l.111–112; §4 l.812–814 | 12% intrinsic (17% total) | system | g_bar | no |
| X30 | Modelled stars: relation parameter errors | "$M_{\star,3D}/M_{gas}$ & $3.90\pm0.02\times10^{-1}$ & $-0.84\pm0.04$" (prescription in E19 l.564: "0.39 … ^{-0.84}") | Go13 Table "Derived $M_j-$\mfive\ Relations" l.1035 | ±0.002 on norm, ±0.04 on slope. Planck-cosmology version: $3.87\pm0.02$, $-0.81\pm0.05$ (l.1755). | dataset | g_bar | no |
| X31 | Modelled stars: Gonzalez M/L and luminosity systematics | "the largest systematic uncertainties in our conversion to stellar mass are clearly defined and impact our results at a level of $15$\%" / faint-end slope "induces a 12\% uncertainty … $5-8$\% uncertainty in the total luminosity" | Go13 l.1257–1259; l.1086–1090 | 15%; 5–8% | dataset | g_bar | no |
| X32 | Modelled stars: galaxy concentration c = 2.9 (radial shape) | "The {\it galaxy} concentration is $c_g=2.90_{-0.22}^{+0.21}$" / "it is possible that the true galaxy distribution concentration is even smaller than 2.9" | L04 §3 l.362; §6 l.1400–1406. Used in E19 l.563 | +0.21/−0.22; possible bias Δc ≈ 0.15–0.35 ("scatter about 0.25"). Go13 l.1279–1286: c ≈ 2.6–3.7 gives "a few percent" in the projection fraction, "$\sim1-2$\%" on total stellar mass. | dataset | g_bar | no |
| X33 | Modelled stars: overall accuracy of the prescription for X-COP | "we measure a median $M_{\rm star}/ M_{\rm gas}$ of 0.09 (0.07--0.12 as 1st and 3rd quartile) at $R_{500}$" | E19 §5 l.565 | Accuracy not stated (the quartiles describe the sample spread, not an error) | system | g_bar | no |
| X34 | Overall mass and R500 accuracy (summary claim) | "show that our masses and the corresponding values of $R_{500}$ are accurate at the $10\%$ and $3\%$ level, respectively" | G19 §2.5 l.314 | 10% (mass), 3% (R500) | system | g_obs | no |

## Looked for and found "not stated"

- **Covariance or correlation of `EM_FORW` across radii.** Not stated in E19 (whole file), G18 §3.4 or App. D, or the hydro header. The only covariance mentioned is the Planck input covariance.
- **Whether `EM_FORW` (and `M_FORW`) is the "Forw" variant (with SZ) or "Forw (no SZ)".** Not stated in the hydro header or E19 Table 2.
- **Whether the temperature-systematic term of G18 (X4) was applied to the X-COP sample masses.** Not stated in E19 §3 or G19 §2.3 (spectral analysis).
- **Size of the μ or metallicity effect on M_gas or M_HSE.** E19 l.182–186, Ek19 l.84 and Gz l.529 give only the adopted values.
- **Redshift uncertainty.** G19 Table 1 note, E19 Table 1 and the headers give values only.
- **Explicit dependence of M_HSE, M_gas or M_star on distance or h.** Not stated in E19 l.115–121, Ek19 l.54 (qualitative only), G19 l.98, l.199–201, or Gz l.693 (luminosity distance used, no scaling stated). Go13 writes h70 macros (l.24–26) but I found no quoted scaling for its relation.
- **Absolute calibration of the Planck y / SZ pressure.** Not stated in G19 §2.4 or §5.1; G19 l.655 refers to Planck 2013 for further systematics.
- **Error definition of `MGAS_LO`/`MGAS_HI` and `EM_FORW` in the release.** No COMMENT, HISTORY or TCOMM cards in any header; no README in the archive.
- **Stellar-mass dependence on radius for the projection correction (X23) other than at R500.** Gz l.715 only.
- **Accuracy of the Ettori §5 prescription at radii other than R500, or for the X-COP mass range.** E19 l.563–565. Go13's fit covers "$M=1-5\times10^{14}$" (l.76).
- **Error on the X-COP M*/M_gas median of 0.09.** E19 l.565 gives quartiles only.

## Doubts and inferences

1. **`EM_FORW` content (inference).** The release does not define it. "Statistical, 1σ, half of the 16–84 interval" is my inference from E19 l.113 and l.226–227 (a general MCMC description) and G18 l.606. The relative size of `EM_FORW` in all 12 files:

   | Radius | EM_FORW / M_FORW |
   |---|---|
   | 30 kpc | 5–84% |
   | ~300 kpc | 1.4–10% |
   | ~1 Mpc | 1.9–5.8% |
   | 3000 kpc | 11–66% |

   The grid is 100 log-spaced radii (ratio 1.0476) from 30 to 3000 kpc. That runs past the data ranges shown in E19 Fig. A.1 (caption l.839–841), so the outer rows are functional-form extrapolation (inference). The forward fit uses smooth functional forms (G18 l.607), so errors at neighbouring radii must be strongly correlated, but no covariance is released (inference).

2. **`MGAS_LO`/`MGAS_HI` are offsets, not bounds (inference).** In all 12 files LO/MGAS is 0.003–0.21 and LO < MGAS everywhere. Bounds would make LO ≈ MGAS. At the innermost row, HI/MGAS is 1.003 (RXC1825) and 0.93 (ZW1215), which fits offsets. Whether they are 1σ is not stated.

3. **`MSTAR_SMOOTHED` total = stat ⊕ CV (inference).**
   - In MSTAR_RAW, `MSTAR_LO`/`HI` and `MSTAR_CV_LO`/`HI` are offsets (≪ MSTAR).
   - In MSTAR_SMOOTHED, `MSTAR_LO`/`HI` are bounds (LO ≤ MSTAR ≤ HI at every row, all 7 clusters) and nearly symmetric.
   - At 0.3, 0.6 and 1.0 R500, the smoothed half-width matches √(mean_stat² + mean_CV²) from RAW within about 0.1×10¹¹ M☉ in all 7 clusters. Examples: A1795 at R500, 3.73 vs 3.8 (smoothed lower) and 3.7 (upper), in 10¹¹ M☉; A2029 at R500, 6.38 vs 6.4.
   - Neither smoothed nor raw MSTAR is strictly monotonic for A85, A644, A1795 and ZW1215.

4. **The released stellar profiles appear to be projected (cylindrical), not spherical (inference, important for g_bar).** 0.75 × MSTAR_SMOOTHED at the Table 1 R500 reproduces Gz Table 2's M_star,500:

   | Cluster | 0.75 × MSTAR(R500) (10¹² M☉) | Gz Table 2 (10¹² M☉) |
   |---|---|---|
   | A1795 | 2.985 | 3.02 |
   | A2142 | 6.93 | 6.97 |
   | A2319 | 5.19 | 5.11 |
   | ZW1215 | 3.195 | 3.34 |
   | A2029 | 6.73 | 6.51 |
   | A85 | 2.21 | 2.10 |
   | A644 | 4.13 | 3.70 (off by 12%) |

   The Gz Table errors also equal about 0.75 × the smoothed half-width (A1795: 0.28 vs 0.75 × 0.38). Gz l.715 states the 0.75 correction was applied only to M_star,500. Neither header says "projected". If this inference holds, treating MSTAR as M(<r) inside a sphere overstates stars by about 1/0.75 at R500. The factor at other radii is not stated.

5. **Archive headers vs Ettori Table 1 (disagreement between sources).**
   - **A644:** header R500 = 1250, M500 = 5.9408, against 1.230 Mpc and 5.66 in E19, G19 and Ek19.
   - **A2029:** header z = 0.0766, R500 = 1414, M500 = 8.6511. E19 Table 1 gives 0.0773, 1.423 and 8.82. The header matches G19 Table 1 (l.131: 0.0766, 8.65, 1414) and Ek19 `table2.tex` l.10 (8.65).
   - **A2319:** header R500 = 1368, M500 = 7.6781, against E19 1.346 and 7.31. It matches G18's forward "$P_{SZ}$ + $T_{X}$, $\beta$ fixed" result, $7.7 \pm 0.4$ and $1368 \pm 26$ (G18 l.563).
   - **A2142:** header z = 0.09, against 0.0909.
   - These are the same three clusters as the Atlas `reproduction_mismatch` flag, plus the A2142 redshift.

6. **Released M_gas vs Gz Table 2 M_gas,500 (disagreement).** Log-interpolating the release MGAS at r/R500 = 1 (header R500) gives values 0–10% lower than Gz Table 2 for 11 of 12 clusters:

   | Release / Gz ratio | Clusters |
   |---|---|
   | 0.90–0.94 | A2255 0.90, A2029 0.91, RXC1825 0.91, A3158 0.92, A85 0.93, A1644 0.93, ZW1215 0.93, A1795 0.93 |
   | 0.95–0.97 | A2142 0.95, A644 0.96, A3266 0.97 |
   | ≈ 1.00 | A2319 1.00 |

   The release errors are about half of Gz's (e.g. A85 +0.030/−0.041 vs +0.09/−0.08 ×10¹³). I cannot attribute the difference. Composition conventions differ between papers (X15), and Gz cites its own derivation.

7. **One paper, two sizes.** E19 gives the HSE/non-thermal/sphericity range as 10–30% (l.449) and 10–20% (l.610).

8. **Units of σ_MHE|M.** The abstract (l.53) says "0.15 dex". l.393 equates 10% to σ < 0.043, which also implies log10 units.

9. **`hydro_mass.fits` has `EM_HER` but no `M_HER` column** (TTYPE12 = 'EM_HER ' in all 12 files).

10. **g_obs and g_bar errors are probably correlated (inference).** The same deprojected density enters both M_HSE (E19 eq. 1) and M_gas (Ek19 l.83–84). No source states this correlation.

11. **Modelled and measured stars are defined differently (from quotes).**
    - Go13 includes BCG+ICL (l.174–176, l.693).
    - Gz includes the BCG and excludes ICL (l.711).
    - Go13 uses dynamical M/L (l.655–666). A LaTeX comment in Gz l.752, which is not in the published text, says such M/L "might be biased high by up to 30\%".
    - E19's prescription gives a median M*/M_gas of 0.09 at R500 (l.565). Dividing the Gz Table 2 values gives about 0.02–0.05 for the 7 measured clusters (my arithmetic, e.g. A1795 3.02/69.2 = 0.044).
    - Go13's fiducial cosmology is WMAP7 with "$H_0=70.2$" (l.252). Lin's c is a galaxy-number concentration with BCGs excluded (L04 l.356, l.412), relative to r200 from ρ_c (l.243–246).

12. **Scale of cosmic variance (X21).** I tagged it system, but one COSMOS reference field serves all clusters (Gz l.713). It may therefore carry a dataset-level common component. Not stated.

13. **The g_obs vs g_bar assignment of X9 (sphericity) and X12 (clumping)** follows each source's wording. Sphericity also enters the density deprojection (G19 l.201), so it plausibly moves g_bar too. Not stated.

14. **I did not open the Planck covariance FITS files**, the thermodynamic profile files, or the PARAMS extension values. The PARAMS header was read.