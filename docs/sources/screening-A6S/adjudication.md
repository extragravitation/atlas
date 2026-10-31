# A6·strong lensing: adjudication of the two readings (2026-10-31)

`compare.py` (committed before either reading was opened): **43 of 59 decisions agree**. R59 differs only in formatting ("— (review)" against "—"); the substantive disagreements are the 15 below. Each was settled by Claude from the two readers' notes and, where they disagreed on a fact, by reading the source. Neither reading is edited. No mass, mass-to-light ratio or result was read.

| # | A | B | Final | Reason |
|---|---|---|---|---|
| R2 | E-pair | X | **X** | Both readers agree on the facts: no new lens model (σ_SIE from R3), photometry only, and the paper's M/L comes from the Fundamental Plane, a scaling relation. R7 re-measures the same HST photometry for the full sample. Superseded; lead for A6·random. |
| R4 | X | E-pair | **X** | The Einstein radii in Table 1 are SLACS models of the same imaging, all refitted in R5 (SLACS V, the full sample). The stellar M/L is a joint fit to the lensing data. The stacked weak-lensing profile is a lead for A6·weak lensing. |
| R7 | E | P | **P** (Q3) | Reader B found that the SED fits use a metallicity prior drawn from the σ–metallicity relation at each lens's own velocity dispersion. That may bring the system's own kinematics into the baryonic side (deviation #6). Otherwise both readers find both sides present, tier 1. |
| R9 | P | E-pair | **E-pair** (baryonic side) | Both readers: no per-lens table in the paper; the per-lens stellar masses from this method are released in R10's VizieR table. The grade-C single-image Einstein-radius constraints are excluded (Q2). |
| R25 | P | E | **P** (Q1, Q2) | Both readers agree on the facts: the luminosity is photometric, the stellar M/L comes from spectral population fits (Kroupa), and two of the three Einstein radii are half the image separation. Both are method questions for JvH. |
| R26 | P | E | **P** (Q1) | The observed side is R25's. The baryonic side is new: r-band luminosity inside the Einstein radius, with a spectroscopic population M/L. |
| R28 | P | E | **P** (Q1, Q6) | 2013 paper: lens model, measured source redshift, F814W luminosity, spectroscopic M/L (Kroupa); quoted statement that gas inside the Einstein radius is assumed negligible. The 2005 paper calls the lens group-dominant. |
| R29 | P | E | **P** (Q1, Q2) | Same pattern as R25: half-image-separation Einstein radius, checked with SIS/SIE; spectroscopic M/L. |
| R31 | E-pair | P | **E-pair** (observed side) | Both readers: new lens model of HST imaging, values printed; the stellar mass in the paper is dynamical and excluded. The possible baryonic pairing with R33 depends on Q1. |
| R34 | E-pair | P | **P** (Q6, Q7) | Paper I: the Einstein mass is Dye et al. 2008's (a lead, not read); the stellar mass inside it comes from SDSS colours but is tabulated only as a fraction of the lens mass; the deflector may be a group. Paper II duplicates SLACS for the lensing side (X; lead for A6·random). |
| R40 | X | E-pair | **E-pair** (baryonic side, photometry only) | Both readers: Einstein radii taken from the literature (duplicate); the stellar M/L is a joint fit (excluded); the GALFIT HST photometry is new. Kept as a photometry source for the lenses it covers; an M/L step would be needed. |
| R45 | E-pair | P | **P** (Q5) | The Zenodo files are restricted and the associated paper was not found. Cannot be verified or redistributed until public. |
| R52 | E-pair | X | **X** | Checked at source (arXiv:2403.16253, PDF): Table 4's caption is "Best-fit power-law mass model parameters using MGE / Sérsic lens light model" and its rows are M1–M3, the mocks of Table 3 ("Parameters used for the three mocks"). No per-lens SLACS mass table; the repository holds isophote shapes only. Lead for lens-light structure. |
| R54 | E-pair | X | **X** | Shape parameters only (half-light radius, ellipticity, position angle); reader B confirms no magnitudes. No luminosity, so not a baryonic input. Lead for lens-light structure. |
| R58 | P | X | **X** | Reader B read the ReadMe columns: candidates with a network score and grade; the SIE parameters are predicted by a neural network and are not released per system. Candidates only. |

Rows where the readers agreed but a question still applies (R19, R21, R32, R38, R41, R44, R47) are listed under the questions in the search log; their codes are unchanged.
