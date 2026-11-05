# Independent review of the KiDS v2 test re-issue (REV3), draft (2026-11-05)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Review: `REPRODUCTION_REV3.md` (test/kids-v2-rev3 @ 6a6f576)

## Bottom line

**Not ready to freeze yet. The fixes are small.** The core of the re-issue is sound and keeps to D-103:
- KiDS-bright rows 1–8 are recorded and not plotted.
- No value changes.
- The test needs no `x_value_change_ruling`.
- The validator accepts the settings it requires.
- The reading files are reproducible.

Four things must be fixed before the hash is taken, because the file cannot be edited after merge: a false statement about the scope of the changes, an overstated claim about what the source excluded, a misquote of l. 821, and an unprotected path for the off-repo covariance file. Optionally, also record the original test's hash.

**What I verified:**
- **Quotes at source.** l. 508, 748 and 821 are verbatim in `RAR_paper_Brouwer_4.tex`, whose SHA-256 is `45aa25ab…4b19` and matches D-103. l. 174, 421, 438, 483, 489 and 512 also say what the test cites them for. l. 525 is the Fig. 5 caption with the shaded region, as D-103 says.
- **Frozen hashes.** All four reading files and REV3 match their freeze records.
- **Parser rerun.** Rerunning `read.py` on the mirror reproduces `kids-second-reading.csv` (`eaca59f7…`) and the off-repo `kids-covariance.csv` (`1d111169…`) exactly.
- **Mirror files.** The mirror is at commit `7606a21d…`, and all seven file hashes match `kids-d096.md`.
- **The reading's claims.** The three files have identical g_bar values, all 45 rows lie inside their bins, and rows 8 and 9 have g_bar 7.3580e-14 and 1.2982e-13.

## Errors (must fix)

1. **The claim about what changed is false (l. 5–13).** The test says "The only changes are those D-103 requires" and "unchanged in substance". The diff against `REPRODUCTION.md` also contains changes D-103 does not require:
   - The g_bar midpoint correction (items 5 and 8). This comes from the second reading, not D-103.
   - The move to standard 2.5.1.
   - A new `notes` exception in item 2.
   - Item 11's pass rule changed. "A disagreement is resolved at source; one resolved against the package is a fail" became "Any mismatch is a fail", and a covariance criterion was added.
   - The new `x_value_change_ruling` bullet (item 10).
   - The new "Order of work" scoring rules.

   **Fix:** reword l. 5 to "Changes: those D-103 requires, plus the following, which are listed so the record is complete", and list each one. None of them needs a separate ruling, but a frozen record must not misstate its own scope.

2. **"Out of every model comparison" overstates the source (l. 36), and so does the frozen note text (l. 101, "excluded by the source from its own analysis").**
   - l. 508 first gives χ²_red = 4.6 and 5.0 for MOND and EG using all KiDS-bright points, and only then the seven-point result.
   - l. 748 says the comparison with MICE uses all points, with the redshift offset mimicked in the simulation. Only "the analytical models (MOND, EG and N17)" are restricted.
   - D-103's own wording is narrower: "every model comparison they draw conclusions from".

   **Fix (l. 36):** "The source leaves the KiDS-bright points beyond its isolation limit out of its tests of the analytical models (MOND, EG, N17; l. 748)."
   **Fix (l. 101):** "excluded by the source from its tests of analytical models (l. 748); recorded, not plotted".

3. **The known issue misquotes l. 821 (l. 65).**
   - l. 821 writes "R>3", not "R < 3".
   - l. 483 and 489 write "R > 0.3". Only l. 748 has "R < 0.3".

   **Fix:** "The source gives the limit as 3 h70⁻¹ Mpc (l. 508 'R < 3'; l. 821 'R>3') and as 0.3 h70⁻¹ Mpc (l. 483, 489 'R > 0.3'; l. 748 'R < 0.3')." D-103 rule 3 has the same slip, so note the correction in the known issue.

4. **The off-repo covariance path is not gitignored.** `data/frozen/kids-v2-reading.json` puts `kids-covariance.csv` at `data/packages/aeg-d-kids1000-rar/v2/reading/`, which is a tracked directory. Regenerating it there in CI or locally risks committing a full transcription of a release that cannot be redistributed.

   **Fix:** regenerate it under a gitignored path (`data/cache/` or `…/v2/source/`), name that path in item 11 and in the record's `off_repo` key, or add a `.gitignore` entry for that one file.

## Weaknesses (should fix)

1. **The original test is not hash-protected.** No `data/frozen` record covers `v2/REPRODUCTION.md`. Its own freeze relied on a `v2/sources.json` that does not exist yet. D-103 rule 2 requires it to "stay as it is", and REV3 depends on that. **Add** `"data/packages/aeg-d-kids1000-rar/v2/REPRODUCTION.md": "b44f5a58fd545d7eb4927ffae341a06cfa4aa3c3e9598affa1dad0a84631190b"` (the current hash on main, last changed in e3e10aa) to `kids-v2-test-rev3.json`.

