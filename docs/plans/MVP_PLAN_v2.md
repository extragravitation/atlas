# Atlas of Extra Gravitation — MVP plan: release v0.1 (v2)

2026-10-28. Supersedes v1 (same date). Derived from `MASTER_PLAN_v2.md`; where they differ, the master plan governs. Rulings referenced are in `docs/decisions.md`. **Changes from v1** are marked ▲.

## 1. Goal

A first public release that a working astronomer would find useful and cite, and that a member of the public would find compelling: the interactive map, a page for every system, honest assumption sliders, downloadable and citable data, built on the full content model and the frozen data standard.

## 2. Scope

**In v0.1**
- **The map:** ▲ observed-against-baryonic view by default (D-012), excess and radius views; dynamics and lensing channels; filters by the source's class labels; linked object card; shareable view addresses; ▲ **Technical · Plain language** switch, Technical by default (D-008).
- **System pages:** ▲ the pull budget (components against g_obs, with uncertainty, assumption ranges and the share g_bar / g_obs), an orbital-speed view, all measurements, per-system assumptions, sources, licence or archival terms, citation, download; per-measurement flags (stars measured or modelled; named assumptions). Structure: `MASTER_PLAN_v2.md` §5.
- ▲ **Scale strip:** coverage of every system across radius, shaded by the discrepancy, with the empty ranges shown.
- **Dataset pages:** method, selection, assumptions, licence, citation, checksums, ▲ reproduction-test result, change history.
- ▲ **Known issues** page and a Validation panel on each dataset page (D-020).
- **Data:** ECSV downloads with units and column labels, plus generated CSV and Parquet; the data standard; the changelog.
- **Methods:** definitions, baseline, both vocabularies, every assumption with formula and range, ▲ why the default view is the default, known limitations.
- **About:** charter, authorship and AI disclosure, competing-interest statement, ▲ analytics disclosure (D-009), ▲ outside-review status (D-011), how to cite, how to report an error, corrections log.
- **Release:** tagged, Zenodo DOI.

▲ **Not in v0.1 unless ruled otherwise:** Solar System anchors (D-013 below). Everything listed for later releases in the master plan.

## 3. Datasets (D-005 as amended)

