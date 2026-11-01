# A6 strong lensing: adjudication of the gas and supplement readings

**Date:** 2026-11-01. **Adjudicator:** Claude (Anthropic, Claude Opus 5.5), working for JvH. Claude did none of the readings, and the readings are not edited.

**AI disclosure.** Claude did all of the following, and JvH has not yet reviewed any of it:
- reconciled the readings;
- read the disputed values at source;
- wrote the two scripts;
- computed the gas-literature ratios;
- drafted the options.

**Status.** This is a proposal. Nothing here is ruled. Every gas number below is **exploratory**: no test was frozen for it, and none is scored.

**Blinding.** No lens g_obs, g_bar or g_obs/g_bar was computed, and `convert.py` was not run. The only lens quantities computed were the ranges of R_E (kpc) and of stellar mass (§4.1) and, for the Salpeter options, the Salpeter-to-Chabrier ratio of R13's printed stellar masses (§6). Incidental exposures are listed in §8.

## 0. Inputs (SHA-256)

Paths are relative to `data/packages/aeg-d-strong-lensing/v1/` unless they start with `docs/` or `pipeline/`.

| File | SHA-256 |
|---|---|
| `docs/decisions.md` | f1364492919db6bd17fa038b65acfd7a86b278d4e38c7367d4d193146d1bb880 |
| `docs/methods/A6S_PRECEDENCE.md` | f103809eadac00dac657061982e963fdfe1e85f46d68188a73953c17dfe9b03d |
| `REPRODUCTION.md` | 44e3b2715f4aab7ac40900e49fd2cf798679d02839363642dff7367c8f2467ef |
| `reading/GAS_AND_SUPPLEMENT_BRIEF.md` | 2221da06b911e0925f692c61247c06a1a3c2eab5914aab172edc9f7b95084839 |
| `docs/sources/search-log-A6-gas.md` | e5cbdfaa6c849ed7ac7f2f2e0019bc32d3e5210b2ae7b095f91706552ee01534 |
| `reading/adjudicated_inputs.csv` | b29a0691c353c09a9de6fd86b59f438a37ae4a69b3109d3743a58934e2a65d3c |
| `reading/gas/reader-a-C.csv` | 5a35e7fe409520d81a599bb9ce7ba55e23a82a6e7da1965d2b07186280235e9f |
| `reading/gas/reader-b-C.csv` | bd09d59702df56e6ea6d4bd1cba3d73dfa7e2089e15d81a9b18b3bbeac8f8cae |
| `reading/gas/reader-a-N.csv` | 0005ca00c32146b53ee88d02bc509aa80626945e23d1e7219cbb97d3512bae69 |
| `reading/gas/reader-b-N.csv` | 35ea530f042e23e06be88a9584d01fe3a31d57d76af60571ffc21db80edd1901 |
| `reading/gas/reader-a-C-questions.md` | 5c534595a3912264498d489ef56ea9ae7771c782d19273db93b58a66ff5295dd |
| `reading/gas/reader-b-C-questions.md` | bd0153faa0d063b03b892e37c7f619e71bb061995f8773923a5306ae0f98f3f7 |
| `reading/gas/reader-a-N-questions.md` | 0e2e6799d838d19c1b8ba2ed14c44a132ba0a58465c8345b45f853c8a31605e3 |
| `reading/gas/reader-b-N-questions.md` | 0eccea2332cc4d4da898146f5a198535cdab78dea0e6c3abc35250f2b57b42a0 |
| `reading/gas/comparison-C.csv` | 763f016b2e4e4793e073611159c7f9b4a755b9dba40484de7ea3f9c95a8ba864 |
| `reading/gas/comparison-N.csv` | 506f762a4bcb925c1dc263d7aaba4ad39f96c3f3111960af4a063cda653942bc |
| `reading/gas/compare_gas.py` | 1c5bd392dab6877cf487e8508615cc6c7bf5a4abb503e2ed9651619775570988 |
| `reading/readings/reader-a-supplement.csv` | 93a9a43198de1bbc69ccab639556afd1c4880c1b71c98b21cede9a13e22ee77e |
| `reading/readings/reader-b-supplement.csv` | 15e1588728ef10fa238c2d7c294142713b6cdedcd85eae83ec70780cbc0bc300 |
| `reading/readings/reader-a-supplement-questions.md` | eb74da3b25dc645041215338d48e0c699f385552a9c1563be20146a47b56ea96 |
| `reading/readings/reader-b-supplement-questions.md` | eb5dd1564842a3ab31951ae1c6fbf8e1f2ac3b880b9a962822c3bb7d26077248 |
| `reading/comparison/supplement-v2.csv` | 7f9298eea9fc2d422e09ede905064be0547ae829231635d71715689618724c6f |
| `pipeline/aeg/lensing.py` (frozen; matches REPRODUCTION.md) | 0755c9390bf114b283d35305c3882bbe46c41303b7a01dc7c376a2a143926ed5 |
| `docs/sources/screening-A6S/packaging-tools/rank_a6s.py` (read only) | 1b8e420395768a82cc557053eb098120e8bdd2c691b8f8e1e92c69caf0d80a2e |
| `docs/sources/screening-A6S/packaging-tools/a6s_options.csv` (read only) | 28a309ee2ecb24ef62c97f85bf270f8d4ef891dd5a05478d821426f2d6158a80 |

**Written by this step** (not committed):

| File | SHA-256 |
|---|---|
| `reading/adjudicated_supplement.csv` (250 rows) | c176d5c73a8d8b64a9af482cc3bdfb49f16a460254fbcf96b174fdc102ff41fe |
| `reading/build_adjudicated_supplement.py` (builds the CSV; stops on any reader disagreement) | 413289be8e76bb94640cc26f0720b1ea9d383744cc2e11c8ab151bd840a257b0 |
| `reading/gas/adjudicate_gas.py` (produces §3 and §4; run `python -I adjudicate_gas.py <repo root>`) | f5dc12f8831e6da8bf7c8f77b8b694fc8eac04108cddbdcedc52f1d33b9ef7f4 |

