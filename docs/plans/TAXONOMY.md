# Atlas taxonomy, coverage and selection protocol (D-028)

**Status: ruled 2026-10-29 (D-028, with D-029 to D-031).** The selection protocol (§6) is a draft: its per-cell eligibility criteria are written next, the outside reader is asked to review it, and it is then frozen by hash in `data/taxonomy.json` and deposited on Zenodo before any new data are converted. After that the list and the protocol change only by a logged decision, recorded in the deviations register.

## 1. Purpose

A field guide is organised by a taxonomy: what kinds of thing exist, how each is recognised, and where each has been seen. For the Atlas the taxonomy does three jobs.

1. **Coverage.** It lists every kind of system in which g_obs and g_bar can be compared, with every way of measuring g_obs. The first public release waits until each cell is either packaged or recorded as a documented gap (D-028).
2. **Navigation.** Readers move through the Atlas by kind of system and by method, at any scale. Kinds are filters and entry points; they never organise the findings (principle 7).
3. **Fair selection.** The list and the rules for choosing data are fixed, and timestamped outside the repository, before any new data are converted. The list is drawn up with the literature's results already known (§2 principle 10); the protocol (§6) is what keeps the choice of data within each kind from following what the data show.

## 2. Principles

1. **Classes describe what a system is and how it is observed, never how large its discrepancy is.** Test: a class must be assignable without knowing g_obs. A class such as "systems with little extra pull" fails the test and is not a class.
2. **Facets, not one tree.** A system has a kind (§3), and each measurement has a tracer and a channel (§4), a baryon inventory and a form. They are recorded separately and combined only when displayed.
3. **Assignment is from the source, through a published mapping.** Each package keeps `class_in_source` exactly as the source writes it. The Atlas kind is assigned by a mapping table in the repository (`class_in_source` and stated criteria → kind), never by hand on the page. A system the mapping cannot place keeps its source label and is listed as unassigned. *This amends the rule "class labels are the source's, not the Atlas's verdict" (master plan §2): the Atlas adds a kind, assigned by a rule; it never replaces the source's label.*
4. **Continuous properties stay continuous.** Size, mass, luminosity, surface brightness, gas fraction, rotational support (v/σ), dynamical state and distance to the nearest massive neighbour are axes, never classes. Kinds are defined by morphology and composition, never by the tracer used to measure g_obs. Kinds are coarse and observational; everything finer is a continuous property.
5. **Gaps are entries.** A kind or method with no obtainable public data appears on the site as an empty cell, with the reason and what would fill it.
6. **Closed for the first public release.** The list is frozen once ruled. Additions after the release come with a version.
7. **Kinds never organise the results.** Findings are shown on continuous axes (the map, the scale strip, profiles against radius or acceleration), with kind as a colour, filter or facet. No page states a result per kind ("clusters show…"). A category boundary drawn across a continuous trend would suggest the category explains it.
8. **Kind and method are entangled, so cross-checks come first.** Most kinds are measured mainly by one method (dwarfs by random motions, discs by rotation, clusters by hot gas and lensing). A difference between kinds can therefore be a difference between methods. Cells where two methods meet on the same systems, or two kinds meet at the same acceleration, are the ones that can separate the two, and they get priority (§5a).
9. **Every kind states why it is included.** Some kinds are common; some are included because their geometry or composition tests the baseline in a different way. The reason is recorded so the selection is visible.
10. **The list is drawn up knowing the literature.** Everyone involved already knows roughly what each kind shows. Kinds included because they were studied as tests (A7, and the contested single objects) name the published debate that made them tests, and for each the list records whether an equally studied test cutting the other way exists and is included.

## 3. Kinds of system (facet A)

Draft list, from smallest to largest. Scope note: the charter says "from star clusters to galaxy clusters". Wide binaries and the Solar System lie below that range; including them needs JvH's ruling (question 1 in §7).

| # | Kind | Includes | Why included | Notes |
|---|---|---|---|---|
| A0 | Planetary system (reference) | the Solar System | Newtonian gravity on known masses, tested to high precision: the high-acceleration reference end | Shown as a limit on anomalous acceleration, not a point (D-028) |
| A1 | Wide binary stars | pairs separated by about 10³–10⁵ AU | The smallest bound systems reaching low accelerations: G M☉ / (10⁴ AU)² ≈ 6 × 10⁻¹¹ m s⁻², comparable to the outer parts of galaxies; measured without galaxy modelling | Case study of each team's published results; no per-system g_obs (D-028) |
| A2 | Open clusters | young and intermediate-age clusters in the disc | Small stellar systems of known age and counted stellar mass, without gas | |
| A3 | Globular clusters | Milky Way and nearby-galaxy globular clusters | Old stellar systems without gas; accelerations from high in the core to low in the outskirts | D-024 |
| A4 | Late-type and irregular galaxies | spirals, irregulars, low-surface-brightness discs; ultra-diffuse galaxies placed by morphology | The best-measured kind: profiles over wide ranges of radius and acceleration | SPARC in hand |
| A5 | Dwarf spheroidal and ultra-faint galaxies | smooth, gas-poor dwarfs, by morphology | Individual systems at the lowest baryonic accelerations measured in single objects | D-024; method D-025 |
| A6 | Early-type galaxies | ellipticals and lenticulars | The other main galaxy type; measured by tracers other than rotation, and by strong lensing | |
| A7 | Galaxies in unusual configurations | tidal dwarf galaxies, polar-ring galaxies | Selected for testing power, not frequency: the same ingredients in a different formation history or geometry (tidal debris; two orthogonal planes) | Small samples; studied as tests in published debates, to be named per principle 10 |
| A8 | Galaxy groups | groups of a few to tens of galaxies | Between single galaxies and clusters in mass and size | D-024 |
| A9 | Galaxy clusters | dynamical state kept as the source's continuous indicators | The largest bound systems; hot gas dominates the detected matter; several independent methods on the same systems | X-COP in hand |
| A10 | Colliding clusters with separated components | gas visibly offset from the galaxies in X-ray and optical images | Gas, galaxies and lensing mass separated on the sky; maps rather than profiles | Maps, not profiles |
| — | Beyond clusters | superclusters, cosmological scales | Not included | Outside the charter; boundary noted on the site |

