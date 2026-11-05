# Independent review of the X-COP v2 test part B, revision 2 (2026-11-05)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Review of the X-COP v2 test, part B, revision 2 (commit 42de647)

## Bottom line

**Don't freeze it yet.** Revision 2 fixes all eight errors from review 1 (E1–E8), and nothing structural is broken. But I found seven new must-fix errors, listed below, which review 1 missed or revision 2 introduced:
- Four are mechanical-decidability gaps.
- One is a real leak path in the consent gate: row values can reach the public CI logs.
- Two are provenance problems with the hydrostatic-bias quotes and references.

All of them are wording or rule changes, and none needs any data. After the fixes, one quick check of the changes should be enough; it doesn't need a full third review.

**How I checked:**
- I read part B at 42de647 against review 1, part A and its result and JSON, and decisions D-034, D-090–D-093, D-095–D-098 and D-103 on main.
- I also checked standard 2.5.1 §4b, §7a, §9 and §12, `validate.py`, `formula_check.py`, `site_check.py`, `atlas.mjs`, `data.yml` and `checks.yml`.
- I checked quotes in these cached files: E22 `hydromass.tex` (SHA-256 `fdf04068…`), Ghizzardi `xcop-metallicity.tex` (`2d862a21…`), Ettori & Eckert 2022 `p_nt_b_aa.tex`, Loubser 2020, and Paper II `tab2.tex`.
- I computed no v2 value. I recomputed the five `mass_model_choice` sizes from the published `result_part_a.json`, only to check the draft's arithmetic.
- The worktree has been removed. The main checkout was not touched; it is on `decision/d-105`.

**Review 1's errors:**

| Item | Status |
|---|---|
| E1 | Fixed. All three pairs are carried, and the max rule is stated. The arithmetic matches the JSON: A644 0.2241, A1795 0.0617, A2029 0.1459, A2142 0.0852, A2319 0.0518. |
| E2 | Fixed. `x_value_change_ruling = D-090`, and D-090 has a `**Ruling (` line, so validator item 18 passes. |
| E3 | Fixed: two builds, the preview, the 4-week follow-up and the site change. Its CI side is incomplete (see M2). |
| E4 | Fixed. E22 l. 38 and l. 97 check out; l. 130 is the `\label{eq:hse}` line. |
| E5 | Fixed in structure. The quote carried over from review 1 is spliced (see M4). |
| E6 | Fixed. |
| E7 | Fixed: l. 309 is correct, Ghizzardi l. 923 checks out, l. 926 is indeed a commented-out line, and the term renames are done. |
| E8 | Fixed. |

## Errors (must fix)

**M1. Nonthermal-pressure α: which column, and what error form (l. 78, l. 116, l. 151).**
- Ettori & Eckert 2022's table (`tab:gamma_beta`) prints α at R500 and R200 twice. The table note says so: "both in \cite{eckert19} (second column) and in the present work (last column)".
- The errors are asymmetric, and some are printed oddly: RXC1825 `0.0^{+28.9}_{+9.8}`, ZW1215 `11.9_{-11.9}^{+0.0}`.
- Part B names neither column. A single `_r500_err` column cannot hold an asymmetric error. As written, the reader or `convert.py` would have to choose.
- **Fix:**
  - Name the "present work" (last) column.
  - Use `_err_lo` and `_err_hi`, filled as printed.
  - Record anomalous signs as printed and mention them in the note. Never repair them.

**M2. Row values can reach the public CI logs (l. 59, l. 226).**
- `data.yml` runs every `convert.py` (Build packages). The v2 tables then exist on the runner, and two later steps print from them:
  - **pytest:** the package tests run with `-rA --tb=short`. Assertion introspection prints the compared values on any failure.
  - **formula check:** `aeg.formula_check` runs on every package that has `tables/measurements.ecsv`, so it covers v2 rows with `xray_hse_bias`. Its failure messages print row values: "changes at the default ({row} -> {v})", "Python {pv} vs JavaScript", "g_obs = …".
- So "the conversion prints none" does not make "no CI log line contains a row value" true, and that line is not checkable as written.
- **Fix:** name these changes as part of the conversion pull request:
  - v2 tests assert only on counts and booleans, with their own messages (or v2 tests run with `--tb=no`);
  - `formula_check` redacts values for any package whose `x_publication` is not `published`;
  - item 12 states a mechanical check, for example a local grep of the captured CI log against the reader's off-repo `values.csv`.