**Opened at source by the adjudicator** (arXiv PDFs fetched with curl's own user agent, read with pdftotext; VizieR from the CfA mirror):

| Source | File | SHA-256 |
|---|---|---|
| R13 VizieR J/A+A/501/461/lens (selected columns zl, thetae, MChaBC, MSalBC and their errors) | r13_lens.tsv | 39082a8e9de93be992f26a0fea392b5d07d8c30d2747abb6df417e3c625affee |
| R7 IOP ascii Tables 3 and 4 | t3, t4 | b99bae9b…dd41dd6 (t3) and 7c8a3297…d66d (t4), the same as reader A |
| R61 arXiv:1709.01931 | pdf | 8b9a54259f783f5b843fcfeca20b1d67e0fb2c4af4f1cc1174b571e2c5436552 |
| R30 arXiv:2502.06505; R32 arXiv:1911.06338; R9 arXiv:1407.2240; R10 arXiv:1711.00072; R13 arXiv:0904.3282 | pdf | identical to reader A's hashes |
| N7 Su et al. 2015, arXiv:1504.01203v1 | pdf | 4ce8bea5ca433ce47e38cedc1bc2bbef9cd67ab1a63802616e07766126393e4b |
| N2 David et al. 2006, arXiv:astro-ph/0609113v1 | pdf | d95b80f1dccf33ce972f4791e28c84e1620d735fb62d9a0bb2762a5782fc6f09 |
| C4 Das et al. 2010, arXiv:1007.5322v1 | pdf | 0ee2ddc73e5e296ebcca5f48099d5426429d941fa7ff1529b5d9754b8f8cb24d |
| N18 Young et al. 2014, arXiv:1312.6318v1 | pdf | d5194efeafa0c41e8412153d448d6319d37ea1eb4c3926f8dd7650ac14537987 |
| C13 Young et al. 2011, arXiv:1102.4633 | pdf | 83a0a162724cc31292a92c74dbb3dc6e4f5a1f14d103ed9321694a57a2076753 |
| N13 Davis et al. 2019, arXiv:1903.08884v1 | pdf | 997957518ab54ce9c5491072f41df21051eec9ec42f2bb88600f19f9efce58a3 |
| C15 Davis et al. 2016, arXiv:1510.00729v1 | pdf | 996f5ffb8ec2595341990091761c003644d8cd0a81ec8be408c8e50a9976c8b7 |
| N14b O'Sullivan et al. 2018, arXiv:1807.09110 | pdf | c9c6d3fa3395c42287ff62bf025760d9ad09fb505a2f836c4a236a22a5658345 |
| N14a O'Sullivan et al. 2015, arXiv:1408.7106 | pdf | 3567055388713747965d48deab4b044a59b3fff6a5c466988795409bc9a3470f |
| C21 Salomé & Combes 2003, arXiv:astro-ph/0309304 | pdf | b75c5db7c489f8a6a07f6571030b21efd951fe1544a046f9699ce4ab6f3c245a |
| C27 Oosterloo et al. 2010, arXiv:1007.2059 | pdf | cd5d46b3bc65f27ce78ada0557045978eb3e85a50971717741c65753897383ac |
| C17 Combes, Young & Bureau 2007, arXiv:astro-ph/0703557 | pdf | 96892b0e00c263ac84c759efd47514bb7ae27ae9ac381afcdbed2c2fb7dc82fe |

Downloads are in the session scratchpad (`gasadj/dl/`), not in the repository.

## 1. Supplement (part S): reconciliation

**Method.** `comparison/supplement-v2.csv` is all `only_a` / `only_b` (174 / 224), because the two readers named the scope differently ("S3 R13 SLACS z_l<0.30" against "SLACS V-modelled lenses"). So the values were compared on a key of normalised system, record, quantity and IMF. This is done in `build_adjudicated_supplement.py`, which stops on any disagreement.

| Block | Rows (A / B) | Value agreement | Checked at source by the adjudicator |
|---|---|---|---|
| R29 cosmology | 3 / 4 | H0 70.4, Ω_m 0.272, Ω_Λ 0.728: agree. B adds "flat: not stated" | — (both quote §4 verbatim) |
| SNL-1, R25 | 9 / 9 | all values agree (L_J 4.3 ± 0.1; Υref 1.47 ± 0.12 and alternative 1.46 ± 0.18; 2.38″ = 1.47 kpc; Kroupa; M05) | not re-read (both readers; same file hash) |
| SNL-1, R26 | 7 / 7 | all values agree (L_r 1.62 ± 0.05; (M*/L_r)MW 3.93 ± 0.20; 2.38″ luminosity aperture, 2.2″ spectroscopic aperture; Kroupa; CvD12-descended) | not re-read |
| R13 totals, z_l < 0.30 | 96 / 96 | **96/96 agree** (48 lenses × Chabrier-BC03 and Salpeter-BC03, asymmetric errors) | **all 96 checked** against VizieR. Rows were matched on (z_l, θe), giving 48 unique matches and 0 mismatches. The 9 VizieR rows not used all have z_l ≥ 0.30 |
| R13 R_e (θe), z_l < 0.30 | 48 / 48 | **48/48 agree** | all 48 checked (the matching key) |
| R7 log M_E, z_l < 0.30 | 74 / 74 | **74/74 agree**: 63 printed values, plus 11 that are not printed (A left them blank, B wrote "...") | **all 74 checked** against IOP Table 4. The selection was checked against Table 3: exactly 74 lenses have z_lens < 0.30 |
| Salpeter conversions | 6 / 5 | R29 α = 1.55; R32 α ≈ 1.65; R30 ÷ 0.61; R10 and R20 model papers: "not printed". All agree | R30 and R32 sentences read at source |

**Differences settled.**
1. *Quantity names only:* `L_Ein`/`L_in_aperture`, `ML_pop`/`ML_stellar_pop`, `salpeter_conversion`/`salpeter_alpha`/`chab_to_salp_ratio`. I used the names in `adjudicated_inputs.csv`. R13 totals are written as `mstar_total`, so they cannot be confused with the default `mstar` inside R_E.
2. *R32's second phrase "α & 1.6"* (B's Q5) is the pdftotext rendering of a relation glyph in "consistency with a Salpeter IMF (α & 1.6)" (§5, line 223 of the extraction). It is a qualitative statement and is not used. The printed conversion is "α ≈ 1.65" (§5, para 1), carried with the flag `approx_printed`.
3. *R7 cosmology* is printed as "h = 0.7". It is written as H0 = 70 with the flag `H0_from_h`. Ω_Λ = 1 − Ω_m, so it is flat under D-075 item 4.
4. *B's extra R25 rows* (M_E 8.9 and the gas statement) are outside part S. They are already covered by the adjudication (§5) and the observed default (R61), so they are not carried.

