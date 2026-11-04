# Independent review of data standard 2.4.0 (D-093), revision 2 (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Independent review of data standard 2.4.0 (D-093), revision 2, 2026-11-04

## Bottom line

**Not ready for JvH's ruling yet. Two text fixes are needed first, and both are small.**

- **What passes:** in an archive copy of ce9e62f, `pytest` gives 211 passed and `aeg.check` gives "All checks passed".
- **2.3.0 is unchanged:** its hash is still `417825fb…` (re-verified).
- **The 2.4.0 hash matches:** `7ccc8f85…`.
- **The gating works.** Probes on a copy of sparc/v2 (2.3.0) show that each new feature is rejected under 2.3.0 and accepted under 2.4.0. There is one edge case (W1).
- **What blocks the ruling:**
  - l.257 contradicts §10 item 17. The two cannot both be met for rows that 2.2.0 already requires.
  - §10 item 11 was not updated for a size_column that names a measurements column.
  - The M_E sentence in rule 7 is muddled on the physics.

Line numbers refer to `docs/data-standard.md` at ce9e62f, except `validate.py` (V) and D-093 (D, counted from its heading at decisions.md l.1906).

## Status of the 14 items from review 1

1. **Subset terms: resolved.** l.243, l.299, V l.222, gated at V l.288. See W3 on scale.
2. **Mixed confidence levels: resolved.** l.62, l.109, l.111, l.293. See W2 for an ambiguity.
3. **err_level_status in §4: resolved.** l.156, V l.149, gated at V l.282.
4. **Bound rows: resolved.** l.120, l.115, item 17 at l.305, V l.335.
5. **§2 conventions: resolved.** l.62.
6. **§7a table and in_error_columns: partly resolved.**
   - Resolved: the table now renders (l.239–254 are contiguous), and l.254, item 17 (l.305) and V l.347 now agree.
   - Not resolved: l.257 now contradicts item 17 (E1).
7. **Rule 7: partly resolved.** Parts (a)–(d), the lens qualification and the bins case are all addressed at l.84–90. The M_E sentence at l.85 is wrong-footed (E3), and l.87 leaves a gap (W4).
8. **Minor-version classification: resolved.** D l.22.
9. **Bound wording and drawing: mostly resolved.**
   - Resolved: the wording, the kept g_obs errors and the plotted rule are at l.115; the D-088 note is at D l.15.
   - Open: `plotted = false` is not enforced (W5).
10. **Duties the build can't check: resolved.** They moved to l.308 and §9 l.284.
11. **x_value_change_ruling: partly resolved.**
    - Pending decisions are now rejected (V l.356).
    - A ruled but unrelated decision is still accepted. The build cannot enforce this, so it is acceptable if stated.
    - New over-strictness: see W6.
12. **Validator and test gaps: mostly resolved.**
    - Fixed: units (V l.178), edges without a basis (V l.317), lo > hi (V l.323), bound together with bin_coordinate (V l.333), stated with an empty level (V l.257), and tests for all of these.
    - Still untested: the gate on a measurements size_column; a list applies_to that names a system not in the package.
13. **size_kind bounds: resolved.** l.248, l.247. The size_value wording at l.246 was not updated (N3).
14. **KiDS bin_coordinate scale: resolved.** l.113.

## Errors (must fix)

**E1. l.257 contradicts l.254, item 17 (l.305) and l.237.**
- l.257 says: "A term that is both point-scale and not in the columns has a row with `in_error_columns = no`."
- Item 17 requires such a row to have `status = given` and `applies_to = *`.
- Two kinds of row are point-scale and not in the columns, yet cannot meet item 17:
  - the l.237 rows "point-scale term whose source gives none", which have `status = not_given_by_source` and are required since 2.2.0;
  - the rule-7 `moves = both` rows (l.87), which may apply to one system or have no size.
- **Fix:** limit l.257 to "a point-scale term **the source states with a size** but leaves out of its released error columns". Say that rule-7 rows and not-given rows leave `in_error_columns` empty.

**E2. §10 item 11 (l.299) was not updated.**
- It still says a size_column must name "an existing systems column".
- But l.247, item 14 (l.302) and V l.229 all allow a measurements column from 2.4.0.
- The frozen text therefore contradicts itself.
- **Fix:** add "(from 2.4.0, or a measurements column)".

