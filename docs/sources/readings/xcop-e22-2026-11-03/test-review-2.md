# Independent review of the X-COP v2 test (revision 3), 2026-11-03

A reviewer agent, working without access to the archives, wrote this report on revision 3 (commit 003ee46). Revision 4 of REPRODUCTION.md addresses it. The report follows verbatim.

**Bottom line.** Revision 3 should not be frozen yet. Its intent is sound: the gas-only bound is mathematically right, and the stage-2 gate is fixed before any data are seen. But:
- A3's 0.05 gate can fail because of a radius-labelling question alone, not the question it is meant to answer.
- The gas-side check (A8 check 3) is almost certain to pass whatever the data show.
- Stage 1 cannot be written under the current data standard.
- Two references point at things that do not exist at 003ee46.

Line numbers below are from `git show 003ee46:data/packages/aeg-d-xcop/v2/REPRODUCTION.md`.

**What I did.** I opened no archive, extraction directory or drive.switch.ch link. The working tree was switching branches while I worked, so I read every repository file from commit 003ee46 or by named branch. I downloaded arXiv 2205.01110 to `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_xcop3/e22/`; its SHA-256 matches `18fc2e80…c7d8`. The synthetic experiment is `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_xcop3/scripts/grid.py`.

## Confirmations
- **The bound's direction (l.171).** E22 l.453–456 defines g_bar as G(M_gas + M★,BCG + M★,sat)(<r)/r². The gas comes from an emissivity ∝ n_e², with azimuthal-median clump removal (l.74), so every term is non-negative. Intracluster light is excluded (l.410), which only strengthens a lower bound. Given the same gas profile, G·MGAS/r² ≤ g_bar exactly.
- **Ratio direction (l.182).** A lower limit on g_bar gives an upper limit on g_obs/g_bar and on g_obs − g_bar, at the central g_obs. The direction is correct.
- **No steering through the radius convention in A3.** `GP_mass.fits` has no R_REF (l.43). Both R1 conventions therefore read it at R_OUT, so A2's selection cannot change A3 or A8 check 3 after the data are seen.
- **Issue #129 exists and matches the text.** It is open, its three boxes match (a)–(c), and its threshold matches l.126.
- **Neutrality.** No wording assumes a cause. M_DM (l.41) appears only as a column name.

## Errors (must fix)
1. **Dangling reference to the review record (l.5).** `test-review-2.md` exists at 003ee46 on no branch. Also, no review of revision 2 exists, so "review reports … test-review-2.md" would cite a review that does not yet exist, inside the frozen text. Either commit the review of revision 3 under that name before freezing and describe it as such, or remove the reference.
2. **"Tracked … in `VALIDATION_COMPLETION_PLAN.md`" is false at 003ee46 (l.184).** The plan has no #129, stage-2 or g_bar-limit text there. That text exists only on the unmerged branch `plan/d090-xcop-v2`, under D-090, which is still "Ruling: pending". Issue #129 says the plan and the continuation guide already link to it; they do not.
3. **No ruling behind the change, and D-089 is no longer engaged.**
   - Revision 2 said that under D-089 rule 1 the seven "get no g_bar in v2" and that JvH had to confirm this.
   - Revision 3 deletes that and adds g_bar lower limits for seven systems. That changes what the Atlas says, so it needs a decision-log ruling (D-090 or another).
   - The file must cite that ruling, and say how a gas-only limit squares with D-089 rule 1 ("only where their baryons are stated by the source"). Freeze only after the ruling.
4. **Stage 1 cannot be represented under standard 2.3.0 (l.172–176).**
   - `limit` "applies to the measured quantity", which is g_obs or delta_g (`docs/data-standard.md` l.100).
   - A limit row must have empty error columns (validation rule 5, l.275). That contradicts keeping g_obs "with the _LO/_HI bounds" (l.173).
   - `g_bar` is required to be the full value from detected baryons (l.102).
   - `stars_status` has no value meaning "not given by the source" (`absent` would read as zero).

   So condition (a), standard 2.4.0, is a precondition of **stage 1**, not only stage 2. Alternatively, l.172–176 must say stage 1 is recorded in the observables table only, with no measurement rows. Say which.
