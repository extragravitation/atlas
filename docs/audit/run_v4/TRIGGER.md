# Audit v4: trigger and seed (plan v4 §1, §2.3)

- **Trigger commit:** `16689894ad171023b34ae550b0247b90e2577c1a`, "Audit plan v4 frozen (D-125) (#258)". Merged on JvH's "merge 258", committed 2026-11-27T17:50:37Z.
- **Frozen files** (`data/frozen/audit-plan-v4.json`): `AUDIT_PLAN_v4.md` SHA-256 `3dd6a680c52ff7d8de16faf932c07c72ee2264e1d7e806a5dbf090c32522686d`, with `sample_v4.py`, `choose_pages_v4.py` and `compare_v4.py`.
- **Seed rule:** the `outputValue` of the NIST Randomness Beacon (version 2.0, chain 2) pulse with the earliest `timeStamp` at or after 2026-11-28T17:50:37Z, which is 24 h after the trigger commit. Pulses come once a minute, so this is expected to be the pulse stamped 2026-11-28T17:51:00.000Z (10:51 in Calgary).
- **Fallback:** if NIST is unreachable for 72 h after that time, the drand mainnet round with the earliest time at or after 2026-11-28T17:50:37Z.
- **Freeze:** from the trigger commit to the end of the readings, no change to methods text or package data is merged (plan §1). Any change that is merged anyway is listed as a deviation.
- **Seed record:** to be added after the pulse exists, before anything is drawn.
