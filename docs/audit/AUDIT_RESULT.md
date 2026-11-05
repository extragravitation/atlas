# Audit result (plan v2, D-082)

**Status: run complete; resolutions pending.**

**Outcome under §2.10 and §3.4, as observed: the audit does not pass.**
- **Part A, values: zero material discrepancies in 254 rows.** The 95 % upper bound on the rate is 1.4 %.
- **Part A, provenance: failures in 250 of 254 rows.** The pass rule requires zero.
- **Methods text: incomplete for 210 of 254 rows.**
- **Part B, neutrality: 4 must-fix and about 120 should-fix findings,** all still unresolved.

Every finding is listed below and resolved by a later pull request, or by no change with the reason. This result is not re-scored.

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


## Part A: re-derivation (§2.5–2.8)

**Run.** 2026-11-05 between 18:50 and 20:15 UTC.

**Readers.** Two fresh agents per stratum, 12 in all, working in separate folders.
- **What each was given:**
  - the fixed brief (§2.6), with an output format added (`run_v2/partA/BRIEF_COMMON.md`);
  - the rows with their `source_ref` locators;
  - the source files, checked by hash;
  - the methods page text;
  - the package's method file or files.
- **Readings and code:** `run_v2/partA/a/` and `run_v2/partA/b/`.
- **Packet build:** `run_v2/partA/build_packets.py`.

**Comparison.**
- `compare.py`, committed at `99547f8` before any reading.
- Output: `run_v2/comparison.csv`.

| Code | SPARC | X-COP | KiDS | Lensing | GC | Dwarfs | All |
|---|---:|---:|---:|---:|---:|---:|---:|
| agree | 0 | 44 | 0 | 0 | 0 | 0 | 44 |
| method incomplete | 170 | 0 | 10 | 10 | 10 | 10 | 210 |
| other codes | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Adjudication.** `adjudication.md`, by Claude, not blind. Every value checked with declared constants agrees with the Atlas within 0.003 dex, so there are **zero material discrepancies**.

| Rows | Clopper–Pearson 95 % upper bound |
|---|---|
| All 254 | 1.4 % |
| SPARC 170 | 2.1 % |
| X-COP 44 | 8.0 % |
| Each 10-row stratum | 30.8 % |

### Methods-text findings (§2.8: findings in their own right)

| # | Dataset | What the written method does not state |
|---|---|---|
| M1 | All | The constants and unit conversions: G, c, M☉, pc/kpc/Mpc in metres, and the astropy version. Every stratum is affected; X-COP's readers also used astropy defaults. |
| M2 | KiDS | That ΔΣ is divided by the released bias(1+K). That g_bar is the released first column. How the `_hotgas` file relates to the stars-plus-cold-gas definition. |
| M3 | Globular clusters | The light-weighted dispersion and King (1966) weights, as formulas; the bin-edge rule; the coverage rule; the solar M_V. |
| M4 | Lensing | The distance formula. The light-profile geometry. SNL-0's redshift choice (CMB frame) and its gas term (the 0.12 % term applies). The source of the gas term. |
| M5 | Dwarfs | The [Fe/H] rule for Υ_V and its source per system. Radii printed already circularised. Choice among several printed moduli or [Fe/H] scales. Preference for the more precisely printed value. "Absent (measured limit)" gas = 0 in g_bar. |
| M6 | Dispersion datasets | The methods page gives only a title line for globular clusters. |
| M7 | X-COP | The public methods page describes v2 (D-089, D-090), not v1. "Row N" is 1-based, but this is not stated. |
| M8 | X-COP | Reader A counts 859 rows inside the D-023 cut, not 861. The modelled-star normalisation has no cited source in `SOURCE.md`. To be checked. |

## Part A: provenance (§2.9)

**Run by** one fresh agent. Full record: `run_v2/provenance/` (summary, CSV and script).

**Failures in 250 of 254 rows.** No file failed its hash.

| # | Rows | Finding |
|---|---:|---|
| P1 | 229 | `sources.json` has no citation field. The citation is in `SOURCE.md` or the role text instead. |
| P2 | 243 | `sources.json` has no licence statement. The "no licence stated" record is in `SOURCE.md` or `descriptor.json` instead. |
| P3 | 2 | Dwarf documents named by the locator have no hashed provenance record: Tucana's Gregory 2019, Saviane 1996 and Bernard 2009, and Leo I's Koch 2007 paper. Confirmed against `reading/originals.csv`. |
| P4 | 10 | Locators without a table, page or column: dwarf σ locators; And XVI's distance column; Draco II's magnitude; the M_V table for CVn II and Leo I (Table 6, not Table 1); Stetson 2014's page; Collins 2013's system list; SNL-0's pages. |
| — | 10 | KiDS: `sources.json` records only the tarball's hash. Its members cannot be checked against the package where the tarball is unreachable. |

**Classifying the causes:**
- **P1 and P2 are where the record is kept.** The text exists in the package, but not in the place §2.9 names.
- **P3 and P4 are real gaps** in the dwarf and lensing reading records.

Under §2.10, each cause is checked across its whole package (exploratory), and each confirmed error is corrected by a new version and logged.

## Part B: neutrality (§3)

See `neutrality.md`.
- **Term scan:** 208 occurrences, of which 10 are findings.
- **Page readers:** 83 and 50 findings, which merge to 4 must-fix (N1–N4) and recurring should-fix themes.
- **Status:** all unresolved at the time of writing.

## Disclosures

- **Who read:** all readers and checkers were fresh Claude agents, isolated by instruction to their own folders.
  - One dwarf reader once listed the session scratch folder by mistake. It saw file names only and opened none; this is recorded in its `notes.md`.
- **Who adjudicated:** Claude, not blind.
- **Deviations from the plan:**
  1. **Method files.** Three packages (lensing, GC, dwarfs) have no `SOURCE.md`. Their readers got `REPRODUCTION.md`, `descriptor.json` and the `docs/methods/` notes these cite. The decision log was not given, because it contains per-row values. This may have raised the "method incomplete" count for those three.
  2. **Dwarf documents.** Dwarf readers also got the package's documents index: the `reading/originals.csv` rows for the sampled systems (citations and hashes only) and the PDFs it lists. Readers could also download arXiv e-prints of cited papers; each did so for some papers, and the URLs and hashes are in their notes.
  3. **KiDS source.** The canonical tarball is unreachable, so KiDS readers got its seven members from the public mirror. Each member's hash matches `aeg-d-kids1000-rar/v2/reading/kids-d096.md`, which CI verifies against the canonical tarball.
  4. **Redacted locators.** Three dwarf locators quote input values. These were replaced by "[value redacted]" in the packets.
  5. **Output format.** An output format was added to the fixed brief (`values.csv` and `inputs.csv`) so that `compare.py` could read the results.
- **Seed:** pulse 2010865, checked as recorded above.
