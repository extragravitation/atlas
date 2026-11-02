# Reader A: uncertainty terms in the X-COP release that affect g_obs and g_bar

**Reader:** Reader A  
**Date:** 2026-11-02  
**Working directory:** `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/readerA`. Each e-print is in its own `dl_<id>/` folder, the archive extract is in `archive_x/`, and my reading scripts are in `scripts/`. Nothing outside this directory was modified.

## Sources read

| arXiv id (latest version on the abs page) | Main .tex | SHA-256 of downloaded e-print |
|---|---|---|
| 1805.00035v3 (Ettori+2019) | `mass_xcop.tex`; tables also in `m_syst.tex`, `m_over.tex`, `m_mod_*.tex` | `3bc07668cc877920ac05ca955c88d80d15aad19a11d9fd7286e25c396d658733` |
| 1805.00034v2 (Eckert+2019) | `NTpressure.tex` and `table2.tex` | `766db09383ff70125677ca0872d6d4b2865e32637cc133c97213222be8427bf0` |
| 1805.00042v2 (Ghirardini+2019) | `XCOP_thermo.tex` | `9edb7d25de34b769d7c8591db38bfbc7325c93f0d83d9569a774396c3d8bfa38` |
| 2007.01084v1 (Ghizzardi+2021) | `xcop-metallicity.tex` | `88c8e91c036077e2ca660cd029943d576df1462daae914d3e58aa24169c5a9e8` |
| 1708.02954v2 (Ghirardini+2018, the A2319 pilot; "ghi18" in Ettori) | `X-COP-A2319.tex` | `ade2df04fe4305c649bde1c75900310bd97d1cc1d15a4b80d401e2f36105434b` |
| 1309.3565v1 (Gonzalez+2013; id found from Ettori's bib entry ApJ 778, 14 and confirmed on the abs page) | `ms.tex` | `e582a681d6656c8752ef3d5057701be9087ff26f2c4e5d6f846a2e3895ac15a3` |
| astro-ph/0402308v3 (Lin+2004) | `arxiv.tex` | `96e3dc16c07c2a979539684d317868b46e2f8180a988db795f2b4044e19b4d8c` |

I also read the repository files `data/packages/aeg-d-xcop/v1/SOURCE.md` and `convert.py`, without modifying them.

## Archive members opened

- I checked the archive's SHA-256 and it matches `0edf5038…0d94`.
- I listed every member. The archive has no README or notes file.
- I extracted and opened `<c>_hydro_mass.fits` (12 files, both the HYDRO_MASS and PARAMS extensions) and `<c>_fgas_profile.fits` (12 files).
- I extracted and opened `<c>_mstar.fits` (7 files: A85, A644, A1795, A2029, A2142, A2319, ZW1215, both MSTAR_RAW and MSTAR_SMOOTHED).
- I extracted all 12 `*_Y-PROF-COVMAT_P-PROF-COVMAT.20170830.fits` files but read the header of the A85 one only.

### What the headers say

- **Hydrostatic mass file:** the only description is `COMMENT Hydrostatic mass profiles for various mass models`. No card defines `EM_FORW`: its confidence level and what it includes are not stated.
- **Gas file:** the only description is `COMMENT Gas mass and hydrostatic gas fraction profile`. No card defines `MGAS_LO` or `MGAS_HI`.
- **Stellar file, MSTAR_RAW extension:** the comment reads "Stellar mass profile used in Ghizzardi et al. 2020. The quoted uncertainties are the statistical uncertainties and the cosmic variance (CV) separately."
- **Stellar file, MSTAR_SMOOTHED extension:** the comment reads "Smoothed stellar mass profile used in Ghizzardi et al. 2020 and total uncertainties."
- **Keywords:** the hydro and gas files carry `REDSHIFT`, `R500`, `ERR_R500` ("Statistical uncertainty on NFW R500"), `M500` and `ERR_M500`.

### What the values show (inferred by reading them)

- **`EM_FORW`** is a single symmetric error per radius. Divided by `M_FORW` at the header R500 it is 2.0 to 5.5 % across the 12 clusters.
- **`MGAS_LO` and `MGAS_HI`** are offsets, not bounds: both are below `MGAS` at every radius. They are mostly 0.2 to 5 % of `MGAS`. At the outermost gas radii `MGAS_HI` reaches 93 % of `MGAS` for ZW1215 and 100 % for RXC1825.
- **MSTAR_RAW:** `MSTAR_LO`, `MSTAR_HI`, `MSTAR_CV_LO` and `MSTAR_CV_HI` are all offsets, roughly 0 to 45 % of `MSTAR`.
- **MSTAR_SMOOTHED:** `MSTAR_LO` and `MSTAR_HI` are bounds that bracket `MSTAR` (0.65 to 0.96 and 1.04 to 1.35 times `MSTAR`).
  - At R500 the smoothed half-width roughly equals the stat and CV offsets added in quadrature (A1795: quadrature 3.8e11 against smoothed 3.8e11/3.7e11). A linear sum would be too large (5.1e11). This is an inference.

## Uncertainty terms

Scale: **point** = varies independently from radius to radius; **system** = shared by all radii of one cluster; **dataset** = shared by all clusters. Each term is listed once, under the quantity it mainly moves; terms that move both are marked in the "Moves" column.

### g_obs (hydrostatic mass)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In release? |
|---|---|---|---|---|---|---|---|
| X1 | Statistical error on the hydrostatic mass | "Unless mentioned otherwise, the quoted errors are statistical uncertainties at the $1 \sigma$ confidence level." / "the errors as half the difference between the 84th and 16th percentiles" | mass_xcop.tex §1 l.113; §3 l.226–227 | "relative (statistical) median error of $3$ \% at $R_{500}$ and $6$\% at $R_{200}$" (l.48, backward NFW). Forward method: not stated as a number. File: `EM_FORW` is 2.0–5.5 % at R500 | point as released, but each profile comes from one fit per cluster (see Doubts) | g_obs | `hydro_mass.fits` HYDRO_MASS `EM_FORW` (the file does not define it) |
| X2 | How forward-method errors are made | "Errors are estimated through a Monte Carlo process." | X-COP-A2319.tex §4 (Hydrostatic mass) l.606 | not stated | system | g_obs | inside `EM_FORW` (inference) |
| X3 | X-ray/SZ intrinsic scatter fitted in the likelihood | "an intrinsic scatter $\sigma_{T,int}$ to account for any tension between X-ray and SZ measurements" | mass_xcop.tex §3 l.208 | NFW fits: 0.001 to 0.079 per cluster (Table A.1, l.681–693). Forward fits: not stated | system | g_obs | no separate column; absorbed in the errors (inference) |
| X4 | Correlated Planck pressure points | "points of our $y$ and SZ pressure profiles are correlated … when pressure is used to derive other quantities we make complete use of the whole covariance matrix" | X-COP-A2319.tex §3 l.365–366; mass_xcop.tex l.209 | not stated as a number | correlated across radii | g_obs | `*_Y-PROF-COVMAT_P-PROF-COVMAT*.fits` (input pressure covariance only; no mass covariance) |
| X5 | Method and mass-model choice | "the use of the {forward} method … introduces a small systematic error … median difference of about 4\% at $R_{500}$, and $<$2\% (1st-3rd quartile: -5.4 / +8.1 \%) at $R_{200}$" | mass_xcop.tex §3.3 l.414–415; Table 2 l.429–435 | Forward minus backward NFW: −4.7 % (−10.9/−0.5) at R500 and +1.2 % (−5.4/+8.1) at R200. ISO and BUR: up to about 25 % (l.420–421). Overall "of the order of 5\%" (l.49–50) | system (one offset per cluster; the quartiles describe the dataset) | g_obs | other models are released: `M_NFW`, `M_EIN`, `M_ISO`, `M_BUR` with `EM_*`. `EM_HER` exists but there is no `M_HER` column |
| X6 | Non-thermal pressure (hydrostatic bias) | "We find a median non-thermal pressure of $5.9_{-3.3}^{+2.9}\%$ and $10.5_{-5.5}^{+4.3}\%$ at $R_{500}$ and $R_{200}$" | NTpressure.tex §4.1 l.211; per-cluster table2.tex l.8–19 | Median 5.9 % (R500) and 10.5 % (R200). Per cluster: up to 43.6 % and 52.3 % for A2319, with upper limits for 3 clusters. "upper limit of 13\% to the mean" (l.219). $M_{\rm 500,HSE}/M_{\rm 500,tot}=0.94\pm0.04$ (l.240). Inputs: $\Omega_b/\Omega_m=0.156\pm0.003$ (l.106), Y_b percentiles (Table 1, l.134–135), $f_{\star}=0.015\pm0.005$ (l.147) | system (radius-dependent α(r) per cluster) | g_obs (masses biased low) | no (the paper's Table 2 only) |
| X7 | Non-thermal pressure, departure from equilibrium and asphericity, taken together | "tend to bias the total mass estimates higher (by 10--30\%) at $r>R_{500}$" | mass_xcop.tex §3.3 l.445–450 | 10–30 % here; 10–20 % in the Conclusions (l.606–610) | system | g_obs | no |
| X8 | Intrinsic scatter of hydrostatic masses | "we can estimate the intrinsic scatter of the hydrostatic masses, $\sigma_{M_\text{HE}\|M}=0.15\pm0.08$" | mass_xcop.tex §3.2 l.391–393; abstract l.53 ("0.15 dex") | 0.15 ± 0.08 (in dex according to the abstract) | system | g_obs | no |
| X9 | X-ray temperature calibration | "If \emph{Chandra} temperatures are correct, our masses should be underestimated by $\sim15\%$" | NTpressure.tex §5.1 l.262; also XCOP_thermo.tex §5.1 l.657 | about 15 % | dataset | g_obs (gas mass only "mild"; XMM and Chandra gas masses agree to 2.5 %) | no |
| X10 | Test of X-ray against SZ pressure | "the parameter $\eta_{SZ}$ shows a distribution consistent with unity" / "ZwCl 1215 … exceeds the SZ pressure by $\sim20\%$" | XCOP_thermo.tex App. A l.730; §5.1 l.657 | consistent with 1; about 20 % for ZW1215 | dataset (ZW1215: system) | g_obs | no |
| X11 | SZ relativistic corrections | "could lead to an underestimate of the integrated SZ signal up to 15\% for the hottest clusters … For typical temperatures of $\sim5$ keV at $R_{500}$ and beyond the expected effect is less than 5\%" | XCOP_thermo.tex §5.1 l.655 | up to 15 % (integrated signal); below 5 % at R500 and beyond | system | g_obs | no |
| X12 | A2319 pilot: temperature systematics | "The relative systematic error ranges between 1.4\% and 9.1\%, apart from the outermost radial point where we measure a value of 19\%." | X-COP-A2319.tex §5.2 l.466–468 | 1.4–9.1 %; 19 % in the outermost bin | point (per temperature bin) | g_obs (A2319) | not stated whether it was propagated into the X-COP release |
| X13 | A2319 pilot: total mass systematics | "the total systematic uncertainties are at the level of 4.18\% and 8.5\% at $R_{500}$ and $R_{200}$" | X-COP-A2319.tex §5.4.1 l.646–649 | 4.18 % (R500), 8.5 % (R200) | system | g_obs (A2319 only) | no |

### Terms that move both g_obs and g_bar

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In release? |
|---|---|---|---|---|---|---|---|
| X14 | X-ray background subtraction | "A systematic error of 5\% of the background value was thus added in quadrature to all our surface brightness measurements." | XCOP_thermo.tex §5.1 l.653; §2.2.4 l.191 | 5 % of the background level. A3266 (sky background taken from ROSAT): "a systematic error of 30\%" | system in origin, but added per point | both (density feeds the gas mass and the hydrostatic mass) | included in the released errors (inference from "added in quadrature to the error budget") |
| X15 | Choice of gas deprojection method | "a remarkable agreement between them, with an average scatter $<5\%$ at each radius" | XCOP_thermo.tex §2.3 l.214 | below 5 % | system | both | no |
| X16 | Residual gas clumping | "Residual clumping on scales smaller than the resolution of our study ($\lesssim 20$ kpc) can still introduce a slight positive bias in our estimates of $M_{\rm gas}$ … less than a few percent." | NTpressure.tex §5.1 l.261 | "less than a few percent". Without the median correction it would be 5–10 % at R200, but that is corrected | system | g_bar (gas), and g_obs through density | no |
| X17 | Helium sedimentation | "a bias of a few per cent restricted to the inner ($<R_{2500}$) cluster regions" | NTpressure.tex §5.1 l.263 | a few per cent inside R2500 | system | both | no |
| X18 | Mean molecular weight and abundance assumption | "$\mu … \approx 0.6$ … for a typical metallicity of 0.3 times the solar abundance from [ag89]" | mass_xcop.tex §3 l.182–186; NTpressure.tex l.84 ($\mu=0.61$, $n_e=1.17n_p$); XCOP_thermo.tex l.201, l.237 | not stated | dataset | both | no |
| X19 | Cosmology | "Note that since our clusters are local ($z<0.1$) the results have a very mild dependence on the adopted cosmology." | NTpressure.tex §1 l.54; mass_xcop.tex l.120–121 (H0 = 70, Ωm = 0.3) | not stated | dataset | both | no |
| X20 | Redshift and angular-diameter distance | Redshift "from the PSZ1 catalogue"; the emission-measure normalisation contains $4\pi [d_A(1+z)]^2$ | XCOP_thermo.tex Table 1 note l.145; §2.3 l.199–201 | no redshift error is given anywhere | system | both | header `REDSHIFT` (no error) |

### g_bar: hot gas

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In release? |
|---|---|---|---|---|---|---|---|
| X21 | Statistical error on gas mass | "The typical uncertainties in the gas density and pressure at $R_{200}$ are at the level of $10\%$" | XCOP_thermo.tex §6 l.692; also xcop-metallicity.tex Table l.549–560 ($M_{\rm gas,500}$ about ±1 %) | about 10 % in density at R200. File: 0.2–5 %, up to 100 % at the outermost radii (RXC1825, ZW1215) | point as released (comes from a smooth fit) | g_bar | `fgas_profile.fits` FGAS `MGAS_LO`, `MGAS_HI` (offsets; confidence level not given in the file) |
| X22 | Systematic accuracy of gas masses | "measurements of $M_{\rm gas}$ are accurate down to the level of a few percent and exhibit very little scatter" | NTpressure.tex §5.1 l.261; xcop-metallicity.tex l.935 | "a few percent" | dataset | g_bar | no |
| X23 | Uncertainty on R500 (gas file radii are in R/R500) | `ERR_R500 / Statistical uncertainty on NFW R500` | FITS headers (hydro and gas files) | for example A85 1235 ± 13 kpc. The effect on gas radii is my inference; the sources state none | system | g_bar (through the Atlas's conversion of gas radii to kpc) and the modelled stars | header `ERR_R500`, `ERR_M500` |
| X24 | Cold gas, dust and other baryons | "Baryons in other forms such as warm and molecular gas or dust typically represent less than 0.1\% of the mass content" | NTpressure.tex §3.1 l.106 | below 0.1 % of total mass | dataset | g_bar | no |

### g_bar: measured stars (7 clusters)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In release? |
|---|---|---|---|---|---|---|---|
| X25 | Statistical error (galaxy fluxes) | "we bootstrap the flux measurements within their uncertainties, and perform 100 perturbations for each galaxy" | xcop-metallicity.tex §5.1 l.712 | not stated as a number; file offsets 1–45 % | point | g_bar | `mstar.fits` MSTAR_RAW `MSTAR_LO`, `MSTAR_HI` (offsets) |
| X26 | Field-to-field ("cosmic") variance of the background subtraction | "there is a substantial uncertainty due to field-to-field (often called "cosmic") variance … the systematic uncertainty on the profile due to field-to-field variance" | xcop-metallicity.tex §5.1 l.713–714 | not stated as a number; file offsets 0–26 % | system (one reference field per cluster) | g_bar | MSTAR_RAW `MSTAR_CV_LO`, `MSTAR_CV_HI` |
| X27 | Total stellar uncertainty | "Smoothed stellar mass profile used in Ghizzardi et al. 2020 and total uncertainties" | FITS COMMENT, MSTAR_SMOOTHED | bounds at 0.65–0.96 and 1.04–1.35 times `MSTAR` | mixed | g_bar | MSTAR_SMOOTHED `MSTAR_LO`, `MSTAR_HI` (bounds) |
| X28 | IMF and stellar-population modelling | "assuming a \citet{salpeter55}-diet Initial Mass Function (IMF) … provides values that exceed by a factor $ \sim 2$ those obtained using a \citet{chabrier03}" | xcop-metallicity.tex §5.2 l.749 (assumptions listed at l.693) | factor of about 2 | dataset | g_bar | no |
| X29 | Offset from other stellar-mass samples | "assuming a systematic discrepancy of $50\%-60\%$ … seems reasonable" / "we may be underestimating stellar masses by as much as 60\%" | xcop-metallicity.tex §5.2 l.782; §6.3 l.923 | 50–60 % (in the low direction) | dataset | g_bar | no |
| X30 | Intracluster light is excluded | "the BCG is included in our mass computation, while the Intra-Cluster Light (hereafter ICL) is not" / "about 10\% … about 50\%" | xcop-metallicity.tex l.711; l.928–931 | ICL is 10 % (Zibetti) to 50 % (Zhang) of total light. Eckert l.146: "ICL can account for $\sim20-30\%$ … of the total stellar mass". Gonzalez l.91–93: leaving out ICL underestimates the normalisation by about 25 % | system / dataset | g_bar | no |
| X31 | Galaxy stellar-mass cut | "only consider galaxies with $M_{\star}>10^{9}$ … this would account for more than 98\% of the stellar mass" | xcop-metallicity.tex l.710 (footnote) | below 2 % missing | dataset | g_bar | no |
| X32 | Choice of centre | "The impact of how these profiles are centred is generally small (the centres differ by at most 2\% of $R_{500}$)." | xcop-metallicity.tex l.700 | centre offset up to 2 % of R500; mass effect "generally small" | system | g_bar | no |
| X33 | Projected versus spherical stellar mass | "the cumulative stellar masses … are derived by integrating within a projected radius … We therefore multiply the stellar mass estimates by a factor 0.75." | xcop-metallicity.tex l.715 | factor 0.75 (gNFW with c = 0.72, α = 1.64); uncertainty on the factor not stated | system | g_bar | not applied in the file (see Doubts, item 3) |

### g_bar: modelled stars (5 clusters, Ettori §5)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In release? |
|---|---|---|---|---|---|---|---|
| X34 | Stellar-to-gas relation: fit errors | "$M_{\star,3D}/M_{gas}$ & $3.90\pm0.02\times10^{-1}$ & $-0.84\pm0.04$" | ms.tex Table 4 l.1035 (relation used at mass_xcop.tex §5 l.563–564) | a = 0.390 ± 0.002; b = −0.84 ± 0.04 | dataset | g_bar (5 clusters) | no |
| X35 | Stellar-to-gas relation: intrinsic scatter | "For the $M_{\star,3d}/M_{gas} -$ \mfive\ relation we derive an intrinsic scatter of only 12\%." | ms.tex §6 l.1562–1563; l.812–813 ("17\% scatter … 12\% intrinsic") | 12 % intrinsic (17 % total) | system | g_bar | no |
| X36 | Mass-to-light systematics in Gonzalez | "the largest systematic uncertainties in our conversion to stellar mass are clearly defined and impact our results at a level of $15$\%" | ms.tex l.1257–1259 | 15 % | dataset | g_bar | no |
| X37 | Galaxy concentration | "The {\it galaxy} concentration is $c_g=2.90_{-0.22}^{+0.21}$" | arxiv.tex §3 l.362 (Ettori cites "2.9", mass_xcop.tex l.563) | +0.21/−0.22. Possible bias "$\Delta c \sim 0.15 - 0.35$, with scatter about 0.25" (l.1402); other published values 2.6 and 3.7 (ms.tex l.1275–1277) | dataset | g_bar (shape) | no |
| X38 | Inputs to the normalisation | M500, R500 and R200 errors | mass_xcop.tex Table 1 l.313–325 | per cluster, for example A2255 M500 5.26 ± 0.34 | system | g_bar | header `ERR_M500` (the header values differ from Table 1 for some clusters; see Doubts) |

## Looked for and found "not stated"

- **Covariance or correlation of the hydrostatic mass across radii.** Not in Ettori (the only covariance is for concentration and mass, l.370), Ghirardini 2018 or 2019, or the file headers. No mass covariance is released.
- **Whether `EM_FORW` includes any systematic term**, and its confidence level in the file. Ettori l.113 implies statistical 1σ. The file is silent.
- **Definition of `MGAS_LO` and `MGAS_HI`** (1σ? statistical only?). Not stated in Eckert, Ghirardini 2019 or the FITS header.
- **Redshift uncertainty.** Not given in any of the papers or the headers.
- **How g_obs or g_bar scale with h or distance.** Not stated anywhere. Eckert l.54 says only "very mild dependence".
- **Effect of the abundance or μ assumption on gas mass**, as a number. Not stated.
- **Uncertainty on Ghizzardi's 0.75 projection factor.** Not stated.
- **Accuracy of Ettori's stellar prescription.** Ettori §5 (l.563–565) gives no error, no scatter and no validation. The only number is the sample "median $M_{\rm star}/ M_{\rm gas}$ of 0.09 (0.07--0.12 as 1st and 3rd quartile) at $R_{500}$" (l.565).
- **Whether Ettori's c = 2.9 refers to R200 or R500.** Ettori does not say. Lin defines it relative to r200 (arxiv.tex l.328–330).
- **Radial distribution of the ICL.** Not given.
- **Whether the A2319-pilot temperature systematics (X12) were propagated** in the 12-cluster analysis. Not stated in Ettori or Ghirardini 2019.
- **A separate size for asphericity.** Only the combined 10–30 % (X7) is given.

## Doubts

1. **Release headers disagree with Ettori Table 1** (which `convert.py` uses for TABLE1 and the modelled-star prescription). Of the clusters listed below, the hydro and gas headers match Ghirardini 2019 Table 1 for A2029 and A2142, and Eckert Table 2 for A2029; I did not cross-check the other values.
   - A2029: z 0.0766 against 0.0773; R500 1414 against 1423 kpc; M500 8.65 against 8.82.
   - A2142: z 0.09 against 0.0909.
   - A3158: z 0.059 against 0.0597.
   - A644: R500 1250 against 1230; M500 5.94 against 5.66.
   - A2319: R500 1368 against 1346; M500 7.68 against 7.31.
   - The converter uses the header R500 for gas radii but Table 1 values for the model-star normalisation.
2. **MSTAR_SMOOTHED radii for A2319 and A644** are the RAW r/R500 grid multiplied by Ettori's Table 1 R500 (1346 and 1230 kpc), not by the header R500 (1368 and 1250). Checked: the maximum smoothed radius divided by the maximum RAW r/R500 gives 1346.0 and 1230.0 exactly.
3. **The released stellar profiles appear to be projected (cylindrical), not spherical.** This is an inference, but the evidence is strong. MSTAR_SMOOTHED at R500 multiplied by 0.75 reproduces Ghizzardi's Table M_star,500 for 6 of 7 clusters:
   - A1795 2.99 against 3.02; A2029 6.59 against 6.51; A2142 6.93 against 6.97; A2319 5.21 against 5.11; A85 2.21 against 2.10; ZW1215 3.20 against 3.34.
   - A644 does not match: 4.18 against 3.70.
   - Ghizzardi l.715 says the profiles integrate "within a projected radius". The table errors are also about 0.75 times the smoothed half-width.
   - SOURCE.md treats MSTAR as M(<r) without comment.
4. **That the smoothed total equals the stat and CV parts in quadrature** is my inference from values at R500. The source says only "total uncertainties". The smoothed bounds are symmetric even where the RAW offsets are not (A2029: quadrature gives 7.1e11 below and 5.8e11 above; the smoothed file gives 6.4e11 each way).
5. **The released gas mass at the header R500 is 7–10 % lower than Ghizzardi's Table M_gas,500** for 9 of 12 clusters (ratios 0.90–0.94; A2142 0.95, A3266 0.97, A644 0.96, A2319 1.00). I could not explain this from the sources. The particle-density conversions also differ between papers:
   - Ettori "$n_{\rm e} + n_{\rm p} \approx 1.83 n_{\rm e}$" (l.173);
   - Eckert $n_e=1.17n_p$, μ = 0.61 (l.84);
   - Ghirardini $n_e=1.17n_H$ (l.201);
   - Ghizzardi "$n_{\rm gas}= … = 2.21 n_{\rm H}$" (l.529).
6. **Ettori gives two ranges for the combined bias:** 10–30 % (l.449) and 10–20 % (l.610).
7. **Units of σ_MHE|M:** the text gives 0.15 ± 0.08 with no unit. The abstract says "0.15 dex", and "less than 10% (i.e. $<0.043$)" (l.393) implies log10 units, so roughly 40 %.
8. **The Gonzalez slope is not unique within the paper.**
   - The table gives −0.84 ± 0.04 (l.1035).
   - The summary gives "$M_{\star,3D}/M_{gas}\propto M_{500}^{-0.82\pm 0.05}$" (l.1551).
   - The Planck-cosmology appendix gives a = 0.387 ± 0.002 and b = −0.81 ± 0.05 (l.1755).
   - Ettori's 0.39 and −0.84 match the WMAP7 table (H0 = 70.2, Ωm = 0.275, l.252), not X-COP's H0 = 70, Ωm = 0.3.
9. **Measured and modelled stars are different quantities.**
   - Gonzalez includes BCG + ICL (abstract l.88–93) and applies the c = 2.9 deprojection only to galaxies, with "no correction to the more compact BCG+ICL" (l.1268–1269).
   - Ghizzardi excludes ICL.
   - Ettori applies an NFW shape to all stellar mass (my inference: §5 states no exception).
   - Lin's c_g describes galaxy number density, "the BCGs are excluded" (l.356).
10. **Mass-range extrapolation.** The Gonzalez sample spans "$M=1-5\times10^{14}$" (l.76; Table l.630–641: 0.95–5.15e14). The modelled X-COP clusters have M500 of 3.48–8.80e14, so A2255 and A3266 lie above that range. This is an observation; no source states its consequence.
11. **`M_FORW` decreases with radius** for A3158 (r ≥ 2166 kpc) and A644 (r ≥ 1129 kpc). For A644, `M_FORW` at R500 is 17 % below `M_NFW`. An enclosed mass that falls with radius is unphysical. A644's gas range reaches 2.13 R500, so some of these rows may lie in the converted range (inference; not checked against the shipped tables).
12. **Smaller oddities in the release:**
    - The hydro file has `EM_HER` but no `M_HER` column.
    - The A644 RAW `MSTAR_HI` offset is negative at one or more radii (minimum −0.9 % of `MSTAR`).
    - The header `ERR_M500` is larger than `EM_NFW` at R500 (for A85, 0.178 against 0.128). My inference: the header error includes the R500 uncertainty, while the column is at fixed radius.
13. **Correlation across radii.** Every hydrostatic and gas profile comes from one smooth fit per cluster (Ettori l.219–222; Ghirardini 2018 l.605–608). The released one-column errors are therefore almost certainly correlated across radii. This is an inference; the size of the correlation is not stated.
14. **Lost asymmetry.** Ettori quotes asymmetric errors (for example c200), but the released `EM_FORW` is a single symmetric column, so any asymmetry is lost.
15. **A commented-out passage in Ghizzardi** (xcop-metallicity.tex l.752, not in the published text) says Gonzalez's dynamical mass-to-light ratios "might be biased high by up to 30\%". I report it only as a pointer, not as a source statement.
16. **Versions.** I read the arXiv versions listed above, not the published A&A versions. Any differences were not checked.

I have no new items to suggest for memory.