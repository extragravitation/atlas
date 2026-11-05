# Audit result (plan v2, D-082)

**Status: in progress.** This file records the seed and the sample, as plan §2.3 requires, before any reading starts. The counts, bounds and findings are added when the run is complete, whether the audit passes or fails.

## Plan

- Plan: `docs/audit/AUDIT_PLAN_v2.md`, sha256 `910b765232ddf9855c4ad34021252d8259b36749b55a8c402ba7d51686931338`.
- Sampler: `docs/audit/sample_v2.py`, sha256 `89957518d44de783e349252821aefe2e6f15f8c1fbe00825bb4952157a85a56b`.
- Both match the hashes frozen in `data/frozen/audit-plan-v2.json`.
- Frozen by merge commit `1fbd47b` (2026-11-02T00:46:17Z).

## Audited commit

`e382edbf110c50b0047a9866b22c83c3a6f49d7e` (main, 2026-11-05). The frame is the six `/v1` packages named in the plan. Under D-083 and D-090 the v1 rows stay published, and the result describes them and the pipeline that made them.

## Seed record

- **Source:** NIST Randomness Beacon 2.0, the primary source.
- **Rule:** the earliest pulse with `timeStamp` ≥ 2026-11-03T00:46:17Z.
- **URL read:** `https://beacon.nist.gov/beacon/2.0/pulse/time/next/1793666777000` (1793666777000 ms = 2026-11-03T00:46:17Z).
- **Read by:** JvH, in his browser, on 2026-11-05 at 18:43 UTC. He pasted the JSON into the session; the workspace cannot reach beacon.nist.gov.
- **Pulse:** chain 2, pulse 2010865 (`https://beacon.nist.gov/beacon/2.0/chain/2/pulse/2010865`).
- **timeStamp:** 2026-11-03T00:47:00.000Z. The period is 60 000 ms, so the previous pulse (2010864) is at 00:46:00, before the cut-off, and this is the earliest pulse at or after it.
- **outputValue (the seed):** `CFBC67BA4CE1EFD7D1631F0A340EE95AF887984A80BB8B86594E5C46FD63D68E3494A669E16729BD655B94EB734D3668CC3A5A3030F44A4BEAEA911BEDDAA060`
- **Full pulse:** `docs/audit/run_v2/seed_pulse.json`.

### What was and was not verified

- **Verified:** the chain (2), and the timestamp against the rule.
- **Not verified:** the link to the previous pulse (this needs pulse 2010864, which was not read), the signature, and the outputValue hash. NIST's Beacon 2.0 page notes (2026-10-23) that pulses issued since 2026-09-03 refer to an incorrect certificate, so signature checks need a different certificate, which NIST has not yet published. Anyone can re-read pulse 2010865 at the URL above and compare.
- **An earlier, malformed URL was tried first.** Before the read above, Claude gave a URL with an undocumented `/chain/2/` segment, which redirected to NIST's project page. This was a URL error, not a beacon outage. The fallback (drand) was not used.

## Sample

- **Draw:** `python docs/audit/sample_v2.py CFBC67BA…A060` on the audited commit.
- **Full ranking:** `docs/audit/run_v2/sample.csv`, with sample and reserve in rank order.

| Stratum | Frame | Sample |
|---|---:|---:|
| aeg-d-sparc/v1 | 3 391 | 170 |
| aeg-d-xcop/v1 | 861 | 44 |
| aeg-d-kids1000-rar/v1 | 45 | 10 |
| aeg-d-strong-lensing/v1 | 94 | 10 |
| aeg-d-gc-baumgardt/v1 | 64 | 10 |
| aeg-d-dwarfs/v1 | 64 | 10 |
| **Total** | 4 519 | **254** |

The sample total matches plan §2.2 (254 rows). No replacements were needed.

## Counts, bounds, findings and disclosures

To be added when the reading is complete.
