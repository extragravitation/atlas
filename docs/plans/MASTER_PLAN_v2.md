# Atlas of Extra Gravitation — Master plan (v2)

2026-10-28. Supersedes v1 (same date). Brings the plan in line with decisions D-001 to D-012 and their amendments (`docs/decisions.md`) and with the source readings (`docs/sources/`). This plan fixes what is expensive to change later; feature detail is left to each release's own plan. The data standard that must be frozen before any data enter the repository is a separate document: `docs/data-standard.md`.

**Changes from v1** are marked ▲. ◆ **Updated 2026-10-29** for D-028 to D-031 (taxonomy and release gate, data standard 2.0, layers and lenses, process safeguards); those changes are marked ◆.

## 1. Purpose and principles

The Atlas describes where and how the observed gravitational acceleration exceeds what Newtonian gravity predicts from detected baryonic matter, across all scales from star clusters to galaxy clusters. It is a field guide, not an argument: "the test to pass" for any account of the acceleration discrepancy. It contains nothing from the author's own theoretical work.

◆ **Stance (D-030): cause-agnostic and reference-explicit.** The Atlas describes observed quantities against a declared reference calculation (Newtonian gravity on detected baryons; General Relativity for converting lensing), registers every step from observation to comparison, and keeps the observables so any account can be checked against the data rather than the Atlas's conversion. It does not claim to be free of theory; it claims to take no side on the cause, and to show its reference openly.

Principles:
- describe, never assume a cause; **describe, never analyse** ▲: the Atlas publishes measurements made by others, with documented conversions; it does not produce new analyses of raw data (D-005 X-COP amendment);
- baseline: Newtonian gravity acting on detected baryonic matter;
- dynamics and lensing are separate channels;
- every number traceable to a published source, with licence (or archival terms) and hash;
- labels never carry the result; continuous properties stay continuous;
- assumptions shown with published ranges, effects computed from data;
- uncertainties, gaps and corrections shown openly;
- tests frozen before data are seen; **every data package reproduces numbers its source published, against tolerances frozen before the pipeline is run** ▲;
- two vocabularies (Technical, Plain language), both precise;
- modern, dynamic and accessible, with every visual showing something real;
- ◆ symmetry: every lens, pattern and account page must be fair by the standard of each account's proponents, and where the discrepancy is absent is shown as prominently as where it is present (D-030).

## 2. Content model

Eight content types. New kinds of system are added as new data in existing types, not as new code.

| Type | What it is | Key fields | First appears |
|---|---|---|---|
| **System** | One astronomical object or bound group, independent of any dataset | `system_id`, names and cross-identifications, position, distance, class labels *as given by each source* | v0.1 |
| **Measurement** | One value of g_obs and g_bar, at one place in one system or for one population bin, from one dataset version | see `docs/data-standard.md` | v0.1 |
| **Profile** | Ordered measurements from one system and dataset | system, dataset, measurements | v0.1 |
| **Average** | A population measurement (e.g. stacked lensing) with its selection rules | selection, N, binning, covariance | v0.1 |
| **Map** | Co-registered 2D layers of one system | layers with source, projection, units, frame | ◆ v1.0 (colliding clusters) |
| **Case study** | Narrative page linking systems, maps and measurements | sections, links, sources | ◆ v1.0 (wide binaries, contested objects) |
| **Pattern** | A field-guide entry: a regularity, where it holds, how strong, what would overturn it | statement (both vocabularies), evidence, strength, open questions, criteria frozen before the cited data are added | ◆ after v1.0 |
| **Test** | A prediction frozen by hash before data are seen, and its result | frozen text, hash, Zenodo timestamp, author, record, data, outcome | ◆ ledger opens with the selection protocol, before new data are converted |

▲ **Method is recorded at two levels.** `channel` is dynamics or lensing (D: never merged by default). `method_class` is kinematic (orbits: rotation curves, velocity dispersions), hydrostatic (gas pressure balance: X-ray, SZ) or lensing. Plain-language labels follow `method_class`, never `channel` alone: X-ray points are "gas pressure balance", not "motions".

▲ **Every assumption that turns an observable into g_obs or g_bar is a named assumption**, recorded on each measurement it affects, including those that are not adjustable (e.g. the lensing deprojection). Each g_bar component (stars, cold gas, hot gas) carries a status: measured, modelled, or absent.

Rules: a System exists once whatever the number of datasets; datasets are never silently merged; Dataset is the unit of provenance; class labels are the source's, not the Atlas's verdict. ◆ The Atlas adds a **kind** (D-028, `docs/plans/TAXONOMY.md`), assigned by a published mapping from the source's label; it never replaces the source's label, and kinds never organise the presentation of findings.

