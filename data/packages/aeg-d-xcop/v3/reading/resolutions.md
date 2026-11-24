# X-COP v2 second reading: resolutions (part B order of work, steps 1–2)

**Reader:** an independent agent, 2026-11-05. It had no access to `convert.py`, any v2 table, or v1's tables, and opened none of them. It parsed only the released FITS columns and computed no g_obs or g_bar.

**Rule-1 conflicts for JvH: none.** No explicit exclusion wording, no preferred value and no fiducial baseline was found among the released values (`d096.csv`).

## 1. Sources as read (all verified by hash)

| Source | File | SHA-256 | e-print SHA-256 | Read |
|---|---|---|---|---|
| `data_E22.tar.gz` | archive | `ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d` (= part A §1) | — | the five `gbar_gobs` members (hashes = `result_part_a.json` A1) |
| `mbar.tar.gz` | archive | `0420a7edba60da7f2df6aa4f38cbb21135ab50949d579176a8c893bab712c496` (= part A §1) | — | hash only; holds no `gbar_gobs` file |
| E22, arXiv 2205.01110v1 | `hydromass.tex` | `fdf040686a41eee38be2b9a2feb28c1c97b0b8cc0a4c8a7aa78785947cfa5cb1` | `18fc2e8025f56c716a864e5ef9436cccb5f0be05cff7a0f004aedd4605e5c7d8` | in full |
| Paper II, arXiv 2205.01123v1 | `einasto.tex` | `7e0034b83a373eb61ea0bb8cdbdae179f676e814607a2b98c43ce153e6d00c20` | `a138d88fec5d3b7627eeb9657d663c30f9aae7a12ce3e968edf08bba07503fcb` | §2.1 (l. 71–82), §3.1 (l. 130–170), conclusions (l. 225–231), appendices (l. 243–265); keyword search of the rest |
| Paper II | `tab2.tex` | `dff5a1093332cfc503467af1be60ab8eaf772610c774e4c47e6e2ecbd4c73fe2` | (same e-print) | in full |
| Ettori & Eckert 2022, arXiv 2112.07554v1 | `p_nt_b_aa.tex` | `c20d6303a6ea020003781040ba25303e312d5c1f463cb9830962e2d8f993ca4c` | `ef5cbd0a2d19b62428c362cfcbf973c3bdf928a3e8c6a36a547a6e9431a6e840` | table `tab:gamma_beta` with foot (l. 256–278), l. 176–186, l. 296–310, l. 375–400; keyword search for units and exclusions |
| Loubser et al. 2020, arXiv 2006.05706v1 | `BCG_v3_withoutBold.tex` | `861938c060fe6e1dfad851652781f44a6fad55b1a812fc9897772950f3b89e26` | `ded65c6d1457b3183ee21b573bf426bf5ddfd20575fc39f429eb0e887dd9044c` | l. 434–537, 547, 684, appendix table l. 920–950 |
| Ghizzardi et al. 2021, arXiv 2007.01084v1 | `xcop-metallicity.tex` | `2d862a214412164dbb1f80e8ae2939033624c8868c3cd36e9a4418d0bedd0f0f` | `88c8e91c036077e2ca660cd029943d576df1462daae914d3e58aa24169c5a9e8` | l. 705, 712, 715, 923, 926; keyword search for exclusions |

All e-prints were downloaded fresh from arxiv.org on 2026-11-05. Their hashes equal the truncated hashes in the test and in readings §3, §3b and §3c. `hydromass.tex` and `xcop-metallicity.tex` equal the test's `fdf04068…` and `2d862a21…`. Every quote in the CSV files was checked by script to occur verbatim on its cited line.

## 2. Agreements with step A, part A and the test

