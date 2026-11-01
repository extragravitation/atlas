# A9: comparison and adjudication of the two readings (2026-10-31)

## Comparison

- **v1** (`compare.py`, committed before either reading was opened): 49 of 115 rows agree. v1 compares rows by letter (C<n>a, C<n>b, …). Reader B gave each VizieR catalogue its own row, while reader A shared one row between a paper and its catalogue, so many letters do not refer to the same record. v1's output is kept (`comparison.csv`).
- **v2** (`compare_v2.py`, written after v1 was run and read; disclosed here): matches rows by the record's identifier (arXiv id, VizieR path, Zenodo DOI, GitHub repository or bibcode). It changes no decision. **54 of 126 matched pairs agree.** Rows that neither identifier matched (mostly records one reader could not identify) were matched by letter within the entry, and are marked so in `final.csv`.

## Independence breach (disclosed)

The readers used one shared scratchpad folder. Reader B reports that it found abstract files reader A had saved there, and opened two of them (C12e, C15b) before noticing. It then re-identified both records and re-read them from arXiv itself. The files held abstracts, not decisions. Both readers code C12e E-pair and C15b E, so the two agreements on these records are not fully independent. Future briefs give each reader its own folder.

## Rules used for the disagreements

- **R1 (most disagreements, 22 pairs):** reader A coded a record "E-pair" when it had only the observed side, even where it named a gas pairing in this search. Reader B coded those "E". The brief defines E as "observed side + baryonic side, *or with a named pairing*", so where either reader names a pairing to a record in this search that gives gas profiles for the same clusters, the code is **E**. Whether the pairing is complete (cluster coverage, gas profile tier) is checked at packaging.
- **R2:** where one reader could not identify or read a record (NS), the other reader's reading is used, marked "read by one reader only". Test 1 (an independent second reading) applies at packaging in any case.
- **R3 (kind):** where the source itself calls a cluster merging, the record goes to A10 as a lead (brief, Kinds) and is coded X for A9.

Every decision and its reason is in `final.csv`.

## Result

| Code | Count |
|---|---|
| E | 28 |
| E-pair | 33 |
| P | 16 |
| X | 28 |
| NS | 2 |
| — (reviews) | 2 |

Excluded records worth naming:
- **Tian et al. 2020** (CLASH radial acceleration relation, the survey lead) is X for both readers. It combines CLASH lensing (C1b) with CLASH-X gas (C3a) and adds no new lensing or gas measurement. Its originals are eligible.
- **Duplicates or circular inputs:** the LoCuSS stack rescaled by X-ray scaling relations (Niikura et al. 2015) and the 2025 sample profiles with richness- or SZ-based radii (C18a, C18b).
- **Merging clusters (A10 leads):** A2465, A370, MACS J0416 and MACS J0717.

## Questions for JvH (needed before any A9 package)

- **QA1. Lensing fitted jointly with dynamics or X-ray in one model.** Applies to C8a, C8c, C8d (Newman et al.: lensing + BCG stellar kinematics); C13e (MS 0440); C13i (A383, lensing + X-ray hydrostatic); C17a and C17b (AS1063).
  - *Recommendation:* the data standard keeps dynamics and lensing separate by default. So these records are used only where the source also publishes a lensing-only profile; the joint-fit products are recorded, not plotted.
- **QA2. Stacked profiles.** Applies to C12a (SDSS), C22 (CNOC1), C26 (WINGS) and the LoCuSS stack.
  - Protocol §2 gives A9 the form "profile". Stacks are the population-average content type.
  - *Recommendation:* a stack is plotted only as a population average, and only where the baryonic side is stacked over the same clusters with the same weights. Otherwise it is recorded.
- **QA3. Projection for clusters** (D-064 item 5). The lensing side is projected. Gas profiles are usually published as 3D densities, and projecting them to a cylinder means integrating along the line of sight beyond the X-ray data.
  - *Recommendation:* project the gas within the radial range the source measures, and carry the outer extrapolation as a registered assumption with the source's own model.
  - This ruling is needed before the first lensing package, not before screening ends.
- **QA4. Epoch** (asked separately): the cut that applies D-033 item 5.
