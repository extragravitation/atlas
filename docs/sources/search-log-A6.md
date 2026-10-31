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