1. **Rows:** A644 19, A1795 21, A2029 22, A2142 20, A2319 27, **109** in all, as part A's result and the D-091 erratum say.
2. **Model form:** no such statement, so `model_dependence` = `none` (`model_form.md`). This is as rule 3 expected.
3. **D-096:** no exclusion wording, no preferred value among the released values, and no fiducial baseline. This is as rule 1 and D-105 O4 expected (`d096.csv`).
4. **Confidence levels:** `not_given_by_source` for both GOBS and GBAR errors (`err_levels.csv`). This is as item 5 expected.
5. **Paper II Table 2:** w is printed with its error as "±", and the unit row (`tab2.tex` l. 4) prints `$10^{-3}$`, as item 6 says.
6. **Ettori & Eckert:** the table rows are at l. 261–272 and the foot at l. 274–276. The foot's "(second column) … (last column)" (l. 274) and "at $1 \sigma$ c.l." (l. 276) are as the test quotes them.
7. **Other quotes rechecked at source:**
   - E22 l. 56, 97, 103–114, 126, 130, 263, 309, 311, 366, 373, 404, 408, 410, 435, 453, 456, 458, 486, 502, 504, 506, 508, 528 and 539;
   - Ghizzardi l. 712, 715 and 923, and the commented-out l. 926 with "$\sim$ 1.74";
   - Loubser l. 547 ("up to $\sim$ 15 per cent");
   - Ettori & Eckert l. 182 and l. 377.

   All match the test's wording.

## 3. Disagreements and additions, resolved at source

**R1. Error form, determined (item 5).** The headers say nothing about the error columns. By item 5's rule, the GOBS pair is error magnitudes: the magnitude condition holds on 109/109 rows and the bounds condition on 0/109. GBAR_ERR is a magnitude (109/109). Item 5's error-form part does not fail. Its level is still not given (R7).

**R2. A2319's hydrostatic statements: 7, not the 3 the test expected (item 9).** The test expected E22 l. 435, l. 502 and Paper II l. 80. `hse_statements.csv` marks 7 rows `in_a2319_notes = yes`:
- E22 l. 435 holds **two** A2319 sentences: "particularly striking in the case of A2319, for which HSE masses are known to be biased low", and, reporting eckert19, "with the notable exception of A2319".
- E22 l. 502, sentence (1) of the test.
- **E22 l. 512** (not expected by the test): "with the exception of a system known for its high level of nonthermal pressure support (A2319)".
- Paper II l. 80.
- **Paper II l. 161 and l. 227** (not expected by the test). They refer to "the quoted outliers" and "a few outliers with $\alpha\gtrsim 0.5$", which Paper II names at l. 135 ("three systems (A2319, A644, and A2255)") and l. 152. l. 161 says that "the validity of the hydrostatic equilibrium assumption in unrelaxed systems is unclear". l. 227 says that the high indices are "likely a systematic effect … caused by hydrostatic bias and/or miscentering". These are marked `by_reference`.

**Left out of A2319's notes:** Paper II l. 163. Its "four objects" are not named by the source. Membership (A644, A2255, A2319, A3266) is the Atlas's inference from Table 2, so it is not presented as the source's statement about A2319. The row is kept, marked `inferred_from_table`.

**Reader's call, stated:** only statements where the source itself identifies the cluster count, by name or by an explicit back-reference within the same paper. This is a reading choice, not a rule-1 matter. It changes only the text of A2319's notes, which item 9 takes from this file. JvH may overrule before the reading is frozen.

**R3. `bcg_ml_extra_mass_model` applies to A644 and A2319 only (item 7).** The test's default is the five. Loubser l. 458, l. 475 and its ★+CEN+DM table show two things. The 8.3 ± 2.9 % is an average over the BCGs that have their own weak-lensing DM halo, and A644 and A2319 are not among them. E22 l. 109 applies that average to A644 and A2319, which lacked weak-lensing masses. The reasoning is in `bcg_extra_mass_systems.md`. `applies_to` = `aeg-s-000177;aeg-s-000183`.

**R4. Two range sentences not named in the test (rule 1).**
- E22 l. 342: "we restrict specifically to the radii corresponding to the existing spectral and SZ data points to avoid extrapolating".
- E22 l. 512: "radial range of interest ($[0.01-2]R_{500}$ …)".

Neither names released rows as removed. The first restricts evaluation to the data radii, which is what the released rows are. The second summarises a range. Both are recorded in `d096.csv` as `no_exclusion_wording`. There is no conflict.

