# Full-text screening brief (2026-10-29), as given to the AI readers

You are screening literature records for eligibility in a public, theory-neutral atlas that compares the observed acceleration of systems with the Newtonian acceleration from their detected ordinary matter. You are a screener, not an analyst.

## Hard rules (blinding: these protect the atlas from bias)
- Read ONLY: the abstract page, the data-availability statement, the methods/observations sections, table captions and column headings, and any data release page (VizieR ReadMe, Zenodo, MAST, author website).
- Do NOT read or record: any numerical velocity dispersion, mass, mass-to-light ratio, acceleration, or any result, conclusion or interpretation about missing mass / dark matter / modified gravity. If a page shows such numbers, ignore them and do not copy them into your output.
- Never state anything from memory. If you could not read something at source, say "unverified". Give the URL you actually read for every record.
- Do not download data tables. Reading a ReadMe/column description is fine.
- Prefer arXiv (https://arxiv.org/abs/<id>, https://ar5iv.labs.arxiv.org/html/<id>) to find the text; ADS pages (ui.adsabs.harvard.edu) may be unreachable from your environment. Use WebSearch to find the arXiv ID from a bibcode/title. VizieR: try https://cdsarc.cds.unistra.fr/viz-bin/cat/J/... or https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/... (cdsarc may reset; GAVO mirror usually works).

## Eligibility rules that apply
- Evidence tiers: 1 = released machine-readable files; 2 = tables printed in the paper; 3 = values only in figures (allowed only where no tier 1/2 data exist for those systems; flag it).
- Observed side must be measured from stellar velocities (not a dynamical mass alone, not a scaling relation).
- Dispersion method rules (ruled):
  - (ii) a binned line-of-sight dispersion PROFILE is usable if it can be light-weighted over the system; it is plotted only if the bins cover at least 80% of the system's light (the screener just records the radial range of the bins relative to the half-light radius if stated, e.g. "bins reach ~2 r_h" or "central only, < 0.2 r_h"; do not compute anything);
  - (iii) a central or aperture dispersion is usable only with the source's own (or a cited published) correction to a global value; record whether such a correction is given and what model it uses;
  - (i) otherwise: recorded, not plotted.
  - Proper-motion-only dispersions: recorded, not plotted (v1.0).
  - Individual stellar velocities only, with no dispersion published: not usable as the observed side (the atlas never computes dispersions itself); if the source ALSO publishes a dispersion, the velocities are kept as observables for a reproduction check — note "per-star velocities released: yes/no, where".
- Baryonic side: luminosity or surface-brightness profile (with a stellar-population mass-to-light ratio, which the atlas registers); a dynamical M/L is not a baryonic input. Star counts are allowed (counted stellar mass is "measured"). If the source gives no photometry, note that a pairing source would be needed.
- No input may be derived from the system's own kinematics (e.g. a distance computed from the dispersions): flag if the source's distance is kinematic.
- Distance or redshift must be given (or available from a cited source): note it and its method.
- Duplicates: a re-analysis of already-published data with no new measurements is X (duplicate) — name the original data source. Compilations: note which originals they repeat.
- Kinds: old globular clusters anywhere are A3 (record the host); young massive clusters are out of v1.0; ultra-compact dwarfs go to A7 labelled "ambiguous: dwarf galaxy or star cluster"; dwarf spheroidal / ultra-faint dwarfs are A5. If the literature disagrees on dwarf vs cluster, label "ambiguous".
- Licence: record any licence statement on the data release page (e.g. CC BY 4.0, ODbL) or "none shown".

## Decision codes
E (eligible: observed side + baryonic side or a pairing), E-pair (baryonic side only), P (eligible pending a named question), X (excluded, give the rule), NS (could not read at source), — (not a dataset).

## Output
Write a markdown file at the path given in your task, containing ONE table with these columns, one row per record entry (keep the R numbers given):
| # | Record (authors year, journal; arXiv id; data location) | Source read (URLs) | Decision | Observed side (type: LOS profile / global / central / aperture / PM-only / velocities only; tier; N systems; radial coverage vs r_h if stated) | Baryonic side and distance | Licence / data statement | Notes (duplicates, overlaps, kind, questions) |
Then a short list "Questions for the maintainer" if any. No numbers of dispersions, masses or M/L anywhere. Keep each cell concise.
