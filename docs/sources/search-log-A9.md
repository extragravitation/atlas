# Search log: A9 (galaxy clusters): lensing and member galaxies

> Protocol `docs/plans/SELECTION_PROTOCOL.md` (frozen at 817bc5a), §1, §1a, §2 (A9 rows), §3, §4; order of work §7 step 2 ("A9 lensing and member galaxies"). A9·hot gas is held by X-COP (`aeg-d-xcop/v1`) and is not re-searched here. Run by Claude (AI-assisted) for JvH. Every statement is read at source at the URL given; "unverified" means not confirmed at source. Nothing from memory.

**Blinding.** As the A6 log: metadata, abstracts, data documentation and methods only. No table is downloaded and no mass, gas fraction, mass-to-light ratio or result is read for or recorded in this log.

**Scope note (D-033 item 5).** Clusters at z ≳ 0.3 belong to the cosmic-epoch cell, a documented gap for v1.0. They are searched and recorded like any other, and the redshift range of every record is noted, but they are not plotted in v1.0.

## 0. Plan, committed before any query is run (2026-10-31)

### 0a. What the A9 rows ask for (§2)

- **A9·lensing.**
  - Observed side: binned weak- or strong-lensing profiles, or quantities evaluated from fits, labelled with `model_dependence`.
  - Baryonic side: gas profiles for the same clusters, with stars if available; a pairing with another dataset is allowed.
  - Form: a profile, in projection.
  - A projection ruling for clusters is needed before the first package, starting from D-064.
- **A9·orbits (member galaxies).**
  - Observed side: caustic or Jeans mass profiles from member-galaxy velocities.
  - Baryonic side: gas and stars for the same clusters, possibly from a paired dataset.
  - Form: a profile.
- **Both rows:** gas status under §1.7 (the hot gas is the dominant detected baryon component in clusters, so a dataset without gas needs a pairing). Redshift per cluster (§1.6). No input from scaling relations (§1.3; for example, no gas mass from an X-ray luminosity–mass relation and no lensing mass from a richness relation).

### 0b. Queries, verbatim (ADS, refereed, astronomy collection, 1990–2026)

| # | Row | Query | Sort |
|---|---|---|---|
| ADS-A9L-1 | lensing | `abs:("galaxy cluster" OR "galaxy clusters" OR "clusters of galaxies") abs:("weak lensing" OR "strong lensing" OR "gravitational lensing") abs:("mass profile" OR "mass profiles" OR "density profile" OR "density profiles" OR "convergence profile" OR "shear profile" OR "shear profiles") collection:astronomy property:refereed year:1990-2026` | citations |
| ADS-A9L-2 | lensing + gas | `abs:("galaxy cluster" OR "galaxy clusters" OR "clusters of galaxies") abs:(lensing) abs:("gas mass" OR "gas fraction" OR "baryon fraction" OR "baryonic mass") abs:(profile OR profiles) collection:astronomy property:refereed year:1990-2026` | citations |
| ADS-A9O-1 | member galaxies | `abs:("galaxy cluster" OR "galaxy clusters" OR "clusters of galaxies") abs:(caustic OR caustics OR "Jeans analysis" OR "Jeans equation" OR "dynamical mass profile" OR "mass profile" OR "projected phase space") abs:("galaxy velocities" OR "member galaxies" OR "redshift survey" OR "spectroscopic survey") collection:astronomy property:refereed year:1990-2026` | citations |
| VIZ-A9 | both | `bibstem:yCat abs:("galaxy cluster" OR "galaxy clusters" OR "clusters of galaxies") abs:(lensing OR "mass profile" OR "mass profiles" OR caustic OR "member galaxies")` | date |
| ZEN-A9 | both | Zenodo, `type=dataset`: `"galaxy cluster" lensing profile` and `"galaxy cluster" caustic mass profile` | best match |
| GH-A9 | both | GitHub repositories: `cluster weak lensing profiles`, `galaxy cluster caustic mass` | — |
| CIT-A9 | both | §3 step 4: data papers cited by eligible records and recent reviews. Starting leads: CLASH radial acceleration relation, Tian et al. 2020 (VizieR J/ApJ/896/70); CLASH binned profiles, Umetsu et al. 2016 (in figures only); HeCS caustic profiles (TAXONOMY §2 table) | — |

If a query fails or returns nothing for a syntax reason, the replacement is recorded beside it. If a query returns more than about 1 000 records, it is run as written and its title screening is done on the 1 000 most cited, with the limit recorded.

### 0c. Screening

