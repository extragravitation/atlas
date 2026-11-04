# Dwarf galaxies, Reader B (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Reader B: Dwarf galaxies (`aeg-d-dwarfs/v1`), step A uncertainty reading

**Reader:** Reader B · **Dataset:** Dwarf galaxies (`aeg-d-dwarfs/v1`) · **Date:** 2026-11-04
**Work directory:** `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/step-a-2026-11-04/dwarfs-B/` (each e-print is in `dl/<id>/`, extracted to `dl/<id>/x/`). Nothing in `/home/claude/atlas` was modified, and no other reader's directory was opened.

## Header: sources read

### Package files (read-only)
All under `data/packages/aeg-d-dwarfs/v1/`:
- `REPRODUCTION.md`, `convert.py`, `descriptor.json`, `datapackage.json` (columns), `sources.json`
- `reproduction/inputs.py`, `reproduction/upsilon.py`, `reproduction/gas.py`
- `reading/conversion_inputs.csv`: read only to find which originals supply most rows and which error fields exist
- `tables/` column names; counts of populated error fields in `tables/observables.ecsv`

Also read:
- `data/assumptions.json`: the `dw_*` and `helium_factor` entries
- `docs/decisions.md`: D-025, D-034 to D-039, D-042, D-045, D-046, D-048, D-051 to D-065

### Original sources
Each e-print was fetched from `arxiv.org/e-print/<id>`, which serves the latest version. The version is taken from the `arxiv.org/abs` page. SHA-256 is of the downloaded e-print file.

| Source | arXiv id, version | Main .tex | e-print SHA-256 |
|---|---|---|---|
| Pace 2024/25, LVDB | 2411.07424 v2 | main.tex | 1b864a9533590fe0976778a22e27acb682f6a21db912813cd5dbeb743fb5915f |
| Wolf et al. 2010 | 0908.2995 v6 | ms-mn2e.tex | 6852fe7e0248278947158c37c30132610c1c4ac4c347448f232e65d78b1bbd94 |
| McLaughlin & van der Marel 2005 | astro-ph/0605132 v1 | mclaughlin_vandermarel.tex | af94cbcf14303090df2ab51ddd864235731d3378d9ba309638da8edf4a431b96 |
| Putman et al. 2021 | 2101.07809 v1 | main.tex, table1.tex | 6382f5293ed3849d9e6db0c885bd6d31821891892920d59998bbd4a858d43fc9 |
| Lelli, McGaugh & Schombert 2016 (helium) | 1606.09251 v1 | SPARC.tex | 792903260765acbb0d2ed5df47bc8f99f97e24da0911527393db7243888bc7fc |
| Woo, Courteau & Dekel 2008 | 0807.1331 v2 | lgmn.tex | 7331f6cfb4154b72984c1b0a53873d8de265c67eab2356bf0dc595762da50fcb |
| Geha et al. 2026 (σ, 20 rows) | 2602.10200 v2 | main.tex | 60461d02dad7af3a17e6b8acc5a84187ef12f076be9cbe9485013906e98c1437 |
| Collins et al. 2013 (σ, 12 rows) | 1302.6590 v1 | M31dsphsv3.tex | bafcfadd98707763034bda8a9e710143bda8e2193cd0378e6ab6762856e7d098 |
| Tollerud et al. 2012 (σ, 9 rows) | 1112.1067 v3 | splashdwarfs1.tex | 082ab431593daf756a635cb17063c3fd1b144f9f60920e49e5da94afef6fdc9e |
| Fritz et al. 2019 (σ, 2 rows) | 1805.07350 v4 | spec_v1_ref1_arx.tex | 41cad1cdfcbbff0901afbbe9e8b3212c1c861d52e53ea2c6e35887b311e5dc90 |
| Simon et al. 2020 (σ method; Tuc V structure, distance, M_V) | 1911.08493 v2 | ms.tex, tuc5_table_y3a2.tex | d0e56936b775b4ba836b174c441924a45917564755feacafb8eff7bc5605eef7 |
| Martin et al. 2016 (structure 19, m_V,0 ~19) | 1610.01158 v1 | ms.tex | 7585942eef8853bd4c4f5dfae9d3d5a675933c0eefe36ec29f6ae57d35b15b2e |
| Muñoz et al. 2018 (structure 19, M_V 20) | 1806.06891 v1 | ms.tex | 36252e479d0ad3ebd05a5c52f22e342fbfaec8e981f972f7234b01b563d6c834 |
| Higgs et al. 2021 (structure, distance) | 2101.03189 v1 | mnras_template.tex | 0dea93b88b1eb5459f5e27e5824b355581fca8708cf2385c62ddb58e3971b3dc |
| Carlin et al. 2017 (structure, distance, M_V) | 1710.06444 v1 | coli_triii_arxiv.tex | d7732055ed36749257de531a59a4d54762bd11484bd203379e877ab0171f76d9 |
| Richstein et al. 2024 (structure, m_V) | 2402.08731 v1 | arxiv.tex, derivedTable.tex | 36d54675b1fb78b600dc248d1f88572cf83583ac7c3121620297e4d9d0decd42 |
| Savino et al. 2022 (distance, 21 rows) | 2206.02801 v2 | main.tex | edd8826b1d6ef9ae7f3dd4a56a47c89f06f6d1fe6aaf79f44e4ea9d0b64bcce1 |
| Medina et al. 2018 (distance, Leo IV/V) | 1802.01581 v1 | ms.tex | 3108c7bf5eafaea1b60eda8a3100b1bd35dd5234b914ce7e25d1de640e23e49b |
| Martínez-Vázquez et al. 2017 (distance) | 1710.09038 v1 | ms_arxiv.tex | 2896fb21d489d24d4904d00e8350f3561405bf13eb2085c4eb804b8812f47139 |

