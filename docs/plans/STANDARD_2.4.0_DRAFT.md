# Data standard 2.4.0: working draft

**Status: working draft, 2026-11-04.** It is not the standard. It collects what step A has shown the standard needs. It will be completed when the dwarf, globular-cluster and lens readings are adjudicated, then written as `docs/data-standard.md` 2.4.0, reviewed independently, and put to JvH for approval. It is frozen on merge. Every item is **additive** (§0: new optional columns, closed-list values or descriptor keys), so 2.4.0 is a minor version and packages stating 2.3.0 or earlier stay valid.

## Items known before the remaining readings

**1. A confidence level that the source does not give.**
- **Need:** an empty `err_level` means 0.683 (§3). The X-COP 2022 files and E22 do not state their level (X-COP test §5).
- **Change:** a new optional column `err_level_status`: `stated` or `not_given_by_source`.
  - When it is `not_given_by_source`, an empty `err_level` means "not given", never 0.683.
  - The site says "confidence level not given by the source" on those rows.
- **Validation:** `not_given_by_source` requires `err_level` to be empty.

**2. g_bar as the source's bin coordinate.**
- **Need:** in KiDS-1000, g_bar is the coordinate the lenses are binned by. It has no point error by construction (readings §1).
- **Change:** a new optional column `g_bar_basis`:
  - `computed` (the default when absent);
  - `bin_coordinate`, with optional `g_bar_bin_lo` and `g_bar_bin_hi` (m s⁻²) where the source gives the bin edges.
- **Validation:** `bin_coordinate` rows have empty `g_bar_err_point_*`, and §7a carries the terms that move the bin coordinate (stellar mass and the like) at system or dataset scale.

**3. A bound on g_bar (X-COP A8 stage 2, #129; D-090).**
- **Need:** systems whose stellar mass the source does not give, where gas alone sets a bound on the source's central g_bar.
- **Change:** a new optional column `g_bar_bound`: `none` (the default), `lower` or `upper`, plus `g_bar_bound_basis` (text, required when not `none`).
  - It means a bound on the source's **central** g_bar from the components the source gives. It is **not a confidence limit** and carries no `err_level`.
  - `limit` keeps its meaning: it applies to the measured quantity only.
  - g_obs errors are kept on such rows (validation rule 5 applies only to `limit`).
- **Rules that travel with it:**
  - rows with `g_bar_bound ≠ none` are excluded from population averages, binned summaries, fits and the inputs of frozen pattern tests;
  - downloads carry the column;
  - views draw the bound in the direction the X-COP test fixes (A8 site requirements).
- **Validation:** `g_bar_bound ≠ none` requires `g_bar_bound_basis`, and empty `g_bar_err_*` columns.

**4. A point-scale term the source states but does not put in its error columns.**
- **Need:** KiDS K2. The paper adds 0.1 dex to every RAR error bar for the ΔΣ-to-g_obs conversion, but the released errors do not include it, and how it was combined is not stated (readings §1).
- **Change:** in §7a, a new optional column `in_error_columns`: `yes` or `no`.
  - A `point` row with `applies_to = *`, a stated size and `in_error_columns = no` records such a term.
  - The site shows it beside the error bars, never added in.
- **Validation:** `in_error_columns = no` requires `status = given` and a size.

**5. A ruled exception to "v2 equals v1" (validation rule 13; D-090 rule 1).**
- **Need:** X-COP v2 is rebuilt from a different analysis by ruling.
- **Change:** a new descriptor key `x_value_change_ruling` (a decision ID).
  - When it is present, rule 13 is replaced, for that package only, by this: the reproduction test reproduces the new source, and the dataset page states the ruling and that the values differ from the previous version.
- **Validation:** the decision ID exists in `docs/decisions.md`.

## Items waiting for the readings (dwarfs, globular clusters, lenses)

**6. One-value systems where distance moves both axes.** §2a rule 5 already says such a term is drawn as a shift along its direction, computed from the registry formula. The readings will show whether anything more is needed: for example, whether the sources give distance errors in a form the systems table can hold, or need a new `size_column`.

**7. Anything else the readings turn up**, added only if a source requires it.
