# aeg-d-xcop/v2: reproduction test, part B (structure, uncertainties, second reading)

**Status: draft, revision 2, for JvH's approval.**
- Revision 1 was written on 2026-11-05, after part A was run and published (`REPRODUCTION_RESULT_PART_A.md`; D-091), and before `convert.py` for v2 existed.
- Revision 2 answers the independent review `docs/sources/readings/step-d-2026-11-05/xcop-part-b-review-1.md` (E1–E8 and the weaknesses).
- Items marked **"subject to D-105 (pending)"** are recommendations awaiting JvH's ruling (open items O1–O4 at the end). If JvH rules otherwise, only the marked text changes before freezing.
- No value from the shared archives was read to write either revision. Every number quoted is from E22, Paper II, Ettori & Eckert 2022, Loubser et al. 2020 or Ghizzardi et al. 2021 as read at source, or from the published part A result (`REPRODUCTION_RESULT_PART_A.md`, `result_part_a.json`).
- On merge, this file's SHA-256 goes into `data/frozen/xcop-v2-part-b.json`. It is not edited after merge.
- If the test fails, the failure is published. The test is not changed to pass (operating rule 5; D-005).
- **Part A is frozen and stays as run.** Nothing here re-scores it or changes a rule it fixed (D-091 rule 1). Where part A fixed something (§1, §5, A7, A8), part B carries it out as fixed.

