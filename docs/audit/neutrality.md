# Audit v2: neutrality findings (plan §3)

**Audited site:** the build of commit `e382edb`, 644 pages.

**Readers**, all fresh agents:
- one term classifier (§3.2);
- two independent page readers (§3.3), covering 29 pages: Home, About, Methods, Known issues, For data providers, Coverage, every dataset page, and two system pages per dataset with systems, chosen with the seed. KiDS has no system pages.

**System pages drawn** (rank 1 and 2 by SHA-256(seed + `|page|` + system_id), over each package's v1 systems):

| Dataset | Pages |
|---|---|
| SPARC | aeg-s-000081, aeg-s-000067 |
| X-COP | aeg-s-000183, aeg-s-000185 |
| Strong lensing | aeg-s-000500, aeg-s-000410 |
| Globular clusters | aeg-s-000241, aeg-s-000255 |
| Dwarfs | aeg-s-000388, aeg-s-000344 |

**Full records:**
- `run_v2/partB/terms/classified.csv`
- `run_v2/partB/reader1/findings.csv`
- `run_v2/partB/reader2/findings.csv`
- each reader's `pages_reviewed.csv`

## Term scan (§3.2)

The scan found 208 occurrences: 198 allowed and **10 findings**.
- **Allowed:**
  - 146 name a source's own fitting function (NFW, Einasto, Burkert in the X-COP papers);
  - 44 quote a source;
  - 1 is in the accounts section;
  - 1 is the single "mass discrepancy" note;
  - 6 are false matches: "A0" is the coverage code for the Solar System (5), and "this page explains" refers to the page (1).
- **Findings:**
  - T1: "explains" ×3. Home ×2 and Methods ×1 say that detected matter "explains" the pull, a causal verb in the Atlas's own voice.
  - T2: "modified Newtonian dynamics (MOND)", in the Methods lens section.
  - T3: "dark-matter halos", in the Methods lens section.
  - T4: "halo" ×4. The KiDS v2 dataset page calls the source's hot-gas allowance a "(hot-gas) halo" in the Atlas's own voice.

The classifier marked one X-COP v1 row as borderline but allowed: the NFW-shaped profile adopted for modelled stars (D-022), credited to Ettori et al. 2019 §5. Claude agrees that it names a source's method.

## Page review (§3.3)

| Reader | Findings | Must fix |
|---|---:|---:|
| Reader 1 | 83 | 5 |
| Reader 2 | 50 | 3 |

Merged, the must-fix findings are:
- **N1. Methods page, lens section.** It names MOND as the origin of the g_obs–g_bar plane, outside the accounts section. Both readers found this; it is the same text as T2.
- **N2. Methods page, lens section.** "Models of dark-matter halos" is used as description. Both readers found this; it is the same text as T3.
- **N3. Coverage page, release gate.** It calls globular clusters "a control where Newtonian gravity on detected matter is expected to suffice". That label carries an expected result. Both readers found this.
- **N4. Two lens system pages (aeg-s-000410, aeg-s-000500).** They say g_obs/g_bar "does not depend on [cosmology] to first order". Reader 1 says D-094 and the strong-lensing v2 page say otherwise. This needs checking at source before the fix.

**Recurring should-fix themes** (details in the CSVs):
- **Wording that assumes an outcome:**
  - "explains" wording;
  - "Excess" and "how many times stronger" labels that assume g_obs > g_bar;
  - the pull-budget chart, which stacks the extra pull as one more component;
  - "extra pull" defined as a difference on system pages but as a ratio on Methods.
- **Uneven rules and cuts:**
  - the out-of-equilibrium exclusion is applied to dispersion data only, so A2319 stays plotted;
  - the z < 0.30 lens cut has no stated data reason.
- **Plain-language layer:**
  - several pages have no plain version: reproduction results, known issues, the changelog, most of Coverage;
  - some plain cells repeat the expert text word for word;
  - some plain lines claim more than the expert text.
- **Stale or contradictory text:**
  - Coverage says three datasets are in hand, then six;
  - the dwarf M/L slider range is copied from the globular-cluster slider;
  - flag counts differ between places;
  - "No sliders yet" appears on GC pages that have sliders;
  - "hot gas: absent" is shown where it is not measured.
- **Numbers without a visible route to their source:** slider sources are given as repository paths with no links, and nine dataset pages have an empty "Source and conversion" section.

## Resolution

Resolved by the "site fixes 1" pull request after #187. Each fix was re-checked with `term_scan.py` on the rebuilt site.

| Finding | Resolution |
|---|---|
| N1 / T2 (MOND) | Changed. "This plane is the one used in published studies of the radial acceleration relation." No account is named. |
| N2 / T3 (dark-matter halos) | Changed. The account clause was removed: "Enclosed-mass profiles and dynamical-to-baryonic mass ratios are standard in mass modelling." |
| N3 (Coverage "control … expected to suffice") | Changed by a new taxonomy version, `docs/plans/TAXONOMY_v2.md` (D-108; deviation #22), which reads "the high-acceleration end of the range: the Solar System (as a limit) and globular clusters". The Coverage page renders version 2. Version 1 stays frozen. The Methods page phrase was changed in the first batch of fixes. |
| N4 (lens pages: ratio "does not depend on [cosmology] to first order") | Changed. It now says the ratio depends on distance at first order, g_obs/g_bar ∝ 1/D (D-094, which corrects D-064 item 4), in both the expert and plain text. |
| T1 ("explains" ×3, plus the same verb in the system-page chart caption and aria label) | Changed to "matches", with "Newton's gravity from the detected matter" as the subject. |
| T4 ("halo" ×4, KiDS v2 page) | **Partly changed.** "Assumed hot-gas component" is now used in the site text and the assumption registry (2 of 4). The other 2 come from the KiDS v2 package's own `datapackage.json` and frozen result text. Packages are not edited (D-006), so these change when the package is re-issued (D-107 rule 4). |

The should-fix findings are resolved in later batches and logged here.

### Should-fix findings

Counts from the three resolution files. Batches A and B are #195 and #196; batch C applies D-109 and resolves the batch A and B items marked `needs ruling` that D-109 covers.

| File | Changed | No change | Needs ruling |
|---|---:|---:|---:|
| `resolutions_batch_a.csv` | 19 | 2 | 7 |
| `resolutions_batch_b.csv` | 67 | 14 | 18 |
| `resolutions_batch_c.csv` | 12 | 0 | 0 |

Batch C changes all 7 open items of batch A and 5 of batch B (pull budget, "extra pull", the Excess lens, the A2319 equilibrium asymmetry, the reason for the z < 0.30 cut). No `needs ruling` row concerned TeX in quotes; D-109 rule 4 is applied across the site anyway.

**Still open: 13 items of batch B.** Eight change only with a package re-issue (package titles and column text, a registry identifier) or a new taxonomy version. Five are method-framing questions held for JvH after v0.2 (the default-lens lineage sentence, the pattern schedule, independence of exclusion evidence, the hydrostatic-bias labels and range).
