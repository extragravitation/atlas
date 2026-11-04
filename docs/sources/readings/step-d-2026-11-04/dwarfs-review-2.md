# Independent review of the dwarf-galaxy v2 test, revision 2 (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

**Bottom line: do not freeze yet.** Every must-fix item from review 1 has been fixed, and nothing in the test assumes a cause. Seven problems remain, all cheap to fix in one more revision.

The biggest is that rule 5 ("one rule for every row") is applied unevenly in the frozen terms table, and the reading in item 11 could overturn it after the freeze. The others are gaps in the D-097 classes, an And XII level that would be wrong, the scope of item 2, and some misquotes.

The terms table is now structurally valid. I built a dummy package from the v1 tables plus the new columns and terms rows and ran `validate_v22` and `validate_v24`. Both pass, except that the new D-038 1A `assumption_id` is not in the registry yet, which is expected because the test adds that entry.

**Review-1 must-fix items, checked:**
1. Precedence: fixed. D-098 rule 5 is applied and conflicts go to JvH before conversion.
2. `half_light_radius`: fixed. It now uses a `size_column`, with `not_given_by_source` rows for each system that has no error.
3. `gas_inside_rhalf`: fixed. It is split into one row per system.
4. `size_column`: fixed. Rule 6 adds the companion `_lo` column.
5. The five systems: fixed. The IDs match v1's `MAG_OVERRIDE` list (And VI 0.07, And VII 0.10, Phoenix 0.1, Leo T 0.2, Tucana 0.16), and Leo T's empty error is handled.
6. Confidence levels: fixed. They now come from the second reading.
7. `r_kpc` and plotting exemptions, and the coverage re-run: fixed.
8. Second reading hashed before conversion, and blind adjudication: fixed.

## Errors (must fix)

1. **l. 43–45 against l. 123, l. 130 and l. 173: rule 5 is not applied consistently, and the reading can contradict the frozen table.**
   - `binaries` and `estimator_normalisation` are set to `not_given_by_source` because Wolf restricts those sizes to some systems.
   - `anisotropy_profile` is `given` 0.05 dex, but the test itself says "Wolf states it for its own analysis". Wolf l. 990–992 is about the M_half error bars of Wolf's own Jeans analysis growing under one extreme β(r) form. It is not about the estimator, and not about these systems.
   - `luminosity_function_martin` 0.2 mag comes from "A test performed by assuming that And I is instead…" (Martin l. 385), a test on one galaxy.
   - Item 11 also asks the reader to record "the scope of each stated size (rule 5)". Rule 5 sets the status, so the reading could overturn statuses that item 7 fixes as "exactly the rows below".
   - **Fix:** apply rule 5 now, at source. Either set both rows to `not_given_by_source` with the quotes in the note, or amend rule 5 and recheck `binaries` and `estimator_normalisation` under the amended rule. Then make item 11's scope field a confirmation only: any disagreement goes to JvH before conversion.

2. **l. 37–39: the D-097 classes are not mechanically decidable.**
   - **Mixed statements.** Collins 2013 l. 1423–1427 says And XXVII "is currently undergoing tidal disruption" (a finding). l. 1439 says it "may no longer be a gravitationally bound system" (a possibility). Nothing says which class wins, either within one source or across the sources that count. Add: "any finding in any source that counts makes the system a finding."
   - **Unclassed words.** "suggest", "consistent with", "possibly" and "perhaps" are not classed. Ji 2021's abstract itself uses "consistent with … tidal disruption" (l. 100).
   - **"Tidally disturbed" on its own.** l. 37 classes it only when it comes with a stated state. Alone, it is in no class, and "tidally stripped" or "perturbed" are not covered either. Put these in "neither" and cite D-097 rule 1's three states. If D-025's wording is meant to count instead, that needs JvH's ruling.
   - **Verbatim wording.** Use D-098's exact phrase "in its own words or by citing others".

