# Search log: A5·random (dwarf spheroidal and ultra-faint dwarf galaxies × random motions)

> Run on 2026-10-29 after the protocol freeze (see `docs/plans/DEVIATIONS.md` #1 and #2). The run calls itself "pre-freeze" or "exploratory" below because the protocol's status line had not been updated; the freeze record is authoritative. ADS and VizieR steps pending (deviation #2). AI-run (Claude); metadata only.

- **Date run:** 2026-10-29
- **Protocol:** `docs/plans/SELECTION_PROTOCOL.md` (draft, D-028), §1, §1a, §2 (A5·random row), §3, §4. **The protocol was not yet frozen when this search was run** (see Open question 1).
- **Run by:** Claude (AI-assisted), for JvH. Every statement below was read at source in this session via WebSearch/WebFetch at the URL given. "Unverified" means not confirmed at source in this session. Nothing from memory.
- **Blinding:** eligibility decided from metadata, data documentation, abstracts and methods sections only. No data table was downloaded, no g_obs or g_bar was computed or plotted, and no result about the acceleration discrepancy was read for or recorded in this log. Where a fetched page summary volunteered a conclusion, it was not recorded. Several records found are result papers about the acceleration discrepancy or its accounts; they are logged by title and screened on their data and methods only.
- **Tool limits that affected the procedure:** ADS (ui.adsabs.harvard.edu and api.adsabs.harvard.edu), the VizieR query interface (vizier.cds.unistra.fr/viz-bin/VizieR), CDS ReadMe files fetched directly, GitHub directory and release pages, and the GitHub API were **not reachable** from this session (allowlist / proxy 403). §3 steps 1 and 2 were therefore run as web searches with the query strings recorded below. VizieR catalogue metadata was read through the GAVO registry mirror (dc.g-vo.org) and the cdsarc directory listing where search results exposed those URLs. **§3 steps 1 and 2 are not complete as the protocol specifies** and should be re-run with ADS and VizieR access.

## 1. Queries (verbatim, 2026-10-29)

| # | Step (§3) | Where run | Query string (verbatim) |
|---|---|---|---|
| Q1 | 1 (ADS, substitute) | WebFetch of ui.adsabs.harvard.edu | `abs:"dwarf spheroidal" abs:"velocity dispersion" property:refereed`, sort date desc. **Failed: URL not on allowlist.** |
| Q2 | 1/2 | curl to api.adsabs.harvard.edu and vizier.cds.unistra.fr | **Failed: proxy CONNECT 403.** |
| Q3 | 2 (VizieR) | WebFetch of vizier.cds.unistra.fr/viz-bin/VizieR?-words=dwarf+spheroidal+velocity+dispersion | **Failed: URL not on allowlist.** |
| Q4 | 4 | WebSearch | `Local Volume Database Pace dwarf galaxies velocity dispersion catalog documentation` |
| Q5 | 2 (substitute) | WebSearch | `VizieR catalogue dwarf spheroidal velocity dispersion stellar radial velocities` |
| Q6 | 1 (substitute) | WebSearch | `ultra-faint dwarf galaxy velocity dispersion data release catalogue refereed` |
| Q7 | 3 | WebSearch | `zenodo local_volume_database apace7 release` |
| Q8 | 4 | WebSearch | `local volume database flux_HI upper limit dwarf_mw yaml column description` |
| Q9 | 4 (gas) | WebSearch | `Putman 2021 gas content stripping Local Group dwarf galaxies HI upper limits satellites` |
| Q10 | 4 (gas) | WebSearch | `Spekkens 2014 HI non-detections dwarf spheroidal satellites gas upper limits` |
| Q11 | 4 | WebSearch | `Walker 2023 comprehensive catalog stellar velocities Milky Way dwarf spheroidal M2FS ApJS` |
| Q12 | 4 | WebSearch | `McConnachie 2012 observed properties dwarf galaxies Local Group updated catalogue velocity dispersion` |
| Q13 | 4 | WebSearch | `Simon 2019 faintest galaxies review table velocity dispersion ultra-faint Milky Way satellites` |
| Q14 | 4 (M31) | WebSearch | `Collins 2013 kinematic study Andromeda dwarf spheroidal system velocity dispersions DEIMOS` |
| Q15 | 4 (M31) | WebSearch | `Tollerud 2012 SPLASH survey Andromeda dwarf spheroidal kinematics VizieR J/ApJ/752/45` |
| Q16 | 4 (M31 baryons) | WebSearch | `Martin 2016 PAndAS structural parameters Andromeda dwarf galaxies half-light radius luminosity catalogue` |
| Q17 | 4 (MW baryons) | WebSearch | `Munoz 2018 uniform analysis structural parameters Milky Way outer halo satellites globular clusters dwarf galaxies Megacam VizieR` |
| Q18 | 4 | WebSearch | `Walker 2009 universal mass profile dwarf spheroidal galaxies velocity dispersion profiles table` |
| Q19 | 4 | WebSearch | `Júlio 2025 A&A 704 A330 dwarf galaxies acceleration profiles Jeans` |
| Q20 | 3 (Zenodo) | WebSearch | `zenodo dwarf spheroidal galaxy velocity dispersion data` |
| Q21 | 3 (GitHub) | WebSearch | `github ultra-faint dwarf galaxies velocity dispersion catalog data` |
| Q22 | 3 (Zenodo) | WebSearch | `zenodo ultra-faint dwarf galaxy stellar radial velocities member catalogue` |
| Q23 | 4 | WebSearch | `Cerny 2026 chemodynamical census Milky Way ultra-faint compact satellites internal kinematics 19 arXiv` |
| Q24 | 2 (substitute) | WebSearch | `dc.g-vo.org VizieR Simon Geha 2007 kinematics ultra-faint Milky Way satellites J/ApJ/670/313` |
| Q25 | 2 (substitute) | WebSearch | `Walker Mateo Olszewski 2009 stellar velocities Carina Fornax Sculptor Sextans MMFS VizieR J/AJ/137/3100` |
| Q26 | 2 (substitute) | WebSearch | `Kirby 2014 dynamics dwarf galaxies Local Group isolated DEIMOS velocity dispersions VizieR` |
| Q27 | 4 | WebSearch | `Tolstoy 2023 VLT FLAMES Sculptor dwarf spheroidal 1604 members radial velocities VizieR` |
| Q28 | 4 | WebSearch | `Heiger 2024 binary stars ultra-faint dwarf galaxies multi-epoch velocity dispersion` |
| Q29 | 4 | WebSearch | `MUSE-Faint survey ultra-faint dwarf galaxies stellar kinematics Zoutendijk velocity dispersion data release` |
| Q30 | 4 (review) | WebSearch | `Battaglia Nipoti 2022 stellar dynamics dwarf galaxies review Nature Astronomy compilation` |
| Q31 | 4 (method) | WebSearch | `Wolf 2010 accurate masses dispersion-supported galaxies half-light radius estimator arXiv 0908.2995` |
| Q32 | 3 (Zenodo) | WebSearch | `"local_volume_database" zenodo 10.5281/zenodo.14076714` |
| Q33 | 4 (M31) | WebSearch | `Andromeda satellites velocity dispersions compilation Keck DEIMOS 2020s M31 dwarf spheroidal kinematics catalogue` |
| Q34 | 4 | WebSearch | `Spencer 2018 Draco multi-epoch binary velocity dispersion MMT Hectochelle` |

Q28 did not return the targeted Heiger et al. 2024 paper; it is cited by the LVDB paper (§3.5) but was not read in this session (unverified).

## 2. Records screened

Decision codes: **E** eligible (or eligible as one side of a pairing); **E-c** conditionally eligible, pending a named ruling; **X** excluded; **NS** identified but not screened beyond the search-result title (insufficient time or access; to be screened in the re-run). Rule references are to SELECTION_PROTOCOL §1, §1a, §2.

### 2a. Compilations (both sides per system)

| # | Record | Source read | Decision | Protocol reason |
|---|---|---|---|---|
| R1 | Pace, Local Volume Database (LVDB), OJAp 8, 142 (2025), arXiv:2411.07424; repo github.com/apace7/local_volume_database; Zenodo concept DOI 10.5281/zenodo.14076714; v1.0.5 DOI 10.5281/zenodo.15476348 | https://github.com/apace7/local_volume_database ; https://local-volume-database.readthedocs.io/en/stable/usage.html ; https://arxiv.org/html/2411.07424v2 ; https://www.research.ed.ac.uk/en/datasets/apace7localvolumedatabase-v105/ | **E** (tier 1, compilation) | §1.1 both sides (vlos_sigma with _em/_ep/_ul; M_V; rhalf; ellipticity); §1.2 tier 1 (CSV/FITS/ECSV releases); §1.4 CC0-1.0; §1.6 distance_modulus per system; §1.5 compilation: every value carries a reference, so independence is resolved per value. §1.7 gas: mass_HI column exists, but HI upper limits not documented, so gas status needs a pairing (R29). |
| R2 | McConnachie 2012, AJ 144, 4 (arXiv:1204.1562); CADC "Local Group and Nearby Dwarf Galaxies" (FITS, Jan 2021 file) | https://www.arxiv.org/pdf/1204.1562 ; https://www.cadc.hia.nrc-cnrc.gc.ca/en/community/nearby | **E** (tier 1, compilation; not default) | §1.1 both sides (Table 4 σ*, Table 3 M_V, r_h, ellipticity; Table 2 distance modulus); §1.7 states HI as zero where a non-detection limit is small (quote below). §4: superseded for default view by R1 (fewer systems, last update Jan 2021, older values). Terms: citation request only. |
| R3 | Battaglia & Nipoti 2022, "Stellar dynamics and dark matter in Local Group dwarf galaxies" (arXiv:2205.07821; journal per search-result title Nature Astronomy 6, 659, unverified at source) | https://ar5iv.arxiv.org/html/2205.07821 | **X** for default; record kept | §1.2 tier 2 only (printed Table 1, 81 dwarfs; Table 2 σ upper limits); no data release. Values duplicate original measurements available at tier 1 via R1 (§1.5 duplicate/compilation). Useful cross-check for transcription. Gas statement recorded below. |
| R4 | Walker et al. 2009, ApJ 704, 1274, "A universal mass profile for dwarf spheroidal galaxies?" (arXiv:0906.0341) | https://ar5iv.arxiv.org/html/0906.0341 | **X** | §1.5 compilation of global σ and R_h (Table 1, per-row references not separated by quantity); duplicates originals in R1. Profiles in figures only, and tier 1 velocities exist for the same systems (R6) so §1a bars tier 3. |
| R5 | Simon 2019, ARA&A, "The Faintest Dwarf Galaxies" (arXiv:1901.05465); MW satellite table dwarf_tab_ascii_14sep2018.dat | https://users.obs.carnegiescience.edu/jsimon/data.html ; https://ned.ipac.caltech.edu/level5/Sept18/Simon/Simon_contents.html ; https://ned.ipac.caltech.edu/level5/Sept18/Simon/Simon5.html | **X** for default; record kept | §1.5 compilation superseded by R1 for the same systems; §1.4 no terms stated ("making generally available"). Table columns unverified. Source of gas statements (below). |

### 2b. Original kinematic measurements (observed side)

| # | Record | Source read | Decision | Protocol reason |
|---|---|---|---|---|
| R6 | Walker, Mateo & Olszewski 2009, AJ 137, 3100 (arXiv:0811.0118); VizieR J/AJ/137/3100 (DOI 10.26093/cds/vizier.51373100) | https://export.arxiv.org/abs/0811.0118v1 ; https://experts.arizona.edu/en/datasets/radial-velocities-of-4-dsph-galaxies/ ; https://ar5iv.labs.arxiv.org/html/astro-ph/0703284 (data-reduction companion) | **E-c** (tier 1, individual velocities) | §1.1 observables are individual stellar velocities (8 855 spectra, 7 103 red-giant candidates, Carina, Fornax, Sculptor, Sextans), not a dispersion. §2 requires a dispersion: eligible only if the Atlas derives dispersions (D-025 extension, Open question 3), or as the original behind R1 values. Baryonic side by pairing (R1/R32). Terms: VizieR, unread. |
| R7 | Walker et al. 2023, ApJS 268, 19 (arXiv:2312.12738); VizieR J/ApJS/268/19; spectra Zenodo 10.5281/zenodo.7837922 | https://arxiv.org/pdf/2312.12738 ; https://cdsarc.cds.unistra.fr/ftp/J/ApJS/268/19 ; https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/ApJS/268/19 | **E-c** (tier 1, individual velocities) | As R6: per-epoch velocities and membership for 16 369 targets toward 38 dSphs and faint clusters; per-system dispersions not reported in the paper (per excerpt). Repeat-epoch outlier model absorbs binaries. ReadMe (table1/table2 contents) unread: whether table2 holds per-system summaries is unverified. Terms unread. |
| R8 | Simon & Geha 2007, ApJ 670, 313 (arXiv:0706.0516); author files on Simon data page | https://arxiv.org/abs/0706.0516v2 ; https://users.obs.carnegiescience.edu/jsimon/data.html | **E-c** (tier 1 velocities; dispersion table unverified) | 8 ultra-faint dwarfs, Keck/DEIMOS, 18 to 214 stars each. Velocity files public; no terms stated (§1.4: link, do not redistribute). Whether per-galaxy σ is tabulated: unverified. |
| R9 | Tollerud et al. 2012, ApJ 752, 45 (SPLASH; arXiv:1112.1067); VizieR J/ApJ/752/45 | https://ar5iv.arxiv.org/html/1112.1067 ; https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/ApJ/752/45 (from search) | **E** (observed side; tier 2 for σ, tier 1 for velocities) | 15 M31 dSphs. Table 3 gives per-galaxy σ (ML, membership-weighted, p>0.1, 2.2 km/s systematic floor; Shapiro–Wilk test for Gaussianity, binaries discussed) and M_V; distances in Table 3 (derivation not read). Half-light radii from a companion paper (Beaton et al.), unverified. |
| R10 | Collins et al. 2013, ApJ 768, 172 (arXiv:1302.6590; journal ref unverified) | https://www.arxiv.org/pdf/1302.6590 | **E** (observed side, tier 2 for σ; Table 3 velocities machine-readable) | 18 M31 dSphs measured (11 new, 6 re-analysed); Table 4 per-galaxy σ (ML, membership probability); systems with <8 members flagged. Table 5 merges with other studies (compilation, §1.5). Table 1 structural parameters and distances (Conn et al. 2012) from cited papers. Overlaps R9 for several systems: precedence by §4. |
| R11 | Kirby et al. 2014, MNRAS 439, 1015 (arXiv:1401.1208); VizieR J/MNRAS/439/1015 | https://ar5iv.arxiv.org/html/1401.1208 ; https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/MNRAS/439/1015 (from search) | **X** for 6 of 7; **E-c** for Cetus | 7 isolated Local Group dwarfs; text calls NGC 6822, VV 124, Pegasus dIrr (out of kind for A5; gas-rich, belong elsewhere), Cetus a dSph; types of Leo A, IC 1613, Aquarius not stated in the text read. §1.7: no HI statement in the paper for these systems; gas would need pairing. Table 3 gives σ, L_V, R_h, distance. |
| R12 | Tolstoy et al. 2023, A&A, Sculptor VLT/FLAMES (arXiv:2304.11980) | https://pdf.arxiv.org/pdf/2304.11980 | **E-c** (tier 1 velocities at CDS) | 1 604 members with v_los; dispersion versus radius only as binned points in figures (Figs. 20–21); tables E.1/E.2 at CDS. Tier 3 barred by §1a because tier 1 velocities exist. Binaries deferred to later work. |
| R13 | Jenkins et al. 2021, ApJ 920, 92 (VLT spectroscopy of UFDs I: Boötes I, Leo IV, Leo V); VizieR J/ApJ/920/92 | https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/ApJ/920/92 | **E-c** | Reprocessed VLT/GIRAFFE archival velocities; reports refined dispersions for Boötes I and Leo IV and binaries identified (abstract). VizieR lists table6 only; contents unread. |
| R14 | Zoutendijk et al. 2021, A&A 651, A80 (MUSE-Faint II, Eridanus 2) | https://www.aanda.org/articles/aa/pdf/2021/07/aa40239-20.pdf | **E** (observed side: binned profile, tier 2; per-star velocities Table A.1) | Table 2: binned σ with radii; Table A.1: per-star velocities. No HI statement for Eri 2 (§1.7: pairing with R29 needed). © ESO 2021; licence not stated. |
| R15 | Vitral et al. 2024, HSTPROMO Draco data, Zenodo 10.5281/zenodo.11111113 | https://zenodo.org/records/11111113 | **E** (observed side, tier 1, CC0) | DRACO_BINS: binned dispersion and rotation behind Fig. 11 (proper-motion based); DRACO_STARS: proper motions; links to R7 IDs. A plane-of-sky dispersion profile: a different observable from line-of-sight σ; how the Atlas uses it depends on D-025. Paper itself not read (unverified). |
| R16 | Cerny et al. 2026, arXiv:2602.17652 (preprint), "Chemodynamical census of the MW's ultra-faint compact satellites I"; Zenodo 10.5281/zenodo.18612486 (v1.0), 10.5281/zenodo.18688283 (v1.1) | https://arxiv.org/abs/2602.17652 ; https://zenodo.org/records/18688283 ; https://zenodo.org/records/18612486 | **E-c** (tier 1 member catalogs, CC BY 4.0) | 19 compact systems (r_h ~1–15 pc); σ for 15, "mostly upper limits"; 17 member catalogues released. Refereed status unverified. **Kind ambiguous** (star cluster vs dwarf): see Open question 4. v1.0 and v1.1 are versions of one record (count once). |
| R17 | Walker et al. 2007, "Velocity dispersion profiles of seven dSphs" (arXiv:0708.0010) | https://ar5iv.arxiv.org/html/0708.0010 | **X** | Profiles in figures only (tier 3), and tier 1 velocities exist for the same systems (R6 and others): §1a. No data release stated. |
| R18 | Júlio et al. 2025, A&A (arXiv:2510.06905), 12 dwarfs | https://arxiv.org/pdf/2510.06905 | **X** | No data availability statement; figures only (tier 3), and tier 1 velocities exist for the same systems: §1a. Also: observed side model-derived through a mass model with an assumed halo-type profile and a baryonic-mass prior (would need `model_dependence`); gas given for Antlia B and Leo T only, dSph gas omitted without statement (§1.7). Only data and methods sections read. |
| R19 | Zenodo 10.5281/zenodo.18538840, supplement to "Velocity dispersion profiles of dSphs with self-interacting ultralight dark matter" | https://zenodo.org/records/18538840 | **X** | §1.1/§1.2: a model supplement PDF, not released measurements; no licence. Also names an account (out of scope for data). |
| R20 | Kleyna et al. 2002, Draco radial velocities, VizieR (2002yCat..73300792K) | search result only | **NS** | Original velocities, Draco; superseded? unverified. |
| R21 | "Radial velocities of stars near Leo I" (Arizona dataset record; Mateo et al. 2008 per R18's citation) | search result only | **NS** | |
| R22 | "Radial velocities in Fornax dSph" (Arizona dataset record) | search result only | **NS** | |
| R23 | "Radial velocities of stars in Boötes I", VizieR J/ApJ/736/146 | search result only | **NS** | |
| R24 | Spencer et al. 2017, Leo II binary fraction (arXiv:1706.04184); Spencer et al. 2018, Draco and Ursa Minor binary fraction (arXiv:1811.06597) | search results only | **NS** | Cited by R18 as velocity sources for Leo II and Draco. |
| R25 | Collins et al. 2010, Keck/DEIMOS faint M31 satellites And IX, XI, XII, XIII; Andromeda II stellar kinematics (arXiv:1209.2116); M31 dSph elemental abundances and kinematics (Caltech record 100637); And VI and And XXIII mass modelling (arXiv:2505.04475) | search results only | **NS** | M31 originals; likely in R10's Table 5 compilation (unverified). |
| R26 | MUSE-Faint further papers (arXiv:2101.00253, 2308.16263, 2603.02643) | search results only | **NS** | |
| R27 | Tucana II extended structure (arXiv:2012.02309); "Stellar kinematics of dwarf galaxies from multi-epoch spectroscopy: Triangulum II" (HAL insu-03699423) | search results only | **NS** | |
| R28 | HSTPROMO Sculptor (arXiv:2508.20711) | search result only | **NS** | Likely a proper-motion profile like R15; check for a Zenodo release. |

### 2c. Baryonic-side and gas datasets (for pairing, §1.1)

| # | Record | Source read | Decision | Protocol reason |
|---|---|---|---|---|
| R29 | Putman et al. 2021, ApJ 913, 53 (arXiv:2101.07809); VizieR J/ApJ/913/53 (DOI 10.26093/cds/vizier.19130053) | https://iopscience.iop.org/article/10.3847/1538-4357/abe391 ; https://ar5iv.arxiv.org/html/2101.07809 ; https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/ApJ/913/53 | **E** (gas side, tier 1) | §1.7: measured HI limits (5σ, 10 km/s width) or detections for 119 dwarfs within 2 Mpc; machine-readable Tables 1–3; article CC BY 4.0 (VizieR terms unread). Satisfies "absent with a measured upper limit". |
| R30 | Grcevich & Putman 2009, ApJ (arXiv:0901.4975) | https://ar5iv.arxiv.org/html/0901.4975 | **X** (superseded) | Same quantity and largely the same systems as R29, older surveys (HIPASS, LAB); §4 precedence to R29; keep as reference for limits. |
| R31 | Martin et al. 2016, ApJ 833, 167, PAndAS II, 23 M31 dSphs (arXiv:1610.01158); VizieR J/ApJ/833/167 | https://ar5iv.arxiv.org/html/1610.01158 | **E** (baryonic side, tier 1) | Table 1 structure (ellipticity, r_h), Table 2 M_V and luminosity; TRGB distances (Conn et al. 2012a) marginalised; MCMC chains released. No gas statement (gas from R29). Terms unread. |
| R32 | Muñoz et al. 2018, ApJ 860, 65/66, MegaCam outer-halo satellites III (arXiv:1806.06891); VizieR J/ApJ/860/65 | search result (ReadMe URL https://cdsarc.cds.unistra.fr/VizieR/ftp/J/ApJ/860/65/ReadMe, not fetched) | **E-c** (baryonic side; unverified) | MW satellites structural parameters; contents, licence and the exact VizieR id (860/65 vs 860/66) unverified. |

### 2d. Method, review and result papers (not data)

| # | Record | Source read | Decision | Protocol reason |
|---|---|---|---|---|
| R33 | Wolf et al. 2010, MNRAS (DOI 10.1111/j.1365-2966.2010.16753.x; arXiv:0908.2995) | https://arxiv.org/abs/0908.2995v4 | **X** (method source) | Not a dataset. Estimator M_1/2 = 3σ²_los r_1/2 / G ≈ 4σ²_los R_eff / G, "mild assumptions" on anisotropy, from the spherical Jeans equation. Input to D-025. |
| R34 | McConnachie & Côté 2010, binaries and dispersions in ultra-faint systems (arXiv:1009.4205) | https://ar5iv.arxiv.org/html/1009.4205 | **X** | Methods (Monte Carlo of binary inflation); compiles published σ (§1.5 duplicate). Relevant to binary caveats. |
| R35 | "One Law To Rule Them All: The Radial Acceleration Relation of Galaxies" (arXiv:1610.08981) | search result only (title) | **X** | Result paper; dSph values compiled from originals (§1.5 duplicate). Not read, by design. |
| R36 | "The Challenge to MOND from ultra faint dwarf galaxies" (arXiv:2104.13961) | search result only (title) | **X** | Result paper on one account; compilation (§1.5). Not read, by design. |
| R37 | "Densities and mass assembly histories of the Milky Way satellites are not a challenge to ΛCDM" (arXiv:2306.08674) | search result only (title) | **X** | Result paper on one account (§1.5). Not read. |
| R38 | Collins et al. 2014, "The masses of Local Group dSphs: the death of the universal mass profile" (arXiv:1309.3053) | search result only | **X** (tentative) | Compilation/result paper (§1.5); not read. |
| R39 | "Solo dwarfs IV: satellite and isolated dwarf galaxies in the Local Group" (arXiv:2106.12649) | search result only | **NS** | Possible compilation (Higgs et al.); check for released tables. |
| R40 | Simon et al. 2018, Gaia proper motions of ultra-faint satellites (arXiv:1804.10230) | search result only | **X** | Systemic proper motions, not internal dispersion (§2). |
| R41 | VizieR J/ApJS/100/105 "Stellar velocity dispersions. II" | search result only | **X** (tentative) | Title suggests galaxy central dispersions (1995), not dSph; unverified. |

## 3. Eligible datasets

### E1. Local Volume Database (LVDB), Pace (R1). Recommended default for the observed and stellar sides
- **Citation:** Pace, A. B. 2025, OJAp 8, 142, DOI 10.33232/001c.144859, arXiv:2411.07424 (v2 2025-09-25); repository https://github.com/apace7/local_volume_database ; Zenodo concept DOI 10.5281/zenodo.14076714; v1.0.5 DOI 10.5281/zenodo.15476348 (2025-05-20). The latest release tag is **unverified** (GitHub releases page unreachable); README says the version is in `code/release_version.txt`. Users are asked also to cite the input reference of every value used.
- **Tier:** 1 (combined catalogues `dwarf_mw`, `dwarf_m31`, `dwarf_local_field`, `dwarf_local_field_distant`, `dwarf_all`, `comb_all`; CSV, FITS, ECSV on GitHub releases).
- **Observed side:** `vlos_sigma`, "velocity dispersion in line-of-sight [km/s]"; YAML: "stellar velocity dispersion … Sometimes called the global velocity dispersion"; errors `_em`/`_ep` (16th/84th percentile); `_ul` "upper limit at 95% confidence/credible interval" (docs note some use other levels). One value per system; **radius of measurement not stated** (global). No profiles. Reference column `ref_vlos`. Membership and binary treatment are those of each original paper; the LVDB paper (§3.5) flags unresolved binaries as a systematic for ultra-faints ("can have incorrect inferred velocity dispersions if there are unidentified binary stars included"). The rule for choosing among several published dispersions for one system is **not documented** in the pages read.
- **Baryonic side:** `apparent_magnitude_v` (extinction-corrected), `M_V`; `rhalf` = "projected (2D) semi-major axis of the half-light ellipse" [arcmin], `rhalf_physical` [pc], `rhalf_sph_physical` (azimuthally averaged, geometric mean); `ellipticity` = 1 − b/a; `mass_stellar` = "log10 stellar mass assuming M/L=2 and computed from M_V" (fixed assumption; the Atlas would use M_V with its own registered M/L). Gas: `mass_HI` (from `flux_HI` and distance); paper §3.8: "The primary HI property cataloged in the LVDB are the HI flux"; HI **upper limits not documented**. Gas status therefore needs pairing with E2.
- **Distance:** `distance_modulus` per system, `distance` [kpc], `ref_distance`. Caveat (paper §4): some systems "inherit the distance and errors of their host galaxy. This is not denoted in the combined catalogs."
- **Licence:** CC0-1.0 (repository licence, read on the GitHub page). The arXiv paper states no licence.
- **Number of systems:** **unverified** (counting requires opening the tables, not done). Paper §3.1: MW dwarf census "at least 65", "over 30 satellites without a secure classification"; complete for known dwarfs to ~3 Mpc (abstract) / 6 Mpc (docs). MW and M31 counts with a measured σ: unverified.
- **Independence:** a compilation. Values trace to the originals per `ref_*` columns. Sources cited in §3.5 for dispersions: Walker et al. 2009a, 2023; Fabrizio et al. 2016; Pace et al. 2020; Simon & Geha 2007; Martin et al. 2007; Koposov et al. 2015; Jenkins et al. 2021; Heiger et al. 2024; Tolstoy et al. 2023; Kirby et al. 2014; Danieli et al. 2019; Fahrion et al. 2020; Müller et al. 2021; Nidever et al. 2024 (the mapping of value to reference is per row and was not read). R2, R3, R4, R5 duplicate it; R6–R14 are among its originals.
- **Rulings it depends on:** D-025 (σ to g_obs: the LVDB itself uses Wolf et al. 2010 for dynamical masses, which is not a ruling for the Atlas); stellar M/L for dwarfs (replaces the fixed M/L = 2); rhalf convention (semi-major versus azimuthally averaged) inside D-025; treatment of `_ul` limits as limits (§2).

### E2. Putman et al. 2021 HI content (R29). Gas side for pairing
- **Citation:** Putman, M. E., Zheng, Y., Price-Whelan, A. M., Grcevich, J., Johnson, A. C., Tollerud, E., Peek, J. E. G. 2021, ApJ 913, 53, DOI 10.3847/1538-4357/abe391; VizieR J/ApJ/913/53, DOI 10.26093/cds/vizier.19130053.
- **Tier:** 1 (machine-readable Tables 1–3, per the journal page; VizieR).
- **Content:** HI detections or 5σ mass limits (assumed 10 km/s width; ~10 km/s Hanning smoothing; HI4PI for most, GALFA-HI DR1/DR2 where covered) for 119 dwarfs within 2 Mpc. Abstract: "Within the virial radius of the Milky Way (224 kpc here), 53 of 55 dwarf galaxies are devoid of gas"; "27 of 30 dwarf galaxies are devoid of gas" (M31). Ionised gas: "molecular and ionized gas are only detected in those galaxies with HI".
- **Distances:** mainly from McConnachie 2012 and Simon 2019 (per the paper).
- **Licence:** article CC BY 4.0 ("Creative Commons Attribution 4.0 licence", journal page); VizieR terms unread.
- **Systems:** 119 total; 55 within the MW virial radius; 30 within M31's.
- **Use:** lets dSph and ultra-faint gas be classed **absent with a measured upper limit** (§1.7, D-034), or **measured** where detected (e.g. transition systems). Supporting statements: Simon 2019 §5.3, "Stringent upper limits have been placed on the H i content of many of the UFDs" and "For the most nearby dwarfs these limits can be as small as ∼ 100 M⊙" (https://ned.ipac.caltech.edu/level5/Sept18/Simon/Simon5.html); McConnachie 2012: "I give the HI mass as zero" where a non-detection limit is small relative to the stellar mass (https://www.arxiv.org/pdf/1204.1562); Battaglia & Nipoti 2022: "the great majority of the LG DGs is devoid of gas" (https://ar5iv.arxiv.org/html/2205.07821); Grcevich & Putman 2009: "The majority of dwarf galaxies within ~270 kpc of the Milky Way or Andromeda are undetected in HI" (https://ar5iv.arxiv.org/html/0901.4975).

### E3. Martin et al. 2016, PAndAS II (R31). M31 stellar side
- Citation: Martin, N. F. et al. 2016, ApJ 833, 167 (arXiv:1610.01158); VizieR J/ApJ/833/167. Tier 1 (tables plus released MCMC chains, which the authors recommend over summary moments). 23 M31 dSphs. Ellipticity, r_h (angular and physical), M_V, log L; TRGB distances from Conn et al. 2012a, marginalised. No gas statement (pair with E2). Licence unread. Likely an input to E1 for M31 systems (independence per E1 `ref_structure`, unverified).

### E4. Original M31 dispersions: Tollerud et al. 2012 (R9) and Collins et al. 2013 (R10)
- R9: 15 M31 dSphs; σ in Table 3 (tier 2), velocities machine-readable (Table 2, tier 1; VizieR J/ApJ/752/45); method ML, membership-weighted. Licence unread.
- R10: 18 M31 dSphs measured; Table 4 σ (tier 2), Table 3 velocities machine-readable; flags for <8 members; Table 5 merges other studies (compilation part). Licence unread.
- Both overlap each other and E1 for several systems; precedence by §4 (deepest observables, then independence of reduction).

### E5. Profiles and per-star data for single systems
- **Zoutendijk et al. 2021 (R14):** Eridanus 2 binned σ profile (tier 2, Table 2) and per-star velocities (Table A.1). Gas: no statement in the paper; pair with E2 (Eri 2 coverage in R29 unverified). Distance per paper unverified. Licence: © ESO, not stated.
- **Vitral et al. 2024 Draco (R15):** proper-motion binned dispersion profile, CC0, tier 1. Observable differs (plane of sky); needs a D-025 statement on combining PM and line-of-sight dispersions. Baryonic side by pairing (E1).

### E-c. Conditionally eligible (each pending a named ruling)
- R6, R7, R8, R12, R13: tier 1 individual velocities. Eligible as observed-side observables only if JvH rules the Atlas may derive σ (global or binned) from released velocities, which would be a registered processing step (Open question 3). Otherwise they serve as the provenance behind E1 values.
- R11 (Cetus only), R16 (kind ruling), R32 (verification).

## 4. PRISMA counts (this run)

| Stage | Count | Notes |
|---|---|---|
| Records identified | 41 record entries (R1–R41), from 31 successful queries (3 failed) | Some entries group several papers (R24–R27); counted as entries. |
| Duplicates removed | 1 | R16 Zenodo v1.0 and v1.1, counted as one. |
| Screened on metadata/methods read at source | 24 | R1–R19, R29–R31, R33, R34. |
| Screened on search-result title only | 7 | R35–R38, R40, R41 (excluded); R32 (conditional, unverified). |
| Not screened (NS) | 10 | R20–R28, R39. To be screened in the re-run. |
| Excluded | 16 | R3, R4, R5 (compilation duplicates, kept as records); R11 (6 of 7 systems; Cetus stays conditional); R17, R18 (§1a); R19 (no data); R30 (superseded); R33, R34 (method); R35–R38, R40, R41 (result papers or out of kind). |
| Eligible | 8 | R1 (E1), R2 (record, not default), R9, R10, R14, R15, R29 (E2), R31 (E3). |
| Conditionally eligible | 8 | R6, R7, R8, R11 (Cetus), R12, R13, R16, R32. |
| Included | 0 | Inclusion awaits the protocol freeze, D-025, the M/L ruling and JvH's ruling on this log. |

## 5. Open questions (for JvH)

1. **Protocol not frozen.** §3 and TAXONOMY say the search starts after the protocol is frozen by hash. This run happened before the freeze. Options: (a) treat this run as exploratory and re-run after the freeze (recommended: a good scientist would not let a pre-freeze search define the cell); (b) freeze now and enter this run in the deviations register (§9) with "data seen: metadata only, no discrepancy results".
2. **ADS and VizieR unreachable.** §3 steps 1–2 were substituted by web searches. The re-run needs ADS (refereed, since 1990) and VizieR keyword search, and the CDS ReadMe files (J/ApJS/268/19, J/ApJ/913/53, J/ApJ/833/167, J/ApJ/860/65, J/ApJ/752/45) for column lists and terms.
3. **Velocities or dispersions.** §2 asks for a velocity dispersion. The deepest observables released are per-star velocities (R6, R7, R8, R12, R13). Should the Atlas compute dispersions (global, and binned profiles) from released velocities as a registered step? This belongs inside D-025 and decides whether the E-c records are included. It affects membership and binary handling, which would then be the Atlas's own choices.
4. **Kind assignment can carry the result.** Whether a faint compact system is a "dwarf" or a "star cluster" is often decided in the literature by its dispersion (dynamical mass) or metallicity spread. If the Atlas assigns A5 versus A3 using dispersion, the label carries the result (project rule 1). Proposal: assign kind by non-kinematic criteria only (morphology, size, metallicity spread) and keep ambiguous systems, such as the UFCSs in R16, in a flagged "ambiguous" group shown in both cells. Needs a ruling.
5. **One value per system in E1.** The LVDB's rule for choosing among several published dispersions is undocumented in the pages read. Ask the author, or keep all published values per system as named alternatives (§4 precedence).
6. **Upper limits.** E1 `_ul` are 95% limits "mostly"; some use other levels. Limits must stay limits (§2); the confidence level per row has to be recorded from the original.
7. **Gas status.** Proposal: dSph and ultra-faint gas = absent with measured limit from E2 (§1.7), measured where E2 detects HI; systems outside E2's 2 Mpc need another source or are ineligible. Coverage of E2 for each E1 system unverified.
8. **Distances inherited from hosts** in E1 are not flagged in the combined tables (paper §4); needs a per-system check against `ref_distance`.
9. **Licences unread** for all VizieR catalogues (R6, R7, R9, R13, R29, R31, R32) and for author-hosted files (R5, R8: no terms; link, do not redistribute).
10. **Rulings this cell depends on:** D-025 (estimator at a stated radius versus Jeans profiles, and the r_half convention); stellar M/L for dwarfs (defaults and ranges, read at source); whether to combine proper-motion and line-of-sight dispersions (R15); the dynamical-equilibrium statement for tidally affected systems (not yet collected per system).
