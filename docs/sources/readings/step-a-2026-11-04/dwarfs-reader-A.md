# Dwarf galaxies, Reader A (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Reader A: Atlas step A, uncertainty terms for dwarf galaxies (`aeg-d-dwarfs` v1)

**Reader:** Reader A
**Dataset:** Dwarf galaxies, `aeg-d-dwarfs/v1` (64 plotted systems, 1 recorded, 65 rows in `reading/conversion_inputs.csv`)
**Date:** 2026-11-04
**Brief:** `git show 32cbc9b:docs/sources/readings/step-a-2026-11-04/brief.md`. The working tree was on branch `reading/step-a-dwarfs-gc-lenses`, HEAD `8d9c11d`.
**Work directory:** `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/step-a-2026-11-04/dwarfs-A/`. Each e-print was downloaded into its own `dl/<name>/` and extracted to `dl/<name>/x/`. Only `grep`, `sed` and `awk` were run on the downloads; nothing from them was executed.

## Sources read

### Package files (read-only)

| File | SHA-256 |
|---|---|
| `data/packages/aeg-d-dwarfs/v1/REPRODUCTION.md` | 43c9420e886ac85634ceaf4408cab7710ffee8391a3afbd30375cbb855973b72 |
| `convert.py` | cde9d77de5539018d0bfd3d2fc09134eccfcf2fcf5cac984524ee8c4fca23634 |
| `descriptor.json` | f042aa163aee782b6787be5e3009559c1762d69d874c5ab9ad47d55e4744f79d |
| `datapackage.json` | f42ac376c4d3cdc93cf46798bbb726ea090f8cb8c517bf65cf84a7be184b1893 |
| `sources.json` | 0f1d8e0ddd0377e982c31154918292b84eb5cad227f5a40b319677d28d5a1b0b |
| `reading/conversion_inputs.csv` | cf86e1d3313c1117ec8784b8f321782eabdfedbc993fced326addcb2027134bd |
| `docs/decisions.md` | 8eae6352d4105e3db852d2668ed56a20291866b17f36b525e27c80e0c025651d |
| `data/assumptions.json` | ed3a40c8d9f65c2d3ab081134806307705642ceb728b08d981bcbb385f56fcf9 |

Also read:
- `reproduction/inputs.py`, `inputs_v2.py` and `inputs_magerr.py`, for how the magnitude errors are built.
- From `docs/decisions.md`: D-025, D-034, D-035, D-038, D-039 and D-048 to D-062.
- `docs/sources/stellar-ml-2026-10-29.md`.
- Table column names and units, with values only where needed to tell what an error column holds.

### Local copy

- Putman et al. 2021, Table 1 (machine-readable table, header and notes, plus the rows for flagged systems): `source/gas/putman2021/apjabe391t1_mrt.txt`, SHA-256 444c6337bde863049b1e1d28d2cf26667c18b0b783bfa667b1e9f542f102637f.

### arXiv e-prints (SHA-256 of the downloaded e-print)

