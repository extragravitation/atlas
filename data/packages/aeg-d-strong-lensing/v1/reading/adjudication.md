# A6 strong lensing: adjudication of the input readings

- **Date:** 2026-10-31.
- **Adjudicator:** Claude (AI, Anthropic; model Claude Opus 5.5), working for JvH. AI assistance is disclosed. The adjudicator did none of the readings. The readings were not edited.
- **Status:** a record of how each reader difference was settled at source, plus questions for JvH. It is not a ruling. Nothing below changes a frozen rule. Every place where the frozen rules do not settle a case is written as a question (§6).
- **Outputs:** this file and `reading/adjudicated_inputs.csv` (777 rows: one per value to be packaged for the systems with printed z_l < 0.30, plus the record-only rows those systems need). Nothing was committed or pushed.

## Inputs

Repository files read (not changed). Worktree `data/a6-reading` at commit `1fb86e10625426a5e727c0f6e452c6485cf2b699`.

| File | SHA-256 |
|---|---|
| `data/packages/aeg-d-strong-lensing/v1/REPRODUCTION.md` (draft; frozen on merge) | `44e3b2715f4aab7ac40900e49fd2cf798679d02839363642dff7367c8f2467ef` |
| `docs/methods/A6S_PRECEDENCE.md` (frozen, D-065) | `f103809eadac00dac657061982e963fdfe1e85f46d68188a73953c17dfe9b03d` |
| `reading/READING_BRIEF.md` | `ef858fc2e7258e4cf17a0078a2b705a94e3677c785717c16673437eebcf3c5bc` |
| `docs/sources/screening-A6S/packaging-inventory.md` | `4421045d7d78ca5cb79f266b9bfd45db15d7640847a61e5963a41c73a2f4cf2e` |
| `docs/decisions.md` (D-063 to D-066 read) | `06c96419c01fe3b90c9520db8eb42b7e43849b1c644af249547b257acc2a5ce6` |
| `reading/compare_readings.py` (v1) | `b3ad8071d47ffbc7fa36739db09e4dcc48578b6239f2a51a3645a3586ca4ec69` |
| `reading/compare_readings_v2.py` | `6fa3aa09011f9dd6093f29dee584c28640badc824651698a430405f37c5fe8fd` |
| `reading/readings/reader-a-block1.csv` | `134e83b135f9cb5e618eb43c69cca836d9e6c3b86c90fec8c14cdfd1036fb70e` |
| `reading/readings/reader-a-block1-questions.md` | `153183d404beda7a22b4c9374f8a72f75b0cdb3f52946953712932f34c4d9854` |
| `reading/readings/reader-a-block2.csv` | `c535e1a0b57ee2094313e0ea0e1cdd1b3555657d1ee64c4f498eab7fc0da6443` |
| `reading/readings/reader-a-block2-questions.md` | `0ea2477f1d2d8f0399a925ea6bae8b96a91161f8d653538772ad5b457bac58be` |
| `reading/readings/reader-a-block3.csv` | `523a796c2f299ec8477a102c79d432bb5da4df19d0336b5d14a1aabd550e22cb` |
| `reading/readings/reader-a-block3-questions.md` | `dbb562d3be07bf5b81ad8ca0f30e91bdc2fb557dd3840c1bad177ce4bba631be` |
| `reading/readings/reader-b-block1.csv` | `ef8e6b2053663dc23d3a383543d2d3e031720005b03ad0aac39f477069dbcf3b` |
| `reading/readings/reader-b-block1-questions.md` | `6580b3fb570826f1c6ea3bfb4b82d145d5f3d84cd7cd1af552bd8332ae25a16e` |
| `reading/readings/reader-b-block2.csv` | `508971b3c4f19cad30af532f98793fac49b2029e5c78b6394e3d72d2951457e1` |
| `reading/readings/reader-b-block2-questions.md` | `a3aca544c81ad65b782cf60e37652a7de1e26c5fb8c1442838181a716a501885` |
| `reading/readings/reader-b-block3.csv` | `906970510eb0a917d2e561bd041fea50cbc12e3d9e040f4341820c1d1b0eac95` |
| `reading/readings/reader-b-block3-questions.md` | `15d6b5a2397f9e93a7026aa3883c475508e71e514821eb5a1e09d71807da223e` |
| `reading/comparison/block1-v2.csv` | `20fd77955e39394c969008e060d6d61599e57375cd8eabe8da8e556d29ab3180` |
| `reading/comparison/block2-v2.csv` | `7f4280c076c6fcd9dcf22b7cb8a3663503a4114eae51f4ac96ef1bb6223ed6fd` |
| `reading/comparison/block3-v2.csv` | `d4a087acb15127c0206873c36c281958440f29e8395ae2f287cc68c5e6fa6c90` |
| `reading/comparison/block1.csv` (v1) | `9407a1114f9632d1554dc6005995dd17d1898dc6c6805af9d92916843405ecb1` |
| `reading/comparison/block2.csv` (v1) | `5d71c55d17122940d8d03700f6f50c597b4974ffc64482f8b6d9d5a3e12a6e1d` |
| `reading/comparison/block3.csv` (v1) | `5ab348bf71e7da80a14a0563c7df5983e039405bb86d641e9ddf559660a0372e` |

Sources opened by the adjudicator are listed with their SHA-256 in the Appendix. They were fetched with curl's default user-agent and kept outside the repository.

## 1. Result in brief

- **Non-agree keys in v2:** 64 (block 1), 15 (block 2), 237 (block 3), 316 in total. Every key is classified in §2.
  - 7 keys are "real difference". They are CASTLES lens redshifts that are estimates, B0712+472's z_s printed differently by the two CASTLES papers, NGC 6505's θ_E error (B missed it), and SNL-0's second M_E and second z_l (A recorded both printed values). Each is settled at source in §2.
  - 41 keys are needed one-reader extras, each verified at source.
  - Everything else is notation (scope, system-id or unit spelling) or an extra that is not needed.
- **Readers' values agree with the sources wherever checked.** These were checked value by value:
  - all 54 SLACS systems below 0.30 (z_l, z_s, morphology, θ_E, and the four R13 inside-R_E masses), against VizieR;
  - all 37 S4TM systems below 0.30, against the IOP tables;
  - all 23 SuGOHI redshifts, against the arXiv table.
  Every other value in `adjudicated_inputs.csv` was read in the source text.
- **Plot table (§4, printed z_l < 0.30):**
  - plottable by the frozen rules: SLACS 46, S4TM 37, SL2S 2, NGC 6505 1;
  - open on a question: SLACS 2, SNELLS 2, MNELLS 1, MaNGA 2;
  - not plotted, with the reason recorded: SLACS 6, SL2S 2, SNELLS 1, CASTLES 4.
  - SuGOHI, KiDS, the Cosmic Horseshoe and J0100+1818 have no system below 0.30.
  - Every plotted system still depends on the gas question (Q14).
- **Gas:**
  - The only statements that meet the letter of §3.4 are system-level source assumptions: R28 for SNL-0 (the example named in the frozen rule), and by the same reading R25 for the SNELLS lenses and R32 for the two MaNGA lenses.
  - No literature statement read so far concerns gas inside the Einstein radius. For every other system the cell returns to JvH (§5, Q14).

## 2. Non-agree keys, per block

How to read the tables:
- "A" and "B" are the v2 value tuples (value, err_minus, err_plus [, form, limit]); "–" is empty.
- "Class" is one of:
  - same value, different notation;
  - one-reader extra (not needed);
  - one-reader extra (needed);
  - real difference.
- "Settled at source" gives the correct value as printed and its location.
- arXiv versions: R5 0805.1931v1, R13 0904.3282v2, R10 1711.00072v2, R9 1407.2240v2, R20 1307.4764v1, R21 1307.4759v1, R28 1306.4983v1, R25 1503.02661v1, R26 1612.00065v2, R61 1709.01931v1, R33 2203.09309v1, R29 1803.07082v1, R27 2002.07191v1, R32 1911.06338v1, R30 2502.06505v1, R66 1111.4215v3, Grillo 2010 0912.0744v1, Eichner 2012 1209.2140v1, R57 1904.10465v2, KKF98 astro-ph/9708161v1, K00 astro-ph/9909018v1.

What v2 does not compare:
- v2 compares numeric quantities only. Text quantities (kind, redshift method, IMF, aperture, flat) are outside it.
- For the systems below 0.30, the adjudicator compared the kind, redshift-method, IMF and aperture rows of the two readings by hand.
- The adjudicator also checked by script that the multiset matching of `mstar` hid no IMF-label disagreement. 550 shared stellar-mass keys were checked. 39 differ only because one reader put the IMF in a separate `imf` row. None has contradictory labels.
- One text difference matters: the word "flat". Readers recorded "not stated in words" or "yes". This is settled in §3b and raised as Q4.

### Block 1 (SLACS: 64 keys)

