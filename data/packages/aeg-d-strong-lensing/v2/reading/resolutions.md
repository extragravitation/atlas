# aeg-d-strong-lensing/v2: second reading, disagreements and findings

**Reader:** independent second reader (Claude), 2026-11-05. Item 11 and "Order of work" step 1 of `data/packages/aeg-d-strong-lensing/v2/REPRODUCTION.md` (main at `b3de95c`).
**Access:** I did not open v1's g columns, `convert.py`, any RESULT file or any v2 table. From `measurements.ecsv` I extracted only identifier, role, scope, θ_E, redshift, cosmology, source and profile columns (script `scripts/rows.py`), and I computed no g_obs, g_bar or ratio.
**Method:** every quote in the six CSV files is an exact substring of the line given. A script places it and fails if the quote is missing or matches more than one line (`scripts/common.py`, `loc()`). Fractions are printed error ÷ printed value only.

## 1. Result in one paragraph

- **No D-096 case found.** No source marks a preferred value, or names a fiducial baseline, that differs from a v1 default. No source excludes data points that the Atlas computes from. This confirms the test's "Expected: no change". **No rule-1 conflict goes to JvH.**
- The rule 5 classes match the test: 107 class A, 1 class B, 37 with no θ_E error, 2 aperture.
- All 147 θ_E values match v1.
- The four H0 values in item 7 are confirmed. The three abstract-page hashes match item 9 exactly.
- Six findings need a call or a note. Items 2.1 to 2.6 are for JvH; none of them is under rule 1.

## 2. Items for JvH (none is a rule-1 conflict; none changes a value under D-096)

### 2.1 J0403−0239 light profile: the reading records "printed"

The test lists J0403 as "the reading decides" in the no-profile scope.

**What R29 prints:**
- "shows a smooth inner light profile, well fitted by a Sersic profile with index $n$\,$\approx$\,4." (newlens.tex l.169, PS1 imaging);
- "an effective (half-light) radius of 5.7\,arcsec" (l.198, PS1 *i* band).

**Why the reading records it as printed:** it is one single-component Sérsic description of this lens, with R_e and n printed. That is the letter of rule 5.

**Caveats:**
- n is printed as approximate.
- R29 does not say that the 5.7″ comes from that same Sérsic fit.
- The galfit model used for the PSF correction has no printed parameters.

**Consequence:**
- J0403 gets `x_strong_lensing_dlngbar_dlntheta` computed with Sérsic n = 4 and R_e = 5.7″.
- The "θ_E error stated; effect on g_bar not computed" line then covers 4 rows: the 2 MaNGA rows and the 2 NGC 6505 rows.

If JvH reads "n ≈ 4" as not printed, change the `profile_status` of that one row in `profiles.csv` to "none printed" before freezing.

### 2.2 SNL-1 and SNL-2: the basis the test gives for `total_mass_form` does not hold at source

Test item 4 says the SIS half-separation approximation "stands in for a full lens model" on SNL-1, SNL-2 and J0403.

- **J0403: confirmed.** "We compute $M_{\rm Ein}$ using the symmetric lens equation" (R29 l.210), with R_Ein the half separation (l.196).
- **SNL-1 and SNL-2: not confirmed.**
  - R61's adopted masses come from full parametric models: SIE+γ and MFL+γ for SNL-1, and MFL+SIS or MFL+SIE with the companion for SNL-2 (l.315, l.317).
  - They are evaluated inside R_ap: "Masses are measured within the fiducial radius, R$_{\rm ap}$. However the values are derived from the HST data and refined mass models." (clean_snl12wcollier.tex l.209).
  - Only the aperture radius is the SLC15 half separation.

No value changes. Whether `total_mass_form` stays on these two rows under D-087 is a labelling call for JvH. `theta_class.csv` records both rows as `aperture`, as the test expects.

### 2.3 SNL-1 gas: newer sources state gas is present; v1 flags it as negligible from R25

