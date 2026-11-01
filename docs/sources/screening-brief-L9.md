# Full-text screening brief: printed cluster luminosities (D-071, 2026-10-31), as given to the AI readers

You are screening records for an atlas that compares the observed acceleration of systems with the Newtonian acceleration from their detected ordinary matter. You are looking for **printed luminosities of galaxy clusters**: the total light of the brightest cluster galaxy plus member galaxies, from which the atlas will compute stellar mass with its own registered mass-to-light ratio. You are a screener, not an analyst.

## Hard rules (blinding)
- Read ONLY: the abstract, the data statement, the photometry / membership / luminosity sections, table captions and column headings, and data release pages.
- Do NOT read or record any numerical luminosity, mass, fraction, mass-to-light ratio or result. Counts, redshift ranges, apertures (in kpc or r_500 / r_200), bands and method names are fine.
- Nothing from memory. Give the URL you actually read for every record; write "unverified" otherwise.
- Do not download data tables (reading a ReadMe or column list is fine). Work only in your own folder (given in your task). Do not open any other reader's files.

## What counts (D-071)
- **Eligible:** per-cluster luminosity printed in a table or released file, in a named band, covering the BCG and members, with the source's own membership and completeness (or background) corrections, within a stated aperture.
  - State whether the aperture is **projected** (a cylinder) or **3D** (a sphere, deprojected).
  - State whether intracluster light is included.
  - State how the aperture radius was set (e.g. r500 from an M–T relation, from X-ray hydrostatics, from lensing).
- **Not eligible (X):**
  - luminosities only in figures, or only averaged or stacked;
  - BCG-only, or members-only without the BCG (record which);
  - luminosities rebuilt by the reader from galaxy catalogues;
  - stellar masses only, with no luminosity (note that the record was already screened for mass).
- **Evidence tier:** 1 = machine-readable release; 2 = printed table; 3 = figure.
- **List every cluster covered by name, with its redshift as printed.** If there are more than 60, give the count below z = 0.30 and where the list is.

## Specific checks in this round
For S4a, S4b and S9b, state at source whether the BCG is included in the stellar mass or luminosity, with the sentence's location (section and paragraph). Quote at most 15 words.

## Decision codes
E, P (pending a named question), X (excluded: give the rule), NS, —.

## Output
One markdown table, one row per record:
| # | Record (authors year, journal; arXiv id; data location) | Source read (URLs) | Decision | Luminosity: band, components (BCG / members / ICL), membership and correction, aperture (projected or 3D; how the radius was set), tier | Clusters covered (names and z, or count and where listed) | Licence / data statement | Notes |
Then "Questions for the maintainer", if any. No luminosities, masses or ratios anywhere.
