# Search log: gas inside the Einstein radius of early-type galaxies (D-075 item 1)

> Purpose: find **measured** gas masses (hot X-ray gas, atomic HI, molecular gas) inside about the effective radius of early-type galaxies, so the A6 gas term rests on quoted measurements (A6S precedence §3.4; protocol §1.7). Run by Claude for JvH. Read at source; nothing from memory.

## 0. Plan, committed before any query is run (2026-11-01)

### 0a. What counts
- A **measurement** of the gas mass, or a measured upper limit, inside a stated radius of the order of the effective radius R_e or a few kpc, for named early-type galaxies or a defined sample of them. It can be per galaxy, or given as a fraction of the stellar mass in the same radius.
- Each of the three phases separately: hot (X-ray, deprojected gas density or mass profiles), atomic (HI), molecular (CO-based H₂, conversion factor stated).
- Massive early-types (stellar masses comparable to the A6 lenses) are preferred, and the mass range is recorded.
- **Not eligible:**
  - whole-galaxy totals with no radius;
  - simulations;
  - gas masses inferred from dynamics or lensing;
  - review statements without a cited measurement (the cited measurement is read instead).

### 0b. Queries, verbatim

| # | Query (ADS, through JvH's Chrome) | Sort |
|---|---|---|
| ADS-G6-1 | `abs:("elliptical galaxies" OR "early-type galaxies") abs:("hot gas" OR "X-ray" OR "hot interstellar medium") abs:("gas mass" OR "gas fraction" OR "mass profile" OR "density profile") abs:(Chandra OR XMM) collection:astronomy property:refereed year:1995-2026` | citations |
| ADS-G6-2 | `abs:("early-type galaxies" OR "elliptical galaxies") abs:("molecular gas" OR "CO" OR "HI" OR "atomic gas") abs:("gas mass" OR "gas fraction" OR "upper limit" OR "detection rate") collection:astronomy property:refereed year:1995-2026` | citations |
| ADS-G6-3 | `abs:("strong lens" OR "lens galaxy" OR "lens galaxies") abs:(gas OR "interstellar medium" OR "X-ray") collection:astronomy property:refereed year:1995-2026` | citations |
| CIT-G6 | The measurement papers cited by the gas statements already read (inventory §4 and adjudication §5), read at source | — |

Fallback if ADS is unreachable: the same terms with WebSearch, with the result lists recorded verbatim.

### 0c. Screening and output
1. Title screening by Claude; exclusions counted.
2. Two independent readers, in separate folders, read the candidates to a committed brief. They record the phase, radius, measured quantity (value or limit, with location and quote), sample, galaxy stellar-mass range and method.
3. The result goes to JvH: per phase, the measurements that apply inside about R_E, and a proposed default and range for the A6 gas term (fraction of the stellar mass inside R_E, by phase, summed). It is registered as an assumption with a slider.

## 1. Fallback queries run (2026-11-01; ADS unreachable)

ADS could not be reached through JvH's Chrome, so the §0b fallback was used: the terms of ADS-G6-1, -2 and -3 run with WebSearch (standard mode), three phrasings each, run before any candidate was opened. WebSearch has no refereed, collection or year filter; the refereed condition of the ADS queries is applied at screening (§3). Each result list is recorded verbatim, in the order returned (title as returned by the tool; where the tool returned only a host name, that is what is shown). The disposition column is filled in §3.

### Q1a (ADS-G6-1, hot gas) — `Chandra XMM hot gas mass profile elliptical galaxies density profile gas fraction`

| # | Title (as returned) | URL | Disp. |
|---|---|---|---|
| 1 | Probing the Dark Matter and Gas Fraction in Relaxed Galaxy Groups with X-ray observations from Chandra and XMM | https://arxiv.org/pdf/astro-ph/0610134 | X-scope |
| 2 | arxiv.org | https://arxiv.org/abs/astro-ph/0509521 | C1 |
| 3 | zendy.io | https://zendy.io/pdf-viewer/10.1086/498081 | U |
| 4 | pdf.arxiv.org | https://pdf.arxiv.org/pdf/astro-ph/0610134 | dup #1 |
| 5 | ntrs.nasa.gov | https://ntrs.nasa.gov/citations/20040046915 | X-type |
| 6 | web3.arxiv.org | https://web3.arxiv.org/pdf/1204.3095 | C3 |
| 7 | arxiv.org | https://arxiv.org/pdf/1007.5322v1 | C4 |
| 8 | X-Ray Constraints on Dark Matter in Galaxy Clusters and Elliptical Galaxies: A View from Chandra and XMM | https://ar5iv.labs.arxiv.org/html/astro-ph/0310579 | X-review |
| 9 | Scaling Mass Profiles around Elliptical Galaxies Observed withChandraandXMM‐Newton | https://scilit.com/publications/255a76c37be93d036b7a890b2c16c3ac | dup C1 |
| 10 | Scaling Mass Profiles around Elliptical Galaxies Observed with Chandra and XMM-Newton | https://scilit.com/publications/7a04e66c2ab01ab77710b8241bd1d0bf | dup C1 |

### Q1b (ADS-G6-1) — `early-type galaxies hot interstellar medium X-ray gas mass within effective radius Chandra`

