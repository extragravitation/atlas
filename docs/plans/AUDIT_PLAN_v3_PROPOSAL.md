# Proposal: audit plan version 3 (D-116, for ruling)

**Proposed by** Claude, 2026-11-24. **Implements** D-113 item 3. **Draft plan:** `docs/audit/AUDIT_PLAN_v3.md`, with sampler `docs/audit/sample_v3.py`. On a ruling, both are hashed into `data/frozen/audit-plan-v3.json` and merged before anything else in the audit happens.

**Data seen:** the row counts per package (from the `role` column), and the version 2 plan and result. No v3 value was looked at.

The plan keeps version 2's method: two blind readers, a beacon seed, a 5 % sample with at least 10 rows per stratum, 0.005 dex tolerances, and the neutrality term scan and checklist. Six choices change it. Each is set out below with its options and a recommendation.

## Q1. Which rows

| Option | For | Against |
|---|---|---|
| **A. A fresh random sample of the v3 frame (recommended)** | Tests the packages as they now stand. A pass then means something about rows nobody chose | Doesn't by itself re-check the 254 rows that failed |
| B. Re-check version 2's 254 rows | Shows directly that the findings were fixed | Those rows are known, so passing them says little about the rest. The validator already checks every row's records mechanically, on every CI run |

**Recommendation: A.** The CI validator already covers the 250 rows that failed provenance (P1 to P4). They are rows in the whole package, and the validator checks those mechanically.

## Q2. When the seed is drawn

| Option | For | Against |
|---|---|---|
| **A. 24 h after the merge that completes the methods text (recommended)** | The methods text cannot be written to fit the sample | The audit starts a day later |
| B. 24 h after this plan is frozen | Starts sooner | The sample would be known while the methods text is still being written, and anyone could make sure those 220 rows were well covered |

**Recommendation: A.**

## Q3. What passes

Version 2 passed on zero material discrepancies and zero provenance failures. Method-incomplete rows were reported but did not fail the audit.

**Recommendation:** Part A passes only if four counts are all zero: material discrepancies, method-incomplete rows, provenance failures, and rows not verified.
- **Method incomplete is added** because D-113 item 2 promises methods text for every row shown. An audit that ignored it would not test that promise.
- **"Not verified" is added** because a row whose source file the readers could not get has not been audited. It should not count as passed.

## Q4. A source hashed after it was read

The only case is van de Rydt et al. 1991 (dwarfs S111). It was read in ADS scans in a browser, and ADS's PDF of those scans was hashed on 2026-11-24, after the reading.

| Option | Effect |
|---|---|
| **A. Passes if both readers find the value in the hashed file; reported as its own count (recommended)** | The file is in the record now, and the check is whether it holds the value. The late hash is disclosed, not hidden |
| B. Always a provenance failure | The audit cannot pass if Phoenix is sampled, whatever the file shows |

**Recommendation: A.** A null hash stays a failure, as D-114 rule 3 says.

## Q5. Who settles reader disagreements

| Option | For | Against |
|---|---|---|
| **A. A third fresh reader; Claude only if all three differ (recommended)** | Blind | More agent runs |
| B. Claude, as in version 2 | Quicker | Not blind. Version 2's own disclosures name this as a weakness |

**Recommendation: A.** Claude still adjudicates Atlas discrepancies at source, quoting the source, and is disclosed as not blind.

## Q6. Source files the workspace cannot reach

The UQ, McMaster, SPARC and VizieR hosts refuse connections from the workspace. CI can fetch from them, but its artifacts cannot be downloaded here. Version 2 used copies that were still in the workspace; those copies are gone.

**Recommendation:**
- Readers get each file only after it has been checked against its recorded hash.
- Files the workspace cannot get are downloaded by JvH in his browser and hash-checked.
- A file that still cannot be supplied makes its rows "not verified", which fails Part A under Q3.
- No mirror or other version is substituted.

**What this asks of JvH:** downloading the sampled rows' files once the sample is drawn. That is probably the SPARC mass-model and galaxy files (two files), a handful of globular-cluster pages, and at most the Harris file and the VizieR exports. I'll list the exact URLs after the draw.

## Part B

The term list, checklist and pass rule are unchanged. The page list adds the new front page, Map, Reproduction and Tests.

One risk to name: D-113 rule 2 deferred some version 2 neutrality items that need new readings. If a reader finds one of them again, it stays an open finding, and Part B fails until it is resolved. The plan says so in advance, rather than leaving it to a judgement after the result.

## Ruling requested

Q1 to Q6 as recommended, or as amended. After the ruling:
- the plan is frozen, logged as D-116 and merged;
- then the methods text (D-113 item 2) is written;
- its merge is the trigger for the seed.
