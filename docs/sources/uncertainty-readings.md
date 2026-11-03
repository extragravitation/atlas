# Uncertainty readings at source (step A, D-080 WP2)

**Purpose.** Step A of `docs/plans/VALIDATION_COMPLETION_PLAN.md` reads, at source and before any v2 test is frozen, every uncertainty term for the five datasets still to be re-issued (SPARC v2 is done). Each term records:
- what the source says, with a quote and its location;
- its stated size;
- its scale under standard 2.2.0: point, system or dataset;
- what it moves (g_obs, g_bar or both);
- whether the release carries it.

A term the source does not quantify is recorded as **not stated**. It is never estimated here.

**Order:** KiDS-1000, X-COP, dwarf galaxies, globular clusters, strong lenses. Each section is added as it is read.

---

## 1. KiDS-1000 weak-lensing RAR (`aeg-d-kids1000-rar`)

**Read 2026-11-02.**

**The paper.** Brouwer et al. 2021, A&A 650, A113, read in its LaTeX source: arXiv e-print 2106.11677, file `RAR_paper_Brouwer_4.tex`. Locations below are section names with the source's line numbers. The 28 October reading used the ar5iv rendering.

**The release README.** It is inside `brouwer2021_rar.tar`. The KiDS server is not reachable from the workspace, so the README was read from a public GitHub mirror (`rstpier/EFF_G_GALAXIES`, `KiDS Brouwer Weak Lensing/README.txt`, SHA-256 `b3680580…8645`).
- **Integrity check.** The three ESD files from the same mirror are value-for-value identical to the v1 package's columns, which were converted from the hash-verified canonical tarball: g_bar, ESD_t, ESD_x, error and bias for all 45 rows.
- **Not yet done.** The README's own hash must be checked against the canonical tarball member in CI before the KiDS v2 test is frozen.

### 1.1 What the release carries

Per row (one bin in g_bar) the release gives:
- g_bar (column 1);
- ESD_t and ESD_x;
- `error`: "The 1-sigma error value on ESD_t, calculated using the lensfit weight 'w' and the lensing weight 'k'";
- `bias(1+K)`;
- a full covariance file per sample.

**The README's error recipe** for g_obs is `error[g_obs] = 4 G error[ESD_t]/bias` (README §2, "Fig-X_RAR_*").
- It adds no other term.
- It gives no error for g_bar.

**The g_bar column is the binning variable.** The paper (§2.1, l. 174) says: "we chose our R-bins such that they corresponded to 15 logarithmic bins between 1×10⁻¹⁵ < g_bar < 5×10⁻¹² m s⁻²". Each lens's own g_bar decides which bin it falls in.
- The released g_bar values all fall inside these bins, and none sits at a bin centre. They therefore appear to be bin means.
- The README describes column 1 as "The mean projected distance", which is radius wording. For the RAR files it does not say how the mean is taken. **To ask (Brouwer email).**

### 1.2 Terms

