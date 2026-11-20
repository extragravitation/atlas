# CSZ reading notes: Cirelli, Strumia & Zupan, arXiv 2406.01705v3

Reader: CSZ. Brief: `brief.md` (committed 2026-11-18), D-111 page ranges.
PDF hash checked: sha256 starts `b2aa18f6fb5b0fca`, matching the brief.

## Pages read

- PDF pages 15–68 (Chapter 1 "Why? Evidence for Dark Matter"; Chapter 2 "Where? Dark Matter distribution in the Galaxy and the Universe", up to the end of §2.5).
- PDF pages 300–310 (§8.3 tail, §8.4 cosmology anomalies, §8.5 astrophysics anomalies, §8.6).
- PDF pages 394–406 (Chapter 11 "Alternatives to Dark Matter", §11.1 to §11.5).

All 78 pages were read in full from the `pdftotext -layout` text, including captions, tables and footnotes. No page outside these ranges was read. I did not consult the reference list.

### Pages that could not be read properly from the text, and how I handled them

- p19 (Fig. 1.2), p395 (Fig. 11.1), p397 (Fig. 11.2): the plot labels are mixed into the text. I rendered these PDF pages and read the figures and captions.
- p53 (Table 2.3): the column layout and the group labels (classical / confirmed ultrafaint / candidates) and the `*` flags were unclear in the text. I rendered the page. Groups confirmed: Sagittarius is set apart below the classical eight; Willman 1 to Leo Minor I are "confirmed ultrafaint"; Triangulum II to Ursa Major III are "candidates".
- p22 (Fig. 1.3), p24 (Fig. 1.4), p26 (Fig. 1.5): axis values are mixed into the captions. I used the captions only; they name no further systems.
- p49 (Fig. 2.3), p59 (Fig. 2.5), p61 (Fig. 2.6): axis labels are garbled. These are model profiles and simulated speed distributions, with no observed system. I used the captions.
- Many equations are garbled (e.g. pp. 18, 21, 27–38, 42–45, 402–405). None of them carries a system or a measurement route, so I did not render them.

## Routes near the boundary (no comparison of observed pull with detected-matter pull)

These rows are `outside` (or noted as boundary cases) in the CSV:

- Cusp versus core / "inner mass deficit": inner profile shape compared with simulations (pp. 48, 54, 304; Sculptor p54). Footnote 15 (p304) restates it as the mass inside a radius, which comes closer to a pull comparison.
- Diversity problem: spread of inner rotation curves at the same maximum velocity, compared with simulations (p305).
- Halo shape: stacked weak lensing (p64, `outside`); the Sagittarius stream and Gaia kinematics for the shape of the Milky Way potential (p64, entered as `system` because it is stream fitting of the potential, but the test is the shape, not the comparison with detected matter).
- Inner density slope of clusters from lensing, compared with simulated profiles (p55).
- Dynamical friction as a probe of unseen mass: bar slow-down (p305), the Fornax globular-cluster timing problem (p305–306), binary pulsars and black-hole binaries (pp. 67–68), and a proposed PTA spectral-slope probe (p309). These test a drag from unseen mass, not the size of the pull.
- Too big to fail, missing satellites, planes of satellites, quiescent fractions (pp. 306–307): satellite counts, masses and arrangement compared with simulations.
- Milky Way stellar-to-halo mass ratio used with simulation trends to argue for a cusp (p305).
- Bullet Cluster offsets used to bound a self-interaction cross-section (p23), and its collision velocity compared with LCDM likelihood (pp. 22–23).
- Baryon budget inputs: BBN baryon-to-photon ratio (p39) and cluster-based Omega_DM (p21) measure the matter side or the cosmic mean, not a pull at a system.
- The local circular speed (220 km/s) and local escape speed (544 km/s) measurements (p60) are used only to set an assumed velocity distribution for direct detection. They are entered as `route` with `how_used` beginning "mentioned, not used as a test".

## Test cases the review names as contested between the two sides

