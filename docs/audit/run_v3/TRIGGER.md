# Audit v3: trigger and seed (plan v3 §1, §2.3)

- **Trigger commit:** `bed8da23e5fa5e3200639861de6ba7754e35c34f`, "Methods text complete (D-113 item 2) (#231)". Merged by JvH ("merge 231"), committed 2026-11-25T15:04:20Z.
- **Seed rule:** the `outputValue` of the NIST Randomness Beacon (version 2.0, chain 2) pulse with the earliest `timeStamp` at or after 2026-11-26T15:04:20Z, which is 24 h after the trigger commit. Pulses come once a minute, so this is expected to be the pulse stamped 2026-11-26T15:05:00.000Z.
- **Fallback:** if NIST is unreachable for 72 h after that time, the drand mainnet round with the earliest time at or after 2026-11-26T15:04:20Z.
- **Freeze:** from the trigger commit to the end of the readings, no change to methods text or package data is merged (plan §1). Any change that is merged anyway is listed as a deviation.
- **Seed record** (read 2026-11-26T15:13Z, before anything was drawn):
  - Pulse: NIST Randomness Beacon v2.0, chain 2, index **2044806**, `timeStamp` **2026-11-26T15:05:00.000Z**.
  - Read at https://beacon.nist.gov/beacon/2.0/chain/2/pulse/2044806 and committed as `seed_pulse.json` (SHA-256 `704579e493b62e20706adaf37406f1c7a95b663b8ba45d7c679d9a962c197b4b`).
  - `outputValue`: `96DE7C5DBE3C933B0BE7DE8D4A14E758A01FDEA8EB480F781217FFF751DCB0657745F2EB99DD4D34A9212D5639C65AB095D674A1C4BA25E36C298827538D73B5`
  - It is the earliest pulse at or after 15:04:20Z: the one before it, index 2044805, is stamped 15:04:00.000Z (`seed_pulse_previous.json`).
  - Chain checks: SHA-512 of this pulse's `localRandomValue` equals the `precommitmentValue` of pulse 2044805, and this pulse's `previous` value equals that pulse's `outputValue`. The pulse signature was not verified here.
  - Read by index: the beacon's `/pulse/time/<ms>` address redirected to NIST's home page when tried. The index was found from `/pulse/last` (2044812 at 15:11:00Z) and the timestamp was confirmed in the pulse itself.
- **Audited commit:** `7f112d491838f2b574ca4db3b6c449ecc41dd2f0` on main, "Front page: the preview chart opens the interactive map (#238)". Since `bed8da2` no file under `docs/methods/` or `data/` has changed (`git diff --name-only bed8da2..7f112d4`: audit tools, one test, the front page). No freeze deviation.
