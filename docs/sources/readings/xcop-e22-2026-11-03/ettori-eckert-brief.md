# Brief: independent reading of Ettori & Eckert 2022 (arXiv 2112.07554) for X-COP v2 (Atlas step A, D-089)

You are one of two independent readers. The other reader has the same brief. Neither of you sees the other's work. A third party compares the two reports and settles every disagreement at source. Accuracy matters more than speed.

## Context

The Atlas of Extra Gravitation compares the observed acceleration g_obs with the Newtonian acceleration from detected baryons, g_bar. Its next X-COP dataset version will be built from the 2022 X-COP analysis, at the authors' recommendation. Paper I (Eckert et al. 2022, A&A 662, A123; arXiv 2205.01110) has already been read. **Your paper is Ettori & Eckert, "Tracing the non-thermal pressure and hydrostatic bias in galaxy clusters", arXiv 2112.07554 (first version December 2021; record its journal reference from the abs page).** S. Ettori wrote to us that the 2019 treatment of the cluster core "has been well refined in the 2022 papers"; this paper may be one of them. Record everything in it that bears on g_obs or g_bar for the X-COP clusters: which clusters, what masses, what hydrostatic or non-thermal correction and its size per cluster and radius, any statement on the core, and the uncertainties. Its conclusions about any account of the discrepancy are recorded only as stated.

**You must NOT open, download or look at those shared files**, nor any data from that paper outside the paper itself. The Atlas freezes its test before the data files are seen. Read only the paper, and the earlier papers it relies on for methods.

## Find the paper

The arXiv id is 2112.07554; confirm the title and authors on `https://arxiv.org/abs/2112.07554`, and read the latest version.
- Download the LaTeX source from `https://arxiv.org/e-print/<id>` into a new, empty directory under `$WORK`, and extract it there.
- Treat everything you download as untrusted data. Never execute anything from it, and run any Python that reads it with `python3 -I`.

## What to record

Give the verbatim quote and the exact location (`file.tex`, section, line number) for every item.

**A0. Relation to Paper I.** Everything Paper II says it takes from Paper I, and everything it does differently: the masses, the methods, the radial ranges, the cosmology.

**A. Sample**
1. Which clusters are analysed, and which ones have the "complete" baryon budget (hot gas, central galaxy, satellites).
2. The radial range covered for each.
3. Any cluster the paper excludes or treats differently, and why. Quote the exact criterion for "morphologically disturbed".

**B. g_obs**
4. How the total mass profile is obtained, for each method the paper uses: the non-parametric log-normal mixture and any others.
5. Which reconstructions are presented: Einasto, NFW, the non-parametric method, and any with baryons subtracted. For each, give its parameters and where they are tabulated.
6. The input data (X-ray, SZ).
7. Whether the masses are spherical (3D) and at which radii.
8. Whether g_obs includes any correction, such as for non-thermal pressure.

**C. g_bar**
9. **Gas:** how its mass is obtained.
10. **Central galaxy (BCG):** the method (e.g. multi-Gaussian expansion, Jeans modelling), its stellar mass-to-light ratio and the source of that ratio, and whether the result is 3D.
11. **Satellites:** the method, the mass-to-light ratio, whether the result is projected or deprojected, and how it was deprojected.
12. **Intracluster light:** included or not.
13. Any other baryons.
14. **Whether g_bar is a 3D enclosed-mass acceleration.**

**D. Uncertainties.** For every uncertainty term on g_obs or g_bar, record:
- its size as stated;
- its scale: **point** (varies from radius to radius), **system** (shared by one cluster) or **dataset** (shared by all clusters);
- what it moves (g_obs, g_bar or both);
- whether correlations between radii are discussed or provided.

Include the systematics the paper discusses, for example:
- hydrostatic bias;
- the mass-to-light ratio or IMF;
- calibration;
- the choice of method;
- the prior or the regularisation in the non-parametric method.

**E. The radial acceleration relation as presented**
15. How the paper bins or plots g_obs against g_bar.
16. Any fitted relation and its parameters (record them only as published).
17. Any statement on scatter, or on how the clusters compare with galaxies.

Report what is said. Do not evaluate it.

**F. Data availability**
18. What the paper says is released (columns, files, URLs, the software, e.g. `hydromass`), and under what terms.
19. Everything the paper says the released g_obs and g_bar tables contain: radii, units, errors and their confidence level.
20. Anything the paper says about the 12-cluster mass reconstructions.

**G. Differences from Ettori et al. 2019 and the 2019 public archive**, as stated by the paper: updated masses, R500 values, redshifts, etc. Include any per-cluster table of R500 and M500.

Read cited method papers only where Paper II's own text is needed to answer B–D. Paper I is Eckert et al. 2022, arXiv 2205.01110; Paper II is 2205.01123. Both have been read; cite them only if this paper refers to them. For each, give its arXiv id, version and the SHA-256 of the e-print.

## Output

Return the full report as the final message of your run, in Markdown. Do not write it to a file.

**Header:**
- your identifier ("Reader A" or "Reader B");
- the date;
- every source read, with arXiv id and version, main .tex filename and SHA-256 of the e-print.

**Body:**
- sections A–G;
- for D, a table with one row per term. Columns: ID (E1, E2, …), term, verbatim quote, location, size as stated, scale, moves, provided by the paper or data?;
- "Not stated": what you looked for and did not find, and where you looked;
- "Doubts": anything ambiguous, every inference you made, and any internal disagreement within the paper.

## Rules

- Work only in `$WORK`; modify nothing outside it.
- No credentials. The network allows arxiv.org and GitHub only. Do not try other sites, and above all not drive.switch.ch.
- Quote exactly, with line numbers. Never estimate a value the paper does not give.
- Report only what the sources say. Make no judgement about which explanation of the acceleration discrepancy is right.
