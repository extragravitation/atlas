# First-naming search log (D-049a item 5)

Reader: independent agent (Claude), 2026-10-30. Rule applied: `docs/methods/D049_KIND_BASIS_V2.md` item 5, codes from `docs/methods/D048_KIND_BASIS.md`, X as redefined in D-049 item 1. Output: `kind_coding_first_naming.csv` (one row per system, role `first_naming`).

The task was to find the earliest paper that calls each system a galaxy, and code it by the grounds it gives. The search looked for the first naming only, not for favourable grounds. No velocity dispersion, mass, mass-to-light or acceleration value is recorded; such numbers in quotes are replaced by `[value]`.

## Method and limits

- **Order.** Papers are ordered by arXiv v1 submission date, read from each paper's arXiv abstract page ("Submitted on ..."). Where two candidates fall in the same year, the date decides which is earliest. The `ref` year is the publication year, which matches the arXiv year in every row.
- **Version read.** Quotes are taken from the arXiv v1 PDF where one exists, so that the naming dates from v1. Text was extracted with `pdftotext` and every quote fragment was checked mechanically against the extracted text (whitespace and hyphenation ignored).
- **Citation lists were not reachable.** ADS (ui.adsabs.harvard.edu), Semantic Scholar, INSPIRE, OpenAlex, Crossref and export.arxiv.org were all refused by the session's network proxy, so no "cited by, in date order" list could be pulled. The forward search therefore used:
  1. arXiv's own search (arxiv.org/search) for the system name in all fields, sorted by date, oldest first. This covers titles and abstracts, not full text.
  2. arXiv title searches for satellite and dwarf papers in the relevant years.
  3. The reference lists and introductions of the earliest naming papers found, read backward to find anything earlier.
  4. Direct reading of every candidate paper found by 1–3.
  5. WebSearch (two queries; neither found anything earlier than what is below).
- **Consequence.** A paper that names a system only in its body text, cites the discovery paper, and is not cited by the later papers checked could have been missed. This risk is largest for Segue 1 (a 21-month window) and Segue 2. For the 2015 systems the windows are days to weeks and were checked paper by paper.
- **Collective naming.** A paper is counted when it names a group of systems as galaxies and the group unambiguously contains the system, even if the system is not named in that sentence. This affects Horologium I, Phoenix II and Segue 1. Each row's `reader_note` says what the earliest by-name naming would be, so the main session can see whether the choice changes a code.

## Per system

### Carina III: Torrealba et al. 2018 (discovery), L
- Discovery paper: arXiv:1801.07279, v1 22 Jan 2018, the only version. The abstract says "both Carina II and Carina III are likely dwarf galaxies, although this is less clear for Carina III". The paper adopts this hedged label.
- Nothing can precede the discovery paper. Li et al. 2018 (arXiv:1802.06810, Feb 2018) is later and concludes the kind is undetermined.
- Ground: size–luminosity comparison with the ultra-faint dwarfs and globular clusters (L). The paper says the cluster alternative stays viable for Car III.

### Draco II: Drlica-Wagner et al. 2015 (DES Y2), L (collective ground)
- Discovery: Laevens et al. 2015b, arXiv:1507.07564, v1 27 Jul 2015. It leaves the kind open ("could either be a faint and extended globular cluster or a faint and compact dwarf galaxy").
- arXiv search for "Draco II", oldest first: Laevens 2015b (1507.07564), then Martin et al. 2016 (1510.01326, v1 5 Oct 2015). No title or abstract hit falls between these two.
- Full-text candidates in the window 27 Jul – 5 Oct 2015 that were checked:
  - Yozin & Bekki 2015 (1508.01031, Aug 2015): no mention of Draco II.
  - **Drlica-Wagner et al. 2015 (1508.03622, v1 14 Aug 2015):** names Draco II among "Other recently reported dwarf galaxy candidates" (Fig. 4 caption) and among the "five recently discovered dwarf galaxy candidates located outside the DES footprint" (Fig. 1 caption). It keeps these separate from "systems of ambiguous classification", where it puts Laevens 3. It states the basis of the provisional classification of "these stellar systems": "low surface brightnesses, large physical sizes, large ellipticities, and/or large heliocentric distances".
  - Martin et al. 2016 (1510.01326, 5 Oct 2015) is later. Its grounds are D and M plus metallicity level.
