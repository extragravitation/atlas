# A6·strong lensing: source inventory for packaging

- **Date:** 2026-10-31. Prepared by Claude (AI assistance, disclosed) for JvH. Exploratory record for packaging; not a data package and not a ruling.
- **Metadata only.** This file records record identifiers, citations, arXiv ids, survey names, which side each record supplies, evidence tiers, file names, file sizes, licences, reachability, numbers of lenses, redshift ranges as the screening readers recorded them, band counts, IMF names and model names. It records no Einstein radius, Einstein mass, stellar mass, mass-to-light ratio, velocity dispersion, fraction, slope or result. No data table was opened: IOP table files, Zenodo files and VizieR tables were tested by HTTP HEAD or a directory listing only; the GitHub repositories were listed by file name and size without fetching file contents.
- **Rule applied:** `docs/methods/A6S_PRECEDENCE.md` §2 and §3 (frozen, D-065; SHA-256 below matches `data/frozen/a6s-precedence.json`), with D-063 and D-064. D-066 (the z < 0.30 cut) is noted per survey but not applied: it needs per-system redshifts, which are not compiled here.
- **Tools:** `packaging-tools/rank_a6s.py` reads `packaging-tools/a6s_options.csv` (one row per source option, compiled by hand from the inputs below) and writes `precedence_result.csv` and `inventory_tables.md`. The two tables in §1 and §2 below are copied from that output unchanged. Re-run: `python -I docs/sources/screening-A6S/packaging-tools/rank_a6s.py`.

## Inputs

Repository files read (not changed), at commit `04467e407a47ec825041ae9164b3ba1036900a56`:

| File | SHA-256 |
|---|---|
| `docs/methods/A6S_PRECEDENCE.md` | `f103809eadac00dac657061982e963fdfe1e85f46d68188a73953c17dfe9b03d` |
| `data/frozen/a6s-precedence.json` | `8df6ba35c0cb2bb6e7fac39c1f34fd70dfefc11355474c2962f0d426e8ce6fd4` |
| `docs/decisions.md` (D-063, D-064, D-065, D-066) | `75d9966d77ff8424582ee539bac25d98a595eaf2d3e253ff3e24be260c21f65e` |
| `docs/sources/search-log-A6.md` | `e383b26fddaf9864742587cc63fe06cd0d54514bd0acb1860dd37fa2ad7909dd` |
| `docs/sources/screening-A6S/final.csv` | `d6d021c866ca7a2c3085afcf533d83931f2295ee8681dd98d4a56c9ca8bb628d` |
| `docs/sources/screening-A6S/adjudication.md` | `6d869b1534cfa2d121aa08cc1fdfc6a3a5b6a8ca478340ff23c3c61f0754840f` |
| `docs/sources/screening-A6S/reader-a-block1.md` | `f76966b01c317f356895dc24469d6a600351540a3462425674b423f8b6c5ac7a` |
| `docs/sources/screening-A6S/reader-a-block2.md` | `a7b4b3c0aabdb85c91ac3554b43ff992ed7f38ed282d048867b9fe5054410b7a` |
| `docs/sources/screening-A6S/reader-a-round2.md` | `912fdad077429fccb205eae38761bc3776040894c74755cf1868a659ae4db88e` |
| `docs/sources/screening-A6S/reader-b-block1.md` | `7a2d0c547a07295c0b333a164f69cd1d921b3534dfb505d67b9cb1b5d50f5511` |
| `docs/sources/screening-A6S/reader-b-block2.md` | `84deac8a2b3e407db3d415c74ba501039a216a34998cf1cb6522481fd087bc04` |
| `docs/sources/screening-A6S/reader-b-round2.md` | `0eb7b7c14ac4b4c5f036793c2b556fd6d458331c1fc69d724feb3bae3bf0d8c5` |
| `data/README.md` | `d057a3e8b34c082db1f88565e898ebc32ab94f8f95a176e44b8dc968aeae8cc7` |
| `docs/data-standard.md` (2.0.0) | `04658f003bdccbfa9370fa15c34a245e84906ac04cdae75359e4e285f60b62d3` |
| `data/packages/aeg-d-dwarfs/v1/sources.json` (shape only) | `0f1d8e0ddd0377e982c31154918292b84eb5cad227f5a40b319677d28d5a1b0b` |
| `data/packages/aeg-d-dwarfs/v1/REPRODUCTION.md` (shape only) | `43c9420e886ac85634ceaf4408cab7710ffee8391a3afbd30375cbb855973b72` |

Read at source in this session (2026-10-31), metadata only:

| What | Where | How | Kept as |
|---|---|---|---|
| Title, DOI, journal reference and licence link of all 65 arXiv ids of the E, E-pair and P records | `https://arxiv.org/abs/<id>` | `curl`; fields extracted by script from `<meta>` tags and the licence link; abstract text not printed | `packaging-tools/arxiv_licences.csv` |
| PDF reachability of the same 65 ids | `https://arxiv.org/pdf/<id>` | `curl -I`: 65 of 65 returned 200 | this file |
| Copyright line and the list of table files on the journal page, for the 27 AAS-journal articles | `https://iopscience.iop.org/article/<doi>` | `curl`; copyright line and links ending `_ascii.txt` or `_mrt.txt` extracted by script. The site answered 12 of the 27 first requests with a redirect to a bot check; these were repeated with a browser user-agent header and then returned 200 (disclosed) | `packaging-tools/iop_table_heads.csv` |
| Reachability of the 70 IOP table files | links above | `curl -I` (browser user-agent): 70 of 70 returned 200; no file body fetched | `packaging-tools/iop_table_heads.csv` |
| Zenodo records 6104823, 10007041, 23681178, 13366012 | `https://zenodo.org/api/records/<id>` | API JSON: title, date, licence, access right, file names, sizes and checksums; `curl -I` on the file links | §1 table |
| GitHub `Project-Dinos/dinos-i` and `williyamshoe/dinos2` | `https://github.com/<repo>` via `git clone --filter=blob:none --no-checkout` | file tree, sizes and commit only; READMEs read from `raw.githubusercontent.com` | §1 table |
| VizieR J/ApJ/705/1099 (SLACS IX) | `https://cdsarc.cds.unistra.fr/ftp/J/ApJ/705/1099` (directory listing) and `https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/ApJ/705/1099` | WebFetch (reached from search results; the workspace cannot reach either host) | §1 table |
| Gas literature candidates (§4) | `https://arxiv.org/abs/1102.4633`, `/abs/1111.4241`, `/abs/astro-ph/0309553`, `/abs/astro-ph/0606215` | `curl`; title, DOI and journal reference only | §4 |

Everything else in the tables (which side a record supplies, model names, IMFs, bands, apertures, numbers of lenses, redshift ranges) is carried from the screening readings and adjudication, which name the URL each reader read. The `basis` column of `packaging-tools/a6s_records.csv` names the reading for every row. Where the two readers differ, both readings are kept and the row is flagged.

## 1. Records coded E, E-pair or P (51)

Counts: E 21, E-pair 28, P 2, as `final.csv`. The table is generated from `packaging-tools/a6s_records.csv`.