- NGC1052-DF2 and DF4 (p20): interpretation "debated". The review uses them both as a challenge to small-galaxy formation and as a strain on modified gravity. p400 point iii and p401 (external field effect) return to them.
- Bullet Cluster (p22 footnote 8 to p23): the collision velocity "had been used as evidence against Dark Matter", disputed by later studies. The lensing–gas offset is used against modified gravity (p23, p400) and is an open issue for the Skordis–Zlosnik theory (p404).
- Baryonic Tully-Fisher relation (pp. 306, 396–399): called "arguably the most important successful prediction from MOND" (p396). The review says it is "unclear" whether LCDM reproduces the relation and its scatter (pp. 398–399).
- Radial acceleration relation and central surface-density relation (pp. 396–398): the open question is whether LCDM gives the tight g_obs–g_bar correlation at low acceleration.
- Dynamical friction (pp. 305–306): bars and Fornax globular clusters are used "to argue against the very existence of DM halos" (Roshan et al.); late bar formation and core stalling are given as the other explanations.
- JWST early massive galaxies (p306; p400 via McGaugh et al. 2024): interpreted by some as evidence for MOND.
- Planes of satellites (p307): an alignment is claimed to work in MOND (Bílek et al. 2017).
- Palomar 14 and NGC2419 (p400): their statistical significance against MOND is "under debate" (eccentric orbits, systematics).
- Galaxy clusters under MOND (p400): MOND "can only partially account" for the missing mass in clusters; undetected baryonic objects are raised as a possibility.
- Cosmic voids (p400 footnote 3): some researchers say voids are too rare in standard cosmology and can be understood in MOND with 11 eV sterile neutrinos.
- External field effect (p401): Chae et al. 2020 statistical detection; Kroupa et al. 2022 asymmetric tidal tails.
- Wide binaries (p401): Banik et al. 2023 (Newtonian, up to 19 sigma) against Chae 2023 (anomaly, up to 10 sigma). The issue named is unseen third bodies.
- Solar System at low acceleration (p401): Oort-cloud simulations (Vokrouhlický et al. 2024) against the Cassini limit on a Saturn-orbit quadrupole (Desmond et al. 2024).
- Weak lensing around isolated galaxies out to about 1 Mpc (p398): "if confirmed", a possible exception for flat curves from DM.
- Weak lensing as a test of superfluid DM (p405, Mistele et al. 2023).

## Scan check

`python3 -I scan_names.py 2406.01705 CSZ` found 59 names and listed 4 as missing from the CSV. Each is a false match:

### Scan false matches

- `F0` (p404): a constant in the function F, eq. near (11.9) ("F0 , F2 and θ̇0 are constants").
- `M 15` (p58): part of the exponent `M 15/8` in eq. (2.22).
- `M1` (p309, p399): binary masses `M1,2`, `M1 M2` in the PTA discussion (p309), and the `M1/3` scaling (p399).
- `M200` (p52): the symbol for the Milky Way mass inside r200, not a catalogue object.

Other scanner hits are in the CSV by name but are partly false matches. They are noted here for the record:
- `Oort` on p21 is the astronomer J. Oort; on pp. 310 and 401 it is the Oort cloud (rows present).
- `Virgo` on pp. 307–308 is the LIGO–Virgo detector. On p53 it is Virgo I and II; on p66 it is the Virgo Supercluster (rows present).
- `M 2`, `M2`, `F2` are equation symbols that happen to match strings already in the CSV.
- `Galaxy` is mostly "the Galaxy" (the Milky Way), entered as "Milky Way (the Galaxy)".
- `Sun` hits on context pages (Sun's position, solar frame) are covered by the Sun and solar-neighbourhood rows; not every passing mention has its own row.
- `Gaia` is entered as a route (p52) and in the Milky Way disk (p66) and wide-binary (p401) rows.

Recording rule I applied: passing context mentions of the Milky Way, the Sun and Gaia (for example the Galactic coordinate system and the direct-detection frame transforms on pp. 58–63) get one row per distinct use, not one row per page. Each dwarf in Table 2.3 has its own row, marked "mentioned, not used as a test" (the table lists J and D factors for indirect searches). Dwarfs that the text uses (Sculptor, Draco, Segue 1, Fornax, Segue 2, Sagittarius) also have use rows.

## Row counts by item_kind

| item_kind | rows |
|:--|--:|
| system | 94 (55 of them are Table 2.3 listing rows) |
| outside | 42 |
| route | 32 |
| type | 26 |
| **total** | **194** |

All quotes were checked by script: each appears verbatim (whitespace-normalised) on the stated PDF page, and each is under 15 words.