**Findings (facts).**
- **R13 coverage.** R13 prints 48 lenses below z_l = 0.30. The adjudicated SLACS set has 54 below 0.30 (from R5). The 6 lenses with no R13 entry (J0841+3824, J0955+0101, J1032+5322, J1103+5322, J1251−0208, J1432+6317) also have no R5 θ_E in `adjudicated_inputs.csv`, so no plotted system loses a stellar-mass record.
- **R13 R_e** is R5's de Vaucouleurs F814W fit as R13 reprints it (R13 Table 1 cites Bolton et al. 2008a). R5's own table was not opened, by either reader or by me. This is the one open check (reader A's Q4).
- **R7.** 54 of the 74 are the adjudicated SLACS-V lenses, all with a printed log M_E and no error (`no_uncertainty`). These are the inputs to the reported §4 formula check. The other 20 are not in the SLACS-V adjudicated set; 11 of them have no printed M_E. They are recorded only (B's Q2: keep, as record-only).
- **SNL-1 fallback (D-075 item 2): the next-ranked record is R61, not R26.** The frozen ranking in `rank_a6s.py` orders eligible records by band count, then per-object fit, then year. Applied to `a6s_options.csv` rows 59–62, that gives R33 (2022), then **R61** (2018; per-object Y; one band), then R26 (2017; Y; one band), then R25 (2015; `partial`).
  - The part-S brief asked only for R25 and R26, so I read R61 at source:
    - Table 1: "LF814W (≤ Rap) (10^10 L⊙) 2.52 ± 0.04", "extinction and band-shifting corrected", inside R_ap = 2.38″;
    - §5: "combined with the converted Υref of 2.75 (Newman et al. 2017)". This is R26's Kroupa SPS M/L, converted to F814W with ezgal. No error is printed.
  - The R61 route uses the same aperture as R61's lensing mass, which is the observed default. It is the same construction already adjudicated for SNL-2.
  - **These two values have one reading only** and need a second reading before packaging. The rank order is a mechanical application of the frozen rule, but JvH should confirm it, because the brief named R26 and R25.
  - R26 and R25 are carried as ranked alternatives. Two caveats:
    - R26's spectroscopic M/L aperture (2.2″) differs from its luminosity aperture (2.38″). The paper says the two are "matched within ≤ 8%".
    - R25's Υref is an assumed-age M/L (10 ± 1 Gyr). It is eligible under D-063 item 1 only with its range carried.
- **R10 and R20 model papers print no Chabrier-to-Salpeter ratio** (both readers). That leaves the S4TM Salpeter top open (§6). SL2S does not need one, because R20 prints its own Salpeter masses.

`adjudicated_supplement.csv` (250 rows, columns of `adjudicated_inputs.csv`):

| Block | Rows |
|---|---|
| R29 cosmology | 3 |
| SNL-1 | R61 3 (fallback candidate); R26 8; R25 9 (ranked alternatives) |
| R13 | 96 totals (`mstar_total`, status "profile-step check input (D-075 item 5)"; Salpeter rows also "range top"); 48 R_e |
| R7 | 74 M_E (54 reported check, 9 record-only, 11 not printed); 3 cosmology |
| Salpeter conversions | 6 (3 factors, 3 "not printed") |

## 2. Gas (part G): reconciliation

**Method.** `compare_gas.py` keys on the radius as printed, so most of its `only_a`/`only_b` rows are formatting differences. I re-keyed the value-bearing rows (`gas_mass_in_radius`, `gas_to_stellar_in_radius`) on candidate plus normalised galaxy. Values were compared as numbers after applying the printed unit multiplier, which is a units normalisation only.

**Result.** Every value that both readers recorded agrees:
- C series: 30 galaxy keys;
- N series: 97 galaxy keys;
- 0 value disagreements, and limit types agree. N14's "upper (3 sigma)" and "upper" are the same limits; the source states 3σ.

All the real differences are about coverage or labels. Each was settled at source:

| # | Candidate | A | B | Settled at source | Ruling (fact) |
|---|---|---|---|---|---|
| 1 | **N7** Su et al. 2015 | 11 per-galaxy hot-gas masses inside 2 r_e (brightest quarter) | `none_found`: "No hot gas masses" | Table 3 header lists "MXgas (10^8 M⊙)"; note "†: derived within 2 re"; §3.3: "we obtained the hot gas mass MXgas for each galaxy … as listed in Table 3". All 11 values, their L_K (same aperture) and r_e (Table 2) checked line by line | **A is right.** B missed the column. N7 is usable: hot gas and L_K in the same 2 r_e aperture |
| 2 | **C21** Salomé & Combes 2003 | 32 per-galaxy rows | catalogue pointer only | Sample of 32 (≤ 40), so the brief requires per-galaxy rows | A is right on coverage. **Not used** (§3): cooling-flow BCGs; beam 22″ at z up to 0.234 (tens of kpc); no stellar mass; "Mgas = 1.36 M(H2) … displayed in Table 4" against a column headed M(H2), unresolved at source (a factor 1.36) |
| 3 | **C27** Oosterloo et al. 2010 | sample statistics only | 15 per-galaxy HI limits with beams | Sample of 33 (≤ 40). §3: limits are "three times" the noise "over one synthesised beam" | B is right. Limits valid inside one beam (an ellipse ~60–78″ × 13–26″). **Not used for ratios** (no stellar mass printed) |
| 4 | **C17** Combes et al. 2007 | 9 rows (quarter of 48 rows) | 11 rows (quarter of 43 observed, tie at M_B −20.42) | NGC 474 "< 0.38" and NGC 1023 "< 0.04" (10^8 M⊙), M_B −20.42 for both: verified | Union of 11. Not used for ratios (M_B only) |
| 5 | **N2** NGC 4552 | omitted (R_m 10.7 kpc) | recorded, flagged | Table 5: R_m 10.7, Mgas 2.5 × 10^8 | Outside the brief's 10 kpc limit, which was set before reading. Excluded from the default; shown as a sensitivity (§4) |
| 6 | **C4** Das et al. 2010 | `gas_total_no_radius` | `sample_statistic`, radius blank | §5 end: "The mass in gas calculated from integrating the gas density profiles is < 0.04% of the mass in stars in all galaxies except in NGC 4486 where it is ∼ 0.4%". No radius is given | `gas_total_no_radius` (A). Recorded, not used. It conflicts with N7 for the same galaxies (§4.3) |
| 7 | **C1** Fukazawa et al. 2006 | `catalogue_location` (n_e at 10 kpc) | `none_in_radius` | Both say the paper prints a density at 10 kpc, not a mass | `none_in_radius` |
| 8 | **N19** NGC 5044 | once | twice (2023 and 2024, same 2.0 × 10^7) | same value | Counted once |
| 9 | Labels | `none_printed`, `none_in_scope`, `NS` | `none_in_radius`, `none_found`, `NS` | — | Unified as `none_in_radius` (full text read, nothing qualifying) and `NS` (full text not reached) |

**Coverage of the 53 candidates after reconciliation:**
- **Usable with a stellar mass** (§3): N2, N7 (hot); N14, N13 (molecular).
- **Usable gas values but no stellar mass on a usable basis:**
  - C8 (hot, 2 S0s inside 9.3 and 8.5 kpc);
  - C15, C16, C17, N17, N19 (molecular);
  - C26, C27 (atomic).
- **Sample statistics only:** C13, C14, C18, C19, C25, C30, N13, N14, N18, N20, N4.
- **No in-radius value** (`none_in_radius`): C1–C3, C5–C7, C9, C10, N1, N3, N5, N6, N8–N12, N16, N21, N22; N4 per galaxy (figure only).
- **Out of scope or not usable:** C20 (not refereed), C21 (§2 row 2), C28 and C29 (HI only beyond 10 kpc; C29 is gas-rich selected), N15 (totals), N20 (model-corrected).
- **NS:** C11, C12, C22, C23, C24, C31.

## 3. Measurement table (usable gas measurements with a stellar mass)

**Radius classes:**
- **physical:** a radius in kpc, as printed;
- **beam:** a telescope beam, printed as a FWHM *diameter*. The radius used is half of it. A beam is a soft, Gaussian-weighted aperture, not a hard edge;
- **model-corrected:** extrapolated by a source model (N20). Not used.

**Stellar mass**, in order of preference:
1. the source's own value in the same aperture;
2. the source's own K-band luminosity in that aperture times its own M*/L_K (N2: 0.8, "M∗/LK = 0.8M⊙/L⊙K", §5);
3. otherwise, the luminosity times **M*/L_K = 0.82**, flagged `ML_K_assumed`. This value is printed by C13 §5.1 and N18 §3.3 for ATLAS3D galaxies, citing Bell et al. 2003. N7's galaxies are ATLAS3D galaxies, and N7 prints no M/L. N13 prints none either ("we utilise the Ks-band luminosity as a measure of the stellar mass").

Where only a total is printed (N14, and N13 through L_K), the ratio is **gas inside the beam / total M\***. This is a lower bound on the ratio inside the beam, because M*(<beam) < M*_total.

Generated by `reading/gas/adjudicate_gas.py`. Masses are in M⊙. "<" marks an upper limit.

| Phase | Cand. | Galaxy | Radius as printed | r (kpc) | Class | M_gas (Msun) | Limit | M* (Msun) | M* basis | Ratio | In lens range | Used | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hot | N2 | ESO 0428-G014 | R_m = 4.8 kpc | 4.80 | physical | 2e+07 |  | 2.9e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.000691 | yes | yes |  |
| hot | N2 | NGC 821 | R_m = 7.0 kpc | 7.00 | physical | 5e+07 | < | 7.03e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | <0.000711 | yes | yes |  |
| hot | N2 | NGC 1023 | R_m = 6.9 kpc | 6.90 | physical | 2.2e+07 |  | 6.75e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.000326 | yes | yes |  |
| hot | N2 | NGC 1386 | R_m = 5.7 kpc | 5.70 | physical | 4.9e+07 |  | 2.78e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.00177 | yes | yes |  |
| hot | N2 | NGC 1389 | R_m = 5.7 kpc | 5.70 | physical | 3.9e+07 | < | 3.13e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | <0.00125 | yes | yes |  |
| hot | N2 | NGC 2434 | R_m = 7.5 kpc | 7.50 | physical | 9.3e+07 |  | 5.9e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.00158 | yes | yes |  |
| hot | N2 | NGC 2787 | R_m = 3.9 kpc | 3.90 | physical | 8.2e+06 |  | 1.17e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.000702 | yes | yes |  |
| hot | N2 | NGC 3115 | R_m = 5.8 kpc | 5.80 | physical | 1.6e+07 |  | 7.16e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.000223 | yes | yes |  |
| hot | N2 | NGC 3245 | R_m = 7.3 kpc | 7.30 | physical | 4.6e+07 |  | 4.74e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.000971 | yes | yes |  |
| hot | N2 | NGC 3377 | R_m = 6.5 kpc | 6.50 | physical | 1.7e+07 |  | 2.2e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.000773 | yes | yes |  |
| hot | N2 | NGC 3379 | R_m = 7.7 kpc | 7.70 | physical | 1.4e+07 |  | 5.85e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.000239 | yes | yes |  |
| hot | N2 | NGC 3608 | R_m = 9.3 kpc | 9.30 | physical | 9e+07 |  | 4.19e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.00215 | yes | yes |  |
| hot | N2 | NGC 4251 | R_m = 6.8 kpc | 6.80 | physical | 3.2e+07 | < | 5.34e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | <0.0006 | yes | yes |  |
| hot | N2 | NGC 4435 | R_m = 4.0 kpc | 4.00 | physical | 1.2e+07 |  | 1.9e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.00063 | yes | yes |  |
| hot | N2 | NGC 4459 | R_m = 7.0 kpc | 7.00 | physical | 4.7e+07 |  | 6.06e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.000775 | yes | yes |  |
| hot | N2 | NGC 4552 | R_m = 10.7 kpc | 10.70 | physical | 2.5e+08 |  | 8.4e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.00298 | yes | no | radius > 10 kpc (outside brief); sensitivity only |
| hot | N2 | NGC 4697 | R_m = 9.1 kpc | 9.10 | physical | 8.2e+07 |  | 7.3e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.00112 | yes | yes |  |
| hot | N2 | NGC 5866 | R_m = 6.7 kpc | 6.70 | physical | 5.9e+07 |  | 7.23e+10 | same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K) | 0.000816 | yes | yes |  |
| hot | N7 | NGC 4472 | 2 r_e = 15.76 kpc | 15.76 | physical | 2.31e+09 |  | 2.91e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.00792 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| hot | N7 | NGC 4649 | 2 r_e = 10.91 kpc | 10.91 | physical | 9.29e+08 |  | 2.43e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.00382 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| hot | N7 | NGC 4406 | 2 r_e = 15.02 kpc | 15.02 | physical | 1.48e+09 |  | 2.2e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.00673 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| hot | N7 | NGC 5846 | 2 r_e = 13.57 kpc | 13.57 | physical | 2.04e+09 |  | 1.95e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.0104 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| hot | N7 | NGC 5813 | 2 r_e = 17.23 kpc | 17.23 | physical | 4.67e+09 |  | 1.84e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.0254 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| hot | N7 | NGC 4261 | 2 r_e = 11.08 kpc | 11.08 | physical | 8.19e+08 |  | 1.72e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.00475 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| hot | N7 | NGC 4382 | 2 r_e = 11.31 kpc | 11.31 | physical | 5.35e+08 |  | 1.71e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.00313 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| hot | N7 | NGC 4374 | 2 r_e = 9.31 kpc | 9.31 | physical | 6.04e+08 |  | 1.62e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.00373 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| hot | N7 | NGC 3665 | 2 r_e = 9.75 kpc | 9.75 | physical | 4.35e+08 |  | 1.49e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.00292 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| hot | N7 | NGC 4494 | 2 r_e = 7.89 kpc | 7.89 | physical | 2.13e+07 |  | 1.41e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.000151 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| hot | N7 | NGC 4365 | 2 r_e = 11.66 kpc | 11.66 | physical | 2.45e+08 |  | 1.31e+11 | same aperture: L_K(<2 r_e) x 0.82 | 0.00187 | yes | yes | ML_K_assumed; 2 r_e > typical R_E |
| molecular | N14 | NGC 128 | beam FWHM 6.22 kpc (radius 3.11) | 3.11 | beam | 1.76e+08 |  | 1.23e+11 | total (SED fit, as printed) | 0.00143 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 252 | beam FWHM 7.63 kpc (radius 3.81) | 3.81 | beam | 6.29e+08 |  | 1.15e+11 | total (SED fit, as printed) | 0.00548 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 410 | beam FWHM 8.17 kpc (radius 4.08) | 4.08 | beam | 1.17e+08 | < | 2.34e+11 | total (SED fit, as printed) | <0.000499 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 584 | beam FWHM 1.97 kpc (radius 0.98) | 0.98 | beam | 1.1e+07 | < | 4.17e+10 | total (SED fit, as printed) | <0.000264 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 924 | beam FWHM 6.76 kpc (radius 3.38) | 3.38 | beam | 5.2e+07 |  | 5.75e+10 | total (SED fit, as printed) | 0.000904 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 978 | beam FWHM 7.3 kpc (radius 3.65) | 3.65 | beam | 7e+07 | < | 1.2e+11 | total (SED fit, as printed) | <0.000582 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 1106 | beam FWHM 6.72 kpc (radius 3.36) | 3.36 | beam | 6.81e+08 |  | 7.41e+10 | total (SED fit, as printed) | 0.00919 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 1453 | beam FWHM 5.68 kpc (radius 2.84) | 2.84 | beam | 7.8e+07 | < | 1.45e+11 | total (SED fit, as printed) | <0.00054 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 1550 | beam FWHM 5.53 kpc (radius 2.77) | 2.77 | beam | 4.7e+07 | < | 7.59e+10 | total (SED fit, as printed) | <0.00062 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 2563 | beam FWHM 6.84 kpc (radius 3.42) | 3.42 | beam | 9.3e+07 | < | 1.05e+11 | total (SED fit, as printed) | <0.000888 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 2911 | beam FWHM 4.85 kpc (radius 2.42) | 2.42 | beam | 2.66e+08 |  | 6.61e+10 | total (SED fit, as printed) | 0.00403 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 3325 | beam FWHM 8.5 kpc (radius 4.25) | 4.25 | beam | 1.57e+08 | < | 7.59e+10 | total (SED fit, as printed) | <0.00207 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 4008 | beam FWHM 5.72 kpc (radius 2.86) | 2.86 | beam | 7.3e+07 | < | 7.94e+10 | total (SED fit, as printed) | <0.000919 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 4169 | beam FWHM 6.01 kpc (radius 3.00) | 3.00 | beam | 1.44e+08 |  | 7.76e+10 | total (SED fit, as printed) | 0.00186 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 4261 | beam FWHM 3.1 kpc (radius 1.55) | 1.55 | beam | 3.7e+07 | < | 1.12e+11 | total (SED fit, as printed) | <0.00033 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 4956 | beam FWHM 7.54 kpc (radius 3.77) | 3.77 | beam | 7.5e+07 | < | 8.13e+10 | total (SED fit, as printed) | <0.000923 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5353 | beam FWHM 3.74 kpc (radius 1.87) | 1.87 | beam | 1.9e+08 |  | 1.12e+11 | total (SED fit, as printed) | 0.00169 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5444 | beam FWHM 6.42 kpc (radius 3.21) | 3.21 | beam | 6.4e+07 | < | 1.1e+11 | total (SED fit, as printed) | <0.000584 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5490 | beam FWHM 7.66 kpc (radius 3.83) | 3.83 | beam | 6.4e+07 | < | 1.41e+11 | total (SED fit, as printed) | <0.000453 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5629 | beam FWHM 7.2 kpc (radius 3.60) | 3.60 | beam | 9.1e+07 | < | 8.91e+10 | total (SED fit, as printed) | <0.00102 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 6658 | beam FWHM 6.79 kpc (radius 3.40) | 3.40 | beam | 7.1e+07 | < | 5.75e+10 | total (SED fit, as printed) | <0.00123 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 4636 | beam FWHM 1.43 kpc (radius 0.71) | 0.71 | beam | 1e+06 |  | 3.24e+10 | total (SED fit, as printed) | 3.09e-05 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5813 | beam FWHM 3.15 kpc (radius 1.57) | 1.57 | beam | 1.1e+07 | < | 7.76e+10 | total (SED fit, as printed) | <0.000142 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5846 | beam FWHM 2.44 kpc (radius 1.22) | 1.22 | beam | 1.4e+07 |  | 6.76e+10 | total (SED fit, as printed) | 0.000207 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 7619 | beam FWHM 5.76 kpc (radius 2.88) | 2.88 | beam | 2.9e+07 | < | 1.62e+11 | total (SED fit, as printed) | <0.000179 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | ESO 507-25 | beam FWHM 6.0 kpc (radius 3.00) | 3.00 | beam | 4.23e+08 |  | 8.91e+10 | total (SED fit, as printed) | 0.00475 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 1779 | beam FWHM 5.9 kpc (radius 2.95) | 2.95 | beam | 4.57e+08 |  | 5.62e+10 | total (SED fit, as printed) | 0.00813 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 2292 | beam FWHM 3.91 kpc (radius 1.96) | 1.96 | beam | 4.7e+07 | < | 6.17e+10 | total (SED fit, as printed) | <0.000762 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 3923 | beam FWHM 2.81 kpc (radius 1.41) | 1.41 | beam | 2.9e+07 | < | 1.07e+11 | total (SED fit, as printed) | <0.000271 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5061 | beam FWHM 3.73 kpc (radius 1.86) | 1.86 | beam | 4.3e+07 | < | 9.12e+10 | total (SED fit, as printed) | <0.000471 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5153 | beam FWHM 8.06 kpc (radius 4.03) | 4.03 | beam | 1.75e+08 | < | 7.76e+10 | total (SED fit, as printed) | <0.00225 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5903 | beam FWHM 4.17 kpc (radius 2.08) | 2.08 | beam | 5.8e+07 | < | 5.37e+10 | total (SED fit, as printed) | <0.00108 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 7377 | beam FWHM 6.2 kpc (radius 3.10) | 3.10 | beam | 4.74e+08 |  | 1.1e+11 | total (SED fit, as printed) | 0.00432 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 1395 | beam FWHM 2.95 kpc (radius 1.48) | 1.48 | beam | 2.7e+07 | < | 8.13e+10 | total (SED fit, as printed) | <0.000332 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 3078 | beam FWHM 4.32 kpc (radius 2.16) | 2.16 | beam | 2.3e+07 | < | 6.92e+10 | total (SED fit, as printed) | <0.000332 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5084 | beam FWHM 3.18 kpc (radius 1.59) | 1.59 | beam | 1.6e+07 | < | 8.13e+10 | total (SED fit, as printed) | <0.000197 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 193 | beam FWHM 6.99 kpc (radius 3.50) | 3.50 | beam | 1.35e+08 | < | 8.32e+10 | total (SED fit, as printed) | <0.00162 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 677 | beam FWHM 8.08 kpc (radius 4.04) | 4.04 | beam | 2.25e+08 | < | 8.13e+10 | total (SED fit, as printed) | <0.00277 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 777 | beam FWHM 7.94 kpc (radius 3.97) | 3.97 | beam | 2.08e+08 | < | 2.09e+11 | total (SED fit, as printed) | <0.000996 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 940 | beam FWHM 8.11 kpc (radius 4.05) | 4.05 | beam | 6.1e+09 |  | 8.71e+10 | total (SED fit, as printed) | 0.07 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 1060 | beam FWHM 8.22 kpc (radius 4.11) | 4.11 | beam | 7.6e+07 | < | 2.63e+11 | total (SED fit, as printed) | <0.000289 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 1167 | beam FWHM 7.83 kpc (radius 3.92) | 3.92 | beam | 3.3e+08 |  | 1.7e+11 | total (SED fit, as printed) | 0.00194 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 1587 | beam FWHM 5.85 kpc (radius 2.92) | 2.92 | beam | 2.3e+08 |  | 1.02e+11 | total (SED fit, as printed) | 0.00225 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 2768 | beam FWHM 2.18 kpc (radius 1.09) | 1.09 | beam | 1.8e+07 |  | 5.75e+10 | total (SED fit, as printed) | 0.000313 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N14 | NGC 5982 | beam FWHM 4.78 kpc (radius 2.39) | 2.39 | beam | 2.5e+07 | < | 8.13e+10 | total (SED fit, as printed) | <0.000308 | yes | yes | gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample |
| molecular | N13 | NGC4889 | beam FWHM 10.9 kpc (radius 5.45) | 5.45 | beam | 8.56e+08 | < | 7.65e+11 | total: L_Ks x 0.82 | <0.00112 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=16.3) = 0.233 |
| molecular | N13 | NGC2832 | beam FWHM 11.2 kpc (radius 5.60) | 5.60 | beam | 3.85e+08 | < | 6.22e+11 | total: L_Ks x 0.82 | <0.000619 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=10.8) = 0.328 |
| molecular | N13 | NGC4073 | beam FWHM 9.7 kpc (radius 4.85) | 4.85 | beam | 7.92e+08 | < | 5.67e+11 | total: L_Ks x 0.82 | <0.0014 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=10.2) = 0.308 |
| molecular | N13 | NGC3158 | beam FWHM 11.0 kpc (radius 5.50) | 5.50 | beam | 6.42e+08 | < | 5.42e+11 | total: L_Ks x 0.82 | <0.00119 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=8.1) = 0.396 |
| molecular | N13 | NGC4874 | beam FWHM 10.9 kpc (radius 5.45) | 5.45 | beam | 7.31e+08 | < | 4.94e+11 | total: L_Ks x 0.82 | <0.00148 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=15.8) = 0.239 |
| molecular | N13 | NGC0741 | beam FWHM 7.9 kpc (radius 3.95) | 3.95 | beam | 4.57e+08 | < | 4.51e+11 | total: L_Ks x 0.82 | <0.00101 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=9.6) = 0.276 |
| molecular | N13 | NGC0533 | beam FWHM 8.3 kpc (radius 4.15) | 4.15 | beam | 4.71e+08 | < | 4.4e+11 | total: L_Ks x 0.82 | <0.00107 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=15.3) = 0.195 |
| molecular | N13 | NGC0507 | beam FWHM 7.4 kpc (radius 3.70) | 3.70 | beam | 4.79e+08 | < | 3.92e+11 | total: L_Ks x 0.82 | <0.00122 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=13.0) = 0.203 |
| molecular | N13 | NGC7265 | beam FWHM 8.8 kpc (radius 4.40) | 4.40 | beam | 4.42e+08 | < | 3.92e+11 | total: L_Ks x 0.82 | <0.00113 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=12.7) = 0.240 |
| molecular | N13 | NGC0410 | beam FWHM 7.6 kpc (radius 3.80) | 3.80 | beam | 4.62e+08 | < | 3.84e+11 | total: L_Ks x 0.82 | <0.0012 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=10.9) = 0.241 |
| molecular | N13 | NGC2256 | beam FWHM 8.5 kpc (radius 4.25) | 4.25 | beam | 3.5e+08 | < | 3.75e+11 | total: L_Ks x 0.82 | <0.000934 | yes | yes | ML_K_assumed; optional scaling f(<R_beam; R_e=16.8) = 0.183 |