| # | Code | Citation | arXiv (licence at arXiv) | Survey | Side(s) supplied | N lenses | Lens z as read | Evidence tier and data location | Licence at the data location | Fetchable from this workspace |
|---|---|---|---|---|---|---|---|---|---|---|
| R3 | E-pair | Koopmans et al. 2006, ApJ 649, 599 (SLACS III) | astro-ph/0601628 (assumed-1991-2003) | SLACS | observed: θ_E, R_E, M_E (SIE); z_l, z_s | 15 | 0.06–0.33 | tier 2: paper Table 1; IOP page links no table file | IOP page: © 2006 AAS, all rights reserved | arXiv PDF yes; IOP page yes (no table files) |
| R5 | E-pair | Bolton et al. 2008, ApJ 682, 964 (SLACS V) | 0805.1931 (nonexclusive-distrib/1.0) | SLACS | observed: b_SIE (θ_E) and b_LTM; z_l, z_s (SDSS spec.); photometry (I814 de Vaucouleurs, R_e) | 63 modelled grade-A (of 70 grade-A) | ≈0.05–0.5 | tier 1: VizieR J/ApJ/682/964 table4.dat, table5.dat; tier 2: paper Tables 4–5; IOP page links no table file | VizieR: none shown (reader B; reader A notes the CDS licence page linked from the record); IOP page: © 2008 AAS, all rights reserved | VizieR/CDS no (connection reset); IOP page yes (no table files); arXiv PDF yes |
| R7 | E | Auger et al. 2009, ApJ 705, 1099 (SLACS IX) | 0911.2471 (nonexclusive-distrib/1.0) | SLACS | observed: R_E, M_E (R5 SIE models + 11 new SIE); baryonic: flagged alternative only (σ–metallicity prior, D-063 item 3) | 85 grade-A + 13 grade-B | 0.063–0.513 | tier 1: VizieR J/ApJ/705/1099 (CDS listing: table1.dat, table3.dat, table4.dat; GAVO record: tables 'table1', 'lenses'); IOP ascii apj326624t1–t5 | VizieR/GAVO record: none shown; IOP page: © 2009 AAS, all rights reserved | VizieR no; IOP ascii t1–t5 HEAD 200; arXiv PDF yes |
| R9 | E-pair | Shu et al. 2015, ApJ 803, 71 (SLACS XII) | 1407.2240 (CC-by/3.0) | S4TM | baryonic: per-lens stellar masses (FSPS SSP, F814W, Chabrier) released only in R10 table2 | 40 S4TM (+58 SLACS in population tables) | — | tier 3 alone (no per-lens table); per-lens values via R10; IOP ascii apj509959t1–t2 (population tables per readers) | IOP page: © 2015 AAS, all rights reserved | IOP ascii HEAD 200; arXiv PDF yes |
| R10 | E | Shu et al. 2017, ApJ 851, 48 (SLACS XIII) | 1711.00072 (nonexclusive-distrib/1.0) | S4TM | observed: b_SIE, logMein; baryonic: logM (R9 method, Chabrier, total); z_L, z_S (SDSS spec.) | 40 grade-A (118 candidates) | z_L 0.06–0.44; z_S 0.22–1.29 | tier 1: VizieR J/ApJ/851/48 table1.dat, table2.dat; IOP ascii apjaa9794t1–t2 | VizieR ReadMe: no licence statement (readers A, B); IOP page: © 2017 AAS, all rights reserved | VizieR no; IOP ascii HEAD 200; arXiv PDF yes |
| R12 | E-pair | Etherington et al. 2022, MNRAS (stac2639) | 2202.09201 (nonexclusive-distrib/1.0) | SLACS; BELLS GALLERY | observed: effective Einstein radius (power law + shear; re-model of existing imaging) | 59 (SLACS 42 or 43, GALLERY 16 or 17: readers differ) | SLACS range; GALLERY ≈0.55 | tier 1: Zenodo 10.5281/zenodo.6104823, autolens_etherington_0.zip (2 651 910 747 bytes; md5 1ce502a032f1c6215f3ff7830e940003); tier 2: paper Tables 2–3 | Zenodo: CC BY 4.0 (open) | Zenodo file HEAD 200 |
| R13 | E | Grillo et al. 2008, A&A 477, L25; Grillo et al. 2009, A&A 501, 461 | 0904.3282 (nonexclusive-distrib/1.0); 0712.0680 (assumed-1991-2003) | SLACS | baryonic: SDSS ugriz SED (BC03, M05; Salpeter, Chabrier, Kroupa), total and inside R_E; observed side quoted from R5 | 57 (2009); 15 (2008 letter) | z_l 0.06–0.51; z_s 0.20–1.19 | tier 1: VizieR J/A+A/501/461 (table1.dat, table4.dat per directory listing, reader B); tier 2: paper Tables 1 and 4 | VizieR: none shown (reader B); B2FIND: OpenAccess, rights per the CDS licence page (reader A) | VizieR no; A&A site 403; arXiv PDF yes |
| R15 | E-pair | Brownstein et al. 2012, ApJ 744, 41 (BELLS I) | 1112.3683 (nonexclusive-distrib/1.0) | BELLS | observed: θ_E (SIE); z_L, z_S (BOSS spec.); photometry (I814) | 25 grade-A | ≈0.4–0.7 | tier 2: Table 5; IOP ascii apj413791t1–t6 | IOP page: © 2012 AAS, all rights reserved | IOP ascii HEAD 200; arXiv PDF yes |
| R17 | E-pair | Shu et al. 2016, ApJ 833, 264 (BELLS IV, GALLERY) | 1608.08707 (nonexclusive-distrib/1.0) | BELLS GALLERY | observed: b_SIE + shear (two lens-light subtractions); z_L, z_S (BOSS spec.) | 17 grade-A | ≈0.55 (z_S 2–3) | tier 2: Table 2; IOP ascii apjaa4c32t1–t4 | IOP page: © 2016 AAS, all rights reserved | IOP ascii HEAD 200; arXiv PDF yes |
| R18 | E-pair | Gavazzi et al. 2012, ApJ 761, 170 (SL2S I) | 1202.3852 (nonexclusive-distrib/1.0) | SL2S | observed: R_Ein (SIE); z_d only | 16 | 0.2–0.9 | tier 2: Table 2; IOP ascii apj451452t1–t2 | IOP page: © 2012 AAS, all rights reserved | IOP ascii HEAD 200; arXiv PDF yes |
| R19 | E | Ruff et al. 2011, ApJ 727, 96 (SL2S II) | 1008.3167 (nonexclusive-distrib/1.0) | SL2S | observed: M_Ein (R_Ein from R18); baryonic: BC03 CFHT (bands: ugriz per reader A, griz per reader B), total; some z_s from a σ-weighted pdf (not plotted, D-063 item 3) | 11 | median 0.5 | tier 2: Tables 2–3; IOP ascii apj375610t1–t3 | IOP page: © 2011 AAS, all rights reserved | IOP ascii HEAD 200; arXiv PDF yes |
| R20 | E | Sonnenfeld et al. 2013, ApJ 777, 97 (SL2S III) | 1307.4764 (nonexclusive-distrib/1.0) | SL2S | observed: R_Ein (SIE, Table 6); baryonic: BC03 fit to CFHT ugriz, separate NIR (J, H, Ks) version, Chabrier and Salpeter, total (Table 7) | 56 candidates (39 grade-A) | 0.2–0.8 (R21) | tier 1: IOP machine-readable tables apj485108t4_mrt.txt–t7_mrt.txt (Tables 4–7); ascii t1–t3 | IOP page: © 2013 AAS, all rights reserved | IOP MRT HEAD 200 (text/plain); arXiv PDF yes |
| R21 | E-pair | Sonnenfeld et al. 2013, ApJ 777, 98 (SL2S IV) | 1307.4759 (nonexclusive-distrib/1.0) | SL2S | redshifts: spectroscopic z_d, z_s (Table 2); R_Ein re-tabulated from R20 | 36 secure (7 grade-A lack z_s) | z_d 0.2–0.8; z_s 1–3.5 | tier 2: Table 2; IOP ascii apj484450t1–t4 | IOP page: © 2013 AAS, all rights reserved | IOP ascii HEAD 200; arXiv PDF yes |
| R22 | E | Sonnenfeld et al. 2015, ApJ 800, 94 (SL2S V) | 1410.1881 (nonexclusive-distrib/1.0) | SL2S | for the new subset only: spectroscopy (Table 1, 8 systems), SIE models (Table 3, 5 systems), CFHT ugriz SPS stellar masses (Table 2, 6 systems; Chabrier and Salpeter) | 5–8 new or updated | — | tier 2: Tables 1–3; IOP ascii apj507479t1–t7 | IOP page: © 2015 AAS, all rights reserved | IOP ascii HEAD 200; arXiv PDF yes |
| R24 | E-pair | Sheu et al. 2025, MNRAS 541, 1 (Project Dinos II) | 2408.10316 (CC-by/4.0) | SL2S | observed: θ_E (power law + shear; new HST F475X imaging); re-model | 21 SL2S (README: 20) | full sample 0.090–0.884 | tier 2: Table 1; GitHub williyamshoe/dinos2 at b3e5671af7d7 (2024-08-18): no per-lens parameter table found in the file tree (hierarchical inputs only) | GitHub: no LICENSE file in the tree (none shown) | git clone (blob-less) yes; raw README yes; GitHub web, API and codeload 403; arXiv PDF yes |
| R25 | E | Smith, Lucey & Conroy 2015, MNRAS 449, 3441 (SNELLS) | 1503.02661 (nonexclusive-distrib/1.0) | SNELLS | observed: R_Ein, M_Ein (SNL-0 from an existing model; SNL-1, SNL-2 half the image separation); baryonic: 2MASS J luminosity inside R_Ein × Kroupa M/L; gas statement | 3 | 0.031–0.052 | tier 2: Table 2 | MNRAS page not reachable (403); paper: no data statement | arXiv PDF yes |
| R26 | E-pair | Newman et al. 2017, ApJ 845, 157 | 1612.00065 (nonexclusive-distrib/1.0) | SNELLS | baryonic: r-band luminosity inside θ_Ein (HST F625W for SNL-0) × spectroscopic Kroupa M/L (also IMF-free variants, never default); θ_Ein from R25 | 3 | 0.031–0.052 | tier 1: VizieR J/ApJ/845/157 table1.dat; IOP ascii apjaa816dt1 and MRT apjaa816dt2_mrt.txt (spectra) | VizieR ReadMe: no licence statement (readers); IOP page: © 2017 AAS, all rights reserved | VizieR no; IOP ascii and MRT HEAD 200; arXiv PDF yes |
| R27 | E-pair | Collier, Smith & Lucey 2020, MNRAS 494, 271 (MNELLS) | 2002.07191 (nonexclusive-distrib/1.0) | MNELLS | observed: J0403−0239 R_Ein from a new HST PyAutoLens model, printed in running text only | 1 galaxy-scale lens (52 ETGs searched) | < 0.07 | tier 2 (text only, flagged) | MNRAS page not reachable (403); paper: none shown | arXiv PDF yes |
| R28 | E | Smith et al. 2005, ApJ 625, L103; Smith & Lucey 2013, MNRAS 434, 1964 (ESO 325-G004) | 1306.4983 (nonexclusive-distrib/1.0); astro-ph/0504453 (assumed-1991-2003) | SNELLS (SNL-0) | 2013: observed R_Ein, M_Ein (measured z_s); baryonic F814W luminosity inside R_Ein × Kroupa M/L (Lick indices); gas statement. 2005: model with assumed z_s (no mass) | 1 | 0.0345 | tier 2: 2013 Table 3 | IOP page (2005): © 2005 AAS, all rights reserved; MNRAS page (2013) not reachable (403) | arXiv PDF yes; IOP page yes (no table files) |
| R29 | E | Collier, Smith & Lucey 2018, MNRAS 478, 1595 | 1803.07082 (nonexclusive-distrib/1.0) | MNELLS | observed: R_Ein = half the image separation, M_Ein in text; baryonic: Pan-STARRS i-band luminosity inside R_Ein × Kroupa M/L (MUSE ages) | 1 (J0403−0239) | 0.066 | tier 2 (text only) | MNRAS page not reachable (403); paper: none shown | arXiv PDF yes |
| R30 | E | O'Riordan et al. 2025, A&A 694, A145 (Euclid, NGC 6505) | 2502.06505 (nonexclusive-distrib/1.0) | Euclid NGC 6505 | observed: θ_E (power law + shear and/or multipole; Table 2); baryonic: Prospector stellar mass inside the Einstein radius, Chabrier (Table 1 photometry) | 1 | 0.042 | tier 2: Tables 1–2 | A&A site 403; paper: Euclid data in MER tile 102158889, no licence shown | arXiv PDF yes |
| R31 | E-pair | Wang et al. 2026, A&A 714, A158 (ESO0286) | 2603.26894 (CC-by-nc-sa/4.0) | SNELLS (SNL-1) | observed: Einstein mass from new EPL and PIEMD models of HST imaging (re-model by another team) | 1 | 0.0312 | tier 2: Table 1 / Sect. 3.2 text | A&A site 403; paper: no data statement | arXiv PDF yes |
| R32 | E | Smith 2017, MNRAS 464, L46; Smith et al. 2020, MNRAS 493, L33 | 1911.06338 (nonexclusive-distrib/1.0); 1608.01967 (nonexclusive-distrib/1.0) | MaNGA | 2020: observed θ_Ein, R_Ein, M_Ein (SIE); baryonic i-band luminosity inside θ_Ein × Kroupa M/L (readers differ: assumed age range vs ages from spectral fits); gas statement | 2 | ≈0.12 | tier 2: 2020 Table 1 | MNRAS page not reachable (403); 2017: SDSS DR13 data statement | arXiv PDF yes |
| R33 | E-pair | Poci & Smith 2022, MNRAS 512, 5298 | 2203.09309 (CC-by/4.0) | SNELLS (SNL-1) | baryonic: F814W MGE (Table A1) with spatially resolved MUSE stellar M/L, revised Kroupa | 1 | — | tier 2: Table A1 | paper: raw data in the ESO archive; products on request; no licence shown | arXiv PDF yes |
| R34 | E | Spiniello et al. 2011, MNRAS 417, 3000 (XLENS I) | 1103.4773 (nonexclusive-distrib/1.0) | Cosmic Horseshoe | baryonic: stellar mass inside R_E printed as a fraction of the R60 Einstein mass (D-063 item 7, flagged); SDSS g, r, i; Salpeter and Chabrier | 1 | 0.444 | tier 2: Table 4 | MNRAS page not reachable (403); paper: none shown | arXiv PDF yes |
| R35 | E-pair | Treu & Koopmans 2004, ApJ 611, 739; Koopmans & Treu 2002, ApJ 568, L5; 2003, ApJ 583, 606 (LSD) | astro-ph/0401373 (assumed-1991-2003); astro-ph/0201017 (assumed-1991-2003); astro-ph/0205281 (assumed-1991-2003) | LSD | observed: SIE models (TK04 Table 4; 2003 R_E); photometry only | 5 | 0.485–1.004 | tier 2: TK04 Table 4 | IOP pages: © 2002, 2003, 2004 AAS, all rights reserved | arXiv PDF yes; IOP pages yes (no table files) |
| R36 | E-pair | Keeton, Kochanek & Falco 1998, ApJ 509, 561; Kochanek et al. 2000, ApJ 543, 131 (CASTLES) | astro-ph/9708161 (assumed-1991-2003); astro-ph/9909018 (assumed-1991-2003) | CASTLES | observed: SIS/SIE models (1998 Table 5); image separation from SIS critical radius (2000); photometry only; some lens z photometric | 17 (1998); 30 (2000) | ≈0.1–1 | tier 2: 1998 Table 5; 2000 Table 3 | IOP pages: © 1998, 2000 AAS, all rights reserved | arXiv PDF yes; IOP pages yes (no table files) |
| R37 | E | Ferreras, Saha & Williams 2005, ApJ 623, L5; Ferreras, Saha & Burles 2008, MNRAS 383, 857 | astro-ph/0503168 (assumed-1991-2003); 0710.3159 (assumed-1991-2003) | CASTLES (2005); SLACS (2008) | both: PixeLens free-form models; BC03 stellar mass in the model aperture (Salpeter and Chabrier); gas statement (2008) | 18 (2005); 9 (2008) | 2005: 0.3–1 plus one z = 0.04 disc bulge (A4) | tier 2: Table 1 of each | IOP page (2005): © 2005 AAS, all rights reserved; MNRAS page (2008) not reachable | arXiv PDF yes |
| R38 | P | Faure et al. 2008, ApJS 176, 19; Faure et al. 2011, A&A 529, A72 (COSMOS) | 1009.1545 (nonexclusive-distrib/1.0); 0802.2174 (nonexclusive-distrib/1.0) | COSMOS | observed: SIE + shear (2011 Table 7); baryonic: Bundy et al. 2006 SED masses (IMF unverified), total; most z_s assumed | 20 modelled (67 candidates) | — | tier 1: VizieR J/ApJS/176/19 (tables 'pcat', 'lens'); tier 2: 2011 Tables 3 and 7 | VizieR resource: no licence shown (readers); IOP page (2008): © 2008 AAS, all rights reserved | VizieR no; A&A site 403; arXiv PDF yes |
| R40 | E-pair | Lagattuta et al. 2010, ApJ 716, 1579 | 0911.2236 (nonexclusive-distrib/1.0) | CASTLES; COSMOS; other | photometry only: GALFIT F814W (R_Ein taken from the literature) | 41 | ≈0.4–0.9 | tier 2: Table 3; IOP ascii apj329017t1–t5 | IOP page: © 2010 AAS, all rights reserved | IOP ascii HEAD 200; arXiv PDF yes |
| R41 | E | Leier et al. 2011, ApJ 740, 97; Leier et al. 2016, MNRAS 459, 3677 (2012 paper X) | 1102.3433 (nonexclusive-distrib/1.0); 1512.00462 (nonexclusive-distrib/1.0) | CASTLES (2011); SLACS (2016) | both: PixeLens models; 2011 BC03 Chabrier stellar mass in the same radii (HST H plus V/I where available); 2016 SPS with the IMF fitted | 21 (2011); 18 (2016) | — | tier 2: 2011 Tables 1–2 (IOP ascii apj401957t1–t2); 2016 Tables 1, 3 | IOP page (2011): © 2011 AAS, all rights reserved; MNRAS page (2016) not reachable | IOP ascii HEAD 200; arXiv PDF yes |
| R43 | E | Li et al. 2025, ApJL 987, L31 (KiDS J0233−3447) | 2503.10180 (CC-by/4.0) | KiDS | both: SIE R_Ein, M_Ein (Table 1); CIGALE stellar mass, 8 bands, Chabrier and Salpeter, total | 1 | ≈1 | tier 2: Table 1; IOP ascii apjlade680t1–t2 | IOP page: © 2025 The Author(s), Creative Commons Attribution 4.0 licence | IOP ascii HEAD 200; arXiv PDF yes |
| R45 | P | Euclid Collaboration: Sonnenfeld et al., Euclid Q1 Golden Lenses (Zenodo 10.5281/zenodo.23681178, 2026-10-27) | — | Euclid Q1 | held (D-063 item 5): record describes SIE Einstein radii, spectroscopic redshifts and lens-light fluxes; files restricted | 95 (record description) | — | tier 1 if released: Zenodo 23681178 (no files listed) | Zenodo: CC BY 4.0 declared; access restricted | record page yes; files not listed |
| R46 | E-pair | Sahu et al. 2024, ApJ 970, 86; Barone et al. 2026, AJ 171, 57 (AGEL DR2) | 2405.15427 (nonexclusive-distrib/1.0); 2503.08041 (nonexclusive-distrib/1.0) | AGEL | observed: R_Eins (SPEMD + shear; Sahu Table A1); redshifts (DR2 Table 4); photometry only | 7 (DR2: 138 with redshifts) | 0.3–0.9 | tier 2: Sahu Table A1 (IOP ascii apjad4ce3t1–t3); DR2 Table 4 | IOP page (Sahu 2024): © 2024 The Author(s), Creative Commons Attribution 4.0 licence | IOP ascii HEAD 200; arXiv PDF yes |
| R47 | E | Bolamperti et al. 2023, A&A 671, A60 (SDSS J0100+1818) | 2211.16528 (CC-by/4.0) | J0100+1818 (A7) | both: GLEE models (Tables 1, 2, 4); CIGALE stellar mass, Salpeter only, total | 1 | 0.581 | tier 2: Tables 1, 2, 4 | A&A site 403; paper: none shown | arXiv PDF yes |
| R49 | E | Grillo et al. 2010, ApJ 710, 372; Eichner et al. 2012, MNRAS 427, 1918; Tu et al. 2009, A&A 501, 475 (Barnabè et al. 2010 is X) | 0912.0744 (nonexclusive-distrib/1.0); 1209.2140 (nonexclusive-distrib/1.0); 0902.4804 (nonexclusive-distrib/1.0) | SLACS (J1538+5817; J1430+4105); SL2S (SL2SJ02176−0513) | both, per system: new lens models; SDSS ugriz Salpeter (Grillo); SDSS griz Salpeter and Chabrier (Eichner); CFHTLS u*griz hyperz Chabrier (Tu); all total | 1 each | — | tier 2: Grillo Table 3 (IOP ascii apj327635t1–t5); Eichner Tables 4–8; Tu Table 3 | IOP page (Grillo 2010): 'Copyright is not claimed for this article. All rights reserved.'; MNRAS and A&A pages not reachable | IOP ascii HEAD 200; arXiv PDF yes |
| R50 | E-pair | Li et al. 2026, MNRAS 548, stag683 (SDSS J0946+1006) | 2602.20889 (CC-by/4.0) | SLACS (J0946+1006) | observed: new composite lens model of HST imaging (stellar M/L from the fit is joint, excluded) | 1 | 0.222 | tier 2: Table 2 | paper: posterior samples on request; MAST imaging; no licence shown | arXiv PDF yes |
| R53 | E-pair | Borsato et al. 2023, MNRAS | 2311.01158 (CC-by/4.0) | Herschel (HST snapshots) | observed: SIE models (Table 7); photometry only (F110W light models) | 23 | — | tier 2: Table 7; Zenodo 10.5281/zenodo.10007041: README (2 459 bytes), DataProducts_Borsato2023.zip (320 276 259 bytes; images and light models, no lens-mass products) | Zenodo: CC BY 4.0 (open) | Zenodo API yes; file HEAD 200; arXiv PDF yes |
| R55 | E-pair | Stacey et al. 2024, A&A 688, A110 | 2403.04850 (CC-by/4.0) | Herschel/SPT (ALMA) | observed: power law + multipoles from ALMA (Table 2) | 3 | — | tier 2: Table 2 | A&A site 403; paper: ALMA archive data, no release | arXiv PDF yes |
| R56 | E-pair | Williams & Zegeye 2020, OJAp 3, 10 (iPTF16geu) | 2006.09391 (CC-by/4.0) | iPTF16geu | observed: two-component models fitted to image positions (readers differ: tier 2 Table 1 vs search ranges only, tier 3) | 1 | 0.2163 | tier 2 or 3 (readers differ) | paper: none shown | arXiv PDF yes |
| R57 | E | Sonnenfeld et al. 2019, A&A 630, A71 (SuGOHI III) | 1904.10465 (nonexclusive-distrib/1.0) | SuGOHI (BOSS CMASS) | both: SIE R_Ein, M_Ein (Tables 4–5); BC03 HSC grizy stellar mass, Chabrier (readers differ: inside R_Ein in the table vs total in the table, inside R_Ein only in Fig. 4) | 23 | spectroscopic z_l; range unverified | tier 2: Tables 4–5 | A&A site 403; paper: chains and code online (URL not read) | arXiv PDF yes |
| R60 | E-pair | Dye et al. 2008, MNRAS (Cosmic Horseshoe) | 0804.4002 (nonexclusive-distrib/1.0) | Cosmic Horseshoe | observed: SIE, power-law and NFW models (Table 2); mass inside the Einstein ring in text | 1 | 0.44 | tier 2: Table 2 and text | MNRAS page not reachable (403); paper: no data statement | arXiv PDF yes |
| R61 | E | Collier, Smith & Lucey 2018, MNRAS (stx2297) | 1709.01931 (nonexclusive-distrib/1.0) | SNELLS (SNL-1 |  SNL-2) | observed: lensing mass inside a fiducial aperture R_ap (Table 2; new HST imaging, lensmodel); baryonic: F814W luminosity inside R_ap (Table 1) × Kroupa M/L from R26 | 2 | 0.0312, 0.0519 | tier 2: Tables 1–2 | MNRAS page not reachable (403); paper: no data statement |
| R63 | E-pair | Tan et al. 2024, MNRAS (Project Dinos I) | 2311.09307 (CC-by/4.0) | SLACS; SL2S; BELLS | observed: θ_E, power law + shear (re-model of archival HST imaging) | 77 (34 SLACS, 24 SL2S, 19 BELLS) | SLACS mean ≈0.2; SL2S mean ≈0.6 | tier 1: GitHub Project-Dinos/dinos-i at 6810ea6d8b7f (2025-04-14): 3_model_parameters/Data/SLACS_mass_params.csv (16 866 bytes), SL2S_mass_params.csv (11 778), BELLS_mass_params.csv (9 424), and *_light_params.csv; tier 2: Tables 3–5 | GitHub: no LICENSE file in the tree (none shown) | git clone (blob-less) yes; raw README yes; GitHub web and API 403 |
| R66 | E-pair | Sonnenfeld et al. 2012, ApJ 752, 163 (SDSS J0946+1006) | 1111.4215 (nonexclusive-distrib/1.0) | SLACS (J0946+1006) | baryonic: five-band HST SPS (BC03; Chabrier and Salpeter), per light component and total (Table 8) | 1 | 0.222 | tier 2: Table 8; IOP ascii apj430577t1–t9 | IOP page: © 2012 AAS, all rights reserved | IOP ascii HEAD 200; arXiv PDF yes |
| R67 | E-pair | Shajib et al. 2021, MNRAS (stab536) | 2008.11724 (nonexclusive-distrib/1.0) | SLACS | observed: R_E, power law + shear (re-model of HST imaging; Table 1) | 23 | mean ≈0.2 | tier 2: Table 1 | MNRAS page not reachable (403); paper: no release of lens-model files | arXiv PDF yes |
| R69a | E | Negrello et al. 2010, Science 330, 800 | 1011.1255 (nonexclusive-distrib/1.0) | H-ATLAS SDP | both: θ_E from SMA image positions with an SIS, M_E (Table 2; 2 systems); total stellar mass from SED fits (da Cunha et al. 2008 models; IMF unverified) | 5 (2 with θ_E) | 0.22–0.94 | tier 2: Table 2 | arXiv note (reader A): 'posted here by permission of the AAAS for personal use, not for redistribution' | arXiv PDF yes |
| R69c | E | Dye et al. 2014, MNRAS 440, 2013 | 1311.5893 (nonexclusive-distrib/1.0) | H-ATLAS SDP | both: θ_E (power law + shear; Table 1); stellar mass inside R_e/2 from Negrello et al. 2014 totals (Table 3; source not screened) | 5 | 0.22–0.94 | tier 2: Tables 1, 3 | MNRAS page not reachable (403); paper: none shown | arXiv PDF yes |
| R69d | E-pair | Dye et al. 2018, MNRAS (sty513) | 1705.05413 (nonexclusive-distrib/1.0) | Herschel ALMA | observed: θ_E, power law + shear (Table 3) | 6 | 0.215–0.663 | tier 2: Table 3 | MNRAS page not reachable (403); ALMA project 2013.1.00358.S | arXiv PDF yes |
| R69e | E-pair | Amvrosiadis et al. 2018, MNRAS 475, 4939 | 1801.07282 (nonexclusive-distrib/1.0) | Herschel ALMA | observed: θ_E = half the image separation (D-063 item 2; alternative where R69d or R69f model the system) | 14–16 ALMA (readers differ) + 18 SMA compiled | 0.215–0.976 | tier 2: Tables 1–2 | MNRAS page not reachable (403); paper: none shown | arXiv PDF yes |
| R69f | E-pair | Maresca et al. 2022, MNRAS (stac585) | 2111.09680 (CC-by/4.0) | Herschel ALMA | observed: θ_E, power law + shear (Table 3) | 7 (4 galaxy-scale, 3 group-scale) | 0.426–0.976 where known | tier 2: Table 3 | paper: derived data on request; ALMA project 2013.1.00358.S | arXiv PDF yes |


