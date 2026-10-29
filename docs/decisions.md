# Atlas of Extra Gravitation — Decision log (v1)

Decisions that change what the Atlas says or how it measures. Each entry gives the ruling, the reason, the main alternative rejected, and what was checked. JvH rules; Claude proposes and checks. This file is the authoritative log. A snapshot of the first eleven-plus-one rulings is kept in the project's working folder as `DECISIONS_v1.md`; new decisions are added here, by pull request.

D-001 to D-027: ruled by JvH on 2026-10-28 (week 1 of the MVP plan). From D-028 each entry also records the data seen at the time of ruling, whether the call was delegated, and JvH's reason in his own words (D-031).

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

## D-013 — Solar System reference points

**Ruling (2026-10-28).** Deferred to v0.2. They need their own sourced data package; v0.1 does not show them.

**Reason.** No unsourced points on the map (rule 2); v0.1's datasets already span the range of the map.

**Alternative rejected.** Build a small sourced package for v0.1.

## D-014 — v0.1 assumption sliders

**Ruling (2026-10-28).** The revised set in `docs/plans/MVP_PLAN_v2.md` §4:
- SPARC: stellar mass-to-light (disc; bulge), distance and inclination (each per galaxy within its published error);
- X-COP: X-ray hydrostatic bias; stellar mass of the 5 clusters without measured stars; intracluster light;
- KiDS: no sliders; the authors' ±0.2 dex stellar-mass systematic shown as a band (amended by D-021: stated in words, no band), and their released hot-gas variant as an alternative baseline;
- dropped: uniform rescaling of SPARC gas for gas beyond atomic hydrogen (molecular gas is not distributed like atomic gas, so a uniform factor is not an exact computation of a real assumption).