2. **Item 11's pass rule cannot be checked as written.**
   - "Every packaged number equals the frozen reading" needs a mapping, because g_obs is not in the reading. Name the pairs:
     - `delta_sigma`, `err_lo` and `err_hi` against `ESD_t` and `error`;
     - `acceleration_released` and `g_bar` against `g_bar`;
     - `g_bar_bin_lo/hi` against `bin_lo/hi`, at item 5's 1e-12 tolerance;
     - the bias column against `bias`, if it is packaged.
   - "Divided by the bias column as the README states" is ambiguous. The README divides the covariance by the covariance file's column 7, which is the product (1+K_i)(1+K_j). It is not the ESD file's `bias`. Say "column 7 (`bias_product`)".

3. **Item 12 checks only the README against the tarball.** All six data and covariance files were also read from a third-party mirror. That repository is someone's working tree: it contains `_fit_*` directories and a PNG.
   - A Nobins file that differs from the tarball would show up only indirectly, as a package-versus-reading mismatch.
   - **Extend item 12:** CI checks all seven tarball members against the hashes in `kids-d096.md`, and any mismatch fails before conversion.
   - Also state what happens if CI cannot reach the tarball either: blocked, not scored.

4. **Item 2's `notes` exception is wider than it reads.** "Notes on the rows named in test 9" covers all 45 rows, because test 9 names every row and its `model_dependence` bullet adds text to every row's notes. Say so plainly: "`notes` on all rows, with content set by tests 5 and 9". Rows 1–8 versus item 2 is otherwise consistent: `role`, `plotted` and `not_plotted_reason` are among the excepted columns.

5. **D-096 rule 4 is not carried over.** The rule requires the result to state how many rows change because of the ruling. The GC test does this at its l. 259. **Add to item 15:** "states that 8 rows change plotting status under D-096 rule 2 (D-103) and 15 under rule 3".

6. **Order of work, step 2, cannot be followed literally.** `kids-d096.md` is prose and cannot be parsed. Say instead that `convert.py` encodes "KiDS-bright rows 1–8: plotted = false" citing item 9, and that test 11 checks it against `kids-d096.md`.

7. **Merge order.** D-103 is only on `decision/d-103-104`. Merge it before or with this PR so that every reference resolves.

## Notes

- **`excluded.csv`.** Leaving these rows out is consistent with standard §5, whose register has columns `system, dataset, reason, citation` and lists systems. It also matches how GC v2 handles the M54 data-point cut. The page statement in item 9 covers the display.
- **`x_value_change_ruling`.** The reasoning holds: §9 applies to "values", and §10 item 13 compares only g_obs and g_bar. It would be stronger to cite D-103 rule 1 ("No value changes") as the authority. That rule explicitly overrides the original item 11's route to a version that changes values under D-096 rule 5.
- **Item 11 accepting exactly two findings** matches `kids-d096.md`:
  - the hot-gas variant;
  - KiDS-bright rows 1–8;
  - no exclusion in GAMA or the README.

  The hot-gas rows inherit the isolation caveat by radius, and this is already disclosed in item 6.
- **Row 8.** Its bin is [5.32e-14, 9.39e-14], which straddles 7.56e-14. The count of "seven data points" in l. 508 settles which rows are excluded, as the test says.
- **The second reader's independence.** The reader saw the original test text, which describes how v1 handles these rows (`kids-d096.md` §1). That is within its brief, but it is not quite "no access to v1".
- **Cosmetic issues in frozen reading files** (leave them, since they are frozen):
  - `kids-bins.md` numbers its checks 1 and 3, with no 2;
  - `kids-d096.md` has a blank header line and no date or reader line.
- **Neutrality.** Nothing assumes a cause. The test describes the source's satellite and photo-z reason as the source's own.
- **Validator.** The validator (`pipeline/aeg/validate.py`) accepts every setting the test requires:
  - `other` is a valid `not_plotted_reason`;
  - `role = default` with `plotted = false` is allowed;
  - 2.5.1 is a known standard version;
  - `g_bar_bin_*` is allowed only with `bin_coordinate`.
- **Cleanup.** I removed my review worktree and scratch outputs. The fetch added remote-tracking refs and nothing else. The main checkout's existing modification to `excluded.csv` on `convert/gc-v2` was there before this review and was not touched.

**Next step:** apply errors 1–4 and weakness 1 on the branch, recompute the REV3 hash in `kids-v2-test-rev3.json`, then merge D-103 first and this PR second.