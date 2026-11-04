# Feature ideas, parked until after v0.2

**Written:** 2026-11-04, from JvH's questions "What would be some compelling features or tools that would really make people sit up straight?" and "What about linking to physical pictures … or highlighting on a star map?". **Status: ideas, not plans.** Nothing here is started before v0.2 ships. Each one needs a JvH ruling before work begins, and the neutrality, provenance and privacy rules apply in full.

## Recommended order

1. **"Why this number?"** and **figures ready for papers and talks** (cheap; they earn trust and citations).
2. **Sky map with measurement rings**, plus links to NED, SIMBAD and ADS.
3. **Public prediction ledger.**
4. **"Test your account" bench**, as the flagship for v1.0.
5. **Live error-budget explorer**, grown as the datasets mature.

## The ideas

**1. "Test your account" bench.**
- Anyone writes down a prediction of g_obs from g_bar and the system's properties.
- The Atlas scores it against every dataset, with the same frozen metrics for every account, and shows the residuals by scale, channel and uncertainty scale.
- It runs in the visitor's browser and collects nothing.
- **Must never become a leaderboard:** it shows the scores and does not rank the accounts.

**2. Public prediction ledger.**
- Predictions are frozen by hash through a pull request before the new data exist.
- They are scored automatically when the data land, and the result is posted pass or fail.
- This is the Atlas's own frozen-test standard, opened to the field.

**3. "Why this number?" on every point.**
- One click shows: the source file and its hash, the table or line in the paper, the conversion step, the assumptions with their published ranges, and any open issue.

**4. Live error-budget explorer.**
- Toggle the point, system and dataset uncertainties, and move the assumption sliders. Everything is recomputed from the data, never approximated.

**5. Figures ready for papers and talks.**
- SVG and PDF export, with the caption, the dataset versions and the DOI built in.
- Exact-view share links.
- A small Python package that loads any versioned snapshot in one line, with notebooks that reproduce the key plots.

**6. Sky map and real images.**
- An all-sky map of every system, by real position, coloured by dataset or channel, opening the system pages. A likely route is Aladin Lite (CDS), whose licence is to be checked against the Atlas's code licence before it is embedded.
- Survey cutouts on each system page, with links to Hubble or JWST images where they exist.
- **Measurement rings on the image** at the radii where g_obs is measured.
- Links to NED, SIMBAD and ADS for every system.
- **Cautions:**
  - neutral captions only; no press composites whose overlays describe an account (for example, inferred-mass maps labelled as one);
  - colour composites are labelled "image, not data";
  - population averages such as KiDS get a survey outline, not an image;
  - imagery loads only on click, because third-party requests expose the visitor's IP address (this needs a ruling under rule 11);
  - images are not hosted without a per-image licence check; cutout services and links are preferred.

**7. Smaller items.**
- **A gap map ("wanted" board):** where in scale and system type the data are missing.
- **A tensions page:** where sources disagree.
- **Version diffs:** what changed between versions of a dataset.
- **Motions against light-bending** for the same systems, side by side, never merged.
- **A feed of corrections and new data** (RSS or Atom; nothing is collected).

## Analysis views (added 2026-11-04)

From JvH's question "Are there any other graphing or data representation methods that might teach us something interesting about the data?". Each is a question about the data, not about any account. **Marked for first after v0.2: items 8 and 13.**

**8. Scatter budget.** At each g_bar, compare the observed vertical spread with the spread the stated uncertainty terms alone would produce, by simulating every point within its own terms. If the errors explain the spread, the data allow a tight relation; if not, something varies between systems. It uses the error terms read in step A.

**9. Within-system against between-system spread.** Draw each system's radii as a connected track, and split the variance into a part within systems and a part between them. Offsets between systems point to per-system quantities (distance, inclination, mass-to-light); different shapes would point elsewhere.

**10. Several x-axes, side by side.** Plot the same points against g_bar, radius, baryonic surface density, radius in units of the half-light radius and orbital time, with one tightness measure for all. Which axis collapses the data best is a factual question, and showing every axis keeps g_bar from being chosen by assumption. **Best candidate for a frozen test after v0.2.**

**11. Distance-cancelling views.** For dwarfs, globular clusters and lenses, g_obs/g_bar ∝ 1/D (step A; D-094), so distance is a large shared error. Plot combinations that cancel it (angular quantities, ratios within one system) to see whether the pattern survives without the distance scale.

**12. Environment.** Plot the discrepancy against the distance from the host and against the host's pull at the system's position, for dwarfs and clusters. It is a neutral, continuous axis on which accounts differ, and it connects to D-097.

**13. Error directions as arrows.** On the main plot, draw each systematic term as an arrow showing which way and how far it moves a point (distance moves dwarfs vertically; mass-to-light moves them sideways). It shows which conclusions are robust. The registry formulas already compute the directions.

**14. Redshift.** Plot the lenses and X-COP clusters against lookback time, to see whether they sit on one pattern or shift with cosmic time.

Any of these used to state a result needs a frozen test first. Anything found by browsing is labelled exploratory.

## Cautions, stated once

- **A residual explorer**, plotting leftovers against any property, invites pattern-fishing. If it is built, anything found with it is labelled exploratory and needs a frozen test before it is stated.
- **Nothing here may rank the accounts**, or describe a data point in the language of any one of them.