"Isolated galaxies" (the KiDS lens sample) is a selection of A4 and A6 galaxies, recorded as an environment selection on a population average, not as a kind.

## 4. Other facets

- **Tracer of g_obs** (extends `method_class`): rotation; random motions (velocity dispersion); discrete orbiting tracers (satellites, globular clusters, planetary nebulae, binary orbits); hot-gas pressure balance; weak lensing; strong lensing. **Channel** stays dynamics or lensing, never merged by default.
- **Baryon inventory:** stars, cold gas, hot gas, intracluster light, each measured, modelled or absent (data standard §3).
- **Form:** profile (several radii), single aperture (one radius, e.g. at the half-light radius), population average (stacked), map.
- **Environment:** as continuous properties where the source gives them (e.g. projected distance to the nearest massive neighbour); labels only as the source's selection (e.g. "isolated, as selected by Brouwer et al. 2021").

## 5. Coverage matrix

Status as read at source on 2026-10-28 (three source surveys; URLs and details in `docs/sources/survey-2026-10-28.md`). Nothing below is ruled, fetched or hashed yet except the three packages in hand.

**Key:** ● in hand · ○ public data found, obtainable · ◐ needs a method ruling, an author's release or an answer · ✕ searched, no public data found · — not applicable

| Kind | Rotation | Random motions | Orbiting tracers | Hot-gas pressure | Weak lensing | Strong lensing |
|---|---|---|---|---|---|---|
| A0 Solar System | — | — | ○ JPL DE440 ephemerides (reference) | — | — | — |
| A1 Wide binaries | — | — | ◐ El-Badry et al. 2021 base catalogue (Zenodo, CC BY 4.0); Chae samples; contested | — | — | — |
| A2 Open clusters | — | ◐ Pang et al. 2021, 13 clusters; authors report most may be expanding | — | — | — | — |
| A3 Globular clusters | — | ○ Baumgardt database: 156 measured dispersion profiles | — | — | — | — |
| A4 Late-type and irregular galaxies | ● SPARC 175; ○ LITTLE THINGS 26 (full mass models); ○ PROBES 3 163 (no gas) | — | ✕ satellite kinematics as profiles | — | ● KiDS-1000 (isolated, stacked; with A6) | — |
| A5 Dwarf spheroidal and ultra-faint | — | ○ Local Volume Database (Pace, CC0): one dispersion per galaxy; ○ stellar velocities for profiles (Walker 2009, Tollerud 2012) | — | — | — | — |
| A6 Early-type galaxies | ◐ HI rings, 16 (Lelli et al. 2017 compilation) | ○ ATLAS3D 260, inside the half-light radius (model-derived) | ○ SLUGGS globular-cluster velocities, 27; ✕ planetary nebulae (not released) | ○ 9 X-ray profiles (Lelli et al. 2017 compilation) | ● KiDS-1000 (with A4) | ○ SLACS ~98, mass inside the Einstein radius |
| A7 Unusual configurations | ◐ tidal dwarfs 6, polar rings (data scattered) | ◐ NGC 1052-DF2, -DF4 (distance contested) | | — | — | — |
| A8 Groups | — | — | ✕ | ◐ X-GAP 49 (release announced, not found); Sun 2009, Lovisari 2015 (parametric, gas only) | ◐ HSC-XXL 136 (one aperture, model-fitted) | — |
| A9 Galaxy clusters | — | — | ○ HeCS caustic profiles 58 | ● X-COP 12 | ○ CLASH 20 (with strong lensing) | ○ CLASH |
| A10 Colliding clusters | — | — | — | ○ Chandra archive (maps) | ○ Frontier Fields mass maps, 6 | ○ Frontier Fields; El Gordo |

### 5a. Cross-checks (priority cells)

Cells that can separate a difference between kinds from a difference between methods. Overlaps between samples are not yet checked at source.

