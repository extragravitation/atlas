# Atlas taxonomy and coverage (draft for ruling, D-028)

**Status: draft, 2026-10-28; revised 2026-10-29. Nothing here is ruled.** Proposed with D-028. Once ruled, the list of kinds in §3 is frozen by hash in `data/taxonomy.json` (as tests are) and changes only by a logged decision.

## 1. Purpose

A field guide is organised by a taxonomy: what kinds of thing exist, how each is recognised, and where each has been seen. For the Atlas the taxonomy does three jobs.

1. **Coverage.** It lists every kind of system in which g_obs and g_bar can be compared, with every way of measuring g_obs. The first public release waits until each cell is either packaged or recorded as a documented gap (D-028).
2. **Navigation.** Readers move through the Atlas by kind of system and by method, at any scale. Kinds are filters and entry points; they never organise the findings (principle 7).
3. **Neutral selection.** The list is drawn from the literature and fixed before any new data are converted, so the choice of what the Atlas covers cannot follow from what the data show.

## 2. Principles

1. **Classes describe what a system is and how it is observed, never how large its discrepancy is.** Test: a class must be assignable without knowing g_obs. A class such as "systems with little extra pull" fails the test and is not a class.
2. **Facets, not one tree.** A system has a kind (§3), and each measurement has a tracer and a channel (§4), a baryon inventory and a form. They are recorded separately and combined only when displayed.
3. **Assignment is from the source, through a published mapping.** Each package keeps `class_in_source` exactly as the source writes it. The Atlas kind is assigned by a mapping table in the repository (`class_in_source` and stated criteria → kind), never by hand on the page. A system the mapping cannot place keeps its source label and is listed as unassigned. *This amends the rule "class labels are the source's, not the Atlas's verdict" (master plan §2): the Atlas adds a kind, assigned by a rule; it never replaces the source's label.*
4. **Continuous properties stay continuous.** Size, mass, luminosity, surface brightness, gas fraction and distance to the nearest massive neighbour are axes, never classes. Kinds are coarse and observational; everything finer is a continuous property.
5. **Gaps are entries.** A kind or method with no obtainable public data appears on the site as an empty cell, with the reason and what would fill it.
6. **Closed for the first public release.** The list is frozen once ruled. Additions after the release come with a version.
7. **Kinds never organise the results.** Findings are shown on continuous axes (the map, the scale strip, profiles against radius or acceleration), with kind as a colour, filter or facet. No page states a result per kind ("clusters show…"). A category boundary drawn across a continuous trend would suggest the category explains it.
8. **Kind and method are entangled, so cross-checks come first.** Most kinds are measured mainly by one method (dwarfs by random motions, discs by rotation, clusters by hot gas and lensing). A difference between kinds can therefore be a difference between methods. Cells where two methods meet on the same systems, or two kinds meet at the same acceleration, are the ones that can separate the two, and they get priority (§5a).
9. **Every kind states why it is included.** Some kinds are common; some are included because their geometry or composition tests the baseline in a different way. The reason is recorded so the selection is visible.

## 3. Kinds of system (facet A)

Draft list, from smallest to largest. Scope note: the charter says "from star clusters to galaxy clusters". Wide binaries and the Solar System lie below that range; including them needs JvH's ruling (question 1 in §7).