## 2. Precedence by survey (metadata only)

How the script applies the frozen rule:
- **Observed side (§2):** originals first (§2.1); then a full lens model before an image-separation or ring-radius estimate (§2.2; D-063 item 2); then, among the survey's own models, the most recent paper that does not only re-use an earlier model (§2.3). The script flags a conflict if an original gives only an image-separation estimate while a re-model is a full model. No such conflict occurs.
- **Stellar mass (§3.3):** σ-based priors, lensing or dynamical masses, and IMF-free fits (D-063 item 1) are excluded as defaults. The rest are ranked by more photometric bands, then a per-object population fit, then the most recent. Band counts are held as ranges where the readers give a range, and the order is checked at both ends of the range. Where the ends disagree, the result is marked provisional.
- **Scopes.** A survey is split where records cover different subsets: for example SLACS lenses modelled in SLACS V against the 11 new models in SLACS IX, the SL2S V additions, each SNELLS lens, and single-system papers. A scope row marked "membership not checked" applies only if that system is among the larger record's lenses. That check needs the identifier columns and has not been made.
- **N with both (upper bound)** is the smallest of the lens counts of the observed default, the stellar-mass default and any redshift record in that scope. It is a ceiling before four checks: per-system membership, kind (late-type and group lenses), spectroscopic source redshifts, and the D-066 cut at z < 0.30.