| # | Term | Source statement (location) | Size as stated | Scale | Moves | In release? |
|---|---|---|---|---|---|---|
| K1 | **Lensing statistical error** (shape noise, with correlations between bins) | "The error values on the ESD profile were estimated by the square-root of the diagonal of the analytical covariance matrix … The full covariance matrix … incorporates the correlation between sources that contribute to the ESD in multiple bins" (§2.1, l. 183) | Per bin. In the main KiDS-bright file, error/ESD_t = 0.073 to 0.126, i.e. 0.031 to 0.051 dex (computed from the release) | point, correlated across bins | g_obs | **Yes**: `error` and the covariance file |
| K2 | **Conversion of ESD to g_obs** (singular-isothermal-sphere deprojection) | "To account for the added uncertainty resulting from the conversion to the RAR, we added 0.1 dex to the error bars of our RAR measurements throughout this work." (§4.4, l. 438) | 0.1 dex. **How it was combined with K1 is not stated** (linear in log or in quadrature) | point (the test was on one stacked system; the paper applies it to every point) | g_obs | **No.** The README recipe omits it. The paper's plotted bars are larger than the released errors |
| K3 | **The SIS shape itself** | "the SIS method assumes a density profile ρ(r) ∝ r⁻² at all radii … At small radii, the power-law slope is in reality about −2.1 … At larger radii … increasingly overestimates the enclosed mass" (§4.4, l. 440). Tested on BAHAMAS mocks: "both the SIS and the PPL method yield acceptable and consistent estimates of g_obs" (l. 442) | Not stated separately; covered by K2 | — | g_obs | — |
| K4 | **Shear calibration** | "the factor (1+μ) calibrates the shear estimates … The value of this correction is μ ≈ 0.014" (§3.1, l. 333–337) | The correction is applied (the `bias` column). **Its uncertainty is not stated** | dataset | g_obs | Correction only |
| K5 | **Source redshift calibration** | "percent-level biases in the mean source redshifts do not significantly impact our analysis" (§3.1, l. 313) | Not stated (described as percent level) | dataset | g_obs | No |
| K6 | **Lens photometric redshift** | "p(z_l) is defined by a normal distribution centred at the lens' z_ANN redshift, with a standard deviation: σ_z/(1+z) = 0.02" (§3.1, l. 315). It is integrated into Σ_crit (eq. 3) | 0.02 in σ_z/(1+z). **Built into the measurement**: it enters ΔΣ through Σ_crit and is not a separate error | sub-point (per lens) | g_obs; and g_bar through M⋆ (K8) | Built in |
| K7 | **Random-point subtraction** | "the random ESD profile is very small … with a mean absolute value of only 1.85 ± 0.75 % of the lensing signal" (§3.1, l. 339) | A correction applied, of 1.85 ± 0.75 % | dataset | g_obs | Correction only |
| K8 | **Stellar mass, statistical** (per lens) | "Taking a middle ground between these two, we have assumed twice the LePhare estimate: σ_M⋆ = 0.12 dex. However, we have confirmed that using the maximal estimate σ_M⋆ = 0.29 dex throughout our analysis does not change the conclusions" (§3.3, l. 368) | 0.12 dex adopted; range 0.06 to 0.29 dex | sub-point (per lens). It decides which g_bar bin a lens falls in; it is not an error on a bin's g_bar | g_bar (bin assignment) | No |
| K9 | **Stellar mass, systematic** | "it has been found impossible to constrain stellar masses to within better than a systematic uncertainty of ΔM⋆ ≈ 0.2 dex … We estimated the effect of this bias by computing the RAR with log₁₀(M⋆) ± ΔM⋆ as upper and lower limits" (§3.3, l. 370). Also: "this uncertainty equally affects the GAMA stellar masses" (§5.2, l. 491) | ±0.2 dex. The authors re-ran the analysis rather than shifting the points, so its effect on each bin is **not** a simple 0.2 dex shift of g_bar | dataset (all lenses together) | g_bar, and g_obs through re-binning | **No.** Shown only as the grey band in Fig. 4. These files are the main data request in the Brouwer email |
| K10 | **Normalisation of stellar masses to GAMA** | "a systematic offset of log(M⋆,ANN) − log(M⋆,G) = −0.056 dex … We therefore normalised the M⋆,ANN values … to the mean M⋆,G of GAMA" (l. 370) | −0.056 dex, applied | dataset | g_bar | Applied |
| K11 | **Cold gas from a scaling relation** | "log(f_cold) = −0.69 log(M⋆/h70⁻² M☉) + 6.63" (Boselli et al. 2014; §4.3, l. 409) | **Scatter not stated** in this paper | dataset | g_bar | No |
| K12 | **Baryons not counted** (hot gas and others) | "we will use the stellar+cold gas mass M_gal as our fiducial estimate … This serves as a secure lower limit on g_bar" (§4.3, l. 421). The released hot-gas variant is "a rough order of magnitude estimate", with "a nominal gas mass equal to the stellar mass" within 100 h70⁻¹ kpc (Fig. 4 caption, l. 483) | Not an error bar. It sets the scope of the baryon inventory, plus one released alternative | dataset | g_bar | The hot-gas variant file (in v1) |
| K13 | **Isolation and satellites** (KiDS-bright only) | "the isolation criterion is no longer reliable when g_bar ≲ 10⁻¹³ m s⁻²"; satellites give "a ∼30% increase in ΔΣ" at R > 0.3 h70⁻¹ Mpc (§5.2, l. 489; App. A, l. 748) | About +30 % in ΔΣ, one-sided, below about 10⁻¹³ m s⁻². GAMA is "still reliable within this region" | point range (low-g_bar bins) | g_obs (upward) | The v1 flag `source_quality_low` |
| K14 | **Point-mass baryon model** | "we can approximate M_bar(<r) as a point mass M_gal" at R > 30 h70⁻¹ kpc (§4.3, l. 405–411) | Not stated as an error | dataset | g_bar | — |
| K15 | **Cosmology and h70** | Distances "using a flat ΛCDM cosmology, ignoring peculiar velocities" (App. A, l. 746). Units carry h70 | Not stated as an error | dataset | both | — (the Atlas uses h = 0.7, as the source does) |