| # | Title (as returned) | URL | Disp. |
|---|---|---|---|
| 1 | The MASSIVE Survey IV.: The X-ray halos of the most massive early-type galaxies in the nearby Universe | https://arxiv.org/pdf/1604.01764 | X-LX |
| 2 | Chandra Early-Type Galaxy Atlas | https://arxiv.org/pdf/1812.02718 | C6 |
| 3 | Chandra Observations of Early-type Galaxies | https://arxiv.org/pdf/0711.0395 | X-type |
| 4 | The MASSIVE Survey V.: The X-ray halos of the most massive early-type galaxies in the nearby Universe | https://bibsonomy.org/bibtex/8af2f7464a78421c49194e1ef987f146 | dup #1 (same title but for the numeral) |
| 5 | arxiv.org | https://arxiv.org/abs/1604.01764v1 | dup #1 |
| 6 | The MASSIVE Survey IV.: | https://ar5iv.arxiv.org/html/1604.01764 | dup #1 |
| 7 | the massive survey iv the x ray halos of the most massive early t | https://collaborate.princeton.edu/en/publications/the-massive-survey-iv-the-x-ray-halos-of-the-most-massive-early-t/ | dup #1 |
| 8 | Early-type galaxies in the Chandra COSMOS Survey | https://ar5iv.arxiv.org/html/1405.7039 | X-LX |
| 9 | The MASSIVE Survey IV.: | https://www.arxiv-vanity.com/papers/1604.01764/ | dup #1 |
| 10 | web3.arxiv.org | https://web3.arxiv.org/pdf/0711.0395 | dup #3 |

### Q1c (ADS-G6-1) — `deprojected hot gas density profiles early-type galaxies XMM-Newton Chandra sample gas mass`

| # | Title (as returned) | URL | Disp. |
|---|---|---|---|
| 1 | Gravitational potential and X-ray luminosities of early-type galaxies observed with XMM-Newton and Chandra | https://arxiv.org/pdf/0903.2540 | C5 |
| 2 | Hot gaseous atmospheres of rotating galaxies observed with XMM-Newton | https://arxiv.org/pdf/2008.01161 | C8 |
| 3 | Constraining the Physical State of the Hot Gas Halos in NGC 4649 and NGC 5846 | https://ar5iv.arxiv.org/html/1706.02303 | C7 |
| 4 | openaccess.inaf.it | https://openaccess.inaf.it/bitstreams/37de169d-919f-461c-bba7-33a8f4a763e0/download | U |
| 5 | unifind.unito.it | https://unifind.unito.it/resource/item/324950 | dup C7 |
| 6 | Constraining the Physical State of the Hot Gas Halos in NGC 4649 and NGC 5846 | https://openaccess.inaf.it/handle/20.500.12386/28986 | dup C7 |
| 7 | Constraining the Physical State of the Hot Gas Halos in NGC 4649 and NGC 5846 | https://openaccess.inaf.it/entities/publication/79399377-7bbf-4713-8516-222441d0ab91 | dup C7 |
| 8 | mpe.mpg.de | https://mpe.mpg.de/~hxb/cluster/WLworkshop08/gastaldello.pdf | X-type |
| 9 | Hot Gas Halos in Early-Type Field Galaxies | https://ar5iv.arxiv.org/html/1004.5376 | X-LX |
| 10 | Scaling Mass Profiles around Elliptical Galaxies Observed with Chandra and XMM-Newton | https://ar5iv.labs.arxiv.org/html/astro-ph/0509521 | dup C1 |

### Q2a (ADS-G6-2, cold gas) — `early-type galaxies molecular gas CO detection rate gas mass upper limit`

| # | Title (as returned) | URL | Disp. |
|---|---|---|---|
| 1 | The Atlas3D project -- XXVII. Cold Gas and the Colours and Ages of Early-type Galaxies | https://arxiv.org/pdf/1312.6318 | X-deriv |
| 2 | Cold Gas and Star Formation in Elliptical Galaxies | https://arxiv.org/pdf/astro-ph/9808266 | X-review |
| 3 | The Atlas3D project -- IV: the molecular gas content of early-type galaxies | https://arxiv.org/pdf/1102.4633 | C13 |
| 4 | The MASSIVE Survey - III. Molecular gas and a broken Tully-Fisher relation in the most massive early-type galaxies | https://arxiv.org/pdf/1510.00729 | C15 |
| 5 | www2.mpia-hd.mpg.de | https://www2.mpia-hd.mpg.de/~QNQ/Slides/MarieMartig.pdf | X-type |
| 6 | Molecular Gas in nearby Early-Type Powerful Classical Radio Galaxies | https://ar5iv.arxiv.org/html/astro-ph/0211279 | C20 |
| 7 | academic.oup.com | https://academic.oup.com/mnras/article/415/1/32/988888 | X-scope (MNRAS 415, 32 = COLD GASS, journal ref on arXiv:1103.1642) |
| 8 | The ATLAS3D project – \Romannum18. CARMA CO imaging survey of early-type galaxies | https://ar5iv.arxiv.org/html/1210.5524 | C14 |
| 9 | ar5iv.arxiv.org | https://ar5iv.arxiv.org/html/1102.1922 | X-type |
| 10 | www.arxiv-vanity.com | https://www.arxiv-vanity.com/papers/1103.1642/ | dup #7 |

### Q2b (ADS-G6-2) — `elliptical galaxies HI atomic gas mass gas fraction survey`

