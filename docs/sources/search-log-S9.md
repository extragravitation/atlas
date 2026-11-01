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
