# aeg-d-dwarfs/v1: brief for reading the velocity dispersions

Written 2026-10-30, before any dispersion was opened. The text given to every reader is this file, verbatim. It implements `REPRODUCTION.md` (frozen), D-038, D-042 and D-050. Two readings are made independently:

- **Reading 1** feeds the conversion.
- **Reading 2** is the second reading (pass/fail test 1).

Neither reader sees the other's sheet or any conversion code. The comparison is made by script, and every disagreement is resolved by going back to the paper, never by the result.

## What you read

You read one sheet of (system, paper) pairs from `reading/sigma_candidates.csv`, with the PDF path for each paper.

- Read the paper itself.
- Do not use LVDB, any compilation, or memory.
- Do not compute anything: record only what the paper prints.

## What you record

Record one row per **dispersion value the paper prints for the system**. A paper may print several values for one system, for example:

- second moment and dispersion about rotation;
- with and without a velocity gradient;
- the whole sample and a subsample or population;
- with and without a binary correction.

Record every one, each in its own row. Do not choose between them: the frozen rules choose.

| Column | What to write |
|---|---|
| `key` | System key, as on the sheet |
| `paper` | As on the sheet |
| `copy_read` | `arXiv <id>v<N>`, or `version of record` (D-050) |
| `value_id` | `v1`, `v2`, … within this system and paper |
| `sigma` | The number as printed, in km/s. Keep printed digits; no rounding, no unit conversion. |
| `err_minus`, `err_plus` | As printed. Symmetric errors go in both columns. Blank if none. |
| `limit` | `upper` if the paper gives only an upper limit, otherwise blank |
| `limit_level` | For a limit, the confidence level as printed (e.g. `90%`, `95.5%`, `2σ`), else blank |
| `estimator` | The paper's words for what this value is (e.g. "intrinsic dispersion, Gaussian likelihood"; "second moment including rotation"; "dispersion about the fitted gradient") |
| `sample` | Which stars: `whole member sample`, or the paper's description of the subset (e.g. "metal-rich population", "stars within R_h") |
| `n_members` | Number of member stars used for this value, as printed. Blank if not stated. |
| `gradient` | `none fitted`, `fitted, value is about the gradient`, `fitted, value is without gradient`, or `not stated` |
| `binaries` | The paper's treatment of binary stars, in its words. Use `not stated` if absent. |
| `coverage_stated` | How far the members reach relative to the half-light radius, in the paper's words (e.g. "members out to 2.5 r_h"; "all within one DEIMOS field, ~1 r_h"). Use `not stated` if the paper does not say it. Do not infer coverage from a figure or a table of positions. |
| `velocities_released` | `yes` (give the table or archive) or `no` / `not stated` |
| `quoted_from` | If the paper takes this value from another paper rather than measuring it, the cited paper; else blank |
| `quote` | The exact sentence or table cell that gives the value |
| `location` | Page, section, table and row, or equation |
| `note` | Anything else the rules may need (e.g. "value from MCMC posterior median"), without judgement |

## Rules for the reader

1. **Copy, don't judge.** If a value is ambiguous (two tables disagree, an erratum is cited), record both and say so in `note`.
2. **Errata (D-050 item 4).** If the paper mentions an erratum, note it. Errata are searched separately on ADS for every paper.
3. **Version of record (D-050 items 1 and 5).** Read the copy on your sheet. The comparison with the version of record is a separate step.
4. **Nothing for this system?** If the paper does not print a dispersion for the system, write one row with `sigma` blank and say why in `note` (e.g. "only per-star velocities; no dispersion printed").
5. **Stay on your sheet.** Do not open papers that are not on your sheet. If a paper cites a better source, write it in `note`.

## Output

CSV, UTF-8, one file per reader per sheet, with the columns above in that order.
