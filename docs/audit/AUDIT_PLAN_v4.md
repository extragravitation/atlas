# Independent audit: plan, version 4

**Frozen:** on merge of the pull request "Audit plan v4 frozen (D-125)", under D-125 (JvH: "Yes, as described (Recommended)", 2026-11-27). The hashes of this file, `docs/audit/sample_v4.py`, `docs/audit/choose_pages_v4.py` and `docs/audit/compare_v4.py` are in `data/frozen/audit-plan-v4.json`. This file is never edited in place; any change is a new version, with the reason logged.

**Frozen before:** the seed exists, and any audit v4 reading. No row of the v4 sample is known. What was known when this plan was set: the audit v3 result (Part A failed on provenance, 3 of 220 rows, 0 material discrepancies; Part B passed after fixes) and every correction made since (D-121 to D-125).

**Supersedes version 3** (`AUDIT_PLAN_v3.md`, D-116) for the next run on the v3 packages, as released in v0.3 and with the v0.4 text work merged. Version 3 and its result (`AUDIT_RESULT_v3.md`) are kept unchanged and are not re-scored.

**Purpose.** D-121 rule 4 and D-125 rule 2: measure, with a fresh random sample, the error rate after the audit v3 corrections. Part A re-derives a fresh sample of rows from the original sources, with a provenance check on the same rows. Part B is a neutrality audit of the built site. The result is published whether it passes or fails.

**What changed from version 3** (D-125 rule 2; nothing else changes):
- **Trigger and seed:** the trigger is the merge of this plan's freeze (§1). The seed follows 24 hours later (§2.3).
- **Key prefix:** `aeg-audit-v4`, so the sample is fresh (§2.4, §3.3).
- **Input comparison:** numeric inputs agree within a relative 10⁻⁶. Version 3's exact comparison flagged the same binary floats printed to different numbers of digits (§2.7).
- **Part B pages:** the six per-dataset methods pages are formally included (§3.3).
- **Packets:** built by one process at a time, and checked complete against their `sources.json` before any reader starts (§2.5). This is version 3's deviation 1 made a rule.
- **Corrections:** the v3 packages are now released, so any correction is a new package version (§2.10). Version 3's deviation 2 cannot recur.

## 1. When it runs

- **Trigger:** the merge to main of the pull request titled "Audit plan v4 frozen (D-125)". Its merge commit is the **trigger commit**. The v0.4 text work (D-125 item 1) is merged before it.
- **Audited state:** the main-branch commit at the start of the run, which is recorded in the result. If it differs from the trigger commit, the differences are listed. No change to methods text or package data is merged between the trigger commit and the end of the readings.
- **Frame:** fixed by §2.1 now, so later work cannot choose which rows are audited.

## 2. Part A: re-derivation and provenance

### 2.1 Frame

- **Rows:** every measurement row in the six v3 packages whose `role` is empty or `default`, plotted or not. Alternative rows are excluded.
- **Strata:** one per package.
- **Counts:** as at main commit `3eea7b4` (2026-11-27), unchanged since version 3. These are counts of rows, read from the `role` column; no value was looked at.

| Stratum | Rows in frame | Sample |
|---|---:|---:|
| `aeg-d-sparc/v3` | 3 391 | 170 |
| `aeg-d-xcop/v3` | 109 | 10 |
| `aeg-d-kids1000-rar/v3` | 30 | 10 |
| `aeg-d-strong-lensing/v3` | 94 | 10 |
| `aeg-d-gc-baumgardt/v3` | 62 | 10 |
| `aeg-d-dwarfs/v3` | 64 | 10 |
| **Total** | 3 750 | **220** |

If a count at the audited commit differs from this table, the sampler uses the audited commit's frame, and the difference is reported as a deviation.

### 2.2 Sample size

- **Per stratum:** n = min(N, max(⌈0.05 N⌉, 10)), as in version 2.
- **Total:** 220 rows.

### 2.3 Seed

- **Primary source:** the `outputValue` of the NIST Randomness Beacon (version 2.0, chain 2) pulse with the earliest `timeStamp` at least 24 hours after the trigger commit's timestamp.
- **Fallback:** if the NIST beacon is unreachable for 72 hours after that time, the `randomness` of the drand mainnet ("default") chain round with the earliest time at least 24 hours after the trigger commit.
- **Record:** the pulse (or round) identifier, its timestamp, the value, the URL read, and who read it go into the result before the sample is drawn.
- **Why after the trigger:** the methods text cannot be written with the sample known.

### 2.4 Draw

- **Command:** `python docs/audit/sample_v4.py SEED_HEX` on the audited commit. It is standard library only and frozen with this plan.
- **Ranking:** within each stratum, by SHA-256(`aeg-audit-v4|` + seed + `|` + `measurement_id`), ascending. The first n are the sample; the rest are the reserve, in rank order.
- **Replacement:** only if a sampled identifier does not exist at the audited commit. The next reserve identifier takes its place, and the replacement is reported.