v1 gives SNL-1 the flag `gas_negligible_source_assumption`, which rests on R25 l.769. Two newer sources state gas inside the aperture, without a size:
- **R26** l.323: "which is likely driven by the presence of warm gas" (SNL-1 nebular emission, from a 2.2″-radius spectrum);
- **R61** l.183: "This suggests the presence of a small cold ISM disc." (inside about 1″, within R_ap = 2.38″).

**R29** (J0403) also reports "a nebular line emission component" in the Einstein-aperture spectrum (l.191, l.225).

The registered gas term (D-076) is unaffected. The notes that record source gas statements (D-075 item 1) are incomplete for SNL-1 and J0403. **Proposed:** add these quotes to the row notes, and let JvH decide whether SNL-1 keeps the flag.

### 2.4 J0403 dust is not in the frozen term table

R27 (lens_search.tex l.600): "there are signs of irregular patchy dust obscuration running close to the lens galaxy near to the inner image". R29 corrects L_Ein for Galactic extinction only, and its emission-line correction assumes "(we assume no internal extinction for this" exercise) (l.230).

SNL-1's dust already has a term (`internal_dust_snl1`); J0403's has none. The term table is frozen ("exactly the rows below"), so the reading cannot add one. **Proposed:** record it in a known issue or in the row note.

### 2.5 The SNELLS H0 pair: R25 adopts 70.4, but its test sentence says 70

- R25 adopts "$H_0$\,=\,70.4" (snellsI_arxiv.tex l.188).
- Its H0 sentence compares 67 "rather than $H_0$\,=\,70\,\kms\,Mpc$^{-1}$ from WMAP7" (l.862–863).
- The test's `cosmology_h0_snells` takes "adopted 70, alternative 67", so p = 67/70.

The reading confirms that 67 and 70 are the pair as R25 states it. The printed adopted value is 70.4, which would give p = 67/70.4. D-104 rule 1 says "each source's value against the alternative it names". Which number counts as "its value" here is for JvH to read; the test as frozen uses 70.

### 2.6 The black-hole inventory: R26 does not fit either of the test's two components

Item 9 splits the black hole into two components:
- "SNELLS, MaNGA and NGC 6505 sources": `stated_negligible`;
- "other sources": `not_addressed`.

