# Atlas taxonomy and coverage (draft for ruling, D-028)

**Status: draft, 2026-10-28. Nothing here is ruled.** Proposed with D-028. Once ruled, the list of kinds in §3 is frozen by hash in `data/taxonomy.json` (as tests are) and changes only by a logged decision.

## 1. Purpose

A field guide is organised by a taxonomy: what kinds of thing exist, how each is recognised, and where each has been seen. For the Atlas the taxonomy does three jobs.

1. **Coverage.** It lists every kind of system in which g_obs and g_bar can be compared, with every way of measuring g_obs. The first public release waits until each cell is either packaged or recorded as a documented gap (D-028).
2. **Navigation.** Readers move through the Atlas by kind of system and by method, at any scale.
3. **Neutral selection.** The list is drawn from the literature and fixed before any new data are converted, so the choice of what the Atlas covers cannot follow from what the data show.

## 2. Principles

1. **Classes describe what a system is and how it is observed, never how large its discrepancy is.** Test: a class must be assignable without knowing g_obs. A class such as "systems with little extra pull" fails the test and is not a class.
2. **Facets, not one tree.** A system has a kind (§3), and each measurement has a tracer and a channel (§4), a baryon inventory and a form. They are recorded separately and combined only when displayed.
3. **Assignment is from the source, through a published mapping.** Each package keeps `class_in_source` exactly as the source writes it. The Atlas kind is assigned by a mapping table in the repository (`class_in_source` and stated criteria → kind), never by hand on the page. A system the mapping cannot place keeps its source label and is listed as unassigned. *This amends the rule "class labels are the source's, not the Atlas's verdict" (master plan §2): the Atlas adds a kind, assigned by a rule; it never replaces the source's label.*
4. **Continuous properties stay continuous.** Size, mass, luminosity, surface brightness, gas fraction and distance to the nearest massive neighbour are axes, never classes. Kinds are coarse and observational; everything finer is a continuous property.
5. **Gaps are entries.** A kind or method with no obtainable public data appears on the site as an empty cell, with the reason and what would fill it.
6. **Closed for the first public release.** The list is frozen once ruled. Additions after the release come with a version.

## 3. Kinds of system (facet A)

Draft list, from smallest to largest. Scope note: the charter says "from star clusters to galaxy clusters". Wide binaries and the Solar System lie below that range; including them needs JvH's ruling (question 1 in §7).

| # | Kind | Includes | Notes |
|---|---|---|---|
| A0 | Planetary system (reference) | the Solar System | Reference points (D-013); g_obs = g_bar is expected at the precision of the ephemerides |
| A1 | Wide binary stars | pairs separated by about 10³–10⁵ AU | Scope extension |
| A2 | Open clusters | young and intermediate-age clusters in the disc | |
| A3 | Globular clusters | Milky Way and nearby-galaxy globular clusters | D-024 |
| A4 | Rotation-supported galaxies | spirals, dwarf irregulars, low-surface-brightness and rotating ultra-diffuse galaxies | SPARC in hand |
| A5 | Dispersion-supported dwarf galaxies | dwarf spheroidals, ultra-faint dwarfs, non-rotating ultra-diffuse galaxies | D-024; method D-025 |
| A6 | Early-type galaxies | ellipticals and lenticulars | |
| A7 | Galaxies in unusual configurations | tidal dwarf galaxies, polar-ring galaxies | Small samples, but they probe the baseline in different geometries |
| A8 | Galaxy groups | groups of a few to tens of galaxies | D-024 |
| A9 | Galaxy clusters, relaxed | | X-COP in hand |
| A10 | Galaxy clusters, merging | colliding clusters with separate gas and galaxy distributions | Maps, not profiles |
| — | Beyond clusters | superclusters, cosmological scales | Outside the charter; boundary noted on the site |

"Isolated galaxies" (the KiDS lens sample) is a selection of A4 and A6 galaxies, recorded as an environment selection on a population average, not as a kind.

## 4. Other facets

- **Tracer of g_obs** (extends `method_class`): rotation; random motions (velocity dispersion); discrete orbiting tracers (satellites, globular clusters, planetary nebulae, binary orbits); hot-gas pressure balance; weak lensing; strong lensing. **Channel** stays dynamics or lensing, never merged by default.
- **Baryon inventory:** stars, cold gas, hot gas, intracluster light, each measured, modelled or absent (data standard §3).
- **Form:** profile (several radii), single aperture (one radius, e.g. at the half-light radius), population average (stacked), map.
- **Environment:** as continuous properties where the source gives them (e.g. projected distance to the nearest massive neighbour); labels only as the source's selection (e.g. "isolated, as selected by Brouwer et al. 2021").

## 5. Coverage matrix

*Filled from the source survey below; status as read at source on 2026-10-28.*

## 6. Release rule (proposed D-028)

## 7. Questions for JvH