### Result table (generated)

| Survey | Scope | Observed default | Observed alternatives | Stellar-mass default | Stellar-mass alternatives | Redshifts from | N with both (upper bound) | Flags |
|---|---|---|---|---|---|---|---|---|
| SLACS | V-modelled lenses | R5 | R12; R3; R37; R41; R63; R67; R7 | R13 | R37; R41; R7 | (with the observed side) | 57 | R7 excluded as default: prior uses the lens's own sigma (§3.3; D-063 item 3)<br>R9 excluded as default: not usable: N (no per-lens table for SLACS lenses)<br>R41 excluded as default: IMF fitted, not a fixed named IMF (D-063 item 1) |
| SLACS | IX new models | R7 | — | none | R7 | (with the observed side) | 0 | no eligible default stellar mass<br>R7 excluded: prior uses the lens's own sigma (§3.3; D-063 item 3) |
| SLACS | J1538+5817 | R5 | R49 | R49 | R13 | (with the observed side) | 1 | conditional: membership of this system in R5 not checked<br>mstar_in_RE_from_profile needed (default prints total)<br>single IMF printed: range from the model paper's Chabrier-to-Salpeter ratio (§3.2) |
| SLACS | J1430+4105 | R5 | R49 | R13 | R49 | (with the observed side) | 1 | conditional: membership of this system in R5 not checked<br>conditional: membership of this system in R13 not checked |
| SLACS | J0946+1006 | R5 | R50 | R66 | R13 | (with the observed side) | 1 | conditional: membership of this system in R5 not checked<br>mstar_in_RE_from_profile needed (default prints total (per light component)) |
| S4TM | S4TM lenses | R10 | — | R10 | — | (with the observed side) | 40 | mstar_in_RE_from_profile needed (default prints total) |
| BELLS | BELLS lenses | R15 | R63 | none | — | (with the observed side) | 0 | no stellar-mass source |
| BELLS GALLERY | GALLERY lenses | R17 | R12 | none | — | (with the observed side) | 0 | no stellar-mass source |
| SL2S | SL2S III sample | R20 | R18; R19; R24; R63 | R20 | R19 | R21 | 36 | mstar_in_RE_from_profile needed (default prints total) |
| SL2S | SL2S V added | R22 | — | R22 | R20 | R22 | 5 | band count order undetermined between R20 and R22 (outcome depends on per-system band counts): provisional<br>mstar_in_RE_from_profile needed (default prints total) |
| SL2S | SL2SJ02176-0513 | R20 | R49 | R20 | R49 | (with the observed side) | 1 | conditional: membership of this system in R20 not checked<br>mstar_in_RE_from_profile needed (default prints total)<br>conditional: membership of this system in R20 not checked |
| SNELLS | SNL-0 (ESO 325-G004) | R28 | R25 | R26 | R25; R28 | (with the observed side) | 1 | aperture is 'inside θ_Ein of R25 (luminosity × M/L)': check it matches the default R_E |
| SNELLS | SNL-1 (ESO 286-G022) | R61 | R25; R31 | R33 | R25; R26; R61 | (with the observed side) | 1 | mstar_in_RE_from_profile needed (default prints profile (MGE)) |
| SNELLS | SNL-2 | R61 | R25 | R61 | R25; R26 | (with the observed side) | 1 | aperture is 'inside R_ap (luminosity × M/L)': check it matches the default R_E |
| MNELLS | J0403-0239 | R27 | R29 | R29 | — | (with the observed side) | 1 | aperture is 'inside R_E of R29 (luminosity × M/L)': check it matches the default R_E |
| MaNGA | J1436+4943 | R32 | — | R32 | — | (with the observed side) | 1 | — |
| MaNGA | J1701+3722 | R32 | R32-2017 | R32 | — | (with the observed side) | 1 | — |
| Euclid NGC 6505 | NGC 6505 | R30 | — | R30 | — | (with the observed side) | 1 | — |
| KiDS | J0233-3447 | R43 | — | R43 | — | (with the observed side) | 1 | mstar_in_RE_from_profile needed (default prints total) |
| SuGOHI | CMASS lenses | R57 | — | R57 | — | (with the observed side) | 23 | aperture disputed between readers: read at source before packaging |
| Cosmic Horseshoe | J1148+1930 | R60 | — | R34 | — | (with the observed side) | 1 | — |
| J0100+1818 (A7) | J0100+1818 | R47 | — | R47 | — | (with the observed side) | 1 | mstar_in_RE_from_profile needed (default prints total)<br>single IMF printed: range from the model paper's Chabrier-to-Salpeter ratio (§3.2) |
| LSD | LSD lenses | R35 | — | none | — | (with the observed side) | 0 | no stellar-mass source |
| CASTLES | CASTLES lenses | R36 | R37; R41 | R41 | R37 | (with the observed side) | 17 | band count not read for R41 or R37: order provisional<br>aperture is 'same radii as the model': check it matches the default R_E |
| COSMOS | COSMOS lenses | none | — | none | R38 | (with the observed side) | 0 | no usable observed-side source<br>no eligible default stellar mass<br>R38 excluded: not usable: N (P: IMF unverified) |
| AGEL | AGEL pilot | R46 | — | none | — | (with the observed side) | 0 | no stellar-mass source |
| H-ATLAS SDP | SDP lenses | R69c | R69a | none | R69a; R69c | (with the observed side) | 0 | no eligible default stellar mass<br>R69a excluded: not usable: N (IMF not stated)<br>R69c excluded: not usable: N (source not screened) |
| Herschel ALMA | ALMA lenses | R69f | R55; R69d; R69e | none | — | (with the observed side) | 0 | no stellar-mass source |
| Herschel HST | HST snapshot lenses | R53 | — | none | — | (with the observed side) | 0 | no stellar-mass source |
| iPTF16geu | iPTF16geu | R56 | — | none | — | (with the observed side) | 0 | no stellar-mass source |

