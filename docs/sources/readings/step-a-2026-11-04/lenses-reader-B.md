# Strong lenses, Reader B (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

I'm Reader B for **Strong lenses (`aeg-d-strong-lensing` v1)**. The full report is below. I read 13 papers at source, plus the package and the released tables, with one exception: the gas literature behind the registered gas term (row L52; `Not stated` part 7).

The findings most likely to matter, in short:
- **Distance and H0 move both axes, and the sources disagree with D-064 item 4 (Doubts 1).** D-064 says the g_obs/g_bar ratio "does not depend on [cosmology] to first order". Three sources say a mass-to-light ratio built this way changes with distance or H0 (rows L32–L35). The package carries no distance or H0 term.
- **The Einstein-radius error also moves both axes and R_E (Doubts 2).** v1 puts it on g_obs alone, at fixed R_E. The sources disagree on its size: 2%, a "conservative 5%", 0.5% and 3% (row L1; Doubts 3).
- **Several stated systematics are not carried.** The stellar-mass systematic for S4TM is about 0.5 dex. The SL2S template systematic is 0.06 dex. The CFHT effective radius behind the SL2S profile step is uncertain by 30%. NGC 6505's lens-model errors are stated by the source to be lower bounds.

---

# Reader B: strong lenses (`aeg-d-strong-lensing` v1), uncertainty terms

**Reader:** Reader B. **Date:** 2026-11-04. **Work directory:** `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/step-a-2026-11-04/lenses-B/`

**Scope.** I covered the 94 plotted default rows, by survey:
- SLACS 48: R5 observed side, R13 stellar side;
- S4TM 37: R10, with method paper R9;
- SL2S 2: R20, with redshifts from R21;
- SNL-0: R28 observed side, R26 stellar side, cosmology from R25;
- SNL-1 and SNL-2: R61;
- J0403−0239: R29;
- MaNGA 2: R32;
- NGC 6505: R30.

Alternatives and the epoch-gap systems were not read for uncertainty terms.

**Package read (read-only):**
- `REPRODUCTION.md`, `convert.py`, `descriptor.json`, `sources.json`, `gas_term.json`, `RESULT_SUMMARY.md`;
- the column metadata of `tables/*.ecsv`, plus values only where needed to tell what an error column holds;
- `reading/adjudicated_inputs.csv`, `reading/gas/adjudication_gas.md` §3–5;
- decisions D-063, D-064, D-065, D-066, D-075 and D-076.

**Quote convention.** Quotes are from the LaTeX source, with markup rendered: `$\sim$3\,per cent` is written "∼3 per cent". Locations are given as file:line in the extracted e-print, so each row can be checked with `sed -n`.

## Sources read

| Rec. | Paper | arXiv id | Main file read | SHA-256 of downloaded e-print |
|---|---|---|---|---|
| R5 | Bolton et al. 2008 (SLACS V) | 0805.1931v1 | ms_arxiv.tex | fb72fd1120d6c53164d1442bd99c2dfa5b02ba81656febc67ce7e35c20e85cc5 |
| R13 | Grillo et al. 2009 | 0904.3282v2 | e-print is a PDF; read via pdftotext (plain.txt) | df3746887007595b00e7fb2564ae1e9121e95849c68c04e55d2a06e3324587cf (= sources.json) |
| R10 | Shu et al. 2017 (S4TM) | 1711.00072v2 | ms_arxiv_v2.tex | b23d5e6a2e56f667f3c8f77fa4b2edfe1c70ee15fa72a19bbec506680c565216 |
| R9 | Shu et al. 2015 (SLACS XII) | 1407.2240v2 | ms_v2.tex | eb8ec838e63006c8417d68d479b238448d59373984bee501e873b628724cace2 |
| R20 | Sonnenfeld et al. 2013a (SL2S III) | 1307.4764v1 | sl2s-rm-pdflatex.tex (+ cfhtfit, lensfit, mstartable .tex) | c7bc75399959c9a4e0e141c2892a3aff251c88f23ba6796ebfc162699b83aba2 |
| R21 | Sonnenfeld et al. 2013b (SL2S IV) | 1307.4759v1 | sl2s-rx.tex, spectable.tex | 3559ca615c3f115b34c495346b038a4e9901b11b0acdadeb98df778be361d487 |
| R28 | Smith & Lucey 2013 (SL13) | 1306.4983v1 | lensz_arXiv.tex | 937049df5ccec96465b3620079e83f3ca180b6f10c5d2b8b9bfc063c440820c8 |
| R25 | Smith, Lucey & Conroy 2015 (SLC15) | 1503.02661v1 | snellsI_arxiv.tex | 0d84014cd169eb0b96c5e18e08910e9e690b8632adba7db3d40e66ad23c7333c |
| R26 | Newman et al. 2017 | 1612.00065v2 | snells.tex | 1731105f1ad5dcb866e94ed71c245600462e28c3e451e00ea3ffc729e3d3b4c7 |
| R61 | Collier, Smith & Lucey 2018a | 1709.01931v1 | clean_snl12wcollier.tex | 6698ce848e622cc5058fdaf6996e6422f37ef2ba0cf5256fb11c639df123096e |
| R29 | Collier, Smith & Lucey 2018b | 1803.07082v1 | newlens.tex | c0e2dfd07e82d086bb59e8d74da318d8deea7a718ca9b90fbf56ef938d7cb46b |
| R32 | Smith et al. 2020 | 1911.06338v1 | main.tex | a2fe49d396d3ae46657cf37c726198e434e6b08b0ed2d70e28faefd90ebdac67 |
| R30 | O'Riordan et al. 2025 | 2502.06505v1 | ms.tex | 7f4f5813fa3e0e52f0b59a240dc4ab32366779975aaed18119f0ad15d8dcfffb |

