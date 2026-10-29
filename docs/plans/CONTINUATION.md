# Continuation guide

**State at end of session, 2026-10-28.** Read this first in the next session, then `docs/decisions.md` (D-001 to D-024). Superseded by the next session's update; the git history keeps every version.

## Where things stand

**Repository** `github.com/extragravitation/atlas`, `main` protected (pull request plus required checks `checks` and `packages`). Site placeholder live at https://extragravitation.org (Cloudflare Workers static assets, D-007 amended); preview address posted on every pull request.

**Data standard** 1.2.1 (`docs/data-standard.md`). Pipeline package `aeg` (`pipeline/`): `fetch`, `validate`, `check`, `formula`, `formula_check`, `package checksums`.

**Three dataset packages merged** (4 297 measurements, 187 systems):

| Package | Channel | Rows | Reproduction | Sliders |
|---|---|---|---|---|
| `aeg-d-sparc/v1` | Dynamics, rotation curves, 175 galaxies | 3 391 | FAILED on 4 points, shippable under D-019; known issue #8 | disc and bulge mass-to-light, distance, inclination |
| `aeg-d-kids1000-rar/v1` | Lensing, stacked isolated galaxies, 3 samples × 15 bins, covariance | 45 | PASSED | none; ±0.2 dex stated in words (D-021) |
| `aeg-d-xcop/v1` | Dynamics, X-ray hydrostatic, 12 clusters | 861 | FAILED for A644, A2029, A2319, shippable under D-019; known issue #19. Modelled-star test (D-023) passed for r/R500 = 0.145–1.38 | hydrostatic bias 0–0.2 (all); intracluster light 0–0.5 (7 measured-star clusters) |

Data the site can render (summary given to JvH 2026-10-28): the g_obs–g_bar map with the 1:1 line (2 SPARC points with g_bar ≤ 0 listed beside it), excess views, object pages for 175 galaxies and 12 clusters with components, a KiDS population page, live sliders from the shared formulas, flags, the Known issues page, a Validation panel per dataset, downloads and citations. Not available: cluster-scale lensing (CLASH gated, #13), Solar System points (D-013), sky positions (not captured), the modelled-star slider (D-022).

## Ruled today, last items

- **D-022** X-COP assumption defaults and ranges.
- **D-023** Modelled stars ship only where validated on the measured clusters (frozen test, passed 0.145–1.38 R500; 204 rows cut).
- **D-024** v0.1 public release waits for galaxy groups, globular clusters and dwarf spheroidals; dispersion-supported systems need a ruled method first (D-025). Site is built meanwhile on the three datasets and previewed privately.

## Design direction (agreed 2026-10-28, not a logged decision)

Light theme after the "Journal figure" look (white, serif headings, thin black axes, numbered figure captions); dark theme after the "Observatory" look (near-black, instrument-like). Both share every encoding: shape for method, colour for dataset, rings for flags, dashed line for Newtonian gravity on detected matter. From the "Data desk" look: system search and the filter rail. Exploratory comps (real data, not wired) on the claude.ai canvas "Atlas look options". Working prototype on real data: claude.ai page "Atlas Map Prototype" (dark by default). D-026 and D-027 govern what the map draws.

## Next, in order

1. **Site v0.1 (#14)** on the three datasets: map (default view D-012), SPARC and X-COP object pages, KiDS population page, sliders (formulas executed by `site/src/formula.mjs`), Known issues page (D-020, generated from issues labelled `known-issue`), Validation panels, downloads and citations, Technical · Plain language switch (D-008), dark and light themes, phones. Mockup update (#15) alongside.
2. **Reading for D-024/D-025**, at source, before any conversion:
   - #21 X-GAP: is there a public release of group profiles, and on what terms?
   - #22 method for dispersion-supported systems: Wolf et al. 2010 (half-light-radius estimator) and alternatives; propose D-025 with options and a recommendation.
   - #23 globular clusters: Baumgardt & Hilker 2018 / Baumgardt et al. 2019: how dispersion profiles were compiled, licence, measured versus fitted. Observed side from measured dispersions only.
   - #24 dwarf spheroidals: identify a published kinematic compilation.
3. For each new dataset: source note, frozen `REPRODUCTION.md`, package, CI, result file, as for X-COP.
4. Still open: #9 (CDS licence line for SPARC; release blocker), #13 (CLASH, gated), #16 (review and release).

## Working notes

- Commits are made under JvH's name with his GitHub no-reply address; never his email. The workspace's automated check asks for a different author on every commit; it is ignored by JvH's instruction, and protected history is never rewritten.
- The workspace cannot reach SPARC, CDS, KiDS or Switch Drive; sources are read in JvH's browser pane or staged from his computer, and verified by SHA-256. CI fetches them itself.
- On a pull request the data workflow commits regenerated tables back as github-actions[bot]; such a commit does not trigger checks, so a further commit is needed before merging. Converters must be bit-deterministic (X-COP uses scalar `math.log`/`math.exp`; numpy's vectorised versions differed between CI runners).
- Errors in CI are reported as annotations (logs are not readable from the workspace).
- Private actions (emails to Umetsu, Lelli, Eckert and Ettori, Brouwer; ORCID; Zenodo; outside neutrality reader) are tracked outside the repository, by JvH.
