# Globular clusters, Reader B (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Reader B: uncertainty terms for the globular-cluster dataset (`aeg-d-gc-baumgardt` v1)

**Reader:** B · **Date:** 2026-11-04 · **Work directory:** `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/step-a-2026-11-04/gc-B/`. Each download is in its own folder under `dl/`. I opened no other reader's directory.

**Summary.** I found 41 terms. Version 1 carries three of them as errors:
- the per-bin dispersion error, which feeds the `g_obs` error bars;
- the population M/L_V error, which feeds the `g_bar` error bars;
- the M/L_V range, through the Salpeter column and the slider.

It records but does not pass on the errors on R_h, W₀ and r₀. It carries nothing for distance, for magnitude, or for binaries, membership and rotation.

Two kinds of term move g_obs and g_bar together:
- **r½** (G20–G22): g_obs ∝ 1/r½ and g_bar ∝ 1/r½².
- **Distance** (G26–G30). The direction depends on the cause, which I inferred (Doubt 1):
  - an error in the horizontal-branch calibration or in V_HB moves R_Sun and M_V,t together, so g_bar is unchanged and only g_obs moves (∝ 1/D);
  - a reddening error moves R_Sun only, so g_obs ∝ 1/D and g_bar ∝ 1/D².

## Header: sources read

**Local package files.** These are under `/home/claude/atlas/data/packages/aeg-d-gc-baumgardt/v1/source/`. Each SHA-256 matches `sources.json`.

| File | SHA-256 |
|---|---|
| `veldis.html` | b1bf703280a33bf4988bbe94e291da1896611623860315e7e71e6c240e5b05de |
| `parameter.html` | c2e231374ba447d5153307c1018c1ea982f03706b813814a24209a32027bd225 |
| `appendix.html` | d6262d46887bd7385861a0b4c94e6017b2498ca3520bb0401e9ffe00ba68bd58 |
| `mwgc.dat` (Harris 2010 edition) | b457a690adc422fb2e8e05a23e1de50b62d1d5ac10dce99963c956c1b17ca658 |
| `mvdm05/J_ApJS_161_304_clusters.vot` | 282ea6daaaa9da0b690c3efd1384a12e83da9e664e939649896aea8d006dc7ec |
| `mvdm05/J_ApJS_161_304_models.vot` | 84647d34642e32734368961fa6a940d25b1f4db81fd797825a734e63c04e4e16 |
| `mvdm05/J_ApJS_161_304_table13.vot` | 42a6f2521bc5562b5e615a4c463cb6753fdc2b1f1a1f4831e31c71f3a2957b96 |
| `mvdm05/J_ApJS_161_304_table5.vot` | 3cbd17d7eea2f7ada1722fd7c7ec152639efcff23b664b027281df72628d14d7 |

I also read the two header lines of `rv/ngc6752.txt`.

**arXiv e-prints.** All are from `https://arxiv.org/e-print/<id>`. Hashes are of the downloaded e-print file.

