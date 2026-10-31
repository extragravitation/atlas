# D-052: selecting the structure, distance and magnitude values for A5/A7 — frozen

**Frozen 2026-10-30, before the selection is run.** The hashes of this file and of `data/packages/aeg-d-dwarfs/v1/reproduction/select_structure.py` are in `data/frozen/d052-structure-selection.json`.

## Input

`reading/structure_values_all.csv`: the two-reader readings, with disagreements adjudicated against the papers.

The papers are the LVDB `ref_structure`, `ref_distance` and `ref_m_v` originals for each system (D-048 item 1). Values a paper quotes from another paper ("quoted from" in `note`) are never selected.

## Rules, applied in order

1. **Profile** (structure). The rows used are those of the fit marked `headline`. If no fit is marked, the first fit present in this order is used: exponential, Plummer, Sérsic, King. The fit is recognised from `variant` or `note`. A row whose fit cannot be recognised is used only when it is the paper's sole fit. The quantities are ra0, dec0, ellipticity, pa and r_h, taken from the same fit wherever the paper gives them per fit.
2. **Angular radius.** r_h in arcmin (or arcsec, converted) is preferred, because the Atlas applies its own distance. A radius printed only in pc is recorded and flagged "physical radius only". Its angular value needs the paper's distance, and the case is listed.
3. **Convention.**
   - "circularised" or "azimuthally averaged" in the row: circularised.
   - "semi-major" or "major axis": semi-major.
   - Otherwise semi-major, flagged `rh_convention_not_stated` (D-052 item 2). The other reading is computed as an assumption effect.
4. **Distance.** The rows used are distance_modulus rows marked `headline`. If none is marked, the row whose location cites the abstract. If neither exists, the case is listed for JvH. A method containing "kinematic", "velocity" or "dynamical" is rejected (D-036 #6).
5. **Magnitude.** M_V is taken by the same headline-then-abstract rule. The paper's own distance modulus is taken from the same paper's rows by that rule. Where both exist, m_V,0 = M_V + (m−M)_paper. Otherwise the case is flagged "distance basis of M_V differs".
6. **Duplicate printings.** Among several rows of the chosen quantity, the table printing is used, then the one with the most significant digits. A remaining tie is listed.

## Output

`reading/structure_selection.csv`: one row per system. It gives each selected value with its paper, row reference and flags, plus a list of the cases left for JvH.