### 2.5 Readers and packets

- **Who:** two independent readers per row, A and B. Both are fresh agents with no access to the Atlas's values.
- **Isolation:** each reader works in its own folder. Neither sees the other's work, the measurement or observables tables, the site, this repository's converters, or the decision log.
- **Building:** by one process at a time. Before any reader starts, every packet is checked to hold every file its `sources.json` names, each matching its recorded hash. A packet that fails is rebuilt before any reader sees it.
- **Packet contents,** built by a script committed before the first packet is opened:
  - the measurement identifier and the system's name as the source gives it;
  - the dataset's methods text: the methods page section for the dataset and the package's method files as of the audited commit. Constants and assumption defaults are kept; measured or derived values of individual rows are removed;
  - the row's `source_ref` text, with any quoted input value redacted, and the rules of `locators.json` it matches;
  - the `sources.json` entries those rules name;
  - every source file those entries name, each checked against its recorded SHA-256 before it goes in the packet;
  - the brief in §2.6.
- **Files that cannot be supplied:** a file is either one no host reachable from the workspace serves, or one whose SHA-256 does not match the record. It may be supplied by JvH, who downloads it in his browser, and then the hash is checked. Any file still not supplied makes its rows **not verified** (§2.10). A file is never replaced by a different version or a mirror whose hash differs.

### 2.6 Reader brief (fixed text)

> You are auditing one measurement of a public dataset. From the source files given, read the inputs that the written method needs, exactly as printed, with their units and where you found them (file, and page, table, row, column or line). Then compute the observed acceleration g_obs and the baryonic acceleration g_bar, both in m s⁻², with your own code, following only the written method. Use only the constants stated in the method. If the method does not say how to do a step, do not guess: record "method incomplete" and what was missing. If you cannot read a value, record "unreadable" and why. For every input, also say whether you found it at the place the locator gives; if not, say where you found it. Return values.csv (measurement_id, g_obs, g_bar, notes) and inputs.csv (measurement_id, input, value, unit, file, place, at_locator yes/no). Do not look for or use any other copy of this dataset.

### 2.7 Comparison