As the A6 log:
1. Title and listing metadata, by Claude.
2. Two independent AI readers to a written brief (`docs/sources/screening-brief-A9.md`), committed before they start, with a comparison script committed before either reading is opened.
3. Counts in the style of a PRISMA flow, and leads for other cells.

## 1. Queries run

Run 2026-10-31, 17:55–18:40 MDT, by Claude through JvH's signed-in Chrome (ADS, Zenodo) and the GitHub API from the workspace. Title-level screening only.

| # | Where | Records |
|---|---|---|
| ADS-A9L-1 | ui.adsabs.harvard.edu, as planned | 572 |
| ADS-A9L-2 | as planned | 84 (48 already seen) |
| ADS-A9O-1 | as planned | 117 (44 already seen) |
| VIZ-A9 | as planned | 154 |
| ZEN-A9 | zenodo.org/api/records, as planned. The best-match ranking is unranked for these terms (totals 7 624 and 21 690), so the top 100 of each were scanned, with a script keeping titles that contain "cluster" and one of lens, mass, caustic, profile, kinematic, dynamic or velocity. **Scripted filter, disclosed.** | 5 kept |
| GH-A9 | api.github.com, as planned, plus `cluster lensing mass profile data` and `CLASH lensing` (added) | 3, 2, 0, 3 |

The listing script hid theses (`PhDT`) from ADS-A9L-2, ADS-A9O-1 and VIZ-A9; they were not screened.

### 1a. Title-level screening

Excluded at title level:
- simulations, theory and methods;
- cosmology from cluster counts, and scaling-relation calibration;
- splashback and stacked large-scale profiles used for cosmology;
- lensed background galaxies and transients;
- cluster catalogues and member photometry without kinematics or lensing;
- result papers that re-use published profiles with no new measurement;
- groups (A8 leads) and merging clusters (A10 leads).

Counted, not listed.

**Passed to full-text screening.** Records are grouped by survey or cluster; readers report per record.