**Released files, fetched and checked against `sources.json`:**
- **IOP tables** (`rel/`), full-file SHA-256 identical to `sources.json`:
  - S4TM t1 6af826bf…, t2 497ca1aa…;
  - SL2S III t6 3c824245…, t7 c6319d4f….
- **VizieR exports** (CfA mirror):
  - J/A+A/501/461/lens: content SHA-256 61d683a6… (= `sources.json`);
  - J/ApJ/682/964/table5: content SHA-256 6a83e12f… (= `sources.json`).
- **Mirror failures:** the CDS mirror reset the connection, and the IDIA mirror returned proxy 403. I did not try to get around either block.

**Downloaded but not read:** 0911.2471v1 (R7, used for a check only) and 2002.07191v1 (R27, used for an alternative row only).

## Terms

Scale: P = point, S = system, D = dataset. One value per lens, so **P and S coincide for every term below**. "D(src)" means shared by all systems from that one source.

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| L1 | θ_E measurement error, SLACS | "In subsequent analyses, we will adopt a 2% RMS fractional error as our best estimate of the uncertainty on measured Einstein radii. For comparison, the median formal statistical error … is 0.2%." | 0805.1931 ms_arxiv.tex:972–975, §5.1; Table 3 (errortab) l.928 "Einstein radius b & 0.2% & 2%" | 2% RMS (formal 0.2%) | S (one fractional size for the whole sample) | g_obs via M_E ∝ θ² (also R_E; see Doubts 2) | Yes: `measurements.g_obs_err_lo/hi` (2% θ → M_E), flag `sample_level_error`. Not in `observables` θ_E err (empty). |
| L2 | θ_E error used by Grillo for SLACS M_tot | "assuming a conservative 5% error in the values of the 'effective' Einstein angles measured by Bolton et al. (2008a)" | 0904.3282 plain.txt:1669–1671, §4.1 | 5% | S | g_obs | No (v1 uses R5's 2%; R13's M_tot not used) |
| L3 | θ_E error, S4TM grade-A (method paper) | "we adopt this scatter as the fractional uncertainty in the measured Einstein radii for grade-A lenses since the statistical errors significantly underestimate the uncertainties" (scatter "0.5%") | 1407.2240 ms_v2.tex:138, §3.1; Fig. 1 caption l.133 "rms=0.005" | 0.5% | S | g_obs | No: R10 prints no error; v1 sets `no_uncertainty` |
| L4 | θ_E error, SL2S | "We thus take 3% as our estimate of the systematic uncertainty … and convolve the posterior … with a Gaussian with 3% dispersion. All the uncertainties on R_Ein quoted in this paper reflect this choice." Also "68% credible intervals (1-σ uncertainties)" | 1307.4764 sl2s-rm-pdflatex.tex:477–478, 462, §4.1; MRT t6 "e_Reff The 68% confidence interval on Reff" | printed per lens, incl. 3% systematic; formal "<1%" (l.467) | S | g_obs | Yes: `g_obs_err_lo/hi` from θ_E err; `observables` einstein_radius err |
| L5 | Lens-model (radial profile) dependence of the aperture mass | "In the case of Einstein ring images or symmetric quadruple-image lenses, this aperture-mass measurement is nearly independent of the radial density profile … When the lensed image configuration is significantly asymmetric, the Einstein radius parameter … becomes somewhat dependent on the assumed mass model" | 0805.1931 ms_arxiv.tex:843–848, §4.2 | not stated (LTM b_LTM printed per lens in Table 4) | S | g_obs | No (b_LTM not packaged) |
| L6 | SIE vs SPLE slope (non-isothermality) | "we tend to overestimate σ_SIE in low-mass galaxies (γ′ > 2) and underestimate σ_SIE in high-mass galaxies (γ′ < 2) … We defer further quantitative studies" | 1407.2240 ms_v2.tex:398–400, §4.4.3 | not stated | S (correlated with mass) | g_obs | No |
| L7 | External convergence (mass sheet) | "the external convergence κ_ext for SLACS lenses is no more than a few percent … only introduce random noise rather than bias" | 1407.2240 ms_v2.tex:386, §4.4.1 | "no more than a few percent" | S | g_obs | No |
| L8 | External shear omitted (S4TM/SLACS models) | "The overall fractional discrepancy is on the level of 2% … we are able to recover the Einstein radii within an accuracy of about 4%" | 1407.2240 ms_v2.tex:388, §4.4.1 | 2% (data); ≈4% (mocks) | S | g_obs | No |
| L9 | b_SIE (intermediate-axis) vs circular θ_E convention | "the ellipicity-dependent b_SIE–θ_E relation from Huterer05, which is accurate to < 1% on average" and "an almost constant offset of −0.002 on average in log₁₀ σ_SIE" | 1407.2240 ms_v2.tex:117, 392; 0805.1931 l.764–766 (intermediate-axis normalisation) | <1%; −0.002 dex in σ_SIE | D(src) convention, S value | g_obs | No |
| L10 | Lens-light subtraction (S4TM) | "this foreground-subtraction strategy could introduce some systematic uncertainties in the lens and source parameters" | 1711.00072 ms_arxiv_v2.tex:291–292, §4 | not stated | S | g_obs | No |
| L11 | Line-of-sight structure inside M_E | "the rms contribution from large-scale structure is calculated to be ∼2 per cent for a z = 2 source (Taruya et al. 2002)" | 1306.4983 lensz_arXiv.tex:320–322, §2.2 | ∼2% rms | S | g_obs | No |
| L12 | SNL-0 M_E systematic (SIS vs MFL) | "The adopted 4 per cent error reflects an conservative estimate of the systematic uncertainties, based on the difference between SIS- and MFL-model masses." Other models "within ∼1 per cent" | 1306.4983 lensz_arXiv.tex:317–325, §2.2 | 4% (1.50±0.06 ×10¹¹) | S | g_obs | Yes: `g_obs_err_lo/hi` (printed M_E err) |
| L13 | SNL-0 θ_E (SIS) has no error; M_E is MFL inside the SIS radius | "we adopt the results of the MFL for the lensing mass-to-light ratio, and the nominal Einstein radius is that derived from the SIS model" | 1306.4983 lensz_arXiv.tex:316; Table 3 l.611 "2.85 arcsec" | not stated | S | both (R_E) | No |
| L14 | Symmetric (half-separation) approximation | "we find a scatter of ≲3 per cent, and a bias ≲1.5 per cent. External shear introduces a comparable level of noise. Including all sources of error, we estimate uncertainties of ∼5 per cent on the lensing masses." | 1503.02661 snellsI_arxiv.tex:652–653, §4.1 | ≲3% scatter, ≲1.5% bias, ∼5% total | S | g_obs | Superseded for SNL-1/2 by R61 (L15); flag `model_dependence_half_image_separation` |
| L15 | SNL-1/SNL-2 adopted mass inside R_ap | "The quoted error is derived from the spread between lens profiles incorporating the flux ratio uncertainty … The positional errors provide a formal uncertainty of ≤ 0.5 per cent." SNL-2: "The uncertainty is dominated by tension between the measured and predicted flux ratios." | 1709.01931 clean_snl12wcollier.tex:315, 317, §5; Table 2 l.250 | 9.49±0.15, 12.59±0.30 ×10¹⁰ M⊙ (1.6%, 2.4%) | S | g_obs | Yes: `g_obs_err_lo/hi` |
| L16 | R_ap vs HST half-separation | "Fiducial aperture, R_ap (arcsec) & 2.38 & 2.21 & SLC2015, SINFONI–based"; "Half image-separation (arcsec) & 2.43±0.03 & 2.30±0.03 & this paper, HST–based" | 1709.01931 Table 1 l.151, 156 | 2–4% difference in radius; ±0.03″ | S | both (R_E, and M and L both inside R_ap) | Half-separation carried as `observables` alternative; R_ap has no error |
| L17 | SNL-2 companion | "a nearby galaxy within a common, extensive and non-symmetric diffuse light halo"; SLC15: "revised downwards by 8–16 per cent. We adopt a correction of 12 per cent and an increased lensing mass error of 10 per cent" | 1709.01931 l.192–197; 1503.02661 l.669–671 | 8–16% (SLC15; superseded by R61) | S | g_obs (and g_bar via light: L44) | Partly: R61 error only (L15) |
| L18 | J0403 M_E (half-separation, ellipticity, shear) | "with the 2 per cent uncertainty dominated by the measurement of R_Ein. Including a small ellipticity (e ≈ 0.1 …) increases the mass by 3 per cent … we revise the uncertainty in M_Ein to ∼4 per cent" | 1803.07082 newlens.tex:210, §4 | 4% (±0.4 ×10¹⁰) | S | g_obs | Yes: `g_obs_err_lo/hi` |
| L19 | J0403 R_Ein = half separation | "The lensed images are separated by 2.94 ± 0.06 arcsec … where the uncertainty is derived from measurements at various emission lines … we adopt R_Ein as half of the image separation, 1.47 ± 0.03 arcsec" | 1803.07082 newlens.tex:196, §3 | ±0.03″ (2%) | S | both (R_E; M_E) | `observables` θ_E err; not in g errors (fixed R_E) |
| L20 | MaNGA J1436 θ_E model spread | "we adopt θ_Ein = 2.03±0.04, averaging the results from pixelised and parametric models with shear, with the error reflecting the variation between models" | 1911.06338 main.tex:176, §3 | ±0.04″ | S | g_obs (M_E printed 28.2±1.1) | Yes: `g_obs_err_lo/hi` from printed M_E err |
| L21 | MaNGA J1701 imposed error | "to reflect the greater systematic uncertainty in modelling J1701, we impose a 10 per cent error on θ_Ein" | 1911.06338 main.tex:261, §4 | 10% on θ_E; M_E ±3.7 (20%) | S | g_obs | Yes: `g_obs_err_lo/hi` |
| L22 | MaNGA R_E in kpc error | Table 2 "R_Ein & kpc & 4.72±0.09 & 3.71±0.37" | 1911.06338 main.tex Table 2 (l.326) | ±0.09, ±0.37 kpc | S | both | `observables` einstein_radius err only; not in g errors |
| L23 | NGC 6505 lens-model errors are lower bounds | "The uncertainties indicated here should therefore be considered lower-bounds which only account for measurement uncertainty, and include no contribution from the systematic uncertainty." | 2502.06505 ms.tex:798, §4.3 | θ_E ±0.001″ (l.813); systematic not stated | S | g_obs | θ_E err in `observables`; M_E has no error → `g_obs_err` empty, `no_uncertainty` |
| L24 | NGC 6505 M_E printed without error | "given that the mass enclosed by the Einstein radius is 1.53 × 10¹¹ M⊙" | 2502.06505 ms.tex:778, §3.5 | not stated | S | g_obs | `no_uncertainty` |
| L25 | NGC 6505 shear / group | "the measured strength of the external shear component is small (2.7%) … [Henry1995] find evidence in X-ray emission that the galaxy is part of a small group" | 2502.06505 ms.tex:794, §4.3 | 2.7% shear; effect on M_E not stated | S | g_obs | No |
| L26 | S4TM M_E printed without error | Table 2 note: "Column 7 is the total projected mass within the Einstein radius from the best-fit lens model." (no error column) | 1711.00072 ms_arxiv_v2.tex:521; IOP t2 | not stated | S | g_obs | `no_uncertainty` |
| L27 | Central black hole (in M_E, not in g_bar) | SLC15: "The average central black-hole mass for σ = 300 km/s early-type galaxies is ∼1.4×10⁹ M⊙"; R30: "only (0.57 +0.68/−0.31)% of the mass within the Einstein radius, we do not include it" | 1503.02661 l.772–773; 2502.06505 l.778 | ∼1.4×10⁹ M⊙; 0.57% of M_E | S | g_obs (contains it); g_bar (does not) | No |
| L28 | Lens redshift, SLACS/S4TM/SL2S | printed without error (SLACS V Table 1 z_FG; S4TM Table 1 note "inferred from the SDSS spectrum"; SL2S IV Table 2) | 0805.1931 l.1783ff; 1711.00072 l.386; 1307.4759 spectable.tex | not stated | S | both | No (`redshift_err` empty) |
| L29 | NGC 6505 z_l and z_s | "We measure a redshift for the galaxy of z_l = 0.04243 ± 0.00003"; "A redshift z = 0.4058 ± 0.003 is derived" | 2502.06505 ms.tex:639, 698 | ±0.00003; ±0.003 | S | both | Yes: `systems.redshift_err`, `observables` redshift err; not in g errors |
| L30 | Peculiar velocity, NGC 6505 | "3% of the redshift of NGC 6505 comes from a bulk flow away from us. On top of the bulk flow peculiar velocities of individual galaxies are typically present at the 150 km/s level. Combining these two effects results in a cosmological redshift of z=0.041±0.001" | 2502.06505 ms.tex:790, §4.2 | z 0.04243 → 0.041±0.001 (≈3.4%) | S | both | Alternative row only (`role=alternative`, z = 0.041); not an error bar |
| L31 | Peculiar velocity / distance, SNELLS | "The lensing M/L is proportional to distance, which was derived from the Hubble flow, and we include an uncertainty corresponding to a 500 km/s peculiar velocity (3–4%)." Also Table 1: L_r,Ein "distance error not included" | 1612.00065 snells.tex:139, §3; Table 1 l.106 | 3–4% | S | both (M ∝ D, L ∝ D², R_E ∝ D) | No ("Distance errors are not added", REPRODUCTION.md) |
| L32 | Peculiar velocity, SLC15 | "Peculiar velocities of ∼500 km/s would induce shifts of up to 5 per cent in α, depending on lens redshift." | 1503.02661 snellsI_arxiv.tex:864–865, §4.3 | up to 5% in α (∝ M*/L) | S | both | No |
| L33 | Distance definition, SNL-0 | "We assume a luminosity distance of 152 Mpc (WMAP7 cosmology, no peculiar velocity)" | 1306.4983 lensz_arXiv.tex:292, §2.2 | not stated | S | both | No |
| L34 | H0 / cosmology choice | SLC15: "Adopting H0 = 67 … from the Planck cosmology … rather than H0 = 70 … from WMAP7, would yield smaller α by ∼5 per cent." R29: "If we had prescribed the Planck2016 cosmology, α would be 4 per cent lower, due to the variation in H0." R32: "adopting the Bennett 2014 cosmological parameters would increase α by 3.5 per cent." | 1503.02661 l.862–863; 1803.07082 l.241; 1911.06338 l.293 | 5%, 4%, 3.5% in α | D(src) | both | Values only: `x_strong_lensing_h0`, `_om` per row; no range |
| L35 | Cosmologies adopted | R5 "Ω_M = 0.3 … Ω_Λ = 0.7, and … H_0 = 70" (l.188–191); R13 "H0 = 70 … Ωm = 0.3, ΩΛ = 0.7" (plain.txt:118–120); R10 "Ω_m = 0.274, Ω_Λ = 0.726 and H_0 = 70" (l.156–157); R20 (l.164–165); R28/R25/R61/R29 WMAP7 "H_0 = 70.4 … Ω_m = 0.272"; R32 "We adopt the cosmological parameters from Planck2018" (main.tex:100, no numbers); R30 "Planck 2015 cosmology with H_0=67.8 … and Ω_m=0.308" (ms.tex:570) | as cited | — | D(src) | both | `x_strong_lensing_h0/_om`; flags `cosmology_named_only`, `flatness_not_stated` |
| L36 | Stellar-mass statistical error, SLACS (R13) | "We measure the uncertainties in the best-fit parameters by projecting the joint probability density distribution onto the corresponding axes"; "typical errors on the order of 30%"; Fig. 9: "The mass estimates (with 1 σ error bars) are considered within the disks defined by the Einstein radii" | 0904.3282 plain.txt:952, 1035, 2975; VizieR E_/e_MChaBC2 | ∼30% typical, 1σ, asymmetric, integer ×10¹⁰ | S | g_bar | Yes: `g_bar_err_lo/hi`; `observables` mass_star err |
| L37 | Aperture factor f_ap (light traces stellar mass) | "The implicit assumption made in this calculation is that the stellar mass is traced by the light distribution." "⟨f_ap⟩ = 0.36 ± 0.01" | 0904.3282 plain.txt:1701–1705, §4.2 | f_ap has no per-lens error (VizieR `fap` has no error column) | D (assumption) / S (value) | g_bar | No |
| L38 | SPS assumptions, R13 (templates, metallicity, dust) | "we choose Bruzual & Charlot (2003; indexed BC) and Maraston (2005; indexed M) dust-free templates at solar metallicity"; "the photometric mass estimates depend on the adopted metallicity … A metallicity of half or less than solar would thus be required to reproduce, with either a Chabrier or Kroupa IMF, the photometric mass values derived from solar-metallicity models with a Salpeter IMF" | 0904.3282 plain.txt:914–916, 1060–1064, 1145–1147, §3 | not stated as a number | D(src) | g_bar | Maraston 2005 pair as `role=alternative`; no range |
| L39 | IMF, R13 | "assuming a Salpeter IMF, we find estimates of photometric mass that are more than one and a half times higher than those obtained by choosing either a Chabrier or Kroupa IMF" | 0904.3282 plain.txt:1038–1040, §3 | >1.5× | D(src) | g_bar (up) | Yes: `x_strong_lensing_mstar_top_msun` (R13 Salpeter-BC03), slider a6s_stellar_imf |
| L40 | SDSS photometry and calibration, R13 | "the lack of possible significant systematical errors caused by calibration or aperture corrections ensure accurate estimates"; Table 1 "extinction-corrected modelMag"; "a possible color gradient would only produce slightly higher photometric errors" | 0904.3282 plain.txt:777, 800–802, 1027–1030 | per-band errors printed (VizieR e_umag…) | S | g_bar | Inside R13's M* errors only |
| L41 | SPS systematic, S4TM (R9) | "Our lower-bound model is dust-free and metal-poor (log Z/Z⊙ = −0.30), while our upper-bound model is dusty and metal-rich (τ=0.95, log Z/Z⊙ = 0.20). The level of the resulting systematic variation in estimated stellar mass is around 0.5 dex." Reference model "t_form = 4 Gyrs, solar metallicity, and no dust" | 1407.2240 ms_v2.tex:424–425, §5 | ∼0.5 dex | D(src) | g_bar | No (`no_uncertainty`) |
| L42 | IMF top for S4TM | R30: "we can rescale these quantities by dividing them with a constant factor of 0.61"; R9 considers Salpeter but prints no Salpeter masses | 2502.06505 ms.tex:649; 1407.2240 l.404 | ×1/0.61 | D | g_bar (up) | `mstar_top_msun`, flag `salpeter_top_from_other_source_same_model_family` |
| L43 | S4TM R_eff (profile step) | Table 1 note: "the effective radius (in the intermediate axis convention) … assuming a de Vaucouleurs model" (no error); SLACS V same pipeline: "an RMS difference of 3.5%; we will adopt this value as our empirical error estimate" | 1711.00072 l.386; 0805.1931 l.1072–1076 | S4TM: not stated; SLACS V method: 3.5% | S | g_bar (via f(<R_E)) | No |
| L44 | SL2S M* statistical error and IMF pair | MRT t7 "e_logMChab Error on logMChab", "logMSalp … Salpeter IMF"; "The fit is based on an MCMC sampling." | 1307.4764 l.735; IOP t7 | ±0.07–0.09 dex (two plotted lenses) | S | g_bar | Yes: `g_bar_err_lo/hi`; Salpeter in `mstar_top_msun` |
| L45 | SL2S template systematic | "The relative scatter between stellar masses obtained from optical photometry alone and with the addition of NIR data is 0.06 dex … in Paper IV, this systematic uncertainty is added to the statistical uncertainty on M_*" | 1307.4764 sl2s-rm-pdflatex.tex:740, §5 | 0.06 dex (bias 0.01) | D(src) | g_bar | No |
| L46 | SL2S R_eff for the profile step (CFHT) | "The scatter on the quantity R_eff,CFHT − R_eff,HST is ∼30%; we take this as our uncertainty on CFHT effective radii." HST: "The dispersion is ∼10%" | 1307.4764 l.354–359; Table 4 comment l.378 | 30% (CFHT), 10% (HST) | S | g_bar (via f(<R_E)) | No (`r_eff` carried without error) |
| L47 | SL2S photometry and colour gradient | "Uncertainties on CFHT lens galaxy magnitudes … 0.3 in u band, 0.2 in g and r, 0.1 in all redder bands"; "this corresponds to an assumption of negligible intrinsic color gradient" | 1307.4764 l.341, 352 | 0.1–0.3 mag | S | g_bar | Inside M* error only |
| L48 | Luminosity calibration, SNL-0 (R28) | "We adopt a 2 per cent error on luminosity to account for absolute calibration uncertainties (the statistical errors are much smaller)." | 1306.4983 lensz_arXiv.tex:298 | 2% | D(src) | g_bar | Not used: v1 uses R26 L_r (L49) |
| L49 | L_r,Ein (R26) | "with 2–3% uncertainties estimated from photometric zero-point and Galactic extinction errors"; corrections "bandpass shifting … (0–0.06 mag)", "Galactic extinction (A_r=0.05–0.13 mag)", "point spread function (0–0.07 mag)"; Table 1 "M_r,⊙ = 4.64 AB; distance error not included" | 1612.00065 snells.tex:139, Table 1 l.106 | 2.84±0.06 ×10¹⁰ (2%) | S | g_bar | Yes: `g_bar_err` (quadrature with Υ) |
| L50 | Population M/L, Kroupa (R26 SNL-0; R61 SNL-1/2) | R26: "Since our spectra now constrain (M_*/L_r)_MW to 2–7%" (4.04±0.10); R61: "With the converted Υ_ref = 2.59" (SNL-2), "converted Υ_ref of 2.75 (Newman2017)" (SNL-1), no error | 1612.00065 l.243, Table 1 l.117; 1709.01931 l.315, 317 | 2.5% (SNL-0); not stated (SNL-1/2) | S | g_bar | SNL-0 yes (`g_bar_err`); SNL-1/2 `no_uncertainty` on Υ |
| L51 | SNELLS L_Ein J-band, SLC15 (superseded) | "The PSF corrections are ∼0.25 mag, and we estimate them to be accurate to 0.02 mag … systematic calibration errors of ∼0.02–0.03 mag"; "total estimated errors of 3–4 per cent"; "the absolute magnitude of the Sun M_J = 3.71" | 1503.02661 l.686–694 | 3–4% | S | g_bar | No (v1 uses R26/R61 luminosities) |
| L52 | Gas inside R_E | SL13: "We assume the gas mass projected within the Einstein radius is negligible"; SLC15: "Other possible non-stellar mass contributions within the Einstein radius, e.g. gas and central black holes, are neglected"; R32: "(and in principle from a central black hole, gas, etc but these are expected to be negligible)" | 1306.4983 l.496; 1503.02661 l.769; 1911.06338 l.274 | not stated | D | g_bar (up) | Registered term: `g_bar_gas_hot/cold`, `x_strong_lensing_gas_*_frac(_min/_max)` (hot 0.12% [0.015–2.5%], cold 0 [0–2%]), flag `gas_negligible_source_assumption` |
| L53 | J0403 luminosity corrections | "We adopt a correction of 0.24 mag, and allocate an error of 0.04 mag"; "k_i = 0.04 ± 0.01 mag"; PSF "0.22 ± 0.02 mag"; "2.59 ± 0.12 ×10¹⁰ L⊙. The uncertainty is dominated by the applied corrections"; solar "4.534" | 1803.07082 newlens.tex:198, 220–223 | 4.6% | S | g_bar | Yes: `g_bar_err` |
| L54 | J0403 Υ_Ref | "Υ*_Ref = 2.90 ± 0.10. The uncertainty is derived from small variations in the metallicity and age (e.g. z_form = 2.5–3.5, metallicity 1–1.5 solar)" | 1803.07082 newlens.tex:237 | 3.4% | S | g_bar | Yes: `g_bar_err` (quadrature) |
| L55 | J0403 model, age, IMF systematics | "If we had assumed … 8.5 Gyrs old (z_form = 1.5), α would have increased by 14 per cent. If we had adopted the Maraston2005 models, α would increase by 10 per cent." Salpeter "α = 1.55" | 1803.07082 l.208, 241 | 14%, 10% | D(src) | g_bar | IMF only (`mstar_top_msun` ×1.55); age and model no |
| L56 | MaNGA L_Ein and corrections | "galactic extinction corrections of ∼0.04 mag in i … a band-shifting correction of ∼0.09 mag … solar absolute magnitude of M⊙,i = 4.53"; PSF "corrections of ∼0.1 mag"; Table 2 L_Ein 6.72±0.10, 5.56±0.35 | 1911.06338 main.tex:270–272, Table 2 | 1.5%, 6% (printed) | S | g_bar | Yes: `g_bar_err` |
| L57 | MaNGA Υ_ref | "The full range in Υ_ref spanned by these models is 2.41–3.46; our calculations adopt this as the 2σ interval, i.e. we assume Υ_ref = 2.93±0.26"; "using Maraston models for Υ_ref would increase α by ∼12 per cent"; Salpeter "α ≈ 1.65" | 1911.06338 main.tex:276–277, 282, 293 | ±0.26 (9%); model 12% | D(src) (same Υ for both lenses) | g_bar | ±0.26 in `g_bar_err` (treated per system; correlated across the 2 lenses); top ×1.65, flag `salpeter_factor_approx_printed` |
| L58 | NGC 6505 stellar mass inside θ_E | "We then perform aperture photometry on the Galfit model within the Einstein radius, and fit the photometric SED with Prospector, finding M⋆Chab = (1.06 ± 0.02) × 10¹¹ M⊙" | 2502.06505 ms.tex:669, §3.2 | ±1.9% | S | g_bar | Yes: `g_bar_err` |
| L59 | Element abundance (α/Fe) in Υ_ref | SLC15: "a 0.3 dex increase in [α/Fe] yields a ∼4 per cent increase in J-band Υ_ref"; SL13: "2–3 per cent brighter in the I-band" | 1503.02661 l.858; 1306.4983 l.384–386 | ∼4%; 2–3% | D(src) | g_bar | No |
| L60 | Neighbour light in L (SNL-2) | "we estimate that this contribution is only 1.5%, a minor effect that we neglect" | 1612.00065 snells.tex:141 | 1.5% | S | g_bar (down) | No |
| L61 | Internal dust, SNL-1 | "uncovering evidence for a previously unknown dust disc within the fast rotating SNL-1" | 1709.01931 l.313 | not stated | S | g_bar | No |
| L62 | Projection: cylinder on both sides; aperture shape | R13: "the value of the projected mass enclosed within the tangential critical curve of an SIE model can be expressed as in an 'effective' axisymmetric model"; "within the disk defined by the Einstein radius" | 0904.3282 plain.txt:1646–1651, 1683 | not stated | D | both (same cylinder, D-064) | Labelled `r_kind = projected`; no term |