### 1.3 Consequences for KiDS v2 (to settle in steps B and D; nothing decided here)

1. **v1 shows only K1.** v1 sets g_obs_err to the released error (K1), which is the README recipe. The paper's own error bars also include K2, the 0.1 dex conversion term, which is two to three times larger than K1. The v2 test must decide how K2 is shown. It cannot be put into the released numbers without knowing how the authors combined it with K1. Options for step D:
   - carry it as a separate point-scale term, stated as a quotation from §4.4;
   - ask the authors how it was combined, and apply the answer when it arrives.

   **This goes into the Brouwer v3 email.**
2. **g_bar has no point error by construction.** It is the binning coordinate (§1.1). The per-lens scatter (K8) and the systematic (K9) act through which lenses fall in each bin, not as an error bar on the bin. Standard 2.4.0 therefore needs a way to say "binning coordinate: no point error, by design", distinct from "not given by the source" (#64).
3. **The dataset-scale g_bar term is ±0.2 dex (K9).** The honest representation is the authors' re-run. A ±0.2 dex shift of the released g_bar is not equivalent, because each lens moves bin. So the shifted-mass files remain the route to a computed effect. Until the authors reply, K9 is stated in words, as v1 already does (D-021).
4. **Terms the source does not quantify** (K4, K5, K11, K14, K15) are listed as not stated. No value is invented.
5. **Built-in terms and applied corrections** (K6, K7, K10) are listed so a reader can see they were handled. They add no error bar.

### 1.4 Questions for the Brouwer v3 email (from this reading)

1. How was the 0.1 dex conversion term (§4.4) combined with the released ESD error in the paper's figures?
2. Is column 1 of the RAR files the lensing-weighted mean g_bar of the lenses in each bin?
3. Can the ±0.2 dex stellar-mass re-runs (the Fig. 4 grey band) be shared? (Already asked in v2.)
4. Licence of the release (already asked in v2).

The lens redshifts per bin and the "anything to treat differently" question (both in v2) are carried over.

---

## 2. X-COP galaxy clusters (`aeg-d-xcop`)

**Read 2026-11-02.**

**Method.** Two independent reader agents worked from one brief: [`readings/xcop-2026-11-02/brief.md`](readings/xcop-2026-11-02/brief.md). Neither could see the other's work. Their reports are kept verbatim as [`reader-A.md`](readings/xcop-2026-11-02/reader-A.md) and [`reader-B.md`](readings/xcop-2026-11-02/reader-B.md). Claude then adjudicated, as follows:
- **Quotes.** Every quoted line in the table below was rechecked against the LaTeX source. Five line numbers were corrected.
- **Disagreements and one-reader findings.** Each was settled at source.
- **Archive inferences.** The two that affect shipped data were recomputed independently from the archive (§2.3).

**Sources.** Both readers downloaded the same e-prints, with identical SHA-256. The archive is `allfiles.tar.gz` (`0edf5038…0d94`).

| Short name | Paper | arXiv (version) | Main .tex | e-print SHA-256 |
|---|---|---|---|---|
| E19 | Ettori et al. 2019, A&A 621, A39 | 1805.00035v3 | `mass_xcop.tex` | `3bc07668…d658733` |
| Ek19 | Eckert et al. 2019, A&A 621, A40 | 1805.00034v2 | `NTpressure.tex` | `766db093…427bf0` |
| G19 | Ghirardini et al. 2019, A&A 621, A41 | 1805.00042v2 | `XCOP_thermo.tex` | `9edb7d25…bfa38` |
| Gz | Ghizzardi et al. 2021, A&A 646, A92 | 2007.01084v1 | `xcop-metallicity.tex` | `88c8e91c…a9e8` |
| G18 | Ghirardini et al. 2018, A&A 614, A7 (A2319) | 1708.02954v2 | `X-COP-A2319.tex` | `ade2df04…105434b` |
| Go13 | Gonzalez et al. 2013, ApJ 778, 14 | 1309.3565v1 | `ms.tex` | `e582a681…a15a3` |
| L04 | Lin, Mohr & Stanford 2004 | astro-ph/0402308v3 | `arxiv.tex` | `96e3dc16…4b8c` |

### 2.1 What the release carries

There is no README in the archive. No FITS card defines `EM_FORW`, `MGAS_LO` or `MGAS_HI`. What the files and values show:
- **`EM_FORW`.** One symmetric error per radius. At R500 it is 2.0–5.5 % of `M_FORW`. E19 states its quoted errors are "statistical uncertainties at the $1 \sigma$ confidence level" (§1, l. 113). Whether this applies to the released column is **not stated**.
- **`MGAS_LO` / `MGAS_HI`.** Offsets, not bounds (inferred from the values); their confidence level is not stated. They are mostly 0.2–5 % of `MGAS`, reaching about 100 % at the outermost radii of RXC1825 and ZW1215.
- **`mstar.fits`, extension MSTAR_RAW.** The header says: "The quoted uncertainties are the statistical uncertainties and the cosmic variance (CV) separately." All four error columns are offsets.
- **`mstar.fits`, extension MSTAR_SMOOTHED.** The header says: "Smoothed stellar mass profile used in Ghizzardi et al. 2020 and total uncertainties." Its `MSTAR_LO` and `MSTAR_HI` are bounds. At R500, their half-width matches the statistical and cosmic-variance offsets added in quadrature (an inference by both readers).
- **No covariance of any mass profile is released.** The `*_Y-PROF-COVMAT_P-PROF-COVMAT*.fits` files hold the input Planck pressure covariance only.

### 2.2 Terms

Scale: **point** varies from radius to radius; **system** is shared by one cluster; **dataset** is shared by all clusters. "Both" means both readers found the term; "A" or "B" means one reader did, and Claude confirmed it at source.

| # | Term | Source statement (location) | Size as stated | Scale | Moves | In release? | Found by |
|---|---|---|---|---|---|---|---|
| X1 | Hydrostatic mass, statistical | "the quoted errors are statistical uncertainties at the $1 \sigma$ confidence level"; "half the difference between the 84th and 16th percentiles" (E19 §1 l. 113; §3 l. 227). For the forward method: "Errors are estimated through a Monte Carlo process" (G18 l. 606) | Abstract: "median error of $3$ \% at $R_{500}$ and $6$\% at $R_{200}$" (E19 l. 48, backward NFW). Forward method: not stated as a number | point as released. Each profile comes from one smooth fit per cluster, so the errors are correlated across radii; the size of the correlation is **not stated** | g_obs | `EM_FORW` (not defined in the file) | Both |
| X2 | X-ray/SZ intrinsic scatter and Planck pressure covariance in the fit | "an intrinsic scatter $\sigma_{T,int}$ to account for any tension between X-ray and SZ measurements … the covariance matrix … in the \planck\ pressure profile" (E19 §3 l. 208–209) | σ_T,int 0.001–0.079 for the NFW fits (Table A.1). Forward fits: not stated | system | g_obs | Absorbed in `EM_FORW` (inferred) | Both |
| X3 | Method and mass-model choice | "median difference of about 4\% at $R_{500}$, and $<$2\% (1st-3rd quartile: -5.4 / +8.1 \%) at $R_{200}$" (E19 §3.3 l. 414–415; Table 2) | Forward vs backward NFW: −4.7 % (−10.9/−0.5) at R500, +1.2 % (−5.4/+8.1) at R200. Isothermal and Burkert: up to about 25 % | system (one offset per cluster; the quartiles describe the dataset) | g_obs | Alternative models in the file (`M_NFW`, `M_EIN`, `M_ISO`, `M_BUR`) | Both |
| X4 | Non-thermal pressure (hydrostatic bias) | "median non-thermal pressure of $5.9_{-3.3}^{+2.9}\%$ and $10.5_{-5.5}^{+4.3}\%$ at $R_{500}$ and $R_{200}$"; "$M_{\rm 500,HSE}/M_{\rm 500,tot}=0.94\pm0.04$" (Ek19 §4.1 l. 211; §4.3 l. 240) | Per cluster in Ek19 Table 2: up to 43.6 % (R500) and 52.3 % (R200) for A2319; some are upper limits | system (varies with radius) | g_obs (low, if present) | no | Both |
| X5 | Non-thermal pressure, departure from equilibrium and asphericity, combined | "bias the total mass estimates higher (by 10--30\%) at $r>R_{500}$" (E19 §3.3 l. 449). The Conclusions give "10--20\%" (l. 610) | 10–30 % or 10–20 %: **the paper gives two ranges** | system | g_obs | no | Both |
| X6 | Intrinsic scatter of hydrostatic masses | "$\sigma_{M_\text{HE}\|M}=0.15\pm0.08$" (E19 §3.2 l. 391). The abstract says "0.15 dex" (l. 53) | 0.15 ± 0.08 dex | system | g_obs | no | Both |
| X7 | X-ray temperature calibration | "If \emph{Chandra} temperatures are correct, our masses should be underestimated by $\sim15\%$" (Ek19 §5.1 l. 262) | about 15 % | dataset | g_obs | no | Both |
| X8 | X-ray vs SZ pressure | ZwCl 1215: "the pressure measured by \xmm\ actually {exceeds} the SZ pressure by $\sim20\%$" (G19 §5.1 l. 657) | Sample consistent with unity; ZW1215 about 20 % | dataset (ZW1215: system) | g_obs | no | Both |
| X9 | Relativistic SZ correction | "up to 15\% for the hottest clusters … less than 5\%" at R500 and beyond (G19 §5.1 l. 655) | below 5 % at R500 and beyond | system | g_obs | no | Both |
| X10 | A2319 pilot systematics | Temperature: "ranges between 1.4\% and 9.1\%, apart from the outermost radial point where we measure a value of 19\%" (G18 l. 468). Mass: "4.18\% and 8.5\% at $R_{500}$ and $R_{200}$" (G18 l. 646) | As quoted (A2319 only). Whether they were propagated into the 12-cluster release: **not stated** | point / system | g_obs | unknown | Both |
| X11 | Overall accuracy claim | "our masses and the corresponding values of $R_{500}$ are accurate at the $10\%$ and $3\%$ level" (G19 §2.5 l. 314) | 10 % (mass), 3 % (R500) | system | g_obs | no | B |
| X12 | X-ray background subtraction | "A systematic error of 5\% of the background value was thus added in quadrature to all our surface brightness measurements" (G19 §5.1 l. 653). A3266: 30 % (G19 l. 191) | 5 % of the background level; A3266 30 % | system in origin, added per point | both | Inside the released errors (inferred) | Both |
| X13 | Gas deprojection method | "a remarkable agreement between them, with an average scatter $<5\%$ at each radius" (G19 §2.3 l. 214) | below 5 % | system | both | no | A |
| X14 | Gas density, statistical | "typical uncertainties in the gas density and pressure at $R_{200}$ are at the level of $10\%$" (G19 §6 l. 692) | about 10 % at R200 | point (from one fit, so correlated) | g_bar (and g_obs) | `MGAS_LO`, `MGAS_HI` | A |
| X15 | Gas mass, systematic accuracy | "measurements of $M_{\rm gas}$ are accurate down to the level of a few percent" (Ek19 §5.1 l. 261) | "a few percent" | dataset | g_bar | no | Both |
| X16 | Gas-density cross-calibration (XMM/Chandra) | "agreement between the two missions at the level of 2.5\%" (Ek19 §5.1 l. 262) | 2.5 % | dataset | g_bar | no | B |
| X17 | Residual gas clumping | "Residual clumping … less than a few percent" (Ek19 §5.1 l. 261) | below a few percent; positive bias | system | g_bar | no | Both |
| X18 | Helium sedimentation | "a bias of a few per cent restricted to the inner ($<R_{2500}$) cluster regions" (Ek19 §5.1 l. 263) | a few per cent inside R2500 | system | both | no | Both |
| X19 | Mean molecular weight and abundances | "$n_{\rm e} + n_{\rm p} \approx 1.83 n_{\rm e}$" (E19 l. 173). Each paper states its own conversion: E19 l. 173, Ek19 l. 84, G19 l. 201, Gz l. 529 | effect **not stated** | dataset | both | no | Both |
| X20 | Other baryons (cold or molecular gas, dust) | "typically represent less than 0.1\% of the mass content" (Ek19 §3.1 l. 106) | below 0.1 % | dataset | g_bar | no | A |
| X21 | Cosmology | "the results have a very mild dependence on the adopted cosmology" (Ek19 §1 l. 54); H0 = 70, Ωm = 0.3 (E19 l. 120–121) | **not stated** | dataset | both | no | Both |
| X22 | Redshift and distance | Redshift "from the PSZ1 catalogue" (G19 Table 1 note, l. 145); no redshift error anywhere | **not stated** | system | both | `REDSHIFT` header (value only) | Both |
| X23 | R500 and M500, statistical | `ERR_R500`: "Statistical uncertainty on NFW R500" (FITS header); E19 Table 1 | e.g. A85: 1235 ± 13 kpc | system | g_bar (the gas radii are in R/R500; the modelled stars are normalised at R500) | `ERR_R500`, `ERR_M500` headers | Both |
| X24 | Measured stars, statistical | "we bootstrap the flux measurements within their uncertainties, and perform 100 perturbations for each galaxy" (Gz §5.1 l. 712) | in the file only | point (cumulative, so correlated) | g_bar | MSTAR_RAW `MSTAR_LO`, `MSTAR_HI` | Both |
| X25 | Measured stars, field-to-field ("cosmic") variance | "a substantial uncertainty due to field-to-field (often called "cosmic") variance" (Gz §5.1 l. 713) | in the file only | system. One reference field serves all clusters, so part of it may be dataset-wide; **not stated** | g_bar | MSTAR_RAW `MSTAR_CV_LO`, `MSTAR_CV_HI` | Both |
| X26 | Measured stars, IMF and population modelling | The Salpeter IMF "provides values that exceed by a factor $ \sim 2$ those obtained using a \citet{chabrier03} mass function" (Gz §5.2 l. 749). "we may be underestimating stellar masses by as much as 60\%" (Gz §6.3 l. 923) | factor of about 2 (IMF); up to 60 % (low) | dataset | g_bar | no | Both |
| X27 | Intracluster light, excluded | "the BCG is included in our mass computation, while the Intra-Cluster Light … is not" (Gz l. 711). Published estimates range from about 10 % to about 50 % of total light (Gz l. 928–930). Ek19: "$\sim20-30\%$ … of the total stellar mass" (l. 146) | 10–50 % of light; 20–30 % of stellar mass | dataset | g_bar | no (excluded) | Both |
| X28 | Galaxy mass limit | "more than 98\% of the stellar mass" (Gz l. 710, footnote) | below 2 % missing | dataset | g_bar | no | Both |
| X29 | Centring | "the centres differ by at most 2\% of $R_{500}$" (Gz §5.1 l. 700) | effect "generally small" | system | g_bar | no | Both |
| X30 | **Projected vs spherical stellar mass** | "the cumulative stellar masses … are derived by integrating within a projected radius … We therefore multiply the stellar mass estimates by a factor 0.75" (Gz l. 715) | 0.75 at R500 only. Other radii: **not stated**. See finding F1 | system | g_bar | The correction is **not applied** in the released profiles (F1) | Both |
| X31 | Modelled stars: intrinsic scatter of the stellar-to-gas relation | "we derive an intrinsic scatter of only 12\%"; "The 17\% scatter about the best fit relation" (Go13 l. 1563; l. 812) | 12 % intrinsic (17 % total) | system | g_bar (5 clusters) | no | Both |
| X32 | Modelled stars: relation parameters | "$3.90\pm0.02\times10^{-1}$ & $-0.84\pm0.04$" (Go13 Table 4, l. 1035; used in E19 §5 l. 563–564) | ±0.002 (normalisation), ±0.04 (slope). The relation was fitted in WMAP7 cosmology (H0 = 70.2); the Planck version has slope −0.81 (Go13 l. 1755) | dataset | g_bar | no | Both |
| X33 | Modelled stars: mass-to-light systematics | "impact our results at a level of $15$\%" (Go13 l. 1259) | 15 % | dataset | g_bar | no | Both |
| X34 | Modelled stars: galaxy concentration | "$c_g=2.90_{-0.22}^{+0.21}$" (L04 §3 l. 362; E19 uses 2.9, l. 563) | +0.21 / −0.22 | dataset | g_bar (shape) | no | Both |
| X35 | Modelled stars: accuracy of the prescription for X-COP | E19 §5 (l. 563–565) gives no error. "median $M_{\rm star}/ M_{\rm gas}$ of 0.09 (0.07--0.12 as 1st and 3rd quartile)" describes the sample spread | **not stated**. The Gonzalez sample spans "$M=1-5\times10^{14}$" (Go13 l. 76); A2255 and A3266 lie above it | system | g_bar | no | Both (A: mass range) |

**Looked for and not stated in any source read:**
- a covariance of any mass profile across radii;
- whether `EM_FORW` includes any systematic term;
- the definitions and confidence levels of `MGAS_LO` and `MGAS_HI`;
- redshift errors;
- how g_obs or g_bar scale with distance or h;
- the size of the effect of the μ or abundance assumption;
- the uncertainty of the 0.75 projection factor, and its value at radii other than R500;
- whether the A2319 pilot systematics were propagated;
- a separate size for asphericity;
- the radial distribution of intracluster light.

### 2.3 Findings that bear on the shipped data (adjudicated by Claude at source)

**F1. The released stellar-mass profiles appear to be projected (within a cylinder), not enclosed within a sphere.** Both readers found this independently, and Claude recomputed it.
- **The source text.** Gz l. 715 says its cumulative stellar masses "are derived by integrating within a projected radius". It converts to a sphere only at R500, with a factor of 0.75.
- **The test.** Multiplying the released `MSTAR_SMOOTHED` at R500 by 0.75 reproduces Gz Table 2's $M_{\rm star,500}$ for six of the seven clusters, to within 5 %:

  | Cluster | 0.75 × release at R500 (10¹² M☉) | Gz Table 2 (10¹² M☉) |
  |---|---|---|
  | A85 | 2.20 | 2.10 |
  | A1795 | 2.98 | 3.02 |
  | A2029 | 6.58 | 6.51 |
  | A2142 | 6.93 | 6.97 |
  | A2319 | 5.22 | 5.11 |
  | ZW1215 | 3.19 | 3.34 |
  | A644 | 4.13 to 4.18 | 3.70 |

- **What the release does not say.** No header says "projected".
- **What v1 does.** `aeg-d-xcop/v1` (`convert.py`, l. 14) uses the profile as a spherical enclosed mass, M(<r).
- **The likely effect.** If the inference holds, v1 overstates the stellar part of g_bar for the seven measured clusters. The stated factor is 1/0.75 at R500, and the factor at other radii is **not stated**. A projected mass exceeds the spherical one by more at small radii, and in v1 stars are the median 65 % of g_bar inside 100 kpc. So the effect is largest exactly where stars dominate.
- **A knock-on effect.** The modelled-star test (D-023), which fixed the 0.145–1.38 R500 range, compared the spherical prescription with these same profiles. Its result may be affected too.
- **Status.** This is not established from the release alone. It is a question for the X-COP team (Ghizzardi is the author of the stellar profiles).

**F2. A644: the forward-method enclosed mass decreases with radius.** Found by Reader A and confirmed in the shipped table.
- In `aeg-d-xcop/v1`, `M_FORW` falls with radius from 1078 kpc to 1884 kpc in 12 of A644's 89 rows. An enclosed mass cannot fall with radius.
- These rows are already flagged `reproduction_mismatch` (#19), but for a different reason.
- Archive A3158 also shows this beyond 2166 kpc, outside the shipped range.

**F3. The stellar radii of A644 and A2319 use a different R500 from the other files.** Found by Reader A and confirmed.
- MSTAR_SMOOTHED radii equal the MSTAR_RAW r/R500 grid times Ettori Table 1's R500: exactly 1230.0 kpc and 1346.0 kpc.
- The same clusters' gas and hydrostatic headers use 1250 kpc and 1368 kpc.
- A2029's stellar radii use the header value, 1414 kpc.
- The archive is therefore internally inconsistent for these clusters, in addition to #19.

**F4. Released gas masses at R500 are 3–10 % below Gz Table 2 for 11 of 12 clusters.** Both readers found this.
- Most ratios are 0.90–0.94; A2319 is 1.00.
- The release's errors are about half of Gz's.
- **Not explained by the sources.** Each paper states its own density conversion (X19).

**F5. More header values differ from Ettori Table 1.** Found by both readers.
- The A2142 redshift is 0.09 against 0.0909.
- The A3158 redshift is 0.059 against 0.0597.
- These are in addition to the three clusters of #19.

### 2.4 Consequences for X-COP v2 (for steps B and D; nothing decided here)

1. **What the error columns are.** `EM_FORW`, `MGAS_LO`/`HI` and the stellar bounds are the point-scale terms carried in the release, all statistical and all correlated along each profile. A covariance was requested from Eckert on 2026-11-02.
2. **System and dataset terms.** These are stated with their source sizes and are not drawn as error bars:
   - from the source papers, X3–X9, X12–X13, X15–X19, X26–X27 and X31–X35;
   - from the release headers, X23.
3. **F1 decides what the stellar data mean.** Before the X-COP v2 test is frozen, JvH rules how to handle it. Options:
   - **(a)** Ask the X-COP team first, and freeze after the answer.
   - **(b)** Freeze now, with the profile treated as projected, as the strongest reading of the sources.
   - **(c)** Freeze now with v1's treatment, flagging F1 as a known issue.

   This changes what the Atlas says, so it is a ruling.
4. **F2, F3 and F5 become known-issue text.** They do not change any value.
5. **Modelled stars.** The source states no accuracy for the prescription (X35). Its inputs carry a 12 % intrinsic scatter (X31) and 15 % mass-to-light systematics (X33). It also counts BCG and intracluster light, which the measured stars exclude. These are stated, not combined.
