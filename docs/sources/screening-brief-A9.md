# Full-text screening brief: A9 galaxy clusters, lensing and member galaxies (2026-10-31), as given to the AI readers

You are screening literature records for eligibility in a public, theory-neutral atlas that compares the observed acceleration of systems with the Newtonian acceleration from their detected ordinary matter. This search covers **galaxy clusters**, by two tracers: **gravitational lensing** (row L) and **member-galaxy motions** (row O: caustic or Jeans mass profiles). You are a screener, not an analyst.

## Hard rules (blinding: these protect the atlas from bias)
- Read ONLY: the abstract page, the data-availability statement, the observations / methods / lensing-analysis / dynamical-analysis / X-ray or SZ sections, table captions and column headings, and any data release page (VizieR ReadMe, Zenodo or GitHub README).
- Do NOT read or record any numerical mass, density, concentration, gas fraction, baryon fraction, mass-to-light ratio, acceleration, slope, or any result, conclusion or interpretation about missing mass / dark matter / modified gravity. If a page shows such numbers, ignore them and do not copy them. Counts of clusters and galaxies, redshift ranges, radial ranges in Mpc or r_500 / r_200 units, and the names of models, instruments and methods are fine.
- Never state anything from memory. If you could not read something at source, write "unverified". Give the URL you actually read for every record.
- Do not download data tables. Reading a ReadMe or column description is fine.
- Prefer arXiv (https://arxiv.org/abs/<id>, https://arxiv.org/pdf/<id>); use WebSearch to find the arXiv id from a bibcode or title. VizieR ReadMe: try the GAVO mirror https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/... GitHub READMEs: `gh api repos/OWNER/REPO/readme --jq .content | base64 -d`.

## Eligibility rules that apply (selection protocol §1, §1a, §2)
- **Observed side, row L:** per-cluster (or stacked, say which) lensing profiles in radial bins (shear, ΔΣ, convergence or projected mass), or quantities evaluated from a fitted model (state the model, e.g. NFW, and whether binned data or only fit parameters are given). Strong-lensing-only models: note the radial range they constrain.
- **Observed side, row O:** a mass profile from member-galaxy velocities by the caustic technique or a Jeans analysis (state which, and the number of members). A single velocity dispersion or a single virial mass is not a profile (record it, code X for this row).
- **Not circular:** no observed-side quantity from a scaling relation (e.g. mass from richness, luminosity or Y_SZ), and no baryonic-side quantity from a scaling relation (e.g. gas mass from L_X–M). Flag any input that comes from the cluster's own total mass or dynamics (e.g. a radius r_500 defined from the lensing mass is fine as a radius, but say so).
- **Baryonic side:** gas profiles (X-ray surface brightness or SZ, giving gas density or gas mass in radial bins) for the same clusters, and stellar mass (galaxies and BCG, and intracluster light if measured) if available. If the record gives no baryonic side, say whether it names a source for the same clusters that does (a pairing), and which.
- **Redshift:** per cluster, with its range. Clusters at z ≳ 0.3 are recorded like any other (the atlas notes the epoch); say how many are below 0.3.
- **Evidence tier:** 1 = released machine-readable files; 2 = tables printed in the paper; 3 = values only in figures (allowed only where no tier 1/2 data exist; flag it).
- **Duplicates:** a re-analysis of published data with no new measurements is X (duplicate); name the originals. A new analysis of existing imaging or spectra (new profiles) is a new measurement: say so.
- **Kinds:** groups (roughly below 10^14 solar masses as stated by the source, or called groups) are A8; merging clusters described as such by the source are A10 leads; otherwise A9.
- **Licence:** record any licence statement on the data release page, or "none shown".

## Decision codes
E (eligible: observed side + baryonic side, or with a named pairing), E-pair (one side only; name the side), P (eligible pending a named question), X (excluded; give the rule), NS (could not read at source), — (not a dataset).

## Output
Write a markdown file at the path given in your task, containing ONE table with these columns, one row per record (number each record within its entry as C<n>a, C<n>b, … in the order listed):
| # | Record (authors year, journal; arXiv id; data location) | Source read (URLs) | Decision | Observed side (row L or O; quantity; method/model; binned or fit; tier; N clusters; z range; radial range) | Baryonic side (gas: method, binned?; stars: method) or pairing named | Licence / data statement | Notes (duplicates, overlaps, kind, leads, questions) |
Then a short list "Questions for the maintainer", if any. No masses, fractions, concentrations or slopes anywhere. Keep each cell concise.