**Usable gas values without a stellar mass on a usable basis** (recorded, no ratio computed):

| Phase | Cand. | What | Radius class | Values (as printed) | Why no ratio |
|---|---|---|---|---|---|
| hot | C8 | NGC 4459, NGC 4526 (S0) | physical (R_max 9.3, 8.5 kpc) | 0.12 ± 0.02, 0.15 (+0.03/−0.02) × 10^9 | no stellar mass printed |
| molecular | C15 | 11 MASSIVE ETGs, ISM-selected | beam 21.3″ (5.6–9.8 kpc diameter) | 6 detections 10^9.02–10^9.49; 5 limits < 10^8.56–10^8.86 | M_K only; selected for ISM signs (gas-rich bound) |
| molecular | C16 | 5 CO discs + 2 limits | physical (CO disc outer radius 1.2–6.2 kpc) | 1.1–47 × 10^8 | L_B only; selected as CO-bright |
| molecular | C17 | 11 brightest SAURON E/S0 | beam 23″ (1.15–4.76 kpc diameter) | 2 detections (0.41, 3.69 × 10^8); 9 limits | M_B only |
| molecular | N17 | 3 detections of 15 | beam 22″ | 2.2 × 10^6 – 4.3 × 10^8 | no stellar mass; non-detections have no printed limit |
| molecular | N19 | 22 massive ellipticals / BCGs | physical (500 pc, ALMA) | ~10^5–10^9; e.g. NGC 4472 < 0.82 × 10^7 | stellar mass inside 500 pc not printed; 9 are cluster BCGs |
| atomic | C26 | NGC 4150 | physical (HI diameter 4 kpc, radius 2 kpc) | 2.5 × 10^6 | only M_HI/L_K = 0.00025 (a light ratio) |
| atomic | C27 | 15 SAURON ETGs (non-detections) | beam (one synthesised beam) | < 1.8 × 10^6 – < 1.2 × 10^7 | no stellar mass printed |

