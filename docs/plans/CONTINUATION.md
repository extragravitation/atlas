# Continuation guide

**State at end of session, 2026-10-29 (20:17 MDT).** Read this first in the next session, then `docs/decisions.md` (D-001 to D-042). Superseded by the next session's update; the git history keeps every version.

## Start here tomorrow: globular-cluster package (A3, issue #23)

Sources go in Dropbox `/00 JVHA/07 AEG/06 Sources/a3/`, downloaded byte for byte with `curl` (never "Save as" in a browser: that adds a "saved from url" note and changes the hash). Claude pulls them with the Dropbox connector, hashes them, and records them in `sources.json`.

| # | File | Status |
|---|---|---|
| 1 | `veldis.html` (Baumgardt GC database v4, dispersion profiles) | **in**, sha256 `b1bf7032…05de`, 506 494 bytes |
| 2 | `parameter.html` (Baumgardt parameters) | **in**, sha256 `c2e23137…d225`, 188 768 bytes |
| 3 | `appendix.html` (index of individual RVs) | **in**, sha256 `d6262d46…bd58`, 12 609 bytes; links 160 per-cluster `.txt` files |
| 4 | `mwgc.dat` (Harris 2010) | **in**, sha256 `b457a690…a658`, 49 364 bytes |
| 5 | McLaughlin & van der Marel 2005, VizieR J/ApJS/161/304 (structure, luminosity, SPS Υ_V for D-039) | **blocked**: JvH's network cannot connect to cdsarc.cds.unistra.fr, cdsarc.u-strasbg.fr or vizier.nao.ac.jp (timeouts); the CfA mirror redirects to CDS or returns Not Found |
| 6 | 160 per-cluster RV files from `appendix/` (for the D-037 reproduction check) | **not yet run**: PowerShell one-liner in the chat of 2026-10-29 19:14 (`mkdir rv`; loop over `href="*.txt"` in appendix.html with `curl.exe -sL`) |

Next steps, in order:
1. JvH: fetch #5 over a phone hotspot (`curl -L --max-time 120 -o J_ApJS_161_304.tar.gz "https://cdsarc.cds.unistra.fr/viz-bin/nph-Cat/tar.gz?J/ApJS/161/304"`); if that fails, Claude finds the ApJS machine-readable tables on IOPscience (option B). Run #6 (expect 160 files). Delete `ReadMe_2` (an error page).
2. Claude: pull and hash all files; package skeleton `data/packages/aeg-d-gc-baumgardt/v1` (name to settle) under standard 2.0.0; write and freeze `REPRODUCTION.md` **before opening any table**; read structure only (headers, column definitions) until frozen.
3. Convert under D-025, D-036 (frozen `aeg.dispersion`), D-037 (frozen `aeg.repro_dispersion`), D-038, D-039 (McLaughlin & van der Marel Table 8 Υ_V), D-042 (Baumgardt as re-analysis; plotting rules before precedence; Harris HB distances).
4. Second reading (`SECOND_READING.md`), validator, site page type for dispersion systems (plotted / recorded with reason; reproduction results).
5. Then the single-cluster originals (search log A3 §3, §7–§8b), then M31 and NGC 5128 sets; then A5 (dwarfs), then A0.

## Where things stand

- **Repository** `github.com/extragravitation/atlas`, `main` protected (pull request plus required checks `checks` and `packages`). Preview site live at https://extragravitation.org (pre-release banner, not indexed). No open pull requests.
- **Protocol** frozen (PR #35) and deposited on Zenodo: DOI 10.5281/zenodo.23780203 (MD5s verified). Data-freeze date 2026-12-24.
- **Frozen by hash** (checked by `python -m aeg.check`): protocol and taxonomy; D-036 profile conversion (`docs/methods/D036_CONVERSION.md`); D-037/D-038 checks (`docs/methods/D037_D038_CHECKS.md`); data standard 2.0.0 text (`data/frozen/`).
- **Data standard** 2.0.0 (`docs/data-standard.md`, D-041); 1.3.0 kept in `docs/data-standard-1.3.0.md`. Validator implements both.
- **Packages:** SPARC, KiDS-1000, X-COP v1 (standard 1.x); re-issued under 2.0 after v1.0.
- **Searches done:** A0, A3, A5 (ADS via JvH's browser; VizieR via ADS `bibstem:yCat`; full-text screening; re-coding under D-038). Logs in `docs/sources/search-log-*.md`. Remaining cells in issue #48.
- **Rulings today:** D-025, D-036 to D-042. D-040 replaced blind rulings: every decision records who proposed it and what was changed.
- **Open issues:** #8, #19 (known issues); #9 (SPARC licence, release blocker); #13 (CLASH; projection ruling); #14 (site); #16 (release v1.0); #21 (X-GAP); #23 (A3); #24 (A5); #48 (remaining searches).

## Working notes

- Commits are authored by JvH (name and GitHub no-reply address); never his email. The workspace's stop hook asks to re-author commits as Claude; it is declined every time by JvH's instruction, and protected history is never rewritten.
- The workspace cannot reach CDS, ADS or most data hosts; sources come through Dropbox (`06 Sources/`) or JvH's browser, and are verified by SHA-256. CI fetches them itself.
- JvH's computer link (device bridge) is not always connected; Dropbox works regardless of which computer he is on.
- Email drafts and private actions stay in Dropbox (`05 Correspondence`); data requests are on hold by JvH.
- Project instructions' first line now reads "D-028 to D-032, D-040".