**E3. The M_E sentence in rule 7 (l.85) is muddled.**
- The identity g_obs = πGΣ_cr depends on how M_E is defined (mean convergence 1 inside θ_E). It does not depend on how the source attributes the error.
- Where M_E is defined that way, g_obs carries no θ_E error at all. The real hazard is propagating the printed M_E error onto g_obs as an independent bar. Putting it on g_bar is not the hazard.
- "There, the printed M_E error is not also placed on g_bar" guards against the wrong mistake.
- **Fix:** "Where M_E is defined by mean convergence 1, g_obs = πGΣ_cr exactly, and the printed M_E error (a θ_E error) is not placed on g_obs. Where it is not (an aperture mass, or a model mass inside θ_E that is not defined by κ̄ = 1), g_obs depends on the radius and this rule applies to both sides."

## Weaknesses

**W1. The gate breaks additivity in one edge case** (V l.292).
- Under 2.3.0, a size_column naming a column that exists in both systems and measurements (for example an extension column, or `system_id`) was valid.
- It is now rejected as "measurements size_column needs 2.4.0" (probe confirmed).
- No shipped package is affected.
- **Fix:** gate only when `col not in sys_cols`, and say which table wins when a name exists in both (l.247 is silent on this).

**W2. When g_bar's confidence level must be filled in is ambiguous** (l.111).
- "Where its level differs from the measured quantity's" suggests leaving `g_bar_err_level` empty when the two are the same.
- But "empty … = 0.683" then reads a 0.95/0.95 row as 0.95/0.683.
- **Fix:** drop "differs"; say g_bar's level is always read from these columns.

**W3. §2a's scale table (l.71–75) still defines `dataset` as "every system".**
- A list-valued applies_to (l.243) fits neither `system` nor `dataset`.
- The validator accepts a list with any scale, including `point` and `system`.
- **Fix:** state that a subset term is `dataset` scale (or a new reading of `system`), and enforce it.

**W4. Rule 7's point-scale `moves = both` term is underspecified** (l.87).
- **Point columns:** the rule doesn't say whether the term is excluded from both sides' point columns. "Never split" implies it but doesn't say so.
- **Size:** its size (an R_h error) lives in the observables table, but a size_column can name only a systems or measurements column (l.247).
- **Fix:** state both points.

**W5. The plotted rule for bound rows is not enforced** (l.115).
- `plotted = false` is not enforced by the validator: a probe with a plotted bound row passes.
- It is not in §10 or in the l.308 duties either.
- "Until the site does so in every view" is a time condition inside a frozen text, with no decision named for lifting it.
- **Fix:** enforce it in V, and say that lifting it needs a ruled decision.
- Minor: `limit_only` as the not-plotted reason sits oddly with "the bound is not a confidence limit". `other` with a note may be cleaner.

**W6. V l.356 is stricter than item 18 (l.306).**
- It requires the substring `**Ruling (`.
- D-001 to D-012 are ruled but use `**Ruling.**`, so the validator rejects them (scan confirmed).
- **Fix:** align the code with the text, or the text with the code.

## Notes

- **N1. Gating confirmed by probe.** `validate_v22` accepts lists and measurements size_columns for all v2 versions, and `CLOSED_V2` accepts `not_given_by_source` for all v2 versions. In both cases `validate_v24` rejects them below 2.4.0 (V l.280–298), and for 1.x packages `CLOSED` excludes `not_given_by_source` (V l.514).
- **N2. §10 items 14–18 are otherwise implemented as written.** Exceptions are W1 and W6. Item 15 covers observables (V l.304).
- **N3. Minor wording.** l.246 ("one-sigma size, or its published range") was not updated for `as_released`, `upper_bound` or `lower_bound`. l.110's duty "views say so" is not in the l.308 duties list.
- **N4. Markdown tables** render correctly: no orphan rows, column counts consistent (scripted check).
- **N5. Cause-neutral wording:** nothing in the new text or in D-093 assumes a cause. The `extra_mass_bound` name at l.166 predates 2.4.0.
- **N6. Housekeeping.**
  - D l.37 cites `standard-review-2.md`, which is not in the tree yet.
  - D-092 is still absent on this branch (the log jumps from D-091 to D-093).
  - `frozen_on: "on merge"` is accepted by `aeg.check`. Set the date at merge.
- **N7. Dwarfs v1 (2.0.0).** Read under its own text, its 7 limit rows still give g_bar errors the σ limit's level. This is not a 2.4.0 defect; it belongs in that dataset's known issues.
- **Verified:** tests, checks, hashes, the probes (`/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_std240b/probe/probe.py`), the table structure and the ruling-format scan. **Not verified:** site rendering, and the reader reports beyond review 1. Nothing in `/home/claude/atlas` was modified.

**Next step:** fix E1–E3 and W1, W2, W5 (all short text or code edits), add the two missing tests, then commit this review as `standard-review-2.md` and put D-093 to JvH.