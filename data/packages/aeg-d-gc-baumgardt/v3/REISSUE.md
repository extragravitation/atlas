# aeg-d-gc-baumgardt v3: re-issue under data standard 3.0.0

**Decision:** D-114. **Test:** `docs/standard-3.0.0-reissue-test.md` (T1 to T7), frozen with the standard before this package was built.

## What changed from v2

- **`sources.json`:** all 169 entries now have their `id`, `kind`, `citation`, `identifier` and `licence`, in v2's order (S1 to S169):
  - S1 to S3: the database pages veldis.html, parameter.html and appendix.html (`web_page`);
  - S4: the Harris catalogue, mwgc.dat;
  - S5 to S8: the four VizieR exports of McLaughlin & van der Marel 2005;
  - S9 to S168: the 160 individual radial-velocity files;
  - S169: the arXiv e-print of Baumgardt, Sollima & Hilker 2020.

  No document is added. Every value in the tables is read from these files, not from the papers behind them, and every file already had a hash in v2.
- **VizieR exports:** they also list v2's hash-verified copies as `local_copies`, as the dwarf package does, because the VizieR mirror sometimes serves an error page to CI.
- **`locators.json` (new):** five rules resolve all 2,800 distinct `source_ref` values: 2,721 in observables and 79 in measurements. There are no corrections.
- **`known_issues.json`:** the measurement identifier of issue #159 now reads v3. Issue #160 names clusters, not rows, and is unchanged.
- **Version labels:** `descriptor.json` and `datapackage.json` carry v3, and identifiers in the tables read `aeg-d-gc-baumgardt/v3/…`. `reproduction/changes.json` is written by the converter and carries v3 identifiers too. `reproduction/score.json` is v2's result and is kept as it was.
- **`data/assumptions.json`:** the twelve registry entries for v2 are copied to v3 unchanged.
- **`data/registry/excluded.csv`:** v2's two exclusion rows, NGC 2298 and Pal 5, are repeated for v3.
- **`tests/`:** v3's test runs the re-issue test (T1 to T6) and the standard validator.

## A limit of the Harris locators

The Harris `source_ref` values do not name the cluster: all 145 distance rows read `mwgc.dat Part I, R_Sun`. The locator therefore gives the part and column, and describes the row by how the converter finds it: by the cluster's ID, matched to the system's `name_in_source` with v1's `norm_name`. The row is fixed, but only through the system the observable belongs to. The table text is not edited (D-114 Q1).

## What did not change

- **Values and text:** every table equals v2's once the version in the identifiers and the two version header lines are mapped back (T1).
- **The converter:** `convert.py` differs from v2's only in the line that sets `DATASET, VERSION, STANDARD` (T2). Its frozen-file check reads the frozen records at their recorded v2 paths, which are unchanged, and v3's `reading/` is a byte copy of v2's.
- **Carried over from v2 and still valid:** `REPRODUCTION.md`, `REPRODUCTION_RESULT.md`, `SECOND_READING.md` and `reading/`.

## Licences, as read on 2026-11-24

- **The database (S1 to S3, S9 to S168):**
  - No licence. The home page carries a copyright line for the seven authors (March 2023) and no terms of use.
  - veldis.html asks users to cite the papers it lists, as recorded in the A3 search log.
  - The file pages were not re-read, because the host refuses connections from the build workspace. CI fetches and hash-checks them on every run.
  - They are not redistributed.
- **Harris (S4):**
  - No licence established for mwgc.dat.
  - Other copies of the catalogue carry a notice that it is free of charge and must be passed on without charge, with a reference to the original website. The catalogue asks to be cited as "Harris 1996 (2010 edition)".
  - Not redistributed.
- **VizieR (S5 to S8):**
  - The CDS/VizieR terms of use, as named by the rights_uri of VizieR exports.
  - These four exports were not re-read.
- **The e-print (S169):** the arXiv non-exclusive distribution licence 1.0, as recorded in v2. Not redistributed.

## Test result

T1 to T6: see `reproduction/reissue_check.txt`. T7: see `reproduction/reachability.json`.