**M3. Three text-search checks have no fixed text (l. 188, l. 189, l. 199).**
- These are: A2319's page "states the asymmetry", the dataset page "states that the `hse_bias` bound holds only out to R500", and the page "states the ruling and that v2's values differ".
- A text search needs a string. Without one, the check is a judgement made at build time.
- **Fix:** fix the exact expert-layer and plain-layer sentences now, as was done for D-092's note and the rule 5 sentence. Check the A2319 wording for neutrality while doing so.

**M4. The `hse_bias` quote joins two sentences, and a stated size is left out (l. 149, l. 150).**
- "with the exception of a single system … (A2319) … we conclude that our measurements are mildly biased (<10%) out to R500" spans two sentences of E22 l. 502.
- The elided text is "the measured baryon fractions agree with the expectations at R500 and slightly exceed … indicating a mild level of hydrostatic bias. Since …". The A2319 exception qualifies the baryon-fraction evidence, not literally the conclusion. Restricting the bound to four clusters is the Atlas's reading, which is defensible but not the source's words.
- The same line also states the X-COP-specific "hydrostatic masses are 10-15% lower than weak lensing estimates" and Eckert 2019's "7% at R500, 10% at R200". Neither is in the note. Leaving out the larger stated figure looks selective.
- **Fix:**
  - Quote the two sentences separately and in full.
  - Say that applying the bound to "the four" is the Atlas's reading of l. 502.
  - Add both figures to the note.

**M5. The `xray_hse_bias` v2 `range_ref` cites a different quantity (l. 169).**
- The slider's parameter is b in M_true = M_HSE/(1 − b). l. 539's "nonthermal pressure (10–20%) at R200" is a pressure fraction, not b. v1's 0.2 came from 1 − b = 0.85 ± 0.05.
- **Fix:** either
  - cite a b figure from l. 502 (10–15 % against weak lensing; 7 % and 10 %; simulations 5–30 %) and state how the 0.2 maximum follows from it, or
  - state explicitly that the nonthermal-pressure fraction is used as a stand-in for b, as an assumption.
- Put this choice in O3.

**M6. The `mass_model_choice` recomputation cannot be compared exactly (l. 132, l. 118).**
- "Any difference is a fail" against 4-decimal values. In float64, 1 − 0.7759 = 0.22409999999999997, which is not 0.2241.
- Recomputing from the JSON's `M_GP`, `M_EIN` and `M500_table1` fields instead of the ratio fields also gives different digits.
- **Fix:**
  - Name the keys: `GP/EIN`, `GP/Table1`, `EIN/Table1`.
  - Name the arithmetic: max of |r − 1|.
  - Name the comparison: round to 4 decimals, then compare exactly.

**M7. No conversion rule when the error form is "undetermined" (l. 103–108).**
- An undetermined form fails item 5, but nothing says what `g_obs_err_*` and `g_bar_err_*` hold, or whether conversion stops.
- **Fix:** state it. For example: the columns are left empty with the `no_uncertainty` flag, the conversion proceeds, and item 5 is reported as failed. Or the conversion stops pending JvH.

## Weaknesses (should fix)

