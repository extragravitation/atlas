# aeg-d-gc-baumgardt/v1 — reproduction test (frozen before conversion)

Written 2026-10-30, **before `convert.py` exists**. This file's SHA-256 goes into `sources.json` when it is frozen (merge of this file), and it is not edited after the first conversion run. If a pass/fail test fails, the package does not ship and the failure is published; the test is not changed to pass (operating rule 5).

## What had been seen when this was written

- The sources' column definitions and documentation text only: `veldis.html` (column heads and list of datasets), `parameter.html` (column key), `appendix.html` (description), the RV files' two header lines, Harris (2010) column keys, and the VOTable field definitions of McLaughlin & van der Marel (2005).
- Values, all disclosed in deviation #19:
  - part of one row of `2ms1.txt` (no velocity);
  - six rows of McLaughlin & van der Marel Table 13 (NGC 6715 to NGC 7089: population M/L, observed and central dispersions);
  - ten rows of Harris Part II (NGC 104 to NGC 1851: metallicity, reddening, horizontal-branch magnitude, distance modulus, integrated V, M_V and colours).
- No dispersion profile, no other structural value, and no g_obs or g_bar has been seen.

## Inputs (D-025, D-036, D-039, D-042, D-045)

| Quantity | Source | Rule |
|---|---|---|
| σ profile | Baumgardt database `veldis.html` (re-analysis, D-042) | Line-of-sight bins only. Proper-motion bins are recorded, not plotted (D-036 #8). Each line-of-sight dataset code in a profile is a separate candidate (D-045 item 1). Edges are inferred from the mean radii (`edges_inferred`). |
| Light weights | King (1966), `aeg.king66` (D-045 item 2) | McLaughlin & van der Marel King fit (W₀, r₀); otherwise Harris c and r_c. Plotted only if coverage ≥ 0.80 (D-036). |
| Global σ | `aeg.dispersion.light_weighted_dispersion` | As frozen. |
| R_h (projected) | McLaughlin & van der Marel King fit `Rh`, rescaled from their `Dist` to the Harris distance; otherwise Harris r_h (D-045 item 3) | r½ = 4/3 R_h (registered assumption). |
| Distance | Harris (2010) R_Sun, from horizontal-branch photometry (D-042) | Never kinematic. |
| L_V | Harris integrated V: M_V,t with the solar absolute V magnitude adopted by McLaughlin & van der Marel (2005), read at source before conversion (D-045 item 4) | McLaughlin & van der Marel model luminosity shown as a cross-check. |
| Υ_V | McLaughlin & van der Marel (2005) (M/L)₁, BC03 + Chabrier disk IMF (D-039) | Range per D-039. Their dynamical ratios (Table 13: King, Wilson, power-law M/L) are never used. |
| g_obs, g_bar | D-025 | g_obs = 3 σ²/r½; g_bar = G (½ L_V Υ_V)/r½². No gas (D-036 #4, literature limit for the kind). |

Systems that D-038 4A places in A7 (for example Crater) are recorded there, not in A3.

## Pass/fail tests

1. **Transcription.** Every packaged source value equals the source file's value, to the digits printed. This covers:
   - Baumgardt: radius, star count, σ, upper and lower errors, and type;
   - Harris: R_Sun, (m−M)_V, V_t, M_V,t, E(B−V), c, r_c, r_h;
   - McLaughlin & van der Marel: W₀, r₀, r₀ in pc, Dist, Conc, Rc, Rh, (M/L)₁ and (M/L)₂ with their errors.

2. **King (1966) reproduces the published fits.** For every row of McLaughlin & van der Marel's `models` table with `Mod = K`, `aeg.king66.King66(W0, r0pc)` must give:
   - log₁₀(r_t/r₀) within 0.02 of `Conc`;
   - log₁₀(half-power radius) within 0.02 dex of `Rc`;
   - log₁₀(projected half-light radius) within 0.02 dex of `Rh`.

   The tolerance covers the two-decimal rounding of the published logarithms (±0.005) and of W₀. **Pass** means every row is within all three tolerances. Any row outside means fail, and the conversion does not run.

3. **Arithmetic integrity.** For every packaged measurement, g_obs and g_bar recomputed from the stored σ, r½, L_V, Υ_V and G (`astropy.constants.G`, as in the other packages; its version recorded) agree with the stored values to a relative 10⁻⁹. Units are m s⁻².

**Pass** means tests 1–3 all hold.

## Decision test (pre-registered; decides, does not fail the package)

4. **Reading of Harris r_c.** For clusters with both a McLaughlin & van der Marel King fit and Harris c and r_c, compute:
   - (a) the median |log₁₀(r_c,Harris / r₀,MvdM)|;
   - (b) the median |log₁₀(r_c,Harris / R_c,MvdM)|, where R_c is the half-power radius.

   Both radii are in pc, at the Harris distance (r₀ and R_c rescaled from their `Dist`).
   - If (a) ≤ (b), Harris r_c is read as r₀ (the D-045 reading) and the Harris-only clusters are converted.
   - If (a) > (b), the reading is wrong. The Harris-only clusters are recorded, not plotted, and the question returns to JvH before anything else is done with them.

   The medians, and the median and scatter of c_Harris − Conc, are published either way.

## Reported, not pass/fail

- **The D-037 reproduction check** on the line-of-sight bins of type "RV", by `aeg.repro_bins` (reconstructed binning, D-045 item 5). It is published per bin and per cluster in `checks/`, whatever the outcome.
- **Cross-checks:**
  - Harris r_h against the King-fit R_h, both at the Harris distance;
  - Harris L_V against McLaughlin & van der Marel `Ltot`;
  - for each cluster, the light-weighted σ from each line-of-sight dataset.

  All are shown on the cluster pages.
- **Clusters with no McLaughlin & van der Marel fit and no Harris c and r_c**, or with a core-collapse flag in place of a measured c, are recorded, not plotted, with the reason.
