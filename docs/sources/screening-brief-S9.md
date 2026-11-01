# Full-text screening brief: stellar masses for galaxy clusters (2026-10-31), as given to the AI readers

You are screening literature records for an atlas that compares the observed acceleration of systems with the Newtonian acceleration from their detected ordinary matter. Here you look for **measured stellar masses of galaxy clusters**: brightest cluster galaxy, member galaxies, intracluster light. You are a screener, not an analyst.

## Hard rules (blinding)
- Read ONLY: the abstract, the data statement, the observations / photometry / membership / stellar-population sections, table captions and column headings, and data release pages.
- Do NOT read or record any numerical stellar mass, mass fraction, mass-to-light ratio, baryon fraction, or any result or interpretation. Counts of clusters and galaxies, redshift ranges, apertures in kpc or r_500 units, bands, and model names are fine.
- Never state anything from memory. Give the URL you actually read for every record; write "unverified" where you could not read something.
- Do not download data tables. Reading a ReadMe or column description is fine.
- Work only in your own folder (given in your task). Do not open any other reader's files.

## What counts
- **Eligible:** a stellar mass for named clusters, measured from photometry (or spectra plus photometry), with a named IMF and population model.
  - Coverage: the brightest cluster galaxy, members, and intracluster light, each stated as included or not.
  - Form: a radial profile, or totals within stated apertures.
  - Membership by spectroscopy, photometric redshift, or statistical background subtraction (record which).
- **Not eligible (X):** stellar masses from richness, X-ray, SZ or total-mass scaling relations; Fundamental Plane or Faber–Jackson masses; models normalised by M500; stacked or average values only, with no per-cluster numbers.
- **Evidence tier:** 1 = machine-readable release; 2 = printed tables; 3 = figures only.
- **List every cluster covered by name, with its redshift**, as the source prints them. If there are more than 40, give the count and where the list is (table or file).

## Decision codes
E (eligible), P (eligible pending a named question), X (excluded: give the rule), NS (could not read at source), — (not a dataset).

## Output
One markdown table, one row per record:
| # | Record (authors year, journal; arXiv id; data location) | Source read (URLs) | Decision | Stellar mass: components (BCG / members / ICL), method, IMF, bands, membership, form (profile or aperture), tier | Clusters covered (names and z, or count and where listed) | Licence / data statement | Notes |
Then "Questions for the maintainer", if any. No stellar masses or fractions anywhere.
