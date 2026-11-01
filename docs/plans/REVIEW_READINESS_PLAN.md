# Review-readiness plan

**Adopted:** 2026-11-01 (D-080). **Goal:** an Atlas that a specialist in galaxy dynamics or cluster lensing can check line by line and find nothing to dismiss: every published number reproduced or its difference explained, errors shown on both axes, methods written down, and an outside reader who has already tried to break it.

**What this plan is not.** It adds no datasets. New dataset work (A9 clusters, A3, A5, A8 and the rest of #48) is frozen until this plan's work packages 1–6 are done or JvH lifts the freeze.

## Rulings (JvH, 2026-11-01)

1. Freeze new datasets.
2. Draft the SPARC courtesy note. It lives in Dropbox (`07 AEG/05 Correspondence/Drafts/`), never in this repository. JvH sends it.
3. Order: fidelity first.

## Work packages, in order

### WP1. Fidelity: every published number reproduced, or the difference explained

- **#8 SPARC, 4 points.** Test the stated hypothesis (a different data version) against the 2016 archival copy (CDS J/AJ/152/157) through any reachable VizieR mirror. Record the outcome in `REPRODUCTION_RESULT.md` whichever way it goes. The courtesy note asks the authors the same question.
- **#19 X-COP, 3 clusters.** Same treatment: locate the source of the difference between the archive profiles and the published Table 1, or state it as unresolved with the evidence.
- **#9 SPARC package.** Close the remaining items, including the licence question (also asked in the courtesy note).
- **A SPARC RAR selection view.** Show the Atlas points under Lelli et al. (2017)'s own selection alongside the full set, so a reader can compare like with like. It uses existing data only.
- **A Reproduction page.** One page listing every dataset's reproduction test, its frozen hash, its result and its open mismatches, linked from each dataset page.

### WP2. Error budget on both axes

- Show the uncertainty on g_bar as well as g_obs, wherever the source allows: distance, inclination and the stellar mass-to-light ratio, with correlated errors marked as correlated rather than added in quadrature.
- **#64:** fix the KiDS-1000 `no_uncertainty` wording so it cannot be read as g_obs having no errors.
- Each error term traces to the source's stated value or a published range (no invented errors).

### WP3. Independent adversarial audit

- A re-derivation of a random 5% of measurements from the original sources by a reader who has not seen the Atlas values. The sample is drawn from a seed frozen before drawing.
- A neutrality audit of every page and label: does any word assume a cause or favour an account?
- Findings are logged publicly as corrections or as no-change, with the reason.

### WP4. Methods

- A methods page for each channel (dynamics; lensing) giving the reference calculation, the assumptions and their published ranges, and the frozen tests.
- The methods paper (JOSS and arXiv astro-ph.IM) drafted from those pages.

### WP5. Reproducibility and downloads

- A clean one-command rebuild runs in CI from an empty checkout and compares hashes with the release.
- Downloads in the formats specialists use: ECSV and CSV per dataset, with a column dictionary, plus a single combined table.

### WP6. Open issues and accessibility

- Every open issue is closed or carries a plain public statement of its status on the known-issues page.
- The accessibility findings are fixed and re-checked.

### WP7. Outside review

- A review packet: what the Atlas claims and does not claim, the reproduction page, the error budget, the audit report, and the known issues.
- Whom to invite, and when, is JvH's decision.

## Done means

WP1–WP6 complete, with checks passing. Then a v0.2 release (JvH tags it). Then WP7.
