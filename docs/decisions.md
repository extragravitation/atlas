# Atlas of Extra Gravitation — Decision log (v1)

Decisions that change what the Atlas says or how it measures. Each entry gives the ruling, the reason, the main alternative rejected, and what was checked. JvH rules; Claude proposes and checks. This file is the authoritative log. A snapshot of the first eleven-plus-one rulings is kept in the project's working folder as `DECISIONS_v1.md`; new decisions are added here, by pull request.

All entries below: ruled by JvH on 2026-10-28 (week 1 of the MVP plan).

---

## D-001 — Name

**Ruling.** "Atlas of Extra Gravitation" (AEG). Subtitle: "The acceleration discrepancy, from star clusters to galaxy clusters."

**Reason.** The phrase describes the observed effect (more gravitational acceleration than detected matter produces under Newtonian gravity) without naming a cause; every account agrees the effect exists. The subtitle puts the standard expert term in view.

**Alternative rejected.** "Atlas of the Acceleration Discrepancy": equally neutral, less compelling.

**Checked.** Web search (2026-10-28): no existing project or catalogue uses the name. The phrase is not standard field vocabulary (the literature uses "mass discrepancy", "missing mass", "acceleration discrepancy"); it appears only occasionally, in varied contexts. JvH confirmed the name was not drawn from his independent theoretical work.

## D-002 — Domain

**Ruling.** `extragravitation.org` as the main address, with `atlasofextragravitation.org` redirecting to it. `.com` equivalents optional, defensive only. WHOIS privacy on.

**Reason.** Short and citable. JvH's first choice, `aeg.org`, is already registered.

**Alternative rejected.** No domain until v0.1 (platform default address).

**Amended 2026-10-28.** `atlasofextragravitation.org` not registered (JvH). Citations point to the DOI, every page carries the full name beside the short domain, and it removes a renewal to maintain. `extragravitation.org` registered 2026-10-28 with Cloudflare Registrar; transfer lock on; DNSSEC active.

**Checked.** Registry RDAP lookups, 2026-10-28 ~16:15 UTC, method validated against known registered domains: `aeg.org` registered; `extragravitation.org`, `atlasofextragravitation.org`, `extra-gravitation.org`, `extragravitationatlas.org`, `extragravitation.com`, `atlasofextragravitation.com` unregistered at that time.

## D-003 — Repository owner

**Ruling.** GitHub organisation `extragravitation`; one repository `atlas` → `github.com/extragravitation/atlas`.

**Reason.** An organisation can add advisers and contributors without transfers; the name matches the domain. JvH's first choice, `github.com/aeg`, is an existing personal account.

**Alternative rejected.** Personal account with later transfer (Zenodo record and site address would start under a personal name).

**Checked.** GitHub API, 2026-10-28: `aeg` and `aeg-org` taken; `extragravitation` returned "not found" (no existing account; GitHub reservation confirmed only at creation).

## D-004 — Licences

**Ruling.**
- Atlas text and figures: CC BY 4.0.
- Code: MIT.
- Data tables produced by the Atlas: CC BY 4.0 where the source's terms allow; otherwise the source's terms govern that table, stated on its dataset page.
- Sources that may not be redistributed: linked with a checksum, never hosted, never archived on Zenodo, never committed to the repository.

**Amendment to MVP acceptance criterion 3.** Replace with: "Every source's terms are read and recorded with a hash; where a source states none, the terms of its archival copy (e.g. CDS/VizieR) apply." Permission emails are courtesy notices, not gates.

**Reason.** Attribution matters for a resource meant to be cited and for crediting source authors.

**Alternative rejected.** CC0 for data tables (drops the attribution requirement).

**Checked.** CDS terms (cds.unistra.fr/legals, read 2026-10-28): datasets with only public information are distributed under an open licence (ODbL or CC BY); VizieR data free for scientific use with citation of original authors and publisher. The specific licence of each record is to be read and recorded at package build.

## D-005 — v0.1 datasets (amended)

**Ruling.** Four packages, all proceeding without waiting for replies except where marked:

