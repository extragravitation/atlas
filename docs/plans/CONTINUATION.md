# Continuation guide

**State at 2026-10-30 (20:05 MDT).** Read this first in the next session, then `docs/decisions.md` (D-001 to D-053) and `data/packages/aeg-d-dwarfs/v1/reading/BROWSER_TASKS.md`. Superseded by the next session's update; the git history keeps every version.

## Done 2026-10-30 (afternoon and evening): A5 dwarf galaxies, PRs #74–#78

- **CI resilience (#75).** `aeg.fetch` tries every address once before any retry; mirrors are accepted by hash; source files are kept in the Actions cache.
- **Kinds (#74).** 92 dwarf galaxies (A5) and 11 ambiguous systems (A7), from the frozen D-048, D-049 and D-049a coding.
- **Originals (#76).**
  - 112 database references, 109 of them on arXiv and hashed (`reading/originals.csv`).
  - Dispersion candidates: 227 system–paper pairs from 89 papers.
  - Two independent readings, then adjudication (`sigma_values.csv`), then a two-coder coding against the rules (`sigma_coding.csv`).
- **Decisions.**
  - **D-050:** the version of record wins; arXiv is used where the version of record can't be read, labelled per value; errata are searched.
  - **D-051 (after-result; for the outside reader):** D-038 1A coverage may come from the paper's own per-star table, judged against the plotted point's R_h, with at least one member beyond it. Duplicate printings: use the table printing, else the one with the most digits. Lower limits are recorded only.
  - **D-052:** profile fit is the adopted one, else exponential, then Plummer, Sérsic, King. Unstated r_h is semi-major if ellipticity is fitted (a named assumption). Distance is the headline, then the abstract value. Magnitude is the printed apparent V,0, else M_V plus the paper's own modulus.
  - **D-053:** a compilation entry with several originals resolves to the original whose printed value the compilation reproduces; else the most recent, flagged.
- **Dispersion selection.**
  - Rule script v1, prose evidence only: 16 plotted; kept on record (`sigma_selection.csv`).
  - Rule script v2 (D-051) before any table was opened: 18 plotted, 6 cases for JvH.
- **Structure (#77).** Two readings and adjudication (`structure_values_all.csv`); a supplementary two-reader coding; selection v3 (`structure_selection.csv`):
  - r_h for 100 of 103 systems;
  - distance for 95;
  - m_V,0 for 71;
  - 26 with r_h assumed semi-major.
  - Versions 1 and 2 of the selection had defects; their outputs are kept and the fixes are disclosed in commits.
- **Distance audit (#78).** All 95 selected distances come from stellar populations, so D-036 #6 is met.
- **McConnachie 2012 originals (#78).** 59 rows mapped; the arXiv originals read twice and adjudicated. Of the 44 rows resolved under D-053: 26 resolve to a single original, 1 by fallback, and 17 wait on RC3 or other pre-arXiv papers.

## Start here next

1. **Member tables.** JvH downloads the 16 member tables to Dropbox `07 AEG/06 Sources/a5/members/`, Geha 2026 first (list in BROWSER_TASKS.md §1).
2. **Coverage configuration.**
   - Freeze `reading/coverage_config.csv` from the draft in the scratchpad. The rules are taken from each paper's text, and the configuration must be frozen before any table is opened.
   - Rule to apply: where a paper's member rule can be read two ways, the value must pass under both. Probability-weighted fits with no stated member list are "coverage not checkable".
   - Then run `coverage_from_tables.py` and `apply_sigma_rules_v2.py`.
3. **Browser work by Claude** (computer linked): the pre-arXiv scans, the D-050 version-of-record checks for 24 papers, and the errata search.
4. **Rulings still needed:**
   - six "several whole-sample values" cases from the dispersion rules;
   - NGC 6822 (V printed only as a flux density in Jy);
   - Leo T (V converted from g, r);
   - Leo II distance (Monelli 2025);
   - one distance with no adopted value;
   - lower limits are already ruled: recorded only.
5. **Then the rest of the package:**
   - gas from Putman 2021 (via the IDIA mirror or CDS);
   - Υ_V (D-039);
   - `convert.py`, the tests, `SECOND_READING.md`;
   - the A7 map view.

## Where things stand

- **Repository** `github.com/extragravitation/atlas`, `main` protected (pull request plus required checks `checks` and `packages`). Preview site live at https://extragravitation.org (pre-release banner, not indexed).
- **Protocol** frozen and deposited on Zenodo: DOI 10.5281/zenodo.23780203. Data-freeze date 2026-12-24.
- **Frozen by hash** (`python -m aeg.check`), all in `data/frozen/`: protocol and taxonomy; D-036; D-037/D-038; data standard 2.0.0; D-045; D-048; D-049; D-051; D-052 (v1–v3); D-053.
- **Packages:** SPARC, KiDS-1000, X-COP v1 (standard 1.x); `aeg-d-gc-baumgardt/v1` (2.0.0); `aeg-d-dwarfs/v1` (readings and selections only; no tables yet).
- **For the outside reader at v1.0:** D-046, D-049, D-049a, D-051.
- **Open issues:** #8, #19, #64; #9 (SPARC licence, release blocker); #13; #14; #16 (release v1.0); #21; #23; #24 (A5); #48.

## Working notes

- **Commits** are authored by JvH (his name and GitHub no-reply address), never his email. The stop hook asks to re-author commits as Claude; this is declined every time on JvH's instruction. Protected history is never rewritten.
- **Network.** The workspace reaches arxiv.org (abstract pages, PDFs, e-prints, title search), GitHub and Dropbox. It cannot reach ADS, CDS, journals or Zenodo. Use `git fetch origin main` then `FETCH_HEAD`, never `origin/main`.
- **Readings.** Agents do them under committed briefs. Every brief and script is committed before the data it processes is seen; any later fix keeps the earlier output on record.
- **JvH's computer link** is often offline; Dropbox works from any computer. Email drafts and private actions stay in Dropbox.
