# Audit v3: trigger and seed (plan v3 §1, §2.3)

- **Trigger commit:** `bed8da23e5fa5e3200639861de6ba7754e35c34f`, "Methods text complete (D-113 item 2) (#231)". Merged by JvH ("merge 231"), committed 2026-11-25T15:04:20Z.
- **Seed rule:** the `outputValue` of the NIST Randomness Beacon (version 2.0, chain 2) pulse with the earliest `timeStamp` at or after 2026-11-26T15:04:20Z, which is 24 h after the trigger commit. Pulses come once a minute, so this is expected to be the pulse stamped 2026-11-26T15:05:00.000Z.
- **Fallback:** if NIST is unreachable for 72 h after that time, the drand mainnet round with the earliest time at or after 2026-11-26T15:04:20Z.
- **Freeze:** from the trigger commit to the end of the readings, no change to methods text or package data is merged (plan §1). Any change that is merged anyway is listed as a deviation.
- **Seed record:** filled in when the pulse is read, before the sample is drawn.
