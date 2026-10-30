# aeg-d-dwarfs/v1 — reproduction test (draft; frozen on merge, before conversion)

**Status: draft.** Written 2026-10-30, before any dispersion, structural or luminosity value of an A5 candidate was opened. Seen so far: the LVDB column headers, row counts and documentation, and the A5 search log (metadata and methods). The package name is provisional. On merge, this file's SHA-256 goes into `sources.json`, and it is not edited after the first conversion run. If a pass/fail test fails, the package does not ship and the failure is published; the test is not changed to pass (operating rule 5).

## Scope

Dwarf galaxies of the Milky Way, M31 and the Local Group field, plus ambiguous systems (A7), that have a published line-of-sight velocity dispersion or upper limit. The index is the Local Volume Database (Pace 2025, v1.1.1, CC0; tables `dwarf_mw`, `dwarf_m31`, `dwarf_local_field`). The record is the original papers (D-048 item 1). `dwarf_local_field_distant` is out of scope for v1.

## Inputs and rules

| Quantity | Rule |
|---|---|
| Kind | The frozen rule `docs/methods/D048_KIND_BASIS.md`: A5, or A7 with the reason. |
| σ | The original paper's published value, located through LVDB `ref_vlos` and the A5 search log.<br>Plotted only if the source states members beyond the half-light radius (D-038 1A); otherwise an aperture value, recorded.<br>The second moment where given (2A); the whole sample (2B); binary-corrected re-analyses as alternatives (2C); Geha et al. 2026 as an alternative, default only where unique (3A); precedence 3B among values that pass the plotting rules (D-042).<br>Upper limits are plotted as limits at the level the source states. |
| R_h | Circularised projected half-light radius, R_h = a √(1 − ε), from the structural original's semi-major axis a and ellipticity ε (D-048 item 2). The semi-major value is recorded. r½ = 4/3 R_h (D-025). |
| Distance | The distance original (LVDB `ref_distance`). Its method is read at source and must not be kinematic (D-036 #6). A system that inherits its host's distance carries the flag `distance_inherited` (noted in LVDB paper §4) and is plotted. |
| L_V | Extinction-corrected apparent V magnitude from the photometry original, with the distance modulus. Solar M_V is the value adopted by the Υ_V source, read at source. |
| Υ_V | D-039 item 1.<br>(a) A star-formation-history value where a cited source gives one per system (Woo, Courteau & Dekel 2008), labelled.<br>(b) Otherwise, BC03 with the Chabrier disk IMF for old populations, interpolated linearly in [Fe/H] in the per-cluster predictions tabulated by McLaughlin & van der Marel 2005 ((M/L)₁ against [Fe/H] for Milky Way globular clusters at 13 ± 2 Gyr). Below the lowest tabulated [Fe/H], the lowest value is used and flagged `beyond_source_range`; there is no extrapolation. The interpolation code is frozen with this file.<br>Range as D-039 item 3 for dwarfs: model, age and metallicity spread plus the IMF span. No dissolution term. |
| Gas | Putman et al. 2021 (VizieR J/ApJ/913/53). A detected HI mass enters g_bar with the registered helium factor (D-034). A 5σ upper limit gives "absent (measured limit)" (D-035 d). Systems outside that sample are "absent (literature limit for the kind)" only where a cited statement covers them; otherwise "not addressed", recorded. |
| g_obs, g_bar | As D-025: g_obs = 3 σ²/r½; g_bar = G (½ L_V Υ_V + M_gas(<r½)) / r½². Gas inside r½ only where the source gives its distribution; otherwise half the total, flagged. |

## Pass/fail tests

1. **Second reading against the originals** (D-031 item 3; D-048 item 1). An independent reader, with no access to the conversion code, reads every packaged σ, error, limit and level, R_h input, ellipticity, apparent magnitude, extinction and distance modulus in the original paper, with a quote and its location. For σ the reader also records the stated member coverage relative to the half-light radius and the binary treatment.
   - **Pass:** every packaged number equals the original as printed.
   - Where LVDB differs from the original, the original is used and the difference is logged. An LVDB difference does not fail the test; a package difference does.
2. **Transcription:** the package tables, read back, equal the values recorded by the second reading.
3. **Arithmetic integrity:** g_obs and g_bar recomputed from the stored inputs agree with the stored values to 10⁻⁹.
4. **Kind coding:** the D-048 coding sheet is complete for every system, and the 20% double-coded sample is resolved by the rule text. Its agreement rate is published.

**Pass** means tests 1–4 all hold.

## Reported, not pass/fail

- The D-038 3A consistency check between the originals and Geha et al. 2026, by the frozen `aeg.repro_dispersion.consistency`.
- The D-037 reproduction check wherever an original releases per-star velocities with membership, by the frozen `aeg.repro_dispersion.reproduce`.
- Cross-checks:
  - the semi-major against the circularised R_h;
  - LVDB stellar masses (fixed M/L = 2), shown but never used.
