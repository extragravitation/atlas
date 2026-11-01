# A9 galaxy clusters (lensing and member galaxies): which values are shown (draft for JvH's approval; frozen by hash once approved)

Written 2026-10-31 under D-066, D-067, D-068, D-064, D-071 and D-072 (updated for D-071 and D-072 the same day), before any A9 table has been opened. Sources are the eligible records of search log A9 (`docs/sources/screening-A9/final.csv`). Once approved, this file is hash-frozen in `data/frozen/` and changes only by a new decision.

## 1. Who is plotted

A cluster is plotted only if all of these hold. Otherwise it is recorded with the reason.

1. **Kind.** A9: not called a group (A8), and not called merging by the source (A10 lead).
2. **Redshift.** The cluster redshift as printed is below 0.30 (D-066).
3. **Observed side.** A lensing-only profile (row L) or a member-galaxy-only mass profile (row O), never a joint fit (D-067 item 1).
4. **Baryonic side: gas.** Measured gas for the same cluster over the same radii: X-ray or SZ density in radial bins, or the source's fitted density model within its measured range.
5. **Baryonic side: stars.** Stars measured for the same cluster (§3.3), either as a stellar mass from photometry or as a printed luminosity times the Atlas's registered ratio (D-071). Stars are present in every cluster, and leaving them out always biases g_bar low (protocol §1.7). A cluster still without measured stars after the logged stellar-mass and luminosity searches (D-068, D-071) is recorded, not plotted. Modelled stars are never the default (§3.4).
6. **Matched geometry for the stars** (D-071 safeguard 2). A projected stellar mass or luminosity pairs only with row L; a 3D one only with row O, unless the source gives both. Otherwise the cluster is recorded, not plotted, for that channel.
7. **No scaling relations.** No input on either side comes from a scaling relation, or from the cluster's own total mass (radii such as r_500 may be used as radii, and are flagged).

## 2. Observed side

1. **Originals first** (protocol §4, D-038): the analysis by the team that took the data is the default. Re-analyses are shown as alternatives.
2. **Row L:**
   - Binned profiles come before fitted models. Fitted quantities are labelled with `model_dependence`.
   - Joint strong-plus-weak binned profiles come before weak-only profiles. Strong-only core models are alternatives, inside their constrained range only.
   - Among a team's own analyses of the same data, the most recent is the default.
3. **Row O:**
   - The source's own caustic or Jeans profile, labelled with its method and its registered assumption: the caustic filling factor, or the anisotropy model.
   - Where both methods exist for a cluster, the one with more spectroscopic members is the default and the other is shown.
4. **Rows L and O are separate channels.** A cluster with both appears twice, marked by channel, never averaged.

## 3. Baryonic side

1. **Gas, by source:**
   - X-COP (an Atlas package) where it covers the cluster;
   - then CHEX-MATE;
   - then the gas source named by the observed-side record's own survey (CLASH-X for CLASH, CHeCS for HeCS, Peng et al. 2009 for Abell 1689);
   - then others.
   - Binned deprojected densities come before parametric fits.
2. **Geometry.**
   - Row L: gas is projected onto the lensing cylinders (D-067 item 3). The contribution from beyond the measured range uses the source's own model, as a registered assumption shown per point.
   - Row O: 3D, against the 3D enclosed gas mass, with no projection.
3. **Stars.** Two routes, both "measured" (D-034). Where a cluster has both, route (a) is the default and route (b) is shown as an alternative (D-072 item 6).
   - **(a) Stellar mass from photometry** of the brightest cluster galaxy plus members (and intracluster light, where measured), with a named IMF. Chabrier or Kroupa is the default (D-039 item 2); the Salpeter value is the top of the range where the source gives it, or else the same model's ratio, read at source and registered.
   - **(b) Printed luminosity × registered ratio** (D-071). The source's printed luminosity of the brightest cluster galaxy plus members, with its own membership and completeness corrections, in a named band, times the Atlas's stellar-population mass-to-light ratio for that band: Chabrier or Kroupa default, Salpeter top, read at source and registered per band (D-039 family). The source's own conversion is not used if it is dynamical or tied to M500 or another scaling relation.
   - **The source's sums only** (D-069; D-071 safeguard 1). The Atlas never sums member catalogues. It may add a source's own printed cluster-level components when the source defines them as disjoint in one aperture (D-072 item 1); it never recovers a total by dividing by a printed fraction.
   - **BCG** (D-072 item 2). A direct sum over all galaxies or members in the aperture includes the BCG (flagged "BCG by method"). A total that is only a fitted Schechter integral with no separate BCG term is members only and is not used.
   - **Faint end** (D-072 item 3). A stated faint limit at least 2 mag fainter than M* is accepted and flagged; bright-only sums are not used. Missing faint light is shown as a range only where the source quantifies it.
   - **Magnitudes and epoch** (D-072 item 4). Absolute magnitudes in a named band count, converted with the registered solar absolute magnitude for that band; observed-frame apparent magnitudes do not. An evolution-corrected luminosity is paired with the ratio for the epoch it was corrected to.
   - **Deprojection** (D-072 item 5). A luminosity deprojected by the source's own model is 3D, labelled `model_dependence` with the source's assumption.
   - **Order for one cluster** (D-072 item 6): route (a) before route (b); within route (b), near-infrared bands first; a team's later analysis of the same data supersedes its earlier one; projected values pair with row L, 3D values with row O.
   - **One radius** (D-071 safeguard 3). For route (b), and for route (a) where the source gives only totals, the comparison is made only at the source's measured aperture; no stellar profile shape is assumed. Where the source gives a stellar profile, stars are taken inside the same radii as the gas: projected for row L, 3D for row O, by frozen and tested code. An aperture set by a scaling relation or by the cluster's own total mass (e.g. r500) is used as a radius only, and flagged.
   - **Intracluster light** (D-071 safeguard 4). Where the source did not measure it, it enters as a registered range (`icl_fraction`), default and range read at source before any A9 table is opened, and shown per point.
   - Masses from the Fundamental Plane, Faber–Jackson or other scaling relations are not used (§1.7).
4. **Modelled stars** (D-034 status "modelled") are shown only as a labelled alternative, never as the default. A model qualifies only if it does not use the cluster's own total mass (deviation #6); a model normalised by a hydrostatic or lensing M500 does not qualify (issue #91).
5. **Cold gas and other components:** a cited, quoted statement for the kind, read at source before conversion (deviation #4).

## 4. Tests frozen with this rule

- **Test 1:** an independent second reading of every packaged input.
- **Test 2:** transcription.
- **Test 3:** arithmetic integrity, including each route-(b) stellar mass recomputed from the printed luminosity and the registered ratio.
- **Reported, not pass/fail:** for clusters in both A9 lensing and X-COP, the projected gas computed here is compared with X-COP's own projected gas profile where X-COP gives one. This checks the projection code, not the result.
