# Reader A — stratum aeg-d-dwarfs_v1 — notes

Read only: my packet (`packets/aeg-d-dwarfs_v1/`) and arXiv e-prints downloaded from arxiv.org.
Not opened: any other reader or provenance folder, the atlas repositories or worktrees, the website.

## Result

All 10 rows: `method incomplete`. `g_obs` and `g_bar` are left empty in `values.csv`.

## Why every row is incomplete

The written method (`methods_page.txt`, `REPRODUCTION.md`, `descriptor.json`, `D048_KIND_BASIS.md`) gives
g_obs = 3σ²/r½ and g_bar = G(½ L_V Υ_V + M_gas)/r½², with σ in km s⁻¹, radii in pc or kpc and masses in M☉. It states:
- no value for **G**;
- no value for the **parsec (or kpc) in metres**. g_obs needs it as well, so g_obs is incomplete too;
- no value for the **solar mass in kg** (or GM☉).

The method does state, or say where to read: the helium factor (1.33), M_V,☉ ("read at source" from the Υ_V source: McLaughlin & van der Marel 2005, p.22, M_V,☉ = +4.85), and the 4/3 projection factor.

### Other gaps, by row (they would matter even if the constants were supplied)

1. **[Fe/H] for Υ_V.** The descriptor says the metallicity comes from the "spectroscopic original (D-057) or the dispersion paper (D-059)". D-057 and D-059 are not in the packet, and no locator names a metallicity source.
   - The dispersion paper gives a system [Fe/H] for:
     - And XII and And XXIII: Collins 2013 Table 4, −2.2;
     - Draco II: Cerny 2026 Table 4. Three columns are printed: model −2.94, weighted average −2.74, brightest star −2.49. The method does not say which to use. All three are below the lowest tabulated value (−2.29), so Υ_V is the floor value either way;
     - Leo I: Koch 2007. Two scales are printed: CG97 −1.31 and ZW84 −1.61. The method does not say which to use.
   - The dispersion paper gives no system [Fe/H] for:
     - And III, IX, XV and XVI (Tollerud 2012);
     - CVn II: Geha 2026 prints per-star values only;
     - Tucana: Gregory 2019 quotes only literature values.
   - For those rows, the "spectroscopic original" can be found only through the LVDB index (Kirby 2020, Wojno 2020). Those papers are not in the packet, and neither the method nor any locator names them, so I did not download them. And XVI has only a photometric value in LVDB.
   - Impact: Υ_V over the tabulated range is 1.867 to 1.946, a spread of at most about 4%.
2. **Tucana R_h.** Saviane 1996 Table 5 gives **Re = 205 pc as an "effective geometric radius"** (p.10). Its profile is plotted against geometric radius, so Re is already circularised. The method's rule R_h = a√(1−ε) assumes a semi-major axis a. Applying it to Re circularises twice, which lowers R_h by a factor of √0.52 = 0.72 and changes g_obs by a factor of 1.39 and g_bar by a factor of 1.92. The method, and the "D-053; D-058 rescaling" in the locator (the decisions themselves are not in the packet), do not say what to do. This is the largest single issue I found.
3. **Tucana σ.** Gregory 2019 adopts 14.4 (+2.8 −2.3) km s⁻¹ after removing one probable member. With all 37 members it is 16.6 (+3.1 −2.6). The method's rule "whole sample (2B)" (D-038 is not supplied) could mean either. I used 14.4, the paper's adopted value.
   - **Packet inconsistency:** `method/documents_index.csv` lists **Taibi 2020** (in the packet) as the σ source for tucana_1, but `rows.csv` names **Gregory 2019** (not in the packet). Taibi 2020 Table 1 gives σ_v = 6.2 (+1.6 −1.3) km s⁻¹. That changes g_obs by a factor of (14.4/6.2)² ≈ 5.4. I followed the locator.