| Package | Channel | Source | Status |
|---|---|---|---|
| `aeg-d-sparc` | Dynamics (rotation curves) | SPARC, Lelli, McGaugh & Schombert 2016, AJ 152, 157; archival copy CDS J/AJ/152/157 | Proceed; courtesy notice to maintainer |
| `aeg-d-kids1000-rar` | Lensing (population averages) | Brouwer et al. 2021, A&A 650, A113; published excess-surface-density profiles | Proceed; g_obs computed by the Atlas from published profiles using the authors' documented method, labelled as such; request to authors for data points, covariance and g_bar components |
| `aeg-d-xcop` | Dynamics (X-ray hydrostatic) | X-COP public data release (masses: Ettori et al., arXiv:1805.00035; gas: Eckert et al., arXiv:1805.00034; stars: Ghizzardi et al., arXiv:2007.01084) | Proceed; see the X-COP amendment below |
| `aeg-d-clash-lensing` | Lensing (individual clusters) | CLASH: Umetsu et al. 2016, ApJ 821, 116 | **Gated**: binned surface-mass-density profiles and covariance are shown only as figures (Fig. 11); all tabulated masses are NFW fits. Requested from the authors. If not supplied by the data-package milestone, v0.1 ships without cluster-scale lensing and says so on the Methods page |

**Conditions.**
1. Each package must reproduce numbers its source published (SPARC table values; KiDS g_obs points; X-COP hydrostatic masses at R500; CLASH profiles if supplied). Tolerances are written and hash-frozen before the pipeline is run. A package that fails does not ship; the reason is published.
2. No digitising of figures.
3. The cluster stellar-mass slider takes its default from the source's adopted value and its range from the cited stellar-mass literature, read at source; sample quartiles are not used as an uncertainty range.
4. CLASH X-ray (Donahue et al. 2014) gas-mass profiles are used for g_bar of CLASH clusters if the lensing package ships.

**Reason.** Every number on the "observed" side is either measured or derived by a documented, reproducible method, with model-dependent pieces shown as assumptions. Both channels covered; scales from galaxy discs to massive clusters.

