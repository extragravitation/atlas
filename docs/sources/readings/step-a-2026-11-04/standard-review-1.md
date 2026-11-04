# Independent review of data standard 2.4.0 (D-093), revision 1 (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Independent review of data standard 2.4.0 (D-093), 2026-11-04

## Bottom line

**Not ready to freeze.** The technical checks pass: `pytest` gives 209 passed, `aeg.check` says "All checks passed", and the 2.3.0 hash `417825fb…` is unchanged. No 2.3.0 package becomes invalid. But the evidence shows four things the draft cannot express:

- terms shared by a subset of systems;
- a row whose two sides have different confidence levels;
- a confidence level the source doesn't give, on observables;
- a valid `stars_status` for gas-only bound rows. Without that, X-COP A8 (a) cannot be met.

Two drafting defects also land in the frozen text. Each fix is additive, so 2.4.0 can still be a minor version.

Line numbers refer to `docs/data-standard.md` @9cb65d3 unless another file is named.

## Errors (must fix)

1. **Terms shared by a subset of systems cannot be expressed** (§7a `applies_to`, l.235; validator `validate.py` l.217, inside `validate_v22`). `applies_to` may only be `*` or a single `system_id`. The step A evidence needs subset terms in many places:
   - the two MaNGA lenses share one Υ_ref (`lenses-adjudication.md` F4: "one dataset-scale term (within R32)");
   - the dwarf distance calibration covers Savino's 21 of 64 systems;
   - dwarf velocity floors are "per pipeline", and LF/IMF and band transformation are "per source" (`dwarfs-adjudication.md` table; `dwarfs-reader-B.md` D3, D18, D24, D27: "Dataset subset").

   Recording these as `dataset` with `*` applies them to every system, which is wrong. Recording them as per-system rows hides that they move together. D-093's "needs no standard change" is not justified for these.
   - **Fix:** allow `applies_to` to be a semicolon list of `system_id`s, or add a `group` column. This is additive.

2. **One `err_level` per row cannot carry mixed levels** (l.62, l.103–104). `err_level` is the level "of the interval or limit", but a row can have two intervals. Dwarfs v1 already has 7 limit rows that carry `g_bar_err_*`: the σ limit is at 90–95.5 %, while the g_bar errors are 1σ (`dwarfs-reader-B.md` l.143). `err_level_status` has the same row-level problem.
   - **Fix:** say that `err_level` and `err_level_status` apply to the measured quantity. Add optional `g_bar_err_level` and `g_bar_err_level_status`.
   - **Also fix:** rule 5 (l.285) says "empty error columns" without saying it means the measured quantity's error columns. The validator already reads it that way.

3. **`err_level_status` is missing from observables** (§4, l.148: "`limit`, `err_level` as §3"; `CORE_OBS`, `validate.py` l.144). The X-COP v2 Part B observables (GOBS, MGAS errors, level not stated: `REPRODUCTION.md` §5; readings §2.1) will default to 0.683. This is exactly what item 1 of D-093 exists to prevent.
   - **Fix:** add `err_level_status` to §4 and to `CORE_OBS`.

4. **Bound rows have no valid `stars_status`** (§3, l.113, against l.108). For A8's seven clusters the source gives no stars. `measured` and `modelled` don't apply. `absent` means "not included in g_bar", but D-034(d) allows it only for a quoted negligible statement or a measured upper limit. `not_separable` is false.
   - So A8 stage 2 rows cannot be written validly, and A8 (a) is not fully met.
   - **Fix:** add `not_given_by_source` to the three `*_status` closed lists. Require it, or `absent`, for the missing component(s) on `g_bar_bound ≠ none` rows.

5. **The §2 conventions contradict §3** (l.62–63). "Empty means 0.683" is unchanged, so a reader of §2 gets the meaning that `err_level_status` exists to forbid.
   - **Fix:** add ", unless `err_level_status` says otherwise" there too.

6. **The §7a table is broken** (l.246–247). The `in_error_columns` row sits after a blank line, so it is not part of the table. It renders as a stray pipe line, and this is the text that would be frozen. Related problems:
   - l.229 ("one row per … point-scale term whose source gives none") and l.249 ("point-scale terms that are present need no row") are not updated for the new stated-but-not-in-columns rows.
   - The §7a column text requires `scale = point`, `applies_to = *` and a size. §10 item 17 (l.297) and the validator (l.296) require only `status = given`. A `system`-scale row with `in_error_columns = no` passes, and its meaning is undefined (probe confirmed).
   - **Fix:** settle one definition and use it in all three places.

## Weaknesses (should fix)

7. **§2a rule 7 (l.84) needs tightening.**
   - **(a) Unclear what is held fixed.** "When the radius changes" doesn't say what else stays fixed. It should say: perturb the measured quantity that sets the radius (θ_E, R_h) with all other inputs fixed.
   - **(b) Double counting with rule 5.** Radius changes caused by distance belong to rule 5 and must not be counted again here.
   - **(c) No home for a two-sided point-scale error.** A point-scale radius error that moves both sides (the Wolf estimator: g_obs ∝ 1/R_h and stellar g_bar ∝ 1/R_h²; dwarfs F4 "moves both") has nowhere legal to go:
     - rule 1 makes the point-scale columns independent;
     - §7 covariance is "only where the source provides" it;
     - rule 5 covers only shared terms.

     State that such a term is a §7a row with `moves = both` and a registry formula.
   - **(d) Hidden profile input.** The aperture derivative dM★(<R)/dR needs a light profile. The rule should say the profile must come from the source or a registered assumption.
   - **Physics.** For the lens case the physics is correct: M_E = π Σ_cr R_E², so G M_E/R_E² = π G Σ_cr. Two qualifications:
     - The identity holds only where the radius is the Einstein radius in the mean-convergence-1 sense. It does not hold for aperture masses (SNL-1/2), and only approximately for printed M_E values whose errors are dominated by R_E (R29). Say this, so a printed M_E error is not also put on g_bar a second time.
     - X-ray and weak-lensing bins have no per-row radius error. The rule should say it does not apply there, so nobody invents a radius error from bin widths.

