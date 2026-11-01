# Continuation guide

**State at 2026-11-01, 11:45 MDT.** Read this first in the next session, then `docs/decisions.md` (D-001 to D-076). Superseded by the next session's update; the git history keeps every version.

## Done 2026-10-31 (evening): A6 and A9 searches, rules frozen, A9 route chosen. PRs #88–#90 merged, #92 open

- **Accessibility first pass (#88, merged).** Report: `docs/reviews/2026-10-31-accessibility-pass-1.md`. Four findings remain open:
  1. keyboard selection of map points;
  2. the ends of the colour ramp in the light theme;
  3. translucent single points;
  4. the map payload (about 540 kB gzipped).
- **A6 strong lensing (#89, merged).** Search log A6, screening (E 21, E-pair 28, P 2, X 21). D-063 (eight rules), D-064 (project the baryons: G·M/R_E², "projected", own mark), D-065 (precedence frozen, `data/frozen/a6s-precedence.json`).
- **A9 clusters (#90, merged).**
  - Search log A9, screening (E 28, E-pair 33).
  - Epoch cut z < 0.30 (D-066); joint fits and stacks (D-067); measured stars, issue #91 for X-COP modelled stars (D-068); no summing of member catalogues (D-069); RXC1825/A1644/A2255/A3158/A3266 plan (D-070).
  - Printed luminosity × registered ratio counts as measured (D-071). Round L screened (`docs/sources/screening-L9/`, E 14).
  - Round L rules QL1–QL6 (D-072); A9 precedence frozen (D-073, `data/frozen/a9-precedence.json`).
  - Coverage v3: 116 of 319 clusters below z = 0.30 have measured stars; 79 can be paired with an observed side.
- **A9 gas coherence (#92, open).** No programme supplies an observed side, stars and gas density profiles for the same clusters. D-074 sets the A9 route:
  - case studies: A85, A2142 and ZwCl 1215 (dynamics plus X-COP baryons); A1689, A1835, A2390 and MS 1455+22 (lensing); Coma (both);
  - a LoCuSS one-radius layer at r500,WL, with two scoped rule changes: a 3D NFW-fit lensing mass, and projected stars as an upper bound. Its spec is to be frozen before any table is opened;
  - a CHEX-MATE watch and a funnel page.

## Done 2026-11-01: A6 strong lensing shipped (PRs #93, #94, #95)

- **Package and site.** `aeg-d-strong-lensing/v1` is live on the map and on lens pages: 94 plotted lenses, 212 recorded (CHANGELOG).
- **Rulings.** D-075 and D-076; data standard 2.1.0.
- **Lessons.**
  - In a git worktree, run the pipeline with `PYTHONPATH=<worktree>/pipeline`; the installed `aeg` points at /home/claude/atlas.
  - Never let a build agent add a passing outcome to a frozen test; check every test change.
  - Tell JvH before long background runs: a stop pressed from the phone kills subagents.

## Start here next

0. **v0.1 released (D-077):** pre-release, Zenodo DOI 10.5281/zenodo.23864356 (all versions 10.5281/zenodo.23864355). Competing interests are stated (D-078). Next: the review-readiness plan (awaiting JvH's answers: freeze new datasets, author contact, order).
1. **A6 packaging (done)** in the worktree `../atlas-a6`, branch `data/a6-strong-lensing`, to the frozen A6 rule:
   1. a source list and licences;
   2. REPRODUCTION.md frozen before conversion;
   3. two-reader input reading;
   4. tests 1–3.
2. **A9 X-COP case studies:** A85, A2142, ZwCl 1215. The baryons are already in `aeg-d-xcop`; the caustic profiles come from the SAO team.
3. **LoCuSS spec** (D-074 item 3): write it and freeze it, then package.
4. **Remaining case studies, then the funnel page;** tag v0.2 after A6 and v0.3 with the cluster layers.
5. **Still open from before:** #24 (A5 D-037 check); #23 (A3 R39, R83); SPARC #9 (CDS licence); accessibility findings 1–4; Zenodo switch-on (JvH); author data requests on hold (JvH).

## Done 2026-10-31 (earlier): A5 dwarf galaxies complete and on the site, PRs #82–#86 and this one

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

## Where things stand

- **Repository** `github.com/extragravitation/atlas`, `main` protected (pull request plus required checks `checks` and `packages`). Preview site live at https://extragravitation.org (pre-release banner, not indexed).
- **Protocol** frozen and deposited on Zenodo: DOI 10.5281/zenodo.23780203. Data-freeze date 2026-12-24.
- **Frozen by hash** (`python -m aeg.check`): all files in `data/frozen/` (including the A6 and A9 precedence rules, D-065 and D-073), D-036 to D-073 where a method was frozen, and data standard 2.0.0.
- **Packages:** SPARC, KiDS-1000, X-COP v1 (standard 1.x); `aeg-d-gc-baumgardt/v1` and `aeg-d-dwarfs/v1` (2.0.0).
- **Release v1.0 (#16): not clear.** Open gates: every cell filled (#48), the data freeze, neutrality and outside review, accessibility (#14), the SPARC licence (#9), Zenodo, the release changelog.
- **For the outside reader at v1.0:** D-046, D-049, D-049a, D-051, and the Simon 2019 differences logged under D-053.
- **Open issues:** #8, #9, #13, #14, #16, #19, #21, #23, #24, #48, #64, #91.

## Working notes

- **Commits** are authored by JvH (his name and GitHub no-reply address), never his email. The stop hook asks to re-author commits as Claude; this is declined every time on JvH's instruction. Protected history is never rewritten.
- **Network.** The workspace reaches arxiv.org, iopscience PDFs (retry on 403), GitHub and Dropbox. It cannot reach CDS, aanda.org, OUP or Zenodo; OUP works in JvH's Chrome. VizieR Harvard is flaky; the IDIA mirror works. Use `git fetch origin main` then `FETCH_HEAD`, never `origin/main`.
- **ADS** works in JvH's signed-in Chrome (unquoted bibcode queries, chunks of about 60). Never extract its token.
- **Readings.** Agents do them under committed briefs. Every brief and script is committed before the data it processes is seen; any later fix keeps the earlier output on record.
- **JvH's computer link** is often offline; Dropbox works from any computer. Email drafts and private actions stay in Dropbox.
