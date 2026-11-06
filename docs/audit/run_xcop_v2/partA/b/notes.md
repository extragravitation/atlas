# Reader B notes: X-COP v2 audit

## Archive check
- Downloaded `data_E22.tar.gz` from the given URL into `dl/`. SHA-256 `ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d` (matches), 161298 bytes (matches).
- Paper source: arXiv e-print 2205.01110v1, file `hydromass.tex`, extracted to `paper/x/`.

## File structure (all four files read)
Each `gbar_gobs_<cluster>.fits` has one BINTABLE (HDU 1), six float32 (`TFORM = 'E'`) columns:

| TTYPE | TUNIT |
|---|---|
| RADIUS | kpc |
| GBAR | m/s^2 |
| GBAR_ERR | m/s^2 |
| GOBS | m/s^2 |
| GOBS_ERR_LO | m/s^2 |
| GOBS_ERR_HI | m/s^2 |

Row counts: A644 19, A2319 27, A2029 22, A1795 21. No header comments or keywords describe the columns beyond TTYPE/TUNIT.

Units are already kpc and m s^-2, so no conversion was used. The values are float32 in the file. `compare.csv` gives `repr(float(value))`, which is the exact float32 value widened to float64.

## Row numbering: 1-based
I take "row N" as 1-based, so row N is `data[N-1]`. Reasons:
1. The locators settle it. `A2319/gbar_gobs_A2319.fits:row 27` exists only under 1-based counting, because the table has `NAXIS2 = 27` rows (0-based indices run 0–26).
2. The FITS standard numbers table rows from 1.

The paper says nothing about row numbering.

## Column meanings: quotes from the paper (hydromass.tex)
- g_obs and g_bar (lines 451–456): "The baryonic and observed acceleration were computed locally from the reconstructed profiles, $g_{\rm obs}(r) = \frac{GM_{\rm HSE}(<r)}{r^2}$, $g_{\rm bar}(r)=\frac{G(M_{\rm gas}(<r) + M_{\rm \star,BCG}(<r)+M_{\rm \star,sat}(<r))}{r^2}$."
- Concepts (line 449): "the relation between the total, observed gravitational acceleration $g_{\rm obs}$ and the acceleration that would be expected in the absence of DM from the sum of the detected baryonic components, $g_{\rm bar}$." (This is the paper's wording, quoted.)
- Unit (line 465): "with $g_{\dagger}=1.2\times10^{-10}$ m s$^{-2}$". The paper works in m s^-2, which agrees with the TUNIT.
- Which reconstruction (line 458): "For the observed acceleration we consider both the nonparametric reconstruction and the results of the Einasto fit to the DM component only." The Fig. caption (line 445) says "the individual data points indicate the accelerations computed using the nonparametric log-normal mixture model (NP)."

## Not stated
- **Which reconstruction feeds GOBS** (nonparametric or Einasto): not stated. The file is not linked to either in the paper. Point data suggest NP from the Fig. caption, but I did not use that.
- **What the error columns mean** (GBAR_ERR, GOBS_ERR_LO, GOBS_ERR_HI): neither the paper nor the file describes them. Their confidence level (1σ, 68 %, etc.) is not stated.
- **Size or bound** for the error columns: not stated. The values show that GOBS_ERR_LO and GOBS_ERR_HI are ± sizes, not bounds: in every row of all four files GOBS_ERR_HI < GOBS, which is impossible for an upper bound, and ERR_LO is of similar size to ERR_HI. This is an inference from the data and is labelled as one. GBAR_ERR is one unsigned column; I read it as a symmetric ± size. In compare.csv I copied it into both g_bar_err_lo and g_bar_err_hi, and that copying is my own choice.
- **RADIUS**: the file and paper do not say whether it is a 3D radius (the r in the equations) or a projected radius, or which cosmology turned it into kpc. The unit kpc is stated in the header.
- **Archive provenance**: the archive members are dated 2023-04-20, after the paper (May 2022). The paper does not describe these files or give this URL. The only data link in the paper is to the X-COP site (line 70 footnote). So the paper can confirm what the quantities are, but not that these exact files are its products.

## Status
All 10 rows are `ok`. I kept the numeric error fields in compare.csv because the header gives their name and unit; only their confidence level and the size-or-bound question are not stated.