◆ **Layers (D-030).** Every page belongs to one layer, with that layer's rules: (1) the **record** (packages; strictest; nothing interpretive); (2) **lenses** (views of the same data with equal standing, each labelled with the tradition its framing comes from); (3) **patterns** (descriptive, criteria frozen first, exceptions with equal weight); (4) **accounts and tests** (one template for every account; an open ledger of frozen predictions); (5) **exploration** (labelled, never cited as a finding).

## 3. Data standard

Moved to its own document, `docs/data-standard.md`, **frozen as v1.0.0 on 2026-10-28 (D-015)**; current 1.3.0. ◆ **Version 2.0.0 ruled (D-029):** observables with their processing steps, every inference step registered, `model_dependence` and `limit` labels, selection and baryon-inventory records, duplicate and exclusion registers, licences per record; specification in `docs/plans/DATA_STANDARD_2_PROPOSAL.md`, written into the standard before the first 2.0 package. Summary: Frictionless Data Packages; ECSV tables with units, descriptions and IVOA UCD labels; SI accelerations; semantic versioning of the standard; namespaced extension columns; sources never committed unless redistributable, always hashed; a reproduction test per package, frozen first.

## 4. Identifiers and addresses (permanent)

As ruled in D-006:
- Systems `aeg-s-000001`; datasets `aeg-d-<short-name>/v<N>`; measurements `aeg-d-<short-name>/v<N>/m000001`; site releases `v0.1`… numbered separately.
- ▲ Population measurements (Average type) have measurement IDs but no system ID; the population is defined by the dataset's selection metadata. No separate population identifier is introduced.
- Addresses: `/systems/<system_id>`, `/datasets/<dataset>/<version>`, `/patterns/<slug>`, `/cases/<slug>`, `/tests/<test_id>`. Every view state is encoded in the address.
- Each release has a Zenodo DOI; the site states which release it shows.

## 5. Site map

▲ **Rewritten 2026-10-28** after the design prototype (D-026, D-027, D-014 clarification). Two levels, and every page is reachable by its own address.

**Population level: all systems at once**
- **Map** (`/`): g_obs against g_bar with the line g_obs = g_bar (D-012); excess and radius views one click away. Display controls per D-027: points by default, tracks or both on request, error bars off by default, colour by dataset or channel, filter by type from the legend, the weighting stated in words, flagged points always visible. No fitted relation (D-026). Selecting a point highlights its system and opens a card with a link to its page.
- **Scale strip** (`/strip`): one bar per system across the radii where it was measured, shaded by log (g_obs / g_bar) on a continuous scale; the ranges with no packaged measurements are shown as empty.
- **Dataset-wide assumptions** (mass-to-light, hydrostatic bias, intracluster light) are set here and apply everywhere (D-014 clarification). Moved points leave an arrow from their default position.

