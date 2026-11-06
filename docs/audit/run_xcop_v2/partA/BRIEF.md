# X-COP v2 audit: reader brief

## The task (fixed text, plan §2.6)

> You are auditing one measurement of a public dataset. Download the archive given, check its SHA-256 against the value given, and stop if it differs. Open the file named in the locator and read the row given: the radius, the observed acceleration GOBS, the baryonic acceleration GBAR, and their error columns, exactly as stored, with the column names and units from the file header. Report the radius in kpc and the accelerations in m s⁻², converting units only if the header gives a unit other than these, and say which conversion you used. Use the paper only to confirm what each column means; quote the line you rely on. If a column's meaning or unit is not stated, record "not stated" and do not guess. Return one CSV row per measurement with: measurement_id, file, row, each value with its unit and column name, and notes. Do not look for or use any other copy of this dataset.

Do this for each of the 10 measurements in `/home/claude/audit_xcop/packet/rows.csv`. The locator gives the archive, the file in it, and the row number.

## The archive and the paper

- **Archive:** `data_E22.tar.gz`
  - URL: https://drive.switch.ch/index.php/s/nKxwcKwftb3Esjc/download (follow redirects, e.g. `curl -sL`)
  - SHA-256: `ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d`
  - bytes: 161298
- **Paper:** Eckert et al. 2022, A&A 662, A123, arXiv 2205.01110. The e-print source is at https://arxiv.org/e-print/2205.01110v1.

The locator does not say whether "row N" counts from 0 or from 1. Say which you assume and why. If the file or the paper settles it, quote that.

## Isolation (strict)

- Work only in your own folder, `/home/claude/audit_xcop/readers/<READER>/`.
- Do NOT open:
  - `/home/claude/atlas`, or any `.claude/worktrees` folder;
  - `/home/claude/audit_v2`, or `/home/claude/audit_xcop/readers/` except your own folder;
  - the session scratchpad;
  - extragravitation.org, or the GitHub repository extragravitation/atlas.
- Download the archive yourself into your folder.

## What to write in your folder

1. `return.csv`: your full return. One row per measurement, with: measurement_id, file, row, and for each column read its name, the value exactly as stored, and its header unit, plus the converted value and the conversion used where one was needed, and notes.
2. `compare.csv`: the comparison input, header exactly
   `measurement_id,status,r_kpc,g_obs,g_obs_err_lo,g_obs_err_hi,g_bar,g_bar_err_lo,g_bar_err_hi`
   - Use kpc and m s⁻², with full stored precision (repr of the float).
   - `status` is `ok`, `unreadable` or `method_incomplete`.
   - Leave a field blank if its meaning or unit is "not stated".
   - For the error fields, give what the file's error columns store, converted to m s⁻² if needed. Say in `return.csv` notes whether each error column holds an uncertainty (a ± size) or a bound (a value). Do not convert between the two.
3. `notes.md`: your column-meaning quotes from the paper, your row-numbering choice, and anything unclear.
4. `code/`: your code.

Reply with: the counts per status, anything you marked "not stated", the paths of your files. Do not paste the values.