| # | Title (as returned) | URL | Disp. |
|---|---|---|---|
| 1 | The Cool ISM in Elliptical Galaxies. II. Gas Content in the Volume - Limited Sample and Results from the Combined Elliptical and Lenticular Surveys | https://arxiv.org/pdf/1009.5259 | C25 |
| 2 | The Cool ISM in Elliptical Galaxies. I. A Survey of Molecular Gas | https://arxiv.org/pdf/astro-ph/0608179 | C18 |
| 3 | The HI content of elliptical and lenticular galaxies with recent star formation | https://arxiv.org/pdf/0705.3469 | X-HI1dish |
| 4 | arxiv-vanity.com | https://www.arxiv-vanity.com/papers/1009.5259/ | dup C25 |
| 5 | ar5iv.labs.arxiv.org | https://ar5iv.labs.arxiv.org/html/1009.5259 | dup C25 |
| 6 | Gas in Galaxies at the End of their Lives - Food for New Stars | https://wwwmpa.mpa-garching.mpg.de/mpa/research/current_research/hl2012-4/hl2012-4-en-print.html | X-type |
| 7 | MPA HOMEPAGE | https://wwwmpa.mpa-garching.mpg.de/mpa/research/current_research/hl2012-4/hl2012-4-en.html | dup #6 |
| 8 | skip to main content | https://par.nsf.gov/biblio/10030106-gas-virgos-red-dead-dwarf-elliptical-galaxies | X-type |
| 9 | سجل دخولك للبدء | https://www.shamra-academia.com/show/3a43484fa02538 | dup C25 (page title read: "The Cool ISM in Elliptical Galaxies. II …") |
| 10 | egg.astro.cornell.edu | https://egg.astro.cornell.edu/alfalfa/highmass.php | X-type |

### Q2c (ADS-G6-2) — `massive early-type galaxies molecular gas fraction CO upper limits survey`

| # | Title (as returned) | URL | Disp. |
|---|---|---|---|
| 1 | COLD GASS, an IRAM legacy survey of molecular gas in massive galaxies: I. Relations between H2, HI, stellar content and structural properties | https://arxiv.org/pdf/1103.1642 | dup Q2a #7 |
| 2 | bohrium.dp.tech | https://bohrium.dp.tech/paper/arxiv/0309304 | C21 |
| 3 | cold gass an iram legacy survey of molecular gas in massive galax | https://researchportalplus.anu.edu.au/en/publications/cold-gass-an-iram-legacy-survey-of-molecular-gas-in-massive-galax/ | dup Q2a #7 |
| 4 | www.arxiv.org | https://www.arxiv.org/abs/1103.1642 | dup Q2a #7 |
| 5 | openresearch-repository.anu.edu.au | https://openresearch-repository.anu.edu.au/items/a5696165-7abc-4d4e-a769-b0378c6803cb/full | dup Q2a #7 |
| 6 | www.mso.anu.edu.au | https://www.mso.anu.edu.au/~krumholz/publications/2011/saintonge11a.pdf | dup Q2a #7 |
| 7 | The ATLAS3D project – \Romannum18. CARMA CO imaging survey of early-type galaxies | https://ar5iv.arxiv.org/html/1210.5524 | dup C14 |
| 8 | ترغب بنشر مسار تعليمي؟ اضغط هنا | https://www.shamra-academia.com/show/5d38dff128c39 | X-scope (page title read: ATCA molecular gas in high-z radio galaxies, 2016) |
| 9 | The Atlas3D Project -- XI. Dense molecular gas properties of CO-luminous early-type galaxies | https://www.shamra-academia.com/show/3a434aff5800d8 | X-scope |
| 10 | The ATLAS3D project – \Romannum18. CARMA CO imaging survey of early-type galaxies | https://ar5iv.labs.arxiv.org/html/1210.5524 | dup C14 |

### Q3a (ADS-G6-3, lenses) — `strong lens galaxies interstellar medium gas X-ray`

