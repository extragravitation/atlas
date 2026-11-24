# X-COP v2 second reading: model form of GOBS (part B rule 3, D-087)

**Outcome: no such statement.** Neither a FITS header of the five `gbar_gobs` files nor any sentence of E22 states that the released GOBS column is the Einasto (or any other parametric) curve. By rule 3, **`model_dependence` = `none`** stands on every row.

## 1. FITS headers

The five headers (keyword list in `error_form.md` §1; file SHA-256 there) carry only the structural keywords and TTYPE/TFORM/TUNIT. There is no keyword naming a method, model, fit or reconstruction (no `EXTNAME`, `COMMENT`, `HISTORY` or other keyword). Column name: `GOBS`. **No statement.**

## 2. E22 (arXiv 2205.01110v1, `hydromass.tex`, SHA-256 `fdf040686a41eee38be2b9a2feb28c1c97b0b8cc0a4c8a7aa78785947cfa5cb1`; e-print `18fc2e8025f56c716a864e5ef9436cccb5f0be05cff7a0f004aedd4605e5c7d8`)

Read in full (727 lines). E22 names no data release and never refers to the files or the column, so no sentence can state what the released column is. The sentences that bear on how g_obs was made, all quoted exactly:

| Line | Quote | Bears on |
|---|---|---|
| 263 | "Thus, for the remainder of the paper we evaluate it at the radii of the observed data and present them in the form of data points rather than continuous models." | the NP method is given as points at the data radii |
| 342 | "Therefore, we restrict specifically to the radii corresponding to the existing spectral and SZ data points to avoid extrapolating." | same |
| 366 | "the results obtained with the NP method are used as a benchmark of the local gravitational field because the method is fully data driven" | NP as benchmark |
| 445 | "The solid colored curves show the result of the Einasto fit to the baryons+DM model, whereas the individual data points indicate the accelerations computed using the nonparametric log-normal mixture model (NP)." | in the RAR figure, points = NP, curves = Einasto |
| 458 | "For the observed acceleration we consider both the nonparametric reconstruction and the results of the Einasto fit to the DM component only." | both methods used for g_obs |
| 486 | "We fitted the nonparametric points on the $g_{\rm obs}-g_{\rm bar}$ plane" | the relation fit uses NP points |

None of these says the released GOBS is a parametric curve. l. 445 and l. 263 associate *points at data radii* with NP and *curves* with Einasto. The released files hold 19–27 rows per cluster, not a model grid; that is consistent with points at the data radii, but it is an observation, not a statement, and it is not used for the criterion.

## 3. Not used

Part A's A3 Einasto diagnostic (GOBS against the Einasto file's MASS) is a computation, not a statement. Rule 3's criterion is statement-based, so it does not enter.

## 4. Result for conversion

`model_dependence` = `none` on all 109 rows. Paper II (arXiv 2205.01123v1) fits Einasto to the total mass only and releases no g_obs (`einasto.tex` l. 263: "in this paper we fitted an Einasto profile to the total gravitational field"); it makes no statement about the released column either.
