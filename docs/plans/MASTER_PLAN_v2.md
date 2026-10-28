# Atlas of Extra Gravitation — Master plan (v2)

2026-10-28. Supersedes v1 (same date). Brings the plan in line with decisions D-001 to D-012 and their amendments (`docs/decisions.md`) and with the source readings (`docs/sources/`). This plan fixes what is expensive to change later; feature detail is left to each release's own plan. The data standard that must be frozen before any data enter the repository is a separate document: `docs/data-standard.md`.

**Changes from v1** are marked ▲.

## 1. Purpose and principles

The Atlas describes where and how the observed gravitational acceleration exceeds what Newtonian gravity predicts from detected baryonic matter, across all scales from star clusters to galaxy clusters. It is a field guide, not an argument: "the test to pass" for any account of the acceleration discrepancy. It takes no side and contains nothing from the author's own theoretical work.

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
- modern, dynamic and accessible, with every visual showing something real.

## 2. Content model

Eight content types. New kinds of system are added as new data in existing types, not as new code.

| Type | What it is | Key fields | First appears |
|---|---|---|---|
| **System** | One astronomical object or bound group, independent of any dataset | `system_id`, names and cross-identifications, position, distance, class labels *as given by each source* | v0.1 |
| **Measurement** | One value of g_obs and g_bar, at one place in one system or for one population bin, from one dataset version | see `docs/data-standard.md` | v0.1 |
| **Profile** | Ordered measurements from one system and dataset | system, dataset, measurements | v0.1 |
| **Average** | A population measurement (e.g. stacked lensing) with its selection rules | selection, N, binning, covariance | v0.1 |
| **Map** | Co-registered 2D layers of one system | layers with source, projection, units, frame | v0.3 |
| **Case study** | Narrative page linking systems, maps and measurements | sections, links, sources | v0.3 |
| **Pattern** | A field-guide entry: a regularity, where it holds, how strong, what would overturn it | statement (both vocabularies), evidence, strength, open questions | v0.4 |
| **Test** | A prediction frozen by hash before data are seen, and its result | frozen text, hash, record, data, outcome | v0.5 |

▲ **Method is recorded at two levels.** `channel` is dynamics or lensing (D: never merged by default). `method_class` is kinematic (orbits: rotation curves, velocity dispersions), hydrostatic (gas pressure balance: X-ray, SZ) or lensing. Plain-language labels follow `method_class`, never `channel` alone: X-ray points are "gas pressure balance", not "motions".

▲ **Every assumption that turns an observable into g_obs or g_bar is a named assumption**, recorded on each measurement it affects, including those that are not adjustable (e.g. the lensing deprojection). Each g_bar component (stars, cold gas, hot gas) carries a status: measured, modelled, or absent.

Rules (unchanged): a System exists once whatever the number of datasets; datasets are never silently merged; Dataset is the unit of provenance; class labels are the source's, not the Atlas's verdict.

## 3. Data standard

Moved to its own document, `docs/data-standard.md`, **frozen as v1.0.0 on 2026-10-28 (D-015)**. Summary: Frictionless Data Packages; ECSV tables with units, descriptions and IVOA UCD labels; SI accelerations; semantic versioning of the standard; namespaced extension columns; sources never committed unless redistributable, always hashed; a reproduction test per package, frozen first.

## 4. Identifiers and addresses (permanent)

As ruled in D-006:
- Systems `aeg-s-000001`; datasets `aeg-d-<short-name>/v<N>`; measurements `aeg-d-<short-name>/v<N>/m000001`; site releases `v0.1`… numbered separately.
- ▲ Population measurements (Average type) have measurement IDs but no system ID; the population is defined by the dataset's selection metadata. No separate population identifier is introduced.
- Addresses: `/systems/<system_id>`, `/datasets/<dataset>/<version>`, `/patterns/<slug>`, `/cases/<slug>`, `/tests/<test_id>`. Every view state is encoded in the address.
- Each release has a Zenodo DOI; the site states which release it shows.

## 5. Site map

As v1, with:
- ▲ The map opens on the **observed-against-baryonic view** (g_obs against g_bar with the 1:1 Newtonian line); excess and radius views one click away (D-012).
- ▲ Reading layer **Technical** by default; switch **Technical · Plain language** on every page, carried in links (D-008).
- ▲ Plain-language term "pull from **detected** matter" (D-008).
- ▲ About page includes the cookieless-analytics disclosure (D-009) and the outside-review status (D-011).

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

| Release | Goal | Main contents |
|---|---|---|
| **v0.1** | Useful and citable | Map (three views), system and dataset pages, data downloads, methods and about pages, DOI. Data: SPARC, KiDS-1000 RAR, X-COP v1; CLASH lensing if supplied |
| **v0.2** | Compelling | "Where is the extra pull?", the ghost disc, galaxy tracks, plot builder; ▲ second independent rotation-curve set; ▲ X-COP v2 if the non-parametric profiles are supplied |
| **v0.3** | Beyond points | Map type; first case study; ▲ method against method on the same clusters (CLASH X-ray against lensing) |
| **v0.4** | The field guide | Patterns; sky and coverage; early-type galaxies, dwarf spheroidals, groups |
| **v0.5** | Open | Tests ledger; API and Python package |
| **v1.0** | Reviewed and published | Adviser review; methods paper |

## 9. Governance

- JvH rules on decisions that change what the Atlas says or how it measures; they go in `docs/decisions.md` by pull request.
- ▲ Outside review (D-011): one outside neutrality reader sought from now; v0.1 ships labelled "not yet externally reviewed" if none is complete. Two or three advisers from different interpretive camps approached after the preview.
- Corrections: logged publicly; released as patch versions.

## 10. Risks

| Risk | Mitigation |
|---|---|
| Data licences unstated | Archival terms where they exist; otherwise link and hash, never commit (D-004) |
| ▲ Link rot (observed: the X-COP address in Ettori et al. 2019 is dead) | Hash every source; private archive copy; record the address actually used |
| ▲ Best data not public (e.g. CLASH profiles, Eckert et al. 2022 profiles) | Ship the best public version; request the better one; add it as a new dataset version |
| Neutrality of choices | Written selection rules; defaults justified on the Methods page |
| Single maintainer | Automation, documentation, advisers |
| ▲ Vendor tooling in beta (Cloudflare previews) | Judge behaviour on production; note known quirks in `site/README.md` |
| Scope creep | Release-by-release plans |

## 11. Before any data enter the repository

Done: `docs/data-standard.md` frozen as v1.0.0 (D-015), together with sections 2 and 4 of this plan.
