# aeg-d-sparc/v2 — independent second reading (D-031 item 3; REPRODUCTION.md test 11)

- **Reader.** An independent agent session (Claude), 2026-11-01. It had no access to `convert.py`, the package tables, v1 or this repository. It worked only in its own folder, from the two source files and the brief.
- **Brief.** `reading/SECOND_READING_BRIEF.md`, committed before the reading was opened (commit `d1f15f9`).
- **Inputs.**
  - `MassModels_Lelli2016c.mrt` (SHA-256 `9108994b…`);
  - `SPARC_Lelli2016c.mrt` (SHA-256 `5aa0501f…`).
  
  These are the hashes recorded in `sources.json`. The canonical site (astroweb.case.edu) was unreachable from the workspace, so the files were taken from a public GitHub copy and accepted only because their SHA-256 equals the recorded hashes. CI fetches the canonical URLs.
- **Output.** `reading/second-reading/`:
  - `massmodels.csv` (3 391 rows) and `galaxies.csv` (175 rows), with every value as printed;
  - the reader's own parser (`parse_sparc.py`) and diagnostics;
  - `REPORT.md`, saved verbatim by Claude because the reader's session could not write `.md` files.

## Result

**PASS: every compared number agrees.**

| Compared | Count | Disagreements |
|---|---|---|
| Per row: R, V_obs, e_V_obs, V_gas, V_disk, V_bul, SB_disk, SB_bul (8 × 3 391), and D within its printed precision | 27 128 values, plus 3 391 distances | 0 |
| Per galaxy: name, D, e_D, Inc, e_Inc, Q, L[3.6], M_HI, V_flat and the rotation-curve references (10 × 175) | 1 750 | 0 |

The comparison is `tests/test_reproduction.py::test_11_second_reading`.

## The header issue, found independently

The reader found that the byte-by-byte header of `SPARC_Lelli2016c.mrt` describes a 113-byte layout, while the data lines are 131 bytes. Every field after the galaxy name is followed by a blank byte that the header omits, so field *k* sits *k* bytes to the right of its stated position. The reader verified this on all 175 rows with no exception, and resolved the layout from the data alone (arXiv was blocked for that session).

This agrees with the note in `docs/sources/sparc.md` and with the question put to the SPARC maintainers (courtesy note, 2026-11-01). `MassModels_Lelli2016c.mrt` has no such issue.

## Disagreements

None.
