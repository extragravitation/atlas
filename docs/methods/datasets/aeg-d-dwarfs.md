# Dwarf galaxies (aeg-d-dwarfs/v3): how each row is computed

This text is meant to be complete for every row of `tables/measurements.ecsv`. Its arithmetic, and the selection rules where the tables allow, are checked against every published row by `pipeline/tests/test_methods_text.py`. Whether a reader who does not know the code can follow it is tested only by the independent audit (D-116). A reader with the source files, the locators (`locators.json`), the per-system input table at the end of this page and this text should be able to recompute g_obs and g_bar without the Atlas code. The code is:
- `v1/reproduction/inputs.py`, with `gas.py` and `upsilon.py`, which assembles the inputs;
- `pipeline/aeg/ml_interp.py`, the interpolation;
- `v1/convert.py`, which computes the accelerations;
- `v2/convert.py`, which makes the two v2 changes.

Where this text and the code differ, the error is in this text; please report it.

## 1. Constants and units

| Quantity | Value | Source |
|---|---|---|
| G | 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻² | CODATA 2018 (stated in code) |
| M☉ | 1.98840987 × 10³⁰ kg | IAU 2015 nominal (stated in code) |
| 1 pc | 3.0856775814913673 × 10¹⁶ m | IAU 2015 B2 (stated in code) |
| M_V,☉ | +4.85 mag | as adopted by McLaughlin & van der Marel 2005 §4, the source of Υ_V |
| Helium factor | 1.33 | `data/assumptions.json` `helium_factor` (Lelli et al. 2016) |
| Distance from a modulus μ | D = 10^(μ/5 + 1) pc | |
| Modulus from a distance | μ = 5 log₁₀(D / 10 pc) | |
| Angle to length | R [pc] = (R [arcmin] / 60) × (π / 180) × D [pc] | |

## 2. Inputs per system

Each input is read from the paper and place in the per-system table (§7). The locators give the page, table, row and column.

| Input | Unit | Use |
|---|---|---|
| σ, the global line-of-sight velocity dispersion, or its upper limit | km s⁻¹ | g_obs |
| r_h, the half-light radius, and the ellipticity ε = 1 − b/a | arcmin, dimensionless | r½ |
| Distance, printed as a modulus (m − M)₀ or in kpc | mag or kpc | r½ and L_V |
| m_V,0, the extinction-corrected apparent magnitude; or M_V with the modulus the paper used | mag | L_V |
| [Fe/H] | dex | Υ_V |
| H I mass from Putman et al. 2021 Table 1, from the galaxy's row: columns `l_MHI`, `MHI` and `Dist` | M☉, kpc | gas |
| The model table for Υ_V: VizieR J/ApJS/161/304 `clusters`, Milky Way rows | | Υ_V |

## 3. Steps

1. **σ.**
   - The value as printed. Where the paper prints the same σ at two precisions, the more precise printing is used; the locator names it.
   - **An upper limit is used at its stated value,** and the row's g_obs is an upper limit (`limit = upper`).
   - **A best value of 0 with no stated limit** becomes an upper limit equal to 0 plus the printed upper error (D-062).
2. **Circularised radius.**
   - If r_h is measured along the major axis, R_h = r_h √(1 − ε). If the paper prints it already circularised (for example an "effective geometric radius"), R_h = r_h.
   - **No axis stated:** where the paper does not say which axis r_h is measured along, it is taken as semi-major (D-052 item 2).
   - **Convention per system:** the per-system table (§7) gives which case applies.
   - **Units:** a radius printed in arcsec is divided by 60.
   - **An ellipticity printed only as an upper limit** is not used. Where the radius is already circularised (Reticulum III), none is needed. Where the paper also prints a circularised radius (Pegasus IV), that radius is used, as the table says.
3. **Distance.**
   - **The package distance D** is the one in the per-system table, read as the table says: as the distance modulus, or as the distance in kpc. Where a paper prints both, the one named is used. A modulus is turned into kpc by §1.
   - **A range** printed for the distance (Leo I, Stetson 2014) is used at its midpoint.
4. **Luminosity:** L_V = 10^(−0.4 (m_V,0 − μ − 4.85)) L☉, with μ the modulus of the package distance D. Where m_V,0 is not printed, it is rebuilt by the route the per-system table gives:
   - **"M_V + (m − M) used by the paper":** m_V,0 = M_V + the paper's own modulus;
   - **Munoz 2018 systems:** m_V,0 = M_V (Table 6) + 5 log₁₀(D_T1 / 10 pc), where D_T1 is the system's distance in Table 1 of the same paper (D-061 item 3);
   - **Andromeda VI and VII:** M_V from McConnachie 2006, with the moduli of McConnachie 2005;
   - **Phoenix:** M_V from van de Rydt et al. 1991 p. 136, with that paper's adopted modulus, p. 134 (D-061 item 5);
   - **Leo T:** M_V from de Jong 2008, with that paper's modulus (D-061 item 6);
   - **Tucana V:** M_V from Simon 2020, with that paper's distance (D-061 item 7);
   - **Tucana:** M_V from Saviane 1996, with its own TRGB modulus (D-053);
   - **Boötes III:** L_V = 10^(−0.4 (M_V − 4.85)) from Correnti 2009's M_V. It is distance-independent (D-061 item 2).
5. **Υ_V** (D-059, D-060):
   - **The table:** the McLaughlin & van der Marel 2005 `clusters` table, rows whose `Cluster` begins with "MW". All of these are at log age 10.11. Its `[Fe/H]` is rounded to 2 decimals and `(M/L)1` to 3 decimals.
   - **Rows:** those whose `Cluster` value begins with `MW` (written `MW-…` in the export).
   - **Interpolation:** sort by [Fe/H], keep one row per [Fe/H], and interpolate (M/L)1 linearly at the system's [Fe/H]. Rows that share an [Fe/H] have the same (M/L)1 in this table, after rounding; a duplicate with a different value would stop the conversion.
   - **Outside the table's range,** the end value is used, never extrapolated (flag `beyond_source_range`).
6. **Gas inside r½** (D-058):
   - **An upper limit in Putman Table 1** (`l_MHI = "<"`) means no gas enters g_bar: M_gas(<r½) = 0. The limit is recorded only.
   - **A system not in Putman Table 1** is treated the same way: M_gas(<r½) = 0, status "not addressed".
   - **A detection:**
     - M_HI,pkg = MHI × (D / Dist_Putman)²;
     - M_gas = 1.33 × M_HI,pkg;
     - M_gas(<r½) = ½ M_gas, because Table 1 gives totals only.
7. **Radii:**
   - R_h [pc] = R_h [arcmin] / 60 × π/180 × D [pc];
   - r½ = (4/3) R_h (Wolf et al. 2010).
8. **Accelerations,** with σ in m s⁻¹ and r½ in m:
   - **g_obs** = 3 σ² / r½;
   - **g_bar** = G × (½ L_V Υ_V + M_gas(<r½)) M☉ / r½²;
   - **g_bar_stars and g_bar_gas_cold** are the two terms.

**Rounding.** The Atlas rounds R_h (arcmin), D (kpc), L_V and M_gas to six significant figures, and m_V,0 to four decimals, before step 8. Recomputing from the printed inputs therefore agrees with the published g to about 10⁻⁴ in relative terms, about 4 × 10⁻⁵ dex.

## 4. Special cases (named in the per-system table)

- **Tucana:**
  - Saviane 1996 prints the radius R_e in pc, circularised, at its own TRGB modulus.
  - It is turned into an angle at that modulus: R_h [arcmin] = R_e / D(μ_Saviane) [pc] × (180/π) × 60.
  - It is then used at the package distance, from Bernard 2009 (D-053).
- **Boötes III:** the radius and ellipticity are those of the standard one-component Plummer fit of Moskowitz 2020, Table 3 (D-061 item 1).

## 5. The two v2 changes (D-096)

