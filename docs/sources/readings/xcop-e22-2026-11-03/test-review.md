# Independent review of the X-COP v2 test draft (revision 1), 2026-11-03

A reviewer agent, working without access to the archives, wrote this report. Revision 2 of REPRODUCTION.md addresses it.

I reviewed the draft without opening anything under `e22files/` and without visiting drive.switch.ch. All transcriptions are correct. The logic has problems, and A6 is the worst: as written it can return the **wrong** verdict, not just "undetermined".

## Confirmations (checked against the source)
- **Cosmology, l.56:** H0 = 67.8 and Ωm = 0.308 match. "Flat" is not in the text; l.56 says "Planck 2015 ΛCDM", so flatness is an inference.
- **Table 1, l.324–335:** z, R500 and M500 with errors match for all five clusters, including A2142 z = 0.09 and A2319 1424 (−4/+5). The line range is right (A85 is on l.324, Zw1215 on l.335).
- **Table 4, l.424–428:** all 45 entries match, checked by an automated diff against the LaTeX. The caption on l.417 matches; it is truncated, so add "…". The f_bar definition (l.433), l.402, and the equations (l.453, l.456) match.
- **vdB15:** the gNFW form matches (vdB15 l.337–339, with c = R200/R_s). (0.64, 1.63) is the "Stellar Mass density" column of the "All" row and (0.72, 1.64) is the number-density column for M★ > 10¹⁰ (l.279). Ghizzardi l.715 uses (0.72, 1.64). The two sets are attributed to the right fits.
- **A2319 caveat (§5):** l.435 and l.502 are correct.
- **Neutrality:** no wording assumes a cause. "M_DM" appears only as a column name.

## Errors (must fix)
1. **A6 can give a false verdict.** I tested this numerically with synthetic profiles only; scripts are in /tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_xcop2/ (`a6.py`, `a6b.py`, `a6c.py`, `a6d.py`).
   - **Weak discrimination.** Over 0.2–1.5 R500, with free K ≥ 0 and N > 0, the 3D and 2D cumulative shapes mimic each other to **1.5–2.3 % rms in ln M**. That figure assumes a central-galaxy term of 10–30 % of S(R500); with no central-galaxy term it is 2.3–6.8 %.
   - **Small mismatches already break it.** Shifting R200 by ±20–25 % or α by 0.14 gives "undetermined". With α off by 0.14 and a 3D truth, the rms ratio is already 1.9 in favour of 2D.
   - **The l.106 premise is false.** The draft says the central galaxy is "enclosed whole" in this range. E22 l.406 gives the central galaxy as a 3D density ρ₀·exp{−b_n((r/r_e)^{1/n} − 1)}. For n = 4 and r_e = 60 kpc, only **45 %** of its mass lies within 0.2 R500 and 96 % within 1.5 R500. With that profile and a **3D truth**, the A6 rule returns **"2D"** (rms3D 1.60 % against rms2D 0.72 %).
   - **Rule to replace it (results from `a6c.py`).** The file is noise-free model output, so test for exact functional reproduction instead:
     - Fit the full radial range with M_STAR = [3D Sérsic-density mass (ρ₀, r_e, n free)] + N·S_{3D or 2D}(r; R200 free, α fixed at 1.63 or 1.64).
     - Verdict = the model whose rms in ln M is ≤ 1e-3 while the other's is ≥ 5× higher. Otherwise "undetermined". Report the fitted R200.
     - Without a central-galaxy term, the wrong model's floor with free R200 is 0.10–0.14 %, and the right model reaches about 1e-10.
2. **§6 overstates what A6 can establish.** A 3D-shaped M_STAR fits two histories: a projected model fitted to projected data and then deprojected (correct), or a 3D model fitted straight to projected cumulative data (normalisation too high by about 1/0.75, per Ghizzardi l.715). A6 cannot tell these apart.
   - Reword: "A6 establishes the functional form of M_STAR in the file, not whether its normalisation was deprojected; that question stays with the authors."
3. **The dates contradict the "Seen" list.** A3 (l.92) cites file dates of 2021 and 2023, but §1 (l.7) does not list dates as seen. Either add "file dates" to l.7 or remove them from A3.
4. **A8 (l.128) overstates.** A85 and ZW1215 have published satellite stellar masses (Ghizzardi Table, M_star,500 = 2.10 and 3.34 × 10¹² M☉). What they lack is a central-galaxy profile and any M_STAR in the shared files.
   - Reword: "have no complete stellar budget in E22 and no M_STAR in any shared file".

