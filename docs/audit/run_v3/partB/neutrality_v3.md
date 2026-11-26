# Audit v3 Part B: neutrality findings and proposed resolutions (plan v3 §3.4)

**Status: proposed, awaiting JvH's rulings.** Each finding must be resolved by a change or by no change with a reason (§3.4). Part B passes only if no deciding finding is left unresolved. Deciding findings are term-scan findings and reader findings under checklist questions 1 to 3.

**Sources:**
- term scan `terms/term_scan.csv`: 247 occurrences, classified in `terms/classified.csv` as 234 allowed and 13 findings;
- reader 1 `reader1/findings.csv`: 34 findings, 17 of them under questions 1 to 3;
- reader 2 `reader2/findings.csv`: 36 findings, 12 of them under questions 1 to 3.

Findings that the readers or the scan share are merged below. Each item names who found it and the question it falls under; where the readers differ, it is counted under the lower-numbered question (§3.4).

## Deciding findings

| # | Finding | Found by | Q | Proposed resolution |
|---|---|---|---|---|
| B1 | **"halo" in Atlas text on the KiDS-1000 v2 and v3 pages:** "the authors' assumed halo", "an assumed hot-gas halo for the variant". | term scan (6), R1, R2 | scan, 1 | **Change:** "the authors' assumed hot-gas distribution". Where the text is in package metadata, it changes in v3, which is not yet released; v2 is released and is not overwritten, so its page notes the wording. |
| B2 | **Plain name "extra pull" for g_obs/g_bar**, used even where the ratio is 1 or below. Seen on the map axes of the Ratio and Scale views, and on Methods. | R1, R2 | 3 | **Change:** plain name "pull ratio (observed ÷ visible)". The expert term "acceleration discrepancy" stays. "Extra pull" is kept only where the ratio is above 1. |
| B3 | **Site name "Atlas of Extra Gravitation"** states a result. Some systems have a ratio below 1, for example NGC 362 at 0.41. | R1, R2 | 3 | **JvH's call** (a ruled name). Option a: no change. The reason would be that the name names the subject, as a field guide is named for what it describes; the About page would say in both layers that the Atlas shows where the ratio is 1 or below too. Option b: rename. |
| B4 | **Reading guidance only for the excess.** The front page explains points above the line but not below it, in both layers, and About opens with "exceeds". | R1 | 1 | **Change:** add a sentence for points below the line, in both layers. About becomes "where and how the observed acceleration differs from". |
| B5 | **Mass framing in the plain layer:** the map's "Mass implied by the observed pull" and "Implied mass"; the symbol M_obs; "dynamical mass" on Methods; the lens page's "Mass that bends the light". | R1, R2 (R2: must fix) | 1 | **Change:** "the observed pull expressed as a mass (g_obs r²/G, a convention)" in both layers. The symbol becomes M_g,obs = g_obs r²/G. The lens label becomes "lensing mass M_E: the mass general-relativistic lensing would need inside the ring". |
| B6 | **"Pull budget" and "Detected share" on system pages,** which present g_bar/g_obs as a share of a total. | R1, R2 (R2: must fix) | 1 | **Change:** the chart becomes "Pull from visible matter ÷ observed pull" with no "share" or "budget", and the reference line becomes "equal pulls". |
| B7 | **About: the reviews listed both centre on one account,** and the heading "The relation taken to one new kind of system" presumes that a relation exists. | R1 | 2, 3 | **Change:** add a review of the other main account (with its source read and cited first), or list none. The heading becomes "The g_obs–g_bar comparison for one kind of system". |
| B8 | **Tests template:** "what it does not yet explain". | R1 | 2 | **Change:** "the Atlas measurements it does not address". |
| B9 | **KiDS dataset title "…radial acceleration relation…"** used as the Atlas's own label. | R1 | 3 | **Change:** "KiDS-1000 weak lensing, stacked isolated lenses (Brouwer et al. 2021)". The paper's own title stays in the citation. |
| B10 | **A7 "Unusual configurations" also holds systems whose kind is unsettled.** Crater is labelled a globular cluster although its kind is disputed. | R1 | 3 | **Change:** a separate "kind not settled" label, outside A1 to A7, for lenses and systems whose readers disagree. Crater is shown as "kind disputed by sources". This changes registry labels, so it needs a ruling. |
| B11 | **Coverage:** "a limit on anomalous acceleration". | R2 | 1 | **Change:** "a limit on any acceleration beyond the Newtonian (ephemeris) prediction". |
| B12 | **Methods:** "Flat ΛCDM" names a model that contains one account. | R2 | 2 | **Change:** "a flat cosmology with each source's H₀ and Ω_m (Ω_Λ = 1 − Ω_m)". |
| B13 | **Dwarfs:** systems are taken off the map on their sources' statements of disequilibrium or tides, which may be interpretations made within one account. | R2 | 2 | **JvH's call.** Option a: no change. The reason would be that D-097 shows these systems in a "recorded, not plotted" list and quotes each source, so nothing is hidden. Option b: plot them with a flag instead. |

## Other findings (questions 4 to 6, reported and resolved, not deciding)

Most are plain/expert mismatches (27) and missing source routes (12). Three are factual errors, which I propose to fix first:
- **X-COP g_obs "from the non-parametric hydrostatic reconstruction"** on Methods and the X-COP dataset page. This contradicts D-119.
- **Dwarf methods page:** some citations carry another paper's arXiv ID, for example "Geha 2026 ApJ 999 140 (arXiv 0706.0516v2)".
- **The X-COP v3 plain layer says "All checks passed"** beside a technical layer that says failures stand.

The full lists are in the two readers' `findings.csv`.

## Not counted

The term scan gives 7 matches that break no rule: 5 are "A0", a kind code, and 2 are "explains" as an ordinary verb. They are resolved by no change, with that reason.