- Chosen: Drlica-Wagner et al. 2015, the earliest found. Code L, but the ground is stated for the group, not argued for Draco II. A stricter reader could code N. The paper attributes the dwarf-galaxy classification to Laevens et al. 2015b, which did not make it.

### Horologium I: Geringer-Sameth et al. 2015, N (collective, unnamed)
- arXiv v1 dates: Koposov et al. 2015a (1503.02079) 6 Mar 2015; Geringer-Sameth et al. 2015 (1503.02320) 8 Mar 2015; Bechtol et al. 2015 (1503.02584) 9 Mar 2015; Drlica-Wagner et al. 2015 Fermi-LAT/DES (1503.02632) 9 Mar 2015.
- Koposov 2015a calls it an "ultra-faint satellite" and leaves the kind open.
- Geringer-Sameth 2015 v1 (Fig. 3 caption) treats "the 8 other newly discovered DES dwarfs" as targets. These are the other eight of Koposov's nine objects, and they include Horologium 1. No ground is stated.
- Earliest by-name naming: Bechtol 2015, one day later: "Its Plummer radius of ~60 pc establishes it as a likely dwarf galaxy" (L).
- Chosen: Geringer-Sameth 2015 under the collective-naming reading. **Uncertain.** The alternative changes the code from N to L. Both papers are 2015, the same year as Koposov 2015a.

### Phoenix II: Geringer-Sameth et al. 2015, N (collective, unnamed)
- Same window and papers as Horologium I. Koposov 2015a puts Phoenix 2 among the six "ultra-faint satellites", kind open. Geringer-Sameth 2015 includes it among "the 8 other newly discovered DES dwarfs".
- By-name candidates, all 9 Mar 2015:
  - Bechtol 2015 lists it as one of eight "dwarf galaxy candidates" but says of it "we cannot draw firm conclusions on its nature". It is already coded X on the sheet.
  - Drlica-Wagner 2015 Fermi-LAT/DES lists DES J2339.9−5424 by name among "DES Dwarf Spheroidal Galaxy Candidates" and computes J-factors. No ground for the label was found in the passages read.
  - Later: Hooper & Linden 2015 (1503.06209, 20 Mar 2015) lists the nine DES "dwarf galaxy candidates".
- Chosen: Geringer-Sameth 2015. **Uncertain** in the same way as Horologium I. Neither alternative gives L, P or G specifically for Phoenix II.

### Reticulum II: Geringer-Sameth et al. 2015, N
- Koposov 2015a (6 Mar): "ultra-faint satellite", kind left open.
- **Geringer-Sameth et al. 2015 (1503.02320, v1 8 Mar 2015):** names it in the title, "Evidence for Gamma-ray Emission from the Newly Discovered Dwarf Galaxy Reticulum 2". No ground is stated. It cites only Koposov's discovery.
- Bechtol 2015 (9 Mar), "almost certainly a dwarf galaxy" (L), is one day later.
- Hooper & Linden 2015 (20 Mar) is later. It gives a size argument (L) for Reticulum II.
- Chosen: Geringer-Sameth 2015, the earliest by date and named by name. All of these papers are 2015.

### Reticulum III: Drlica-Wagner et al. 2015 (discovery), L
- Discovery paper: arXiv:1508.03622, v1 14 Aug 2015: "can be tentatively classified as a dwarf galaxy based on its physical size and low surface brightness". The same sentence is in v1 and v2. The paper's title is "Eight Ultra-faint Galaxy Candidates ...".
- Nothing can precede the discovery paper. Fritz et al. 2019 (1805.07350) is later and inconclusive.