**Object level: one system**
- **System page** (`/systems/<system_id>`): source facts (class as the source gives it, distance and inclination with errors, redshift, R500, stellar status); the **pull budget** (the source's baryonic components stacked against g_obs, with the g_bar uncertainty band, the full published ranges of the assumptions as outlines, each point's range within its own errors, and the share g_bar / g_obs underneath); an orbital-speed view (V = √(g r), components as lines because speeds add in quadrature); the measurements table; flags with links to known issues; citation and downloads.
- **Per-system assumptions** (distance and inclination, within that system's published errors) are set only here and move only that system; the map marks systems changed this way.

◆ **Lenses (D-030)** on the population level: acceleration (g_obs against g_bar; default), mass (enclosed dynamical against baryonic mass), surface density, scale (radius), speed (rotation curves). Uncertainty display: shifts on both axes from shared assumptions, limits as arrows, stacked bins marked distinctly.

◆ **Kinds** (D-028): browse by kind of system and by tracer; the coverage matrix and its gaps are a page of their own.

◆ **Object level additions:** an **As measured** panel (the observables with errors, and the steps from them to g_obs and g_bar); the baryon inventory beside the pull budget.

◆ **Accounts and tests:** a confrontations section with one template per account, and the test ledger. **Exploration** pages labelled as such.

**Every page**
- A **changed-assumptions bar** whenever anything differs from the sources' defaults, listing each change with its scope and a reset.
- **Technical · Plain language** switch (D-008); **dark theme by default**, light on request (D-027); the view state in the address.

**Reference pages**
- **Dataset pages** (`/datasets/<dataset>/<version>`): method, selection, assumptions with formulas and ranges, licence or archival terms, citation, checksums, the **Validation panel** with the reproduction result (and the D-023 model test for X-COP), change history, downloads.
- **Known issues** (`/known-issues`, D-020), **Methods** (definitions, baseline, both vocabularies, every assumption, why the default view is the default, known limitations and gaps), **Data** (downloads, the data standard, changelog), **About** (charter, authorship and AI disclosure, competing interest, analytics D-009, review status D-011, how to cite, how to report an error, corrections log).

Population averages (KiDS lensing bins) appear on the map and on their dataset page; they have no system page, because they belong to no single system.

## 6. Architecture

- Repository: `github.com/extragravitation/atlas` (D-003): `data/`, `pipeline/` (Python), `site/`, `docs/`. `main` protected: pull request plus passing checks (ruleset, 2026-10-28).
- Checks: GitHub Actions on every pull request.
- ▲ Hosting: **Cloudflare Workers, static assets only** (D-007 amended), at `extragravitation.org`, with a preview for every pull request. No server code, no database, no user data beyond the cookieless counter.
- Site generator: candidate Astro; GPU charts: candidates regl-scatterplot, deck.gl. Chosen when the site is built.
- Releases: tagged; archived on Zenodo with a DOI (D-010); minor releases for additions, patch releases for corrections.
- ▲ Source files that may not be redistributed are fetched at build time by address and verified by hash. A private archive copy of each is kept outside the repository (Dropbox `07 AEG/06 Sources/`) against link rot.
- Reproducibility: one command rebuilds every table from the sources.

## 7. Design system

As v1. ▲ The mockup is updated to D-008, D-012 and the plain-language corrections, and its illustrative points, generated from a published fitting function, are replaced by neutral placeholder geometry.

## 8. Roadmap

◆ Rewritten 2026-10-29 (D-028). The first public release is **v1.0** and covers the taxonomy; previews before it are unnumbered and private.

| Stage | Contents |
|---|---|
| **Preview 1** (built) | Site on the three v1 datasets: map, scale strip, system and dataset pages, known issues, methods, about, downloads (PR #29) |
| **Protocol** | Per-cell eligibility; search protocol and log; data-freeze date; data standard 2.0 text; outside reader asked to review; deposit on Zenodo; test ledger opened for outside predictions |
| **Methods** | Rulings each cell needs, with deadlines before the data-freeze date: D-025 (systems supported by random motions), lensing projection, stellar mass-to-light per kind, wide-binary case study |
| **Packages** | One per eligible dataset, under 2.0.0, each with a blind second reading and a frozen test |
| **Preview 2** | Lenses, As measured panel, kinds and coverage pages, case studies, colliding-cluster maps |
| **v1.0** | Release gate met (TAXONOMY §7); outside review status stated; DOI |
| **After v1.0** | Patterns; accounts pages; v2 of the first three packages under 2.0.0; API and Python package; methods paper (JOSS and arXiv) |

## 9. Governance

- JvH rules on decisions that change what the Atlas says or how it measures; they go in `docs/decisions.md` by pull request.
- ▲ Outside review (D-011): one outside neutrality reader sought from now; v0.1 ships labelled "not yet externally reviewed" if none is complete. Two or three advisers from different interpretive camps approached after the preview.
- Corrections: logged publicly; released as patch versions.
- ◆ **Process safeguards (D-031):** every decision records the data seen when it was ruled, whether it was delegated, and JvH's reason; rules changed after a result apply only to later cases unless the outside reader agrees; every number entering a package gets a blind second reading; for at least one in three method decisions JvH rules before seeing the recommendation; AI reviews are labelled and never presented as outside review. Outside review is brought forward to the selection protocol.

## 10. Risks

| Risk | Mitigation |
|---|---|
| Data licences unstated | Archival terms where they exist; otherwise link and hash, never commit (D-004) |
| ▲ Link rot (observed: the X-COP address in Ettori et al. 2019 is dead) | Hash every source; private archive copy; record the address actually used |
| ▲ Best data not public (e.g. CLASH profiles, Eckert et al. 2022 profiles) | Ship the best public version; request the better one; add it as a new dataset version |
| Neutrality of choices | Written selection rules; defaults justified on the Methods page |
| Single maintainer | Automation, documentation, advisers |
| ▲ Vendor tooling in beta (Cloudflare previews) | Judge behaviour on production; note known quirks in `site/README.md` |
| Scope creep | Release-by-release plans; ◆ closed taxonomy with gap rules and deadlines (D-028) |
| ◆ Selection following the data | Protocol frozen and timestamped outside the repository; eligibility on metadata only; deviations register (D-028) |
| ◆ AI anchoring and unchecked AI readings | Blind second readings; recorded reasons; some rulings made before the recommendation is seen (D-031) |
| ◆ Dependence on others' releases | Gap rule: 8 weeks after a request, a cell becomes a documented gap |

## 11. Before any data enter the repository

Done: `docs/data-standard.md` frozen as v1.0.0 (D-015), together with sections 2 and 4 of this plan.
