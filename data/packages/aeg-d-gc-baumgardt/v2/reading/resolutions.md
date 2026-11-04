# aeg-d-gc-baumgardt/v2: second reading, resolutions

Second reader, 2026-11-04. Written without access to v1's g values, `convert.py`, any `REPRODUCTION_RESULT*` or any v2 table.

## Dissent from ruled outcomes

None. All three ruled outcomes were confirmed at source.
- **The M54 cut.** B17 (arXiv 1609.08794v1, `paper.tex` l. 588–589): "We have therefore neglected all data points beyond 200'' in the dynamical analysis of this cluster". v1's RV bins beyond 200″ are `o002481` (269.01″), `o002482` (410.12″) and `o002483` (679.1″). That leaves 13 of 16.
- **NGC 2298 and Pal 5 as findings.** BH18 (arXiv 1804.08359v2, `vltpaper_ver6.tex` l. 226–227) says the rise "could be due to the ongoing tidal disruption of these clusters". "Could" hedges the cause of the profile's rise. "The ongoing tidal disruption" is stated as fact.
  - BH18's own bins for these clusters (`veldis_tab.tex` l. 103–104 and l. 649–650) are not v1's bins. This confirms D-098 rule 1: these are not D-096 changes.

## Disagreements with the frozen test's expectations

None. The reading agrees with the frozen test on all of these:
- the changed rows: M54, `m000067`;
- the excluded systems: NGC 2298 and Pal 5, with no further finding;
- all six error levels and the g_bar level;
- the RV screening value.

Every line the frozen test cites in B17, BH18, K18, D21, F13, MvdM, BSH20, Wolf and L13 was spot-checked and holds.

## Resolved: the D-099 rule 3 anchors (2026-11-04)

**The reader could not reach Rees (1996, ASP Conf. Ser. 92, 289).** It is not on arXiv, and ADS showed a block (a 403, then human verification), which was not worked around. JvH then obtained the scanned PDF from ADS (`1996ASPC...92..289R`, 4 pages, SHA-256 `6a4d9cfaabf2aa71af5a897afa0dcf2edb5c3c4fd8e9298a3e1c8669b1f37db9`; not redistributed, © ASP). Claude read it at source.

**What Rees (1996) contains:**
- **Abstract, p. 289:** "Distances to eight galactic globular clusters (M2, M4, M5, M15, M22, M92, NGC 6397, and 47 Tuc) are derived by comparison of proper motions and radial velocities of cluster stars".
- **Table 1, p. 290,** lists those eight. It also lists M3 and M13, which §3 describes as "previous astrometric distance determinations" (Cudworth 1979; Lupton, Gunn, & Griffin 1987).

**The anchors, with `harris_anchor = yes`:**

| Cluster | Source |
|---|---|
| NGC 104 = 47 Tuc | McLaughlin et al. 2006, and Rees 1996 |
| NGC 5139 = ω Cen | van de Ven et al. 2006 |
| NGC 5904 = M5 | Rees 1996 |
| NGC 6121 = M4 | Rees 1996 |
| NGC 6341 = M92 | Rees 1996 |
| NGC 6656 = M22 | Rees 1996 |
| NGC 7089 = M2 | Rees 1996 |
| NGC 5272 = M3 | Rees 1996 Table 1, from an earlier paper |
| NGC 6205 = M13 | Rees 1996 Table 1, from an earlier paper |

- M3 and M13 are recorded as anchors because Harris cites Rees (1996), whose table includes them. Each note says that Rees quotes these distances and did not derive them.
- NGC 6397 and NGC 7078 (M15) have no measurement row.
- Every other cluster is `no`.
- The anchors carry a note only (D-099 rule 3). No value and no plotting decision changes.

## Items for JvH (classifications and observations, not dissent)

1. **A new possibility: NGC 1851.** BH18 l. 465–466 says "tidal effects ... or non-members could be responsible for the higher than predicted velocity dispersion profiles seen in the outer parts of some clusters like NGC~1851".
   - The word "could" makes this a possibility, so it stays plotted with the quotation (D-097 rule 2).
   - The frozen test lists no expected possibilities, so this is not a disagreement.
2. **A borderline "neither": NGC 6362.** D21 (arXiv 2105.02246v1, l. 184–187): "our previous analyses suggest ... that the cluster underwent severe mass-loss due to long-term dynamical evolution and quite strong interaction with the Galaxy".
   - **Classed neither:** it describes a past mass loss and its cause. It does not say that the cluster is now out of equilibrium, unbound, being disrupted or tidally disturbed (D-099 rule 4, mass loss mentioned on its own).
   - **If it were read as "tidally disturbed",** the word "suggest" would make it a finding. NGC 6362 would then be excluded, including its plotted RV row `m000049`.
   - **Recommendation:** keep "neither".
3. **MvdM's model ranking is not a D-096 preference.** MvdM (l. 242–245) finds the Wilson models "equally good or significantly better" than King (1966) for about 90 % of clusters. It names no family's parameters as the default, so D-096 rule 1 is not applied. The Atlas keeps the King (1966) fits. The frozen test's `king_wilson_family` term already carries this.
4. **Binary screening for L13 is `integrated_light`, with one exception.** NGC 5824's outermost L13 bin in `veldis.html` (25.12″, 8.31 km/s) is a Fabry-Perot point from individual stars, not integrated light (L13 l. 440: "only one kinematic point can be extracted from the sample"). The value is per dataset code, so the exception is recorded here.
5. **L15's code label.** `veldis.html` labels the L15 code "(VLT/SINFONI)". The L15 values (23.30 down to 16.80 km/s; innermost error 5.20 km/s, which is more than 20 %) fit L15's description of the ARGUS integrated-light bins (l. 255). They do not fit the SINFONI value of "about 13 km/s" (l. 293).
   - So `integrated_light` and "consistent with the preferred measurement" are inferences. L15 prints no table of values.
6. **The D21 radii in `veldis.html` do not match D21's table.** The σ values are identical, but the radii differ:
   - D21 Table PROF (l. 464–468) prints the MUSE bins at 8.5″, 16.0″, 21.3″, 25.5″ and 29.5″;
   - `veldis.html` gives the same five values at ⟨r⟩ = 55.98″, 72.30″, 79.68″, 84.54″ and 88.14″.
   - This affects only v1's D21 row (`m000048`, an unplotted alternative) through its weights and coverage. It is not a D-096 or D-097 matter, but it is a discrepancy between the database and the source.
7. **Bins present in a source but missing from `veldis.html`.** None was excluded by its source, so none is a D-096 matter:
   - K18's two outer NGC 5139 bins (177.1″ and 267.5″, `tableb1_1.tex` l. 47–48);
   - F13's seventh FLAMES bin (20.54″) and its two RFP bins (l. 384, l. 397–398).
8. **A statement in a source that does not count for the system.** L13 l. 633 says of NGC 1851: "accreted and stripped by the Milky Way. For that reason Jeans models might not be sufficient". It is not recorded, because L13 is not a dispersion source as used for NGC 1851: v1 has no L13 row for it, and `veldis.html` has no L13 profile for it.
9. **Quotation format.** Quotes are copied from the LaTeX source with runs of whitespace collapsed to one space. Line ranges are computed by the build script on the original files.