3. **l. 40 against l. 181–183: the known findings conflict with "the converter takes D-097 classes only from that file".** If the reader classes And XXVII or Antlia II differently, the test does not say what happens.
   - **Fix:** say they are findings by ruling (D-097 rule 1's examples). The reading confirms each one at source, and any disagreement goes to JvH before conversion.
   - At source, both are confirmed findings. Collins l. 1426–1427 matches the quote verbatim, and also states the disruption as fact at l. 1424. Ji l. 104 is in the abstract; quote the full sentence ("…support a tidal disruption scenario for the origin of these large and extended dwarf spheroidal galaxies") in `excluded.csv`.

4. **l. 89: And XII `err_level` = 0.683 would misstate the limit.**
   - On a `limit = upper` row, `err_level` is the level of the limit (§3).
   - The upper end of a two-sided 1σ interval is not a 68.3 % one-sided limit, and Collins states no limit level.
   - Collins does say "formal 1σ confidence interval", at l. 1063, but for And XVIII.
   - **Fix:** set `err_level` empty and `not_given_by_source` unconditionally. Put the 1σ wording in the note. This follows D-093 rule 1.

5. **l. 59–65 against l. 91–94: item 2's "every other v1 column is unchanged" collides with item 6.** Item 6 changes the observables' `err_lo`, `err_hi` and `source_ref`. In v1, no `half_light_radius` or `structural_param` row carries an error.
   - **Fix:** limit item 2 to the measurements table. Then add a clause listing the allowed changes in observables and systems, with everything else in those tables unchanged.

6. **Misquotes and locators in a file that will be frozen.**
   - **l. 105:** "vary with radius" is not Pace's text. l. 699 reads "show changes in the position angle and/or ellipticity with radius".
   - **l. 27:** "calculated from all possible members" and "the certain members" are in the caption at l. 436, not at l. 446 and l. 452 (those lines hold only the values).
   - **l. 110:** Savino l. 952 is in §5 ("Checking the Robustness…"), not §4. l. 1244 is in §7 (Conclusions), not §6.
   - **l. 111, Medina l. 264:** my local copy (SHA 0eb83029…) has the passage at l. 266. Reader A's recorded hash is 3108c7…, so this cannot be confirmed against the copy that was read. Recheck it.

7. **l. 121 and l. 150: the D-038 1A `assumption_id` is not named.** So "exactly the rows below" cannot be checked, and it is the one item in my dummy run that fails the validator. Name the ID now, and record the dummy run before the freeze, not in the result (l. 151).

## Weaknesses (should fix)

- **l. 24–25:** "D-038 and the other value rulings choose the source … D-096 then chooses" reads as the precedence rule that D-098 rejected. Reword it as a statement of scope, and rely on the escalation clause.
- **Sizes in the terms table.**
  - `distance` and `ellipticity` (l. 103, l. 108) have no `size_kind`, which §7a requires for given rows.
  - `half_light_radius` (l. 101) says "`one_sigma` or as the second reading records". One row cannot carry mixed kinds: split it by kind, or fix the kind.
  - `distance_calibration_savino` has no `size_unit`.
- **l. 123 `correlated_with`:** §7a defines this field as the correlation "as the source states it". The test says the source does not state it, so move it to the note.
- **l. 80–81, "μ_paper cancels":**
  - For Phoenix and Leo T this holds only under D-061's `mv_modulus_assumed`.
  - For And VI and VII, M_V is from McConnachie 2006 and the modulus from McConnachie 2005.
  - Say "cancels under the D-061 / D-053 pairing", or have the reading confirm at source that the M_V was derived with that modulus.
- **l. 166–177, second reading:**
  - The D-096 and D-097 fields get one reader, compared only against step A, which did not classify every system. D-097 rule 4 says "second readers", plural.
  - R_h and ε errors were already read twice in v1 (`reading/structure_values_all.csv`, `err_minus`/`err_plus`). Compare against those too.
- **l. 36, sources that count:** D-098 rule 3's "for pooled data, the re-analysis papers behind it" is left out. Say how it applies to rows whose σ comes from Geha 2026, and say explicitly that magnitude originals do not count.
- **l. 150, registry formulas:** "the effects formulas above" exist only for R_h and distance. Write out the formulas for ε (a√(1−ε)), for the semi-major against circularised convention, and for the 4/3 parameter (r½ = k·R_h).
- **l. 30, Phoenix II coverage:** name the frozen code and the v1 coverage-config row (Richstein's centres and fits) to be used. State that if 11.0 fails, 9.5 is not promoted to default.
- **Fritz's abstract (l. 75) prints 9.5 km/s,** while the bold table row (l. 452) and the conclusions (l. 546, "for the preferred membership selection") give 11.0. Record this in rule 2 so the reader does not raise it as a D-055 item 2 conflict.
- **l. 55:** require the appended 9.5 alternative row to be bit-equal to v1 `m000051` on the g columns.
- **l. 162:** "where the σ is a member-sample σ" has no defined criterion. Say "every row that passed D-038 1A", or name the coding column.
- **l. 5:** "not edited after the first conversion run" leaves a window between merge and conversion. The KiDS test has the same wording. It should say "not edited after merge".
- **l. 157 and l. 191:** `data/registry/excluded.csv` exists nowhere, and no pipeline or site code reads it. Item 12's page check depends on a site feature that has not been built.

## Notes

- **Checked at source and correct:**
  - Fritz: l. 388, 393, 415, 436, 446 and 452 (the five certain members at 0.57, 1.78, 1.71, 1.82 and 1.54 R_half; Table 2, `mem` = 1).
  - Wolf: l. 150–152, 922–927, 990–992, 1212–1214 and 1797–1800.
  - Geha: l. 420 (k_v 1.4, floor 1.1 km/s) and l. 741 (1σ; 95th percentile).
  - Tollerud l. 268; Heiger l. 109; Kvasova l. 260; Collins l. 571–573.
  - Savino l. 952 and l. 1244 (wording); Carlin l. 114; Higgs l. 221–222 and l. 361; Vivas l. 264–266.
  - Martin l. 377, 379 and 385; Muñoz l. 416 and 468; Putman l. 166 and 176, and MRT Notes 4 and 22.
  - Pace l. 694 and l. 800.
  - Putman's HI mass errors are consistent with coming from distance alone: Leo T, 0.4E5 against 2.8E5, about 2 × 7 %.
- **All named system IDs match v1.** v1 has 64 rows, all plotted, 7 of them limits. `beyond_source_range` is on 39 rows.
- **D-098 applied:**
  - Rule 2 of D-096 is limited to the same data points ✓.
  - Three classes, including "neither" ✓.
  - Sources that count, except the pooled-data clause ✓.
  - Phoenix II default 11.0 ✓.
  - And XXVII and Antlia II are confirmed as findings at source ✓.
- **Neutrality:** nothing assumes a cause. Tidal wording appears only inside source quotations.
- **l. 201, Columba I:** the reason is that the existing plotting rules still apply, not "(rule 1)".
- **Housekeeping:**
  - I worked read-only, using `git show` and a detached worktree, which I removed.
  - The main checkout is now on `test/gc-v2`, not `decision/d-098`. I did not run a checkout, so another session changed it.
  - The dummy package and script are in `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/rev_dw3_dummy/` and `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/rev_dw3_scripts/mk.py`.

**Next step:** make the seven fixes in a third revision, name the new assumption ID and record the dummy validator run, then freeze. A second review is not needed if only these items change.