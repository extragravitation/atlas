# aeg-d-dwarfs/v1: brief for reading structure, distance and magnitude

Written 2026-10-30, before any structural, distance or magnitude value of an A5 or A7 candidate was opened. Every reader is given this file verbatim. It implements `REPRODUCTION.md` (frozen), D-036 #6, D-048 item 2, D-050 and D-051.

Two readings are made independently:
- **Reading 1** feeds the conversion.
- **Reading 2** is the second reading (pass/fail test 1).

The two are compared by script. Disagreements are resolved by going back to the paper, never by the result.

## What you read

Your sheet lists (system key, name, paper, role, PDF), where role is `structure`, `distance` or `magnitude`. Read the paper itself. Do not use LVDB, compilations or memory. Do not compute anything: record what the paper prints, with its units.

## What you record

Record one row per **printed value** of a quantity your role asks for. If a paper prints several values of one quantity, record each in its own row. Examples: from different fits (exponential, Plummer, Sérsic, King), from different data sets, with and without a correction, or the same value printed twice with different digits.

| Column | What to write |
|---|---|
| `key`, `paper`, `role` | As on the sheet |
| `copy_read` | `arXiv <id>v<N>`, or `version of record` |
| `quantity` | One of the names below |
| `value`, `err_minus`, `err_plus` | As printed. Symmetric errors go in both columns. Blank if none. |
| `unit` | As printed: arcmin, arcsec, pc, kpc, mag, deg, or "hms"/"dms" for sexagesimal coordinates |
| `variant` | The paper's description of what distinguishes this value: profile model, data set, method. Write `headline` first if the paper presents this value as its adopted result. |
| `quote` | The exact sentence or table cell |
| `location` | Page, section, table and row |
| `note` | Anything the rules may need, without judgement |

**Quantities by role**

- **`structure`**
  - `ra0`, `dec0`: the centre;
  - `ellipticity`: as printed. Say in `note` if the paper gives axis ratio b/a instead;
  - `pa`: position angle of the major axis, and its convention if stated;
  - `r_h`: the half-light radius as printed. In `note`, say whether the paper calls it semi-major axis, circularised (azimuthally averaged), or does not say;
  - `profile`: the profile model used.
- **`distance`**
  - `distance_modulus` or `distance`;
  - `method`: the paper's words, e.g. "RR Lyrae, period–luminosity", "tip of the red-giant branch", "horizontal branch", "isochrone fit", "Cepheids", "kinematic". Record the method even when it is not your sheet's main role.
- **`magnitude`**
  - `m_v`: apparent V;
  - `M_V`: absolute V;
  - `extinction`: A_V, E(B−V) or another band, exactly as given, and whether `m_v` is already corrected;
  - `luminosity`: in L_sun, if printed;
  - `band_note`: the filter system, if the paper converts to V.

## Rules for the reader

1. **Copy, don't judge.** Ambiguities go in `note`, with both printings recorded.
2. **Errata (D-050).** Note any erratum the paper mentions.
3. **Nothing printed.** If the paper prints no value for a quantity of your role for this system, write one row with `value` blank and the reason in `note`.
4. **Stay on your sheet.** Do not open papers that are not on it. If a paper takes a value from elsewhere, record it, fill `note` with "quoted from <paper>", and record the cited paper.

## Output

One CSV per reader per sheet: UTF-8, quoted, with the columns above in order.