**Terms that move g_obs and g_bar together:** L13, L16, L19, L22, L28–L35 and L62. Doubts 1 and 2 add θ_E (L1–L4).

For the low-redshift lenses, **distance** is stated by three sources to enter the M/L ratio at first order (L31, L32, L34):
- SNL-0, SNL-1 and SNL-2 (z ≈ 0.03–0.05);
- J0403−0239 (z ≈ 0.066);
- NGC 6505 (z ≈ 0.042).

## Not stated (looked for, not found)

1. **Redshift errors.** Not printed for SLACS V (Table 1), S4TM (Table 1), SL2S IV (Table 2), R28 (Table 3), R61 (Table 1) or R32 (Table 2). Only R30 prints them (L29).
2. **Error on b_SIE, M_Ein or M*.** S4TM (R10) prints none, in Tables 1 and 2 or in the text.
3. **Error on f_ap.** None from R13: not in the text, not in Table 4, and the VizieR `fap` column has no error column. R13 does not say whether its M*(≤R_E) errors include an f_ap error.
4. **Confidence level of R5's 2%.** R5 says only "RMS fractional". The confidence level of R13's error columns is stated as "1 σ" in the figure captions only. VizieR labels them "Error … (upper limit)" and "(lower limit)".
5. **Size of the NGC 6505 lens-modelling systematic.** R30 §4.3 says it dominates but gives no number.
6. **Size of the foreground-subtraction systematic in S4TM** (L10).
7. **Gas literature.** Gas detection limits, the helium factor and the fraction inside R_E for the lens systems themselves: no lens source measures gas. I did **not** re-read the gas literature at source (N2, N7, N13, N14, N18, C4 and others); I read only `reading/gas/adjudication_gas.md` §3–5. Its stated caveats are Atlas-internal:
   - radii larger than R_E, with a bias toward overstatement (§4.3 item 5);
   - N7's masses are upper bounds by method;
   - C4 and N7 disagree by a factor of about 10–26 for the same galaxies.
