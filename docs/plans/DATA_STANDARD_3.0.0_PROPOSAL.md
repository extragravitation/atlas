# Data standard 3.0.0 (minimal): proposal for ruling

**Status: proposal, 2026-11-24. Not in force.** Written for D-113 item 1 (V0.3_PLAN.md §1, work step 1). Once JvH rules, the text goes to `docs/data-standard.md` as 3.0.0. It is frozen by hash, with the re-issue test in §5, before any package is re-issued.

## 1. Why

The audit (`docs/audit/AUDIT_RESULT.md`) found no wrong values in 254 rows. Provenance failed in 250 of them, for four reasons:

| Audit code | Rows | Cause | Fixed here by |
|---|---|---|---|
| P1 | 229 | `sources.json` has no citation | R1 |
| P2 | 243 | `sources.json` has no licence statement | R1 |
| P3 | 2 | a document named in a locator has no hashed entry | R2 |
| P4 | 10 | a locator gives no table, page or column, or names the wrong table | R4 |
| (KiDS) | 10 | the archive's members are not hashed | R3 |

Today, 36 of the 226 `sources.json` entries in the six v2 packages state a licence, and none states a citation. That text exists, but it lives in `SOURCE.md`, `descriptor.json` or the `role` field, outside the record a reader or a script checks.

## 2. Scope

**In:** the four requirements below and their checks. Nothing else changes, and every column, unit, meaning and value stays as in 2.5.1.

**Out (left for the full re-issue before v1.0):** structured citations (BibTeX fields), rewriting `source_ref` text inside the tables, new readings of sources, taxonomy changes. Methods text (D-113 item 2) is site and methods documentation, not the package standard.

**Why this is a major version:** fields that were optional become required (§0: making something required is breaking). Packages that state 2.x stay valid as published and are never edited (D-006). The v3 packages state 3.0.0.

## 3. Requirements

### R1. Every `sources.json` entry carries its identity, citation and licence

New required fields, added next to the existing ones (which stay unchanged):

