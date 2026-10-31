# aeg-d-dwarfs/v1: supplementary reading (half-light radius convention; magnitude basis)

Written 2026-10-30. The first run of the frozen selection script (`reproduction/select_structure.py`, output kept as `reading/structure_selection_v1.csv`) showed that two facts D-052 needs were not captured as explicit fields. Free-text notes cannot supply them reliably. This brief asks for them directly. Two readers code independently, and disagreements are resolved against the paper. No rule is changed by this brief.

The sheet lists (system key, name, paper, role, pdf). The role is `structure` or `magnitude`. Read the paper itself. Do not compute anything, do not use memory, and do not use LVDB.

## For role `structure`, one row per system

| Column | Values |
|---|---|
| `rh_definition` | `semi_major_stated` (the paper says the radius is along the semi-major axis, or is the semi-major axis of the half-light ellipse); `circularised_stated` (it says circularised, azimuthally averaged, geometric mean, or multiplied by √(1−e)); `elliptical_radius_profile` (the profile is written in an elliptical radius whose scale is the semi-major axis, and r_h is the half-light value of that profile, without the word semi-major); `not_stated` |
| `ellipticity_fitted` | `yes` if the paper fits ellipticity in the same model that gives r_h, `no`, or `not_stated` |
| `rh_quote`, `rh_location` | The paper's words and their location |

## For role `magnitude`, one row per system

| Column | Values |
|---|---|
| `apparent_v_printed` | `yes`, `no`. Is an apparent V magnitude printed for the system by this paper, its own measurement? |
| `apparent_v_extinction_corrected` | `yes`, `no`, `not_stated`. Is that apparent magnitude corrected for extinction (m_V,0)? |
| `apparent_v_quote`, `apparent_v_location` | |
| `mv_distance_basis` | For the absolute magnitude M_V this paper prints: which distance modulus it used, as the paper states. Use `own` (this paper's modulus), `cited` (another paper, named in `mv_distance_source`), or `not_stated` |
| `mv_distance_modulus` | The modulus value as printed in this paper where it is printed (own or cited), else blank |
| `mv_distance_quote`, `mv_distance_location` | |
| `note` | Anything uncertain |

## Output

A CSV, UTF-8 and quoted, with the columns `key`, `paper`, `role`, then the columns of that role, then `copy_read`.
