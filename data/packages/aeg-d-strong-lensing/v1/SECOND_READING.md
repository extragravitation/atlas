# aeg-d-strong-lensing/v1: second reading and reproduction tests

Run 2026-11-01; re-run 2026-11-01 for the systems at z_l ≥ 0.30 (D-066 item 2). Method in `REPRODUCTION.md` (frozen, D-065); readings and adjudication in `reading/`. Claude (Anthropic, Claude Opus 5.5) wrote the conversion and the test scripts and ran them; AI assistance is disclosed. JvH has not reviewed this run.

## Result

| Test | Result |
|---|---|
| 1. Second reading against the sources | **PASS (version 4): 1497 of 1497** packaged numbers pass: 1451 found in both readings, 10 adjudicated at source with the adjudication cited, and 36 epoch-gap numbers found in one reading only, on systems flagged `readers_differ` (below). `checks/second_reading.csv`. Earlier versions: v3 PASS 1111 of 1111 (`checks/second_reading_v3.csv`); v2 FAIL 1107 of 1111 (kept on record below). |
| 2. Transcription | **PASS (version 3):** 8503 of 8503 table values equal the readings (`checks/transcription.csv`). Version 2: 5927 of 5927 (`checks/transcription_v2.csv`). |
| 3. Arithmetic integrity | **PASS:** 1178 recomputations from the stored columns agree to 10⁻⁹, in memory and again on the table read back (run inside `convert.py`). They cover M_E where computed, R_E, the L × Υ products, f(<R_E), M*(<R_E), g_obs, g_bar_stars, each gas component and g_bar. |
| 4. Code | **PASS:** `pipeline/tests/test_lensing.py` (frozen) and the full pipeline suite, 197 passed; the converter's own synthetic tests (`pipeline/tests/test_a6_convert.py`, 26) are part of it. |

Under REPRODUCTION.md, the package passes only if tests 1–4 all hold. **Test 1, version 2, failed** on 4 numbers, and that failure stays on record here. The test was not changed. The 4 numbers were R32's R_E errors in kpc, which only reader A had recorded. An independent second reader then read R32 Table 1 (`reading/readings/second-reader-r32.csv`) and found the same values: ±0.09 kpc and ±0.37 kpc.
- **Test 1, version 3**, adds that reading and nothing else: **PASS, 1111 of 1111.**
- The version 2 output is kept as `checks/second_reading_v2.csv`.

### The 4 numbers that fail test 1

They are the printed errors of R32's Einstein radius in kpc (Smith et al. 2020, Table 1, row R_Ein):

| System | Value | Reader A | Reader B |
|---|---|---|---|
| J1436+4943 | 4.72 ± **0.09** kpc | 4.72, 0.09, 0.09 | "R_Ein = 4.72 kpc (theta_Ein)", no error recorded |
| J1701+3722 | 3.71 ± **0.37** kpc | 3.71, 0.37, 0.37 | "R_Ein = 3.71 kpc (theta_Ein)", no error recorded |

- The adjudicated rows record "both readers agree (scope spelling differs)", which is true of the values but not of the errors.
- The adjudication table (`reading/adjudication.md` §4) prints "4.72 ± 0.09 kpc" and "3.71 ± 0.37 kpc", but no settlement at source is recorded for the errors. The test's rule, written before it was run, accepts a one-reader number only where the adjudicated row says it was settled or verified at source.
- **What these numbers do.** They are stored as the errors of the `einstein_radius` observables of the two MaNGA lenses. They do not enter g_obs, g_bar or their errors: R_E is the coordinate, and errors are carried at fixed R_E (REPRODUCTION.md, Uncertainties).
- **Next step:** a targeted re-read of R32 Table 1 (R_Ein errors) by reader B or by JvH. Then test 1 is run again, and the re-read is recorded, as was done for aeg-d-dwarfs/v1.

## How test 1 was run

