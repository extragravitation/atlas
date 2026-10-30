# Continuation guide

**State at 2026-10-30 (12:05 MDT).** Read this first in the next session, then `docs/decisions.md` (D-001 to D-047). Superseded by the next session's update; the git history keeps every version.

## Done today (2026-10-30)

- **A3 globular clusters live:** `aeg-d-gc-baumgardt/v1` (data standard 2.0.0), PRs #65, #67–#71.
  - 155 Milky Way clusters recorded; 64 plotted, one value each at the 3D half-light radius (D-025).
  - Inputs: King (1966) light weights (`aeg.king66`, D-045); Harris distances and luminosities; population M/L_V (D-039) with the slider from 0.53× to the Salpeter value.
  - Test results: test 2 **FAIL** on record (Pal 1 source-table defect; D-046, for the outside reader); test 4 rejected the Harris r_c reading, so 36 Harris-only clusters are recorded only (D-047); the D-037 check gave 3 pass, 1 fail, 148 not testable (the released velocities cover fewer stars than the profiles).
  - Independent second reading: 3 535 of 3 535 numbers agree.
- **Sources:** McLaughlin & van der Marel 2005 came from the IDIA VizieR mirror (deviation #19, which also discloses values seen early). Fetch the CDS original archive when a network reaches CDS, and compare.
- **Site:**
  - map: no hidden points; per-point error bars (D-044, #63); plotted rows only; `--gc` colour and outlined marks for one-value-per-system data;
  - a system page type for dispersion systems;
  - Safari check passed (#66 closed).
- **Known issues:** #64 (KiDS `no_uncertainty` flag refers to g_bar).
- **For the outside reader at v1.0:** D-046; the 22 below-line SPARC points with Q = 3 need nothing (shown, flagged).

## Start here next: A5 dwarf galaxies (issue #24)

Search log `docs/sources/search-log-A5.md` §3, §7–§8b. Candidates:
- E1 LVDB (Pace 2025): CC0, on GitHub, a compilation with references per value.
- E2 Putman et al. 2021 HI limits (gas side).
- E3 Martin et al. 2016 (M31 structure).
- E4 Tollerud 2012 and Collins 2013 (M31 originals).
- R85 Geha et al. 2026 (alternative; default only where unique; frozen D-038 3A check).
- R86 Ji et al. 2021 (Antlia 2).

Decisions needed before conversion:
- how a compilation that carries the originals' values with references is treated against D-036 #5 and D-038 3B;
- the D-038 1A member-coverage check per system;
- the stellar M/L for dwarfs (D-039: star-formation-history values where cited, otherwise frozen metallicity interpolation);
- the r_half convention (semi-major versus azimuthally averaged).

Then write and freeze REPRODUCTION.md before any table is opened.

## Where things stand

- **Repository** `github.com/extragravitation/atlas`, `main` protected (pull request plus required checks `checks` and `packages`). Preview site live at https://extragravitation.org (pre-release banner, not indexed).
- **Protocol** frozen (PR #35) and deposited on Zenodo: DOI 10.5281/zenodo.23780203 (MD5s verified). Data-freeze date 2026-12-24.
- **Frozen by hash** (checked by `python -m aeg.check`): protocol and taxonomy; D-036 profile conversion (`docs/methods/D036_CONVERSION.md`); D-037/D-038 checks (`docs/methods/D037_D038_CHECKS.md`); data standard 2.0.0 text; D-045 King (1966) and reconstructed binning (`docs/methods/D045_KING66_AND_BINS.md`); all in `data/frozen/`.
- **Data standard** 2.0.0 (`docs/data-standard.md`, D-041); 1.3.0 kept in `docs/data-standard-1.3.0.md`. Validator implements both.
- **Packages:** SPARC, KiDS-1000, X-COP v1 (standard 1.x; re-issued under 2.0 after v1.0); `aeg-d-gc-baumgardt/v1` (standard 2.0.0).
- **Searches done:** A0, A3, A5 (ADS via JvH's browser; VizieR via ADS `bibstem:yCat`; full-text screening; re-coding under D-038). Logs in `docs/sources/search-log-*.md`. Remaining cells in issue #48.
- **Map:** one point per system (outermost measured radius, or first measured radius ≥ 2 × half-light radius), plus an outermost-radius colour check (D-043, PR #58, live).
- **Rulings 2026-10-29:** D-025, D-036 to D-043. **2026-10-30:** D-044 to D-047. D-040 replaced blind rulings: every decision records who proposed it and what was changed.
- **Open issues:** #8, #19, #64 (known issues); #9 (SPARC licence, release blocker); #13 (CLASH; projection ruling); #14 (site); #16 (release v1.0); #21 (X-GAP); #23 (A3: originals and M31/NGC 5128 sets still to come); #24 (A5); #48 (remaining searches).

## Working notes

- Commits are authored by JvH (name and GitHub no-reply address); never his email. The workspace's stop hook asks to re-author commits as Claude; it is declined every time by JvH's instruction, and protected history is never rewritten.
- The workspace cannot reach CDS, ADS or most data hosts; sources come through Dropbox (`06 Sources/`) or JvH's browser, and are verified by SHA-256. CI fetches them itself.
- JvH's computer link (device bridge) is not always connected; Dropbox works regardless of which computer he is on.
- Email drafts and private actions stay in Dropbox (`05 Correspondence`); data requests are on hold by JvH.
- Project instructions' first line now reads "D-028 to D-032, D-040".
