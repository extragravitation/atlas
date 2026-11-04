# Dwarf galaxies (`aeg-d-dwarfs/v1`): adjudication of the two step A readings

**2026-11-04, Claude.** It compares `dwarfs-reader-A.md` (72 terms) and `dwarfs-reader-B.md` (42 terms, grouped more coarsely). Both readers read the same core sources:
- the package sources: Pace 2025, Wolf 2010, McLaughlin & van der Marel 2005, Woo 2008, Putman 2021 and Lelli 2016;
- the σ originals: Geha 2026, Collins 2013, Tollerud 2012 and Fritz 2019;
- the structure originals: Martin 2016 and Muñoz 2018;
- the distance original: Savino 2022.

The e-print hashes agree for every source both read.

## Agreement

The two readings agree on every term they share:
- the quotes;
- the sizes as stated;
- the scales;
- which axis each term moves;
- whether v1 carries it.

Reader B's grouping merges terms that Reader A splits. For example, B's D3 covers A's D5–D9 (velocity-error floors), and B's D18 covers A's D37, D41 and D42 (distance calibrations). No term in one reading contradicts the other.

**The term list for v2 is the union**, grouped as follows. Each group is one row of the v2 uncertainty-terms table unless stated.

| Group | Terms (A / B) | Scale | Moves | v1 carries |
|---|---|---|---|---|
| σ statistical error | A D1–D3 / B D1 | point = system | g_obs | yes |
| Upper-limit level, mixed by source | A D4 / B D2 | point = system | g_obs | yes (`x_dwarfs_sigma_limit_level`) |
| Per-star velocity error floors and calibration | A D5–D9 / B D3 | dataset, per pipeline | g_obs | no (inside the printed σ) |
| Unresolved binaries | A D10–D12 / B D4 | system | g_obs, usually up; up to ~20 % in σ (Wolf, citing Minor 2010) | no |
| Membership and contamination | A D13–D15 / B D5 | system | g_obs, either sign; "few-percent" (Tollerud) | no |
| Aperture or coverage; flat profile | A D16–D17, D22–D23 / B D6 | system | g_obs; +0.05 dex on mass for general β (Wolf) | no (D-051 coverage only) |
| Rotation or gradients | A D18 / B D8 | system | g_obs | no |
| Estimator normalisation | A D20–D21 / B D9 | dataset | g_obs; ±10 % (Wolf) | named only |
| Equilibrium and sphericity | A D19, D24 / B D10 | dataset; system where tides apply | g_obs | named only |
| Light-weighted against member-sample σ | A D25 / B D7 | dataset | g_obs; not stated | no; the D-038 1A assumption is missing (below) |
| Deprojection 4/3 | A D27–D28 / B D11 | dataset | both; < 2 % (Wolf), 1.305–1.352 by profile | named only |
| R_h measurement error | A D29 / B D12 | point = system | both | **no: empty in 64 of 64 rows** |
| Ellipticity error, radial variation | A D30–D31 / B D13 | point = system | both | **no** |
| r_h convention, profile family, tracer | A D32–D35 / B D14–D16 | system | both | flag `rh_semimajor_assumed` only |
| Distance statistical error | A D36, D39–D40 / B D17, D19 | point = system | g_obs (see below) | partly: observables only |
| Distance calibration (shared scale) | A D37–D38, D41–D42 / B D18, D20 | dataset, per calibration (Savino: 21 systems, ~3.5 %) | g_obs (see below) | no |
| Inherited host distances | A D43 / B D22 | system | g_obs | flag named in REPRODUCTION.md, absent from rows |
| Magnitude error | A D45–D46, D53 / B D23 | point = system | g_bar | yes |
| Luminosity-function population and IMF | A D47–D48 / B D24 | dataset, per source | g_bar; ~0.2 mag (age) | no |
| Band transformation; extinction | A D49–D50 / B D25, D27 | dataset per source; system | g_bar; not stated | no |
| M_V,⊙ = 4.85 | A D52 / B D26 | dataset | g_bar; no error stated; others use 4.83 | fixed |
| Υ_V model (age, [Fe/H], code, IMF, SFH) | A D54–D61 / B D28–D35 | dataset (with system-scale [Fe/H]) | g_bar | yes, as the D-060 envelope |
| HI detections and limits | A D62–D66 / B D37–D39 | system | g_bar | partly; HI mass errors not carried |
| Helium factor 1.33 | A D67 / B D36 | dataset | g_bar; no range stated | fixed |
| Gas inside r½ = ½ total | A D68 / B D40 | system | g_bar | flag `gas_half_total` |
| Molecular and ionised gas | A D69 / B D41 | dataset | g_bar | `not_addressed` |
| Heterogeneity of compiled originals | A D70–D72 / B D42 | dataset | both | no |

