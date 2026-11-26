# Gaps

## 1. Two of the four source files are missing (affects all 10 rows: unreadable)
METHOD.md §2 and rows.json take W0 and r0 (`W0/gamma`, `r0`), Rh and Dist from VizieR J/ApJS/161/304 `models` (S7, `mvdm05/J_ApJS_161_304_models.vot`), and Upsilon_V from `clusters` column `(M/L)1` (S5, `mvdm05/J_ApJS_161_304_clusters.vot`). sources.json lists both files, but `files/` holds only `mwgc.dat` and `veldis.html`. So for every row:
- W0 and r0 are unreadable. Without them there is no King model, so I could not get the light weights (§4 steps 1 to 4), sigma (step 5) or g_obs. I also could not check whether the light coverage reaches 0.80 (§3).
- Rh and Dist are unreadable, so R_h (step 6) and r1/2 (step 7) are missing. Both g_obs and g_bar need r1/2.
- (M/L)1 is unreadable, so g_bar cannot be computed.
I left g_obs and g_bar blank for all 10 rows.

## 2. Inputs that were read, all at their locators
- veldis.html: the RV bins (<r>, NStar, sigma, Δσ Up, Δσ Low) for all 10 clusters. The bin count matches the number of sigma_los inputs in rows.json for each row. Each of these clusters has RV as its only line-of-sight Type, so the default profile is RV whatever the coverage turns out to be.
- mwgc.dat: Part I R_Sun and Part II M_V,t for all 10 clusters. Each value was read by the character positions of its column label in the header line.

## 3. Points that are not gaps
- Ter 7 and IC 4499 have exactly two RV bins. The edge rule in §4 step 3 handles two bins.
- NGC 6723 has a core-collapse flag `c:` in Harris Part III. That matters only for the §6 path, which applies to clusters without a McLaughlin & van der Marel fit, and does not touch these rows.
