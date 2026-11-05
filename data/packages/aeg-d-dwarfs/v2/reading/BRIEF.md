# Second reading for aeg-d-dwarfs/v2: brief (2026-11-04)

This brief serves item 11 of the frozen test `data/packages/aeg-d-dwarfs/v2/REPRODUCTION.md`, frozen in `data/frozen/dwarfs-v2-test.json`. Two readers, A and B, work independently. Neither sees the other's file.

## What you may and may not open

**You may open:**
- the frozen test;
- `docs/decisions.md` (D-025, D-036, D-038, D-051 to D-062, D-093, D-096 to D-099);
- `docs/data-standard.md`;
- the step A readings in `docs/sources/readings/step-a-2026-11-04/` (dwarfs-*);
- `v1/sources.json`, `v1/SECOND_READING.md` and `v1/reading/`;
- the three manifests in this folder. They are v1's rows, observables and systems with no g values.

**You may not open:**
- `v1/tables/measurements.ecsv`;
- any `convert.py`;
- any `REPRODUCTION_RESULT*`;
- any v2 table;
- the other reader's file.

You never compute g_obs or g_bar.

## Sources

Read the papers at source, from the arXiv e-print (LaTeX) wherever one exists. Record the e-print's SHA-256. Copies from step A are under `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/step-a-2026-11-04/dwarfs-A/dl/` and `dwarfs-B/dl/`, and from the reviews under `review_dwarfs2/src/`. Use them if the hash matches what `v1/sources.json` or the step A reading recorded. Otherwise fetch the e-print as step A did. Do not work around a blocked site.

Never state a value from memory. Every value you record has a quote and a location (file and line).

## What to record

Record it for every one of the 65 systems and 64 rows in the manifest, following item 11 and rules 1 to 6 of the frozen test.

Write it as one long-format CSV, `reader-<A|B>.csv`, with these columns:
`system_id, name, field, value, quote, location, source, sha256, note`

**`field` is one of:**
- `rh_err` and `eps_err`: as printed, or `none printed`.
- `sigma_level` and `mag_level`: the confidence level as stated, or `not stated`.
- `d096_preferred`, `d096_excluded` and `d096_fiducial`: `yes` or `no`, per source. For `yes`, say what is preferred or excluded, and, for exclusions, whether the Atlas computes from the same data points (D-098 rule 1).
- `d096_conflict`: a stated preference that conflicts with an earlier value ruling (D-052, D-055, D-061, D-062), or `none`.
- `d097`: one row per statement about equilibrium, binding or tides in the sources that count (D-098 rule 3; D-099 rule 2). `value` is `finding`, `possibility` or `neither`, by D-099 rule 4's words exactly.
- `d097_class`: one row per system. `value` is `finding`, `possibility` or `none`; any finding in any source that counts wins. And XXVII and Antlia II are findings by ruling: confirm them at source, or report disagreement in `note`.
- `binary_screening`: as item 9's closed list.
- `distance_inherited`: `yes` or `no`, with the source sentence.
- `mv_modulus_match`: only for the five systems of item 5. Whether the M_V used was derived with the modulus used.
- `size_scope`: one row per given size in item 7's table. Confirm whether the source states it for these systems or their class (rule 5).

Systems with nothing to record for a field still get a row, with `value` `none` and the sources checked in `note`.

## When you finish

Write a short summary at the end of your report:
- counts per field;
- every disagreement with the frozen test's stated expectations;
- every source you could not read.
