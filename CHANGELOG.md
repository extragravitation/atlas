# Changelog

All notable changes to the Atlas are recorded here. Site releases (v0.1, …) are numbered separately from dataset versions (see `docs/decisions.md`, D-006 and D-010).

## Unreleased

- Frozen: the D-037 reproduction check and the D-038 3A consistency check, tested on synthetic data (`docs/methods/D037_D038_CHECKS.md`).
- D-040: blind rulings replaced by recording who proposed each ruling (JvH or Claude) and what was changed before it was ruled (amends D-031).
- D-036 (ii) conversion frozen: light-weighted dispersion from binned profiles with the 80% light-coverage rule, tested on synthetic profiles (`docs/methods/D036_CONVERSION.md`); repository check that frozen files keep their hashes.
- D-039: stellar mass-to-light ratio for star clusters and dwarf galaxies (one model family; per-system defaults; wide asymmetric ranges; counted masses as a cross-check).
- Selection protocol deposited on Zenodo: DOI 10.5281/zenodo.23780203.
- Citation metadata: author affiliation and ORCID in `CITATION.cff`; `.zenodo.json` for Zenodo releases.
- D-025, D-036, D-037: dispersion method for v1.0 (half-light estimator; light-weighted profiles at 80% coverage; published dispersions with a frozen reproduction check); who belongs in the globular-cluster cell. Search logs for A0, A3 and A5 with the ADS step; deviations register (`docs/plans/DEVIATIONS.md`).
- Preview 2 of the site (D-030, D-032): lenses on the map (acceleration, excess, mass, scale, speed; surface density pending standard 2.0), an As measured panel on system pages and the KiDS dataset page, the matter counted in g_bar, Coverage page rendered from the taxonomy, Accounts and tests page with the open test ledger procedure, a page for data providers, methods and about rewritten to the cause-agnostic, reference-explicit stance, a pre-release banner on every page and no search-engine indexing. The site is built by wrangler's custom build step.
- D-028 to D-032: taxonomy and selection protocol, data standard 2.0 (observables first), layers and lenses, process safeguards, outside review when v1.0 is complete. Methodology review by two independent AI sessions (`docs/reviews/`).
- Site first pass (Astro, static): map, scale strip, 187 system pages with the pull budget, systems index, dataset pages with validation panels, Known issues (D-020), Methods, About, Data, downloads (ECSV and CSV per table). Both reading layers on every page; dark and light themes; assumption state in the page address. New check `aeg.site_check`: every served value equals the package table, downloads are byte-identical, internal links resolve, reading layers are paired. Hosting now serves `site/dist`.
- KiDS-1000 RAR package (`aeg-d-kids1000-rar/v1`); reproduction PASSED. D-021: KiDS stellar-mass systematic stated in words, no band.
- Slider formula engine in Python and JavaScript with a build check that they agree on every measurement (D-014); assumption registry with SPARC entries; standard validator; data standard 1.2.1 (clarifications).
- D-019 (shipping rule when a reproduction test fails) and D-020 (Known issues page); data standard 1.2.0; first known issue #8 (SPARC).
- Data standard 1.1.0 (D-018). SPARC package in progress: reproduction test failed on first run, recorded; test implementation bug corrected (D-016); discrepancies referred to the maintainer (D-017).
- Data standard v1.0.0 frozen (D-015); master plan v2 and MVP plan v2; D-013 and D-014 ruled.
- Source readings for SPARC, KiDS-1000 and X-COP (`docs/sources/`).
- Hosting moved from Cloudflare Pages to Cloudflare Workers static assets (`wrangler.jsonc`); D-007 amended.
- In-preparation placeholder page (`site/public/index.html`).
- Repository skeleton: licences, citation file, decision log, system-ID registry, identifier checks, automated checks.
