# Independent audit: plan, version 2 (frozen)

**Frozen:** 2026-11-01, under D-082, before the seed exists and before any audit reading. The hashes of this file and of `docs/audit/sample_v2.py` are in `data/frozen/audit-plan-v2.json`. Any change after freezing is a new version, with the reason logged. This file is never edited in place.

**Supersedes version 1** (`AUDIT_PLAN.md`, D-081), which is kept unchanged. Version 1's frame listed four shipped packages; six are shipped. The globular-cluster (`aeg-d-gc-baumgardt/v1`) and dwarf-galaxy (`aeg-d-dwarfs/v1`) packages were left out in error. Version 2 adds them and changes nothing else. Version 1's seed was never read, and no sample was drawn under it.

**Purpose.** Work package 3 of `docs/plans/REVIEW_READINESS_PLAN.md`:
- (A) an independent re-derivation of a random sample of the Atlas's shipped measurements from their original sources;
- (B) a neutrality audit of the published site.

The results are published whether they pass or fail, and are never re-scored.

## 1. When it runs

- After work packages 1 and 2 are merged, so that it audits what reviewers will see.
- The audited state is the main-branch commit at the start of the run, recorded in the result.
- The sample frame (section 2) is fixed by measurement identifiers now, so later work cannot choose which rows are audited.

## 2. Part A: re-derivation

### 2.1 Frame

- **Rows:** every measurement row in the six shipped packages whose `role` is empty or `default`. Alternative rows are excluded; they are never plotted.
- **Strata:** one per package.
- **Counts:** as at main commit `d102bc9` (2026-11-01).

| Stratum | Rows in frame |
|---|---|
| `aeg-d-sparc/v1` | 3 391 |
| `aeg-d-xcop/v1` | 861 |
| `aeg-d-kids1000-rar/v1` | 45 |
| `aeg-d-strong-lensing/v1` | 94 |
| `aeg-d-gc-baumgardt/v1` | 64 |
| `aeg-d-dwarfs/v1` | 64 |

Packages shipped later are not in this audit; they get their own.

### 2.2 Sample size

- Per stratum: n = min(N, max(⌈0.05 N⌉, 10)).
- That gives 170 + 44 + 10 + 10 + 10 + 10 = **254 rows**.

### 2.3 Seed

- **Source:** a public random value that does not exist when this plan is frozen and that no one involved can influence.
- **Primary:** the `outputValue` of the NIST Randomness Beacon (version 2.0, chain 2) pulse with the earliest `timeStamp` at least 24 hours after the merge commit that freezes this version of the plan.
- **Fallback:** if the NIST beacon is unreachable for 72 hours after that time, the `randomness` of the drand mainnet ("default") chain round with the earliest time at least 24 hours after that merge commit.
- **Record:** the pulse (or round) identifier, its timestamp, the value, and the URL it was read from go into the result before the sample is drawn.

### 2.4 Draw

- `python docs/audit/sample_v2.py SEED_HEX` on the audited commit. It is standard library only and frozen with this plan.
- **Method:** for each stratum, the measurement identifiers are ranked by SHA-256(`seed` + `|` + `measurement_id`), ascending. The first n are the sample; the rest are the reserve, in rank order.
- **Replacement** happens only if a sampled identifier no longer exists in the audited commit (for example, removed by a logged correction). It is replaced by the next reserve identifier in its stratum, and the replacement is reported.

### 2.5 Readers

- **Who:** two independent readers per row, who are fresh agents with no access to the Atlas's values.
- **Isolation:** each reader works in its own folder. Neither sees the other's work, the Atlas measurement tables, the site, or this repository's converters.
- **What each reader gets:**
  - the measurement identifier;
  - the dataset's citation, and the source file or document with the row locator from `source_ref`;
  - the Atlas's written method for that dataset (the methods page and the package's `SOURCE.md`). Its constants and assumption defaults are kept. Any measured or derived values of individual rows are removed;
  - the brief in section 2.6.
- **What each reader does:**
  - transcribes the inputs from the source;
  - computes g_obs and g_bar in m s⁻² with their own code, following the written method;
  - records any step where the written method was not enough to compute the value.

### 2.6 Reader brief (fixed text)

> You are auditing one measurement of a public dataset. From the source given, read the inputs that the written method needs, exactly as printed, with their units and where you found them (page, table, row, column, or file and row). Then compute the observed acceleration g_obs and the baryonic acceleration g_bar, both in m s⁻², with your own code, following only the written method. Use only the constants stated in the method. If the method does not say how to do a step, do not guess: record "method incomplete" and what was missing. If you cannot read a value, record "unreadable" and why. Return one CSV row per measurement with: measurement_id, each input with its unit and locator, g_obs, g_bar, and notes. Do not look for or use any other copy of this dataset.