### Reading of the result, per survey

| Survey | Default observed side | Default stellar mass | N with both (ceiling) | Lens z as read (D-066 relevance) |
|---|---|---|---|---|
| SLACS | R5 (SLACS V), for its 63 models; R7 (SLACS IX) for its 11 new models | R13 (Grillo et al. 2009, SDSS ugriz, three IMFs, inside R_E as printed) | 57 | 0.06–0.51: part below 0.30 |
| S4TM | R10 (SLACS XIII) | R10 table2 (R9 method; single band, fixed SSP) | 40 | 0.06–0.44: part below 0.30 |
| BELLS | R15 (BELLS I) | none | 0 | ≈0.4–0.7: all above 0.30 |
| BELLS GALLERY | R17 (BELLS IV) | none | 0 | ≈0.55: all above 0.30 |
| SL2S | R20 (SL2S III); R22 (SL2S V) for its additions | R20 (CFHT ugriz, NIR version where available); R22 for its additions (provisional) | 36 + 5 | 0.2–0.8: part below 0.30 |
| SNELLS | R28 (Smith & Lucey 2013) for SNL-0; R61 (Collier et al. 2018) for SNL-1 and SNL-2 | R26 for SNL-0; R33 for SNL-1; R61 for SNL-2 | 3 | ≤ 0.052: all below 0.30 |
| MNELLS | R27 | R29 | 1 | 0.066 |
| MaNGA | R32 (2020) | R32 (2020) | 2 | ≈0.12 |
| Euclid NGC 6505 | R30 | R30 | 1 | 0.042 |
| SuGOHI III | R57 | R57 (aperture disputed) | 23 | not read |
| CASTLES | R36 (CASTLES 1998 models) | R41 (Leier et al. 2011; provisional) | 17 | ≈0.1–1: mostly above 0.30 |
| KiDS, Cosmic Horseshoe, J0100+1818 (A7) | R43; R60; R47 | R43; R34 (fraction × M_E, flagged); R47 | 1 each | ≈1; 0.444; 0.581: all above 0.30 |
| LSD, AGEL, H-ATLAS SDP, Herschel ALMA, Herschel HST, iPTF16geu | R35; R46; R69c; R69f; R53; R56 | none | 0 | most above 0.30 |
| COSMOS (P) | none (most z_s assumed) | none (IMF not verified) | 0 | — |
| Euclid Q1 Golden Lenses (P) | held: files restricted | — | — | — |