- **Phoenix II:** σ is the value Fritz et al. 2019 mark as preferred (bold) in Table 4, certain members (arXiv 1805.07350v4, l. 452; caption l. 436). The earlier value is kept as an alternative row.
- **Fornax:** the half-light radius is the Sérsic-fit value that Wang et al. 2019 state gives the best fit (Fornax_main.tex Table 1, l. 106; best-fit statement l. 333). The earlier value is kept as an alternative row.

## 6. Recorded, not plotted (D-097)

**Eight systems** are computed as above but not plotted, because their sources state they are out of equilibrium or tidally disrupted. Each row's notes and the exclusion register (`data/registry/excluded.csv`) quote the source. Their rows keep g_obs and g_bar.

## 7. Per-system inputs

For each default row:
- **the paper and place** of each input. Values are not given: read them at the place. Page numbers are those of the copy named (usually the arXiv PDF), counting the PDF's pages from 1;
- **the radius convention:** semi-major, semi-major assumed (D-052 item 2), or circularised as printed;
- **the gas case;**
- **the [Fe/H]:** which quantity, mean or median, and of which kind, as the source gives it;
- **the magnitude route:** for a route through M_V, the place of M_V and which modulus is added.

The table is generated from the package by `docs/methods/datasets/make_input_tables.py`, which removes every printed value from the location text.

<!-- INPUT TABLE -->