### 2.7 Comparison

- **Script:** `docs/audit/compare.py`, written and committed before any reading is opened. It compares each reader with the other and with the Atlas row.
- **Tolerances:**
  - **Inputs:** equal at the source's printed precision.
  - **Accelerations:** |Δ log₁₀ g| ≤ 0.005 dex for g_obs and for g_bar.
- **Codes per row:**
  - **agree:** both readers agree with each other and with the Atlas.
  - **reader disagreement:** the readers differ from each other; adjudicated at source.
  - **Atlas discrepancy:** the readers agree with each other but not with the Atlas.
  - **method incomplete**
  - **unreadable**

### 2.8 Adjudication

- Every non-"agree" row is settled by reading the source again, with the reading quoted in `docs/audit/adjudication.md`.
- **Material discrepancy:** the Atlas is wrong on an input, or by more than 0.005 dex on g_obs or g_bar, for a reason other than reader error.
- **Method incomplete** is a finding in its own right, against the methods text, even when the Atlas value is right.
- Each adjudication is labelled with who made it. If Claude adjudicates, that is disclosed as not blind.

### 2.9 Provenance check (same rows)

For each sampled row, a reader checks that the source's citation, licence statement, units and file hash in the package's `sources.json` exist and refer to the document the value came from. Any failure is a finding.

### 2.10 Outcome (fixed before the draw)

- **Reported, per stratum and overall:**
  - the counts per code;
  - the number of material discrepancies;
  - the 95 % Clopper–Pearson upper bound on the material-discrepancy rate.
- **Pass:** zero material discrepancies and zero provenance failures.
- **Any material discrepancy or provenance failure:**
  - the audit result stays as observed;
  - the cause is classified;
  - the whole package is checked for that cause, labelled exploratory;
  - each confirmed error is corrected by a new version and entered in the public corrections log.
- **Method incomplete:** fixed in the methods text, and reported.

## 3. Part B: neutrality

### 3.1 Scope

All text a visitor can read on the built site at the audited commit: every page in the build, chart labels and legends, tooltips, slider labels, download README files, and the dataset and system descriptions.

### 3.2 Term scan

A script, committed before it is run, lists every occurrence (case-insensitive, whole words) of:
- "dark matter";
- "halo" and "haloes" (also "halos");
- "missing mass";
- "mass discrepancy";
- "unseen", "invisible" or "hidden" followed by mass or matter;
- "MOND";
- "Milgrom";
- "modified gravity";
- "modified Newtonian";
- "emergent gravity";
- "a0" and "a₀";
- "acceleration scale";
- "NFW";
- "Einasto";
- "Burkert";
- "explains" and "explained by";
- "evidence for".

Each occurrence is classified by a reader as either:
- **allowed:**
  - quoting a source;
  - naming an account in the confrontations section;
  - the single note on the conventional term "mass discrepancy";
  - naming a source's own fitting function as the source's method;
- **finding:** any other use.

### 3.3 Reader review

- **Who:** two fresh readers, independently.
- **Pages:**
  - the home page, About, Methods, Known issues, For data providers and Coverage;
  - every dataset page;
  - two system pages per shipped dataset, chosen with the seed of section 2.3, rank 1 and 2 by SHA-256(`seed` + `|page|` + `system_id`).
- **Checklist for each page:**
  1. Does any sentence, label or visual assume a cause of the acceleration discrepancy?
  2. Does any favour one account over another, by wording, ordering, colour or emphasis?
  3. Does any label or category name carry a result (for example, a class named by its g_obs/g_bar value or by an interpretation)?
  4. Is a continuous property binned or thresholded where the data do not require it?
  5. Are the plain and expert versions both present and saying the same thing?
  6. Is any number shown without a visible route to its source?

### 3.4 Outcome

- Every finding is logged in `docs/audit/neutrality.md`, with the page, the text and the reader.
- Each finding is resolved by a change (a pull request) or by no change, with the reason.
- **Pass:** zero findings left unresolved. The finding counts are reported either way.

## 4. Reporting

- **Result file:** `docs/audit/AUDIT_RESULT.md`, with:
  - the audited commit;
  - the seed record;
  - the sample;
  - the counts;
  - the bounds;
  - every finding and its resolution;
  - the disclosures (who read, who adjudicated, any deviation from this plan).
- **Site:** the result is linked from the Reproduction page and from the About page.
- **Deviations:** any deviation from this plan is listed as a deviation, never folded silently into the result.
