# aeg-d-dwarfs/v2: resolution of the two second readings (2026-11-04)

This serves item 11 of the frozen test (`data/frozen/dwarfs-v2-test.json`). Readers A (`reader-A.csv`) and B (`reader-B.csv`) worked independently. The resolved reading is `resolved.csv`: the readers' columns plus `resolution`, which is one of:
- `agree`;
- `resolved_at_source`;
- `ruled`;
- `awaiting_ruling`.

The resolving session saw no v1 or v2 g value, `measurements.ecsv`, `convert.py` or result file. Disagreements were resolved by reading the cited line in the readers' e-prints (hashes as recorded in their rows). Rulings applied: D-096 to D-101.

**Not frozen yet:** the Tollerud question below is awaiting JvH's ruling.

## Counts

- **Rows:** 1,539 in `resolved.csv`.
  - 1,259 agree;
  - 247 resolved at source;
  - 22 ruled;
  - 11 awaiting ruling.
- **D-096 value changes: 2, both ruled.**
  - Phoenix II: σ 11.0 km/s is the default and 9.5 km/s the alternative (D-098 rule 5).
  - Fornax: r_h 20.1′ (Sérsic) is the default and 19.8′ (exponential) the alternative (D-101).
  - All other stated preferences and exclusions leave the values unchanged. Either v1 already uses the preferred value, or the exclusion is not of data points the Atlas computes from (D-098 rule 1).
- **D-097 classes under D-100:**

| Class | Count | Systems |
|---|---|---|
| Finding | 8 | And XXVII, Antlia II, Boötes III, Boötes I, Hercules, Ursa Major II, Willman 1, And XXI |
| Possibility | 14 | And I, And XIX, Aquarius II, Boötes II, Draco II, Eridanus IV, Hydrus I, Leo I, Leo VI, Pegasus III, Segue 1, Sextans, Triangulum II, Tucana V |
| None | 43 | |

  The findings are exactly D-100's list. The resolved file has 204 `d097` statements: the union of both readers, deduplicated, plus two from Monelli 2025.

## Disagreements and how they were resolved

**R_h and ε errors.** No disagreement. One difference in format only (Pegasus IV).

**σ confidence level.** There were 25 raw differences.
- **Wording only (21).** These are the Geha 2026 systems: Reader A wrote "0.683; limits 95th percentile" and Reader B gave the level per row. Each row now takes 0.683 if resolved and 0.95 if it is an upper limit (Geha l. 741, Table 1 note 17).
- **Resolved at source (4):**
  - **And XVIII:** 0.68, stated. Kvasova 2024 Table 2 note a (`2_main.tab` l. 40): "Errors cover the 68% confidence interval". Reader B had not searched the table file.
  - **Willman 1:** 0.68, stated. Chiu 2026 l. 344, the figure caption for the posterior of v_sys and σ, says "median value and 16th and 84th percentiles". Line 328, cited by both readers, covers v_sys only.
  - **Phoenix II:** 0.683, stated. Fritz 2019 l. 386 calls the errors on the measured parameters "1 σ". Reader A had found no statement.
  - **Tucana V:** not stated. The v1 row is a resolved value. Hansen 2024's 90% (95.5%) levels apply to its upper limits only.
- **Agreed in substance:** And XII (upper end of a formal 1σ interval, no limit level; item 5 gives an empty `err_level`, `not_given_by_source`), Reticulum III (0.90) and Triangulum II (0.90).

