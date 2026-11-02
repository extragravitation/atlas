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
