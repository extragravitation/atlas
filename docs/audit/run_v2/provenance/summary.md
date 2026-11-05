# Provenance check (plan v2 §2.9): summary

The checker was a fresh agent. It read the reader packets and `sources.json` only; it did not see the Atlas values. Claude transcribed this summary from the agent's report, because the agent could not write `.md` files. The full record is `provenance.csv`, produced by `provenance_check.py`.

- 254 measurements, 7 checks each, 1 778 rows: **1 259 pass, 484 fail, 35 n/a**. 250 measurements have at least one failure.
- Every source file present matches its recorded SHA-256. This includes the VizieR content hashes and the 14 dwarf PDFs.

| Check | pass | fail | n/a |
|---|---:|---:|---:|
| 1 Locator matches an entry | 252 | 2 | 0 |
| 2a Citation in the `sources.json` entry | 24 | 229 | 1 |
| 2b Licence statement in the entry | 10 | 243 | 1 |
| 2c Hash recorded | 253 | 0 | 1 |
| 3 File matches its hash | 243 | 0 | 11 |
| 4 Located table, row and column exist | 243 | 10 | 1 |
| 5 Units match | 234 | 0 | 20 |

## Failures

**F1. No citation in `sources.json` (229 rows).**
- SPARC (170) and X-COP (44): the entry gives only a role. The citation is only in `SOURCE.md`.
- Globular clusters (10): the `veldis.html` entry has no year or reference.
- Strong lensing (5, S4TM): the entry for `iop/apjaa9794t2_ascii.txt` has no citation.

**F2. No licence statement in `sources.json` (243 rows).**
- SPARC, X-COP, KiDS (224): only `"redistributable": false`. The "no licence stated" record is in `SOURCE.md`.
- Globular clusters (10): no entry has a licence statement. `descriptor.json` has a licence status.
- Dwarfs (9): `documents_index.csv` (from `reading/originals.csv`) has no licence field.

**F3. A document named by the locator has no provenance record (2 rows).**
- dwarfs m000059 (Tucana): Gregory 2019 (σ), Saviane 1996 (R_e and M_V) and Bernard 2009 (distance) are not in `sources.json` or `reading/originals.csv`. Claude confirmed this in the repository during adjudication.
- dwarfs m000042 (Leo I): the Koch 2007 paper is not recorded or hashed; only its VizieR star table is.

**F4. The located table, row or column is missing or ambiguous (10 rows).**
- Dwarfs (9 checkable rows): the σ locator names the paper only, with no table or page.
- dwarfs m000013: the distance locator names no column, and the source row has four.
- dwarfs m000036: "M_V + (m-M) used by the paper (own)" names no table.
- dwarfs m000031 and m000042: the M_V locator points to Table 1, but M_V is in Table 6.
- dwarfs m000042: the Stetson 2014 locator gives no page.
- dwarfs m000020: the documents index omits andromeda_23 from Collins 2013's systems.
- strong lensing m000140: both records are PDFs, and the locator gives no page or table.

**Not applicable.**
- KiDS (10): the canonical tarball is unreachable. `sources.json` records only the tarball's hash, so its mirrored members cannot be checked against the package record.
- Units for strong lensing and dwarfs (20): the written method states none.
- Tucana (5): no document to check (F3).

## Also noted by the checker
- X-COP: the methods page describes the v2 conversion (D-089, D-090), while the v1 package's `SOURCE.md` describes v1.
- X-COP locators name only the hydrostatic-mass file, not the gas and stellar files that give g_bar.
- X-COP "row N" does not say whether rows count from 0 or 1.
