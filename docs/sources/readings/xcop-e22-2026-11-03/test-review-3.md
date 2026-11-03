# Independent review of the X-COP v2 test (revision 4), 2026-11-03

A reviewer agent, working without access to the archives, wrote this report on revision 4 (commit 13f2d80). Revision 5 of REPRODUCTION.md addresses it. The report follows verbatim.

## Bottom line

Revision 4 is not ready to freeze. It answers most of the previous review, and nothing in it looks steerable in a serious way. Four things still need fixing first:
- **A3's error bound is wrong.** The "off by at most δ" claim (l.129) does not hold for gas mass.
- **A3's justification misquotes E22 and is wrong on the facts** (l.136–137).
- **One arrow direction in A8 is wrong** (l.195).
- **Stage 1 cannot be written as stated** (l.185).

All four are wording or threshold fixes. None needs data. D-090 is still unruled, and l.3 already holds the freeze until it is.

**How I worked.** I read every repository file with `git show 13f2d80:` or `ee222a8:`. I opened no archive and no extraction directory, and did not visit drive.switch.ch. I read the previous reviewer's `hydromass.tex` copy (727 lines) without executing it. My synthetic experiment is `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_xcop4/exp.py`. Line numbers below are from `git show 13f2d80:data/packages/aeg-d-xcop/v2/REPRODUCTION.md`.

## Item-by-item status of the previous review

1. **Resolved.** l.5 cites `test-review-2.md`, which is committed at 13f2d80.
2. **Resolved.** The plan reference is gone; l.192 points to #129.
3. **Resolved in the text, ruling still pending.** l.3 holds the freeze until D-090 is ruled. D-090 rule 4 explains how this squares with D-089 rule 1.
4. **Partly resolved.** Stage 1 now has no measurement rows. But "listed in the observables table … with the reason" (l.185) cannot be represented (Error E4).
5. **Partly resolved.** The midpoint plus δ approach is right in principle, but the bound and the step definition are wrong (E1, W1). A2 still claims "about 1.5 %" (l.123), which is an unverified figure (W2).
6. **Resolved**, with one gap: nothing says what happens if A2 fails (W3).
7. **Mostly resolved.** l.192 says a failed stage-1 check blocks stage 2. "Resolved in the open" is undefined (W5).
8. **Partly resolved.** The g_obs − g_bar direction is wrong (E3).
9. **Resolved in substance.** The quote is truncated and gives the wrong line (E2).
10. **Partly resolved.** A reason is now given, but it misreads E22 (E2).
11. **Resolved** (l.130, l.134–135, l.137).
12. **Mostly resolved** (l.199). Table 1's R500 for the seven is used but not transcribed (W6).
13. **Resolved** (l.203).
14. **Resolved in the test** (l.183). Issue #129 still says "exact lower bound" (W7).
15. **Resolved in the test** (l.194). #129 still gives the old reason (W7).
16. **Resolved** (l.196–198).
17. **Resolved** (l.127).
18. **Resolved** (l.90–91). A8's radius is the midpoint, through the R1 exception.
19. **Resolved** (l.229–230, l.238, l.243–244). l.238 repeats the faulty "method-agreement" wording (E2).
20. **Resolved** (l.44).

Notes in the previous review:
- **Ruling after the authors answer:** done (l.138).
- **"Measured" wording:** fixed (l.182). It remains in #129.
- **Quoting "DM plus baryons":** fixed (l.175).
- **A1 failure:** fixed (l.114).
- **`limit_only` mapping:** moot now that stage 1 has no measurement rows.

## Errors (must fix)

**E1. The "off by at most δ" bound is false for gas (l.91, l.129).**
- The midpoint is half a log step from either edge. So the error in ln M is at most s·δ/2, where s = d ln M/d ln r. The bound "≤ δ" needs s ≤ 2.
- s = 3ρ(r)/ρ̄(<r). For any density that does not rise outward, s ≤ 3, not 2, and s approaches 3 in any cored region.
- **For gas, s > 2 is common in exactly the rows A3's gas part uses** (those where M_STAR is below half the baryons). Synthetic β-models (β = 2/3):
  - core radius 150 kpc: s = 2.95, 2.61 and 2.10 at 30, 100 and 200 kpc;
  - core radius 250 kpc: s > 2 out to about 300 kpc;
  - a cuspy cool-core profile: s about 2.2–2.4 inside 60 kpc.