5. **A3's gate can fail on the radius convention alone (l.124–126).**
   - The R_IN/R_OUT step size of the 200-row grid is not known; no values have been read. The "about 1.5 %" at l.120 is an assumption carried over from the revision-1 review.
   - Synthetic case: an NFW total mass on a log grid over 0.01–2 R500 (E22's stated range, l.528) gives a step of 2.7 %. If GP_mass's true radius is R_IN but it is read at R_OUT, the A3 median is biased by **+0.043**.
   - For a grid over 10–3000 kpc the bias is +0.048. For 1–5000 kpc it is +0.072, which fails the gate with no physical difference at all.
   - Fix this now, before the data are seen. Either compute A3 under both R_IN and R_OUT and require the gate under both, or under the GP convention A2 can identify (see item 6). Also state the grid-spacing assumption, and what happens if the step is larger than about 2 %.
6. **Nothing gates the g_bar side of stage 2.**
   - Condition (c) tests only total mass (GOBS against GP MASS). The seven's g_bar comes from GP **MGAS**.
   - A8 check 3 (l.188), MGAS_GP ≤ 1.01 × GBAR, is not sensitive. At R500, stars are f★/f_gas ≈ 9–15 % of the baryons (Table 4). The check therefore passes even if the GP gas is **10–16 % higher** than the 2023 gas, and in the star-dominated core it passes trivially.
   - The reason given, "1 % allows for the gas coming from a different run", is therefore wrong: the stars, not the 1 %, set the tolerance.
   - Replace it with a direct gas comparison: median over rows of MGAS_GP / (GBAR·r²/G − M_STAR) within a stated tolerance, for each of the five.
   - Because that subtracts a term, restrict it to rows where M_STAR < 50 % of GBAR·r²/G, so the difference cannot go noisy or negative in the core.
   - Make it part of condition (c).
7. **A failed stage-1 check has no stated consequence (l.185–188).** If the rows, gas-fraction or bound check fails, stage 2 neither waits nor proceeds by any rule, which leaves it to whoever runs the test. State that any stage-1 fail blocks stage 2 until it is resolved in the open.
8. **The rendering condition (b) misses where the arrow points (l.179, l.182).**
   - In a view of g_obs/g_bar (or g_obs − g_bar) against g_bar, a larger true g_bar moves the point down **and** to the right: slope −1 in log–log, a single diagonal direction. Drawing a vertical upper-limit arrow plus a horizontal one misstates it.
   - On g_obs against g_bar the arrow is horizontal, and against radius it is vertical.
   - Condition (b) must require the direction in each view to be derived from how that view's quantity depends on g_bar. Any view where that dependence is not monotonic must leave the tracks out.

## Weaknesses (should fix)
9. **A3 may compare two different analyses (l.124–125).**
   - E22 l.456: "For the observed acceleration we consider both the nonparametric reconstruction and the results of the Einasto fit."
   - If GOBS in the 2023 files is the Einasto curve, A3 measures model dependence (Paper II gives Einasto/NFW of 0.78 to 1.26), not 2021 against 2023.
   - Also report GOBS / [G·MASS_EIN3/r²], so a failed gate can be told apart from "GOBS is Einasto".
10. **The 0.05 threshold is not justified (l.126).**
    - If GOBS is the same 2021 NP run evaluated at the data radii, the ratio should be about 1 within interpolation. If not, E22 expects method differences "within 10%" (l.373).
    - It is also inconsistent with A2, which applies 0.02 to the **same** 2021-against-2023 question. The Einasto file, M_STAR included, is dated 2021-09-16, one day after GP_mass (l.43–44).
    - State the reason, and say why total mass gets more room than baryons.
11. **The median hides parts of the profile.** A 5 % median says nothing about the core or the outskirts, yet the seven would be drawn over all 200 rows. Add a per-row criterion, or at least report the maximum. Define a minimum number of testable rows; a cluster with fewer fails the gate.
12. **Rows beyond the source's range (l.175).** E22 l.263 says the NP method "cannot be extrapolated outside of the fitted range". "All 200 grid rows are kept" may include extrapolated rows. These could fail "positive MASS" (l.186) or be drawn as tracks. Freeze a rule now: rows outside the source's data range are flagged `beyond_source_range` and kept off the tracks. Name where that range comes from for the seven (ask the authors, or E22's 0.01–2 R500 using Table 1's R500, stated as an inference).
13. **Gas-fraction check of 1 % on every row (l.187).** There are 2 400 rows and no stated reason. In the outer rows, where posteriors are broad and skewed, a median of the ratio is not the ratio of the medians. A fail there would be unrelated to anything the check is for. State its purpose, or make it a median, or report it only.
14. **"Exact lower bound" (l.171) holds only for central values.** As a statistical limit its confidence level is undefined. Under the standard, an empty `err_level` would read as 0.683. Say "bound on the source's central g_bar for this gas profile, not a confidence limit", and have 2.4.0 carry that.
15. **The reason for tracks (l.182) applies equally to the five.** Their GOBS values are also non-parametric reconstructions, evaluated at the data radii (E22 l.263), and correlated. The real distinction is that the 200-row grid is not tied to the data radii. Also say how the g_obs _LO/_HI range is drawn on a track.
16. **Condition (b) also misses non-display uses.** Limit rows must be excluded from population averages, binned summaries, fits, and the inputs of frozen pattern tests. There are 1 400 grid rows against 105 points, so anything weighted per row would be dominated by them. Downloads must mark `limit` explicitly. The arrows must be readable without colour.
17. **A3 contradicts itself (l.123–126).** It says "Not a pass/fail check" and then sets a pass/fail gate. Reword: "A3 does not pass or fail v2; its stage-2 condition is pass/fail."
18. **R1 is stale (l.90).** The A2-selected convention is said to be used in "A4, A6, A7 and A9", but A3 (l.124) and A8 (l.188) now use it too. Also say explicitly that it means R_OUT for GP_mass, and give r_kpc for the seven's stage-1 rows; A8 never states it.
19. **§5 and §6 are not updated for stage 2.**
    - §5 l.214 records the stellar projection "on every row", but the seven have no stellar term.
    - §5 does not say that stage 2 flips `plotted` on released rows. Under the rule that released data are never overwritten, that means a new dataset version; say so.
    - §6 (l.218–226) omits what A3 and A8 establish, and what they do not (that GP 2021 is the analysis behind GOBS; that the seven's g_bar is anything but a bound).
20. **l.44 states "byte-identical" as a fact.** The "Seen" list (l.7–10) includes no member hashes, while A1 (l.111) checks it. Either list member hashes as seen, or write "expected identical (A1 checks)".

## Notes
- **What happens after the authors answer (l.126, l.184).** The answer should be recorded, and the eligibility decision taken by a JvH ruling in the decision log, with the 0.05 threshold unchanged.
- **Wording (l.170).** "Measured total … mass profiles": the expert-layer term is the hydrostatic mass (source column MASS), and "measured" overstates a reconstruction that assumes hydrostatic equilibrium. l.163's "DM plus baryons" is the Table 1 caption's own wording; mark it as quoted.
- **Mapping the stage-1 label.** The not-plotted label at l.176 should map to `not_plotted_reason = limit_only`, once `limit` can apply to g_bar.
- **A1 failing.** The file does not say whether A3 and A8 still run if A1 fails.

**Next step:** fix items 1–8. That means a ruling on D-090 (or its equivalent) merged with the plan, a gas condition and both radius conventions added to the stage-2 gate, and the stage-1 representation tied to standard 2.4.0. Then rerun an independent review before freezing.

**Memory items:** none new.