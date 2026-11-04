# Strong lenses, Reader A (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Reader A report: uncertainty terms in the Strong lenses dataset (aeg-d-strong-lensing v1)

**Reader:** Reader A
**Dataset:** Strong lenses, package `aeg-d-strong-lensing/v1`
**Date:** 2026-11-04
**Repository state:** branch `reading/step-a-dwarfs-gc-lenses`, HEAD `8d9c11d`. The working tree was clean, I modified nothing, and the brief matched `32cbc9b`.
**Work directory:** `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/step-a-2026-11-04/lenses-A/`. Each download sits in its own directory: `dl/<id>/` for arXiv e-prints and `rel/fN/` for released tables. All Python ran with `python3 -I`.

## Package files read (read-only)

| File | SHA-256 |
|---|---|
| `REPRODUCTION.md` | 44e3b2715f4aab7ac40900e49fd2cf798679d02839363642dff7367c8f2467ef |
| `convert.py` | d67c651516df50ab288f517b7cf1cc6ed4ed9fe3b189f5882a634d02784df894 |
| `descriptor.json` | 46bb891edd3438a78c99b12f42dcdadc9f6cb730941dfd432192a37f90765b1b |
| `datapackage.json` | d27649c7546d68d0639487a2a130927d1743238a6ecc5c097d5ebe6d86329b9b |
| `sources.json` | bd7a97a418f8f093bc9eb08f99364b00a107294c6221fc340e8b3aa67dcfb06f |
| `gas_term.json` | faf4fecbf34e1bb8047de307b2eba054e324a32811c9bbbee40c65662518a891 |
| `reading/adjudicated_inputs.csv` | b29a0691c353c09a9de6fd86b59f438a37ae4a69b3109d3743a58934e2a65d3c |
| `reading/gas/adjudication_gas.md` (§4.3, §5, §6) | 9b9433d993b799d42e039dc50994819fb65f4e18532ac46a60a4f578e54b5cb7 |
| `tables/measurements.ecsv` (headers, plus one plotted row per scope to identify the error columns) | 8f321f711004e54cfa572c0b84847c9dd07d36c5b4b3ce9f03187def953ab877 |
| `docs/decisions.md` (D-063 to D-066, D-075, D-076) | 8eae6352d4105e3db852d2668ed56a20291866b17f36b525e27c80e0c025651d |

I also read `RESULT_SUMMARY.md`, the `tables/observables.ecsv` and `tables/systems.ecsv` headers, `data/assumptions.json` (all `a6s_*` entries) and `reading/adjudication.md` (searched for errors).

## Sources read