| # | Title (as returned) | URL | Disp. |
|---|---|---|---|
| 1 | X-ray detection of the most extreme star-forming galaxies at the cosmic noon via strong lensing | https://arxiv.org/pdf/2312.05442 | X-scope |
| 2 | Identifying the Lens Galaxy B1152+199 as a Ghostly Damped Lyman Alpha System by the Cosmic Origins Spectrograph | https://arxiv.org/pdf/1612.04848 | X-column |
| 3 | SLICE -- Combining Strong Lensing and X-ray in AC 114. Further Insights into the Merger Scenario | https://arxiv.org/pdf/2512.09512 | X-scope |
| 4 | A Study of Interstellar Gas and Stars in the Gravitationally Lensed Galaxy `The Cosmic Eye' from Rest-Frame Ultraviolet Spectroscopy | https://arxiv.org/pdf/0910.0840 | X-scope |
| 5 | pdf.arxiv.org | https://pdf.arxiv.org/pdf/0910.0840 | dup #4 |
| 6 | numericalatlas.doc.ic.ac.uk | https://numericalatlas.doc.ic.ac.uk/source/0904.0018 | X-scope (arXiv:0904.0018, cluster AC 114) |
| 7 | Directly to content | https://archiv.ub.uni-heidelberg.de/volltextserver/7723 | U (bot check; not bypassed) |
| 8 | Identifying the Lens Galaxy B 1152+199 as a Ghostly Damped Lyman Alpha System by the Cosmic Origins Spectrograph | https://ar5iv.arxiv.org/html/1612.04848 | dup #2 |
| 9 | arxiv.org | https://arxiv.org/pdf/0711.2066v1 | X-scope |
| 10 | heidok eprint 7723 | https://archiv.ub.uni-heidelberg.de/volltextserver/cgi/export/eprint/7723/RDFNT/heidok-eprint-7723.nt | dup #7 |

### Q3b (ADS-G6-3) — `lens galaxy gas content X-ray emission strong lensing elliptical`

| # | Title (as returned) | URL | Disp. |
|---|---|---|---|
| 1 | Probing the Cool Interstellar and Circumgalactic Gas of Three Massive Lensing Galaxies at z=0.4-0.7 | https://arxiv.org/pdf/1510.04307 | X-column |
| 2 | X-ray detection of the most extreme star-forming galaxies at the cosmic noon via strong lensing | https://arxiv.org/pdf/2312.05442 | dup Q3a #1 |
| 3 | The distribution of dark matter in galaxies | https://arxiv.org/pdf/1811.08843 | X-review |
| 4 | X-Ray And Optical Flux Ratio Anomalies In Quadruply Lensed Quasars. II. Mapping the Dark Matter Content in Elliptical Galaxies | https://arxiv.org/pdf/1108.2725 | X-scope |
| 5 | www.arxiv.org | https://www.arxiv.org/pdf/astro-ph/0502007 | X-column |
| 6 | web3.arxiv.org | https://web3.arxiv.org/pdf/astro-ph/9803092 | X-scope |
| 7 | Content area | https://proquest.com/docview/1272041086/abstract/D5D114F6BB8F40A4PQ | X-type |
| 8 | Chandra Observations of Gravitational Lenses B1600+434 and B1608+656 | https://ar5iv.labs.arxiv.org/html/astro-ph/0502007 | dup #5 |
| 9 | arxiv.org | https://arxiv.org/abs/astro-ph/0502007v1 | dup #5 |
| 10 | web3.arxiv.org | https://web3.arxiv.org/pdf/astro-ph/9603101 | X-sim |

### Q3c (ADS-G6-3) — `strong gravitational lens galaxies dust gas interstellar medium extinction lens galaxy`

| # | Title (as returned) | URL | Disp. |
|---|---|---|---|
| 1 | The Saas Fee Lectures on Strong Gravitational Lensing | https://arxiv.org/pdf/astro-ph/0407232 | X-review |
| 2 | Strong gravitational lensing and microlensing of supernovae | https://arxiv.org/pdf/2301.07729 | X-review |
| 3 | The Interstellar Medium of Lens Galaxies | https://arxiv.org/pdf/astro-ph/9910065 | X-dust |
| 4 | Dust and Extinction Curves in Galaxies with z>0: The Interstellar Medium of Gravitational Lens Galaxies | https://arxiv.org/pdf/astro-ph/9901037 | X-dust |
| 5 | Extinction properties of lensing galaxies | https://arxiv.org/pdf/0711.4267 | X-dust |
| 6 | Dust and extinction curves in galaxies with z > 0: The interstellar medium of gravitational lens galaxies | https://experts.arizona.edu/en/publications/dust-and-extinction-curves-in-galaxies-with-z-gt-0-the-interstell/ | dup #4 |
| 7 | arxiv.org | https://arxiv.org/abs/astro-ph/9901037 | dup #4 |
| 8 | web3.arxiv.org | https://web3.arxiv.org/pdf/astro-ph/9901037 | dup #4 |
| 9 | Identifying the Lens Galaxy B 1152+199 as a Ghostly Damped Lyman Alpha System by the Cosmic Origins Spectrograph | https://ar5iv.arxiv.org/html/1612.04848 | dup Q3a #2 |
| 10 | web3.arxiv.org | https://web3.arxiv.org/abs/astro-ph/9901037 | dup #4 |

**Tally:** 9 queries × 10 results = 90 entries; 36 duplicates or mirrors; **54 unique records**.

**How records were identified.** Every arXiv record was identified from its arXiv abstract page (`https://arxiv.org/abs/<id>`, fetched with curl's own user-agent); pages saved under the session scratchpad (`gas6/abs*/`), SHA-256 in `gas6/abs_sha256.txt`. The arXiv API host (export.arxiv.org) was refused by the network proxy and was not used. Non-arXiv results without a title were opened once with WebFetch: ntrs 20040046915 (a NASA grant report on a fossil group), proquest 1272041086 (a Yale dissertation, theoretical), par.nsf 10030106 (an AAS meeting abstract, HI in three Virgo dwarf ellipticals), unifind 324950 (Paggi et al. 2017, = C7). Three could not be identified: zendy (empty page), the openaccess.inaf.it bitstream (not opened), and heidelberg 7723 (bot-check page; not bypassed).

## 2. Citation chase (CIT-G6)

Sources opened at arXiv (PDF, `gas6/dl/`, run with `python3 -I`/pdftotext; SHA-256 below). Only the citations attached to gas statements were followed. The source's own gas values were not re-read or recorded here.

| Source | arXiv | SHA-256 (PDF) |
|---|---|---|
| Mathews & Brighenti 2003 | astro-ph/0309553 | 0c47e181ff9dbea2672bd06bcdf317382f57e4ff07b86e7821f46ee1f9cb43bb |
| Young et al. 2011 | 1102.4633 | 83a0a162724cc31292a92c74dbb3dc6e4f5a1f14d103ed9321694a57a2076753 |
| Serra et al. 2012 | 1111.4241 | da31581734759374d9fa516bfb69f0eb486ffee2106efde9c2b829aef0b41be4 |
| Eichner et al. 2012 (R49) | 1209.2140 | 9af0df3615bbcde44a0e1b1aaaee4c216b0149bdc2870ff7c24459b02b15b1d9 |
| R61 | 1709.01931 | 8b9a54259f783f5b843fcfeca20b1d67e0fb2c4af4f1cc1174b571e2c5436552 |
| R26 | 1612.00065 | 542370972c06f894fa4f16658a2aee698a3e01410ea8652ee52e36f19febcff9 |
| R29 | 1803.07082 | 240f01b5b90632642a38029702b4fd663df9e035b0826941b14f535fc6bdd604 |
| R64 Treu et al. 2010 | 0911.3392 | 410e2e7368f03c98f1cc98719233064853b9166f0f24afcce0461806bcdb75c7 |
| R31 Wang et al. 2026 | 2603.26894 | bb39d93d14baeb08806f6807c114a19f405e11126964f8c996909ac70ee6c545 |
| R35 Koopmans & Treu 2002 | astro-ph/0201017 | b9171618053ae533359ef942caea555b3509f31689aa730cfd8d59034d3b3ef3 |
| R37 Ferreras, Saha & Burles 2008 | 0710.3159 | 565799d2aca9419c2c4d9814b31e34df974e4378c092bed3db4b990e465cfc0b |