Points that need JvH's attention, because the frozen text does not settle them from metadata alone:
1. **SLACS, §2.4.** The default model (R5) prints θ_E only, while R7 prints M_E for the same R5 models. Read literally, §2.4 computes M_E from R5's θ_E with the D-064 formula, and R7's printed M_E then serves as the §4 "reported" check. The alternative is to take R7's printed value as "M_E as printed" for that model. *Recommendation:* the literal reading, because it keeps the default record and the check separate.
2. **SNELLS SNL-1 and SNL-2.** The default observed record (R61, named in §2.1) prints the lensing mass inside a fiducial aperture R_ap. Whether R_ap is R_E was not read. If it is not, D-064 needs R_E, and R61 Table 1 (half the image separation) or R25 would supply it. This must be read at source before packaging.
3. **Aperture matching.** For SNL-0 the stellar-mass default (R26) uses R25's θ_Ein, not the R_E of the observed default (R28). For J0403−0239 the stellar mass (R29) uses R29's half-separation radius, not R27's model radius. §3.1 allows computing the cylinder mass from the source's own light profile. Whether R26 and R29 print enough of a profile to do that is not yet read.
4. **Coding choices made here** (open to correction): R7 is coded as re-using R5's models for the 63 SLACS V lenses; R19 as re-using SL2S I radii; R25 as re-using the 2005 model for SNL-0; Project Dinos II (R24) as an alternative, as §2.1 names it, although it took new HST imaging; single-system papers (R49 Grillo 2010, Eichner 2012, Tu 2009) as re-models, because the authors' survey membership was not checked.

