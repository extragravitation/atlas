# SPARC — source reading

Read 2026-10-28 from the maintainers' site, https://astroweb.case.edu/SPARC/ (page last updated 29 May 2020).

## Files

| File | Bytes | SHA-256 |
|---|---|---|
| `MassModels_Lelli2016c.mrt` (Table 2, mass models) | 269 518 | `9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c` |
| `SPARC_Lelli2016c.mrt` (Table 1, galaxy sample) | 28 259 | `5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243` |

The CDS/VizieR copy (J/AJ/152/157) could not be reached from this environment on this date; its ReadMe and record licence remain to be read (backlog D1, partly open).

## Mass-model table (Table 2)

3 391 rows; 175 galaxies; radii 0.08–108.31 kpc. Columns, as documented in the file header:

| Column | Unit | Meaning |
|---|---|---|
| ID | — | Galaxy identifier |
| D | Mpc | Assumed distance |
| R | kpc | Galactocentric radius |
| Vobs | km/s | Observed circular velocity |
| e_Vobs | km/s | Uncertainty in Vobs: random error from non-circular motions and/or kinematic asymmetries; **excludes** systematic uncertainty from inclination |
| Vgas | km/s | Gas contribution; **includes a factor 1.33 for helium** |
| Vdisk | km/s | Stellar disc contribution, **for M/L = 1 M☉/L☉ at 3.6 µm** |
| Vbul | km/s | Bulge contribution, same M/L convention |
| SBdisk, SBbul | L☉/pc² | Disc and bulge surface brightness |

Observed in the data:
- **Vgas is negative in 361 rows (48 galaxies).** The sign carries meaning (the gas contribution to the radial force is outward at those radii), so g_bar must be built as V|V| per component, not V². The pipeline must test this explicitly.
- Bulge present (Vbul > 0) in 32 galaxies.

## Galaxy table (Table 1)

Per galaxy: Hubble type, distance D with error e_D and **distance method** f_D (1 Hubble flow with H0 = 73 km/s/Mpc and Virgo-infall correction; 2 tip of the red giant branch; 3 Cepheids; 4 Ursa Major cluster; 5 supernovae), inclination with error, 3.6 µm luminosity with error, disc scale length, HI mass and radius, Vflat, **quality flag Q (1 high, 2 medium, 3 low)**, and references for the HI/Hα data.

## Consequences for the Atlas

- g_obs = Vobs²/R and g_bar = (Υ_disk Vdisk|Vdisk| + Υ_bul Vbul|Vbul| + Vgas|Vgas|)/R. The stellar mass-to-light ratios Υ are **not** in the table (the table uses Υ = 1). The default Υ values must be read at source in the SPARC paper before use; they are not stated here from memory.
- Distance and inclination errors are per galaxy (Table 1), so the distance slider can use published per-galaxy errors rather than a global factor.
- The quality flag is the source's own label; the Atlas shows it as a property and never uses it to hide data by default.
- Licence: the site states none; it asks that the master paper be cited, and the original rotation-curve sources where relevant (D-004: archival terms apply; record when the CDS ReadMe is read).
