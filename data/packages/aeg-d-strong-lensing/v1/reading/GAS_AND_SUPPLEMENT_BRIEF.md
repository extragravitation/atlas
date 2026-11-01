# A6: gas and supplement reading brief (2026-11-01), as given to the AI readers — version 2

**Version 2 (2026-11-01 09:05).** The first run of this brief was stopped by JvH before it finished, and its partial outputs are not used. Version 2 changes only the scope of part G, to keep each reading manageable:
- per-galaxy rows only for small samples or massive galaxies;
- large catalogues are described by table and column, not transcribed;
- parts G and S are read in separate runs.

Nothing else changed.

You transcribe published values for an atlas that compares the observed gravitational acceleration of systems with the Newtonian acceleration from their detected ordinary matter. You are a reader: copy what sources print, exactly. You do not compute or judge.

## Hard rules
- **Nothing from memory.** Every value comes from a source you opened. Give the URL, the location (table, column, row, or section and paragraph) and a quote of at most 15 words for every text statement.
- **Copy values exactly as printed:** digits, units, log or linear form, limits and errors. Do not convert.
- **Version:** prefer the journal version or a machine-readable table. Where only arXiv can be read, mark `version = arXiv vN`.
- **Access:** never spoof a user-agent or get around a bot check. If a site refuses, record that and use another route, or mark NS.
- Work only in your own folder. Do not open other readers' folders.

## Part G: gas in early-type galaxies (candidates C1–C31 in `docs/sources/search-log-A6-gas.md` §3)

For each candidate record:
- the phase (hot X-ray, HI, molecular);
- the sample: number of galaxies, their selection, the stellar-mass or luminosity range as printed, and the distance or redshift range;
- the method: for X-ray, deprojection or modelling, and the metallicity assumed; for CO, the conversion factor; for HI, the beam and sensitivity;
- **gas masses, or upper limits, inside a stated radius of 10 kpc or less, or inside a stated multiple of R_e of 2 or less.** Give the radius as printed (kpc, arcsec, or in R_e) and the value with its errors or limit type. Where the paper gives a gas-to-stellar mass ratio in such a radius, record that. Where it gives both the gas mass and the stellar mass in the same radius, record both.
  - **Per-galaxy rows** only where the sample has 40 galaxies or fewer, or for galaxies whose printed stellar mass is at least 10^11 M_sun (or whose printed K-band luminosity or absolute magnitude is the sample's brightest quarter, where no stellar mass is printed).
  - **Larger samples:** one row per sample-level statistic the paper prints (median, mean, range, detection rate with its limit), plus one row `quantity = catalogue_location` naming the table, the columns and how many galaxies it holds, so the values can be taken from the machine-readable table later.
- whole-galaxy totals only as `quantity = gas_total_no_radius` (recorded, not used).

Output `gas_reading.csv` with the columns:

`candidate, citation, phase, galaxy, radius_value, radius_unit, quantity, value, err_minus, err_plus, limit, unit, form, stellar_mass_same_radius, stellar_mass_unit, location, quote, url, version, note`

where `quantity` is one of `gas_mass_in_radius`, `gas_to_stellar_in_radius`, `sample_statistic`, `catalogue_location`, `gas_total_no_radius`.

## Part S: supplement for the lens package (from `adjudication.md` and the conversion code)

Record these in `supplement_reading.csv`, with the columns of `READING_BRIEF.md`:
1. **R29** (Collier, Smith & Lucey 2018b): the cosmology, H0 and Ω_m (and Ω_Λ), as printed.
2. **SNL-1 (ESO 286-G022):**
   - the stellar mass or the luminosity and stellar-population M/L inside the Einstein radius from R25 (Smith, Lucey & Conroy 2015);
   - R26 (Newman et al. 2017), if it covers SNL-1;
   - the IMF, the population model, and the aperture.
3. **R13** (Grillo et al. 2009; VizieR J/A+A/501/461) for every SLACS lens with printed z_l below 0.30:
   - the **total** stellar masses (Chabrier–BC03 and Salpeter–BC03);
   - the de Vaucouleurs R_e that R13 or R5 prints for the same lens, naming which.
4. **R7** (Auger et al. 2009): the printed M_E (log) for every SLACS lens below 0.30, if not already in `adjudicated_inputs.csv`.
5. **Salpeter conversions,** quoted with the sentence and its location:
   - R29's α for Salpeter;
   - R32's α for Salpeter;
   - R30's factor;
   - for R10 (S4TM, FSPS) and R20 (SL2S), the Chabrier-to-Salpeter mass ratio of the population model as printed in the model paper they cite. Name the model paper and give the location. If no ratio is printed there, write "not printed".

Write `questions.md` for anything not settled. Reply in under 150 words.