| Rec. | Paper | arXiv id / version | Main file | SHA-256 of e-print |
|---|---|---|---|---|
| R5 | Bolton et al. 2008, SLACS V | 0805.1931v1 | ms_arxiv.tex | fb72fd1120d6c53164d1442bd99c2dfa5b02ba81656febc67ce7e35c20e85cc5 |
| R13 | Grillo et al. 2009 | 0904.3282v2 | The e-print is a PDF only; read with pdftotext | df3746887007595b00e7fb2564ae1e9121e95849c68c04e55d2a06e3324587cf (= sources.json) |
| R7 | Auger et al. 2009, SLACS IX | 0911.2471v1 | ms.tex (§5 and §7 only) | 74db62e49adea4cb7dea3c6933378a9af0646704348a89c1dc619642a1b3b2d7 |
| R10 | Shu et al. 2017, S4TM | 1711.00072v2 | ms_arxiv_v2.tex | b23d5e6a2e56f667f3c8f77fa4b2edfe1c70ee15fa72a19bbec506680c565216 |
| R9 | Shu et al. 2015, SLACS XII | 1407.2240v2 | ms_v2.tex | eb8ec838e63006c8417d68d479b238448d59373984bee501e873b628724cace2 |
| R20 | Sonnenfeld et al. 2013a, SL2S III | 1307.4764v1 | sl2s-rm-pdflatex.tex | c7bc75399959c9a4e0e141c2892a3aff251c88f23ba6796ebfc162699b83aba2 |
| R21 | Sonnenfeld et al. 2013b, SL2S IV | 1307.4759v1 | sl2s-rx.tex (searched for redshift errors only) | 3559ca615c3f115b34c495346b038a4e9901b11b0acdadeb98df778be361d487 |
| R28 | Smith & Lucey 2013, SNL-0 | 1306.4983v1 | lensz_arXiv.tex | 937049df5ccec96465b3620079e83f3ca180b6f10c5d2b8b9bfc063c440820c8 |
| R25 | Smith, Lucey & Conroy 2015 | 1503.02661v1 | snellsI_arxiv.tex | 0d84014cd169eb0b96c5e18e08910e9e690b8632adba7db3d40e66ad23c7333c |
| R26 | Newman et al. 2017 | 1612.00065v2 | snells.tex | 1731105f1ad5dcb866e94ed71c245600462e28c3e451e00ea3ffc729e3d3b4c7 |
| R61 | Collier, Smith & Lucey 2018a | 1709.01931v1 | clean_snl12wcollier.tex | 6698ce848e622cc5058fdaf6996e6422f37ef2ba0cf5256fb11c639df123096e |
| R29 | Collier, Smith & Lucey 2018b | 1803.07082v1 | newlens.tex | c0e2dfd07e82d086bb59e8d74da318d8deea7a718ca9b90fbf56ef938d7cb46b |
| R32 | Smith et al. 2020, MaNGA lenses | 1911.06338v1 | main.tex | a2fe49d396d3ae46657cf37c726198e434e6b08b0ed2d70e28faefd90ebdac67 |
| R30 | O'Riordan et al. 2025, NGC 6505 | 2502.06505v1 | ms.tex | 7f4f5813fa3e0e52f0b59a240dc4ab32366779975aaed18119f0ad15d8dcfffb |
| R27 | Collier et al. 2020 | 2002.07191v1 | Downloaded but not read (alternative record only) | c15f94c12a9e16b785ec6affcf16a9814daf7eca3e13c327f999bb7311b1567a |

**Released tables fetched.** All four match the hashes in `sources.json`:

| File | SHA-256 |
|---|---|
| IOP `apjaa9794t1_ascii.txt` | 6af826bf2f6e4a0d4804c12e97c72ba56fefc619be3c4b0ad143cef38301a22d |
| IOP `apjaa9794t2_ascii.txt` | 497ca1aaf3bd3b9c546eb4f0e1ae40bfbac48fa384ee8a623ed293ecfba439ed |
| IOP `apj485108t6_mrt.txt` | 3c824245e6c0a5cafbe3036171fb70169697831c3bd76619afd5515b71af60f5 |
| IOP `apj485108t7_mrt.txt` | c6319d4f682eb2f4de25617c03d65636fd51df466aca1ef6afa3f8f99d175f02 |

**VizieR was not reachable.** The CfA mirror cut the transfer, the CDS mirror reset the connection, and IDIA returned a 403 from the proxy. I did not try to get around this. I therefore did not open the VizieR exports for R5 table5 or R13. I checked R13's error format against Table 4 of the paper PDF instead. For J0029−0055 it reads M*Cha,BC(≤R_Ein) = 5 (+2, −1) × 10¹⁰ M⊙, which matches the package row.

**Not read at source:**
- the gas-literature papers behind the registered gas term (N2, N7, N13, N14, N18 and others). I used the package's own adjudication file for that term;
- R33, R36, the FSPS and BC03 model papers, and R27.

The Wolf et al. 2010 estimator is not used in this package (D-064: projected masses, no 3σ²/r½), so I did not read it.

## Table of terms

"Atlas" in the last column means the v1 package. Abbreviations:
- **meas.** = `tables/measurements.ecsv`
- **obs.** = `tables/observables.ecsv`
- **sys.** = `tables/systems.ecsv`

