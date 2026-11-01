# A9 galaxy clusters (lensing and member galaxies): which values are shown (draft for JvH's approval; frozen by hash once approved)

Written 2026-10-31 under D-066, D-067 and D-064, before any A9 table has been opened. Sources are the eligible records of search log A9 (`docs/sources/screening-A9/final.csv`). Once approved, this file is hash-frozen in `data/frozen/` and changes only by a new decision.

## 1. Who is plotted

A cluster is plotted only if all of these hold. Otherwise it is recorded with the reason.

1. **Kind.** A9: not called a group (A8), and not called merging by the source (A10 lead).
2. **Redshift.** The cluster redshift as printed is below 0.30 (D-066).
3. **Observed side.** A lensing-only profile (row L) or a member-galaxy-only mass profile (row O), never a joint fit (D-067 item 1).
4. **Baryonic side: gas.** Measured gas for the same cluster over the same radii: X-ray or SZ density in radial bins, or the source's fitted density model within its measured range.
5. **Baryonic side: stars.** Stars are measured for the same cluster (§3.3). Stars are present in every cluster, so a cluster with no stellar measurement is recorded, not plotted (protocol §1.7).
6. **No scaling relations.** No input on either side comes from a scaling relation, or from the cluster's own total mass (radii such as r_500 may be used as radii, and are flagged).

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
3. **Stars.**
   - Brightest cluster galaxy plus members (and intracluster light, where measured) from photometry, with a named IMF.
   - Chabrier or Kroupa is the default (D-039 item 2). The Salpeter value is the top of the range where the source gives it, or else the same model's ratio, read at source and registered.
   - Masses from the Fundamental Plane, Faber–Jackson or other scaling relations are not used (§1.3).
   - Stars inside the same radii as the gas: projected for row L, 3D for row O, by the source's own profile, frozen and tested code before use.
4. **Cold gas and other components:** a cited, quoted statement for the kind, read at source before conversion (deviation #4).

## 4. Tests frozen with this rule

- **Test 1:** an independent second reading of every packaged input.
- **Test 2:** transcription.
- **Test 3:** arithmetic integrity.
- **Reported, not pass/fail:** for clusters in both A9 lensing and X-COP, the projected gas computed here is compared with X-COP's own projected gas profile where X-COP gives one. This checks the projection code, not the result.
