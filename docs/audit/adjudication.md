# Audit v2: adjudication (plan §2.8)

**Adjudicated by Claude, not blind.** Claude prepared the reader packets and could see the Atlas values while adjudicating. Every non-"agree" row is settled here, with what was read and where. The codes from `compare.py` stand as observed (`run_v2/comparison.csv`), and nothing is re-scored.

## Codes as observed

| Stratum | agree | reader disagreement | Atlas discrepancy | method incomplete | unreadable | n |
|---|---:|---:|---:|---:|---:|---:|
| aeg-d-sparc/v1 | 0 | 0 | 0 | 170 | 0 | 170 |
| aeg-d-xcop/v1 | 44 | 0 | 0 | 0 | 0 | 44 |
| aeg-d-kids1000-rar/v1 | 0 | 0 | 0 | 10 | 0 | 10 |
| aeg-d-strong-lensing/v1 | 0 | 0 | 0 | 10 | 0 | 10 |
| aeg-d-gc-baumgardt/v1 | 0 | 0 | 0 | 10 | 0 | 10 |
| aeg-d-dwarfs/v1 | 0 | 0 | 0 | 10 | 0 | 10 |
| **all** | **44** | 0 | 0 | **210** | 0 | 254 |

## How the 210 "method incomplete" rows were settled

Plan §2.8 makes "method incomplete" a finding against the methods text, even when the Atlas value is right. Whether each Atlas value is right was settled separately, as follows.

- **Evidence used.** Values the readers computed outside the written method, with constants they named themselves (CODATA G, IAU parsec and solar mass, or astropy 8.0.2), kept in files separate from `values.csv`. Where no reader computed a value, Claude recomputed it.
- **Tolerance.** The plan's 0.005 dex on g_obs and g_bar.

### SPARC (170 rows)
- **Gap:** the method gives no kpc-to-metre (or km-to-metre) conversion. Both readers said so for every row.
- **Values:** both readers computed every row with the IAU 2015 parsec. Reader A put these in `conditional_SI.csv`; reader B put them in `values.csv` with status "method incomplete". All 170 rows agree with the Atlas within 2 × 10⁻⁷ dex, and the 850 inputs agree between the readers.
- **No material discrepancy.**

### KiDS-1000 (10 rows)
- **Gaps:**
  - no G and no unit conversions;
  - the method does not say that ΔΣ is divided by the released `bias(1+K)`;
  - the method does not say that g_bar is the released first column (labelled `Radius(m/s^2)`, described in the README as the mean projected distance);
  - three sampled rows come from the `_hotgas` file, which the method's g_bar definition (stars plus cold gas) does not mention.
- **Values:** reader B used the README's own constants and bias correction, with g_bar read from the first column. That reproduces the Atlas within 3 × 10⁻⁴ dex for g_obs and exactly for g_bar.
- **No material discrepancy.** The method text must state these steps.

### Strong lensing (10 rows)
- **Gaps:**
  - no G, c, solar mass or length constants;
  - the distance integral is not written out;
  - the light-profile geometry is not specified;
  - for SNL-0 (ESO 325-G004), which of the two printed lens redshifts to use;
  - for SNL-0, whether the source's "gas negligible" statement replaces the registered 0.12 % term;
  - the gas term's source file is not in the written method.
- **Values:** reader B's `conditional_values.csv` (astropy constants) reproduces the Atlas within 2 × 10⁻⁷ dex on all 10 rows, so the Atlas's redshift and gas choices for SNL-0 are the ones B used: 0.0347 (CMB frame) and the 0.12 % term.
- **No material discrepancy.** The SNL-0 choices must be written into the method.

### Globular clusters (10 rows)
- **Gaps:**
  - the light-weighted dispersion is named (`aeg.dispersion.light_weighted_dispersion`, King 1966 weights) but not written out;
  - the solar mass and parsec are not stated;
  - the solar M_V is not printed in any packet source.