8. **R61 Υ_ref conversion.** No error on the ezgal conversion from r to F814W for SNL-1 or SNL-2.
9. **The mass estimator.** No source quantifies an error in the projected estimator M_E = πΣ_cr θ_E² beyond L5–L9, L11 and L14. Wolf et al. 2010 does not apply (no σ is used).
10. **Solar absolute magnitude.** No source gives an uncertainty: 4.066 F814W (SL13), 4.64 r AB (R26), 3.71 J (SLC15), 4.534 i (R29), 4.53 i (R32).

## Doubts

1. **The sources disagree with the text of D-064 item 4.**
   - D-064 says the g_obs/g_bar ratio "does not depend on [cosmology] to first order, because both masses scale with the same distances".
   - Newman et al. state "The lensing M/L is proportional to distance" (L31).
   - SLC15, R29 and R32 each give a first-order shift of α with H0 (L34): 5%, 4% and 3.5%. α ∝ M*/L.
   - My inference, not a quote:
     - M_E ∝ D_l D_s/D_ls and R_E ∝ D_l, so g_obs = GM_E/R_E² ∝ 1/D;
     - M* from L × Υ, or from SED fitting, ∝ D_L², so g_bar ∝ D_L²/D_A², which is roughly independent of distance at low z;
     - so H0 and peculiar velocity move mainly g_obs, along with R_E.
   - I report this; I do not rule on it.
