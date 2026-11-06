# Reader A notes: X-COP v2 audit

## Archive
- Downloaded `data_E22.tar.gz` from the given SWITCHdrive URL with `curl -sL`. It is 161298 bytes, and its SHA-256 `ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d` matches the brief, so I continued.
- Members used: `A644/`, `A1795/`, `A2029/`, `A2319/` `gbar_gobs_<cluster>.fits`. The tar records them as dated 2023-04-20, which is after the paper's v1 (2022-05). The SHA-256 of each member file is in `return.csv`.
- Each file has one BINTABLE HDU with 6 float32 ('E') columns. The header gives every TTYPE and TUNIT:
  `RADIUS [kpc]`, `GBAR [m/s^2]`, `GBAR_ERR [m/s^2]`, `GOBS [m/s^2]`, `GOBS_ERR_LO [m/s^2]`, `GOBS_ERR_HI [m/s^2]`.
  The header has no other keywords: no COMMENT, HISTORY, TDISP or TNULL.
- **No unit conversion was applied.** The header units are already kpc and m s^-2.

## Row numbering: 1-based
- The FITS binary-table convention numbers rows from 1.
- The data settle it. `gbar_gobs_A2319.fits` has NAXIS2 = 27, and the packet asks for A2319 "row 27". That row exists only if counting starts at 1, so I applied 1-based numbering to all 10 rows. Under 0-based counting, row 27 would be out of range.

## Column meanings: lines quoted from the paper
The paper is the arXiv e-print source `hydromass.tex` for 2205.01110v1, subsection "The galaxy cluster radial acceleration relation" (`\label{sec:rar}`):
- "The availability of precise measurements of the gas, stellar, and DM mass components allows us to study the relation between the total, observed gravitational acceleration $g_{\rm obs}$ and the acceleration that would be expected in the absence of DM from the sum of the detected baryonic components, $g_{\rm bar}$."
- "The baryonic and observed acceleration were computed locally from the reconstructed profiles,
  g_{\rm obs}(r) = \frac{GM_{\rm HSE}(<r)}{r^2},
  g_{\rm bar}(r)=\frac{G(M_{\rm gas}(<r) + M_{\rm \star,BCG}(<r)+M_{\rm \star,sat}(<r))}{r^2}."
- From the Fig. `fig:rar` caption: "the individual data points indicate the accelerations computed using the nonparametric log-normal mixture model (NP)."

How I map columns to these lines:
- GOBS = g_obs(r).
- GBAR = g_bar(r).
- RADIUS = r, the radius of the enclosed-mass sphere (3D, spherical) in those equations.

## What is not stated (and what I did about it)
- **Error-column definition.** Neither the file header nor the paper says what GBAR_ERR, GOBS_ERR_LO or GOBS_ERR_HI represent: 1σ, a 68% interval, or statistical only versus including systematics. The paper never describes this file. I record the definition as "not stated".
- **Uncertainty or bound.** The data settle this, not a guess. In all 5 files, every GOBS_ERR_LO and every GOBS_ERR_HI is smaller than GOBS, at most 38% of it. A bound would be a value near GOBS, so these columns hold ± sizes (a lower-side and an upper-side uncertainty). GBAR_ERR is at most about 9% of GBAR, so it is also a single symmetric ± size.
- **I filled the error fields in compare.csv.** Their unit is given in the header and their kind (± size) is established from the data. Only the confidence level is not stated.
  - Flag for the comparator: if the audit rule treats the missing confidence level as "meaning not stated", these 6 fields per row would be blank instead.
- **The file has one symmetric g_bar error.** I put GBAR_ERR in both `g_bar_err_lo` and `g_bar_err_hi`.
- **Which g_obs reconstruction the file holds.** The paper shows both the nonparametric (NP) and the Einasto-fit g_obs. The file header does not say which one GOBS is. The figure caption says the plotted points are NP, but nothing ties this file to those points.
  - I recorded this as "not stated". It does not affect the values read.

## Precision
- The stored values are big-endian float32.
- `compare.csv` and `return.csv` `*_value` hold `repr(float(v))`, the exact float32 value expanded losslessly to double.
- `return.csv` `*_stored_float32` holds the shortest float32 repr.

## Checks
- `code/rawcheck.py` re-reads every value by parsing the FITS bytes directly with `struct`, with no astropy. All 70 compare fields matched exactly.

## Isolation
I worked only in this folder. I did not open the atlas repo, other readers, audit_v2, the scratchpad, the site or the GitHub repo. I used no other copy of the dataset.