## 4. Per-phase distributions

### 4.1 Lens range (ranges only, from `adjudicated_inputs.csv` and the R7 r_Ein printed in the supplement)

**R_E** (kpc):

| Lenses | R_E (kpc) | Note |
|---|---|---|
| SLACS (n = 54) | 1.14–6.91, median 3.5 | R7's printed r_Ein |
| S4TM (n = 37) | 1.11–4.99, median 2.6 | computed with the frozen `einstein_radius_kpc` in R10's cosmology |
| SL2S | 4.85, 6.64 | |
| SNL-1 | 1.47 | printed |
| MaNGA | 3.71, 4.72 | printed |

**Stellar mass** (M⊙):
- SLACS M*(<R_E), Chabrier-BC03: 1.0 × 10^10 – 1.9 × 10^11 (median 6 × 10^10);
- SLACS totals: 3 × 10^10 – 4.3 × 10^11;
- S4TM totals: 5.5 × 10^10 – 1.2 × 10^12 (median 1.8 × 10^11);
- SL2S totals: 1.9 and 3.9 × 10^11;
- L × M/L masses inside the aperture (SNELLS, MNELLS, MaNGA): 6.9 × 10^10 – 2.0 × 10^11;
- NGC 6505: 1.06 × 10^11.

**Criterion, fixed before any ratio was computed.** A gas galaxy is "in the lens range" if its stellar mass is:
- in [1.0 × 10^10, 1.2 × 10^12] for a same-aperture mass (from the smallest lens M*(<R_E) to the largest lens total);
- in [3.0 × 10^10, 1.2 × 10^12] for a total.