| Source | arXiv id, version | Main .tex | SHA-256 |
|---|---|---|---|
| Pace 2025, LVDB (database-level) | 2411.07424, latest (v2) | main.tex | 1b864a9533590fe0976778a22e27acb682f6a21db912813cd5dbeb743fb5915f |
| Wolf et al. 2010 (estimator) | 0908.2995, latest (v6) | ms-mn2e.tex | 6852fe7e0248278947158c37c30132610c1c4ac4c347448f232e65d78b1bbd94 |
| McLaughlin & van der Marel 2005 (Υ_V) | astro-ph/0605132, v1 | mclaughlin_vandermarel.tex | af94cbcf14303090df2ab51ddd864235731d3378d9ba309638da8edf4a431b96 |
| Woo, Courteau & Dekel 2008 (Υ_V range) | 0807.1331v2 | lgmn.tex | 7331f6cfb4154b72984c1b0a53873d8de265c67eab2356bf0dc595762da50fcb |
| Putman et al. 2021 (gas) | 2101.07809v1 | main.tex | 6382f5293ed3849d9e6db0c885bd6d31821891892920d59998bbd4a858d43fc9 |
| Lelli et al. 2016 (helium factor) | 1606.09251, v1 | SPARC.tex | 792903260765acbb0d2ed5df47bc8f99f97e24da0911527393db7243888bc7fc |
| σ: Geha et al. 2026 (20 rows) | 2602.10200v2 | main.tex | 60461d02dad7af3a17e6b8acc5a84187ef12f076be9cbe9485013906e98c1437 |
| σ: Collins et al. 2013 (12 rows) | 1302.6590v1 | M31dsphsv3.tex | bafcfadd98707763034bda8a9e710143bda8e2193cd0378e6ab6762856e7d098 |
| σ: Tollerud et al. 2012 (9 rows) | 1112.1067v3 | splashdwarfs1.tex | 082ab431593daf756a635cb17063c3fd1b144f9f60920e49e5da94afef6fdc9e |
| σ: Fritz et al. 2019 (2 rows) | 1805.07350v4 | spec_v1_ref1_arx.tex | 41cad1cdfcbbff0901afbbe9e8b3212c1c861d52e53ea2c6e35887b311e5dc90 |
| σ and structure: Ji et al. 2021 (Antlia 2) | 2106.12656v2 | main-arxiv.tex | 843ea841c80c8e969fbbf94197d033356ba6f27054ccddebeca27c25c1695e2d |
| σ: Heiger et al. 2024 (Eridanus IV) | 2308.08602v1 | heiger_imacs_spectroscopy_of_eri4_and_cen1.tex | 866249d2c1f548a791d9450ab16824f7a9ce374eda0e399591a6b3640102fa7b |
| σ: Kvasova et al. 2024 (And XVIII), binary and error statements only | 2404.11804v4 | andromeda18.tex | 04369e37ab096f5300a0cc199f7439577ec03b1c1be65b98fee57a272fcd2cd5 |
| Structure and m_V,0: Martin et al. 2016 (19 to 20 rows) | 1610.01158v1 | ms.tex | 7585942eef8853bd4c4f5dfae9d3d5a675933c0eefe36ec29f6ae57d35b15b2e |
| Structure and M_V: Muñoz et al. 2018 (19 to 20 rows) | 1806.06891v1 | ms.tex | 36252e479d0ad3ebd05a5c52f22e342fbfaec8e981f972f7234b01b563d6c834 |
| Structure and distance: Higgs et al. 2021 | 2101.03189v1 | mnras_template.tex | 0dea93b88b1eb5459f5e27e5824b355581fca8708cf2385c62ddb58e3971b3dc |
| Structure and distance: Carlin et al. 2017 | 1710.06444v1 | coli_triii_arxiv.tex | d7732055ed36749257de531a59a4d54762bd11484bd203379e877ab0171f76d9 |
| Structure: Moskowitz et al. 2020 (Boötes III) | 1910.10134v3 | draft.tex | b2af6e4757e9731aec48250f1e0ef0ed2809bfe0ec9efb1c8af1db0ae950ad2b |
| Distance: Savino et al. 2022 (21 rows) | 2206.02801v2 | main.tex | edd8826b1d6ef9ae7f3dd4a56a47c89f06f6d1fe6aaf79f44e4ea9d0b64bcce1 |
| Distance: Medina et al. 2018 (Leo IV, Leo V) | 1802.01581v1 | ms.tex | 3108c7bf5eafaea1b60eda8a3100b1bd35dd5234b914ce7e25d1de640e23e49b |
| Distance: Vivas et al. 2022 (Antlia 2) | 2112.08467v1 | main_arXiv.tex | 4f0bdf3d82601286e963315d2e22f9b3176d9f4c3baee2aba6be6c7d163b3e18 |
| Distance and M_V: Simon et al. 2020 (Tucana V), binarity and limit statements only | 1911.08493v2 | ms.tex | d0e56936b775b4ba836b174c441924a45917564755feacafb8eff7bc5605eef7 |

Sample size per input type: σ, 7 papers (≥5 required). Structure, 6 (Martin, Muñoz, Higgs, Carlin, Moskowitz, Ji). Distance, 5 (Savino, Medina, Vivas, Carlin, Higgs). Magnitude, 5 (Martin, Muñoz, Simon, Carlin, Ji); Carlin, Ji and Simon were read only for the passages cited.

Line numbers below refer to the extracted `.tex` files. All quotes are from arXiv versions, not versions of record.

## Terms

Scale codes: P = point, S = system, DS = dataset. With one value per system, P and S coincide for every term marked "P=S". In the v1 column, "meas" means `tables/measurements.ecsv` and "obs" means `tables/observables.ecsv`.