| Paper | arXiv id and version | Main .tex | SHA-256 of e-print |
|---|---|---|---|
| Baumgardt & Hilker 2018 (BH18) | 1804.08359v2 | `vltpaper_ver6.tex` (+ `veldis_tab.tex`) | f52c50c561028ef86eae80b320de742ab2bf16cbcd64ff7a8c58a48eae1ed8ad |
| Baumgardt 2017 (B17) | 1609.08794v1 | `paper.tex` | 0e6dc3b76f52310a05d0ab61c090edf99c7f16c7635877844e7dfcfab415fb49 |
| Harris 2010 | 1012.3224v1 | `Harris.tex` | a250b8dcb55ba495c23d6ecae40c5c5bd77a6924201f5b5f232d5916d5f49ff4 |
| McLaughlin & van der Marel 2005 (MvdM05) | astro-ph/0605132v1 | `mclaughlin_vandermarel.tex` | af94cbcf14303090df2ab51ddd864235731d3378d9ba309638da8edf4a431b96 |
| Wolf et al. 2010 | 0908.2995v6 | `ms-mn2e.tex` | 6852fe7e0248278947158c37c30132610c1c4ac4c347448f232e65d78b1bbd94 |
| Kamann et al. 2018 (K18) | 1710.07257v1 | `muse_gc_kinematics_skamann.tex` | cdf9666eec5bc305fa162da26ee52bca2c9f2d6d0f2ab19e41a5dcdb1384718e |
| Lützgendorf et al. (L13) | 1212.3475v1 | `luetzgendorf_2012c.tex` | 91af3fa6deb1b2c00cfdfe180149fe8bd7c0defe3371de29572c88a14f309681 |
| Lützgendorf et al. 2015 (L15) | 1507.02813v1 (A&A 581, A1) | `6388ifu_paper.tex` | 22eeb020ec7fee4d4d158cb9ba411adf651a137015594a8779b3c747fb49fac8 |
| Olivares Carvajal et al. (C22) | 2204.06628 (latest is v1) | `CL001.tex` | 0cbeb6dc9fc9104e5bcc2d4cf6545e5ad1dd075ce3fa1645dbebd32a1602485c |
| Gran et al. (G22) | 2108.11922 (latest is v2) | `NewGCs.tex` | 097aa326d50dcbc1e51d42841d57c5c48b8aaabce21e9c528b923ee561957069 |
| Baumgardt & Vasiliev 2021 (BV21) | 2105.09526v2 | `paper.tex` | 406a18fad1cf251a1e3c46d2138acf3e33a5be70b4d3fceacdc3da6e821dc575 |
| Baumgardt, Sollima & Hilker 2020 (BSH20) | 2009.09611v1 | `paper.tex` | 0e1a2b34d587ba8dacfc0ddd243e534ac15e22c3ea4b72d0606b0340dcf636b2 |
| Kruijssen & Mieske 2009 (KM09) | 0903.4683v1 | `KruijssenMieske.tex` | 78d8184dcdf873425a39d5e662b7fff3d487052401e6bb69eee236ea1ec19109 |
| Chantereau et al. 2020 | 2002.02401v1 | `main.tex` | 3654a1411327c4737912f99d07f258861a2c2e2afc4f7906a2c6dd6c8a2bd854 |

**Atlas files read (read-only).**
- In the package: `REPRODUCTION.md`, `REPRODUCTION_RESULT.md`, `convert.py`, `analysis.py`, `descriptor.json`, `sources.json`, and the column names of the three tables.
- Elsewhere: `pipeline/aeg/dispersion.py`, `data/assumptions.json` (the `gc_*` entries), and `docs/decisions.md` D-025, D-036 to D-039, D-042 and D-045 to D-047.
- Not read: `datapackage.json`, and the body of `SECOND_READING.md` (headings only).

**Sample of original papers per input:**
- **σ:** B17, BH18, K18, L13 and L15, plus C22 and G22 for their dataset codes. Not read: F13 and D21.
- **Distance and luminosity:** Harris 2010, BV21, BSH20, and the statement about Harris in L13. This is fewer than five per-cluster originals. Harris's bibliography file could not be fetched (see Blocked).
- **Structure and Υ_V:** MvdM05, whose own fits are the original, and KM09.

**Blocked, not worked around:**
- `export.arxiv.org`, the arXiv search API (proxy 403). I found ids through `arxiv.org/search` and `arxiv.org/abs` instead.
- `physics.mcmaster.ca/~harris/mwgc.ref`, Harris's bibliography and calibration file (proxy 403).

## Terms