- **Packaged numbers.** These are every number of every adjudicated row that enters the tables (the observables: value and printed errors). They also include the numbers that enter only measurement columns: H0 and Ω_m of each observed-side record, and the printed Salpeter conversions used for the IMF top (R29 α = 1.55, R32 α ≈ 1.65, R30 ÷ 0.61).
- **Readings.**
  - Readers A and B: `reading/readings/reader-{a,b}-{block1,block2,block3,supplement}.csv`. They read independently, in separate folders, without the conversion code.
  - SNL-1's R61 values (L_F814W 2.52 ± 0.04 × 10¹⁰ L⊙ inside 2.38″; Υ_ref 2.75, Kroupa, no printed error): the adjudicator read these at source (`reading/gas/adjudication_gas.md` §1), and a further second reader confirmed them (`reading/readings/second-reader-r61-snl1.csv`; D-076 item 3).
- **Matching.** A number counts as found in a reading if it is among the values and errors that reader recorded for the same record and system. It may appear as printed or in base units after the reader's own unit scaling. Matching is by record and system, not by quantity name, because the readers named some quantities differently. This is a limitation: a number could in principle match another quantity of the same system and record.

**Adjudicated at source (10 numbers).** Each is settled in `reading/adjudication.md` §2:
- J0403−0239 (R29): M_E error 0.4. "adopted error 0.4 (statistical 0.23)"; both readers recorded 0.23.
- J0403−0239 (R29): z_l 0.06569 and z_s 0.19130. One-reader extras (A), verified at source.
- NGC 6505 (R30): θ_E errors ±0.001. B missed the printed error.
- NGC 6505 (R30): M_E 1.53 × 10¹¹ and the alternative z_l 0.041 ± 0.001. One-reader extras (A), verified at source.

**Script versions (disclosed).**
- **Test 1, version 2.** The first run is kept in `checks/second_reading_v1.csv`: 1109 of 1115. It contained one script defect and one converter defect.
  - *Script defect:* a record-level number (a printed Salpeter conversion) was looked up only under the readers' "(record)" rows. Reader A had filed the conversions under the systems they apply to. Version 2 looks such numbers up among all of that reader's rows for the record. R29 α = 1.55, R30 0.61 and R32 1.65 are now found in both readings.
  - *Converter defect:* R26's 2.2″ spectroscopic (M/L) aperture for SNL-1, an alternative record, had been packaged as an alternative `einstein_radius` observable. It is not an Einstein radius. `convert.py` now keeps apertures of stellar-side alternatives in the alternative's note only. That removed 4 alternative observables (630, not 634). No default value, g_obs or g_bar changed.
  - The 4 R32 failures are the same in both runs.
- **Test 1, version 4** and **test 2, version 3** add the epoch-gap systems (section below). Earlier outputs are kept as `checks/second_reading_v3.csv` and `checks/transcription_v2.csv`.
- **Test 2, version 2.** The first run is kept in `checks/transcription_v1.csv`: 5736 of 5927. One script defect: an empty text cell reads back as None, so the 191 dimensionless redshift rows (unit "") were counted as unequal. No value changed.

## Epoch-gap systems (D-066 item 2)

D-066 item 2 records every system at printed z_l ≥ 0.30 in full, flagged `epoch_gap_v1`. The adjudication (`reading/adjudication.md`) covered only the systems below 0.30, so `convert.py` now records the others straight from the two independent readings (`reading/readings/reader-{a,b}-block{1,2,3}.csv`). **Nothing in this section was adjudicated.**