| Field | Content |
|---|---|
| `id` | Short and unique within the package (for example `S1`). Existing record numbers are kept where a package already has them (the strong lenses' `R5`). |
| `kind` | `data_file`, `archive`, `document` or `web_page`. |
| `citation` | One string: the reference in the source's own recommended form where it gives one, otherwise authors, year, journal, volume and first page. For a database: its name, version or commit, and the paper it asks users to cite. |
| `identifier` | An object with at least one of `doi`, `ads_bibcode`, `arxiv` (with the version read, such as `1612.00065v2`), `vizier`, or `landing_url`. |
| `licence` | An object (below). |

The `licence` object:

| Key | Content |
|---|---|
| `status` | `stated`, `none_stated` or `asked` |
| `spdx` | The SPDX identifier, when `stated` and one exists (for example `CC0-1.0`, `CC-BY-4.0`) |
| `text`, `uri` | The terms as stated, when there is no SPDX identifier (for example the CDS/VizieR terms) |
| `checked_where`, `checked_on` | Where the licence was looked for and when (all statuses) |
| `asked` | A link to the request (an issue or a dated email record), when `asked` |

Consistency rule: `redistributable: true` is allowed only when `status` is `stated` and the stated terms permit redistribution. Otherwise the package links to the source and keeps only the hash (project rule 2).

### R2. Every document a value is read from is a source

Any paper, table, page or web page that a locator names gets its own entry, with the hash of the file actually read: the PDF, the arXiv source, or a saved copy of the page. Where no file can be retrieved, `sha256` is `null`, `unhashed_reason` says why, and the entry is also listed in `known_issues.json`. Such an entry still counts as a provenance failure in the re-run audit. A missing hash is recorded openly, never waved through.

### R3. Archives hash their members

An entry of kind `archive` has `members_sha256` for every member the conversion reads (X-COP already does this). With it, the package can be checked member by member even when the archive itself can no longer be fetched.

### R4. Every `source_ref` resolves to a source and a place in it

There is a new file, `locators.json`, next to `sources.json`. It holds a list of rules:

```json
{"table": "observables",
 "match": "^MassModels_Lelli2016c\\.mrt:data row (?P<row>\\d+), column (?P<column>\\w+)",
 "sources": ["S1"],
 "where": {"row": "{row}", "column": "{column}"}}
```

- `match` is a regular expression, anchored at the start, over the exact `source_ref` text.
- `where` uses keys from a closed list: `table`, `page`, `column`, `row`, `line`, `section`, `figure`, `hdu`, `member`. Each value is either literal text or a named group from `match`.
- Every `source_ref` in `observables` and `measurements` must match **exactly one** rule. Each rule names at least one existing `id` and at least one `where` key.
- **Corrections:** where the v2 text points to the wrong place (audit P4: the M_V values for CVn II and Leo I are in Table 6, not Table 1), the rule gives the correct place and a `correction` field quoting the v2 text. Each correction is also listed in `known_issues.json`. The table text is not edited (see the choice under Q1).

Rules keep this workable. There are about 23,000 distinct `source_ref` strings across the six packages (SPARC alone has 19,412, one per data row and column), but they follow a handful of patterns per package.

### R5. The descriptor agrees with `sources.json`

`sources.json` is the authority for citation and licence. The descriptor's `licenses`, `x_licence_status` and `x_citation` must not contradict it; the check compares them.

## 4. Choices for JvH

**Q1. Where do the locators go?**
- **A (recommended): a separate `locators.json`; the tables stay unchanged apart from the version label.** This keeps D-113's promise: `convert.py` is unchanged except its version constants, and the values are provably the same. The cost is that a reader of a table sees the v2 `source_ref` text and must look in `locators.json` for the resolved place and any correction.
- **B: rewrite `source_ref` in the v3 tables** (prefix the source `id` and fix wrong places in the text). The tables read cleanly on their own. But every `convert.py` changes, the table identity test has to exempt one column, and the re-issue is no longer mechanical.

**Q2. A document that can't be retrieved as a file (paywalled or offline).**
- **A (recommended): the entry has `sha256: null` with a reason, is listed as a known issue, and counts as a failure in the re-run audit.** Where an arXiv version exists, hash that and record which version was read.
- **B:** accept a citation without a hash for documents (but not for data files) and pass it. This would weaken the provenance rule to make the audit pass, so I don't recommend it.

**Q3. Citation form.**
- **A (recommended): one `citation` string plus the `identifier` object.** It is enough to find and cite the source, and it can be filled from text the packages already hold.
- **B:** structured fields (authors, year, journal and so on, BibTeX-ready). Better for tools, but it is more work and better suited to the v1.0 re-issue.

## 5. Re-issue test (frozen by hash before the first v3 package is built)

For each of the six packages, v3 passes only if all of these hold:

1. **Same tables.** Take each v3 table, replace `<dataset>/v3/` with `<dataset>/v2/` in the identifiers and set the two header lines `version` and `standard_version` back to v2's values. The resulting file must have the same sha256 as the v2 table. (A literal "bit for bit", as written in V0.3_PLAN.md, is impossible because the version is part of every measurement identifier and of the table header. This is the exact form of that promise.)
2. **Same code.** `convert.py` differs from v2's only in the line that sets `VERSION` and `STANDARD`.
3. **Complete entries.** Every `sources.json` entry has the R1 fields, with valid values, and meets the redistribution rule.
4. **Every locator resolves.** Every `source_ref` in `observables` and `measurements` matches exactly one rule; every rule names existing ids and at least one `where` key.
5. **Archives covered.** Every archive member named in a `where.member` value or a `match` group has a hash in `members_sha256`.
6. **Descriptor consistent.** The descriptor's licence and citation statements agree with `sources.json`.
7. **Addresses reachable.** Every `url` and `landing_url` returns HTTP 200 after redirects, on a dated run, or is recorded as unreachable with its hash present. This runs as a GitHub Actions job: the build workspace cannot reach most of these hosts.

Tests 1 to 6 become part of `python -m aeg.check` for every package that states 3.0.0. Test 7 runs on a schedule and on release.

## 6. Work after the ruling, in order

1. Write 3.0.0 into `docs/data-standard.md`, keep 2.5.1 at its own path, freeze both the standard and this test, and log the decision.
2. Add the checks to `aeg.check`, with tests that fail on purpose.
3. Re-issue the six packages as v3, one pull request each, smallest first: KiDS, SPARC, X-COP, strong lenses, dwarfs, globular clusters (169 entries). The dwarf package will gain the most new `document` entries, because its locators name many papers.
4. Point the site at v3, then run the audit again under a newly frozen plan (D-113 item 3).
