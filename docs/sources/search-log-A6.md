# Search log: A6 (early-type galaxies), starting with A6·strong lensing

> Protocol `docs/plans/SELECTION_PROTOCOL.md` (frozen at 817bc5a), §1, §1a, §2 (A6 rows), §3, §4; order of work §7 step 2 (A6, strong lensing first). Run by Claude (AI-assisted) for JvH. Every statement is read at source at the URL given; "unverified" means not confirmed at source. Nothing from memory.

**Blinding.** Eligibility is decided from metadata, abstracts, data documentation and methods sections only. No data table is downloaded, no g_obs or g_bar is computed or plotted, and no mass, mass-to-light ratio, dark-matter fraction or result about the acceleration discrepancy is read for or recorded in this log. Many strong-lensing papers are result papers about mass fractions or the IMF; they are screened on their data and methods only.

## 0. Plan, committed before any query is run (2026-10-31)

### 0a. What the A6·strong lensing row asks for (§2)

- **Observed side:** the mass within the Einstein radius (projected), from a lens model, with the model named.
- **Baryonic side:** stellar mass from photometry, with the IMF and the population model named.
- **Form:** a single aperture (projected).
- **§1.7 gas:** a component may be "absent" only if the source states it is negligible or gives a limit. The screener records whether each source says anything about gas inside the Einstein radius. If it doesn't, the dataset needs a pairing or a cited statement for the kind (deviation #4).
- **Projection ruling (§5):** needed before the first lensing package, not before the search.
- **Distances:** the lens and source redshifts are recorded per system (§1.6).

### 0b. Queries, verbatim (ADS, refereed, 1990–2026)

