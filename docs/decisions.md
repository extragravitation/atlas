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

---

## D-049 — Kind-basis rule, version 2 (after-result decision)

**Ruling (2026-10-30 13:35 MDT, JvH).** "Fix D 049 as proposed." **Proposed by** Claude; **adopted unchanged**. **Made after the version 1 coding result was seen, and before any velocity dispersion, structural value or luminosity of an A5 candidate was opened.** It goes to the outside reader at the v1.0 review (D-031 item 2).

`docs/methods/D049_KIND_BASIS_V2.md` replaces version 1. Version 1 stays frozen, and its literal result stays on record (`aeg-d-dwarfs/v1/reading/kinds_v1.csv`).
1. **X narrowed:** only "calls it a star cluster" or "concludes the kind is undetermined". A hedged or provisional galaxy label is coded by its stated grounds.
2. **Supersession:** an X counts unless a later paper in the evidence set gives the kind on light, population or gas grounds. A later settlement by dynamics or metallicity spread leaves the X standing.
3. **Evidence:** pre-arXiv papers are read as ADS scans through JvH's browser. Systems with no discovery reference add their structural reference.
4. **Re-coding:** the sheets are re-coded and the 20% double coding is re-compared. Both agreement rates are published.

**Reason.** These were Claude's reasons, adopted by JvH. Applied literally, version 1 put the classical dwarf spheroidals and the Magellanic Clouds in A7 for two reasons unconnected with their evidence:
- their discovery papers are not on arXiv, and the LMC and SMC have none;
- one 1938 paper's uncertainty counted even though it was settled later.

The coders also disagreed on whether "provisional" means X: 2 of 21 double-coded systems differed for that reason. Version 2 keeps the intended effect: systems whose galaxy label was settled only by dynamics stay in A7.

**Alternative rejected.** Apply the version 1 result as written.

**Data seen at the time of ruling.** The version 1 coding sheets and their result (kinds and reasons); the coders' reports. No dispersion, mass, structural value, luminosity or acceleration of any A5 candidate.

**D-049a (2026-10-30 13:47 MDT, JvH: "D-049a as recommended").** **Proposed by** Claude after JvH asked for a review "as a good scientist"; **adopted unchanged**.
- For systems version 2 places in A7, the evidence set adds the **earliest paper that calls the system a galaxy**, coded by its grounds. This replaces Claude's first proposal, which searched for the earliest paper arguing on light grounds. That proposal was withdrawn as a search for favourable evidence: unequal in effort and not reproducible.
- arXiv-era papers are read by an independent agent and pre-arXiv papers as ADS scans by the main session (disclosed), with a second reader checking a sample of scan readings.
- **The rule is then frozen with no version 3.** Whatever it produces is published with its reasons. Both D-049 and D-049a go to the outside reader.

**Reason (Claude, adopted).**
- The rule's purpose (D-036 #7) is to prevent circular selection by dynamics. The deciding fact is therefore historical: was the system named a galaxy before or without its dynamics?
- Three revisions after seeing outputs risk tuning the list toward expectations. A fixed, reproducible target and a commitment to stop are the safeguards.
- An A7 system is still shown, in its own view.

**Data seen.** The version 1 and version 2 coding results; no dispersion, structural value, luminosity or acceleration.

---

## D-050 — Which copy of a paper is "the original"

**Ruling (2026-10-30 15:28 MDT, JvH).** "Let's go with B." **Proposed by** Claude (option B, recommended); **adopted unchanged**. Made before any value of an A5 candidate was opened. Applies to the second reading of every package converted after this date; the second readings already published are not reopened.

1. **The version of record is read wherever it can be read.** Otherwise the latest arXiv version is read.
2. **Each packaged value records the copy it was read from:** version of record, or arXiv identifier and version.
3. **Where both are readable,** the second reader checks the arXiv value against the version of record. On any difference the version of record wins, and the difference is logged.
4. **Errata:** an erratum is searched for every paper used. An erratum overrides the printed value, and the override is logged.
5. **Papers whose arXiv record shows no sign of acceptance** (no journal-ref and no "accepted" or "published" in the comments) must be read in the version of record.

**Reason (Claude, adopted).**
- D-048 makes the original papers the record but did not say which copy. arXiv versions can differ from the published text, and errata can correct printed numbers.
- The version of record is what is cited, so it should decide.
- Allowing the arXiv version where the version of record cannot be read, labelled per value, keeps the work possible without hiding where a number came from.
- In `aeg-d-dwarfs/v1`, 24 of the 109 arXiv versions show no sign of acceptance, 12 of them dispersion papers. Item 5 covers them.

**Alternatives rejected.**
- (A) Version of record only: some older papers may not be readable by JvH.
- (C) arXiv only: this fails D-048 wherever the versions differ.

**Data seen at the time of ruling.**
- LVDB reference columns and bibliography.
- arXiv abstract pages (versions, journal-ref, comments).
- No value of any A5 candidate.

---

## D-051 — Member coverage from the source's own table (after-result decision)

**Ruling (2026-10-30 16:59 MDT, JvH).** "Proceed with B and its refinements." **Proposed by** Claude after JvH asked "what would a good scientist do?". **Adopted unchanged.**

**Made after seeing results.** Under D-038 1A, with evidence from the papers' prose only, 16 of 103 A5/A7 systems had a plotted default. Claude had seen that count, and dispersion values had appeared in the readers' reports. No value entered the choice. **Goes to the outside reader** at the v1.0 review (D-031 item 2), with D-046, D-049 and D-049a.

Specification: `docs/methods/D051_COVERAGE.md`, frozen with `pipeline/aeg/coverage.py`, `reproduction/coverage_from_tables.py` and `reproduction/apply_sigma_rules_v2.py`.

1. **D-038 1A is unchanged.** Member stars used for the dispersion must reach beyond the half-light radius.
2. **Evidence admitted:** the source's prose (in half-light-radius units), or the source's own per-star member table.
   - Members are those the source states it used for the value.
   - Each member's elliptical radius is computed against the **same R_h the plotted point uses**: the structural original's centre, ellipticity, position angle and semi-major half-light radius.
   - The value passes if at least one member lies beyond the half-light ellipse: 1A's literal threshold.
3. **Published for every system checked:** members, members beyond R_h, the fraction, and the largest r/R_h. These are not a second threshold.
4. **Safeguards.**
   - Specification and code are frozen before any table is opened.
   - Unreachable tables leave the value as "coverage not checkable", never guessed.
   - The prose-only result stays on record and is published beside this one.
5. **Duplicate printings** of a paper's adopted estimate: the table printing, otherwise the most significant digits. A tie, or genuinely different estimates with no stated preference, go to JvH.
6. **Lower limits:** recorded, never plotted.

**Reason (Claude, adopted).**
- 1A exists because g_obs = 3σ²/r½ needs a dispersion that represents the whole system.
- Testing only the prose measures how papers are written, not where their members are. A paper whose released table reaches several R_h failed while a vaguely worded one passed.
- The alternative rejected in D-038 (an 80%-of-light test) was set aside because sources "rarely state member positions". That reason does not apply where the source releases its table.
- Option B keeps the rule's wording and threshold, and admits only the source's own data. It is reproducible and adds no model.
- Judging coverage against the plotted point's own R_h keeps the test consistent with the estimator.

**Alternatives rejected.**
- (A) Prose only: tests writing style, not coverage.
- (C) Read "within N r_h" (N > 1) as "beyond": an outer bound is not evidence that members reach there.
- (D) Relax 1A: this changes a ruled standard after seeing the count.
- A stricter threshold than one member (e.g. a minimum fraction): inventing it after seeing counts would itself be after-result tuning.

**Data seen at the time of ruling.**
- The two codings, the adjudication and the counts from the version 1 rule script: plotted 16, aperture 75, flagged 16, lower limits 3.
- The readers' and coders' reports, which mention some dispersion values.
- No per-star table and no structural value.

---

## D-052 — A5 structure, distance and magnitude: which printed value is used

**Ruling (2026-10-30 18:09 MDT, JvH).** "Rule as recommended." **Proposed by** Claude. **Adopted unchanged.** Made before any structural, distance or magnitude value was looked at by the main session or used. The two independent readings and their adjudication were complete; the values were seen by the readers and adjudicators only.

Specification: `docs/methods/D052_STRUCTURE_SELECTION.md`, frozen with `reproduction/select_structure.py`.

1. **Profile fit.**
   - Use the fit the paper adopts.
   - If it adopts none, take the first printed fit in this fixed order: exponential, Plummer, Sérsic, King.
   - All other fits are recorded and shown.
