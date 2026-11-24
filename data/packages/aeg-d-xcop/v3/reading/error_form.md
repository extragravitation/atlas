# X-COP v2 second reading: error form (part B item 5)

**Outcome.**
- **GOBS_ERR_LO and GOBS_ERR_HI are error magnitudes** (determined by the item 5 rule; the headers do not say).
- **GBAR_ERR is an error magnitude** (determined by the item 5 rule; the headers do not say).
- Item 5's error-form part is therefore **not undetermined**. By item 5: `g_obs_err_lo` = GOBS_ERR_LO, `g_obs_err_hi` = GOBS_ERR_HI, `g_bar_err_lo` = `g_bar_err_hi` = GBAR_ERR.

## 1. What the FITS headers state

Files: the five `gbar_gobs_<C>.fits` members of `data_E22.tar.gz` (archive SHA-256 `ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d`, equal to part A §1). Member SHA-256, equal to `result_part_a.json` A1:

| File | SHA-256 | NAXIS2 |
|---|---|---|
| `A644/gbar_gobs_A644.fits` | `6994602130138d7f67ee1bdc542143efaa8e3788c0673968fb90e911a9da4b07` | 19 |
| `A1795/gbar_gobs_A1795.fits` | `8a6ff9f7ae360047aa0f3be5c51442d0e217f989e81c15e75e7fa54766c4982c` | 21 |
| `A2029/gbar_gobs_A2029.fits` | `8ed65afd32061e822e45730338ce55ae34b9098eecfddf9fba4cde5f88d83ed4` | 22 |
| `A2142/gbar_gobs_A2142.fits` | `f700885754486cc6bddca599cb71b7e59431f9dba48135f88f58434bf0b7cb87` | 20 |
| `A2319/gbar_gobs_A2319.fits` | `cb89b6b3a0fc3c4fa361a671713b33b47dc35dca9b837c17ad16cac9cc6c5cd9` | 27 |

The five headers are identical except NAXIS2. Complete keyword list, as read:
- HDU 0: `SIMPLE = T`, `BITPIX = 8`, `NAXIS = 0`, `EXTEND = T`.
- HDU 1: `XTENSION= 'BINTABLE'`, `BITPIX = 8`, `NAXIS = 2`, `NAXIS1 = 24`, `NAXIS2`, `PCOUNT = 0`, `GCOUNT = 1`, `TFIELDS = 6`, then
  `TTYPE1 = 'RADIUS  '` `TFORM1 = 'E       '` `TUNIT1 = 'kpc     '`;
  `TTYPE2 = 'GBAR    '` `TUNIT2 = 'm/s^2   '`; `TTYPE3 = 'GBAR_ERR'` `TUNIT3 = 'm/s^2   '`;
  `TTYPE4 = 'GOBS    '` `TUNIT4 = 'm/s^2   '`; `TTYPE5 = 'GOBS_ERR_LO'` `TUNIT5 = 'm/s^2   '`;
  `TTYPE6 = 'GOBS_ERR_HI'` `TUNIT6 = 'm/s^2   '` (all TFORM `'E       '`).
- No `EXTNAME`, `TCOMM`, `TDISP`, `COMMENT` or `HISTORY` keyword. **The headers state nothing about what the error columns are.** The column units (m/s², the same as GOBS and GBAR) fit both readings.

E22 (`hydromass.tex`, SHA-256 `fdf040686a41eee38be2b9a2feb28c1c97b0b8cc0a4c8a7aa78785947cfa5cb1`) describes no data release and no error columns (read in full; agrees with readings §3.2 item 2). So item 5's rule decides.

## 2. The rule (item 5, fixed before the data were seen), applied

Computed per row on the float32 values widened to float64. Counts only (no values are printed or stored here).

| Cluster | Rows | LO < GOBS < HI (bounds) | LO < GOBS and HI < GOBS (magnitudes) | GBAR_ERR < GBAR |
|---|---|---|---|---|
| A644 | 19 | 0 | 19 | 19 |
| A1795 | 21 | 0 | 21 | 21 |
| A2029 | 22 | 0 | 22 | 22 |
| A2142 | 20 | 0 | 20 | 20 |
| A2319 | 27 | 0 | 27 | 27 |
| **All** | **109** | **0** | **109** | **109** |

- Bounds condition: holds on 0 of 109 rows, so it fails (on every row, not just one).
- Magnitudes condition: holds on 109 of 109 rows, and the bounds condition fails on at least one row. **GOBS pair = error magnitudes.**
- GBAR_ERR < GBAR on 109 of 109 rows. **GBAR_ERR = magnitude.**

Also observed (reported, decides nothing): all six columns finite on every row; GOBS, GBAR, RADIUS and all three error columns positive on every row; RADIUS strictly increasing within each file; GOBS_ERR_LO < GOBS_ERR_HI on 52 of 109 rows (so the pair is asymmetric in both directions).

## 3. What this does not establish

- Whether the magnitudes are standard deviations, half-widths of a percentile interval or something else, and at what level: see `err_levels.csv` (`not_given_by_source`). The authors' question 6 (part A result), extended by part B item 5, still applies.
- The rule's magnitude reading is a decision rule, not a statement by the source. A source statement would govern if one is received; that comes in under a new ruling.

Script: `scripts/parse.py` (reader's scratch; not committed). Values file: off-repo `values.csv`, SHA-256 `c320382cfe9e1bb798f1f458c301bfa07bec44586ba7ae0c0b704dfe340b42dc`.
