# aeg-d-dwarfs/v1: brief for coding the dispersion values against the frozen rules

Written 2026-10-30, before any rule was applied to the values. The text given to every coder is this file, verbatim. Two coders code independently; disagreements are resolved by the rule text and the paper, never by the result. A script then applies the frozen rules to the coded table (`reproduction/apply_sigma_rules.py`, written and committed before the coding is seen).

The rules come from:
- `REPRODUCTION.md` (frozen);
- D-036 #6 and iii;
- D-038 1A, 1B, 2A–2D, 3A, 3B and its addendum;
- D-042 item 2.

The coder does not apply them. The coder records, for every row of `reading/sigma_values.csv`, the facts the rules need. Each fact is taken from the row's own columns, or, where those are silent or unclear, from the paper at the row's `location`.

## Columns to add per row (keep `key`, `paper`, `value_id`, `sigma` to identify the row)

| Column | Values | Meaning |
|---|---|---|
| `what` | `measured`, `quoted`, `prediction`, `simulation`, `gas`, `assumed`, `other` | `measured`: this paper's own estimate from line-of-sight velocities of member stars, made in this paper (including a re-analysis of others' velocities). `quoted`: taken from another paper (`quoted_from` filled). The rest as named. |
| `dimension` | `los`, `3d`, `other` | Line-of-sight dispersion, or 3-D, or other |
| `form` | `global`, `profile_bin`, `approximate`, `range` | `global`: one value for the system's sample. `profile_bin`: one radial bin of a profile. `approximate`: printed with ∼ or ≈ or "around". `range`: printed as a range. |
| `whole_sample` | `yes`, `no` | `yes`: all members the paper uses for the system. `no`: a population, metallicity group, radial subset, a "certain members only" or "excluding star X" variant, or a jackknife. |
| `variant` | free text, short | What distinguishes this value from the paper's other values for the system: the membership variant, the prior, the treatment of binaries, the treatment of rotation. Use `headline` for the value the paper itself presents as its result, if it says so. |
| `rotation` | `second_moment`, `about_rotation`, `none_fitted`, `not_stated` | D-038 2A. `second_moment`: includes rotation. `about_rotation`: dispersion about a fitted rotation or velocity gradient. `none_fitted`: no rotation or gradient was fitted. |
| `binaries` | `multi_epoch_removed`, `statistical_correction`, `none`, `not_stated` | How the paper treats binaries for this value |
| `limit` | `upper`, `lower`, `none` | As printed |
| `limit_level` | as in the row | |
| `coverage` | `beyond_rh`, `within_rh`, `not_stated` | D-038 1A, as the paper states it. `beyond_rh`: the paper states that members used for this value reach beyond the half-light radius (any statement in r_h, R_h, r_half, r_e or r_eff units, or "twice the half-light radius", etc.). `within_rh`: it states that they lie within it. `not_stated`: no statement in half-light-radius units. A statement in core radius, King radius, kpc or arcmin is `not_stated`; quote it in `coverage_quote`. |
| `coverage_quote` | the paper's words and location | Required whenever `coverage` is not `not_stated`, and whenever a statement in other units exists |
| `n_members` | integer or blank | As printed for this value |
| `velocities_released` | `yes`, `no` | D-038 3B: does this paper release its per-star velocities (table in the paper, machine-readable table or archive)? |
| `year` | the paper's year | From `paper` |
| `coder_note` | free text | Anything uncertain |

## Rules for the coder

- **Code what the paper says; do not infer.** If coverage is shown only in a figure, it is `not_stated`.
- **One row out per row in.** Do not merge, drop or add rows.
- **No computing, no memory of values, no other source.**
- **Unclear?** If a row's columns are unclear, open the paper at `location` and read what it says.