| Package | Channel / method class | Built from | Status |
|---|---|---|---|
| `aeg-d-sparc/v1` | dynamics / kinematic | SPARC mass models (175 disc galaxies) | Ready to build |
| `aeg-d-kids1000-rar/v1` | lensing / lensing | KiDS-1000 public release: g_bar bins, ESD, covariance; g_obs = 4GΔΣ (authors' method) | Ready to build |
| `aeg-d-xcop/v1` | dynamics / hydrostatic | X-COP public archive: forward-method masses (12), gas mass (12), stellar mass (7) | Ready to build |
| `aeg-d-clash-lensing/v1` | lensing / lensing | CLASH binned profiles, if supplied by the authors | Gated on reply |

Selection rule (published on the Methods page) unchanged from v1. ▲ The rule now also states: the Atlas uses the least assumption-laden version of each dataset that is public, and records better versions as later dataset versions.

## 4. Assumption sliders in v0.1 (▲ revised; D-014 below)

Only assumptions whose effect can be computed exactly from what the packages store. Defaults and ranges are read at source before a slider is enabled (registry `status: confirmed`).

| Assumption | Applies to | Exact computation | Default and range |
|---|---|---|---|
| Stellar mass-to-light, disc | SPARC | g_bar,disc scales linearly with Υ_disc | Source's adopted value; range to be read at source |
| Stellar mass-to-light, bulge | SPARC (32 galaxies with bulges) | g_bar,bulge scales linearly with Υ_bulge | As above |
| Distance | SPARC | Per galaxy within its published error: R ∝ D, g_obs ∝ 1/D at fixed angle; g_bar unchanged | Table 1 distance and error |
| Inclination | SPARC | g_obs ∝ 1/sin²i (V_obs ∝ 1/sin i); g_bar unchanged under the thin-disc treatment of the photometry (to be confirmed in the SPARC paper before enabling) | Table 1 inclination and error |
| X-ray hydrostatic bias | X-COP | g_obs scales by 1/(1−b) | b = 0 (source); range to be read at source |
| Cluster stellar mass (modelled clusters only) | X-COP, 5 clusters | g_bar,stars of those clusters scales linearly | Range to be read at source |
| Intracluster light | X-COP | Adds a fraction of measured stellar mass to g_bar,stars | 0 (source excludes it); ≈10–50 % of cluster light per Ghizzardi et al. 2020, underlying studies to be read at source |

**Shown but not adjustable:**
- KiDS: the authors' ±0.2 dex stellar-mass systematic **stated in words**, citing their Fig. 4 (D-021: not computable from the release, so no band), and their released "with hot gas" variant as a switchable alternative baseline.
- Lensing deprojection (KiDS: singular isothermal sphere, validated by the authors against a shape-free method).

**Dropped from v1:** "gas beyond atomic hydrogen" as a uniform rescaling of SPARC gas. Molecular gas is not distributed like atomic gas, so a uniform scale factor is not an exact computation of a real assumption. It returns if a source with molecular-gas profiles is added.

## 5. Acceptance criteria (v0.1 is done when all hold)

1. One command rebuilds every table from the sources; all checks pass.
2. Every measurement traces to source, dataset version, licence or archival terms, and checksum, shown on its system page.
3. ▲ Every source's terms are read and recorded with a hash; where a source states none, the terms of its archival copy apply (D-004 amendment).
4. Every slider changes only the measurements it should, by the registry formula; a test checks this.
5. ▲ Neutrality review of all text by Claude; an outside reading if one is complete, otherwise the release is labelled "not yet externally reviewed" (D-011).
6. Accessibility: WCAG 2.2 AA contrast and keyboard; phone, tablet and desktop; reduced motion respected.
7. Performance: the map stays smooth with every v0.1 measurement shown, on a mid-range laptop and phone.
8. Zenodo DOI, CITATION file, changelog.
9. No illustrative data anywhere on the site.
10. ▲ Every package passes its conversion-integrity check exactly; any mismatch with the source's published reference is recorded as failed, flagged per measurement, listed on the Known issues page and referred to the source (D-019).

## 6. Milestones (▲ replace weeks)

| # | Milestone | Done when | Estimate |
|---|---|---|---|
| M1 | Repository and accounts | Repository, checks, protection, domain, hosting, previews | ✅ 2026-10-28 |
| M2 | Plans and standard | These plans approved; data standard frozen (D-015); D-013 and D-014 ruled | ✅ 2026-10-28 |
| M3 | Data packages | SPARC, KiDS, X-COP passing reproduction tests; assumption registry confirmed | 2–3 weeks |
| M4 | Site | Map, system and dataset pages, data, methods, about, on the preview | 3–4 weeks |
| M5 | Review and release | Neutrality, accessibility, performance reviews; v0.1 tagged with DOI | 1–2 weeks |

Total estimate 7–10 weeks from today with one maintainer. CLASH lensing joins at M3 or M5 if the data arrive; it never holds up the release.

## 7. Decisions (ruled 2026-10-28)

| # | Decision | Ruling |
|---|---|---|
| **D-013** | Solar System anchors | Deferred to v0.2 |
| **D-014** | v0.1 slider set | Section 4, with formulas written once and executed identically by pipeline and site |
| **D-015** | Data standard | Frozen as v1.0.0: semantic versioning, ECSV with units and UCD labels, namespaced extension columns |

## 8. Risks for v0.1

- **CLASH reply** (most likely gap): v0.1 ships without cluster-scale lensing and says so.
- **Assumption ranges** must each be read at source; a slider without a confirmed range stays disabled rather than shipping a guessed range.
- **Overreach:** anything not in section 2 waits.
