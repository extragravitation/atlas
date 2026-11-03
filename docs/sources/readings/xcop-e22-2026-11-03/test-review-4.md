# Independent final check of the X-COP v2 test (revision 5), 2026-11-03

A reviewer agent, working without access to the archives, wrote this report on revision 5 (commit f2ac017). Revision 6 of REPRODUCTION.md makes its fixes. The report follows verbatim.

## Bottom line

Revision 5 is **not quite freeze-ready**. It needs three short wording fixes, none of which needs data. After that it is freeze-ready once D-090 is ruled:
- one in D-090, whose rule 4 contradicts the test's stage 1;
- two in the test: A3's allowance takes the wrong bracketing row, and the g_obs − g_bar arrow rule has a reading under which it removes the tracks from every such view.

Everything else answers review 3:
- **Table 1:** all 12 rows match the LaTeX exactly, checked by script.
- **Quotes:** the l.373 and l.458 quotes are exact.
- **Steering:** I found no way to steer A3 after seeing data.

**How I worked.** I read the test file at f2ac017 (line numbers below), D-090 at 7fd5dea, the data standard at f2ac017, and the live body of #129 (updated 2026-11-03 20:22Z). I also read `hydromass.tex` without executing it. The comparison script is `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_xcop5/t1.py`. I opened no archive or extraction directory and did not visit drive.switch.ch.

## Item status (test-review-3.md)

| Item | Status | Where in revision 5 |
|---|---|---|
| E1 | **Resolved** | l.143–144: s·δ/2, with s ≤ 3 stated as an assumption; allowance e^(1.5δ) − 1. The bound is correct for one row, but see E-2 below |
| E2 | **Resolved** | l.156 and l.161: quotes exact at l.373 and l.458, truncation fixed; thresholds now 0.03 and 0.10, with the sample-level caveat; l.270 matches |
| E3 | **Partly** | l.225: the linear-axis direction is now right, but the ≤ 0 clause has two readings (E-3) |
| E4 | **Resolved in the test** | l.209–211. D-090 still contradicts it (E-1) |
| E5 | **Resolved** | l.139–141: label, interpolation and testable range each have one reading |
| W1 | **Resolved** | l.139 and l.143: per-row δ and the R_IN = 0 rule. Row choice: see E-2 |
| W2 | **Resolved** | l.132 now states it as an assumption, and A3 reports δ (l.158) |
| W3 | **Resolved** | l.151–152 |
| W4 | **Resolved** | l.162 |
| W5 | **Resolved** | l.218; the monotonicity check is reported only (l.234), decided before data |
| W6 | **Resolved** | l.59–70 and l.160 |
| W7 | **Partly** | #129 is fixed except one phrase: its heading says "as fixed in the frozen test", although its header correctly says the test is not yet frozen |
| W8 | **Resolved** | l.27 now defers to D-090 rule 5. It holds only if D-090 is ruled as written |
| W9 | **Resolved** | l.29 |
| W10 | **Partly** | l.214 is now version-neutral, but D-090 rule 4 still says "standard 2.4.0 supports that bound" |

## Errors (must fix)

**E-1. D-090 rule 4 contradicts the test's stage 1.**
- D-090 (7fd5dea) says the seven are "listed in the observables table only, with no measurement rows and no g_bar value".
- Test l.209–211 puts them in `systems.ecsv` and `excluded.csv`, and leaves observables rows to Part B. That is the E4 fix, which D-090 did not take up.
- The test rests on D-090 (l.3), so JvH would be ruling a text that conflicts with the frozen test.
- **Fix:** in D-090 rule 4, replace that clause with the l.209–211 wording. In the same edit, change "standard 2.4.0 supports that bound" to "a data standard version supports that bound" (W10).

**E-2. A3's allowance takes δ from the wrong row (l.143).**
- The interpolated ln M is a weighted average of two rows, and each row has its own labelling error, up to 1.5·δ_i.
- So the bound is a = e^(1.5·max(δ_lower, δ_upper)) − 1, not the lower row's δ.
- **Example:** with δ_lower = 0.03 and δ_upper = 0.05, at s = 3 the error near the upper row can reach e^0.075 − 1 = 0.078, against an allowance of 0.046.
- The gate at l.145 ("δ > 0.05 on any testable row") likewise never sees the δ of the upper bracketing row.
- This matters only if the grid's log step grows outward. Still, a frozen bound should be a bound.
- **Fix:** "δ is the larger of ln(R_OUT/R_IN) of the two bracketing rows." Apply the same δ in the l.145 gate. l.100 calls it "the local grid step"; align that wording too.

