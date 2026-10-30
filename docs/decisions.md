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


## D-025 — From velocity dispersion to g_obs

**Ruling (2026-10-29, JvH).** JvH: "Please Rule as A for v1.0, with C held as a labelled overlay to add after v1.0." Not blind: ruled after Claude's weighing of the options (D-031 item 4; the next method ruling is to be made blind). JvH's criteria: "We want usefulness, but can't be seen to be unscientific and we don't want to invite too much scrutiny."
1. **v1.0 uses the half-light-radius estimator** (Wolf et al. 2010, arXiv:0908.2995): M(<r½) = 3 σ²_los r½ / G, so g_obs = 3 σ²_los / r½ at the 3D half-light radius r½; g_bar = G (½ L Υ★) / r½², with gas added where measured (D-034, D-035). One point per system, for globular clusters, dwarf spheroidal and ultra-faint galaxies, and dispersion-supported early-type galaxies where applicable.
2. **Sub-choices.**
   - σ is the source's global or luminosity-weighted line-of-sight dispersion. Where a source gives only a profile and no global value, the system is recorded but not plotted (computing one would be new analysis).
   - r½ is taken from the source; where only the projected half-light radius is given, the conversion is registered as an assumption with its source.
   - Upper limits on σ are plotted as limits.
   - A flag records whether the source states multi-epoch screening for binary stars.
   - Systems the source itself describes as tidally disturbed or out of equilibrium go to the exclusion register with the quotation.
   - Assumptions registered: spherical symmetry, dynamical equilibrium, the estimator, the radius conversion, the stellar mass-to-light ratio (default and range read at source).
3. **After v1.0:** sources' own published dynamical profiles or masses (Jeans or N-body fits) are added as a labelled overlay, with `model_dependence`, never in the default view, under rules ruled then.
4. **Never:** Jeans modelling run by the Atlas itself.

**Reason.** The estimator is the standard published method, chosen by its authors for its insensitivity to velocity anisotropy at r½; it covers nearly every known system, including those with only a global dispersion or an upper limit, with the fewest added assumptions, and the Atlas performs no modelling. Atlas-run Jeans modelling would break "describe, never analyse" and depend on the anisotropy assumption; sources' fitted profiles are heterogeneous and often assume a halo shape, so they are deferred to a labelled overlay.

**Alternatives rejected.** Atlas-run Jeans modelling (B); sources' results only (C alone); both at once for v1.0 (D, deferred in two stages instead); dispersions only, with no g_obs (E: omits the lowest-acceleration systems and the controls).

**Data seen at the time of ruling.** As D-035; the A0, A3 and A5 searches had started (metadata only); no candidate dataset examined for results or plotted.

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
4. ~~For at least one in three method decisions, JvH rules before seeing Claude's recommendation; the log records which.~~ Replaced by D-040 (2026-10-29): every decision records who proposed it and, for proposals not his own, whether JvH adopted, amended or overruled them.
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

## D-033 — Scope in cosmic time; systematics checks; plot builder deferred

