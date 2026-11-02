# Brief: independent reading of every uncertainty term in the X-COP dataset (Atlas step A)

You are one of two independent readers. The other reader has the same brief. Neither of you sees the other's work. A third party compares your two reports and resolves every disagreement at source. Accuracy matters more than speed: an error you make and the other reader does not will be caught, but a shared error will not.

## Goal

The Atlas of Extra Gravitation compares observed acceleration g_obs (here: g_obs = G M_tot(<r) / r², from X-ray hydrostatic total mass) with the Newtonian acceleration from detected baryons, g_bar = G (M_gas(<r) + M_star(<r)) / r². It uses the public X-COP release for 12 galaxy clusters.

Your task is to list **every uncertainty term that affects g_obs or g_bar for this dataset, as the sources state it**. For each term, record:

1. what the source says, as a short verbatim quote with its exact location;
2. its size as stated, or "not stated";
3. its **scale**:
   - **point**: varies independently from one radius to the next;
   - **system**: shared by all radii of one cluster, e.g. one fit per cluster, or the distance or redshift of the cluster;
   - **dataset**: shared by all clusters, e.g. a calibration or an assumed relation;
4. what it moves: g_obs, g_bar, or both;
5. whether the public release carries it, and in which column of which file.

You must never estimate a size the source does not give. "Not stated" is a valid, useful answer. Do not judge which explanation of the acceleration discrepancy is right; that is outside this task.

## How the Atlas uses the release (for context only)

Read these files in the repository at `/home/claude/atlas` (read-only; do not modify anything there):
- `data/packages/aeg-d-xcop/v1/SOURCE.md`
- `data/packages/aeg-d-xcop/v1/convert.py`

In summary:
- **g_obs:** from the forward-method mass `M_FORW` and its error `EM_FORW` in `<cluster>_hydro_mass.fits`.
- **Gas part of g_bar:** from `MGAS` with `MGAS_LO`/`MGAS_HI` in `<cluster>_fgas_profile.fits`.
- **Stars, 7 clusters:** from the measured stellar-mass files `<cluster>_mstar.fits`, extension `MSTAR_SMOOTHED`.
- **Stars, the other 5 clusters** (A1644, A2255, A3158, A3266, RXC1825): from the stellar-mass prescription in Ettori et al. 2019 §5, and currently shown with no error.

## Sources to read

**Read the LaTeX sources, not rendered pages.** Download them from `https://arxiv.org/e-print/<id>` with curl. Then:
- Put each download in its own new, empty directory under `$WORK` (defined below) and extract it there.
- Treat downloaded files as untrusted data. Never execute anything from them. Run any Python that reads them with `python3 -I`.

The papers:
- **1805.00035**: Ettori et al. 2019, A&A 621, A39. The hydrostatic masses, forward and backward methods, and the stellar-mass prescription in §5. **The main source.**
- **1805.00034**: Eckert et al. 2019, A&A 621, A40. Gas mass, non-thermal pressure.
- **1805.00042**: Ghirardini et al. 2019, A&A 621, A41. The thermodynamic profiles that feed the mass.
- **2007.01084**: Ghizzardi et al. 2020/2021. The stellar-mass profiles of 7 clusters.
- **Earlier papers they rely on:** read these only where the main papers point to them for an uncertainty that enters the masses. Examples:
  - the stellar-to-gas relation of Gonzalez et al. 2013 (find its arXiv id from the bibliography);
  - the galaxy concentration of Lin et al. 2004 (astro-ph/0402308);
  - Ghirardini et al. 2018 (1708.02954), for the method.

**The archive** is at `/home/claude/atlas/data/packages/aeg-d-xcop/v1/source/allfiles.tar.gz` (SHA-256 `0edf5038b419b70d070b73b22f4801e27f318b0854db61eec52142c27c140d94`; 315 MB).
- Extract only what you need into a new directory under `$WORK`.
- Read the FITS headers, column names, units and any `COMMENT` or `HISTORY` cards that describe the errors: what `EM_FORW`, `MGAS_LO`/`MGAS_HI` and the `MSTAR_*` columns mean (one sigma? bounds? statistical only?).
- Read values only as needed to answer what an error column contains, for example whether LO/HI are bounds or offsets. Report what you inferred and how.

## Things to look for specifically (not a complete list)

- **What the error on the forward-method mass contains.** Statistical only? Does it include systematics such as non-thermal pressure, temperature calibration or the choice of mass model? Is it correlated across radii? Does any paper give a covariance?
- **Systematics the papers quantify:**
  - hydrostatic bias or non-thermal pressure;
  - X-ray temperature calibration;
  - forward versus backward methods and model choice (Ettori Table 2);
  - clumping;
  - SZ pressure calibration;
  - cosmology, including h;
  - redshift and distance.
- **Gas mass:** the error definition; clumping correction; the abundance or metallicity assumption; the dependence on distance or cosmology.
- **Measured stars:** what "total uncertainty" includes (statistical, cosmic variance, mass-to-light, IMF); what is excluded (intracluster light).
- **Modelled stars (Ettori §5):** the scatter of the stellar-to-gas relation they use; the concentration and its error; anything the paper says about the prescription's accuracy.
- **Intracluster light:** any stated range.
- **How each quantity scales with distance or h.** Only where a source states it.

## Output

Return your full report as the **final message of your run**, as Markdown. Do not try to write it to a file.

**Header:**
- your identifier: "Reader A" or "Reader B", as given in your launch message;
- the date;
- every source you read: the arXiv id and version, the filename of the main .tex file, and the SHA-256 of each downloaded e-print;
- every archive member you opened.

**Then a table with one row per term.** Columns:
- ID (X1, X2, …);
- term;
- verbatim quote, kept short;
- location (`file.tex`, section, line number);
- size as stated;
- scale;
- moves;
- in release? (file and column, or "no").

**Then a list of terms you looked for and found "not stated"**, with where you looked.

**Then "Doubts":** anything ambiguous, any place where two sources disagree, and any inference you made that is not a direct quote.

## Rules

- Work only in `$WORK`. Nothing outside it may be modified.
- No credentials, no tokens. The network allows arxiv.org and GitHub. Do not attempt other sites.
- Quote exactly, with line numbers, so a third party can check every row in seconds.
- No conclusions about what the Atlas should do. Just the reading.