Every system has one plotted value, so "point" and "system" coincide for every per-lens term.

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| L1 | SLACS θ_E (b_SIE) adopted empirical error | "Einstein radius $b$ & 0.2\% & 2\%"; "we will adopt a 2\% RMS fractional error as our best estimate of the uncertainty on measured Einstein radii" | R5 Table 3 (errortab); §6.1 | 2% (formal 0.2%) | Dataset-level number applied to each point | M_E, so g_obs. Also R_E, which enters both axes; see Doubts D1 | Yes. meas. `g_obs_err_lo/hi` (flag `sample_level_error`); not in obs. `err_lo/err_hi` (empty) |
| L2 | SLACS θ_E error used by R13 | "assuming a conservative 5% error in the values of the 'effective' Einstein angles measured by Bolton et al. (2008a)" | R13 §4.1 | 5% | Dataset | M_E (R13's own lensing mass) | No (R5's 2% is carried) |
| L3 | SLACS lens-model / method dependence of b | "The RMS fractional differences are 2\% for Paper~III and B07 … Paper~IV exhibit a larger 6\% fractional scatter, though this reduces to 3\%" (without two outliers); Table 5 prints both b_SIE and b_LTM | R5 §6.1; Table 5 | 2% (3–6% against Paper IV) | Point | g_obs (and R_E) | Folded into L1 by the source; b_LTM not carried |
| L4 | SLACS mass centred on light (assumption) | "As a fraction of the measured Einstein radii, the RMS shift is 3.5\%." | R5 §5.2 | RMS centroid shift 3.5% of R_E; effect on b not stated | Point | Not stated | No |
| L5 | S4TM θ_E and M_E | Table 2 has no error columns. R10: "Column 7 is the total projected mass within the Einstein radius from the best-fit lens model." R9 (earlier S4TM models): "we adopt this scatter [0.5%] as the fractional uncertainty in the measured Einstein radii for grade-A lenses" | R10 Table 2 note; R9 §3.1 | Not stated by R10; 0.5% stated by R9 for its own models | Point | g_obs, R_E | No (flag `no_uncertainty`) |
| L6 | External shear omitted (S4TM) | "We do not include any external shear in the lens model because it is a minor effect"; R9: "The overall fractional discrepancy is on the level of $2\%$"; mocks: "within an accuracy of about $4\%$" | R10 §4; R9 §4.3.1 | 2% (data), about 4% (mocks) | Point | g_obs, R_E | No |
| L7 | Line-of-sight mass / external convergence | R9: "external convergence $\kappa_{\rm ext}$ for SLACS lenses is no more than a few percent, and no significant bias was detected"; R28: "the rms contribution from large-scale structure is calculated to be ∼2 per cent for a z=2 source" | R9 §4.3.1; R28 §2.2 | "a few percent"; about 2% rms | Point | M_E, so g_obs | No |
| L8 | b_SIE intermediate-axis convention against circular θ_E | "accurate to $< 1\%$ on average within the axis-ratio ranges of our lenses"; "an almost constant offset of $-0.002$ on average in $\log_{10}\sigma_{\rm SIE}$" | R9 §3; §4.3.2 | Under 1%; −0.002 dex in σ_SIE | Dataset | R_E, M_E | No |
| L9 | Profile slope (non-isothermality) of the SIE | R9: "we tend to overestimate $\sigma_{\rm SIE}$ in low-mass galaxies … and underestimate … in high-mass galaxies"; R20: "mass models with density slope different from isothermal … can produce different Einstein radii" | R9 §4.3.3; R20 §4.1 | Direction stated by R9 (mass-dependent); size not stated ("We defer further quantitative studies") | Point (correlated with mass) | g_obs, R_E | No |
| L10 | Lens-light subtraction | "this foreground-subtraction strategy could introduce some systematic uncertainties in the lens and source parameters" | R10 §4 | Not stated | Point | g_obs | No |
| L11 | SL2S θ_E (68%, with 3% systematic) | "We thus take $3\%$ as our estimate of the systematic uncertainty … and convolve the posterior … with a Gaussian with $3\%$ dispersion. All the uncertainties on $R_{\rm Ein}$ quoted in this paper reflect this choice."; MRT: "e_Reff The 68% confidence interval on Reff" | R20 §4.1; t6 MRT byte description | Formal under 1%; total for the plotted pair 0.05″/1.76″ and 0.04″/1.16″ | Point (contains a dataset-level 3%) | g_obs, R_E | Yes. meas. `g_obs_err_lo/hi`; obs. `err_lo/err_hi` |
| L12 | SNL-0 M_E | "The adopted 4 per cent error reflects an conservative estimate of the systematic uncertainties, based on the difference between SIS- and MFL-model masses."; "within ∼1 per cent" for SIE ± shear | R28 §2.2 | 4% (±0.06 × 10¹¹) | Point | g_obs | Yes. meas. `g_obs_err_lo/hi`; obs. einstein_mass err. θ_E = 2.85″ has no printed error (not carried) |
| L13 | SNL-0 mass and radius come from different models | "we adopt the results of the MFL for the lensing mass-to-light ratio, and the nominal Einstein radius is that derived from the SIS model." | R28 §2.2 | MFL mass 4% above SIS | Point | g_obs | Covered by L12 only |
| L14 | SNL-1/2 lensing mass inside R_ap | "The quoted error is derived from the spread between lens profiles incorporating the flux ratio uncertainty."; "The positional errors provide a formal uncertainty of ≤0.5 per cent."; SNL-2: "The uncertainty is dominated by tension between the measured and predicted flux ratios." | R61 §5; Table 2 | 9.49 ± 0.15 and 12.59 ± 0.30 × 10¹⁰ M⊙ | Point | g_obs | Yes. meas. `g_obs_err_lo/hi`; obs. einstein_mass err |
| L15 | SNL-1/2 aperture against the HST half-separation | R_ap "2.38 & 2.21 & SLC15, SINFONI–based"; HST half-separation "2.43±0.03 … 2 per cent larger"; SNL-2 "2.30±0.03 arcsec (a 4 per cent increase on SLC15)" | R61 Table 1; §3 | 2% (SNL-1), 4% (SNL-2); ±0.03″ | System | R_E: both axes (M and L are both inside R_ap) | No. R_ap is used as R_E (flag `aperture_as_RE_half_image_separation`); the HST value is in obs. only |
| L16 | Symmetric half-image-separation lens approximation | "we find a scatter of ≲3 per cent, and a bias ≲1.5 per cent. External shear introduces a comparable level of noise. Including all sources of error, we estimate uncertainties of ∼5 per cent on the lensing masses." | R25 §4.1 | ≲3% scatter, ≲1.5% bias, about 5% total | Point | g_obs | No separate term (flag `model_dependence_half_image_separation`) |
| L17 | SNL-2 companion and flux-ratio tension | "there are no models which match both the image positions and the observed image flux ratio"; masses of "∼12.33" against "∼12.85 × 10^10" | R61 §4.2 | About 4% between the two regimes | System | g_obs | Within L14's ±0.30 only |
| L18 | J0403−0239 M_E and θ_E | "separated by 2.94±0.06 arcsec … uncertainty is derived from measurements at various emission lines"; "the 2 per cent uncertainty dominated by the measurement of R_Ein. Including a small ellipticity … increases the mass by 3 per cent … we revise the uncertainty in M_Ein to ∼4 per cent, i.e. 0.4×10^10" | R29 §3; §4 | θ_E ±0.03″; M_E about 4% (±0.4 × 10¹⁰) | Point | g_obs, R_E | Yes. M_E ±0.4 in meas. `g_obs_err_lo/hi`; θ_E error in obs. only |
| L19 | MaNGA θ_E, R_E and M_E | J1436: "the error reflecting the variation between models" (2.03±0.04); J1701: "we impose a 10 per cent error on θ_Ein"; Table 1 R_Ein 4.72±0.09 and 3.71±0.37 kpc; M_Ein 28.2±1.1 and 18.8±3.7 | R32 §3; §4; Table 1 | As printed | Point | g_obs, R_E | M_E error yes (meas. `g_obs_err_lo/hi`). R_E error in obs. only, not propagated (R_E is the coordinate) |
| L20 | NGC 6505 θ_E and M_E | "θE = 2″.500 ± 0″.001"; "The uncertainties indicated here should therefore be considered lower-bounds which only account for measurement uncertainty, and include no contribution from the systematic uncertainty."; M_E "1.53 × 10^11" with no error; Table 2 θ_E 2.496–2.503″ across models | R30 §5; §4.3; §3.5; Table 2 | ±0.001″ (lower bound); M_E not stated | Point | g_obs, R_E | θ_E error in obs. only; M_E no (`no_uncertainty`; meas. `g_obs_err` empty) |
| L21 | Redshift measurement errors | R30: "zd = 0.04243 ± 0.00003"; "A redshift z=0.4058 ± 0.003"; R28: "D_s/D_ls = 1.027 (with negligible error)" | R30 §3.1, §3.3; R28 §2.2 | As printed; none printed for SLACS, S4TM, SL2S, SNELLS, MaNGA | Point | Σ_cr and D_l, so g_obs and R_E | R30 only: sys. `redshift_err` and obs. `err_lo/hi`; not propagated |
| L22 | Peculiar velocity / redshift frame (distance) | R30: "results in a cosmological redshift of z=0.041±0.001"; R26: "we include an uncertainty corresponding to a 500 km s−1 peculiar velocity (3-4%)" and L "distance error not included"; R25: "Peculiar velocities of ∼500 km s−1 would induce shifts of up to 5 per cent in α"; R28: "WMAP7 cosmology, no peculiar velocity" | R30 §4.2; R26 §3, Table 1; R25 §4.3; R28 §2.2 | 0.041 against 0.04243 (about 3%); 3–4%; up to 5% in α | System | Distance: R_E on both axes, M_E ∝ D, L ∝ D_L² (Doubts D2) | No. NGC 6505 z = 0.041 is an alternative row; not plotted |
| L23 | Cosmology / H0 choice | R25: "Adopting H0=67 … rather than H0=70 … would yield smaller α by ∼5 per cent"; R29: "If we had prescribed the Planck 2016 cosmology, α would be 4 per cent lower"; R32: "adopting the [Bennett et al. 2014] cosmological parameters would increase α by 3.5 per cent" | R25 §4.3; R29 §4; R32 §5 | 3.5–5% in α | Dataset (per source) | M_E/(LΥ), i.e. g_obs relative to g_bar (Doubts D2) | No (`a6s_source_cosmology`, no slider) |
| L24 | SLACS M*(≤R_E): SED-fit error | "We measure the uncertainties in the best-fit parameters by projecting the joint probability density distribution onto the corresponding axes"; "typical errors on the order of 30%"; "(with 1 σ error bars)" | R13 §3; Fig. 9 caption | Per lens, asymmetric, 1σ | Point | g_bar | Yes. meas. `g_bar_err_lo/hi`; obs. `err_lo/err_hi` |
| L25 | SLACS fixed solar metallicity, dust-free templates | "dust-free templates at solar metallicity"; "the photometric mass estimates depend on the adopted metallicity"; R7: "the G09 choice of solar metallicity may therefore be inappropriate"; "G09 find systematically lower masses for the less massive systems (∼0.1 dex lower at 10^11 M⊙)" | R13 §3; R7 §5, §7 | About 0.1 dex at 10¹¹ M⊙, mass-dependent (R7) | Dataset (mass-dependent) | g_bar (R7: G09 low at low mass) | No |
| L26 | SLACS aperture factor (mass follows light, de Vaucouleurs) | "The implicit assumption made in this calculation is that the stellar mass is traced by the light distribution."; "⟨fap⟩ = 0.36 ± 0.01"; R5 "Effective radius $R_e$ & $<$0.2\% & 3.5\%" | R13 §4.2; R5 Table 3 | Per-lens f_ap error not stated; R_e 3.5% | Point | g_bar | No (taken as printed) |
| L27 | S4TM stellar mass: population assumptions | "we adopt a reference model with typical values of $t_{\rm form} = 4$ Gyrs, solar metallicity, and no dust"; "The level of the resulting systematic variation in estimated stellar mass is around 0.5 dex." | R9 §5 | 0.5 dex (metal-poor dust-free to dusty metal-rich) | Dataset (applies per system) | g_bar | No (`no_uncertainty`; no error in R10 Table 2) |
| L28 | S4TM profile step | R10 R_eff "(in the intermediate axis convention) … assuming a de Vaucouleurs model" (no error); R9's masses use "the core-Sérsic fit" | R10 Table 1 note; R9 §5 | Not stated | Point | g_bar | No (flags `mstar_in_RE_from_profile`, `profile_differs_from_mass_photometry`) |
| L29 | SL2S M*: statistical error and template systematic | t7 "e_logMChab … Error on logMChab"; "The relative scatter … is $0.06$ dex … and the bias is $0.01$ … in Paper IV, this systematic uncertainty is added to the statistical uncertainty on $M_*$" | R20 t7 MRT; §5 | Per lens (0.07 dex for the plotted pair); +0.06 dex systematic | Point plus dataset | g_bar | Table 7 error yes (meas. `g_bar_err_lo/hi`); the 0.06 dex no |
| L30 | SL2S CFHT R_e (profile step) | "The scatter on the quantity $R_{\rm eff,CFHT}-R_{\rm eff,HST}$ is ∼30%; we take this as our uncertainty on CFHT effective radii." | R20 §3.1; Table 4 comments | 30% | Point | g_bar (via f(<R_E)) | No |
| L31 | SL2S photometry contamination | "Uncertainties on CFHT lens galaxy magnitudes are dominated by contamination from the background source and are estimated to be $0.3$ in $u$ band, $0.2$ in $g$ and $r$, $0.1$ in all redder bands" | R20 §3.1 | 0.1–0.3 mag | Point | g_bar | Only through L29 (inference) |
| L32 | SNL-0 L_r inside θ_E | "with 2-3\% uncertainties estimated from photometric zero-point and Galactic extinction errors"; Table 1 "M_{r,⊙} = 4.64 AB; distance error not included" | R26 §3; Table 1 | 2.84 ± 0.06 × 10¹⁰ | Point | g_bar | Yes, in quadrature in meas. `g_bar_err_lo/hi` |
| L33 | SNL-0 (M*/L_r)_MW (Kroupa) | "4.04 ± 0.10 … Kroupa IMF"; "our spectra now constrain $(M_*/L_r)_{\rm MW}$ to 2-7\%" | R26 Table 1; §5.2 | ±0.10 (2–7%) | Point | g_bar | Yes, in quadrature in meas. `g_bar_err_lo/hi` |
| L34 | SNL-1/2 L_F814W inside R_ap | "2.52±0.04 & 3.86±0.07 & extinction and band-shifting corrected" | R61 Table 1 | As printed | Point | g_bar | Yes. meas. `g_bar_err_lo/hi` (L only) |
| L35 | SNL-1/2 converted Υ_ref | "combined with the converted Υref of 2.75 (Newman et al. 2017)"; "With the converted Υref = 2.59" (no error; R26 prints 3.93±0.20 and 3.65±0.24 in r) | R61 §5; R26 Table 1 | Not stated after conversion | Point | g_bar | No (`no_uncertainty`) |
| L36 | SNL-1 internal dust | "the HST imaging reveals dust obscuration within the central region (∼1 arcsec …). This suggests the presence of a small cold ISM disc." | R61 §3 | Not stated | System | g_bar (L) | No |
| L37 | SNL-2 neighbour light | "we estimate that this contribution is only 1.5%, a minor effect that we neglect." | R26 §3 | 1.5% of L_Ein (r band, R26 photometry) | System | g_bar | No |
| L38 | J0403 L_i and its corrections | "aperture luminosity of 2.59±0.12 ×10^10 L⊙. The uncertainty is dominated by the applied corrections."; extinction "0.24 mag … error of 0.04 mag"; PSF 0.22±0.02; k 0.04±0.01; M⊙ 4.534 | R29 §3–4 | ±0.12 (4.6%) | Point | g_bar | Yes. meas. `g_bar_err_lo/hi` |
| L39 | J0403 Υ_Ref and population systematics | "ΥRef = 2.90±0.10. The uncertainty is derived from small variations in the metallicity and age (e.g. z_form = 2.5–3.5, metallicity 1–1.5 solar)"; 8.5 Gyr: "α would have increased by 14 per cent"; Maraston: "α would increase by 10 per cent"; "further uncertainty of (∼15 per cent) ±0.17 for the systematics" | R29 §4; §5 | ±0.10; 10–15% in α | System (assumed population) | g_bar | ±0.10 yes (in quadrature); 10–15% no |
| L40 | MaNGA L_i and Υ_ref | L 6.72±0.10 and 5.56±0.35; "The full range in Υref … is 2.41–3.46; our calculations adopt this as the 2σ interval, i.e. we assume Υref = 2.93±0.26"; Maraston "would increase α by ∼12 per cent"; PSF "∼0.1 mag", extinction "∼0.04 mag", band-shift "∼0.09 mag", M⊙,i 4.53 | R32 §5; Table 1 | As printed | L: point. Υ_ref: shared by both MaNGA systems (dataset within R32) | g_bar | Both in quadrature in meas. `g_bar_err_lo/hi`, carried per system; 12% no |
| L41 | NGC 6505 M*(<θ_E), Prospector | "M⋆Chab = (1.06 ± 0.02) × 10^11"; "An error floor of 5% is introduced to account for various systematics in the underlying stellar models" | R30 §3.2; §3.1 | ±2% (fit); 5% floor applied inside the fit | Point | g_bar | Yes. meas. `g_bar_err_lo/hi` |
| L42 | IMF (Chabrier/Kroupa → Salpeter) | R13: "more than one and a half times higher"; R29 "Salpeter … has α = 1.55"; R32 "α ≈ 1.65"; R30 "dividing them with a constant factor of 0.61"; R20 prints Salpeter columns | R13 §3; R29 §4; R32 §5; R30 §3.1; R20 Table 7 | Factor about 1.55–1.8 (per-source values) | Dataset | g_bar (upward) | Yes. Slider `a6s_stellar_imf` via meas. `x_strong_lensing_mstar_top_msun` (S4TM uses R30's factor). SNELLS: none (`imf_top_not_read`) |
| L43 | Population-synthesis model family | R13: Salpeter BC and M "consistent, within the errors"; R29 "+10 per cent"; R32 "∼12 per cent" (Maraston against Conroy) | R13 §3; R29 §4; R32 §5 | 10–12% in α | Dataset | g_bar | SLACS Maraston pair only as `role = alternative` rows (not plotted); else no |
| L44 | Gas inside R_E | Sources: R28 "We assume the gas mass projected within the Einstein radius is negligible."; R25 "gas and central black holes, are neglected"; R32 "expected to be negligible". Atlas: hot 0.0012 (0.00015–0.025), cold 0 (0–0.02) of M*(<R_E) | R28 §3 fn; R25 §4.2; R32 §5; `gas_term.json`; D-076 item 1 | 0.12% (0.015–2.5% hot; 0–2% cold) | Dataset | g_bar (upward) | Yes. Slider `a6s_gas_in_RE`: meas. `g_bar_gas_hot/cold`, `x_strong_lensing_gas_{hot,cold}_frac(_min/_max)` |
| L45 | Central black hole | R28: "the mean expected black hole mass is 2.5×10^9 M⊙, or 2 per cent of M_Ein"; R25: "∼1.4×10^9 M⊙" | R28 §4; R25 §4.2 | About 2% of M_E (SNL-0) | System | Inside M_E; not in g_bar (Doubts D9) | No |
| L46 | Lensed-source light in lens photometry | R13: "our photometric mass measurements are not affected in any significant way by the lensed objects" | R13 §3 | "not … significant" | Point | g_bar | No |

## Terms that move g_obs and g_bar together

**1. The Einstein radius.** R_E = θ_E·D_l is the denominator of both g_obs = G M_E/R_E² and g_bar = G M*(<R_E)/R_E². The Atlas holds R_E fixed and puts the θ_E error only into M_E and hence g_obs (`convert.py` lines 48–49; meas. column description "From the M_E error at fixed R_E"). See Doubts D1 for what this implies when M_E is computed from θ_E.

**2. Distance and cosmology (L22, L23).** R_E ∝ D_l on both axes, M_E ∝ D, and L or M* ∝ D_L². The three sources that size the effect state it as a change in α ∝ (lensing mass)/(L Υ): 3.5–5% for H0, and up to 5% for a 500 km s⁻¹ peculiar velocity. They therefore state that distance moves the two masses differently, not together. See D2.

**3. The SNELLS aperture (L15).** It is shared by the lensing mass and the luminosity, so R_ap moves both axes. The R_ap against HST half-separation difference is 2% (SNL-1) and 4% (SNL-2).

**4. One-sided terms.** IMF (L42), gas (L44), population family (L43) and metallicity (L25) move g_bar only.

## Not stated (what I looked for and where)

- **Redshift errors** for SLACS (R5 text and Table 4 notes), S4TM (R10 Table 1 note), SL2S (R21 tex; searched "uncertaint", "accura", "error"), SNELLS (R28, R25, R61 tables) and MaNGA (R32 Table 1). Only R30 prints them.
- **Per-lens error on M_E or θ_E in R10 (S4TM):** Table 2 and §4. None.
- **Error on R10's de Vaucouleurs R_eff:** Table 1 note. None.
- **Confidence level of R20 Table 7 stellar-mass errors:** table comments and MRT. None. Table 6 is "68%".
- **Confidence level of R26 Table 1 and R61 Table 1 errors:** not stated.
- **Error on R13's per-lens f_ap, and whether R13's M*(≤R_E) errors include the θ_E or θ_e error:** §4.2. Not stated.
- **Error on R30's printed M_E:** §3.5. None.
- **Error of R61's ezgal band conversion of Υ_ref:** §5. Not stated.
- **Effect of SNL-1's central dust on L_F814W:** R61 §3. Not stated.
- **Luminosity distance and cosmology behind R30's Prospector mass:** §3.1–3.2. Not stated beyond the global Planck 2015 cosmology in §1.
- **Any source statement on projection (cylinder against sphere) accuracy:** all sources work in projection; R13 "disk", R25 "circular aperture". None quantifies a deprojection, and none is needed under D-064.
- **Solar absolute magnitude for R61's L_F814W:** not found in the text.
- **Dust as a baryonic component inside R_E:** no source. The descriptor says "not_addressed".

## Doubts and inferences (not direct quotes)

**D1. θ_E error and computed M_E (inference from the formulas).** For systems whose M_E is computed from θ_E (SLACS, SL2S), M_E = Σ_cr π R_E² (R10 §4 equation; R13 Eq. 8). It follows that g_obs = G M_E/R_E² = π G Σ_cr, independent of θ_E. A θ_E error then moves g_bar (through 1/R_E² and M*(<R_E)) and leaves g_obs unchanged. The package instead carries it as a g_obs error at fixed R_E. The same applies approximately to printed M_E values whose error is dominated by R_E (R29: "dominated by the measurement of R_Ein"). This is my derivation; no source states it.

**D2. Distance (inference, with stated support).** From M_E ∝ R_Ein² D (R25 §4.1 equation), R_E ∝ D_l and L from the luminosity distance:
- g_obs ∝ 1/D to first order;
- g_bar is roughly independent of D for luminosity-based M*.

R25, R29 and R32 state α shifts of 3.5–5% with H0, which agrees with this. The registry note on `a6s_source_cosmology` ("g_obs/g_bar does not depend on it to first order") and D-064 item 4 ("both masses scale with the same distances") read differently from those source statements. I report the difference and settle nothing.

**D3. Disagreement on the SLACS θ_E error.** R5 adopts 2% and R13 uses 5% for the same radii (L1, L2). R9 finds 0.5% scatter between its refits and R5's.

**D4. Disagreement on SLACS stellar masses.** R7 states R13's masses are about 0.1 dex low at 10¹¹ M⊙ and questions R13's solar metallicity (L25).

**D5. Rounding (inference).**
- R13 prints M*(≤R_E) as integers in units of 10¹⁰ M⊙. For J0405−0455 the default is 1 (−1, +1) × 10¹⁰ per the adjudication table, so the lower error equals the value.
- R7 and R10 round log masses to 0.01 dex.

No source gives a rounding error; any size would be my estimate.

**D6. SL2S Table 7 column order.** The MRT byte description orders the columns Chab, Salp, ChabNIR, SalpNIR. The paper header orders them Chab, Chab(NIR), Salp, Salp(NIR). The package follows the paper header (adjudication §3c). For the plotted pair it uses 11.59 ± 0.07 and 11.27 ± 0.07 as Chab(NIR). I did not re-adjudicate this.

**D7. Shape mismatch (inference).** R13 §4.1 states that the SIE mass is that "enclosed within the elliptical critical curves", while R13's f_ap integrates a circular de Vaucouleurs profile (Eq. 11). Whether the two masses refer to exactly the same region is not stated.

**D8. MaNGA Υ_ref range.** R32 states it as a 2σ model range common to both lenses. The package adds ±0.26 in quadrature per system, as if it were independent between them.

**D9. Black hole and gas.** The black hole (L45) is inside the measured M_E. Whether it counts as "detected baryons" for g_bar is a definitional question no source addresses. I list it as "moves: neither as carried". The three sources' "gas negligible" statements conflict with the registered nonzero hot-gas default. D-076 keeps both, as notes and term.

**D10. SNL-0 mass and radius from different models (L13).** The printed M_E (MFL) sits at the SIS θ_E. RESULT_SUMMARY's formula-check ratio of 0.969 reflects this.

**D11. Scale labels are mine.** "Dataset" for a sample-wide adopted error (L1, L11's 3%, L27) means one number applied identically to every point. Its realisation per lens is independent, so it could also be read as "point". I flag the choice.

**D12. Not verified at source.** The VizieR files for R5 table5 and R13 (blocked). The gas-term literature. R7 beyond §5 and §7, and R21 beyond its redshift-error statements.