**Alternatives rejected.** (a) Original plan with CLASH required (would block v0.1 on unconfirmed data). (b) Using published NFW-based masses and modelled quantities as observations (puts one account's functional form on the observed side).

**Checked (2026-10-28, at source).** SPARC site: no licence stated, citation requested, mass-model files with baryonic contributions offered. KiDS science-data page: no licence stated; only ESD profiles released for this paper. Ettori et al. 2019: reference hydrostatic method assumes NFW; forward method assumes no potential shape; stellar mass modelled from a stellar-to-gas relation. Umetsu et al. 2016: five tables, all model-based; individual profiles reconstructed non-parametrically but tabulated nowhere. X-COP and CLASH data-release statements not found.

**Known limitation to state on the Methods page.** If CLASH lensing is not supplied, v0.1 has no lensing at cluster scale.

**Amended 2026-10-28 (X-COP), ruled by JvH.** Source readings (`docs/sources/xcop.md`) showed that Ettori et al. 2019 does not tabulate per-cluster profiles, that the public X-COP release does, and that the non-parametric profiles of Eckert et al. 2022 are not released. An interim ruling to use Eckert et al. 2022 was therefore superseded the same day. Final ruling for `aeg-d-xcop/v1`:

- g_obs: **forward-method hydrostatic masses** (no assumed shape for the mass) for all 12 clusters, from the public release.
- g_bar, gas: **measured gas mass** for all 12.
- g_bar, stars: **measured** (Ghizzardi et al. 2020) for the 7 clusters that have it, flagged `stars: measured`; for the other 5, a labelled, adjustable assumption, flagged `stars: modelled`.
- **Intracluster light**: a named assumption with its published range, read at source before use.
- The non-parametric profiles of Eckert et al. 2022 are requested from the authors; if supplied, they become `aeg-d-xcop/v2` beside v1 (D-006, D-010).

**Reason.** The least assumption-laden option the public data allow; every compromise is visible per measurement; a better source can replace it later as a new version without breaking any identifier or citation.

**Alternatives rejected.** Waiting for the authors (blocks cluster dynamics on a reply); running the authors' public code ourselves (makes the Atlas an analyst, with unreviewed choices).

## D-006 — Identifiers (permanent)

**Ruling.**
- Systems: `aeg-s-000001` (six digits, sequential, assigned once from a registry file in the repository, never reused). Names and cross-identifications stored alongside, never encoded in the ID.
- Datasets: `aeg-d-<short-name>`, versioned `/v1`, `/v2`, … A released version is never changed.
- Measurements: `aeg-d-sparc/v1/m000123` (permanent because dataset versions are immutable).
- Site releases (`v0.1`, …) are numbered separately from dataset versions.

**Reason.** Stable, neutral across catalogues, exact targets for citations and corrections.

**Alternative rejected.** Name-based IDs (`aeg-s-ngc3198`): break on naming conflicts and favour one catalogue's names.

## D-007 — Hosting

**Ruling.** Cloudflare Pages, connected to the GitHub repository, serving `extragravitation.org`.

**Reason.** Automatic preview site for every pull request (lets every change be checked rendered before merge) and an access-controlled private preview for week 3.

**Alternative rejected.** GitHub Pages (no per-PR previews; public from day one).

**Amended 2026-10-28.** Cloudflare Workers (static assets only, via Workers Builds) instead of Cloudflare Pages. When the project was created, Cloudflare's dashboard labelled Pages the "legacy Pages workflow" and defaulted new projects to Workers. Workers Builds keeps everything D-007 was chosen for: a preview for every pull request, with the preview address posted on the pull request, and optional Cloudflare Access protection. Configuration: `wrangler.jsonc` at the repository root, serving `site/public`; no server code. Starting a long-lived project on a product its vendor calls legacy would mean a migration later.

## D-008 — Reading layer and plain vocabulary

**Ruling.**
- Default layer: Technical. Switch always available on every page, labelled **Technical · Plain language**.
- The choice is remembered in the visitor's own browser and can be carried in a link (`?layer=technical` / `?layer=plain`).
- The default is a single site setting; changing it later is a one-line log entry.
- Plain-layer term: "pull from **detected** matter" (replaces "visible matter": X-ray gas and neutral hydrogen are not visible).

**Reason.** The primary audience is scientists; the plain layer remains one click away. "Plain language" is the recognised term; "Technical" describes the text rather than the reader.

**Alternative rejected.** Plain language by default.

## D-009 — Visitor analytics

**Ruling.** A cookieless, aggregate page counter: no cookies, no stored IP addresses, no personal data. Disclosed on the About page.

**Reason.** Usage evidence for the methods paper and for approaching advisers, at no cost to visitors' privacy.

**Alternative rejected.** No analytics.

## D-010 — Release rhythm

**Ruling.**
- Minor release (v0.2, …) when a meaningful addition is ready.
- Patch release (v0.1.1, …) for corrections, issued promptly.
- Every release gets a Zenodo DOI and a changelog entry.

**Alternative rejected.** Fixed quarterly calendar (makes corrections wait).

## D-011 — Outside review

**Ruling.**
- Building proceeds without advisers.
- One outside neutrality reader (an astronomer reading the text for neutrality; not a formal adviser) is sought in parallel from week 1.
- If no outside reading is complete by release, v0.1 ships labelled "not yet externally reviewed", and the review happens before v0.2.
- A shortlist of two or three advisers from different interpretive camps, each checked against their published work at source, is approached after the preview exists.

**Amendment to MVP acceptance criterion 5.** As above.

**Alternative rejected.** Approach advisers only after the preview (no outside reader possible before v0.1).

## D-012 — Default map view

**Ruling.** The map opens on the observed-against-baryonic view (g_obs against g_bar, with the 1:1 line as Newtonian gravity on detected matter). Excess and radius views one click away. The reason is published on the Methods page. The mockup is updated to match.

**Reason.** Shows the two measured quantities without transforming either; the reference line is the charter's own baseline; any account must reproduce this plot.

**Alternative rejected.** Excess against radius (scatters across scales; can read as hiding the tight relation). The mockup's former default (excess against g_bar) is also replaced.

---

## Recorded alongside (not decisions; corrections to the plans)

- X-ray hydrostatic measurements are not "motions": the method field distinguishes kinematic from hydrostatic, and plain-language labels for X-ray points must say gas pressure balance, not motions.
- Lensing g_obs always involves a deprojection; it is recorded as a named assumption for each lensing package.
- Solar System anchors on the map need their own data package with full provenance, or they are omitted from v0.1.
- The mockup's illustrative points are generated from a published fitting function for the radial acceleration relation; that code is not reused, and mockup screenshots are not circulated.
- Schedule: the four-week estimate is replaced by milestones (decisions; repository; data packages passing reproduction tests; site; reviews; release). Estimated 8–12 weeks with one maintainer.
- JvH to register an ORCID before the first Zenodo release.