### Velocity dispersion σ (moves g_obs ∝ σ²)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| D1 | σ measurement error (posterior interval) | "If resolved, we quote the 1-sigma errors of the posterior distributions." | Geha 2026, §8.2 (ssec:results), l.741 | per system, Table A1 cols 15–16 | P=S | g_obs | yes: meas `x_dwarfs_sigma_err_lo/hi`, `g_obs_err_lo/hi`; obs sigma_los `err_lo/err_hi` |
| D2 | σ error convention, different source | "We adopt as the error on σ and μ the square root of the diagonal elements of this matrix." (Hessian) | Tollerud 2012, §3.3, l.352 | per system | P=S | g_obs | as D1. The convention itself is not recorded. |
| D3 | σ error convention, different source | "dashed lines represent canonical 1, 2 and 3σ confidence intervals, derived assuming Gaussian uncertainties" | Collins 2013, Fig. And XVII caption, l.1044–1045 | per system | P=S | g_obs | as D1 |
| D4 | Upper-limit confidence level varies by source | Geha: "an upper limit … as the 95th percentile of the posterior" (l.741). Fritz: "upper limits (defined as the values at the 90-th percentile …)" (l.388). Collins, And XVIII: "upper bound is determined from the formal 1σ confidence interval" (l.1063). | as cited | 95%, 90%, 1σ; package also has "90%" (Kirby) and the D-062 1σ upper error (And XII) | P=S (level DS per source) | g_obs (as a limit) | yes: meas `limit`, `x_dwarfs_sigma_limit_level`; flag `limit_from_1sigma_upper_error` |
| D5 | Per-star velocity error model: scale factor and floor | "we infer k_v = 1.4 and σ_v,floor = 1.1 km s⁻¹"; "Underestimating (overestimating) velocity errors … translates directly into larger (smaller) values of the internal velocity dispersions" | Geha 2026, §4.1, l.420, l.402 | k_v 1.4; floor 1.1 km/s | DS (Geha rows) | g_obs (direction stated) | no (inside the printed σ error only) |
| D6 | Velocity systematic floor | "an additional systematic error component of 2.2 km s⁻¹" | Tollerud 2012, §3.1, l.268 | 2.2 km/s | DS (Tollerud rows) | g_obs | no (inside the printed σ error) |
| D7 | Velocity systematic floor | "a systematic error of 1 km s⁻¹ are added in quadrature" | Heiger 2024, §2.x Radial velocity, l.109 | 1 km/s | DS (Heiger rows) | g_obs | no |
| D8 | Velocity systematic floor | "δv_i = √(δv_i,obs² + (1.49 km s⁻¹)²)" | Kvasova 2024, l.260 | 1.49 km/s | DS | g_obs | no |
| D9 | Mask, slit and telluric velocity offsets | "This can translate to velocity uncertainties of up to ∼15 km s⁻¹"; "average measured offset across all our masks is 3.8 km s⁻¹ … average end-to-end mask difference of 2.6 km s⁻¹" | Collins 2013, §2.2.1, l.508, l.571–573 | up to ~15 km/s per star; 3.8 and 2.6 km/s mask averages | P (per mask) | g_obs | no |
| D10 | Unresolved binaries inflate σ | "Systems with the smallest intrinsic velocity dispersion (σ_los ≲ 5 km s⁻¹), with small … sample sizes (N ≲ 10–20), and/or without multi-epoch … data can have incorrect inferred velocity dispersions" | Pace 2025, §3.5, l.518–519 | not stated | S | g_obs (up; "inflated dynamical masses") | no per-system column (obs `steps` names `binary_treatment` generically) |
| D11 | Binaries, size | "medium-to-high binary fractions can inflate velocity dispersions by up to ∼20% in the smallest dSphs" (citing Minor 2010) | Wolf 2010, §5 Conclusions, l.1212–1214 | up to ~20% in σ | S | g_obs (up) | no |
| D12 | Binary treatment differs by source | Geha removes variables ("flag_var"; "log₁₀p < −1"; l.444, l.694). Kvasova: "binary stars can inflate … we ignored them because we do not have multi-epoch spectroscopy" (l.246). Ji: "We expect the true binary fraction to be closer to 50% … unlikely to affect Ant2" (l.359). Fritz: "undetected binaries usually cannot inflate … to the values measured for Phx II" (l.415). Collins 2013 and Tollerud 2012 (Tollerud only re Gaussianity, l.339) do not describe a binary removal. | as cited | not stated | S | g_obs | no |
| D13 | Membership and contamination | "inclusion of a few outlier stars … may artificially inflate the velocity dispersion … filtering outliers that are true members … will … decrease"; footnote: "can bias the velocity dispersion at the few-percent level" | Tollerud 2012, §3.2, l.323–325 | "few-percent" | S | g_obs (either sign) | no |
| D14 | Systematic membership error | "any systematic errors in the velocity dispersion resulting from our method of assigning membership … could manifest as systematic shifts in M_1/2 for M31 dSphs relative to those of the MW" | Tollerud 2012, §5.1, l.945 | not stated | DS (Tollerud rows) | g_obs | no |
| D15 | Membership subjectivity | "note this estimate includes subjective choices which may not be appropriate on a case-by-case basis" | Geha 2026, §7.3, l.694 | not stated | S | g_obs | no |
| D16 | Aperture of σ | "using member stars (P_mem_novar = 1) within two half-light radii"; Table A1 note: r_eff "taken from [Pace 2024]" | Geha 2026, l.743; Table A1 notes, l.950 | 2 r_eff (r_eff = LVDB v1.0.6) | S | g_obs | partly: D-051 coverage is in `reading/`; no column in the tables |
| D17 | Small member counts | "(*) – indicates velocity dispersions derived from fewer than 8 members stars, and require confirmation" | Collins 2013, Table 4 note, l.1648 | not stated | S | g_obs | no |
| D18 | Rotation or velocity gradient | Ji: "σ_v, no k_v … Radial velocity dispersion without linear gradient" (Table, l.298); the abstract "detects a clear velocity gradient in Antlia 2" (l.99) | Ji 2021, §4, l.298; abstract | Ant2 k_v 5.72 (+0.60/−0.56) km/s/deg | S | g_obs | no (the D-038 addendum value is used; the gradient is not stored) |
| D19 | Disequilibrium or tides (named systems) | Collins, And XXVII: "unlikely to be in virial equilibrium, if it remains bound at all" (l.1426); "may no longer be a gravitationally bound system" (l.1438). Martin 2016: "cannot derive parameters for And XXVII as it is likely not a bound stellar system" (abstract, l.217). Ji 2021: "support a tidal disruption scenario" (l.104). Putman note 8 (Boötes III): "tidally extended galaxy". | as cited | not stated | S | g_obs (and the estimator's validity) | no (all of And XXVII, Antlia 2 and Boötes III are plotted; assumption `dw_equilibrium` is named in `assumptions`) |

### The estimator (Wolf et al. 2010)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| D20 | Estimator normalisation | "The dashed lines indicate ±10% variation about the predicted relation" (classical dSphs); "good enough to warrant the need for 10% accuracy" | Wolf 2010, §3.3 Tests, l.927, l.996 | ±10% | DS | g_obs | named only: `dw_equilibrium`; no size |
| D21 | r½ against r₋₃, anisotropy | "the slight (∼15%) difference between r½ and r₋₃ will not matter"; "the errors on M_half increased by roughly 0.05 dex when the (rather extreme) second β(r) form was used" | Wolf 2010, §3.2.x, l.889; §3.3, l.990–992 | ~15% (radius); ~0.05 dex | DS | g_obs | no |
| D22 | Flat-profile requirement | "Equation … can be understood under the assumption that the observed stellar velocity dispersion profile is relatively flat near R_half … Equation will no longer be as accurate" | Wolf 2010, §1, l.155–160 | not stated | S | g_obs | no |
| D23 | Flat profile, source checks | Collins: "if … not flat, but declined or increased with radius, this would no longer [be] true … low-number statistics means we are unable to completely rule out this possibility". Tollerud: "satisfy that requirement within the error bars (aside from possibly And I and And III)". | Collins 2013, §5.1, ~l.1605; Tollerud 2012, §5.1, l.943 | not stated | S | g_obs | no |
| D24 | Sphericity and equilibrium | "The two main assumptions … are that the systems … are spherically symmetric and are in dynamical equilibrium. Testing the accuracy … as a function of ellipticity will be an important future step." | Wolf 2010, §5, l.1185–1187 | not stated | DS | g_obs | named: `dw_equilibrium` (no size) |
| D25 | Light-weighted σ² against member-sample σ | "the brackets indicate a luminosity-weighted average"; Collins: "we assume our measured values of σ_v are representative of the luminosity-averaged velocity dispersion" | Wolf 2010, l.139; Collins 2013, §5.1, ~l.1600 | not stated | S | g_obs | no (see Doubt 6) |
| D26 | Non-Gaussian velocity distributions | "a small amount of excess kurtosis is measured in the outer parts of some systems" | Wolf 2010, §2.3, l.393 | not stated | S | g_obs | no |

### Half-light radius (moves both: g_obs ∝ 1/r½, g_bar ∝ 1/r½²)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| D27 | Deprojection factor 4/3 | "R_half ≃ (3/4) r_half … accurate to better than 2% for exponential, Gaussian, King, Plummer, and Sérsic profiles"; App. table r_half/R_half: Exponential 1.329, Plummer 1.305, Sérsic n=8 1.352 | Wolf 2010, §1, l.150–152; Appendix, l.1793–1800 | <2%; 1.305–1.352 | DS (per profile) | both (opposite powers) | named: `dw_rhalf_wolf`; fixed 4/3, no range |
| D28 | Other sources' deprojection factor | "r_1/2 = 1.315 R_eff" | Tollerud 2012, §5.1, l.943 | 1.315 | DS | both | no |
| D29 | Statistical error on r_h | "uncertainties are bound by the values of the parameters for which the probability is 61 percent of the peak value"; Muñoz: "10 000 bootstrap realizations … 1-σ uncertainty" | Martin 2016, §2.1, l.323; Muñoz 2018, §3.1, l.369–374 | per system (e.g. And I r_h = 3.9 ± 0.1′) | P=S | both | **no** (obs half_light_radius `err_lo/hi` empty in 64 of 64 rows) |
| D30 | Ellipticity error and circularisation | Pace: "R_1/2 = R_h √(1−ε) … to approximate spherical symmetry as most dwarf galaxies are non-spherical"; Martin And I "ε = 0.28 ± 0.03" | Pace 2025, §4.4, l.460; Martin 2016, §4.1, l.480 | per system | P=S | both | **no** (obs structural_param `err_lo/hi` empty in 64 of 64) |
| D31 | Ellipticity and position angle vary with radius | "Some galaxies show changes in the position angle and/or ellipticity with radius and the current LVDB format does not account for this"; Muñoz (Sculptor): "ellipticity was found to range between 0.23 and 0.49, depending on the adopted stellar subsample" | Pace 2025, §5, l.699; Muñoz 2018, §4.x, l.770–771 | 0.23–0.49 (Sculptor example) | S | both | no |
| D32 | Choice of profile fit | "neither of the three types of profiles actually accounts for the complexity"; Moskowitz: "systematic errors that we observe when the input model violates the assumptions of the model adopted in the fit" | Martin 2016, §2.1, l.340; Moskowitz 2020, §3.1, l.165 | not stated (Muñoz tabulates exponential, Plummer, King and Sérsic r_h side by side, Tables 4–6) | S | both | flagged only via obs `x_dwarfs_parameter` convention; no alternative-fit column |
| D33 | Unstated semi-major or circularised convention | D-052 item 2 named assumption; Muñoz 2018: no convention statement found | D-052; Muñoz 2018 (searched "semi-major", "circular", "geometric") | not stated | S | both | flag `rh_semimajor_assumed` (20 systems); computed alternative not found in the tables |
| D34 | Half-density against half-light | "What we really determine here is the half-density radius … under the assumption that a system harbors uniform stellar populations and does not suffer from mass segregation, this quantity is equivalent to the more common half-light radius" | Martin 2016, §2.1 fn., l.280 | not stated | S | both | no |
| D35 | Near against far structural systematics | "there may be some systematics in the structural parameters between near (resolved stars) and far (integrated light) dwarf galaxies"; Higgs: crowding near centres; "the outskirts of several dwarfs are not ideally characterized by the Sersic fit" | Pace 2025, §4.4, l.472; Higgs 2021, l.304, l.587 | not stated | DS / S | both | no |

### Distance (see Doubt 1 for the net effect on each axis)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| D36 | Distance statistical error (RR Lyrae, M31 satellites) | "uniformly measure heliocentric distances to a precision of ∼20 kpc (3%)"; the dominant random term is "the unknown metallicity of the RR Lyrae, which limits precision to roughly 0.05 magnitudes" | Savino 2022, abstract l.384; §3.3, l.922 | ~3%; ~0.05 mag | P=S | both (see Doubt 1) | partly: obs distance `err_lo/err_hi` (62 of 64 rows); not propagated to `g_obs_err` or `g_bar_err` |
| D37 | Distance systematic (shared scale) | "we quantified our typical systematic uncertainties to be ∼3.5%"; "maximum systematic variation of 3.4% … ∼26 kpc (0.07 mag)"; "Retaining the M15 original distance scale systematically increases the measured distance by a median of 0.073 mag" | Savino 2022, §6 Conclusions l.1244; §4.6 l.1117; §4.2 l.988 | ~3.5% (0.07 mag) | **DS** (21 Savino systems move together) | both | no |
| D38 | RR Lyrae metallicity prior | "median absolute change in distance modulus … is 0.06 mag or ∼3%"; "systematic differences are generally contained within 0.1 mag" | Savino 2022, §4.4, l.1003–1006; §4.6, l.1117 | 0.06 mag median; ≤0.1 mag | S / DS | both | no |
| D39 | RR Lyrae metallicity (MW) | "a mean metallicity offset of ±0.5 dex … would lead to fractional difference in heliocentric distances of 1.8% … ±1.0 dex … ∼3.6%" | Medina 2018, §3.2, l.264 | 1.8%; 3.6% | S | both | no |
| D40 | Line-of-sight depth or gradient (Antlia 2) | "mean distance … 124.1 kpc, with a standard deviation of 5.4 kpc"; "a difference in distance of ∼13 kpc" across the galaxy | Vivas 2022, §3.3, l.264, l.266 | dispersion 5.4 kpc; gradient ~13 kpc | S | both | **no**: Antlia 2 distance err blank in `conversion_inputs.csv` |
| D41 | Calibration anchor (BHB ridge line) | "(assuming a distance modulus of m−M = 15.39 to NGC 7078, here and throughout this work)" | Carlin 2017, §3, l.114 | anchor not given an error | DS (Carlin rows) | both | no |
| D42 | TRGB calibration | "absolute magnitude of i_o = −3.49 … derived from the Darthmouth isochrones" | Higgs 2021, §3.2, l.361 | not stated | DS (Higgs rows) | both | no |
| D43 | Inherited host distances | "systems without an independent distance measurement … inherit the distance and errors of their host galaxy … This is not denoted in the combined catalogs." | Pace 2025, §5, l.704 | not stated | S | both | REPRODUCTION.md names flag `distance_inherited`; it does not appear in v1 flag counts (Doubt 9) |
| D44 | Leo I modulus depends on metallicity | D-061 item 4 (Stetson 2014 range 22.06 ± 0.08 to 22.25 ± 0.07); Stetson not read by me | D-061 | −0.175/+0.165 mag | S | both | yes: obs distance errors; flag `distance_range_midpoint` |

### Luminosity L_V (moves g_bar only)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| D45 | Photometric or shot-noise error on M_V | "we randomly draw a number N* of stars from the luminosity function … 10 000 times … to estimate 1-σ errors" | Muñoz 2018, §3.2, l.432–437 | per system | P=S | g_bar | yes: obs apparent_magnitude `err_lo/hi`; meas `g_bar_err_lo/hi` |
| D46 | Completeness-model error on m_V,0 | "These typically yield uncertainties of ±0.2 and we therefore add a Gaussian random deviate of width 0.2 to the values of m_V,0" | Martin 2016, §2.2.2, l.381 | ±0.2 mag | P=S | g_bar | inside the printed error, so yes via D45 columns |
| D47 | Assumed stellar-population age (luminosity function) | "assuming that And I is instead entirely composed of an 8-Gyr stellar population does lead to magnitudes that are systematically brighter by ∼0.2 magnitudes"; "overall, 0.29 ± 0.11 magnitudes fainter" than the literature | Martin 2016, §2.2.2, l.385 | ~0.2 mag; 0.29 ± 0.11 mag | DS (Martin rows) | g_bar (fainter means lower) | no |
| D48 | IMF in the luminosity-function correction | Muñoz: "assuming a Salpeter initial mass function". Martin: "assuming the default Chabrier IMF". | Muñoz 2018, §3.2, l.416; Martin 2016, l.377 | not stated | DS per source | g_bar | no |
| D49 | Transformation to V | "V = g − 0.569 × (g − r) − 0.021 derived by [Jordi 2006]"; Martin: "convert to the V band with the color equations … of [Ibata 2007]" | Muñoz 2018, §3.2, l.468; Martin 2016, l.379 | not stated | DS per source | g_bar | no |
| D50 | Extinction | Martin: "extinction measured from [Schlegel 1998] as recalibrated by [Schlafly 2011]". Higgs: "No corrections are applied for extinction internal to the dwarfs." Pace: "The extinction correction is adopted from the literature source." Muñoz: no extinction statement found. | Martin 2016, l.377; Higgs 2021, l.221–222; Pace 2025, App. A, l.800 | not stated | P=S | g_bar (more extinction means brighter) | no (inside printed errors at most) |
| D51 | M_V errors exclude distance | "the distance errors are commonly not included when computing the absolute magnitude and I follow that convention here" | Pace 2025, App. B, l.935 | not stated | S | g_bar | n/a: package rebuilds m_V,0 (Doubt 3) |
| D52 | Solar absolute magnitude | "a solar absolute magnitude M_V,⊙ = +4.85 [e.g. lan99]" | McLaughlin & vdM 2005, §4.2.2, l.2161 | 4.85, no error | DS | g_bar | stated in meas `x_dwarfs_l_v` description; no error |
| D53 | Magnitude rebuilt from the paper's modulus; modulus error folded in | Package: `m_lo = hypot(M_V err, mod_err)` (`inputs_v2.py` l.207–208); D-052 item 4, D-061 | package | per system | S | g_bar | yes: within `g_bar_err` for And VI, And VII, Phoenix, Leo T and Tucana I |

### Stellar mass-to-light ratio Υ_V (moves g_bar only, ∝ Υ_V)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| D54 | Age and [Fe/H] error on model Υ_V | "All uncertainties on the population-synthesis quantities … follow directly from uncertainties in the cluster ages and [Fe/H] values"; "assigned a single age of 13 ± 2 Gyr" | McLaughlin & vdM 2005, §3.2, l.1491, l.1513–1516 | 13 ± 2 Gyr; per-cluster e_(M/L) | DS (model) / S (via [Fe/H]) | g_bar | yes: inside meas `x_dwarfs_upsilon_v_low/high` (D-060) |
| D55 | Population-synthesis code | "these differences are generally slight: at the level of ≲0.05 mag in (B−V)₀ and ≲10% in Υ_V" | McLaughlin & vdM 2005, §3.1, l.1358–1359 | ≲10% | DS | g_bar | yes: factors 0.90 / 1.10 in `x_dwarfs_upsilon_v_low/high` |
| D56 | IMF | "The Salpeter IMF gives Υ_V consistently higher than the Chabrier disk IMF (by factors of ∼60%–75%)" | McLaughlin & vdM 2005, §3.1, l.1424–1425 | +60–75% | DS | g_bar (up) | yes: `x_dwarfs_upsilon_v_high` ((M/L)₂ column) |
| D57 | Star-formation-history against colour Υ_V | Woo Table 2, V band, dE: SFH 1.6, BdJ 1.3 (`\MLBCvs`, `\MLBJvs`, l.145, l.148); "uncertainties in the SFH, and the uncertainties in extrapolating BdJ's colour–M*/L correlation" | Woo 2008, §2.1.2–2.1.3, l.680, l.753–756 | ratio 1.3/1.6 = 0.81 | DS | g_bar | yes: factor 0.81 in `x_dwarfs_upsilon_v_low`; Woo values as obs `star_formation_history_ml` (15) |
| D58 | Stellar mass typical uncertainty | "The typical uncertainty: 0.17 dex." | Woo 2008, Table 1 note c, l.512 | 0.17 dex | S | g_bar | no (not used as such) |
| D59 | Metallicity input to Υ_V | [Fe/H] errors and spread (D-060 item 2) | `reading/feh_values.csv`; D-060 | per system | S | g_bar | yes: obs metallicity_feh `err_lo/hi` (62 rows); enters the D-060 range |
| D60 | Below the tabulated metallicity range | REPRODUCTION.md: "the lowest value is used and flagged beyond_source_range; there is no extrapolation" | REPRODUCTION.md, Inputs table | not stated | S | g_bar | flag `beyond_source_range` (39 measurements) |
| D61 | Dwarf IMF evidence | Not read by me at source; the project note records Filion et al. 2024 as consistent with Chabrier/Kroupa | `docs/sources/stellar-ml-2026-10-29.md` | not stated | DS | g_bar | covered by the D-060 range |

### Gas (moves g_bar only; 2 of 64 systems carry gas mass)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| D62 | HI upper limit (5σ) | "5σ HI mass limits … calculated using a velocity width of 10 km s⁻¹ and the distance to the dwarf galaxy: M_HI = 2.36 × 10⁵ 5σ(Jy) 10 km s⁻¹ D²(Mpc)" | Putman 2021, §2, l.176 | 5σ | P=S | g_bar (limit; package sets gas = 0) | yes: obs `mass_gas_limit` (limit = upper), meas `x_dwarfs_gas_status`; gas set to 0 in `g_bar` |
| D63 | Assumed line width for limits | "We debated whether to use the stellar dispersion values … but given the variations on availability and errors we chose the fixed value" | Putman 2021, §2, l.176 | 10 km/s fixed | DS | g_bar (limit level) | no |
| D64 | Assumed central concentration | "it does assume the HI is more centrally concentrated (Coma Berenices, Andromeda XIX and Andromeda II)" | Putman 2021, §2, l.166 | not stated | S | g_bar (limit) | no |
| D65 | HI mass error from distance | "Errors on the mass limits are given based on the distance errors." Table note 4: "The errors are from the distance errors shown." | Putman 2021, §2, l.176; MRT Note (4) | per system (e_MHI) | S | g_bar | **no** (obs mass_hi and mass_gas_limit have no errors) |
| D66 | Confusion and limit caveats per system | Note 8: "limit is only for the core of this tidally extended galaxy" (Sagittarius, Boötes III). Note 11: "twice the median flux … due to strong Galactic contamination" (Willman 1). Note 14: Sculptor "claimed as a detection … HI clouds are offset". Note 19: Fornax "velocities that confuse any associated HI with Galactic emission". Note 22: Phoenix "confusion with Galactic emission". | Putman 2021, MRT Note (1) | not stated | S | g_bar | no |
| D67 | Helium factor | "We assume a thin disk with a total mass of 1.33 M_HI, where the factor 1.33 considers the contribution of helium." | Lelli 2016, §3.3, l.199 | 1.33; range not stated | DS | g_bar | named: `helium_factor` (not adjustable) |
| D68 | Fraction of gas inside r½ | REPRODUCTION.md: "otherwise half the total, flagged"; Putman gives totals only | REPRODUCTION.md; D-058 | not stated by source | S | g_bar | named `dw_gas_half_total`; flag `gas_half_total` (Leo T, Phoenix) |
| D69 | Molecular and ionised gas | descriptor: "No per-system source read for v1" | `descriptor.json` `x_baryon_inventory` | not stated | DS | g_bar (would raise it) | status `not_addressed` |

### Database-level (Pace 2025)

| ID | Term | Verbatim quote | Location | Size as stated | Scale | Moves | In v1? |
|---|---|---|---|---|---|---|---|
| D70 | Heterogeneity of methods | "Due to this inhomogeneity, there will be systematics in the LVDB" | Pace 2025, §5, l.694 | not stated | DS | both | no |
| D71 | Subjective choice among measurements | "the decision of which measurement to include is subjective" | Pace 2025, App. A, l.916 | not stated | S | both | n/a (package uses its own rules) |
| D72 | Different limit levels | "even with this reanalysis some limits are quoted at different values" (HI limits "vary from 2–5σ") | Pace 2025, App. A, l.906 | 2–5σ (HI) | S | g_obs, g_bar | via D4, D62 |

## Terms that move g_obs and g_bar together

- **Distance (D36–D44).** It enters r½ ∝ D on both axes and L_V ∝ D² on the baryonic side (M_HI ∝ D² after the D-058 rescale). The net effect is my arithmetic, not a source statement; see Doubt 1.
- **R_h, ε, the circularisation, the 4/3 factor, the profile choice and the half-density assumption (D27–D35).** These enter as g_obs ∝ 1/r½ and g_bar ∝ 1/r½². They are correlated across the two axes with different powers. v1 carries no R_h or ε error.

## Not stated (looked for and not found)

- **Size of the binary inflation per system** in Collins 2013 and Tollerud 2012. In Collins I found no binary statement at all; Tollerud mentions binaries only in relation to Gaussianity (l.339).
- **Extinction source or value in Muñoz 2018** (searched "extinction", "redden", "dered", "Schlegel", "Schlafly"). Found only differential reddening for Palomar 2 (l.919–920).
- **Semi-major or circularised r_h convention in Muñoz 2018** (searched "semi-major", "circular", "geometric").
- **An error on Muñoz 2018 Table 1 heliocentric distances** (Table 1 header, l.2194–2210).
- **Errors on McLaughlin & vdM 2005's adopted M_V,⊙ = 4.85**, and on Lelli 2016's helium factor 1.33.
- **The fraction of HI inside r½.** Putman gives totals only (§2; Table 1).
- **Accuracy of r½ = 4/3 R_h for elliptical systems.** Wolf calls testing against ellipticity "an important future step" (l.1187).
- **Effect of a star-count-weighted σ in place of a luminosity-weighted σ.** No size is given by Wolf, Collins or Tollerud.
- **Metallicity-scale offsets** between Harris-catalogue globular-cluster [Fe/H] (the axis of McLaughlin & vdM's (M/L)₁) and the spectroscopic dwarf [Fe/H]. No statement found in McLaughlin & vdM §3 or Woo §2.
- **A Geha 2026 statement of the number of members inside 2 r_eff** (Table A1 notes, l.950).
- **The size of Savino's 3.5% systematic in Table 5's per-galaxy errors** (§4.6, Table caption l.865). See Doubt 2.

## Doubts

1. **Net distance dependence is my inference from the v1 formulas, not a source statement.**
   - With L_V = 10^(−0.4(m_V,0 − μ − M_V,⊙)) ∝ D² and r½ ∝ D, `g_bar_stars` ∝ D⁰, and `g_bar_gas` ∝ D⁰ after the (D/D_Putman)² rescale. g_obs = 3σ²/r½ ∝ D⁻¹.
   - So under v1, distance moves g_obs only, and the ratio g_obs/g_bar moves ∝ D⁻¹.
   - Exception: Boötes III uses a distance-independent M_V (D-061 item 2), so its g_bar ∝ D⁻².
   - The brief's "it moves both axes" is true at the level of the inputs, but the stellar g_bar cancels. I have not checked this numerically against the tables.
2. **Savino's systematic and the printed errors.** It is unclear whether the ~3.5% systematic (l.1244) is inside the Table 5 errors. l.952 says the quoted intervals "account for … the adopted PWZ calibration", while §4.6 lists the systematic separately. I read them as separate, but that is an inference.
3. **Magnitude errors are mixed in kind.**
   - For 5 systems the package folds the source modulus error into the magnitude error in quadrature (D53).
   - For the Muñoz route, the M_V error (bootstrap shot noise) is used with D from Table 1, which has no error.
   - Martin's m_V,0 is built from draws of the distance chain (l.377), so its printed error may contain some distance dependence.
   - Pace says compiled M_V errors usually exclude distance (l.935).
4. **Martin 2016 and Collins 2013 on And XXVII both say the system is likely unbound.** v1 plots it with Richardson 2011 structure. Ji 2021 reports tidal-disruption kinematics for Antlia 2. D-025 says sources that describe a system as out of equilibrium go to the exclusion register. I report this only as what the sources say.
5. **The aperture of Geha 2026's σ (2 r_eff) uses LVDB v1.0.6 r_eff, not the package's R_h.** Whether the two match was not checked.
6. **D-038 1A registers "member-sample σ taken as representative of the light-weighted σ" as a named assumption.** I did not find it in the v1 `assumptions` string or in `data/assumptions.json` under the dwarfs package.
7. **No per-system binary-screening flag found in the v1 tables**, although D-025 asks for one. The word "binary" appears only in the generic obs `steps` text. The `reading/` files hold it (for example `sigma_values.csv` col `binaries`).
8. **`beyond_source_range` counts differ.** It appears on 39 of 64 measurements; D-060 recorded "26 of 64" below the floor at ruling. This is possibly due to D-059 fallback metallicities; not investigated.
9. **The `distance_inherited` flag named in REPRODUCTION.md does not appear in v1 `x_dwarfs_flags` counts.** I did not check whether any system inherits a host distance.
10. **And XVIII distance.** Kvasova 2024 rescales an HI limit to "1.33 Mpc" (l.426); the package distance is 1180 kpc. This is a disagreement between sources on one system's distance, not checked further.
11. **Antlia 2** has no distance error in v1, while Vivas gives a 5.4 kpc dispersion and a ~13 kpc depth gradient (D40).
12. **Wolf's own Table 1 R_half convention** "differs from the geometric means" (l.443), while v1 uses the circularised radius. Whether the 4/3 accuracy statement applies equally to circularised radii is not stated (see D24).
13. **Sources quoted from arXiv only.** All quotes come from arXiv e-prints, not versions of record. Pace, Wolf, Lelli and McLaughlin & vdM were taken at the latest arXiv version, because the package does not pin a version for them.

**Read lightly or not at all:**
- Kvasova 2024 and Simon 2020: only the passages cited.
- Not read: the remaining single-system originals (for example Sandford 2026, Ou 2024, Kirby 2013/2017, Koch 2007, Spencer 2017, Hendricks 2014, Battaglia 2011/2012, Kacharov 2017, Gregory 2019, Hansen 2024, Chiu 2026, Li 2026, Cerny 2026, Koposov 2018, Simon 2011, Collins 2021, Ho 2012, Richardson 2011, McConnachie 2006, Correnti 2009, de Jong 2008, van de Rydt 1991, Saviane 1996, Stetson 2014, Richstein 2022/2024, RC3) and Bruzual & Charlot 2003.

**Memory used:** none. No report file was written; nothing in `/home/claude/atlas` was modified.