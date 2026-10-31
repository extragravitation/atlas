# Continuation guide

**State at 2026-10-31.** Read this first in the next session, then `docs/decisions.md` (D-001 to D-062). Superseded by the next session's update; the git history keeps every version.

## Done 2026-10-31: A5 dwarf galaxies complete and on the site, PRs #82–#86 and this one

- **Package `aeg-d-dwarfs/v1` (#82, #83).** 65 systems; 64 plotted as one value each at the 3D half-light radius (one, And XII, as an upper limit under D-062); And XIII recorded, not plotted. 586 observables.
  - Gas (D-058): Putman 2021 HI rescaled to the package distance by (D_pkg/D_Putman)², helium 1.33, half inside r½.
  - Metallicity (D-059): read at source twice; the dispersion paper's value as a flagged fallback.
  - Υ_V (D-060): an envelope from the McLaughlin & van der Marel 2005 model tables; slider `dw_stellar_ml`.
  - Inputs (D-061, D-062): Boötes III, Muñoz 2018 magnitudes, Leo I, Phoenix, Leo T, Tucana V, And XII, Pegasus IV.
- **Tests.** 1: 534 of 534 numbers found as printed (after disclosed script fixes); 2: 554 of 554; 3: pass; 4: pass.
- **D-050 version of record and errata (#84).** All plotted values agree with the version of record; two errata found, neither changes a value.
- **Site (#85).** Dwarfs on the map (own colour, upper-limit marks), system pages with status, flag explanations and inputs.
- **Magnitude errors (#86).** Printed m_V,0 errors carried into g_bar; values unchanged.
- **D-038 3A consistency check (this branch).** Frozen before it was run: 13 pairs, none beyond 2σ, median z −0.03. Consistent. Reported in `SECOND_READING.md`.
- **#64 (this branch).** The KiDS dataset page says the `no_uncertainty` flag refers to g_bar only. The flag itself is renamed in the 2.0.0 re-issue.

## Start here next

1. **#24 (A5).** The D-037 reproduction check from released per-star velocities: freeze a per-source membership configuration before opening any velocity table, then run `aeg.repro_dispersion.reproduce`. Then close #24.
2. **#23 (A3).** R39 and R83 are still pending.
3. **Accessibility and performance first pass (#14):** contrast in both themes, keyboard use of the map, labels, page weight; a written report.
4. **#48 searches,** A9 (CLASH) and A8 (X-GAP) first, then A6, A4, A10, A1, A2, A7.
5. **Waiting on others.**
   - **SPARC #9 (release blocker):** the CDS licence line for J/AJ/152/157. CDS is unreachable from here and from Chrome; retry when it recovers, and do #8 (the CDS table comparison) on the same visit.
   - **Rulings JvH could make:** record #19 (X-COP) and #8 (SPARC) as known issues for the outside reader.
   - **Zenodo:** `.zenodo.json` is ready; JvH switches on the integration.
   - **Author data requests:** on hold by JvH.

## Where things stand

- **Repository** `github.com/extragravitation/atlas`, `main` protected (pull request plus required checks `checks` and `packages`). Preview site live at https://extragravitation.org (pre-release banner, not indexed).
- **Protocol** frozen and deposited on Zenodo: DOI 10.5281/zenodo.23780203. Data-freeze date 2026-12-24.
- **Frozen by hash** (`python -m aeg.check`): all files in `data/frozen/`, D-036 to D-062 inclusive where a method was frozen, and data standard 2.0.0.
- **Packages:** SPARC, KiDS-1000, X-COP v1 (standard 1.x); `aeg-d-gc-baumgardt/v1` and `aeg-d-dwarfs/v1` (2.0.0).
- **Release v1.0 (#16): not clear.** Open gates: every cell filled (#48), the data freeze, neutrality and outside review, accessibility (#14), the SPARC licence (#9), Zenodo, the release changelog.
- **For the outside reader at v1.0:** D-046, D-049, D-049a, D-051, and the Simon 2019 differences logged under D-053.
- **Open issues:** #8, #9, #13, #14, #16, #19, #21, #23, #24, #48, #64.

## Working notes

- **Commits** are authored by JvH (his name and GitHub no-reply address), never his email. The stop hook asks to re-author commits as Claude; this is declined every time on JvH's instruction. Protected history is never rewritten.
- **Network.** The workspace reaches arxiv.org, iopscience PDFs (retry on 403), GitHub and Dropbox. It cannot reach CDS, aanda.org, OUP or Zenodo; OUP works in JvH's Chrome. VizieR Harvard is flaky; the IDIA mirror works. Use `git fetch origin main` then `FETCH_HEAD`, never `origin/main`.
- **ADS** works in JvH's signed-in Chrome (unquoted bibcode queries, chunks of about 60). Never extract its token.
- **Readings.** Agents do them under committed briefs. Every brief and script is committed before the data it processes is seen; any later fix keeps the earlier output on record.
- **JvH's computer link** is often offline; Dropbox works from any computer. Email drafts and private actions stay in Dropbox.
