# Patterns P2 (baryonic Tully–Fisher relation) and P3 (flat rotation curves): criteria and reproduction test

**Status: approved by JvH 2026-11-02 07:11 CST ("Proceed as recommended": approve the P2/P3 test, merge #116); frozen on merge** (D-085). It is written before any V_f has been computed by the Atlas and before the per-galaxy rows of the anchor table have been opened.

**Seen so far:**
- the anchor table's header (column list);
- the SPARC galaxy counts for Q = 3 and i < 30° (12 and 12, with 2 in both, leaving 153), which also determine the SPARC selection view already published (#105);
- SPARC's own V_flat values for a few galaxies, in passing on system pages (e.g. NGC 3198). None has been analysed.

If the test fails, the failure is published and the test is not changed (operating rule 5).

## 1. Readings at source (2026-11-02)

**Lelli, McGaugh & Schombert 2016, ApJL ("The small scatter of the baryonic Tully–Fisher relation"; arXiv:1512.04543v1, LaTeX source `BTFR.EmuApJ.tex`, §2.2).** The V_f algorithm:

> "We start by calculating the mean of the two outermost points of the RC: V̄ = ½(V_N + V_{N−1}), and require that |V_{N−2} − V̄| / V̄ ≤ 0.05. If the condition is fulfilled, the algorithm includes V_{N−2} in the estimate of V̄ and iterates to the next velocity point. When the condition is falsified, the algorithm returns V_f = V̄ … Galaxies that do not satisfy the condition at the first iteration are rejected, hence we only consider RCs that are flat within ∼5% over at least three velocity-points."

That Letter's sample (118 galaxies) predates the final SPARC release. It is used here only for the algorithm.

**Lelli, McGaugh, Schombert, Desmond & Katz 2019, MNRAS 484, 3267 ("The baryonic Tully–Fisher relation for different velocity definitions …"; arXiv:1901.05966v1, LaTeX source `BTFR2019.tex`).**
- **§2:** "we use a sub-sample of 153 objects … This excludes 22 objects with low inclinations (i < 30°) … as well as 7 objects with low quality rotation curves (quality flag Q = 3)".

  **Note:** these counts do not add up to 175 − 153 = 22. SPARC Table 1 gives 12 galaxies with i < 30° and 12 with Q = 3, 2 of them in both, which leaves 153. The Atlas applies the criteria (i ≥ 30°, Q < 3), not the counts.
- **§2.2:** "We measure V_f for 123 objects. The remaining 30 galaxies do not satisfy the 5% flatness criteria … because their rotation curves are either rising or declining in the outer parts."
- **§2.2, the outer slope of the flat part:** "If we consider the innermost and outermost points defining V_f, the logarithmic slope S_{1,2} = log(V_1/V_2)/log(R_1/R_2) has an average value of 0.05 and rms scatter of 0.12."
- **§2.2, errors on V_f:** "we revise the values from Lelli et al. (2016a) because we found a minor 'indexing bug' in our software". The Atlas does not reproduce the V_f errors (§4).
- **§3:** M_b = 1.33 M_HI + Υ⋆ L[3.6], with "Υ⋆ = 0.5 M☉/L☉ at [3.6] for all galaxies". "We do not treat bulge and disc separately".
- **§3:** the errors on M_b use "Eq. 5 of Lelli et al. (2016a) … galaxy-to-galaxy variations in Υ⋆ with a standard deviation of 0.11 dex".
- **Table 1:** the published fit for V_f is s = 3.85 ± 0.09, I = 1.99 ± 0.18, σ⊥ = 0.026 ± 0.007, σ_o = 0.24, N = 123 (orthogonal maximum likelihood).
- **Anchor table:** `BTFR_Lelli2019.mrt` ("datafile1.txt"). Columns per the header: Name, log(Mb), e_log(Mb), Inc, e_Inc, Vf, e_Vf, V2exp, V2eff, Vmax, Wp20, Wm50 and Wm50c with errors. Note (1): log(Mb) assumes Υ = 0.5 at 3.6 µm.
  - The local copy (from a public GitHub repository) has SHA-256 `a9b5776f…3a66f` and 20 360 bytes.
  - The canonical copy on the SPARC site must be fetched and its hash recorded before the test runs. If the two differ, the canonical one is used and the difference is reported.

## 2. Definitions (frozen)

- **D1. Rotation curve.**
  - **Points:** a galaxy's points are its `v_rot` observables in `aeg-d-sparc/v2`, ordered by radius: V_1 … V_N at R_1 … R_N.
- **D2. V_f (flat rotation speed).** The algorithm quoted in §1, implemented literally:
  1. Set V̄ = mean(V_N, V_{N−1}) and k = N − 2.
  2. While k ≥ 1 and |V_k − V̄| / V̄ ≤ 0.05: add V_k to the included points, recompute V̄ as their mean, and set k = k − 1.
  3. V_f = V̄, the mean of the included points.

  Rules:
  - If the first test (k = N − 2) fails, or N < 3, the galaxy has **no V_f by the source's criterion**.
  - The included points are the flat part. R_1 and R_2 of S_{1,2} are the innermost and outermost included radii.
- **D3. Authors' sample.** Q < 3 and i ≥ 30° (SPARC Table 1).
  - Every page shows all 175 galaxies; membership is a flag, never a filter.
  - Galaxies without V_f are listed with the reason, never hidden.
- **D4. Baryonic mass.** M_b = 1.33 M_HI + 0.5 L[3.6], in M☉, from SPARC Table 1 (M_HI and L[3.6] in 10⁹ units). It uses one Υ for disc and bulge, as the anchor does "to have a direct comparison".
  - The registry `ml_disk` range (0.2–0.7) may later drive the page through a registry formula.
  - The default stays 0.5.
- **D5. Outer slope of the flat part.** S_{1,2} = log(V_1/V_2)/log(R_1/R_2), over the innermost and outermost points defining V_f (D2).
- **D6. P3 descriptive quantities.** These are Atlas definitions, labelled as such on the page.
  - **(a) Outer slope:** for every galaxy, the least-squares slope of log V against log R over its outermost three points.
  - **(b) Extent:** R_N / R_disk and R_N / R_eff, with R_disk and R_eff from SPARC Table 1.

  Both are continuous quantities, shown as values and never binned into named classes. The only categorical label on P3 is the source's own: V_f found or not found.

## 3. Reproduction test (pass/fail)

The test is run on the D2 output, against the anchor table and SPARC Table 1.

- **R1. Sample.** The 153 galaxies of D3 are exactly the galaxies listed in `BTFR_Lelli2019.mrt`, matched by name after stripping padding. If the table lists a different set, R1 fails, and both lists are published.
- **R2. Which galaxies have V_f.** Within the 153, the Atlas finds V_f for exactly the galaxies with Vf > 0 in the anchor table. The text says 123.
- **R3. V_f values.** For those galaxies, |V_f(Atlas) − Vf(table)| ≤ 0.051 km/s, which is the table's rounding (0.05) plus a margin for the printed velocities.
- **R4. Baryonic mass.** For all 153, |log M_b(Atlas) − log(Mb)(table)| ≤ 0.006 dex, which is the table's rounding (0.005) plus a margin for the Table 1 rounding.
- **R5. SPARC Table 1.** For all 175 galaxies:
  - V_f found ⇔ Vflat > 0 in SPARC Table 1;
  - where found, |V_f − Vflat| ≤ 0.051 km/s.

**Pass** = R1–R5 all hold. Anything else is a fail, published with the per-galaxy differences.

## 4. Reported, not pass/fail

- The mean and rms of S_{1,2} over the Atlas's flat galaxies in the authors' sample, against the source's 0.05 and 0.12.
- V_f errors. The source revised them for an indexing bug, and the Atlas does not reimplement its error code. The table's e_Vf are shown as published.
- The published fit (s = 3.85, I = 1.99, orthogonal maximum likelihood) is shown only as an optional overlay, credited to Lelli et al. 2019. The Atlas does not fit the relation (D-085 rule 1). Published fits by other groups of the same relation, where found, are offered on equal terms.

## 5. What the pages will not do

- Name a cause, or compare with theoretical predictions. Those are on the account pages.
- Drop galaxies without V_f, or galaxies outside the authors' sample.
- Bin continuous quantities into classes.
