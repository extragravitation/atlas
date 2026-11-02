# Plan to finish data validation (D-080 WP2 and WP3)

**Written:** 2026-11-02, at JvH's request ("we need a plan to finish data validation"). It schedules work already ruled (D-080, D-083, D-084, D-081/D-082). One open question needs a ruling (§4).

**"Done" means:**
- all six shipped datasets are re-issued under the current standard, with uncertainties by scale (WP2);
- the independent audit has run and its result is published, pass or fail (WP3).

The patterns pages come after this (D-085 item 8).

## 1. Where things stand

| Dataset | Current version | Standard | Observables | Second reading | Uncertainties by scale |
|---|---|---|---|---|---|
| SPARC | v2 | 2.3.0 | yes | yes (32 269 values, 0 disagreements) | **done** |
| KiDS-1000 | v1 | 1.2.1 | no | no | no; g_bar has no error at all (#64) |
| X-COP | v1 | 1.2.1 | no | no | no; profile errors correlated; modelled stars carry no error |
| Dwarf galaxies | v1 | 2.0.0 | yes | yes | no; distance moves both axes |
| Globular clusters | v1 | 2.0.0 | yes | yes | no; distance moves both axes; MW-PAL1 ruling (D-046) still awaits the outside reader |
| Strong lenses | v1 | 2.1.0 | yes | yes | no; 38 rows lack a printed g_obs error (to check) |

**The audit:**
- The plan is frozen (v2, D-082).
- The seed is the first NIST beacon pulse at or after **2026-11-03 00:46:17 UTC** (18:46 CST, 2 November).
- No sample has been drawn. The audit runs after WP2.

## 2. How the work is ordered, and why

The proven SPARC route had four steps: read at source, freeze the test, convert, then an independent second reading. Two changes make it cheaper and more coherent for the remaining five:

1. **Read all five sources first, in one pass** (step A). Every uncertainty term and every new quantity is then known before anything is frozen.
2. **One standard change for all of them** (step B). The likely needs, to be confirmed by step A:
   - an observed or baryonic quantity for KiDS's released g_bar;
   - a stated rule for one-value systems (dwarfs, globular clusters, lenses), where "one point" and "whole system" coincide but distance still moves both axes together.

   One minor version (2.4.0) is better than one per dataset.

## 3. Steps

| Step | Work | Who decides | Estimate |
|---|---|---|---|
| **A. Readings** | For KiDS (Brouwer et al. 2021 and its README), X-COP (Ettori et al. 2019 §5 for the modelled-star scatter; the archive's error columns), dwarfs, globular clusters and lenses (the already-read originals, re-checked for the uncertainty statements): every uncertainty term, its size as stated, its scale, and what it moves, with quotes and locations. Written to `docs/sources/uncertainty-readings.md`. | — | 1 session |
| **B. Standard 2.4.0** | Only what A shows is needed. Frozen on merge. | JvH approves | short |
| **C. #110 rule** | One rule for `model_dependence` across datasets (§4), applied in every v2. | **JvH rules** | short |
| **D. Frozen tests** | One v2 reproduction test per dataset, as SPARC's: values bit-for-bit equal to v1; uncertainty decomposition; the exact terms list; the full current structure. For KiDS and X-COP this adds observables and an independent second reading. | JvH approves each | 1 session for all five |
| **E. Conversions** | Converters and tests, in this order: KiDS, X-COP, dwarfs, globular clusters, lenses. Second readers run in the background, where needed (KiDS, X-COP). | merges | 2–3 sessions |
| **F. Site** | The reproduction ledger and uncertainty sections for each v2 (the components exist since #115). Map bars use point-scale columns. | merges | with E |
| **G. Audit (WP3)** | As frozen: read the beacon pulse, draw 254 rows with `sample_v2.py`, commit the reader brief and comparison script before any reading is opened, two blind readers per row, adjudication at source, neutrality term scan and page review, and `AUDIT_RESULT.md` published pass or fail. | — | 1–2 sessions |

**Total:** about 6–8 working sessions.

**Milestone after G:** a v0.2 release (JvH tags it), then the patterns pages, then the outside-review packet (WP7).

## 4. Ruling needed now: #110, one rule for `model_dependence`

Every v2 sets this label, so the rule must exist before step D. The options:

- **(a) Substitution rule (recommended).** `observable_form` applies when a fitted functional form stands in for missing data **at the compared quantity**. Examples: an assumed gas profile where no profile was measured, or a fitted dispersion profile used instead of binned data. A form fitted to well-sampled data that only interpolates or extends it (Sérsic or King light profiles, exponential stellar extrapolation) is `none`, and is stated in the baryon inventory. `total_mass_form` is unchanged.
  - **Effect:** globular clusters move from all `observable_form` to mostly `none`, except where a form substitutes for data. The dwarfs and SPARC v2 already conform. Lenses are to be checked.
- **(b) Any-fit rule.** Any fitted form anywhere in either side's chain is `observable_form`.
  - **Effect:** nearly every row of every dataset is labelled, and the label stops discriminating.
- **(c) Leave as is**, documenting each package's usage.
  - **Effect:** inconsistent across datasets, which a reviewer will notice.

The recommendation is (a), because it is the reading of D-029's intent ("a functional form fitted to an observable" used for the comparison) that keeps the label informative. Under D-031, a rule changed after a result applies to later packages only, so it applies through the v2 re-issues and v1 stays as published.

## 5. Risks, stated once

- **Sources unreachable from the workspace** (CDS, astroweb). Hash-identical mirrors are acceptable locally, and CI fetches the canonical copies.
- **A v2 test may fail.** Then it is published as such, as SPARC v1's was.
- **The outside reader is still needed** for the MW-PAL1 ruling (D-046) and the D-019 note. This is WP7, not a blocker for WP2 and WP3.