| # | Scope | System (normalised) | Rec. | Quantity | A | B | Status | Class | Settled at source |
|---|---|---|---|---|---|---|---|---|---|
| 1.1 | J0946+1006 | J09461006 | R66 | R_e | (0.066, 0.010, 0.010);(0.082, 0.010, 0.010);(0.50, 0.05, 0.05);(0.50, 0.10, 0.10 | (0.50, 0.10, 0.10);(4.46, 0.50, 0.50) | differ | same value, different notation | R66 Table 2 (double Sérsic) r_eff = 0.50 ± 0.10″ (comp. 1), 4.46 ± 0.50″ (comp. 2): both readers. A also filed Table 3 tPIEMD r_c = 0.066 ± 0.010″, 0.082 ± 0.010″ and r_t = 0.50 ± 0.05″, 6.05 ± 0.10″ under R_e (noted 'NOT an effective radius'); B put them in a note. Values agree; arXiv:1111.4215v3 Tables 2–3. |
| 1.2 | J0946+1006 | J09461006 | R66 | z_s |  | (0.609, –, –) | only_b | one-reader extra (not needed) | R66 z_s1 = 0.609 (B). Observed default R5 prints zBG = 0.6085 (VizieR J/ApJ/682/964 table4), which is used. |
| 1.3 | J1538+5817 | J15385817 | R49 | z_l |  | (0.143, –, –) | only_b | one-reader extra (not needed) | Grillo et al. 2010 prints z_l = 0.143, z_s = 0.531 (arXiv:0912.0744v1 abstract, Table 1). The observed default R5 prints 0.1428 / 0.5312, which are used. |
| 1.4 | J1538+5817 | J15385817 | R49 | z_s |  | (0.531, –, –) | only_b | one-reader extra (not needed) | Grillo et al. 2010 prints z_l = 0.143, z_s = 0.531 (arXiv:0912.0744v1 abstract, Table 1). The observed default R5 prints 0.1428 / 0.5312, which are used. |
| 1.5 | SLACS V-modelled lenses | J00290055 | R7 | R_e |  | (2.16, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.6 | SLACS V-modelled lenses | J00370942 | R7 | R_e |  | (1.80, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.7 | SLACS V-modelled lenses | J00440113 | R7 | R_e |  | (1.92, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.8 | SLACS V-modelled lenses | J01091500 | R7 | mstar | (–, –, – log);(–, –, – log) |  | only_a | same value, different notation | A recorded R7's printed '...' (no mass; fewer than 2 HST bands) as an empty row; B wrote no row. R7 is an alternative only (D-063 item 3). |
| 1.9 | SLACS V-modelled lenses | J02520039 | R7 | R_e |  | (1.39, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.10 | SLACS V-modelled lenses | J04050455 | R7 | mstar | (–, –, – log);(–, –, – log) |  | only_a | same value, different notation | A recorded R7's printed '...' (no mass; fewer than 2 HST bands) as an empty row; B wrote no row. R7 is an alternative only (D-063 item 3). |
| 1.11 | SLACS V-modelled lenses | J07283835 | R7 | R_e |  | (1.78, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.12 | SLACS V-modelled lenses | J08222652 | R7 | R_e |  | (1.82, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.13 | SLACS V-modelled lenses | J08413824 | R13 | mstar | (–, –, –) |  | only_a | same value, different notation | A recorded an empty 'not in R13' row; B wrote none. System is not in Grillo et al. 2009 (checked: absent from VizieR J/A+A/501/461/lens, 57 rows). |
| 1.14 | SLACS V-modelled lenses | J08413824 | R7 | R_e |  | (4.21, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.15 | SLACS V-modelled lenses | J09120029 | R7 | R_e |  | (4.01, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.16 | SLACS V-modelled lenses | J09360913 | R7 | R_e |  | (2.11, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.17 | SLACS V-modelled lenses | J09461006 | R7 | R_e |  | (2.35, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.18 | SLACS V-modelled lenses | J09550101 | R13 | mstar | (–, –, –) |  | only_a | same value, different notation | A recorded an empty 'not in R13' row; B wrote none. System is not in Grillo et al. 2009 (checked: absent from VizieR J/A+A/501/461/lens, 57 rows). |
| 1.19 | SLACS V-modelled lenses | J09550101 | R7 | R_e |  | (1.47, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.20 | SLACS V-modelled lenses | J09565100 | R7 | R_e |  | (2.19, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.21 | SLACS V-modelled lenses | J09590410 | R7 | R_e |  | (1.29, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.22 | SLACS V-modelled lenses | J09594416 | R7 | R_e |  | (1.98, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.23 | SLACS V-modelled lenses | J10163859 | R7 | R_e |  | (1.46, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.24 | SLACS V-modelled lenses | J10201122 | R7 | R_e |  | (1.59, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.25 | SLACS V-modelled lenses | J10234230 | R7 | R_e |  | (1.77, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.26 | SLACS V-modelled lenses | J10290420 | R7 | R_e |  | (1.56, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.27 | SLACS V-modelled lenses | J10325322 | R13 | mstar | (–, –, –) |  | only_a | same value, different notation | A recorded an empty 'not in R13' row; B wrote none. System is not in Grillo et al. 2009 (checked: absent from VizieR J/A+A/501/461/lens, 57 rows). |
| 1.28 | SLACS V-modelled lenses | J10325322 | R7 | R_e |  | (0.81, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.29 | SLACS V-modelled lenses | J11035322 | R13 | mstar | (–, –, –) |  | only_a | same value, different notation | A recorded an empty 'not in R13' row; B wrote none. System is not in Grillo et al. 2009 (checked: absent from VizieR J/A+A/501/461/lens, 57 rows). |
| 1.30 | SLACS V-modelled lenses | J11035322 | R7 | R_e |  | (2.85, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.31 | SLACS V-modelled lenses | J11065228 | R7 | R_e |  | (1.39, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.32 | SLACS V-modelled lenses | J11120826 | R7 | R_e |  | (1.32, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.33 | SLACS V-modelled lenses | J11346027 | R7 | R_e |  | (2.02, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.34 | SLACS V-modelled lenses | J11421001 | R7 | R_e |  | (1.24, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.35 | SLACS V-modelled lenses | J11430144 | R7 | R_e |  | (2.66, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.36 | SLACS V-modelled lenses | J11534612 | R7 | R_e |  | (1.16, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.37 | SLACS V-modelled lenses | J12040358 | R7 | R_e |  | (1.09, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.38 | SLACS V-modelled lenses | J12054910 | R7 | R_e |  | (1.79, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.39 | SLACS V-modelled lenses | J12136708 | R7 | R_e |  | (1.50, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.40 | SLACS V-modelled lenses | J12180830 | R7 | R_e |  | (2.70, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.41 | SLACS V-modelled lenses | J12500523 | R7 | R_e |  | (1.32, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.42 | SLACS V-modelled lenses | J12510208 | R13 | mstar | (–, –, –) |  | only_a | same value, different notation | A recorded an empty 'not in R13' row; B wrote none. System is not in Grillo et al. 2009 (checked: absent from VizieR J/A+A/501/461/lens, 57 rows). |
| 1.43 | SLACS V-modelled lenses | J12510208 | R7 | R_e |  | (2.61, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.44 | SLACS V-modelled lenses | J14026321 | R7 | R_e |  | (2.29, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.45 | SLACS V-modelled lenses | J14030006 | R7 | R_e |  | (1.14, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.46 | SLACS V-modelled lenses | J14165136 | R7 | R_e |  | (0.98, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.47 | SLACS V-modelled lenses | J14206019 | R7 | R_e |  | (2.25, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.48 | SLACS V-modelled lenses | J14304105 | R7 | R_e |  | (2.55, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.49 | SLACS V-modelled lenses | J14326317 | R13 | mstar | (–, –, –) |  | only_a | same value, different notation | A recorded an empty 'not in R13' row; B wrote none. System is not in Grillo et al. 2009 (checked: absent from VizieR J/A+A/501/461/lens, 57 rows). |
| 1.50 | SLACS V-modelled lenses | J14326317 | R7 | R_e |  | (3.04, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.51 | SLACS V-modelled lenses | J14360000 | R7 | R_e |  | (1.63, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.52 | SLACS V-modelled lenses | J14430304 | R7 | R_e |  | (0.70, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.53 | SLACS V-modelled lenses | J14510239 | R7 | R_e |  | (1.54, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.54 | SLACS V-modelled lenses | J15310105 | R7 | R_e |  | (1.97, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.55 | SLACS V-modelled lenses | J15385817 | R7 | R_e |  | (1.00, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.56 | SLACS V-modelled lenses | J16213931 | R7 | R_e |  | (1.51, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.57 | SLACS V-modelled lenses | J16270053 | R7 | R_e |  | (1.98, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.58 | SLACS V-modelled lenses | J16304520 | R7 | R_e |  | (1.65, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.59 | SLACS V-modelled lenses | J16364707 | R7 | R_e |  | (1.68, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.60 | SLACS V-modelled lenses | J22380754 | R7 | R_e |  | (1.82, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.61 | SLACS V-modelled lenses | J23000022 | R7 | R_e |  | (1.52, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.62 | SLACS V-modelled lenses | J23031422 | R7 | R_e |  | (2.94, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.63 | SLACS V-modelled lenses | J23210939 | R7 | R_e |  | (4.11, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |
| 1.64 | SLACS V-modelled lenses | J23410000 | R7 | R_e |  | (2.36, –, –) | only_b | one-reader extra (not needed) | R7 F814W r_e (alternative record). Not needed: R13 prints M* inside R_E. |

### Block 2 (S4TM, SL2S: 15 keys)

| # | Scope | System (normalised) | Rec. | Quantity | A | B | Status | Class | Settled at source |
|---|---|---|---|---|---|---|---|---|---|
| 2.1 | SL2S III sample | (RECORD) | R21 | H0 |  | (70, –, –) | only_b | one-reader extra (not needed) | R21 states H0 = 70, Ωm = 0.3, ΩΛ = 0.7 (arXiv:1307.4759v1 §1). Not needed: θ_E and distances use R20's own statement (same values). |
| 2.2 | SL2S III sample | SL2SJ022511045433 | R20 | M_E |  | (–, –, –) | only_b | same value, different notation | B recorded 'not printed'; A wrote no row. R20 prints R_Ein only (Table 6); M_E is computed (REPRODUCTION §Inputs). |
| 2.3 | SL2S III sample | SL2SJ022511045433 | R21 | R_e |  | (8.59, –, –) | only_b | one-reader extra (not needed) | R21 Table 3 R_eff in kpc (alternative). The profile route uses R20's own fit (see Q4). |
| 2.4 | SL2S III sample | SL2SJ084959025142 | R20 | M_E |  | (–, –, –) | only_b | same value, different notation | B recorded 'not printed'; A wrote no row. R20 prints R_Ein only (Table 6); M_E is computed (REPRODUCTION §Inputs). |
| 2.5 | SL2S III sample | SL2SJ084959025142 | R21 | R_e |  | (6.11, –, –) | only_b | one-reader extra (not needed) | R21 Table 3 R_eff in kpc (alternative). The profile route uses R20's own fit (see Q4). |
| 2.6 | SL2S III sample | SL2SJ140533550231 | R21 | z_s |  | (–, –, –) | only_b | same value, different notation | B recorded 'not printed' for a system absent from R21 Table 2; A wrote no row. No redshift is printed (arXiv:1307.4759v1 Table 2). |
| 2.7 | SL2S III sample | SL2SJ141917511729 | R21 | z_s |  | (–, –, –) | only_b | same value, different notation | B recorded 'not printed' for a system absent from R21 Table 2; A wrote no row. No redshift is printed (arXiv:1307.4759v1 Table 2). |
| 2.8 | SL2S III sample | SL2SJ142321572243 | R21 | z_s |  | (–, –, –) | only_b | same value, different notation | B recorded 'not printed' for a system absent from R21 Table 2; A wrote no row. No redshift is printed (arXiv:1307.4759v1 Table 2). |
| 2.9 | SL2S III sample | SL2SJ221929001743 | R20 | M_E |  | (–, –, –) | only_b | same value, different notation | B recorded 'not printed'; A wrote no row. R20 prints R_Ein only (Table 6); M_E is computed (REPRODUCTION §Inputs). |
| 2.10 | SL2S III sample | SL2SJ222012010606 | R20 | M_E |  | (–, –, –) | only_b | same value, different notation | B recorded 'not printed'; A wrote no row. R20 prints R_Ein only (Table 6); M_E is computed (REPRODUCTION §Inputs). |
| 2.11 | SL2SJ02176-0513 | SL2SJ021760513 | R49 | z_l |  | (0.6459, 0.0003, 0.0003) | only_b | same value, different notation | System-id spelling only (A appended the J2000 coordinates). Values identical: Tu et al. 2009 (arXiv:0902.4804v1) Table 1. z_l > 0.30. |
| 2.12 | SL2SJ02176-0513 | SL2SJ021760513 | R49 | z_s |  | (1.8470, 0.0003, 0.0003) | only_b | same value, different notation | System-id spelling only (A appended the J2000 coordinates). Values identical: Tu et al. 2009 (arXiv:0902.4804v1) Table 1. z_l > 0.30. |
| 2.13 | SL2SJ02176-0513 | SL2SJ021760513(J200002:17:37.13605:13:29 | R49 | H0 | (70, –, –) |  | only_a | same value, different notation | System-id spelling only (A appended the J2000 coordinates). Values identical: Tu et al. 2009 (arXiv:0902.4804v1) Table 1. z_l > 0.30. |
| 2.14 | SL2SJ02176-0513 | SL2SJ021760513(J200002:17:37.13605:13:29 | R49 | z_l | (0.6459, 0.0003, 0.0003) |  | only_a | same value, different notation | System-id spelling only (A appended the J2000 coordinates). Values identical: Tu et al. 2009 (arXiv:0902.4804v1) Table 1. z_l > 0.30. |
| 2.15 | SL2SJ02176-0513 | SL2SJ021760513(J200002:17:37.13605:13:29 | R49 | z_s | (1.8470, 0.0003, 0.0003);(2.90, 0.24, 0.18) |  | only_a | same value, different notation; plus one-reader extra (not needed) | Same z_l 0.6459 ± 0.0003, z_s 1.8470 ± 0.0003 (Tu et al. 2009 Table 1); A's system_id includes coordinates. A also recorded the second source z_dbl = 2.90 (+0.18 −0.24, photometric): not needed (z_l > 0.30). |

### Block 3 (SNELLS, MNELLS, MaNGA, NGC 6505, CASTLES, SuGOHI, KiDS, Cosmic Horseshoe, J0100+1818: 237 keys)

| # | Scope | System (normalised) | Rec. | Quantity | A | B | Status | Class | Settled at source |
|---|---|---|---|---|---|---|---|---|---|
| 3.1 | CASTLES lenses | 00472808 | R36 | z_l | (0.48, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.2 | CASTLES lenses | 00472808 | R36 | z_s | (3.60, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.3 | CASTLES lenses | B0712472 | R36 | z_l | (0.41, –, –);(0.41, –, –) | (0.41, –, –) | differ | same value, different notation | Same value; A recorded it from both R36 papers (KKF98 and K00). KKF98 Table 1 z_s = 1.33; K00 Table 5 z_s = 1.34. A recorded both, B only KKF98. Both printed; z_l = 0.41 (> 0.30). |
| 3.4 | CASTLES lenses | B0712472 | R36 | z_s | (1.33, –, –);(1.34, –, –) | (1.33, –, –) | differ | real difference between the two R36 papers | KKF98 Table 1 z_s = 1.33; K00 Table 5 z_s = 1.34. A recorded both, B only KKF98. Both printed; z_l = 0.41 (> 0.30). |
| 3.5 | CASTLES lenses | B1030071 | R36 | z_l | (0.60, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.6 | CASTLES lenses | B1030071 | R36 | z_s | (1.54, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.7 | CASTLES lenses | B1127385 | R36 | z_l | (0.78, –, –, 'estimate (zFP), not a measured z_l') |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.8 | CASTLES lenses | B1127385 | R36 | z_s | (–, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.9 | CASTLES lenses | B1422231 | R36 | z_l | (0.34, –, –);(0.34, –, –) | (0.34, –, –) | differ | same value, different notation | Same value(s); A recorded the value from both R36 papers (KKF98 and K00), B from one. K00 = Kochanek et al. 2000 (astro-ph/9909018v1) Table 5; KKF98 = Keeton, Kochanek & Falco 1998 (astro-ph/9708161v1) Table 1. |
| 3.10 | CASTLES lenses | B1422231 | R36 | z_s | (3.62, –, –);(3.62, –, –) | (3.62, –, –) | differ | same value, different notation | Same value(s); A recorded the value from both R36 papers (KKF98 and K00), B from one. K00 = Kochanek et al. 2000 (astro-ph/9909018v1) Table 5; KKF98 = Keeton, Kochanek & Falco 1998 (astro-ph/9708161v1) Table 1. |
| 3.11 | CASTLES lenses | B1608656 | R36 | z_l | (0.63, –, –);(0.63, –, –) | (0.63, –, –) | differ | same value, different notation | Same value(s); A recorded the value from both R36 papers (KKF98 and K00), B from one. K00 = Kochanek et al. 2000 (astro-ph/9909018v1) Table 5; KKF98 = Keeton, Kochanek & Falco 1998 (astro-ph/9708161v1) Table 1. |
| 3.12 | CASTLES lenses | B1608656 | R36 | z_s | (1.39, –, –);(1.39, –, –) | (1.39, –, –) | differ | same value, different notation | Same value(s); A recorded the value from both R36 papers (KKF98 and K00), B from one. K00 = Kochanek et al. 2000 (astro-ph/9909018v1) Table 5; KKF98 = Keeton, Kochanek & Falco 1998 (astro-ph/9708161v1) Table 1. |
| 3.13 | CASTLES lenses | B1938666 | R36 | z_l | (0.88, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.14 | CASTLES lenses | B1938666 | R36 | z_s | (–, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.15 | CASTLES lenses | B2045265 | R36 | z_l | (0.87, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.16 | CASTLES lenses | B2045265 | R36 | z_s | (1.28, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.17 | CASTLES lenses | B2319052 | R36 | z_l | (0.62, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.18 | CASTLES lenses | B2319052 | R36 | z_s | (–, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.19 | CASTLES lenses | BRI09520115 | R36 | z_l | (0.41, –, –, 'estimate (zFP), not a measured z_l');(0.99, –, –) | (0.99, –, –) | differ | real difference (both are estimates) | KKF98 0.99 is a ‡ estimate; K00 Table 5 leaves z_l blank and prints z_FP = 0.41. No measured lens redshift is printed. Not plotted either way. |
| 3.20 | CASTLES lenses | BRI09520115 | R36 | z_s | (4.5, –, –);(4.50, –, –) | (4.5, –, –) | differ | same value, different notation | Same value; A recorded it from both R36 papers (KKF98 and K00). KKF98 0.99 is a ‡ estimate; K00 Table 5 leaves z_l blank and prints z_FP = 0.41. No measured lens redshift is printed. Not plotted either way. |
| 3.21 | CASTLES lenses | FBQ09512635 | R36 | z_l | (0.21, –, –, 'estimate (zFP), not a measured z_l') |  | only_a | one-reader extra (needed) | K00 Table 5: z_l blank, z_s 1.24, z_FP 0.21. Needed as a record: the only lens z is a fundamental-plane estimate, so it fails the spectroscopic-redshift condition. |
| 3.22 | CASTLES lenses | FBQ09512635 | R36 | z_s | (1.24, –, –) |  | only_a | one-reader extra (needed) | K00 Table 5: z_l blank, z_s 1.24, z_FP 0.21. Needed as a record: the only lens z is a fundamental-plane estimate, so it fails the spectroscopic-redshift condition. |
| 3.23 | CASTLES lenses | FSC10214472 | R36 | z_l | (0.78, –, –, 'estimate (zFP), not a measured z_l') |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.24 | CASTLES lenses | FSC10214472 | R36 | z_s | (2.29, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.25 | CASTLES lenses | HE11041805 | R36 | z_l | (0.73, –, –, 'estimate (zFP), not a measured z_l') |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.26 | CASTLES lenses | HE11041805 | R36 | z_s | (2.32, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.27 | CASTLES lenses | HE21492745 | R36 | z_l | (0.43, –, –, 'estimate (zFP), not a measured z_l') |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.28 | CASTLES lenses | HE21492745 | R36 | z_s | (2.03, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.29 | CASTLES lenses | HST125312914 | R36 | z_l | (0.63, –, –, 'estimate (zFP), not a measured z_l');(–, –, –) | (–, –, –) | differ | same value, different notation | No z_l printed in either paper; A also recorded K00 z_FP = 0.63, flagged as an estimate. |
| 3.30 | CASTLES lenses | HST125312914 | R36 | z_s | (–, –, –);(–, –, –) | (–, –, –) | differ | same value, different notation | No z_l printed in either paper; A also recorded K00 z_FP = 0.63, flagged as an estimate. |
| 3.31 | CASTLES lenses | HST14113521 | R36 | z_l | (0.46, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.32 | CASTLES lenses | HST14113521 | R36 | z_s | (2.81, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.33 | CASTLES lenses | HST141765226 | R36 | z_l | (0.81, –, –);(0.81, –, –) | (0.81, –, –) | differ | same value, different notation | z_s printed '(3.4)' in KKF98 ('(···) denotes a tentative measurement') and 3.40 in K00. B kept the parentheses, which the script could not parse. |
| 3.34 | CASTLES lenses | HST141765226 | R36 | z_s | (3.4, –, –);(3.40, –, –) | (–, –, –) | differ | same value, different notation | z_s printed '(3.4)' in KKF98 ('(···) denotes a tentative measurement') and 3.40 in K00. B kept the parentheses, which the script could not parse. |
| 3.35 | CASTLES lenses | LBQS1009025 | R36 | z_l | (0.88, –, –, 'estimate (zFP), not a measured z_l') |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.36 | CASTLES lenses | LBQS1009025 | R36 | z_s | (2.74, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.37 | CASTLES lenses | MG04140534 | R36 | z_l | (0.44, –, –);(0.96, –, –) | (0.44, –, –) | differ | real difference (A correct) | KKF98 Table 1 prints 0.44 with ‡ = 'Estimated median lens redshift … computed from the probability of producing the observed image separation'. K00 Table 5 prints z_l = 0.96. B's 0.44 is the estimate. Correct printed lens z: 0.96 (K00). > 0.30. |
| 3.38 | CASTLES lenses | MG04140534 | R36 | z_s | (2.64, –, –);(2.64, –, –) | (2.64, –, –) | differ | same value, different notation | Same value; A recorded it from both R36 papers (KKF98 and K00). KKF98 Table 1 prints 0.44 with ‡ = 'Estimated median lens redshift … computed from the probability of producing the observed image separation'. K00 Table 5 prints z_l = 0.96. B's 0.44 is the estimate. Correct printed lens z: 0.96 (K00). > 0.30. |
| 3.39 | CASTLES lenses | MG11310456 | R36 | z_l | (0.84, –, –);(–, –, –) | (–, –, –) | differ | one-reader extra (not needed) | K00 Table 5 z_l = 0.84 (A); KKF98 blank (B). > 0.30. |
| 3.40 | CASTLES lenses | MG11310456 | R36 | z_s | (–, –, –);(–, –, –) | (–, –, –) | differ | one-reader extra (not needed) | K00 Table 5 z_l = 0.84 (A); KKF98 blank (B). > 0.30. |
| 3.41 | CASTLES lenses | MG15493047 | R36 | M_E |  | (–, –, –) | only_b | same value, different notation | z_l = 0.11 in both papers; no z_s in either. B's extra M_E/R_e rows are empty 'not printed' rows. |
| 3.42 | CASTLES lenses | MG15493047 | R36 | R_e |  | (–, –, –) | only_b | same value, different notation | z_l = 0.11 in both papers; no z_s in either. B's extra M_E/R_e rows are empty 'not printed' rows. |
| 3.43 | CASTLES lenses | MG15493047 | R36 | z_l | (0.11, –, –);(0.11, –, –) | (0.11, –, –) | differ | same value, different notation | z_l = 0.11 in both papers; no z_s in either. B's extra M_E/R_e rows are empty 'not printed' rows. |
| 3.44 | CASTLES lenses | MG15493047 | R36 | z_s | (–, –, –);(–, –, –) | (–, –, –) | differ | same value, different notation | z_l = 0.11 in both papers; no z_s in either. B's extra M_E/R_e rows are empty 'not printed' rows. |
| 3.45 | CASTLES lenses | MG16541346 | R36 | M_E |  | (–, –, –) | only_b | one-reader extra (not needed) | z_l 0.25, z_s 1.74 in both papers. B's extra rows: R_e 1.80 ± 0.02″ (KKF98 Table 3) and an empty M_E row; not needed (no stellar-mass default, see plot table). |
| 3.46 | CASTLES lenses | MG16541346 | R36 | R_e |  | (1.80, 0.02, 0.02) | only_b | one-reader extra (not needed) | z_l 0.25, z_s 1.74 in both papers. B's extra rows: R_e 1.80 ± 0.02″ (KKF98 Table 3) and an empty M_E row; not needed (no stellar-mass default, see plot table). |
| 3.47 | CASTLES lenses | MG16541346 | R36 | z_l | (0.25, –, –);(0.25, –, –) | (0.25, –, –) | differ | same value, different notation | z_l 0.25, z_s 1.74 in both papers. B's extra rows: R_e 1.80 ± 0.02″ (KKF98 Table 3) and an empty M_E row; not needed (no stellar-mass default, see plot table). |
| 3.48 | CASTLES lenses | MG16541346 | R36 | z_s | (1.74, –, –);(1.74, –, –) | (1.74, –, –) | differ | same value, different notation | z_l 0.25, z_s 1.74 in both papers. B's extra rows: R_e 1.80 ± 0.02″ (KKF98 Table 3) and an empty M_E row; not needed (no stellar-mass default, see plot table). |
| 3.49 | CASTLES lenses | MG2016112 | R36 | z_l | (1.01, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.50 | CASTLES lenses | MG2016112 | R36 | z_s | (3.27, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.51 | CASTLES lenses | PG1115080 | R36 | z_l | (0.31, –, –);(0.31, –, –) | (0.31, –, –) | differ | same value, different notation | Same value(s); A recorded the value from both R36 papers (KKF98 and K00), B from one. K00 = Kochanek et al. 2000 (astro-ph/9909018v1) Table 5; KKF98 = Keeton, Kochanek & Falco 1998 (astro-ph/9708161v1) Table 1. |
| 3.52 | CASTLES lenses | PG1115080 | R36 | z_s | (1.72, –, –);(1.72, –, –) | (1.72, –, –) | differ | same value, different notation | Same value(s); A recorded the value from both R36 papers (KKF98 and K00), B from one. K00 = Kochanek et al. 2000 (astro-ph/9909018v1) Table 5; KKF98 = Keeton, Kochanek & Falco 1998 (astro-ph/9708161v1) Table 1. |
| 3.53 | CASTLES lenses | Q0142100 | R36 | z_l | (0.49, –, –);(0.49, –, –) | (0.49, –, –) | differ | same value, different notation | Same value(s); A recorded the value from both R36 papers (KKF98 and K00), B from one. K00 = Kochanek et al. 2000 (astro-ph/9909018v1) Table 5; KKF98 = Keeton, Kochanek & Falco 1998 (astro-ph/9708161v1) Table 1. |
| 3.54 | CASTLES lenses | Q0142100 | R36 | z_s | (2.72, –, –);(2.72, –, –) | (2.72, –, –) | differ | same value, different notation | Same value(s); A recorded the value from both R36 papers (KKF98 and K00), B from one. K00 = Kochanek et al. 2000 (astro-ph/9909018v1) Table 5; KKF98 = Keeton, Kochanek & Falco 1998 (astro-ph/9708161v1) Table 1. |
| 3.55 | CASTLES lenses | Q0957561 | R36 | z_l | (0.36, –, –);(0.36, –, –) | (0.36, –, –) | differ | same value, different notation | Same value(s); A recorded the value from both R36 papers (KKF98 and K00), B from one. K00 = Kochanek et al. 2000 (astro-ph/9909018v1) Table 5; KKF98 = Keeton, Kochanek & Falco 1998 (astro-ph/9708161v1) Table 1. |
| 3.56 | CASTLES lenses | Q0957561 | R36 | z_s | (1.41, –, –);(1.41, –, –) | (1.41, –, –) | differ | same value, different notation | Same value(s); A recorded the value from both R36 papers (KKF98 and K00), B from one. K00 = Kochanek et al. 2000 (astro-ph/9909018v1) Table 5; KKF98 = Keeton, Kochanek & Falco 1998 (astro-ph/9708161v1) Table 1. |
| 3.57 | CASTLES lenses | Q1017207 | R36 | z_l | (0.78, –, –, 'estimate (zFP), not a measured z_l') |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.58 | CASTLES lenses | Q1017207 | R36 | z_s | (2.55, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.59 | CASTLES lenses | Q2237030 | R36 | z_l | (0.04, –, –) |  | only_a | one-reader extra (needed) | K00 Table 5: z_l 0.04, z_s 1.69, z_FP 0.02. Needed: z_l < 0.30, so the system must be recorded with its reason (late-type; K00 arXiv PDF p. 7: 'Where the bulge of a late-type galaxy dominates the lensing, as in Q2237+0305'). B did not record it. |
| 3.60 | CASTLES lenses | Q2237030 | R36 | z_s | (1.69, –, –) |  | only_a | one-reader extra (needed) | K00 Table 5: z_l 0.04, z_s 1.69, z_FP 0.02. Needed: z_l < 0.30, so the system must be recorded with its reason (late-type; K00 arXiv PDF p. 7: 'Where the bulge of a late-type galaxy dominates the lensing, as in Q2237+0305'). B did not record it. |
| 3.61 | CASTLES lenses | Q2237030 | R41 | H0 | (72, –, –) |  | only_a | one-reader extra (not needed) | Q2237+030 in Leier et al. 2011 Table 1 (A only). Not needed: the system is late-type (see plot table). |
| 3.62 | CASTLES lenses | Q2237030 | R41 | Om | (0.3, –, –) |  | only_a | one-reader extra (not needed) | Q2237+030 in Leier et al. 2011 Table 1 (A only). Not needed: the system is late-type (see plot table). |
| 3.63 | CASTLES lenses | Q2237030 | R41 | R_e | (1.090, 0.014, 0.014) |  | only_a | one-reader extra (not needed) | Q2237+030 in Leier et al. 2011 Table 1 (A only). Not needed: the system is late-type (see plot table). |
| 3.64 | CASTLES lenses | Q2237030 | R41 | mstar | (1.15, 0.12, 0.12) |  | only_a | one-reader extra (not needed) | Q2237+030 in Leier et al. 2011 Table 1 (A only). Not needed: the system is late-type (see plot table). |
| 3.65 | CASTLES lenses | Q2237030 | R41 | z_l | (0.039, –, –) |  | only_a | one-reader extra (not needed) | Q2237+030 in Leier et al. 2011 Table 1 (A only). Not needed: the system is late-type (see plot table). |
| 3.66 | CASTLES lenses | Q2237030 | R41 | z_s | (1.7, –, –) |  | only_a | one-reader extra (not needed) | Q2237+030 in Leier et al. 2011 Table 1 (A only). Not needed: the system is late-type (see plot table). |
| 3.67 | CASTLES lenses | RXJ09110551 | R36 | z_l | (0.77, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.68 | CASTLES lenses | RXJ09110551 | R36 | z_s | (2.80, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.69 | CASTLES lenses | SBS1520530 | R36 | z_l | (0.52, –, –, 'estimate (zFP), not a measured z_l') |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.70 | CASTLES lenses | SBS1520530 | R36 | z_s | (1.86, –, –) |  | only_a | one-reader extra (needed) | System only in K00 (30 lenses); B read KKF98's 17. Needed as a record (D-066 item 2). A's values match K00 Table 5 (checked). z_l ≥ 0.30 or not measured. |
| 3.71 | Cosmic Horseshoe | COSMICHORSESHOE(PRINTEDINR60TITLEAS"J100 | R60 | z_l |  | (0.44, –, –) | only_b | same value, different notation | System-id spelling only. R60 z_l 0.44, z_s 2.38; R34 z_l 0.444, z_s 2.38115 ± 0.00012 (A: both records; B: R60). z_l > 0.30. |
| 3.72 | Cosmic Horseshoe | COSMICHORSESHOE(PRINTEDINR60TITLEAS"J100 | R60 | z_s |  | (2.38, –, –) | only_b | same value, different notation | System-id spelling only. R60 z_l 0.44, z_s 2.38; R34 z_l 0.444, z_s 2.38115 ± 0.00012 (A: both records; B: R60). z_l > 0.30. |
| 3.73 | Cosmic Horseshoe | J11481930(COSMICHORSESHOE) | R34 | z_l | (0.444, –, –) |  | only_a | same value, different notation | System-id spelling only. R60 z_l 0.44, z_s 2.38; R34 z_l 0.444, z_s 2.38115 ± 0.00012 (A: both records; B: R60). z_l > 0.30. |
| 3.74 | Cosmic Horseshoe | J11481930(COSMICHORSESHOE) | R34 | z_s | (2.38115, 0.00012, 0.00012) |  | only_a | same value, different notation | System-id spelling only. R60 z_l 0.44, z_s 2.38; R34 z_l 0.444, z_s 2.38115 ± 0.00012 (A: both records; B: R60). z_l > 0.30. |
| 3.75 | Cosmic Horseshoe | J11481930(COSMICHORSESHOE) | R60 | z_l | (0.44, –, –) |  | only_a | same value, different notation | System-id spelling only. R60 z_l 0.44, z_s 2.38; R34 z_l 0.444, z_s 2.38115 ± 0.00012 (A: both records; B: R60). z_l > 0.30. |
| 3.76 | Cosmic Horseshoe | J11481930(COSMICHORSESHOE) | R60 | z_s | (2.38, –, –) |  | only_a | same value, different notation | System-id spelling only. R60 z_l 0.44, z_s 2.38; R34 z_l 0.444, z_s 2.38115 ± 0.00012 (A: both records; B: R60). z_l > 0.30. |
| 3.77 | Euclid NGC 6505 | NGC6505 | R30 | H0 | (67.8, –, –) |  | only_a | same value, different notation | System-id spelling only; values identical. |
| 3.78 | Euclid NGC 6505 | NGC6505 | R30 | M_E | (1.53E+11, –, –) |  | only_a | one-reader extra (needed) | R30 §3.5 (Fig. 8 discussion): 'the mass enclosed by the Einstein radius is 1.53 × 10¹¹ M☉'. No error printed. B did not record it; needed (observed default prints M_E). |
| 3.79 | Euclid NGC 6505 | NGC6505 | R30 | Om | (0.308, –, –) |  | only_a | same value, different notation | System-id spelling only; values identical. |
| 3.80 | Euclid NGC 6505 | NGC6505 | R30 | mstar | (1.06E+11, 2E+9, 2E+9) |  | only_a | same value, different notation | 1.06 ± 0.02 × 10¹¹ M☉ inside θ_E (R30 §3.2, last paragraph). |
| 3.81 | Euclid NGC 6505 | NGC6505 | R30 | theta_E | (2.500, 0.001, 0.001) |  | only_a | real difference (A correct) | A: 2.500 ± 0.001″, as printed in R30 §5. See the B-keyed row. |
| 3.82 | Euclid NGC 6505 | NGC6505 | R30 | z_l | (0.041, 0.001, 0.001);(0.04243, 0.00003, 0.00003) |  | only_a | same value, different notation; plus one-reader extra (needed) | 0.04243 ± 0.00003 (§3.1) agrees. A also recorded the cosmological redshift 0.041 ± 0.001 (§4.2, peculiar-velocity corrected): needed for Q8. |
| 3.83 | Euclid NGC 6505 | NGC6505 | R30 | z_s | (0.4058, 0.003, 0.003) |  | only_a | same value, different notation | System-id spelling only; values identical. |
| 3.84 | Euclid NGC 6505 | NGC6505("ALTIERI'SLENS";RA17H51M07.46S,D | R30 | H0 |  | (67.8, –, –) | only_b | same value, different notation | System-id spelling only; values identical. |
| 3.85 | Euclid NGC 6505 | NGC6505("ALTIERI'SLENS";RA17H51M07.46S,D | R30 | Om |  | (0.308, –, –) | only_b | same value, different notation | System-id spelling only; values identical. |
| 3.86 | Euclid NGC 6505 | NGC6505("ALTIERI'SLENS";RA17H51M07.46S,D | R30 | mstar |  | (1.06E+11, 2E+9, 2E+9);(2.51E+10, 6E+8, 6E+8) | only_b | same value, different notation; plus one-reader extra (not needed) | 1.06 ± 0.02 × 10¹¹ M☉ inside θ_E agrees. B's extra 2.51 ± 0.06 × 10¹⁰ M☉ is the central 1.5″ SED fit (§3.1): not needed. |
| 3.87 | Euclid NGC 6505 | NGC6505("ALTIERI'SLENS";RA17H51M07.46S,D | R30 | theta_E |  | (2.500, –, –) | only_b | real difference (B missed the printed error) | B: 2.500 with no error. R30 §5 prints 'θE = 2″.500 ± 0″.001' (arXiv:2502.06505v1); Table 2 (γext + m4) prints 2″.500. Correct: 2.500 ± 0.001″. |
| 3.88 | Euclid NGC 6505 | NGC6505("ALTIERI'SLENS";RA17H51M07.46S,D | R30 | z_l |  | (0.04243, 0.00003, 0.00003) | only_b | same value, different notation | 0.04243 ± 0.00003 (R30 §3.1); id spelling only. |
| 3.89 | Euclid NGC 6505 | NGC6505("ALTIERI'SLENS";RA17H51M07.46S,D | R30 | z_s |  | (0.4058, 0.003, 0.003) | only_b | same value, different notation | System-id spelling only; values identical. |
| 3.90 | J0100+1818 (A7) | J01001818(J010049.18181827.7;RA01:00:49. | R47 | z_l |  | (0.581, –, –) | only_b | same value, different notation | System-id spelling only. R47 z_l 0.581, z_s 1.880. z_l > 0.30. |
| 3.91 | J0100+1818 (A7) | J01001818(J010049.18181827.7;RA01:00:49. | R47 | z_s |  | (1.880, –, –) | only_b | same value, different notation | System-id spelling only. R47 z_l 0.581, z_s 1.880. z_l > 0.30. |
| 3.92 | J0100+1818 (A7) | J010049.18181827.7(J01001818;CSWA15/CSWA | R47 | z_l | (0.581, –, –) |  | only_a | same value, different notation | System-id spelling only. R47 z_l 0.581, z_s 1.880. z_l > 0.30. |
| 3.93 | J0100+1818 (A7) | J010049.18181827.7(J01001818;CSWA15/CSWA | R47 | z_s | (1.880, –, –) |  | only_a | same value, different notation | System-id spelling only. R47 z_l 0.581, z_s 1.880. z_l > 0.30. |
| 3.94 | J1436+4943 | J143607.49494313.2(J14364943) | R32 | H0 |  | (–, –, –) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.95 | J1436+4943 | J143607.49494313.2(J14364943) | R32 | M_E |  | (28.2, 1.1, 1.1) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.96 | J1436+4943 | J143607.49494313.2(J14364943) | R32 | Om |  | (–, –, –) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.97 | J1436+4943 | J143607.49494313.2(J14364943) | R32 | R_e |  | (3.78, –, –) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.98 | J1436+4943 | J143607.49494313.2(J14364943) | R32 | mstar |  | (2.93, 0.26, 0.26);(6.72, 0.10, 0.10) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.99 | J1436+4943 | J143607.49494313.2(J14364943) | R32 | theta_E |  | (2.03, 0.04, 0.04) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.100 | J1436+4943 | J143607.49494313.2(J14364943) | R32 | z_l |  | (0.125, –, –) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.101 | J1436+4943 | J143607.49494313.2(J14364943) | R32 | z_s |  | (1.231, –, –) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.102 | J1701+3722 | J170124.01372258.1(J17013722) | R32 | H0 |  | (–, –, –) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.103 | J1701+3722 | J170124.01372258.1(J17013722) | R32 | M_E |  | (18.8, 3.7, 3.7) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.104 | J1701+3722 | J170124.01372258.1(J17013722) | R32 | Om |  | (–, –, –) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.105 | J1701+3722 | J170124.01372258.1(J17013722) | R32 | R_e |  | (4.30, –, –) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.106 | J1701+3722 | J170124.01372258.1(J17013722) | R32 | mstar |  | (2.93, 0.26, 0.26);(5.56, 0.35, 0.35) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.107 | J1701+3722 | J170124.01372258.1(J17013722) | R32 | theta_E |  | (1.63, 0.16, 0.16) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.108 | J1701+3722 | J170124.01372258.1(J17013722) | R32 | z_l |  | (0.122, –, –) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.109 | J1701+3722 | J170124.01372258.1(J17013722) | R32 | z_s |  | (0.791, –, –) | only_b | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.110 | KiDS J0233-3447 | KIDSJ02333447(EINSTEIN'BLUEEYE') | R43 | z_l | (0.9906, 0.0001, 0.0001) |  | only_a | same value, different notation | System-id spelling only. R43 z_l 0.9906 ± 0.0001; z_s 2.8230 ± 0.0001 (Table 1); A also recorded the text value 2.823 ± 0.001. z_l > 0.30. |
| 3.111 | KiDS J0233-3447 | KIDSJ02333447(EINSTEIN'BLUEEYE') | R43 | z_s | (2.823, 0.001, 0.001);(2.8230, 0.0001, 0.0001) |  | only_a | same value, different notation | System-id spelling only. R43 z_l 0.9906 ± 0.0001; z_s 2.8230 ± 0.0001 (Table 1); A also recorded the text value 2.823 ± 0.001. z_l > 0.30. |
| 3.112 | KiDS J0233-3447 | KIDSJ02333447(RA02:33:41.29,DEC34:47:59. | R43 | z_l |  | (0.9906, 0.0001, 0.0001) | only_b | same value, different notation | System-id spelling only. R43 z_l 0.9906 ± 0.0001; z_s 2.8230 ± 0.0001 (Table 1); A also recorded the text value 2.823 ± 0.001. z_l > 0.30. |
| 3.113 | KiDS J0233-3447 | KIDSJ02333447(RA02:33:41.29,DEC34:47:59. | R43 | z_s |  | (2.8230, 0.0001, 0.0001) | only_b | same value, different notation | System-id spelling only. R43 z_l 0.9906 ± 0.0001; z_s 2.8230 ± 0.0001 (Table 1); A also recorded the text value 2.823 ± 0.001. z_l > 0.30. |
| 3.114 | MNELLS J0403-0239 | 2MASXJ040350240239275(J04030239) | R29 | M_E | (1.064E+11, 2.3E+9, 2.3E+9) | (10.64, 0.23, 0.23) | differ | same value, different notation | 10.64 ± 0.23 × 10¹⁰ M☉ (unit scaling). R29 §4 then states: 'we revise the uncertainty in MEin to ∼4 per cent, i.e. 0.4 × 10¹⁰ M☉'. Both readers noted it; the adopted error is 0.4 × 10¹⁰. |
| 3.115 | MNELLS J0403-0239 | 2MASXJ040350240239275(J04030239) | R29 | Om | (0.272, –, –) |  | only_a | one-reader extra (not needed) | R29 Ωm = 0.272 (WMAP7, §4). B recorded R29's H0 only in a note. R29 is not the observed default; needed only under Q2 option (c). |
| 3.116 | MNELLS J0403-0239 | 2MASXJ040350240239275(J04030239) | R29 | mstar | (2.59, 0.12, 0.12);(2.90, 0.10, 0.10);(8.63E+10, 5.4E+9, 5.4E+9) | (2.59, 0.12, 0.12);(2.90, 0.10, 0.10) | b_subset | same value, different notation; plus one-reader extra (not needed) | Factors agree: L_Ein = 2.59 ± 0.12 × 10¹⁰ L☉ (i band), Υ_Ref = 2.90 ± 0.10 (Kroupa). A's extra 8.63 ± 0.54 × 10¹⁰ M☉ is lensing mass minus an EAGLE dark-matter estimate (R29 §4): not eligible (D-063 item 1), not needed. |
| 3.117 | MNELLS J0403-0239 | 2MASXJ040350240239275(J04030239) | R29 | sersic_n | (4, –, –, 'approximate (≈)') | (4, –, –, 'approximate (printed "n ≈ 4")') | differ | same value, different notation | Both: n ≈ 4 (R29 §3: 'well fitted by a Sersic profile with index n ≈ 4'). Note wording only. |
| 3.118 | MNELLS J0403-0239 | 2MASXJ040350240239275(J04030239) | R29 | z_l | (0.06569, –, –);(0.06604, –, –);(0.06655, –, –) |  | only_a | one-reader extra (needed) | R29 prints zH = 0.06604 (MUSE, §3), zH = 0.06655 (Jones et al. 2009, §3) and zCMB = 0.06569 (§4). B kept them in notes. Needed for Q2. |
| 3.119 | MNELLS J0403-0239 | 2MASXJ040350240239275(J04030239) | R29 | z_s | (0.19130, –, –);(0.19165, –, –) | (0.19165, –, –) | differ | same value, different notation; plus one-reader extra (needed) | 0.19165 (zH, §3) agrees; A also recorded zCMB = 0.19130 (§4). Needed for Q2. |
| 3.120 | MaNGA J1436+4943 | J143607.49494313.2(J14364943) | R32 | H0 | (–, –, –) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.121 | MaNGA J1436+4943 | J143607.49494313.2(J14364943) | R32 | M_E | (28.2, 1.1, 1.1) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.122 | MaNGA J1436+4943 | J143607.49494313.2(J14364943) | R32 | Om | (–, –, –) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.123 | MaNGA J1436+4943 | J143607.49494313.2(J14364943) | R32 | R_e | (3.78, –, –) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.124 | MaNGA J1436+4943 | J143607.49494313.2(J14364943) | R32 | mstar | (2.93, 0.26, 0.26);(6.72, 0.10, 0.10) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.125 | MaNGA J1436+4943 | J143607.49494313.2(J14364943) | R32 | theta_E | (2.03, 0.04, 0.04) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.126 | MaNGA J1436+4943 | J143607.49494313.2(J14364943) | R32 | z_l | (0.125, –, –) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.127 | MaNGA J1436+4943 | J143607.49494313.2(J14364943) | R32 | z_s | (1.231, –, –) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.128 | MaNGA J1701+3722 | J170124.01372258.1(J17013722) | R32 | H0 | (–, –, –) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.129 | MaNGA J1701+3722 | J170124.01372258.1(J17013722) | R32 | M_E | (18.8, 3.7, 3.7) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.130 | MaNGA J1701+3722 | J170124.01372258.1(J17013722) | R32 | Om | (–, –, –) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.131 | MaNGA J1701+3722 | J170124.01372258.1(J17013722) | R32 | R_e | (4.30, –, –) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.132 | MaNGA J1701+3722 | J170124.01372258.1(J17013722) | R32 | mstar | (2.93, 0.26, 0.26);(5.56, 0.35, 0.35) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.133 | MaNGA J1701+3722 | J170124.01372258.1(J17013722) | R32 | theta_E | (1.63, 0.16, 0.16) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.134 | MaNGA J1701+3722 | J170124.01372258.1(J17013722) | R32 | z_l | (0.122, –, –) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.135 | MaNGA J1701+3722 | J170124.01372258.1(J17013722) | R32 | z_s | (0.791, –, –) |  | only_a | same value, different notation | Scope spelling only (A: 'MaNGA J…', B: 'J…'). Values identical; checked against arXiv:1911.06338v1 Table 1. |
| 3.136 | SNL-0 (ESO 325-G004) | ESO325G004(SNL0;J1343331381033) | R26 | mstar | (2.84, 0.06, 0.06);(4.04, 0.10, 0.10);(6.24, 1.00, 1.12);(6.36, 0.71, 0.80);(7.4 | (2.84, 0.06, 0.06);(4.04, 0.10, 0.10) | b_subset | same value, different notation; plus one-reader extra (not needed) | Factors agree: L_r,Ein = 2.84 ± 0.06 × 10¹⁰ L☉,r; (M*/L_r)_MW = 4.04 ± 0.10 (Kroupa). A's extras 7.58, 7.41, 6.36, 6.24 are the IMF-free M*/L fits (1PL, 2PL, 2PL+cut, non-parametric; R26 Table 1): never defaults (D-063 item 1); not needed. |
| 3.137 | SNL-0 (ESO 325-G004) | ESO325G004(SNL0;J1343331381033) | R26 | theta_E | (2.85, –, –) |  | only_a | one-reader extra (needed) | R26 Table 1 θEin = 2.85″ ('Denoted REin by S15'): the luminosity aperture. Needed for aperture matching (equals R28's 2.85″). |
| 3.138 | SNL-0 (ESO 325-G004) | ESO325G004(SNL0;J1343331381033) | R26 | z_l | (0.034, –, –) |  | only_a | one-reader extra (not needed) | R26 Table 1 'Redshift' 0.034 (rounded). R28's 0.0347 is used. |
| 3.139 | SNL-0 (ESO 325-G004) | ESO325G004(SNL0;J1343331381033) | R28 | M_E | (1.44E+11, –, –);(1.50E+11, 6E+9, 6E+9) | (1.50E+11, 6E+9, 6E+9) | differ | real difference in scope (A recorded a second value) | Default value: 1.50 ± 0.06 × 10¹¹ M☉, R28 (Smith & Lucey 2013, arXiv:1306.4983v1) Table 3 'Total lensing mass inside REin' and §2.2: 'we adopt the lensing mass from the MFL model, MEin = 1.50 ± 0.06 × 10¹¹ M☉'. A's 1.44 × 10¹¹ is the SIS value the paper does not adopt (§2.2). The 2005 paper (astro-ph/0504453) prints 1.4 × 10¹¹ M☉ 'assuming a high redshift for the source' (no measured z_s): not the default. |
| 3.140 | SNL-0 (ESO 325-G004) | ESO325G004(SNL0;J1343331381033) | R28 | z_l | (0.0339, –, –);(0.0347, –, –) | (0.0347, –, –) | differ | real difference in scope (two printed values) | R28 Table 3: 'Lens redshift (heliocentric) 0.0339 From 6dF' and 'Lens redshift (CMB frame) zl 0.0347'; D_l 'From zl with WMAP7 cosmology'. Default: 0.0347 (the value carrying the symbol z_l and used for distances). 2005 paper: z = 0.0345 (title). |
| 3.141 | SNL-1 (ESO 286-G022) | ESO286G022(SNL1;J2100286422523) | R33 | z_l | (0.0312, –, –) |  | only_a | one-reader extra (not needed) | R33 Table 1 z = 0.0312 (citing Smith et al. 2015) equals R61's 0.0312; R61 is the observed default. |
| 3.142 | SNL-1 (ESO 286-G022) | ESO286G022(SNL1;J2100286422523) | R61 | M_E | (9.49E+10, 1.5E+9, 1.5E+9) | (9.49, 0.15, 0.15) | differ | same value, different notation | 9.49 ± 0.15 × 10¹⁰ M☉ (A as 9.49e10, B in units of 10¹⁰). R61 Table 2 'Adopted Mass' = M(≤ R_ap), R_ap = 2.38″ (arXiv:1709.01931v1). |
| 3.143 | SNL-1 (ESO 286-G022) | ESO286G022(SNL1;J2100286422523) | R61 | theta_E |  | (2.43, 0.03, 0.03) | only_b | one-reader extra (needed) | R61 Table 1 'Half image-separation' 2.43 ± 0.03″ ('this paper, HST–based'). Needed for Q1 (R_ap vs R_E). Not labelled an Einstein radius by R61. |
| 3.144 | SNL-2 | 2MASXJ014142320735281(SNL2;J014142307352 | R61 | M_E | (1.259E+11, 3.0E+9, 3.0E+9) | (12.59, 0.30, 0.30) | differ | same value, different notation | 12.59 ± 0.30 × 10¹⁰ M☉ (unit scaling). R61 Table 2 'Adopted Mass' = M(≤ R_ap), R_ap = 2.21″. |
| 3.145 | SNL-2 | 2MASXJ014142320735281(SNL2;J014142307352 | R61 | theta_E |  | (2.30, 0.03, 0.03) | only_b | one-reader extra (needed) | R61 Table 1 'Half image-separation' 2.30 ± 0.03″ (HST). Needed for Q1. |
| 3.146 | SuGOHI CMASS lenses | HSCJ015618010747 | R57 | z_l | (0.542, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.147 | SuGOHI CMASS lenses | HSCJ015618010747 | R57 | z_s | (1.167, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.148 | SuGOHI CMASS lenses | HSCJ015618010747(RA29.07554,DEC1.12977DE | R57 | z_l |  | (0.542, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.149 | SuGOHI CMASS lenses | HSCJ015618010747(RA29.07554,DEC1.12977DE | R57 | z_s |  | (1.167, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.150 | SuGOHI CMASS lenses | HSCJ020241064611 | R57 | z_l | (0.502, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.151 | SuGOHI CMASS lenses | HSCJ020241064611 | R57 | z_s | (2.748, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.152 | SuGOHI CMASS lenses | HSCJ020241064611(RA30.67247,DEC6.76979DE | R57 | z_l |  | (0.502, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.153 | SuGOHI CMASS lenses | HSCJ020241064611(RA30.67247,DEC6.76979DE | R57 | z_s |  | (2.748, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.154 | SuGOHI CMASS lenses | HSCJ021411040502 | R57 | z_l | (0.609, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.155 | SuGOHI CMASS lenses | HSCJ021411040502 | R57 | z_s | (1.880, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.156 | SuGOHI CMASS lenses | HSCJ021411040502(RA33.54670,DEC4.08411DE | R57 | z_l |  | (0.609, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.157 | SuGOHI CMASS lenses | HSCJ021411040502(RA33.54670,DEC4.08411DE | R57 | z_s |  | (1.880, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.158 | SuGOHI CMASS lenses | HSCJ021737051329 | R57 | z_l | (0.646, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.159 | SuGOHI CMASS lenses | HSCJ021737051329 | R57 | z_s | (1.847, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.160 | SuGOHI CMASS lenses | HSCJ021737051329(RA34.40492,DEC5.22482DE | R57 | z_l |  | (0.646, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.161 | SuGOHI CMASS lenses | HSCJ021737051329(RA34.40492,DEC5.22482DE | R57 | z_s |  | (1.847, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.162 | SuGOHI CMASS lenses | HSCJ022346053418 | R57 | z_l | (0.499, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.163 | SuGOHI CMASS lenses | HSCJ022346053418 | R57 | z_s | (1.444, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.164 | SuGOHI CMASS lenses | HSCJ022346053418(RA35.94227,DEC5.57180DE | R57 | z_l |  | (0.499, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.165 | SuGOHI CMASS lenses | HSCJ022346053418(RA35.94227,DEC5.57180DE | R57 | z_s |  | (1.444, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.166 | SuGOHI CMASS lenses | HSCJ022610042011 | R57 | z_l | (0.496, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.167 | SuGOHI CMASS lenses | HSCJ022610042011 | R57 | z_s | (1.232, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.168 | SuGOHI CMASS lenses | HSCJ022610042011(RA36.54440,DEC4.33656DE | R57 | z_l |  | (0.496, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.169 | SuGOHI CMASS lenses | HSCJ022610042011(RA36.54440,DEC4.33656DE | R57 | z_s |  | (1.232, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.170 | SuGOHI CMASS lenses | HSCJ023307043838 | R57 | z_l | (0.671, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.171 | SuGOHI CMASS lenses | HSCJ023307043838 | R57 | z_s | (1.869, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.172 | SuGOHI CMASS lenses | HSCJ023307043838(RA38.27945,DEC4.64396DE | R57 | z_l |  | (0.671, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.173 | SuGOHI CMASS lenses | HSCJ023307043838(RA38.27945,DEC4.64396DE | R57 | z_s |  | (1.869, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.174 | SuGOHI CMASS lenses | HSCJ023817054555 | R57 | z_l | (0.599, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.175 | SuGOHI CMASS lenses | HSCJ023817054555 | R57 | z_s | (1.763, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.176 | SuGOHI CMASS lenses | HSCJ023817054555(RA39.57402,DEC5.76542DE | R57 | z_l |  | (0.599, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.177 | SuGOHI CMASS lenses | HSCJ023817054555(RA39.57402,DEC5.76542DE | R57 | z_s |  | (1.763, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.178 | SuGOHI CMASS lenses | HSCJ085855010208 | R57 | z_l | (0.468, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.179 | SuGOHI CMASS lenses | HSCJ085855010208 | R57 | z_s | (1.421, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.180 | SuGOHI CMASS lenses | HSCJ085855010208(RA134.73330,DEC1.03567D | R57 | z_l |  | (0.468, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.181 | SuGOHI CMASS lenses | HSCJ085855010208(RA134.73330,DEC1.03567D | R57 | z_s |  | (1.421, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.182 | SuGOHI CMASS lenses | HSCJ094427014742 | R57 | z_l | (0.539, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.183 | SuGOHI CMASS lenses | HSCJ094427014742 | R57 | z_s | (1.179, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.184 | SuGOHI CMASS lenses | HSCJ094427014742(RA146.11446,DEC1.79511D | R57 | z_l |  | (0.539, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.185 | SuGOHI CMASS lenses | HSCJ094427014742(RA146.11446,DEC1.79511D | R57 | z_s |  | (1.179, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.186 | SuGOHI CMASS lenses | HSCJ120623001507 | R57 | z_l | (0.563, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.187 | SuGOHI CMASS lenses | HSCJ120623001507 | R57 | z_s | (3.120, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.188 | SuGOHI CMASS lenses | HSCJ120623001507(RA181.59937,DEC0.25199D | R57 | z_l |  | (0.563, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.189 | SuGOHI CMASS lenses | HSCJ120623001507(RA181.59937,DEC0.25199D | R57 | z_s |  | (3.120, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.190 | SuGOHI CMASS lenses | HSCJ121052011905 | R57 | z_l | (0.700, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.191 | SuGOHI CMASS lenses | HSCJ121052011905 | R57 | z_s | (2.295, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.192 | SuGOHI CMASS lenses | HSCJ121052011905(RA182.71869,DEC1.31810D | R57 | z_l |  | (0.700, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.193 | SuGOHI CMASS lenses | HSCJ121052011905(RA182.71869,DEC1.31810D | R57 | z_s |  | (2.295, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.194 | SuGOHI CMASS lenses | HSCJ121504004726 | R57 | z_l | (0.642, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.195 | SuGOHI CMASS lenses | HSCJ121504004726 | R57 | z_s | (1.297, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.196 | SuGOHI CMASS lenses | HSCJ121504004726(RA183.76850,DEC0.79056D | R57 | z_l |  | (0.642, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.197 | SuGOHI CMASS lenses | HSCJ121504004726(RA183.76850,DEC0.79056D | R57 | z_s |  | (1.297, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.198 | SuGOHI CMASS lenses | HSCJ140929011410 | R57 | z_l | (0.584, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.199 | SuGOHI CMASS lenses | HSCJ140929011410 | R57 | z_s | (2.302, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.200 | SuGOHI CMASS lenses | HSCJ140929011410(RA212.37381,DEC1.23631D | R57 | z_l |  | (0.584, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.201 | SuGOHI CMASS lenses | HSCJ140929011410(RA212.37381,DEC1.23631D | R57 | z_s |  | (2.302, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.202 | SuGOHI CMASS lenses | HSCJ141300012608 | R57 | z_l | (0.749, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.203 | SuGOHI CMASS lenses | HSCJ141300012608 | R57 | z_s | (2.666, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.204 | SuGOHI CMASS lenses | HSCJ141300012608(RA213.25030,DEC1.43560D | R57 | z_l |  | (0.749, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.205 | SuGOHI CMASS lenses | HSCJ141300012608(RA213.25030,DEC1.43560D | R57 | z_s |  | (2.666, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.206 | SuGOHI CMASS lenses | HSCJ141815015832 | R57 | z_l | (0.556, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.207 | SuGOHI CMASS lenses | HSCJ141815015832 | R57 | z_s | (2.139, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.208 | SuGOHI CMASS lenses | HSCJ141815015832(RA214.56556,DEC1.97564D | R57 | z_l |  | (0.556, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.209 | SuGOHI CMASS lenses | HSCJ141815015832(RA214.56556,DEC1.97564D | R57 | z_s |  | (2.139, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.210 | SuGOHI CMASS lenses | HSCJ142449005321 | R57 | z_l | (0.795, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.211 | SuGOHI CMASS lenses | HSCJ142449005321 | R57 | z_s | (1.302, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.212 | SuGOHI CMASS lenses | HSCJ142449005321(RA216.20420,DEC0.88934D | R57 | z_l |  | (0.795, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.213 | SuGOHI CMASS lenses | HSCJ142449005321(RA216.20420,DEC0.88934D | R57 | z_s |  | (1.302, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.214 | SuGOHI CMASS lenses | HSCJ142720001916 | R57 | z_l | (0.551, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.215 | SuGOHI CMASS lenses | HSCJ142720001916 | R57 | z_s | (1.266, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.216 | SuGOHI CMASS lenses | HSCJ142720001916(RA216.83562,DEC0.32114D | R57 | z_l |  | (0.551, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.217 | SuGOHI CMASS lenses | HSCJ142720001916(RA216.83562,DEC0.32114D | R57 | z_s |  | (1.266, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.218 | SuGOHI CMASS lenses | HSCJ144307004056 | R57 | z_l | (0.500, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.219 | SuGOHI CMASS lenses | HSCJ144307004056 | R57 | z_s | (1.071, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.220 | SuGOHI CMASS lenses | HSCJ144307004056(RA220.77985,DEC0.68225D | R57 | z_l |  | (0.500, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.221 | SuGOHI CMASS lenses | HSCJ144307004056(RA220.77985,DEC0.68225D | R57 | z_s |  | (1.071, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.222 | SuGOHI CMASS lenses | HSCJ220506014703 | R57 | z_l | (0.476, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.223 | SuGOHI CMASS lenses | HSCJ220506014703 | R57 | z_s | (2.526, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.224 | SuGOHI CMASS lenses | HSCJ220506014703(RA331.27884,DEC1.78441D | R57 | z_l |  | (0.476, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.225 | SuGOHI CMASS lenses | HSCJ220506014703(RA331.27884,DEC1.78441D | R57 | z_s |  | (2.526, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.226 | SuGOHI CMASS lenses | HSCJ222801012805 | R57 | z_l | (0.647, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.227 | SuGOHI CMASS lenses | HSCJ222801012805 | R57 | z_s | (2.462, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.228 | SuGOHI CMASS lenses | HSCJ222801012805(RA337.00824,DEC1.46826D | R57 | z_l |  | (0.647, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.229 | SuGOHI CMASS lenses | HSCJ222801012805(RA337.00824,DEC1.46826D | R57 | z_s |  | (2.462, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.230 | SuGOHI CMASS lenses | HSCJ223733005015 | R57 | z_l | (0.604, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.231 | SuGOHI CMASS lenses | HSCJ223733005015 | R57 | z_s | (2.143, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.232 | SuGOHI CMASS lenses | HSCJ223733005015(RA339.38973,DEC0.83772D | R57 | z_l |  | (0.604, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.233 | SuGOHI CMASS lenses | HSCJ223733005015(RA339.38973,DEC0.83772D | R57 | z_s |  | (2.143, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.234 | SuGOHI CMASS lenses | HSCJ230335003703 | R57 | z_l | (0.458, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.235 | SuGOHI CMASS lenses | HSCJ230335003703 | R57 | z_s | (0.936, –, –) |  | only_a | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.236 | SuGOHI CMASS lenses | HSCJ230335003703(RA345.89654,DEC0.61755D | R57 | z_l |  | (0.458, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |
| 3.237 | SuGOHI CMASS lenses | HSCJ230335003703(RA345.89654,DEC0.61755D | R57 | z_s |  | (0.936, –, –) | only_b | same value, different notation | System-id spelling only (B appended RA, Dec). Values identical; checked against arXiv:1904.10465v2 Table 1 (all 23 rows; minimum z_d = 0.458). |

### Named cases, in short

- **SNL-0 (R28).** R28 is two papers.
  - Smith et al. 2005 (astro-ph/0504453) has no measured source redshift. It prints z = 0.0345 (title) and "Assuming a high redshift for the source, the mass within REin is 1.4 × 10¹¹ M⊙" (abstract), with H0 = 71, Ωm = 0.27, ΩΛ = 0.73.
  - Smith & Lucey 2013 measured z_s = 2.141. It adopts "the lensing mass from the MFL model, MEin = 1.50 ± 0.06 × 10¹¹ M⊙" (§2.2), as printed in Table 3. Its SIS value of 1.44 × 10¹¹ M⊙ is not adopted.
  - The default value is therefore 1.50 ± 0.06 × 10¹¹ M⊙ inside R_Ein = 2.85″, with z_l = 0.0347. Table 3 prints that value as "Lens redshift (CMB frame) zl" and uses it for D_l ("From zl with WMAP7 cosmology"). The heliocentric 0.0339 is also printed.
- **MNELLS z_s.**
  - R27 prints "The pair of background emitters lie at z = 0.195" (§4.1).
  - R29, which measured the source, prints "zH = 0.19165" (§3; abstract) and zCMB = 0.19130 (§4).
  - Both are printed, and they are a real difference between the two sources, not between the readers. Q2 asks which redshifts the J0403 point uses.
- **CASTLES.**
  - B read only KKF98 (17 lenses). A read the union with K00 (34).
  - KKF98's ‡ lens redshifts (MG0414+0534 0.44, BRI0952−0115 0.99) are "Estimated median lens redshift … computed from the probability of producing the observed image separation". They are not measurements.
  - K00 prints z_l = 0.96 for MG0414+0534 and none for BRI0952−0115.
  - Below 0.30: Q2237+030 (0.04) and MG1549+3047 (0.11) and MG1654+1346 (0.25). FBQ0951+2635 has only the estimate z_FP = 0.21.
- **SuGOHI.** Notation only. All 23 lenses have printed z_d ≥ 0.458 (R57 Table 1, checked), so no system is below the cut.
- **NGC 6505.**
  - z_l: R30 prints both 0.04243 ± 0.00003 (§3.1, spectroscopic) and 0.041 ± 0.001 (§4.2, "cosmological redshift" after a peculiar-velocity correction). See Q13.
  - θ_E: the error is printed. R30 §5 reads "We measured an Einstein radius of θE = 2″.500 ± 0″.001". B recorded no error; A is right.
- **J0946+1006 (R66) radii.**
  - The readers agree on every value; A filed the tPIEMD radii as `R_e` rows, B put them in notes.
  - Table 2 (double Sérsic): r_eff 0.50 ± 0.10″ (n 2.34 ± 0.50) and 4.46 ± 0.50″ (n 1.60 ± 0.50).
  - Table 3 (double tPIEMD): r_c 0.066 ± 0.010″, r_t 0.50 ± 0.05″; r_c 0.082 ± 0.010″, r_t 6.05 ± 0.10″.
  - The Table 8 stellar masses use the tPIEMD description: "For the description of the photometry of the lens we use the double tPIEMD model" (§5). See Q7.

## 3. Facts settled at source (task 2)

### 3a. Stellar M/L: population (eligible, D-063 item 1) or lensing/dynamical (not eligible)?

| Record | Statement at source | Population M/L with named IMF? | Stellar mass printed? |
|---|---|---|---|
| R26 (Newman et al. 2017) | Table 1, section "Spectroscopic M∗/L": "(M∗/Lr)MW … 4.04 ± 0.10 … Kroupa IMF". §3: "where (M∗/Lr)MW is inferred from SPS modeling assuming a fiducial Kroupa (2001) IMF". §3: "We fit our higher quality IMACS spectra using the SPS models described in Section 6." | **Yes**: a spectroscopic SPS fit with a fixed Kroupa IMF (eligible). Not eligible as defaults: the lensing and dynamical M*/L in the same table ("(M∗/Lr)L+EAGLE", "(M∗/Lr)L+D") and the IMF-free spectroscopic fits (1PL, 2PL, 2PL+cut, non-parametric). | **No.** Only L_r,Ein = 2.84 ± 0.06 × 10¹⁰ L☉,r inside θEin = 2.85″ for SNL-0, and the M/L. |
| R29 (Collier, Smith & Lucey 2018b) | §4: "The reference mass-to-light ratio is estimated with Conroy et al. (2009) stellar population models accessed via ezgal … For a Kroupa (2001) IMF, with an old, solar metallicity stellar population (zform = 3), the models predict ΥRef = 2.90 ± 0.10. The uncertainty is derived from small variations in the metallicity and age (e.g. zform = 2.5–3.5, metallicity 1–1.5 solar)." | **Yes**: a population M/L for a named IMF from an assumed age and metallicity range, supported by a spectral fit ("age 12.0 ± 1.0 Gyr"). Eligible under D-063 item 1 as an assumed-range M/L. | **No population mass.** The printed "aperture stellar mass MEin∗ of 8.63 ± 0.54 × 10¹⁰ M⊙" is lensing minus an EAGLE dark-matter estimate ("which yields an aperture stellar mass"): not eligible. L_Ein = 2.59 ± 0.12 × 10¹⁰ L☉ (i) inside 1.47″. |
| R32 (Smith et al. 2020) | §5: "we used EzGal to derive the latter for stellar population models from Conroy, Gunn & White (2009), for metallicities 1.0–1.5× the solar value and ages 8–12 Gyr … our calculations adopt this as the 2σ interval, i.e. we assume Υref = 2.93±0.26. These assumptions are supported by fits of single-burst models from Conroy & van Dokkum (2012) to the Einstein-aperture spectra". Table 1 caption: "Υref is the expected stellar mass-to-light ratio for a Kroupa IMF". | **Yes**: an assumed age and metallicity range, Kroupa IMF (eligible, with the range carried). This settles the screening readers' dispute: the M/L is from an assumed range, and the spectral fit is a consistency check. | **No.** L_Ein printed (Table 1: 6.72 ± 0.10 and 5.56 ± 0.35 × 10¹⁰ L☉). |
| R61 (Collier, Smith & Lucey 2018) | §5: "with the spectroscopically fit Kroupa reference stellar mass-to-light ratio (Υref) (Newman et al. 2017, table 1) (converted to IF814W from the r-band, with ezgal)"; "With the converted Υref = 2.59". | **Yes**: R26's SPS M/L, converted in band (eligible). The ΥRap values (3.21, 2.49) are lensing-based: not eligible. | **No population mass.** "We obtain the stellar mass by subtracting the eagle DM mass contribution … from the lensing mass": lensing-based, not eligible. L_F814W(≤R_ap) printed (Table 1). Υref has no printed error. |
| R33 (Poci & Smith 2022) | §2.2: "the binned spectra were fit using the E-MILES SSP templates … with a fixed 'revised' Kroupa (2001) IMF"; "We used the resulting distribution of age and metallicity in each spatial bin to compute the F814W-band stellar mass-to-light ratio"; the per-Gaussian M*/L "converts the luminosity of that Gaussian into mass. The final set of scaled Gaussians represents a projected mass model, which we denote MGEΣ". | **Yes**: a spatially resolved SPS M/L with a fixed named IMF (eligible). The global Υ = 0.66 (Table 2) is a dynamical scaling: not eligible. | **A projected stellar-mass MGE** (Table A1, 11 Gaussians) is printed. No mass inside θEin. The printed "log10(M⋆/M⊙) = 11.23" (within r_max) and "11.01" (within R_e) are from the "intrinsic enclosed mass profiles" of the dynamical model: three-dimensional, and not eligible. |

### 3b. Cosmology statements

Only K00 (CASTLES) uses the word "flat", and it gives no single model. Every other source prints Ω_Λ = 1 − Ω_m, names a cosmology, or does neither, as listed.

| Record | Quoted statement | H0 | Ω_m | Flat |
|---|---|---|---|---|
| R5 (SLACS V) | "we assume a general-relativistic Friedmann-Robertson-Walker (FRW) cosmology with matter-density parameter ΩM = 0.3, vacuum energy-density parameter ΩΛ = 0.7, and Hubble parameter H0 = 70 km s−1 Mpc−1" (§1) | 70 | 0.3 | Ω_Λ = 0.7 = 1 − Ω_m printed; "flat" not stated |
| R13 (Grillo 2009) | "we assume a concordance cosmology with Hubble parameter H0 = 70 km s−1 Mpc−1, and matter and dark-energy density parameters Ωm = 0.3, ΩΛ = 0.7" (§1) | 70 | 0.3 | same |
| R7 (SLACS IX, alternative) | "a standard concordance cosmology with Ωm = 0.3 ΩΛ = 0.7 h = 0.7 is assumed" (§1) | 70 | 0.3 | same |
| R49 Grillo 2010 | "Throughout this work we assume H0 = 70 km s−1 Mpc−1, Ωm = 0.3, and ΩΛ = 0.7." (§1) | 70 | 0.3 | same |
| R49 Eichner 2012 | "The cosmological model adopted in this paper is parametrized by Ωm = 0.3, ΩΛ = 0.7, H0 = 70 km s−1 Mpc−1" (§1) | 70 | 0.3 | same |
| R66 | "values for the cosmological parameters: H0 = 70 km s−1 Mpc−1, ΩM = 0.3, ΩΛ = 0.7" (§1) | 70 | 0.3 | same |
| R10 (S4TM) | "we adopt a cosmological model with Ωm = 0.274, ΩΛ = 0.726 and H0 = 70 km s−1 Mpc−1 (WMAP7; Komatsu et al. 2011)" (§1) | 70 | 0.274 | Ω_Λ = 0.726 = 1 − Ω_m; not stated |
| R9 | "standard cosmology with Ωm = 0.274, ΩΛ = 0.726 and H0 = 70 km s−1 Mpc−1 (WMAP7, Komatsu et al. 2011)" | 70 | 0.274 | same |
| R20 (SL2S III) | "we assume a ΛCDM cosmology with matter and dark energy density Ωm = 0.3, ΩΛ = 0.7, and Hubble constant H0 = 70 km s−1 Mpc−1" (§1) | 70 | 0.3 | same |
| R21 (SL2S IV) | "We assume a concordance cosmology with matter and dark energy density Ωm = 0.3, ΩΛ = 0.7, and Hubble constant H0 = 70" (§1) | 70 | 0.3 | same |
| R28 (Smith & Lucey 2013) | "Where necessary, we adopt cosmological parameters from WMAP7: H0 = 70.4 km s−1 Mpc−1, Ωm = 0.272 and ΩΛ = 0.728" (§1) | 70.4 | 0.272 | same |
| R25 (SNELLS) | "we adopt cosmological parameters from WMAP7 where necessary, i.e. H0 = 70.4 km s−1 Mpc−1, Ωm = 0.272 and ΩΛ = 0.728" (§1) | 70.4 | 0.272 | same |
| R26 (Newman 2017) | **No cosmology stated.** "Throughout we adopt the distances, effective radii, and Einstein radii of the SNELLS lenses measured by S15." (§1); Table 1: "distance error not included" | via R25 | via R25 | by reference (Q4) |
| R61 | "We use parameters from the 7-year Wilkinson Microwave Anisotropy Probe (WMAP) when required, i.e. H0 = 70.4 km s−1 Mpc−1, Ωm = 0.272 and ΩΛ = 0.728" (§1) | 70.4 | 0.272 | Ω_Λ printed |
| R33 (Poci & Smith 2022) | "we assume the cosmology of the Wilkinson Microwave Anisotropy Probe (WMAP) 7-year experiment (Komatsu et al. 2011)" (§1). **Named, no numbers.** | — | — | not stated (Q4) |
| R29 | "We adopt cosmological parameters from the 7-year Wilkinson Microwave Anisotropy Probe (WMAP), i.e. H0 = 70.4 km s−1 Mpc−1, Ωm = 0.272 and ΩΛ = 0.728 (Komatsu et al. 2011), to calculate the lensing geometry for redshifts in the CMB frame" (§4) | 70.4 | 0.272 | Ω_Λ printed |
| R27 (MNELLS) | "In this paper we adopt cosmology from Planck Collaboration et al. (2018), i.e. H0 = 67.4 km s−1 Mpc−1, Ωm = 0.315 and ΩΛ = 0.685." (§1) | 67.4 | 0.315 | Ω_Λ printed |
| **R32 (MaNGA)** | "**We adopt the cosmological parameters from Planck Collaboration et al. (2018).**" (§1). No H0, Ω_m or Ω_Λ printed anywhere. | — | — | not stated (Q4) |
| R30 (NGC 6505) | "Throughout the paper we assume a Planck 2015 cosmology with H0 = 67.8 km s−1 Mpc−1 and Ωm = 0.308 (Planck Collaboration et al. 2016)." (§1) | 67.8 | 0.308 | **Ω_Λ not printed; flatness not stated** (Q4) |
| R36 KKF98 (CASTLES) | "We use H0 = 50 km s−1 Mpc−1 and consider several discrete values for Ω0 and λ0" (arXiv PDF p. 7) | 50 | several | no single model |
| R36 K00 | "The models were computed for H0 = 65 km s−1 Mpc−1 and three cosmological models (a flat cosmology with Ω0 = 1, a flat cosmology with Ω0 = 0.3 and λ0 = 0.7, and an open cosmology with Ω0 = 0.3)" (arXiv PDF p. 7) | 65 | three | no single model |

### 3c. R20 Table 7 column order: the MRT labels against the paper

- **Fact.** The journal MRT (`apj485108t7_mrt.txt`) labels its byte columns as follows:
  - bytes 26–30 `logMChab`;
  - bytes 37–41 `logMSalp`;
  - bytes 48–52 `logMChabNIR`;
  - bytes 59–63 `logMSalpNIR`.

  The arXiv v1 Table 7 header orders the same columns as log M∗(Chab), log M∗(Chab)(NIR), log M∗(Salp), log M∗(Salp)(NIR).
- **The data follow the paper.**
  - Of the 56 MRT rows, 30 have a value at bytes 26–30, bytes 37–41 blank, and a value at bytes 48–52. The paper says "For the systems with additional NIR observations the fit is repeated including those data" (§5). Under the paper's order, these 30 rows have an optical fit and no NIR fit, which is consistent.
  - Under the MRT labels, the same 30 rows would have a Chabrier-NIR mass but no Salpeter mass. That would be a NIR fit for systems the paper says have no NIR data.
  - Bytes 48–52 minus bytes 26–30 is 0.23–0.28 dex in every row. That is a Chabrier-to-Salpeter offset, not a NIR offset (the paper: optical and optical+NIR masses agree with "0.06 dex" scatter).
- **Settled.**
  - The column identity follows the paper header: bytes 37–41 are Chabrier (NIR) and bytes 48–52 are Salpeter (optical). The MRT labels for these two columns are swapped.
  - Both readers assigned the IMF from the paper header, and their values agree.
  - The values are the same in both versions; only the labels differ. Converters must take column identity from the paper header, not from the MRT labels.
  - The journal HTML table was not opened (the IOP article page has a bot check; see Disclosures).

## 4. Who can be plotted: systems with printed z_l below 0.30

These rules are applied, and nothing beyond them:
- REPRODUCTION.md "Who is plotted";
- A6S_PRECEDENCE §1–3;
- D-063, D-064 and D-066;
- the inventory §2 defaults per scope.

"Plottable" means every condition holds under the frozen text. Every row still depends on the gas question (Q14), which REPRODUCTION.md sends back to JvH before conversion.

Notes that apply to the whole table:
- **SLACS.** The three single-system scopes (J1538+5817, J1430+4105, J0946+1006) are R5 grade-A systems in R5 Table 5 and R13 (both readers, checked). They are listed once, under the defaults of their own scope.
- **SLACS cylinder.** For all 48 early-type systems, R13's θEin equals R5's b_SIE as printed (checked against VizieR). The R13 inside-R_E masses are therefore in exactly the R5 cylinder: "the disk defined by the Einstein radius of each lensing system" (R13 §4.2).
- **J1430+4105.** Eichner et al. 2012 models a nearby group halo as an external term: "including a galaxy group centred on galaxy I has only minor influence on the lens parameters" (§2, environment). That is one main deflector, so the system is A6 (D-063 item 6).
- **S4TM.** R10 prints a total only ("we have derived the total stellar mass of the S4TM lenses", abstract). The masses come from R9: "scaling of SSP models to HST I-band photometry", FSPS with "tform = 4 Gyrs, solar metallicity, and no dust" (R9 §5). The light fit R10 prints is its own de Vaucouleurs fit ("we also fit the two-dimensional elliptical de Vaucouleurs model … to derive some standardized quantities such as the effective radius", §3). R9's half-light radius "is derived from a core-Sérsic fit", which is not tabulated. See Q9.
- **SL2S default version.** "NIR version where available" follows the inventory §2 reading. Both grade-A systems below 0.30 have NIR fits.

| Survey | System | z_l | z_s | Kind (at source) | Spec. z | Observed default (aperture) | Stellar mass inside R_E or profile route | IMF variants | Cosmology | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| SLACS | J0029-0055 | 0.2270 | 0.9313 | E (R5 Mph) | yes (SDSS) | R5 θ_E 0.96″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 5 (−1 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 9; Kro-M05 3; Sal-M05 4 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0037-0942 | 0.1955 | 0.6322 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.53″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 13 (−5 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 22; Kro-M05 14; Sal-M05 22 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0044+0113 | 0.1196 | 0.1965 | E (R5 Mph) | yes (SDSS) | R5 θ_E 0.79″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 3 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 5; Kro-M05 4; Sal-M05 6 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0109+1500 | 0.2939 | 0.5248 | E (R5 Mph) | yes (SDSS) | R5 θ_E 0.69″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 8 (−2 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 14; Kro-M05 6; Sal-M05 10 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0252+0039 | 0.2803 | 0.9818 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.04″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 5 (−2 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 9; Kro-M05 5; Sal-M05 8 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0405-0455 | 0.0753 | 0.8098 | E (R5 Mph) | yes (SDSS) | R5 θ_E 0.80″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 1 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 2; Kro-M05 2; Sal-M05 2 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0728+3835 | 0.2058 | 0.6877 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.25″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 6 (−1 +3) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 10; Kro-M05 7; Sal-M05 9 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0822+2652 | 0.2414 | 0.5941 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.17″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 13 (−2 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 22; Kro-M05 12; Sal-M05 20 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0841+3824 | 0.1159 | 0.6567 | R5 Mph = L | yes (SDSS) | R5 θ_E 1.41″ | none: not in R13 (early-types only) | – | 70 / 0.3 / ΩΛ 0.7 | **Not plotted**: not early-type at source (D-063 item 6) |
| SLACS | J0912+0029 | 0.1642 | 0.3239 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.63″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 12 (−2 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 21; Kro-M05 14; Sal-M05 22 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0936+0913 | 0.1897 | 0.5880 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.09″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 6 (−1 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 11; Kro-M05 5; Sal-M05 9 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0946+1006 | 0.2219 | 0.6085 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.38″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 9 (−2 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 15; Kro-M05 8; Sal-M05 13 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Open (Q7)**: own-scope default R66 masses are per tPIEMD component; no frozen tPIEMD routine |
| SLACS | J0955+0101 | 0.1109 | 0.3159 | R5 Mph = L | yes (SDSS) | R5 θ_E 0.91″ | none: not in R13 (early-types only) | – | 70 / 0.3 / ΩΛ 0.7 | **Not plotted**: not early-type at source (D-063 item 6) |
| SLACS | J0956+5100 | 0.2405 | 0.4699 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.33″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 16 (−7 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 28; Kro-M05 15; Sal-M05 24 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0959+0410 | 0.1260 | 0.5350 | E (R5 Mph) | yes (SDSS) | R5 θ_E 0.99″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 3 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 5; Kro-M05 3; Sal-M05 5 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J0959+4416 | 0.2369 | 0.5315 | E (R5 Mph) | yes (SDSS) | R5 θ_E 0.96″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 9 (−2 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 14; Kro-M05 8; Sal-M05 14 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1016+3859 | 0.1679 | 0.4394 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.09″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 5 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 9; Kro-M05 5; Sal-M05 7 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1020+1122 | 0.2822 | 0.5530 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.20″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 10 (−3 +3) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 16; Kro-M05 8; Sal-M05 13 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1023+4230 | 0.1912 | 0.6960 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.41″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 10 (−2 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 17; Kro-M05 10; Sal-M05 15 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1029+0420 | 0.1045 | 0.6154 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.01″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 3 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 5; Kro-M05 4; Sal-M05 6 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1032+5322 | 0.1334 | 0.3290 | R5 Mph = L | yes (SDSS) | R5 θ_E 1.03″ | none: not in R13 (early-types only) | – | 70 / 0.3 / ΩΛ 0.7 | **Not plotted**: not early-type at source (D-063 item 6) |
| SLACS | J1103+5322 | 0.1582 | 0.7353 | R5 Mph = U | yes (SDSS) | R5 θ_E 1.02″ | none: not in R13 (early-types only) | – | 70 / 0.3 / ΩΛ 0.7 | **Not plotted**: not early-type at source (D-063 item 6) |
| SLACS | J1106+5228 | 0.0955 | 0.4069 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.23″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 5 (−1 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 9; Kro-M05 6; Sal-M05 8 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1112+0826 | 0.2730 | 0.6295 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.49″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 18 (−1 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 31; Kro-M05 19; Sal-M05 29 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1134+6027 | 0.1528 | 0.4742 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.10″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 5 (−2 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 8; Kro-M05 6; Sal-M05 9 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1142+1001 | 0.2218 | 0.5039 | E (R5 Mph) | yes (SDSS) | R5 θ_E 0.98″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 6 (−2 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 10; Kro-M05 6; Sal-M05 8 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1143-0144 | 0.1060 | 0.4019 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.68″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 5 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 9; Kro-M05 6; Sal-M05 10 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1153+4612 | 0.1797 | 0.8751 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.05″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 3 (−1 +3) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 6; Kro-M05 2; Sal-M05 4 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1204+0358 | 0.1644 | 0.6307 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.31″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 5 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 8; Kro-M05 4; Sal-M05 7 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1205+4910 | 0.2150 | 0.4808 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.22″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 9 (−3 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 15; Kro-M05 10; Sal-M05 16 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1213+6708 | 0.1229 | 0.6402 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.42″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 6 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 10; Kro-M05 7; Sal-M05 11 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1218+0830 | 0.1350 | 0.7172 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.45″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 6 (−1 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 10; Kro-M05 8; Sal-M05 12 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1250+0523 | 0.2318 | 0.7953 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.13″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 11 (−3 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 19; Kro-M05 11; Sal-M05 18 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1251-0208 | 0.2243 | 0.7843 | R5 Mph = L | yes (SDSS) | R5 θ_E 0.84″ | none: not in R13 (early-types only) | – | 70 / 0.3 / ΩΛ 0.7 | **Not plotted**: not early-type at source (D-063 item 6) |
| SLACS | J1402+6321 | 0.2046 | 0.4814 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.35″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 12 (−2 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 21; Kro-M05 13; Sal-M05 21 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1403+0006 | 0.1888 | 0.4730 | E (R5 Mph) | yes (SDSS) | R5 θ_E 0.83″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 5 (−2 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 8; Kro-M05 5; Sal-M05 8 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1416+5136 | 0.2987 | 0.8111 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.37″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 16 (−3 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 27; Kro-M05 15; Sal-M05 22 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1420+6019 | 0.0629 | 0.5351 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.04″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 2 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 4; Kro-M05 2; Sal-M05 3 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1430+4105 | 0.2850 | 0.5753 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.52″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 12 (−4 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 20; Kro-M05 11; Sal-M05 14 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14); own scope J1430+4105 has the same defaults (R5, R13) |
| SLACS | J1432+6317 | 0.1230 | 0.6643 | R5 Mph = L | yes (SDSS) | R5 θ_E 1.26″ | none: not in R13 (early-types only) | – | 70 / 0.3 / ΩΛ 0.7 | **Not plotted**: not early-type at source (D-063 item 6) |
| SLACS | J1436-0000 | 0.2852 | 0.8049 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.12″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 10 (−4 +3) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 18; Kro-M05 5; Sal-M05 8 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1443+0304 | 0.1338 | 0.4187 | E (R5 Mph) | yes (SDSS) | R5 θ_E 0.81″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 3 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 6; Kro-M05 4; Sal-M05 6 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1451-0239 | 0.1254 | 0.5203 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.04″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 5 (−3 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 8; Kro-M05 5; Sal-M05 8 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1531-0105 | 0.1596 | 0.7439 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.71″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 12 (−2 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 19; Kro-M05 12; Sal-M05 19 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1538+5817 | 0.1428 | 0.5312 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.00″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 4 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 8; Kro-M05 4; Sal-M05 6 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Open (Q6)**: own-scope default R49 prints a Salpeter total only, profile taken from R5 |
| SLACS | J1621+3931 | 0.2449 | 0.6021 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.29″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 12 (−4 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 22; Kro-M05 14; Sal-M05 19 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1627-0053 | 0.2076 | 0.5241 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.23″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 8 (−1 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 14; Kro-M05 7; Sal-M05 10 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1630+4520 | 0.2479 | 0.7933 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.78″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 19 (−2 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 34; Kro-M05 19; Sal-M05 30 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J1636+4707 | 0.2282 | 0.6745 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.09″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 6 (−2 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 10; Kro-M05 5; Sal-M05 8 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J2238-0754 | 0.1371 | 0.7126 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.27″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 5 (−2 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 8; Kro-M05 6; Sal-M05 9 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J2300+0022 | 0.2285 | 0.4635 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.24″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 10 (−2 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 18; Kro-M05 10; Sal-M05 15 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J2303+1422 | 0.1553 | 0.5170 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.62″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 10 (−1 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 17; Kro-M05 12; Sal-M05 18 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J2321-0939 | 0.0819 | 0.5324 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.60″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 6 (−1 +2) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 11; Kro-M05 8; Sal-M05 12 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| SLACS | J2341+0000 | 0.1860 | 0.8070 | E (R5 Mph) | yes (SDSS) | R5 θ_E 1.44″ → M_E computed (2% adopted error, R5 Table 3) | R13 M*(<R_E) Chab-BC03 9 (−4 +1) ×10¹⁰ M☉, inside R5 θ_E (exact match) | Sal-BC03 16; Kro-M05 10; Sal-M05 14 | R5 and R13: 70 / 0.3 / ΩΛ 0.7 | **Plottable** by the frozen rules (IMF pairing Q5, θ_E error Q12, gas Q14) |
| S4TM | J0143-1006 | 0.2210 | 1.1046 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.26 (θ_E 1.23″), no error | R10 total log M* 11.53 (Chab) × f(<R_E) from R10 de Vauc. R_eff 3.24″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J0159-0006 | 0.1584 | 0.7477 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.89 (θ_E 0.92″), no error | R10 total log M* 11.03 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.58″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J0753+3416 | 0.1371 | 0.9628 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.05 (θ_E 1.23″), no error | R10 total log M* 11.23 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.89″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J0754+1927 | 0.1534 | 0.7401 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.99 (θ_E 1.04″), no error | R10 total log M* 11.13 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.46″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J0757+1956 | 0.1206 | 0.8326 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.24 (θ_E 1.62″), no error | R10 total log M* 11.34 (Chab) × f(<R_E) from R10 de Vauc. R_eff 3.67″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J0826+5630 | 0.1318 | 1.2907 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.85 (θ_E 1.01″), no error | R10 total log M* 11.38 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.64″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J0847+2348 | 0.1551 | 0.5327 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.97 (θ_E 0.96″), no error | R10 total log M* 11.19 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.54″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J0851+0505 | 0.1276 | 0.6371 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.79 (θ_E 0.91″), no error | R10 total log M* 11.05 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.35″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J0920+3028 | 0.2881 | 0.3918 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.34 (θ_E 0.70″), no error | R10 total log M* 12.08 (Chab) × f(<R_E) from R10 de Vauc. R_eff 4.25″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J0956+5539 | 0.1959 | 0.8483 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.19 (θ_E 1.17″), no error | R10 total log M* 11.46 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.96″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1010+3124 | 0.1668 | 0.4245 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.21 (θ_E 1.14″), no error | R10 total log M* 11.68 (Chab) × f(<R_E) from R10 de Vauc. R_eff 3.26″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1031+3026 | 0.1671 | 0.7469 | E-U-A (E = early-type) | yes (SDSS) | R10 log M_E 10.88 (θ_E 0.88″), no error | R10 total log M* 11.22 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.04″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1040+3626 | 0.1225 | 0.2846 | E-U-A (E = early-type) | yes (SDSS) | R10 log M_E 10.54 (θ_E 0.59″), no error | R10 total log M* 10.99 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.30″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1041+0112 | 0.1006 | 0.2172 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.50 (θ_E 0.60″), no error | R10 total log M* 11.07 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.50″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1048+1313 | 0.1330 | 0.6679 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.03 (θ_E 1.18″), no error | R10 total log M* 11.22 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.90″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1051+4439 | 0.1634 | 0.5380 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.02 (θ_E 0.99″), no error | R10 total log M* 11.16 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.66″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1056+4141 | 0.1343 | 0.8318 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.59 (θ_E 0.72″), no error | R10 total log M* 11.12 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.81″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1101+1523 | 0.1780 | 0.5169 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.23 (θ_E 1.18″), no error | R10 total log M* 11.23 (Chab) × f(<R_E) from R10 de Vauc. R_eff 0.89″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1116+0729 | 0.1697 | 0.6860 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.83 (θ_E 0.82″), no error | R10 total log M* 11.29 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.44″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1127+2312 | 0.1303 | 0.3610 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.18 (θ_E 1.25″), no error | R10 total log M* 11.44 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.69″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1137+1818 | 0.1241 | 0.4627 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.12 (θ_E 1.29″), no error | R10 total log M* 11.31 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.79″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1142+2509 | 0.1640 | 0.6595 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.80 (θ_E 0.79″), no error | R10 total log M* 11.21 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.51″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1144+0436 | 0.1036 | 0.2551 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.68 (θ_E 0.76″), no error | R10 total log M* 10.74 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.22″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1213+2930 | 0.0906 | 0.5954 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.98 (θ_E 1.35″), no error | R10 total log M* 11.09 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.73″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1301+0834 | 0.0902 | 0.5331 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.72 (θ_E 1.00″), no error | R10 total log M* 10.92 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.25″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1330+1750 | 0.2074 | 0.3717 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.32 (θ_E 1.01″), no error | R10 total log M* 11.74 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.85″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1403+3309 | 0.0625 | 0.7720 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.55 (θ_E 1.02″), no error | R10 total log M* 10.78 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.00″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1430+6104 | 0.1688 | 0.6537 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.01 (θ_E 1.00″), no error | R10 total log M* 11.32 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.24″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1433+2835 | 0.0912 | 0.4115 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.12 (θ_E 1.53″), no error | R10 total log M* 11.45 (Chab) × f(<R_E) from R10 de Vauc. R_eff 3.23″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1541+3642 | 0.1406 | 0.7389 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.04 (θ_E 1.17″), no error | R10 total log M* 11.25 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.55″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1543+2202 | 0.2681 | 0.3966 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.32 (θ_E 0.78″), no error | R10 total log M* 11.74 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.32″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1550+2020 | 0.1351 | 0.3501 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.02 (θ_E 1.01″), no error | R10 total log M* 11.30 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.68″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1553+3004 | 0.1604 | 0.5663 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.86 (θ_E 0.84″), no error | R10 total log M* 11.26 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.15″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1607+2147 | 0.2089 | 0.4865 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.71 (θ_E 0.57″), no error | R10 total log M* 11.55 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.63″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J1633+1441 | 0.1281 | 0.5804 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.17 (θ_E 1.39″), no error | R10 total log M* 11.39 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.39″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J2309-0039 | 0.2905 | 1.0048 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 11.35 (θ_E 1.14″), no error | R10 total log M* 11.68 (Chab) × f(<R_E) from R10 de Vauc. R_eff 2.08″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| S4TM | J2324+0105 | 0.1899 | 0.2775 | E-S-A (E = early-type) | yes (SDSS) | R10 log M_E 10.97 (θ_E 0.59″), no error | R10 total log M* 11.32 (Chab) × f(<R_E) from R10 de Vauc. R_eff 1.10″ | Chabrier only; Salpeter top from FSPS model paper (Q11) | 70 / 0.274 / ΩΛ 0.726 | **Plottable** by the literal rule, flagged `mstar_in_RE_from_profile`, `no_uncertainty` (Q9 asks JvH to confirm) |
| SL2S | SL2SJ022511-045433 | 0.238 | 1.20 | grade A; sample 'massive early-type galaxies' (R21) | yes (R21 Table 2) | R20 θ_E 1.76 ± 0.05″ (SIE) → M_E computed | R20 total log M* 11.59 ± 0.07 (Chab, NIR) × f(<R_E), de Vauc. R_e 2.12″ CFHT / 2.28″ HST (Q10) | Salpeter NIR printed | 70 / 0.3 / ΩΛ 0.7 | **Plottable** via profile route (which R_e: Q10) |
| SL2S | SL2SJ084959-025142 | 0.274 | 2.09 | grade A; sample 'massive early-type galaxies' (R21) | yes (R21 Table 2) | R20 θ_E 1.16 ± 0.04″ (SIE) → M_E computed | R20 total log M* 11.27 ± 0.07 (Chab, NIR) × f(<R_E), de Vauc. R_e 1.34″ CFHT / 1.46″ HST (Q10) | Salpeter NIR printed | 70 / 0.3 / ΩΛ 0.7 | **Plottable** via profile route (which R_e: Q10) |
| SL2S | SL2SJ221929-001743 | 0.289 | 1.02 | grade B ('does not predict multiple images') | yes | R20 θ_E 0.52 ± 0.13″ | R20 Table 7 total | – | 70 / 0.3 | **Not plotted**: grade B is a probable, not a confirmed, lens (D-063 item 5) |
| SL2S | SL2SJ222012+010606 | 0.232 | 1.07 | grade C ('probably not strong') | yes | R20 θ_E 2.16 ± 0.07″ | R20 Table 7 total | – | 70 / 0.3 | **Not plotted**: grade C, not confirmed (D-063 item 5) |
| SNELLS | SNL-0 ESO 325-G004 | 0.0347 (CMB; helio 0.0339) | 2.141 | giant elliptical; group-dominant, single deflector | yes (6dF; X-Shooter) | R28 M_E 1.50 ± 0.06 ×10¹¹ M☉ inside R_E 2.85″ (MFL) | R26 L_r(<2.85″) 2.84 ± 0.06 ×10¹⁰ × (M*/L)_Kroupa 4.04 ± 0.10: same radius as R28 | Kroupa only; Salpeter top from model paper (Q11) | R28 70.4 / 0.272 / ΩΛ 0.728; R26 by reference to R25 (same) | **Open (Q3, Q4)**: stellar mass is L × M/L, not printed |
| SNELLS | SNL-1 ESO 286-G022 | 0.0312 | 0.926 | E/S0 | yes | R61 M(≤R_ap) 9.49 ± 0.15 ×10¹⁰ M☉, R_ap 2.38″ (= R25 half-separation R_Ein; R61 HST half-sep. 2.43″) | R33 MGE (Table A1), E-MILES, revised Kroupa | Kroupa only | R61 WMAP7; R33 WMAP7 (named, 'Komatsu et al. 2011') | **Not plotted under current rules**: R_ap not stated = R_E (Q1); no frozen MGE routine (Q8) |
| SNELLS | SNL-2 2MASX J0141−0735 | 0.0519 | 1.969 | elliptical (pair with edge-on companion) | yes | R61 M(≤R_ap) 12.59 ± 0.30 ×10¹⁰ M☉, R_ap 2.21″ (HST half-sep. 2.30″) | R61 L_F814W(≤R_ap) 3.86 ± 0.07 ×10¹⁰ × Υ_ref 2.59 (Kroupa, no error): same radius | Kroupa only | R61 70.4 / 0.272 / ΩΛ 0.728 | **Open (Q1, Q3)** |
| MNELLS | J0403−0239 | 0.06655 (R27); R29: 0.06604 helio, 0.06569 CMB | 0.195 (R27); 0.19165 / 0.19130 (R29) | giant elliptical, isolated | yes (MUSE) | R27 θ_E 1.49″ 'peak pixel' (no error, no M_E) | R29 L_i(<1.47″) 2.59 ± 0.12 ×10¹⁰ × Υ_Ref 2.90 ± 0.10 (Kroupa); n ≈ 4, R_e 5.7″ | Kroupa; R29 prints Salpeter α = 1.55 | R27 Planck 2018 67.4/0.315; R29 WMAP7 70.4/0.272 (mixed) | **Open (Q2, Q3)** |
| MaNGA | J1436+4943 | 0.125 | 1.231 | elliptical | yes (SDSS; IFU) | R32 M_E 28.2 ± 1.1 ×10¹⁰ M☉ inside R_E 4.72 ± 0.09 kpc (θ 2.03″) | R32 L_i(<R_E) 6.72 ± 0.10 ×10¹⁰ × Υ_ref 2.93 ± 0.26 (Kroupa, assumed 8–12 Gyr): same radius | Kroupa; R32 prints Salpeter α ≈ 1.65 | 'Planck Collaboration et al. (2018)', no numbers | **Open (Q3, Q4)** |
| MaNGA | J1701+3722 | 0.122 | 0.791 | elliptical | yes (SDSS; IFU) | R32 M_E 18.8 ± 3.7 ×10¹⁰ M☉ inside R_E 3.71 ± 0.37 kpc (θ 1.63″) | R32 L_i(<R_E) 5.56 ± 0.35 ×10¹⁰ × Υ_ref 2.93 ± 0.26 (Kroupa, assumed 8–12 Gyr): same radius | Kroupa; R32 prints Salpeter α ≈ 1.65 | 'Planck Collaboration et al. (2018)', no numbers | **Open (Q3, Q4)** |
| NGC 6505 | NGC 6505 | 0.04243 ± 0.00003 (cosmological 0.041 ± 0.001) | 0.4058 ± 0.003 | elliptical; single deflector | yes (DESI; KCWI) | R30 M_E 1.53 ×10¹¹ M☉ (no error) inside θ_E 2.500 ± 0.001″ | R30 M*_Chab(<θ_E) 1.06 ± 0.02 ×10¹¹ M☉, printed inside R_E | Chabrier; R30 prints ÷0.61 for Salpeter (Q11) | 67.8 / 0.308; ΩΛ, flatness not printed (Q4) | **Plottable** (minor: Q4, Q11, Q13) |
| CASTLES | Q2237+030 | 0.04 | 1.69 | bulge of a spiral (late-type) | z_l, z_s printed; method not stated | R36 K00 only | none | – | H0 65 (K00) | **Not plotted**: late-type (D-063 item 6) |
| CASTLES | MG1549+3047 | 0.11 | none printed | FP sample (early-type) | no z_s | R36 critical radius | none (not in R41) | – | H0 50, several Ω0 | **Not plotted**: no source redshift |
| CASTLES | MG1654+1346 | 0.25 | 1.74 | not stated per system | not stated | R36 critical radius (no M_E) | none (not in R41) | – | H0 50, several Ω0 (no single cosmology) | **Not plotted**: no stellar-mass default |
| CASTLES | FBQ0951+2635 | none (z_FP 0.21 estimate) | 1.24 | not stated | no measured z_l | – | none | – | – | **Not plotted**: lens redshift is a fundamental-plane estimate |

Counts (z_l < 0.30):

| Survey | Below 0.30 | Plottable by the frozen rules | Open (question) | Not plotted |
|---|---|---|---|---|
| SLACS | 54 | 46 | 2 (J1538+5817 Q6; J0946+1006 Q7) | 6 (morphology L or U) |
| S4TM | 37 | 37 (Q9 asks JvH to confirm the profile route) | 0 | 0 |
| SL2S | 4 | 2 | 0 | 2 (grades B, C) |
| SNELLS | 3 | 0 | 2 (SNL-0; SNL-2) | 1 (SNL-1: R_ap and MGE; becomes open if Q1 and Q8 are ruled yes) |
| MNELLS | 1 | 0 | 1 | 0 |
| MaNGA | 2 | 0 | 2 | 0 |
| NGC 6505 | 1 | 1 | 0 | 0 |
| CASTLES | 3 (+1 with only an estimate) | 0 | 0 | 4 |
| SuGOHI III, KiDS J0233, Cosmic Horseshoe, J0100+1818 | 0 | — | — | — |
| **Total** | **105 (+1)** | **86** | **7** | **13** |

## 5. Gas (§3.4)

The frozen rule (REPRODUCTION.md; A6S_PRECEDENCE §3.4):
- "A system-level statement or limit where the source gives one (for example ESO 325-G004)."
- Otherwise "a cited, quoted statement for the kind on gas inside the Einstein radius of early-type galaxies, read at source before conversion".
- "If no such statement is found, the cell returns to JvH."

### System-level statements

| System(s) | Record | Statement (quoted at source) | Judgement |
|---|---|---|---|
| SNL-0 | R28 footnote 3 | "In principle, there are also contributions from gas and from a central supermassive black hole. We assume the gas mass projected within the Einstein radius is negligible. This is equivalent to assuming all gas is initially converted into stars, and that the gas lost in winds and supernovae is either recycled into further generations of stars or else expelled into a hot, low-density halo." | **Qualifies under the letter.** It is a system-level statement, and it is the frozen rule's own example. It is an **assumption**, not a measurement or a limit. |
| SNL-0, SNL-1, SNL-2 | R25 §4 | "Other possible non-stellar mass contributions within the Einstein radius, e.g. gas and central black holes, are neglected. We implicitly assume that all gas lost during stellar evolution has either been heated and dispersed into a low-density halo or else recycled into subsequent generations of stars" | **Qualifies by the same reading** (system level, inside the Einstein radius). An assumption. |
| J1436+4943, J1701+3722 | R32 §5 | "which includes contributions from dark matter (and in principle from a central black hole, gas, etc but these are expected to be negligible)" | **Qualifies by the same reading.** An expectation, not a measurement. |
| SNL-1 | R61 §3 | "This suggests the presence of a small cold ISM disc." (dust in the central ~1″) | Does not qualify. It is evidence that **some gas is present**, not quantified. |
| SNL-1 | R26 §6 | "nebular emission in SNL-1, which is likely driven by the presence of warm gas" | Does not qualify. Gas present, no mass. |
| J0403−0239 | R29 §4 | "both are contaminated by gas emission, to different extent" (Hα, Hβ in the Einstein-aperture spectrum) | Does not qualify. Gas present, no mass. |
| NGC 6505 | R30 §4.3 | "Henry et al. (1995) find evidence in X-ray emission that the galaxy is part of a small group" | Does not qualify. Nothing inside θ_E. |
| J1430+4105 | Eichner et al. 2012 §4.2 | gas "needs to be incorporated in either the dark matter or the de Vaucouleurs component"; cites Young et al. 2011 for M(H2) ≲ 10⁹ M⊙, "less than 1% of the total galaxy masses derived here", and Sanderson et al. 2003 for hot gas that "can contribute up to 10% of the total mass in the centre"; "the uncertainty of our mass estimates due to the neglected gas is ≈ 10%" | Does not qualify as "absent". It is a cited, quantified statement that gas **may be up to ~10%**, for groups and cluster centres. |
| SLACS, S4TM, SL2S | R5, R13, R10, R20, R21 | none (both readers searched; R5 §5.2 has only "any significant gas mass be well aligned") | Nothing to judge. |

### Statements for the kind (literature)

None of these is about gas **inside the Einstein radius**. Each is unquantified or describes the whole galaxy.

| Source | Statement (quoted) | Judgement |
|---|---|---|
| R31 Wang et al. 2026 §1 | "In most cases, the gas content in elliptical galaxies can be safely neglected (Mamon & Łokas 2005; Diehl & Statler 2007; Grillo et al. 2013)" | Cited and for the kind, but for the whole galaxy, unquantified and hedged ("in most cases"). Does not meet "inside the Einstein radius". |
| R37 Ferreras et al. 2008 §3 | "Other baryonic components, hot and cold gas or dust, are known to contribute a small fraction to the net baryon budget in these systems (Roberts & Haynes 1994)." | Same. The cited source was not located. |
| R64 Treu et al. 2010 §2.1 (X record) | "X-ray observations show that the residual gas is a small fraction of the stellar mass (e.g. Mathews & Brighenti 2003; Humphrey et al. 2006)" | Whole galaxy, unquantified. |
| Mathews & Brighenti 2003 §2 | "the total mass of hot gas in massive E galaxies varies up to at least several 10¹⁰ M⊙ or about ≲ 1 percent of the total stellar mass" | Quantified, but for the whole galaxy and hot gas only. The same review (§7) reports central molecular discs "of mass 10⁷ − 10⁹ M⊙" in a small number of E galaxies (read by reader A; not re-read here). |
| Young et al. 2011 (abstract) | "The overall CO detection rate is 56/259 = 0.22 ±0.03"; a few galaxies with H2 masses "≳ 10⁹ M⊙" | Whole galaxy, molecular only. |
| Serra et al. 2012 (abstract) | HI "small discs (M(H I) < 10⁸ M⊙), which are confined within the stellar body" | Whole galaxy, HI only. |
| Diehl & Statler 2007 | No gas-mass statement found (both readers) | — |

### Verdict

- No literature statement read so far meets the rule: none concerns gas inside the Einstein radius of early-type galaxies.
- The only qualifying statements are the three system-level **assumptions** above (R28, R25, R32), which cover SNL-0, SNL-1, SNL-2, J1436+4943 and J1701+3722.
- For the other systems (SLACS, S4TM, SL2S, NGC 6505, J0403−0239), **the cell returns to JvH**, as REPRODUCTION.md requires.
- Two sources state that gas is present in specific lenses (R61 and R26 for SNL-1; R29 for J0403−0239), and one says it may reach ~10% (Eichner et al. 2012). A label of "absent" would therefore overstate what is known. See Q14.

## 6. Questions for JvH

Each question gives options and a recommendation. Nothing is decided here.

What the adjudicator had seen when writing them:
- the input values (masses, radii, M/L) were read at source;
- no g_obs, g_bar or ratio was computed;
- no plot was made.

**Q1. SNELLS R_ap (SNL-1, SNL-2).**
- R61 measures its adopted masses "within the fiducial radius, Rap" (Table 2 caption), with R_ap = 2.38″ and 2.21″, "the half-image separation derived by SLC15" (§3).
- R25 prints those same numbers as its Einstein radii: Table 2 "REin … 0.5×image-separation for SNL-1,2"; §4 "For SNL-1 and SNL-2, we approximate REin by half the image separation".
- R61 never states that R_ap equals the Einstein radius. Its own HST half-separations are 2.43 ± 0.03″ and 2.30 ± 0.03″.
- REPRODUCTION.md: "unless the source states that the aperture equals R_E".

Options:
- (a) Treat R_ap as R_E, because R25 (the cited origin) prints it as its Einstein radius. Flag the point `model_dependence: "aperture = SLC15 half-image separation (D-063 item 2); mass from R61's full model"`.
- (b) Literal rule: record, not plotted.
- (c) Use R25's own M_Ein at the same radius as the observed side (an alternative record).

*Recommendation: (a).* For SNL-2 both masses are printed inside the same R_ap, so the cylinder match that D-064 needs is exact. It would be logged as a decision that reads R25 as "the source" for the aperture.

**Q2. J0403−0239 (MNELLS).** R27 is the observed default by §2.3 (most recent). What it prints:
- "the peak pixel REin is 1.49 arcsec, which is 0.5 per cent larger than the same measurement in the MUSE data" (§4.1). As printed, 1.49 against 1.47 is 1.4%, not 0.5%.
- No mass profile is named, no error is given and no M_E is printed. It says "This changes our mass-measurement by less than 2 per cent".
- z = 0.06655 and z_s = 0.195, and the Planck 2018 cosmology.

R29, which measured both redshifts, prints:
- R_E = 1.47 ± 0.03″ (half separation);
- M_Ein = 10.64 × 10¹⁰ M⊙ with the error revised to "∼4 per cent, i.e. 0.4 × 10¹⁰ M⊙";
- L_Ein inside 1.47″;
- WMAP7 cosmology and CMB-frame redshifts 0.06569 and 0.19130.

Options:
- (a) Literal: M_E from R27's θ_E with R27's redshifts and cosmology. Move R29's luminosity from 1.47″ to 1.49″ with the "n ≈ 4", R_e = 5.7″ profile (flagged). The stellar mass then stays in WMAP7 distances, so the cosmologies are mixed (see Q4).
- (b) As (a), but with R29's measured redshifts.
- (c) Use R29's matched pair as the default for this system (same radius, cosmology and redshifts; no profile step), with R27's 1.49″ as the alternative. Grounds: §2.3's re-use clause, since R27 says "the only change in constraints relative to the earlier analysis is that the peak pixel REin is 1.49 arcsec".

*Recommendation: (c).* It is the only option with one cylinder, one cosmology and measured redshifts. R27 itself reports that its update changes the mass by less than 2%.

**Q3. Stellar mass as luminosity × M/L** (SNL-0 R26, SNL-2 R61, J0403 R29, MaNGA R32).
- D-063 item 1 accepts "a photometric luminosity times a stellar-population M/L fitted to spectra" as the input.
- REPRODUCTION.md says "the default record's value as printed", and its Test 3 list of recomputed quantities has no product.

Options:
- (a) M* = L × Υ, computed by package code, flagged `mstar_from_L_times_ML`. Printed errors are combined in quadrature, and R61's Υref = 2.59 carries `no_uncertainty`. The product is added to Test 3.
- (b) Record, not plotted.

*Recommendation: (a)*, because it is exactly the input D-063 item 1 accepted.

**Q4. Cosmology stated by reference, by name only, or incompletely.**
- R26 states none and adopts R25's distances (R25 states WMAP7 numbers).
- R33 names WMAP7 without numbers.
- R32 names "Planck Collaboration et al. (2018)" without numbers. It prints R_Ein in kpc, M_Ein and L_Ein, so no distance needs computing.
- R30 prints H0 and Ω_m only.
- Every other source prints Ω_Λ = 1 − Ω_m but never the word "flat".

Options:
- (a) Accept the following:
  - printed Ω_Λ = 1 − Ω_m as flat;
  - R26 → R25's numbers;
  - R32's printed R_Ein (kpc), M_Ein and L_Ein used directly, with no distance recomputed. The cosmology is recorded as "Planck 2018, named; numbers not printed", and `R_E_printed_kpc` is flagged, a stated departure from "R_E = θ_E D_l by the frozen code";
  - R30 taken as flat with its printed H0 and Ω_m, flagged "flatness not stated". M_E is printed, so this affects R_E only.
- (b) Strict: record, not plotted, wherever numbers are not printed (MaNGA ×2; SNL-0 through R26).

*Recommendation: (a).* None of these choices changes g_obs/g_bar to first order (D-064 item 4), and each is visible in the record.
- One exception needs its own flag: J0403 under Q2 option (a) or (b) mixes cosmologies. There a luminosity-based mass scales as D_l², so the ratio would not be invariant.

**Q5. SLACS (R13) default IMF and model.** R13 prints Chabrier only with BC03, Kroupa only with Maraston 2005, and Salpeter with both: "We adopt a Salpeter … and a Chabrier … IMF for Bruzual & Charlot models and a Salpeter and a Kroupa … IMF for Maraston models" (§3). §3.2 says "Chabrier or Kroupa".

Options:
- (a) Chabrier–BC03 as the default, Salpeter–BC03 as the top, and the M05 pair as a model alternative.
- (b) Kroupa–M05 as the default, Salpeter–M05 as the top.

*Recommendation: (a).* Pairing within one population model isolates the IMF. BC03 is also the model of the other SPS defaults that name one (R20, R66, R49).

**Q6. J1538+5817.** The own-scope stellar default (R49, Grillo et al. 2010) has two problems:
- It prints only a total, "20 (+1 −4) × 10¹⁰ M⊙", for "a Salpeter initial mass function". There is no Chabrier or Kroupa value.
- Its θe = 1.58″ is cited from Bolton et al. 2008 (R5; Table 1 "References – Bolton et al. 2008"), so it is not its own fit.

R13 prints Chabrier inside R5's θ_E for this system.

Options:
- (a) R13 as the default for this system, with R49 as the alternative.
- (b) R49 × a de Vaucouleurs fraction from R5's θe, Salpeter only.
- (c) Record, not plotted.

*Recommendation: (a).* R49 cannot supply the Chabrier or Kroupa default that §3.2 requires, nor its own profile (§3.1).

**Q7. J0946+1006.**
- The own-scope stellar default (R66) prints Chabrier and Salpeter masses per **tPIEMD** component (Table 8; Table 3 profile). The frozen `sersic_projected_fraction` cannot evaluate tPIEMD components.
- R66's double-Sérsic components (Table 2) are a different decomposition: different magnitudes per component. R66 notes "The logarithm of the stellar masses changes by 0.06 if we use the description of the light profile with Sérsic components instead of tPIEMDs".
- R13 prints Chabrier inside R5's θ_E.

Options:
- (a) Write, test and freeze a tPIEMD projected-fraction routine (closed form, with an elliptical-to-circular-aperture convention). Apply it per component to the Table 8 masses, flagged. R13 is shown as the alternative and serves as the "profile step" report. Until the routine is frozen, record, not plotted.
- (b) R13 as the default.
- (c) Sérsic fractions applied to the tPIEMD component masses (mismatched components).

*Recommendation: (a)*, frozen in the same code PR as Q8. It keeps the frozen ranking and uses the source's own decomposition.

**Q8. SNL-1 MGE (R33).** REPRODUCTION.md: "A multi-Gaussian (MGE) model is evaluated only if a frozen MGE routine exists".

Options:
- (a) Write, test (against analytic circular cases) and freeze an MGE cylinder-mass routine, then package R33 Table A1 MGEΣ.
- (b) Record SNL-1, not plotted, in v1.

*Recommendation: (a)*, together with Q7. SNL-1 still needs Q1.

**Q9. S4TM profile route.** R10's total mass comes from R9's I-band photometry of a core-Sérsic fit, which is not tabulated. The only per-lens profile printed is R10's own de Vaucouleurs fit, with R_eff "in the intermediate axis convention".

Options:
- (a) Apply R10's de Vaucouleurs fit (the source's own printed fit, as §3.1 reads), flagged `mstar_in_RE_from_profile` and `profile_differs_from_mass_photometry`.
- (b) Record, not plotted, until a per-lens core-Sérsic table is found.

*Recommendation: (a)*, with the flag shown on each point.

**Q10. SL2S: which R_e.** R20 prints two de Vaucouleurs fits:
- CFHT (Table 4, "typical uncertainty … 30% on the effective radii"). Its magnitudes produced the SPS masses.
- HST (Table 5, with a stated ~10% systematic).

Options:
- (a) CFHT as the default, HST as the alternative.
- (b) HST as the default.

*Recommendation: (a)*, because it keeps the light profile and the mass from the same photometry.

**Q11. Salpeter top for single-IMF sources (§3.2).** Some sources print their own conversion:
- R29: "a Salpeter IMF … has α = 1.55" (relative to its Kroupa ΥRef);
- R32: "α ≈ 1.65 for an unbroken power-law IMF with the Salpeter (1955) slope";
- R30: divide Chabrier masses "with a constant factor of 0.61".

Others print none:
- R26 and R61 (R26's 1.53 is a Vazdekis-model convention for converting other authors' results);
- R10 and R9 (FSPS; Salpeter shown only in R9 Fig. 9).

Options:
- (a) Use the source's printed ratio where it exists (registered with the quote), and read the model paper where it does not.
- (b) Always use the model paper.

*Recommendation: (a).*

**Q12. Sample-level errors.** R5 prints no per-lens θ_E error. Its Table 3 gives "Adopted Empirical Error" 2% for the Einstein radius b ("we will adopt a 2% RMS fractional error", §6.1).

Options:
- (a) Carry 2%, flagged `sample_level_error`.
- (b) `no_uncertainty`.

*Recommendation: (a).* The cases where no error is printed at all (R10 b_SIE, M_E and M*; R28 θ_E; R30 M_E; R61 Υref) are settled by the rule: `no_uncertainty`.

**Q13. NGC 6505 lens redshift for distances.** R30 prints both z_d = 0.04243 ± 0.00003 (§3.1) and "a cosmological redshift of z = 0.041 ± 0.001" (§4.2). It does not say which it used for "2.1 kpc at the redshift of the lens".

Options:
- (a) Use 0.04243 (the spectroscopic measurement) for R_E, with 0.041 shown as the alternative.
- (b) Use 0.041.

*Recommendation: (a).* It is the printed spectroscopic redshift that the rules name. The choice moves R_E by about 3.5% and both g values together; it does not change the ratio.

**Q14. Gas (the cell returns to JvH).**

Options:
- (a) Label honestly:
  - SNL-0, SNL-1, SNL-2, J1436+4943 and J1701+3722: "gas inside R_E assumed negligible by the source (assumption, not a measurement)", with the quote;
  - every other system: "gas inside R_E not measured; not included";
  - g_bar labelled "stars only";
  - the statements that gas is present (R61, R26, R29) and Eichner's "up to 10%" shown in the notes.
- (b) Build a quantified assumption range for the kind from whole-galaxy figures (Mathews & Brighenti 2003 ≲1% hot gas; Young et al. 2011 H2; Serra et al. 2012 HI), applied to the cylinder. This is a new rule. These are not limits inside R_E, and central molecular discs make a whole-galaxy fraction an unsafe bound for a central cylinder.
- (c) Hold the cell until a source on gas inside Einstein radii is found.

*Recommendation: (a).* It states only what was measured, keeps the baseline as detected baryons, and does not mark gas "absent" where sources report gas present.

## 7. Source inconsistencies noted (facts, no action)

- **R20 Table 7.** The MRT labels for bytes 37–41 and 48–52 are swapped against the paper (§3c).
- **R20 Table 6.** The MRT labels the Einstein-radius column `Reff` (its explanation reads "Einstein radius").
- **R27 §4.1.** "1.49 arcsec, which is 0.5 per cent larger" than 1.47″ (R29); as printed, the difference is 1.4%. R27's z_s = 0.195 differs from R29's measured 0.19165.
- **R29.** It prints M_Ein = 10.64 ± 0.23 × 10¹⁰ M⊙ and then revises the error to 0.4 × 10¹⁰. Both readers recorded 0.23 with a note; the adjudicated error is 0.4.
- **R32.** The text refers to "Table 5", but the table is numbered Table 1 in arXiv v1.
- **Tu et al. 2009** (SL2SJ02176−0513). The abstract prints z_lens = 0.656 and Table 1 prints 0.6459 ± 0.0003 (both readers). This is above the cut.
- **R36.** The two CASTLES papers print B0712+472 z_s as 1.33 (KKF98) and 1.34 (K00).

## 8. Disclosures

- **AI assistance.** Prepared by Claude (AI) for JvH. Every quote above was taken from `pdftotext` output of the file listed in the Appendix, and checked by eye against the surrounding text. The classifications, the plot table and the questions are Claude's. JvH rules on the questions.
- **Data seen.**
  - Every packaged input value of the systems below 0.30 was read: Einstein radii and masses, stellar masses, M/L, luminosities and profile parameters.
  - No g_obs, g_bar or ratio was computed. No plot was made. The plot verdicts depend only on the rule conditions, not on any value.
- **Comparison script.** v2 (`compare_readings_v2.py`) was written after the v1 output was seen and before this adjudication, as its docstring states. Its changes are to matching only. It does not compare text quantities; see §2 for the checks made by hand.
- **Version labels.**
  - R5, R13: VizieR (vizier.cfa.harvard.edu `asu-tsv`).
  - R10, R20: journal tables (content.cld.iop.org).
  - Everything else: arXiv PDFs at the versions listed in §2.
  - The journal versions of MNRAS and A&A papers were not opened (the inventory records those sites as refusing this workspace).
- **Access.** No user-agent was changed and no bot check was approached. IOP article pages were not opened. vizier.cfa.harvard.edu and content.cld.iop.org answered default curl requests.
- **Not verified.**
  - The journal HTML of R20 Table 7.
  - Roberts & Haynes 1994 (not located).
  - Mathews & Brighenti 2003 §7.2 (the molecular-disc figures are as reader A quoted them; not re-read).
  - The values of R33 Table A1 (both readers transcribed it; not checked here, since SNL-1 is not plotted under current rules).
  - The above-cut values in the KiDS, Cosmic Horseshoe and J0100+1818 scopes, beyond redshifts.
- **Outputs.**
  - `adjudicated_inputs.csv` holds values read at source, with their locations. The `status` column marks defaults, alternatives, record-only rows and rows pending a question.
  - Values pending a question are not defaults until JvH rules.
- **Next step.** JvH rules Q1–Q14. Then the decisions are logged and the code PR for Q3 (product), Q7 (tPIEMD) and Q8 (MGE) is written and frozen. Conversion starts only after that.

## Appendix: sources opened by the adjudicator (SHA-256)

Kept in the session scratchpad (`a6adj/dl/`), not in the repository. PDFs are `https://arxiv.org/pdf/<id>`, with `_` standing for `/` in old-style ids. `vz_*` files are VizieR `asu-tsv` exports. `iop_*` files are content.cld.iop.org tables.

| File | SHA-256 |
|---|---|
| `0710.3159.pdf` | `565799d2aca9419c2c4d9814b31e34df974e4378c092bed3db4b990e465cfc0b` |
| `0805.1931.pdf` | `bfe4a042dbfcfac2d0ed49a7fdf155ff777de3bf1b06edd8aca6db5d815d4a96` |
| `0904.3282.pdf` | `df3746887007595b00e7fb2564ae1e9121e95849c68c04e55d2a06e3324587cf` |
| `0911.2471.pdf` | `31f2d6b38c8143a9d8216a0cdfda3ca95e7f5536d3f784f479f47c01228e1668` |
| `0911.3392.pdf` | `410e2e7368f03c98f1cc98719233064853b9166f0f24afcce0461806bcdb75c7` |
| `0912.0744.pdf` | `be9bc2b897256188b9aefcb0b2713f703ed69eab95099ffd834ee26d66443b7c` |
| `1007.2880.pdf` | `72308349c88a32c1932478f4a0653f22f4feb51cd29e5ce060941c0eb25db5d8` |
| `1102.3433.pdf` | `17084d0aeee4da425fd18edd611dc6dad5bf44579ee1519c95e8ada85abc9775` |
| `1102.4633.pdf` | `83a0a162724cc31292a92c74dbb3dc6e4f5a1f14d103ed9321694a57a2076753` |
| `1111.4215.pdf` | `cb75508f8dbfe31543d2a43d43efa6482dcc42889277b08383fa121fabc8d72c` |
| `1111.4241.pdf` | `da31581734759374d9fa516bfb69f0eb486ffee2106efde9c2b829aef0b41be4` |
| `1209.2140.pdf` | `9af0df3615bbcde44a0e1b1aaaee4c216b0149bdc2870ff7c24459b02b15b1d9` |
| `1306.4983.pdf` | `d719b53e79ec224c03677cb0b880d3b77ac8b9a3f2bcafec90d7cf574190236d` |
| `1307.4759.pdf` | `03e3818848a9b1d169ebf301b453699720a9fdd878103886cd5b79de3494081e` |
| `1307.4764.pdf` | `95dd93ea5ee9d303ea63c0ef2a5bc4c7df6debdeea8ae3fdb6531b471d40d4d1` |
| `1407.2240.pdf` | `f53c4026d226980310117105c9b92b482996bc5803788246bc0c109575165481` |
| `1503.02661.pdf` | `b6d67d236133a9e7d4e80d22f2d027748a8d32539e5877d5395c96ed8ea89d0e` |
| `1608.01967.pdf` | `06f2781498d94f863410ee535a7c62da8a2480a79f459c333675c6cccd0ec6eb` |
| `1612.00065.pdf` | `542370972c06f894fa4f16658a2aee698a3e01410ea8652ee52e36f19febcff9` |
| `1709.01931.pdf` | `8b9a54259f783f5b843fcfeca20b1d67e0fb2c4af4f1cc1174b571e2c5436552` |
| `1711.00072.pdf` | `062808fc803780906933f5c6e7d21f3b613ed2f6b91c7c5a8d7e25cfea5e42b5` |
| `1803.07082.pdf` | `240f01b5b90632642a38029702b4fd663df9e035b0826941b14f535fc6bdd604` |
| `1904.10465.pdf` | `c39903d55f371bd46e0297e9a86391cf4420aa90ea40fb2083c1d2f2ccdfd191` |
| `1911.06338.pdf` | `9c08bcb07a8c21d07e6dcca1d8ce200a98b52fd26148f3324feb0cff046aa02b` |
| `2002.07191.pdf` | `6465636a5be7989f556b6f9eb2d8b6acb83ad1f3de2a4c1f8d584e11af4ab26d` |
| `2203.09309.pdf` | `92fc46a03b616e627346ff9aea938e7c3b1ac1efdddef8bda9d6909c9106e64e` |
| `2502.06505.pdf` | `0b593fc45bd284b7906fda3e35323d9779695448da9bcd930978ffdedea41dd6` |
| `2603.26894.pdf` | `bb39d93d14baeb08806f6807c114a19f405e11126964f8c996909ac70ee6c545` |
| `astro-ph_0309553.pdf` | `0c47e181ff9dbea2672bd06bcdf317382f57e4ff07b86e7821f46ee1f9cb43bb` |
| `astro-ph_0504453.pdf` | `2d601ec97a94e0686527456657f271302caf1558f3ae459b3d187d7696cf495a` |
| `astro-ph_9708161.pdf` | `fce85fe777592a87a3468160463b7e5c815de9f2f8616dc2eb5521cf9cf9e1b2` |
| `astro-ph_9909018.pdf` | `bb7c1ec2ffec8bf6c8067cfeab1056b42bdcc408252e8228588c0394dcbf6ae2` |
| `iop_apj485108t4_mrt.txt` | `261fe9e05dcbaed986889e47c91ec9cce571cd0f6c7504efcded970060f8dfa5` |
| `iop_apj485108t6_mrt.txt` | `3c824245e6c0a5cafbe3036171fb70169697831c3bd76619afd5515b71af60f5` |
| `iop_apj485108t7_mrt.txt` | `c6319d4f682eb2f4de25617c03d65636fd51df466aca1ef6afa3f8f99d175f02` |
| `iop_apjaa9794t1_ascii.txt` | `6af826bf2f6e4a0d4804c12e97c72ba56fefc619be3c4b0ad143cef38301a22d` |
| `iop_apjaa9794t2_ascii.txt` | `497ca1aaf3bd3b9c546eb4f0e1ae40bfbac48fa384ee8a623ed293ecfba439ed` |
| `vz_R13_lens.tsv` | `37ef7bc1247df1afa7a83df7302825f72b1004894998f88ddc0d41adc077b338` |
| `vz_R5_t4.tsv` | `2851a7ab9592f89c913c2d1ab24b2018a5d8b998d70f5c097d23d2fc70462be0` |
| `vz_R5_t5.tsv` | `4a8388060afd70e9c3a6a1c3ff1ee0ee0e5f78c4c759f0305261cfd4d6dc56b4` |