## 3. Gaps per survey

| Survey | Gap | Consequence |
|---|---|---|
| SLACS | No stellar mass without the σ prior for the 11 lenses modelled first in SLACS IX (R13 covers R5's lenses only) | Those 11 recorded, not plotted, unless a later source is found |
| SLACS | VizieR tables of R5, R7 and R13 unreachable (CDS, GAVO and mirrors refuse the workspace). R5 and R13 have no reachable machine-readable copy: R5's IOP page links no table files, and A&A is unreachable. R7 has IOP ascii tables t1–t5 | R5 and R13 from the arXiv PDF tables (tier 2), or VizieR fetched from elsewhere |
| SLACS | Membership of J1538+5817, J1430+4105 and J0946+1006 in R5 and R13 not checked. The SLACS VI model of J0946+1006 (Gavazzi et al. 2008) is not a screened record | Read the identifier columns; screen Gavazzi et al. 2008 |
| SLACS | Licence: VizieR none shown; IOP © AAS, all rights reserved; Zenodo 13366012 (CC BY 4.0) is the redistribution route under D-063 item 8, after a value-by-value check | Link, not redistribute, until the check passes |
| S4TM | Stellar mass is total only | `mstar_in_RE_from_profile` needed; whether R10 prints a light-profile size (R_e) was not read |
| S4TM | Single band, fixed SSP (not a per-object fit) | Only source; flagged |
| BELLS, BELLS GALLERY | No stellar mass in any eligible record | 0 plotted; all above z = 0.30 in any case (D-066) |
| SL2S | Stellar masses are totals | `mstar_in_RE_from_profile` needed from the R20 photometry tables |
| SL2S | 7 grade-A without spectroscopic z_s; σ-assisted z_s in R19 | Recorded, not plotted (D-063 items 3 and 5) |
| SL2S | Which R20 systems have the NIR fit; R19 tabulated IMF (readers differ on bands) | Decides the provisional R22 vs R20 order for SL2S V additions |
| SNELLS | R_ap vs R_E (R61); aperture mismatch for SNL-0 (R26); SNL-1 default (R33) is an MGE profile | `mstar_in_RE_from_profile` for SNL-1; read R61 and R26 for apertures |
| SNELLS, MNELLS, MaNGA | All tier 2 (paper tables or text); MNRAS pages unreachable (403); no data licence shown | Link to the source; values transcribed with citation |
| MNELLS | R27 radius in text only (tier 2, flagged, deviation #16) | As adjudicated |
| MaNGA | Readers differ on whether R32's M/L is a per-object fit or an assumed age range | Read at source; affects the assumption range, not the default (single source) |
| SuGOHI III | Readers differ on whether the table gives the stellar mass inside R_Ein or the total; lens z range not read | Read at source |
| CASTLES | Band counts of R37 not read; some lens z photometric (K00); source z per system not checked; mixed morphologies | Provisional default; redshift check needed |
| H-ATLAS SDP | R69a IMF not stated; R69c stellar masses come from Negrello et al. 2014 (arXiv:1311.5898), not screened; aperture R_e/2 | 0 with a default stellar mass until Negrello et al. 2014 is screened |
| KiDS, J0100+1818 | Total stellar masses only | `mstar_in_RE_from_profile` needed; both above z = 0.30 |
| COSMOS (P) | IMF of Bundy et al. 2006 masses not verified; most z_s assumed | Not plotted |
| Euclid Q1 Golden Lenses (P) | Zenodo files restricted (access "restricted", no files listed) | Held (D-063 item 5) |
| Project Dinos I and II | GitHub: no LICENSE file in either tree | Alternatives only; link, not redistribute |
| All AAS-journal tables | IOP pages state © AAS, all rights reserved, except R43 and R46 (CC BY 4.0) and R49 Grillo 2010 ("Copyright is not claimed for this article") | Link to the source; redistribution question for JvH where a package would carry the files |

**Unreadable from this workspace:** CDS and VizieR (all mirrors: connection reset or 403), GAVO, ADS (405), doi.org, A&A (aanda.org), OUP (academic.oup.com), GitHub web, API and codeload (403), MAST, slacs.org, projectdinos.com, the CASTLES site, B2FIND, and export.arxiv.org. Reachable: arxiv.org, iopscience.iop.org (with the bot-check note above), content.cld.iop.org, zenodo.org, raw.githubusercontent.com, and git over HTTPS to github.com.

## 4. Gas inside the Einstein radius (§3.4): candidates, not judged

System-level statements in eligible records (quoted by the screening readers; locations as given there):

| System | Record | Statement (as quoted by the reader) | Location |
|---|---|---|---|
| ESO 325-G004 (SNL-0) | R28, Smith & Lucey 2013 | "We assume the gas mass projected within the Einstein radius is negligible." | footnote 3 (reader-b-block1 R28; arXiv:1306.4983) |
| SNL-0, SNL-1, SNL-2 | R25, Smith, Lucey & Conroy 2015 | "Other possible non-stellar mass contributions within the Einstein radius, e.g. gas and central black holes, are neglected." | reader-b-block1 R25; arXiv:1503.02661 |
| J1436+4943, J1701+3722 | R32, Smith et al. 2020 | "(and in principle from a central black hole, gas, etc but these are expected to be negligible)" | reader-b-block2 R32; arXiv:1911.06338 |
| MG2016+112 | R35, Koopmans & Treu 2002 | Chandra shows "no evidence for hot X-ray gas" (cited) | reader-a-block2 R35; arXiv:astro-ph/0201017 |
| SNL-1 | R61 | dust "suggests the presence of a small cold ISM disc" (not quantified) | reader-a-round2 R61; arXiv:1709.01931 |
| SNL-1 | R26 | nebular emission "likely driven by the presence of warm gas" (no mass) | reader-a-block1 R26; arXiv:1612.00065 |
| J0403−0239 | R29 | spectrum "contaminated by gas emission" (no mass) | reader-b-block1 R29; arXiv:1803.07082 |
| NGC 6505 | R30 | cites a prior X-ray observation (Henry et al. 1995); no statement inside θ_E | reader-b-block1 R30; arXiv:2502.06505 |

Statements for the kind, made inside eligible or screened records:

| Record | Statement (as quoted by the reader) | Location |
|---|---|---|
| R31, Wang et al. 2026 | "In most cases, the gas content in elliptical galaxies can be safely neglected" | reader-b-block2 R31; arXiv:2603.26894 |
| R37, Ferreras, Saha & Burles 2008 | "Other baryonic components, hot and cold gas or dust, are known to contribute a small fraction to the net baryon budget in these systems (Roberts & Haynes 1994)." | reader-a-block2 R37; arXiv:0710.3159 |
| R49, Eichner et al. 2012 | gas "incorporated in either the dark matter or the de Vaucouleurs component"; cites a literature molecular-gas fraction | reader-a-block2 R49; arXiv:1209.2140 |
| R8 (X), Auger et al. 2010 | "any gas is effectively treated as dark matter" | reader-a-block1 R8; arXiv:1007.2880 |
| R64 (X), Treu et al. 2010 | a discussion paragraph cites X-ray literature on residual hot gas | reader-b-round2 R64; arXiv:0911.3392 |

Literature on gas in early-type galaxies, located only (title, DOI and journal read at arXiv; content not read):

| Citation | arXiv | DOI |
|---|---|---|
| Young et al. 2011, "The Atlas3D project – IV: the molecular gas content of early-type galaxies" | 1102.4633 | 10.1111/j.1365-2966.2011.18561.x |
| Serra et al. 2012, MNRAS 422, 1835, "The Atlas3D project – XIII. Mass and morphology of HI in early-type galaxies as a function of environment" | 1111.4241 | 10.1111/j.1365-2966.2012.20219.x |
| Mathews & Brighenti 2003, ARA&A 41, 191, "Hot Gas In and Around Elliptical Galaxies" | astro-ph/0309553 | 10.1146/annurev.astro.41.090401.094542 |
| Diehl & Statler 2007, "The Hot Interstellar Medium of Normal Elliptical Galaxies. I." | astro-ph/0606215 | 10.1086/521009 |
| Roberts & Haynes 1994 (cited by R37) | not located | — |

None of these has been read for a statement about gas inside the Einstein radius. Under §3.4, a statement must be quoted and read at source before any system is marked "absent (literature limit for this kind)". If none qualifies, the cell returns to JvH.

## 5. Disclosures

- Prepared with AI assistance (Claude). The coding of `a6s_options.csv` (original or re-model, re-use, scope, band ranges, aperture class) is Claude's reading of the screening files and is open to JvH's correction. The script only applies the frozen order to that coding.
- No data table was opened, and no measured value of any kind was seen in preparing this file. Redshift ranges and lens counts are as the screening readers recorded them.
- The IOP bot check was passed by sending a browser user-agent string. No login, cookie or other circumvention was used. **Claude's note (2026-10-31):** sending a browser user-agent to get past a site's bot check is circumvention and was not authorised. It will not be repeated. The IOP copyright lines and table-file names recorded here (rows marked IOP) will be re-checked in JvH's browser before any IOP table is fetched for a package, and package fetches will not use a spoofed user-agent.
- The SLACS IX VizieR directory listing and the GAVO record were read through WebFetch, because the workspace cannot reach CDS or GAVO. The ReadMe could not be fetched by either route.
- Downloads (arXiv abstract pages, IOP article pages, Zenodo JSON, GitHub trees) are kept outside the repository, in the session scratchpad. Only the derived metadata files listed above are in `packaging-tools/`.

## 6. Next step

Extract only the identifier and redshift columns from the reachable tables: IOP ascii and MRT files for R7, R10, R15, R17, R20, R21 and R22, the Dinos I GitHub tables, and the arXiv PDF tables for R5 and R13. Then:
- cross-match the systems;
- settle the "membership not checked" rows;
- count spectroscopic source redshifts;
- apply the D-066 cut.

This turns each ceiling in §2 into a count. Before that, JvH rules on point 1 of §2 (SLACS §2.4), and R61's R_ap is read at source (point 2).
