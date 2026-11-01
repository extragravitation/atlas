# A6 strong lensing: input reading brief (2026-10-31), as given to the AI readers

You read published values for an atlas that compares the observed gravitational acceleration of systems with the Newtonian acceleration from their detected ordinary matter. This package covers galaxy-scale strong lenses that are early-type galaxies. You are a reader: you transcribe what the sources print, exactly. You do not compute, judge results or interpret.

The rules are frozen in `data/packages/aeg-d-strong-lensing/v1/REPRODUCTION.md` (read it first) and `docs/methods/A6S_PRECEDENCE.md`.

## Hard rules
- **Nothing from memory.** Every value comes from a source you opened. Give the URL and the location (table, column, row, or section and paragraph) for every value, plus a quote of at most 15 words for text statements.
- **Copy values exactly as printed:** digits, rounding, units and log or linear form. Asymmetric errors are kept as printed. Do not convert units or take logs. Where a value is printed as an upper or lower limit, record the limit and its kind.
- **Version.** Prefer the journal version or the journal's machine-readable table (`content.cld.iop.org` MRT/ASCII files for AAS journals; VizieR mirrors such as `vizier.idia.ac.za` or `vizier.cfa.harvard.edu`). Where only the arXiv version can be read, mark `version = arXiv vN` for that value. Never send a spoofed user-agent and never get around a bot check; if a site refuses, note it and use another route.
- **Work only in your own folder.** Do not open other readers' folders.
- Do not compute anything except where this brief says so explicitly. Nowhere does it.

## What to read

For **every system** in each scope listed in your task, read:
- `system_id`: the name as printed, plus coordinates-based names where printed;
- `z_l` and `z_s`: values as printed, and how each was measured (spectroscopic, photometric, or derived with the system's velocity dispersion), with a quote and its location;
- `kind`: the source's statement of morphology or type (early-type, elliptical, S0, late-type, disc, group or cluster lens), with a quote.

**Then, only for systems with printed z_l below 0.30**, read in addition:
- **Observed side.**
  - `theta_E` in arcsec, or `M_E` with its unit and log or linear form, from the scope's observed-default record, with errors.
  - The lens model's name (SIE, power law, composite, image half-separation).
  - The cosmology the source states for its distances: H0, Ω_m, flat or not (once per record).
  - Where the record prints both θ_E and M_E, read both.
  - Where it prints a mass inside an aperture, read the aperture and whether the source says it equals the Einstein radius.
- **Stellar mass,** from the scope's stellar-mass default record:
  - the value as printed, with errors;
  - its aperture: inside R_E (which R_E: whose model), total, or another radius (read it);
  - the IMF, the population model, and the bands or spectra used;
  - every IMF variant the source prints (e.g. Chabrier and Salpeter columns).
- **Light profile,** only where the stellar mass is not printed inside R_E:
  - the source's own fit: profile type (Sérsic n, de Vaucouleurs, MGE);
  - R_e in arcsec or kpc as printed;
  - per-component values for multi-component fits, with each component's printed share of light or mass.
- **Gas:** any statement in the source about gas inside the Einstein radius of this system, with a quote; otherwise "none".

## Specific questions (settle at source, quote the sentence)
1. R61 (Collier, Smith & Lucey 2018): is the fiducial aperture R_ap the Einstein radius?
2. R57 (Sonnenfeld et al. 2019, SuGOHI III): which radius does the printed stellar mass refer to?
3. R26 (Newman et al. 2017) and R29 (Collier, Smith & Lucey 2018b): do they print a light-profile fit (type, R_e, n) for their lens?
4. The gas candidates listed in `docs/sources/screening-A6S/packaging-inventory.md` §4 that are in your scopes: quote each statement and give its location.

## Output
Write one CSV file, `reading.csv`, with one row per value and these columns:

`scope, system_id, record, quantity, value, err_minus, err_plus, limit, unit, form, location, quote, url, version, note`

- `quantity` is one of `z_l`, `z_s`, `z_l_method`, `z_s_method`, `kind`, `theta_E`, `M_E`, `aperture`, `lens_model`, `H0`, `Om`, `flat`, `mstar`, `mstar_aperture`, `imf`, `pop_model`, `bands`, `profile_type`, `R_e`, `sersic_n`, `component_share`, `gas`.
- `form` is `linear` or `log10`.
- `version` is `VoR`, `MRT`, `VizieR` or `arXiv vN`.
- Leave cells blank where they don't apply.

Also write `questions.md`: the answers to the four specific questions, plus anything the rules did not settle. Then reply in under 150 words: rows written, systems per scope, the count below z = 0.30, and anything you could not read.