"In v1?" names the table and column. "obs." means the `observables` table and "meas." the `measurements` table.

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| G1 | σ per bin, statistical error (RV) | "the velocity dispersion together with the $1\sigma$ upper and lower error bars"; "The 1$\sigma$ lower and upper uncertainties of the velocity dispersion were calculated by determining the velocity dispersion where the likelihood is less than 0.5 the maximum value in each direction." | BH18 `veldis_tab.tex` l.2; B17 `paper.tex` l.295–296; `veldis.html` column heads "Δσ Up / Δσ Low [km/sec]" | Per bin, as printed | Point (bin). It becomes one system value through the light weighting. | g_obs | obs.`err_lo`/`err_hi` (sigma_los); meas.`x_gc_baumgardt_sigma_err_lo/hi`; meas.`g_obs_err_lo/hi` (σ only) |
| G2 | Error on each star's velocity | "The median uncertainty of an individual measurement is about 0.5 km/sec and 90\% of our stars have velocity errors of less than 2 km/sec … except for the lowest mass clusters in which the internal velocity dispersion is less than 1 km/sec." | BH18 `vltpaper_ver6.tex` l.191–193 | Median 0.5 km/s; 90% below 2 km/s | Point (star) | g_obs | Only inside G1 |
| G3 | Shifting datasets to a common mean velocity | "The necessary radial velocity shifts were usually less than 1 km/sec." | BH18 l.199 | < 1 km/s, typically | Dataset within a system | g_obs (direction not stated) | No |
| G4 | Binary inflation left after screening (RV) | "Stars where the individual measurements had a less than 5\% probability to be compatible with a constant radial velocity were removed"; Pal 13: "reduces the velocity dispersion by about 50\%"; "Undetected binaries might also be present in a few other low-mass and low density clusters like Arp~2 or Ter~3"; "On average each member star has 1.8 radial velocity measurements" | BH18 l.203, l.229–233; also l.464; `appendix.html` text | Pal 13 about 50%; others not stated | System | g_obs, upward (inflation) | No. D-025's binary flag is not among the v1 columns; meas.`flags` = `edges_inferred` only. |
| G5 | Binary inflation, simulated by K18 (NGC 6121) | "we overestimated the intrinsic velocity dispersion by $0.3\,{\rm km\,s^{-1}}$ and $0.6\,{\rm km\,s^{-1}}$ for binary fractions of 5\% and 10\%" | K18 l.330 | +0.3 and +0.6 km/s | System | g_obs, upward | No |
| G6 | Membership and contamination | "rejected all stars as binaries or background stars that deviated more than three standard deviations"; M54: "neglected all data points beyond 200'' in the dynamical analysis"; "non-members could be responsible for the higher than predicted velocity dispersion profiles seen in the outer parts of some clusters like NGC~1851" | B17 l.301, l.586–589; BH18 l.466 | Not stated | System | g_obs, upward | No. v1 uses all RV bins of NGC 6715, including 269″, 410″ and 679″, and NGC 6715 is plotted. |
| G7 | Tidal effects in the outer profile | "NGC~2298 and Pal~5 have velocity dispersion profiles which increase towards the outer parts … We therefore neglected the outermost data point"; "tidal fields, which increase the velocity dispersion of stars near the tidal radius" | BH18 l.226–228; B17 l.583–584 | Not stated | System | g_obs, upward | No. Both clusters are plotted with all bins. |
| G8 | Rotation: second moment versus dispersion | "the velocity dispersion $\sigma_{\rm r}$ is often equated with the central second velocity moment $V_{\rm rms}=\sqrt{\sigma_{\rm r}^2 + v_{\rm rot}^2}$" | K18 l.324; `parameter.html` key "A Rot: Rotation velocity", "P Rot" | Not stated for the `veldis` values | System | g_obs | No |
| G9 | Calibration of velocity errors | "Systematically underestimating the uncertainties would lead to an overestimate of the intrinsic velocity dispersion and vice versa." | K18 l.257 | Not stated | Dataset or system | g_obs | No (K18 is an alternative only) |
| G10 | Tracer mass and mass segregation | "the mass differences would correspond to a difference of $\lesssim5\%$ in the velocity dispersion"; "the dispersion increases towards lower masses" (NGC 3201); BH18 kept K18 clusters "with a high effective mass" | K18 l.344; BH18 l.184–187 | ≲ 5% for a 0.70–0.73 vs 0.85 M☉ tracer | System | g_obs | No |
| G11 | Integral-field and adaptive-optics biases (L13, L15, F13) | "For a measured velocity dispersion of about 13 km/s, an input velocity dispersion of about 25 km/s is required"; ARGUS innermost bin: "an uncertainty of more than 20 \%"; "the uncertainties in \citet{nora11} are underestimated"; NGC 1904: "the velocity dispersion drops the fainter the stars are … integrated light with $\sigma \sim 6 - 9$ km/s is most likely correct" | L15 l.293, l.255, l.279; L13 l.525 | SINFONI about ×0.5; ARGUS more than 20% | Point (bin) or system | g_obs (SINFONI biased low) | Alternatives only (L13, L15, F13; not plotted); printed errors in obs. |
| G12 | L13 integral-field error method | "The final value results from a quadratic summation of both errors" (Monte Carlo plus shot noise) | L13 l.423 | As printed | Point (bin) | g_obs | obs.`err_lo/hi` for L13 rows |
| G13 | K18 confidence level | "median values and the 16th and 84th percentiles" | K18 l.282 | 16th–84th percentiles | Point (bin) | g_obs | obs. errors for K18 rows (alternative) |
| G14 | Crowding | "contamination by background light tends to bias the measured radial velocities towards the cluster mean" | K18 l.326 | Not stated | Point (central bins) | g_obs, downward | No |
| G15 | Bin edges inferred by the Atlas | BH18 gives "the average distance of stars from the cluster centre". Atlas code: "edges are inferred at arithmetic midpoints between adjacent radii". | BH18 `veldis_tab.tex` l.2; `pipeline/aeg/dispersion.py` docstring | Not stated | System | g_obs (through the weights) | meas.`flags` = `edges_inferred`; no error |
| G16 | Light-model (King) parameter errors, not passed on | "Uncertainty in the structural model is not propagated (registered as a known limitation)"; MvdM: errors from "the subgrid of fits with $\chi^2\le \chi_{\rm min}^2+1$" | `dispersion.py` docstring; MvdM05 l.1901–1903 | Per cluster (`E_`/`e_` W0, r0) | System | g_obs (weights and coverage) | obs.`err_lo/hi` for W0/gamma and r0; not in meas. |
| G17 | Coverage: Wolf's whole-system weighting versus the bins | Wolf: "a luminosity-weighted average over the entire system". Atlas: plotted only at coverage ≥ 0.80. | Wolf l.557; D-036 item 1 | Not stated | System | g_obs | meas.`x_gc_baumgardt_coverage` (value, not an error) |
| G18 | Adequacy of the King (1966) model | "the single-mass and isotropic King models that we fit have long been known to be inadequate for many old GCs" | MvdM05 l.2002–2003 | Not stated | System | Both (weights and R_h) | No (assumption `gc_light_model`) |
| G19 | Brightness-profile error recipe behind the structural fits | "adopting the heuristic prescription that the relative surface-brightness errorbars grow as $\sigma_i \propto 1/w_i$" | MvdM05 l.1066–1067; Table 4 | σ_μ per cluster, 0.074–0.454 mag | System | Both (through the R_h and King errors) | Indirectly, through G20 and G16 |
| G20 | R_h fit error | `E_Rh` "Upper 1{sigma} error in Rh", `e_Rh` "Lower 1{sigma} error in Rh"; MvdM: "taking the differences between the extreme and best-fit values" | `models.vot` FIELD descriptions; MvdM05 §4.2 | Per cluster, in log pc | System (= point here) | **Both together:** g_obs ∝ 1/r½, g_bar ∝ 1/r½² | obs.`err_lo/hi` for the Rh rows; **not passed on** to the g errors |
| G21 | Deprojection factor 4/3 | "This approximation is accurate to better than 2\% for exponential, Gaussian, King, Plummer, and S\'ersic profiles"; "$\rhalf/\Rhalf \simeq 4/3$ is accurate to better than 2\% for most surface brightness profiles" | Wolf l.152–153, l.1829 | < 2% | Dataset | **Both together** | No (`gc_rhalf_wolf`, fixed) |
| G22 | Ellipticity and spherical symmetry | "Testing the accuracy of Equation \ref{eq:main} as a function of ellipticity will be an important future step." Harris: "(14) Projected ellipticity of isophotes, e = 1-(b/a)" | Wolf l.1186–1187; `mwgc.dat` Part II key | Not stated for the estimator | System | Both | No (Harris ellipticity not packaged) |
| G23 | Accuracy of the estimator | "The dashed lines indicate $\pm 10\%$ variation about the predicted relation"; "only mild assumptions … as long as the projected velocity dispersion profile is fairly flat near the half-light radius"; "projection effects can add an additional $\sim 20-30 \%$ uncertainty" | Wolf l.927; l.84–87; l.1940 | ±10% (classical dwarf spheroidals); 20–30% (projection, cited) | Dataset | g_obs | No (`gc_equilibrium`, fixed) |
| G24 | Wolf's binary caution | "medium-to-high binary fractions can inflate velocity dispersions by up to $\sim 20 \%$ in the smallest dSphs" | Wolf l.1212–1214 | Up to 20% (dwarf galaxies, not clusters) | System | g_obs, upward | No |
| G25 | Pal 1: inconsistent structural row | "the table's scale radius in parsecs (`r0pc` = 0.040) differs by 0.060 dex from its own angular scale radius times its own distance" | `REPRODUCTION_RESULT.md` (Atlas reading of the MvdM05 table); D-046 | 0.060 dex | System | Both | Pal 1 recorded, not plotted (`systems.properties`) |
| G26 | Harris distance, error per cluster | Key: "(7) Distance from Sun (kiloparsecs)", with no error column. L13: "the average errors on the distance (5 \%) and the reddening (10 \%) as taken from \cite{harris_1996}" | `mwgc.dat` Part I; L13 l.489 | Harris: not stated. L13: 5% on average. | System | **Both** (Doubt 1) | Value only: obs. R_Sun, meas.`x_gc_baumgardt_distance_kpc`; no error. `assumptions.json`: "Harris gives no per-cluster distance error." |
| G27 | Horizontal-branch calibration | "$M_V(HB) = (0.160 \pm 0.033) {\rm [Fe/H]} + (0.844 \pm 0.049)$"; "The rms scatter around these best-fit relations is $\pm 0.11$ magnitude."; adopted 0.16[Fe/H]+0.84, "slightly fainter (though at most 0.05 mag) than in previous editions" | Harris.tex l.148, l.152, l.116–118 | ±0.049 mag zero point; ±0.033 slope; 0.11 mag rms | Dataset | **Both** (R_Sun and M_V,t; Doubt 1) | No |
| G28 | Reddening | L13 "(10 \%)" (G26); BV21: highly reddened clusters' scatter "probably reflects an uncertainty in the exact amount of reddening" | L13 l.489; BV21 l.~404–405 | 10% on average (L13) | System | R_Sun, hence both (Doubt 1) | No |
| G29 | Scatter among literature distances | "individual distance moduli show a scatter of around 0.07 to 0.10 mag around the mean"; Harris (2010) "based on an averaging of literature values up to 2010" | BV21 l.402; l.618 (figure caption) | 0.07–0.10 mag | System | Both | No |
| G30 | Offset in the distance scale | "our distances are on average 8\% smaller … we obtain a similar difference when using the \citet{harris1996} distances" | B17 l.556–558 | About 8% | Dataset | Both | No |
| G31 | Integrated V_t magnitude | Harris has no error column. BSH20 Table 2, Harris (2010) row: "$+0.03$ & $0.22$ & $+0.01$ & $0.45$ & $-0.25$ & $0.70$"; "can reach up to two magnitudes for individual clusters"; aperture methods "have problems distinguishing between field and cluster stars" | `mwgc.dat` Part II; BSH20 l.266, l.203–204, l.70 | σ_V 0.22 / 0.45 / 0.70 mag for V < 8 / 8–11 / > 11 | System | g_bar | No (obs. M_V,t, no error) |
| G32 | Solar absolute magnitude | "a solar absolute magnitude $M_{V,\odot}=+4.85$ \citep[e.g.,][]{lan99}" | MvdM05 l.2160–2161; `analysis.py` `M_V_SUN` | No error stated | Dataset | g_bar | Constant only (meas.`x_gc_baumgardt_l_v` description) |
| G33 | Error on population M/L_V | `e_(M/L)1` "The 1{sigma} error in BC/ChD"; "All uncertainties on the population-synthesis quantities … follow directly from uncertainties in the cluster ages and [Fe/H] values"; "ages are set to a uniform $13\pm2$ Gyr … assigned uncertainties of $\pm$0.2 dex" | `clusters.vot` FIELD; MvdM05 l.1506–1509; Table 8 note (l.3513–3515) | 1σ per cluster; age ±2 Gyr; [Fe/H] ±0.2 dex | System | g_bar | obs.`err_lo/hi` (stellar_ml_population); meas.`g_bar_err_lo/hi` (**only** term) |
| G34 | IMF | "The Salpeter IMF gives $\Upsilon_V$ consistently higher than the Chabrier disk IMF (by factors of $\sim60\%-75\%$)" | MvdM05 l.1424–1425 | +60–75% | Dataset | g_bar, upward | meas.`x_gc_baumgardt_ml_v_salpeter`; slider `gc_stellar_ml` upper bound |
| G35 | Population-synthesis code | "at the level of $\la 0.05$ mag in $(B-V)_0$ and $\la 10\%$ in $\Upsilon_V$" | MvdM05 l.1358–1359 | ≲ 10% | Dataset | g_bar | No |
| G36 | Dissolution and loss of low-mass stars | Q_pred column, 0.53 (NGC 6121) to 1.00; abstract: "the $\sim 20$\% gap between canonically expected and observed $M/L_V$ ratios" | KM09 Table `tab:pred` (l.505–532); abstract | 0.53–1.00 | System per KM09; the Atlas uses it as a dataset bound | g_bar, downward | Slider lower bound 0.53× (`assumptions.json`); no column |
| G37 | Mass-loss prescription in the models | "This amounts to a $\sim30\%$ reduction in total cluster mass after a Hubble time." | MvdM05 Fig. 4 caption, l.1311–1313 | About 30% (included; its uncertainty is not stated) | Dataset | g_bar | No |
| G38 | Single-burst model, common IMF | "we {\it always} assume that every cluster is a single-age population formed instantaneously … share a common stellar IMF" | MvdM05 l.1259–1262 | Not stated | Dataset | g_bar | No |
| G39 | Stellar remnants | Descriptor: "stellar remnants … modelled … Included in the population-synthesis M/L_V" | `descriptor.json` `x_baryon_inventory` | Not stated | Dataset | g_bar | Only as status |
| G40 | Gas | "M15 (NGC~7078) displays 0.3~M$_\odot$ of neutral hydrogen HI"; "observational upper limits found in GCs often lower than 1~M$_\odot$" | Chantereau 2020 l.70, l.189 | 0.3 M☉ (M15); limits usually < 1 M☉ | System | g_bar, upward if added | meas.`gas_cold_status`/`gas_hot_status` = absent; no value |
| G41 | Membership not reproduced (Atlas check, not a source statement) | "the published RV bins contain 116 544 stars, but the released RV files give 54 067 members … The profiles therefore use velocities that are not in the released files" | `REPRODUCTION_RESULT.md`, D-037 section | 148 of 152 not testable; NGC 6638 fails | System | g_obs | `checks/d037_*.csv` only |

