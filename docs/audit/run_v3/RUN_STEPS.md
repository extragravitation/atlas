# Audit v3: run procedure (plan v3, D-116)

Committed before the seed exists, with the scripts it names. It fixes the order of work and the tools; the plan fixes the rules. Where the two differ, the plan wins, and the difference is reported as a deviation.

## Tools, all committed before the seed

| Step | Tool |
|---|---|
| Draw | `docs/audit/sample_v3.py` (frozen with the plan) |
| Packets | `docs/audit/build_packets_v3.py` (tried in the pilot, D-118) |
| Comparison and verdict | `docs/audit/compare_v3.py` |
| Provenance | `docs/audit/provenance_check_v3.py` |
| Part B pages | `docs/audit/choose_pages_v3.py` |
| Term scan | `docs/audit/term_scan.py` (v2, unchanged) |
| Tests | `pipeline/tests/test_audit_v3_scripts.py` (synthetic readers) |

## Order

1. **Seed.** Read the NIST beacon v2.0, chain 2 pulse with the earliest `timeStamp` at or after 2026-11-26T15:04:20Z. Record its index, timestamp, `outputValue` and the URL read in `TRIGGER.md`, and commit it before anything is drawn.
2. **Audited commit.** Record the main-branch commit. List any change to methods text or package data since `bed8da2` as a deviation.
3. **Draw.** Run `python docs/audit/sample_v3.py <outputValue>` and commit the output as `sample.csv`. Run `python docs/audit/choose_pages_v3.py <outputValue>` and commit it as `pages.csv`. Compare the frame counts with plan §2.1, and report any difference.
4. **Packets.** Build one packet set per reader, A and B, in separate folders, with the brief of plan §2.6 exactly as written (the builder's default). List any missing file, and supply it as plan §2.5 says.
5. **Readings.** Give each reader its own packet and nothing else. Readers are fresh agents told to work only in their folder. Their outputs are copied into `readings/a`, `readings/b` and, for step 7, `readings/c`, without being edited.
6. **Comparison.** Run `python docs/audit/compare_v3.py compare readings sample.csv`.
7. **Third reader.** Every "reader disagreement" row goes to a fresh reader C with the same packet and brief. Then re-run step 6.
8. **Provenance.** Run `python docs/audit/provenance_check_v3.py packets readings sample.csv provenance.csv`.
9. **Adjudication.** Claude adjudicates at source, quoting the source, in `adjudication_v3.md`, with one line per row in `adjudication.csv`. This covers:
   - Atlas discrepancies, unresolved disagreements, unreadable and missing rows;
   - blocking method gaps;
   - provenance "review" rows.

   The adjudication outcomes are fixed in the headers of `compare_v3.py` and `provenance_check_v3.py`. Every adjudication is disclosed as not blind.
10. **Verdict.** Run `python docs/audit/compare_v3.py verdict <run dir>`, and report both the verdict and the strict verdict.
11. **Part B.** Run the term scan on the built site at the audited commit. Two fresh readers review the pages of §3.3, including `pages.csv`. Log findings in `neutrality_v3.md`.
12. **Result.** Write `AUDIT_RESULT_v3.md` as plan §4 says, whether the audit passes or fails.

## Dry run on the pilot (D-118), before the seed

The tools were run on the 12 pilot rows and the 16 pilot readers' files. That data is not part of the audit. The dry run found five problems in the tools, all fixed before this commit:
- **Input comparison:** inputs were compared as whole strings, so a value with its error attached ("-1.7 +/- 0.2") differed from the bare value. They are now compared on the first number.
- **Unit check:** physical types used the wrong names ("speed" for astropy's "speed/velocity"), and units like log(pc) and M☉/L☉ could not be read.
- **at_locator answers:** an answer such as "yes (p. 12 ...)" was not read as yes. The first word now decides.
- **Check 6:** a first version counted only inputs tied by name to a locator. It would have missed the X-COP citation errors that the pilot found (D-119), so any input both readers mark "no" now goes to adjudication.
- **The 95 % bound:** the function taken from v2 computes the two-sided interval's upper end. That gives 2.51 % for one row in 220, which would fail the 2.5 % threshold. Plan v3 §2.10 states the one-sided bound by its numbers (1.35 %, 2.14 %, 2.83 %), and D-116 was ruled on those numbers, so the one-sided bound is used. A test pins those numbers.
