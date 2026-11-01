# aeg-d-strong-lensing/v1: result summary

Conversion run 2026-11-01 under D-063 to D-066, D-075 and D-076, with data standard 2.1.0. Status: **not shipped**, because test 1 fails (4 numbers; see "Tests").

## Counts per survey

Plotted points use printed lens redshifts z_l < 0.30 (D-066). Each plotted system has one default row (projected g_obs and g_bar at R_E). Alternatives are role = alternative rows and are never plotted.

| Survey (inventory scope) | Systems | Plotted | Recorded, not plotted | Alternative rows |
|---|---|---|---|---|
| SLACS (R5 observed, R13 stellar) | 54 | 48 | 6 | 48 (Maraston 2005 pair) |
| S4TM (R10) | 37 | 37 | 0 | 0 |
| SL2S (R20, redshifts R21) | 4 | 2 | 2 | 4 (ugriz-only fit; HST R_e) |
| SNELLS SNL-0 (R28 observed, R26 stellar) | 1 | 1 | 0 | 0 |
| SNELLS SNL-1 (R61; D-076 item 3) | 1 | 1 | 0 | 0 |
| SNELLS SNL-2 (R61) | 1 | 1 | 0 | 0 |
| MNELLS J0403−0239 (R29 matched pair) | 1 | 1 | 0 | 0 |
| MaNGA (R32) | 2 | 2 | 0 | 0 |
| NGC 6505 (R30) | 1 | 1 | 0 | 1 (z_l = 0.041) |
| CASTLES (R36) | 3 | 0 | 3 | 0 |
| **Total in the tables** | **105** | **94** | **11** | **53** |

**Reasons for the 11 recorded systems:**
- **SLACS (6).** Five are late-type at source (R5 Mph = L: J0841+3824, J0955+0101, J1032+5322, J1251−0208, J1432+6317) and one is unclassified (Mph = U: J1103+5322) (D-063 item 6). The inputs hold no θ_E for them.
- **SL2S (2).** SL2SJ221929−001743 is grade B and SL2SJ222012+010606 is grade C. Neither is a confirmed lens (D-063 item 5).
- **CASTLES (3).** Q2237+030 is late-type at source. MG1549+3047 and MG1654+1346 have no kind stated in the inputs. None of the three has a spectroscopic redshift pair in the inputs, an Einstein radius or mass in the inputs, or a stellar-mass default.

**Not in the tables (21; `checks/not_tabulated.csv`).** Data standard §10 item 7 requires a redshift for each tabulated system.
- FBQ0951+2635 (CASTLES): its lens redshift is a fundamental-plane estimate, not a measurement.
- 20 SLACS IX (R7) lenses outside the SLACS V adjudicated set. Their only inputs are R7's printed M_E (11 not printed). There is no θ_E, kind or redshift row, and SLACS IX new models have no stellar-mass default (REPRODUCTION.md).

## Tests (REPRODUCTION.md; details in SECOND_READING.md)

| Test | Result |
|---|---|
| 1. Second reading | **PASS** (version 3): 1111 of 1111. 1101 found in both readings; 10 adjudicated at source with the adjudication cited. Version 2 failed on 4 numbers, the printed errors of R32's R_E in kpc, which only reader A had recorded. An independent second reader then read R32 Table 1 and found the same values (`reading/readings/second-reader-r32.csv`). The version 2 output is kept as `checks/second_reading_v2.csv`. |
| 2. Transcription | PASS, 5927 of 5927 |
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
