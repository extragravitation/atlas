# High-redshift source survey (2026-10-29, D-033)

One survey session on 2026-10-29, read at source to the depth stated; "unverified" means not confirmed. **Nothing has been fetched, hashed or converted, and nothing is ruled.** AI-assisted (Claude); the eligibility notes at the end were checked against the Atlas rules afterwards.

## 1. Rotation curves of individual galaxies, z ≈ 0.3–3.5

| Candidate | z | Observed side | Baryonic side (stars; gas) | Public data | Terms | N | Status |
|---|---|---|---|---|---|---|---|
| RC100, Nestor Shachar et al. 2023, ApJ 944 (arXiv:2209.12199) | 0.6–2.5 | Hα/CO, forward-modelled (DYSMAL/DysmalPy), pressure correction (Burkert et al. 2010); disc + bulge + NFW model | SED stellar masses; gas from the Tacconi et al. 2020 scaling relation | RC100 tables not stated; parent KMOS3D and SINS cubes public | not stated | 100 | not released |
| MUSE-DARK III, Ciocan et al. 2026, A&A 709, L16 (arXiv:2604.22613) | 0.33–1.44 | g_obs from best-fit disc + halo (DC14) models; GalPaK3D; pressure-corrected; r < 2 kpc excluded | stellar M/L derived; gas folded into a disc normalised by M★ (method unverified) | no data statement found | article CC BY 4.0 | 79 | unverified, likely not released |
| MUSE-DARK I, Ciocan et al. 2026, A&A 708, A112 (arXiv:2506.19721) | 0.3–1.5 | as above (α = 0.92 pressure correction) | as above | §6.3 data availability not readable | CC BY 4.0 | 127 | unverified |
| KROSS, Sharma et al. 2021, MNRAS (arXiv:2005.00279) | 0.57–1.04 | 3DBarolo; pressure correction raises velocities 30–50 % | SED stellar masses; **no gas** | KROSS website; Dataverse catalogue of 344 | not stated | 256 | observed side obtainable; no g_bar |
| ALPAKA, Rizzo et al. 2023, A&A 679, A129; Roman-Oliveira et al. 2026 (arXiv:2601.03338) | 0.5–3.5 | CO/[CI], 3DBarolo, small asymmetric-drift correction | JWST stellar profiles (mass free); **gas from the ALMA line profile** times a conversion factor (not a scaling relation) | raw ALMA and JWST public; derived curves only in paper tables | article CC BY 4.0 | 28 (3 with full mass models) | derived products not released |
| Lelli et al. 2023, A&A (arXiv:2302.00030) | 1.47, 2.24 | CO rotation curves, g = V²/R | assumed stellar M/L; CO gas with fitted normalisation (one prior ties gas to M★) | raw data only | not stated | 2 | not released |
| KMOS3D data release, Wisnioski et al. 2019 (VizieR J/ApJ/886/124) | 0.38–2.7 | cubes only | M★ column; no gas | VizieR, MPE | cite the paper | 739 cubes | raw only (would require new analysis) |

Interpretations differ between sources: RC100 reports little discrepancy on galactic scales; Sharma et al. 2021 report flat curves like local ones; Lelli et al. 2023 describe disc–halo degeneracy. The Atlas takes no side.

## 2. Galaxy–galaxy lensing

KiDS-1000 (Brouwer et al. 2021, already in the Atlas): lenses at z ≈ 0.1–0.5 (source statement; not yet recorded in the package); the released ESD profiles could be binned by lens redshift only with new analysis. No redshift-binned lensing release at z ≳ 0.5 was found (unverified absence).

## 3. Galaxy clusters

| Candidate | z | Observed side | Baryonic side | Public data | Terms | N | Status |
|---|---|---|---|---|---|---|---|
| CLASH RAR, Tian et al. 2020, ApJ 896, 70 (arXiv:2001.08340) | 0.187–0.686 | strong + weak lensing (Umetsu et al. 2016) evaluated through NFW posterior fits | Chandra gas (Donahue et al. 2014); BCG Hernquist model; member-galaxy stars from a mean correction calibrated on SPT (Chiu et al. 2018) | VizieR J/ApJ/896/70 | VizieR (licence per record to be read) | 20 | obtainable |
| CLASH-X, Donahue et al. 2014 (arXiv:1405.7876) | 0.187–0.890 | Chandra/XMM hydrostatic profiles | gas; no stars | MAST listing unverified | not stated | 25 | unverified |
| SPT/XMM, Bulbul et al. 2019, ApJ 871, 50 (arXiv:1807.02556) | 0.2–1.5 | integrated values; R500 from SZ scaling | ICM mass in R500 | no profiles | — | 59 | not usable as profiles |
| SPT + XMM, Sarkar et al. 2025 (arXiv:2504.00113) | 0.16–0.35 | hydrostatic profiles to R200 | gas; stellar fraction from simulations | no release stated | — | 8 | not released |

## 4. Compilations testing redshift dependence

MUSE-DARK III reports a characteristic acceleration at z ≈ 1 that rises with redshift, a form its authors call phenomenological; its g_obs is model-derived and no data release was confirmed. Tian et al. 2020 do not test redshift dependence.

## Eligibility under the Atlas rules (checked 2026-10-29)

The survey was briefed to treat scaling-relation gas as ineligible. That is stricter than the rules: D-029 excludes only **observed-side** masses from scaling relations; a fitted total-mass profile (e.g. NFW) is **included with `model_dependence = total_mass_form`**, and a modelled baryon component is included with its status `modelled` (as KiDS's gas already is). Under the rules as ruled:
- **CLASH (Tian et al. 2020, z 0.19–0.69)** appears eligible for the cluster lensing cell (A9) with labels: total-mass form (NFW) on the observed side; member-galaxy stars modelled. It would extend cluster coverage to z ≈ 0.7. Eligibility is decided under the protocol (§6 of `docs/plans/TAXONOMY.md`) from metadata, before any plot.
- **Galaxies at z ≳ 0.3:** no machine-readable release found with both sides; ALPAKA (measured gas) is closest, with derived products in paper tables only. Requests to the ALPAKA, MUSE-DARK and RC100 teams would be the route.

Open questions: whether CO/[CI] gas (line luminosity times an assumed conversion factor) is labelled measured or modelled; whether the Umetsu et al. 2016 non-parametric profiles and the Donahue et al. 2014 gas profiles are released (would allow a CLASH package without the NFW step).