**R5. Anomalous α error signs: five clusters, not two (item 6).** The test names RXC1825 (l. 271) and ZW1215 (l. 272) as examples. As printed in the last column, these clusters have a "+" sign on the **lower** error at both R500 and R200:
- A644 (l. 269);
- A1644 (l. 261);
- A3266 (l. 268);
- RXC1825 (l. 271);
- ZW1215 (l. 272).

A1644, A3266 and ZW1215 print `0.0^{+0.0}_{+0.0}`, with zero-width errors. All are recorded as printed, signs included, and none is repaired (`properties.csv`, column `alpha_sign_anomaly`). Four of these five have no rows in v2. A644 is one of the five plotted clusters, so its `x_xcop_alpha_nt_*_err_lo` columns hold "+" values.

**R6. α unit: `inferred_percent`.** The table, its caption (l. 257) and its foot (l. 274–277) give no unit. The nearest text, l. 385 ("$b = \alpha$ from turbulence of about $<$11\%, $<$51\%, and $<$29\% for A85, A1795, and A2029"), compares per-cent figures with the table. That supports the per-cent reading but does not state the table's unit. By item 6, the columns hold the values as printed.

**R7. Confidence levels: no statement, with three near misses.** E22 l. 362 calls the points "posterior NP mass estimates" but gives no level. l. 370's "68\% interval" belongs to the sample median NP-to-model ratio. l. 111's "1$\sigma$ errors on the weak lensing masses" belongs to an input of the BCG mass-to-light error. None of them is a stated level for GOBS_ERR_* or GBAR_ERR. Paper II gives no level for w's error either. The status is `not_given_by_source`, and no level is read as 0.683 (D-093 rule 1).

**R8. Which R500 for `hse_bias` (item 7).** No sentence at or near E22 l. 502 defines R500. The paper's stated scaling convention is the NFW R500 and M500 (l. 366; also l. 362 and the l. 277 caption, "from the NFW fit"). Table 1's R500,TOT is also an NFW fit (l. 316). This supports using Table 1's R500,TOT but does not establish it, so it stays labelled an inference, as the test says. The `r500_context` rows are in `hse_statements.csv`.

**R9. Minor points, recorded with no action.**
- E22 spells the cluster "Zw1215" (Table 1, l. 335). Paper II and Ettori & Eckert spell it "ZW1215".
- E22 l. 109 says "the 23 other clusters". Loubser's average also leaves out A2055 and A963 (l. 475), so it covers 21.
- Part A §1 defers member hashes to `sources.json` at conversion. This reader verified the members against `result_part_a.json` A1, and all five match.

## 4. Not read, or read only in part

- **Not read:** Ghirardini et al. 2018 (cited by E22 and Paper II for A2319), Ettori et al. 2019, Eckert et al. 2019, Herbonnet et al. 2020, van der Burg et al. 2015, and the published A&A versions (only the arXiv versions were read). None is needed for the fields in this reading. A2319's statements are taken from E22 and Paper II as item 9 requires.
- **Read in part:** Paper II, Ettori & Eckert, Loubser and Ghizzardi (sections listed in §1, plus keyword searches). E22 was read in full.
- **Not opened:** the `<C>_BCG.txt`, `GP_thermo.fits` and `EIN3_bar_mass.fits` members, and all of `mbar.tar.gz` apart from its hash.

## Main-session resolution (2026-11-05; no access to any v2 table)

- **Paper II l. 163 ("four objects", unnamed):** left out, as the reader did. D-100 rule 3 counts a statement only if it is about the system itself. An unnamed set, identified only by the reader's reading of Table 2, is not a statement about A2319.
- **The other differences from the test's stated expectations** follow from the frozen rules and need no ruling:
  - the 7 A2319 statements;
  - the 8.3 % figure applies to A644 and A2319;
  - five "+" lower errors, recorded as printed;
  - α unit `inferred_percent`;
  - R500 labelled an inference.

  Each is recorded above with its quote, and the result reports it.