It was fixed after the raw gas masses and luminosities had been seen during reconciliation. It excluded no row.

### 4.2 Distributions (gas mass / stellar mass in the stated radius)

"Median (limits at value)" counts each limit as if it were a detection at its limit; that is the upper bracket of the median. "Median (limits at 0)" is the lower bracket. No censored-data model is used.

| Group | N | Detections | Limits | Detected range | Limit range | Median (limits at value) | Median (limits at 0) |
|---|---|---|---|---|---|---|---|
| hot, N2 (same aperture, M*/L_K 0.8) | 17 | 14 | 3 | 0.000223–0.00215 | 0.0006–0.00125 | 0.000773 | 0.000702 |
| hot, N7 (same aperture 2 r_e, M*/L_K 0.82 assumed) | 11 | 11 | 0 | 0.000151–0.0254 | — | 0.00382 | 0.00382 |
| hot, N2 + N7 | 28 | 25 | 3 | 0.000151–0.0254 | 0.0006–0.00125 | 0.00119 | 0.00105 |
| molecular, N14 (beam / total M*) | 45 | 16 | 29 | 3.09e-05–0.07 | 0.000142–0.00277 | 0.000904 | 0 |
| molecular, N13 (beam / total M*, M*/L_K 0.82 assumed) | 11 | 0 | 11 | — | 0.000619–0.00148 | 0.00113 | 0 |
| molecular, N14 + N13 | 56 | 16 | 40 | 3.09e-05–0.07 | 0.000142–0.00277 | 0.001 | 0 |
| sens.: hot, radius <= 6.91 kpc (largest lens R_E) | 10 | 8 | 2 | 0.000223–0.00177 | 0.0006–0.00125 | 0.000696 | 0.00066 |
| sens.: hot, M* >= 1e11 | 11 | 11 | 0 | 0.000151–0.0254 | — | 0.00382 | 0.00382 |
| sens.: molecular, M* >= 1e11 | 28 | 6 | 22 | 0.00143–0.00548 | 0.000179–0.00148 | 0.00104 | 0 |

**Script notes (verbatim output):** N13 with optional de Vaucouleurs scaling to the beam radius: n=11, limits 0.00188–0.00618; Outside lens range: []; N2 incl. NGC 4552 (10.7 kpc): n=18 median(limits at value)=0.000774 max det=0.00298

The rows marked "sens." are sensitivities, not candidates for the default.

**Atomic (HI): no per-galaxy ratio can be computed.** No candidate prints an HI mass inside a stated radius together with a stellar mass on a usable basis. The atomic evidence consists of sample statements:

| Statement | Source | Read by |
|---|---|---|
| Central HI ("within one WSRT resolution element", ~35″ × 45″) detected in **15 ± 4 %** of high-mass ATLAS3D ETGs (log M_JAM > 10.7, 61 with HI data), and 19 ± 3 % of all 166 | N18 Table 3 | reader B |
| "red sequence galaxies have total ratios M(H I)/MJAM ⩽ 0.16, central M(H I)/MJAM ⩽ 0.01 and M(H2)/MJAM ⩽ 0.07" | N18 §4 | adjudicator, at source |
| Abstract: "massive red sequence early-type galaxies (stellar masses > 5×10^10 M⊙, derived from dynamical models) are found to have H I masses up to M(H I)/M⋆ ∼ 0.06 and H2 masses up to M(H2)/M⋆ ∼ 0.01" | N18 abstract | adjudicator, at source |
| In-beam HI limits < 1.8 × 10^6 – < 1.2 × 10^7 M⊙ for 15 SAURON ETGs | C27 | reader B, wording verified |
| Small "class d" discs < 10^8 M⊙ in total | C30 | both readers |

Note that **M_JAM is a dynamical mass**. Its denominator includes any non-stellar mass inside its radius, so a ratio to M_JAM is at most the ratio to M*. This is flagged `denominator_dynamical`.

### 4.3 What the distributions show (facts, then one inference)

1. **Hot gas** is detected in 25 of 28 same-aperture measurements. The fraction rises with stellar mass:
   - N2 (M* 1.2–7.3 × 10^10): median 0.077 %;
   - N7 brightest quarter (M*(<2 r_e) 1.3–2.9 × 10^11): median 0.38 %, maximum 2.5 % (NGC 5813).

   N2 prints its own sample average, "Mgas/M∗ = 8.0 × 10^−4" (§5), and the table reproduces it (0.077 %).
