# Globular clusters, Reader A (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

I've finished the reading. Full report below.

# Reader A: Step A uncertainty reading, Globular clusters (`aeg-d-gc-baumgardt`)

**Reader:** Reader A  
**Dataset:** Globular clusters, `aeg-d-gc-baumgardt/v1`  
**Date:** 2026-11-04  
**Work directory:** /tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/step-a-2026-11-04/gc-A/ (downloads under `dl/<id>/`, each extracted to `dl/<id>/x/`)

## Sources read

**Package (read-only):** `/home/claude/atlas/data/packages/aeg-d-gc-baumgardt/v1/`
- `REPRODUCTION.md`, `REPRODUCTION_RESULT.md`, `convert.py`, `analysis.py`, `descriptor.json`, `sources.json`
- the column headers and descriptions of `tables/measurements.ecsv`, `tables/observables.ecsv` and `tables/systems.ecsv`
- `/home/claude/atlas/pipeline/aeg/dispersion.py`
- the gc_* entries of `/home/claude/atlas/data/assumptions.json`
- `/home/claude/atlas/docs/decisions.md`: D-025, D-036, D-037, D-038, D-039, D-042, D-045, D-046, D-047, D-083

**Local source copies.** My SHA-256 of each matches `sources.json`.

| File | SHA-256 |
|---|---|
| `source/veldis.html` | b1bf703280a33bf4988bbe94e291da1896611623860315e7e71e6c240e5b05de |
| `source/parameter.html` | c2e231374ba447d5153307c1018c1ea982f03706b813814a24209a32027bd225 |
| `source/appendix.html` | d6262d46887bd7385861a0b4c94e6017b2498ca3520bb0401e9ffe00ba68bd58 |
| `source/mwgc.dat` (Harris 2010 edition) | b457a690adc422fb2e8e05a23e1de50b62d1d5ac10dce99963c956c1b17ca658 |
| `source/mvdm05/J_ApJS_161_304_clusters.vot` | 282ea6daaaa9da0b690c3efd1384a12e83da9e664e939649896aea8d006dc7ec |
| `source/mvdm05/J_ApJS_161_304_models.vot` | 84647d34642e32734368961fa6a940d25b1f4db81fd797825a734e63c04e4e16 |
| `source/mvdm05/J_ApJS_161_304_table13.vot` | 42a6f2521bc5562b5e615a4c463cb6753fdc2b1f1a1f4831e31c71f3a2957b96 |
| `source/mvdm05/J_ApJS_161_304_table5.vot` | 3cbd17d7eea2f7ada1722fd7c7ec152639efcff23b664b027281df72628d14d7 |
| `source/rv/ngc6752.txt` | header only |

**arXiv e-prints,** fetched from `https://arxiv.org/e-print/<id>` (latest version). Versions are as listed on each abs page.

