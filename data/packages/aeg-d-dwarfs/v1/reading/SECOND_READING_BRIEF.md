# aeg-d-dwarfs/v1: brief for the second reading (REPRODUCTION.md test 1)

Written 2026-10-31, after the conversion was first run.

**Readers.**
- Independent agent sessions, working without access to the conversion code, the package tables or any earlier reading of these papers.
- The sheet is split between two readers by row. Each row is read once by one of them, and that reading is the second reading of that value.

**Sheet** (`second_reading_sheet.csv`).
- Columns: key, name, block, task, paper, file.
- Blocks: `sigma`, `structure`, `distance` and `magnitude`. Each block is one quantity for one system from one paper.

**For every row**, record each value the task asks for, exactly as printed. If the paper prints several candidates (several fits, several distances, a range), record all of them and mark the paper's headline. Output columns:

`key, block, paper, quantity, value, err_minus, err_plus, unit, limit, limit_level, variant, quote, location, note`

- `quantity`: one of `sigma`, `r_h`, `ellipticity`, `distance`, `distance_modulus`, `m_V0`, `M_V`, `mv_distance` or `mv_modulus`.
  - `mv_distance` and `mv_modulus` are the distance or modulus the paper says it used for M_V.
- `limit`: `upper` for an upper limit, with its confidence level as printed.
- In `note`, say whether `r_h` is semi-major or circularised and how the paper defines ellipticity.

**Rules.**
- Copy, don't judge, and compute nothing.
- Use no other source and no memory.
- If a value is not printed, write one row with `value` blank and the reason.