- **g_bar:** both readers computed it with astropy constants, and it agrees with the Atlas within 1.3 × 10⁻⁷ dex.
- **g_obs:** neither reader computed it. Claude took each reader's transcribed RV bins (radius, σ and both errors) and applied the Atlas's frozen `bins_from_radii` and `light_weighted_dispersion`, with the Atlas's King (1966) model for each cluster. For all 10 clusters, both readers' bins give the Atlas's σ exactly, with the same number of bins.
  - **This is not an independent check of the algorithm.** It checks the transcription and the arithmetic. The algorithm itself is checked only by the package's frozen reproduction test.
- **No material discrepancy.**

### Dwarf galaxies (10 rows)
- **Gaps:**
  - no G, solar mass or parsec;
  - the [Fe/H] rule that sets Υ_V (D-057, D-059) is not in the written method, and no locator names the [Fe/H] source;
  - no rule for a radius printed already circularised (Tucana, Saviane 1996, "effective geometric radius");
  - no rule for choosing among several printed distance moduli (And XVI) or [Fe/H] scales (Leo I);
  - no statement that "absent (measured limit)" gas enters g_bar as zero.
- **g_obs:** reader B computed g_obs for all 10 rows. All are within 0.003 dex of the Atlas, inside the tolerance.
  - The largest difference is Tucana. Gregory et al. 2019 prints σ = 14.4 (+2.8 −2.3) km/s in the text and 14.35 (+2.78 −2.32) km/s in the Fig. 5 panel. The Atlas uses the more precise figure value, as recorded in `reading/sigma_values.csv` (row v2, "p7, Figure 5 panel annotation"). The method does not say that the more precise printing is preferred.
- **g_bar:** reader A computed every row with declared constants in `values_declared_constants.csv`. Eight agree within 10⁻⁶ dex.
  - **Tucana:** reader A applied the semi-major rule R_h = a√(1−ε) to Saviane's already-circularised radius. The source calls R_e an "effective geometric radius", so that circularises twice. Reader A's own alternative without the extra step equals the Atlas: g_bar 1.006997 × 10⁻¹² against 1.006999 × 10⁻¹², and g_obs 7.2078 × 10⁻¹¹ against B's matching value. **The Atlas reads the source correctly; the method text does not cover the case.**
  - **Leo I:** reader A used [Fe/H] = −1.31 from Koch 2007, giving Υ_V = 1.942. The Atlas uses −1.58, the Geha et al. 2026 headline mean (`reading/feh_comparison.csv`, row leo_1), which gives Υ_V = 1.876. This follows D-057/D-059, which reader A did not have. A's value scaled to Υ_V = 1.876 equals the Atlas's g_bar. **The Atlas follows its frozen rule; the method text and the locator do not show the rule or the source.**
- **No material discrepancy.**

### X-COP (44 rows)
- **Result:** all 44 agree.
- **Notes from both readers:**
  - The public methods page describes the v2 conversion (D-089, D-090), not v1. A reader of the site cannot reconstruct v1 from it.
  - "Row N" does not say whether it counts from 0 or 1; both readers took 1.
  - Reader A counted 859 rows inside the D-023 cut, not the 861 that `SOURCE.md` states. No sampled row is affected.
  - Neither reader traced the modelled-star normalisation (0.39 (M500/10¹⁴ M☉)^−0.84) to a cited source.
  - These are recorded as methods-text findings: M1 (the methods page) and M8 (the cut count and the normalisation). See `AUDIT_RESULT.md`.

## Material discrepancies

**None**, in all six strata. The Clopper–Pearson 95 % upper bounds (two-sided interval) on the material-discrepancy rate are:

| Stratum | n | Upper bound |
|---|---:|---:|
| SPARC | 170 | 2.1 % |
| X-COP | 44 | 8.0 % |
| Each 10-row stratum | 10 | 30.8 % |
| All rows | 254 | 1.4 % |

**Caveat, stated once.** For 210 rows, "no material discrepancy" rests on values computed outside the written method (the readers' declared constants and Claude's recomputation), adjudicated by Claude, not blind.
