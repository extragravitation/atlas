# X-COP v2 audit: neutrality findings (plan §3)

**Pages:** `datasets/aeg-d-xcop/v2/` and system pages aeg-s-000177 (A644), aeg-s-000179 (A1795) and aeg-s-000183 (A2319). Built from commit `81a026b`.

**Records:** `run_xcop_v2/partB/reader1/findings.csv` (41 findings), `run_xcop_v2/partB/reader2/findings.csv` (24 findings), and `run_xcop_v2/partB/terms/classified.csv` (98 occurrences, all allowed).

## Must-fix findings, merged

| # | Page(s) | Finding | Readers |
|---|---|---|---|
| X1 | the system pages | The pull-budget legend calls the g_bar error "one sigma" and "shared by the whole system", and the g_obs bars "one-sigma bars". The package records the level as not given by the source, and the error as mixing point-scale and whole-system parts. | 1, 2 |
| X2 | all four | The "mass-model choice" uncertainty term shows status "given by the source", but the Atlas computed it. | 1 |
| X3 | A2319 | The plain subtitle says the gas is "held in balance by the pull", directly below the flag quoting the source's "clear evidence of a breakdown of hydrostatic equilibrium". | 2 |
| X4 | A2319 | The hydrostatic-bias slider's 0–0.20 "full published range" is applied to A2319, but the page says no size is stated for it. | 2 |
| X5 | dataset page | The plain summary says "109 measurements from 12 clusters"; all 109 come from 5. | 1, 2 |

## Should-fix themes

- **Plain-language layer:**
  - "Matches the source" (plain) claims more than "Reproduction: passed" (expert);
  - "held in balance by the pull" on A644 and A1795 states an assumption as fact;
  - "too low" is added to a quote that gives no direction;
  - chart captions describe stacked layers that X-COP (total g_bar only) does not draw;
  - "all detected matter" overstates what is counted;
  - several blocks have no plain version.
- **Routes to sources:** H0 values without a line citation; "roughly half the size" is never computed; the system pages drop the Source column from the uncertainty table.
- **Scope labels:** the A2319-only and two-system uncertainty terms are labelled "whole dataset".
- **Needs a ruling (method):** the only X-COP slider, hydrostatic bias, can only raise g_obs. The g_bar terms with published sizes (satellite stellar mass, intracluster light) have no slider, so the interactive view can widen the ratio but never narrow it (reader 2).

## Resolution

Resolved on branch `site/xcop-neutrality` (2026-11-06), in the shared components and the site's data mapping, so the fixes apply to all five X-COP clusters (and, where the cause was shared, to other datasets). No package file, frozen file, taxonomy or decision-log entry was changed. Every finding row is resolved in `run_xcop_v2/partB/resolutions.csv` (65 rows: 41 reader 1, 24 reader 2).

| Item | What changed, or why not |
|---|---|
| X1 one-sigma legend | Legend text is built from each system's rows: `err_level_status` and `g_bar_err_level_status` (`not_given_by_source`) give "confidence level not given by the source"; empty `g_bar_err_point_*` gives "they mix point-scale parts with parts shared by the whole system". "one sigma" is no longer said for X-COP; it stays only for packages with no level columns (SPARC). Both layers; measurement-table headers read "−/+ error" where the level is not given. |
| X2 mass-model status | A size column the package marks "Atlas-computed" now shows status "computed by the Atlas, not given by the source", with its route (the column `x_xcop_mass_model_frac` and its package description). |
| X3 equilibrium as fact | X-COP plain labels now say the pull is worked out from the hot gas "assuming the gas is in balance". On A2319 the subtitle adds that the source says this assumption breaks down for the cluster, from the D-109 flag. |
| X4 A2319 slider range | Kept, with a note, because the registry gives `xray_hse_bias` scope `dataset` and every A2319 row lists it as adjustable. Where every package term tied to the assumption has no size for a system (`hse_bias_a2319`), the slider, chart hint, range legend and term row say the range is the registry's dataset-wide range and not one stated for A2319. |
| X5 cluster count | Counted from the measurement rows: "109 measurements from 5 clusters … 7 more clusters are listed in the record with no measurements". The datasets index card had the same error and is fixed. |
| Slider asymmetry (ruling) | Slider kept (JvH). By the slider (map, scale strip, system pages) and under the dataset page's assumption table, in both layers: the g_bar terms with published sizes cannot be adjusted because the source releases g_bar only as a total; the Atlas does not split it without the components; the authors have been asked for the component profiles. The term list is computed from the package and names four terms: the two the ruling names (satellite stellar mass, intracluster light) and two central-galaxy terms (extra mass component, model geometry). |
| Plain: "Matches the source" | Both layers now read "part B: passed", with part A's result named beside it. Datasets index as well. |
| Plain: "held in balance" (A644, A1795) | As X3. |
| Plain: "too low" | Removed. The plain text now quotes "mildly biased", with no direction. |
| Plain: stacked-layer captions | Caption, plain caption, aria-label and speed caption say g_bar is drawn as one total when the system has no component values. |
| Plain: "all detected matter" | Changed to "the detected matter counted (listed below the chart)". |
| Plain: missing plain versions | Added for the g_bar error legend, the stellar row notes (parsed from the note), the Facts block (labels, notes, method) and the equilibrium-rule paragraph, which now matches the expert scope (velocity-dispersion measurements). "Share matched" (reader 2) became "Detected share" and "as a share of the observed pull". |
| Routes: H0 = 73 and 70 | No line is recorded in the package. The page now says "as stated by" Loubser et al. 2020 (73) and van der Burg et al. 2015 (70), says the package has no line, and routes to the reader record that has them (`docs/sources/readings/xcop-e22-2026-11-03/reader-A.md` l. 319). |
| Routes: "roughly half the size" | Not computed: the alternative's normalisation is not defined, so no number could be computed without inventing a rule. The sentence is removed from the displayed note, and the page says why. The build fails if the package sentence changes. |
| Routes: Source column | Restored in the uncertainty table on every system page. |
| Scope labels | Read from `applies_to`. A term listing fewer than the systems with rows shows "one system only" or "N systems together", naming them, and the recorded scale. Terms covering every system with rows keep "whole dataset". |