Not opened this session: R28, R25, R32 (their statements are assumptions with no citation, per adjudication §5), R30 (per inventory §4 it cites Henry et al. 1995 for group-scale X-ray emission; not chased), Diehl & Statler 2007 (already read by both readers; it is screened in §3 as a cited paper).

### Cited measurement papers, by citing statement

Reference details are as printed in the citing paper's reference list. arXiv ids were matched by WebSearch and confirmed on the arXiv abstract page (authors, date, and journal reference where printed); "not located" means no arXiv record was found in the searches run.

| Cited by (location) | Cited paper (as printed) | arXiv |
|---|---|---|
| M&B 2003 Fig. 2 (NGC 4472 hot-gas density profile) | Trinchieri, Fabbiano & Canizares 1986, ApJ 310, 637 | pre-arXiv |
| M&B 2003 Fig. 2 | Irwin & Sarazin 1996, ApJ 471, 683 | not located |
| M&B 2003 Fig. 2 | Loewenstein, Mushotzky, Angelini, Arnaud & Quataert 2001, ApJ 555, L21 | astro-ph/0106326 |
| M&B 2003 Fig. 2b (temperature only) | Jones et al. 1997, ApJ 482, 143; David et al. 1994, ApJ 428, 544; Trinchieri et al. 1994, ApJ 428, 555 | not searched (T profiles) |
| M&B 2003 §7.2 (HI) | Knapp, Turner & Cunniffe 1985, AJ 90, 454 | pre-arXiv |
| M&B 2003 §7.2; Young 2011 §1 (HI) | Huchtmeier 1994, A&A 286, 389; Huchtmeier, Sage & Henkel 1995, A&A 300, 675 | not located |
| M&B 2003 §7.2 (HI discs) | Sadler, Oosterloo, Morganti & Karakas 2000, AJ 119, 1180 | not located |
| M&B 2003 §7.2 (HI discs) | Oosterloo, Morganti, Sadler, Vergani & Caldwell 2002, AJ 123, 729 | astro-ph/0111141 (matched on authors and date; no journal ref printed) |
| M&B 2003 §7.2; Young 2011 §1 (CO) | Wiklind, Combes & Henkel 1995, A&A 297, 643 | not located |
| M&B 2003 §7.2 (CO) | Knapp & Rupen 1996, ApJ 460, 271 | not located |
| M&B 2003 §7.2 (CO maps) | Young 2002, AJ 124, 788 | astro-ph/0205162 |
| M&B 2003 §7.2 (cold gas vs age) | Georgakakis et al. 2001, MNRAS 326, 1431 | astro-ph/0105435 |
| M&B 2003 §7.3 (gas with dust) | van Dokkum & Franx 1995, AJ 110, 2027; Martel et al. 2000, ApJS 130, 267; Colbert et al. 2001, AJ 121, 808; Tran et al. 2001, AJ 121, 2928; Kleijn et al. 2002, AJ 123, 1334 | not searched (dust) |
| Young 2011 §1 (CO) | Lees, Knapp, Rupen & Phillips 1991, ApJ 379, 177 | pre-arXiv |
| Young 2011 §1 (hot gas) | O'Sullivan, Forbes & Ponman 2001, MNRAS 328, 461 | astro-ph/0108181 |
| Young 2011 §1 (dust discs) | Goudfrooij et al. 1994, A&A (vol. not captured) | not searched (dust) |
| Young 2011 §1; Serra 2012 §1 (HI) | Wardle & Knapp 1986, AJ 91, 23 | pre-arXiv |
| Young 2011 §1; Serra 2012 §1 (HI) | Morganti et al. 2006, MNRAS 371, 157 | astro-ph/0606261 |
| Young 2011 §1; Serra 2012 §1 (HI) | Oosterloo, Morganti, Crocker, Jütte et al. 2010, MNRAS 409, 500 | 1007.2059 |
| Young 2011 §1 (CO) | Combes, Young & Bureau 2007, MNRAS 377, 1795 | astro-ph/0703557 |
| Young 2011 §1 (CO) | Welch, Sage & Young 2010, ApJ 725, 100 | 1009.5259 |
| Young 2011 §3 (CO, compared) | Welch & Sage 2003, ApJ 584, 260 | astro-ph/0210337 |
| Young 2011 §3 (CO, compared) | Sage, Welch & Young 2007, ApJ 657, 232 | astro-ph/0608179 |
| Serra 2012 §1 (HI, HIPASS) | Sadler, Oosterloo & Morganti 2002, ASP Conf. Ser. 273 | astro-ph/0205151 |
| Serra 2012 §1 (resolved HI) | Oosterloo, Morganti, Sadler, van der Hulst, Serra 2007 | astro-ph/0701716 |
| Eichner 2012 §4.2 (H₂) | Young et al. 2011 | 1102.4633 (source above) |
| Eichner 2012 §4.2 (hot gas) | Sanderson, Ponman, Finoguenov, Lloyd-Davies & Markevitch 2003, MNRAS 340, 989 | astro-ph/0301049 |
| R64 Treu 2010 §2.1 (X-ray) | Mathews & Brighenti 2003 (source above); Humphrey et al. 2006, ApJ 646, 899 | astro-ph/0601301 |
| R31 Wang 2026 §1 | Mamon & Łokas 2005, MNRAS 363, 705 | astro-ph/0405491 |
| R31 Wang 2026 §1 | Diehl & Statler 2007, ApJ 668, 150 | astro-ph/0606215 |
| R31 Wang 2026 §1 | Grillo, Christensen, Gallazzi & Rasmussen 2013, MNRAS 433, 2604 | 1305.5844 |
| R35 Koopmans & Treu 2002 §1 | Chartas, Bautz, Garmire, Jones & Schneider 2001, ApJ 550, L167 | astro-ph/0101019 |
| R37 Ferreras 2008 §3 | Roberts & Haynes 1994, ARA&A 32, 115 | pre-arXiv (review) |
| R61 §1 (dust in SNL-1) | none: the statement rests on the paper's own HST imaging | — |
| R26 §6 (nebular emission, SNL-1) | none: own spectra | — |
| R29 §4 (gas emission, J0403−0239) | none: own spectrum | — |

