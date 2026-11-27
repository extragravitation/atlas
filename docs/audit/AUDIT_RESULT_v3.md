# Audit v3: result (plan v3, D-116)

**Part A (re-derivation and provenance): fail.** All 220 sampled rows reproduced from the original sources: 0 material discrepancies and 0 method gaps. 3 rows had provenance failures. The 95 % upper bound on that rate is 3.49 %, above the 2.5 % threshold. **Strict verdict: not pass.**

**Part B (neutrality): pass.** 13 deciding findings were found and all are resolved: 11 by a change, 2 by no change with a stated reason (D-122). **Strict verdict (version 2's rule, zero findings of any kind left unresolved): not pass.** Findings under checklist questions 4 to 6 remain open; three of them, which were factual errors, are fixed.

The result is reported as observed and has not been re-scored. Every number below is read from the files in `docs/audit/run_v3/`.

## 1. Commits, seed and sample

- **Trigger commit:** `bed8da23e5fa5e3200639861de6ba7754e35c34f`, "Methods text complete (D-113 item 2) (#231)", 2026-11-25T15:04:20Z.
- **Audited commit:** `7f112d491838f2b574ca4db3b6c449ecc41dd2f0` (main at the start of the run). Since the trigger commit, no file under `docs/methods/` or `data/` had changed, so the freeze held.
- **Seed:** NIST Randomness Beacon v2.0, chain 2, pulse **2044806**, `timeStamp` 2026-11-26T15:05:00.000Z, read by Claude at 15:13Z. The `outputValue` begins `96DE7C5DBE3C933B`; the full value, the raw pulse and the pulse before it are in `run_v3/TRIGGER.md` and `run_v3/seed_pulse*.json`.
  - Pulse 2044805 is stamped 15:04:00Z, so 2044806 is the earliest pulse at or after 15:04:20Z.
  - The hash chain checks pass: the precommitment and the link to the previous output. The pulse signature was not verified.
  - The seed record was merged (#239) before anything was drawn.
- **Sample:** `sample_v3.py` was run on the audited commit (`run_v3/sample.csv`, SHA-256 `d1bd9ec1…`). The frame is 3,750 rows, the same as plan §2.1, and 220 were drawn: SPARC 170, and X-COP, KiDS, lenses, GC and dwarfs 10 each. No replacement from the reserve was needed.
- **Part B pages:** `choose_pages_v3.py` (`run_v3/pages.csv`) chose two system pages per dataset; KiDS has none.

## 2. Part A

### 2.1 Readings and comparison

- **Readers:** one fresh agent per dataset on each side, A and B, so 12 in all. A third fresh reader C, given the same packet and brief, read each package that had a disagreement.
- **Comparison** (`compare_v3.py`, committed before any reading was opened; `run_v3/comparison.csv`):

| Stratum | agree | agree (2 of 3) | disagreement unresolved | Atlas discrepancy | method incomplete | unreadable |
|---|---:|---:|---:|---:|---:|---:|
| SPARC | 170 | 0 | 0 | 0 | 0 | 0 |
| X-COP | 0 | 10 | 0 | 0 | 0 | 0 |
| KiDS-1000 | 10 | 0 | 0 | 0 | 0 | 0 |
| Strong lenses | 9 | 1 | 0 | 0 | 0 | 0 |
| Globular clusters | 10 | 0 | 0 | 0 | 0 | 0 |
| Dwarfs | 10 | 0 | 0 | 0 | 0 | 0 |
| **All** | **209** | **11** | 0 | 0 | 0 | 0 |

- **The 10 X-COP disagreements:** readers A and B read the same stored float32 FITS values but printed them to 9 and 8 significant figures, and the frozen tool compares input values exactly. Their g_obs and g_bar were identical. This is a property of the tool, not of the Atlas. It was not changed or re-scored, and reader C settled every row.
- **The lens disagreement:** a quoted gas-assumption text, also settled by reader C.

### 2.2 Provenance (`provenance_check_v3.py`; `run_v3/provenance.csv`)

| Check | pass | review | n/a | fail |
|---|---:|---:|---:|---:|
| 1 locator | 220 | | | 0 |
| 2 record | 220 | | | 0 |
| 3 hash | 220 | | | 0 |
| 4 place | 180 | | 40 | 0 |
| 5 units | 220 | | | 0 |
| 6 found at the place given | 37 | 173 | 10 | — |

- **Late hash:** no sampled row used source S111 (dwarfs), so the late-hash rule was not exercised.
- **Adjudication** at source by Claude, not blind (`run_v3/adjudication.csv`) covered 173 rows:
  - **170 SPARC rows: provenance confirmed.** Both readers marked Inc and e_Inc "not at the locator", because the row's locator does not name them. The methods page gives their place: the galaxy's row of `SPARC_Lelli2016c.mrt`. All 340 reader values were checked by script against that file, with 0 mismatches.
  - **3 dwarf rows: provenance failure.**
    - Andromeda XVIII and Leo T: the ellipticity is recorded at Higgs et al. 2021 p. 16 Table 3, which prints no ellipticity. Both readers found it in Table 2, column e.
    - Antlia II: M_V is routed to Vivas et al. 2022, which prints none. Both readers found it in Ji et al. 2021 p. 7 Table 1.
    - All three values were reproduced by both readers.

### 2.3 Counts, bounds and verdict (`compare_v3.py verdict`)

| Decision count | Rows | One-sided 95 % upper bound | Threshold |
|---|---:|---:|---:|
| Material discrepancies | 0 | 1.35 % | 2.5 % |
| Provenance failures | **3** | **3.49 %** | 2.5 % |
| Blocking method gaps | 0 | 1.35 % | 2.5 % |

There were 0 non-blocking method gaps and 0 rows not verified. **Verdict: fail. Strict verdict: not pass.**

### 2.4 Causes, the whole-package check, and corrections

The two causes were checked across all 64 dwarf systems. This check is exploratory: Claude did it after the audit, not under the frozen plan.
- **Ellipticity placed in Higgs Table 3:** 3 systems (Andromeda XVIII, Andromeda XXVIII, Leo T).
- **M_V routed to the paper of the package distance, when another paper prints it:** 3 systems (Antlia II → Ji 2021; Andromeda XXVIII → Slater 2015; Eridanus IV → Casey 2025, where the distance paper prints a different M_V).

That is 6 corrections across 5 systems, since Andromeda XXVIII has both errors (an earlier draft said "six systems"). The values of all five systems were checked against the printed numbers. They were corrected by locator corrections in dwarfs v3 (D-121, issue #243, #244); no value changed.

## 3. Part B

### 3.1 Term scan

`term_scan.py` (v2, unchanged, SHA-256 `32ec3774…`) on the build of the audited commit found 247 matches. A fresh classifier marked 234 allowed and 13 findings: 6 were "halo" in Atlas wording on the KiDS pages, and 7 were false matches (the kind code "A0", and "explains" as an ordinary verb).

### 3.2 Reader review

Two fresh readers each read 32 pages: those of plan §3.3, plus the six per-dataset methods pages. Reader 1 logged 34 findings and reader 2 logged 36. Merged with the term scan, they give 13 deciding findings (questions 1 to 3 and the scan). `run_v3/partB/neutrality_v3.md` lists them, and D-122 records how each was resolved:

| # | Finding | Resolution |
|---|---|---|
| B1 | "halo" in KiDS wording | Change (#247): v3 column descriptions reworded. No change, with reason, for the released v2 pages and the frozen KiDS reproduction record. |
| B2 | "extra pull" for a ratio that can be ≤ 1 | Change (#246): "pull ratio" |
| B3 | Site name | No change, with reason (D-122) |
| B4 | Reading guidance only for points above the line | Change (#246) |
| B5 | Mass framing in the plain layer | Change (#246): a change of units, M_g,obs |
| B6 | "Pull budget", "Detected share" | Change (#246) |
| B7 | Reviews all from one account; a heading presuming a relation | Change (#246): two reviews added, read at source; the heading is neutral |
| B8 | "does not yet explain" | Change (#246) |
| B9 | KiDS title "…radial acceleration relation…" | Change (#247) |
| B10 | A7 used for unsettled kinds | Change (#249): "kind not settled" on the site; the package codes are unchanged |
| B11 | "anomalous acceleration" | Change (#246): a note under the frozen taxonomy, which is not edited |
| B12 | "Flat ΛCDM" | Change (#246) |
| B13 | Dwarfs taken off the map on their sources' statements | No change, with reason (D-122) |

The three factual errors found under questions 4 to 6 are also fixed:
- the X-COP "non-parametric" claim (#246, #247);
- the X-COP v3 plain status line (#246);
- the σ citations on the dwarf methods page, where 33 of 64 rows named another paper's arXiv identifier and place (#248).

The other question 4 to 6 findings are open and listed in the readers' `findings.csv`. Most are mismatches between the plain and expert layers and missing source routes.

**Verdict: pass** (no deciding finding left unresolved). **Strict verdict: not pass.**

## 4. Disclosures and deviations

- **Readers and adjudicator.** Every reader was a fresh AI agent (Claude), instructed to use only its own folder. Claude built the packets, ran the tools and adjudicated, not blind. JvH ruled on the corrections (D-121, D-122) and authorised Claude to merge the audit's record PRs (D-120).
- **Deviation 1, a defective packet (Claude's operational error).** A stray background build overwrote the B packet for the globular clusters without its two VizieR tables. Reader B reported all 10 rows unreadable. This was found before any comparison. The packet was rebuilt to match packet A byte for byte and read by a fresh reader B. The defective reading is kept in `run_v3/readings_void/` and was not used (`run_v3/DEVIATIONS.md`).
- **Deviation 2, corrections in the unreleased v3 rather than in a new version.** Plan §2.10 says errors are corrected "by a new version". The dwarfs, X-COP and KiDS v3 packages were not yet released, and JvH ruled to correct them in place (D-121, D-122), as D-117 and D-119 did. They are listed as known issue #243 and in CHANGELOG.
- **Deviation 3, Part B scope.** The readers also read the six per-dataset methods pages, which plan §3.3 does not list.
- **Disclosed, not deviations.**
  - S5 and S7 (McLaughlin & van der Marel 2005, VizieR) were supplied from copies downloaded from the same host the day before, because the host returned 504. Each was checked against its recorded content hash, as plan §2.5 allows.
  - The Part B briefs are the version 2 texts with only the paths changed.
  - During the corrections Claude merged one record PR (#242) while its site build was failing, and first edited a hash-frozen document. The repository's check caught the edit and it was reverted (#246). Neither affected the audit's data.

## 5. Reader notes for follow-up (not counted)

The readers' `gaps.md` files record wording points that changed no value. Examples:
- the KiDS method calls the source column g_bar, where its README says "mean";
- two parsing conventions in the globular-cluster method are unstated;
- the SPARC row locators do not name Inc and e_Inc.

These are inputs to the next revision of the methods text, before audit v4 (D-121).

## 6. Independent check of the corrections (exploratory, after the result; D-123)

The corrections in §2.4 were made by Claude. Before release, two fresh blind readers re-read the five corrected dwarf systems from packets built on the corrected locators (main after #244). They used the same frozen brief and tools: Andromeda XVIII, Andromeda XXVIII, Antlia II, Eridanus IV and Leo T (m000015, m000023, m000024, m000037, m000047).
- **Comparison:** 5 of 5 rows agree with the Atlas; 0 method gaps.
- **Provenance:** checks 1 to 6 pass on all 5 rows. Both readers found every input at the place its corrected locator gives, so no row needed adjudication.

This check does not change or re-score the audit; Part A's verdict stays fail. It shows only that the corrections hold. The records are in `run_v3/verify_corrections/`.