**Magnitude confidence level.** There were 29 differences.
- **Muñoz 2018 photometry (21 systems):** 0.683, stated. Lines 432–437 say the bootstrap gives "1-σ errors". Reader B cited l. 432 only.
- **Richstein 2024 (Hydra II, Phoenix II, Triangulum II):** 0.68, stated. Line 326 says the uncertainties in the derived-quantities table, which holds m_V and M_V, are the 84th and 16th percentiles.
- **Reticulum III:** 0.68, stated. The table caption (`main.tex` l. 325) gives a highest-density interval of `\interval`, which `commands.tex` l. 109 defines as 68%.
- **Not stated:**
  - Antlia II: M_V carries a Poisson star-count error (Ji 2021 Table 1 note a).
  - Aquarius II: M_V comes from the stellar-population sum (Torrealba 2016 l. 578–589), not from the posterior.
  - Aquarius III and Leo VI: M_V is a derived quantity, and the stated levels cover the fitted parameters only.
  - Phoenix: van de Rydt 1991 states no level; Reader B could not read the scan.

**Binary screening.** One difference. **Tucana** is `no_multi_epoch_stated`: Gregory 2019 l. 533 says it has no repeat measurements ("Without repeat measurements from FLAMES+GIRAFFE").

**M_V against modulus.** Phoenix is "yes", from Reader A, who read the van de Rydt scan; Reader B could not.

