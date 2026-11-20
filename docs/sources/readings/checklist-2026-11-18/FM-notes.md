# FM reading notes: Famaey & McGaugh 2012 (arXiv 1112.3960v2)

Reader: FM. Brief: `brief.md` in this folder (committed 2026-11-18).
PDF sha256 (first 16) checked before reading: `bb226b40f570df0b` (matches the brief).

## Pages read

- PDF pages 1 to 130, every page, in order, from `/home/claude/reviews/1112.3960.txt` (pdftotext layout, split on form feeds; 165 pages in the file, range ends at 130 as the brief says). Figure captions, tables (Table 1 p 70, Table 2 p 130) and footnotes were read.
- Reference list (pages 131 onwards) not read. No system needed identifying from a citation alone.
- Pages with no recordable item: 1 to 5 (abstract, contents, introduction), 43 to 44, 47 to 49, 51, 55, 87 to 88, 90, 92, 95 to 97, 100, 111, 116, 120, 125, 128 to 129. These are theory, formalism or discussion with no system, type or route used as a test; items they repeat are recorded at their first use.

### Pages that needed the PDF image

- **p 62 (Figure 24), p 64 (Figure 26), p 65 (Figure 27):** galaxy names appear only inside the plot panels, not in the extracted text. Read from the PDF image. Names recorded: UGC 2953 and UGC 2487 (Fig 24); DDO 154, IC 2574, NGC 3621, NGC 5055, NGC 2903, NGC 3521, NGC 7331, NGC 2841 (Fig 26); F583-4, F583-1, F563-V2, F563-1, F568-3, UGC 1230 (Fig 27). Because these names are not in the text, `scan_names.py` cannot see them. They are in the CSV anyway.
- **p 63 (Figure 25):** checked on the image. The panel names (DDO 210, UGC 11583) match the caption.
- Figures that are only plots, with nothing to name beyond the caption (Figs 2 to 11, 14 to 16, 19, 20, 28 to 30, 35 to 40, 44 to 48), were handled from their captions. Figures 12, 31, 33, 34, 41 to 43 are images of named systems. Their names are in the captions.
- Garbled equations (pp 36 to 56, 86, 89 to 101) are theory only. No value was read from them.

### Recording conventions

- `scale` uses the brief's list. Where a route spans several scales it is written `other (dwarf galaxy to cluster)` and so on.
- Rows for a figure carry the figure's page. A few named systems have more than one row because the review uses them for different tests: NGC 6946, NGC 1560, M33, the Bullet Cluster, Fornax, Pal 14, NGC 2419, the Local Group and the Milky Way.
- `quote` was checked automatically. Every quote has fewer than 15 words and appears verbatim (ignoring whitespace and hyphenation) in the text of the page it is filed under or the page next to it. For panel-only systems the quote is the figure caption.
- `how_used` describes the comparison only. The review's verdict words ("success", "problematic", Table 2 grades) were not copied into it.

## Routes close to the boundary (not a straight observed-pull versus detected-matter comparison)

- Cusp versus core and Einasto-index fits (p 15, p 29): this is profile shape. It is inferred from rotation curves, but it tests the shape of a fitted halo, not g_obs against g_bar.
- Central surface density of fitted halos, about a0/(2πG) (p 30, p 39): this is a property of fitted mass models.
- Freeman limit, and the distribution of disk surface density and size (pp 24, 26): a population property with no dynamics. The review ties it to disk stability.
- Disk stability, bar growth, bar pattern speeds, rings, warps (pp 6, 16, 70 to 72): these test whether there is enough disk self-gravity relative to a halo potential. The comparison is indirect and made through simulations.
- Missing satellites, masses within 300 pc of Milky Way satellites, the satellite phase-space disk, bulgeless disk fraction, angular momentum (pp 14 to 15): these are counts, geometry and formation statistics. The 300 pc masses are dynamical, but they are compared with predicted subhalos, not with detected baryons.
- Bullet Cluster collision speed and cluster bulk flows (pp 13, 126): kinematics compared with infall expectations from simulations, not a pull-versus-matter comparison. The Bullet Cluster's lensing-versus-gas-position use (p 104) is a separate row and is a direct comparison.
- Compact-group merger timescales and dynamical friction on Fornax's globular clusters (pp 72, 82): orbital decay timescales.
- Tremaine-Gunn neutrino phase-space limit (p 86): compares a required unseen density with what a hypothesised component could supply.
- Gravitational redshifts of galaxies in 7800 clusters (p 106): a third channel, neither dynamics nor lensing. Channel recorded as `unclear`.
- Gravitational slip from lensing plus peculiar velocities (p 109): compares the two channels with each other on cosmological scales.
- Detected baryon fraction f_d versus potential well (pp 16 to 17), and cluster baryon fraction versus radius (p 82): these are a direct comparison, but expressed against a cosmic baryon fraction.
- Laboratory low-acceleration inertia tests, LISA Pathfinder saddle points, negative phantom-density lensing pockets, lopsided cluster ellipticals (pp 45, 57 to 58, 77, 104): proposed tests with no data cited. Recorded as `mentioned, not used as a test`.

## Test cases the review names as contested