- **`mass_model_choice` mixes radii.** The NFW pairs compare masses at Table 1's R500 with masses at R500 from R3. The size therefore partly reflects the R500 definition, not only the model, and it is applied as a fractional g_obs size at every radius. Say both in the note.
- **"The R500 is the source's (Table 1 R500,TOT)" (l. 149) is asserted, not read.** l. 502 does not define R500. Either have the reading record it, or label it an inference (Table 1 is E22's only tabulated R500).
- **The unit of w (l. 117).** Paper II Table 2 prints w in units of 10⁻³. Say whether the column holds the value as printed, with that unit, or scaled.
- **Which items run where.**
  - Item 11 needs the off-repo `values.csv`, and build 1 is local, so neither runs in CI. Say which items are local.
  - The result should record the local runs' outputs (hashes, pass/fail).
  - Say plainly that these items are not reproducible in one command until consent.
- **Reproduction ledger (l. 226).** `data/reproduction.json` holds "one entry per shipped dataset". Say whether a v2 entry is added at conversion or at publication.
- **Steps.**
  - §4b marks `newtonian_g` as an Atlas step, and here the source performed it.
  - The baryonic steps mix the Gas and Stellar-mass ladders.
  - The validator only checks the union of the ladders, so this passes, and D-095 allows it. Still, add one line to D-105 saying that `newtonian_g` is listed for a source-computed g under D-095.
- **`bcg_dm_systems.md` (l. 80, l. 158, l. 212).** The filename uses "dm" (project rule 8). Rename it, for example to `bcg_extra_mass_systems.md`.
- **`reconstruction_bias` as `given` on a mock basis** differs from the lens test's handling. It is justified at l. 129, but D-105 should record the difference so JvH rules it knowingly.
- **Rebase before freezing.** The branch base is fa4de38, and main is now eefb3b2. Only `data/assumptions.json` changed in the relevant paths (new KiDS entries), so this is low risk, but the mock should be re-run after the rebase.

## Notes

- **Consent-gate mechanics are otherwise sound.**
  - I tested `git add -A` with an ignored `tables/` among other paths. It still stages the other packages' changes; the exit code is swallowed by `|| true`. So ignoring v2's tables does not weaken the "committed tables equal regenerated tables" step for other datasets.
  - Including `checksums.sha256` in that step makes it the determinism check, as l. 60 says.
  - `atlas.mjs` (l. 36–38, 72–79) skips any version without tables, so v1 stays current in build 2.
  - The exclusion-register rows for `aeg-d-xcop/v2` don't attach to v1 systems (they are matched by `s.dataset`, l. 90).
  - `validate()` needs the tables, but it runs only through package tests after conversion, so it is not a problem.
- **The cached sources are not public.** The archives in the CI source cache stay private to the repository's Actions. The share URLs, however, are already public in part A, as stated.
- **D-105 is free.** It is not used on main or on any remote branch as of now.
- **On O4:** I searched E22 for exclusion wording ("exclud", "remov", "discard", "restrict", "ignor"). Nothing applies to the g_obs–g_bar points: l. 74 and l. 95 are about X-ray and SZ processing, and l. 342 restricts the NP masses to the data radii. Paper II Table 2 gives Einasto fit ranges (R_min, R_max). Those belong to a different analysis, which D-098 rule 1 excludes, but `d096.csv` should record them.
- **Quotes that checked out at source:**
  - E22 l. 38, 97, 109, 111, 116, 130, 263, 309, 311, 366, 373, 404, 408, 410, 453–458, 486, 502 (the pieces, not the splice), 504, 506, 528 and 539;
  - Ghizzardi l. 705, 712, 715, 923 and 926;
  - Ettori & Eckert 2022 l. 182, 276 and 377;
  - Loubser 2020 l. 547.
- **Values that match:** system IDs 177/179/180/181/183, the A9 ratios, and the 22 terms.

## O1–O4

- **O1 (no observables for the seven clusters): agree.**
- **O2 (the max |ratio − 1| rule): adopt, and say plainly in D-105 that the rule was chosen after the values were public.**
  - It is not blind. Every candidate rule (max, mean, half-range, the GP/Einasto pair only) could be compared against values that are already published.
  - It is still defensible:
    - Part A said "each pair" and "these ratios" become the term, so all three pairs are forced by frozen text, and max is the simplest rule over them.
    - It is the conservative envelope, the opposite of the selection review 1 caught.
    - It decides no pass or fail.
  - The honest residual: half the spread of the three masses is an equally conventional rule and would give roughly half the size. D-105 should name that alternative and why max was chosen.
- **O3 (keep `xray_hse_bias`, drop `icl_fraction`): agree,** once the `range_ref` is fixed (M5) and the 0.2 maximum is justified explicitly against the 10–15 % and 5–30 % figures at l. 502.
- **O4 (only explicit exclusion wording counts): agree.** The criterion is mechanical, it matches D-103, and my search found no such wording in E22.

**Next step:** apply M1–M7 and the short fixes above as revision 3, re-run the full `validate()` mock after rebasing on main, have the changed lines checked, then JvH rules D-105 and the test is frozen.

**Possible memory item (source: this review, from `data.yml` and `formula_check.py`):** the data CI runs `aeg.formula_check` and the package tests on regenerated tables, and both can print row values on failure. Any package whose rows are not yet published needs those outputs redacted.