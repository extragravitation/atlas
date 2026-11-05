# aeg-d-kids1000-rar/v2: independent second reading (D-031 item 3; REPRODUCTION_REV3.md item 11)

- **Reader.** An independent agent session (Claude), 2026-11-05. It had no access to `convert.py`, the package tables or v1, other than the source URL and hashes in `v1/sources.json`.
- **Where it read.** The canonical tarball (`https://kids.strw.leidenuniv.nl/sci_data/brouwer2021_rar.tar`) was refused by the workspace proxy and was not worked around. The reader read the three RAR files, their covariance files and the README from the public GitHub mirror `rstpier/EFF_G_GALAXIES`, folder `KiDS Brouwer Weak Lensing/`, commit `7606a21d5e7118b49ec57aef79d357da87118346`, and the paper from its arXiv e-print (2106.11677, `RAR_paper_Brouwer_4.tex`, SHA-256 `45aa25ab…4b19`).
- **Frozen files** (`data/frozen/kids-v2-reading.json`, frozen before the first v2 conversion run):
  - `reading/kids-second-reading.csv`: g_bar, ESD_t, ESD_x, error and bias for each of the 45 rows, as printed, with the bin edges;
  - `reading/kids-bins.md`: the 15 bin edges derived from §2.1;
  - `reading/kids-d096.md`: the D-096 fields per file, and the SHA-256 of all seven release members;
  - `reading/scripts/read.py`: the parser.
- **Not committed.** The covariance reading, `kids-covariance.csv`, transcribes a release that is not redistributable. Its SHA-256 is held under `off_repo` in the freeze record. `convert.py` regenerates it with the frozen parser from the fetched release, into the gitignored `source/reading/`, and stops if the hash differs.

## Findings

- **Values.** Every number the package uses was read. The comparison with the package is item 11 of `REPRODUCTION_REV3.md`; the result is in `REPRODUCTION_RESULT.md`.
- **g_bar.** The released value is the arithmetic midpoint of its §2.1 bin, identical in the three files: a fixed coordinate, not a mean over the lenses (`kids-bins.md`). This corrects step A's "bin means" and changes no value.
- **D-096.** Two findings, both applied by ruling and no others:
  - the hot-gas variant is a non-fiducial alternative (D-096 rule 3);
  - KiDS-bright rows 1–8 lie beyond the source's isolation limit and are left out of its tests of analytical models (l. 508, 748, 821). This was beyond what the first frozen test allowed, so that test's item 11 failed, and D-103 re-issued the test as `REPRODUCTION_REV3.md`.
- **Provenance check.** The mirror's README has SHA-256 `b3680580…8645`. Whether the canonical tarball's members carry the same hashes is decided by `convert.py` against the fetched tarball (item 12).