### Sample stated per input type
- **σ:** Geha 2026, Collins 2013, Tollerud 2012 and Fritz 2019, which together supply 43 of 64 plotted rows, plus Simon 2020. Simon 2020 was read for method only: its σ values are not among the plotted rows, because Tuc V's σ comes from Hansen 2024.
- **Structure:** Martin 2016, Muñoz 2018, Higgs 2021, Carlin 2017, Richstein 2024 (and Simon 2020).
- **Distance:** Savino 2022, Carlin 2017, Medina 2018, Martínez-Vázquez 2017, Higgs 2021.
- **Photometry:** Martin 2016, Muñoz 2018, Carlin 2017, Richstein 2024, Simon 2020.

Line numbers below are lines of the main .tex file named in the header table.

## Table of uncertainty terms

"Pt=sys" means point and system coincide, because there is one value per system.

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| D1 | σ statistical error | "If resolved, we quote the 1-sigma errors of the posterior distributions." / "the Hessian is computed at this maximum, and inverted to obtain the covariance matrix" | Geha 2602.10200 l.741; Tollerud 1112.1067 l.352; Collins Table 4 (l.1630ff) | Per system as printed, e.g. And V "12.2^{+2.5}_{-1.9}" (Collins l.1630) | Pt=sys | g_obs (∝σ²) | Yes: `measurements.x_dwarfs_sigma_err_lo/hi`, `g_obs_err_lo/hi`; `observables` sigma_los `err_lo/err_hi` |
| D2 | Upper-limit confidence level (differs between sources) | "we report only an upper limit on the velocity dispersion as the 95th percentile of the posterior distribution" / "upper limits (defined as the values at the 90-th percentile of the distributions)" / "where the upper bound is determined from the formal $1\sigma$ confidence interval" / "Upper limits listed here are at 95.5\% confidence" | Geha l.741; Fritz 1805.07350 l.388; Collins l.1063; Simon 2020 tuc5_table l.41 | 95th pct; 90th pct; 1σ; 95.5%; 90% (Simon l.561) | Pt=sys; mixed levels across the dataset | g_obs (limit) | Yes: `measurements.limit`, `x_dwarfs_sigma_limit_level` |
| D3 | Per-star velocity-error calibration (scale factor and floor) | "we infer $k_v$ = 1.4 and $\sigma_{v,\rm floor} = 1.1$\kms" / "Underestimating (overestimating) velocity errors for individual stars translates directly into larger (smaller) values of the internal velocity dispersions" | Geha l.420, l.402 | k_v 1.4; floor 1.1 km/s (Geha). Tollerud "additional systematic error component of 2.2 \kps" (l.268). Simon 2020 "1.2~\kms … 1.0~\kms" (l.344–346). Collins "Typically our velocity uncertainties lie in the range of $5-15\kms$" (l.457); slit misalignment "up to $\sim15\kms$" (l.508) | Dataset subset: shared by all systems from one pipeline | g_obs; direction stated by Geha: errors underestimated → σ larger | No (inside the published σ) |
| D4 | Unresolved binary stars | "can have incorrect inferred velocity dispersions if there are unidentified binary stars included" / "Including non-member stars or undetected binary stars will inflate, but sometimes deflate" / "This assumption of Gaussianity would be violated if there is significant contamination from unresolved binaries" | Pace 2411.07424 l.518; Geha l.739; Tollerud l.339; Simon 2020 l.607 | Not stated per system. Geha: restricting repeats to <30 d "reduces the inferred velocity error floor by 20\%", attributed to "undetected binary stars" (l.420). Collins 2013: no mention (0 hits) | Pt=sys | g_obs, usually up (Geha: "sometimes deflate") | No column found in v1 tables |
| D5 | Membership and contamination | "filtering outliers that are true members … will serve to incorrectly \emph{decrease} the inferred dispersions" with footnote "can bias the velocity dispersion at the few-percent level" / "we impose a subjective membership threshold of $P_{\rm mem} > 0.5$" | Tollerud l.323–325; Geha l.636; Tollerud Table note "*" l.468; Collins η "values of $\eta\sim2-4$" l.754 | "few-percent level" (Tollerud, clipping only). Fritz Phx II: 9.5^{+6.8}_{-4.4} (all possible members, l.446) vs 11.0^{+9.4}_{-5.3} (certain members, bold "prefer", l.452, l.436) | Pt=sys | g_obs; contaminants inflate, clipping deflates (Tollerud) | No |
| D6 | Radial coverage (aperture) and the flat-profile assumption | "We determine the internal velocity dispersion for each system using member stars ($P_{\rm mem\_novar} =1$) within two half-light radii." / "Equation \ref{eq:main} is not able to capture the full uncertainty on the half-light mass in cases where the kinematic data does not constrain $\sigmalos$ beyond $\Rhalf$." / "adding an error of 0.05 dex to the propagated mass error provides a reasonable means to allow for a range of $\beta$ profiles" | Geha l.743; Wolf 0908.2995 l.956, l.974; Fritz members "contained within 2.1 R$_\mathrm{half}$" l.344; Collins l.1610 | 0.05 dex (Wolf, on mass) | Pt=sys | g_obs | No (D-051 coverage pass/fail in `reading/`, not an error column) |
| D7 | Member-sample σ taken as the luminosity-weighted σ² | "$\avelos$ is the luminosity-weighted square of the line-of-sight velocity dispersion" / "we assume our measured values of $\sigma_v$ are representative of the luminosity-averaged velocity dispersion" | Wolf l.89; Collins l.1606 | Not stated | Dataset (method) | g_obs | No. The D-038 1A named assumption is absent from the v1 `assumptions` string |
| D8 | Rotation and velocity gradients | "The current stellar kinematic setup assumes a system has a constant velocity dispersion and no rotation." | Pace l.700; Collins mask-gradient "average end-to-end mask difference of 2.6$\kms$" l.571–574 | Not stated for dwarfs; 2.6 km/s is an instrumental gradient (Collins) | Pt=sys | g_obs | No |
| D9 | Anisotropy and estimator normalisation | "The dashed lines indicate $\pm 10\%$ variation about the predicted relation." / errors "dominated by observational uncertainties rather than theoretical uncertainties associated with $\beta(r)$" | Wolf l.927, caption l.831; 0.05 dex l.974 | ±10% (classical dSphs); +0.05 dex for general β | Dataset | g_obs | Named only: `measurements.assumptions` → `dw_equilibrium` (no size) |
| D10 | Equilibrium and sphericity | "under the assumption of dynamical equilibrium with no streaming motions" / "I use the azimuthally-averaged half-light radius to approximate spherical symmetry as most dwarf galaxies are non-spherical." / "have been significantly altered by tides" | Wolf l.274; Pace l.460; Collins l.180 | Not stated | Dataset (or system where tides apply) | g_obs (and r½) | Named: `dw_equilibrium`; no size |
| D11 | 2D→3D factor r½ = 4/3 R_h | "This approximation is accurate to better than 2\% for exponential, Gaussian, King, Plummer, and S\'ersic profiles" | Wolf l.152; Appendix table l.1797 (Plummer 1.305; exponential 1.329; Sérsic n=8 1.352) | <2%; tabulated 1.305–1.352. Tollerud uses "$r_{1/2} = 1.315 \, \Reff$" (l.943) | Dataset | Both (g_obs ∝ 1/r½; g_bar ∝ 1/r½²) | Named: `dw_rhalf_wolf`; no size |
| D12 | R_h measurement error | "lists the median of the distributions and the limits of their central 68\% confidence interval" / "we carry out 10\,000 bootstrap realizations" | Martin 1610.01158 l.387; Muñoz 1806.06891 l.369–374; Simon 2020 tuc5 l.22 "$2.1^{+0.6}_{-0.4}$" | Per system, e.g. Muñoz Hydra II 1.65±0.39′ (l.2506) | Pt=sys | Both | No: `observables` half_light_radius has no error in 64/64 rows |
| D13 | Ellipticity error; ε and PA varying with radius | "Some galaxies show changes in the position angle and/or ellipticity with radius and the current LVDB format does not account for this." | Pace l.699; e.g. Martin And XIII "$\epsilon = 0.61^{+0.14}_{-0.20}$" l.579 | Per system as printed | Pt=sys | Both (through R_h = a√(1−ε)) | No: `observables` structural_param has no error |
| D14 | r_h convention (semi-major vs circularised) | "much of the past literature … reporting structural parameters has used $r_h$ when referring to the elliptical half-light radius, though $r_h$ has also been used to report azimuthally-averaged half-light radius values" | Richstein 2402.08731 l.295; Muñoz l.260 ("the radius, $r_{\rm h}$, containing half the luminosity"; axis not named) | Factor √(1−ε) (formula); not stated by the source | Pt=sys | Both | Flag only: `x_dwarfs_flags` `rh_semimajor_assumed`; no effect column |
| D15 | Choice of profile family | "neither of the three types of profiles actually accounts for the complexity of the brighter dwarf galaxies" | Martin l.340; Muñoz Table 3 l.2506 (Hydra II exp 1.65±0.39, Plummer 1.52±0.28) | Not stated as an uncertainty | Pt=sys | Both | No (one fit in tables) |
| D16 | Tracer, population gradient and field-of-view systematics on R_h | "What we really determine here is the half-density radius … under the assumption that a system harbors uniform stellar populations and does not suffer from mass segregation, this quantity is equivalent" / "there is a difference between the half-light radius of a galaxy, and a half-mass radius" / "observations covering a large field of view (FOV; $>$3 times the galaxy half-light radius)" | Martin l.280; Higgs 2101.03189 l.640; Richstein l.277; Muñoz l.266; Pace l.472 | Not stated | Pt=sys | Both | No |
| D17 | Distance statistical error | "the respective uncertainties (15.9th and 84.1th percentiles of the PPD)" / "The median precision of our distances is 21~kpc (2.9\%)" | Savino 2206.02801 l.920, l.1119; Carlin "$m-M = 21.31\pm0.11$" l.114; Medina "$151.4 \pm 4.4$\,kpc" l.370; MV17 "statistical uncertainties $<$ 0.11 mag" l.166 | Per system; median 2.9%, max 3.9% (Savino) | Pt=sys | **Both by formula.** By the package's own formulas: g_obs ∝ D⁻¹, while stellar g_bar is independent of D (see Doubts 1); Boötes III g_bar ∝ D⁻² | Partly: `observables` distance `err_lo/err_hi` (62/64 rows); not propagated into `g_obs_err`/`g_bar_err` |
| D18 | Distance-scale calibration and zero point | "Retaining the M15 original distance scale systematically increases the measured distance by a median of 0.073~mag" / "resulted in a maximum systematic variation of 3.4\% … systematic differences are generally contained within 0.1 mag" | Savino l.988, l.1114; MV17 "systematic uncertainties of 0.08 mag" l.166; Carlin "assuming a distance modulus of $m-M=15.39$ to NGC~7078" l.114; Higgs TRGB "$i_{o,MP9703} = -3.49$" l.361; Fritz adds "0.1 mag as saveguard against systematic errors" l.137 | 0.073 mag; ≤3.4%; ≤0.1 mag; 0.08 mag | Dataset subset (shared by all systems on one calibration; Savino covers 21 rows) | As D17 | No |
| D19 | Metallicity assumed for the RR Lyrae | "the dominant source of random uncertainties is the unknown metallicity of the RR Lyrae, which limits precision to roughly 0.05 magnitudes" / "would introduce a systematic error in the distance modulus estimates, at the level of $\sim$0.2 mag" | Savino l.922; MV17 l.1079–1080; Medina "fractional difference in heliocentric distances of $1.8\%$" l.266 | 0.05 mag; ~0.2 mag per 1 dex; 1.8% per 0.5 dex | Pt=sys | As D17 | Inside Savino's printed error only |
| D20 | TRGB bias in faint systems | "the TRGB distance is systematically larger than inferred through the RR Lyrae … (up to 0.7 mag, or $\sim 35\%$ distance difference, for $M^{\rm eff}_V \approx -6$)" | Savino l.1030 | Up to 0.7 mag | Pt=sys (TRGB rows) | As D17; TRGB too far | No |
| D21 | Mixed distance bases inside the magnitude | "we start by drawing a distance modulus from the distance MCMC chains of \citet{aconn12}" | Martin l.377 (m_V,0 modelled at Conn 2012 distances; package distance is Savino); Muñoz M_V rebuilt with Table 1 R_⊙ (no error column, l.2194ff) | Not stated | Pt=sys | g_bar | Flags `mv_distance_from_table1`, `mv_modulus_assumed` in `x_dwarfs_flags` |
| D22 | Distance inherited from host | "There are a number of systems without an independent distance measurement and they inherit the distance and errors of their host galaxy." | Pace l.704 | Not stated | System | As D17 | `REPRODUCTION.md` names a `distance_inherited` flag; none seen in plotted rows' flags |
| D23 | Magnitude photometric and shot-noise error | "These typically yield uncertainties of $\pm0.2$ and we therefore add a Gaussian random deviate of width 0.2" / "use the distribution of magnitudes to estimate 1-$\sigma$ errors" / "This accounts for the effects of CMD shot-noise." | Martin l.381; Muñoz l.437 (shot noise l.389); Carlin l.159; Richstein l.314 | Per system; Martin's includes 0.2 mag completeness | Pt=sys | g_bar (brighter → larger) | Yes: `observables` apparent_magnitude err (63/63); `measurements.g_bar_err_lo/hi` ("From the magnitude error only") |
| D24 | Population and IMF assumed in the luminosity (missing light) | "assuming that And~I is instead entirely composed of an 8-Gyr stellar population does lead to magnitudes that are systematically brighter by $\sim0.2$ magnitudes" / "assuming a Salpeter initial mass function" / "our integrated magnitudes may be biased fainter by at most $\sim0.1$ mag" | Martin l.385 (Chabrier LF l.377); Muñoz l.416, l.407; Carlin broken power-law IMF l.159; Richstein l.316 | ~0.2 mag (age); ≤0.1 mag, "1--10\%… average of $\sim3\%$" (Richstein) | Dataset subset (per photometry source) | g_bar (younger or complete → brighter → larger) | No |
| D25 | Foreground extinction correction | "reddened by the relevant amount of extinction measured from \citet{schlegel98} as recalibrated by \citet{schlafly11}" / "No corrections are applied for extinction internal to the dwarfs." / "The extinction correction is adopted from the literature source." | Martin l.377; Higgs l.222; Pace l.800; Carlin l.104; Richstein l.272 | Not stated (none of the sources read) | Pt=sys | g_bar | No |
| D26 | Solar absolute V magnitude | "solar absolute magnitude $M_{V,\odot}=+4.85$" vs "Assuming a $V-$band absolute magnitude for the Sun of +4.83" | MvdM l.2161; Carlin l.177; Richstein l.326 ("Solar $M_V=4.83$") | 4.85 vs 4.83; no error stated | Dataset | g_bar | Fixed: `x_dwarfs_l_v` description "M_V,sun = 4.85"; no range |
| D27 | Band transformation to V | "which we convert to the $V$ band with the color equations given in section~2.2 of \citet{ibata07}" | Martin l.379; Richstein l.309 (Sirianni 2005 / Harris 2018) | Not stated | Dataset subset | g_bar | No |
| D28 | Υ_V model error from age and [Fe/H] | "All uncertainties on the population-synthesis quantities in Table \ref{tab:poptable} follow directly from uncertainties in the cluster ages and [Fe/H] values" | MvdM l.1506; e.g. MW-1636-283 "$ 1.888\pm0.155$" l.3497 | ~±0.15 per tabulated cluster | Dataset (model table) | g_bar | Yes, as an envelope: `x_dwarfs_upsilon_v_low/high` (uses e1, e2) |
| D29 | IMF | "The Salpeter IMF gives $\Upsilon_V$ consistently higher than the Chabrier disk IMF (by factors of $\sim60\%-75\%$)" | MvdM l.1422–1425; Chabrier disk adopted l.1250 | +60–75% | Dataset | g_bar (Salpeter → up) | `x_dwarfs_upsilon_v_high` ((M/L)₂ Salpeter ×1.10) |
| D30 | Population-synthesis code | "these differences are generally slight: at the level of $\la 0.05$ mag in $(B-V)_0$ and $\la 10\%$ in $\Upsilon_V$" | MvdM l.1359 | ≲10% | Dataset | g_bar | Factors 0.90 / 1.10 inside low/high |
| D31 | Υ from star-formation history vs colour | Table 2 dE V-band: SFH 1.6, BdJ 1.3 / "Sampling and systematic errors in the SFH's are not easily estimated." / "The typical uncertainty: \elogMs dex" (= 0.17) | Woo 0807.1331 l.736 (macros l.145, l.148), l.643, l.512 | 1.6 vs 1.3; 0.17 dex in log M★ | Dataset | g_bar | Factor 0.81 in `x_dwarfs_upsilon_v_low`; Woo values as `observables` star_formation_history_ml (15 rows, no error) |
| D32 | Single-age burst at 13±2 Gyr | "we {\it always} assume that every cluster is a single-age population formed instantaneously" / "assigned a single age of $13\pm2$ Gyr to all clusters" | MvdM l.1260, l.1491 | ±2 Gyr (inside e(M/L)) | Dataset | g_bar | Through e1/e2 in low/high only |
| D33 | [Fe/H] input to Υ_V | "The tail towards higher $\Upsilon_V^{\rm pop}$ values … is a direct reflection of the metal-rich (bulge-cluster) tail" / "Most observed metallicity distributions are generally non-Gaussian and skewed … most dwarf galaxies have radial metallicity gradients" | MvdM l.1519–1520; Pace l.701 | Per system [Fe/H] error or spread | Pt=sys | g_bar (higher [Fe/H] → higher Υ) | `observables` metallicity_feh `err_lo/hi` (62/64); enters low/high via ±s |
| D34 | [Fe/H] below the lowest tabulated value (−2.29) | (Package rule; MvdM's table has no clusters below this) | `upsilon.py` docstring; D-060 item 5 | Not stated by source | Pt=sys | g_bar | Flag `beyond_source_range` in `measurements.flags` |
| D35 | Stellar mass loss and remnants in the SSP | "a $\sim30\%$ cumulative effect over a Hubble time" (mass loss through massive-star ejecta, included in their models) | MvdM l.1568 | ~30% | Dataset | g_bar | No (inside the model) |
| D36 | Helium factor | "We assume a thin disk with a total mass of 1.33~$M_{\hi}$, where the factor 1.33 considers the contribution of helium." | Lelli 1606.09251 l.199 | 1.33; error not stated | Dataset | g_bar (gas) | Fixed: `g_bar_gas_cold` and `x_dwarfs_m_gas_rh` descriptions; `helium_factor` not adjustable |
| D37 | HI mass error | "The errors are from the distance errors shown." / "Errors on the mass limits are given based on the distance errors." | Putman table1.tex l.8; main.tex l.176 | Leo T "$2.8^{\pm0.4}\times 10^ {5}$"; Phoenix "$1.2^{\pm0.1}\times 10^ {5}$" (table1 l.116–117) | Pt=sys | g_bar (2 systems) | No: `observables` mass_hi has no error; `x_dwarfs_m_gas_rh` has none |
| D38 | HI detection adopted, not remeasured; association | "we did not remeasure the HI masses and largely adopted values from the references in M12" / "The Phoenix dwarf galaxy was considered highly uncertain as well" | Putman l.182, l.184; table1 note (22) l.27 | Not stated | Pt=sys | g_bar | No |
| D39 | HI upper limits (5σ, fixed 10 km/s width) | "$5\sigma$ HI mass limits are quoted … calculated using a velocity width of 10~\kms" / "it does assume the HI is more centrally concentrated" | Putman l.176, l.166 | 5σ | Pt=sys | g_bar (no gas is added; status only) | `observables` mass_gas_limit (limit=upper); `x_dwarfs_gas_status` |
| D40 | Gas inside r½ = ½ total | (No source statement; Putman Table 1 gives totals only) | `REPRODUCTION.md` (Gas); `gas.py` | Not stated | Pt=sys | g_bar | Flag `gas_half_total`; assumption `dw_gas_half_total` |
| D41 | Molecular, ionised and hot gas | descriptor: "No per-system source read for v1" | `descriptor.json` x_baryon_inventory | Not stated | Dataset | g_bar (would raise it if present) | `gas_hot_status`="absent"; molecular and ionised not in tables |
| D42 | Heterogeneity of the compiled originals | "Due to this inhomogeneity, there will be systematics in the LVDB" / "there may be some systematics in the structural parameters between near (resolved stars) and far (integrated light)" | Pace l.694, l.472 | Not stated | Dataset | Both | No |

### Terms that move g_obs and g_bar together
- Distance: D17 to D22. Doubts 1 gives the arithmetic for how it actually acts.
- R_h, ε, r_h convention, profile family and tracer: D12 to D16.
- The 4/3 factor: D11.

For every system, point and system coincide for D1–D2, D4–D6, D8, D12–D17, D19–D21, D23, D25, D33 and D37–D39.

## Not stated

Things I looked for and did not find:
- **Extinction:** no size of the E(B−V) or A_V uncertainty in Martin 2016, Carlin 2017, Richstein 2024, Higgs 2021 or Muñoz 2018. Muñoz 2018 does not state its extinction method at all (greps for extinct/redden/Schlegel/Schlafly hit only the cluster-specific Palomar 2 text). Savino's sentence on the extinction-law systematic ("below 0.02~mag", l.733) is a LaTeX comment and is **not** in the printed paper.
- **Binary inflation:** no size per system in Geha, Tollerud, Pace or Simon 2020. Collins 2013 has no binary treatment or statement anywhere.
- **Flattening:** no size of the error the Wolf estimator takes from flattening or non-sphericity. Wolf l.1981 only defers non-spherical models to "Future investigations".
- **Rotation:** no size of rotational support for the packaged dwarfs in the σ papers read.
- **Helium factor:** no uncertainty in Lelli 2016 §2.4 (l.199).
- **Solar M_V:** no uncertainty in MvdM 2005 (cited "e.g., lan99") or in Carlin or Richstein.
- **Muñoz 2018 distances:** Table 1 has no distance-error column. The description of how its M_V errors were derived (l.432–437) names only the luminosity-function sampling; whether distance error is included is not stated.
- **Gas inside r½:** no source gives the fraction of HI inside r½ (Putman gives totals).
- **Molecular and ionised gas:** no per-system source in the package.
- **Υ_V for dwarfs:** MvdM's uncertainties are for single-burst clusters. No dwarf-specific (extended star-formation history) Υ uncertainty is stated there.
- **Carlin 2017 M_V error:** what it contains beyond shot noise is not stated.

## Doubts

1. **Inference (arithmetic from the package's own formulas): distance does not move stellar g_bar.**
   - R_h(phys) = θ·D, so g_obs ∝ D⁻¹.
   - L_V = 10^(−0.4(m_V,0 − μ − 4.85)) ∝ D², so g_bar,stars ∝ L/r½² ∝ D⁰. Gas rescaled by D-058 also scales ∝ D⁰.
   - Checked numerically on andromeda_01: D×1.1 gives g_obs×0.909 and g_bar×1.000.
   - **Exception:** Boötes III (L_V from a distance-independent M_V, D-061 item 2), where g_bar ∝ D⁻².
   - So for 63 of 64 rows a distance error shifts only g_obs (a vertical shift), and the ratio g_obs/g_bar ∝ D⁻¹.
   - `data/assumptions.json` `dw_distance` says "Enters g_obs and g_bar together". Both distance enters both formulas and g_bar cancels are true; how the error is drawn depends on which reading is meant.
2. **Fritz 2019, Phoenix II.** The package uses σ = 9.5 (+6.8/−4.4), which is the abstract value and the Table 4 "all possible members" row (l.446). The table marks in bold the "certain members" value 11.0 (+9.4/−5.3) as preferred (l.436, l.452), and §5 calls it "the preferred membership selection" (l.546). This is a membership term (D5) whose size the source shows. It needs the third party.
3. **Geha 2026 σ comes from members "within two half-light radii"** (l.743): an aperture-limited sample. Whether Wolf's "+0.05 dex" (l.974) applies is a judgement, not a quote. Wolf's 0.05 dex is on mass. Saying it is the same fractional term on g_obs at fixed r½ is my inference.
4. **The 4/3 factor differs between sources.** Wolf tabulates 1.305–1.352 (exponential 1.329); Tollerud uses 1.315; the Atlas uses 4/3.
5. **Solar M_V: 4.85 (MvdM, adopted) vs 4.83 (Carlin, Richstein).** The difference is 0.02 mag, about 1.9% in L (my arithmetic). For Richstein and Carlin rows the package rebuilds L from magnitudes, not from their printed L_V, so their 4.83 does not enter. Noted only as a disagreement between sources.
6. **Martin 2016's m_V,0 is not distance-free.** It was modelled at distance moduli drawn from Conn 2012 (l.377), while the package distance is Savino 2022. How much of Martin's m_V,0 error is distance-driven is not stated (inference).
7. **Limit levels are mixed:** 95th percentile, 90th percentile, 90%, 95%, 95.5%, and a 1σ bound for And XII. They are plotted under one `limit = upper`, with the level kept in `x_dwarfs_sigma_limit_level`.
   - For And XII, Collins Table 4 prints only "$0.0^{+4.0}$" (l.1633).
   - The "formal 1σ" wording is stated for And XVIII (l.1063); I infer the same method applies to And XII.
8. **The IMF used in the luminosity modelling differs by source:** Chabrier (Martin), Salpeter (Muñoz), a Kroupa-like broken power law (Carlin). None states the effect on M_V. This is separate from the Υ_V IMF term (D29).
9. **TRGB in faint systems (Savino l.1030).** Two plotted rows take their distance from Higgs 2021, which uses TRGB (l.353, l.361). Whether those systems lie in Savino's unreliable regime (M_V^eff > −9.5) I did not check.
10. **g_bar_err rules differ by route.** For rows rebuilt via `MAG_OVERRIDE`, `inputs.py` adds the paper's modulus error in quadrature to the M_V error. For printed m_V,0 rows, only the m_V,0 error is used. A third party should check whether this is consistent with D17's cancellation (inference).
11. **D-025 2nd sub-choice** requires "a flag records whether the source states multi-epoch screening for binary stars". I found no such column or flag in the v1 `measurements` or `observables` columns. I did not search every reading file.
12. **D-038 1A named assumption** ("member-sample σ taken as representative of the light-weighted σ") is not among the nine names in `convert.py` `ASSUMPTIONS`.
13. **Collins 2013 uses a different estimator.** It applies Walker 2009 (μ = 580) and notes that "the mass tends to be slightly over-estimated the more embedded the stars are" (l.1601). That statement concerns their estimator, not Wolf's, and is recorded only as context.
14. **arXiv versions are the latest** returned by the e-print endpoint. They may differ from the versions of record. I did not check that the line-numbered text matches the journal versions.
15. **Simon 2020's σ values are not among the plotted rows.** It counts toward the σ sample as a method source only, so the σ sample has four originals with plotted values plus one method source.