### Segue 1: Martin, de Jong & Rix 2008, N (collective; weakest row)
- Discovery: Belokurov et al. 2007 (astro-ph/0608448, 21 Aug 2006), which calls Segue 1 a globular cluster.
- arXiv search for "Segue 1", oldest first: Belokurov 2007; Walsh et al. 2008 (0712.3054); Geha et al. 2009 (0809.2781); then 2009 papers.
- Papers read in the window Aug 2006 – Sep 2008. Each **does not** adopt a galaxy label unless stated:
  - Liu et al. (astro-ph/0612173, 7 Dec 2006): "probably globular clusters: Willman 1 ... and Segue 1".
  - Gilmore et al. 2007 (astro-ph/0703308, 13 Mar 2007): "probable star clusters Segue 1 and Willman 1".
  - Walsh, Jerjen & Willman 2007 (0705.1378, 10 May 2007): "Willman 1 and Segue 1 straddle the intersection of dwarfs and globular clusters".
  - Martin et al. 2007 (0705.4622, 31 May 2007): calls it "small satellites (such as the structurally similar Segue 1)".
  - Simon & Geha 2007 (0706.0516, 4 Jun 2007): puts it among "3 further new Milky Way satellites that lie in the uncertain parameter space between dwarf galaxies and globular clusters".
  - Koposov et al. 2008 (0706.2687, 19 Jun 2007): "another large globular cluster, Segue 1".
  - Peñarrubia et al. 2008 (0708.3087, 23 Aug 2007): "peculiar systems ... intermediate properties between a dSph and a globular cluster".
  - de Jong et al. 2008 (0708.3758, 28 Aug 2007): groups it with "dwarf galaxies and globulars" and otherwise calls it a "satellite".
  - Walsh et al. 2008 (0712.3054, 19 Dec 2007): "classification ... less straightforward".
  - Madau et al. 2008 (0802.2265, 15 Feb 2008): "lie at the uncertain boundary".
  - Checked with no Segue 1 mention: Strigari et al. (0704.1817, 0709.1510, astro-ph/0611925), Metz et al. (astro-ph/0610933, 0802.3899), 0802.0302, 0805.1058, 0806.3279, 0807.1502, Bovill & Ricotti v1 (0806.2340v1).
  - **Martin, de Jong & Rix 2008 (0805.2945, v1 19 May 2008):** Seg1 is in Fig. 1, "Stellar profiles of the dwarf galaxies", and is counted in "the complete MW dwarf galaxy sample". The same paper hedges ("it might appear more difficult to assign these systems to one population or the other") and excludes Seg1 from its dynamical argument.
  - Tollerud et al. 2008 (0806.4381, v1 26 Jun 2008): "a galaxy like Segue 1". This is the earliest explicit by-name naming found. The table ground stated is large mass-to-light ratios (D).
  - Geha et al. 2009 (0809.2781, 16 Sep 2008): "The Least Luminous Galaxy", D.
- Chosen: Martin, de Jong & Rix 2008, coded N. **Uncertain:** the naming is collective and hedged. If it is not accepted, the next is Tollerud 2008 (D). None of the candidates gives L, P or G.

### Segue 2: Belokurov et al. 2009 (discovery), D
- Discovery: arXiv:0903.0818, v1 4 Mar 2009. In its conclusions, Segue 2 is "the tiny dwarf" in a circular-velocity and halo-mass argument (D). Its keywords are "galaxies: dwarf — galaxies: individual (Segue 2)". Elsewhere it calls the system a "satellite", and its introduction leaves the kind of its analogues open.
- arXiv search for "Segue 2" (many hits are the SEGUE-2 survey and are irrelevant): Belokurov 2009; then Kirby et al. 2013 (1304.6080), "Segue 2: The Least Massive Galaxy".
- Full-text candidates checked: Walker et al. 2009 (0906.0341, v1 1 Jun 2009) lists Segue 2 in "dSph Structural Parameters, Velocity Dispersions and Estimated Masses" (D). Checked with no Segue 2 mention: 0906.1822, 0906.3669, 0908.2995. 0909.3300 cites the discovery paper only.
- Chosen: Belokurov 2009. **Uncertain** whether "dwarf" alone counts as a galaxy label. The fallback, Walker 2009, is also D.

