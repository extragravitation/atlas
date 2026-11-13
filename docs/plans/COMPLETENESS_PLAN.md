# Atlas of Extra Gravitation: completeness plan

2026-11-12, clock 17:58 (TZ=America/Edmonton). **FILED (JvH, 17:57). Each phase is a proposal for JvH's ruling.**
- **Requested by JvH, 17:57:** "make a detailed phased plan and file under a new folder that makes sense. Then we will do the phase 0 to start."
- **Inputs (filed alongside):**
  - `AU-02_ATLAS_COMPLETENESS_REVIEW.md`: site and repository review at v0.2;
  - `CK-01_TAXONOMY_COMPLETENESS_CHECK.md`: comparison with four field reviews.
- **Repository state read:** `extragravitation/atlas` main at 3ab9151 (6 Nov 2026), tag v0.2.

## Why this plan exists

**The main neutrality risk is incompleteness.** A reader who looks for a well-known test case (the Bullet Cluster, Crater II, M33, DF2) and does not find it, with no stated reason, will read the gap as selection.

**What "complete" means here:**
- every kind of system and every way of measuring the pull that the field uses is either **in the Atlas, scheduled with a rule, or a documented gap with a reason**;
- every well-known test system has a stated status;
- what lies outside the Atlas's scope is listed for **both** sides of the debate.

Data will always lag behind. The *plan* can be complete well before the data are.

## Principles (carried from the Atlas's own rules)

1. **Inclusion by symmetric rule, not by quota.** A system is a candidate if it has been used as a test case in the published debate, by any side. The same data rules then apply to every candidate.
2. **Kinds are defined by what a system is**, never by its measured discrepancy (TAXONOMY §2).
3. **Rules are written before data are examined** (SELECTION_PROTOCOL §1). Changes to frozen documents go through a new version plus the deviations register (D-031, D-108).
4. **Disputes are shown, not settled.** Contested inputs (e.g. DF2's distance, AGC 114905's inclination) are carried as published alternatives.
5. **Readings stay out of the record.** Interpretations belong to the accounts layer, in one template per account (Tests page).
6. **JvH rules.** Claude proposes; each ruling is logged with who proposed it and what was seen (D-110 rule 3).

## Release framing (D-110, deviation #23)

| Release | Contents |
|:--|:--|
| **v1.0** | the datasets in hand + the data freeze (24 Dec 2026) + the standard 3.0.0 re-issue + the formal outside review + the methods paper |
| **v1.x** | new cells and systems |

**This plan's Phase 1 (defining "complete") should be live before v1.0**, so the formal review judges a complete plan, not only the data in hand.

---

## Phase 0: Correct what the site says now (hours; wording only)

**Goal:** remove text that contradicts the decision record. Two errors were found today; both undercut credibility.

