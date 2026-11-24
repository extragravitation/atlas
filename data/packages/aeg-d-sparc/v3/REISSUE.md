# aeg-d-sparc v3: re-issue under data standard 3.0.0

**Decision:** D-114. **Test:** `docs/standard-3.0.0-reissue-test.md` (T1 to T7), frozen with the standard before this package was built.

## What changed from v2

- **`sources.json`:**
  - Both SPARC files, S1 (mass models) and S2 (galaxy sample), now have their `id`, `kind`, `citation`, `identifier` and `licence`.
  - A new entry, S3, is the SPARC paper's arXiv e-print (1606.09251v1). The `source_ref` values cite it for the distance methods and the gas-profile assumption. This is the first time the Atlas has recorded a hash for this paper.
- **`locators.json` (new):** six rules resolve all 19,412 distinct `source_ref` values: 16,021 in observables and 3,391 in measurements. One rule carries a correction (below).
- **`known_issues.json`:** the measurement identifiers of issue #8 now read v3, so the same four rows keep their `#8` and flag. The new issue #222 records the correction.
- **Version labels:** `descriptor.json` and `datapackage.json` carry v3, and identifiers in the tables read `aeg-d-sparc/v3/…`.
- **`data/assumptions.json`:** the five registry entries for v2 are copied to v3 unchanged.
- **`tests/`:** v2's frozen reproduction test stays in v2. v3's test runs the re-issue test (T1 to T6) and the standard validator.

## Correction (issue #222)

The 26 gas observables of D512-2, D564-8 and D631-7 cite "arXiv:1606.09251 §3.4" for the assumed exponential gas profile. The paper has no §3.4. The statement is in §3.3, Mass Models, at `SPARC.tex` l. 199: "For D512-2, D564-8, and D631-7, HI surface density profiles are not available, hence we compute V_gas assuming an exponential profile with a scale length of 2 R_d."

The locator rule gives §3.3, l. 199, and quotes the text it corrects. The table text stays as converted. No value changes.

The distance references, to §2.2 (Galaxy Distances, l. 113–121), are correct.

## What did not change

- **Values and text:** every table equals v2's once the version in the identifiers and the two version header lines are mapped back (T1).
- **The converter:** `convert.py` differs from v2's only in the line that sets `DATASET, VERSION, STANDARD` (T2). Its docstring still says "2.3.0 (aeg-d-sparc/v2)" because T2 allows no other edit.
- **Carried over from v2 and still valid:** `REPRODUCTION.md`, `REPRODUCTION_RESULT.md`, `SECOND_READING.md` and `reading/`.

## Licences, as read on 2026-11-24

- **S1 and S2, the SPARC files:** the SPARC home page states no licence, copyright or terms of use. It asks users to cite the SPARC master paper and to consider citing the original rotation-curve sources. The file headers were not read for this check, because the host refuses connections from the build workspace. CI fetches and hash-checks the files on every run. They are not redistributed, as before.
- **S3, the e-print:** the arXiv perpetual, non-exclusive licence to distribute 1.0. It is not redistributed.

## Test result

T1 to T6: see `reproduction/reissue_check.txt`. T7: see `reproduction/reachability.json`. Both results are summarised in the reproduction ledger and the pull request.