**D-096 preferred values.** 31 agreed, 12 were found by one reader only. All 12 were checked at the quoted line:
- **Fornax (Wang 2019):** ruled under D-101, Sérsic.
- **No change** for: Hydra II (Vivas i-band distance 151 kpc, which v1 uses), Leo T (−8.0), Phoenix (van de Rydt), Sculptor, Sextans (King), Tucana (14.4 ≈ v1's 14.35), Phoenix II (Mutlu-Pakdil's mean distance), Pisces II (Sand's adopted 183 kpc), Ursa Major I (Garofalo's 19.94 mag) and Willman 1 (Chiu's 4.7 km/s).
- **Phoenix (Kacharov's P83 sample):** no change. It is the printed dispersion v1 uses.

**D-096 excluded data.** 30 agreed, 39 were found by one reader only. None changes a value except the two ruled cases:
- **Martin 2016's masks (structure):** the Atlas uses the printed parameters.
- **Distance exclusions** (Dall'Ora 2006, Bhardwaj 2024, Garofalo 2013, Monelli 2025): the Atlas uses the printed distance.
- **Down-weighting or removals** in Sandford 2026, Ou 2024 and Gregory 2019: the Atlas does not compute coverage from those tables.
- **Coverage computed from a source table** (D-096 rule 2): see the Tollerud check below.

**D-097.** 74 statements differed between the readers or from a check under D-100. Each was classed by D-100's words, with the reason in its row's `note`. The main points:
- **Unbound from a host** (And XIV, And XXII, Pisces II, Tucana) is an orbital statement, not the system's own binding, so "neither".
- **Statements arguing against disruption** ("no evidence of", "rule out", "disfavor") are "neither".
- **Coma Berenices:** "most of these galaxies are in process of disruption" concerns a class of galaxies, so "neither" (D-100 rule 3).

**Leo II.** Monelli 2025 (A&A 700, A201) was read at source by the main session, from the PDF JvH supplied (SHA-256 `6cf940d5…8b5845`, CC BY 4.0, not committed).
- **Preferred distance:** 21.60 ± 0.03 mag, which v1 uses. No change.
- **Exclusion:** V88 is excluded from the average, which is not a data point the Atlas uses.
- **Distance:** not inherited.
- **D-097:** no listed state.

## The Tollerud 2012 check (D-096 rule 2): awaiting ruling

Applies to And I, And III, And V, And VII, And IX, And X, And XIV, And XV and And XVI, whose v1 σ is from Tollerud 2012. And XIII has no v1 row.

**The source's selection.** Tollerud 2012 (`splashdwarfs1.tex` l. 354): "we only accept stars with membership probabilities P_memb > 0.1 … we also reject stars with velocities far from the cold spike for each dwarf (limits determined on a case-by-case basis …)".

**The Atlas's selection.** The D-051 coverage rule (`v1/reading/coverage_config_batch3.csv`) selects `Mask` in the dwarf's masks and `Prob ≥ 0.1`. It does not apply the per-dwarf velocity windows.
- **So yes:** the Atlas computes coverage from a member set that may include stars the source rejected.
- **The windows are not printed as numbers.** They are drawn in figures: And IX's "more stringent final velocity restrictions (vertical dashed lines …)", l. 660. The text names removed stars only for And XIII (l. 749), which has no row. So the source's exclusion cannot be applied mechanically from the text.
- **The MRT was fetched and checked** (`apj430011t2_mrt.txt`, SHA-256 `681c6711…8842`, matching `v1/sources.json`). It has no flag for the velocity cut.
- **Options for JvH:**
  - (a) Read the windows from the figures, by two readers, before conversion.
  - (b) Keep the current member set, and record a known issue on these 9 systems' coverage.
  - (c) Ask the authors for the windows.
- **Other coverage tables apply the source's own exclusion,** so no issue:
  - Koch 2007 (Leo I): the same 3σ cut, |HRV − 284.2| ≤ 3 × 9.9;
  - Battaglia 2011 (Sextans): the same [Fe/H]-error cut;
  - Spencer 2017 (Leo II): the source's `Mem` flag.

## For JvH: dissent and readings to confirm (none changes D-100's outcome)

1. **Tucana V.** Hansen 2024 l. 104 reports that Conn et al. 2018 "suggested that Tuc V is either an unbound part of the halo of the SMC or a tidally disrupted star cluster". Both alternatives are listed states, and "suggest" is finding wording, so under D-100's words this could be a finding. D-100's listed findings do not include it, so it is kept as a possibility, plotted with the quotation, as both readers classed it. Simon 2020 l. 937 finds "no significant evidence favoring tidal disruption".
2. **"Cannot rule out" is not in D-100's hedge list.** Boötes II (Walsh 2008, "can not rule out that Boötes II is a star cluster on the verge of disruption") is classed as a possibility, because the statement asserts nothing.
3. **Leo I.** Koch 2007 l. 580–584 reports claims of "hints of extratidal stars and thus tidal disruption" for dSphs, "Evidence for this has also been reported for Leo I". It is classed as a possibility, because the hedge "hints" carries through "this".
4. **And XIX** is a possibility, not "neither". D-100's "neither" concerns the abstract statement ("altered by tides"). Two other hedged statements make it a possibility, so it stays plotted with the quotation:
   - McConnachie 2008's question "whether And XIX was truly a dynamically relaxed system", reported by Collins 2013 l. 1102–1104;
   - Martin 2016 l. 652, "uncertain whether … so disrupted".
5. **Segue 1** is a possibility. Simon 2011 l. 1410–1413 says "not possible to rule out recent tidal disturbances", while concluding the data "do not provide significant support". The quotation note should carry the whole sentence.

## Smaller notes

- **Phoenix II's ε error** is printed "±0.6" for the exponential fit (Richstein 2024 l. 784), probably a typo for 0.06. It is recorded as printed.
- **Phoenix:** Kacharov 2017 prints only a σ corrected for the velocity gradient, so the D-038 addendum's value without the gradient does not exist.
- **Fornax:** Wang 2019's Sérsic r_h (20.1′) has no printed error, like the exponential value.

## Rulings after resolution (D-102, 2026-11-04 21:00 MDT)

- **Tollerud 2012 velocity windows (10 systems, 9 with rows).** The exclusion cannot be applied: the windows are drawn in figures and never printed as numbers. The member set stays as it is, and known issue #156 is shown on these systems. A query goes to the authors; it is not a release gate. All 11 rows that were awaiting this ruling are now `ruled`.
- **Tucana V** stays a possibility. Hansen 2024 reports Conn 2018's suggestion and disputes it in the next sentence ("On the other hand"). The suggestion is about what kind of object Tucana V is, not about its internal balance.
- **Confirmed as resolved:** "cannot rule out" counts as a possibility hedge (Boötes II). Leo I is a possibility. And XIX is a possibility, from hedged lines other than the "altered by tides" line, which is "neither".

No row is now awaiting a ruling.