- **For total mass, s ≤ 2 mostly holds**, because the central galaxy and an NFW-like inner slope keep it there. But an Einasto profile with α = 0.18 gives s = 2.16 at about 1 % of r₋₂, so it is not guaranteed.
- **For g:** the radius r is the gbar_gobs RADIUS on both sides of each ratio, so only the mass slope matters. The bound on g's own slope is irrelevant.
- **Size of the effect:**
  - at δ = 0.05 and s = 3, the bias is ratio − 1 = 0.078, against an allowance of 0.05;
  - at δ = 0.027, it is 0.041 against 0.027;
  - also, |ratio − 1| = e^(s·δ/2) − 1, which is slightly more than s·δ/2.
- **Fix:** use 1.5δ, which holds for any density that does not rise outward, and state that assumption. Apply e^x − 1 to the allowance.

**E2. A3's justification misquotes E22 and reaches a false conclusion (l.136–137, echoed at l.238).**
- **Wrong line for one quote.** "within less than 10%" over [0.2–1] R500 is at **l.373**, not l.263.
- **Truncated quote, wrong line.** The g_obs quote is at **l.458**, not l.456 (l.456 is the g_bar equation). It is cut mid-sentence: the full text is "…the results of the Einasto fit **to the DM component only**." The cut should be marked and the full clause given. It matters for which Einasto quantity the "Einasto alternative" is.
- **The 10 % figure is a sample average, not a per-row scale.** "less than 10% at all radii" (l.373) follows "On average, we do not observe systematic deviations…" and describes the sample-median NFW/NP ratio. So "the paper's own method-agreement scale" for one cluster's individual rows overstates it.
- **The "more closely" claim is false.** l.373 also says the median masses of all methods over [0.05–2] R500 agree "within 3% of one another". A median gate of 0.05 is therefore *looser* than the stated agreement between two different methods.
- **Fix:** either keep 0.05 and correct the stated reason, or tighten the median gate to 0.03 with this quote. Decide before freezing. Correct l.238 to match.
- **Checked and exact:**
  - l.263, "cannot be extrapolated outside of the fitted range";
  - l.528, "[0.01-2]R_{500}";
  - l.456, the g_bar definition used at l.183.

**E3. The arrow direction for g_obs − g_bar is wrong (l.195).**
- Slope −1 in log–log holds only for g_obs/g_bar.
- For g_obs − g_bar, d ln(g_obs − g_bar)/d ln g_bar = −g_bar/(g_obs − g_bar). That is −5 at a ratio of 1.2, −1 at 2, −0.11 at 10, and −0.02 at 50. In log–log it is also a curve, not a straight line.
- The bounded quantity can also cross zero, where a log axis cannot draw it.
- (The error came from previous-review item 8 and was copied.)
- **Fix:**
  - on a linear axis, the direction is down-right with slope −1;
  - on a log axis, it is a curve that is drawn only while g_obs − g_bar > 0;
  - if the bound allows a value ≤ 0, draw an open-ended arrow labelled as such, or leave the track out.
- **Also define the case where a view's quantity does not depend on g_bar at all** (for example g_obs against radius). "Does not change monotonically" as written would exclude those views from showing tracks, which is probably not intended.

**E4. Stage 1 as written cannot be represented under standard 2.3.0 (l.185).**
- The observables table (standard §4) has no reason column.
- Each observables row needs a `value`, `quantity`, `steps` and `evidence_tier`. "Listed … only" does not say which values. Is it MASS and MGAS (`mass_hse`, `mass_gas`) on 200 radii per cluster, or nothing?
- **Fix:**
  - put the reason in `data/registry/excluded.csv` (system, dataset, reason, citation; standard §5), and the seven in `systems.ecsv`;
  - say whether any observables rows are written, or leave that explicitly to Part B.

