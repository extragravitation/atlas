# X-COP v2 audit result (plan: `AUDIT_PLAN_XCOP_v2.md`, D-090 rule 3, D-106 rule 4)

**Status: in progress.** This file records the seed and the sample before any reading starts. The counts and findings are added when the run is complete, whether it passes or fails.

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

## Counts, findings and disclosures

To be added when the run is complete.