**E-3. The g_obs − g_bar arrow rule can be read to remove every track from that view (l.225).**
- A lower bound on g_bar is an upper bound on g_obs − g_bar, with no lower end. So "the bound allows a value ≤ 0" is literally true on every row.
- On that reading the clause empties the view, and the log-axis curve rule before it never applies.
- The intended meaning is presumably "where the gas-only value already gives g_obs − g_bar ≤ 0".
- **Fix:** "On log axes, the track is drawn only where the gas-only value gives g_obs − g_bar > 0, and the arrow points down toward 0. Rows where the gas-only value gives ≤ 0 are left out of the log view."

## Weaknesses (should fix)

**W-a. The 3 % reason covers a narrower range than A3 tests (l.156).**
- E22's 3 % is for [0.05–2] R500 (l.373). A3's median runs over every testable row, which may reach down to about 0.01 R500, where E22 says the methods spread more.
- l.156 calls the per-cluster use a deliberate strict choice, but does not mention the range.
- **Fix:** add "and over A3's full testable range, which may extend below 0.05 R500". Or restrict the median to rows inside 0.05–2 × Table 1's R500,TOT. Either is fine if fixed now.

**W-b. "median(a)" does not say over which rows (l.154–155).**
- The gas part uses a subset of rows (l.150). State "median of a over the rows used in that part".

**W-c. l.152 overstates what A2 variant (ii) implies.**
- A2 reads GP_mass at R_OUT (l.99); A3 labels it at the midpoint.
- So under (ii), ratio_gas is near 1 only up to the labelling shift.
- **Fix:** "close to 1 up to the labelling allowance".

**W-d. Stage-1 pass/fail is now thin (l.233).**
- The only remaining pass/fail check is "200 rows; MASS and MGAS positive inside range". That is acceptable, and moving monotonicity to reported-only before seeing data is legitimate.
- Note that stage 2 then rests almost entirely on A3.

**W-e. The ratio arrow is given only for log–log axes (l.223).**
- On linear axes, g_obs/g_bar against g_bar is a hyperbola.
- The general rule at l.221 covers it, but if the site offers linear axes, say so.

## Notes

- **Table 1 (l.59–70).** All 12 rows (z, R500, M500, M200 and asymmetric errors) are identical to `hydromass.tex` l.324–335. The caption is at l.316.
- **Quotes.**
  - l.373: "the median masses in the range [0.05-2]R_{500}", "within 3% of one another" and "less than 10% at all radii" are exact, and correctly attributed to the sample and to NFW against NP.
  - l.458: exact and complete.
  - l.263 and l.528 are unchanged and correct.
- **A3 is computable from one reading.** Midpoint labelling, log–log interpolation, the testable span, the δ gate, the minimum rows and fixed thresholds are all set before data. The only input chosen from data is the A2 convention for M_STAR, and that follows a fixed order (l.131). There is no free choice after the data are seen, beyond E-2 and W-b.
- **Arrow directions** at l.222–224 and l.226–227 are correct.
- **Stage-1 representation (l.209–211).** It is consistent with standard §5:
  - `excluded.csv` takes system, dataset, reason and citation;
  - `systems.ecsv` needs a redshift, available from Table 1;
  - no validation rule in §10 requires a system to have measurement rows.

  v1 (`v1/tables/systems.ecsv`) lists all 12 clusters, so v2 dropping the seven's rows must be explained on the dataset page. Some v1 redshifts differ from E22 Table 1: A2029 0.0773 against 0.0766, A2142 0.0909 against 0.09, A3158 0.0597 against 0.059. A note in Part B is enough.
- **A7 against A3 (l.99, l.197).** A7 reads GP_mass at R_OUT while A3 uses the midpoint. This is harmless, because A7 is reported only, but say so in one line.
- **#129.** The rest is consistent with the test and D-090:
  - it gives the bound as "a bound below the source's central g_bar. It is not a confidence limit";
  - it uses 0.03/0.10 plus the allowance;
  - it states the authors-and-ruling rule.
- **Neutrality.** No wording assumes a cause. "DM" appears only as a column name (l.43) and inside marked quotes (l.161, l.199).

**Next step:** fix E-1 in D-090 on `plan/d090-xcop-v2`, and E-2, E-3 and W-a to W-c in REPRODUCTION.md as revision 6. Remove "frozen" from the #129 heading. JvH then rules D-090, and the file can be frozen without another full review.

**Memory items:** none new.