- **Script:** `docs/audit/compare_v4.py`, frozen with this plan. It compares each reader with the other and with the Atlas row.
- **Tolerances:**
  - **inputs:** numbers agree within a relative 10⁻⁶ (equal at the source's printed precision, and no stricter, for binary floats printed to different digits); text agrees as stripped, case-insensitive strings;
  - **accelerations:** |Δ log₁₀ g| ≤ 0.005 dex for g_obs and for g_bar.
- **Codes per row:**
  - **agree:** both readers agree with each other and with the Atlas;
  - **reader disagreement:** the readers differ from each other;
  - **Atlas discrepancy:** the readers agree with each other but not with the Atlas;
  - **method incomplete:** either reader records it;
  - **unreadable:** either reader records it.

### 2.8 Adjudication

- **Reader disagreements:** a third fresh reader, C, re-derives the row with the same packet and brief and does not see A or B. The row then takes the value two of the three readers agree on. If no two agree, Claude adjudicates at source.
- **Atlas discrepancies and unreadable rows:** Claude reads the source again and quotes the reading in `docs/audit/run_v4/adjudication.csv`.
- **Material discrepancy:** the Atlas is wrong on an input, or by more than 0.005 dex on g_obs or g_bar, for a reason other than reader error.
- **Method incomplete** stays a finding against the methods text even when the Atlas value is right. It is never adjudicated away. If Claude judges that the missing step is stated in the packet, the row stays method incomplete and the judgement is recorded beside it.
- **Blocking or not.** Each method-incomplete row is classed mechanically by `compare_v4.py`, not by judgement:
  - **blocking:** at least one reader recorded the gap and either gave no value or a value outside tolerance of the Atlas;
  - **non-blocking:** the gap was recorded, but every reader who recorded it still computed g_obs and g_bar within tolerance of the Atlas.
- **Labelling:** every adjudication says who made it. Claude's are disclosed as not blind.

### 2.9 Provenance check (same rows)

**Mechanical part,** by a script committed before it is run, per sampled row:
1. the row's `source_ref` matches exactly one rule of `locators.json`;
2. every source the rule names has `id`, `kind`, `citation`, `identifier` and `licence` with `status`, `checked_where` and `checked_on`;
3. each such source has a recorded SHA-256, and the file supplied in the packet matches it;
4. every place the rule gives (table, page, column, row, line, section, figure, HDU, member) exists in that file;
5. the units in the row agree with the source's units, or with the conversion the methods text states.

**Human part:** both readers' `at_locator` answers. An input found by both readers somewhere other than the locator's place fails check 6, unless the rule's `correction` already gives that place.

**Failures and labels:**
- **Failure:** any of checks 1 to 6 failing is a provenance failure for the row.
- **Null hash:** a source with a null `sha256` is a provenance failure (D-114 rule 3).
- **Hashed after reading:** a source whose hash was recorded after the reading was made is reported as its own count. It passes checks 3 and 6 only if both readers find the input in the hashed file. This is the case of van de Rydt et al. 1991, `aeg-d-dwarfs/v3` S111.

### 2.10 Outcome (fixed before the draw)

- **Reported, per stratum and overall:**
  - the counts per code, and per provenance check;
  - the number of material discrepancies, provenance failures, blocking and non-blocking method gaps, and rows not verified;
  - for each of the three decision counts below, the 95 % Clopper–Pearson upper bound on its rate over the whole sample.
- **Decision counts:** material discrepancies, provenance failures and blocking method gaps. Each is counted in rows; a row is counted once per count.
- **Verdict for Part A:**
  - **pass:** every decision count has a 95 % upper bound of at most 2.5 %, and every sampled row is verified. With 220 rows that allows at most one row per count (0 rows gives 1.35 %, 1 row 2.14 %, 2 rows 2.83 %);
  - **fail:** any decision count's upper bound is above 2.5 %;
  - **incomplete:** no count fails, but some rows are not verified (§2.5). The verdict stays incomplete until their files are supplied and read. Unverified rows are never replaced from the reserve.
- **The strict verdict is reported too:** the result also states whether Part A would pass under version 2's rule, extended to method gaps: zero rows in each count, blocking or not, and no row unverified.
- **Whatever the verdict:**
  - the result stays as observed and is not re-scored;
  - every error found is corrected by a new package version (the v3 packages are released) and entered in the public corrections log, whether or not it is within the threshold;
  - the cause of each finding is classified, and the whole package is checked for that cause, labelled exploratory;
  - every method gap, blocking or not, is fixed in the methods text and reported.
- **Why a threshold, and what was known when it was set:** as in version 3 (§2.10 there). The threshold and decision counts are unchanged, set before version 3's result was known; version 4 keeps them so the two results are comparable.

## 3. Part B: neutrality

### 3.1 Scope

All text a visitor can read on the built site at the audited commit:
- every page in the build;
- chart labels and legends, tooltips and slider labels;
- download README files;
- the dataset and system descriptions.

### 3.2 Term scan

- **Script:** `docs/audit/term_scan.py`, the version 2 script unchanged. Its hash is recorded in the result.
- **Terms:** the version 2 list (`AUDIT_PLAN_v2.md` §3.2).
- **Classes:** each occurrence is classed allowed or finding, by the version 2 rules.

### 3.3 Reader review

- **Readers:** two fresh readers, working independently.
- **Pages:**
  - the front page;
  - Map, About, Methods, Known issues, For data providers, Coverage, Reproduction and Tests;
  - every dataset page of a current version;
  - the six per-dataset methods pages (`methods/<dataset>/`);
  - two system pages per current dataset, chosen with the seed of §2.3. They are ranks 1 and 2 by SHA-256(`aeg-audit-v4|page|` + seed + `|` + `system_id`), by `docs/audit/choose_pages_v4.py`.
- **Checklist:** the six questions of version 2 (`AUDIT_PLAN_v2.md` §3.3), unchanged.

### 3.4 Outcome

- **Log:** every finding goes in `docs/audit/run_v4/partB/neutrality_v4.md`, with the page, the text, the reader and the checklist question it falls under (or "term scan").
- **Resolution:** each finding is resolved by a change or by no change, with the reason.
- **Deciding findings:** term-scan findings, and reader findings under checklist questions 1 to 3:
  1. the text assumes a cause;
  2. it favours an account;
  3. a label carries the result.

  Findings under questions 4 to 6 (binning, the two layers, the route to a source) are reported and resolved, but do not decide the verdict. Where readers disagree on the question a finding falls under, it is counted under the lower-numbered question.
- **Earlier rulings:** a finding on wording that an earlier ruling kept (for example D-122 B3 and B13), if re-found, is logged and resolved again with its reason. It is not dropped.
- **Pass:** zero deciding findings left unresolved. All counts are reported either way.
- **Strict verdict:** the result also states whether Part B would pass under version 2's rule, which is zero findings of any kind left unresolved.

## 4. Reporting

- **Result file:** `docs/audit/AUDIT_RESULT_v4.md`, with:
  - the audited commit and the trigger commit;
  - the seed record and the sample;
  - the counts and the bounds;
  - every finding and its resolution;
  - the disclosures: who read, who adjudicated, and every deviation from this plan.
- **Site:** the result is linked from the front page, the Reproduction page and the About page, next to the earlier results.
- **Deviations:** any deviation from this plan is listed as a deviation, never folded silently into the result.
