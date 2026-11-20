# BBK reader notes: Bullock & Boylan-Kolchin 2017 (ARA&A 55, 343), arXiv 1707.04256v2

Reader: BBK. Date: 2026-11-18. Brief: `brief.md` in this folder.

## Pages read

- PDF sha256 checked: `a5abbf831b67974f...`, which matches the brief.
- I read PDF pages 1–42 in full from `/home/claude/reviews/1707.04256.txt` (form-feed page n equals PDF page n equals printed page n). That includes all figure captions, the margin notes, the sidebars ("Adopted dwarf galaxy naming convention", "We define small scales", "Robust predictions from CDM-only simulations", "Three challenges to basic ΛCDM predictions", "Scale where feedback becomes ineffective", "The challenge of detecting empty dark matter halos") and the footnotes. Page 42 holds the end of the acknowledgments and the start of the reference list. I did not read the reference list.
- I opened these pages as images from the PDF, because they contain figures or garbled text: 4 (Fig. 1), 11 (Fig. 3), 20–26 (Figs. 7–12), 28 (Fig. 13) and 34 (Fig. 15).
- The garbling is systematic and minor. pdftotext drops or replaces some symbols: M★ appears as "M?", ⊙ is dropped, ≲/≳ appear as ".", and ϵ in the Fig. 3 caption is lost. I read all of these from the page images where they mattered. No page was unreadable.
- I read pages 7, 12, 14, 15, 29 and 33–35 (theory and simulation figures: the power spectrum, mass functions, abundance matching, FIRE-2 profiles, WDM/SIDM) from their captions and the surrounding text only. Their axis text is garbled in the extraction, but none of them shows an observed system beyond what the captions state.
- One discrepancy, recorded as found: the Fig. 12 caption (p. 26) says "2700 individual data points from 153 galaxy rotation curves", while the plotted panel is labelled "2693 points". The review does not name the sample. SPARC is not mentioned anywhere in pp. 1–42, so the CSV row cites McGaugh, Lelli & Schombert (2016) as the review does.

## Classification rule used

- The `item_kind` value `outside` is used for evidence that compares no pull with detected matter. This covers counts, spatial planes, mass functions, the CMB, the Lyman-α forest, annihilation and decay searches, and stream gaps.
- Rows where an inferred dynamical mass, density or circular velocity is compared with a predicted halo rather than with the detected baryons are kept as `route`/`type`/`system` with channel `dynamics`. They are listed below as boundary routes, because the measurement itself is a dynamical one even when the comparison is not with g_bar.

## Boundary routes (do not compare an observed pull with the pull of detected matter, but sit close)

- Inner density slope from rotation curves, cusp versus core (p. 21–22; DDO 126 and DDO 43, LITTLE THINGS). This is a profile shape.
- The "central density problem": central enclosed mass against the abundance-matched halo (p. 21).
- Too-big-to-fail: V1/2 or HI-width circular velocities against the most massive simulated subhalos (pp. 22–24, 30–31).
- The velocity function of field galaxies (pp. 23–24). It mixes counts and velocities.
- Rotation-curve diversity, Vc(2 kpc) against Vmax, compared with dark-matter-only expectations (p. 26–27). The review adds that the spread correlates with baryonic content, which brings it close to the RAR.
- Central densities of galaxy clusters used to bound self-interaction cross-sections (p. 35). The measurement method is not stated.
- Abundance matching and the galaxy size versus 0.015 Rvir relation (pp. 11, 13–15). These link observed galaxies to predicted halos and are used throughout as the reference for the dynamical comparisons.
- Masses within 300 pc of lensing-detected subhalos compared with luminosity upper limits (p. 38). This is close to a direct mass-to-light comparison in the lensing channel. It is recorded as a `route` with channel `lensing`.
- Comparisons that are direct (observed pull against detected matter) are the baryonic Tully-Fisher relation (p. 26), the radial acceleration relation (pp. 26–27, 32), the dSph mass-to-light ratios (p. 3) and the 1970s rotation curves (p. 16).

## Test cases the review names as contested between the two sides

- **Milky Way satellite plane** (pp. 24–25, 31). Kroupa, Theis & Boily 2005, Metz, Kroupa & Jerjen 2007/2009 and Pawlowski et al. 2012/2013/2015 are set against Zentner et al. 2005, Kang et al. 2005, Libeskind et al. 2009 and Lovell et al. 2011. The disputed points are filamentary accretion and sky coverage (SDSS, DES; Pawlowski 2016).
- **M31 satellite plane** (pp. 25, 31). Whether it is rotationally supported is disputed: work rooted in ΛCDM finds similar but non-rotating planes (Bahl & Baumgardt 2014; Gillet et al. 2015; Buck et al. 2016). The plane is seen edge-on, and proper motions are proposed as the test.
- **Co-rotating satellites in SDSS** (pp. 25–26). Ibata et al. 2015 is set against the re-analysis of Phillips et al. 2015.
- **Field velocity function / too-big-to-fail in the field** (pp. 23–24, 31). Macciò et al. 2016 and Brooks et al. 2017 argue there is no discrepancy. The inputs disputed are HI extent, pressure support and inclination (Papastergis & Ponomareva 2017; Kormendy & Freeman 2016).
- **Radial acceleration relation** (p. 27 footnote 6; p. 32). The review says this type of relation is generally expected in MOND. Keller & Wadsley 2017 and Navarro et al. 2016 argue that ΛCDM can produce a similar relation. The review states that low-mass galaxies remain the open case.
- Open, but not framed as two sides: lensing subhalo masses against Milky Way satellite masses (p. 38: "lens modeling" or a real difference); whether stream gaps exist at all (p. 38); and simulation disagreement on feedback cores (Sawala et al. 2016 find no cores, Read, Agertz & Collins 2016 find cores at all masses; p. 30).

## Scan check

I ran `python3 -I scan_names.py 1707.04256 BBK`: 38 names found, 6 not in the CSV, all false matches.

Scan false matches (not in the CSV):
- `M 1.0`, `M 107`, `M 4.1` (p. 29): stellar-mass labels from the Fig. 14 panel text ("M? =4.7×105 M ... 4.1×106 M ... 1.0×107 M").
- `M 1.5.2.` (p. 16): a section number following a solar-mass symbol ("... M 1.5.2. Kinematic Measures").
- `M200`, `M200m` (p. 8): halo-mass definitions, not objects.

Names the scan matched in the CSV that are false matches in substance (they appear in the CSV only inside another row's text):
- `Aquarius` (pp. 22–23): the Aquarius N-body simulation, not the Aquarius dwarf. It appears in the too-big-to-fail row as a simulation name.
- `Willman` (pp. 3, 19, 36): an author name (Willman 2010; Hargis, Willman & Peter 2014; Willman & Strader 2012).
- `Malin` (p. 37): an author name (Impey, Bothun & Malin 1988), carried in the ultra-diffuse galaxy row.
- `M300` (p. 38): a mass label, but it sits inside a real use (Strigari et al. 2008 row).
- `Galaxy` is the review's name for the Milky Way (pp. 6, 12, 13, 20, 24, 36, 38). It is covered by the Milky Way rows.
- `Sun` (p. 40) is covered by the Solar System sidebar row.
- `Local Group` (pp. 1–38) is covered by the Local Group rows (pp. 19, 23, 30, 38).

## Row counts by item_kind

| item_kind | rows |
|:--|--:|
| system | 38 |
| type | 26 |
| route | 14 |
| outside | 29 |
| **total** | **107** |

Of these, 36 rows have `how_used` starting with "mentioned, not used as a test:".