Records seen only while locating the cited papers above (not results of a committed query, not cited by a source): astro-ph/9702080, astro-ph/0611612, astro-ph/0406132, astro-ph/0009070, astro-ph/0011399, astro-ph/0009112, astro-ph/9809075, astro-ph/9902011, 0712.2852, 0903.0602, 1005.5642, astro-ph/0304048, astro-ph/0307457, astro-ph/9808204. They are **not** in the candidate pool; adding any of them is JvH's call.

## 3. Title-level screening

Screened by Claude on title and abstract only (arXiv abstract pages; for the six papers not on arXiv, on the citing context alone, marked †). No gas mass, fraction or limit was recorded. §0a applied; at this stage a record is kept when the abstract plausibly offers a gas measurement or limit for named early-type galaxies or an ETG sample at radii that can be set to about R_e (deprojected X-ray profiles, interferometric maps, or single-dish CO pointings with a central beam). Whether the radius actually fits is for the readers. The refereed condition of the ADS queries is applied here, since WebSearch could not apply it.

### Kept (31)

**Hot (X-ray), 12**

| C | Citation | arXiv | What it appears to measure (title/abstract) | From |
|---|---|---|---|---|
| C1 | Fukazawa et al. 2006, ApJ 636, 698 | astro-ph/0509521 | Hot-gas temperature and density profiles, 53 ellipticals (Chandra archive); mass profiles at 0.1–1 r_e | Q1a, Q1c |
| C2 | Humphrey et al. 2006, ApJ 646, 899 | astro-ph/0601301 | Chandra mass profiles of 7 ellipticals from hot gas, flat M/L within R_eff | CIT (R64, R31) |
| C3 | Humphrey et al. 2012 (ElIXr II) | 1204.3095 | Chandra+XMM hot-gas halo and baryon budget of one isolated L* elliptical (NGC 1521) | Q1a |
| C4 | Das et al. 2010 | 1007.5322 | Deprojected hot-gas density and temperature profiles, 6 X-ray-bright ellipticals | Q1a |
| C5 | Nagino & Matsushita 2009 | 0903.2540 | XMM+Chandra mass profiles of 22 ETGs, 0.5–6 r_e (gas density profiles implied by method, not stated) | Q1c |
| C6 | Kim et al. (arXiv 2018), Chandra Galaxy Atlas | 1812.02718 | Uniform hot-gas data products for 70 ETGs (2D spectral maps); gas masses not stated in abstract | Q1b |
| C7 | Paggi et al. 2017, ApJ | 1706.02303 | Chandra/XMM hot-gas mass profiles of NGC 4649 and NGC 5846 within ~12 kpc, incl. r < 3 kpc | Q1c |
| C8 | Juráňová et al. (arXiv 2020) | 2008.01161 | Hot atmospheres (entropy profiles) of 6 lenticulars + 1 spiral (XMM) | Q1c |
| C9 | Loewenstein et al. 2001, ApJ 555, L21 | astro-ph/0106326 | Central hot-gas surface-brightness profiles of NGC 1399, 4472, 4636 (Chandra) | CIT (M&B) |
| C10 | Sanderson et al. 2003, MNRAS 340, 989 | astro-ph/0301049 | Gas density profiles of 66 systems, mostly groups/clusters, incl. 2 isolated ETGs | CIT (Eichner) |
| C11† | Irwin & Sarazin 1996, ApJ 471, 683 | not located | NGC 4472 hot-gas density profile (ROSAT), per M&B Fig. 2 | CIT (M&B) |
| C12† | Trinchieri, Fabbiano & Canizares 1986, ApJ 310, 637 | pre-arXiv | Hot-gas profiles of NGC 4472/4649/4636 (Einstein), per M&B | CIT (M&B) |

**Molecular (CO), 12**