At source:
- **R26** (a SNELLS source, used for SNL-0's g_bar) includes a black hole on the McConnell M_BH–σ relation in its fiducial dynamical model (snells.tex l.169), and tests none and 10¹⁰ M☉ (l.196). It neither calls the black hole negligible nor leaves it unaddressed.
- **R61** (the SNL-1 and SNL-2 default source) does not address it. For those two lenses, the negligible statement comes from R25 only.

`baryon_inventory.csv` records R26 as `addressed_in_dynamical_model_only`. The quotes for R25, R28, R30 and R32 are confirmed at the lines the test cites. **Proposed:** name the component by source list rather than by survey.

## 3. Disagreements with the test's stated expectations (resolved at source; no ruling needed)

| # | Test says | Source says | Reading |
|---|---|---|---|
| 3.1 | Item 6: "An asymmetric θ_E error (SL2S)" | R20 prints one symmetric error: tex `$1.76 \pm 0.05$` (lensfit.tex l.15) and MRT `e_Reff` "The 68% confidence interval on Reff" (one column) | `_lo` = `_hi` for both SL2S lenses (0.0284091; 0.0344828) |
| 3.2 | Item 6: `r_eff_sl2s` 0.10 "where the reading records HST imaging", 0.30 for CFHT | Both SL2S lenses have HST imaging (MRT t6 "HST = Y") | The imaging is recorded per R_e variant, not per lens. CFHT R_eff (v1 default rows m134, m135, m137, m138) → 0.30; HST R_eff (alternatives m136, m139) → 0.10 (`profiles.csv`, `applies_to_rows`) |
| 3.3 | `aperture_radius_snl12`: "R61 Table 2 l.151" | R_ap is in R61 **Table 1** (`\label{tab:lens}` l.140; row l.151) | Location label only; values 2.38″ and 2.21″ confirmed |
| 3.4 | Item 5, class A: "the source defines M_E as the mass inside the radius of mean convergence 1" | Stated by R13 (Eq. 8, plain.txt l.1651), R9 (l.117), R20 (l.414), and R29 with R25 (l.210; R25 l.642). **Not stated** by R32 or R30 | R32 and R30 kept as class A on inference. R32's M_Ein errors are exactly twice the fractional θ_E errors (1.1/28.2, 3.7/18.8). R30 has only "the mass enclosed by the Einstein radius" (l.778). Recorded in `me_definition` |
| 3.5 | Item 5, MaNGA J1701: "we impose a 10 per cent error on θ_Ein" | Text 10 % (l.261); Table 1 prints 1.63 ± 0.16 (0.0982) | Fraction recorded as 0.10, the stated percentage; the table ratio is in the note |
| 3.6 | Err-level table: R32 g_bar `not_given_by_source` (the "2σ interval" belongs to the dataset term) | The ±0.26 on Υ_ref is 1σ by R32's own construction (2.41–3.46 adopted "as the 2σ interval"); the L_Ein errors carry no level | Agrees for `g_bar_err_point_*` (L_Ein only) and for the combined `g_bar_err_*` (one component unlevelled). The Υ_ref component's implied 0.683 is recorded on its own row |
| 3.7 | Item 1: "The reading records whether R30 states which one it uses for distances" | Not stated. z_l = 0.04243 (l.639); cosmological z = 0.041 ± 0.001 (l.790, in Discussion); no sentence links either one to R30's distances | No D-096 case; the v1 default stands (D-075 item 4) |
| 3.8 | Item 1: "a preference stated [in R27] could change a default" | R27 measures R_Ein 1.49″ from HST (l.604) and says it "changes our mass-measurement by less than 2 per cent … our previous conclusions are unchanged". It prints no M_Ein and marks no preference | No D-096 case. Borderline (a newer value exists), so it is listed here. R27 also gives z_s = 0.195 (l.598), against R29's 0.19165 (z_H) and 0.19130 (z_CMB); not resolved by either source |

## 4. Findings not in step A (all recorded; none changes a value)

1. **R28's distance statement in α** (lensz_arXiv.tex l.727–730): "rescaling the distance assumed for [ESO 325-G004] affects $\alpha_{\rm MW}$ linearly". At the Abell 3570 distance α_MW is 1.15; at +1000 km/s it is 0.95. This is an α statement, so it belongs in the `lens_distance_snl0` note only (D-104 rule 1).
2. **R20 states a preference for NIR stellar masses:** "NIR should give more reliable stellar masses" (sl2s-rm-pdflatex.tex l.813–814). v1's Chab(NIR) default already agrees.
3. **R5 states a preference for SIE over LTM:** "strongly favor the SIE radial mass-density profile over the LTM profile" (l.875–876). v1 already agrees.
4. **R9's reference model is a fiducial baseline under D-096 rule 3** (l.424). R10 prints only that model, and v1 uses it.
5. **R25 gives a different SNL-0 mass.** It prints M_Ein(SNL-0) = 14.3 ± 0.7 × 10¹⁰ (symmetric formula; l.596), and R26 uses "M_Ein from S15" for its (M/L)_L. Neither marks a preference over R28's MFL 1.50 × 10¹¹, so it is not a D-096 case.
6. **R29 is internally inconsistent on its M_Ein error.** M_Ein ∝ R_Ein², so a 2 % R_Ein error would give about 4 % on M_Ein. R29 prints 10.64 ± 0.23 (2 %) "dominated by the measurement of R_Ein" (l.210). The θ_E term uses the R_Ein fraction 0.03/1.47, so the class A treatment is unaffected.
7. **R13 overlap (requested by the order of work):** R13 does not state that its M*(≤R_Ein) errors include the θ_E error.
   - R13 applies "a conservative 5% error" in θ_E to the lensing masses only (plain.txt l.1671).
   - M*(≤R_Ein) = f_ap M* (Eq. 10, l.1686) carries the SED-fit errors (l.952), with no f_ap or θ_E error stated.
   - The `theta_e` note should say "R13 does not state that its M* errors include the θ_E error".
8. **SLACS profiles:** R5 Table 4 R_e (de Vaucouleurs, F814W, intermediate axis; l.1855–1856 notes) equals R13 Table 1 θ_e for all 48 systems. R13 states θ_e is "measured by fitting a de Vaucouleurs luminosity profile on the F814W images" (l.140) and uses it in f_ap (Eq. 1, Eq. 11). So R5's profile is the one behind R13's M*(≤R_E).

## 5. Disagreements with step A

- **None on any value or size.** Every step A quote I re-read is at the line given, apart from these location slips:
  - Reader B gives R61's L_F814W at l.155; it is l.154 (l.155 is the half-separation).
  - Reader B gives R61 Table 1 "l.151, 156" for R_ap and the half-separation; they are l.151 and l.155.
- **Step A did not record** the items in §4 (1, 2, 5, 6), the gas and dust statements in §2.3 and §2.4, or R26's black hole (§2.6).
- **Adjudication F2** lists "3.5–5 % for H0" as sizes. D-104 since re-sized these as H0 values; the reading supports D-104. All three percentages are stated in α (R25 l.863, R29 l.241, R32 l.293).

## 6. Sources

- **Read at source:** R5, R9, R10, R13, R20, R21, R25, R26, R27, R28, R29, R30, R32, R61, plus the three abstract pages.
  - Cached step-A e-prints were used, because their SHA-256 matches readers A and B. They were copied into `dl/<id>/` and re-extracted.
  - The abstract pages were fetched on 2026-11-05. Their hashes equal those in test item 9.
- **Released tables used as cross-checks:** IOP R20 t6 and t7, R10 t1 and t2. These are step-A copies; their hashes equal `sources.json`.
- **Not read:**
  - VizieR R5 table4/table5 and R13 — not fetched. Their values were taken from the e-print tables instead; nothing was blocked, because no fetch was tried.
  - Planck Collaboration 2014 (named by R25, which prints 67 itself).
  - Komatsu et al. 2011 (WMAP7; the sources print 70.4).
  - R7, R33 and R36 (outside this task's list).

| Record | e-print | e-print SHA-256 | file read | file SHA-256 |
|---|---|---|---|---|
| R5 | 0805.1931v1 | fb72fd1120d6c53164d1442bd99c2dfa5b02ba81656febc67ce7e35c20e85cc5 | ms_arxiv.tex | 378fa2f309420310a1e0df85898f5d1bedefc0e5f34325cd0179445a8bf84f0f |
| R13 | 0904.3282v2 (PDF) | df3746887007595b00e7fb2564ae1e9121e95849c68c04e55d2a06e3324587cf | plain.txt / layout.txt (pdftotext 24.02.0, default / -layout) | 9c33e0c6f2447e5f5d5ced2b434090970a7868e881a5ca1481a8ae89c06bbacb / 127e3f5e26a68c128df4d7ec2544dd0c07acca6b4c843d05e0484c372bb3db76 |
| R10 | 1711.00072v2 | b23d5e6a2e56f667f3c8f77fa4b2edfe1c70ee15fa72a19bbec506680c565216 | ms_arxiv_v2.tex | 8e773d700fd9e3808660c869f33051acd13e5652e5181d011e64f2a660628bd1 |
| R9 | 1407.2240v2 | eb8ec838e63006c8417d68d479b238448d59373984bee501e873b628724cace2 | ms_v2.tex | e96834f21027138b1cfddc3531da5ff36cda6efc9949e423e7dfa43d0149d0cf |
| R20 | 1307.4764v1 | c7bc75399959c9a4e0e141c2892a3aff251c88f23ba6796ebfc162699b83aba2 | sl2s-rm-pdflatex.tex; lensfit/cfhtfit/hstfit.tex | 94deec72…2ac7; adf3badc…42de; 8c5a0185…683f; a3e7c981…16fb |
| R21 | 1307.4759v1 | 3559ca615c3f115b34c495346b038a4e9901b11b0acdadeb98df778be361d487 | sl2s-rx.tex; spectable.tex | 03e6b329…7356; 9756a657…a04a3d |
| R28 | 1306.4983v1 | 937049df5ccec96465b3620079e83f3ca180b6f10c5d2b8b9bfc063c440820c8 | lensz_arXiv.tex | 6825e0a41be274b3d19142e0e9cf955f34f5a319e43e56f16a5af43b865cba58 |
| R25 | 1503.02661v1 | 0d84014cd169eb0b96c5e18e08910e9e690b8632adba7db3d40e66ad23c7333c | snellsI_arxiv.tex | 81993a940718aa3b44db0a441cccbbf5296df0b83996b226779ae0f83b6e6a7c |
| R26 | 1612.00065v2 | 1731105f1ad5dcb866e94ed71c245600462e28c3e451e00ea3ffc729e3d3b4c7 | snells.tex | c49a14cc16eace5ad63346ba7db117a9cef1409b58e776725242e06d5e3dc654 |
| R61 | 1709.01931v1 | 6698ce848e622cc5058fdaf6996e6422f37ef2ba0cf5256fb11c639df123096e | clean_snl12wcollier.tex | 482c7c71fba3d110ff663146c056553faa56f7f1a9cbec8d5bb85a22c702f7d1 |
| R29 | 1803.07082v1 | c0e2dfd07e82d086bb59e8d74da318d8deea7a718ca9b90fbf56ef938d7cb46b | newlens.tex; newlens.bbl | c315888c…9b31b; 9cf88bb0…e78d |
| R27 | 2002.07191v1 | c15f94c12a9e16b785ec6affcf16a9814daf7eca3e13c327f999bb7311b1567a | lens_search.tex | 08b079ce6410627276e10657c10688ee6c0e178550a0c266a4668c028290a3fa |
| R32 | 1911.06338v1 | a2fe49d396d3ae46657cf37c726198e434e6b08b0ed2d70e28faefd90ebdac67 | main.tex; main.bbl | e7dad417…a397; 7f2545f5…ddc1 |
| R30 | 2502.06505v1 | 7f4f5813fa3e0e52f0b59a240dc4ab32366779975aaed18119f0ad15d8dcfffb | ms.tex; ms.bbl | e6cce9d6…510d; 08c66f0a…2296 |
| Planck 2015 XIII | abs/1502.01589 | d85fc462fcabf12405ff913a587196bf78b1e1a35b235de8812f49a4662f9cb9 | abs.html | same |
| Planck 2018 VI | abs/1807.06209 | 17256f2d1adbc17162eb3d0e29bf1a547d6dfb131efe3231d2d32abfc72429fa | abs.html | same |
| Bennett 2014 | abs/1406.1718 | 4f18ff396491283c7e0fce47b2010caae4ab0c6ab5344a1efabcb924f1f78008 | abs.html | same |

The full hashes of every file are in the CSV columns `file_sha256` and `eprint_sha256`.

## Resolutions of the reader's six calls (main session, 2026-11-05, no access to any v2 value)

None of these changes a value, and none is a rule-1 conflict.

1. **J0403 light profile: none printed.** `profiles.csv` is updated. n is printed only as approximate, and R_e is not tied to that fit, so the test's mechanical definition is not met. D-104 rule 3 applies.
2. **SNL-1 and SNL-2 `total_mass_form`.** The classification stands: their masses come from full lens models evaluated inside R_ap (R61 l. 209), which is a fitted total-mass form. The reason the test states is corrected in the result and in the row notes. The value of `model_dependence` is unchanged.
3. **Gas reported in SNL-1** (R26 l. 323; R61 l. 183) **and nebular emission in J0403 (R29).** The sources give no size. The frozen test keeps v1's gas status columns. The statements go into `baryon_inventory.csv` (already there) and into a known issue, with the quotes, for the next version.
4. **Dust in J0403** (R27 l. 600). There is no term row in the frozen table, so it goes into a known issue with the quote, for the next version.
5. **SNELLS H0 pair.** The frozen test uses R25's own comparison, 67 against 70 (l. 862–863). The note records that R25 adopts 70.4 (l. 188). The effect is the ratio R25 states. No change.
6. **R26's black hole** is part of R26's dynamical model, not of a lensing g_bar. It is recorded in the `not_addressed` component's note, with the quote. R61 is `not_addressed`.