**Rules (in `convert.py`).** Disclosure: they were written after looking at the readers' z_l, z_s, kind and method rows for these lenses. They choose no value between the readers.
- **One lens, one system.** Readers' names are matched after removing spaces, dashes, plus signs and the SDSS prefix, on the part before any parenthesis. 12-digit J designations are matched on the coordinates alone, so a lens read in SL2S and in SuGOHI is one system. Four spellings are joined by an explicit alias list (`LENS_ALIASES`: SDSS J0100+1818, the Cosmic Horseshoe, SL2SJ02176−0513, and the two MaNGA lenses already in the tables).
- **z_l.** Only measured values count. A z_l row marked as an estimate (fundamental-plane z_FP, or estimated from the image separation) is kept in properties as `z_l_estimates` and not used. A lens with no measured z_l is not tabulated (`checks/not_tabulated.csv`), as FBQ0951+2635 already was.
- **Compared per scope and reader:** the sets of z_l and z_s values; the method classes of z_l and z_s (the earliest of "not measured", "not stated", "tentative", "estimate", "photometric", "spectroscopic" in the reader's text; the full texts are kept); and the kind. Kinds agree when the texts are identical, or when both readers recorded the same printed code (R5 Mph, R10 class code).
- **Agree:** the value is used. **Differ** (including one reader recording a value the other did not): both readings are recorded in properties and the system is flagged `readers_differ`. A kind on which the readers differ becomes `A7` (ambiguous, not adjudicated).
- **Redshift column:** the value where every reading agrees; otherwise the lowest printed value, so the D-066 test holds for every reading. All readings are in properties. Where scopes (sources) print different values for one lens, the flag is `sources_differ`.

**Result.** 107 systems recorded (SLACS 9, S4TM 3, SL2S 54, CASTLES 21, SuGOHI 17, Cosmic Horseshoe 1, KiDS J0233−3447 1, J0100+1818 1). 48 have both readers in full agreement. 59 are flagged `readers_differ`, 5 also `sources_differ`. 12 more lenses are added to `checks/not_tabulated.csv` (9 CASTLES with estimates only, 3 SL2S with no printed z_l). No lens below z_l = 0.30 was found in the readings outside the adjudicated inputs (`convert.py` stops if one is).

**Where the readers differ.** Most kind differences are wording. Reader B read only the 1998 CASTLES paper (Keeton, Kochanek & Falco), so values from the 2000 paper (Kochanek et al.) have one reading. These rows need a second reading, or an adjudication at source, before they can be called settled. Method columns show the method class.

| System | Scope | Quantity | Reader A | Reader B | Difference |
|---|---|---|---|---|---|
| 0047-2808 | CASTLES lenses | z_l | 0.48 | – | only reader A recorded it |
| 0047-2808 | CASTLES lenses | z_s | 3.6 | – | only reader A recorded it |
| 0047-2808 | CASTLES lenses | z_l_method | not stated | – | only reader A recorded it |
| 0047-2808 | CASTLES lenses | kind | no per-system statement; sample described as early-type | – | only reader A recorded it |
| B0218+357 | CASTLES lenses | kind | spiral (Sa colour; HI and molecular gas) | spiral (Sa-like colour, HI) | values differ |
| B0712+472 | CASTLES lenses | z_s | 1.33; 1.34 | 1.33 | values differ |
| B0712+472 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type; no per-system statement; sample described as early-type | sample-level only: most lens galaxies early-type, a few spirals | values differ |
| B1030+071 | CASTLES lenses | z_l | 0.6 | – | only reader A recorded it |
| B1030+071 | CASTLES lenses | z_s | 1.54 | – | only reader A recorded it |
| B1030+071 | CASTLES lenses | z_l_method | not stated | – | only reader A recorded it |
| B1030+071 | CASTLES lenses | kind | no per-system statement; sample described as early-type | – | only reader A recorded it |
| B1422+231 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type; no per-system statement; sample described as early-type | galaxy in a small group | values differ |
| B1600+434 | CASTLES lenses | kind | late-type | late-type per R36 2000 paper; ambiguous in 1998 | values differ |
| B1608+656 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type; no per-system statement; sample described as early-type | colours more consistent with spiral models; luminosity fits early-type correlation | values differ |
| B1933+503 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type | colours more consistent with spiral models; luminosity fits early-type correlation | values differ |
| B1938+666 | CASTLES lenses | z_l | 0.88 | – | only reader A recorded it |
| B1938+666 | CASTLES lenses | z_l_method | not stated | – | only reader A recorded it |
| B1938+666 | CASTLES lenses | kind | no per-system statement; sample described as early-type | – | only reader A recorded it |
| B2045+265 | CASTLES lenses | z_l | 0.87 | – | only reader A recorded it |
| B2045+265 | CASTLES lenses | z_s | 1.28 | – | only reader A recorded it |
| B2045+265 | CASTLES lenses | z_l_method | not stated | – | only reader A recorded it |
| B2045+265 | CASTLES lenses | kind | no per-system statement; sample described as early-type | – | only reader A recorded it |
| B2319+052 | CASTLES lenses | z_l | 0.62 | – | only reader A recorded it |
| B2319+052 | CASTLES lenses | z_l_method | not stated | – | only reader A recorded it |
| B2319+052 | CASTLES lenses | kind | no per-system statement; sample described as early-type | – | only reader A recorded it |
| HST14113+521 | CASTLES lenses | z_l | 0.46 | – | only reader A recorded it |
| HST14113+521 | CASTLES lenses | z_s | 2.81 | – | only reader A recorded it |
| HST14113+521 | CASTLES lenses | z_l_method | not stated | – | only reader A recorded it |
| HST14113+521 | CASTLES lenses | kind | no per-system statement; sample described as early-type | – | only reader A recorded it |
| HST14176+5226 | CASTLES lenses | z_s_method | tentative | not stated | values differ |
| HST14176+5226 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type; no per-system statement; sample described as early-type | sample-level only: most lens galaxies early-type, a few spirals | values differ |
| MG0414+0534 | CASTLES lenses | z_l | 0.96 | – | only reader A recorded it |
| MG0414+0534 | CASTLES lenses | z_l_method | estimate; not stated | estimate | values differ |
| MG0414+0534 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type; no per-system statement; sample described as early-type | sample-level only: most lens galaxies early-type, a few spirals | values differ |
| MG0751+2716 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type | galaxy in a small group | values differ |
| MG1131+0456 | CASTLES lenses | z_l | 0.84 | – | only reader A recorded it |
| MG1131+0456 | CASTLES lenses | z_l_method | not stated | – | only reader A recorded it |
| MG1131+0456 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type; no per-system statement; sample described as early-type | sample-level only: most lens galaxies early-type, a few spirals | values differ |
| MG2016+112 | CASTLES lenses | z_l | 1.01 | – | only reader A recorded it |
| MG2016+112 | CASTLES lenses | z_s | 3.27 | – | only reader A recorded it |
| MG2016+112 | CASTLES lenses | z_l_method | not stated | – | only reader A recorded it |
| MG2016+112 | CASTLES lenses | kind | two lens galaxies at different redshifts (KKF98) | – | only reader A recorded it |
| PG1115+080 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type; no per-system statement; sample described as early-type | galaxy in a small group | values differ |
| Q0142-100 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type; no per-system statement; sample described as early-type | sample-level only: most lens galaxies early-type, a few spirals | values differ |
| Q0957+561 | CASTLES lenses | kind | no per-system statement; sample described as mostly early-type; no per-system statement; sample described as early-type | galaxy in a cluster | values differ |
| RXJ0911+0551 | CASTLES lenses | z_l | 0.77 | – | only reader A recorded it |
| RXJ0911+0551 | CASTLES lenses | z_s | 2.8 | – | only reader A recorded it |
| RXJ0911+0551 | CASTLES lenses | z_l_method | not stated | – | only reader A recorded it |
| RXJ0911+0551 | CASTLES lenses | kind | no per-system statement; sample described as early-type | – | only reader A recorded it |
| SDSS J1148+1930 | Cosmic Horseshoe | z_l | 0.44; 0.444 | 0.44 | values differ |
| SDSS J1148+1930 | Cosmic Horseshoe | z_s | 2.38; 2.38115 | 2.38 | values differ |
| SDSS J1148+1930 | Cosmic Horseshoe | kind | LRG in a galaxy group; massive early-type galaxy | Luminous Red Galaxy in a group or loose cluster; title prints "J1004+4112" | values differ |
| SDSS J0100+1818 | J0100+1818 (A7) | kind | ultra-massive early-type galaxy; candidate fossil system / group | ultra-massive early-type galaxy / elliptical; candidate fossil group | values differ |
| KIDSJ0233-3447 | KiDS J0233-3447 | kind | early-type (elliptical) | early-type galaxy (ETG); massive elliptical | values differ |
| SL2SJ021411-040502 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| SL2SJ021737-051329 | SL2SJ02176-0513 | z_s | 1.85; 1.847; 2.9 | 1.85; 1.847 | values differ |
| SL2SJ021737-051329 | SL2SJ02176-0513 | z_s_method | photometric; spectroscopic | spectroscopic | values differ |
| SL2SJ021737-051329 | SL2SJ02176-0513 | kind | early-type (sample statement); elliptical; galaxy lens in a group environment | early-type (sample statement); cusp configuration; elliptical lens; massive early-type galaxy ~400 kpc from a galaxy-group centre | values differ |
| SL2SJ021737-051329 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| SL2SJ021801-080247 | SL2S III sample | kind | early-type (sample statement); upgraded to grade A | early-type (sample statement) | values differ |
| SL2SJ022046-094927 | SL2S III sample | z_s_method | not measured; spectroscopic | not measured | values differ |
| SL2SJ022046-094927 | SL2S III sample | kind | early-type (sample statement); upgraded to grade A | early-type (sample statement) | values differ |
| SL2SJ022346-053418 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| SL2SJ022610-042011 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| SL2SJ022648-040610 | SL2S III sample | kind | early-type (sample statement); disky | early-type (sample statement); Table 6 note: disky | values differ |
| SL2SJ084934-043352 | SL2S III sample | kind | early-type (sample statement) | early-type (sample statement); Table 6 note: Fixed PA | values differ |
| SL2SJ085019-034710 | SL2S III sample | kind | early-type (sample statement); disky; disk galaxy | disk galaxy | values differ |
| SL2SJ142003+523137 | SL2S III sample | kind | early-type (sample statement); disky; disk galaxy | disk galaxy | values differ |
| SL2SJ142731+551645 | SL2S III sample | kind | early-type (sample statement); disky; disky galaxy | disky galaxy | values differ |
| SL2SJ220506+014703 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| SL2SJ221326-000946 | SL2S III sample | kind | early-type (sample statement); disky; disky lens | disky lens | values differ |
| SL2SJ221407-180712 | SL2S III sample | kind | early-type (sample statement) | early-type (sample statement); Table 6 note: Fixed PA | values differ |
| SL2SJ020457-110309 | SL2S V added | kind | early-type (sample statement); early-type galaxy | early-type | values differ |
| SL2SJ022708-065445 | SL2S V added | z_s_method | – | not measured | only reader B recorded it |
| SL2SJ022708-065445 | SL2S V added | kind | early-type (sample statement); disky early-type galaxy | early-type; disky | values differ |
| SL2SJ023307-043838 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| SL2SJ085317-020312 | SL2S V added | z_s_method | – | not measured | only reader B recorded it |
| HSCJ015618-010747 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ020241-064611 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ023817-054555 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ085855-010208 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ094427-014742 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ120623+001507 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ121052-011905 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ121504+004726 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ140929-011410 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ141300-012608 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ141815+015832 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ142449-005321 | SuGOHI CMASS lenses | kind | most probable brightest galaxy of a rich cluster | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ142720+001916 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ144307-004056 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ222801+012805 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ223733+005015 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |
| HSCJ230335+003703 | SuGOHI CMASS lenses | kind | massive CMASS galaxy; no per-system morphology printed | BOSS CMASS galaxy (sample-level morphology: keywords "elliptical and lenticular, cD") | values differ |

**Next step for these rows:** a second reading of Kochanek et al. (2000) Table 5 for the CASTLES lenses that reader B did not read, and an adjudication of the kind for the SuGOHI and SL2S lenses, if JvH wants the epoch-gap kinds settled before release.

## Released files (additional check, run inside `convert.py`)

- Every tier-1 number used is found in its system's row of the released file, hash-verified by `aeg.fetch`: **972 of 972** (`checks/released_files.csv`).
  - VizieR J/ApJ/682/964 tables 4–5 (SLACS V);
  - VizieR J/A+A/501/461 (R13);
  - IOP tables of R10 (S4TM) and R20 (SL2S III).
- A fresh VizieR export differs in its raw bytes (request time) but matched the recorded content hash (2026-11-01).

## Reported, not pass/fail

See `RESULT_SUMMARY.md` for the summary statistics.
- §2.4 formula check: `checks/formula_check.ecsv`.
- D-075 item 5 profile-step check: `checks/profile_step.ecsv`.
- Overlap between surveys: `checks/overlap.csv`, none.

## Disclosure

While building the released-file check, the converter's author saw a few rows of R7 Table 4 in the terminal. These included R7's f*,Ein columns (lensing-based stellar fractions, which the Atlas does not use). None was recorded or used.
