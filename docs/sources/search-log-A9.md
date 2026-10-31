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