| Source | arXiv id (version) | Main .tex | SHA-256 of e-print |
|---|---|---|---|
| Wolf et al. 2010 | 0908.2995 (v6) | ms-mn2e.tex | 6852fe7e0248278947158c37c30132610c1c4ac4c347448f232e65d78b1bbd94 |
| Harris 2010, "A New Catalog of GCs in the MW" | 1012.3224 (v1) | Harris.tex | a250b8dcb55ba495c23d6ecae40c5c5bd77a6924201f5b5f232d5916d5f49ff4 |
| McLaughlin & van der Marel 2005 (MvdM) | astro-ph/0605132 (v1) | mclaughlin_vandermarel.tex | af94cbcf14303090df2ab51ddd864235731d3378d9ba309638da8edf4a431b96 |
| Baumgardt 2017 (B17) | 1609.08794 (v1) | paper.tex | 0e6dc3b76f52310a05d0ab61c090edf99c7f16c7635877844e7dfcfab415fb49 |
| Baumgardt & Hilker 2018 (BH18) | 1804.08359 (v2) | vltpaper_ver6.tex (+ veldis_tab.tex) | f52c50c561028ef86eae80b320de742ab2bf16cbcd64ff7a8c58a48eae1ed8ad |
| Baumgardt et al. 2019 (B19, Gaia DR2; one of the "plus updates") | 1811.01507 (v1) | paper_v6.tex | 66ea5a58630bfd8113f3ede4d225fe095de3d8b8e320d72f862e8bc6e571171e |
| K18: Kamann et al. 2018 | 1710.07257 (v1) | muse_gc_kinematics_skamann.tex | cdf9666eec5bc305fa162da26ee52bca2c9f2d6d0f2ab19e41a5dcdb1384718e |
| L13: Lützgendorf et al. 2013 | 1212.3475 (v1) | luetzgendorf_2012c.tex | 91af3fa6deb1b2c00cfdfe180149fe8bd7c0defe3371de29572c88a14f309681 |
| F13: Feldmeier et al. 2013 | 1304.4176 (v1) | ngc5286_final.tex | 41c16aaa04630014d107c9f15853dfd8d86e415bf583632a73ea55ec1d81ad2a |
| L15: Lützgendorf et al. 2015, A&A 581, A1 (journal reference confirmed on the abs page) | 1507.02813 (v1) | 6388ifu_paper.tex | 22eeb020ec7fee4d4d158cb9ba411adf651a137015594a8779b3c747fb49fac8 |
| D21 (identified by title and author; journal reference not shown on the abs page): Dalessandro et al., NGC 6362 MUSE | 2105.02246 (v1) | ms_final.tex | 5efe99ea10bce4fb3fcd496ee342b93b89d2e84ea12c7c8f2346cee6cdfe4d30 |
| C22 (identified as above): Olivares Carvajal et al., VVV CL001 MUSE | 2204.06628 (v1) | CL001.tex | 0cbeb6dc9fc9104e5bcc2d4cf6545e5ad1dd075ce3fa1645dbebd32a1602485c |
| G22 (identified as above): Gran et al., "Hidden in the Haystack" | 2108.11922 (v2) | NewGCs.tex | 097aa326d50dcbc1e51d42841d57c5c48b8aaabce21e9c528b923ee561957069 |
| Kruijssen & Mieske 2009 (D-039 range bound) | 0903.4683 | KruijssenMieske.tex | 78d8184dcdf873425a39d5e662b7fff3d487052401e6bb69eee236ea1ec19109 |
| Chantereau et al. 2020 (gas-absent citation) | 2002.02401 | main.tex | 3654a1411327c4737912f99d07f258861a2c2e2afc4f7906a2c6dd6c8a2bd854 |

**Not reachable:**
- `export.arxiv.org` returned 403. I located ids through arxiv.org/search instead.
- `physics.mcmaster.ca` returned 403, so I could not read the Harris bibliography file. I did not try to get around either block.

**Sample of originals per input type:**
- **σ:** all seven line-of-sight originals named on veldis.html (F13, L13, L15, K18, D21, C22, G22), plus the three Baumgardt method papers behind the RV code (B17, BH18, B19). All 64 plotted defaults use the RV code.
- **Structure and Υ_V:** MvdM itself is the original fit. Its input surface-brightness profiles (Trager et al. 1995) were **not** read.
- **Distance and luminosity:** only the Harris 2010 paper and the `mwgc.dat` keys. **No per-cluster original horizontal-branch or photometry paper was read,** because the bibliography that maps clusters to originals was blocked. The brief asks for at least five per input type; I did not meet that for distance and luminosity.

## How v1 builds g_obs and g_bar (from `convert.py` and `analysis.py`)

- **σ:** the light-weighted rms of the bins in the default line-of-sight dataset (`aeg.dispersion`), with weights from King (1966) (W₀, r₀ in arcsec).
- **r½:** 4/3 × R_h, where R_h = 10^Rh(MvdM) × D_Harris / Dist(MvdM).
- **L_V:** 10^(−0.4(M_V,t,Harris − 4.85)).
- **Υ_V:** MvdM (M/L)1.
- **g_obs** = 3σ²/r½. **g_bar** = G·½·L_V·Υ_V/r½².
- **Error columns in v1:**
  - `g_obs_err_lo/hi` come from the σ errors only.
  - `g_bar_err_lo/hi` = g_bar × e_(M/L)1 / (M/L)1, so only the M/L error.
  - `dispersion.py` states: "Uncertainty in the structural model is not propagated (registered as a known limitation)."

## Terms