| C | Citation | arXiv | What it appears to measure | From |
|---|---|---|---|---|
| C13 | Young et al. 2011 (ATLAS3D IV), MNRAS | 1102.4633 | IRAM 30 m CO, 260 ETGs, volume-limited; detections and limits (abstract read before; aperture not yet read) | Q2a, CIT |
| C14 | Alatalo et al. (arXiv 2012) (ATLAS3D XVIII) | 1210.5524 | CARMA CO maps of 40 CO-rich ETGs (extent, morphology) | Q2a, Q2c |
| C15 | Davis et al. (arXiv 2015) (MASSIVE III) | 1510.00729 | CO in 15 of the most massive ETGs (M* > 10^11.5), pre-selected for ISM signs | Q2a |
| C16 | Young 2002, AJ 124, 788 | astro-ph/0205162 | Interferometric CO maps of 7 ellipticals (5 detected), disc diameters | CIT (M&B) |
| C17 | Combes, Young & Bureau 2007, MNRAS 377, 1795 | astro-ph/0703557 | CO in 43 SAURON E/S0s | CIT (Young 2011) |
| C18 | Sage, Welch & Young 2007, ApJ 657, 232 | astro-ph/0608179 | CO in a volume-limited sample of non-cluster ellipticals (partial) | Q2b, CIT |
| C19 | Welch & Sage 2003, ApJ 584, 260 | astro-ph/0210337 | CO in volume-limited field S0s; gas "inside the central few kpc" | CIT (Young 2011) |
| C20 | Leon et al. (arXiv 2002) | astro-ph/0211279 | CO in 18 early-type hosts of powerful radio galaxies (AGN-selected) | Q2a |
| C21 | Salomé & Combes 2003, A&A 412, 657 | astro-ph/0309304 | CO in 32 central cluster galaxies with cooling flows (BCG-selected) | Q2c |
| C22† | Lees, Knapp, Rupen & Phillips 1991, ApJ 379, 177 | pre-arXiv | CO in ellipticals, per Young 2011 | CIT |
| C23† | Wiklind, Combes & Henkel 1995, A&A 297, 643 | not located | CO in FIR-selected ellipticals, per M&B | CIT |
| C24† | Knapp & Rupen 1996, ApJ 460, 271 | not located | CO in ellipticals, per M&B | CIT |

**Atomic (HI), 7**

| C | Citation | arXiv | What it appears to measure | From |
|---|---|---|---|---|
| C25 | Welch, Sage & Young 2010, ApJ 725, 100 | 1009.5259 | HI and CO, volume-limited ellipticals (also molecular) | Q2b, CIT |
| C26 | Morganti et al. 2006, MNRAS 371, 157 | astro-ph/0606261 | Deep WSRT HI imaging of 12 SAURON E/S0s | CIT |
| C27 | Oosterloo et al. 2010, MNRAS 409, 500 | 1007.2059 | Deep WSRT HI imaging of 33 SAURON ETGs, field and Virgo; inner HI discs | CIT |
| C28 | Oosterloo et al. 2002, AJ 123, 729 | astro-ph/0111141 | ATCA HI in 5 dust-lane ellipticals (2 detections, 3 limits) | CIT (M&B) |
| C29 | Oosterloo et al. (arXiv 2007) | astro-ph/0701716 | Resolved HI in 30 HI-rich ETGs selected from HIPASS (biased to gas-rich) | CIT (Serra) |
| C30 | Serra et al. 2012 (ATLAS3D XIII), MNRAS 422, 1835 | 1111.4241 | WSRT HI in 166 ETGs; small discs "confined within the stellar body" (abstract read before) | CIT |
| C31† | Sadler, Oosterloo, Morganti & Karakas 2000, AJ 119, 1180 | not located | HI discs in low-luminosity ETGs, per M&B | CIT |

### Excluded (unique records), with reasons

From the fallback (54 unique records; 14 kept): **40 excluded or unresolved**

| Reason | n | Records |
|---|---|---|
| X-scope: not ETG galaxy-scale gas (groups/clusters, lensed sources, high-z hosts, mixed-type sample, line ratios, microlensing) | 11 | astro-ph/0610134, 1103.1642, ATLAS3D XI (shamra), shamra 5d38dff128c39, 2312.05442, 2512.09512, 0910.0840, 0904.0018, 0711.2066, 1108.2725, astro-ph/9803092 |
| X-LX: X-ray luminosity/temperature only, no gas mass | 3 | 1604.01764, 1405.7039, 1004.5376 |
| X-review | 5 | astro-ph/0310579, astro-ph/9808266, 1811.08843, astro-ph/0407232, 2301.07729 |
| X-type: not a refereed paper (thesis, slides, proceedings, press page, web page, meeting abstract, grant report) | 9 | 0711.0395 (thesis), ntrs, mpe slides, mpia slides, 1102.1922, MPA page, par.nsf, egg.astro.cornell, proquest |
| X-deriv: re-analyses data already in the pool | 1 | 1312.6318 (uses ATLAS3D CO/HI = C13, C30) |
| X-HI1dish: single-dish HI, whole galaxy | 1 | 0705.3469 |
| X-column: absorption column along a sightline, not a mass | 3 | 1612.04848, 1510.04307, astro-ph/0502007 |
| X-dust: extinction only | 3 | astro-ph/9910065, astro-ph/9901037, 0711.4267 |
| X-sim | 1 | astro-ph/9603101 |
| U: not identified | 3 | zendy (empty), openaccess.inaf bitstream (not opened), heidelberg 7723 (bot check) |

From the citation chase (cited papers not already kept): **19 excluded, 2 unresolved**

| Reason | n | Records |
|---|---|---|
| X-LX | 1 | O'Sullivan et al. 2001 |
| X-T: temperature profiles only | 3 | Jones et al. 1997; David et al. 1994; Trinchieri et al. 1994 |
| X-read: already read by both readers, no gas-mass statement | 1 | Diehl & Statler 2007 |
| X-scope | 1 | Chartas et al. 2001 (cluster-scale X-ray field of MG2016+112) |
| X-radius: gas inside a 70 kpc Einstein radius of a group-scale lens | 1 | Grillo et al. 2013 |
| X-model | 1 | Mamon & Łokas 2005 |
| X-review | 1 | Roberts & Haynes 1994 |
| X-HI1dish† | 2 | Knapp, Turner & Cunniffe 1985; Wardle & Knapp 1986 (Serra 2012 describes both as single-dish, integrated) |
| X-compilation | 1 | Georgakakis et al. 2001 |
| X-dust: gas inferred from dust | 6 | Goudfrooij et al. 1994; van Dokkum & Franx 1995; Martel et al. 2000; Colbert et al. 2001; Tran et al. 2001; Kleijn et al. 2002 |
| X-type: proceedings | 1 | Sadler, Oosterloo & Morganti 2002 |
| Unresolved: not located, not screened | 2 | Huchtmeier 1994; Huchtmeier, Sage & Henkel 1995 |

