# Adjudication log: disputed sigma codings

Input: `disputed.csv`, with 102 rows and 106 disputed fields. Output: `resolved.csv`, with one line per disputed field.
Sources opened: the brief (`reading/SIGMA_CODING_BRIEF.md`) and the 34 PDFs named in the input. I opened no LVDB file, no `reproduction/` file and no other scratch directory. I computed nothing and used no remembered values. For `headline`, each coder's value is `yes` when their `variant` starts with "headline" and `no` otherwise.

## Clarifications as applied

1. **coverage.** `beyond_rh` only where the paper says, in half-light-radius units, that members used for this value lie beyond r_h. A per-star table with an R/r_h column and a membership flag also counts.
   - Applied to Fritz 2019, Table 2. Phx II very-likely members lie at 1.54 to 1.82 Rhalf.
   - "Out to 2.5 R_HL" gives only an outer bound, so it is `not_stated`. This covers the Alfaro-Cuello mosaic, which is measured in M54's r_h.
   - Kirby 2017: star 31 lies at 2.0 r_h and is "retained in our sample", so that sample is `beyond_rh`. The 10-star M16 subset is `not_stated`, because the paper does not say whether star 31 is among the ten.
2. **whole_sample.** An alternative membership method applied to all the data is `yes`. This covers:
   - Collins 2013 "v & Pi cuts";
   - the preliminary mixture or Gaussian fits on all observed stars (Pickett, Charles, Collins 2020 and 2021, Gregory, Spencer);
   - the Jenkins M3 mixture;
   - Battaglia's 182-star 3-sigma pass;
   - Taibi's unweighted P > 0.05 analysis.

   These are `no`:
   - added named stars (binaries, RR Lyrae);
   - single-instrument subsets;
   - bulk-only values with the cluster modelled separately (Zoutendijk);
   - the paper's method run on another paper's data set alone (Collins 2013 on T12, Zoutendijk on Li 2017, Kirby 2014 on Lewis and on Brown). This data set is not the paper's member sample for the system, so it counts as a subset of the data sets.
3. **headline.** `yes` only where the paper says which estimate it adopts, prefers or reports as its result.
   - **How I read it:** a printing of that same estimate elsewhere also counts as headline. Examples are a rounded text value, a corner-plot label with more digits, or a figure annotation. A different estimate that the paper does not prefer is `no`.
     - Simon 2020: the abstract reports the 90% upper limit, so the resolved 1.2 value is not headline.
     - Harris 2006: the abstract reports the gradient-removed 27.5, so the global Gaussian fit is not headline.
   - **Weakest calls:**
     - Row 140, Geha Fig. 16. The caption does not state how the annotation relates to Table A1. It is the only dispersion the paper gives for that system.
     - Row 93, Collins 2013 Table A1 "Full algorithm". This is the adopted method, but the text prints 8.6 where Table A1 prints 8.7.
4. **velocities_released.** If the velocities belong to another paper, the answer is `no`: T12 re-analysis (Collins 2013), M16 velocities (Kirby 2017), and the Spencer et al. 2018 MMT data (Pace 2020, which gives membership only).
5. **n_members.** Counted as printed for this value.
   - Blank where the count is printed only as approximate ("Approximately 60-70", "~30") or as a sum of parts ("23 RGB + 3 HB").
   - Blank for Geha 2026 arXiv Table A1. Its column 9 is "number of member stars identified", but the dispersion uses only stars within 2 r1/2, so it is not the count for this value. Its own Sgr II text, "34 stars", differs from the table's 28.
   - Heiger rows where the count is printed as a single number ("31 RGB") take that number.
6. **what.**
   - Collins 2013 App. A.3, random 4- to 30-star draws repeated 1000 times: `simulation`.
   - Kirby 2014, Leo A re-analysis of Brown et al. data: `other`. The tracers are 10 B supergiants plus 2 H II regions. The brief's `measured` requires member stars, and `gas` would mean gas only.

**form (brief text).** `approximate` only for values printed with ~, ≈ or "around". "As high as 15" (Hendricks) and "up to 8" (Taibi) are neither approximate nor a range, so they are `global`. Munoz 2006 gives one value for stars beyond 0.6 rlim. That is not a bin of the paper's profile, so it is `global`; `whole_sample = no` records the subset.

**Close call in coverage.** Kacharov 2017 (row 264) is `beyond_rh` on the text "starting to flatten out ... beyond the half-light radius". This describes the member rotation profile.

## Agreement with final values

| field | disputed | coder 1 matches | coder 2 matches |
|---|---|---|---|
| coverage | 10 | 4 | 6 |
| form | 3 | 0 | 3 |
| headline | 18 | 2 | 16 |
| n_members | 19 | 0 | 19 |
| velocities_released | 5 | 0 | 5 |
| what | 16 | 15 | 1 |
| whole_sample | 35 | 6 | 29 |
| **total** | **106** | **27** | **79** |

Unresolved: none. Rows 140, 93 and 264 rest on the weakest basis, as noted above.
