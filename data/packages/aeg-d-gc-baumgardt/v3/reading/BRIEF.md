# Second reading for aeg-d-gc-baumgardt/v2: brief (2026-11-04)

This brief serves item 11 and the order of work in the frozen test `data/packages/aeg-d-gc-baumgardt/v2/REPRODUCTION.md`, frozen in `data/frozen/gc-v2-test.json`.

## What you may and may not open

**You may open:**
- the frozen test;
- `docs/decisions.md` (D-025, D-036, D-038, D-045 to D-047, D-093, D-096 to D-099);
- `docs/data-standard.md`;
- the step A readings in `docs/sources/readings/step-a-2026-11-04/` (gc-*);
- `v1/sources.json`;
- `v1/SECOND_READING.md`;
- `v1/source/` (veldis.html, parameter.html and the other source files);
- the three manifests in this folder. They are v1's rows, observables and systems with no g values.

**You may not open:**
- `v1/tables/measurements.ecsv`;
- any `convert.py`;
- any `REPRODUCTION_RESULT*`;
- any v2 table.

You never compute g_obs or g_bar.

## Sources

The sources that count are set by rule 2 of the frozen test:
- the re-analysis papers B17, BH18 and B19 for the RV code;
- the integral-field and other dataset-code papers;
- McLaughlin & van der Marel (2005);
- Harris (2010).

Read them at source, from the arXiv e-print wherever one exists, and record each one's SHA-256. Copies from step A and review 2 are under `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/step-a-2026-11-04/gc-A/dl/`, `gc-B/dl/` and `review_gc2/dl/`. Use them if the hash matches the recorded one. Otherwise fetch the e-print as step A did. Do not work around a blocked site.

**For the D-099 rule 3 anchors,** read the four papers cited at Harris l. 125–127 (Rees 1996; McLaughlin et al. 2006; van de Ven et al. 2006; van den Bosch et al. 2006) and list the clusters whose distances they give.

Never state a value from memory. Every value has a quote and a location.

## Output files (in this folder)

**`d096_d097.csv`** has the columns:
`system_id, name, field, value, quote, location, source, sha256, status, note`

- **`field` is one of:**
  - `d096_preferred`, `d096_excluded` and `d096_fiducial`: per source. For exclusions, say whether the Atlas computes from the same data points. If it does, list the v1 bins dropped, by observable ID and ⟨r⟩.
  - `d097`: one row per statement, classed by D-099 rule 4's words.
  - `d097_class`: one row per system.
  - `harris_anchor`: `yes` or `no`, with the anchor paper's sentence.
- **`status`** is `read`, or `ruled` for the outcomes D-098 and D-099 fixed:
  - the M54 cut: bins with ⟨r⟩ > 200″, at 269.01″, 410.12″ and 679.1″;
  - NGC 2298 and Pal 5 as findings.

  Write these `ruled` rows yourself, and confirm each at source. If you disagree, keep the ruled value and write your dissent in `resolutions.md`.

**`err_levels.csv`** has the columns:
`dataset_code, level, status, quote, location, source, sha256`

It has one row per dispersion dataset code in the manifest (`x_gc_baumgardt_dataset`), plus one row for g_bar's level from MvdM.

**`binary_screening.csv`** has the columns:
`dataset_code, value, quote, location, source, sha256`

`value` comes from item 9's closed list.

**`resolutions.md`** holds any dissent from a ruled outcome, and any disagreement you find with the frozen test's stated expectations. Write "None." if there is none.

Every cluster with a measurement row gets at least a `d097_class` row and a `harris_anchor` row.

## When you finish

Write a short summary at the end of your report:
- counts per field;
- every disagreement;
- every source you could not read.
