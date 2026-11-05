# Reader A notes: aeg-d-gc-baumgardt_v1

## What the written method gives
From `method/REPRODUCTION.md` (inputs table, D-025):
- g_obs = 3 σ² / r½
- g_bar = G (½ L_V Υ_V) / r½², no gas
- r½ = 4/3 R_h; R_h = McLaughlin & van der Marel (2005) King-fit `Rh` (log pc), rescaled from their `Dist` to the Harris (2010) R_Sun
- L_V from Harris M_V,t with the solar absolute V magnitude adopted by McLaughlin & van der Marel (2005)
- Υ_V = McLaughlin & van der Marel (2005) (M/L)₁ (BC03 + Chabrier disk IMF)
- G = `astropy.constants.G` (named in test 3)

## Status: all 10 rows "method incomplete" (g_obs missing; g_bar computed)

### g_obs: method incomplete
The global σ is defined only as "`aeg.dispersion.light_weighted_dispersion`, as frozen", with "King (1966) light weights" from `aeg.king66`. Neither function's code or formula is in the packet. These steps are not specified:
1. The weighting formula: whether σ² or σ is weighted, and by what light (light in each annulus? per bin? projected or 3D King profile?).
2. How bin edges are "inferred from the mean radii" (midpoints, geometric means, the treatment of the innermost and outermost edges).
3. How "light coverage" is defined (the fraction of total projected light between the outer edges?), and what is done with light outside the covered radii (renormalise or extrapolate).
4. How the King (1966) model is evaluated: numerical integration details, and whether the projected surface brightness profile or the 3D profile is used.

The rows' locators say "(RV)", so I took the RV line-of-sight bins as the dataset candidate. I read and recorded every RV bin for each cluster in `inputs.csv` (radius, NStar, σ, ΔσUp, ΔσLow), but did not compute a σ from them. Any weighting I chose would be a guess.

### g_bar: computed; the constants M_sun and pc are not stated
- The method names only `astropy.constants.G`. Converting L_V Υ_V (in solar units) to kg needs M_sun, and converting pc to m needs a parsec length. The method states neither, so I took both from the same library (astropy 8.0.2: `astropy.units.M_sun`, which is `constants.M_sun`, and `astropy.units.pc`). Strictly, this is a second item where the method is incomplete. A hand check with G = 6.6743e-11, pc = 3.0856775814913673e16 m and M_sun = 1.98840987e30 kg reproduces the NGC 6496 value to every printed digit.
- M_V,sun is not printed in the packet's sources. Following the brief, I downloaded the arXiv e-print of McLaughlin & van der Marel (2005):
  - URL: https://arxiv.org/e-print/astro-ph/0605132
  - SHA-256: af94cbcf14303090df2ab51ddd864235731d3378d9ba309638da8edf4a431b96
  - `mclaughlin_vandermarel.tex` line 2161 reads: "solar absolute magnitude $M_{V,\odot}=+4.85$". The same value appears at lines 2173 and 3806 (V_tot = 4.85 − 2.5 log L_tot).
  - Note: I first tried astro-ph/0507570, which is a different paper (quasar absorbers). I did not use it.
- L_V = 10^(−0.4 (M_V,t − 4.85)), with M_V,t from Harris Part II, column 8.
- All 10 clusters have exactly one row with `Mod = K` in the McLaughlin & van der Marel `models` table, so the "otherwise Harris r_h" fallback was never used.

## Locators
- In `mwgc.dat`, the locators are file line numbers, counted from 1.
- In the VOTables, the locator is `recno`. I checked that it equals the TR order for the rows used.
- In `veldis.html`, the locator is the file line of the bin's `<r>` cell. Bins are numbered within the RV dataset only, so proper-motion bins (VB21, LI22, etc.) are skipped in the numbering.

## Other observations (not used)
- My veldis parser finds 155 cluster names, but the page says 156 clusters. This does not affect the 10 target clusters: I checked their bin lists against the raw HTML for NGC 6496, Pal 5 and NGC 6366.
- Pal 5 has only 2 RV bins. That meets the "≥ 2 bins" selection rule, but light coverage with 2 bins is not checkable without the coverage definition.
- For NGC 6496, the King fit has W0 = 0.30 with a large upper error (E_W0 = 4.30) and Conc = 0.00. It is a poorly constrained fit. This affects the light weights for g_obs only.

## Code
- `code/vot.py`: a raw-text VOTable reader that keeps the printed digits.
- `code/veldis.py`: the veldis.html bin parser.
- `code/compute.py`: reads the inputs and writes `values.csv` and `inputs.csv`. Run it with `python3 -I code/compute.py`.
