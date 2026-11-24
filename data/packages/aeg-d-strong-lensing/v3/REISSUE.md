# aeg-d-strong-lensing v3: re-issue under data standard 3.0.0

**Decision:** D-114. **Test:** `docs/standard-3.0.0-reissue-test.md` (T1 to T7), frozen with the standard before this package was built.

## What changed from v2

- **`sources.json`:** all 28 entries now have an `id` (S1 to S28), `kind`, `citation`, `identifier` and a structured `licence`. The record numbers (R5, R10, …) stay in `record`; R5 has several entries, so they cannot serve as ids.
  - Citations are built from the arXiv records read on 2026-11-24: exact titles, and author lists as arXiv gives them (the first three, then "et al."). Years and journal references come from the packaging inventory and the arXiv records.
  - The VizieR catalogue ids (J/ApJ/682/964, J/A+A/501/461, J/ApJ/845/157) are identifiers of the papers' tables.
- **New entry, S29:** the SLACS V e-print's LaTeX source (0805.1931v1). The locators of the 48 R_e observables cite its `ms_arxiv.tex` by line, but v2 recorded only the PDF. Its hash and the hash of `ms_arxiv.tex` equal those in the frozen reading `reading/profiles.csv`.
- **`locators.json` (new):** 29 rules resolve all 116 distinct `source_ref` values, 108 in observables and 8 in measurements. One rule carries a correction (below). Each measurement row names its observed and stellar records; its rule points to those records' entries and to the observables rows it is computed from.
- **`known_issues.json`:**
  - Issue #174 (gas and dust stated in two systems, not yet in the package) also applies to v3, so its measurement identifiers now read v3.
  - New issue #225 records the correction.
- **Version labels:** `descriptor.json` and `datapackage.json` carry v3, and identifiers in the tables read `aeg-d-strong-lensing/v3/…`.
- **`data/assumptions.json`:** the ten registry entries for v2 are copied to v3 unchanged.
- **`tests/`:** runs the re-issue test (T1 to T6) and the standard validator.

## Correction (issue #225)

Four lens-redshift observables cite "R21 Table 2 z_d (IOP ascii t2)". No IOP table for R21 is recorded or hashed anywhere in the package or its readings, and the reading gives the arXiv paper as the address. All four values (0.238, 0.274, 0.289 and 0.232) were checked on 2026-11-24 in Table 2 of the arXiv e-print 1307.4759v1. The rule points to R21's arXiv paper (S15), Table 2, column z_d, and quotes the text it corrects. No value changes.

## Licences

- **arXiv records (S9 to S29), read on 2026-11-24:**
  - R9 (S13) is CC BY 3.0 and R33 (S20) is CC BY 4.0. Both were already marked redistributable in v2.
  - Kochanek et al. 2000 (S25) and Bruzual & Charlot 2003 (S28) carry arXiv's "assumed 1991–2003" licence.
  - All the others carry the non-exclusive licence to distribute 1.0.
  - The three SPS model papers (S26 to S28), marked "not read" in v2, are now read.
  - v2's licence wording is kept in each entry's note.
- **VizieR exports (S1 to S3) and IOP tables (S4 to S8):** recorded as the packaging inventory read them on 2026-10-31. VizieR shows no licence on the record and its terms come through the export's `rights_uri`. The IOP pages state © AAS, all rights reserved. Neither was re-read for this check, because these hosts refuse connections from the build workspace. CI fetches and hash-checks every file on each run.

## What did not change

- **Values and text:** every table equals v2's once the version labels are mapped back (T1).
- **The converter:** `convert.py` differs from v2's only in its version line (T2). It still builds from v1's tables and v2's frozen reading, and checks both against their freeze records.
- **Carried over and still valid:** v2's frozen test (`REPRODUCTION.md`), its result, the second reading and `reading/`. The site takes the lens formula checks from v1, the earliest version that holds them, as it did for v2.

## Test result

- **T1 to T6:** pass (`reproduction/reissue_check.txt`). CI rebuilt the package and it equals the committed tables.
- **T7:** pass (`reproduction/reachability.json`, 2026-11-24). All 29 file addresses and all 21 landing pages returned 200. Of the 29 DOI links, 9 returned 200, 11 got HTTP 403 from the publishers, and 9 got HTTP 429 (too many requests) from doi.org. Every entry is hashed, so under T7 these are recorded, not failed.