**Ruling (2026-10-29, JvH; on Claude's recommendation, not delegated).** JvH: "record D-033 as recommended and run the high-redshift source survey."
1. **Lenses stay framings of the comparison** (D-030). Redshift is a property of a system, not a lens.
2. **Redshift or distance in the record.** Data standard 2.0 requires, for every system, the redshift or distance as the source gives it (with its method), and for every stacked bin the lenses' redshift distribution or range as released.
3. **Coverage report.** The coverage report on continuous axes (TAXONOMY §5b) includes distance or redshift, and states plainly that the current data describe the nearby universe.
4. **Systematics checks.** The map can colour every measurement by a property its source gives (inclination, distance method, the source's quality flag, distance, redshift). If the comparison were affected by the property, colours would separate at fixed g_bar. No fit is made and no pass or fail is claimed; measurements without the property are shown faint and counted.
5. **Cosmic epoch is a documented gap for v1.0.** High-redshift sources (z ≳ 0.3) are surveyed under the same protocol; the cell is declared a gap for v1.0 with the reason, and filled after v1.0 if eligible data exist.
6. **The general plot builder** (any source property against any other) is deferred until after v1.0 and, when built, lives in the exploration layer.

**Reason.** Honest scope (the Atlas is local) and visible systematics checks are cheap and are what a referee looks for first; evolution with cosmic time is scientifically valuable but expensive to fill, because high-redshift baryon inventories often rely on scaling relations; a general builder invites patterns found by chance.

**Alternatives rejected.** Redshift as a lens (wrong category; with current data it would read as "no evolution" when there is no reach in time); filling the high-redshift cell before v1.0 (likely months of delay).

**Data seen at the time of ruling.** As D-028, plus the distance and redshift ranges of the three packages.

## D-034 — Measured, modelled, absent: what each baryon status means

**Ruling (2026-10-29, JvH; on Claude's recommendation, not delegated).** JvH: "agreed". Clarifies D-029 and the status columns of the data standard.
- **Measured:** the component's distribution is observed in that system: starlight, the 21 cm line, CO or [CI] line emission, X-ray emission. The conversion from what is observed to mass is a registered assumption, adjustable where a published range exists: stellar mass-to-light ratio, the CO-to-molecular-gas conversion factor α_CO or the [CI] abundance, the helium factor, and line ratios when a higher CO transition is observed.
- **Modelled:** the component is not observed in that system and is inferred from other properties: scaling relations (e.g. gas fraction against stellar mass), fractions taken from simulations, or an assumed profile shape (e.g. X-COP's modelled stars, D-022).
- **Absent:** not included in g_bar.
Defaults and ranges for any conversion factor are read at source before a package uses them.

**Reason.** Treating line-derived gas as modelled while starlight with an assumed mass-to-light ratio counts as measured would be inconsistent and would penalise some kinds of galaxy over others. Registering the conversion factor with its published range lets readers see how much a result depends on it.

**Alternative rejected.** Count any component that needs an assumed conversion factor as modelled (inconsistent with stars; would mark almost every gas and stellar component as modelled).

**Data seen at the time of ruling.** As D-033, plus the high-redshift survey (`docs/sources/survey-highz-2026-10-29.md`) and Umetsu et al. 2016 read at source (per-cluster binned convergence profiles shown in figures only; no data release stated).

## D-035 — Flexible inclusion with evidence tiers

**Ruling (2026-10-29).** JvH agreed to (a), (b), (d) and (e) as recommended, and delegated (c): "rule on c as to be the most flexible while being scientifically rigorous." His concern: "our criteria might be so restrictive that we'll have trouble finding enough data."
- (a) **No minimum number of systems** for a cell; N is shown with every dataset.
- (b) **Tables printed in papers are eligible** (tier 2), transcribed twice independently and reconciled.
- (c) **Digitised figures are eligible** (tier 3) in any cell where no tier 1 or 2 data exist for the same systems: data points and error bars only; figure hashed with its calibration points; two independent digitisations, their difference added to the uncertainty; authors asked for tables in the next batch, and tier 3 replaced by a new version when they arrive; never in default views, never the sole evidence for a pattern, never scored in a frozen test unless the test says so in advance. Supersedes the earlier practice of not digitising.
- (d) **A baryon component may be absent** only where the source states it is negligible (quoted) or gives a measured upper limit.
- (e) **Every measurement carries an evidence tier** (data standard 2.0).

**Reason.** Excluding by format rather than by quality would leave cells empty that published numbers can fill; labelled tiers keep the strength of each measurement visible, and fixing the tier rules before the search keeps flexibility from following the data. Omitting a present component is excluded because it biases the comparison in one direction.

**Alternatives rejected.** Keep minimum N and machine-readable-only (thin coverage for format reasons); allow digitisation without tiers or replacement (blurs evidence strength); allow digitising only for case studies after an unanswered request (requests are on hold, so it would block cells indefinitely).

**Data seen at the time of ruling.** As D-034; no candidate dataset examined or plotted.

## D-036 — Globular clusters: profiles, apertures and the coverage rule; protocol clarifications

**Ruling (2026-10-29, JvH).** JvH: "1: (ii) + (iii) labelled + (i) otherwise, with the coverage threshold (I suggest 80%); 2: yes. 3: proceed as recommended." Not blind: ruled after Claude's analysis (D-031 item 4 is so far unmet; the stellar mass-to-light ruling is to be made blind).
1. **σ for the D-025 estimator**, in order:
   - **(ii) Registered conversion** where a source gives a line-of-sight dispersion profile: ⟨σ²_los⟩ = Σ wᵢ σᵢ², with weights wᵢ the light in each radial bin from the source's own surface-brightness profile or its cited structural model; errors propagated; only line-of-sight profiles. **Coverage rule:** the binned profile must span radii containing at least **80 %** of the system's light; the covered fraction is recorded and shown; below 80 % the system is recorded but not plotted. The code is written and tested on synthetic profiles, and the test is frozen, before any real profile is opened.
   - **(iii)** Where a source gives only a central or aperture dispersion: the source's own correction to a global value, or a cited published correction, never one derived by the Atlas; labelled `model_dependence = observable_form`.
   - **(i)** Otherwise the system is recorded, not plotted.
2. **ADS and VizieR** steps of the search (protocol §3) are run through the browser on JvH's computer; deviation #2 is remedied when their results are in the logs.
3. **Clarifications to the frozen protocol** (deviations register #3 to #9), all decided before any candidate data were opened:
   - stellar mass counted from stars is measured (D-034);
   - absent gas: system-specific upper limits where they exist, otherwise a cited, quoted statement for the kind, each system marked "absent (literature limit for this kind)";
   - original datasets are preferred over compilations that repeat them; the compilation fills only systems the originals lack, and both stay in the record;
   - no input on either side may be derived from the system's own kinematics or acceleration (e.g. a distance from the dispersions);
   - dwarf galaxy or star cluster: the source's label where sources agree; where they disagree or the label rests on dynamics, "ambiguous: dwarf galaxy or star cluster"; size, luminosity and metallicity spread are continuous properties, never the classifier;
   - proper-motion-only dispersions are recorded, not plotted, in v1.0;
   - Solar System: default bounds are those printed as accelerations with a stated confidence level, shown as published (a value with errors shown as an interval), with GM☉ and distances from cited sources; lunar laser ranging is recorded for a possible separate system.

**Reason.** Recording only would leave the control (globular clusters) with one to three Milky Way systems, an omission that reads as selection; the weighted average is a fixed reduction of published numbers with no free parameters, of the same kind as g = V²/r; aperture corrections are model-dependent but labelled under D-029, as for X-COP. The clarifications close circular routes and keep labels from carrying the result.

**Alternatives rejected.** Record only (i) as the rule; aperture corrections derived by the Atlas; metallicity spread as a classifier (it is used in the literature as a proxy for the depth of the potential).

**Data seen at the time of ruling.** The A0, A3 and A5 search logs (metadata, documentation and methods sections); no profile, dispersion table or result opened or plotted.

---

## D-037 — Published dispersions with a reproduction check; who belongs in the globular-cluster cell

**Ruling (2026-10-29, JvH).** JvH: "1. Merge PRs #37 and #38. 2. Show the published dispersions. Also run a frozen recomputation from the velocities as a reproduction check … It is never plotted in place of the published value. 3. Old globular clusters go in, wherever they are … Young massive clusters stay out of v1.0 … Ultra-compact dwarfs go in the unusual-configurations cell (A7), labelled 'ambiguous: dwarf galaxy or star cluster' … and stay out of both default cells." Not blind: ruled after Claude's options and recommendation, which JvH adopted. JvH's reason (item 3): "classifying by age and structure doesn't use the dynamics. Mixing in the ultra-compact dwarfs would let a disputed label shape the globular-cluster picture."
1. **Dispersions from individual velocities** (A3, A5, and any cell where a source releases per-star velocities and its own dispersion):
   - the **published dispersion** is the value shown, with the source's membership and binary treatment recorded;
   - the released velocities are kept in the record as observables;
   - the Atlas runs a **reproduction check**: a recomputation of the dispersion from the released velocities, with the source's own membership, by a method written and frozen by hash before any velocity file is opened, and a pass/fail tolerance frozen with it. The result (pass or fail, with the numbers) is published for every system, whichever way it goes;
   - the recomputed value is never plotted in place of, or beside, the published value in default views.
2. **Globular-cluster cell (A3):**
   - old globular clusters are included wherever they are (Milky Way, Magellanic Clouds, dwarf galaxies, M31, more distant hosts); the host galaxy is recorded as a property and is never used as a filter;
   - young massive clusters are outside v1.0 and kept as leads for a later cell;
   - ultra-compact dwarfs go in A7 (unusual configurations), labelled "ambiguous: dwarf galaxy or star cluster" (D-036 clarification on kinds), and stay out of the A3 and A5 default views.

**Reason.** Computing dispersions would put the Atlas's own membership, binary and outlier choices on top of the result, which matter most for the faintest systems; showing only published values and checking them is reproducible and keeps the sources' numbers as the result. Classifying clusters by age and structure does not use the dynamics.

**Alternatives rejected.** Published dispersions only, without a check; Atlas-derived dispersions shown as Atlas values; ultra-compact dwarfs in A3 or A5.

**Data seen at the time of ruling.** The A0, A3 and A5 search logs, including the ADS and VizieR (via ADS) addenda: titles and listing metadata, methods sections from the first run; no velocity file, dispersion table or result opened or plotted.

---

## D-038 — When a dispersion is plotted, which number counts, precedence, boundary objects

**Ruling (2026-10-29, JvH).** JvH ruled on the fourteen questions raised by the full-text screening of the A0, A3 and A5 candidates, adopting Claude's recommendations as worded in his message of 13:56 MDT (quoted in substance below). Not blind: ruled after Claude's options and recommendations (D-031 item 4 still unmet; the stellar mass-to-light ruling is to be made blind). JvH's reasons are those he quoted with each ruling.

**1. When a dispersion is plotted**
- **1A. Whole-sample dispersion.** Plotted only if the member stars reach beyond the half-light radius, as the source states it. Otherwise it is treated as an aperture value (needs the source's own or a cited correction, otherwise recorded only). The star-count weighting is registered as a named assumption ("member-sample σ taken as representative of the light-weighted σ"), shown on every point that uses it.
- **1B. Aperture values corrected only to a central value.** Recorded, not plotted, unless the source or a cited paper gives the whole-system value. Earlier extragalactic sets (M31, NGC 5128 and others screened E) are re-checked the same way.

**2. Which number counts**
- **2A.** Where a source gives both, the second moment (including rotation) is used; the dispersion about rotation is recorded. Reason (JvH): "The estimator measures how much motion holds the system up, and rotation is part of that."
- **2B.** Multi-population fits: the single whole-sample value is used; components are recorded. Reason: "Splitting into components adds a model choice on top of the data."
- **2C.** Later re-analyses adding a binary-star correction to someone else's data: recorded as alternatives, never the default. Reason: "They add no new measurements, and the original stays the record."
- **2D.** Fitted dispersion profiles: used under the profile rule (D-036 ii) only where no binned profile is tabulated; labelled as fitted forms (`model_dependence = observable_form`); the 80% light coverage is judged from where the data reach, never from where the fit extends.

**3. Several measurements of one system**
- **3A.** Original papers are the default. Geha et al. (2026, Keck/DEIMOS Stellar Archive) is a labelled alternative, and the default only for systems it alone covers. A consistency check between the originals and Geha is written and frozen before either set of values is opened; its result is published whichever way it goes. Reasons (JvH): D-036 already prefers originals; switching to whichever dataset turned out bigger, mid-search, is an after-the-fact change.
- **3B.** Among several originals for one system: first the paper that releases its per-star velocities; then the one with the most member stars; then the most recent. All are kept and shown.

**4. Boundary objects**
- **4A.** Objects whose classification the sources dispute (Crater/Laevens I, UMa3/U1, Tucana III, G1 and others like them) go to A7, labelled "ambiguous: dwarf galaxy or star cluster", consistent with D-037; they stay out of the A3 and A5 default views.
- **4B.** M54 is a globular cluster (A3). The Sagittarius nucleus's own stars count as part of the Sagittarius dwarf galaxy (A5). Membership rests on a metallicity cut, noted on both pages.
- **4C.** VV124 goes to A5 with its measured gas in the baryonic side; its "transition" label is shown as a property.
- **4D.** AIMSS compact stellar systems: the source's own label where it gives one; otherwise A7, labelled ambiguous. The Atlas never assigns a type from size or dynamics.

**5. Small calls**
- **5A.** A dispersion given only in a paper's running text is tier 2, flagged "text", transcribed twice.
- **5B.** Bounds on a single distant body (Planet Nine-type) are recorded in A0 as a separate "localised extra mass" sub-row, never a default: their implied pull is directional and tidal, not a uniform outward pull.
- **5C.** A bound from a single asteroid's orbit (Icarus) is recorded, never a default, consistent with R3.

**Addendum (2026-10-29 14:06 MDT, JvH: "apply the rule 2A by analogy").** Where a source gives a dispersion both with and without a fitted velocity gradient (first case: Antlia 2, Ji et al. 2021), the value without the gradient model is used and the gradient-removed value is recorded, by analogy with 2A. Not blind; data seen: search-log metadata and methods only.

**Alternatives rejected.** 1A: plot every whole-sample value; apply the 80% light test (sources rarely state member positions). 1B: Atlas conversion of central to global with a model. 3A: the re-reduction as default everywhere. 4A: placing disputed objects in A3 or A5.

**Data seen at the time of ruling.** The A0, A3 and A5 search logs including §6 (ADS titles and listing metadata) and §7 (full-text screening: abstracts, methods, data statements, table headings); no dispersion, velocity, mass, mass-to-light value or result opened or plotted.

---

## Note on D-028 — Protocol deposited on Zenodo

**2026-10-29, deposited by JvH.** The frozen selection protocol, taxonomy and freeze record are deposited on Zenodo as "Atlas of Extra Gravitation: v1.0 taxonomy and selection protocol (frozen 2026-10-29)", DOI [10.5281/zenodo.23780203](https://doi.org/10.5281/zenodo.23780203) (concept DOI 10.5281/zenodo.23780202), CC BY 4.0, open access. Claude checked the MD5 checksums Zenodo shows for all four files against the repository copies: all match, so the deposited protocol files are byte-identical to the frozen versions (SHA-256 in `data/taxonomy.json`). This meets TAXONOMY §6.8: the outside timestamp exists before the first new conversion.

---

## D-039 — Stellar mass-to-light ratio for star clusters and dwarf galaxies

**Ruling (2026-10-29 16:14 MDT, JvH).** Adopted Claude's recommendations on the four choices (protocol §5; issue #45). **Not blind:** JvH asked for the analysis and recommendations before ruling, so D-031 item 4 (at least one method ruling in three made blind) remains unmet; JvH confirmed (2026-10-29 16:18 MDT) that D-031 stays as written and that the lensing-projection ruling (protocol §5; issue #13) is the next blind ruling: Claude presents the options and evidence without a recommendation, and JvH rules before seeing one. JvH's reasons are those stated with each ruling, resting on the charter: assumptions shown with published ranges and effects computed from the data; observations first; continuous properties stay continuous; symmetry; the control shown as firmly as honest.

1. **Default value per system.** One model family: Bruzual & Charlot (2003) with the Chabrier (2003) IMF, as used by McLaughlin & van der Marel (2005) for clusters and Woo, Courteau & Dekel (2008) for dwarfs.
   - Milky Way and Magellanic globular clusters: the per-cluster values tabulated by McLaughlin & van der Marel (2005, Table 8); the Atlas computes nothing.
   - Other old systems: interpolation of the published model tables by metallicity (old age, unless the source gives another), with code frozen before use.
   - Dwarf galaxies with a cited star-formation-history value: that value, labelled.
   - Sources' own stellar-population values: recorded as alternatives, not the default.
   - A single fixed value for all systems was rejected: the ratio depends on metallicity and age, which correlate with kind and size, so a fixed value would build a trend along a continuous property into the comparison.
2. **IMF default:** Chabrier/Kroupa. Before the assumption is frozen, the direct evidence on the low-mass IMF in old clusters and dwarfs (for example counted mass functions) is read at source and recorded; if it contradicts this default, it returns to JvH.
3. **Range (slider):**
   - star clusters: from about 0.5× the model value (loss of low-mass stars through dissolution; Kruijssen & Mieske 2009, range 0.53–1.00) up to the Salpeter value (60–75% above Chabrier, McLaughlin & van der Marel 2005; about 1.5×, Maraston 2005); asymmetric, shown as such. The dissolution correction is a range bound only, never a per-cluster default (it would need masses that may be dynamical; D-036 #6);
   - dwarf galaxies: model, age and metallicity spread plus the IMF span, plus the published spread between star-formation-history and colour-based values (Woo et al. 2008); no dissolution term.
4. **Counted stellar mass** (star counts, D-036 #3): the ratio route is the default for every system; counted masses are shown as alternatives wherever the source shows they do not depend on the cluster's motions (verified per source before use). A cross-check (do counted masses fall inside the ratio's range?) is written and frozen before either is compared, and its result is published whichever way it goes.

**Alternatives rejected.** A fixed value for all; sources' own values as default; Salpeter default; a range without the IMF; counted mass as default (possible dependence on the motions, and mixing two routes by which clusters happen to be nearby).

**Data seen at the time of ruling.** The model sources' descriptions and stated ranges (McLaughlin & van der Marel 2005 §3; Maraston 2005; Kruijssen & Mieske 2009 Table 1 and Eq. 5, canonical model values only; Woo et al. 2008 §2.1 and Tables 1–2; Pace 2025 on its mass-to-light ratio). No dynamical mass or dynamical mass-to-light value was shown to JvH. Claude saw some dynamical values in passing in older abstracts during screening (search logs §8a); none was used or recorded.

**Item 2 confirmed (2026-10-29 16:19 MDT, JvH: "keep").** After the low-mass IMF evidence was read (`docs/sources/stellar-ml-2026-10-29.md`): the dwarf-galaxy evidence is consistent with the default; the cluster evidence for fewer low-mass stars rests partly on fits to the motions and its direction lies inside the ruled range. The Chabrier/Kroupa default stands; the evidence is recorded in the assumption's registry entry. Baumgardt et al. (2023) global masses depend on the motions and are not used as the counted-mass alternative.

**To read before freezing:** the Bruzual & Charlot (2003) model tables; the direct low-mass IMF evidence; the Baumgardt et al. star-count method (independence from the motions).

---

## D-040 — Who proposed each ruling, instead of blind rulings (amends D-031 item 4)

**Ruling (2026-10-29 16:29 MDT, JvH; on Claude's recommendation).** JvH: "go for b." Replaces D-031 item 4 ("for at least one in three method decisions, JvH rules before seeing Claude's recommendation").
1. **Dropped:** the requirement that some method rulings be made before JvH sees Claude's recommendation. D-039's designation of the lensing-projection ruling as blind is withdrawn.
2. **Recorded for every decision from D-040 on,** in addition to D-031 item 1 (options, data seen at ruling, delegation, JvH's reason): **who proposed** the ruling (JvH, Claude or another named party) and, where the proposal was not JvH's own, **whether JvH adopted it unchanged, amended it or overruled it**, with what he changed. Earlier entries already show this in their ruling line and are not rewritten.
3. The project description's line "Claude proposes, builds and checks; JvH rules, sometimes before seeing Claude's recommendation" becomes "JvH and Claude both propose; Claude builds and checks; JvH rules, and the record shows who proposed what and what was changed." (Wording corrected by JvH, 16:33 MDT: "JvH can propose too.")
4. The frozen selection protocol (§5) still mentions D-031 item 4; it is not edited, and the change is recorded in the deviations register (#17).

**Reason (JvH's question, Claude's analysis).** Asking a collaborator for an opinion before deciding is normal practice; blind rulings are not a standard requirement of science and were added here as an extra safeguard against the perception that the methods were chosen by the AI. Their cost is that JvH would rule on technical questions without the analysis he wants, which can make rulings worse rather than more independent. The checkable protections are already in place: pre-registration with outside timestamps, the decision record (data seen, delegation, reasons, and now who proposed and what changed), disclosure of AI assistance, the outside review before v1.0, and results published whichever way they go.

**Alternatives rejected.** Keep D-031 item 4 (a); one symbolic blind ruling, then drop it (c); a sealed-recommendation procedure (judged overkill by JvH).

**Data seen at the time of ruling.** None relevant (a process decision).

**Proposed by** Claude; **adopted unchanged.**

---

## D-041 — Data standard 2.0.0 frozen

**Ruling (2026-10-29 17:08 MDT, JvH).** "approve 2.0.0, merge 54." **Proposed by** Claude (PR #54); **adopted unchanged.**
- `docs/data-standard.md` version 2.0.0 is frozen (`data/frozen/data-standard-2.0.0.json`). The validator that implements it is not frozen, so bugs can be fixed through tested pull requests; it must keep implementing the frozen text. Version 1.3.0 is kept unchanged in `docs/data-standard-1.3.0.md`; the three 1.x packages stay valid under it and are re-issued under 2.0 after v1.0 (D-029).
- Content: D-029's specification (observables first, selection, baryon inventory, precedence) with the rulings since: D-033 (distance or redshift required), D-034 (statuses), D-035 (evidence tiers), D-036 (light weighting, coverage, aperture corrections, no kinematic inputs, kinds), D-037 (published values; reproduction check; host), D-038 (plotting rules, which number counts, defaults and alternatives, boundary objects in A7), D-039 (stellar mass-to-light registry fields).

**Reason.** Every v1.0 package must be built to one fixed format, written before any of them is converted.

**Alternatives rejected.** Building the first packages before freezing the standard (the format would follow the data).

**Data seen at the time of ruling.** The standard text and validator tests (synthetic); no new data.

---

## D-042 — Globular clusters: the Baumgardt database, precedence after the plotting rules, distances

**Ruling (2026-10-29 18:52–18:53 MDT, JvH).** **Proposed by** Claude; **adopted unchanged** on all three questions.
1. **The Baumgardt Galactic Globular Cluster Database** (v4, 2023; Baumgardt & Hilker 2018 and later) pools stellar velocities from many teams with its own, applies its own membership and binary rules, and computes profiles. It is treated as a **re-analysis**, like Geha et al. 2026 (D-038 3A): an alternative to the original papers, and the default only for clusters it alone covers.
2. **Plotting rules first, then precedence.** For each system, the plotting rules (D-036 ii coverage ≥ 80%, D-036 iii, D-038 1A and 1B, D-035 tiers, D-036 #6) are applied to every candidate value first; the default is then chosen by precedence (D-038 3A, 3B; item 1 above) among the values that pass. A value that fails a plotting rule is recorded, never the default, and never hides a value that passes. Applies to every kind.
3. **Distances for Milky Way globular clusters:** Harris (1996, 2010 edition) horizontal-branch distances are the default. Distances derived from a cluster's own motions are never used (D-036 #6). Baumgardt & Vasiliev (2021) distances are shown as a cross-check only, and only with any motion-based method removed if their table lists methods separately.

**Reason.** Treating every pooled re-analysis the same way keeps one rule; choosing the default only among values that pass the plotting rules prevents a valid measurement from being hidden because a higher-ranked one covers too little of the system, which would read as selection; horizontal-branch distances come from starlight only. Ruled before any profile, coverage value or distance table was opened. Claude stated in advance that, with items 1 and 2 together, the Baumgardt profiles will probably supply most plotted Milky Way clusters.

**Alternatives rejected.** Item 1: Baumgardt as an original (it would be the default almost everywhere by D-038 3B) or as a compilation under D-036 #5. Item 2: precedence first, then plotting rules. Item 3: Baumgardt & Vasiliev (2021) averages as default (they include motion-based distances).

**Data seen at the time of ruling.** The A3 search log (metadata and methods), the Baumgardt database index page (list of files and terms only); no profile, coverage value or distance opened.

---

## D-043 — One point per system on the map

**Ruling (2026-10-29 20:55 MDT, JvH).** "Yes I like your recommendations for the build." **Proposed by** Claude; **adopted unchanged**, with the light-radius multiple (2 × the source's half-light radius) proposed by Claude in the build and confirmed by JvH before merge (21:02 MDT: "Do twice the half light").
1. The map gains a reader's choice of points: **every measurement** (the default view, unchanged under D-012 and D-027), **one per system at the outermost measured radius**, or **one per system at a radius set by the light** (the first measured radius at or beyond 2 × the source's effective radius).
2. Each point is an existing packaged measurement chosen by the rule; nothing is interpolated, extrapolated or recomputed. Values are labelled as within a radius, never as totals.
3. Systems whose data do not reach the light-defined radius, or whose source gives no half-light radius (the X-COP clusters, whose usual size R500 is defined from total mass and is not used), are left out and counted on the page.
4. Stacked lensing bins are averages over many galaxies, not systems, and are unchanged.
5. A systematics colour, "outermost measured radius", lets readers check whether survey depth shapes the one-per-system picture (D-033).

**Reason.** The full map has many points per system and is hard to read; a one-per-system view is simpler, but a total mass cannot be measured, so the honest form picks a measured point by a declared rule. Outermost radius uses everything measured; the light-defined radius makes systems comparable and is independent of survey depth; showing both, with the depth check, keeps either from carrying the result.

**Alternatives rejected.** Extrapolated total masses; R500 for clusters (defined from the observed side); replacing the default view.

**Data seen at the time of ruling.** The published map of the three v1 packages.

---

## Recorded alongside (not decisions; corrections to the plans)

- X-ray hydrostatic measurements are not "motions": the method field distinguishes kinematic from hydrostatic, and plain-language labels for X-ray points must say gas pressure balance, not motions.
- Lensing g_obs always involves a deprojection; it is recorded as a named assumption for each lensing package.
- Solar System anchors on the map need their own data package with full provenance, or they are omitted from v0.1.
- The mockup's illustrative points are generated from a published fitting function for the radial acceleration relation; that code is not reused, and mockup screenshots are not circulated.
- Schedule: the four-week estimate is replaced by milestones (decisions; repository; data packages passing reproduction tests; site; reviews; release). Estimated 8–12 weeks with one maintainer.
- JvH to register an ORCID before the first Zenodo release.

---

## D-044 — Map windows set by the data; per-point error bars by default

**Ruling (2026-10-30, JvH).** "Yes, please fix the issues" (audit issue #61). **Proposed by** Claude; **adopted unchanged**.
1. **No hidden points.** Each lens's default window is widened from its fixed frame to the full extent of the packaged data (padding 0.15 dex, rounded to 0.5 dex). If a point still falls outside the window (zoomed or not), it is never silently dropped: unzoomed, it is drawn as a small diamond on the frame edge; zoomed, the page states how many measurements lie outside the window. Lenses with equal axes keep equal spans when zoomed.
2. **Error bars say what they are.** Only g_obs error bars are drawn, and the control says so ("Error bars on g_obs"). The default is **per point**: for SPARC rotation curves, the velocity uncertainty only (2 e_V / V), because distance and inclination errors move a whole galaxy together and are not independent per point. A **Full** switch shows the packaged total (velocity, distance, inclination). Other datasets show their packaged errors in both settings.
3. Error bars whose lower end reaches zero or below are drawn open-ended (an arrowhead) and counted on the page, never clipped silently.

**Reason.** The audit found 26 measurements (17 SPARC points with ratio 0.07–0.30; 9 KiDS bins with ratio 103–307) outside the fixed windows and therefore invisible, which lets the frame carry the result; and full per-point error bars double-count distance and inclination, which are correlated within a galaxy. Showing everything, and labelling what the bars include, follows the standards that labels never carry the result and that uncertainties are shown openly.

**Data seen at the time of ruling.** The packaged SPARC, KiDS-1000 and X-COP v1 tables as plotted on the map (already public); the audit counts above. No new data.

---

## D-045 — Globular clusters: bins, light model, radius, luminosity and the reproduction check for the Baumgardt profiles

**Ruling (2026-10-30 10:03 MDT, JvH).** "do 1-5 as recommended." **Proposed by** Claude; **adopted unchanged**.
1. **Bins.** Proper-motion bins are recorded, not plotted (D-036 #8). Each line-of-sight dataset within a Baumgardt profile is a separate candidate value, converted on its own (bin edges inferred from the mean radii, flagged `edges_inferred`). The plotting rules are applied first, then precedence (D-042). Datasets are never merged.
2. **Light model.** The D-036 (ii) conversion gains King (1966) as version 2 (`aeg.king66`), written, tested and frozen before use. Parameters come from McLaughlin & van der Marel (2005), King fit; otherwise from Harris (2010) c and r_c, read as log₁₀(r_t/r₀) and r₀. That reading is a registered assumption, decided by a pre-registered test in the package's REPRODUCTION.md.
3. **Half-light radius.** McLaughlin & van der Marel's projected half-light radius from the same King fit, rescaled to the Harris distance; otherwise Harris r_h. r½ = 4/3 R_h (D-025). Harris r_h is shown as a cross-check.
4. **Luminosity.** Harris integrated V with the Harris distance (consistent with D-042); McLaughlin & van der Marel's model luminosity as a cross-check.
5. **Reproduction check (D-037) without published bin edges.** Bins are rebuilt as consecutive groups of the published star counts, in order of radius. Members have RV membership probability > 0.5; stars with single-star probability < 0.5 are excluded. The rule is frozen (`aeg.repro_bins`) and every result is labelled "reconstructed binning".

**Reason.** These were Claude's reasons, adopted by JvH.
- Datasets in one profile can overlap, and merging them would be an Atlas analysis choice.
- King (1966) is the model both structural sources fit. Without it, the conversion would substitute a model family neither source used.
- Taking the radius and the light model from the same fit keeps the weights and r½ consistent.
- Harris distances and magnitudes keep one distance scale (D-042).
- Rebuilding bins by a frozen rule tests something real. Marking every system "not testable" would be honest, but it would test nothing; the label says where a fail may come from.

**Alternatives rejected.**
- Merged or first-listed datasets (1).
- King 1962 with Harris parameters, or Plummer with the Baumgardt radius, which rests on fits that use the motions (2).
- Harris r_h as default (3).
- McLaughlin & van der Marel luminosity as default (4).
- All systems not testable (5).

**Data seen at the time of ruling.**
- Column definitions and documentation of the Baumgardt pages, RV files, Harris (2010) and McLaughlin & van der Marel (2005).
- The values disclosed in deviation #19: part of one RV-file row (no velocity), six rows of McLaughlin & van der Marel Table 13, and ten rows of Harris Part II.
- No dispersion profile or structural value.

---

## D-046 — Globular-cluster package proceeds after reproduction test 2 failed (after-result decision)

**Ruling (2026-10-30 10:25 MDT, JvH).** "Go for B." **Proposed by** Claude (option B of three); **adopted unchanged**. **This decision was made after a frozen test result was known** (D-031 item 2). It therefore goes to the outside reader at the v1.0 review (D-032). If the reader does not confirm it in writing, `aeg-d-gc-baumgardt` stays out of v1.0.
1. Reproduction test 2 of `aeg-d-gc-baumgardt/v1` stays recorded as **FAIL** (152 of 153 King fits reproduced; `REPRODUCTION_RESULT.md`). It is shown on the dataset page and never re-scored.
2. Despite REPRODUCTION.md's clause that a failed test stops the package, the conversion and tests 1, 3 and 4 and the D-037 check run as frozen. Each is published whichever way it goes, and any further fail stops the package.
3. MW-PAL1 is recorded, not plotted. The reason given is: "source structural parameters internally inconsistent (scale radius in pc vs angular radius × distance; reproduction test 2)". Its parameters are not repaired, and Harris is not substituted.

**Reason.** These were Claude's reasons, adopted by JvH.
- The test did its job: it confirmed the King (1966) code on 152 fits to a median of 0.0006 dex. It found a defect in one row of the source table, which is documented.
- The cause is independent of any acceleration: none had been computed.
- Pal 1 could not be plotted in any case, since its profile has one bin.
- Holding the whole control cell until the outside review would delay a v1.0 gate item by months and change no plotted value.

**Alternatives rejected.**
- (A) Hold the package until the outside review. This was the strictest option, and was rejected for its cost.
- (C) Re-run test 2 with the angular radius. This would be re-scoring after the result, which is forbidden.

**Data seen at the time of ruling.**
- The structural tables of McLaughlin & van der Marel (2005), as test 2 read them, and test 2's per-row results.
- The Baumgardt profile rows for Pal 1 (one bin).
- The values disclosed in deviation #19.
- No converted dispersion, g_obs or g_bar.

**For the outside reader (v1.0 review):** confirm or reverse D-046.

---

## D-047 — Harris-only globular clusters stay recorded only

**Ruling (2026-10-30 10:48 MDT, JvH).** "Ruling: keep recorded only." **Proposed by** Claude (option A of two); **adopted unchanged**. Ruled after reproduction test 4's result and before any g_obs or g_bar of the package was looked at.

The 36 clusters whose structural model would come only from Harris (2010) are recorded, not plotted, in `aeg-d-gc-baumgardt/v1`, as test 4 pre-registered. They may return in a later version under a reading frozen before use, or through packages of the original papers.

**Reason.** This was Claude's reason, adopted by JvH. Test 4 showed that Harris r_c is the half-power radius, while Harris c behaves as log(r_t/r₀) (median difference 0.000 against McLaughlin & van der Marel) despite the catalogue key defining c = log(r_t/r_c). Any new reading would be built after the result, on an internally ambiguous source.

**Alternative rejected.** (B) Read r_c as the half-power radius and c as log(r_t/r₀) now. That would be a rule changed after a test result (D-031 item 2) and would rest on a guess about which definition is the misprint.

**Data seen at the time of ruling.**
- Test 4's per-cluster comparison (`checks/test4_harris_rc.csv`).
- The conversion counts.
- The D-037 check results.
- No g_obs or g_bar.

---

## D-048 — Dwarf galaxies (A5): LVDB as an index, the half-light radius, and kinds whose label rests on dynamics

**Ruling (2026-10-30 12:23 MDT, JvH).** "As recommended." **Proposed by** Claude; **adopted unchanged**. Ruled before any LVDB value was opened: column headers and documentation only.
1. **The Local Volume Database (Pace 2025; v1.1.1, CC0) is an index; the originals are the record.** Each default value is the original paper's published value, located through LVDB's reference column. An independent agent reads every value at source in the original and records:
   - the value with its quote and location;
   - whether the members reach beyond the half-light radius as the source states it (D-038 1A);
   - the binary treatment.

   Disagreements with LVDB are logged. This applies D-036 #5 (originals before compilations) and D-031 item 3.
2. **Half-light radius:** the azimuthally averaged (circularised) projected half-light radius, consistent with the spherical estimator of D-025. The semi-major value is recorded as a cross-check.
3. **Kinds:** D-036 #7 is applied as written.
   - A system whose galaxy label rests only on its velocity dispersion or its metallicity spread goes to A7, labelled "ambiguous: dwarf galaxy or star cluster".
   - The basis of each label is read in its reference by a rule frozen before any dispersion is opened.
   - A7 gets its own view on the map, so these systems are shown, labelled, and kept out of the A3 and A5 default views.

   **Amends D-028 item 5:** the gate item "the lowest-g_bar individual systems (dwarf spheroidals and ultra-faint dwarfs)" is met when those systems are live in A5, or in the A7 view where their kind is disputed.

**Reason.** These were Claude's reasons, adopted by JvH.
- LVDB carries the originals' numbers, but only the originals state member coverage (1A) and binary treatment.
- The estimator assumes sphericity.
- "Confirmed galaxy based on spectroscopy" often means the dispersion or metallicity spread, which D-036 forbids as a classifier. An A7 view keeps the faintest systems visible without letting dynamics decide their kind.

**Alternatives rejected.**
- (1) LVDB values used directly as a compilation: this skips 1A.
- (2) The semi-major radius as default.
- (3) LVDB's "confirmed galaxy" label accepted for A5: dynamics would decide the kind.

**Data seen at the time of ruling.** LVDB column headers, row counts and documentation (definitions of `confirmed_real` and `confirmed_galaxy`). The A5 search log. No dispersion, structural or luminosity value.
