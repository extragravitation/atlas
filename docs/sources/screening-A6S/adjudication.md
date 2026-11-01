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

## Round 2 (R60–R69f)

`compare_round2.py` (committed before either round-2 reading was opened): **12 of 15 decisions agree**. The three disagreements were settled under D-063, which was ruled before round 2 began.

| # | A | B | Final | Reason |
|---|---|---|---|---|
| R61 | E-pair | P | **E** | Both readers: new lens models fitted to new HST imaging (the observed side) and the F814W luminosity inside the aperture. Reader B: the reference M/L is the Kroupa spectroscopic value from Newman et al. 2017 (R26), converted to F814W. That M/L is accepted under D-063 item 1. |
| R62 | P | X | **X** | Both readers: no new lensing measurement (values quoted from R25 and R61). The population fit has a free IMF slope (never a default, D-063 item 1) and covers only a central aperture much smaller than the Einstein radius. Lead for A6·random. |
| R69e | X | P | **E-pair** (observed side) | Both readers: θ_E is half the image separation, measured from ALMA images. Accepted as "SIS from image separation" (D-063 item 2), and an alternative only where R69d or R69f give a full model of the same system. Systems without a lens redshift are recorded, not plotted (D-063 item 5). No baryonic side. |

R68 is NS for both readers: no "Lemon et al. 2024" paper about CASTLES could be identified from the review's citation.

## Round-1 P codes resolved under D-063

These applications of the ruling were made by Claude and are open to correction by JvH.

| # | Final | How D-063 applies |
|---|---|---|
| R7 | **E** (flagged alternative, never default) | Item 3. The metallicity prior uses the lens's own σ. |
| R25 | **E** | Item 1 (spectroscopic Kroupa M/L) and item 2 (half-separation θ_E). The full HST models in R61 are the default for SNL-1 and SNL-2. |
| R26 | **E-pair** (baryonic side) | Item 1. The observed side is R25's, or R61's as default. |
| R28 | **E** (A6) | Item 1. Item 6: the model has one deflector; "group-dominant" describes its environment, not a group lens model. Gas is stated negligible inside the Einstein radius. |
| R29 | **E** | Items 1 and 2. R27's HST value is the default for J0403−0239. |
| R27 | **E-pair** (observed side) | Item 2. The updated θ_E of J0403−0239 is printed in the text (tier 2, flagged, deviation #16). Single-image limits are recorded only. |
| R34 | **E** (A6) | Item 7: fraction × the Einstein mass of Dye et al. 2008 (R60), flagged. Item 6: R60 models one galaxy plus external shear. |
| R38 | **P** | Item 5: systems without a spectroscopic source redshift are recorded, not plotted. The IMF behind the stellar masses is unverified and must be read before admission. |
| R44 | **X** for v1.0 | Item 5: unconfirmed candidates, mostly without source redshifts. Kept as a lead for later confirmation. |
| R45 | **P** (held) | Item 5: a restricted release is held until public. |
| R47 | **E** (A7, ambiguous) | Item 6: the paper says "galaxy/group" and the 2024 follow-up says "lens group", so the sources disagree. |
