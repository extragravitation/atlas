# Methodology review, 2026-10-29 (AI, two independent sessions)

**What was reviewed:** `docs/plans/TAXONOMY.md` (D-028 draft), `docs/plans/DATA_STANDARD_2_PROPOSAL.md` (D-029 draft), the source survey, the current data standard, the decision log and the master plan, at commit `e7ff1f5` of PR #30.

**Brief:** each reviewer received the charter and the file list, not the proposing session's reasoning or conclusions. Reviewer A was asked to act as an observational astronomer working on dynamics and lensing; reviewer B as a methodologist (philosophy of science, classification, data curation). Both were asked to be adversarial and to verify literature claims at source.

**Status:** AI reviews, not the outside review of D-011. Nothing here is ruled.

## Checked at source afterwards (2026-10-29)

| Claim | Result |
|---|---|
| X-COP forward method fits functional forms to temperature and pressure | **Confirmed.** Ettori et al. 2019 (arXiv:1805.00035) §3: "some functional forms are fitted to the deprojected gas temperature and pressure profiles", "with instead no assumptions on the form of the gravitational potential". Which forms: not confirmed (the paper refers to Ghirardini et al. 2018a). |
| KiDS g_obs assumes a singular isothermal sphere | **Confirmed** in `data/packages/aeg-d-kids1000-rar/v1/SOURCE.md` (Brouwer et al. 2021 §2.2). |
| CDS licences may be ODbL | **Partly confirmed.** https://cds.unistra.fr/legals : public datasets are "distributed under an Open Licence or ODbL"; CC BY also listed; a contributor's own licence is shown on the dataset page. Licence must be read per record. |
| D-019 relaxed the shipping rule the same day D-017 said not to, and applied it to SPARC | **Confirmed** from `docs/decisions.md`. |
| X-COP (z ≈ 0.04–0.1) and HeCS (0.1 < z < 0.3) do not overlap | Not checked. |
| Clusters are where the galaxy relation is reported to fail (Eckert et al. 2022) | Not checked. |

## Reviewer A (astronomer)

**Verdict.** The provenance machinery is better than most published compilations. The scientific design has two problems that cut against the charter. First, the rule that decides which observed-side estimates count (TAXONOMY §7 Q2) is applied unevenly; applied evenly it would remove two of the three packages in hand, and as written it thins coverage at the scales where one class of account has its known difficulty. Second, the D-028 release gate is unbounded for one maintainer and does not remove the bias it was meant to remove, because kind and method are entangled. D-029 points the right way but "the deepest level the source releases" is not yet a rule. Not covered: errors shared between the axes, censored data, binning bias, systems out of equilibrium, duplicate systems.

**Critical**
- **C1. Shape rule applied asymmetrically.** Admitted methods are not shape-free: KiDS g_obs = 4GΔΣ assumes a singular isothermal sphere; the X-COP forward method fits a temperature form and a generalized-NFW pressure profile (Ghirardini et al. 2018, arXiv:1708.02954); the Wolf estimator assumes a roughly flat dispersion profile. The NFW exclusion removes most group and cluster lensing, where the galaxy relation is reported to fail (Eckert et al. 2022, arXiv:2205.01110). Fix: a graded `model_dependence` facet (non-parametric; parametric on a thermodynamic or projected observable; parametric on total mass), all included, labelled, filterable; prefer the exact lensing deprojection of Mistele et al. 2024 (arXiv:2310.15248, Eq. 2.3) over SIS, registering its own assumption (ΔΣ ∝ 1/R beyond the last radius).
- **C2. The D-028 gate cannot be met and is the wrong gate.** About ten packages, several dependent on authors' releases. Fix: gate on frozen inclusion criteria plus a minimum set: a control where no discrepancy is expected (globular clusters or the Solar System), the lowest-g_bar individual systems (Local Volume Database dwarfs), one galaxy kind that is not a rotating disc, both channels. Everything else a documented gap. Freeze inclusion criteria, not the navigation list.

**Major**
- **M1. Acceleration as the main axis is not neutral.** The g_obs–g_bar plane is the radial-acceleration-relation framing, historically from MOND; dark-matter-side analyses use enclosed mass against radius, surface density or r/R500. Fix: say so on Methods; give radius, baryonic surface density, enclosed baryonic mass and normalised radius equal standing; run the coverage report on each.
- **M2. Errors shared between axes not modelled** (distance: g_obs ∝ D⁻¹, stellar g_bar independent of D; clusters g_obs ∝ D⁻¹, g_gas ∝ D^½; KiDS stellar mass sets both the bin and the isolation cut). Fix: ±1σ shifts on both axes per named assumption from the registry formulas, drawn as error vectors or ellipses.
- **M3. Stacked bins open to Eddington-type bias;** KiDS-bright isolation unreliable below g_bar ≈ 10⁻¹³ m s⁻². Fix: flag those bins; record the binning variable's scatter; distinct mark style for stacked bins.
- **M4. No way to store limits** (LVDB dispersion upper limits; unresolved binaries bias the other way). Fix: `limit` column (none/upper/lower) on g_obs and observables, drawn as arrows; `binaries_unresolved` flag from source statements.
- **M5. Equilibrium acts as hidden selection** (open clusters dropped as super-virial; Lelli et al. 2017 excluded Sagittarius and Boötes III; DF2/DF4 and tidal dwarfs borderline). Fix: a public register of excluded systems with reasons; a ruling on a uniform environment measure (Newtonian acceleration from detected neighbouring baryons).
- **M6. "Deepest level" not workable as written** (SPARC V_obs is a tilted-ring reduction; X-COP T and n_e are deprojected; ΔΣ depends on the cosmology in Σ_crit, KiDS WMAP9 H0 = 70, unregistered; wide binaries give a velocity distribution with no per-system g_obs; level can differ within a source). Fix: a fixed ladder of observable levels per tracer; observables optional (standard 1.4), required only where released machine-readable; do not re-issue v1 before release; register cosmology; wide binaries as a case study.
- **M7. Duplicate systems not handled** (LITTLE THINGS and THINGS overlap SPARC; Lelli et al. 2017 reuses SPARC; re-reductions of the same HI cube). Fix: `independent_data` on crossids; frozen precedence rule for the default map; only independent pairs in cross-checks.
- **M8. Cluster cross-checks overstated** (X-COP z = 0.04–0.1; HeCS 0.1–0.3). Fix: check overlaps at source; use CoMaLit LC² to find lensing for X-COP clusters.

