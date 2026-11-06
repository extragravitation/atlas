# X-COP v2 audit result (plan: `AUDIT_PLAN_XCOP_v2.md`, D-090 rule 3, D-106 rule 4)

**Status: run complete. Part A passes; part B has unresolved findings.**
- **Part A, values:** 10 of 10 rows agree. Zero material discrepancies; the 95 % upper bound on the rate is 30.8 % (n = 10).
- **Part A, provenance:** zero failures.
- **Part B, neutrality:** no finding that a page assumes a cause, favours an account, or carries a result in a label. There are must-fix findings on layer consistency and on routes to sources (`neutrality_xcop_v2.md`). They are unresolved at the time of writing, so part B does not pass yet.

## Plan

- **Frozen files:** `AUDIT_PLAN_XCOP_v2.md`, `sample_xcop_v2.py` and `compare_xcop_v2.py`. Their SHA-256 hashes match `data/frozen/audit-plan-xcop-v2.json` (`d7d23e91…`, `da3fdab0…`, `6ae0aaf2…`).
- **Frozen by** the merge of #183, commit `d4344b2`, at 2026-11-05T16:40:21Z.

## Audited commit

`81a026bac99cfc4546d1a8a6f107e71c4915d86d`, main at the start of the run, 2026-11-06.

## Seed record

- **Source:** NIST Randomness Beacon 2.0, chain 2, the primary source.
- **Rule:** the earliest pulse with `timeStamp` at least 24 hours after the freezing merge, so at or after 2026-11-06T16:40:21Z.
- **URL read:** `https://beacon.nist.gov/beacon/2.0/pulse/time/next/1793983221000` (1793983221000 ms = 2026-11-06T16:40:21Z).
- **Read by:** JvH in his browser, 2026-11-06 at 16:52 UTC, pasted into the session.
- **Pulse:** 2016139 (`https://beacon.nist.gov/beacon/2.0/chain/2/pulse/2016139`).
- **timeStamp:** 2026-11-06T16:41:00.000Z. The period is 60 000 ms, so the previous pulse (2016138, at 16:40:00) is before the cut-off, and this is the earliest pulse at or after it.
- **outputValue (the seed):** `EEE93A1C151CEE59A996F4080B7986E2F3B563A5D3862B295D0D44E73DA731E4CE7C1E3E9C4252C35D497EACAC9FB291D4BA1E8F61AB2BFF1A05BBC296271F4F`
- **Full pulse:** `run_xcop_v2/seed_pulse.json`.
- **Verified:** the chain and the timestamp against the rule.
- **Not verified:** the signature (see NIST's 2026-10-23 certificate note), the outputValue hash, and the link to the previous pulse. This is the same as the general audit.

## Sample

- **Draw:** `python docs/audit/sample_xcop_v2.py <seed>` on the audited commit. The full ranking is in `run_xcop_v2/sample.csv`.
- **n = 10 of 109.** No replacements.
- **The 10 rows:** m000012 (A644), m000109, m000097, m000095 and m000099 (A2319), m000048, m000054 and m000062 (A2029), and m000020 and m000032 (A1795).

**Disclosure.** The sample was computed in the session immediately after the seed was received (2026-11-06 ~16:53 UTC), and before this record was committed. The draw is fully determined by the seed, so no choice entered it. The plan's order (record, then draw) was not followed to the letter. The same was true of the general audit.

## Part A: re-derivation (§2.5–2.8)

**Readers.** Two fresh agents worked under the fixed brief (`run_xcop_v2/partA/BRIEF.md`). Each downloaded `data_E22.tar.gz` itself, and both hashes matched. Their returns and code are in `run_xcop_v2/partA/a/` and `run_xcop_v2/partA/b/`.

**Comparison.** The frozen `compare_xcop_v2.py` (output: `run_xcop_v2/comparison.txt`) found agree 10, reader disagreement 0, Atlas discrepancy 0, method incomplete 0, unreadable 0. All seven fields of every row agree within 1 × 10⁻¹² relative: radius, g_obs and g_bar, and their error columns.

**Adjudication.** None was needed. The Clopper–Pearson 95 % upper bound with 0 of 10 is 30.8 %.

**What both readers recorded as not stated by the source** (findings about the source's documentation, not Atlas errors):
- the confidence level of `GBAR_ERR`, `GOBS_ERR_LO` and `GOBS_ERR_HI`. Both readers inferred from the values that these are ± sizes, not bounds;
- which of the paper's two g_obs reconstructions (non-parametric or Einasto) `GOBS` holds;
- whether the radius is 3D or projected.

These overlap with the open questions to the authors.

**Row numbering.** The locators count rows from 1. The data settle it: A2319's file has 27 rows, and a sampled locator names row 27.

## Part A: provenance (§2.9)

One fresh agent checked the archive URL and hash (it downloaded the archive and matched all 20 member hashes), the citation, and the required notes. Result: 45 pass, 15 n/a, 0 fail (`run_xcop_v2/provenance/provenance.csv`).

The agent asked whether Paper II l. 161 and l. 227, which don't name A2319, belong on A2319's rows. Claude checked the frozen `v2/reading/hse_statements.csv`: rows 28 and 30 list both as A2319 statements by reference, with `in_a2319_notes = yes`. They belong.

The agent also noted that `REPRODUCTION.md` §1 still says "21 rows" per file. That is the erratum D-091 already records.

## Part B: neutrality (§3)

**Pages:** the X-COP v2 dataset page; the system pages chosen with the seed, A644 (aeg-s-000177) and A1795 (aeg-s-000179); and A2319 (aeg-s-000183), as the plan requires.

**Term scan:** 98 occurrences, all allowed: 87 name the source's fitting functions as its method, and 11 are quotes or the source file name `einasto.tex`. The scan's term list does not match "gNFW", so 4 occurrences were not listed; read in context, they are also the source's method.

**Page readers:** reader 1 found 41 (10 must fix) and reader 2 found 24 (6 must fix). Repeated findings are counted once per page. Neither reader found anything under checklist items 1–4. All findings are about plain-layer consistency (item 5) and routes to sources (item 6). They are listed and resolved in `neutrality_xcop_v2.md`.

## Disclosures

- All readers and checkers were fresh Claude agents, isolated by instruction.
- No adjudication was needed in part A.
- Claude settled the provenance question at source, not blind.
- The draw happened before the seed record was committed (see Sample).
