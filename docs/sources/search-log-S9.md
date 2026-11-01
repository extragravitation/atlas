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