**Where point and system coincide.** Version 1 has one g value per cluster per dataset. Every term except the per-bin and per-star σ errors (G1, G2, G11–G14) is therefore both point-scale and system-scale.

## Not stated

These were looked for and not found:
- **Confidence level of Δσ in `veldis.html`.** The page gives column heads only. BH18 and B17 state 1σ for the published versions; the method behind the "plus updates" values is not described.
- **Harris errors per cluster** for R_Sun, (m−M)_V, E(B−V), V_HB and V_t. They are not in `mwgc.dat`, nor in Harris 2010 §2 to §4. The bibliography file (`mwgc.ref`) could not be fetched.
- **Error on M_V,☉ = 4.85.** MvdM05 cites Lang 1999 without an error.
- **r½/R_h for King (1966) models specifically.** Wolf Appendix B treats King (1962) only.
- **Accuracy of 3σ²/r½ for globular clusters specifically.** Wolf's ±10% check is for classical dwarf spheroidals. Clusters appear in his Fig. 1 without a stated scatter.
- **Size of anisotropy** for the clusters, in any source read.
- **Binary fraction or inflation for the Baumgardt RV profiles in general.** Only Pal 13 has a stated size.
- **How much rotation is in the `veldis` RV values.**
- **The v4 membership method.** The RV-file columns `PMEM RV`, `PMEM PM` and `P_Single` suggest proper-motion membership was used, but no documentation was read.
- **A dispersion in C22 (2204.06628) or a MUSE line-of-sight dispersion in G22 (2108.11922).** The C22 and G22 bins in `veldis.html` (VVV-CL001, Gran 5) have no stated method or error source. Neither cluster has a v1 measurement row.
- **F13 and D21 papers.** Not read.
- **Gas mass fraction inside r½, and a helium factor.** Not stated (not applicable for absent gas).
- **Error on the gravitational constant G.** Not stated in the package; astropy constant.