| # | Row | Record(s) | What (from title) |
|---|---|---|---|
| C1 | L | 2014ApJ...795..163U; 2016ApJ...821..116U; 2015ApJ...801...44Z; 2018ApJ...860..104U; 2017ApJ...836..231U | CLASH weak and strong lensing profiles, 20 clusters |
| C2 | L | 2020ApJ...896...70T and 2021yCat..18960070T; 2024A&A...684A.180T | CLASH radial acceleration relation (survey lead); BCGs and clusters |
| C3 | L | 2014ApJ...794..136D | CLASH-X: lensing and X-ray mass profiles |
| C4 | L | 2019A&A...632A..36C; 2019yCat..36320036C | Strong-lensing models of 8 CLASH clusters |
| C5 | L | 2012ApJ...757...22C; 2012ApJ...755...56U; 2017A&A...607A..93C; 2020A&A...639A.125M; 2013ApJ...777...43M; 2017MNRAS.466.4094M | CLASH single clusters (A2261, MACS J1206, MACS J0717, MACS J2129) |
| C6 | L | 2010MNRAS.404..325R and 2011yCat..74040325R; 2013ApJ...769L..35O; 2016MNRAS.461.3794O; 2015PASJ...67..103N | LoCuSS lensing |
| C7 | L | 2012MNRAS.420.3213O; 2020yCat..22470012S | SGAS strong and weak lensing |
| C8 | L | 2013ApJ...765...24N; 2013ApJ...765...25N; 2009ApJ...706.1078N; 2011ApJ...728L..39N | Relaxed clusters: lensing, stellar kinematics, X-ray (A611, A383) |
| C9 | L | 2005ApJ...621...53B; 2005ApJ...619L.143B; 2006MNRAS.372.1425H and 2007yCat..83721425H; 2008ApJ...684..177U; 2011ApJ...729..127U; 2018yCat..74460683D; 2025A&A...699A.141C; 2009ApJ...701.1283P | Abell 1689 |
| C10 | L | 2011ApJ...738...41U; 2013ApJ...769...13U | Combined lensing profiles (Umetsu) |
| C11 | L | 2009ApJ...694.1643U; 2014PASJ...66...99O; 2009ApJ...699.1038O | Subaru weak lensing with SZ or Suzaku X-ray |
| C12 | L | 2001ApJ...554..881S; 2002ApJS..139..313D; 2005A&A...434..433B; 2007A&A...470..449B; 2012yCat..35460079I; 2002A&A...395..385C | Weak-lensing cluster samples (SDSS/RASS, Dahle, CFH12k, 400d, A1835/A2204) |
| C13 | L | 2009A&A...498L..33G; 2009A&A...504....1H; 2007A&A...467..427P; 2017ApJ...844...67W; 2020ApJ...897....4V; 2007ApJ...664..162M; 2016MNRAS.456.4475O; 2011A&A...529A..93H; 2012MNRAS.421.3147M; 2003A&A...398L...5E | Single clusters: Coma, A1351/A1995, A209, A2465, MS 0440, A478, Hydra A, A383, MS 1008 |
| C14 | L | 2026A&A...706A..83D; 2026A&A...708A.345S | Euclid ERO: Abell 2390 |
| C15 | L | 2006ApJ...652..232H; 2018A&A...610A..71T; 2022A&A...661A..65F; 2022ApJ...934..169U; 2017ApJ...842..132B; 2017ApJ...851...81A | Lensing with X-ray gas: CNOC, MACS J0647, A370, MACS J0416 |
| C16 | L | 2026A&A...714A.127A; GitHub tmcclintock/PLANCK_DES_Clusters | Planck clusters: DES shear profiles and Chandra |
| C17 | L | 2026MNRAS.550ag829B; 2024MNRAS.527.3246B; 2010A&A...518A..55S | Separating dark and baryonic components from lens models |
| C18 | L | 2025A&A...695A..49S; 2025A&A...696A.227S; 2021yCat..18900148U; 2019MNRAS.488.1704K and 2022yCat..74881704K | Sample weak-lensing profiles (XXL, APEX-SZ, others) |
| C19 | L | Zenodo 10.5281/zenodo.18646525; Zenodo 10.5281/zenodo.16534337; GitHub tau-core-research/tau-hff-cross-readout-paper6 | Released lens models (MACS J1931, SPT-CL J0546) and a lensing–X-ray package |
| C20 | O | 2013ApJ...767...15R; 2016yCat..17970106H; 2022A&A...665A.124L; 2021A&A...646A.105P | HeCS caustic profiles, with Chandra follow-up |
| C21 | O | 2003AJ....126.2152R; 2004AJ....128.1078R; 2002AJ....124.1266R; 2017ApJ...842...88S | CAIRNS and A2199 infall |
| C22 | O | 2000AJ....119.2038V | CNOC1 velocity and mass distribution |
| C23 | O | 1999ApJ...517L..23G; 2001ApJ...561L..41R; 2026A&A...710A.218P; 2026JCAP...06..005B; 2026yCat..22780051K; 2024yCat..36940216J | Coma |
| C24 | O | 2003ApJ...585..205B; 2008ApJ...676..218H; 2017ApJ...834..204G | Stacked and ensemble dynamical profiles |
| C25 | O | 2023A&A...677A..24L | Cluster mass profiles into the low-acceleration regime from galaxy kinematics |
| C26 | O | 2019A&A...631A.131M | WINGS dynamical modelling |
| C27 | O | 2013A&A...558A...1B; 2020A&A...637A..34S; 2023A&A...676A..66F; 2026A&A...708A.264M; 2026A&A...707A.153B; 2014ApJ...783L..11S | CLASH-VLT dynamical mass profiles |
| C28 | O | 2014A&A...566A..68M; 2017MNRAS.468..364A; 2024ApJS..272...22K; 2018ApJ...869..124S | Single clusters: A2142, A85, Perseus, A2107 |
| C29 | O | 2024A&A...692A.253L; 2025A&A...699A..88P | eROSITA gas with galaxy kinematics; CHEX-MATE kinematics |
| C30 | — | 2020A&ARv..28....7U; 2026A&ARv..34....9B | Reviews (cluster weak lensing; galaxy dynamics in clusters), for §3 step 4 |

**Leads for other cells:**
- **A10:** 2004ApJ...606..819M; 2026A&A...710A.207R; 2026yCat..37100207R; 2014ApJ...785...20J; 2012A&A...540A..61S; 2020A&A...635A..98R.
- **A8:** 2012ApJ...749...38M; 2010ApJ...714.1355T; 2010AJ....139..580R; 2004ApJ...607..202M; 2024MNRAS.527.1580W; 2025A&A...704A.163Z.
- **A9·hot gas** (beyond X-COP): 2014MNRAS.443.2342M; 1999ApJ...527..545M; 2002MNRAS.335..256A; 2014PASJ...66...85S; 2022yCat..19110082C.
- **A6:** 2020MNRAS.496.1857L.

| Stage | Count |
|---|---|
| Records identified (per query, not deduplicated) | ADS 572 + 84 + 117; VizieR 154; Zenodo 200 scanned; GitHub 8 |
| Passed to full-text screening | 30 entries (C1–C30), grouping about 110 records |
| Full-text screening | pending: two independent readers, brief `docs/sources/screening-brief-A9.md` |