Scale codes: P = point (one bin, or one star's velocity); S = system (one cluster); D = dataset.

**Important for this dataset:** one value per cluster is plotted, so every bin-level (point) term has been reduced to one system-level value. The **point and system scales coincide** for the plotted g_obs.

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| G1 | σ statistical error per bin (RV code) | "The 1$\sigma$ lower and upper uncertainties of the velocity dispersion were calculated by determining the velocity dispersion where the likelihood is less than 0.5 the maximum value in each direction." | B17 paper.tex l.295–296 (§3) | Per bin (Δσ Up / Δσ Low in veldis.html); stated as 1σ | P (per bin); S after light weighting | g_obs (∝σ²), both directions | Yes. observables.ecsv `err_lo`/`err_hi` (sigma_los rows); measurements.ecsv `x_gc_baumgardt_sigma_err_lo/hi`, `g_obs_err_lo/hi` |
| G1a | Confidence level of the veldis.html Δσ columns | veldis.html header gives only "Δσ Up", "Δσ Low" [km/sec]. BH18 table caption: "the velocity dispersion together with the $1\sigma$ upper and lower error bars." | veldis.html (header text); BH18 veldis_tab.tex l.2 | 1σ (BH18). Not stated on the database page itself | — | — | Assumed 1σ in column descriptions ("one-sigma") |
| G2 | Individual-velocity errors entering the likelihood | "The median uncertainty of an individual measurement is about 0.5 km/sec and 90\% of our stars have velocity errors of less than 2 km/sec. The errors should therefore be small enough to reliably derive the velocity dispersion profiles of most globular clusters, except for the lowest mass clusters in which the internal velocity dispersion is less than 1 km/sec." | BH18 l.191–194 (§2.1) | Median 0.5 km/s; 90% < 2 km/s | P (per star) | g_obs | Folded into G1 only; no separate column |
| G2a | Mis-estimated velocity errors bias σ | "Systematically underestimating the uncertainties would lead to an overestimate of the intrinsic velocity dispersion and vice versa." | K18 l.257 (§5) | Not stated in general | P/S | g_obs (underestimated errors push σ up) | No |
| G3 | Zero-point shifts between merged RV datasets | "we cross-correlated the radial velocities from the different data sets against each other to bring them to a common mean radial velocity. The necessary radial velocity shifts were usually less than 1 km/sec." | BH18 l.198–199 (§2.2) | Shifts usually < 1 km/s; effect on σ not stated | S | g_obs | No |
| G3a | Gaia RV offset (B19 update) | "The necessary shifts were usually less than 0.5 km/sec, in agreement with the systematic offset in the \textit{Gaia} line-of-sight velocities found by \citet{katzetal2018} for faint stars." | B19 paper_v6.tex l.137–138 (§2.1) | < 0.5 km/s shift; effect on σ not stated | S | g_obs | No |
| G4 | Binary rejection (multi-epoch) | "Stars where the individual measurements had a less than 5\% probability to be compatible with a constant radial velocity were removed before the velocity dispersion profile was calculated." | BH18 l.202–205 (§2.2) | Threshold 5%; residual effect not stated | P (per star) → S | g_obs | No binary flag or column (`flags` = `edges_inferred` only) |
| G4a | Residual undetected binaries (named clusters) | "This reduces the velocity dispersion by about 50\% compared to the case when we use all stars. However the resulting $M/L$ ratio is still significantly larger than what we find for other globular clusters, indicating that undetected binaries might still be present in the Pal~13 sample. Undetected binaries might also be present in a few other low-mass and low density clusters like Arp~2 or Ter~3" | BH18 l.230–233 (§2.2) | Pal 13: about 50% fall when only multi-epoch stars are used; residual not stated | S | g_obs, up (inflation) | No. Pal 13, Arp 2 and Ter 3 are "recorded", for other reasons |
| G4b | Binary inflation, size from simulation (K18) | "We found that on average, we overestimated the intrinsic velocity dispersion by $0.3\,{\rm km\,s^{-1}}$ and $0.6\,{\rm km\,s^{-1}}$ for binary fractions of 5\% and 10\%, respectively." | K18 l.330 (§5.2) | +0.3 km/s (5% binaries), +0.6 km/s (10%), for NGC 6121 | S | g_obs, up | No |
| G4c | Single-epoch stars cannot be screened | "On average each member star has 1.8 radial velocity measurements" | appendix.html (prose) | Mean 1.8 epochs; fraction single-epoch not stated | D | g_obs (up, if binaries remain) | No |
| G5 | Membership / foreground clipping | "rejected all stars as binaries or background stars that deviated more than three standard deviations from the mean. We repeated the above procedure for each bin until we found a stable value" | B17 l.300–302 (§3) | 3σ clip; effect not stated | P → S | g_obs | No |
| G5a | Proper-motion cleaning lowers outer σ | "Proper motion cleaning was most useful for the outer parts of bulge globular clusters, where it generally lead to a reduction of the velocity dispersion profile" | B19 l.251–252 (§2.3) | Direction stated (down); size not stated | S | g_obs, down with cleaning | No |
| G5b | Released velocities do not reproduce published bins | "We have not included most VLT/MUSE data in this list since this data has been published by the authors." | appendix.html. Atlas-side consequence in REPRODUCTION_RESULT.md ("116 544 stars … 54 067 members") | Not a size on σ | D | g_obs (cannot be checked) | `checks/d037_rv_*.csv` (148 not testable) |
| G6 | Rotation / second moment | K18: "In the globular cluster literature, the velocity dispersion $\sigma_{\rm r}$ is often equated with the central second velocity moment $V_{\rm rms}=\sqrt{\sigma_{\rm r}^2 + v_{\rm rot}^2}$, implying that no rotation exits" | K18 l.324 (§5.2) | Not stated per cluster for the RV code (B17 likelihood has no rotation term) | S | g_obs | No |
| G7 | Tracer population / mass segregation (giants vs light) | "The literature profiles are based mainly on giant stars whereas the bulk of our sample in those two clusters consists of less massive main-sequence stars… the mass differences would correspond to a difference of $\lesssim5\%$ in the velocity dispersion" | K18 l.344 (§5.2) | ≲5% in σ (NGC 3201, NGC 6121) | S | g_obs | No |
| G8 | Aperture / radial coverage (Atlas 80% rule) | Atlas: "The value is plotted only if the covered fraction is at least 0.80" | pipeline/aeg/dispersion.py docstring | Coverage per candidate | S | g_obs | Yes. measurements `x_gc_baumgardt_coverage`, `x_gc_baumgardt_n_bins` |
| G8a | Bin edges not published | Atlas: "edges are inferred at arithmetic midpoints between adjacent radii" | dispersion.py docstring; REPRODUCTION.md | Not stated by any source | S | g_obs (through weights) | Flag only: `flags` = `edges_inferred` |
| G9 | Light-model (King W₀, r₀) error in the weights | MvdM: "The uncertainties in $W_0$, $c$, $\gamma$, and $r_0$ reflect their variations among model fits with $\chi^2\le \chi_{\rm min}^2+1$." Atlas: "Uncertainty in the structural model is not propagated" | MvdM l.2121–2123 (§4.2.2); dispersion.py | Per cluster in VOT (E_/e_W0/gamma, E_/e_r0) | S | g_obs (through σ weights) | Values carried: observables `err_lo/err_hi` on W0/gamma and r0 rows. Not propagated to g_obs |
| G10 | Centre position | "At present the center coordinates for the clusters are now uncertain to typically 1-2 arcseconds"; L13: "The center determination is critical for this work as errors in the center position can cause differences in the velocity-dispersion profile and the surface brightness profile" | Harris 2010 l.94 (§2); L13 l.242 (§2.2) | 1–2″ (Harris); effect on σ not stated | S | g_obs | No |
| G11 | IFU σ errors: spectral MC plus shot noise (L13 and F13 codes) | L13: "The final value results from a quadratic summation of both errors assuming that they are independent of each other." F13: "The error for $V_{rms}$ comes from Monte Carlo simulations, and is an estimate for the amount of shot noise." | L13 l.423 (§4.3); F13 l.351–352 | Per bin; confidence level not stated (L13); "sigma-clipped standard deviation of these 1,000 velocity dispersions" (F13) | P → S | g_obs | Yes, through veldis.html Δσ (alternatives only; none plotted) |
| G11a | IFU bias and underestimated errors (L15 code) | "the individual radial velocities, i.e. the measurements from the simulated SINFONI data, are systematically biased towards lower velocity dispersions"; "the simulations of the innermost bin result in a very large scatter and an uncertainty of more than 20 \%"; "the uncertainties in \citet{nora11} are underestimated" | L15 l.94 (abstract), l.255, l.279 (§5) | > 20% (innermost ARGUS bin); SINFONI biased low, size depends on Strehl | S | g_obs, down (SINFONI) | No (L15 is an unplotted alternative for NGC 6388) |
| G11b | MUSE σ error level (K18, D21 codes) | K18: "The values we provide in the following are the median values and the 16th and 84th percentiles of the resulting parameter distributions." D21: "as uncertainty the interval between the 16-th and 84-th percentile of the marginalised posterior PDF." | K18 l.282 (§4); D21 l.~418 (§4) | 16th–84th percentiles | P → S | g_obs | Through veldis Δσ (alternatives only) |
| G11c | Crowding bias (MUSE centres) | "such a feature could be artificially caused by crowding effects -- contamination by background light tends to bias the measured radial velocities towards the cluster mean" | K18 l.326 (§5.2) | Not stated | S | g_obs, down | No |
| G12 | Out of equilibrium / tidal disruption (named clusters) | "NGC~2298 and Pal~5 have velocity dispersion profiles which increase towards the outer parts, which could be due to the ongoing tidal disruption of these clusters… We therefore neglected the outermost data point of their velocity dispersion profiles in our fits." | BH18 l.226–228 (§2.2) | Not stated | S | g_obs, up (outer rise) | No. Both clusters are plotted in v1 (systems.ecsv `properties`) |
| G13 | Equilibrium, spherical symmetry, estimator | "Equation \ref{eq:main} can be understood under the assumption that the observed stellar velocity dispersion profile is relatively flat near $\Rhalf$"; "adding an error of 0.05 dex to the propagated mass error provides a reasonable means to allow for a range of $\beta$ profiles." | Wolf l.156–157 (§1); l.973–975 (§3.2) | 0.05 dex (if the flat-σ assumption is not accepted); normalisation "$\pm 10\%$" (l.927); r₋₃ vs r½ "slight ($\sim 15\%$) difference" (l.889) | D | g_obs | Named only: `assumptions` = `gc_equilibrium` (not adjustable) |
| G14 | Deprojection r½ = 4/3 R_h | "Thus, $\rhalf/\Rhalf \simeq 4/3$ is accurate to better than 2\% for most surface brightness profiles used to describe observed stellar systems." | Wolf l.1829 (App. A); also l.152 | < 2% | D | Both: g_obs ∝ r½⁻¹, g_bar ∝ r½⁻² | Named only: `gc_rhalf_wolf` |
| G15 | R_h fit error (MvdM King fit) | "Again, the uncertainties on all of these derived parameters have been estimated … by calculating them in every model which yields $\chi^2$ within 1 of the global minimum" | MvdM l.2187–2190 (§4.2.2) | Per cluster, asymmetric, in log pc (VOT E_Rh/e_Rh) | S | **Both together:** g_obs ∝ R_h⁻¹, g_bar ∝ R_h⁻² | Value carried in observables (`half_light_radius` row, `err_lo/err_hi`, log(pc)). Not propagated to the g columns |
| G15a | Surface-brightness point errors are MvdM's estimate | "we decided instead to de-weight such points even further by adopting the heuristic prescription that the relative surface-brightness errorbars grow as $\sigma_i \propto 1/w_i$" | MvdM l.1065–1067 (§2.2) | σ_μ per cluster (MvdM Table 4) | S | Both (through R_h); g_obs also through the weights | No |
| G15b | Model family (King vs Wilson) for R_h | "Wilson models are also associated with slightly larger projected half-intensity radii $R_c$ and smaller half-light radii $R_h$"; for the LMC/SMC/Fornax set, "their $R_h$ values differ by factors of 2.5--3" when χ² are comparable | MvdM l.2703–2704; l.2656–2657 (§4.3.3) | Galactic GCs: not stated numerically. LMC/SMC/Fornax: up to 2.5–3× in comparable-χ² cases; "agree within $\sim5\%$" otherwise (l.2578) | S | Both (Wilson gives smaller R_h, so g_obs and g_bar both higher) | No (King only; Wilson rows not used) |
| G16 | Ellipticity | Harris key: "(14) Projected ellipticity of isophotes, e = 1-(b/a)" | mwgc.dat Part II key | Per cluster (where listed) | S | Both (through R_h and the spherical assumption); direction not stated | No (not read into the package) |
| G17 | **Distance, per cluster** | Harris gives no per-cluster distance error. B19: "assuming a relative distance error of 10\% for the Harris distances" | mwgc.dat Part I (no error column); B19 l.375 (§3.1) | Not stated by Harris. 10% assumed by B19 | S | **Both** (see Doubts D1 for the direction in v1's construction) | No error column. Value carried: observables `distance`, measurements `x_gc_baumgardt_distance_kpc`, systems `distance_mpc`. Registry: "No slider yet: Harris gives no per-cluster distance error." |
| G17a | Distance scale offset (Harris against kinematic) | B19: "$D_{Gaia}/D_{Harris} = 0.97 \pm 0.01$ … typical distance differences (8\% vs the Harris data…)"; B17: "our distances are on average 8\% smaller" | B19 l.351–352; B17 l.557 | 3 ± 1% mean; 8% typical; 8% (B17) | D (mean) and S (scatter) | Both | No |
| G18 | Horizontal-branch calibration zero point and slope | "$M_V(HB) = (0.160 \pm 0.033) {\rm [Fe/H]} + (0.844 \pm 0.049)$ … The rms scatter around these best-fit relations is $\pm 0.11$ magnitude." | Harris 2010 l.148–152 (§2) | Slope ±0.033, zero point ±0.049 mag, rms 0.11 mag | D (zero point, slope); S (rms, per cluster) | Distance, so both (see D1) | No |
| G19 | Metallicity scale feeding M_V(HB) | "The new heavy-element abundance scale adopted for the catalog is the one established by Carretta et al.~(2009)." | Harris 2010 §3 | Not stated as an error | S/D | Distance (through M_V(HB)), so both | [Fe/H] value only: systems `metallicity_feh` |
| G20 | Extinction / reddening | Harris key "(4) Foreground reddening"; MvdM: "$A_V=3.1\,E(B-V)$" | mwgc.dat Part II key; MvdM l.1210 | No error stated in Harris. R_V = 3.1 fixed (MvdM); no range stated | S (E(B−V)); D (R_V) | Distance and possibly L (see D1) | No |
| G21 | Integrated magnitude V_t / M_V,t | Harris key "(8) Absolute visual magnitude (cluster luminosity), M_V,t = V_t - (m-M)V" | mwgc.dat Part II key | No error stated | S | g_bar (∝ L) | Value carried: observables `absolute_magnitude` (no error); `x_gc_baumgardt_l_v` |
| G22 | Solar absolute magnitude | "The surface-brightness zeropoint of 26.422 corresponds to a solar absolute magnitude $M_{V,\odot}=+4.85$ \citep[e.g.,][]{lan99}." | MvdM l.2160–2161 (§4.2.2) | No uncertainty stated | D | g_bar (∝ 10^(0.4·M_V,⊙)) | Fixed constant `M_V_SUN = 4.85` in analysis.py; named in the registry `default_ref` |
| G23 | Υ_V statistical error from age and [Fe/H] | "All uncertainties on the population-synthesis quantities in Table \ref{tab:poptable} follow directly from uncertainties in the cluster ages and [Fe/H] values"; "Milky Way globular cluster ages are set to a uniform $13\pm2$ Gyr … metallicities … assigned uncertainties of $\pm$0.2 dex." | MvdM l.1506–1508 (§3.2); l.3513–3515 (Table 8 note a) | e_(M/L)1 per cluster, 1σ (VOT: "The 1{sigma} error in BC/ChD") | Mixed: the age part (13 ± 2 Gyr for all) is D; the [Fe/H] part (±0.2 dex each) is S | g_bar | Yes. observables `stellar_ml_population` err; measurements `g_bar_err_lo/hi` |
| G24 | IMF (Chabrier against Salpeter) | "The Salpeter IMF gives $\Upsilon_V$ consistently higher than the Chabrier disk IMF (by factors of $\sim60\%-75\%$)" | MvdM l.1424–1425 (§3.1) | +60–75% | D | g_bar, up | Yes, slider upper bound: `x_gc_baumgardt_ml_v_salpeter`; `adjustable` = `gc_stellar_ml` |
| G25 | Population-synthesis code (BC03 against PÉGASE) | "these differences are generally slight: at the level of $\la 0.05$ mag in $(B-V)_0$ and $\la 10\%$ in $\Upsilon_V$" | MvdM l.1358–1359 (§3.1) | ≲ 10% | D | g_bar | No ((M/L)3 not read into the package) |
| G26 | Stellar mass-loss prescription in the models | "This amounts to a $\sim30\%$ reduction in total cluster mass after a Hubble time." | MvdM Fig. 4 caption l.1312–1313 | ~30% (built in; no range stated) | D | g_bar | No (inside Υ) |
| G27 | Single burst and common IMF | "we {\it always} assume that every cluster is a single-age population formed instantaneously in one coherent burst of star formation, and that all clusters, of any age or metallicity in any galaxy, share a common stellar IMF" | MvdM l.1259–1262 (§3) | Not stated | D | g_bar | Named only (`gc_stellar_ml` `name_technical`) |
| G28 | Low-mass-star loss (dissolution) | Q_pred column, e.g. "6121 … 0.53$_{-0.09}^{+0.07}$"; abstract: "the $\sim 20$\% gap between canonically expected and observed $M/L_V$ ratios is bridged by accounting for the preferential loss of low-mass stars" | KM09 tab:pred (4th table in the .tex, §4.1, l.504–533); abstract l.160 | Q_pred 0.53–1.00 across 24 clusters; ~20% mean | D (Atlas uses it as a bound); S in source | g_bar, down | Yes, slider lower bound (0.53 × default) in assumptions.json |
| G29 | Gas | "Other searches for HI, CO, and H$\alpha$ in GCs all lead to only observational upper limits often lower than 1~M$_\odot$ and as low as 10$^{-5}$~M$_\odot$"; detections: M15 "0.3~M$_\odot$ of neutral hydrogen HI"; 47 Tuc "0.023$\pm$0.005~M$_\odot$" (inner 1 pc) | Chantereau 2020 l.70 (§1) | Limits often < 1 M☉; detections 0.3 M☉ (M15), 0.023 ± 0.005 M☉ (47 Tuc) | S | g_bar, up if included | Status only: `gas_cold_status`/`gas_hot_status` = `absent`; `gc_gas_absent` |
| G30 | Harris 2010 kinematic-calibration input | The M_V(HB) calibration includes "(c) dynamical parallax from combined solutions to radial velocity and proper motion dispersions" | Harris 2010 §2 | Contribution not separated | D | Distance, so both | No |
| G31 | Gaia PM error scaling (proper-motion dispersions only) | "For faint clusters, the derived velocity dispersions can change by up to 10\%, however even then the changes remain usually within the formal error bars" | B19 l.266–267 (§2.3) | Up to 10% | S | None in v1 (PM bins recorded, not plotted) | PM bins in observables only |

**Terms that move g_obs and g_bar together:** G14 (deprojection), G15, G15a and G15b (R_h), G16 (ellipticity), G17, G17a, G18, G19 and G30 (distance), and G20 (extinction, through distance). Only R_h's fit error is carried, and only in `observables.ecsv`, not in the g error columns.

## Not stated

What I looked for and did not find, and where I looked:
- **Per-cluster errors in Harris 2010** on R_Sun, (m−M)_V, V_t, M_V,t, E(B−V), c, r_c, r_h and ellipticity. `mwgc.dat` Part III gives errors only for v_r and σ_v (keys "(3) Observational (internal) uncertainty in radial velocity" and "(6) … in velocity dispersion"). Not in the Harris 2010 arXiv text either. I could not check the Harris bibliography file, because the host was blocked.
- **An uncertainty on M_V,⊙ = 4.85.** MvdM cites "e.g., Lang 1999" with no error. Not in Harris.
- **A range on R_V = 3.1.** MvdM uses it fixed. Harris 2010 does not state it.
- **A confidence level on the veldis.html Δσ columns.** That page states none. The 1σ statement comes from BH18 and B17.
- **The size of residual single-epoch binary inflation in the RV code.** B17, BH18, B19 and appendix.html give no size. K18 gives a size for its own data (G4b).
- **Whether the RV-code σ is the second moment or the dispersion about rotation.** The B17 likelihood has no rotation term. No source states the effect on the RV bins.
- **The effect of the merger zero-point shifts (G3, G3a) on σ.** Only the shift sizes are stated.
- **An R_h error that includes distance.** MvdM's Dist column has no error. Their R_h errors come from χ² only, at fixed distance (l.2121–2126).
- **The size of the King vs Wilson R_h difference for Galactic clusters.** Only the direction is stated (G15b).
- **The effect of ellipticity on R_h or the estimator.** Wolf states spherical symmetry only.
- **What the gas limits are inside r½ for individual plotted clusters.** Chantereau gives general limits plus two detections.
- **The effect of centring errors on σ** (Harris, B17, L13).
- **The method and errors behind the G22 and C22 line-of-sight profiles.** G22's dispersion section uses Gaia EDR3 proper motions ("$\sigma_0^2 = \sigma_{\rm vel}^2 - \sigma_{\rm errors}^2$", NewGCs.tex l.663). In C22 I found no binned line-of-sight dispersion profile. See Doubts D6.

## Doubts

- **D1. Distance direction (my inference, not a quote).**
  - Harris key: "M_V,t = V_t - (m-M)V".
  - R_Sun is consistent with (m−M)_V − 3.1·E(B−V). I checked this for two rows only: NGC 104 gives 4.45 kpc against the listed 4.5; NGC 288 gives 8.89 against 8.9.
  - In v1, r½ ∝ D_Harris (convert rescales R_h by D_Harris/Dist), while L_V comes from the printed M_V,t and is not recomputed from R_Sun.
  - If the error enters through (m−M)_V (the V_HB or M_V(HB) terms G18 and G19), then L ∝ D², so g_obs ∝ D⁻¹ and **g_bar ∝ D⁰**.
  - If it enters through E(B−V) alone (G20), then M_V,t is unchanged and D moves, so g_obs ∝ D⁻¹ and g_bar ∝ D⁻².
  - If one perturbs R_Sun alone, as the v1 columns are stored, then g_obs ∝ D⁻¹ and g_bar ∝ D⁻².
  - No source states any of these directions. They are my arithmetic.
- **D2. Wolf's 4/3 accuracy is for the King (1962) profile, not King (1966).** Wolf's appendix: "For the \citet{King_62} profile … $c_k \equiv \log_{10}(\rlimit/\rcore)$". v1 uses King (1966) fits. The statement "accurate to better than 2\% for most surface brightness profiles" is general.
- **D3. Wolf's ⟨σ²_los⟩ is a luminosity-weighted average over the whole system.** v1 averages over bins covering ≥ 80% of the light. Each bin's σ weights stars equally (K18: "each star was considered one measurement"), and the RV samples are "mainly restricted to giant stars" (BH18 l.185). How much this differs from Wolf's average is not stated by any source.
- **D4. Location of the dissolution bound.** assumptions.json cites "Kruijssen & Mieske 2009 … §2, Table 1 (Q = 0.53–1.00)". In the e-print, Q_pred values 0.53–1.00 are in the table labelled `tab:pred` (fourth table, §4.1). `tab:obs` (first table) holds observed properties. Journal numbering may differ; I did not check the journal version. Also, KM09's Q_pred comes from orbit-based dissolution timescales, and its Q_obs uses dynamical M/L (abstract l.157–159).
- **D5. MvdM's Dist column.** MvdM says MW distances "are taken from the catalogue of \citet{har96}" (l.2069–2070). It was a pre-2010 edition (2003 or earlier; not stated). v1 rescales R_h to the 2010 edition. The two editions' distance difference is a system-level change, not an error, but it shows the R_h and distance terms are coupled.
- **D6. Dataset labels on veldis.html against the papers.**
  - veldis.html lists G22 and C22 under "Line-of-sight radial velocities … (VLT/MUSE)". G22's dispersion section is proper-motion based. C22 reports a systemic radial velocity but no dispersion profile that I found. So the G22/C22 σ were probably computed by Baumgardt from their radial velocities (inference). Neither code is in v1's measurements.
  - L15 is labelled "(VLT/SINFONI)". The L15 paper finds SINFONI biased low and re-evaluates ARGUS errors. Which data the L15 bins in veldis.html hold is not stated.
  - BH18 says it "include[s] the velocity dispersion profiles recently published by \citet{kamannetal2018}" (l.183–184). Yet veldis.html lists K18 as a separate code. Whether K18 stars also enter the RV code is not stated.
  - Whether the K18 code holds σ_r or V_rms is not stated.
- **D7. Typo in B17's likelihood.** B17 eq. (1) is printed with "+ Σ v²/(σ²+e²)", a sign typo relative to the standard form. Its text says the 1σ limits are where "the likelihood is less than 0.5 the maximum". Read literally, that is a likelihood ratio of 0.5, not Δln L = 0.5. Which one was meant is not stated.
- **D8. NGC 2298 and Pal 5 (G12).** BH18 attributes their rising outer profiles possibly to "ongoing tidal disruption" and drops the outermost point in its own fits. Both are plotted in v1, using all RV bins. I did not look at their bin values.
- **D9. e_(M/L)1 mixes two scales.** The age part (13 ± 2 Gyr assigned to every MW cluster) is common to the dataset; the [Fe/H] part (±0.2 dex) is per cluster. MvdM does not split them. v1 carries the sum as a per-system symmetric error.
- **D10. Possible circularity in the distance calibration.** The Harris M_V(HB) calibration includes dynamical parallaxes from velocity and proper-motion dispersions (G30). This is a dataset-scale input to every Harris distance. I make no judgement on it here.
- **D11. Values I opened, outside headers.**
  - The R_Sun, (m−M)_V and E(B−V) rows of NGC 104 and NGC 288, for D1.
  - Two rows each of the Rh, Dist, R_Sun, M_V,t and (M/L)1 observables, to see what the error columns hold.
  - The KM09 Q_pred column.
  - Plotting status of ten named clusters (systems.ecsv).
  - The dataset/plotted counts in measurements.ecsv.
  - Median relative σ and M/L errors of the plotted rows. I printed these by mistake while checking columns; they are not used in this report.
  - No g_obs or g_bar value was examined.

The main session can pass this to the third-party comparison.