2. **Half-light radius convention.**
   - Where the paper does not say whether r_h is semi-major or circularised, and it fits ellipticity in the same model, the value is treated as semi-major.
   - This is a named assumption, "r_h convention not stated". Its effect (the circularised reading) is computed from the data and shown on each affected point.
3. **Distance.**
   - Use the paper's adopted value, otherwise the value stated in its abstract.
   - Anything still undecided goes to JvH.
   - D-036 #6 applies: no distance derived from the system's own motions.
4. **Magnitude.**
   - Rebuild the apparent magnitude as m_V,0 = M_V + (m−M)_paper wherever the magnitude paper prints both, then apply the Atlas distance.
   - Otherwise use the paper's M_V, flagged "distance basis of M_V differs".
5. **Duplicate printings** (as D-051): use the table printing, otherwise the one with the most significant digits.

**Reason (Claude, adopted).**
- A fixed order chosen before any value is seen keeps the choice of fit from tracking the result. Exponential comes first because it is the most widely used fit in this literature, which keeps systems comparable.
- Semi-major is the field's standard definition when ellipticity is fitted in the same model. Showing the other reading as a computed effect keeps the assumption visible, not hidden.
- REPRODUCTION.md takes the apparent magnitude as the observable. Rebuilding it from the paper's own modulus keeps L_V consistent with the Atlas distance.

**Alternatives rejected.**
- Averaging the profile fits: this mixes models.
- Treating unstated r_h as circularised: this is against the field's convention.
- Using M_V as printed throughout: this mixes distance bases.

**Data seen at the time of ruling.**
- Main session: the counts and kinds of disagreement between readings, and the quantity names and units present. No structural, distance or magnitude value of an A5 or A7 candidate.
- The readers' and adjudicators' reports mention a few values in passing. None entered the choice.

---

## D-053 — Resolving a compilation entry that lists several originals

**Ruling (2026-10-30 19:36 MDT, JvH).** "I choose A." **Proposed by** Claude as option A, recommended. **Adopted unchanged.** Made before any value in the originals behind McConnachie 2012 was read.

Specification: `docs/methods/D053_COMPILATION_ORIGINALS.md`, frozen with `reproduction/resolve_compilation.py`.

1. **Candidates.** Every original that the compilation lists for the value is a candidate, and each is read by two independent readers.
2. **One printer.** If only one candidate prints the quantity, it is used.
3. **Several printers.** The candidate whose printed value the compilation reproduces is used. This is a mechanical match at the compilation's printed precision, recorded with its location.
4. **No match** (the compilation averaged or converted): the most recent candidate that prints the quantity is used, flagged.
5. **Centres.** These come from the structure original if it prints one, otherwise from the discovery paper, which is the only reference in the compilation's centre table.
6. **Pre-arXiv originals** are read through JvH's browser (D-050).

**Reason (Claude, adopted).**
- D-048 makes the originals the record.
- The value match only identifies which paper a compiled value came from. It never chooses a value for its effect on the result.
- The fallback is fixed in advance.

**Alternatives rejected.**
- (B) Most recent original always: this may silently substitute a different measurement.
- (C) Leave these values undetermined: this loses data that has real originals.

**Data seen at the time of ruling.**
- McConnachie 2012's reference columns, notes and reference list, and the originals' titles and arXiv records.
- No value from the originals.
- Readers had read McConnachie 2012's own values in the earlier readings (structure, magnitude and dispersion sheets). The main session has not.

---

## D-054 — Centre used for the coverage check

**Ruling (2026-10-31 08:33 MDT, JvH).** "Proceed with 'B': The centre the structural paper used, measured or adopted." **Proposed by** Claude (option B, recommended, after JvH asked for a review "as a great scientist"). **Adopted.**

JvH's reason, in his words: "This is the only choice that keeps centre, ellipticity, angle and radius as one consistent set. The 'quoted, not measured' filter exists to keep the Atlas from taking a result second-hand. A centre used as the origin of a fit is part of that paper's own model, not someone else's result. The value is already double-read, and the source it was adopted from is recorded."

1. **Which centre.** The D-051 coverage check uses the centre the structural original used for its fit, whether that paper measured it or adopted it from another paper. Which of the two it was, and the cited source, is recorded.
2. **No centre.** A structural original that neither prints nor cites a centre leaves the value "coverage not checkable". There is no fallback.
3. **Cross-check (information only, not a gate).** Where the kinematics paper states its own centre, the outcome with that centre is also reported.

**Alternatives rejected.**
- (A) The measured centre only. This dropped 20 systems for a bookkeeping reason.
- (C) The kinematics paper's centre as the default. It pairs a centre with an ellipse fitted about a different one.
- (D) The LVDB centre. The database is an index (D-048).
- (E) Requiring a pass under every candidate centre. Usually there is only one consistent candidate.