**Depends on:**
- part A (`REPRODUCTION.md`, revision 6, frozen in `data/frozen/xcop-v2-part-a.json`) and its result, with the D-091 erratum;
- D-089 (v2 from Eckert et al. 2022); D-090 (rules 1, 3, 4 and 5); D-091; D-092 (A644);
- data standard 2.5.1 (D-095 for `acceleration_released`; D-099 rule 1 for §12);
- D-087 (`model_dependence`), D-093 (confidence levels, §2a rules, `x_value_change_ruling`), D-096 with D-098 rule 1 (defer to the source's stated choices, same data points only), D-103 (precedent for explicit exclusion wording);
- D-105 (pending): O1–O4.

**Sources and their files.** E22 = Eckert et al. 2022, arXiv 2205.01110v1, `hydromass.tex` (SHA-256 `fdf04068…`, as read in step A). Paper II = arXiv 2205.01123v1. Ghizzardi et al. 2021 = arXiv 2007.01084, `xcop-metallicity.tex` (SHA-256 `2d862a21…`). Loubser et al. 2020 and Ettori & Eckert 2022 (arXiv 2112.07554) as read in step A. Line numbers refer to these files.

**Term numbering.** "E1–E30" are the term rows of step A reader A (`docs/sources/readings/xcop-e22-2026-11-03/reader-A.md`). Reader B numbers its rows differently (for example, B's E19 and E26 are other terms). Where both are cited, the reader is named.

## Purpose

Part B fixes, before conversion, how the v2 package is built from the source's own released values, and what it must contain:
- the 2.0 structure: measurements, observables, systems, the uncertainty-terms table and the descriptor (D-083, D-084);
- the uncertainty terms read at source in step A (`docs/sources/uncertainty-readings.md` §3, §3b, §3c, and readers A and B);
- the system-scale "choice of mass model" term that part A A7 fixed;
- the handling of the seven clusters without stellar data (part A A8 stage 1; D-090 rule 4);
- an independent second reading, frozen before conversion;
- the consent gate (D-090 rule 5), including its preview and follow-up.

**Values are the source's own** (part A §5): g_obs = GOBS and g_bar = GBAR from the five `gbar_gobs_<C>.fits` files. X-COP is the one exception to D-083 item 3 (D-090 rule 1). v2's values therefore differ from v1's by ruling, and the descriptor says so (item 10).

## Rules applied

1. **Which rows (part A §5; D-091 erratum; D-092).**
   - Every row of the five `gbar_gobs` files is a v2 measurement row: A644 19, A1795 21, A2029 22, A2142 20, A2319 27, **109 rows** (part A result, A1). Part A's "105" and "exactly 21" are the erratum D-091 records; the count here is the files' own.
   - A644's 19 rows are included and carry D-092's note (item 9).
   - **D-096 rule 2 (excluded data), as limited by D-098 rule 1.** Only **explicit exclusion wording** counts: a statement in E22 or a file header that named released rows or points were removed, not used, or cut from the source's own analysis of the relation (as in D-103: "removed all data points beyond …"). A summary of the range analysed is not exclusion wording. *Subject to D-105 (pending), O4.*
     - On step A's reading, E22 l. 528 ("over the radial range $[0.01-2]R_{500}$") summarises the range in the conclusions, and l. 486 ("We fitted the nonparametric points …") states no exclusion. **The expected outcome is no exclusion.** The second reading confirms or refutes this at source (`d096.csv`).
     - If the reading finds explicit exclusion wording, the rows it names are recorded, not plotted, with the quotation in `notes`, and the radius definition (which R500) is taken from the same source sentence. If the sentence does not define it, the question goes to JvH before conversion; the conversion never chooses.
     - The valid radial range is also asked of the authors (part A result, question 5). An answer from them comes in later under a new ruling, not under this test.
   - **D-096 rule 1 and rule 3.** The archives also release parametric (Einasto, NFW) and non-parametric mass profiles, and E22 l. 458 uses both kinds for g_obs. These are closed by part A §5, frozen: "Parametric files: used only for the checks and the uncertainty terms". They therefore give no alternative rows. The reading still records, for E22 and every file used, whether the source marks a preferred value or names a fiducial baseline among the values in the `gbar_gobs` files. One GOBS and one GBAR per radius are released, so no change is expected. A conflict with part A or an earlier ruling goes to JvH before conversion.
2. **The seven clusters without stellar data** (A85, A1644, A2255, A3158, A3266, RXC1825, ZW1215; part A A8 stage 1, D-090 rule 4).
   - **No measurement rows and no observables rows in v2** (*subject to D-105 (pending), O1*). Part A left the observables question to part B. They get none, because:
     - no measurement row would cite them (D-029 records the inputs of a row);
     - their only g_bar is a bound below the central value, which standard 2.5.1 cannot hold (part A A8 (a));
     - A8's stage-1 check failed (A3158), so stage 2 is blocked (#129).
   - **Systems table:** all twelve clusters are listed (item 8).
   - **Exclusion register:** each of the seven gets one row in `data/registry/excluded.csv`, with `dataset` = `aeg-d-xcop/v2`, the reason exactly as part A A8 fixed it ("stellar mass not in the source; g_bar bounded below by gas only; recorded under D-090") and the citation "Eckert et al. 2022, A&A 662, A123 (arXiv 2205.01110v1), l. 103, 114, 402".
   - **D-070 items 2 and 3** (measured stars for A2255, A3158 and A3266 from other sources) are superseded by D-089 and D-090 rule 4 for v2. The D-105 entry records this.
3. **D-087.** `model_dependence` = `none` on every row. GOBS is the non-parametric reconstruction "evaluate[d] … at the radii of the observed data" (E22 l. 263) and the paper's benchmark (l. 366). GBAR's fitted forms (Sérsic, gNFW) interpolate or extend measured profiles (D-087 item 1). E22 l. 458 says g_obs used "both the nonparametric reconstruction and the results of the Einasto fit to the DM component only".
   - **Criterion, fixed now:** the rows are `total_mass_form` only if a FITS header of a `gbar_gobs` file, or a sentence of E22, states that the released GOBS column is the Einasto (or another parametric) curve. The reading records the header keywords or the sentence with its line, or "no such statement". Without such a statement, `none` stands. This is never decided at conversion.
4. **D-097 does not apply.** D-025, which D-097 implements, governs g_obs from a velocity dispersion. The hydrostatic assumption is a registry assumption (`xcop_hse_equilibrium`, item 7), and its bias is the `hse_bias` and `nonthermal_pressure` terms. Part A §5, frozen, already fixes A2319: plotted, with its hydrostatic-validity statements on every row (item 9).
   - Paper II l. 80 ("clear evidence of a breakdown of hydrostatic equilibrium") would be a finding under the wording rules for dwarfs and globular clusters (D-099, D-100). This asymmetry between datasets follows from D-025's scope and part A §5. It is stated on A2319's page (item 9) and noted in D-105.
5. **The consent gate (D-090 rule 5).** Building, converting and scoring are done in the open. Publishing v2's rows waits for the authors' consent.
   - **Until consent, the tables are not committed.** v2's tables (`tables/*.ecsv`) are written by `convert.py` but are never committed or pushed: the conversion pull request adds `data/packages/aeg-d-xcop/v2/tables/` to `.gitignore`. The committed package holds the test, result, reading files, `convert.py`, `sources.json`, `datapackage.json`, the descriptor and `checksums.sha256` (hashes of the tables, no rows).
   - **No row values in logs.** `convert.py` and every v2 test or script print counts, hashes and pass/fail only, never row values. CI logs are public.
   - **Determinism** is checked through `checksums.sha256`: CI regenerates the tables from the fetched archives, recomputes the checksums and compares them with the committed file. The "committed tables equal regenerated tables" step is trivially satisfied for ignored tables and is not relied on.
   - **The deployed site** is built from the repository. With no committed v2 tables, v1 stays the current version on the map, its dataset page and its downloads. v1's files are not edited.
   - **Site change, part of the conversion pull request:** `site/src/lib/atlas.mjs` reads `datapackage.json` (or the descriptor) of a package version that has no `tables/measurements.ecsv`. If that version's `x_publication` is `awaiting_authors_consent`, the dataset page of the dataset's current version shows: "Version 2, built from Eckert et al. 2022, is ready and awaiting the authors' confirmation." The version without tables gets no pages, map points or downloads.
   - **The authors' preview** (D-090 rule 5: "offered a preview link before it goes live"). JvH builds the site locally with the v2 tables present and shares that build privately with the authors (for example as a zipped static site or a private link he controls). It is never pushed to the repository, to a branch, or to any per-pull-request preview: a table pushed anywhere, or built into a per-PR preview, is publication. The preview's date is recorded in the known issue for #19.
   - **Follow-up:** if there is no answer 4 weeks after the preview is offered, one follow-up is sent (D-090 rule 5). Its date is recorded the same way.
   - **Publication** is a later pull request that commits the tables and sets `x_publication` = `published`. It needs JvH's ruling recording the authors' answer, and `03c` sent first (D-092 rule 4).
   - The result is published like part A's: outcomes, counts and ratios, no rows.

## Order of work (against steering)

1. **The second reading** (item 11) is done before the first v2 conversion run, by a reader with no access to `convert.py`, any v2 table or v1's tables. It writes to `v2/reading/`:
   - `values.json`: the reader's own parse of the five `gbar_gobs_<C>.fits` files (RADIUS, GBAR, GBAR_ERR, GOBS, GOBS_ERR_LO, GOBS_ERR_HI per row), as **hashes only**. The parsed rows go to the gitignored `v2/source/reading/values.csv`, because the archives are not redistributed (D-004; D-090 rule 5). That file's SHA-256 is recorded under `off_repo` in the freeze record.
   - `error_form.md`: the meaning of the error columns, read from the FITS headers, or else decided by the rule in item 5.
   - `model_form.md`: the rule 3 criterion, with the header keywords or E22 sentence, or "no such statement".
   - `d096.csv`: the D-096 fields (preferred, excluded, fiducial) per source and file, with quote and location, under rule 1's explicit-wording criterion.
   - `err_levels.csv`: the confidence level of GOBS_ERR_* and GBAR_ERR as stated, with quote and location, or `not_given_by_source`.
   - `properties.csv`: per cluster, from the published papers, with quote and location:
     - the centroid shift w and its error (Paper II, arXiv 2205.01123v1, `tab2.tex`);
     - the non-thermal pressure fraction α at R500 and at R200, with its 1σ errors (Ettori & Eckert 2022, Table 1, "at $1 \sigma$ c.l.", l. 276). Each α is recorded **as printed**, with a `unit_status` column: `stated` if the table or text gives the unit, `inferred_percent` if the per-cent reading rests only on the magnitude of the numbers (§3c). Nothing is divided by 100 silently; item 6 states how the column is filled.
   - `hse_statements.csv`: every statement in E22 and Paper II about a cluster's hydrostatic validity, in file order, with quote and location. These are notes (rule 4), not exclusions.
   - `bcg_dm_systems.md`: whether E22 l. 109's "8.3 $\pm$ 2.9 per cent on average" describes all the central galaxies or only A644 and A2319, with the sentence(s) that decide it, or "not decidable" (item 7, `bcg_ml_extra_mass_model`).
   - `resolutions.md`.
2. **Disagreements** with step A, part A or this test's expectations are resolved at source by a session with no access to any v2 table, and recorded in `resolutions.md`. A conflict under rule 1 goes to JvH.
3. **Freezing the reading.** The SHA-256 of every committed reading file, and of the off-repo `values.csv`, goes into `data/frozen/xcop-v2-reading.json`, by a pull request merged before the first conversion run.
4. **Conversion.** `convert.py` takes D-096 changes, the error form, the model form, confidence levels, cluster properties, hydrostatic notes and the central-galaxy systems **only** from the frozen reading files, and its values only from the archives verified by hash (part A §1). It contains no cluster-specific rule of its own, apart from what this test names. It prints no row values (rule 5).

## The test

### A. Values and tables

1. **Rows.** v2 has exactly 109 measurement rows: the rows of the five `gbar_gobs` files in file order (A644, A1795, A2029, A2142, A2319, as in part A §1), with `system_id` from `data/registry/systems.csv` (v1's IDs for these clusters) and `measurement_id` `aeg-d-xcop/v2/m000001` onward. `kind` = `profile_point`, `channel` = dynamics, `method_class` = hydrostatic, as v1.
2. **Values.** On every row, compared with the reader's off-repo `values.csv`:
   - `r_kpc` = RADIUS, `r_kind` as v1;
   - `g_obs` = GOBS and `g_bar` = GBAR, as float64 of the FITS values, bit for bit;
   - the error columns as item 5 sets them;
   - `g_bar_stars`, `g_bar_gas_cold` and `g_bar_gas_hot` are **empty**: the archive releases g_bar as a total. The Einasto files reproduce GBAR for four clusters only (part A A2), so components are not split out in v2.
   - **Component statuses** (D-034): `stars_status` = `not_separable` and `gas_hot_status` = `not_separable`, because the released value is a total and no component column is filled. The source measured both (E22 l. 103–114, 142–156); that is recorded in `x_baryon_inventory` (item 10). `gas_cold_status` is v1's.
3. **Changed values.** v2 is not compared with v1 (D-090 rule 1; item 10). Any row recorded and not plotted under rule 1 is listed in the result with the quotation and the source's reason. A plotting change not traceable to the frozen reading is a fail.
4. **Arithmetic.** For each row, `observed_from` and `baryonic_from` name its two observables (item 8), and `g_obs` and `g_bar` equal those observables' values exactly.

### B. Uncertainties (standard 2.5.1 §2a, §3, §7a)

5. **Error columns and confidence levels.**
   - **Error form.** If the FITS headers state what GOBS_ERR_LO, GOBS_ERR_HI and GBAR_ERR are, that governs. If not, the reader decides by this rule, fixed now:
     - the GOBS pair is read as **bounds** if GOBS_ERR_LO < GOBS < GOBS_ERR_HI on every row;
     - as **error magnitudes** if GOBS_ERR_LO < GOBS and GOBS_ERR_HI < GOBS on every row, and the bounds condition fails on at least one row;
     - otherwise "undetermined";
     - GBAR_ERR is read as a magnitude if GBAR_ERR < GBAR on every row, and otherwise "undetermined".
     - **Undetermined is a fail of this item**, and the question goes to the authors. Question 6 of the part A result is extended to ask what the error columns mean, not only their confidence level.
   - **`g_obs_err_lo`, `g_obs_err_hi`** are the magnitudes (GOBS − lower bound and upper bound − GOBS, if bounds). **`g_bar_err_lo` = `g_bar_err_hi`** = the GBAR_ERR magnitude.
   - **Scales (§2a rule 6).**
     - `g_obs_err_point_*` = `g_obs_err_*`: GOBS_ERR is the per-radius posterior (E1). Its correlation between radii is not released (term `radial_covariance`).
     - `g_bar_err_point_*` are **empty**: GBAR_ERR mixes point-scale gas errors with the central galaxy's mass-to-light error, which is "constant with radius" (E22 l. 111; E18), a system-scale term. The term `g_bar_point` records that the source gives no point-scale part.
   - **Confidence levels.** `err_level`, `err_level_status`, `g_bar_err_level` and `g_bar_err_level_status` come from `err_levels.csv`. Expected: `not_given_by_source` on both sides (part A §5; question 6 of the part A result). A level is never read as 0.683 by default (D-093 rule 1).
6. **New extension columns** (standard 2.5.1 §12). Each header names the term or rule that uses it and says what an empty value means.
   - **Systems table:**
     - `x_xcop_alpha_nt_r500`, `_r500_err`, `x_xcop_alpha_nt_r200`, `_r200_err`: Ettori & Eckert 2022 Table 1, from `properties.csv`, all twelve clusters. If the unit is `stated` as per cent, the column holds the fraction (value ÷ 100) and the header says so. If it is `inferred_percent`, the column holds the value as printed, its unit is given as "as printed (per cent inferred, not stated)", and the term note says the same.
     - `x_xcop_centroid_w`, `_err`: Paper II Table 2, all twelve.
     - `x_xcop_mm_gp_ein`, `x_xcop_mm_gp_nfw`, `x_xcop_mm_ein_nfw`: part A A7's three published ratios per cluster (non-parametric/Einasto at R500 from R3; non-parametric/Table 1 NFW M500 and Einasto/Table 1 NFW M500, the NFW values at Table 1's R500, as the part A result says), copied from `result_part_a.json` at its stored precision. The five clusters only; empty for the seven.
     - `x_xcop_mass_model_frac`: item 7's size for `mass_model_choice`, computed by the rule stated there. The five only.
     - `x_xcop_status`: `plotted` for the five, `recorded_not_plotted` for the seven (rule 2). This is an Atlas state, so it is an extension column, not in `properties`.
   - **Measurements table:**
     - `x_xcop_centroid_w`, `x_xcop_centroid_w_err`: the cluster's systems values, repeated on every row, so that part A §5's "recorded on every row" holds in the measurements table itself.
     - `x_xcop_r500_rule1_kpc` is written only if rule 1 applies an exclusion: the R500 that the source's exclusion sentence names, from the reading. Otherwise this column is not written. Table 1's R500,TOT stays in the systems `properties` (part A §2).
7. **Uncertainty terms and registry.** `tables/uncertainty_terms.ecsv` contains exactly the rows below.
   - Each cites its source at the location given, from the step A readings (readers A and B) and §3b–§3c of `uncertainty-readings.md`, which serve as the D-031 second reading of these sizes.
   - `covariance` is `not_published` on every row.
   - `in_error_columns` is empty on every row: no row is a given point-scale term whose size sits outside the error columns (§7a), so none is `no`.
   - **One sizing rule for every row,** as in the dwarf, globular-cluster and lens tests: a size is `given` only where the source states it for these clusters, or for a class that contains them (the X-COP sample). Otherwise the row is `not_given_by_source`, and any figure stated elsewhere goes in the note.
     - Sizes the source states from mock tests of its own pipeline on a cluster built to match X-COP's data (E22 §3.6) count as stated for the sample's method: `reconstruction_bias` is `given` on that basis, said in its note.
     - Sizes E22 only cites from other work (Schellenberger 2015's 15 %) are not stated for these clusters: `xmm_calibration` is `not_given_by_source`, with the figure in the note.
   - **`given_by_other_source`** is used where the size is stated for these clusters by another paper of the same programme (Ettori & Eckert 2022; Loubser et al. 2020; Ghizzardi et al. 2021). These are other analyses of the same data, not independent measurements. The label is used because §7a has no closer value, and each note says "same programme, not independent".
   - **The one Atlas-computed exception (*subject to D-105 (pending), O2*):** `mass_model_choice` is `given`, although its size is computed by the Atlas, not stated by the source. Part A A7, frozen, fixed it as this term ("These ratios become the system-scale 'choice of mass model' term in v2's uncertainty table", part A l. 202). Its size uses **all three** of part A's published pairs by a rule fixed now: **per cluster, the largest |ratio − 1| across `x_xcop_mm_gp_ein`, `x_xcop_mm_gp_nfw` and `x_xcop_mm_ein_nfw`**. Its note states that it is the one row whose `given` size the Atlas computed. At `result_part_a.json` precision this gives A644 0.2241, A1795 0.0617, A2029 0.1459, A2142 0.0852, A2319 0.0518; the conversion recomputes these from the JSON, and any difference is a fail.
   - **`size_unit`** is given on every `given` or `given_by_other_source` row.
   - **`applies_to`.**
     - `*` is every system in the package (twelve). The five clusters with rows are "the five": `aeg-s-000177;aeg-s-000179;aeg-s-000180;aeg-s-000181;aeg-s-000183` (A644, A1795, A2029, A2142, A2319). The four without A2319 are "the four": `aeg-s-000177;aeg-s-000179;aeg-s-000180;aeg-s-000181`.
     - A listed subset has `scale = dataset` (§7a, 2.4.0). Point- and system-scale rows therefore use `*`. The seven clusters have no measurement rows, so such a term reaches the five only, and any `size_column` is empty for the seven.
   - **Not uncertainty terms (§2a rule 4):** spherical symmetry and hydrostatic equilibrium, as the method's assumptions, are registry assumptions (below). The doubtful validity of hydrostatic equilibrium in the outskirts (E30, E22 l. 373: "although the validity of the HSE assumption at large radii is unclear") goes in the note of `hse_bias` and in `xcop_hse_equilibrium`, not as a separate term.
   - **Left out, with reasons:**
     - E10's "10–20 % each" (E22 l. 508) summarises the separate effects below, so it would count them twice.
     - E15 (parametric priors) and E17 (miscentring, A2255) concern methods or clusters without rows.
     - E28 and E29 (Table 4 fraction errors) are at overdensity radii, not per row, and are already in GBAR_ERR.

| term_id | scale | applies_to | moves | status | size | assumption_id | Note |
|---|---|---|---|---|---|---|---|
| `radial_covariance` | point | * | g_obs | not_given_by_source | — | — | E1, E2: the SZ covariance is "accounted for and propagated" (E22 l. 91, 97), but no covariance between radii is released |
| `g_bar_point` | point | * | g_bar | not_given_by_source | — | — | Item 5: GBAR_ERR mixes scales; the source gives no point-scale part |
| `np_smoothing` | point | * | g_obs | not_given_by_source | — | — | E14: "fluctuations on scales smaller than the bin size are suppressed" (E22 l. 235) |
| `reconstruction_bias` | dataset | the five | g_obs | given | 0.05, `upper_bound`, fraction | — | E12: "The nonparametric technique follows the true profile with minimal bias (<5\%)" (E22 l. 309), from the source's mock test of its own pipeline (§3.6), which counts as stated for the sample's method (item 7). NFW "at most 3\%" (l. 309, l. 311) and Einasto "about 6\%" (l. 309) in the note |
| `hse_bias` | dataset | the four | g_obs | given | 0.10, `upper_bound`, fraction, **valid for r ≤ R500 only** | `xray_hse_bias` | E5: "with the exception of a single system that is known to be strongly biased (A2319) … we conclude that our measurements are mildly biased ($<10\%$) out to $R_{500}$. The HSE assumption is likely to be a poorer approximation beyond this point" (E22 l. 502). The R500 is the source's (Table 1 R500,TOT; part A §2). Beyond R500 the source gives "a mild contribution of nonthermal pressure ($10-20\%$) at $R_{200}$" (l. 539); this is in the note and on the page, not a size. In the note: simulations "$5-30\%$ at $R_{500}$" (E3, l. 502); E30's "validity … at large radii is unclear" (l. 373). One-sided: hydrostatic g_obs is biased low. Never applied as a correction |
| `hse_bias_a2319` | dataset | `aeg-s-000183` (A2319) | g_obs | not_given_by_source | — | `xray_hse_bias` | E7: "a single system that is known to be strongly biased (A2319)" (E22 l. 502); the quotes in `hse_statements.csv` (E22 l. 435, l. 502; Paper II l. 80). No size is stated for A2319 |
| `nonthermal_pressure` | system | * | g_obs | given_by_other_source | `size_column` `x_xcop_alpha_nt_r500` (R200 value in `x_xcop_alpha_nt_r200`), `as_released`, fraction of total pressure (or as printed; item 6) | — | Ettori & Eckert 2022 Table 1, "at $1 \sigma$ c.l." (l. 276); same programme, not independent: computed from the 2019 thermal-only masses (l. 182). Median trend "$b(0.1 R_{500}) \approx 0.5 b(R_{500})$" (l. 377). Overlaps `hse_bias`; the two are not added. Never applied as a correction (§3c) |
| `gas_inhomogeneity` | dataset | the five | g_obs | given | 0.10, `upper_bound`, fraction | — | E8: "the impact of gas inhomogeneities is small ($<10\%$)" (E22 l. 504). Temperature inhomogeneities "$\sim10\%$" (l. 311, citing other work) in the note. Would also move the gas mass, and so g_bar; that effect is not stated |
| `xmm_calibration` | dataset | the five | g_obs | not_given_by_source | — | — | E9: the size is cited from other work: "effective area calibration (15\%)" (E22 l. 311, citing Schellenberger 2015); "reaches $\sim20\%$ for 10 keV plasma" (l. 506). Conditional and one-sided: "If the \emph{Chandra} temperatures are correct, our masses at fixed radii would be underestimated by a similar amount" (l. 506); "mostly affects the regions located inside $0.5 R_{500}$" (l. 506) |
| `mass_model_choice` | system | * | g_obs | given | `size_column` `x_xcop_mass_model_frac`, `as_released`, fraction | — | **The one Atlas-computed `given` size (item 7; D-105 pending, O2).** Part A A7 (fixed there as this term): per cluster, the largest \|ratio − 1\| across GP/Einasto (R500 from R3), GP/NFW and Einasto/NFW (NFW = Table 1 M500 at Table 1's R500), from `result_part_a.json`, in `x_xcop_mm_*`. E22's sample statement: methods "within 3\%" in median and NFW against NP "less than 10\%" (l. 373). Paper II's Einasto against NFW M500 (§3b). Never applied as a correction |
| `cosmology` | dataset | * | both | not_given_by_source | — | — | E22 adopts H0 = 67.8, Ω_m = 0.308 (l. 56); its central-galaxy and satellite sources assume H0 = 73 and 70, and harmonisation is not stated (§3.2 item 3). No alternative is tested by the source; the distance dependence is not computed in v2 |
| `gas_density_conversion` | dataset | the five | g_bar | not_given_by_source | — | — | The conversion from X-ray emissivity to gas density is not stated (§3.1) |
| `bcg_ml` | system | * | g_bar | not_given_by_source | — | — | E18: dynamical mass-to-light ratio; its error is dominated by the weak-lensing mass and "constant with radius" (E22 l. 111). Photometry "$< 0.25$ mag arcsec$^{-2}$" and kinematics "$\pm4.7$ per cent" are inputs, not the size of this term |
| `bcg_ml_extra_mass_model` | dataset | the systems named in `bcg_dm_systems.md` (default: the five; if the reading decides A644 and A2319 only: `aeg-s-000177;aeg-s-000183`) | g_bar | given | 0.083, `as_released`, fraction | — | E19 (reader A): including an extra mass component in the central-galaxy dynamical models lowers the fitted mass-to-light ratio by "8.3 $\pm$ 2.9 per cent on average" (E22 l. 109, which names the component "a DM mass component"). If the reading returns "not decidable", `applies_to` is the five and the note says the source may mean A644 and A2319 only |
| `bcg_jam_geometry` | dataset | the five | g_bar | given_by_other_source | 0.15, `upper_bound`, fraction | — | E20: "changing our cylindrically-aligned JAM models to spherically-aligned JAM models, results in the best-fitting $\Upsilon_{\star \rm DYN}$ parameters changing by up to $\sim$ 15 per cent" (Loubser et al. 2020, l. 547). Same programme, not independent |
| `bcg_sersic_extrapolation` | system | * | g_bar | not_given_by_source | — | — | E21: measured "only within a limited radial range out to $\sim50$ kpc", then a Sérsic form (E22 l. 404) |
| `satellite_cosmic_variance` | system | * | g_bar | not_given_by_source | — | — | E22 (reader A's term E22): estimated with Moster et al. 2011 (E22 l. 116); shown separately by Ghizzardi (l. 705); no size stated in E22 |
| `satellite_flux` | system | * | g_bar | not_given_by_source | — | — | E23: bootstrap of the fluxes (Ghizzardi l. 712); no size stated |
| `satellite_gnfw_smoothing` | system | * | g_bar | not_given_by_source | — | — | E24: the profiles are "quite noisy and not smooth" and fitted beyond 100 kpc with a gNFW of fixed shape (E22 l. 408); which parameter set is not stated (§3.2 item 1) |
| `satellite_projection` | system | * | g_bar | not_given_by_source | — | — | E25: whether the satellite profile was deprojected is not stated (§3.2 item 1; #124). Ghizzardi: "75$\%$ of the mass obtained integrating along the line of sight lies within the sphere with radius $R_{500}$" (l. 715). Part A A6 (undetermined) and A9 (1.86–2.42 against Ghizzardi's spherical masses) in the note and on every row (item 9) |
| `satellite_mass_systematic` | dataset | the five | g_bar | given_by_other_source | 0.60, `upper_bound`, fraction | — | E26 (reader A): "Although we lack a clear understanding for the origin of different estimates of $M_{\rm star}$, our comparison shows that we may be underestimating stellar masses by as much as 60\%" (Ghizzardi et al. 2021, `xcop-metallicity.tex` l. 923). Same programme, not independent. Stated for Ghizzardi's own masses; part A A9 shows the shared files hold about twice those masses, so how far the size applies to GBAR is unclear (said in the note). A Salpeter factor "$\sim$ 1.74" appears only in a commented-out line of the source file (l. 926, not printed) and is not used; reader A's "factor ∼2" is noted as its paraphrase. One-sided, upward |
| `icl_omitted` | dataset | the five | g_bar | given | 0.05, `upper_bound`, fraction of the baryon budget | — | E27: "the contribution of ICL to the total baryon budget is expected to be small ($<5\%$)" (E22 l. 410). One-sided, upward. Replaces v1's `icl_fraction` slider in v2 (D-105 pending, O3) |

   - **Registry update for v2** (`data/assumptions.json`). Every assumption named in a v2 row's `assumptions` has an `aeg-d-xcop/v2` entry (validator item on registry ids; D-029 2b).
     - **`xray_hse_bias`** (*subject to D-105 (pending), O3*) gains an `aeg-d-xcop/v2` entry: v1's formulas on `g_obs`, `g_obs_err_lo`, `g_obs_err_hi`, and the same form on `g_obs_err_point_lo/hi`; default 0, range 0–0.2. Its references are read from E22, not v1's 2019 sources: `default_ref` = E22 l. 502 ("mildly biased ($<10\%$) out to $R_{500}$"; the source applies no correction), `range_ref` = E22 l. 539 ("a mild contribution of nonthermal pressure ($10-20\%$) at $R_{200}$"), with l. 502's simulation range "$5-30\%$ at $R_{500}$" in the note. It stays the one slider. Item 12's formula check runs it.
     - **`xcop_hse_equilibrium`** (new): "hydrostatic equilibrium of the hot gas, used to infer M(<r) from its pressure and density profiles". Read at source: E22 l. 130 (the HSE equation, `\label{eq:hse}`), l. 38 ("under the assumption of hydrostatic equilibrium"). Not adjustable; `not_adjustable_reason`: "the method's defining assumption; its bias is the slider `xray_hse_bias` and the terms `hse_bias`, `nonthermal_pressure`". Note: E22 l. 373 ("the validity of the HSE assumption at large radii is unclear").
     - **`xcop_spherical`** (new): "spherical symmetry of the gas, used to deproject the projected profiles". Read at source: E22 l. 97 ("We assumed spherical symmetry and applied a deconvolution … and a geometrical deprojection"). Not adjustable; effect not computed in v2.
     - **`icl_fraction`** (*subject to D-105 (pending), O3*) gets no v2 entry. Its v1 formula scales `g_bar_stars`, which v2 does not have (item 2), and the source gives no radial profile of intracluster light, so any formula on the total g_bar would assume one. Its effect is stated by the term `icl_omitted`.
     - **`stars_cluster_modelled`** (v1, draft) gets no v2 entry: v2's stars come from the source.
     - Every v2 row's `assumptions` lists `xcop_hse_equilibrium`, `xcop_spherical` and `xray_hse_bias=0`.

### C. Structure and flags

8. **Tables.**
   - **Observables** (`tables/observables.ecsv`), two per measurement row:
     - `observed`, `acceleration_released` = GOBS, unit `m / s2`, with the error columns of item 5. Steps, from the hot-gas ladder in its order (§4b): `events;spectra;projected_t_and_density;deprojected_profiles;hydrostatic_mass;newtonian_g`. `source_ref` names the file and row and says "the source computed g: non-parametric hydrostatic reconstruction evaluated at the radii of the data (E22 §3.4, l. 263); g_obs = G M_HSE(<r)/r² (l. 453)".
     - `baryonic`, `acceleration_released` = GBAR, unit `m / s2`, with GBAR_ERR. Steps: `xray;mass;photometry;luminosity;structural_model;newtonian_g`. `source_ref` names the file and row and says "the source computed g, including the central galaxy's dynamical mass-to-light ratio: G (M_gas + M★,BCG + M★,sat)(<r)/r² (E22 l. 456); ICL excluded (l. 410)". The Atlas step `stellar_ml` is not listed, because the source, not the Atlas, applied the mass-to-light ratio.
     - `r_kpc` = RADIUS; `err_level` and `err_level_status` as item 5.
   - **Systems** (`tables/systems.ecsv`): all twelve clusters, v1's `system_id`s, `taxonomy_kind` and `kind_label` as v1, `redshift` from part A §2 (Table 1), the item 6 columns, and `properties` holding only source-given values: Table 1's R500,TOT, M500,TOT and M200,TOT (part A §2).
   - **Plotting.** All 109 rows `plotted = true`, `role = default`, except rows recorded and not plotted under rule 1 by the frozen reading (`not_plotted_reason = other`, quotation in `notes`). No alternative rows (rule 1, part A §5).
   - **Flags.** Every row carries the `no_uncertainty` flag only where an error column is empty for want of a stated error (standard §2); the empty `g_bar_err_point_*` are explained in their column description (item 5), not flagged.
9. **Named items.**
   - **A644 (D-092).** Every A644 row's `notes` and its system page carry D-092's expert-layer note exactly; the page also carries the plain-layer note. Both are checked by a text search of the built page (HTML unescaped). The row flag `reproduction_mismatch` and known issue #136.
   - **A2319 (part A §5).** Every A2319 row's `notes` carries **all** of A2319's statements in the frozen `hse_statements.csv`, in file order, with their locations (expected: E22 l. 435, l. 502; Paper II l. 80). Its page states the asymmetry noted in rule 4. Checked by a text search of the built page.
   - **Hydrostatic bound beyond R500.** The X-COP v2 dataset page states that the `hse_bias` bound holds only out to R500 (E22 l. 502), and gives the l. 539 figure for R200. Checked by a text search.
   - **Stellar projection (part A §5).** Every row's `notes` states "stellar projection: undetermined (part A, A6); stellar normalisation against Ghizzardi et al. 2021: <the cluster's A9 ratio> (part A, A9)", with the A9 ratios as published: A644 2.04, A1795 1.86, A2029 2.42, A2142 2.27, A2319 2.25. Known issue #124.
   - **Centroid shift (part A §5)** is on every measurement row and in the systems table (item 6), continuous, never a label.
   - **Known issues** (`known_issues.json`):
     - #136 (A644); #124 (projection); #129 (stage 2 blocked); the D-091 erratum, linked from the result;
     - a new issue for A3158's negative masses at 18–30 kpc (part A A8), on the system only. Question 5 of `03c` serves as the D-086 notice for it, as D-092 rule 4 does for A644; the issue says so.
   - **Exclusion page text.** The seven clusters' "Recorded, not plotted" text on their system pages states the register's reason, not D-097's equilibrium wording. Checked by a text search of each built page in build 1 of item 12.
10. **Descriptor.**
    - `standard_version` `2.5.1`;
    - `x_publication` `awaiting_authors_consent` (rule 5);
    - **`x_value_change_ruling` = `D-090`** (standard §9; D-093 rule 5, which created the key for exactly this case: "a ruled exception to §10 item 13 (X-COP v2, D-090 rule 1)"; part A §1 l. 29). D-090 has a ruling line, as the validator requires. The v2 dataset page states the ruling and that v2's values differ from v1's (checked in build 1 of item 12);
    - `x_precedence` cites D-089 and D-090 rule 1;
    - `x_second_reading` points to `SECOND_READING.md` and the frozen reading files;
    - `x_baryon_inventory`: hot gas `measured`; central galaxy `measured`; satellites `measured`; intracluster light `stated_negligible` (E22 l. 410, quoted); cold gas as v1. The note says the measured components are released as one total (item 2).
    - `sources.json` lists both archives with part A's hashes (and their members' hashes, recorded at conversion as part A §1 says), E22, Paper II, Ettori & Eckert 2022, Loubser et al. 2020 and Ghizzardi et al. 2021 with their e-print hashes and `bytes` (so `python -m aeg.fetch` works in CI), licence "not stated; asked (#19)" and `redistributable: false` for the archives.
11. **Second reading (D-031 item 3).** One independent reader, as in the order of work.
    - **Pass:** the package equals the frozen reading on every field it holds, by these pairs:
      - `values.csv` RADIUS, GOBS, GBAR against `r_kpc`, `g_obs`, `g_bar` and the observables' values, bit for bit;
      - `values.csv` error columns, through the form in `error_form.md`, against `g_obs_err_*` and `g_bar_err_*`;
      - `model_form.md` against `model_dependence`;
      - `err_levels.csv` against the four level columns;
      - `properties.csv` against `x_xcop_alpha_nt_*` (by item 6's unit rule) and `x_xcop_centroid_w*` in both tables;
      - `hse_statements.csv` against A2319's `notes`;
      - `bcg_dm_systems.md` against `bcg_ml_extra_mass_model`'s `applies_to`;
      - `d096.csv` against the plotting of rule 1.
    - Any mismatch is a fail.
12. **Standard and site,** in two builds:
    - **Build 1, with the v2 tables present locally** (never committed; rule 5):
      - `PYTHONPATH=pipeline python -m aeg.validate data/packages/aeg-d-xcop/v2` passes under 2.5.1 (the full `validate()`);
      - `PYTHONPATH=pipeline python -m aeg.formula_check` passes, including `xray_hse_bias`'s v2 entry;
      - the site builds, and `aeg.site_check` reports 0 errors;
      - the v2 pages show the texts that items 9 and 10 require (text search, HTML unescaped).
    - **Build 2, as deployed** (no v2 tables, as the repository holds it):
      - `git ls-files data/packages/aeg-d-xcop/v2/tables` is empty;
      - the site builds, `aeg.site_check` reports 0 errors, and v1 is the current X-COP version;
      - the built page of X-COP v1's dataset shows the rule 5 sentence (text search, HTML unescaped);
      - no v2 page, map point or download exists.
    - **CI:** the reproduction ledger's hash check passes; the regenerated `checksums.sha256` equals the committed one (rule 5, determinism); no CI log line contains a row value (the conversion prints none).
13. **v1 untouched.** Every file in `aeg-d-xcop/v1/` has the checksum it had at commit `5dc4091`.

**Pass** = all thirteen hold. Anything else is a fail. Part A's result stands beside it, unchanged.

## Not tested here

- Whether the source's error sizes are right.
- Part A's checks. They stand as run (D-091).
- How A644's GBAR was built, the units and R_Δ behind Table 4, the stellar projection, A3158's negative masses, the valid radial range and the meaning of the error columns: all with the authors (part A result, questions 1–6, with question 6 extended).
- The seven clusters' g_bar, and stage 2 (#129).
- The X-COP v2 audit (D-090 rule 3), written and frozen after v2 ships.
- The share links of the archives are already in part A (public). This weakens the consent gate for anyone who reads part A, but is outside part B; it is raised with JvH.

## Open items for JvH before this test is frozen (D-105, pending)

- **O1. Observables for the seven clusters.** **Recommended: none in v2** (rule 2). No row would cite them, their only g_bar is a bound the standard cannot hold, and stage 2 is blocked. Writing their 200-row gas and total-mass profiles as observables would publish values from privately shared files with no use on the site.
- **O2. The `mass_model_choice` size.** **Recommended:** size it from **all** of part A's published A7 pairs, by the rule fixed in item 7 (per cluster, the largest |ratio − 1| across the three pairs), as the one `given` row whose size the Atlas computed, stated as such in its note. Using only the non-parametric/Einasto pair would select the smallest subset after the results were published. E22's sample statement (l. 373: "within 3\%", "less than 10\%") goes in the note.
- **O3. Sliders.** **Recommended:** keep `xray_hse_bias` as the one slider, with references read from E22 (l. 502, l. 539), not v1's 2019 sources. Drop `icl_fraction`: v2 has no stellar component for it to scale, and the source gives no radial profile of intracluster light, so any formula on the total g_bar would assume one. E22's "$<5\%$" (l. 410) becomes the term `icl_omitted`.
- **O4. Rule 1's radial range.** **Recommended:** only explicit exclusion wording counts under D-096 rule 2, as in D-103. E22 l. 528 summarises the analysed range and l. 486 states no exclusion, so the expected outcome is no exclusion. If the authors state a valid range (part A result, question 5), it comes in under a new ruling.

D-105 also records: D-070 items 2–3 superseded for v2 by D-089 and D-090 rule 4 (rule 2), and the A2319 asymmetry between datasets (rule 4).

## Checked before freezing (revision 2, 2026-11-05)

A mock package was built with **placeholder values (not data)**:
- 109 measurement rows over the five clusters, with the item 5 columns (`g_bar_err_point_*` empty; levels empty with status `not_given_by_source`), the component statuses of item 2, the measurement-table centroid columns of item 6, and `assumptions` = `xcop_hse_equilibrium;xcop_spherical;xray_hse_bias=0`;
- 218 observables with the steps of item 8;
- the twelve systems with the item 6 columns (including `x_xcop_mm_*`, `x_xcop_mass_model_frac` and `x_xcop_status`);
- the 22 terms above, parsed from this file;
- a descriptor with `x_value_change_ruling` = `D-090` and `x_publication`, `SECOND_READING.md`, `sources.json` and `checksums.sha256`;
- the three registry entries of item 7 (`xray_hse_bias` v2 entry, `xcop_hse_equilibrium`, `xcop_spherical`) added to a temporary copy of `data/assumptions.json`, restored afterwards.

**Result:** the full `validate()` at 2.5.1 reports **0 problems**; `validate_v22` and `validate_v24` report 0. The first mock run found that no term may carry `in_error_columns = no` unless it is a given point-scale row; this revision says so (item 7).

**Not exercised:** `aeg.formula_check` on the `xray_hse_bias` v2 entry, the site change of rule 5 and the page texts of items 9, 10 and 12 (item 12 runs them on the real package). **No archive value was read for this revision.** The mock and its script are not committed.