8. **Rule 7 is classified two ways.** The lens adjudication calls it "patch-level clarifying text". §0 (l.9) counts "making something required" as major. D-093 should state why rule 7 is a minor-version clarification of §2a rule 2 ("the axes it moves").

9. **The g_bar_bound wording is ambiguous, and the drawing rules were dropped.**
   - "has no `err_level`" (l.108) can be read as "the row's `err_level` must be empty". Write instead: "the bound itself carries no confidence level; `err_level` continues to refer to the measured quantity."
   - A8 (a) asks the standard to keep g_obs errors on bound rows. This is only implied (draft l.26 said it explicitly; it was dropped). Restore the sentence.
   - The draft's "views draw the bound in the direction the X-COP test fixes" (draft l.30) was also dropped. Nothing in the standard says how a plotted bound row is drawn, and the site (`site/src/scripts/map.js` l.257) knows only `limit`.
   - **Fix:** either reference the A8 drawing rules, or require `plotted = false` until the site implements them.
   - The definition ("bound on the source's central g_bar") does not cover D-088 item 2's upper bound, which is a bound relative to a corrected spherical value. Note this in D-093.

10. **Item 17's second sentence and item 18's page requirement can't be enforced by the build** (l.297–298). They are site and pipeline duties under a heading that says "automated; fails the build". No code reads the new columns (`grep`: none outside `validate.py`). Either move them out of §10 or name the check that enforces them.

11. **`x_value_change_ruling` accepts any decision heading** (`validate.py` l.301). It accepts pending ones too: D-093 itself passes (probe confirmed). It also accepts decisions unrelated to value changes. Require a ruled decision, and record in D-093 that this generalises D-090 rule 1's "the one exception".

12. **Validator and test gaps.**
    - **Units not checked.** `g_bar_bin_lo/hi` are missing from `UNITS_V2` (l.172), so their stated unit m s⁻² is not checked.
    - **Bin edges.** Edges without `bin_coordinate`, or with lo > hi, pass silently (probe).
    - **Meaningless combinations pass.** `bound` together with `bin_coordinate` passes, and so does `err_level_status = stated` with an empty `err_level`. The text doesn't say what these mean.
    - **Untested branches.** `pipeline/tests/test_validate_v24.py` has no tests for: closed-list violations, a bad `in_error_columns` value, `x_value_change_ruling` or `in_error_columns` in a 2.3.0 package, or a valid `bin_coordinate` row. The probe shows the code handles the first three, but they are untested.

13. **Sizes that are bounds or come at other confidence levels** (§7a `size_kind`, l.240). The evidence includes:
    - "up to 5 %" (SLC15);
    - a scatter that bounds the Harris error from above (GC F2);
    - errors stated as lower bounds (NGC 6505, F5);
    - hydrostatic bias sizes at two radii per cluster (readings §3c).

    None fits `one_sigma`, `range` or `as_released` (one value per system). Add `upper_bound` and `lower_bound` to `size_kind`, and allow a per-radius size.

14. **The bin_coordinate wording mis-scales KiDS K8** (l.106). "Terms that move it are system- or dataset-scale" doesn't fit K8, a per-lens stellar-mass scatter that acts through bin assignment, not as an error on a bin's g_bar. KiDS has no systems, so only `dataset` scale with `*` applies. State that.

## Notes

- **Cause-neutral wording:** nothing in the new text assumes a cause. "DM" appears only inside quoted source column names and captions.
- **Backward compatibility:** fine for packages; a 2.3.0 package cannot use the new columns or keys (item 14, enforced). A reader that ignores `g_bar_bound` or `bin_coordinate` in a 2.4.0 package would misread `g_bar`. That is acceptable only because the site must be updated before any such package ships. Say so in D-093.
- **Version history (l.20):** says "Nothing else changes", but item 13 and §9 `standard_version` were also edited. Both edits are consequential and harmless.
- **Freeze records:** `data/frozen/data-standard-2.3.0.json` was re-pointed to `docs/data-standard-2.3.0.md` with the same hash, as was done for 2.2.0. The 2.4.0 record (hash `1e52f725…`, matches) carries `frozen_on: 2026-11-04` while D-093 is still pending. Set the date at merge.
- **Merge order:** D-092 exists only on another branch (commit `6a189cd`), so this branch's decision log skips from D-091 to D-093. Check the merge order.
- **Distance findings:** "no change needed" is justified for cause-dependent distance directions (GC F1, dwarfs F1). Each cause is its own §7a row with its own formula, and per-system sizes can go in extension columns of the systems table.
- **What was verified:** I ran the test suite and `aeg.check` on an archive copy of 9cb65d3, plus my own probe at `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_std240/probe/probe.py`. Nothing in `/home/claude/atlas` was modified. I did not check the site rendering, and did not read the reader reports in full beyond the adjudications and targeted searches.

**Next step:** fix Errors 1–6 in the draft, decide items 7, 9 and 13, then re-run the review before JvH rules on D-093.