## Findings settled at source

**F1. Distance does not move the stellar g_bar under v1's construction.** *Both readers; Reader B checked it numerically.*
- With L_V ∝ D² and r½ ∝ D, g_bar(stars) ∝ D⁰, and the D-058 gas rescale keeps the gas ∝ D⁰.
- g_obs = 3σ²/r½ ∝ D⁻¹.
- Boötes III is the exception. Its L_V comes from a distance-independent M_V (D-061 item 2), so its g_bar ∝ D⁻².
- Reader B: on andromeda_01, D × 1.1 gives g_obs × 0.909 and g_bar × 1.000.
- **Consequence:**
  - for 63 of 64 systems, a distance error is a vertical shift on g_obs against g_bar, not a diagonal one;
  - `data/assumptions.json` `dw_distance` ("enters g_obs and g_bar together") is true of the inputs, but misleading about the effect;
  - the v2 registry formula must give the net direction (§2a rule 5).

  This needs no standard change.

**F2. Phoenix II: v1 uses the "all possible members" σ; the source prefers the "certain members" value.** *Reader B; verified at source.*
- Fritz et al. 2019 (arXiv 1805.07350v4, `spec_v1_ref1_arx.tex`):
  - Table 4 gives σ = 9.5 (+6.8/−4.4) km/s "calculated from all possible members" (l. 446) and 11.0 (+9.4/−5.3) from "the certain members" (l. 452).
  - The caption reads "We indicate in bold which determination we prefer" (l. 436), and the bold row is the certain-members one.
  - l. 393: "our preferred set of values are those derived when excluding this star".
  - l. 415: σ "does not depend significantly on which set of members is considered".
- v1 uses 9.5. No frozen rule found selects the all-members value: D-038 2B covers multi-population fits, not membership sets.
- **To be ruled in the frozen v2 dwarf test (step D), not changed here.** The two values agree well within their errors.

**F3. Systems the source describes as out of equilibrium are plotted.** *Reader A; verified against D-025 and the σ coding.*
- D-025: "Systems the source itself describes as tidally disturbed or out of equilibrium go to the exclusion register with the quotation."
- **And XXVII:**
  - v1's σ original is Collins 2013, which says it is "unlikely to be in virial equilibrium, if it remains bound at all".
  - The σ coding records that quote (`reading/sigma_rules_rows.csv`), but the system is plotted.
  - Martin 2016 calls it "likely not a bound stellar system".
- **Antlia 2:** Ji 2021, its σ original, says its kinematics "support a tidal disruption scenario" (abstract). It is plotted.
- **Boötes III:** "tidally extended" appears only in Putman 2021's gas table note, not in its σ or structure originals. It is not covered by D-025 as written.
- **This is a possible inconsistency in v1 with a frozen rule.** It is to be resolved in the v2 test, with a known-issue entry. No value is changed here.

**F4. Uncertainties v1 omits.**
- v1 carries no error on R_h or ε (64 of 64 rows), although both originals print them.
- v1 does not propagate the distance error into any g error column.
- Both readers agree. v2 must carry them: R_h and ε as point = system terms moving both axes; distance per F1.

**F5. Named items missing from v1.** *Both readers.*
- The D-038 1A assumption ("member-sample σ taken as representative of the light-weighted σ") is not in the `assumptions` string or the registry.
- No binary-screening flag exists, although D-025 asks for one. The information is in `reading/sigma_values.csv`.
- The `distance_inherited` flag named in REPRODUCTION.md appears on no row; whether any system inherits a host distance is unchecked.

**F6. Smaller items, recorded for the v2 test.**
- Antlia 2 has no distance error in v1, while Vivas 2022 gives a 5.4 kpc dispersion and a ~13 kpc gradient (Reader A).
- And XVIII: Kvasova 2024 uses 1.33 Mpc; the package uses 1180 kpc (Reader A).
- `beyond_source_range` is on 39 of 64 rows, against D-060's "26 of 64" below the metallicity floor. The difference is unexplained (Reader A).
- Savino 2022's extinction-law systematic ("below 0.02 mag", l. 733) is in a LaTeX comment, not the printed paper, so it is not used (Reader B).
- Solar M_V is 4.85 in v1; Carlin and Richstein use 4.83, which does not enter the package's L_V (Reader B).

## What this means for standard 2.4.0

- **Nothing new beyond the draft.**
- F1 shows that §2a rule 5 (direction from the registry formula) is sufficient, as long as the registry formula gives the net effect.
- The mixed upper-limit levels are already handled by `err_level`, and per source in `x_dwarfs_sigma_limit_level`.
