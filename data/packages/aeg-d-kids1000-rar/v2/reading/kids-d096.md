# KiDS-1000 RAR: D-096 fields (second reading, item 11)

Read 2026-11-05. For every file the package uses: does the source (paper) or the release README mark a preferred value, exclude data, or name a fiducial baseline? Quotations are verbatim from the LaTeX source (`RAR_paper_Brouwer_4.tex`, arXiv 2106.11677, SHA-256 `45aa25ab…4b19`) with its line numbers, or from the README (SHA-256 `b3680580…8645`).

## Provenance of the files read

- **Canonical release not obtained.** `https://kids.strw.leidenuniv.nl/sci_data/brouwer2021_rar.tar` was refused by the workspace proxy (CONNECT 403, policy denial). Not worked around. No file below is verified against `v1/sources.json` (which holds only the tarball's hash, `73adc2d4…8733`).
- **Files read** from the public GitHub mirror `rstpier/EFF_G_GALAXIES`, folder `KiDS Brouwer Weak Lensing/`, commit `7606a21d5e7118b49ec57aef79d357da87118346` (the same mirror step A used for the README).
- **README SHA-256** `b3680580696c5dbf5671c700d5e8f90fbfd1dc614fa7e3e07b2f66d1624e8645`: **equal** to the value in test 12. (This confirms the mirror copy is the one step A read; it does not settle test 12, which needs the tarball member.)

| File | SHA-256 (mirror copy) |
|---|---|
| `Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt` | `5343d81c06643e2cc5126490d9f03918ac2708b0cdc4586b1534157c225578a9` |
| `Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt` | `c5fa734affa2e56228f9e78848419a38405775a0cf4c42471ae1c37cdea575ae` |
| `Fig-4-C1_RAR-GAMA-isolated_Nobins.txt` | `b613425287e1600c3ee866d058ca6ead0649095903debc89f09b100070270d74` |
| `Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt` | `963a81504c467feeff8c33043e331ce092f5dab55f0835decd3e8ff419583afc` |
| `Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt` | `5f81078112e1b5cfff24189d1b755db7c48f52d50b179224ed9ab7d8771928fe` |
| `Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt` | `0ae8b6ea736ff4037afaed02552cc389f0f131062c34774bea2542dfab59e6e8` |
| `README.txt` | `b3680580696c5dbf5671c700d5e8f90fbfd1dc614fa7e3e07b2f66d1624e8645` |

## README

- **Preferred value:** none among data values. It marks columns as "(not needed)" (ESD_x, variance, wk², w²k², correlation), which is a statement of use, not a choice between values of g_obs.
- **Excluded data:** none.
- **Fiducial baseline:** none named.
- **Corrections it requires:** "ESD_t[corrected] = ESD_t / bias, error[corrected] = error / bias" and "covariance[corrected] = covariance / bias" (the covariance file's column 7, "bias(1+K[m,i])(1+K[n,j])"). Not a D-096 item; recorded because the released covariance is uncorrected.

## 1. KiDS-bright isolated (`Fig-4-5-C1_RAR-KiDS-isolated_*`)

- **Fiducial baseline:** stars plus cold gas. §4.3, l. 421: "we will use the stellar+cold gas mass $M\un{gal}$ as our fiducial estimate of the total baryonic mass $M\un{bar}$ … throughout this work. This serves as a secure lower limit on $g\un{bar}$." §5.2, l. 516 calls it "our main observational result: the lensing RAR from the KiDS-bright sample without an estimate for the additional hot gas". (Already applied in the test: test 9, 10.)
- **Preferred value:** none beyond the fiducial above. l. 516's "main observational result" contrasts the KiDS-bright result with its hot-gas variant. It is not a choice between KiDS-bright and GAMA, which are different lens samples.
- **Excluded data: YES. Finding beyond the hot-gas variant.** The source removes the KiDS-bright points beyond its isolation limit from its own model comparisons, while still plotting them (shaded) in Figs. 4, 5 and C1:
  - §5.2, l. 508: "Taking into account the effect of the photometric redshift uncertainty of KiDS-bright by only using the seven data points within the isolation criterion limit ($R < 3 \hMpc$) we find: $\chi\un{red}^2 = 4.0$ for MOND …" and "(with the data points beyond the isolation criterion limit still removed)".
  - App. A, l. 748: "When testing these models, we can only use the ESD profile of isolated KiDS-bright lenses within $R < 0.3 \hMpc$. For the mean galaxy mass of the KiDS-bright isolated sample ($\log[M\un{gal}/\hmsun] = 10.69$) this corresponds to a baryonic acceleration of $g\un{gal}>7.56\E{-14} \mpss$. For each RAR measurement resulting from isolated KiDS-bright lenses we will indicate the range in $g\un{bar}$ where the measurement is reliable".
  - App. C, l. 821: "Here we have removed all data points beyond the KiDS isolation limit ($R>3 \hMpc$)".
  - §5.2, l. 489: "the isolation criterion is no longer reliable when $g\un{bar} \lessapprox 10^{-13} \mpss$".
  - **Which rows.** Seven retained points means rows 9–15 (released g_bar 1.2982e-13 to 3.9169e-12, all above 7.56e-14). Rows 1–8 (1.3822e-15 to 7.3580e-14) are the removed points; row 8 (7.3580e-14) lies just below the 7.56e-14 limit. These are the same released bins the Atlas uses (D-098 rule 1, "same data points", is met).
  - **Scope.** The removal is from the model-comparison χ² fits (MOND, EG, N17). The source still presents the points as measurements, and for the ΛCDM simulation comparison it keeps them and mimics the effect (l. 748: "When comparing our KiDS-bright lensing measurements to the MICE simulation, we always take this effect into account by mimicking the redshift offset in the simulation"; Fig. 5 caption, l. 525). Whether this counts as excluding them "from its own analysis of the quantity the Atlas uses" (D-096 rule 2) is a reading the test does not settle and this reader does not rule on.
  - **Text inconsistency at source, recorded as-is:** the radius limit is written "R < 3 h70⁻¹ Mpc" (l. 508, l. 821) and "R < 0.3 h70⁻¹ Mpc" (l. 748, Fig. 4 caption l. 483, l. 489).
- **Relation to v1/v2 handling (from the test text only; v1 tables not opened):** the test says v1 flags these rows `source_quality_low` and keeps them plotted as `default`. A flag is not exclusion. Under item 11 ("Any finding beyond the hot-gas variant (already applied) is a fail of this test"), this is reported as a finding for ruling.

## 2. GAMA isolated (`Fig-4-C1_RAR-GAMA-isolated_*`)

- **Fiducial baseline:** stars plus cold gas (l. 421, applies to all samples; l. 487: the x-axis is "the expected baryonic (star+cold gas) radial acceleration").
- **Preferred value:** none.
- **Excluded data:** none found. The source states the opposite for the low-g_bar region: "We note that the GAMA results, which are based on accurate spectroscopic redshift measurements, are still reliable within this region" (l. 489; also Fig. 4 caption, l. 483). GAMA χ² values use all points (l. 508: "Comparing the GAMA data to the two MG models results in $\chi\un{red}^2$-values of $0.8$"; l. 506: "$N\un{data}= 15$"; l. 821).

## 3. KiDS-bright hot-gas variant (`Fig-4_RAR-KiDS-isolated_hotgas_*`)

- **Fiducial baseline:** this file is not the fiducial. Fig. 4 caption, l. 483: "we show the effect on the RAR of KiDS-bright galaxies if $g\un{bar}$ contained an additional isothermal hot gas contribution within a $100\hkpc$ radius, with a nominal gas mass equal to the stellar mass (orange crosses with $1\sigma$ error bars). We emphasise that this is only a rough order of magnitude estimate of the possible effect of gaseous haloes". §5.2, l. 512: "emphasising that this is only an order of magnitude estimate". (Already applied: test 9, `role = alternative`.)
- **Preferred value:** see fiducial.
- **Excluded data:** the source does not state a separate removal for this file. It inherits the KiDS-bright isolation caveat (same lens sample); the source's stated limit is a radius (l. 748), which in the hot-gas g_bar maps to a different g_bar than in the fiducial file. Not a new finding; the test already discloses it (test 6).

## Other observation (description, not D-096)

Column 1 (g_bar) is identical in all three files and equals the arithmetic midpoint of each §2.1 logarithmic bin to float precision (see `kids-bins.md`). It is a fixed bin coordinate, not a per-sample mean. This contradicts step A's inference ("appear to be bin means", `uncertainty-readings.md` §1.1). No value changes.