- Oort discrepancy (p 6): "largely (though perhaps not fully) gone away".
- BTFR slope from single-dish line-widths versus resolved V_f (p 20, footnote 12).
- Stellar M/L systematics as a way out of the BTFR residual argument (p 22). Maximum disk versus dark-dominated disks (pp 22, 27, 31).
- NGC 1560 wiggle: possibly non-circular motions from spiral arms (p 32, footnote 16).
- NGC 3198: possible Cepheid distance problem (pp 67, 124). NGC 2841: historically a problem, said to be resolved with modern data (p 67).
- Local surface density and velocity-ellipsoid tilt in the Milky Way (p 70, Table 1): the review says a round halo with no disk is also compatible, and the tilt at 2 kpc is more discriminating.
- HI flaring at 10 to 15 kpc in the Milky Way (p 69), and layer thickness in external galaxies (p 71): a possible underprediction, or non-gravitational support.
- LSB vertical velocity dispersion of about 8 km/s (pp 71, 122 to 123): usually attributed to non-gravitational phenomena. The review says it is not yet a test.
- NGC 7507 (p 78): the review's fit is set against the claim of ref. [376].
- Satellites of isolated ellipticals, stacked SDSS (p 78): a 10σ exclusion was claimed for constant anisotropy, and good fits were found with varying anisotropy.
- Classical dwarf spheroidals (p 79): equilibrium and membership disputed for Sextans (interlopers), Draco and Ursa Minor (out of equilibrium). Carina's M/L is called suspiciously high.
- Ultra-faint dwarfs (pp 79 to 80): equilibrium, the 2 versus 5 km/s dispersion systematics, and stochastic M/L.
- Globular clusters Pal 3, Pal 14, NGC 2419, NGC 1851, NGC 1904 (pp 81 to 82). NGC 2419 is "heavily debated", and may be a stripped nucleus in the Virgo stream.
- Fornax globular clusters and dynamical friction (p 82): depends on their initial orbits.
- Tidal dwarfs in NGC 5291 (pp 74 to 75): only three objects, and inclination assumed from the ring geometry.
- Galaxy clusters, X-ray hydrostatics (pp 82 to 87, 125 to 126): a residual factor of about 2. Each side's normalisation and slope are discussed.
- Galaxy-lens M/L (p 103): a claimed missing mass in lenses, which depends on the transition function used.
- Galaxy-galaxy weak lensing at L > 1e11 Lsun (p 104): the result is driven by one data point.
- Bullet Cluster (pp 104 to 105, 126): "an outstanding challenge for all MOND theories" and also a challenge to ΛCDM on collision speed. The shock velocity correction is in footnote 71.
- Abell 520 (p 105): a counter-example to the Bullet Cluster pattern. Cl0024+17 (pp 105 to 106): the ring may be an analysis artefact, and reproducing it depends on the transition function.
- Gravitational redshifts in clusters (p 106): the first analysis is disputed.
- CMB second-to-third peak and lithium versus CMB baryon density (pp 115 to 118): the third peak's sensitivity to beam corrections (footnote 62), and lithium depletion is disputed.

## Scan check

`python3 -I scan_names.py 1112.3960 FM`: 64 names found, and 2 are not in the CSV (`F2body`, `M500`). I went through every reported name, including those the script counts as present, because several only match by accident:

### Scan false matches

- `F2body` (p 46): an equation symbol for the two-body force, Eq. 24.
- `M500` (pp 17, 38): the mass within R500 in Figure 2 and in Kepler-like law 4. A variable, not an object.
- `M1`, `M2`, `M3` (pp 47 to 50, 56) and `M 3` (p 46): grid points in the discretisation scheme (Figure 17, Eqs. 25 and 35), and a term in Eq. 22. The script counts them as present only because they are substrings of "M33". They are not objects.
- `Kepler` (pp 2, 35 to 37 and others): Kepler's laws and "Kepler-like laws", not the Kepler mission. Its only object-like use is "Kepler's constant" for the inner planets (p 57), which is recorded as a route.
- `NGC 1543.`, `NGC 1560.`, `NGC 2419.`, `NGC 6946.`, `NGC5291W.`: the same objects with a trailing full stop. They are recorded without it.

### Names present as real items

Abell 2218, Abell 2390, Abell 520, Andromeda/M31, the Bullet Cluster (1E0657-56), Carina, the Centaurus spiral arm, Cl0024+17, DDO 210, Draco, ESO 509-98, Fornax, Gaia (mentioned), Galaxy (= Milky Way), KK98 250 (= UGC 11583), Leo I, Leo II, the Local Group, the Local Void, the Local Volume, M33, the Magellanic Clouds, the Milky Way, NGC 1543, NGC 1560, NGC 1851, NGC 1904, NGC 2419, NGC 2841, NGC 3198, NGC 5291 (with N, S, W), NGC 6946, NGC 7507, Oort (discrepancy), Pal 14, Pal 3, Pioneer, Sagittarius (stream), Saturn, Sculptor, Sextans, Shapley (supercluster), Solar System, Sun (mentioned), UGC 11583, UGC 2487, UGC 2885, Ursa Minor, Virgo (stream, mentioned).

Objects outside the script's patterns, recorded by hand: XMMU J2235.3-2557, the Sloan Great Wall, Q2237+030 (Einstein cross, Huchra's lens), the Antennae, Mars, UGC 2953, UGC 1230, DDO 154, IC 2574, NGC 3621, NGC 5055, NGC 2903, NGC 3521, NGC 7331, F583-4, F583-1, F563-V2, F563-1, F568-3.

## Row counts by item_kind

| item_kind | rows |
|:--|--:|
| route | 123 |
| system | 77 |
| type | 49 |
| outside | 43 |
| **total** | **292** |

24 of the 292 rows have `how_used` beginning `mentioned, not used as a test:`.
By channel: dynamics 209, neither 61, lensing 17, both 3, unclear 2.
