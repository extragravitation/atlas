# Reader A — aeg-d-sparc_v1 — notes

## What I read
- Packet method: `method/methods_page.txt`, `method/SOURCE.md`, `method/sources.json`.
- Source: `sources/MassModels_Lelli2016c.mrt` (SHA-256 9108994b…3244c, matches sources.json).
  `SPARC_Lelli2016c.mrt` hash also matches; not needed by the written g_obs/g_bar method.
- No arXiv download was made. Nothing outside the packet was opened.

## Reading the inputs
- Columns parsed by the byte ranges in the file's own byte-by-byte description
  (R bytes 20-25 kpc; Vobs 27-32, Vgas 40-45, Vdisk 47-52, Vbul 54-59, km/s).
- "data row N" taken as the N-th data line after the last dashed separator (file line 25),
  i.e. file line N+25. The file has 3,391 data rows. For all 170 rows the galaxy ID at that
  data row equals `system_name` in rows.csv, which confirms the reading of the locator.
  No "[value redacted]" placeholders appear in this packet's rows.csv.
- Values copied exactly as printed (e.g. `238.00`, `-1.58`).

## Method as applied
- g_obs = Vobs^2 / R; g_bar = (|Vgas|Vgas + Ups_disk|Vdisk|Vdisk + Ups_bul|Vbul|Vbul) / R,
  Ups_disk = 0.50, Ups_bul = 0.70 (stated defaults). Helium factor 1.33 already in Vgas per
  the method and the file header, so not applied again.
- 13 of the 170 rows have a negative component velocity (Vgas in all cases checked); the signed
  square in the stated formula handles it directly.

## Method incomplete (all 170 rows)
The method states inputs in kpc and km/s and outputs in m s^-2 but does not state the
kpc-to-metre conversion (nor which parsec definition). The brief says an unstated constant is
"method incomplete", so `values.csv` leaves g_obs and g_bar empty for every row.
km -> m (1e3) is an SI prefix, not a constant, and is not the gap.

To keep the audit usable, two supplementary files (not read by the comparison script):
- `native_values.csv`: g_obs, g_bar in (km/s)^2/kpc, computed with no unstated constant.
- `conditional_SI.csv`: the same in m s^-2 IF 1 pc = 648000/pi au, 1 au = 149597870700 m
  (IAU 2012 B2 / 2015 B2 exact definitions). This is the reader's assumption, not the method's.
Recommended fix to the method text: state the kpc-to-metre constant used (or the parsec
definition / astropy version) so readers can reproduce m s^-2 values exactly.

Spot check (m002399, UGC05253, file line 2424): g_obs = 238.00^2/0.89; g_bar recomputed by
hand from the printed components agrees with the script.