- **Same systems, two or more methods.** Overlaps must be checked at source before any cross-check is promised; the X-COP (z ≈ 0.04–0.1) and HeCS (0.1–0.3) redshift ranges may not overlap at all (reviewer note, unchecked). CoMaLit's meta-catalogue of lensing masses is the first place to look for lensing of X-COP clusters.
  - Relaxed clusters: X-ray hydrostatic (X-COP), lensing (CLASH) and member-galaxy dynamics (HeCS). Which clusters appear in more than one is unverified.
  - Early-type galaxies: X-ray, strong lensing (SLACS) and globular-cluster orbits (SLUGGS) on the same galaxies, where they overlap (unverified).
- **Same kind, two methods, different systems.** Rotation-supported galaxies: rotation curves (SPARC) and stacked weak lensing (KiDS) at overlapping g_bar.
- **Same acceleration, different kinds.** Low g_bar: outer discs (A4), dispersion-supported dwarfs (A5), outskirts of globular clusters (A3), wide binaries (A1) and stacked lensing.
- **Same kind, two baryon routes.** Clusters with measured and modelled stars (X-COP, D-023).

### 5b. Coverage in continuous space

Complete in kinds is not complete in parameter space. Each release reports how the measurements fill the continuous axes: g_bar, radius, baryonic surface density, and the number of systems and measurements per bin, by method. Empty or thinly covered regions are listed alongside the gaps in §5.

**What the survey shows.**
- Every kind from A0 to A10 has at least one candidate except open clusters, where the one dispersion study warns against assuming equilibrium.
- Lensing coverage is thin below clusters: one stacked galaxy dataset (KiDS) and one strong-lensing sample (SLACS). No HSC or DES galaxy-lensing release of g_obs against g_bar was found.
- Groups are the weakest kind with profiles: X-GAP has announced a release that could not be found.
- Many observed sides are model-derived (Jeans models, caustics, parametric mass fits). This is the main method question (§7, question 2).
- About ten new packages would be needed if every ruling went the inclusive way, against three so far.

## 6. Selection protocol (draft; frozen before any new conversion)

1. **Eligibility, per cell, written in advance.** A dataset is eligible for a cell if:
   - it measures the cell's tracer for systems of the cell's kind;
   - g_obs and g_bar, or the observables they are computed from, are public in machine-readable form, or will be supplied by the authors on request;
   - the observed side does not come from a scaling relation (circular; D-029);
   - its licence permits redistribution, or it can be fetched by address and verified by hash (D-004);
   - it adds data independent of datasets already included, or a re-reduction is recorded as such (D-029).
   Per-cell additions (minimum radial coverage, minimum number of systems, required baryon components) are written in a table here before the freeze.
2. **Search protocol.** For each cell: ADS queries (strings recorded), VizieR, Zenodo and GitHub searches, and the literature cited by eligible datasets, all on a recorded date. A log lists every record found, screened and excluded, with the reason.
3. **Inclusion.** Every eligible dataset is included by default. Where a choice is unavoidable (e.g. two reductions of the same data), the ranking is: deepest observables released; independence; number of systems; licence. Judgement is not a criterion.
4. **Blind to results.** Eligibility is decided from metadata, papers' method sections and data documentation. No g_obs–g_bar plot of a candidate is made before its eligibility is decided.
5. **Gaps.** A cell is a gap only if the logged search found no eligible public data, or a data request has gone unanswered for 8 weeks. "Method not yet ruled" is never a reason; each method ruling a cell needs has a deadline before the data-freeze date.
6. **Data-freeze date.** Set in the protocol before deposit. Datasets found or released later go to the next version.
7. **Deviations register.** Any departure from the protocol is logged publicly with its reason and the data seen at the time (D-031).
8. **Timestamp and review.** The protocol is reviewed by the outside reader (if one replies within 4 weeks), frozen by hash, and deposited on Zenodo before any new conversion.

## 7. Release gate (D-028)

v1.0, the first public release, is published when every cell is a package or a gap under §6.5, and these are live:
- a control where Newtonian gravity on detected matter is expected to suffice: the Solar System (as a limit) and globular clusters;
- the lowest-g_bar individual systems: dwarf spheroidals and ultra-faint dwarfs;
- at least one galaxy kind other than rotating discs;
- both channels;
- at least two lenses (D-030);
- the cross-check status (§5a) and the coverage report on continuous axes (§5b).

## 8. Rulings (2026-10-29)

D-028 to D-031 rule the questions raised in the draft:
1. Scope: A0 included as a limit; A1 as a case study; A2 as a kind (may be a gap).
2. Model-derived observed sides: all included with a `model_dependence` label; only scaling-relation masses excluded (D-029). The draft's proposal to exclude fits that assume a total-mass shape was withdrawn: it could not be applied evenly.
3. Projection: like with like; baryons projected where their data reach far enough.
4. Stellar mass-to-light for star clusters and dwarfs: published default and range, adjustable per kind.
5. Contested single objects: case studies with each side's values as named alternatives.
6. First public release: v1.0; previews unnumbered.
7. Requests to send (JvH): X-GAP release and licence; HSC-XXL profiles; Bullet cluster maps.