**Totals:** 92 unique records screened (54 from the fallback + 38 cited papers not already among them); 31 kept (12 hot, 12 molecular, 7 atomic; 6 of them † on citing context only); 56 excluded (37 fallback + 19 cited); 5 unresolved (3 + 2).

### Flags for JvH (facts, no action taken)

1. **Lens-specific gas, excluded by §0a as worded.** Three records measure gas *in strong-lens galaxies* at about the Einstein radius, but as absorption columns along quasar sightlines, not masses: 1510.04307 (three massive lens ETGs, sightlines at ~1–2 r_e), 1612.04848 (B1152+199), astro-ph/0502007 (differential N_H, B1600+434). Grillo et al. 2013 gives a hot-gas term inside a lens Einstein radius, but at group scale (R_Ein = 70 kpc). If JvH wants lens-galaxy evidence even when it is not a mass inside R_e, these are the ones.
2. **Refereed filter.** The thesis 0711.0395 (54 ETGs, gas properties "scaled to one effective radius") was excluded only because it is not refereed. Its refereed successor, if any, was not located.
3. **Six † candidates** (C11, C12, C22, C23, C24, C31) were kept on the citing paper's description, as no arXiv record was found; the readers need the journal versions.
4. **Pool bias.** C15, C20, C21, C29 are selected for gas or activity (ISM signs, radio AGN, cooling flows, HIPASS-detected). They bound the gas-rich end, not the typical lens.
5. **Single-dish CO.** C13, C17, C18, C22–C24 are single-dish surveys; whether the beam is a usable "stated radius" (Young 2011 prints the beam's physical size) is the readers' call under §0a.

## 4. ADS queries run (primary; 2026-11-01, 09:10–09:20 MDT, JvH's signed-in Chrome)

The ADS queries of §0b were run once Chrome was reachable again, after the fallback (§1–3), so the search is complete as committed.

| # | Records | Title-screened |
|---|---|---|
| ADS-G6-1 | 52 | all 52 |
| ADS-G6-2 | 159 | all 159 |
| ADS-G6-3 | 761 | 128: a title keyword prefilter (gas, X-ray, HI, CO, molecular, interstellar, ISM, absorption, dust, baryon, hot) with cluster, quasar and high-redshift titles removed |

**Deviation (disclosed):** the ADS-G6-3 keyword prefilter was not in the committed plan. ADS-G6-3 matches every lens paper whose abstract mentions X-rays or gas, mostly cluster lenses, lensed quasars and lensed high-redshift sources. The 633 titles the prefilter removed were not read one by one.

Excluded at title level, by the §0a rules and §3's categories (counted, not listed):
- high-redshift lensed sources;
- clusters and groups;
- quasar microlensing;
- black-hole and AGN studies without gas masses;
- simulations;
- single-phase studies of spirals;
- sightline absorption columns;
- theory;
- records already kept as C1–C31.

New candidates kept (not in C1–C31). The readers read them in a second batch with the same brief (version 2):

| # | Record | Phase | What (from title) |
|---|---|---|---|
| N1 | 2007ApJ...668..150D | hot | Hot ISM of normal ellipticals I: Chandra gas gallery |
| N2 | 2006ApJ...653..207D | hot | Hot gas content of low-luminosity early-types |
| N3 | 2010ApJ...715L...1M | hot | Hot gas halos in early-type field galaxies |
| N4 | 2018MNRAS.481.4472L | hot | Thermodynamic properties of a large sample of giant ellipticals |
| N5 | 2011ApJ...729...53H | hot | Census of baryons in an isolated elliptical |
| N6 | 2018ApJ...857...32B | hot | X-ray scaling relations of early-type galaxies |
| N7 | 2015ApJ...806..156S | hot | Scatter in the hot gas content of early-type galaxies |
| N8 | 2006MNRAS.370.1797P | hot | NGC 3379: optical and X-ray mass estimates |
| N9 | 2009ApJ...706..980J | hot | NGC 4636: X-ray and dynamical mass profiles |
| N10 | 2019ApJ...877...91B | hot | Mrk 1216, a compact elliptical |
| N11 | 2017ApJ...844....5P | hot | Hot gas halos of NGC 4649 and NGC 5846 |
| N12 | 2010MNRAS.403.2143H | hot | Mass-profile slope in early-type galaxies (X-ray) |
| N13 | 2019MNRAS.486.1404D | molecular | MASSIVE XI: molecular gas of early-type galaxies |
| N14 | 2015A&A...573A.111O; 2018A&A...618A.126O | molecular, atomic | Cold gas in group-dominant ellipticals |
| N15 | 2018MNRAS.477.2741Y | atomic | HI in slow-rotator early-types |
| N16 | 2000PASJ...52..743F | molecular | Detection rate of molecular gas in ellipticals |
| N17 | 2007PASJ...59...61N | molecular | ASTE CO(3–2) survey of ellipticals |
| N18 | 2014MNRAS.444.3408Y | molecular, atomic | ATLAS3D XXVII: cold gas and colours |
| N19 | 2023PASJ...75..925F; 2024ApJ...964...29F | molecular | Molecular gas within 500 pc of massive ellipticals |
| N20 | 2010A&A...518A...9O | molecular | TANGO I: molecular gas in nearby radio galaxies |
| N21 | 2016MNRAS.458.2423Z | lens, cool gas | Cool ISM and CGM of three massive lensing galaxies |
| N22 | 2012MNRAS.424..104L | lens | Baryonic cooling in lensing galaxies |
