# Pilot of the v3 audit readings (D-118)

**Purpose.** Find gaps in the methods text (D-113 item 2) before its merge starts the audit (D-116). The pilot is a dry run of Part A on a few rows. It is not part of the audit, it is not scored, and its results are published here whether or not they find anything.

**Written before any pilot packet was opened**, 2026-11-25. Committed together with `docs/audit/build_packets_v3.py`, which builds the packets, so the audit's packet builder is tried out at the same time.

## Rows

- **How many:** two per package, 12 in all.
- **How drawn:** ranked as in `docs/audit/sample_v3.py`, but with the prefix `aeg-pilot-v3` in place of `aeg-audit-v3`.
- **Seed:** the full hash of main commit `c0cf4c4a0194e52dbf0e62ac65d53db14031bfe8`, the merge of D-117. It is public, and was fixed before the draw. It is not the audit seed.

| Package | Rows |
|---|---|
| aeg-d-sparc/v3 | m000669, m001593 |
| aeg-d-xcop/v3 | m000001, m000078 |
| aeg-d-kids1000-rar/v3 | m000003, m000012 |
| aeg-d-strong-lensing/v3 | m000021, m000101 |
| aeg-d-gc-baumgardt/v3 | m000066, m000020 |
| aeg-d-dwarfs/v3 | m000053, m000014 |

## Readers

- **Who:** two fresh agents per package, A and B.
- **What each gets:** only its packet, which is the same as the audit packet (plan v3 §2.5) and is built by `build_packets_v3.py`.
- **Brief:** the audit brief (§2.6), with one sentence added: "Also list, as method gaps, every step you had to infer or guess, even where you are confident of the result."
- **Isolation:** each reader is told to use only its own folder.

## What is done with the results

- **Gaps:** every method gap a reader reports is fixed in the methods text before the text is merged. The fix is listed in `RESULT.md`.
- **Values:** the readers' values are compared with the Atlas's rows by the audit tolerances (§2.7). A discrepancy is investigated, labelled exploratory. A confirmed error goes through the corrections log as usual.
- **Packets:** problems with the packet builder are fixed before the audit.
- **Overlap with the audit:** a pilot row may also be drawn in the audit sample. It is not replaced, and the overlap is reported in the audit result.
- **The frozen plan:** the pilot does not change audit plan v3.

## Files

- **The problem:** some source hosts refuse connections from the workspace (SPARC, KiDS, the globular-cluster database, Harris, and the VizieR mirror at IDIA).
- **The fix:** packets for those packages wait until the hosts are allowed or JvH supplies the files.
- **The check:** every file is verified as `aeg.fetch` verifies it.