## Weaknesses (should fix)
5. **A4 tolerance.**
   - **Use FGAS, not MGAS/MASS.** Table 4's f_bar is not always f_gas + f★: for A2029, 11.1 + 2.8 = 13.9 against a printed 13.8, and for A2319, 9.2 + 2.0 = 11.2 against 11.3. So the table quotes posterior medians of each ratio. R4 therefore names the wrong primary estimator, since the file has an FGAS column. Make FGAS primary, report MGAS/MASS as secondary, and state that the secondary cannot turn a fail into a pass.
   - **Allow for rounding.** Add the 0.05 percentage-point rounding half-unit to the tolerance: |Δ| ≤ quoted error + 0.05.
   - **±0.1 is sensitive to R_Δ.** With the local slope d ln f_gas/d ln r ≈ 0.64 (from 7.7 → 12.8 between R2500 and R500), a 2 % shift in R2500 moves f_gas by about 0.1 percentage points. A4 is therefore really testing the R_Δ definition. That is acceptable only if it is stated, and if the Table 1 R500 variant is pre-declared as reported-only. For A644, Paper II's Einasto mass is 0.78 × the NFW mass, so R500 differs by about 8 %, shifting f_gas,500 by about 0.5 percentage points against a quoted error of 0.6.
   - **f★ error source.** M_STAR has no error column, so state where Table 4's f★ errors could come from, or that they cannot be reproduced and only central values are tested for f★.
6. **R1 is a fork, and A2 at 1 % is sensitive to it.** With 200 log-spaced rows, R_OUT/R_REF ≈ 1.015. Mislabelling the radius shifts the mass by d ln M/d ln r × 1.5 % ≈ 1.5–3 %, which fails A2 regardless of composition. The draft also uses R_REF for one file and R_OUT for the other without a reason.
   - Rule: compute A2 under both conventions. A2 asks whether the stars are included: g_bar changes by about 10 % at R500 between gas-only and gas-plus-stars, and by more in the core. So set the pass at |median ratio − 1| ≤ 0.02 per cluster, with every row ≤ 0.05, under either convention, and report which convention fits. Freeze now that whichever convention A2 selects is the one used in A4 and A6.
7. **Gas source in A2.** GBAR may use MGAS from the non-parametric run (`GP_mass.fits` has its own MGAS), not from the Einasto run. Pre-register two variants: EIN3 MGAS + M_STAR, and GP MGAS + EIN3 M_STAR. Report both.
8. **R3 (l.74).**
   - "Smallest r" is harmless, because the enclosed mean density is monotonic for an outward-falling density.
   - What is missing: the radius column (R_REF, or the R1 outcome), the root-finding rule (log-log interpolation between bracketing rows), the rule when no crossing exists inside the grid (entry "not computable", which counts as an A4 fail), and Tcmb = 0 (no radiation term).
9. **A2 needs an extrapolation rule** for RADIUS values outside the 200-row grid: no extrapolation, and the row is reported as untestable.
10. **A5 and A7.** Label Table 1's R500 and M500 as "NFW fit (DM + baryons), Table 1 caption l.316", so a ratio ≠ 1 is not read as an error.
11. **A1.** "Exactly those listed" (l.81) is undefined, because §1 does not enumerate every member, for example the 12 lower-case folder names. Either list them, or state that the member list follows from the archive hash.
12. **Freeze mechanics (l.3).** "Frozen on merge" should say the file's SHA-256 is recorded, for example in the decision log, before any archive is opened (rule 5).

## Missing (a referee would ask)
- **Stellar normalisation against published values.** This is my arithmetic on published tables only, using E22 f★,500 × Table 1 M500 against Ghizzardi's sphere-corrected M_star,500:

  | Cluster | E22 / Ghizzardi |
  |---|---|
  | A1795 | 1.9 |
  | A644 | 2.7 |
  | A2029 | 2.2 |
  | A2142 | 2.2 |
  | A2319 | 2.4 |

  Projection alone would give 1.33. Removing a central galaxy of about 10¹² M☉ does not close the gap, and nor does the H0 difference, which is about 7 %. Add a reported check: M_STAR(<R500) minus the central-galaxy term from the file, compared with Ghizzardi's M_star,500 and with that value divided by 0.75, as ratios with no threshold. Flag the tension to the authors with question #124.
- **GOBS errors.** The confidence level of GOBS_ERR_LO and GOBS_ERR_HI is not stated anywhere; this belongs in the questions to the authors or in Part B.
- **The gNFW in E22 is a different profile.** E22 l.408 points to "Eq. eq:gnfw", but that equation (l.218–222) is the 5-parameter **pressure** gNFW, not vdB15's density form. Note this in A6, because it adds to the ambiguity about which form E22 used.

No data were read. A6 needs the most work before freezing, so the next step is to rewrite it under the exact-reproduction rule in item 1, then fix items 2–4 and 5–6.