| # | Where | Now says | Change to |
|:--|:--|:--|:--|
| 0.1 | `site/src/pages/coverage.astro` l.63, lede (technical and plain) | v1.0 covers every kind; each cell packaged or a gap (D-028) | v1.0 is the data in hand plus re-issue and review (D-110). The rest arrives in v1.x. This page shows the full plan and what is in each cell now. |
| 0.2 | `coverage.astro` l.93, heading "Selection protocol (draft)" | "draft" | **"Selection protocol (frozen 2026-10-29)"**, plus one status line: frozen at commit 817bc5a, deposited on Zenodo (10.5281/zenodo.23780203), data freeze 2026-12-24; the "draft" wording inside is part of the frozen text. |
| 0.3 | `coverage.astro` l.95–96, "Release gate" | renders the TAXONOMY §7 gate unqualified | Keep the frozen text. **Add a note above it:** narrowed by D-110 (deviation #23); link both. |
| 0.4 | `site/src/pages/methods.astro` l.222 and l.230, "Limitations and gaps" | the pre-D-110 v1.0 sentence | the same correction as 0.1 |
| 0.5 | `docs/plans/MASTER_PLAN_v2.md` §8 | the pre-D-110 v1.0 row | a dated note at the top of §8 pointing to D-110. The rest of the plan text is unchanged. |
| 0.6 | `docs/plans/CONTINUATION.md` | state at 5 Nov | current state: v0.2 tagged, invites sent 6 Nov, this plan |
| 0.7 | `docs/plans/` | – | add this plan, AU-02 and CK-01 |

**Process:**
- One pull request. The wording changes are recorded in the PR and the changelog, not as decisions (D-110 rule 3).
- **No `Claude-Session:` line** in commits or PRs (standing rule, CONTINUATION).
- **Check:** the site builds; the Coverage and Methods pages are read in both views (technical and plain).
- **Done when:** merged to main and live.

---

## Phase 1: Define "complete" (rulings; no new data; 1–2 weeks)

**Goal:** the full list of kinds, measurement routes and named test systems, each with a status and a reason, plus a stated scope boundary. **All of it is written before any new data are examined.**

### 1.1 Full-text read of the field's checklists

- **Sources:**
  - Famaey & McGaugh 2012 (all sections);
  - Banik & Zhao 2022 (§6–12 not yet read);
  - Bullock & Boylan-Kolchin 2017 (body);
  - Salucci 2019 (body);
  - **one more dark-matter-side observational review** to balance (candidates: Sales, Wetzel & Fattahi 2022; Wechsler & Tinker 2018 for the galaxy–halo connection). The final choice is a ruling.
- **Output:** a single list of (system or type, which review, how it is used as a test). Kept as `docs/sources/checklist-reviews.md`.
- **Rule:** the list records what each review *uses as a test*, not what it concludes.

### 1.2 Taxonomy version 3

**Candidate additions from CK-01, to be confirmed by 1.1:**

| Kind of addition | Items |
|:--|:--|
| New tracers | vertical dynamics of discs; tidal streams; shell positions; direct acceleration measurements (Gaia barycentre, pulsar timing); tidal radii |
| New kinds or sub-kinds | the Milky Way (multi-tracer, its own row); binary galaxies and satellite systems; the Local Group (timing argument, local Hubble flow) |
| Forms | "map" (needed for A10), formally defined in the data standard |

**Also:**
- Eligibility rows for each new cell, in the same table as SELECTION_PROTOCOL §2.
- **Process:** TAXONOMY_v3.md + a deviations register entry. Frozen by hash on main and deposited on Zenodo before any search of the new cells. The Coverage page then renders v3 automatically.

### 1.3 Test-system checklist

**One row per named system** used as a test in the reviews (1.1). Columns:
- system;
- kind;
- who uses it as a test, and for what;
- Atlas status: **in** / **candidate (cell, search status)** / **excluded (rule, with link)** / **gap (reason)**;
- disputed inputs.

**Starting list (CK-01, to be completed by 1.1):**
- M33, LMC, M31, Milky Way;
- DF2, DF4, Dragonfly 44, AGC 114905;
- Crater II, Carina, Antlia II;
- Pal 5, Pal 14, NGC 2419;
- NGC 5291;
- NGC 720, NGC 1521;
- Bullet, Abell 520, El Gordo, MACS J0025;
- Coma, Fornax cluster.

**Rendering:** a new Coverage section, "Well-known test systems", built from the ruled file like the rest of the page.

### 1.4 Scope statement

Evidence the Atlas does **not** carry, because it is not a comparison of observed and baryonic acceleration. Listed for **both** sides, each item with its review source, as a ruled document rendered on Coverage.

| Group | Items |
|:--|:--|
| Structural and dynamical | bars (fraction, strength, pattern speed); disc thinness and stability; warps; spiral-arm counts; dynamical friction (e.g. Fornax's globular clusters); shell generations; formation of tidal dwarfs; satellite planes |
| Population and small-scale | satellite counts; too-big-to-fail; rotation-curve diversity as a population statistic; starless halos; indirect detection |
| Cosmological | CMB, BBN, BAO, supernovae, large-scale structure, cluster abundance, voids and bulk flows, the Hubble tension |
| Partly inside | colliding-cluster offsets (A10 maps); cusp vs core (inner rotation-curve shape is in the profiles); high redshift (documented gap) |

### 1.5 Exclusion-effect audit

- For every exclusion rule in force (D-038 dispersion rules, D-047, D-066 epoch cut, D-069/D-070 cluster stars, and others): list which **named test systems** it removes, and **whose case those systems are usually cited for**.
- **Where a rule's effect is one-sided:**
  - re-examine the rule (any change via the deviations register); or
  - keep it and state the effect prominently on Coverage.
- **First case:** Crater II, Carina and Antlia II under D-038.

### 1.6 Accounts rule

- The rule for which explanations get an account page, written before any page (the Tests page promises this).
- **Proposal to rule on:** every account with a published, peer-reviewed prediction for at least two kinds in the taxonomy.

**Phase 1 is done when** 1.2–1.6 are ruled, frozen where they are rules, deposited, and rendered on Coverage.

---

## Phase 2: Build what is already searched and ruled (v1.x, 2–4 weeks)

**In the protocol's order of work, cells whose search and method rulings are complete:**

| Item | Basis | Output |
|:--|:--|:--|
| **A9 route** | D-067, D-071 to D-074 | X-COP case studies (A85, A2142, ZwCl 1215); LoCuSS spec (frozen first), then the one-radius layer; other case studies (A1689, A1835, A2390, MS 1455+22, Coma); the funnel page |
| **A0 limit** | search-log-A0 (5 E, 23 E-conv) | the Solar System bound, shown as a limit (D-028) |
| **A3 additions** | search-log-A3 (49 E) | eligible records not yet packaged |
| **A5 additions** | search-log-A5 (46 E) | likewise, after the Phase 1.5 audit of D-038 |

**Each package** follows the standing process: data standard, blind reading where values are read, frozen reproduction test, known issues.

---

## Phase 3: Search and build the untouched cells (v1.x, ongoing)

**Protocol order, then the v3 additions:**
1. **A4 second disc set** (LITTLE THINGS, PROBES, WALLABY); **A10 maps** (El Gordo, Frontier Fields; Bullet maps by request); **A1 wide-binary case study**.
2. **A2** open clusters, **A7** unusual configurations (DF2/DF4, tidal dwarfs, polar rings, shells), **A8** groups (X-GAP by request; leads in the A9 search log).
3. **A6** stellar dynamics, globular clusters and planetary nebulae, X-ray, HI rings (SLUGGS, ATLAS3D, the Lelli+17 compilation).
4. **v3 cells:** the Milky Way, streams, vertical dynamics, satellites and pairs, the Local Group, direct accelerations.

**Each cell gets:** a logged search, a screening, method rulings (with deadlines), a package or a documented gap. Data requests go out only where no public route exists (protocol §6); the 8-week clock starts on sending.

---

## Phase 4: Accounts and patterns (after Phase 1.6)

- **Account pages** in the single template, each reviewed by its proponents before publication.
- **Patterns** under the frozen criteria (`docs/patterns/P2_P3_CRITERIA.md`).

---

## Outreach (kept separate from this plan)

- **Feedback** (D-110 rule 2): two invitations sent 6 Nov. Follow up around 20 Nov. Further invitations go to people chosen for the critique needed; a dark-matter-side reader tests neutrality.
- **Data:** only through the protocol.
- **Endorsement:** a separate question, not a factor in choosing recipients.

## Where the work happens

**A dedicated Claude session for the Atlas**, linked to the AEG Website project, with the repository attached for push. Reasons:
- **clean context and the Atlas's own rules** (CONTINUATION, decisions log);
- **provenance:** the Atlas is declared independent of Partition Theory, so its work should not run in a PT session.

This plan and its two inputs are that session's starting brief.