## Doubts and inferences (none of these is a direct quote)

1. **How distance moves the two axes (inference).**
   - I checked the source values numerically:
     - Harris `M_V,t` = `V_t` − `(m-M)V` exactly, for all 151 clusters with complete rows;
     - `R_Sun` matches 10^((m−M)_V − 3.1 E(B−V) + 5)/5 to within the rounding (median 0.2%, at most 1.5%);
     - (m−M)_V ≈ V_HB − (0.16[Fe/H]+0.84), with a small offset of about −0.02 to −0.03 mag.
   - From this I infer, though no source says it:
     - errors in the horizontal-branch calibration or in V_HB move R_Sun and L_V together (L ∝ D²), so g_bar is unchanged and g_obs ∝ 1/D;
     - reddening moves R_Sun only, so g_obs ∝ 1/D and g_bar ∝ 1/D²;
     - errors in V_t move g_bar only.
   - The light weights are computed in arcseconds, so they do not depend on distance.
2. **B17's error criterion.** B17 sets its "1σ" bounds where the likelihood falls to 0.5 of the maximum. For a Gaussian likelihood, 1σ corresponds to e^(−1/2) ≈ 0.61. I did not test what this means in practice.
3. **`veldis.html` "plus updates" differ from BH18's printed table.** Arp 2's first bin is 1.97 (+0.39 / −0.31) in `veldis.html` and 2.03 (+0.40 / −0.32) in BH18 Table 3. The updated method and error definition are not documented.
4. **Which K18 quantity Baumgardt lists is not stated.** K18 gives both σ_r and V_rms. Likewise, the L15 entries are labelled SINFONI, and L15 itself says SINFONI individual-velocity dispersions are biased low.
5. **The L15 quote about underestimated uncertainties refers to Lützgendorf et al. 2011,** not to F13 (Feldmeier 2013). I did not read F13.
6. **L13's "5%" and "10%"** are L13's description of Harris (1996) averages, not Harris's own statement.
7. **B17's 8% distance offset rests on kinematic distances,** which D-036 #6 excludes as inputs. I report it only as a source statement.
8. **Location mismatches with Atlas records:**
   - `assumptions.json` cites KM09 "§2, Table 1 (Q = 0.53–1.00)". In arXiv v1, the Q_pred column with 0.53–1.00 is in Table 4 (`tab:pred`, §5 "Predicted and observed mass-to-light ratios"). The journal numbering may differ; I did not check it.
   - MvdM05 R_h is in Table 11 (`tab:struc`), while W₀ and r₀ are in Table 10. `assumptions.json` cites "Table 10" for both.
