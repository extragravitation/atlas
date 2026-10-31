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