### Triangulum II: Hooper & Linden 2015, N
- Discovery: Laevens et al. 2015a (1503.05554, v1 18 Mar 2015), which is "agnostic about the nature of this object".
- arXiv search for "Triangulum II", oldest first: Laevens 2015a, then Kirby et al. 2015 (1510.03856), Martin et al. 2016 (1510.04433), and so on. No title or abstract hit falls between Laevens 2015a and Kirby 2015.
- Full-text candidates from 18 Mar 2015 onward:
  - **Hooper & Linden 2015 (1503.06209, v1 20 Mar 2015):** "yet another dwarf candidate (Triangulum II)"; Table I lists it as "the new Pan-STARRS dwarf candidate" alongside the dwarf galaxies; analysed as a dwarf-galaxy target. No ground for Tri II.
  - Martin et al. 2015 Hydra II (1503.06216, 20 Mar): no Tri II mention.
  - Kim et al. 2015a (1503.08268), Deason et al. 2015 (1504.04372), Walker et al. 2015 (1504.03060), Simon et al. 2015 (1504.02889), Koposov et al. 2015b (1504.07916), Kirby et al. 2015 Hydra II (1506.01021), Westmeier et al. 2015 (1507.03661): no Tri II mention.
  - Later namings: Pawlowski et al. 2015 (1505.07465, 27 May), "the dwarf satellite Triangulum II"; DES Y2 (14 Aug 2015).
- Chosen: Hooper & Linden 2015, two days after discovery.

### Ursa Major II: Zucker et al. 2006 (discovery), L;P
- Grillmair 2006 (astro-ph/0605396, v1 16 May 2006) is earlier but says only "a new globular cluster or dwarf galaxy (Grillmair 2006)", citing a paper "in preparation". It does not adopt the galaxy label.
- Belokurov et al. 2007 Orphan stream (astro-ph/0605705, v1 29 May 2006): the v1 abstract does not mention the object, and the v1 PDF cannot be produced by arXiv ("file unavailable"). The v2 text (Nov 2006) calls it a dSph but cites Zucker et al. 2006, so it is not an earlier naming. This was not read in full at v1.
- **Zucker et al. 2006 (astro-ph/0606633, v1 26 Jun 2006):** "we conclude that this is most likely a hitherto unknown dSph galaxy", on extent, surface brightness and CMD morphology "not ... a single stellar population" (L;P).
- arXiv search for "Ursa Major II", oldest first: Zucker 2006 is the earliest hit.

### Andromeda XV: Ibata et al. 2007 (discovery), N
- Discovery: arXiv:0704.1318, v1 10 Apr 2007: "Two new relatively luminous (MV ∼ −9) dwarf galaxies And XV and XVI". No earlier paper can exist.
- No argument is given for the label. Luminosity, distance and profile fits are reported but never used to argue the kind. Coded N, borderline L.

## Summary

| key | first naming | arXiv v1 | codes | uncertain? |
|---|---|---|---|---|
| carina_3 | Torrealba 2018 (discovery) | 2018-01-22 | L | hedged label |
| draco_2 | Drlica-Wagner 2015 (DES Y2) | 2015-08-14 | L | collective ground; full-text gap in window |
| horologium_1 | Geringer-Sameth 2015 | 2015-03-08 | N | collective; by-name alternative Bechtol 2015 = L |
| phoenix_2 | Geringer-Sameth 2015 | 2015-03-08 | N | collective; alternatives give no L/P/G |
| reticulum_2 | Geringer-Sameth 2015 | 2015-03-08 | N | no |
| reticulum_3 | Drlica-Wagner 2015 (discovery) | 2015-08-14 | L | no |
| segue_1 | Martin, de Jong & Rix 2008 | 2008-05-19 | N | collective and hedged; next is Tollerud 2008 = D |
| segue_2 | Belokurov 2009 (discovery) | 2009-03-04 | D | "dwarf" alone; fallback Walker 2009 = D |
| triangulum_2 | Hooper & Linden 2015 | 2015-03-20 | N | no |
| ursa_major_2 | Zucker 2006 (discovery) | 2006-06-26 | L;P | no |
| andromeda_15 | Ibata 2007 (discovery) | 2007-04-10 | N | borderline L/N |
