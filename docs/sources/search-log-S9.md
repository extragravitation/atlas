# Search log: stellar masses for galaxy clusters (D-068)

> Purpose (D-068 item 1): find measured stellar-mass sources for the clusters of the eligible A9 records below z = 0.30 and for the five X-COP clusters with modelled stars (A1644, A2255, A3158, A3266, RXC1825; issue #91), before the A9 precedence rule is frozen. Protocol §3 procedure. Run by Claude for JvH. Read at source; nothing from memory.

**Blinding.** Metadata, abstracts, data documentation and methods only. No stellar mass, mass fraction, mass-to-light ratio or result is read for or recorded here.

## 0. Plan, committed before any query is run (2026-10-31)

### 0a. What counts (§1, §2 A9 baryonic side, D-034, D-068)

- **Measured stellar mass** for a named cluster, from photometry (or spectra-plus-photometry) of the brightest cluster galaxy, the members, and intracluster light where measured, with a named IMF and population model.
- Given as a radial profile, or as totals within stated apertures, per cluster.
- **Membership** by spectroscopy, photometric redshift or statistical background subtraction: recorded, since each is a different kind of selection.
- **Not eligible:** stellar mass from richness, X-ray, SZ or total-mass relations; Fundamental Plane or Faber–Jackson masses; model normalisations by M500.

### 0b. Queries, verbatim

| # | Query | Sort |
|---|---|---|
| ADS-S9-1 | `abs:("galaxy cluster" OR "galaxy clusters" OR "clusters of galaxies") abs:("stellar mass" OR "stellar masses" OR "stellar mass profile" OR "stellar content" OR "baryon budget" OR "baryonic content") abs:("brightest cluster galaxy" OR "brightest cluster galaxies" OR "intracluster light" OR "member galaxies" OR "satellite galaxies") collection:astronomy property:refereed year:1990-2026` | citations |
| ADS-S9-2 | `abs:("stellar mass fraction" OR "stellar baryon fraction" OR "stellar fraction" OR "baryon budget") abs:("galaxy clusters" OR "clusters of galaxies") abs:("X-ray" OR "X-COP" OR LoCuSS OR HeCS OR CLASH OR "CHEX-MATE" OR WINGS) collection:astronomy property:refereed year:1990-2026` | citations |
| VIZ-S9 | `bibstem:yCat abs:("galaxy cluster" OR "galaxy clusters" OR "clusters of galaxies") abs:("stellar mass" OR "stellar masses")` | date |
| CIT-S9 | The stellar-mass source each eligible A9 record cites for its own clusters, and Ghizzardi et al. 2020 (X-COP) and the sources it compares with. | — |

### 0c. Screening and output

1. Title screening by Claude.
2. Two independent readers to `docs/sources/screening-brief-S9.md`. **Each reader has its own folder** (lesson from A9).
3. A coverage table: for each target cluster, which eligible stellar-mass sources cover it. The target clusters are taken from the A9 readings' notes (names and redshifts only) and from D-022.

## 1. Queries run

Run 2026-10-31, 19:15–19:40 MDT, through JvH's signed-in Chrome.

| # | Records |
|---|---|
| ADS-S9-1 | 580 |
| ADS-S9-2 | 74 (19 already seen) |
| VIZ-S9 | 44 |
| CIT-S9 | Ghizzardi et al. 2020 (X-COP stellar masses; arXiv:2007.01084), added as S12b |

ADS-S9-1 and -2 hid theses (`PhDT`) from the listing; they were not screened.

### 1a. Title-level screening

Excluded at title level:
- simulations and semi-analytic models;
- star formation, quenching and AGN studies;
- high-redshift clusters and protoclusters;
- galaxy–halo connection and clustering;
- black holes, globular clusters, single-galaxy studies;
- richness- or scaling-relation-based masses.

Counted, not listed.

| # | Record(s) | What (from title) |
|---|---|---|
| S1 | 2018A&A...609A.133C; 2026yCat..75211292P; 2010yCat..35260045F | OmegaWINGS stellar light and mass profiles; OmegaWINGS galaxies; WINGS-SPE catalogue |
| S2 | 2004ApJ...617..879L; 2003ApJ...591..749L | K-band BCG, ICL and cluster light (Lin & Mohr) |
| S3 | 2007ApJ...666..147G; 2013ApJ...778...14G | Baryon census and fractions (Gonzalez) |
| S4 | 2013A&A...555A..66L; 2011ApJ...743...13L; 2011A&A...535A..78Z; 2008A&A...485..633L | Baryons in groups and clusters; star-formation efficiency in clusters |
| S5 | 2010MNRAS.407..263A | Stellar mass fraction of clusters and groups |
| S6 | 2019MNRAS.484...60M | LoCuSS: mass, gas and stellar content |
| S7 | 2022PASJ...74..175A; 2016A&A...592A..12E | XXL baryon budget and content |
| S8 | 2015MNRAS.449.2353B; 2014A&A...571A..80A; 2014A&A...565A.126P; 2016A&A...585A.160A | CLASH BCG and ICL; CLASH-VLT stellar mass profile, ICL and A209 galaxies |
| S9 | 2016ApJ...816...98Z and 2016yCat..18160098Z; 2023yCat..74934591P | DES X-ray clusters' stellar mass; stellar mass of DES clusters |
| S10 | 2013MNRAS.435.3469H; 2018MNRAS.478.3072C | ACT and SPT cluster stellar and baryon content |
| S11 | 2015A&A...577A..19V | Stellar mass distribution in clusters (profiles) |
| S12 | 2022A&A...662A.123E; Ghizzardi et al. 2020 (arXiv:2007.01084) | X-COP gravitational field; X-COP stellar masses |
| S13 | 2020ApJ...894...32G; 2025A&A...697A..11C; 2020ApJ...892...34S; 2021ApJ...915..106C; 2023MNRAS.525.2519G; 2026ApJ..1001..185P | Single clusters and small sets: Coma ICL, Perseus (Euclid), A133, BCG and ICL inner profiles, A1689 core, nine local clusters' stellar mass function |
| S14 | 2021MNRAS.502.2419F; 2023MNRAS.521..478G; 2018MNRAS.474..917M; 2017ApJ...846..139M | ICL samples (XCS-HSC, DES-ACT, Frontier Fields) |
| S15 | 2017yCat..74602862B; 2024yCat..19330061H; 2019A&A...631A.175E | BCG stellar-mass catalogues |
| S16 | 2007ApJ...659.1106M; 2007ApJ...663..150M | Near-infrared properties of moderate-redshift clusters |
| S17 | 2010MNRAS.402..753M; 2011A&A...527A.101K; 2006AJ....132..347C | Shapley (ACCESS), A1367, nearby-cluster luminosity functions |
| S18 | 2014MNRAS.437.1362B; 2013MNRAS.429.3288S; 2009ApJ...703..982G | Stellar fractions across groups and clusters |
| S19 | 2017yCat..17940031T | A2255 membership (an X-COP modelled-star cluster) |

## 2. Full-text screening (2026-10-31)

Two readers, each in its own folder. Readings as returned: `screening-S9/reader-{a,b}.md`. Comparison: 44 of 49 agree. Final codes: E 13, P 11, X 23, — 1. One ruling is needed (QS4, summing member catalogues). The coverage of the five X-COP clusters is set out in `screening-S9/adjudication.md`.

## 3. Round L: printed cluster luminosities (D-071), plan committed before any query or reading (2026-10-31)

Under D-071, a printed cluster luminosity (BCG plus members, with the source's own membership and completeness corrections) counts as measured stars once multiplied by the Atlas's registered ratio. Two steps:

1. **Re-screen S1–S19** for printed per-cluster luminosities (band, aperture, projected or 3D, components), whatever their own conversion to mass. Records coded X only for their conversion (S2b, S3a, S3b, S5, S18b, S4c and others) are re-read for this. The three disputed central-galaxy readings (S4a, S4b, S9b) are settled at source in the same pass.
2. **Supplementary search** for sources that print cluster luminosities but not stellar masses:

| # | Query | Sort |
|---|---|---|
| ADS-L9-1 | `abs:("galaxy cluster" OR "galaxy clusters" OR "clusters of galaxies") abs:("total luminosity" OR "total luminosities" OR "K-band luminosity" OR "near-infrared luminosity" OR "optical luminosity" OR "cluster light" OR "luminosity content") abs:("brightest cluster galaxy" OR "member galaxies" OR members OR "luminosity function") collection:astronomy property:refereed year:1990-2026` | citations |
| VIZ-L9 | `bibstem:yCat abs:("galaxy cluster" OR "galaxy clusters" OR "clusters of galaxies") abs:(luminosity OR luminosities) abs:("K-band" OR "near-infrared" OR 2MASS OR SDSS)` | date |

Screening uses the brief `docs/sources/screening-brief-L9.md` with two readers, each in their own folder, and a comparison script committed first. The output is an updated coverage table.

### 3a. ADS-L9-1 run and title screening (2026-10-31)

Run 2026-10-31 through JvH's signed-in Chrome: **363 records** (7 theses, `PhDT`, hidden from the listing and not screened). VIZ-L9 was run at 20:25 MDT, after the Chrome extension reconnected (it had disconnected after ADS-L9-1): **77 records**, screened in §3b.

Excluded at title level (counted, not listed), by the S9 rules (§1a) plus:
- groups, compact groups and fossil groups (A8 leads, not A9);
- radio, X-ray-source, quasar and AGN luminosity functions;
- luminosity functions with no per-cluster total implied by the title, above z = 0.30;
- ICL studies of single clusters above z = 0.30 (MACS J1206, Frontier Fields, CL0024, El Gordo and others);
- records already listed in S1–S19 (Lin & Mohr 2003 and 2004b, Gonzalez 2007, Giodini 2009, Lagana 2008, CLASH and CLASH-VLT, Muzzin 2007, Shapley ACCESS, DES-ACT and XCS-HSC ICL, Frontier Fields ICL, Gonzalez 2020 Coma ICL, the 2021 BCG and ICL inner-profile study 2021ApJ...915..106C).

| # | Record(s) | What (from title) |
|---|---|---|
| L1 | 2004ApJ...610..745L | K-band LF and radial distribution of 93 clusters (Lin, Mohr & Stanford) |
| L2 | 2000ApJ...530...62G | Optical luminosities and mass-to-light ratios of nearby clusters |
| L3 | 2002ApJ...569..101M; 2002ApJ...569...91M | Mass-to-light function and optical luminosity function of virialized systems |
| L4 | 2000ApJ...543..521H | Mass-to-light ratios of groups and clusters |
| L5 | 2004A&A...423..449P; 2007A&A...464..451P; 2007A&A...461..397P | RASS-SDSS cluster survey I, V, VII |
| L6 | 2009ApJ...703.2232S | SDSS cluster weak-lensing cross-correlation III: mass-to-light (stacked; recorded for completeness) |
| L7 | 2007ApJ...663..717M; 2008MPLA...23.1521M | A1689 luminous content from weak-lensing dilution |
| L8 | 2014MNRAS.443.3309M | LoCuSS near-infrared luminosity and weak-lensing mass |
| L9 | 2016A&A...592A...9Z | XXL K-band luminosity and weak-lensing mass |
| L10 | 2009MNRAS.394..357L | ICM iron content and galaxy optical luminosity |
| L11 | 2012A&A...548A..83A | Survey-based cluster mass proxy (Andreon) |
| L12 | 2013AstL...39....1K; 2011AstL...37..219K | Hercules and Leo supercluster cluster properties (Kopylova & Kopylov) |
| L13 | 2002AJ....123...66Y; 2002AJ....123...87Y | Luminosity functions of 10 nearby clusters, I and II |
| L14 | 2003A&A...408...57M; 2008MNRAS.387.1374M | ABCG 209 luminosity functions; spectroscopic and photometric catalogue |
| L15 | 2000A&A...353..479A | Coma near-infrared luminosity function |
| L16 | 2009MNRAS.396.2367S | Norma cluster Ks luminosity function |
| L17 | 2006AJ....131.1989C | Photometry of SARS clusters |
| L18 | 2026MNRAS.550ag829B; 2026MNRAS.550g1017B | Separation of mass components in galaxy clusters (two papers) |
| L19 | 2025MNRAS.537.3954M | Stellar mass composition of galaxy clusters |
| L20 | 2025ApJ...988..229Y | Central regions of clusters from galaxies, gas and ICL |
| L21 | 2025MNRAS.543.4020M | Clusters from deep optical observations |
| L22 | 2020ApJS..247...43K; 2021ApJS..252...27K | BCG and ICL structure and photometry, local clusters (Kluge) |
| L23 | 2005ApJ...618..195G; 2000ApJ...536..561G | ICL in nearby clusters; diffuse light in A1651 (Gonzalez) |
| L24 | 2025A&A...694A.216J; 2025A&A...698A.134E; 2021ApJ...910...45M; 2016MNRAS.461..230E; 2017ApJ...849....6A | Single-cluster ICL below z = 0.30: Coma, A2390, A85, A85/A2457/IIZw108 (corrected from the readings), one more |
| L25 | 2015A&A...575A.108A | Dark and stellar mass in three massive clusters (redshift to check) |
| L26 | 2023TJAA....4S.184A | Abell 1589 luminosity function |
| L27 | 2020A&A...643A.136C | Clusters and early-type galaxies III: mass–radius relation |
| L28 | 1991ChA&A..15..260Z; 1992ChA&A..16..257Z | Coma and Virgo virial mass and kinematics |

The re-screen of S1–S19 (step 1) uses the S numbering of §1a; readers give one row per record, as in the S9 round.

### 3b. VIZ-L9 title screening (2026-10-31)

77 records. Excluded at title level (counted, not listed), by the rules of §1a and §3a plus: catalogues of single-galaxy properties, stellar clusters, quasars, voids, X-ray-only or richness-only cluster catalogues, and high-redshift samples. Already listed: WINGS-SPE (S1), MaNGA BCGs (S15), RASS-SDSS V (L5).

| # | Record(s) | What (from title) |
|---|---|---|
| LV1 | 2026yCat..75222223H | VSCL clusters and galaxies properties |
| LV2 | 2016yCat..18190063R | HeCS-SZ Hectospec survey of SZ clusters (an A9 observed-side survey; re-read for printed luminosities) |
| LV3 | 2015yCat..74492345P | Mass and luminosity of maxBCG groups |
| LV4 | 2012yCat..35420036E | Rich clusters from SDSS DR8 (Einasto) |
| LV5 | 2010yCat..21830197W; 2014yCat..74360275W | Clusters from SDSS-DR6; relaxation parameter of 2092 rich clusters (Wen) |
| LV6 | 2003yCat..21480243B | Catalogue of clusters from SDSS (Bahcall) |
| LV7 | 2016yCat..35880014T; 2018yCat..36180081T | Friends-of-friends group catalogues from 2MRS and combined local surveys (Tempel; corrected from the readings), which include rich clusters |
| LV8 | 2013yCat..35580075T; 2014yCat..35640054T | 2XMMi/SDSS cluster survey II and III (Takey) |

### 3c. Round L screening result (2026-10-31)

Six readings (two readers × three blocks, separate folders): `screening-L9/reader-{a,b}-{S,L1,L2}.md`. Comparison: 83 of 104 agree. Adjudication and six rule questions (QL1–QL6, for JvH): `screening-L9/adjudication.md`. Final codes (`screening-L9/final.csv`): E 8, P 10, X 79, NS 6, — 1.
