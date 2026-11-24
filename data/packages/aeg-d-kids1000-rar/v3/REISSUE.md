# aeg-d-kids1000-rar v3: re-issue under data standard 3.0.0

**Decision:** D-114. **Test:** `docs/standard-3.0.0-reissue-test.md` (T1 to T7), frozen with the standard before this package was built.

## What changed from v2

- **`sources.json`:**
  - The release tarball (S1) now has its `id`, `kind`, `citation`, `identifier`, `licence` and `members_sha256`. The member hashes are the seven in the frozen reading `reading/kids-d096.md`. `convert.py` checks each one against the tarball before it writes a table.
  - A new entry, S2, is the paper's arXiv e-print (2106.11677v1), which the readings and the tables quote by section and line.
- **`locators.json` (new):** three rules resolve all 135 distinct `source_ref` values, 90 in observables and 45 in measurements.
- **Version labels:** `descriptor.json`, `datapackage.json` and `known_issues.json` carry v3. Identifiers in the tables read `aeg-d-kids1000-rar/v3/…`.
- **`data/assumptions.json`:** the three registry entries for v2 are copied to v3 unchanged.

## What did not change

- **Values and text:** every table equals v2's once the version in the identifiers and the two version header lines are mapped back (T1).
- **The converter:** `convert.py` differs from v2's only in the line that sets `DATASET, VERSION, STANDARD` (T2). Its docstring still says "2.5.1 (aeg-d-kids1000-rar/v2)" because T2 allows no other edit. The paths to v2 in `regenerate_reading()` are keys into the freeze record `data/frozen/kids-v2-reading.json`. That record covers the same reading files, which are copied here unchanged.
- **Carried over from v2 and still valid:** `REPRODUCTION*.md`, `SECOND_READING.md`, `reading/` and `reproduction/`. v3 makes no new reading and no new reproduction claim; its claim is T1.

## Licences, as read on 2026-11-24

- **S1, the release:** no licence is stated, either on the KiDS science-data page entry or in the release README. The page asks users of KiDS data to include the acknowledgements given in the paper. The release is not redistributed, as in v2.
- **S2, the e-print:** the arXiv perpetual, non-exclusive licence to distribute 1.0. That licence gives distribution rights to arXiv only, so the e-print is not redistributed. The journal version is open access under CC BY 4.0, but the file hashed here is the arXiv e-print.

## Test result

Reported in the pull request. T1 is checked twice: by `python -m aeg.reissue_check aeg-d-kids1000-rar`, and in CI, where the package is rebuilt from the canonical tarball and must equal the committed tables. T7 runs in the reachability workflow, and its dated result is committed to `reproduction/reachability.json`.