9. **Wolf's King profile is King (1962);** the Atlas light model is King (1966). Wolf's whole-system ⟨σ²⟩ differs from the Atlas's average over the covered bins only (coverage ≥ 0.80). I did not quantify the difference.
10. **Clusters whose own sources exclude some of their bins.** v1 plots NGC 6715 (M54) with bins beyond 200″, which B17 excluded as contaminated by Sagittarius stars. It also plots NGC 2298 and Pal 5 with their rising outermost bins, which BH18 dropped from its fits.
11. **Edition mismatch.** MvdM05 used Harris (1996), an earlier edition, for [Fe/H] (behind M/L₁) and for the distance (behind `Dist`). The Atlas rescales R_h to the 2010 distance, but M/L₁ keeps the old [Fe/H]. No source states the effect.
12. **Paper identification:**
    - G22 was matched to 2108.11922 by title, authors and year. Its own dispersions are from proper motions, and it reports MUSE radial velocities. The journal reference (MNRAS 509, 4962) was not shown on the abstract page I read.
    - L13 (1212.3475) was matched by title. Its journal reference (A&A 552, A49) was not shown on the abstract page.
13. **No IFU star counts, and dropped single-bin profiles.**
    - Integral-field datasets give no star counts, so the "N Star" ranking treats them as zero. This decided no default (`REPRODUCTION_RESULT.md`).
    - Single-bin profiles, such as Pal 1 and UKS 1, are refused, not converted, so their σ errors never reach v1.