**Data seen at the time of ruling.**
- The count and source papers of the 22 systems lacking a measured centre, and that 20 of them print an adopted centre.
- The coverage outcomes of batches 1 and 2 (PR #80).
- No dispersion value entered the proposal.

---

## D-055 — Nine A5 cases the frozen rules could not settle

**Ruling (2026-10-31 09:32 MDT, JvH).** "Proceed as recommended." **Proposed by** Claude. **Adopted unchanged.** Some coverage outcomes and the counts were known when these were proposed. Each recommendation follows a principle stated in advance, and none was chosen for its effect on any value.

Implemented in:
- `reading/d055_choices.csv` and `reproduction/apply_sigma_rules_v3.py` (items 2–5);
- `reading/sigma_candidates.csv` (item 1).

Items 6–9 are applied in the conversion.

1. **Hendricks 2014 (Fornax)** reports new VLT/FLAMES spectra, so it is an **original**. The candidate list had marked it "unclear".
2. **A paper prints its adopted value differently in two places.** Use the printing that matches the abstract or text:
   - And XXVI, Collins 2013: Table 4, not Table A1;
   - Cen I, Heiger 2024: Table 1, not Table 5.
3. **Unresolved dispersion given as a best value plus several upper limits.** Plot the upper limit the paper states in its abstract (REPRODUCTION.md: "plotted as limits at the level the source states"):
   - Grus II, Simon 2020: 90%;
   - Tucana III, Simon 2017: **95.5%**.

   Claude's proposal said "90% in both". That was wrong for Tucana III, whose abstract states the 95.5% limit. The rule as worded governs.
4. **SMC, Harris 2006.** The table value and the rounded summary are printings of one fit, so the table value is used.
5. **And II, Côté 1999.** The maximum-likelihood estimate is used. The biweight estimate is recorded as an alternative. The central σ₀ of the King-Michie fit is excluded, because it describes the centre only.
6. **NGC 6822.** A V flux density in Jy is not converted. The magnitude comes from RC3, the other listed original, once it is read.
7. **Leo T.** Where only g and r are printed, the published g,r→V transformation that McConnachie 2012 cites is used. It is registered as a named assumption, with its published scatter added to the error. It applies only where no V exists.
8. **Distance with no adopted value** (Segue 2, Boettcher 2013). Use the estimate based on the most stars: the blue horizontal-branch value rather than the single RR Lyrae star. This is a general tie-break after D-052 item 3.
9. **Coverage when the centre differs by fit** (Horologium I, Phoenix II). Run the test with each fit's centre, and pass only if both pass. This is as D-051 applies to ambiguous member windows.

**Data seen at the time of ruling.**
- The coverage counts and pass/fail outcomes of batches 1–3.
- The variant labels and locations of the values in items 2–5.
- In preparing item 3, the main session saw the printed Simon 2017 and Simon 2020 dispersion values and limits.

---

## D-056 — Converting RC3 catalogue values

**Ruling (2026-10-31 10:03 MDT, JvH).** "Rule as A for D-056." **Proposed by** Claude (A recommended, with items 2–3). **Adopted.** Made after reading RC3's column descriptions, and before any galaxy's RC3 value was used.

Implemented in `reproduction/rc3_convert.py` (frozen). It reads the identified rows (`reading/rc3_values.csv`, two readers) by record number from the VizieR VII/155 export.

1. **Magnitude:** V₀ = B₀ᵀ − (B−V)₀ᵀ, from RC3's own corrected columns. RC3's correction includes Galactic and internal extinction and a redshift term; the internal-extinction part is registered as a named assumption ("RC3 corrected magnitudes include internal extinction").
2. **Radius:** r_h = ½ × 0.1′ × 10^Aₑ (Aₑ = log effective-aperture diameter in 0.1′), treated as circularised.
3. **Shape:** ε = 1 − 10^(−R25), with RC3's position angle. The 25 mag arcsec⁻² isophote's shape stands in for the half-light ellipse; this substitution is recorded.

**Reason (Claude, adopted).**
- Only printed numbers are used, with no extinction model of the Atlas's own, as when a paper prints its own m_V,0.
- The radius and shape steps are unit arithmetic.

**Alternatives rejected.**
- (B) Raw values with a Galactic correction by an assumed A_V/A_B ratio.
- (C) Leave RC3 unused: nine systems would then have no luminosity.

**Data seen.** RC3 column descriptions only.

---

## D-057 — Metallicity used for the stellar mass-to-light interpolation (A5)

**Ruling (2026-10-31 10:18 MDT, JvH).** He ruled in these words: "the mean spectroscopic [Fe/H] from the original paper the database cites for it (ref_metallicity_spectroscopic), read twice like everything else. Where no spectroscopic value exists, use the database's photometric or isochrone original, flagged as such. This keeps D-048's 'originals are the record', and spectroscopic iron abundances are the standard input for these models." **Proposed by** Claude (option A, recommended). **Adopted unchanged.** Made before any metallicity value of an A5/A7 candidate was read.

1. **Spectroscopic first.** For REPRODUCTION.md's Υ_V route (b), each system's [Fe/H] is the mean spectroscopic value printed by the LVDB `ref_metallicity_spectroscopic` original. It is read by two independent readers.
2. **Fallback.** Where none exists, use the LVDB `ref_metallicity_photometric` original, else the `ref_metallicity_isochrone` original. Either is flagged with its kind.
3. **Floor.** REPRODUCTION.md's floor applies: below the lowest tabulated [Fe/H], use the lowest value, flagged `beyond_source_range`, with no extrapolation.

**Alternatives rejected.**
- (B) The dispersion paper's own [Fe/H]: patchy coverage.
- (C) One fixed value: discards measured information.

**Data seen.** None of the metallicity values.

## D-058 — HI masses rescaled to the package distance (A5)

**Ruling (2026-10-31 10:28 MDT, JvH).** He ruled in these words: "rescale each HI mass and each upper limit by (D_package / D_Putman)², and record both distances. Why: the HI mass scales exactly as D², so this is an exact conversion, not a model. It also keeps one distance per system, as D-052 does." **Proposed by** Claude (option A, recommended). **Adopted unchanged.**

1. **Rescaling.** Each HI mass and each 5σ upper limit from Putman et al. 2021 Table 1 is multiplied by (D_package / D_Putman)². D_package is the D-052 distance. D_Putman is the table's `Dist`. Putman computes M_HI = 2.36 × 10⁵ S D² (§2, read at source in arXiv:2101.07809v1), so the conversion is exact.
2. **Record.** Both distances and the factor are stored with each system.
3. **Settled under existing rulings, stated here for the record.**
   - Helium factor: the registered default of 1.33 (Lelli et al. 2016, read at source). It is not adjustable until a published range is read (D-034).
   - Gas inside r½: half the total, flagged (REPRODUCTION.md), because Table 1 gives only total masses.

**Alternative rejected.** (B) Use the masses as printed, with Putman's distance shown. This mixes two distances in one system's g_bar.

**Data seen.** Both readings of Table 1, compared and adjudicated (`reading/gas_adjudication.md`). That includes Cassiopeia II: Putman's distance is 682 kpc and the package distance is 559.8 kpc. The conversion was not run.

## D-059 — Stellar mass-to-light route for every dwarf; metallicity fallback (A5)

**Ruling (2026-10-31 10:59 MDT, JvH).** "Go for 1a and 2a." **Proposed by** Claude (both recommended). **Adopted unchanged.** Ruled after the Woo 2008 and metallicity readings were compared. No mass-to-light value, g_bar or g_obs had been computed.

1. **One route for all.**
   - Every A5/A7 system takes Υ_V from the frozen metallicity interpolation: REPRODUCTION.md route (b), at the D-057 [Fe/H].
   - Woo et al. 2008 data-set "b" values are shown as labelled alternatives where they exist (30 systems). They enter the Υ_V range as D-039 item 3 provides.
   - Route (a) is not used. Its condition, "a cited star-formation-history value per system", cannot be verified. Woo assigns M*/L by type and data availability (Table 3, Cases 1–3) and does not print which case applies to each galaxy (both readers, `reading/feh_adjudication.md`).
2. **Metallicity fallback.** Some plotted systems have no LVDB metallicity original. For these, use the mean spectroscopic [Fe/H] printed by the system's dispersion original, read twice and flagged `feh_from_dispersion_paper`. Where that paper prints none, the system is recorded and not plotted. At the time of ruling there are ten such systems: And VI, XI, XII, XIII, XVII, XX, XXII, XXIII, XXVII and Cassiopeia II. Their originals are Collins 2013, and Tollerud 2012 for And XIII.

**Reason.** One method for every system avoids a split by which galaxies happen to be in Woo's table. The fallback is still a spectroscopic measurement from an original paper.

**Alternatives rejected.**
- (1B) Woo values as printed, labelled: the method per galaxy is unknown.
- (2B) Not plotted: discards a measurement that exists.
- (2C) The lowest tabulated model value with the full range: assumes an unmeasured metallicity.

**Data seen.**
- Both readings of the D-057 originals and of Woo 2008 Table 1.
- The list of plotted systems without a metallicity original.

## D-060 — Stellar mass-to-light range for dwarfs: an envelope (A5)

**Ruling (2026-10-31 11:06 MDT, JvH).** "Proceed with envelope." He restated the rule and its reason and cost as proposed. **Proposed by** Claude (option A, recommended). **Adopted unchanged.** This makes D-039 item 3 concrete for dwarfs.

1. **Default.** The default is unchanged. It is the BC03 + Chabrier-disk (M/L)₁ of McLaughlin & van der Marel (2005), interpolated at the D-057/D-059 [Fe/H] by the frozen `aeg.ml_interp`.
2. **Metallicity interval.** The interval is [Fe/H] ± s.
   - s is the intrinsic spread the metallicity original prints.
   - Where no spread is printed, s is the [Fe/H] error, using the larger of the two sides.
3. **Lower bound.** Take the smallest value of ((M/L)₁ − e_(M/L)₁) over the interval, then multiply by 0.90 and by 0.81.
   - 0.90: the two population-synthesis codes agree within about 10% in Υ_V (McLaughlin & van der Marel 2005 §3.1).
   - 0.81 = 1.3/1.6: Woo et al. (2008) median Υ_V from colours against from star-formation histories (`docs/sources/stellar-ml-2026-10-29.md`).
4. **Upper bound.** Take the largest value of ((M/L)₂ + e_(M/L)₂) over the interval, the Salpeter IMF column, then multiply by 1.10.
5. **Beyond the table.** Outside the tabulated [Fe/H] range the end values apply, flagged `beyond_source_range`. Nothing is extrapolated.

**Reason (JvH).** "These are alternative models, not random errors. An envelope shows their honest combined reach, and every factor traces to a printed number." **Cost:** a wide range, about a factor of 2 to 3 end to end.

**Alternative rejected.** (B) Quadrature, with the IMF as a separate one-sided term. It treats model systematics as independent random scatter.

**Data seen.**
- The McLaughlin & van der Marel table's metallicity span (lowest [Fe/H] −2.29).
- The count of plotted systems below that floor (26 of 64).

No mass-to-light value, g_bar or g_obs of a dwarf had been computed.

## D-061 — Boötes III: structural fit and luminosity (A5)

**Ruling (2026-10-31 12:27 MDT, JvH).** "Go with 1a and 2a." **Proposed by** Claude (both recommended). **Adopted unchanged.**

1. **Structure.** Use the standard single-component Plummer fit of Moskowitz et al. 2020 ("1-Plummer", DECaLS: r_h = 33.03′, ε = 0.33, θ = 278.91°). The paper marks no fit as adopted. D-052's fixed order names Plummer, and the paper calls this one "the standard 1-Plummer profile". The three-component fit (r_h = 32.45′) is recorded as an alternative.
2. **Luminosity.** L_V comes directly from Correnti et al. 2009's M_V = −5.8 ± 0.5, with no distance correction, flagged `mv_distance_independent`. The paper derives M_V from the count of core-helium-burning stars and states that this estimate is independent of distance.

**Alternatives rejected.**
- (1B) The three-component fit: not the profile D-052 names.
- (2B) Not plotting the system: the magnitude needs no distance.

**Data seen.** Both readings of Moskowitz 2020 (the four Boötes III fits) and of Correnti 2009. No g_obs or g_bar had been computed.

**Items 3–7, ruled 2026-10-31 (JvH, by selecting the recommended option for each).** Each value is flagged on the point.

3. **Muñoz 2018 (20 systems).** m_V,0 = M_V + 5 log₁₀(D / 10 pc), where D is the paper's Table 1 adopted heliocentric distance. Flag: `mv_distance_from_table1`. The paper does not tie Table 6 M_V to Table 1 in a sentence. It states that its luminosity functions use "the adopted … distance information".
4. **Leo I distance (Stetson 2014).** The paper prints a range that depends on the assumed metallicity: 22.06 ± 0.08 to 22.25 ± 0.07. Use the midpoint, 22.155, with errors of −0.175 and +0.165, which span both ends and their errors. Flag: `distance_range_midpoint`.
5. **Phoenix.** Use the paper's adopted modulus, 23.1 ± 0.1 (van de Rydt 1991), for its M_V = −9.9 ± 0.4. Flag: `mv_modulus_assumed`.
6. **Leo T.** Use the headline red-clump modulus, 23.1 ± 0.2 (de Jong 2008), for M_V ≃ −8.0. Flag: `mv_modulus_assumed`.
7. **Tucana V.** Use the Table 6 distance, 55 (+3/−8) kpc (Simon 2020), for the M_V,0 in the same table. Flag: `mv_modulus_assumed`.

**Reason (items 3–7).** Where the paper prints the value, use it over dropping the system, and flag it on the point.

**Alternatives rejected.**
- Not plotting the systems.
- For Leo I, the end of the range at the metallicity nearer the D-057 value.

**Data seen.** Both residual readings (`reading/residual_adjudication.md`). No g_obs or g_bar had been computed.

## D-062 — And XII dispersion at zero; Pegasus IV radius (A5)

**Ruling (2026-10-31 14:06 MDT, JvH).** "1. Plot the upper limit. 2 use circularized radius." **Proposed by** Claude. **Adopted.**

1. **And XII.** Collins 2013 gives σ = 0.0 (+4.0) km/s and states no limit. It is plotted as an upper limit at σ = 0.0 + 4.0 = 4.0 km/s, the 1σ upper end, flagged `limit_from_1sigma_upper_error`. The level is recorded as "1σ upper error (no limit stated)".
2. **Pegasus IV.** Cerny et al. 2023 prints the ellipticity only as a 95% upper limit (< 0.41), so a √(1 − ε) is undefined. Use the circularised (azimuthally averaged) r_h that the paper prints in Table 1: 1.55 (+0.29/−0.24) arcmin. This replaces a_h = 1.60′ with ε = 0.

**Reason.**
- Item 1: a best value of zero cannot be placed on a logarithmic axis. Its printed upper error bounds σ at the level the paper gives.
- Item 2: the paper's own circularised radius is the quantity R_h is meant to be, and it needs no assumed ellipticity.

**Alternatives rejected.**
- Recording And XII only.
- Keeping ε = 0 for Pegasus IV, which would overstate R_h by up to ×1.30.

**Data seen.** The computed tables of PR #83 (62 plotted g_obs and g_bar values). These rulings were proposed from the inputs, not from any acceleration.

## D-063 — A6·strong lensing: eight method rulings

**Ruling (2026-10-31 17:29 MDT, JvH).** "Rule as recommended." **Proposed by** Claude (search log A6 §2a). **Adopted** without change.

1. **Stellar M/L from spectra.** A photometric luminosity times a stellar-population M/L fitted to spectra, with a fixed named IMF and named population models, is an accepted baryonic input. An M/L from an assumed age and metallicity range is also accepted, with the range carried as an assumption range. IMF-free spectral fits are never defaults. This clarifies "stellar mass from photometry" in protocol §2 (deviation #21).
2. **Einstein radius from half the image separation** is accepted as a lens model, with `model_dependence` "SIS from image separation". Where a full model of the same system exists, that model is the default. Single-image limits are recorded, not plotted, in v1.0.
3. **Priors that use the system's own velocity dispersion** count as inputs derived from the system's own kinematics (deviation #6).
   - Stellar masses fitted with a metallicity prior from the σ–metallicity relation at the lens's own σ (SLACS IX) are recorded and shown as a flagged alternative, never the default.
   - Systems whose source redshift used the velocity dispersion (SL2S) are recorded, not plotted.
4. **Several lens models and stellar-mass sources for the same lenses.** The observed default is the Einstein mass, and other lens models are shown as alternatives. A precedence rule for both sides is written and hash-frozen before any table is opened.
5. **Redshifts and confirmation.** An Einstein mass needs measured lens and source redshifts; systems without a spectroscopic source redshift are recorded, not plotted. Candidates count only when confirmed. Restricted releases are held until public.
6. **Galaxy or group.** The source's own label is used where sources agree.
   - A6: the model has one main deflector (with external shear or minor perturbers).
   - A8: the source models several group members, or calls it a group lens.
   - A7 "ambiguous": the sources disagree (as deviations #7 and #15).
7. **Stellar mass printed as a fraction of the lens mass** (XLENS I). Fraction × the published Einstein mass is accepted, flagged.
8. **Licence route for SLACS.** The original (SLACS IX and its VizieR table) is the source of record and is cited. The CC BY 4.0 copy on Zenodo is used for redistribution only after a value-by-value check that it matches.

**Reason.**
- Items 1 and 7: the protocol's wording was written to exclude lensing and dynamical masses, not to exclude population M/Ls measured from spectra.
- Items 2, 4 and 5: every plotted point keeps a lens model, measured redshifts and a stated model dependence, with alternatives visible.
- Item 3: applies deviation #6 consistently.
- Item 6: follows the kind rules already used for star clusters and dwarfs.
- Item 8: follows D-004.

**Alternatives rejected.**
- Excluding spectroscopic M/Ls, which would lose every lens below z ≈ 0.07.
- Treating priors as minor and accepting them silently.
- Choosing one lens model per system without showing the others.

**Data seen.** Search log A6 and the two screening readings: metadata, abstracts, methods and table headings only. No data table was opened and no mass, M/L or result was read.

**Still open.** The protocol §5 projection ruling (baryons projected, or lensing deprojected), which is needed before the first lensing package.

## D-064 — Lensing projection: project the baryons (protocol §5)

**Ruling (2026-10-31 17:40 MDT, JvH).** Option (a), as recommended. **Proposed by** Claude (2026-10-31, with option (b) set out beside it). **Adopted.** JvH's words: "Project the baryons. Compare the lensing mass with the stellar mass inside the same projected radius, and express both as G·M/R_E² labelled 'projected'."

1. For galaxy-scale strong lensing (A6), the observed side is the projected mass inside the Einstein radius, M_E. The baryonic side is the projected baryonic mass inside the same cylinder of radius R_E. Both are expressed as G·M/R_E², labelled **projected**.
2. g_obs/g_bar is then exactly M_E / M_bar(<R_E): no mass-profile model enters either side.
3. Projected points carry their own mark and label on the map and in downloads (`projection = projected`). They are never merged with 3D accelerations without that mark.
4. R_E in kpc and M_E use the source's own cosmology, registered where it enters (D-029); the ratio does not depend on it to first order, because both masses scale with the same distances.
5. Applies to A6·strong lensing now. Other lensing cells (A8, A9) get their own ruling when they arrive, with this one as the starting proposal.

**Reason.** It compares like with like (two measured masses in the same projected aperture), adds no profile assumption, and keeps the comparison exact. The cost, that these points are a different quantity from 3D accelerations, is handled by marking them, not by converting them.

**Alternatives rejected.** (b) Deprojecting the lensing mass with an assumed density profile: every point would depend on the profile chosen.

**Data seen.** Search log A6 and the screening readings: metadata and methods only. No lensing mass or stellar mass was read.

**Note.** D-039 had named this ruling as the next blind one. D-040 since replaced blind rulings with recording the proposer, so it was ruled with a recommendation, recorded above.

## D-065 — A6·strong lensing precedence rule (frozen)

**Ruling (2026-10-31 17:43 MDT, JvH).** "Approved as written." **Proposed by** Claude (`docs/methods/A6S_PRECEDENCE.md`, under D-063 item 4 and D-064). **Adopted** without change. Frozen by hash in `data/frozen/a6s-precedence.json`.

What the rule covers:
- who is plotted;
- which lens model is the default (originals first; full models over image-separation estimates);
- which stellar mass is the default (inside R_E; Chabrier/Kroupa default with the Salpeter value as the top of the range; no priors using the lens's own σ; then more bands, a per-object fit, and the most recent);
- the gas route;
- the tests.

**Reason.** It fixes every choice between published values before any value is read, as D-063 item 4 requires.

**Data seen.** Search log A6 and the screening readings only. No lensing table was opened.

## D-066 — The epoch cut for v1.0 plots (applies D-033 item 5)

**Ruling (2026-10-31 18:49 MDT, JvH).** "Rule as recommended. Be a good scientist." **Proposed by** Claude (2026-10-31, option (a)). **Adopted.**

1. **Per-system redshift.** A system with its own redshift (a lens galaxy, a cluster) is plotted in v1.0 only if that redshift, as printed by the source, is below 0.30 exactly.
2. **Above the cut.** Systems at z ≥ 0.30 are recorded in full, flagged `epoch_gap_v1`, and counted on the Coverage page as part of the documented cosmic-epoch gap.
3. **Scope.** The cut applies to every cell whose systems carry a per-system redshift: A6·strong lensing, A9, and later cells. It adds a condition to the who-is-plotted list of D-065 §1. The frozen file is not changed; this decision is the amendment.
4. **Not covered: stacked samples whose bins span a redshift range** (the KiDS-1000 package and any A9 stacks under D-067 item 2). Changing what an existing package shows is a separate decision. Claude proposes it with the KiDS lens redshift distribution read at source, and it returns to JvH. Until then nothing already published changes.

**Reason.** D-033 item 5 set the gap but not the line. An exact cut on the printed redshift is fixed before any value is seen, and leaves no case-by-case judgement after.

**Alternatives rejected.** An approximate threshold decided per case.

**Data seen.** Search logs A6 and A9 (redshift ranges as stated in the readings). No masses or results.

## D-067 — A9 method rulings: joint fits, stacks, projection for clusters

**Ruling (2026-10-31 18:49 MDT, JvH).** "Rule as recommended. Be a good scientist." **Proposed by** Claude (`docs/sources/screening-A9/adjudication.md`, QA1–QA3). **Adopted.**

1. **Joint fits.** A lensing profile fitted jointly with stellar dynamics, X-ray hydrostatics or member-galaxy dynamics in one model is not used as the observed side. A record is usable only where the source also publishes a lensing-only (or dynamics-only) profile. Joint-fit products are recorded, not plotted. This follows the standard: channels are never merged by default.
2. **Stacked profiles.** A stack is plotted only as a population average (content type `population_average`), and only where the baryonic side is stacked over the same clusters with the same weights. Otherwise it is recorded.
3. **Projection for clusters** (extends D-064 to A9 lensing). The lensing side stays projected, and the gas is projected onto the same cylinders.
   - The projection integrates only over the radial range the source measured.
   - The contribution from beyond that range uses the source's own fitted model, as a registered assumption with its share shown per point.
   - Points whose outer contribution cannot be bounded this way are recorded, not plotted.

**Reason.**
- Item 1 keeps the dynamics and lensing channels separate.
- Item 2 compares like with like.
- Item 3 keeps the comparison in projection without a mass-profile model on the lensing side, and makes the one unavoidable extrapolation explicit and visible.

**Alternatives rejected.**
- Joint fits as the observed side.
- Stacks paired with per-cluster gas.
- Deprojecting the lensing.
- Silent extrapolation of the gas.

**Data seen.** Search log A9 and the two screening readings: metadata and methods only.

## D-068 — Stars in clusters: measured, searched for, never silently modelled; X-COP's modelled stars reported

**Ruling (2026-10-31 19:03 MDT, JvH).** "I agree on all fronts. Please proceed." **Proposed by** Claude (2026-10-31, in answer to "as a good scientist, what do you recommend?"). **Adopted.**

1. **A9 needs measured stars.** Before the A9 precedence rule is frozen, a logged search for stellar-mass sources covering the eligible A9 clusters below z = 0.30 is run, with its brief committed first. The five X-COP clusters with modelled stars are added to that search. Only clusters still without measured stars afterwards are recorded, not plotted.
2. **Modelled stars** (D-034) are shown only as a labelled alternative, never the default, and only where the model does not use the cluster's own total mass.
3. **X-COP.**
   - The modelled stars of A1644, A2255, A3158, A3266 and RXC1825 are normalised by the hydrostatic M500 (D-022 item 3). That conflicts with deviation #6, which was ruled the day after D-022.
   - The conflict is reported as known issue #91 and appears on the Known issues page.
   - Where measured stellar masses are found, they replace the model in the data standard 2.0 re-issue. Where none are found, JvH rules whether those rows stay plotted as labelled "modelled" or become recorded only.
   - The 7 clusters with measured stars (Ghizzardi et al. 2020) are unaffected.
4. **Site.**
   - Clusters measured by several channels (X-ray hydrostatic, lensing, member galaxies) get a system page showing each channel's profile side by side, each marked, never averaged.
   - Every point shows whether it is projected or 3D, and whether its stars are measured or modelled, by mark, legend and tooltip.

**Reason.**
- Leaving stars out, or modelling them from the total mass, biases g_bar in a known direction or makes it circular.
- Searching before excluding keeps coverage without lowering the standard.
- A problem found in one's own published data is reported at once.
- Showing channels side by side is both the honest display and the most informative one.

**Correction recorded.** Claude's recommendation said the X-COP stars would be replaced "with measured stellar masses (Ghizzardi et al. 2020)". On checking D-022: Ghizzardi et al. 2020 covers the 7 clusters that are already measured, not the 5 modelled ones. Item 3 above states the plan correctly.

**Data seen.** D-022 and D-023 and the X-COP package's status columns (counts of measured and modelled rows). No masses were read.

## D-069 — No summing of member-galaxy catalogues for cluster stellar masses (v1.0)

**Ruling (2026-10-31 19:49 MDT, JvH).** "We'll do no for summing member catalogues." **Proposed by** Claude (`docs/sources/screening-S9/adjudication.md`, QS4, option (a)). **Adopted.**

In v1.0, the Atlas does not build a cluster's stellar mass by summing a published catalogue of member galaxies, or by integrating a published stellar mass function. Such records are kept as inputs and leads, coded X for the baryonic side.

**Reason.** Summing needs the Atlas's own membership and completeness corrections, which is new analysis, not reading. The same line was drawn for star clusters and dwarfs, where velocity dispersions are never computed from individual stars.

**Effect.**
- A1644 (X-COP) has no eligible measured stellar mass.
- S1b, S1c, S19, S13b and S13f become X for the baryonic side.

**Data seen.** The stellar-mass screening readings: metadata and methods only.

## D-070 — X-COP clusters without measured stars: recorded, not plotted (2.0 re-issue)

**Ruling (2026-10-31 19:50 MDT, JvH).** "I'll say yes." **Proposed by** Claude. **Adopted.**

1. **RXC1825 and A1644** (no measured stellar mass found; D-068, D-069) are **recorded, not plotted**, in the data standard 2.0 re-issue of `aeg-d-xcop`. Their only available stellar model is normalised by the cluster's own hydrostatic M500, which D-068 item 2 forbids even as an alternative. Leaving stars out is forbidden by protocol §1.7. Each system page states the reason. A cluster returns to the map if measured stellar masses are published.
2. **A2255** gets measured stars from Laganá et al. 2011. Their Salpeter values are converted to the Chabrier default by a registered ratio, read at source. This waits on a check of whether the sources call A2255 a merger (A10).
3. **A3158 and A3266** get measured stars from the OmegaWINGS profiles, once the IMF is confirmed at source (QS2).
4. **Until the re-issue,** the current v1 rows stay as published and are marked by known issue #91. The pre-release data are not patched by hand.

**Reason.** Neither a circular model nor an omission may stand in for measured stars. Recording the cluster with its reason keeps it visible and honest.

**Data seen.** The stellar-mass screening and coverage table (names, codes); D-022 and D-023.

## D-071 — Cluster stars from printed luminosity × the Atlas's registered stellar M/L

**Ruling (2026-10-31 20:17 MDT, JvH).** "Yes." **Proposed by** Claude (2026-10-31, option (a)). **Adopted.**

A cluster's stellar mass counts as **measured** (D-034) when it is the luminosity printed by the source times the Atlas's own registered stellar-population mass-to-light ratio. The luminosity covers the brightest cluster galaxy plus members, with the source's own membership and completeness corrections. The ratio follows the D-039 model family: Chabrier or Kroupa default, Salpeter as the top of the range, read at source and registered per band. The source's own conversion to mass is not used where it is dynamical, or tied to M500 or another scaling relation.

Safeguards:
1. **The source's light and the source's sums only.** The Atlas sums nothing (D-069).
2. **Matched geometry.** A projected luminosity is paired only with lensing (row L), a 3D luminosity only with member-galaxy dynamics (row O), unless the source gives both. Otherwise the cluster is recorded, not plotted.
3. **One radius.** The comparison is made only at the aperture where the luminosity is measured; no stellar profile shape is assumed. An aperture set by a scaling relation is used as a radius and flagged.
4. **Missing light.** Intracluster light the source did not measure gets a registered range, as `icl_fraction` for X-COP. Its default and range are read at source.

**Reason.**
- It is the method already used for star clusters and dwarfs.
- It removes the circularity at its root: the light is measured, and the conversion does not use the cluster's dynamics.
- At the radii compared, gas dominates the detected baryons, so the stellar ratio's range moves g_bar modestly. The slider shows by how much, computed from the data.

**Cost.**
- Most clusters get one point, at their measured aperture.
- The stellar-mass sources are re-screened for printed luminosities, under a brief committed first.

**Alternative rejected.** Keeping only sources that print stellar masses with an acceptable conversion (about 7 to 14 clusters).

**Data seen.** The stellar-mass readings and the coverage table: names, codes, methods. No luminosities or masses.

## D-072 — Round L rules: printed components, BCG by method, faint-end limit, magnitudes, deprojection, precedence

**Ruling (2026-10-31 20:49 MDT, JvH).** "Proceed as recommended." **Proposed by** Claude (2026-10-31, QL1–QL6 in `docs/sources/screening-L9/adjudication.md`). **Adopted.**

1. **Printed components (QL1).** The Atlas may add a source's own printed cluster-level components when the source defines them as disjoint and they share one aperture (e.g. BCG + red members + blue members). This is arithmetic on the source's cluster totals, not a sum over a member catalogue (D-069), and Test 3 checks it. A total is never recovered by dividing a printed luminosity by a printed fraction.
2. **BCG not stated (QL2).**
   - A direct sum over all galaxies or members in the aperture, with no stated exclusion, includes the BCG. It is flagged "BCG by method".
   - A total that is only an analytic integral of a fitted Schechter function, with no separate BCG term, counts as members only and is not used.
3. **Faint end (QL3).**
   - Accepted: a sum truncated at a stated faint limit at least 2 mag fainter than M*, flagged with its limit. Where the source quantifies the missing faint light, it is shown as a range.
   - Not used: bright-only sums (a limit brighter than M* + 1).
   - The Atlas does not model missing light.
4. **Magnitudes and evolution (QL4).**
   - An absolute magnitude in a named band counts as a printed luminosity. It is converted with that band's solar absolute magnitude, read at source and registered.
   - An observed-frame apparent magnitude does not count.
   - A luminosity the source has evolution-corrected is paired with the stellar M/L for the epoch it was corrected to.
5. **Deprojection (QL5).** A luminosity deprojected by the source's own model counts as 3D and pairs with row O. It is labelled `model_dependence` with the source's assumption.
6. **Precedence (QL6),** written into `docs/methods/A9_PRECEDENCE.md`:
   1. the source's measured stellar mass (route a), then luminosity × registered ratio (route b);
   2. within route (b), near-infrared bands first;
   3. a team's later analysis of the same data supersedes its earlier one;
   4. projected values pair with row L, 3D values with row O.

**Reason.**
- Each rule keeps the light measured by the source and the conversion independent of the cluster's dynamics, consistent with D-069 and D-071.
- QL2 follows what each method actually counts. A Schechter integral replaces the brightest galaxy, often the largest single component, with the fitted form.
- Near-infrared first because the stellar-population ratio varies least there.

**Effect on codes.**
- E: L2, L8, LV3, S6 (QL2); L10, L23b, S3a (QL1).
- X: L4, S4b, S4d (QL2); S10a (QL4).

**Alternative rejected.** Strict QL2 (an explicit BCG statement required), which would also exclude L2, L8, LV3 and S6.

**Data seen.** Names, codes, methods, column lists and text describing methods. No luminosities or masses.

## D-073 — A9 galaxy-cluster precedence rule (frozen)

**Ruling (2026-10-31 21:09 MDT, JvH).** "Approved." **Proposed by** Claude (`docs/methods/A9_PRECEDENCE.md`, under D-064, D-066, D-067, D-068, D-071 and D-072). **Adopted** without change. Frozen by hash in `data/frozen/a9-precedence.json`.

What the rule covers:
- **Who is plotted:** A9 kind, printed z < 0.30, a lensing-only (row L) or dynamics-only (row O) observed side, measured gas, measured stars, star geometry matched to the channel, and no scaling-relation inputs.
- **The observed side:** originals first; binned before fitted; rows L and O never averaged.
- **The gas:** X-COP, then CHEX-MATE, then the survey's own source; projected for row L, 3D for row O.
- **The stars:** route (a), stellar mass from photometry, or route (b), printed luminosity × the registered ratio, with the D-069, D-071 and D-072 rules and the per-cluster order; intracluster light as a registered range; modelled stars only as labelled alternatives (#91).
- **The tests.**

**Reason.** It fixes every choice between published values before any A9 value is read. The coverage table (`docs/sources/screening-L9/coverage-A9-v3.md`) shows the rule leaves about 79 clusters with stars that can be paired with an observed side, before the gas check.

**Data seen.** The search logs, screening readings, coverage tables (names, redshifts, codes, methods) and catalogue column lists. No A9 table, luminosity or mass was opened.

## D-074 — A9 route: case studies, a LoCuSS one-radius layer, and a CHEX-MATE watch

**Ruling (2026-10-31 22:07 MDT, JvH).** "Proceed as recommended in this analysis." **Proposed by** Claude (2026-10-31, option E, after `docs/sources/screening-L9/gas-coherence-A9.md`). **Adopted.**

1. **No A9 population profiles for now.** No programme supplies an observed side, stars and a gas density profile for the same clusters below z = 0.30 (gas-coherence record, PR #92).
2. **Case studies** (content type "case study"), about eight clusters whose inputs are all published:
   - Member dynamics with X-COP baryons: A85, A2142, ZwCl 1215.
   - Lensing: A1689, A1835, A2390, MS 1455+22.
   - Coma: both channels.
   - Each page shows every channel, every baryon component, and every centre and aperture with their offsets. A case study is never merged into the population map.
3. **LoCuSS layer, one point per cluster at r500,WL**, with two scoped rule changes that apply to this layer only:
   - (a) **3D comparison.** The observed side is the source's 3D lensing mass from its NFW profile fit, labelled `model_dependence`. This replaces D-067 item 3 (project the baryons) for LoCuSS, whose gas is published only as 3D masses within the aperture.
   - (b) **Stars as an upper bound.** The projected K-band light (S6) × the registered ratio is used as an upper bound on the 3D stars, flagged as a one-sided bias (g_bar slightly high, so the discrepancy slightly low). This replaces D-071 safeguard 2 for this layer.
   - The aperture comes from the cluster's own lensing mass: radius only, flagged.
   - The points carry their own mark ("one radius").
   - A spec is written and hash-frozen before any LoCuSS table is opened.
4. **CHEX-MATE watch.** When its density profiles are released, a coherent lensing population (19 clusters) is screened as a later version.
5. **Funnel page.** It shows the A9 counts from the search to the plot, with the reason at each step.

**Order:**
1. A6 packaging.
2. The X-COP case studies.
3. The LoCuSS spec, frozen, then packaged.
4. The other case studies.
5. The funnel page.

**Reason.**
- Coherent sources over a mosaic. LoCuSS is the most coherent sample found: one team, one BCG centre, one aperture, all inputs printed in tables.
- Case studies give depth that can be checked by hand.
- Every departure from the general rules is scoped to one layer, labelled, and one-sided where it biases.

**Disclosure.** The two LoCuSS rule changes were proposed after the coverage (names, codes and methods) was seen, not after any value.

**Alternatives rejected.**
- Case studies only: too thin to show the cluster regime.
- XXL from figures: tier 3, and its centres differ in kind.
- Waiting for releases or author data.

**Data seen.** Coverage and gas-coherence records only: names, redshifts, codes, centres, apertures and methods. No masses, luminosities or densities.

## D-075 — A6 strong lensing: rulings on the adjudication (gas, fallback record, input forms, conventions, IMF and profiles)

**Ruling (2026-11-01 08:29 MDT, JvH).** "Proceed as recommended." **Proposed by** Claude (2026-11-01, five decisions in reply to Q1–Q14 of `data/packages/aeg-d-strong-lensing/v1/reading/adjudication.md`). **Adopted.**

1. **Gas.** No A6 point is plotted until the gas term inside R_E rests on a quoted literature measurement. Labelling g_bar "stars only" is rejected (protocol §1.7: no omission of a present component).
   - Next, a logged search for measured gas masses (hot X-ray gas, HI, molecular gas) inside about the effective radius of early-type galaxies, with its plan committed before it is run.
   - From it, a registered default and range is proposed to JvH and shown with a slider.
   - The five systems whose sources state gas negligible (R28, R25, R32) keep those statements as quoted source assumptions (Q14).
2. **Fallback record.** Where a system's default record cannot supply a quantity the frozen rules require, the next-ranked eligible record in the frozen ranking (inventory §2) is the default for that system, flagged `fallback_record`. This covers:
   - J0946+1006 (R66 tPIEMD) → R13;
   - J1538+5817 (R49 has no Chabrier or Kroupa value) → R13;
   - J0403−0239: R29's matched pair (one radius, cosmology and redshifts), R27 shown as the alternative;
   - SNL-1 (R33 MGE): the next eligible stellar-mass record.

   No tPIEMD or MGE code is written for v1 (Q2, Q6, Q7, Q8).
3. **Input forms already covered by D-063.**
   - The SNELLS masses inside half the image separation, which the cited source uses as its Einstein radius (D-063 item 2), are accepted, flagged `model_dependence` (Q1).
   - A stellar mass printed as luminosity × a stellar-population M/L with a named IMF (D-063 item 1) is computed by package code, flagged `mstar_from_L_times_ML`, and the product is added to Test 3 (Q3).
4. **Conventions**, each flagged on the point:
   - a printed Ω_Λ = 1 − Ω_m is flat;
   - a cosmology given only by name or reference uses the numbers in the named paper, read at source;
   - R5's stated survey-wide 2% error on θ_E is carried, flagged `sample_level_error`;
   - where no error is printed, `no_uncertainty`;
   - NGC 6505 uses its spectroscopic z = 0.04243 (Q4, Q12, Q13).
5. **IMF and light profiles.**
   - SLACS (R13): Chabrier–BC03 is the default, Salpeter–BC03 the top, and the Maraston 2005 pair an alternative (Q5).
   - The Salpeter top elsewhere is the source's own printed conversion where it gives one; otherwise the model paper's ratio, read at source (Q11).
   - S4TM uses R10's printed de Vaucouleurs fit for the profile step, flagged `mstar_in_RE_from_profile` and `profile_differs_from_mass_photometry` (Q9).
   - SL2S uses the CFHT fit, the same photometry as its masses (Q10).
   - **Profile-step check (reported, not pass/fail):** for SLACS, R13 prints both totals and masses inside R_E. The §3.1 profile step is run on the SLACS totals and compared with R13's printed values, and the result is shown on the S4TM and SL2S pages.

**Reason.**
- Each choice either applies a rule already frozen (D-063, D-065) or picks the option that keeps one cylinder, one cosmology and one source.
- Item 2 replaces four case-by-case choices with one rule set before any value was seen.
- The gas term is the one physical gap, so it is filled from measurements, not from a label.

**Data seen.** The adjudicated input values of the systems below z = 0.30 (Einstein radii and masses, stellar masses, M/L, luminosities, profile parameters). No g_obs, g_bar or ratio was computed, and nothing was plotted.

## D-076 — A6 strong lensing: gas term, Salpeter top for S4TM, SNL-1 record, data standard 2.1.0

**Ruling (2026-11-01 09:49 MDT, JvH).** "Proceed as recommended." **Proposed by** Claude (2026-11-01, from `data/packages/aeg-d-strong-lensing/v1/reading/gas/adjudication_gas.md`). **Adopted.**

1. **Gas term (option G1).** For every A6 system, as a fraction of M*(<R_E):

   | Component | Default | Range | Evidence |
   |---|---|---|---|
   | hot X-ray gas | 0.12% | 0.015–2.5% | 28 same-aperture gas and stellar measurements of early-type galaxies, 25 detected |
   | cold gas (molecular plus atomic) | 0 | 0–2% | molecular: 56 measurements, 16 detected, top from a published bound of about 1%; atomic: top from a flagged sample bound of about 1% |
   | **total** | **0.12%** | **0.015–4.5%** | |

   Radii are never rescaled. A single-dish beam counts as half its printed width, flagged. Non-detections are kept as limits.

   - The term is registered as an assumption with a slider, with the measurement table and quotes in the adjudication file.
   - The five systems whose sources call gas negligible (SNL-0, SNL-1, SNL-2, J1436+4943, J1701+3722) take the same term; the source statements are shown as notes.
   - Rejected: G2, a hot-gas default of 0.38% from lens-mass galaxies only, whose masses are high by method.
2. **Salpeter top for S4TM.** R30's printed FSPS factor (Chabrier masses divided by 0.61, i.e. × 1.64), read at source. The other printed conversions span 1.55–1.71. SL2S uses its own printed Salpeter masses.
3. **SNL-1.** D-075 item 2 applied as written: the next-ranked record in the frozen ranking is R61. Its two values (L_F814W and Υ_ref) are confirmed by a second reader before conversion.
4. **Data standard 2.1.0.** One quantity, `einstein_mass`, is added to the observed side (§4a), with a validator test. Nothing else changes.

**Disclosure (proposer not fully blind).** While checking table layouts, the gas adjudicator saw a few lens-related printed values in its terminal:
- the first eight rows of R7 Table 4, including R7's f*,Ein from its σ-prior alternative masses;
- R61's lensing-based Υ_Rap;
- one M_DM entry in R32;
- R9's qualitative text.

None was recorded or used. The gas numbers were computed by a committed script from literature galaxies only. JvH was offered a fully blind re-derivation and ruled to proceed.

**Reason.**
- The gas term rests on measured gas and stars in the same apertures of early-type galaxies, which is what D-075 item 1 required.
- The range runs from the lowest measured value to an upper bound, so the slider shows how far gas can move g_bar.
- The Salpeter factor is printed by a source for the same model family.

**Data seen.**
- The gas measurements of the literature galaxies, and the lens inputs.
- No lens g_obs, g_bar or ratio has been computed. The adjudicator's exposures are as disclosed above.

## D-077 — First release: v0.1, marked preliminary

**Ruling (2026-11-01 11:51 MDT, JvH).** "Tag v0.1 as recommended." **Proposed by** Claude (2026-11-01). **Adopted.**

1. **The tag.** The first tag is **v0.1**, on `main` after the changelog for A6 is merged. No earlier release or tag exists.
2. **Marked preliminary everywhere it appears.**
   - The GitHub release is marked "pre-release" and titled "v0.1 — preliminary (not peer reviewed)".
   - The release notes open by saying that the data are preliminary and pre-review, and that the v1.0 gates (#16) are not met.
   - The site keeps its pre-release banner.
3. **DOI.** The release is made after JvH connects Zenodo to the GitHub organisation, so it can be archived with a DOI. If Zenodo does not archive GitHub pre-releases, a separate ruling is needed: an ordinary release with "preliminary" in its title and notes, or no DOI for v0.1.
4. **Content.** The six live datasets: SPARC, KiDS-1000, X-COP, Baumgardt globular clusters, Local Group dwarfs, and A6 strong lenses.

**Reason.** It is the project plan's first goal, a citable, versioned snapshot of what is live, labelled so nobody mistakes it for a reviewed result.

**Data seen.** Not applicable.

**Done (2026-11-01 12:24 MDT).** JvH published the GitHub release; this session is not permitted to create releases. Tag `v0.1` is on commit 3edbcd0, marked pre-release. Zenodo archived it:
- version DOI **10.5281/zenodo.23864356**;
- concept DOI (all versions) **10.5281/zenodo.23864355**.

The Zenodo record shows the preliminary note.

## D-078 — Competing-interests statement

**Ruling (2026-11-01 15:07 MDT, JvH).** "Yes, I approve." **Proposed by** Claude (2026-11-01). **Adopted.**

1. **The statement.** On the About page, in both language layers, and in the methods paper:
   > "The maintainer also works independently on theoretical physics, including questions related to the acceleration discrepancy. None of that work is used in the Atlas, by rule, and the Atlas takes no side between the accounts of the discrepancy. The maintainer has no financial interests in this work."
2. **It replaces a draft placeholder** that v0.1 was released with ("will appear here before release"). That release is corrected by this change on the live site; the archived v0.1 snapshot keeps the placeholder, and the next release carries the statement.
3. **Zenodo metadata** for future releases:
   - title "Atlas of Extra Gravitation — data release";
   - "isDocumentedBy" the frozen selection protocol (10.5281/zenodo.23780203), so the two Atlas records are linked.

   The v0.1 record gets the same link by a manual metadata edit (JvH).

**Reason.**
- Reviewers will look the maintainer up. A non-financial interest declared up front is standard practice and reads as integrity; discovered undeclared, it would read as an agenda.
- The statement names no paper or theory, and says what a reader needs before trusting a neutral atlas.

**Data seen.** Not applicable.

## D-079 — Naming of the Atlas's Zenodo records

**Ruling (2026-11-01 15:11 MDT, JvH).** "Approve." **Proposed by** Claude (2026-11-01). **Adopted.**

1. **One pattern for every Atlas record on Zenodo:** "Atlas of Extra Gravitation — {what it is}". The version goes in Zenodo's Version field, never in the title.
2. **Titles:**

   | Record | Title | Version |
   |---|---|---|
   | Protocol (10.5281/zenodo.23780203) | Atlas of Extra Gravitation — selection protocol (pre-registered 2026-10-29) | 1.0 |
   | Data release (concept 10.5281/zenodo.23864355; v0.1 10.5281/zenodo.23864356) | Atlas of Extra Gravitation — data release | v0.1 (preliminary) |
   | Methods paper (when deposited) | Atlas of Extra Gravitation — methods | — |

3. **The protocol rename is metadata only.** Its frozen files, their hashes, its DOI and its publication date (2026-10-29) do not change. Its previous title was "Atlas of Extra Gravitation: v1.0 taxonomy and selection protocol (frozen 2026-10-29)".
4. **Who edits.** The existing records are edited by JvH (or by Claude in JvH's browser with his go-ahead), as metadata edits that create no new version. Future data releases take their title from `.zenodo.json` (D-078 item 3).

**Reason.** "v1.0" in the protocol title next to a v0.1 data release, and a data release titled only with the Atlas's name, made the two records look like rival versions of one thing.

**Data seen.** Not applicable.

## D-080 — Review readiness: freeze new datasets, fidelity first

**Ruling (2026-11-01, JvH).** "1. Freeze new datasets. 2. Draft the sparc courtesy note. 3. Order: fidelity first." **Proposed by** Claude (2026-11-01). **Adopted.**

1. **Freeze.** No new dataset work (A9 clusters, A3, A5, A8 and the rest of #48) until `docs/plans/REVIEW_READINESS_PLAN.md` work packages 1–6 are done, or JvH lifts the freeze. Fixes to shipped datasets are not frozen.
2. **SPARC courtesy note.** The draft is refreshed in Dropbox (`07 AEG/05 Correspondence/Drafts/`), outside this repository. JvH sends it. The hold on author correspondence (2026-10-29) is lifted for this note only.
3. **Order.** Fidelity first (#8, #19, #9, a SPARC RAR selection view, a Reproduction page), then the error budget, an independent audit, methods, reproducibility, open issues, and outside review, as set out in the plan.

**Reason.**
- The first thing a specialist will do is compare the Atlas with the published numbers they know best. An unexplained mismatch in SPARC, the most-used dataset in this field, would be enough to dismiss everything else.
- More datasets widen the surface for that kind of error; finishing the shipped ones narrows it.

**Data seen.** Not applicable.

## D-081 — Freeze the independent audit plan before the sample exists

**Ruling (2026-11-01, JvH).** "I approve freezing the audit plan." **Proposed by** Claude (2026-11-01). **Adopted.**

1. **Plan.** `docs/audit/AUDIT_PLAN.md` and the draw script `docs/audit/sample.py` are frozen by hash (`data/frozen/audit-plan.json`). They fix:
   - the frame and sample size: four shipped packages, default rows, 5 % per package with a minimum of 10, so 234 rows;
   - the seed: a public randomness beacon pulse at least 24 hours after this ruling's merge;
   - the readers: two blind readers per row, with a fixed brief;
   - the tolerances and the codes;
   - the pass rule: zero material discrepancies and zero provenance failures;
   - the neutrality term scan and page checklist.
2. **Timing.** The audit runs after work packages 1 and 2. The frame is fixed now by measurement identifier, so later work cannot steer which rows are audited.
3. **Results** are published whether they pass or fail, and are not re-scored. Errors found become logged corrections.

**Reason.**
- The audit is only independent if its sample and rules are fixed before anyone knows which rows it will check.
- Claude has worked inside these datasets and is not a blind auditor. Fixing the plan now, and giving the reading to fresh readers, limits that.

**Data seen.** The row counts per package at commit `d102bc9`, to set the sample sizes. No values were consulted. The draw script was run once with a dummy seed ("00"), to check the counts. That draw is not the sample.

## D-082 — Audit plan version 2: the frame includes all six shipped packages

**Ruling (2026-11-01 18:44 CST, JvH).** "approve D-082, merge 103". **Proposed by** Claude (2026-11-01). **Adopted.**

1. **The error.** The audit plan frozen under D-081 lists four shipped packages in its frame. Six are shipped:
   - `aeg-d-gc-baumgardt/v1`, 64 plotted globular clusters;
   - `aeg-d-dwarfs/v1`, 64 plotted dwarf galaxies.

   Both are on the site and in the v0.1 release. Claude found the omission while building the Reproduction page, about half an hour after D-081 was merged.
2. **The fix.**
   - A new version: `docs/audit/AUDIT_PLAN_v2.md` and `docs/audit/sample_v2.py`, frozen by hash in `data/frozen/audit-plan-v2.json`.
   - It adds the two packages, with 10 rows each under the existing rule (5 %, minimum 10). The sample becomes 254 rows.
   - Nothing else changes.
   - Version 1 is kept unchanged and marked superseded.
3. **The seed** follows version 2: the first beacon pulse at least 24 hours after the merge that freezes version 2.
   - No seed had been read under version 1, and the 24 hours had not passed. So no sample existed, and nothing could have been steered.

**Reason.**
- An audit that left out a third of the shipped datasets would not support the claim it is meant to support.
- Fixing it before the seed exists costs nothing in independence. Fixing it after the draw would.

**Data seen.** Row counts of the two packages (64 default rows each). The v2 draw script was run once with the dummy seed "00", to check the counts.

## D-083 — Error budget: three-scale error model, in two phases

**Ruling (2026-11-01 19:10 CST, JvH).** "Rule as recommended." **Proposed by** Claude (2026-11-01; `docs/plans/ERROR_BUDGET_OPTIONS.md`, with the analysis given in conversation). **Adopted.**

1. **Option B.**
   - Every uncertainty is assigned one scale:
     - **point:** one measurement;
     - **system:** every point of one galaxy, cluster or lens;
     - **dataset:** every system in a dataset.
   - Error bars carry point-scale terms only.
   - System-scale terms are shown as a shift of the whole system along the direction the term actually moves it. For example, distance moves g_obs and g_bar together.
   - Dataset-scale terms are the sliders.
   - Terms are added only where a source publishes them. Where none does, the figure says "not given by the source".
   - Physical assumptions (equilibrium, hydrostatic balance, deprojection) stay named assumptions and are never folded into error bars.
   - Option C (Monte Carlo realisations) stays on the backlog.
2. **Phase 1 (no new data).**
   - Data standard 2.2.0 defines the scales, the axes each term moves, and the column contents. It is frozen before any building.
   - Then the site:
     - point-scale bars;
     - the whole-system shift view;
     - gap labels;
     - the KiDS flag wording (#64).
3. **Phase 2 (terms from sources).**
   - A new version of each package, in this order: SPARC, KiDS-1000, X-COP, dwarfs, globular clusters, strong lensing.
   - Each version's reproduction test is frozen first. It **must require g_obs and g_bar to equal the previous version's values exactly**, so that only uncertainty columns change.
   - This keeps the frozen audit (D-081, D-082), which samples the v1 rows, valid for both versions.
   - The v1 packages stay published and unchanged.
4. **Scope.** All six shipped datasets, for v0.2.
5. **X-COP profile covariance.** Ask the X-COP team for it in the courtesy note. It improves a shipped dataset and is not new-dataset work under D-080.

**Reason.**
- The size of the intrinsic scatter about the g_obs–g_bar relation is the most contested quantitative question this Atlas describes. Drawing a shared (system- or dataset-scale) uncertainty as an independent bar on every point, or adding correlated terms as if independent, changes how much scatter appears to be explained by errors. Getting the error structure right is therefore a neutrality requirement, not presentation.
- Option A labels the flaw but leaves it in the figures. Option C requires distribution shapes that most sources do not give.

**Data seen.** Error-column descriptions and median errors of the shipped packages (`ERROR_BUDGET_OPTIONS.md` §3). No source re-read.
