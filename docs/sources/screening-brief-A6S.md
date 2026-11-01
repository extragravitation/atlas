# Full-text screening brief: A6·strong lensing (2026-10-31), as given to the AI readers

You are screening literature records for eligibility in a public, theory-neutral atlas that compares the observed acceleration of systems with the Newtonian acceleration from their detected ordinary matter. This cell is **early-type galaxies × strong gravitational lensing**. You are a screener, not an analyst.

## Hard rules (blinding: these protect the atlas from bias)
- Read ONLY: the abstract page, the data-availability statement, the methods / observations / lens-modelling / stellar-population sections, table captions and column headings, and any data release page (VizieR ReadMe, Zenodo or GitHub README).
- Do NOT read or record any numerical Einstein mass, total mass, stellar mass, mass-to-light ratio, dark-matter fraction, IMF normalisation, density slope, or any result, conclusion or interpretation about missing mass / dark matter / modified gravity / the IMF. If a page shows such numbers, ignore them and do not copy them into your output. Counts of systems, redshift ranges, and the names of models, bands and instruments are fine.
- Never state anything from memory. If you could not read something at source, write "unverified". Give the URL you actually read for every record.
- Do not download data tables. Reading a ReadMe or column description is fine.
- Prefer arXiv (https://arxiv.org/abs/<id>, https://arxiv.org/pdf/<id>). ADS pages may be unreachable; use WebSearch to find the arXiv id from a bibcode or title. VizieR ReadMe: try https://cdsarc.cds.unistra.fr/viz-bin/cat/J/... or the GAVO mirror https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/...

## Eligibility rules that apply (selection protocol §1, §1a, §2)
- **Observed side:** the projected mass within the Einstein radius (or the Einstein radius plus the lens and source redshifts, from which it follows), from a lens model fitted to the lensed images. Record the mass model (e.g. SIE, power law, composite), and whether a mass, an Einstein radius, or both are tabulated. A velocity dispersion alone is not the lensing observed side (note it as a lead for A6·random).
- **Baryonic side:** stellar mass (or luminosity plus a stated stellar-population mass-to-light ratio) from photometry, with the IMF and the population model named. Record whether it is total or within the Einstein radius / an aperture, and the bands. A stellar mass derived from lensing or dynamics is not a baryonic input. If the source gives photometry only, note that a mass-to-light step would be needed; if it gives no photometry, note that a pairing source would be needed.
- **Gas (§1.7):** record any statement in the source about gas (cold or hot) inside the Einstein radius: measured, stated negligible (quote it), a limit, or "no statement".
- **Redshifts:** lens and source redshifts per system, and how measured (spectroscopic or photometric).
- **Evidence tier:** 1 = released machine-readable files; 2 = tables printed in the paper; 3 = values only in figures (allowed only where no tier 1/2 data exist; flag it).
- **Not circular:** nothing on either side may come from a scaling relation, or from the system's own kinematics or lensing (e.g. a stellar mass fitted jointly with the lens model is flagged "joint fit"; a stellar mass from photometry alone is not).
- **Duplicates:** a re-analysis of published lens models and published stellar masses with no new measurements is X (duplicate); name the originals. A new lens model of existing imaging, or new stellar masses for known lenses, is a new measurement: say which side is new.
- **Kinds:** early-type (elliptical / lenticular) lens galaxies are A6. Spiral or disc lenses are A4 (lead). Group- or cluster-scale lenses are A8 or A9 (lead). Lens galaxies above z ≈ 0.3 are still recorded: the epoch is a property, never a filter, but note the redshift range.
- **Candidates only** (lens-finding papers with no lens models and no confirmations) are X.
- **Licence:** record any licence statement on the data release page or "none shown".

## Decision codes
E (eligible: observed side + baryonic side, or with a named pairing), E-pair (one side only; name the side), P (eligible pending a named question), X (excluded; give the rule), NS (could not read at source), — (not a dataset).

## Output
Write a markdown file at the path given in your task, containing ONE table with these columns, one row per record (keep the R numbers given):
| # | Record (authors year, journal; arXiv id; data location) | Source read (URLs) | Decision | Observed side (quantity; mass model; tier; N lenses; lens z range) | Baryonic side (stellar mass method, IMF, bands; aperture) and gas statement | Licence / data statement | Notes (duplicates, overlaps, kind, leads, questions) |
Then a short list "Questions for the maintainer", if any. No masses, mass-to-light ratios, fractions or slopes anywhere. Keep each cell concise.