| # | Kind | Includes | Why included | Notes |
|---|---|---|---|---|
| A0 | Planetary system (reference) | the Solar System | Newtonian gravity on known masses, tested to high precision: the high-acceleration reference end | Reference points (D-013); g_obs = g_bar is expected at the precision of the ephemerides |
| A1 | Wide binary stars | pairs separated by about 10³–10⁵ AU | The smallest bound systems reaching low accelerations: G M☉ / (10⁴ AU)² ≈ 6 × 10⁻¹¹ m s⁻², comparable to the outer parts of galaxies; measured without galaxy modelling | Scope extension |
| A2 | Open clusters | young and intermediate-age clusters in the disc | Small stellar systems of known age and counted stellar mass, without gas | |
| A3 | Globular clusters | Milky Way and nearby-galaxy globular clusters | Old stellar systems without gas; accelerations from high in the core to low in the outskirts | D-024 |
| A4 | Rotation-supported galaxies | spirals, dwarf irregulars, low-surface-brightness and rotating ultra-diffuse galaxies | The best-measured kind: profiles over wide ranges of radius and acceleration | SPARC in hand |
| A5 | Dispersion-supported dwarf galaxies | dwarf spheroidals, ultra-faint dwarfs, non-rotating ultra-diffuse galaxies | Individual systems at the lowest baryonic accelerations measured in single objects | D-024; method D-025 |
| A6 | Early-type galaxies | ellipticals and lenticulars | The other main galaxy type; measured by tracers other than rotation, and by strong lensing | |
| A7 | Galaxies in unusual configurations | tidal dwarf galaxies, polar-ring galaxies | Selected for testing power, not frequency: the same ingredients in a different formation history or geometry (tidal debris; two orthogonal planes) | Small samples |
| A8 | Galaxy groups | groups of a few to tens of galaxies | Between single galaxies and clusters in mass and size | D-024 |
| A9 | Galaxy clusters, relaxed | | The largest bound systems; hot gas dominates the detected matter; several independent methods on the same systems | X-COP in hand |
| A10 | Galaxy clusters, merging | colliding clusters with separate gas and galaxy distributions | Gas, galaxies and lensing mass separated on the sky; maps rather than profiles | Maps, not profiles |
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
| A4 Rotation-supported galaxies | ● SPARC 175; ○ LITTLE THINGS 26 (full mass models); ○ PROBES 3 163 (no gas) | — | ✕ satellite kinematics as profiles | — | ● KiDS-1000 (isolated, stacked; with A6) | — |
| A5 Dispersion-supported dwarfs | — | ○ Local Volume Database (Pace, CC0): one dispersion per galaxy; ○ stellar velocities for profiles (Walker 2009, Tollerud 2012) | — | — | — | — |
| A6 Early-type galaxies | ◐ HI rings, 16 (Lelli et al. 2017 compilation) | ○ ATLAS3D 260, inside the half-light radius (model-derived) | ○ SLUGGS globular-cluster velocities, 27; ✕ planetary nebulae (not released) | ○ 9 X-ray profiles (Lelli et al. 2017 compilation) | ● KiDS-1000 (with A4) | ○ SLACS ~98, mass inside the Einstein radius |
| A7 Unusual configurations | ◐ tidal dwarfs 6, polar rings (data scattered) | ◐ NGC 1052-DF2, -DF4 (distance contested) | | — | — | — |
| A8 Groups | — | — | ✕ | ◐ X-GAP 49 (release announced, not found); Sun 2009, Lovisari 2015 (parametric, gas only) | ◐ HSC-XXL 136 (one aperture, model-fitted) | — |
| A9 Clusters, relaxed | — | — | ○ HeCS caustic profiles 58 | ● X-COP 12 | ○ CLASH 20 (with strong lensing) | ○ CLASH |
| A10 Clusters, merging | — | — | — | ○ Chandra archive (maps) | ○ Frontier Fields mass maps, 6 | ○ Frontier Fields; El Gordo |

### 5a. Cross-checks (priority cells)

Cells that can separate a difference between kinds from a difference between methods. Overlaps between samples are not yet checked at source.

- **Same systems, two or more methods.**
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

## 6. Release rule (proposed D-028)

**Proposed ruling.** The first public release covers the taxonomy. It is published when every cell of the ruled coverage matrix is either (a) a shipped package or (b) a documented gap: no public data, data gated with the request on record, or a method not yet ruled, with the reason shown on the site. The release also publishes the cross-check status (§5a) and the coverage report on the continuous axes (§5b). Kinds organise coverage and navigation, never the presentation of findings. The taxonomy is frozen by hash before any new dataset is converted. Data packages keep their own versions and land one at a time. The private preview continues and is shown to the outside reader and advisers before release. Amends the charter's "launch v0.1 quickly", D-010 (release rhythm) and the master-plan roadmap; extends D-024.

**Reason.** A first public picture built on some kinds of system answers the Atlas's question before asking it. Fixing the list before converting data keeps the selection independent of the results. A closed list with documented gaps bounds the work.

**Alternatives.** Release v0.1 on the three datasets now (rejected in D-024 for bias); release only when every cell is filled (unbounded: several cells depend on others' releases).

## 7. Questions for JvH

1. **Scope.** Include A0 (already D-013), A1 wide binaries and A2 open clusters? The charter's range starts at star clusters. Recommendation: include all three as kinds; A1 and A2 may end as documented gaps if their method rulings fail.
2. **Model-derived observed side.** Some observed values come from a model: Jeans models of stellar motions, caustics, and fits with an assumed mass profile (e.g. NFW). Recommendation: accept direct measurements and estimates that assume no shape for the total mass profile (as with X-COP's forward method), each labelled by form. Exclude fits that assume a shape for the total mass, because the shape itself presumes an account (an NFW profile is a dark-matter halo shape). This would exclude most group lensing (HSC-XXL), so groups may rest on X-GAP alone.
3. **Projected and 3D.** Lensing measures mass in projection; dynamics and baryon profiles are 3D. Recommendation: compare like with like; for lensing, project the baryons rather than deproject the lensing, where the baryon data reach far enough; ruling per dataset.
4. **Stellar mass-to-light for star clusters and dwarfs.** g_bar is luminosity times an assumed ratio. Recommendation: the default and range from stellar-population literature, read at source, as a slider for each kind (as for SPARC).
5. **Contested single objects** (NGC 1052-DF2 and -DF4, AGC 114905, Abell 520, wide binaries). Recommendation: case studies that present each side's published values as named alternatives, with neither as the default.
6. **Release name.** Recommendation: v1.0 for the first public release, since it is the complete taxonomy; previews stay unnumbered.
7. **Requests to send** (JvH): X-GAP release and licence (Eckert; already on the X-COP email list), HSC-XXL profiles, Bullet cluster maps.