**Minor:** m1 rotation/dispersion support and relaxed/merging are continua: keep continuous indicators. m2 Lelli et al. 2017 compiled 240 galaxies of several types and Eckert et al. 2022 extended to X-COP: the methods paper must state what the Atlas adds; adopt PDG-style lists of data not used and a visible marker of tension between sources, without averaging. m3 uniform-H0 option. m4 Solar System as a limit, not a point.

**Keep:** provenance chain and frozen tests; separate channels; baryon inventory with `known_unmeasured` and `not_addressed`; required selection record; principle 7; D-026; D-023; no digitising.

## Reviewer B (methodologist)

**Verdict.** Unusually careful, and the decision log is candid enough to show where it fails. The weak point is "neutral". The Atlas cannot be theory-neutral and does not need to be: its baseline is an observed-minus-computed residual against a stated reference. The proposals move theory-ladenness rather than remove it, which is acceptable if every move is declared and fixed before the data are seen. Gaps: pre-registration is internal and owner-controlled; choice among datasets and declaring gaps are ungoverned; the log shows a rule relaxed after a failure (D-017 → D-019); AI readings are not independently checked and most rulings accept recommendations.

**Critical**
1. **Neutrality claim not true as stated** (g_bar assumes Newtonian gravity; lensing g_obs assumes GR; kinematics assume equilibrium; SEP, *Theory and Observation*). Fix: restate as **cause-agnostic and reference-explicit**; Methods and paper say so; D-029 required.
2. **The freeze guards the wrong exposure.** Everyone already knows the literature's results per kind; A7 and DF2/DF4 are "selected for testing power" relative to particular accounts. Fix: state that selection is made with the literature known; mark kinds included as tests and the debate that made them so; a symmetric check for tests cutting the other way.
3. **"Gap" is a back door** ("method not yet ruled" is in the owner's control; choice among datasets in a cell is unconstrained). Fix, frozen with the taxonomy: (a) eligibility per cell in advance; (b) a fixed search protocol with a PRISMA-style log; (c) include every eligible dataset by default, a pre-written ranking where a choice is unavoidable; (d) gap criteria in advance, "method not ruled" never valid, method rulings with deadlines; (e) a fixed data-freeze date; (f) eligibility decided on metadata only, no g_obs–g_bar plot before; (g) a public deviations register.
4. **The log shows the failure mode** (D-017's reason "avoid relaxing a rule immediately after seeing a failure"; D-019 relaxed it the same day and applied it to SPARC). Fix: rule changes after a result apply prospectively unless an outside reader agrees in writing; every decision records the data seen at the time of ruling.

**Major**
5. **Pre-registration rewritable by the person it constrains.** Fix: deposit frozen protocols on Zenodo or OSF for an outside timestamp; consider Registered Reports; bring outside review before freezing D-028 (D-011 timing), more urgent given the disclosed competing interest.
6. **AI readings with no independent check;** D-001 to D-027 ruled in one day, mostly accepted recommendations. Fix: a second, blind reading of every number used (separate session or a person) with quote and page anchor, disagreements logged; each decision records options, recommendation and the owner's reason in his words; for a sample of decisions the owner rules before seeing the recommendation.
7. **"No assumed mass shape" uneven and leaky** (GR lensing, Jeans, Wolf admitted; X-COP fits functional forms to pressure, Ettori et al. arXiv:1805.00035; Ghirardini et al. arXiv:1805.00042). Fix: a `model_dependence` facet; exclude only scaling-relation masses (circular).
8. **Observable `level` too coarse** (V(r) is already a model output). Fix: record the processing chain; map it to the IVOA Provenance Data Model.
9. **Licences:** CDS datasets may be ODbL (share-alike for derived databases); a source without a licence is not open. Fix: licence per record; ODbL-derived tables released under ODbL.
10. **Kind defined by the tracer** (rotation- versus dispersion-supported). Fix: v/σ continuous; photometric kinds only, or state the definition.

**Minor:** 11 a "frozen" standard changed four times in a day; 12 a DOI per dataset version under a concept DOI, DataCite `IsDerivedFrom`; 13 VOTable export, consider VizieR deposit; 14 two formula evaluators are a maintenance cost; 15 coverage counts unique systems.

**Keep:** D-029's observable layer and registered inference steps; principle 7; the baryon inventory; cross-checks first; failed results published as failed; D-023; D-026; separate channels.
