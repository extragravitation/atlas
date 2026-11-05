# Independent audit of X-COP v2: plan (frozen on merge)

**Frozen on merge**, under D-090 rule 3 and D-106 rule 4. The plan was written after X-COP v2 was published (#182, 2026-11-05) and before its seed exists. The hashes of this file and of `docs/audit/sample_xcop_v2.py` are in `data/frozen/audit-plan-xcop-v2.json`. Any change after freezing is a new version, with the reason logged.

Nothing in this plan changes the frozen general audit (`AUDIT_PLAN_v2.md`, D-082), whose X-COP stratum audits v1 (D-090 rule 2).

**Purpose.**
- (A) An independent re-derivation of a random sample of `aeg-d-xcop/v2` rows from the source.
- (B) A neutrality review of the X-COP v2 pages.

The method is that of `AUDIT_PLAN_v2.md`, applied to one stratum. Results are published whether they pass or fail, and are never re-scored.

## 1. When it runs

- After this plan is merged and the seed exists (section 2.3).
- **The audited state** is the main-branch commit at the start of the run, recorded in the result.

## 2. Part A: re-derivation

### 2.1 Frame

- **Rows:** every row of `data/packages/aeg-d-xcop/v2/tables/measurements.ecsv` whose `role` is empty or `default`.
- **The count when this plan was written:** 109 (A644 19, A1795 21, A2029 22, A2142 20, A2319 27), all `default`.
- **One stratum:** `aeg-d-xcop/v2`.

### 2.2 Sample size

- n = min(N, max(⌈0.05 N⌉, 10)), as `AUDIT_PLAN_v2.md` §2.2.
- For N = 109 this gives **10 rows**.

### 2.3 Seed

- **Primary:** the `outputValue` of the NIST Randomness Beacon (version 2.0, chain 2) pulse with the earliest `timeStamp` at least 24 hours after the merge commit that freezes this plan.
- **Fallback:** if the NIST beacon is unreachable for 72 hours after that time, the `randomness` of the drand mainnet ("default") chain round with the earliest time at least 24 hours after that merge commit.
- **Record:** the pulse (or round) identifier, its timestamp, the value and the URL it was read from go into the result before the sample is drawn.
- **Separate from the general audit.** This seed is not the general audit's seed (`AUDIT_PLAN_v2.md` §2.3), and neither is reused for the other.

### 2.4 Draw

- **Command:** `python docs/audit/sample_xcop_v2.py SEED_HEX` on the audited commit. It is standard library only and frozen with this plan.
- **Method:** the measurement identifiers are ranked by SHA-256(`seed` + `|` + `measurement_id`), ascending. The first n are the sample; the rest are the reserve, in rank order. This is `sample_v2.py`'s method.
- **Replacement:** only if a sampled identifier no longer exists in the audited commit. It is replaced by the next reserve identifier, and the replacement is reported.

### 2.5 Readers

- **Who:** two independent readers per row, fresh agents with no access to the Atlas's values.
- **Isolation:** each reader works in its own folder. Neither sees:
  - the other's work;
  - the Atlas measurement or observables tables;
  - the site;
  - `convert.py`;
  - the part B second reading (`v2/reading/` and the off-repo `values.csv`).
- **What each reader gets:**
  - the measurement identifier;
  - its `source_ref` locator (archive, file and row, for example `data_E22.tar.gz:A644/gbar_gobs_A644.fits:row 1`);
  - the archive URLs and SHA-256 from part A §1;
  - Eckert et al. 2022 (A&A 662, A123; arXiv 2205.01110);
  - the brief in section 2.6.
- **What each reader does:**
  - downloads the archive and checks its hash. A mismatch stops the reader and is reported;
  - reads the row as released;
  - converts it to the units below with their own code.

### 2.6 Reader brief (fixed text)

> You are auditing one measurement of a public dataset. Download the archive given, check its SHA-256 against the value given, and stop if it differs. Open the file named in the locator and read the row given: the radius, the observed acceleration GOBS, the baryonic acceleration GBAR, and their error columns, exactly as stored, with the column names and units from the file header. Report the radius in kpc and the accelerations in m s⁻², converting units only if the header gives a unit other than these, and say which conversion you used. Use the paper only to confirm what each column means; quote the line you rely on. If a column's meaning or unit is not stated, record "not stated" and do not guess. Return one CSV row per measurement with: measurement_id, file, row, each value with its unit and column name, and notes. Do not look for or use any other copy of this dataset.

### 2.7 Comparison

- **Script:** `docs/audit/compare_xcop_v2.py`, written and committed before any reading is opened. It compares each reader with the other and with the Atlas row.
- **Tolerances, fixed now:**
  - **Values read from the file** (radius, GOBS, GBAR and the error columns): equal to the stored value, at |relative difference| ≤ 1 × 10⁻¹².
  - **Accelerations as packaged** (`g_obs`, `g_bar`, `r_kpc` and the error columns): the same tolerance.
- **Why so tight:** part B fixed these values as the released numbers, with no Atlas arithmetic. Its items 2 and 4 require exact equality with the file and with the observables. The only allowed difference is the float rounding of a unit conversion, if one is needed.
- **Codes per row:** agree, reader disagreement, Atlas discrepancy, method incomplete, unreadable, as in `AUDIT_PLAN_v2.md` §2.7.

### 2.8 Adjudication

- **At source:** every non-"agree" row is settled by reading the archive file again, with the reading quoted in `docs/audit/adjudication_xcop_v2.md`.
- **Material discrepancy:** the Atlas differs from the file beyond the tolerance, on any compared value, for a reason other than reader error.
- **Labelled:** each adjudication says who made it. If Claude adjudicates, that is disclosed as not blind.

### 2.9 Provenance check (same rows)

For each sampled row, a reader checks three things. Any failure is a finding.
- **Archive and file:** the archive URL and SHA-256 in part A §1 and in `v2/sources.json` identify the file the row came from.
- **Citation:** the citation is Eckert et al. 2022.
- **The row's notes:** they carry what part B requires for its cluster:
  - D-092's note for A644;
  - the A2319 statements for A2319;
  - the stellar-projection note on every row.

### 2.10 Outcome (fixed before the draw)

- **Reported:**
  - the counts per code;
  - the number of material discrepancies;
  - the 95 % Clopper–Pearson upper bound on the material-discrepancy rate.
- **Pass:** zero material discrepancies and zero provenance failures.
- **Otherwise:**
  - the result stays as observed;
  - the cause is classified;
  - all 109 rows are checked for that cause, labelled exploratory;
  - each confirmed error is corrected by a new version and logged.

## 3. Part B: neutrality

### 3.1 Pages

- the X-COP v2 dataset page;
- two system pages, chosen with the seed of section 2.3 from the five clusters with rows (A644, A1795, A2029, A2142, A2319): rank 1 and 2 by SHA-256(`seed` + `|page|` + `system_id`);
- the A2319 page, if it is not already one of the two, because part B fixes neutrality-sensitive text there.

### 3.2 Term scan

- **Terms:** the list of `AUDIT_PLAN_v2.md` §3.2, run on these pages, with the same classes.
- **Script:** committed before it is run.

### 3.3 Reader review

Two fresh readers review the pages independently, with the six-question checklist of `AUDIT_PLAN_v2.md` §3.3.

### 3.4 Outcome

- **Logged:** every finding goes in `docs/audit/neutrality_xcop_v2.md`, with the page, the text and the reader.
- **Resolved:** each finding by a pull request, or by no change with the reason.
- **Pass:** zero findings left unresolved. The counts are reported either way.

## 4. Reporting

- **Result file:** `docs/audit/AUDIT_RESULT_XCOP_v2.md`, with:
  - the audited commit;
  - the seed record;
  - the sample;
  - the counts;
  - the bound;
  - every finding and its resolution;
  - the disclosures.
- **Linked from:** the Reproduction page and the X-COP v2 dataset page.
- **Deviations:** any deviation from this plan is listed as a deviation, never folded silently into the result.
