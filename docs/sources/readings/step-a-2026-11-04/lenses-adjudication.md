# Strong lenses (`aeg-d-strong-lensing/v1`): adjudication of the two step A readings

**2026-11-04, Claude.** This compares `lenses-reader-A.md` (46 terms) and `lenses-reader-B.md` (62 terms).

**Sources.** Both read the same 13 papers. Their e-print hashes agree, and the four IOP tables they fetched match `sources.json`.
- **Reader B** also fetched two VizieR exports, which match `sources.json`.
- **Reader A** found VizieR unreachable and did not work around it. It checked R13's error format against the paper's Table 4 instead.

## Agreement

The two readings agree on every shared term: quotes, sizes, scales, axes, and whether v1 carries it. Reader B's list is finer. For example, it splits the cosmologies (L35), α/Fe (L59) and the SLC15 superseded values (L51). Reader A adds the SLACS centroid shift (L4) and R7's metallicity critique (L25). Nothing in one contradicts the other.

**What v1 carries:**
- the printed M_E errors, and the SLACS 2 % θ_E error, both on g_obs;
- the printed stellar-mass, luminosity and Υ errors, on g_bar;
- the IMF top and the gas term, as sliders.

**What v1 does not carry:**
- distance, H0 and peculiar velocity;
- redshift errors (only NGC 6505 prints them);
- the population-synthesis systematics: S4TM ~0.5 dex, SL2S 0.06 dex, the model family 10–12 %, age 14 %;
- the profile-step radii: SL2S CFHT 30 %, S4TM unstated;
- the stated lower-bound nature of NGC 6505's errors;
- external convergence and line-of-sight terms of a few per cent.

## Findings settled at source

**F1. The Einstein-radius error is on the wrong axis in v1.** *Both readers derived this independently; I checked it at source and confirmed the algebra.*
- **The algebra.** The mass inside the Einstein radius is M_E = π Σ_cr R_E² (R10 §4; R13 Eq. 8). Mean convergence 1 inside θ_E is the definition of the Einstein radius. So g_obs = G M_E / R_E² = π G Σ_cr = c² D_s / (4 D_l D_ls). This depends on distances only, not on θ_E.
- **The consequence.** A θ_E error moves R_E, and therefore g_bar = G M★(<R_E)/R_E² through both the radius and the aperture of M★. It leaves g_obs unchanged.
- **What v1 does instead** (`convert.py` l. 48–49): it carries the θ_E error as a g_obs error "at fixed R_E".
- **Scope.** This applies exactly to the systems whose M_E is computed from θ_E (SLACS, SL2S). It applies approximately to printed M_E values whose error "is dominated by the measurement of R_Ein" (R29). It does not apply to the aperture masses of SNL-1 and SNL-2 (inside R_ap, not θ_E).
- **This is an error in how v1 draws its uncertainties, not in any value.** It goes to the frozen v2 lens test (step D), with a known-issue entry. No value changes.

**F2. D-064 item 4 is contradicted by the sources and by the algebra.** *Both readers.*
- **D-064 item 4 says** the g_obs/g_bar ratio "does not depend on [the source's cosmology] to first order, because both masses scale with the same distances".
- **The sources say otherwise:**
  - Newman et al. 2017: "The lensing M/L is proportional to distance".
  - SLC15, R29 and R32 each give a first-order shift in α (∝ lensing mass / stellar mass) with H0: 5 %, 4 % and 3.5 % respectively.
  - SLC15: peculiar velocities of about 500 km/s "would induce shifts of up to 5 per cent in α".
- **The algebra agrees with the sources.** From F1, g_obs ∝ 1/D. g_bar ∝ M★/R_E² ∝ D_L²/D_A², which is nearly independent of D at low redshift. So g_obs/g_bar ∝ 1/D at first order, the same as for the dwarfs and globular clusters.
- **This is an error in a ruled decision's stated reason.** It needs a JvH ruling, a correction to D-064 item 4 by a new entry, before the v2 lens test is frozen.
- **In v2:** distance (H0, peculiar velocity, redshift frame) becomes a system- or dataset-scale term moving g_obs, with the source-stated sizes:
  - 3–4 % (Newman, 500 km/s);
  - up to 5 % in α (SLC15);
  - 3.5–5 % for H0;
  - z = 0.041 ± 0.001 against 0.04243 for NGC 6505 (R30).

**F3. The SLACS θ_E error differs between sources.**
- The sizes are 2 % (R5, adopted by v1), a "conservative 5 %" (R13), 0.5 % (R9, for its own models) and 3 % (SL2S's own choice).
- After F1, this term moves g_bar. Its size is R5's adopted 2 %, with the others recorded in the term's note.

**F4. Shared terms carried as independent ones.**
- The two MaNGA lenses share one Υ_ref = 2.93 ± 0.26, which R32 gives as half a 2σ model range. v1 adds it in quadrature per system, as if independent.
- In v2 it becomes one dataset-scale term (within R32) with `size_kind = range`.

**F5. Smaller items, recorded for the v2 test.**
- The NGC 6505 lens-model errors are "lower-bounds which only account for measurement uncertainty" (R30 §4.3). The term is listed, with its size not given.
- R32's L_Ein errors appear to be magnitude errors only; the corrections carry no stated error (Reader B, inference).
- **The black hole:** about 2 % of M_E for SNL-0 (R28) and 0.57 % for NGC 6505 (R30). It is inside M_E; whether it is a "detected baryon" is a definitional question for a ruling. It is listed, not classified.
- **Gas.** Three sources assume gas inside R_E is negligible. The registered gas term (D-076) keeps a small default. Both are recorded, as now.
- SL13 prints M/L 3.69 ± 0.06 in the text and ± 0.03 in Table 3. Not used by v1.

## What this means for standard 2.4.0

- **No new column.** F1 and F2 are about which axis a term moves, which §7a `moves` and the registry formula already express.
- **One rule worth stating in 2.4.0's §2a**, as clarifying text (a patch-level wording change within the minor version): when a radius is both the coordinate and an input to one side's mass, its error is carried by the side whose value changes, computed from the formula, not "at fixed radius" by convention.
