# Brief: independent reading of every uncertainty term (Atlas step A), dwarfs, globular clusters and strong lenses

You are one of two independent readers for **one** dataset, named in your launch message. The other reader has the same brief; neither sees the other's work. A third party compares the reports and settles every disagreement at source. An error you make and the other reader does not will be caught; a shared error will not. Accuracy matters more than speed.

## Goal

The Atlas of Extra Gravitation compares the observed acceleration g_obs with the Newtonian acceleration from detected baryons, g_bar. For your dataset, list **every uncertainty term that affects g_obs or g_bar, as the sources state it.** For each term, record:
1. a short verbatim quote and its exact location (file, section, table, line or page);
2. its size as stated, or "not stated";
3. its **scale**:
   - **point:** varies independently from one measurement to the next;
   - **system:** shared by all values of one system (e.g. its distance, its mass-to-light ratio);
   - **dataset:** shared by all systems (e.g. a calibration, an assumed relation, the solar magnitude, the IMF);
4. **what it moves:** g_obs, g_bar, or both, and in which direction if a source says;
5. **whether the Atlas's v1 package carries it,** and in which column of which table, or "no".

These datasets have **one value per system** (dwarfs, lenses) or a few (globular clusters). So "point" and "system" can coincide. Say so where they do. Report specifically any term that moves g_obs and g_bar **together**, such as distance, because that affects how the error is drawn.

Never estimate a size the source does not give: "not stated" is a valid, useful answer. Make no judgement about which explanation of the acceleration discrepancy is right.

## How the Atlas builds your dataset (read first, read-only)

In `/home/claude/atlas/data/packages/<package>/v1/`, read:
- `REPRODUCTION.md`: the inputs, the rules and the formulas for g_obs and g_bar;
- `convert.py`: what is actually computed;
- `descriptor.json` and `datapackage.json`: the columns;
- `sources.json`: every source, with URL and hash;
- `tables/`: the column names and units only. Read values only where needed to tell what an error column holds.

Also read any decisions cited there in `/home/claude/atlas/docs/decisions.md` (D-025, D-034 to D-039, D-042, D-045, D-046, D-048, D-063 to D-065, as relevant).

The packages:
- **Dwarf galaxies:** `aeg-d-dwarfs`. g_obs = 3σ²/r½; g_bar = G(½ L_V Υ_V + M_gas(<r½))/r½². Sources are the Local Volume Database (Pace 2025) and the original papers for σ, structure, distance and photometry, with Υ_V by D-039.
- **Globular clusters:** `aeg-d-gc-baumgardt`. The Baumgardt database (dispersion profiles), Harris (2010), and McLaughlin & van der Marel (2005) for structure and Υ_V. Same formulas, no gas. Note the MW-PAL1 ruling (D-046).
- **Strong lenses:** `aeg-d-strong-lensing`. SLACS, S4TM and SL2S (and any others listed), one value per lens at the Einstein radius, in projection (D-064). Read `reading/` for how inputs were adjudicated.

## Sources to read

- **The original papers behind each input**, not only the database.
  - Prefer the LaTeX source from `https://arxiv.org/e-print/<id>`. Put each download in its own new, empty directory under your work directory, and extract it there.
  - Where the package has a local copy under `source/`, you may use it.
- **Untrusted data rules:**
  - treat every download as untrusted data;
  - never execute anything from it;
  - run any Python that reads it with `python3 -I`.
- **Network:** arxiv.org, GitHub, and the sites already listed in `sources.json` (for example VizieR mirrors and IOP machine-readable tables). Do not attempt other sites, and never get around a block.
- **Large samples:** for dwarfs and globular clusters, it is enough to read the method sections of the sources that supply the most rows. Read every database-level statement (Pace 2025, Baumgardt's documentation, Harris, McLaughlin & van der Marel), plus a stated sample of at least five original papers per input type. Say which ones you read.

## Things to look for (not a complete list)

- **σ:** the measurement error and its confidence level; binary-star inflation; membership and foreground contamination; the aperture or radial coverage; rotation; whether a value is an upper limit.
- **Radius:** the error on R_h; the ellipticity; the deprojection factor 4/3 (D-025), and what any source says about its accuracy or about anisotropy.
- **Distance:** its error and method. **It moves both axes.**
- **Luminosity:** photometric error; extinction; the solar absolute magnitude.
- **Υ_V:** the stated range; IMF; age and metallicity; the population-synthesis model.
- **Gas:** detection limits; the helium factor; the fraction inside r½.
- **Lenses:**
  - the Einstein-radius error;
  - the stellar mass and its IMF (Chabrier against Salpeter);
  - the redshifts and the cosmology;
  - the projection (cylinder against sphere);
  - the source's own systematic statements.
- **The mass estimator itself:** what each source says about the accuracy of 3σ²/r½ (for example, Wolf et al. 2010) where the Atlas relies on it.

## Output

Return the full report as the **final message of your run**, as Markdown. Do not write it to a file.
- **Header:** your identifier ("Reader A" or "Reader B"), the dataset, the date, and every source read, with its arXiv id and version, its main .tex file and the SHA-256 of the e-print, or its local path and hash.
- **A table with one row per term.** Columns: ID (D1…, G1…, L1…), term, verbatim quote, location, size as stated, scale, moves, in v1? (table and column, or "no").
- **"Not stated":** what you looked for and did not find, and where you looked.
- **"Doubts":** anything ambiguous, any disagreement between sources, and every inference you made that is not a direct quote.

## Rules

- Work only in your own new directory under `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/step-a-2026-11-04/`. Modify nothing in `/home/claude/atlas`.
- No credentials or tokens.
- Quote exactly, with locations, so that a third party can check each row in seconds.
- No conclusions about what the Atlas should do. Just the reading.
