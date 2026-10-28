# aeg-d-sparc/v1 — source

**SPARC** (Spitzer Photometry and Accurate Rotation Curves): mass models for 175 disc galaxies. Lelli, F., McGaugh, S. S. & Schombert, J. M. 2016, AJ 152, 157 (arXiv:1606.09251). Maintainers' site: https://astroweb.case.edu/SPARC/ (read 2026-10-28; page last updated 29 May 2020). Archival copy: CDS/VizieR J/AJ/152/157.

Full reading notes: `docs/sources/sparc.md`.

## Terms

The maintainers' site states no licence. It asks that the master paper be cited, and the original rotation-curve sources where relevant (listed per galaxy in SPARC Table 1). Under D-004 (amended), the terms of the archival CDS/VizieR copy apply; the licence line of that specific record is still to be read (backlog D1). Until then `redistributable` is recorded as false: source files are fetched at build time and never committed.

## Method (as read at source)

- g_obs = V_obs² / R (arXiv:1610.08981 eq. 1).
- g_bar = (|V_gas|V_gas + Υ_disk |V_disk|V_disk + Υ_bul |V_bul|V_bul) / R (arXiv:1606.09251 eq. 2). The table gives V_disk and V_bul for Υ = 1; V_gas includes a factor 1.33 for helium.
- Catalogue defaults: Υ_disk = 0.5, Υ_bul = 1.4 Υ_disk = 0.7 M☉/L☉ at 3.6 µm, "as suggested by SPS models" (arXiv:1606.09251; arXiv:1610.08981 Table 1).
- Values of Υ_disk explored by the source: 0.2 (as suggested by the DiskMass survey) and 0.7 (mean maximum-disc limit in bright galaxies) (arXiv:1606.09251 abstract).
- g_obs uncertainty: δg_obs = g_obs √[(2δV/V)² + (2δi/tan i)² + (δD/D)²] (arXiv:1610.08981 eq. 2).
- g_bar is independent of distance (arXiv:1610.08981 §II.1.2).
- A change in inclination changes the normalisation of the rotation curve without altering its shape (arXiv:1606.09251 §III.2).

## Cite

Lelli, McGaugh & Schombert 2016, AJ 152, 157; plus the rotation-curve source for each galaxy shown (SPARC Table 1, column Ref.).
