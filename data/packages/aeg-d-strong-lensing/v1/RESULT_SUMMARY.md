# aeg-d-strong-lensing/v1: result summary

Conversion run 2026-11-01 under D-063 to D-066, D-075 and D-076, with data standard 2.1.0. Re-run 2026-11-01 to record the systems at z_l ≥ 0.30 (D-066 item 2). Status: not shipped (PR #94 open).

## Counts per survey

Plotted points use printed lens redshifts z_l < 0.30 (D-066). Each plotted system has one default row (projected g_obs and g_bar at R_E). Alternatives are role = alternative rows and are never plotted. Systems at printed z_l ≥ 0.30 are recorded in the systems table in full, not plotted, flagged `epoch_gap_v1` (D-066 item 2); they have no measurement row.

| Survey (inventory scope) | Systems | Plotted | Recorded, not plotted (z_l < 0.30) | Recorded, z_l ≥ 0.30 (epoch gap) | Alternative rows |
|---|---|---|---|---|---|
| SLACS (R5 observed, R13 stellar) | 63 | 48 | 6 | 9 | 48 (Maraston 2005 pair) |
| S4TM (R10) | 40 | 37 | 0 | 3 | 0 |
| SL2S (R20, redshifts R21; SL2S V added; R49 for SL2SJ02176−0513) | 58 | 2 | 2 | 54 | 4 (ugriz-only fit; HST R_e) |
| SNELLS SNL-0 (R28 observed, R26 stellar) | 1 | 1 | 0 | 0 | 0 |
| SNELLS SNL-1 (R61; D-076 item 3) | 1 | 1 | 0 | 0 | 0 |
| SNELLS SNL-2 (R61) | 1 | 1 | 0 | 0 | 0 |
| MNELLS J0403−0239 (R29 matched pair) | 1 | 1 | 0 | 0 | 0 |
| MaNGA (R32) | 2 | 2 | 0 | 0 | 0 |
| NGC 6505 (R30) | 1 | 1 | 0 | 0 | 1 (z_l = 0.041) |
| CASTLES (R36) | 24 | 0 | 3 | 21 | 0 |
| SuGOHI CMASS (R57) | 17 | 0 | 0 | 17 | 0 |
| Cosmic Horseshoe | 1 | 0 | 0 | 1 | 0 |
| KiDS J0233−3447 | 1 | 0 | 0 | 1 | 0 |
| J0100+1818 | 1 | 0 | 0 | 1 | 0 |
| **Total in the tables** | **212** | **94** | **11** | **107** | **53** |

Six SuGOHI lenses are also SL2S lenses (same coordinates): SL2SJ021411−040502, J021737−051329, J022346−053418, J022610−042011, J023307−043838 and J220506+014703. Each is one system, counted under SL2S, with both surveys' readings in its properties. Five of the six have redshifts printed differently by the two sources (flag `sources_differ`).

**Reasons for the 11 recorded systems below the cut:**
- **SLACS (6).** Five are late-type at source (R5 Mph = L: J0841+3824, J0955+0101, J1032+5322, J1251−0208, J1432+6317) and one is unclassified (Mph = U: J1103+5322) (D-063 item 6). The inputs hold no θ_E for them.
- **SL2S (2).** SL2SJ221929−001743 is grade B and SL2SJ222012+010606 is grade C. Neither is a confirmed lens (D-063 item 5).
- **CASTLES (3).** Q2237+030 is late-type at source. MG1549+3047 and MG1654+1346 have no kind stated in the inputs. None of the three has a spectroscopic redshift pair in the inputs, an Einstein radius or mass in the inputs, or a stellar-mass default.

**The 107 epoch-gap systems (D-066 item 2).** Recorded from the two independent readings (`reading/readings/reader-{a,b}-block{1,2,3}.csv`), not adjudicated. Each row carries its identifiers, z_l and z_s, their measurement methods, its kind as read, `plotted: false`, the reason "z_l ≥ 0.30 (D-066)" and the flag `epoch_gap_v1`. No other plotting condition was evaluated for them.
- **Readers agree on everything: 48.** The values are used as recorded.
- **Readers differ: 59** (flag `readers_differ`). Both readings are recorded in properties; nothing was chosen between them. 58 differ on the kind, 11 on z_l, 9 on z_s, 10 on the z_l method and 5 on the z_s method (a system can differ on several). Most differences are wording, or values that only one reader recorded: reader B read the 1998 CASTLES paper only, so the 2000 paper's values have one reading. They are listed in SECOND_READING.md. Where the kind readings differ, the kind is `A7` (ambiguous, not adjudicated).
- **Redshift column.** It holds the printed z_l where every reading agrees on one value. Otherwise it holds the lowest printed value, so the D-066 test holds for every reading. All values are in properties (`z_l_all_readings`, `z_s_all_readings`). z_s is left empty where readings differ.

**Not in the tables (33; `checks/not_tabulated.csv`).** Data standard §10 item 7 requires a redshift for each tabulated system.
- FBQ0951+2635 (CASTLES): its lens redshift is a fundamental-plane estimate, not a measurement.
- 9 more CASTLES lenses whose only printed lens redshift is an estimate (fundamental-plane or image-separation): B1127+385, BRI0952−0115, FSC10214+472, HE1104−1805, HE2149−2745, HST12531−2914, LBQS1009−025, Q1017−207, SBS1520+530.
- 3 SL2S III lenses with no lens redshift printed: SL2SJ140533+550231, SL2SJ141917+511729, SL2SJ142321+572243.
- 20 SLACS IX (R7) lenses outside the SLACS V adjudicated set. Their only inputs are R7's printed M_E (11 not printed). There is no θ_E, kind or redshift row, and SLACS IX new models have no stellar-mass default (REPRODUCTION.md).

## Tests (REPRODUCTION.md; details in SECOND_READING.md)

| Test | Result |
|---|---|
| 1. Second reading | **PASS** (version 4): 1497 of 1497. 1451 found in both readings; 10 adjudicated at source with the adjudication cited; 36 epoch-gap numbers found in one reading only, on systems flagged `readers_differ` with both readings recorded. Version 4 adds the 386 epoch-gap numbers (D-066). Version 3 passed 1111 of 1111 (`checks/second_reading_v3.csv`). Version 2 failed on 4 numbers, the printed errors of R32's R_E in kpc, which only reader A had recorded. An independent second reader then read R32 Table 1 and found the same values (`reading/readings/second-reader-r32.csv`). The version 2 output is kept as `checks/second_reading_v2.csv`. |
| 2. Transcription | PASS (version 3), 8503 of 8503. Version 3 adds the systems table: every column read back equals the row built in memory, and each reader's z_l and z_s for each epoch-gap system equal that reader's file. Version 2 passed 5927 of 5927 (`checks/transcription_v2.csv`). |
| 3. Arithmetic | PASS, 1178 recomputations to 10⁻⁹, including the L × Υ products, the profile step and the gas term |
| 4. Code (pytest) | PASS, 197 tests (pipeline suite, including the frozen `test_lensing.py` and 26 converter tests) |
| Released files (in `convert.py`) | 972 of 972 tier-1 numbers found in the hash-verified VizieR and IOP files |
| Slider formulas (`aeg.formula_check`) | passed; Python and JavaScript agree, with identity at the defaults |

Test scripts with disclosed version-2 fixes: test 1 (record-level lookup) and test 2 (empty unit). The first-run outputs are kept in `checks/*_v1.csv`. One converter defect was found by the first run of test 1 and fixed: R26's 2.2″ spectroscopic aperture had been packaged as an alternative Einstein radius.

## Reported checks (not pass/fail)

**§2.4 formula check** (`checks/formula_check.ecsv`). The table below gives the ratio of M_E computed from the printed θ_E with the frozen formula, in the source's cosmology, to the printed M_E.

| Printed M_E from | θ_E from | N | min | median | max | mean | SD |
|---|---|---|---|---|---|---|---|
| R7 (SLACS IX) | R5 (SLACS V) | 48 | 0.983 | 1.000 | 1.020 | 1.001 | 0.008 |
| R10 (S4TM) | R10 | 37 | 0.983 | 1.003 | 1.021 | 1.001 | 0.009 |
| R28 (SNL-0) | R28 | 1 | 0.969 | | | | |
| R29 (J0403−0239) | R29 | 1 | 0.998 | | | | |
| R30 (NGC 6505) | R30 | 1 | 1.010 | | | | |

- The printed M_E values are rounded to 0.01 dex (R7, R10).
- R32 is not checked, because its cosmology is named but its numbers are not printed (D-075 item 4).
- For SNL-0, the printed M_E is from the MFL model, while the θ_E is that of the SIS(+shear) model (adjudication.md §2).

**D-075 item 5 profile-step check on SLACS** (`checks/profile_step.ecsv`). The profile step (R13 total × the de Vaucouleurs fraction inside θ_E from R13's printed θ_e) is compared with R13's printed mass inside R_E. The ratio is computed over printed.

| IMF (BC03) | N | min | median | max | mean | SD | within ±10% |
|---|---|---|---|---|---|---|---|
| Chabrier | 48 | 0.936 | 1.002 | 1.127 | 1.009 | 0.045 | 46 |
| Salpeter | 48 | 0.898 | 0.992 | 1.045 | 0.993 | 0.027 | 47 |

R13 prints its masses as integers in units of 10¹⁰ M⊙, so part of the spread is rounding. This is the check D-075 item 5 asks to show on the S4TM and SL2S pages.

**Overlap** (`checks/overlap.csv`): no system is in more than one survey's default.

## Flagged (default rows)

| Flag | Systems | Meaning |
|---|---|---|
| `sample_level_error` | SLACS 48 | θ_E error is R5's survey-wide 2% (D-075 item 4) |
| `fallback_record` | J0946+1006, J1538+5817, J0403−0239, SNL-1 | next-ranked record is the default (D-075 item 2; D-076 item 3) |
| `mstar_in_RE_from_profile` | S4TM 37, SL2S 2 | printed total × the source's own light-profile fraction |
| `profile_differs_from_mass_photometry` | S4TM 37 | R10's de Vaucouleurs fit, not the photometry of R9's masses (D-075 item 5) |
| `salpeter_top_from_other_source_same_model_family` | S4TM 37 | IMF top from R30's printed FSPS factor (÷ 0.61; D-076 item 2) |
| `imf_top_not_read` | SNL-0, SNL-1, SNL-2 | no Salpeter value or conversion read; these rows have no IMF slider |
| `salpeter_factor_approx_printed` | J1436+4943, J1701+3722 | R32 prints α ≈ 1.65 |
| `mstar_from_L_times_ML` | SNELLS 3, J0403−0239, MaNGA 2 | stellar mass computed as L × Υ (D-075 item 3) |
| `model_dependence_half_image_separation` (model_dependence = total_mass_form) | SNL-1, SNL-2, J0403−0239 | R_E is half the image separation (D-063 item 2) |
| `aperture_as_RE_half_image_separation` | SNL-1, SNL-2 | R61's R_ap taken as R_E (D-075 item 3) |
| `no_uncertainty` (core) | S4TM 37, NGC 6505, SNL-1, SNL-2 | an input has no printed error (S4TM M_E and M*; NGC 6505 M_E; R61 Υ_ref) |
| `R_E_printed_kpc`, `cosmology_named_only` | MaNGA 2 | R32 prints R_E in kpc and names Planck 2018 without numbers |
| `cosmology_by_reference` | SNL-0 | R26 adopts R25's distances |
| `flatness_not_stated` | NGC 6505 | R30 prints H0 and Ω_m only |
| `gas_negligible_source_assumption` | SNL-0, SNL-1, SNL-2, J1436+4943, J1701+3722 | the source states gas negligible; the registered term applies (D-076 item 1) |
| `flat_from_omega_lambda` | all others | Ω_Λ = 1 − Ω_m as printed (D-075 item 4) |

**Gas.** Every default row carries the registered term a6s_gas_in_RE (D-076 item 1): hot 0.12% of M*(<R_E) (range 0.015–2.5%) and cold 0 (range 0–2%). Both are on a slider.

**IMF slider.** 91 of the 94 plotted rows have a Salpeter top; the three SNELLS rows do not.

**Site.** The site builds and `aeg.site_check` passes. The map does not yet give projected points their own mark, which D-064 item 3 requires before these points appear beside 3D values.


## Test 1 version 5 and test 2 version 4 (2026-11-01)

- **Test 1 v4 weakened the test, and that is reversed.** Version 4 let 36 epoch-gap redshifts, each found in one reading only, pass under a new outcome `readers_differ`. Version 5 removes that outcome. An independent second reading of those redshifts (`reading/readings/second-reader-epoch-gap-z.csv`: Kochanek et al. 2000 Table 5, Keeton, Kochanek & Falco 1998, Dye et al. 2008, Spiniello et al. 2011, SL2S IV, SuGOHI III) supplies the missing reader. The version 4 output is kept as `checks/second_reading_v4.csv`.
- **Version 5 found one converter defect, now fixed.** The photometric redshift of a second lensed source of SL2SJ021737−051329 (Tu et al. 2009 Table 1, "Double system", z ≈ 2.9) had been merged into that lens's source-redshift readings. The converter now leaves out rows whose table location names a second source, and test 2 v4 applies the same rule (version 3 output kept).
- **Results:** test 1 v5 PASS, 1496 of 1496; test 2 v4 PASS, 8503 of 8503; test 3 passes; pytest 197 pass.
