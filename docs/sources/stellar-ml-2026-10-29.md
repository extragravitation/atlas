# Stellar mass-to-light ratio: sources read (2026-10-29, D-039)

Read at source by Claude (AI) on 2026-10-29, for issue #45 and D-039. Model values only; no dynamical mass or dynamical mass-to-light value is recorded here.

## Model sources (read before the ruling)

| Source | What was read | Content used |
|---|---|---|
| McLaughlin & van der Marel 2005, ApJS 161, 304 (arXiv:astro-ph/0605132) | §3.1–3.2, Table 8 description | Bruzual & Charlot (2003) and PÉGASE; IMFs Chabrier disk (adopted), Salpeter, Kroupa et al. 1993, Chabrier GC; age 13 ± 2 Gyr with Harris [Fe/H]; the two codes agree within ~10% in Υ_V; Salpeter 60–75% above Chabrier; Kroupa and Chabrier converge at old ages; Galactic GCs concentrated near Υ_V ≈ 1.9 with a metal-rich tail. Per-cluster values in Table 8 (BC03, Chabrier, column 6). |
| Maraston 2005 (arXiv:astro-ph/0410207) | text | Salpeter and Kroupa IMFs; remnants included (Renzini & Ciotti 1993); [Z/H] −2.25 to +0.67; Salpeter ≈ 1.5× Kroupa in M/L, nearly independent of metallicity. Tabulated values not read. |
| Kruijssen & Mieske 2009 (arXiv:0903.4683) | §2, Table 1 (canonical column), Eq. 5 | Kroupa IMF, Padova isochrones, remnants included; canonical Υ_V ≈ 1.99 at [Fe/H] ≈ −2.3 to 2.68 at −0.76 (12 Gyr); dissolution factor Q = 0.53–1.00 for their sample. |
| Woo, Courteau & Dekel 2008 (arXiv:0807.1331) | §2.1, Tables 1–2 | Dwarfs: BC03 with Chabrier IMF from star-formation histories (Mateo 1998), and Bell & de Jong colour relations; per-galaxy Υ_V 0.5–1.8 for dE/dSph; medians 1.6 (SFH) vs 1.3 (colours); typical 0.17 dex in log M★. |
| Pace 2025, Local Volume Database (arXiv:2411.07424) | §3.4, Fig. 7 caption | "a mass-to-light ratio of 2" for all systems; no band, source or uncertainty stated. |

## Read after the ruling (D-039 items 2 and 4)

**Baumgardt, Hénault-Brunet, Dickson & Sollima 2023, MNRAS (arXiv:2303.01636), "Evidence for a bottom-light initial mass function in massive star clusters".** Read: abstract, §2, §3.1, §4.1, §4.3, §5 (via ar5iv and the arXiv PDF).
- Data: HST photometry for 91 Milky Way and 29 Magellanic Cloud clusters; Gaia DR3 for membership.
- **Masses depend on the motions.** §4.3: the global mass functions and masses come from N-body model grids fitted by χ² to the surface-density profile, the mass-function slopes at several radii **and the observed velocity dispersion profiles** (line-of-sight and proper-motion sources in Table C1). Only a subset of six clusters (§4.1.1) has mass functions from star counts alone, used to test the low-mass slope.
- **Consequence under D-036 #6 and D-039 §4:** the global stellar masses of this source are not independent of the motions and cannot be used as the counted-mass alternative. The six star-count-only mass functions (§4.1.1) are partial in radius; whether they give an independent total mass is to be checked.
- IMF conclusion (§5, in words): fewer low-mass stars than Kroupa (2001) or Chabrier (2003) ("bottom-light"); no variation with metallicity, mass or density found. This conclusion rests partly on the kinematics-fitted models.

**Filion et al. 2024, ApJ 967, 165 (arXiv:2404.11571), "The low-mass stellar initial mass function in nearby ultrafaint dwarf galaxies".** Read: abstract, data, conclusions.
- HST ACS star counts in Reticulum II, Ursa Major II, Triangulum II and Segue 1, about 0.2–1 M☉.
- IMFs consistent with the Milky Way form (Kroupa or Chabrier) are not rejected in any of the four; no evidence of systematic variation; Ursa Major II favours a bottom-heavier form but may be contaminated. Earlier claims of shallower-than-Salpeter single slopes (Geha et al. 2013; Gennaro et al. 2018) are discussed; single-slope comparisons with Salpeter are not straightforward.

## Assessment against D-039 item 2 (Chabrier/Kroupa default)

- Dwarf galaxies: the direct star-count evidence read (Filion et al. 2024) is consistent with the default.
- Globular clusters: the evidence read (Baumgardt et al. 2023) points to fewer low-mass stars than Chabrier, which would lower the ratio. That conclusion rests partly on fits to the motions, so adopting it as the baryonic default would breach D-036 #6. The direction of the effect lies inside the ruled cluster range (down to about 0.5×).
- Neither source supports a Salpeter-like low-mass IMF in these systems.
- Returned to JvH under D-039 item 2 (2026-10-29).

## Not yet read

The Bruzual & Charlot (2003) model tables (to be fetched, hashed and read at source when the interpolation code is written and frozen); McLaughlin & van der Marel (2005) Table 8 itself (VizieR J/ApJS/161/304).