2. **The θ_E error is shared by both axes (inference).**
   - Where M_E is computed from θ_E (SLACS, and SL2S through R20's θ_E), M_E ∝ θ_E² and R_E ∝ θ_E. So g_obs = GM_E/R_E² does not depend on θ_E for an SIS-type normalisation.
   - At the same time, g_bar moves with R_E⁻² and with the aperture of M*. R13's masses are evaluated inside R5's θ_E.
   - v1 puts the whole θ_E error on g_obs at fixed R_E (`convert.py` l.48–49, l.677ff). Whether that matches the sources' intent is not stated by them.
3. **The θ_E error for the same SLACS lenses differs between sources:**
   - 2% (R5, adopted by v1);
   - "conservative 5%" (R13, L2);
   - 0.5% (R9, L3; this is the scatter between R9's re-fits and R5);
   - SL2S quotes "Bol++08a … about 2%" and adopts 3%.
4. **R9's 0.5% may not apply to R10.** R9's 0.5% was derived for its own MPFIT models. R10's S4TM models use `lfit_gui` (R10 §4), and no source says the 0.5% carries over.
5. **SL13 is internally inconsistent on one value.** M/L is 3.69±0.06 in the text (l.314) and 3.69±0.03 in Table 3 (l.613). Not used by v1.
6. **Aperture shape for SLACS.** R13's M* sits inside a circular "disk defined by the Einstein radius". The SIE mass sits within "elliptical critical curves" expressed as an "effective" axisymmetric radius (L62). No source quantifies the difference.
7. **R32's L_Ein errors look like magnitude errors only.** Inference: 0.02 mag gives ≈1.8%, matching 6.72±0.10; 0.07 mag gives ≈6%, matching 5.56±0.35. The extinction (∼0.04 mag), band-shift (∼0.09 mag) and PSF (∼0.1 mag) corrections carry no stated error.
8. **R32's two lenses share one Υ_ref = 2.93±0.26.** The error is fully correlated across them, while v1 propagates it per system. R32 also says the ±0.26 is half the 2σ model range, so it is a model range, not a measurement error.
9. **Redshift frames differ by source.**
   - R28's z_l is "CMB frame".
   - R29 computes geometry with z_CMB but also prints z_H.
   - R30's default z = 0.04243 is spectroscopic, and its cosmological z is 0.041±0.001.
   - SL13 uses "no peculiar velocity".
   - v1 adds no distance error for any of these (REPRODUCTION.md "Distance errors are not added (the redshifts are spectroscopic)"). The sources (L30–L32) state a distance uncertainty separate from redshift precision.
10. **R61's luminosity.** The SNL-1 value I read is L_F814W(≤R_ap) = 2.52±0.04 ×10¹⁰ (Table 1, l.155). It is not in `adjudicated_inputs.csv` under R61. I assume it is in `adjudicated_supplement.csv`, which I did not open; the g_bar error on the SNL-1 row (1.6%) is consistent with ±0.04/2.52.
11. **The black hole mass is not clearly either side (L27).** It sits inside M_E, and the sources discuss it only as a correction to the stellar mass. Whether it counts as "detected baryons" is not a source statement. I record it without classifying it.
12. **The SL2S 0.06 dex systematic is not in the Table 7 errors (L45).** It is "added in Paper IV". I did not check whether SL2S IV prints combined errors, because v1 uses Table 7.
13. **Reading method.** R13 was read from pdftotext output; the two-column layout can mis-order lines, so locations are plain.txt line numbers plus section numbers. Every quote was checked in the extracted text.
14. **Scale for SLACS's 2%.** R5 derives it as a per-measurement RMS, a point/system error, but gives it once for the whole sample. I classed it S, with its size set at dataset level.