**Clarified 2026-10-28 (JvH), scope of each slider.** Dataset-wide (one value for every system in the dataset, as the sources adopt it): SPARC disc and bulge mass-to-light, X-COP hydrostatic bias, X-COP intracluster light (measured-star clusters only). Per system (each system only, within its own published error, set on that system's page): SPARC distance and inclination. Every page shows a list of changed assumptions with their scope and a reset for each; galaxies with per-system changes are marked on the map. The full published range of each assumption is shown separately on system pages, independent of the current setting. Recorded in the registry as the field `scope` (data standard 1.3.0).

**Plus:** each slider's effect is written once, as a formula in a restricted expression language, and executed from that same text by both the pipeline and the site; the build checks that the two agree on every measurement (`docs/data-standard.md` §6).

**Reason.** Only effects that can be computed exactly; one formula, proven identical in tests and on the site.

**Alternative rejected.** The v1 slider set; separate Python and JavaScript implementations.

## D-015 — Data standard frozen

**Ruling (2026-10-28).** `docs/data-standard.md` frozen as **version 1.0.0**, with:
- semantic versioning of the standard (patch: wording; minor: additive and backward-compatible; major: breaking);
- **ECSV** tables carrying each column's unit, data type, description and **IVOA UCD** label (UCD1+ vocabulary v1.6, 2024-12-18, validated automatically);
- namespaced extension columns (`x_<dataset>_<name>`) for source-specific extras that the core never depends on.

**Reason.** Settle the template before any data are poured into it, so released data, checks and site share one meaning per column; use the astronomy community's own table format and vocabulary so the data are interoperable; allow growth without breaking anything published.

**Alternative rejected.** Revise further before freezing; plain CSV without embedded metadata.

**Checked.** UCD list read from astropy 8.0.2's bundled copy (`EN-UCDlist-v1.6-2024-12-18`); every UCD used in the standard validated with astropy's parser against it; ECSV header written and read back with astropy.

## D-016 — SPARC reproduction test: implementation bug

**Ruling (2026-10-28, JvH accepted the recommendation).** Correct the test implementation so the frozen rule δV/V < 0.1 is applied in exact decimal arithmetic on the published two-decimal values. `REPRODUCTION.md` is unchanged. The failed first run is kept on record in `REPRODUCTION_RESULT.md`.

**Reason.** The frozen text is unambiguous; floating-point division kept two points (F568-3, ratios 10.7/107.0 and 11.7/117.0) that the rule excludes. Correcting an implementation to match its frozen specification is not re-scoring; changing the specification would be.

**Alternative rejected.** Leaving the bug in place.

## D-017 — SPARC reproduction discrepancies

**Superseded by D-019 (same day).** **Ruling (2026-10-28, JvH accepted the recommendation).** Four SPARC points (UGC00128 at 53.75 kpc; UGC07524 at 2.41 and 10.69 kpc; UGC09133 at 77.5 kpc) do not match the authors' published file. Ask the maintainer (draft to Lelli). Whether SPARC v1 ships is decided at milestone M5 with the answer in hand, not now. D-005 condition 1 ("a package that fails does not ship") is unchanged.

**Reason.** Avoid relaxing a rule immediately after seeing a failure; the site takes weeks to build, so waiting costs nothing.

**Alternative rejected.** Ship now with the four points flagged.

## D-018 — Data standard 1.1.0

**Ruling (2026-10-28, JvH accepted the recommendation).** Minor (additive) version of `docs/data-standard.md`: optional measurement columns `g_bar_stars_disk`, `g_bar_stars_bulge`; optional systems columns `inclination_deg`, `inclination_err_deg` (UCD `src.orbital.inclination`); slider formulas may reference core columns of the row's system as `system.<column>`. Every package valid under 1.0.0 stays valid.

**Reason.** Needed by D-014 (separate disc and bulge mass-to-light sliders; per-galaxy distance and inclination sliders) and found while building the first package.

**Alternative rejected.** Revise further before approving.

## D-019 — Shipping rule for packages whose reproduction test fails

**Ruling (2026-10-28, JvH).** Amends D-005 condition 1 for all packages, ruled before the KiDS and X-COP tests had run. Supersedes D-017's "decide at M5".
- A package **must** pass its conversion-integrity check exactly. Any failure there blocks it.
- A mismatch with the source's published reference **stays recorded as a failed test**; it is never redefined as a pass. In the test suite the failing checks are kept unchanged and marked as strict expected failures, and a separate test locks the discrepancy to exactly the documented set (so any new or vanished mismatch fails the build).
- Every mismatched measurement carries the flag `reproduction_mismatch` and a link to its known issue; every mismatch is listed publicly (D-020) and referred to the source.
- The dataset page states the result as failed, with the numbers.

**Applied to SPARC:** known issue #8; 4 measurements flagged; SPARC v1 may ship in v0.1.

**Reason.** The reproduction test exists to catch errors in our conversion; conversion integrity is exact. Withholding 175 galaxies over 4 documented points serves readers worse than publishing everything with the discrepancy shown, and the discrepancy is itself a finding about the sources.

**Alternative rejected.** Keep "a package that fails does not ship" (D-005 condition 1 as first ruled).

**Note (2026-10-29, D-031).** This ruling was made after SPARC's reproduction test had failed, and applied to SPARC; D-017 had said not to relax a rule immediately after a failure. The ruling stands pending the outside reader's written view (D-011, D-031). If the reader disagrees, SPARC v1 is held back from the first public release and the question is ruled again.

## D-020 — Known issues page

**Ruling (2026-10-28, JvH).** A public **Known issues** page in the site's Data section, generated at build time from GitHub Issues labelled `known-issue`. Each entry: affected dataset and measurement IDs, date found, status (open, under investigation, resolved), action, evidence. Two-way links between flagged measurements and issues. Resolved issues move to the Corrections log with the release that fixed them. Each dataset page gets a Validation panel with its reproduction result. Development work stays in public GitHub Issues and Projects, linked from About.

**Reason.** Established practice for serious data releases (e.g. Gaia "known issues", SDSS "known problems"); open problems shown openly, from a single record that cannot drift.

**Alternative rejected.** A "backlog" or "to do" page mixing project work with data reliability.

**Checked.** Label `known-issue` created; first issue opened: #8 (SPARC).

## D-021 — KiDS stellar-mass uncertainty: no band

**Ruling (2026-10-28, JvH).** Amends D-014 for KiDS. No band is drawn for the authors' ±0.2 dex stellar-mass systematic. It is stated in words on every KiDS point and on the dataset page, citing Brouwer et al. 2021 Fig. 4. The shifted-mass files are requested from the authors; if supplied, the band is added as a computed layer from them.

**Reason.** The band is not in the data release: the authors produced it by re-running the analysis with shifted stellar masses, which moves lenses between g_bar bins, so it cannot be computed exactly from the public files. An approximate shift would be "approximated for show", which the charter forbids.

**Alternative rejected.** Shift g_bar by ±0.2 dex as an approximate band.

## D-022 — X-COP assumptions: defaults and ranges

**Ruling (2026-10-28, JvH), before the X-COP conversion was run.** Applies D-014 to `aeg-d-xcop/v1`.

1. **X-ray hydrostatic bias** `xray_hse_bias`, b, with M_true = M_hydrostatic / (1 − b). Default **0**, range **0 to 0.2**, adjustable on all 12 clusters. Effect: g_obs and its errors divided by (1 − b); g_bar unchanged (gas mass comes from the gas density, not from hydrostatic balance).
   - Default: the X-COP team find about 6 % non-thermal pressure at R500 and 10 % at R200, and that hydrostatic masses "require little correction" (Eckert et al. 2019, arXiv:1805.00034).
   - Upper end: the same paper reports 1 − b = 0.85 ± 0.05 for Planck's SZ-based masses; 0.2 is that value's one-sigma edge.
2. **Intracluster light** `icl_fraction`, f, the share of total cluster starlight not counted in the measured stellar masses. Default **0**, range **0 to 0.5**, adjustable on the **7 clusters with measured stars only**. Effect: g_bar,stars divided by (1 − f), so the extra light is assumed to follow the measured stars' radial distribution (Zibetti et al. 2005 find it more concentrated; stated on the page).
   - Range: the span the stellar-mass source itself gives (Ghizzardi et al. 2020, arXiv:2007.01084): Zibetti et al. 2005, 10.9 ± 5.0 % within 500 kpc; Zhang et al. 2019, 44 ± 17 % within 1 Mpc. Zhang's figure includes the central galaxy, which the measured masses already count, so 0.5 is generous.
3. **Modelled stars, 5 clusters** (A1644, A2255, A3158, A3266, RXC1825) `stars_cluster_modelled`. The default follows Ettori et al. 2019 (arXiv:1805.00035 §5): an NFW-shaped cumulative profile with concentration 2.9 (Lin et al. 2004, arXiv:astro-ph/0402308, from galaxy number counts with the central galaxy excluded, defined relative to r200, which Ettori's Table 1 gives per cluster), normalised so that M★(<R500) / M_gas(<R500) = 0.39 (M500 / 10¹⁴ M☉)^−0.84 (Gonzalez et al. 2013). M500 and R200 are Ettori Table 1's hydrostatic values and are not recomputed under the bias slider. **Status draft, no slider ("disabled until read")**: the slider is switched on only after Gonzalez et al. 2013 has been read at source for the relation's scatter and for whether its stellar masses include the central galaxy and intracluster light. Rows carry `stars_status = modelled`.

**Reason.** Defaults are the source team's own; ranges are the spans the cited literature gives, read at source. Nothing ships switched on whose range has not been read.

**Alternatives rejected.** Range 0 to 0.3 for the bias (beyond what any cited X-COP or Planck figure supports); intracluster light on all 12 clusters (the modelled-star prescription may already include it); a modelled-stars slider from sample quartiles (forbidden by D-005 condition 3).


## D-023 — Modelled stars: ship only where the model is validated

**Ruling (2026-10-28, JvH), before the test was run.** The modelled-star profile (D-022 item 3) excludes the central galaxy, so near the centre it under-predicts g_bar and inflates g_obs/g_bar for the 5 modelled clusters. The prescription is tested where the truth is known: applied to the 7 clusters with measured stars, it must reproduce their g_bar within 10 % (median of the absolute deviation over the clusters, as a function of r/R500). Modelled rows ship only within the validated range of r/R500. Exact procedure frozen in `data/packages/aeg-d-xcop/v1/MODEL_TEST.md` (hash in `sources.json`); outcome in `MODEL_TEST_RESULT.md`; the dataset page explains the cut.

**Reason.** A model artefact must not sit on the map as an observation; the cut is set by data, by a rule fixed before the comparison was made. The 10 % is a judgement call, inside the hydrostatic-bias range already allowed (0 to 20 %).

**Alternatives rejected.** A fixed inner radius chosen after the star fractions had been seen (post hoc); shipping every row with the problem stated in words (leaves an artefact on the map).

**Result (first run, 2026-10-28).** Validated range r/R500 = 0.145 to 1.38; inside 0.145 R500 the prescription misses the measured clusters' g_bar by up to 74 %, outside 0.2 R500 by 4 % or less (median). 204 modelled rows removed (innermost kept radius 153–212 kpc); 861 measurements ship. Details: `MODEL_TEST_RESULT.md`.


## D-024 — Scope of v0.1: add groups, globular clusters and dwarf spheroidals

**Ruling (2026-10-28, JvH).** The public v0.1 release waits until it also covers:
- **galaxy groups** (candidate: X-GAP, Eckert et al. 2024, arXiv:2403.17145; release status to be read at source), filling the range between single galaxies and massive clusters;
- **globular clusters** (candidate: Baumgardt & Hilker 2018, arXiv:1804.08359; VizieR J/MNRAS/478/1520), which include systems where Newtonian gravity on detected matter is expected to suffice;
- **dwarf spheroidal galaxies** (source to be identified), the individual systems with the lowest g_bar.

Systems supported by random motions need a ruled method before any of their data are converted (D-025, to come; leading candidate: a mass estimator at the half-light radius, Wolf et al. 2010, to be read at source). Measured velocity dispersions, not masses fitted with simulations, form the observed side (the principle of D-005). If X-GAP has not released usable profiles, alternatives are brought to JvH; the other two do not wait on groups. Wide binary stars are left to v0.2 with their own method ruling. Meanwhile the site is built on the three existing datasets and previewed privately.

**Reason.** An atlas that shows only systems with large extra pull answers its question before asking it: the test to pass must include systems where no extra pull is expected, the most extreme low-acceleration systems, and more than one kind of system. Delay is acceptable; a biased first release is not.

**Alternative rejected.** Ship v0.1 with three datasets and state the gap (faster, but the first public picture would rest almost entirely on rotating disc galaxies).

**Backlog.** Issues #21 (groups), #22 (method, D-025), #23 (globular clusters), #24 (dwarf spheroidals).


## D-026 — No fitted relation on the map in v0.1

**Ruling (2026-10-28, JvH).** The map draws the data and the line g_obs = g_bar (Newtonian gravity on detected matter) only. No fitted relation (for example the published radial-acceleration fitting function) is drawn in v0.1. A fit may return later as a sourced Pattern entry, clearly labelled and switched off by default.

**Reason.** A fitted curve on the default view tells readers what the pattern "is" before they have looked; the data and the Newtonian baseline say enough on their own.

**Alternative rejected.** Show a published fit as an optional overlay from v0.1.

## D-027 — Map display defaults

**Ruling (2026-10-28, JvH).** Readers choose how the data are drawn; every choice is kept in the shareable address.
- Marks: **points by default**; tracks (each system's points joined in order of radius) or both on request. Selecting a point highlights its whole system in every mode.
- Error bars: **off by default** on the map, one click to show; every uncertainty is shown on hover and on the system page.
- Colour by dataset by default; by method or source class label on request; continuous properties only with continuous scales.
- A density layer for when the number of points makes overplotting unreadable.
- Theme: **dark by default**; light on the reader's choice, remembered in their browser. (JvH, 2026-10-28, after the prototype; supersedes "follow the system setting".)
- Filter by type in one click: selecting a type in the legend shows only that type; selecting it again shows everything.
- Selection: no system is selected on arrival; selecting one draws its measurements joined in order of radius, labelled with its name, with a clear-selection control.
- The legend states the weighting in words (for example "X-COP: 861 points from 12 clusters").
- Display options never change which measurements appear or their values; flagged points stay visible, with their rings, in every mode.
- Not a display option: one point per system (needs a rule for the representative radius, which is a method choice for a separate ruling).

**Reason.** Points are the most literal picture (one mark per packaged measurement) and the easiest to read; tracks show where in each system the extra pull appears; stating the weighting stops a few densely sampled systems from reading as a population.

**Alternative rejected.** Tracks or error bars on by default (harder to read at 4 300 points).

## D-028 — Taxonomy, selection protocol and release gate

**Ruling (2026-10-29).** Delegated: JvH asked "As a good scientist, what do you recommend?" and approved the recommendation ("Proceed"). JvH's reason: "We need non-bias, but at the same time we need compelling and useful." Earlier in the same discussion: "It's of huge advantage to have all the types accounted for and all data gathered."
1. **Taxonomy.** The first public release covers the kinds of system in `docs/plans/TAXONOMY.md` (A0 Solar System to A10 colliding clusters). Kinds are defined by morphology and composition, never by the tracer or by g_obs; rotational support (v/σ) and dynamical state are continuous properties. Kinds organise coverage and navigation only, never the presentation of findings.
2. **Selection protocol, written before any new data are converted** (TAXONOMY §6): eligibility criteria per cell; a fixed search protocol with a logged record of what was found, screened and excluded and why; every eligible dataset included by default, with a pre-written ranking where a choice is unavoidable; eligibility decided on metadata only, with no g_obs–g_bar plot of a candidate before; a public deviations register.
3. **Gaps.** A cell is a documented gap only if the logged search found no eligible public data, or a data request has gone unanswered for 8 weeks. "Method not yet ruled" is never a reason: every method ruling a cell needs has a deadline before the data-freeze date.
4. **Freeze.** The taxonomy and protocol are frozen by hash and deposited on Zenodo for an outside timestamp before any new conversion. The outside reader is asked to review them first; if none has replied within 4 weeks, they are deposited and the page says so. A data-freeze date is set in the protocol; later finds go to the next version.
5. **Release gate.** The first public release, named **v1.0**, is published when every cell is a package or a gap under 3, and these are live: a control where Newtonian gravity on detected matter is expected to suffice (Solar System as a limit; globular clusters); the lowest-g_bar individual systems (dwarf spheroidals and ultra-faint dwarfs); at least one galaxy kind other than rotating discs; both channels; at least two lenses (D-030); the cross-check status and the coverage report on continuous axes. Previews before v1.0 are unnumbered. Amends the charter's "launch v0.1 quickly", the D-010 rhythm before v1.0, and the master-plan roadmap; extends D-024.
6. **Scope.** The Solar System is included as a limit on anomalous acceleration, not as a point. Wide binaries are included as a case study of each team's published results (they give no per-system g_obs). Open clusters are included as a kind and may end as a gap.
7. **Contested single objects** (NGC 1052-DF2 and -DF4, AGC 114905, Abell 520, wide binaries) are case studies that present each side's published values as named alternatives, neither as the default.
8. **Projection.** Lensing (projected) and dynamics (3D) are compared like with like; per dataset, the baryons are projected rather than the lensing deprojected, where the baryon data reach far enough.
9. **Stellar mass-to-light** for star clusters and dwarfs: default and range from the stellar-population literature, read at source, adjustable per kind.

**Reason.** A first public picture built on a few kinds answers the Atlas's question before asking it; fixing the selection rules before conversion, with an outside timestamp, makes the choice of data independent of what the data show; gap rules with deadlines bound the work without leaving an escape hatch; the minimum set guarantees the controls and extremes that make the picture fair.

**Alternatives rejected.** Release on the three datasets now (D-024); release only when every cell is filled (unbounded); a minimum set alone without accounting for every kind (JvH wants all kinds accounted for).

**Data seen at the time of ruling.** The three v1 packages and their results; the exploratory stress test of 2026-10-28; the source survey (metadata, abstracts and data pages; nothing converted); two AI methodology reviews (`docs/reviews/2026-10-29-methodology.md`).

## D-029 — Data standard 2.0: observables first

**Ruling (2026-10-29).** Delegated, as D-028. Data standard 2.0.0, as specified in `docs/plans/DATA_STANDARD_2_PROPOSAL.md` (revised 2026-10-29):
- Packages record the observables the source releases machine-readable, with the chain of processing steps from data to each quantity (a ladder per tracer), and link every g_obs and g_bar to them. Where a source releases only inferred quantities, the package says so.
- Every inference step is a registered assumption with a role (observed inference, baryonic inference, selection), adjustable or not; the background cosmology is registered where it enters (e.g. Σ_crit in lensing).
- A `model_dependence` label on each measurement: none; parametric on a thermodynamic or projected observable; parametric on the total mass. All are included, labelled and filterable. Masses derived from scaling relations are excluded (circular).
- A `limit` column (none, upper, lower) on g_obs and observables.
- Required records: selection criteria (`x_selection`) and the baryon inventory (`x_baryon_inventory`, including components known to exist but not measured).
- Cross-identifications record whether two datasets use independent data; a frozen precedence rule sets which dataset the default map shows; cross-checks use independent pairs only. A public register lists systems excluded by a source or by the Atlas, with reasons.
- Licence recorded per source record; derived tables follow share-alike terms where a source requires them (e.g. ODbL).
- Frozen tests compare at the observable level where the source releases observables.
- The standard text is written into `docs/data-standard.md` and frozen before the first 2.0 package. New packages follow 2.0.0. The three v1 packages are not re-issued before v1.0 (they keep their observables as extension columns); they are re-issued afterwards. "Frozen" means no non-patch change for 30 days, except by a decision naming the package it blocks.

**Reason.** g_obs and g_bar are inferences whose steps include assumptions not every account shares; keeping the observables lets any account be checked against the data rather than against the Atlas's conversion. The model-dependence label replaces an exclusion rule that could not be applied evenly (it would have excluded KiDS's isothermal deprojection and X-COP's fitted pressure forms).

**Alternatives rejected.** Keep 1.x with optional observables (record stays framework-dependent); exclude fits that assume a total-mass shape (uneven, see Reason); re-derive every g_obs uniformly from raw data (replaces the sources' expertise; outside "describe, never analyse").

**Data seen at the time of ruling.** As D-028.

## D-030 — Layers, lenses and stance

**Ruling (2026-10-29).** Delegated, as D-028.
1. **Stance.** The Atlas is **cause-agnostic and reference-explicit**: it describes observed quantities against a declared reference calculation (Newtonian gravity on detected baryons; General Relativity for the lensing conversion), registers every step, and keeps the observables so any account can bypass the reference. "Theory-neutral" is not used. (The project description on claude.ai is JvH's to update.)
2. **Five layers, each with its own rules.** (1) The record: data packages; strictest; nothing interpretive. (2) Lenses: several views of the same data, equal standing, each labelled with the tradition its framing comes from. (3) Patterns: descriptive regularities and where they fail, with strength, scope, exceptions and what would overturn them, judged by criteria frozen before the data they cite are added. (4) Accounts and tests: each account presented from its proponents' published claims in the same template; a test ledger open to frozen predictions deposited by anyone before new data are converted, results posted pass or fail. (5) Exploration: open, labelled exploratory, never cited as a finding.
3. **Lenses for v1.0:** acceleration (g_obs against g_bar; default per D-012), mass (enclosed dynamical against baryonic mass), surface density, scale (radius), speed (rotation curves). Methods states that the acceleration plane comes from the radial-acceleration-relation tradition and the mass view from the dark-matter tradition.
4. **Symmetry.** Before publishing any lens, pattern or account page: would a proponent of each account call it fair? The outside reader and advisers are asked exactly that. Where the discrepancy is absent is shown as prominently as where it is present.
5. **Display of uncertainty:** shifts on both axes from shared assumptions (distance, inclination, mass-to-light) drawn from the registry formulas; limits as arrows; stacked bins with a mark style distinct from single systems.

**Reason.** Respect for neutrality comes from rigour in the record and symmetry in presentation, not from showing less; plural lenses answer the objection that any single plane carries a tradition; an open test ledger makes "the test to pass" literal and gives every camp a reason to engage.

**Alternatives rejected.** One privileged view (carries one tradition); no patterns or accounts until after v1.0 (safe but not compelling, and the charter calls for a confrontations section).

**Data seen at the time of ruling.** As D-028.

## D-031 — Process safeguards

**Ruling (2026-10-29).** Delegated, as D-028. Responds to the methodology review.
1. From D-028, every decision records the options as proposed, the recommendation, whether the call was delegated, JvH's reason in his own words, and the data seen at the time of ruling.
2. A rule changed after a result is known applies only to later cases, unless the outside reader agrees in writing. D-019 carries a note to this effect.
3. **Blind second reading.** Every number entering a package is read a second time at source by an independent session or a person, with a quote and its location; disagreements are logged in the package.
4. For at least one in three method decisions, JvH rules before seeing Claude's recommendation; the log records which.
5. Outside review (D-011) is brought forward: the outside reader is asked to review the D-028 protocol and D-030 before the protocol is deposited.
6. AI reviews are labelled as such and never presented as outside review.

**Reason.** The log shows a rule relaxed after a failure (D-017, D-019); most rulings so far accepted Claude's recommendations; AI readings had no independent check. These steps make the process auditable from outside.

**Alternative rejected.** Rely on the repository history alone (shows what changed, not what was known when).

**Data seen at the time of ruling.** As D-028.

## D-032 — Outside review when v1.0 is complete; full preview site before data requests

**Ruling (2026-10-29, JvH; not delegated).** In his words: "We will delay (at risk) the outside reader - this will happen when v1 is complete. I also want to fully create the site in the absence of data requests, and this way I can forward the site url WITH the request emails so that respondents can see what we are doing."
1. The outside review (D-011) takes place when v1.0 is complete, before it is published. Amends D-028 item 4 (the taxonomy and selection protocol are frozen and deposited on Zenodo without outside review; the timestamp still precedes any new conversion) and D-031 item 5. The D-019 note stands until the review.
2. **Risk accepted.** The protocol and the method rulings are frozen without outside review. A flaw found by the reviewer after conversion is corrected as a logged deviation (TAXONOMY §6.7) and may require the selection to be re-run for the affected cells; the release waits for that.
3. The site is built out on the three existing datasets before the data requests are sent, and its address goes with the requests.

**Implementation (Claude; JvH may overrule).** Until v1.0, extragravitation.org serves the preview, marked on every page as a pre-release preview, not yet reviewed, and excluded from search engines. The pull-request previews remain for review of changes.

**Reason (JvH).** Respondents can see what the data will be used for; the outside reader reviews a complete v1.0 rather than a plan.

**Alternative rejected.** Outside review of the protocol before it is frozen (D-028 as first ruled; slower, and no reader is yet in place).

**Data seen at the time of ruling.** As D-028.

---

## Recorded alongside (not decisions; corrections to the plans)

- X-ray hydrostatic measurements are not "motions": the method field distinguishes kinematic from hydrostatic, and plain-language labels for X-ray points must say gas pressure balance, not motions.
- Lensing g_obs always involves a deprojection; it is recorded as a named assumption for each lensing package.
- Solar System anchors on the map need their own data package with full provenance, or they are omitted from v0.1.
- The mockup's illustrative points are generated from a published fitting function for the radial acceleration relation; that code is not reused, and mockup screenshots are not circulated.
- Schedule: the four-week estimate is replaced by milestones (decisions; repository; data packages passing reproduction tests; site; reviews; release). Estimated 8–12 weeks with one maintainer.
- JvH to register an ORCID before the first Zenodo release.
