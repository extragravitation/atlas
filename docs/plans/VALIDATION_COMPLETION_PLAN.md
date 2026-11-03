# Plan to finish data validation (D-080 WP2 and WP3)

**Written:** 2026-11-02, at JvH's request ("we need a plan to finish data validation"). It schedules work already ruled (D-080, D-083, D-084, D-081/D-082). Rulings: #110 as option (a) (D-087) and the notice rule (D-086), both 2026-11-02. Updated 2026-11-03 for D-089 and D-090: the X-COP exception, its own audit, and A8 stage 2.

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
| **B. Standard 2.4.0** | Only what A shows is needed. Already known: a bound on g_bar for X-COP A8 stage 2 (#129), probably as a new optional column, so the version number follows standard §0. Frozen on merge. | JvH approves | short |
| **C. #110 rule** | One rule for `model_dependence` across datasets (§4), applied in every v2. | **JvH rules** | short |
| **D. Frozen tests** | One v2 reproduction test per dataset, as SPARC's: values bit-for-bit equal to v1 (**except X-COP**, rebuilt from Eckert et al. 2022 under D-089 and D-090, with its own test in `data/packages/aeg-d-xcop/v2/REPRODUCTION.md`); uncertainty decomposition; the exact terms list; the full current structure. For KiDS and X-COP this adds observables and an independent second reading. | JvH approves each | 1 session for all five |
| **E. Conversions** | Converters and tests, in this order: KiDS, X-COP, dwarfs, globular clusters, lenses. Second readers run in the background, where needed (KiDS, X-COP). | merges | 2–3 sessions |
| **F. Site** | The reproduction ledger and uncertainty sections for each v2 (the components exist since #115). Map bars use point-scale columns. **X-COP A8 stage 2 (#129):** draw g_bar lower limits as tracks with arrows in every view (map, excess, mass, scale, speed, surface density, system pages, downloads), checked on desktop and phone; plot the seven clusters only if the frozen test's A3 condition holds. | merges | with E |
| **Emails** | As §5: SPARC today; X-COP and KiDS this week, before their tests are frozen; Baumgardt before v0.2. | JvH sends | — |
| **G. Audit (WP3)** | As frozen (the X-COP stratum audits v1; D-090): read the beacon pulse, draw 254 rows with `sample_v2.py`, commit the reader brief and comparison script before any reading is opened, two blind readers per row, adjudication at source, neutrality term scan and page review, and `AUDIT_RESULT.md` published pass or fail. | — | 1–2 sessions |
| **G2. X-COP v2 audit (D-090)** | Its own plan, same method, frozen after X-COP v2 ships and before its seed exists. Runs with G if v2 has shipped; otherwise v0.2 states that X-COP v2 is not yet audited. | JvH approves the freeze | 1 session |

**Total:** about 6–8 working sessions, plus G2.

**Planned beyond the core steps, not to be dropped:** X-COP A8 stage 2 (#129), expected in v0.2, about 4–6 sessions from 2026-11-03. v0.2 does not wait for it.

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

## 5. Correspondence with data owners

Drafts live in Dropbox (`07 AEG/05 Correspondence/Drafts/`), never in this repository. JvH sends every email from his own address and tells Claude the date. The date is then recorded on the related issue and in the send list.

**What is and is not mandatory.**
- **No email to a data owner is a gate** for building or shipping a package. Under D-004 (amended), "Permission emails are courtesy notices, not gates". Where a licence is unclear, the Atlas links rather than redistributes, as it already does. A reply that changes data or a citation is applied as a new version.
- **Proposed rule (needs a ruling, D-086):** before a release that publicly flags a source's data, as a known issue or a recorded inconsistency, the source's authors are sent a notice describing the flag, and the send date is recorded. This would make three notices mandatory **before v0.2**: SPARC, X-COP and the Baumgardt globular-cluster database. Reason: authors should hear about a public flag from us, not discover it. v0.1 already flagged SPARC (#8) and X-COP (#19) without a notice, so this is a catch-up, stated as such.

**Schedule:**

| Email | To | Purpose | When | Mandatory? |
|---|---|---|---|---|
| `01_Lelli_SPARC_v3` | F. Lelli (copies to S. McGaugh and J. Schombert are JvH's choice) | The four points (#8), the licence (#9), the header layout error | **Today (2 Nov)**, as JvH planned | Yes, under D-086 if ruled (SPARC is flagged) |
| `03_Eckert_Ettori_XCOP_v5` | D. Eckert, cc S. Ettori | Archive provenance (#19), licence, profile covariance (D-083 item 5) | **This week, before the X-COP v2 test is frozen (step D)**, so that any answer can shape v2 or a later version | Yes, under D-086 (X-COP is flagged). Questions 4–5 (new-data requests) stay JvH's choice under the freeze |
| `02_Brouwer_KiDS` (refresh to v3 after step A) | M. Brouwer | Licence; the ±0.2 dex stellar-mass files (the visible-matter uncertainty KiDS v2 needs); lens redshifts per bin | **After the KiDS reading (step A) and before the KiDS v2 test is frozen**: this week | No. No KiDS data are flagged (#64 is the Atlas's own wording). Strongly recommended, because the ±0.2 dex files are the best route to a real g_bar uncertainty |
| New: `08_Baumgardt_GC` (to be drafted after step A) | H. Baumgardt | Pal 1: the database's r0pc is inconsistent with its own angular radius and distance (D-046); the outcome of the Atlas's reproduction | **Before v0.2** | Yes, under D-086 (Pal 1 is flagged in a published test) |
| Dwarf galaxies and strong lenses | Many original authors | — | Not planned: no source data are flagged | No |
| `04` CLASH, `05` HSC-XXL, `06` Bullet, `07` ALPAKA | New-dataset requests | New cells | **Held** until the new-dataset freeze (D-080) is lifted, after v0.2. The 8-week gap clock (D-028) starts only when they are sent | No |
| Pattern-page reviewers (D-085 item 4) | Anchor authors (Lelli et al.) and at least one galaxy-formation group | Review of the RAR, BTFR and flat-rotation pages | After WP3, when the drafts exist. JvH chooses whom | Not for v0.2. Required before the pattern pages are published (D-085 rule) |
| Outside reader (D-011) | Independent reviewer, not a data owner | The MW-PAL1 ruling (D-046), the D-019 note, the review packet (WP7) | After v0.2 | **Yes, before v1.0** |

**Clock.** The 8-week rule (D-028) applies to data requests for cells that would otherwise be empty. It does not apply to courtesy notices or to questions about shipped data. Those stay open, with their status stated on the issue, until answered.

## 6. Risks, stated once

- **Sources unreachable from the workspace** (CDS, astroweb). Hash-identical mirrors are acceptable locally, and CI fetches the canonical copies.
- **A v2 test may fail.** Then it is published as such, as SPARC v1's was.
- **The outside reader is still needed** for the MW-PAL1 ruling (D-046) and the D-019 note. This is WP7, not a blocker for WP2 and WP3.