| # | Step (§3) | Query | Sort |
|---|---|---|---|
| ADS-A6S-1 | 1 | `abs:("strong lensing" OR "strong gravitational lensing" OR "strong lens" OR "strong lenses" OR "lens galaxies" OR "lensing galaxies") abs:("early-type" OR elliptical OR ellipticals) abs:("stellar mass" OR "stellar masses" OR "stellar population" OR "stellar populations" OR photometry) property:refereed year:1990-2026` | citations |
| ADS-A6S-2 | 1 | `abs:("Einstein radius" OR "Einstein radii") abs:("early-type" OR elliptical OR ellipticals) abs:(catalog OR catalogue OR sample OR survey OR "data release") property:refereed year:1990-2026` | citations |
| ADS-A6S-3 | 1 | `abs:("lens sample" OR "lens samples" OR "lens catalog" OR "lens catalogue" OR "sample of strong lenses" OR "galaxy-scale lenses" OR "galaxy-scale strong lenses") property:refereed year:1990-2026` | citations |
| VIZ-A6S | 2 (substitute, deviation #2) | `bibstem:yCat abs:("strong lensing" OR "gravitational lens" OR "gravitational lenses" OR "lens galaxies" OR "lens galaxy" OR "Einstein radius" OR "Einstein radii")` | date |
| ZEN-A6S | 3 | Zenodo search: `strong lens Einstein radius stellar mass` and `galaxy-scale lens catalogue` | — |
| GH-A6S | 3 | GitHub search: `strong lens catalog Einstein radius` | — |
| CIT-A6S | 4 | The data papers cited by eligible datasets, and recent reviews of galaxy-scale strong lensing found by the queries above. Starting lead: SLACS IX, Auger et al. 2009 (survey 2026-10-28). | — |

Queries are run as written. If one fails or returns nothing for a syntax reason, the replacement is recorded beside it, as in the A3 log.

### 0c. Screening

1. **Title and listing metadata**, by Claude: exclude other kinds (clusters, groups, quasars as sources only, discs), theory, simulations and methods, lens-finding papers with no lens models, time-delay cosmography with no stellar masses, papers with no new measurements.
2. **Full text**, by two independent AI readers to a written brief (`docs/sources/screening-brief-A6S.md`, committed before the readers start). They read the abstract, data statement, methods and observations, table captions and headings, and release pages only.
3. Counts in the style of a PRISMA flow, and a list of leads for the other A6 rows and other cells.

## 1. Queries run

Run 2026-10-31, 17:10–18:00 MDT, by Claude through JvH's signed-in Chrome (ADS, Zenodo) and the GitHub API from the workspace. Screening at this stage is on titles and listing metadata only; no abstract values, tables or figures were read.

| # | Query (as in §0b unless noted) | Where | Records |
|---|---|---|---|
| ADS-A6S-1 | as planned; sort citations | ui.adsabs.harvard.edu | 229 |
| ADS-A6S-2 | as planned | ui.adsabs.harvard.edu | 103 (39 also in ADS-A6S-1) |
| ADS-A6S-3 | as planned | ui.adsabs.harvard.edu | 536 (51 already seen). **Defect:** the query has no `collection:astronomy` filter, so most records are optics, spectroscopy and medicine ("lens sample"); they are excluded at title level as other subjects. Not re-run, so the plan stands as written. |
| VIZ-A6S | as planned; sort date | ui.adsabs.harvard.edu | 362 (mostly microlensing, lensed quasars and clusters) |
| ZEN-A6S | Zenodo API, `type=dataset`, sort best match: (a) `"strong lens" OR "strong lensing" OR "Einstein radius"`; (b) `"lens galaxies" stellar mass`; (c) `early-type lens Einstein radius catalogue` | zenodo.org/api/records, in Chrome | (a) 48; (b) 15 704 and (c) 27 231, unranked by relevance, so only the top 100 of each were scanned. Titles were filtered by a script to those containing "lens" or "Einstein" and not "simulat", "challenge", "neural", "machine learning", "training", "mock", "microlens", "weak lens", "cosmic shear", "cluster", "ML scores" or "deep learning". **This scripted title filter is a screening step and is disclosed here.** |
| GH-A6S | GitHub repository search: `strong lens catalog` (planned), plus `strong lens catalogue Einstein radius`, `lens galaxies stellar mass`, `galaxy-scale strong lenses data`, `SLACS lens` (added) | api.github.com | 7, 0, 0, 1, 9 |

**Display limit.** For ADS-A6S-2, -3 and VIZ-A6S, the listing script hid records with bibstems `PhDT`, `PhRv` and `AcASn` (theses and physics-journal papers). For ADS-A6S-1 these were shown: all were theses or result papers on gravity theories or dark-matter physics. The hidden records were not screened; they are regenerable by re-running the queries.

### 1a. Title-level screening

Excluded at title level: other kinds (clusters, groups, quasar hosts, discs and spirals, the Milky Way); other subjects (optics, laboratory spectroscopy, medicine, geology); microlensing; weak lensing; lensed-source studies (the lensed galaxy, not the lens); time-delay cosmography and lens statistics for cosmology; lens-finding papers with candidates only; theory, simulations and methods; result papers that re-use published lens models and stellar masses with no new measurement. Counted, not listed.

**Passed to full-text screening (R1–R59)** (paper and catalogue records grouped):

| # | Record(s) | What (from title) |
|---|---|---|
| R1 | 2006ApJ...638..703B | SLACS I: sample |
| R2 | 2006ApJ...640..662T | SLACS II: stellar populations and structure |
| R3 | 2006ApJ...649..599K | SLACS III |
| R4 | 2007ApJ...667..176G | SLACS IV: density profile to 100 Re (strong + weak) |
| R5 | 2008ApJ...682..964B; 2009yCat..16820964B | SLACS V: full ACS sample |
| R6 | 2009ApJ...690..670T; 2011yCat..16900670T | SLACS VIII: environment |
| R7 | 2009ApJ...705.1099A; 2011yCat..17051099A | SLACS IX: colours, lensing, stellar masses (survey lead) |
| R8 | 2010ApJ...724..511A | SLACS X: stellar, dynamical and total masses |
| R9 | 2015ApJ...803...71S | SLACS XII: lower masses |
| R10 | 2017ApJ...851...48S; 2019yCat..18510048S | SLACS XIII: 40 new lenses |
| R11 | 2024A&A...690A.325S; 2025A&A...697A..95S; Zenodo 10.5281/zenodo.13366012 | SLACS sample, debiased (I, II) |
| R12 | Zenodo 10.5281/zenodo.6104823 ("Automated galaxy-galaxy strong lens modelling: no lens left behind") | Uniform re-modelling of HST lens imaging |
| R13 | 2008A&A...477L..25G; 2009A&A...501..461G; 2009yCat..35010461G | Photometric masses of early-type lens galaxies |
| R14 | 2018ApJ...864...91S; 2019yCat..18640091S | Compilation of 128 galaxy-galaxy lenses |
| R15 | 2012ApJ...744...41B | BELLS I |
| R16 | 2012ApJ...757...82B | BELLS II |
| R17 | 2016ApJ...833..264S | BELLS IV: GALLERY lens models |
| R18 | 2012ApJ...761..170G | SL2S I |
| R19 | 2011ApJ...727...96R | SL2S II |
| R20 | 2013ApJ...777...97S | SL2S III: lens models, photometry, stellar masses |
| R21 | 2013ApJ...777...98S | SL2S IV |
| R22 | 2015ApJ...800...94S | SL2S V |
| R23 | 2026A&A...705A..13M; 2025yCat..37050013M | TDCOSMO XXI: SL2S velocity dispersions (lead A6·random unless lens data are new) |
| R24 | 2025MNRAS.541....1S; GitHub williyamshoe/dinos2 | Project Dinos II: 20 new SL2S models plus SLACS |
| R25 | 2015MNRAS.449.3441S | SNELLS: two new low-z lenses |
| R26 | 2017ApJ...845..157N; 2018yCat..18450157N | SNELLS: three low-z lenses |
| R27 | 2020MNRAS.494..271C | MNELLS |
| R28 | 2005ApJ...625L.103S; 2013MNRAS.434.1964S | ESO 325-G004 (z = 0.0345 by title) |
| R29 | 2018MNRAS.478.1595C | New lens at z = 0.066 (by title) |
| R30 | 2025A&A...694A.145O | Euclid: Einstein ring in NGC 6505 |
| R31 | 2026A&A...714A.158W | ESO0286 |
| R32 | 2017MNRAS.464L..46S; 2020MNRAS.493L..33S | MaNGA lens ellipticals |
| R33 | 2022MNRAS.512.5298P | Nearby massive lens: lensing and orbital models |
| R34 | 2011MNRAS.417.3000S; 2015MNRAS.452.2434S | X-Shooter Lens Survey I, II |
| R35 | 2004ApJ...611..739T; 2002ApJ...568L...5K; 2003ApJ...583..606K | Lenses Structure and Dynamics survey |
| R36 | 1998ApJ...509..561K; 2000ApJ...543..131K | CASTLES lens-galaxy photometry |
| R37 | 2005ApJ...623L...5F; 2008MNRAS.383..857F | Stellar and total mass of CASTLES lenses |
| R38 | 2008ApJS..176...19F; 2009yCat..21760019F; 2011A&A...529A..72F | COSMOS strong lenses |
| R39 | 2018MNRAS.480..431L | Total-mass profile of z ≈ 0.5 early types |
| R40 | 2010ApJ...716.1579L | Virial and stellar mass of lens early types |
| R41 | 2011ApJ...740...97L; 2012MNRAS.424..104L; 2016MNRAS.459.3677L | Baryon fraction in lensing galaxies |
| R42 | 2007ApJ...671.1568J | Baryon fractions and M/L of early types |
| R43 | 2025ApJ...987L..31L | KiDS Einstein ring at z ≈ 1 |
| R44 | 2026A&A...711A..26E; Zenodo 10.5281/zenodo.15025832; Zenodo 10.5281/zenodo.19260200 | Euclid Q1 Strong Lensing Discovery Engine (A, F) |
| R45 | Zenodo 10.5281/zenodo.23681178 | Euclid Q1 Golden Lenses: sample and analysis |
| R46 | 2026AJ....171...57B; 2024ApJ...970...86S | AGEL survey: DR2 and galaxy-evolution analysis |
| R47 | 2023A&A...671A..60B | SDSS J0100+1818, ultra-massive elliptical |
| R48 | 2011MNRAS.418..929G; 2013MNRAS.433.2604G | CASSOWARY 5 and 31 |
| R49 | 2010ApJ...710..372G; 2012MNRAS.427.1918E; 2010MNRAS.406.2339B; 2009A&A...501..475T | Single SLACS and SL2S systems |
| R50 | 2026MNRAS.548ag683L | Double-source-plane elliptical |
| R51 | GitHub lenscat/lenscat | Community catalogue of known lenses |
| R52 | GitHub qiuhan96/isophotes_MGE_SLACS | Lens-light models of 35 SLACS lenses (photometry) |
| R53 | Zenodo 10.5281/zenodo.10007041 | Surface-brightness modelling of lenses (Borsato et al. 2023) |
| R54 | 2015yCat..35850084B | Shape parameters of lensing galaxies (Biernaux et al. 2016) |
| R55 | 2024A&A...688A.110S | Three ellipticals with ALMA lens data |
| R56 | 2020OJAp....3E..10W | Lens galaxy of iPTF16geu |
| R57 | 2019A&A...630A..71S | SuGOHI III: CMASS lenses |
| R58 | 2025A&A...693A.291S; 2024yCat..36930291S | Characteristics of 162 strong lenses (HOLISMOKES) |
| R59 | 2024SSRv..220...87S | Review "Strong lensing by galaxies" (for §3 step 4, citations) |

**Leads for other cells:**
- **A6·random** (stellar kinematics of lens galaxies): 2011MNRAS.415.2215B; 2012MNRAS.419..656C; 2011MNRAS.415..545T; 2023yCat..36730009S; 2025ApJ...990...51K.
- **A6·weak lensing:** 2007ApJ...667..176G.
- **A4** (spiral lenses): 2012MNRAS.422.3574B; 2013MNRAS.428.3183D; 2014MNRAS.437.1950B; 2010ApJ...719.1481V.
- **A8** (group lenses): 2009A&A...502..445L; 2010A&A...524A..95L; 2012ApJ...749...38M; 2013A&A...559A.105F; 2014A&A...571A..65V; 2015ApJ...814...26N; 2010yCat..74040749M.
- **A9** (cluster lenses): 2015ApJ...801...44Z; 2021yCat..18960070T; 2019yCat..36320036C; 2017MNRAS.471..383S; 2016MNRAS.458.1493P; 2023A&A...679A.124G.

### 1b. Counts (title level)

| Stage | Count |
|---|---|
| Records identified (per query, not deduplicated) | ADS 229 + 103 + 536; VizieR 362; Zenodo 48 + 200 scanned; GitHub 17 |
| Passed to full-text screening | 59 entries (R1–R59), grouping 80 records |
| Leads for other cells | 23 records |
| Excluded at title level | the rest (regenerable by re-running the queries) |
| Full-text screening | **pending**: two independent readers, brief `docs/sources/screening-brief-A6S.md` |

## 2. Full-text screening (2026-10-31)

Two independent AI readers (A and B) screened R1–R59 to the brief `docs/sources/screening-brief-A6S.md`, each in two blocks. Their tables are kept as returned in `docs/sources/screening-A6S/reader-{a,b}-block{1,2}.md`. `compare.py`, committed before either reading was opened, found **43 of 59 decisions in agreement** (`comparison.csv`). The 15 substantive disagreements were settled in `adjudication.md`, one of them (R52) by reading the source. Final codes are in `final.csv`. Claude checked the readings for recorded masses, mass-to-light ratios and results and found none.

| Code | Count | Records |
|---|---|---|
| E (both sides) | 12 | R10, R13, R19, R20, R22, R30, R32, R37, R41, R43, R49, R57 |
| E-pair (one side) | 19 | R3, R5, R9, R12, R15, R17, R18, R21, R24, R31, R33, R35, R36, R40, R46, R50, R53, R55, R56 |
| P (pending a ruling) | 11 | R7, R25, R26, R27, R28, R29, R34, R38, R44, R45, R47 |
| X | 16 | R1, R2, R4, R6, R8, R11, R14, R16, R23, R39, R42, R48, R51, R52, R54, R58 |
| — (review) | 1 | R59 |

Several agreed codes still depend on a question below: R32 and R41 on Q1, R19 and R21 on Q3.

### 2a. Questions for JvH (method rulings; recommendations given). **Ruled as recommended, D-063 (2026-10-31).**

These change how the cell measures, so each needs a ruling before any lens package is converted. The §5 projection ruling (baryons projected, or lensing deprojected) is also still needed.

1. **Stellar M/L from spectra.** Several nearby lenses (R25, R26, R28, R29, R31 with R33, R32, R41) give a photometric luminosity inside the Einstein radius times a stellar-population M/L fitted to *spectra*, with a fixed named IMF, rather than an SED fit to photometry. Some (R32) use an assumed age and metallicity range. *Recommendation:* accept both, with the IMF and population models named and the assumed ranges carried as an assumption range. Both are stellar-population M/Ls independent of lensing and dynamics, which is what "from photometry" in §2 was written to secure; IMF-free spectral fits are not defaults. Recorded as a clarification of §2 in the deviations register.
2. **Einstein radius from half the image separation** (R25, R29), and single-image limits (R9 grade C, R27). *Recommendation:* accept the half-separation value as a lens model with `model_dependence` "SIS from image separation". Where a full model of the same system exists, that model is the default (R27 for J0403−0239). Single-image limits are recorded, not plotted, in v1.0.
3. **Priors that use the system's own velocity dispersion.** R7 (SLACS IX) draws its metallicity prior from the σ–metallicity relation at each lens's own σ. R19 and R21 (SL2S) derive some source redshifts with the help of the velocity dispersion. *Recommendation:* treat both as inputs derived from the system's own kinematics (deviation #6). R7's stellar masses are recorded and shown as a flagged alternative; the default comes from a source without that prior (R13 or R9/R10), by a precedence rule frozen before any value is seen. SL2S systems whose source redshift used σ are recorded, not plotted.
4. **Several lens models and stellar-mass sources for the same lenses** (SLACS: R5, R7, R12; SL2S: R20, R24; stellar masses: R7, R9/R10, R13). *Recommendation:* the observed default is the Einstein mass, which depends little on the model; the other models are shown as alternatives. A precedence rule for both sides is written and hash-frozen before any table is opened.
5. **Source redshift and confirmation** (R38, R44, R45, R58). *Recommendation:* an Einstein mass needs measured lens and source redshifts, so systems without a spectroscopic source redshift are recorded, not plotted. Candidates count only when confirmed. R45 is held until its files are public.
6. **Galaxy or group** (R28, R34, R35 MG2016+112, R47, R48, R49, R53). *Recommendation:* the source's own label where sources agree. A6 where the model has one main deflector (with external shear or minor perturbers); A8 where the source models several group members or calls it a group lens; A7 "ambiguous" where sources disagree (as deviations #7 and #15).
7. **Stellar mass printed as a fraction of the lens mass** (R34, XLENS I). *Recommendation:* accept fraction × the published Einstein mass, flagged, since both are printed values and the product is the authors' own stellar mass.
8. **Licence route for SLACS** (R11 Zenodo CC BY 4.0 copy of SLACS IX values). *Recommendation:* the original (R7 and its VizieR table) is the source of record, cited. The CC BY copy is used for redistribution only after a value-by-value check that it matches.

### 2b. Leads from the readers and the review (for §3 step 4, citations; round 2)

Named but not in R1–R59, to be screened in a second round with the same brief: Dye et al. 2008 (Cosmic Horseshoe lens model); Collier, Smith & Lucey 2018 (arXiv:1709.01931, HST models of SNELLS lenses); SNELLS-HD I (arXiv:2509.01732); Tan et al. 2024 (Project Dinos I); Treu et al. 2010 (ApJ 709, 1195); Ferreras et al. 2010 (MNRAS 409, 30); Sonnenfeld et al. 2012 (ApJ 752, 163); Shajib et al. 2021 (23 SLACS re-modelled); Lemon et al. 2024 (CASTLES); H-ATLAS and HerMES lens models (Negrello 2010, 2017; Dye 2014, 2018; Amvrosiadis 2018; Maresca 2022). Spiral lenses (SWELLS, Treu et al. 2011) go to A4.

### 2c. Counts

| Stage | Count |
|---|---|
| Passed to full-text screening | 59 entries |
| Eligible (E) | 12 |
| One side (E-pair) | 19 |
| Pending a ruling (P) | 11 |
| Excluded at full text (X) | 16 |
| Review (leads only) | 1 |
| Round-2 leads (citations) | 10 named sources or groups |