2. **N7's masses are upper bounds for their volume.** They come from "the average hot gas density from the best fit normalization" over a sphere of radius 2 r_e. For a fixed emission measure ∫n² dV over a volume V, the Cauchy–Schwarz inequality gives (∫n dV)² ≤ V ∫n² dV. A uniform density therefore gives the largest mass consistent with the measured emission. This is a mathematical property of the method, not a statement from N7.
3. **The sources disagree for the same galaxies.** C4 states that hot gas is "< 0.04% of the mass in stars" for NGC 4472, 4649 and 5846. N7 gives 0.79 %, 0.38 % and 1.0 % inside 2 r_e (with M*/L_K = 0.82). C4 states no radius, so the two cannot be reconciled from the text. The disagreement is a factor of about 10–26. It is reported, not resolved.
4. **Molecular gas is undetected in most massive ETGs.**
   - N14 + N13: 16 detections of 56.
   - In lens-mass galaxies (M* ≥ 10^11), 6 detections of 28, at most 0.55 % of total M*.
   - N13 prints a "molecular-to-stellar mass fraction of 0.1%" detection threshold (3σ) and 25 % detected.
   - N18's abstract gives "up to M(H2)/M⋆ ∼ 0.01" for massive red-sequence ETGs.
   - The highest detections in the pool (7 % of total M*, N14 NGC 940; N18's 0.076) are not from lens-mass red-sequence galaxies.
5. **Inference, labelled as such.** N2's own density model (β = 0.5, core radius 1 kpc) makes the enclosed gas mass grow faster with radius than the stellar mass. So hot-gas ratios measured inside R_m ≈ 4–9 kpc or 2 r_e ≈ 8–17 kpc are expected to *overstate* the ratio inside a lens R_E of 1–7 kpc. The size of this effect was **not computed**: it would need a scaling assumption. For molecular gas, N14 cites interferometric mapping (Davis et al. 2013): "CO is only observed in the central 4 kpc", and "only a handful of galaxies have CO extent >2 kpc". So beam masses are close to central masses. But the ratio to *total* M* understates the ratio inside the beam by 1/f(<R_beam). For N13, the optional de Vaucouleurs scaling (n = 4 with the printed R_e) turns the limits from < 0.06–0.15 % into < 0.19–0.62 %.

## 5. Options for the A6 gas term (fraction of M*(<R_E)); proposal only

Each option gives a default and a range per phase, with the evidence behind each number. The summed range adds the per-phase tops, which assumes all three maxima occur in the same galaxy; that makes it generous.

| Option | Hot: default [range] | Molecular: default [range] | Atomic: default [range] | Summed: default [range] |
|---|---|---|---|---|
| **G1 (recommended)** pooled same-aperture median; tops from printed maxima for massive red-sequence ETGs | **0.12 %** [0.015 %, 2.5 %] | **0** [0, 1 %] | **0** [0, 1 %] | **0.12 %** [0.015 %, 4.5 %] |
| G2 mass-matched (M* ≥ 10^11 only) | 0.38 % [0.015 %, 2.5 %] | 0 [0, 1 %] | 0 [0, 1 %] | 0.38 % [0.015 %, 4.5 %] |
| G3 upper bracket (each limit counted at its value) | 0.12 % [same] | 0.10 % [same] | no number | 0.22 % [same] |
| G4 G1 with the atomic phase declared unconstrained (no slider) | as G1 | as G1 | not quantified, shown as "not measured inside R_E" | 0.12 % [0.015 %, 3.5 %] |

**Evidence for each number:**
- **Hot 0.12 %.** Median of 28 same-aperture measurements (N2 17, N7 11; 25 detections, 3 limits). The median lies between 0.105 % (limits at 0) and 0.119 % (limits at value).
- **Hot 0.015 %.** The lowest measured value (N7 NGC 4494, 2.1 × 10^7 / 1.4 × 10^11). The data do **not** support zero for the hot phase: 25 of 28 are detected.
- **Hot 2.5 %.** The highest measured value (N7 NGC 5813, inside 2 r_e = 17 kpc). It is an upper bound by method (§4.3 item 2) and comes from a radius larger than any lens R_E.
- **Hot 0.38 % (G2).** Median of N7's 11 galaxies, the only same-aperture hot measurements at lens mass. It is biased high by method and aperture (§4.3 items 2 and 5).
- **Molecular 0.** 40 of 56 are limits, so the median is a non-detection (bracket 0 – 0.10 %). N13 prints that 75 % fall below a 0.1 % threshold.
- **Molecular 1 %.** N18 abstract, H2 "up to M(H2)/M⋆ ∼ 0.01" for massive red-sequence ETGs. The highest detection at M* ≥ 10^11 in this pool is 0.55 % of total M*. Scaled to the beam as in §4.3 item 5 (1/f ≈ 3–5.5 for N13's beams), that would be about 1.7–3 % inside the beam; this is an inference, not used.
- **Atomic 0.** Central HI is undetected in 85 % of high-mass ATLAS3D ETGs (N18 Table 3).
- **Atomic 1 %.** N18 §4, red-sequence central M(HI)/M_JAM ≤ 0.01, flagged `denominator_dynamical`. **The evidence cannot support a per-galaxy atomic distribution** (§4.2).

**How the options handle the required cases:**
- **Beams against physical radii.** A beam radius is half the printed FWHM, never the full diameter. Beam rows carry `beam_aperture`. Physical radii are used as printed. Neither kind is rescaled for the default. The de Vaucouleurs scaling is a sensitivity only (G1–G4 do not use it).
- **Radii larger than R_E.** No scaling. Values are used at their own radius, flagged `gas_radius_gt_RE`. The direction of the bias is stated (§4.3 item 5), and the default is checked against the subset inside the largest lens R_E: 10 hot rows with r ≤ 6.91 kpc give a median of 0.070 %, below the 0.12 % default.
- **Non-detections.** Limits stay limits. Medians are bracketed. Where the median is a non-detection, the default is zero.
- **A range from zero.** Molecular and atomic ranges start at 0, as the data allow. The hot range starts at the lowest measurement (0.015 %), because the data exclude zero. If JvH prefers a slider that starts at 0, 0.015 % can be marked on it.

**Recommendation: G1.**
- Its hot default comes from all same-aperture measurements. These are bracketed by a low-mass sample whose densities are modelled (N2) and a lens-mass sample whose masses are upper bounds (N7), so no single sample's bias sets the default.
- Its tops are printed values for massive red-sequence ETGs, which is the population closest to the lenses.
- It never rescales a radius.
- G2 is the honest alternative if JvH weights the mass match above the method bias. The difference (0.12 % against 0.38 % of M*(<R_E)) is shown on the slider in either case.

Under D-075 item 1 the result is registered as an assumption with a slider. The five systems with source-stated gas assumptions (R28, R25, R32) keep those quotes.

## 6. Salpeter top for S4TM (R10, FSPS) and SL2S (R20, BC03)

**SL2S needs no decision.** R20 Table 7 prints both Chabrier and Salpeter BC03 masses, and these are already in `adjudicated_inputs.csv` as default and "range top". That is precedence §3.2's first clause ("The Salpeter value printed by the same source sets the top"). The model-paper route is not needed, so BC03's "not printed" has no consequence.

**S4TM needs a ruling.**
- R10 takes its Chabrier masses from R9 (Shu et al. 2015), "SSP models obtained with the Flexible Stellar Population Synthesis (FSPS: Conroy et al. 2009; Conroy & Gunn 2010)". R9 shows Salpeter masses only in a figure (Fig. 9).
- Neither FSPS model paper prints a Chabrier-to-Salpeter ratio (both readers).
- So D-075 item 5's route ("otherwise the model paper's ratio, read at source") returns nothing, and a new choice is needed.

| Option | Factor (Salpeter / Chabrier) | Basis | Flag |
|---|---|---|---|
| **S-a (recommended)** R30's printed FSPS conversion | 1/0.61 = **1.64** | R30 §3.1: "to convert the stellar mass … from Chabrier (2003) to Salpeter (1955) IMFs, we can rescale these quantities by dividing them with a constant factor of 0.61". R30's fit uses "the Flexible Stellar Populations Synthesis (FSPS) code (Conroy et al. 2009; Conroy & Gunn 2010)": the same code and the same two model papers as R9. Differences: R30 uses a non-parametric SFH and MILES/MIST, where R9 uses a fixed SSP with t_form = 4 Gyr, and R30 prints no citation for 0.61 | `salpeter_top_from_other_source_same_model_family` |
| S-b R13's BC03 per-lens ratio | median 1.71 (range 1.53–1.88; integer-rounded masses, 48 lenses) | R13 prints Chabrier-BC03 and Salpeter-BC03 totals per lens | different model family (BC03, not FSPS) |
| S-c No IMF top for the 37 S4TM points | — | — | `no_imf_range`; the slider has no top for these points |
| S-d Digitise R9 Fig. 9 | — | not a reading of a printed value | rejected |

**Cross-checks** (reported, not used):
- R32 prints α ≈ 1.65 for Salpeter relative to Kroupa, with Conroy, Gunn & White 2009 models via EzGal (FSPS family, Kroupa reference);
- R29 prints α = 1.55, also relative to Kroupa;
- R13's BC03 ratio is 1.71.

S-a's 1.64 lies inside the 1.55–1.71 spread of the printed conversions.

**Recommendation: S-a.** It is a printed conversion for the same population-synthesis code. The flag records that it comes from another paper, and the spread of the other printed conversions is shown on the S4TM page. S-c is the strict alternative: it keeps the rule exactly as written, at the cost of an IMF range for 37 points. This changes how the Atlas measures, so it goes to the decision log after the ruling.

## 7. Answers to the readers' questions

1. **Beam as radius** (A-C Q2, B-C Q2, A-N Q2, B-N Q2). Yes, as a radius class of its own. The radius is half the printed FWHM. A rectangular region (C16's 22.5″ square) or an ellipse (WSRT) is kept as printed and classed `beam`; it is not used for ratios. The 10 kpc test applies to the radius (half the beam), not the diameter.
   - C14 §3.4 says most CARMA galaxies extend beyond the IRAM beam. C25 says the central pointing holds a median 57 % of the CO.
   - Beam masses are therefore lower limits on a galaxy's total CO, but close to the CO inside the beam radius.
   - N14 cites Davis et al. 2013 that CO sits within the central 2–4 kpc.
2. **N2 NGC 4552 at 10.7 kpc.** Excluded from the default, because the 10 kpc limit was set in the brief before reading. Shown as a sensitivity: with it, the N2 median is unchanged (0.077 %) and the N2 maximum rises from 0.22 % to 0.30 %.
3. **N6 at 5 R_e.** Not used. Computing a mass inside ≤ 2 R_e from the printed β-model parameters (β, r_c, ρ0) would be a model extrapolation (class `model-corrected`) and a reader-side computation. If JvH wants it, it should be a separate, logged step with its own check against a source that prints masses at small radius (N7 overlaps N6's sample). Recommendation: no.
4. **N4: plotted only.** Not used. Digitising Fig. 1 is not reading a printed value, and the source prints only the M_gas–T_X fit. Option: write to the authors for the per-galaxy M_gas(<10 kpc). Recommendation: not for v1.0.
5. **N20: model-corrected.** Classed `model-corrected`: the masses include a source/beam coupling factor from an exponential disc model (h = D_B/10). Not used. The sample is also radio-selected, and no stellar mass or L_K is printed.
6. **Extra labels.** Unified as `none_in_radius` (full text read, nothing qualifying) and `NS` (full text not reached). `catalogue_location` and `gas_total_no_radius` stay as in the brief. Whole-galaxy totals (N14, N15) stay as recorded and are not used. No per-galaxy transcription of totals is needed (B-C Q9: no).
7. **Other questions:**
   - **Brightest quarter.** C17 (A Q5, B Q5): the union of both selections, verified. C13 and C30 (A Q6, B Q6): no M_K is printed, so no selection; N13 and N18 cover the massive end, so ATLAS3D Paper I need not be read. N13 (A-N Q9): ties included; the agreed 17.
   - **C20.** Not refereed; dropped, as are C28 and C29 (beyond 10 kpc or gas-rich selected).
   - **C21's Mgas / M(H2) ambiguity.** Unresolved at source. Not used.
   - **C4.** No radius; recorded. It conflicts with N7 (§4.3 item 3).
   - **C8.** arXiv v1 only; values agree between readers. No stellar mass, so no ratio.
   - **N14b mixed beams** (A-N Q3). Where IRAM CO(2-1) supplied the larger mass, the beam may be half the listed one. The effect on the N14 ratios is none, because they are taken to total M*. Only the beam-radius label could be too large by up to a factor of 2. Flag `beam_may_be_CO21`.
   - **Gas-to-stellar ratios not taken in the same radius** (A-N Q11). N14b's and N18's printed ratios use total M*. They are quoted as sample statements, not as same-radius values.
   - **N18's M_JAM** is a dynamical denominator; flagged.
   - **N19's BCG names.** Kept as the host-cluster names printed; not mapped.
   - **N10's g_obs–g_bar figure.** Out of scope here; noted for JvH as a possible dynamics-channel source (no action taken).
   - **Exponent conventions and symmetric errors.** Accepted.
   - **C28 NGC 3108's three printings.** Not used (beyond 10 kpc).
   - **The six NS candidates.** Not retried. G1 rests on candidates already read.

## 8. Disclosures

**Values that rest on fewer than two readings:**
- R61's SNL-1 L_F814W 2.52 ± 0.04 and Υref 2.75: adjudicator only, outside the brief. They need a second reading.
- N7's 11 rows: reader A plus the adjudicator at source.
- C17 NGC 474 and NGC 1023, and C27's 15 limits: reader B plus the adjudicator (spot check).
- C21: reader A only. Not used.

**Not verified at source by the adjudicator** (both readers agree):
- R25 and R26 values;
- N14 stellar masses and gas values;
- N13 L_Ks and R_e;
- N2 values were verified; C8 values were not.

Everything was read from arXiv versions, except B's N14b VizieR table and the R7 IOP tables. R5's own R_e table was not opened.

**Assumptions introduced here, all flagged on the rows:**
- M*/L_K = 0.82 for N7 and N13 (`ML_K_assumed`), with 0.8 for N2 (its own value). C15 prints 1.0 for MASSIVE galaxies. Using 1.0 would lower the N7 and N13 ratios by 18 %.
- The lens-range criterion (§4.1).

**Blinding exposures** (seen while locating printed values; not recorded, not used, no ratio computed):
- The first 8 rows of R7 Table 4 were printed to the terminal while checking its layout. They include R7's f*,Ein columns, a stellar-to-lens mass fraction from R7's σ-prior alternative masses (D-063 item 3).
- R61 §5 text gives R61's lensing-based Υ_Rap and IMF-mismatch α for SNL-1 and SNL-2.
- A line of R32's table with an M_DM value.
- R9's qualitative §6 text on dark-matter fractions and the Salpeter IMF.

None of these is a value of the Atlas's g_obs/g_bar. They are disclosed because they relate to it.

**Deviations from the task as written:**
- Two scripts were added: `reading/build_adjudicated_supplement.py` and `reading/gas/adjudicate_gas.py`. They make the CSV and the tables reproducible, and they are not committed.
- R61 was read for the SNL-1 fallback, because the frozen ranking puts it before R26 and R25.

**Not done:**
- No decision was made.
- `decisions.md` was not edited.
- No reading was edited.
- Nothing was committed.

**Next step.** JvH rules on:
- the gas term (G1 recommended; G2 is the alternative);
- the S4TM Salpeter top (S-a recommended);
- the SNL-1 fallback rank (R61).

Then a second reader reads R61's two SNL-1 values, and the rulings go into the decision log.
