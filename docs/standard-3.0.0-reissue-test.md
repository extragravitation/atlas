# Re-issue test: v2 → v3 under data standard 3.0.0

**Frozen with data standard 3.0.0** (D-114; `data/frozen/data-standard-3.0.0.json`), before any v3 package is built. It applies to each of the six packages: `aeg-d-kids1000-rar`, `aeg-d-sparc`, `aeg-d-xcop`, `aeg-d-strong-lensing`, `aeg-d-dwarfs`, `aeg-d-gc-baumgardt`. A v3 package ships only if it passes every test. A failure is reported as it is; the test is not changed after a result (project rule 5).

Purpose: show that v3 adds source records and locators and changes no value (D-113 rule 1.1, D-114).

## Definitions

- **v2, v3:** `data/packages/<dataset>/v2/` and `.../v3/`.
- **N(file):** the v3 file with these replacements, and no others:
  1. every occurrence of `<dataset>/v3/` replaced by `<dataset>/v2/` (the version inside identifiers);
  2. the header line `# - {version: v3}` replaced by `# - {version: v2}`;
  3. the header line `# - {standard_version: 3.0.0}` replaced by v2's own `standard_version` line (`2.5.1`, or `2.3.0` for SPARC).

## Tests

**T1. Same tables.** Every file in `v2/tables/` exists in `v3/tables/` and no other file is there. For each, sha256(N(v3 file)) = sha256(v2 file), with one exception. In the `known_issues` column, a v3 cell may list issue numbers the v2 cell does not (new provenance issues raised under §13 R2 or R4). It may not drop any. With that column's cells set back to the v2 cells, the hash must match. Every added issue number is listed.

**T2. Same code.** `v3/convert.py` differs from `v2/convert.py` only on the line that assigns `DATASET, VERSION, STANDARD` (VERSION `"v3"`, STANDARD `"3.0.0"`).

**T3. Complete source records.** `v3/sources.json` passes data standard 3.0.0 §10 items 19 to 21. Every v2 entry is still present, with its `url`, `file`, `bytes` and `sha256` unchanged.

**T4. Every locator resolves.** `v3/locators.json` passes §10 item 23. The counts of rules, matched `source_ref` values and corrections are reported.

**T5. Archives covered.** §10 item 22.

**T6. Descriptor consistent.** §10 item 24.

**T7. Addresses reachable.** Every `url` and `identifier.landing_url` in `v3/sources.json` (and every `doi`, through https://doi.org/) returns HTTP 200 after redirects on a dated run. Any that do not are listed with their date and HTTP status, and the entry's `sha256` must not be null. This runs as a GitHub Actions job, because the build workspace cannot reach most of these hosts. It runs once per package before it ships, and the dated result is committed to `v3/reproduction/reachability.json`.

## Reporting

Each package's pull request gives the result of T1 to T7: each test's pass or fail, the counts in T4, the issues added under T1, and the unreachable addresses under T7. Entries with `sha256: null` (§13 R2) are counted and listed. They do not fail this test, but they count as provenance failures in the re-run audit (D-114 Q2).
