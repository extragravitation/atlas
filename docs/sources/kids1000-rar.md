# KiDS-1000 weak-lensing RAR — source reading

Read 2026-10-28: the paper (Brouwer et al. 2021, A&A 650, A113; arXiv:2106.11677, via ar5iv) and the data release on https://kids.strw.leidenuniv.nl/sciencedata.php.

## Data release

| File | Bytes | SHA-256 |
|---|---|---|
| `brouwer2021_rar.tar` | 2 430 464 | `73adc2d4e848fa0a6a43187f7b5447e749b92eaec4a795b9902b0beaf8a78733` |

30 data files plus a README (the tarball also carries macOS `._` metadata files, to be ignored). One ESD profile per file, named by the paper figure it reproduces, each with a full covariance matrix file. Includes: the main isolated-galaxy RAR (Fig. 4-5), the same in four stellar-mass bins (Fig. 9; bin edges log10 M*/(h70⁻² M☉) = 8.5, 10.3, 10.6, 10.8, 11.0), a variant with an estimated hot-gas contribution (Fig. 4 "hotgas"), early/late-type splits by colour and Sérsic index (Fig. 8), dwarfs (Fig. 10), GAMA lenses (Fig. 4), lensing rotation curves (Fig. 3), and a non-isolated sample (Fig. A4).

**In the RAR files the first column is g_bar (m/s²), not radius.** Each row is a bin in g_bar. Other columns: ESD_t and its error (h70 M☉/pc²), the cross-component (null check), and a multiplicative bias (1+K) to divide out. The README gives the conversion: g_obs = 4 G ESD_t / bias.

README contact for questions: the first author (address given in the README).

## How g_obs is obtained (paper §2.2, App. B, §4.4)

- **Default (used throughout the paper):** each ESD value is converted assuming the enclosed profile is locally a singular isothermal sphere (ρ ∝ r⁻²), giving g_obs = 4 G ΔΣ. The paper frames the r⁻² form in both interpretive contexts.
- **Check:** a piece-wise power-law deprojection that assumes only spherical symmetry (App. B), compared with the SIS conversion on simulated lensing maps (§4.4).
- For the Atlas this is a named assumption ("lensing deprojection: SIS, validated against a shape-free method by the authors"), shown on every KiDS point.

## How g_bar is obtained (paper §3.3, §4.3)

- Lenses treated as **point masses** M_gal at R > 30 h70⁻¹ kpc, with M_gal = stars + cold gas.
- Stellar masses from 9-band photometry (LePhare; Bruzual & Charlot 2003; Chabrier IMF), **normalised to the GAMA mean**; random uncertainty adopted 0.12 dex; systematic uncertainty **±0.2 dex**, shown by the authors as a band.
- Cold gas from a scaling relation with stellar mass (Boselli et al. 2014).
- Hot gas not included in the main result; a separate released variant includes an estimate.
- Isolation criterion: no neighbour with more than 10 % of the lens stellar mass within 3 h70⁻¹ Mpc; lens M* < 10¹¹ h70⁻² M☉; 259 383 isolated lenses.

## Consequences for the Atlas

- **The package can be built from the public release alone**: g_bar is given; g_obs follows from the README formula; covariance is provided. The email to the authors becomes a courtesy notice, not a data request.
- **Stellar mass-to-light cannot be a continuous slider for KiDS**: g_bar is pre-binned over stacked galaxies, and stars and cold gas are not given separately. The honest representation is the authors' own ±0.2 dex systematic band, and the "hotgas" file as a discrete alternative baseline. Both are shown as the source's published variants, not Atlas computations.
- **No radius coordinate**: the RAR files are binned in g_bar. KiDS points appear in the observed-against-baryonic and excess views, not in the radius view, unless the lensing rotation-curve files (binned in radius) are packaged as well.
- Units carry h70; with h = 0.7 these are physical. The package records this.
