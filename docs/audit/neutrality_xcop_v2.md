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

Pending.
