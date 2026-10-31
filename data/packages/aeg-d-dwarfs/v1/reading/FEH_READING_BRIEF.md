# aeg-d-dwarfs/v1: brief for reading metallicities (D-057) and Woo et al. 2008 mass-to-light ratios

Written 2026-10-31, before any metallicity or Woo 2008 value was opened. Every reader gets this file verbatim. Two readings are made independently, compared by script, and disagreements are resolved against the paper.

## Sheet A: metallicity

The sheet lists (system key, name, paper, kind, pdf). Kind is `spectroscopic` or `photometric`. For the named system, record **one row per printed value of the system's mean or median [Fe/H]**, and a separate row for each printed spread in [Fe/H] if there is one. Copy what is printed and compute nothing.

| Column | What to write |
|---|---|
| `key`, `paper`, `kind` | As on the sheet |
| `copy_read` | `arXiv <id>v<N>` from the file name |
| `quantity` | `feh_mean`, `feh_median`, `feh_spread` (intrinsic dispersion), or `other` (say what in `note`) |
| `value`, `err_minus`, `err_plus` | As printed |
| `variant` | The paper's words: the sample, the calibration (e.g. "CaT, Carrera 2013", "spectral synthesis"), and whether the value is weighted. Start with `headline` if the paper presents this value as its result. |
| `n_stars` | As printed for this value |
| `quote`, `location` | The exact text or table cell, and its page, section and table |
| `note` | Anything uncertain |

If the paper prints no system mean [Fe/H], write one row with `value` blank and the reason in `note`. If the paper quotes another paper's value, record it and fill `note` with "quoted from <paper>".

## Sheet B: Woo, Courteau & Dekel 2008 (arXiv 0807.1331)

For each system on the sheet, find its row in the paper's table of galaxy properties. Record every printed quantity that is a stellar mass-to-light ratio, or a stellar mass with the luminosity used to derive it. Give the band, the method in the paper's words (e.g. "from colour", "from star-formation history"), quote and location. If the system is not in the paper, write one row saying so.

## Rules

- Copy, don't judge.
- Use no other source and no memory.
- Do not open any other reader's work.