**E5. The A3 radius rule is ambiguous (l.129–130).**
- "`GP_mass.fits` is interpolated … at the geometric midpoint" reads as interpolating *at* the midpoint. The intent is to label each GP row with its midpoint and then interpolate at each gbar_gobs RADIUS. Say that.
- "Median of ln(R_OUT/R_IN) over its rows" does not say whose rows (GP's 200, or the 21 gbar_gobs rows).
- "Inside the grid" does not say whether it means the midpoint span or the R_IN–R_OUT span.
- A frozen computation must have only one reading.

## Weaknesses (should fix)

**W1. One median δ is wrong if the grid is not log-uniform (l.129).**
- On a linear 200-row grid over 0–3000 kpc, the median δ is 0.01, which passes the 0.05 check. The local step at 30 kpc is 0.405.
- The per-row gate would then fail in the core on radius labelling alone.
- **Fix:** use each row's local ln(R_OUT/R_IN) as its allowance. Define what happens to a row with R_IN = 0, since its midpoint is 0.

**W2. A2's "about 1.5 % between neighbouring grid radii" (l.123) is still an unverified assumption, and A2 is pass/fail.**
- If GP's true radius is R_IN, both A2 conventions read GP at R_OUT. Variant (ii) could then be off by s·δ, roughly 0.05–0.08 for gas in the inner rows, against a per-row 0.05.
- Variant (a)(i) probably protects A2, but the sentence should be removed or stated as an assumption.

**W3. A3's gas ratio depends on A2's outcome (l.132).**
- If A2 selected (ii), then GBAR equals G(MGAS_GP + M_STAR)/r² within 2 % by construction, so ratio_gas passes trivially.
- If no A2 variant passes, the subtraction is meaningless, and ratio_gas can pass or fail for reasons unrelated to its purpose.
- **Fix:** state "if A2 fails, the gas part of the stage-2 condition fails", and note the case where (ii) passes.

**W4. If GOBS turns out to be the Einasto curve, A3 measures model dependence, not 2021 against 2023 (l.137–138).**
- The condition would fail and go to the authors. That is acceptable, but say it explicitly in the "if the condition fails" clause, so the reported Einasto ratio is read as diagnostic only.

**W5. "Resolved in the open" is undefined (l.192).**
- For A3, l.138 forbids changing thresholds. The stage-1 checks (l.201–202) have no such clause.
- A later analyst could "resolve" a failed check, such as a non-monotonic MASS, by flagging rows away.
- **Fix:** apply l.138's rule to the stage-1 checks: authors' answer recorded, JvH ruling, checks unchanged.
- Note that "do not decrease" has zero tolerance. Per-radius posterior medians of a hydrostatic mass need not be monotonic. Decide now whether a small dip is a fail.

**W6. Table 1's R500,TOT for the seven is used (l.199) but not transcribed in §2 (l.55–61).**
- E22 l.324–335 gives A85 1214, A1644 1031, A2255 1202, A3158 1146, A3266 1381, RXC1825 1109 and Zw1215 1346 kpc, with redshifts.
- Transcribe them into the frozen text.
- Also report each of the five clusters' gbar_gobs RADIUS range in units of R500. That tests the "0.01–2 R500" inference with no extra reading.

**W7. Issue #129 contradicts the test and D-090.** It still says:
- "exact **lower bound**" (item 14);
- "lines … because the profiles are model curves on a 200-step grid" (item 15);
- "in views of g_obs/g_bar it becomes an upper limit" (item 8, superseded by l.195);
- "measured total and gas mass profiles";
- "(frozen test, revision 4)", although it is not frozen.

Update the issue body.

**W8. The licence wording is narrower than D-089 rule 3 (l.27).**
- D-089 rule 3 says "values are linked, not redistributed".
- l.27 says only the *archives* are never committed or redistributed.
- Yet §5 (l.220) publishes 105 value rows, and l.197 requires downloads.
- State how v2's committed rows and downloads square with D-089 rule 3 (or D-004), or get a ruling.

**W9. Standard validation rule 13 (D-083 item 3, "fails the build") is not addressed.**
- v2 cannot reproduce v1. D-090 rule 1 is the exemption.
- The test, or Part B, should cite it so the automated check is handled by rule and not by an ad hoc override.

**W10. The version number for the limit change is probably wrong (l.188, plan step B).**
- Letting `limit` apply to g_bar, while keeping errors on g_obs, changes the meaning of `limit` ("applies to the measured quantity") and validation rule 5. Under standard §0 that is a **major** change.
- A new optional column (for example `g_bar_limit`) would be minor.
- l.188 says "a data standard (planned for 2.4.0)". Make it version-neutral, or specify the new-column route.

## Notes

- **Neutrality:** no wording assumes a cause. "DM" appears only as a column name (l.41) and in marked quotes (l.175). "Hydrostatic" (l.182, l.245) is correct.
- **The bound's direction is sound at the level of central values** (l.183). Stars are non-negative in every posterior sample, so every quantile of g_bar is at least the same quantile of the gas term, for the same gas profile.
- **D-090 rule 4 and test l.184–192 agree:** observables only, no g_bar value, the three conditions, exclusion from averages and fits. D-090's "Expected in v0.2" (a site release) and the test's "v3 or after" (a dataset version) are compatible.
- **The other arrow directions at l.195 are correct:** horizontal on g_obs against g_bar; down-right with slope −1 in log–log on g_obs/g_bar against g_bar; vertically downward on g_obs/g_bar against radius.
- **A2's data-dependent choice of convention follows a fixed order** (l.122), so it cannot be steered. It still feeds A3's M_STAR (l.132).

**Next step:** fix E1–E5 and W3, W5 and W6 in the file, and update the #129 body (W7). JvH then rules D-090, and the file goes to a short final check before freezing.

**Memory items:** none new.