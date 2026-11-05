# Reader B notes: aeg-d-gc-baumgardt_v1

## What the method says
The methods page gives only the title line for "Baumgardt GCs" (no formulas). The formulas are in `method/REPRODUCTION.md` (inputs table):
- g_obs = 3 σ² / r½, with σ the light-weighted line-of-sight dispersion from `aeg.dispersion.light_weighted_dispersion` ("as frozen"), King (1966) light weights from the McLaughlin & van der Marel (2005) King fit (W0, r0), edges inferred from mean radii, coverage ≥ 0.80.
- g_bar = G (½ L_V Υ_V) / r½², r½ = 4/3 R_h, R_h = MvdM King-fit `Rh` rescaled from their `Dist` to Harris R_Sun.
- L_V from Harris M_V,t with the solar absolute V magnitude adopted by MvdM (2005).
- Υ_V = MvdM (M/L)1 (BC03 + Chabrier disk IMF).
- G = `astropy.constants.G` (test 3).

## Status: all 10 rows "method incomplete" (g_obs missing; g_bar computed)
g_obs not computed. The packet contains no formula or algorithm for the light-weighted dispersion. Missing:
1. the definition of `aeg.dispersion.light_weighted_dispersion` (for example, whether σ² or σ is weighted, and how the weights are normalised);
2. which King (1966) light quantity is the weight (projected luminosity in each annulus, presumably, but not written down);
3. how bin edges are "inferred from the mean radii" (midpoints? what inner and outer edge?);
4. how "coverage" is computed, and whether it changes σ or only gates plotting.

Only the RV dataset has line-of-sight bins for these 10 clusters, which matches the locators, so choosing among datasets is not an issue here. All RV bins (<r>, N_Star, σ, Δσ_Up, Δσ_Low) are transcribed in inputs.csv. The King parameters W0/gamma, r0pc and Conc are transcribed for completeness.

## g_bar inputs and constants
- M_V,sun = 4.85: read at source in McLaughlin & van der Marel (2005), arXiv e-print astro-ph/0605132, file `mclaughlin_vandermarel.tex`, line 2161 ("solar absolute magnitude $M_{V,\odot}=+4.85$"). Downloaded from https://arxiv.org/e-print/astro-ph/0605132. The tarball's SHA-256 is af94cbcf14303090df2ab51ddd864235731d3378d9ba309638da8edf4a431b96. The arXiv ID was found by a web search for the paper title, not for any converted values.
- G is from astropy 8.0.2, as the method states. M_sun (kg) and pc (m) are not stated in the method. I took them from the same astropy (`constants.M_sun` and `units.pc`), because the method uses astropy for G and the result has to be in m s⁻². This is a minor gap: the method names neither conversion.
- L_V = 10^(−0.4 (M_V,t − 4.85)) L_sun.
- Every cluster has exactly one MvdM `Mod = K` row and one `clusters` row, so the Harris-only fallback was not needed. Pal 5 (MW-PAL5) has a King fit. The descriptor reports that Pal 5 failed test 2 (D-046). That failure does not change the g_bar recipe.

## Unsure / caveats
- Harris Part II columns were split on whitespace after the 12-character ID field. M_V,t is the 7th field ([Fe/H], wt, E(B−V), V_HB, (m−M)V, V_t, M_V,t). I checked this against the header line for every cluster used.
- The veldis.html locators give the HTML line where each bin's first value cell appears.
- The MvdM `Conc` for NGC 6496 is printed as 0.00, and W0 as 0.30. I transcribed them as printed. They are not used in g_bar.