4. **And XII σ.** Collins 2013 prints 0.0 (+4.0) km s⁻¹, "unresolved … the upper bound represents the formal 1σ uncertainty" (p.40). It is not explicitly called an upper limit. I computed at 4.0 and marked it `limit`. This is the level at which the source states the bound.
5. **Draco II σ** < 2.6 km s⁻¹ (95% credible level, Cerny 2026 Table 3 note): `limit`.
6. **Gas.** Putman 2021 gives 5σ upper limits for all 10 systems, so gas is "absent (measured limit)" and I took M_gas = 0 in g_bar. The method's wording ("absent") implies zero but does not state it.
7. **CVn II and Leo I ellipticity.** The locator names only the column r_e,s of Muñoz 2018 Table 5. I took ε_s from the same row. Geha 2026 σ for CVn II uses stars inside 2 R_eff (MRT note 4), so it is an aperture value.
8. **And XVI distance.** The locator gives Martínez-Vázquez 2017 Table 8, row And XVI, but no column. Table 8 has seven methods. I used PWR, 23.70, because the paper calls the PWR distances its adopted ones (p.17). Recorded only: LVDB gives 23.57 with this reference, a value I could not find in Table 8. It equals Savino 2022's value.
9. **Leo I distance.** The locator says "midpoint of two printed values". I took the two Stetson 2014 μ0 values, 22.06 and 22.25, which gives 22.155.
10. **Angle-to-length conversion.** The method does not say. I used the small-angle relation, a[pc] = a[rad] · D[pc]; the difference from tan is under 10⁻⁶.

## Other observations (recorded, not used)

- LVDB `ref_vlos` for And XXIII is Pickett 2025 (σ 6.8), while the locator uses Collins 2013 (7.1).
- LVDB structure for CVn II and Leo I is the exponential fit (1.52′, 0.4; 3.65′, 0.3); the locator uses the Sérsic r_e,s (1.51′, 0.46; 3.30′, 0.30).
- Saviane 1996: M_V −9.55 in Table 5 versus "−9.6" in the text, p.10. I used the Table 5 value.
- Saviane's distance modulus is written as (m − M)0 in the abstract (p.1) and as (m − M) in §4 (p.7). Both give 24.69.
- MvdM05 duplicate [Fe/H] entries among Milky Way GCs carry identical (M/L)₁, so the interpolation is well defined. All 148 MW rows have logAge 10.11. I read the values as printed strings from the VOTable TABLEDATA.

## Supplementary values (outside the method; for the coordinator only)

`values_declared_constants.csv` gives g_obs and g_bar computed with constants I **declared**, not taken from the method:
- G = 6.67430e−11 (CODATA 2018);
- pc = 3.0856775814913673e16 m (IAU 2015);
- M☉ = 1.988409870698051e30 kg.

It uses the [Fe/H] choices listed there; several are LVDB index values, marked `Fe_H_within_method = False`. It also gives an alternative without the √(1−ε) circularisation, which is relevant for Tucana. These numbers are not part of `values.csv`.

## Downloads (arXiv e-prints, arxiv.org only; in `downloads/`)

| Paper | URL | SHA-256 |
|---|---|---|
| Koch et al. 2007, ApJ 657, 241 (Leo I σ) | https://arxiv.org/pdf/astro-ph/0611372 | 6fdfb5b5fcb066c885aba77624e5cbc3327d58baca67cf7dbd75c61000fa5a3c |
| Gregory et al. 2019 (Tucana σ), v2 | https://arxiv.org/pdf/1902.07228 | 30a451f8ae8804c37f7d7a94e3c9de9c2ecf64fc116351ba53a8164c332422ac |
| Saviane et al. 1996, A&A (Tucana structure, M_V, TRGB) | https://arxiv.org/pdf/astro-ph/9601165 | a00ce53f0564da44f12c5819ec2913e6f081d3f82424df4647abf4c0acf7d528 |
| Bernard et al. 2009, ApJ 699, 1742 (Tucana RR Lyrae distance) | https://arxiv.org/pdf/0904.4463 | 48354807f724ccdb427831829b2f74a8fea63d6f577c1f271346981f86a600d2 |
| McLaughlin & van der Marel 2005, ApJS 161, 304 (M_V,☉) | https://arxiv.org/pdf/astro-ph/0605132 | 8605aae32a4f021f1213f735c3f7f5e84bcae496f3ea49234e1e2e1c00920d22 |

I found the arXiv identifiers with the arxiv.org search page; export.arxiv.org was blocked by the proxy. I checked the packet PDFs against `documents_index.csv` (SHA-256): all 14 match.

## Code

- `code/upsilon_v.py`: Υ_V interpolation from the MvdM05 VOTable.
- `code/inputs_table.py`: the inputs as read, with locators; writes `inputs.csv`.
- `code/compute.py`: writes `values.csv` and `values_declared_constants.csv`.

Run with `python3 -I code/inputs_table.py > inputs.csv` and then `python3 -I code/compute.py`.