### Andromeda I

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Tollerud 2012 ApJ 752 45 (arXiv 1112.1067v3), p9, Table 3, row And I, column σLOS. | page: 9 · table: 3 · row: And I; And III; And V; And VII; And IX; And X; And XIV; And XV; And XVI · column: σLOS |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And I. Convention: semi-major. | page: 9 · table: 1 · row: And I |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And I'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And I' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And I). | page: 9 · table: 2 · row: And I |
| [Fe/H] | Kirby2020AJ....159...46K, p.13, Sec. 4.1, Table 4 (Chemical Properties of M31 dSphs), row And I (mean [Fe/H], spectroscopic). | page: 13 · table: 4 · row: And I; And III; And V; And VII; And X · section: 4.1 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda I"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda I") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Ho 2012 ApJ 758 124 (arXiv 1209.2116v1), p1 abstract; p7 Sec. 5.2.1 ('average dispersion, ⟨σv⟩ = [value] km s−1'). | page: 1; 7 · section: 5.2.1 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And II. Convention: semi-major. | page: 9 · table: 1 · row: And II |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And II'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And II' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And II). | page: 9 · table: 2 · row: And II |
| [Fe/H] | Wojno2020ApJ...895...78W, p.23, Sec. 7.3, Table 6 (Mass-metallicity Relation and Abundance Trends in M31 dSphs), row And II (mean [Fe/H], spectroscopic). | page: 23 · table: 6 · row: And II; And IX; And XIV; And XV · section: 7.3 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda III

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Tollerud 2012 ApJ 752 45 (arXiv 1112.1067v3), p9, Table 3, row And III, column σLOS. | page: 9 · table: 3 · row: And I; And III; And V; And VII; And IX; And X; And XIV; And XV; And XVI · column: σLOS |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And III. Convention: semi-major. | page: 9 · table: 1 · row: And III |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And III'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And III' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And III). | page: 9 · table: 2 · row: And III |
| [Fe/H] | Kirby2020AJ....159...46K, p.13, Sec. 4.1, Table 4 (Chemical Properties of M31 dSphs), row And III (mean [Fe/H], spectroscopic). | page: 13 · table: 4 · row: And I; And III; And V; And VII; And X · section: 4.1 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda III"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda III") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda IX

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Tollerud 2012 ApJ 752 45 (arXiv 1112.1067v3), p9, Table 3, row And IX, column σLOS. | page: 9 · table: 3 · row: And I; And III; And V; And VII; And IX; And X; And XIV; And XV; And XVI · column: σLOS |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And IX. Convention: semi-major. | page: 9 · table: 1 · row: And IX |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And IX'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And IX' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And IX). | page: 9 · table: 2 · row: And IX |
| [Fe/H] | Wojno2020ApJ...895...78W, p.23, Sec. 7.3, Table 6 (Mass-metallicity Relation and Abundance Trends in M31 dSphs), row And IX (mean [Fe/H], spectroscopic). | page: 23 · table: 6 · row: And II; And IX; And XIV; And XV · section: 7.3 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda IX"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda IX") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda V

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Tollerud 2012 ApJ 752 45 (arXiv 1112.1067v3), p9, Table 3, row And V, column σLOS. | page: 9 · table: 3 · row: And I; And III; And V; And VII; And IX; And X; And XIV; And XV; And XVI · column: σLOS |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And V. Convention: semi-major. | page: 9 · table: 1 · row: And V |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And V'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And V' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And V). | page: 9 · table: 2 · row: And V |
| [Fe/H] | Kirby2020AJ....159...46K, p.13, Sec. 4.1, Table 4 (Chemical Properties of M31 dSphs), row And V (mean [Fe/H], spectroscopic). | page: 13 · table: 4 · row: And I; And III; And V; And VII; And X · section: 4.1 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda V"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda V") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda VI

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.33 Table 5, p.37 Table A1 Full algorithm, p.39 Sec B.2. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | McConnachie2006MNRAS.365.1263M p. 10, Table 4 (Integrated photometry), row Andromeda VI, col r1/2 (′); no_uncertainty: no error printed. Convention: circularised. | page: 10 · table: 4 · row: Andromeda VI · column: r1/2 (′ |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And VI'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And VI' |
| m_V,0 | McConnachie 2006 M_V + McConnachie 2005 modulus. | page: 10 (McConnachie 2006); 23 and 9 (McConnachie 2005) · table: 4 (McConnachie 2006, M_V); 2 (McConnachie 2005, modulus) · section: 3.10 (McConnachie 2005) |
| [Fe/H] | Collins2013ApJ...768..172C, p.27, Table 4 (Kinematic properties of Andromeda dSph galaxies as derived within this work), row And VI (mean [Fe/H], kind not stated by the source). | page: 27; 33; 30 · table: 4; 5 · row: And VI; And XI; And XII; And XVII; And XX; And XXII; And XXIII; And XXVII; And XXX (Cass II |
| Gas | Putman et al. 2021 Table 1, row "Andromeda VI"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda VI") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda VII

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Tollerud 2012 ApJ 752 45 (arXiv 1112.1067v3), p9, Table 3, row And VII, column σLOS. | page: 9 · table: 3 · row: And I; And III; And V; And VII; And IX; And X; And XIV; And XV; And XVI · column: σLOS |
| r_h and ε | McConnachie2006MNRAS.365.1263M p. 10, Table 4 (Integrated photometry), row Andromeda VII, col r1/2 (′); no_uncertainty: no error printed. Convention: circularised. | page: 10 · table: 4 · row: Andromeda VII · column: r1/2 (′ |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And VII'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And VII' |
| m_V,0 | McConnachie 2006 M_V + McConnachie 2005 modulus. | page: 10 (McConnachie 2006); 23 and 9 (McConnachie 2005) · table: 4 (McConnachie 2006, M_V); 2 (McConnachie 2005, modulus) · section: 3.10 (McConnachie 2005) |
| [Fe/H] | Kirby2020AJ....159...46K, p.13, Sec. 4.1, Table 4 (Chemical Properties of M31 dSphs), row And VII (mean [Fe/H], spectroscopic). | page: 13 · table: 4 · row: And I; And III; And V; And VII; And X · section: 4.1 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda VII"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda VII") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda X

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Tollerud 2012 ApJ 752 45 (arXiv 1112.1067v3), p9, Table 3, row And X, column σLOS. | page: 9 · table: 3 · row: And I; And III; And V; And VII; And IX; And X; And XIV; And XV; And XVI · column: σLOS |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And X. Convention: semi-major. | page: 9 · table: 1 · row: And X |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And X'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And X' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And X). | page: 9 · table: 2 · row: And X |
| [Fe/H] | Kirby2020AJ....159...46K, p.13, Sec. 4.1, Table 4 (Chemical Properties of M31 dSphs), row And X (mean [Fe/H], spectroscopic). | page: 13 · table: 4 · row: And I; And III; And V; And VII; And X · section: 4.1 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda X"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda X") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XI

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.33 Table 5, p.37 Table A1 Full algorithm, p.40 Sec B.3. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XI. Convention: semi-major. | page: 9 · table: 1 · row: And XI |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XI'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XI' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XI). | page: 9 · table: 2 · row: And XI |
| [Fe/H] | Collins2013ApJ...768..172C, p.27, Table 4 (Kinematic properties of Andromeda dSph galaxies as derived within this work), row And XI (mean [Fe/H], kind not stated by the source). | page: 27; 33; 30 · table: 4; 5 · row: And VI; And XI; And XII; And XVII; And XX; And XXII; And XXIII; And XXVII; And XXX (Cass II |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XI"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XI") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XII

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.33 Table 5, p.37 Table A1 Full algorithm ('0+4.0'), p.40 Sec B.4. An upper limit. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XII. Convention: semi-major. | page: 9 · table: 1 · row: And XII |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XII'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XII' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XII). | page: 9 · table: 2 · row: And XII |
| [Fe/H] | Collins2013ApJ...768..172C, p.27, Table 4 (Kinematic properties of Andromeda dSph galaxies as derived within this work), row And XII (mean [Fe/H], kind not stated by the source). | page: 27; 33; 30 · table: 4; 5 · row: And VI; And XI; And XII; And XVII; And XX; And XXII; And XXIII; And XXVII; And XXX (Cass II |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XII"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XII") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XIV

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Tollerud 2012 ApJ 752 45 (arXiv 1112.1067v3), p9, Table 3, row And XIV, column σLOS. | page: 9 · table: 3 · row: And I; And III; And V; And VII; And IX; And X; And XIV; And XV; And XVI · column: σLOS |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XIV. Convention: semi-major. | page: 9 · table: 1 · row: And XIV |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XIV'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XIV' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XIV). | page: 9 · table: 2 · row: And XIV |
| [Fe/H] | Wojno2020ApJ...895...78W, p.23, Sec. 7.3, Table 6 (Mass-metallicity Relation and Abundance Trends in M31 dSphs), row And XIV (mean [Fe/H], spectroscopic). | page: 23 · table: 6 · row: And II; And IX; And XIV; And XV · section: 7.3 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XIV"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XIV") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XIX

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.11 Sec 4.3, p.27 Sec 5 text, p.33 Table 5, p.37 Table A1 Full algorithm. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XIX. Convention: semi-major. | page: 9 · table: 1 · row: And XIX |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XIX'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XIX' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XIX). | page: 9 · table: 2 · row: And XIX |
| [Fe/H] | Cullinane2024ApJ...972..133C, p.12-13, Sec. 4.2 (Comparison with literature metallicities) (mean [Fe/H], spectroscopic). | page: 12-13 · section: 4.2 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XIX"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XIX") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XV

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Tollerud 2012 ApJ 752 45 (arXiv 1112.1067v3), p9, Table 3, row And XV, column σLOS. | page: 9 · table: 3 · row: And I; And III; And V; And VII; And IX; And X; And XIV; And XV; And XVI · column: σLOS |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XV. Convention: semi-major. | page: 9 · table: 1 · row: And XV |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XV'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XV' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XV). | page: 9 · table: 2 · row: And XV |
| [Fe/H] | Wojno2020ApJ...895...78W, p.23, Sec. 7.3, Table 6 (Mass-metallicity Relation and Abundance Trends in M31 dSphs), row And XV (mean [Fe/H], spectroscopic). | page: 23 · table: 6 · row: And II; And IX; And XIV; And XV · section: 7.3 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XV"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XV") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XVI

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Tollerud 2012 ApJ 752 45 (arXiv 1112.1067v3), p9, Table 3, row And XVI, column σLOS. | page: 9 · table: 3 · row: And I; And III; And V; And VII; And IX; And X; And XIV; And XV; And XVI · column: σLOS |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XVI. Convention: semi-major. | page: 9 · table: 1 · row: And XVI |
| Distance | MartinezVazquez2017ApJ...850..137M p. 18, Table 8 (Summary of the different true distance moduli (µ0) obtained using several methods), row And XVI. Read as the distance modulus. | page: 18 · table: 8 · row: And XVI |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XVI). | page: 9 · table: 2 · row: And XVI |
| [Fe/H] | Fu2024ApJ...975....2F, p.9, Table 2 (Metallicity Properties of And XVI and And XXVIII), Global MDF; also abstract p.1, Sec. 4.1 p.7 (mean [Fe/H], photometric). | page: 9; 1; 7 · table: 2 · section: 4.1 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XVI"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XVI") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XVII

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.33 Table 5, p.10 Sec 4.1 text, Fig. 6 label. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XVII. Convention: semi-major. | page: 9 · table: 1 · row: And XVII |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XVII'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XVII' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XVII). | page: 9 · table: 2 · row: And XVII |
| [Fe/H] | Collins2013ApJ...768..172C, p.27, Table 4 (Kinematic properties of Andromeda dSph galaxies as derived within this work), row And XVII (mean [Fe/H], kind not stated by the source). | page: 27; 33; 30 · table: 4; 5 · row: And VI; And XI; And XII; And XVII; And XX; And XXII; And XXIII; And XXVII; And XXX (Cass II |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XVII"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XVII") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XVIII

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Kvasova 2024 ApJ 972 180 (arXiv 2404.11804v4), p.7, Table 2, Kinematic models, σv (no rotation), column '38 stars, (56)'; also p.11 Table 4 'This work' row. | page: 7; 11 · table: 2; 4 · column: '38 stars |
| r_h and ε | Higgs2021MNRAS.503..176H PDF p.16, Table 3 (Best-fit Sérsic parameters), row And XVIII. Convention: semi-major. | page: 16 · table: 3 (r_h: column Rs); 2 (ε: column e) · row: And XVIII |
| Distance | Higgs2021MNRAS.503..176H PDF p.16, Table 2 (Derived positional and shape information), row And XVIII. Read as the distance modulus. | page: 16 · table: 2 · row: And XVIII |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XVIII). | page: 9 · table: 2 · row: And XVIII |
| [Fe/H] | Kvasova2024ApJ...972..180K, p.10-11, Sec. 4.3 (Metallicity) (mean [Fe/H], spectroscopic). | page: 10-11; 11 · section: 4.3 · table: 4 · row: 'This work' |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XVIII"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XVIII") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XX

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.14 Sec 4.4 text, p.33 Table 5, p.37 Table A1 Full algorithm. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XX. Convention: semi-major. | page: 9 · table: 1 · row: And XX |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XX'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XX' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XX). | page: 9 · table: 2 · row: And XX |
| [Fe/H] | Collins2013ApJ...768..172C, p.27, Table 4 (Kinematic properties of Andromeda dSph galaxies as derived within this work), row And XX (mean [Fe/H], kind not stated by the source). | page: 27; 33; 30 · table: 4; 5 · row: And VI; And XI; And XII; And XVII; And XX; And XXII; And XXIII; And XXVII; And XXX (Cass II |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XX"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XX") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XXI

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2021 MNRAS 505 5686 (arXiv 2102.11890v2), p.5, Sect. 3.1; p.4, Table 2 (The properties of And XXI); abstract; Sect. 6. | page: 5; 4 · table: 2 · section: 3.1; 6 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XXI. Convention: semi-major. | page: 9 · table: 1 · row: And XXI |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XXI'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XXI' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XXI). | page: 9 · table: 2 · row: And XXI |
| [Fe/H] | Collins2021MNRAS.505.5686C, p.4, Table 2 (The properties of And XXI); also abstract p.1, Sec. 3.4 p.7, Fig. 8 caption p.10, Sec. 6 (mean [Fe/H], spectroscopic). | page: 4; 1; 7; 10 · table: 2 · section: 3.4; 6 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XXI"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XXI") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XXII

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.15 Sec 4.6 text, p.33 Table 5, p.37 Table A1 Full algorithm. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XXII/Tri I. Convention: semi-major. | page: 9 · table: 1 · row: And XXII/Tri I |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XXII'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XXII' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XXII/Tri I). | page: 9 · table: 2 · row: And XXII/Tri I |
| [Fe/H] | Collins2013ApJ...768..172C, p.27, Table 4 (Kinematic properties of Andromeda dSph galaxies as derived within this work), row And XXII (mean [Fe/H], kind not stated by the source). | page: 27; 33; 30 · table: 4; 5 · row: And VI; And XI; And XII; And XVII; And XX; And XXII; And XXIII; And XXVII; And XXX (Cass II |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XXII"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XXII") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XXIII

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.15 Sec 4.7 text, Fig.12 label, p.33 Table 5, p.37 Table A1 Full algorithm, p.38 Table A3 Full sample. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XXIII. Convention: semi-major. | page: 9 · table: 1 · row: And XXIII |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XXIII'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XXIII' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XXIII). | page: 9 · table: 2 · row: And XXIII |
| [Fe/H] | Collins2013ApJ...768..172C, p.27, Table 4 (Kinematic properties of Andromeda dSph galaxies as derived within this work), row And XXIII (mean [Fe/H], kind not stated by the source). | page: 27; 33; 30 · table: 4; 5 · row: And VI; And XI; And XII; And XVII; And XX; And XXII; And XXIII; And XXVII; And XXX (Cass II |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XXIII"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XXIII") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XXV

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.16 Sec 4.9 text, p.27 Sec 5 text, p.33 Table 5, p.37 Table A1 Full algorithm, p.38 Table A3 Full sample. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row And XXV. Convention: semi-major. | page: 9 · table: 1 · row: And XXV |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XXV'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XXV' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row And XXV). | page: 9 · table: 2 · row: And XXV |
| [Fe/H] | Charles2023MNRAS.521.3527C, p.4, Table 2 (The properties of And XXV); also abstract p.1, Sec. 5 p.6, Sec. 8 (mean [Fe/H], spectroscopic). | page: 4; 1; 6 · table: 2 · section: 5; 8 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XXV"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XXV") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XXVII

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.19 Sec 4.11 text, p.33 Table 5, p.37 Table A1 Full algorithm. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Richardson2011ApJ...732...76R p.11, Table 1, col And XXVII, row rh (arcmin). Convention: semi-major. | page: 11 · table: 1 · row: rh (arcmin · column: And XXVII |
| Distance | Richardson2011ApJ...732...76R p.11, Table 1, col And XXVII, row (m − M)0. Read as the distance modulus. | page: 11 · table: 1 · row: (m − M · column: And XXVII |
| m_V,0 | M_V from Richardson2011ApJ...732...76R p.11, Table 1, col And XXVII, row MV, plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Collins2013ApJ...768..172C, p.27, Table 4 (Kinematic properties of Andromeda dSph galaxies as derived within this work), row And XXVII (mean [Fe/H], kind not stated by the source). | page: 27; 33; 30 · table: 4; 5 · row: And VI; And XI; And XII; And XVII; And XX; And XXII; And XXIII; And XXVII; And XXX (Cass II |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XXVII"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XXVII") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Andromeda XXVIII

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.33 Table 5. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Higgs2021MNRAS.503..176H PDF p.16, Table 3 (Best-fit Sérsic parameters), row And XXVIII. Convention: semi-major. | page: 16 · table: 3 (r_h: column Rs); 2 (ε: column e) · row: And XXVIII |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XXVIII'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XXVIII' |
| m_V,0 | M_V from Slater2015ApJ...806..230S p.3, Table 1, column And XXVIII, plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Slater2015ApJ...806..230S, p.3, Table 1 (Properties of And XXVIII & XXIX); method Sec. 4 p.4 (mean [Fe/H], spectroscopic). | page: 3; 4 · table: 1 · section: 4 |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XXVIII"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XXVIII") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Antlia II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Ji 2021 ApJ 921 32 (arXiv 2106.12656v2), p.7, Table 1, 'σv, no kv' row, Antlia 2. | page: 7 · table: 1 |
| r_h and ε | Ji2021ApJ...921...32J p. 7, Table 1 (Galaxy Properties), Antlia 2 column, row rh (arcmin); also p. 6, §3 [value], no error). Convention: circularised. | page: 7; 6 · table: 1 · row: rh (arcmin · section: 3 |
| Distance | Vivas2022ApJ...926...78V p.9, §3.3; no_uncertainty: no error printed. Read as the distance modulus. | page: 9 · section: 3.3 |
| m_V,0 | M_V from Ji2021ApJ...921...32J PDF p.7, Table 1 (Galaxy Properties), Antlia 2 column, row MV, plus the modulus the paper uses (cited). | page: 7 · table: 1 · column: Antlia 2 · row: MV; µ (mag) |
| [Fe/H] | Ji2021ApJ...921...32J, p.7, Sec. 4, Table 1 (Galaxy Properties), row ⟨[Fe/H]⟩ (dex, CaT) (mean [Fe/H], spectroscopic). | page: 7; 12; 15 · table: 1; 2 · row: ⟨[Fe/H]⟩ (dex; Antlia2 · section: 4; 5; 7.1.2 |
| Gas | Putman et al. 2021 Table 1, row "Antlia 2"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Antlia 2") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Aquarius II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p32, Appendix, Table A1, row Aqr2, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Torrealba2016MNRAS.463..712T p. 2, Table 1 (Properties of Aqu 2), rh row. Convention: semi-major. | page: 2 · table: 1 |
| Distance | Torrealba2016MNRAS.463..712T p. 2, Table 1 (Properties of Aqu 2), (m − M) row; also p. 4 Fig. 2 caption (printed value). Read as the distance modulus. | page: 2; 4 · table: 1 |
| m_V,0 | M_V from Torrealba2016MNRAS.463..712T p. 2, Table 1 (Properties of Aqu 2), MV row, plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Bruce2023ApJ...950..167B, p.5, Table 2 (Properties of Aquarius II and Boötes II), row [Fe/H]; also abstract p.1 and Sec. 4.1 p.12 (mean [Fe/H], spectroscopic). | page: 5; 1; 12 · table: 2 · row: [Fe/H] · section: 4.1 |
| Gas | Putman et al. 2021 Table 1, row "Aquarius II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Aquarius II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Aquarius III

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p32, Appendix, Table A1, row Aqr3, col. 17. An upper limit. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Cerny2025ApJ...979..164C p.7, Table 1, row ah. Convention: semi-major (a_h; circularised value printed too). | page: 7 · table: 1 · row: ah |
| Distance | Cerny2025ApJ...979..164C p.7, Table 1, row (m − M)0. Read as the distance modulus. | page: 7 · table: 1 · row: (m − M |
| m_V,0 | M_V from Cerny2025ApJ...979..164C p.7, Table 1, row MV, plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Aquarius III Aqr3 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Not in Putman et al. 2021 Table 1: no gas term |  |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Bootes I

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Sandford 2026 ApJ 998 47 (arXiv 2509.02546v1), p8 Table 3 row σv,B; p15–16 Sec. 4.4; p13 Table 5 column Combined; p20 Sec. 5.2; p26 Sec. 9 summary. | page: 8; 15–16; 13; 20; 26 · table: 3; 5 · row: σv · column: Combined · section: 4.4; 5.2; 9 |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Bootes I, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Bootes I · column: re |
| Distance | DallOra2006ApJ...653L.109D p.6, Sect. 5. Read as the distance modulus. | page: 6 · section: 5 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Sandford2026ApJ...998...47S, p.8, Table 3 (Boo I Systemic Properties), Additional Derived Properties; also Sec. 4.4 p.16 and Table 5 'Combined' column p.13 (mean [Fe/H], spectroscopic). | page: 8; 16; 13; 26 · table: 3; 5 · column: p.13 · section: 4.4; 8 |
| Gas | Putman et al. 2021 Table 1, row "Bootes"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Bootes") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Bootes II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p32, Appendix, Table A1, row Boo2, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Bootes II, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Bootes II · column: re |
| Distance | Walsh2008ApJ...688..245W p. 11, Table 1 (Boötes II Properties), row (m − M). Read as the distance modulus. | page: 11 · table: 1 · row: (m − M |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Bootes II Boo2 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Bootes II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Bootes II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Bootes III

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Li 2026 arXiv 2607.07803 (arXiv 2607.07803v1), p.5, §3.2; p.5 Table 1 row (7) 'This work'; abstract. | page: 5 · table: 1 · row: (7 · section: 3.2 |
| r_h and ε | Moskowitz2020ApJ...892...27M p. 12, Table 3, row BooIII_DCLS (1-Plummer, D-061 item 1). Convention: circularised. | page: 12 · table: 3 · row: BooIII_DCLS (1-Plummer |
| Distance | Li2026arXiv260707803L p.10, §4. Read as the distance modulus. | page: 10 · section: 4 |
| Magnitude route (if no m_V,0) | Correnti 2009 M_V, distance-independent (D-061 item 2). | page: 5 · section: 4 (iii) |
| [Fe/H] | Li2026arXiv260707803L, p.5, Table 1 (Comparison of literature and updated Boötes III parameters), row (8), 'This work'; also abstract p.1, Sec. 3.3 p.6, Sec. 7 p.23 (mean [Fe/H], spectroscopic). | page: 5; 1; 6; 23 · table: 1 · row: (8 · section: 3.3; 7 |
| Gas | Putman et al. 2021 Table 1, row "Bootes III"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Bootes III") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Canes Venatici I

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p32, Appendix, Table A1, row CVn1, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row CVn I, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: CVn I · column: re |
| Distance | Kuehn2008ApJ...674L..81K PDF p.6, Section 5 (An Improved Distance Estimate for CVn I). Read as the distance modulus. | page: 6 · section: 5 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row CVn I CVn1 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Canes Venatici I"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Canes Venatici I") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Canes Venatici II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p32, Appendix, Table A1, row CVn2, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row CVn II, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: CVn II · column: re |
| Distance | Greco2008ApJ...675L..73G §5, p. 7. Read as the distance modulus. | page: 7 · section: 5 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row CVn II CVn2 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Canes Venatici II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Canes Venatici II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Cassiopeia II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Collins 2013 ApJ 768 172 (arXiv 1302.6590v1), p.27, Table 4, sigma_v column; also p.20 Sec 4.13 text, p.33 Table 5, p.37 Table A1 Full algorithm. | page: 27; 33; 37; 39; 40; 10; 11; 14; 15; 38; 16; 19; 20 · table: 4; 5 |
| r_h and ε | Martin2016ApJ...833..167M p. 9, Table 1 (Derived structural parameters of the dwarf galaxies), row Cas II/And XXX. Convention: semi-major. | page: 9 · table: 1 · row: Cas II/And XXX |
| Distance | Savino2022ApJ...938..101S p.15, Table 5, row 'And XXX'. Read as the distance modulus. | page: 15 · table: 5 · row: 'And XXX' |
| m_V,0 | printed m_V,0 (Martin2016ApJ...833..167M p. 9, Table 2 (Derived luminosity-related properties of the dwarf galaxies), row Cas II/And XXX). | page: 9 · table: 2 · row: Cas II/And XXX |
| [Fe/H] | Collins2013ApJ...768..172C, p.27, Table 4 (Kinematic properties of Andromeda dSph galaxies as derived within this work), row And XXX (Cass II) (mean [Fe/H], kind not stated by the source). | page: 27; 33; 30 · table: 4; 5 · row: And VI; And XI; And XII; And XVII; And XX; And XXII; And XXIII; And XXVII; And XXX (Cass II |
| Gas | Putman et al. 2021 Table 1, row "Andromeda XXX"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Andromeda XXX") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Columba I

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p32, Appendix, Table A1, row Col1, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Carlin2017AJ....154..267C p.5, Table 1, col Col I, row rh,exp (arcmin). Convention: semi-major. | page: 5 · table: 1 · row: rh · column: Col I |
| Distance | Carlin2017AJ....154..267C p.5, Table 1, col Col I, row m − M. Read as the distance modulus. | page: 5 · table: 1 · row: m − M · column: Col I |
| m_V,0 | M_V from Carlin2017AJ....154..267C p.5, Table 1 (Properties of Col I and Tri II), row MV, plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Fritz2019A&A...623A.129F, p.12, Sec. 5, Table 3 (Average and global properties), lower block (certain members), row Columba I (mean [Fe/H], spectroscopic). | page: 12 · table: 3 · row: Columba I; Phoenix II; Reticulum III · section: 5 |
| Gas | Putman et al. 2021 Table 1, row "Columba I"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Columba I") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Coma Berenices

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p32, Appendix, Table A1, row CB, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row ComBer, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: ComBer · column: re |
| Distance | Musella2009ApJ...695L..83M PDF p.7, Section 4. Read as the distance modulus. | page: 7 · section: 4 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row ComaBer CB (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Coma Berenices"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Coma Berenices") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Draco

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p32, Appendix, Table A1, row Dra, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Draco, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Draco · column: re |
| Distance | Bhardwaj2024AJ....167..247B p.10, Table 5 (Distance modulus estimates to Draco dSph galaxy), final rows. Read as the distance modulus. | page: 10 · table: 5 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Draco Dra (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Draco"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Draco") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Draco II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Cerny 2026 arXiv 2602.17652 (arXiv 2602.17652v1), p38 Table 3 row Draco II (σv); p33 Sec. 5.2; p34 Fig. 21; p48–49 Sec. 7.3.5. An upper limit. | page: 38; 33; 34; 48–49 · table: 3 · row: Draco II (σv · section: 5.2; 7.3.5 |
| r_h and ε | Longeard2018MNRAS.480.2609L p.8, Table 1, row rh (arcmin). Convention: semi-major. | page: 8 · table: 1 · row: rh (arcmin |
| Distance | Longeard2018MNRAS.480.2609L p.8, Table 1, row Distance modulus. Read as the distance modulus. | page: 8 · table: 1 · row: Distance modulus |
| m_V,0 | M_V from Longeard2018MNRAS.480.2609L p.8, Table 1, row MV, plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Cerny2026arXiv260217652C, p.40, Sec. 6.2, Table 4 (Metallicity Properties of the UFCS derived in this Work), row Draco II, column [Fe/H]model; also Sec. 7.3.5 p.48 (mean [Fe/H], spectroscopic). | page: 40; 48 · table: 4 · row: Draco II · column: [Fe/H]model · section: 6.2; 7.3.5 |
| Gas | Putman et al. 2021 Table 1, row "Draco II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Draco II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Eridanus IV

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Heiger 2024 ApJ 961 234 (arXiv 2308.08602v1), p3 Table 1 row σv; p12 Sec. 5.1; p15 Table 5 row 'Full vsys (fiducial)'; abstract; Sec. 7. | page: 3; 12; 15 · table: 1; 5 · row: σv; 'Full vsys (fiducial · section: 5.1; 7 |
| r_h and ε | Casey2025ApJ...984..148C p. 5, Table 4, column Eri IV. Convention: semi-major. | page: 5 · table: 4 · column: Eri IV |
| Distance | Cerny2021ApJ...920L..44C PDF p.5, Table 1 (Morphological, isochrone, and proper motion parameters for Eri IV), row m − M. Read as the distance modulus. | page: 5 · table: 1 · row: m − M |
| m_V,0 | M_V from Casey2025ApJ...984..148C p. 5, Table 4, column Eri IV, plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Heiger2024ApJ...961..234H, p.3, Table 1, row [Fe/H]; also abstract p.1, Sec. 5.2 p.13, Table 5 p.15, Sec. 7 p.21 (mean [Fe/H], spectroscopic). | page: 3; 1; 13; 15; 21 · table: 1; 5 · row: [Fe/H] · section: 5.2; 7 |
| Gas | Not in Putman et al. 2021 Table 1: no gas term |  |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Fornax

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Hendricks 2014 A&A 572 A82 (arXiv 1408.5597v1), p.5, Sect. 2.1. | page: 5 · section: 2.1 |
| r_h and ε | Wang2019ApJ...881..118W Table 1, Sérsic column (arXiv 1809.07801v1 Fornax_main.tex l. 106); the source's stated best fit, l. 333 (D-101; D-096 rule 1); no_uncertainty: no error printed. Convention: as printed (semi-major (assumed, D-052 item 2)); Sérsic fit. | table: 1 · column: (arXiv 1809.07801v1 Fornax_main.tex l. 106 · line: 106; 333 |
| Distance | Oakes2022ApJ...929..116O p.13, §7; also p.1 abstract and p.13 §6.4. Read as the distance modulus. | page: 13; 1 · section: 7; 6.4 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Kirby2013ApJ...779..102K, p.12, Table 4 (Summary of MDFs), Milky Way dSphs, row Fornax (mean [Fe/H], spectroscopic). | page: 12 · table: 4 · row: Fornax; Leo T; Sculptor; Sextans |
| Gas | Putman et al. 2021 Table 1, row "Fornax"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Fornax") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Hercules

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Ou 2024 ApJ 966 33 (arXiv 2403.00921v1), p.15, Table 2, 'No Gradient' column. | page: 15 · table: 2 |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Hercules, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Hercules · column: re |
| Distance | MutluPakdil2020ApJ...902..106M PDF p.6, Table 9 (Structural Properties of Hercules), row m − M. Read as the distance modulus. | page: 6 · table: 9 · row: m − M |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Herc Herc (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Hercules"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Hercules") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Hydra II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p32, Appendix, Table A1, row Hyd2, col. 17. An upper limit. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Secondary Sample, row Hydra II, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Hydra II · column: re |
| Distance | Vivas2016AJ....151..118V p. 17, Sect. 4. Read as the distance in kpc. | page: 17 · section: 4 |
| m_V,0 | printed m_V,0 (Richstein2024ApJ...967...72R p. 9, Table 2, row Hya II). | page: 9 · table: 2 · row: Hya II |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Hydra 2 Hyd2 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Hydra II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Hydra II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Hydrus I

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Koposov 2018 MNRAS 479 5343 (arXiv 1804.06430v1), p9, Sect. 4.3; p6 Table 1 (σlos). | page: 9; 6 · table: 1 · section: 4.3 |
| r_h and ε | Koposov2018MNRAS.479.5343K p. 6, Table 1 (Key photometric and kinematic properties of the Hydrus 1 dwarf galaxy), rhalf,maj row. Convention: semi-major (a_h; circularised value printed too). | page: 6 · table: 1 |
| Distance | Koposov2018MNRAS.479.5343K p. 6, Table 1 (Key photometric and kinematic properties of the Hydrus 1 dwarf galaxy), m-M row. Read as the distance modulus. | page: 6 · table: 1 |
| m_V,0 | M_V from Koposov2018MNRAS.479.5343K p. 6, Table 1 (Key photometric and kinematic properties of the Hydrus 1 dwarf galaxy), MV row, plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Koposov2018MNRAS.479.5343K, p.6, Table 1 (Key photometric and kinematic properties of the Hydrus 1 dwarf galaxy); also Sec. 4.3 p.9 (mean [Fe/H], spectroscopic). | page: 6; 9 · table: 1 · section: 4.3 |
| Gas | Putman et al. 2021 Table 1, row "Hydrus I"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Hydrus I") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Leo I

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Koch 2007 ApJ 657 241 (arXiv astro-ph/0611372v1), p.18, Table 3 (Mean velocities and dispersions for different fields), row 'GMOS + DEIMOS'. | page: 18 · table: 3 · row: 'GMOS + DEIMOS' |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Leo I, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Leo I · column: re |
| Distance | Stetson 2014, midpoint of the two printed values. Read as printed. | page: 11 · section: 4.1 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Leo I Leo1 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Leo I"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Leo I") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Leo II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Spencer 2017 ApJ 836 202 (arXiv 1702.08836v1), p7, Sect. 3.2; also p1 abstract; p11 Sect. 4. | page: 7; 1; 11 · section: 3.2; 4 |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Leo II, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Leo II · column: re |
| Distance | Monelli2025A&A...700A.201M (headline; version of record). Read as printed. | page: 7 · section: 4 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Leo II Leo2 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Leo II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Leo II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Leo IV

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p33, Appendix, Table A1, row Leo4, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Leo IV, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Leo IV · column: re |
| Distance | Medina 2018, RR Lyrae mean. Read as printed. | page: 10 · section: 5.1 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.17, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Leo IV Leo4 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Leo IV"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Leo IV") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Leo T

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p33, Appendix, Table A1, row LeoT, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Higgs2021MNRAS.503..176H PDF p.16, Table 3 (Best-fit Sérsic parameters), row Leo T. Convention: semi-major. | page: 16 · table: 3 (r_h: column Rs); 2 (ε: column e) · row: Leo T |
| Distance | Higgs2021MNRAS.503..176H PDF p.16, Table 2 (Derived positional and shape information), row Leo T. Read as the distance modulus. | page: 16 · table: 2 · row: Leo T |
| m_V,0 | de Jong 2008 M_V + red-clump modulus (D-061 item 6). | page: 5 (M_V); 7 (red-clump modulus) · table: 1 · section: 4 (M_V); 6 (modulus) |
| [Fe/H] | Kirby2013ApJ...779..102K, p.12, Table 4 (Summary of MDFs), Local Group dIrrs, row Leo T (mean [Fe/H], spectroscopic). | page: 12 · table: 4 · row: Fornax; Leo T; Sculptor; Sextans |
| Gas | Putman et al. 2021 Table 1, row "Leo T"; a detection: MHI and Dist | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Leo T") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Leo V

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p33, Appendix, Table A1, row Leo5, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Leo V, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Leo V · column: re |
| Distance | Medina 2018, RR Lyrae mean. Read as printed. | page: 10 · section: 5.1 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Jenkins2021ApJ...920...92J, p.17, Table 5 (UFD properties), bottom panel, row [Fe/H] M1, Leo V column; also Sec. 5.6 p.21 and Sec. 6 (mean [Fe/H], spectroscopic). | page: 17; 21 · table: 5 · row: [Fe/H] M1 · section: 5.6; 6 |
| Gas | Putman et al. 2021 Table 1, row "Leo V"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Leo V") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Leo VI

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p33, Appendix, Table A1, row Leo6, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Tan2025ApJ...979..176T p.8, Table 1, row ah. Convention: semi-major (a_h; circularised value printed too). | page: 8 · table: 1 · row: ah |
| Distance | Tan2025ApJ...979..176T p.8, Table 1, row (m − M)0. Read as the distance modulus. | page: 8 · table: 1 · row: (m − M |
| m_V,0 | M_V from Tan2025ApJ...979..176T p.8, Table 1, row MV, plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Tan2025ApJ...979..176T, p.8, Table 1 (Measured and derived parameters of Leo VI), row [Fe/H]spec; also Sec. 5 p.11 (mean [Fe/H], spectroscopic). | page: 8; 11 · table: 1 · row: [Fe/H]spec · section: 5 |
| Gas | Not in Putman et al. 2021 Table 1: no gas term |  |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Pegasus III

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p33, Appendix, Table A1, row Peg3, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Richstein2022ApJ...933..217R p. 7, Table 1 (Pegasus III), Exponential block, column This Work, row ah (arcmin). Convention: semi-major (a_h; circularised value printed too). | page: 7 · table: 1 · row: ah (arcmin · column: This Work |
| Distance | Kim2016ApJ...833...16K p. 5, Table 1. Read as the distance modulus. | page: 5 · table: 1 |
| m_V,0 | printed m_V,0 (Richstein2022ApJ...933..217R PDF p.12, Table 3, Pegasus III). | page: 12 · table: 3 |
| [Fe/H] | Geha2026arXiv260210202G, p.18, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Pegasus 3 Peg3 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Pegasus III"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Pegasus III") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Pegasus IV

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p33, Appendix, Table A1, row Peg4, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Cerny2023ApJ...942..111C p.7, Table 1 (azimuthally averaged r_h; D-062 item 2). Convention: circularised. | page: 7 · table: 1 |
| Distance | Cerny2023ApJ...942..111C p.7, Table 1. Read as the distance modulus. | page: 7 · table: 1 |
| m_V,0 | M_V from Cerny2023ApJ...942..111C p.7, Table 1, plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Geha2026arXiv260210202G, p.18, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Pegasus 4 Peg4 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Not in Putman et al. 2021 Table 1: no gas term |  |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Phoenix

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Kacharov 2017 MNRAS 466 2006 (arXiv 1612.01560v1), p10, Sect. 5. | page: 10 · section: 5 |
| r_h and ε | Battaglia2012MNRAS.424.1113B p.3, Table 1. Convention: semi-major. | page: 3 · table: 1 |
| Distance | Battaglia2012MNRAS.424.1113B p.3, Table 1, row (m-M)0. Read as the distance modulus. | page: 3 · table: 1 · row: (m-M |
| m_V,0 | van de Rydt 1991 M_V + adopted modulus (D-061 item 5). | page: 136 (M_V); 134 (modulus) · section: 8 (M_V); 4 (modulus) |
| [Fe/H] | Kacharov2017MNRAS.466.2006K, p.12, Sec. 6 (Metallicity properties); also abstract p.1 and Sec. 6.3 p.17 (mean [Fe/H], spectroscopic). | page: 12; 1; 17 · section: 6; 6.3 |
| Gas | Putman et al. 2021 Table 1, row "Phoenix"; a detection: MHI and Dist | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Phoenix") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Phoenix II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Fritz 2019 A&A 623 A129, Table 4, certain members (arXiv 1805.07350v4 spec_v1_ref1_arx.tex l. 452; bold = preferred, caption l. 436); D-096 rule 1 (D-098 rule 5); reading/resolved.csv. | table: 4 · line: 452; 436 |
| r_h and ε | Richstein2024ApJ...967...72R p. 9, Table 2, row Phe II. Convention: circularised. | page: 9 · table: 2 · row: Phe II |
| Distance | MutluPakdil2018ApJ...863...25M p.8, Table 6 (Structural Properties), row m − M; also p. 12, §4.3 (printed value). Read as the distance modulus. | page: 8; 12 · table: 6 · row: m − M · section: 4.3 |
| m_V,0 | printed m_V,0 (Richstein2024ApJ...967...72R p. 9, Table 2, row Phe II). | page: 9 · table: 2 · row: Phe II |
| [Fe/H] | Fritz2019A&A...623A.129F, p.12, Table 3, lower block (certain members), row Phoenix II (mean [Fe/H], spectroscopic). | page: 12 · table: 3 · row: Columba I; Phoenix II; Reticulum III · section: 5 |
| Gas | Putman et al. 2021 Table 1, row "Phoenix 2"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Phoenix 2") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Pisces II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p34, Appendix, Table A1, row Pisc2, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Richstein2022ApJ...933..217R p. 7, Table 2 (Pisces II), Exponential block, column This Work, row ah (arcmin). Convention: semi-major (a_h; circularised value printed too). | page: 7 · table: 2 · row: ah (arcmin · column: This Work |
| Distance | Sand2012ApJ...756...79S p.16, Table 5, row Pisces II. Read as the distance modulus. | page: 16 · table: 5 · row: Pisces II |
| m_V,0 | printed m_V,0 (Richstein2022ApJ...933..217R PDF p.12, Table 3, Pisces II). | page: 12 · table: 3 |
| [Fe/H] | Kirby2015ApJ...810...56K, p.10, Table 3 (Satellite Properties), row ⟨[Fe/H]⟩, Pisces II column; also abstract p.1 (mean [Fe/H], spectroscopic). | page: 10; 1 · table: 3 · row: ⟨[Fe/H]⟩ |
| Gas | Putman et al. 2021 Table 1, row "Pisces II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Pisces II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Reticulum III

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Fritz 2019 A&A 623 A129 (arXiv 1805.07350v4), p12, Table 3, Reticulum III row. An upper limit. | page: 12; 1 · table: 3 |
| r_h and ε | DrlicaWagner2015ApJ...813..109D p. 17, Table 1 (Detection of ultra-faint galaxy candidates), row DES J0345−6026 (Ret III). Convention: circularised. | page: 17 · table: 1 · row: DES J0345−6026 (Ret III |
| Distance | DrlicaWagner2015ApJ...813..109D p. 17, Table 1 (Detection of ultra-faint galaxy candidates), row DES J0345−6026 (Ret III). Read as the distance modulus. | page: 17 · table: 1 · row: DES J0345−6026 (Ret III |
| m_V,0 | M_V from DrlicaWagner2015ApJ...813..109D p. 17, Table 2 (Derived properties of ultra-faint galaxy candidates), row DES J0345−6026 (Ret III); also p. 34 Table 4 (printed value), plus the modulus the paper uses (its own, read as above). | row: the system's row in the paper that gives its distance modulus |
| [Fe/H] | Fritz2019A&A...623A.129F, p.12, Table 3, upper block (all possible members), row Reticulum III (mean [Fe/H], spectroscopic). | page: 12 · table: 3 · row: Columba I; Phoenix II; Reticulum III · section: 5 |
| Gas | Putman et al. 2021 Table 1, row "Reticulum III"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Reticulum III") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Sculptor

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p34, Appendix, Table A1, row Scl, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Sculptor, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Sculptor · column: re |
| Distance | MartinezVazquez2015MNRAS.454.1509M p.7, Table 3, row <µ>ADOPTED, CLEAN; also p. 3, §3 (printed value). Read as the distance modulus. | page: 7; 3 · table: 3 · row: <µ>ADOPTED · section: 3 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Kirby2013ApJ...779..102K, p.12, Table 4 (Summary of MDFs), Milky Way dSphs, row Sculptor (mean [Fe/H], spectroscopic). | page: 12 · table: 4 · row: Fornax; Leo T; Sculptor; Sextans |
| Gas | Putman et al. 2021 Table 1, row "Sculptor"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Sculptor") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Segue 1

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Simon 2011 ApJ 733 46 (arXiv 1007.4198v3), p.11 §5.2; p.3 Table 1 row (11); abstract. | page: 11; 3 · table: 1 · row: (11 · section: 5.2 |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5 (Sérsic Models), row Segue 1. Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Segue 1 |
| Distance | Belokurov2007ApJ...654..897B PDF p.6, Table 1 (Properties of the New Milky Way Satellites), column Segue 1, row (m−M)0. Read as the distance modulus. | page: 6 · table: 1 · row: (m−M · column: Segue 1 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Bissonette2026arXiv260512810B, p.2, Table 1 (Summary of Properties of Segue 1), row (14); also abstract p.1, Sec. 4 p.5, Table 4 p.7 (Single Gaussian µ), Sec. 5 p.6 (mean [Fe/H], spectroscopic). | page: 2; 1; 5; 7; 6 · table: 1; 4 · row: (14 · section: 4; 5 |
| Gas | Putman et al. 2021 Table 1, row "Segue 1"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Segue 1") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Segue 2

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Kirby 2013 ApJ 770 16 (arXiv 1304.6080v3), p8, Sect. 5; p9 Table 5; p1 abstract; p15 Sect. 8. An upper limit. | page: 8; 9; 1; 15 · table: 5 · section: 5; 8 |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Segue 2, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Segue 2 · column: re |
| Distance | Boettcher 2013, BHB stars (D-055 item 8). Read as printed. | page: 6 · section: 3.2 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.18, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Segue 2 Seg2 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Segue II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Segue II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Sextans

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Battaglia 2011 MNRAS 411 1013 (arXiv 1009.4857v2), p.5, Sect. 3.4; p.15, Table 1. | page: 5; 15 · table: 1 · section: 3.4 |
| r_h and ε | Cicuendez2018A&A...609A..53C p.9, Table 3, row 2D Half-light rh, col King. Convention: semi-major. | page: 9 · table: 3 · row: 2D Half-light rh · column: King |
| Distance | Lee2009ApJ...703..692L p.4, Sect. 3; p.19, Table 3; no_uncertainty: no error printed. Read as the distance modulus. | page: 4; 19 · table: 3 · section: 3 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Kirby2013ApJ...779..102K, p.12, Table 4 (Summary of MDFs), Milky Way dSphs, row Sextans (mean [Fe/H], spectroscopic). | page: 12 · table: 4 · row: Fornax; Leo T; Sculptor; Sextans |
| Gas | Putman et al. 2021 Table 1, row "Sextans"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Sextans") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Triangulum II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Kirby 2017 ApJ 838 83 (arXiv 1703.02978v2), p.6, Sect. 3.4; Table 3; abstract. An upper limit. | page: 6 · table: 3 · section: 3.4 |
| r_h and ε | Carlin2017AJ....154..267C p.5, Table 1, col Tri II, row rh,exp (arcmin). Convention: semi-major. | page: 5 · table: 1 · row: rh · column: Tri II |
| Distance | Carlin2017AJ....154..267C p.5, Table 1, col Tri II, row m − M. Read as the distance modulus. | page: 5 · table: 1 · row: m − M · column: Tri II |
| m_V,0 | printed m_V,0 (Richstein2024ApJ...967...72R p. 9, Table 2, row Tri II). | page: 9 · table: 2 · row: Tri II |
| [Fe/H] | Kirby2017ApJ...838...83K, p.6, Table 3 (Properties of Triangulum II); Sec. 4 p.8 ('Table 3 gives the mean of the stellar metallicities weighted by their inverse variances') (mean [Fe/H], spectroscopic). | page: 6; 8 · table: 3 · section: 4 |
| Gas | Putman et al. 2021 Table 1, row "Triangulum II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Triangulum II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Tucana

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Gregory 2019 MNRAS 485 2010 (arXiv 1902.07228v2), p7, Figure 5 panel annotation. | page: 7 |
| r_h and ε | Saviane 1996[value]0 = [value], as an angle (D-053; D-058 rescaling); error printed in pc ([value]), converted as the value. Convention: circularised. | page: 9 · table: 5 · row: Re (pc) |
| Distance | Bernard 2009, RR Lyrae, reddening-corrected (D-053). Read as printed. | page: 19 · section: 6.3 |
| m_V,0 | Saviane 1996 M_V + its own TRGB modulus (D-053). | page: 9 · table: 5 · row: MV |
| [Fe/H] | Taibi2020A&A...635A.152T, p.11, Sec. 6.1 (Metallicity properties); also Table 1 p.3 ('[Fe/H] dex −1.58 (4)', described in caption as 'the median metallicity'), Sec. 8 (median [Fe/H], spectroscopic). | page: 11; 3 · table: 1 · section: 6.1; 8 |
| Gas | Putman et al. 2021 Table 1, row "Tucana"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Tucana") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Tucana V

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Hansen 2024 ApJ 968 21 (arXiv 2403.13060v1), p8 Sec. 5.1. | page: 8 · section: 5.1 |
| r_h and ε | Simon2020ApJ...892..137S p.9, Table 6, row (4); also p. 7, §4.1 (printed value). Convention: semi-major. | page: 9; 7 · table: 6 · row: (4 · section: 4.1 |
| Distance | Simon2020ApJ...892..137S p.9, Table 6, row (3). Read as the distance in kpc. | page: 9 · table: 6 · row: (3 |
| m_V,0 | Simon 2020 M_V + Table 6 distance 55 kpc (D-061 item 7). | table: 6 |
| [Fe/H] | Hansen2024ApJ...968...21H, p.8, Sec. 5.1 (sentence starts p.7) (mean [Fe/H], spectroscopic). | page: 8; 7 · section: 5.1 |
| Gas | Putman et al. 2021 Table 1, row "Tucana V"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Tucana V") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Ursa Major I

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p34, Appendix, Table A1, row UMa1, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row UMa I, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: UMa I · column: re |
| Distance | Garofalo2013ApJ...767...62G p.7–8, §4; also abstract p.1 and §6 p.9. Read as the distance modulus. | page: 7–8; 1; 9 · section: 4; 6 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.19, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row UMa 1 UMa1 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Ursa Major I"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Ursa Major I") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Ursa Major II

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p34, Appendix, Table A1, row UMa2, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row UMa II, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: UMa II · column: re |
| Distance | DallOra2012ApJ...752...42D p.7, Sect. 3. Read as the distance modulus. | page: 7 · section: 3 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.19, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row UMa 2 UMa2 (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Ursa Major II"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Ursa Major II") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Ursa Minor

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Geha 2026 ApJ 999 140 (arXiv 2602.10200v2), p34, Appendix, Table A1, row UMi, cols. 14-16. | page: 32; 33; 34 · row: Aqr2; Aqr3; Boo2; CVn1; CVn2; Col1; CB; Dra; Hyd2; Leo4; Leo5; Leo6; LeoT; Peg3; Peg4; Pisc2; Scl; UMa1; UMa2; UMi |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row UMi, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: UMi · column: re |
| Distance | Garofalo2025A&A...695A..88G PDF p.6, Section 3.1. Read as the distance modulus. | page: 6 · section: 3.1 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Geha2026arXiv260210202G, p.19, Appendix, Table A1 (Derived Properties of Milky Way Satellites Observed with Keck/DEIMOS), row Ursa Minor UMi (mean [Fe/H], spectroscopic). | page: 17; 18; 19 · row: Aquarius III Aqr3; Bootes II Boo2; CVn I CVn1; CVn II CVn2; ComaBer CB; Draco Dra; Herc Herc; Hydra 2 Hyd2; Leo I Leo1; Leo II Leo2; Leo IV Leo4; Pegasus 3 Peg3; Pegasus 4 Peg4; Segue 2 Seg2; UMa 1 UMa1; UMa 2 UMa2; Ursa Minor UMi |
| Gas | Putman et al. 2021 Table 1, row "Ursa Minor"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Ursa Minor") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |

### Willman 1

| Input | Read from | Place (locator) |
|---|---|---|
| σ | Chiu 2026 ApJ 1002 55 (arXiv 2602.20272v2), p8, Sect. 4.1; p7 Table 2 (footnote b: cited value); p1 abstract. | page: 8; 7; 1 · table: 2 · section: 4.1 |
| r_h and ε | Munoz2018ApJ...860...66M p.27, Table 5, Primary Sample, row Willman 1, col re,s (arcmin). Convention: semi-major (assumed, D-052 item 2). | page: 27 · table: 5 · row: Willman 1 · column: re |
| Distance | Willman2006astro.ph..3486W §3.1, p. 3. Read as the distance in kpc. | page: 3 · section: 3.1 |
| m_V,0 | Munoz 2018 M_V + 5 log10(D/10 pc), D = [value] (Table 1; D-061 item 3). | table: 6 (M_V); 1 (R, the distance) |
| [Fe/H] | Chiu2026ApJ..1002...55C, p.7, Table 2 (Properties of Willman 1); also abstract p.1, Sec. 4.2 p.9, Sec. 8 Summary p.16 (mean [Fe/H], spectroscopic). | page: 7; 1; 9; 16 · table: 2 · section: 4.2; 8 |
| Gas | Putman et al. 2021 Table 1, row "Willman 1"; an upper limit: no gas term | table: 1 · row: the galaxy's row: the name in column galaxy_as_printed ("Willman 1") · column: l_MHI, MHI and Dist |
| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |
