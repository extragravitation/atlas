# Reader B notes: aeg-d-sparc_v1

## Source and indexing
- Only file used: packet `sources/MassModels_Lelli2016c.mrt` (SHA-256 checked in code against sources.json: 9108994b...244c). No downloads; no other copy consulted. `SPARC_Lelli2016c.mrt` was not needed (the written method uses only R, Vobs, Vgas, Vdisk, Vbul).
- "data row N" taken as the N-th line after the fourth dashed separator (first data row = file line 26; 3391 data rows). Fields parsed by the byte ranges in the file's own byte-by-byte description. All 170 system names in rows.csv match the ID column at the indexed row, which confirms the indexing.
- No rows had R <= 0 or g_bar <= 0. No "[value redacted]" locators occurred.

## Method as applied
- g_obs = Vobs^2 / R; g_bar = (|Vgas|Vgas + 0.5 |Vdisk|Vdisk + 0.7 |Vbul|Vbul) / R (SOURCE.md "Method", Upsilon defaults stated there and on the methods page).
- Vgas taken as printed (already includes the 1.33 helium factor per file Note 2); negative Vgas values handled by the |V|V form.

## Incomplete step (all 170 rows)
- The method says outputs are in m s^-2 and radii in kpc, and the file gives V in km/s, but the method states no conversion constant for kpc -> m (nor km -> m). Per the brief, an unstated constant is "method incomplete", so every row has that status.
- Because the missing item is a unit definition rather than an empirical constant, values were still computed (and filled in) using exact definitions: 1 km = 1000 m; 1 au = 149597870700 m (IAU 2012 B2); 1 pc = 648000/pi au (IAU 2015 B2); 1 kpc = 1000 pc = 3.0856775814913673e19 m. If the comparison should treat these as ok, the numbers are there; a different kpc value (e.g. a rounded 3.086e19) would shift every g by the same ratio.
- Values written to 7 significant figures.

## Not checked
- The reproduction reference (RAR.mrt) and REPRODUCTION.md are listed in sources.json but are not in the packet; not used.
