# Search log: cell A3·random (globular clusters × random motions)

> Run on 2026-10-29 after the protocol freeze (see `docs/plans/DEVIATIONS.md` #1 and #2). The run calls itself "pre-freeze" or "exploratory" below because the protocol's status line had not been updated; the freeze record is authoritative. ADS and VizieR steps pending (deviation #2). AI-run (Claude); metadata only.

- **Date run:** 2026-10-29
- **Run by:** Claude (AI), for JvH. The search used literature, metadata, ReadMe and data-documentation pages only. No data table was downloaded. No candidate was compared, computed or plotted for g_obs and g_bar. No result about the acceleration discrepancy was read for this log or is reported in it.
- **Protocol:** `docs/plans/SELECTION_PROTOCOL.md` (draft, **not yet frozen**), §1, §1a, §2 row A3·random, §3 and §4. Method rulings that apply: D-025 (half-light-radius estimator, Wolf et al. 2010; global or luminosity-weighted line-of-sight σ; "Where a source gives only a profile and no global value, the system is recorded but not plotted"), D-034 (baryon statuses) and D-035 (evidence tiers).
  - §2 A3 observed side: "Velocity-dispersion values or binned profiles measured from stellar velocities; not a dynamical mass alone".
  - §2 A3 baryonic side: "Luminosity, or a luminosity profile, with a stellar-population mass-to-light ratio (registered); a dynamical M/L is not a baryonic input".
- **Status of this run: pre-freeze scoping run.** §3 says the logged search runs after the protocol is frozen on `main`. This run must either be repeated after the freeze or registered in §9 as a deviation. It is also **incomplete on venue** (see §1a): ADS, native VizieR search, the Zenodo API and the GitHub search API could not be reached.
- **Rule applied:** every statement below was read at source in this session, at the URL given. Anything not read is marked **unverified**. Some fetched pages volunteered numerical dispersion or M/L values. Those values are deliberately left out of this log.

---

## 1. Queries

### 1a. Where queries were run

| Protocol step | Planned venue | Outcome |
|---|---|---|
| §3.1 ADS | ui.adsabs.harvard.edu via WebFetch | **Not reachable.** "URL_NOT_ON_ALLOWLIST". The proxy log also shows api.adsabs.harvard.edu was denied (403). ADS-style queries were run through WebSearch instead (strings below). |
| §3.2 VizieR | vizier.cds.unistra.fr / cdsarc via WebFetch and curl | **Native search not reachable.** curl to cdsarc reset, and vizier.cds.unistra.fr was denied by the proxy (403). VizieR records were found by WebSearch and read through their cdsarc directory, `viz-bin/cite` or GAVO registry pages, wherever WebSearch surfaced those URLs. Several ReadMe files could not be opened (marked unverified). |
| §3.3 Zenodo | zenodo.org/api/records via WebFetch | **Not reachable** ("URL_NOT_ON_ALLOWLIST"). Searched through WebSearch instead, and record pages surfaced by search were read. |
| §3.3 GitHub | `gh search repos` | **Refused:** "HTTP 403: This GitHub API path is not available: sessions are bound to their configured repositories." Searched through WebSearch instead. |
| §3.4 Citations | Reference lists in screened papers, the source list on the Baumgardt `veldis.html` page, and the Frank (2014) review | Partial. Leads that were not followed are in §5. |

### 1b. Query strings, verbatim

ADS query attempted but not executed: `abs:"globular cluster" abs:"velocity dispersion profiles" property:refereed year:1990-2026`

All WebSearch queries were run on 2026-10-29 in standard mode, against the US index.

| # | Query string | Step |
|---|---|---|
| Q1 | `globular clusters velocity dispersion profiles catalogue radial velocities Milky Way` | 1 |
| Q2 | `globular cluster "velocity dispersion" data release catalogue MUSE radial velocities Kamann 2018` | 1 |
| Q3 | `Gaia EDR3 proper motion velocity dispersion profiles globular clusters Vasiliev Baumgardt 2021 catalogue` | 1 |
| Q4 | `HST proper motion velocity dispersion profiles 22 globular clusters Watkins 2015 catalog` | 1 |
| Q5 | `outer halo globular clusters velocity dispersion low acceleration Baumgardt Hilker Kroupa NGC 2419 Pal 14 Pal 4` | 1 |
| Q6 | `Baumgardt Sollima Hilker 2020 absolute V-band magnitudes mass-to-light ratios Galactic globular clusters surface brightness profiles` | 1/4 |
| Q7 | `cdsarc J/MNRAS/478/1520 ReadMe Milky Way globular clusters Baumgardt` | 2 |
| Q8 | `VizieR globular clusters velocity dispersion profiles catalogue` | 2 |
| Q9 | `McLaughlin van der Marel 2005 resolved massive star clusters Milky Way Magellanic Clouds Fornax population-synthesis mass-to-light VizieR J/ApJS/161/304` | 2/4 |
| Q10 | `"J/ApJS/161/304" McLaughlin van der Marel VizieR` | 2 |
| Q11 | `CDS VizieR data licence CC BY 4.0 catalogues terms of use cdsarc` | terms |
| Q12 | `globular clusters intracluster medium gas content upper limits HI ionized gas negligible mass` | §1.7 |
| Q13 | `Strader 2011 M31 globular clusters velocity dispersions mass-to-light ratios stellar population` | 1 |
| Q14 | `Libralato 2022 HST proper motions globular clusters kinematic profiles MAST HLSP velocity dispersion` | 1 |
| Q15 | `Scarpa velocity dispersion outer regions globular clusters test Newtonian low acceleration VLT` | 1 |
| Q16 | `Vasiliev Baumgardt 2021 Gaia EDR3 globular clusters proper motion dispersion profiles data availability zenodo github` | 3 |
| Q17 | `Lane Kiss Lewis 2010 halo globular clusters AAOmega velocity dispersion profiles` | 1 |
| Q18 | `Scarpa Marconi Carraro Falomo Villanova 2011 NGC 1851 NGC 1904 NGC 7099 velocity dispersion profile A&A` | 1 |
| Q19 | `Kamann 2018 MUSE stellar census 22 globular clusters kinematics data release velocity dispersion profiles table` | 1 |
| Q20 | `Palomar 14 velocity dispersion Jordi 2009 Keck radial velocities outer halo globular cluster` | 1 |
| Q21 | `NGC 2419 velocity dispersion profile Ibata 2011 DEIMOS radial velocities table` | 1 |
| Q22 | `Dalgleish 2020 WAGGS integrated light velocity dispersions globular clusters` | 1 |
| Q23 | `Ferraro 2018 MIKiS survey KMOS FLAMES velocity dispersion profiles Galactic globular clusters` | 1 |
| Q24 | `musegc.uni-goettingen.de MUSE globular clusters radial profiles data` | 3 |
| Q25 | `cosmic-lab.eu MIKiS radial velocity catalogs download globular clusters` | 3 |
| Q26 | `Baumgardt globular cluster database individual radial velocities file rv.html` | 3 |
| Q27 | `zenodo globular cluster velocity dispersion data` | 3 |
| Q28 | `github globular clusters velocity dispersion profiles data` | 3 |
| Q29 | `site:github.com globular cluster velocity dispersion profiles` | 3 |
| Q30 | `nmdickson GCfit-results github globular cluster data` | 3 |
| Q31 | `de Boer 2019 globular cluster number density profiles Gaia DR2 81 clusters data` | 4 |
| Q32 | `Baumgardt Hénault-Brunet Dickson Sollima 2023 MNRAS stellar mass functions globular clusters radial velocities update` | 4 |
| Q33 | `Fornax dwarf galaxy globular clusters internal velocity dispersions Larsen 2012 UVES mass-to-light` | 1 |
| Q34 | `NGC 5128 Centaurus A globular clusters internal velocity dispersions mass-to-light ratios Taylor 2015` | 1 |
| Q35 | `Pryor Meylan 1993 velocity dispersions Galactic globular clusters compilation central velocity dispersion catalog` | 1/4 |
| Q36 | `Gaia DR3 internal kinematics globular clusters proper motion dispersion profiles catalogue 2023 2024` | 1 |
| Q37 | `Strader Caldwell Seth 2011 M31 globular clusters velocity dispersions VizieR J/AJ/142/8` | 2 |
| Q38 | `Larsen Brodie Strader 2012 Fornax globular clusters velocity dispersions dynamical masses` | 1 |
| Q39 | `zenodo 14978551 oMEGACat omega Centauri kinematics` | 3 |
| Q40 | `Dumont 2022 NGC 5128 globular clusters velocity dispersions dynamical masses MUSE UVES` | 1 |
| Q41 | `Taylor 2015 observational evidence dark side NGC 5128 globular cluster system velocity dispersions 125 clusters` | 1 |
| Q42 | `outskirts of globular clusters velocity dispersion flattening low acceleration analysis Hernandez Jimenez 2012` | 1 |
| Q43 | `Scarpa Marconi Gilmozzi Carraro 2007 globular clusters NGC 6171 NGC 7099 NGC 288 velocity dispersion A&A 462 L9` | 1 |

Q15, Q42 and Q43 name papers whose titles refer to tests of gravity. Those records were screened for methods and data only, and their conclusions were not read into this log.

---

## 2. Records screened

Decision codes:
- **E**: eligible (both sides, or one side plus a recorded pairing).
- **E-pair**: eligible as the baryonic-side pairing source only.
- **P**: eligible pending a question in §5.
- **X**: excluded.
- **NS**: identified but not screened, because it was not read at source (title or abstract only).
- **—**: not a dataset (a review, or the source of a §1.7 statement).

| # | Record | Source read (URL) | Decision | Protocol reason |
|---|---|---|---|---|
| R1 | Baumgardt et al., Galactic GC Database v4 (Mar 2023): velocity dispersion profiles (`veldis.html`) | https://people.smp.uq.edu.au/HolgerBaumgardt/globular/veldis.html ; https://people.smp.uq.edu.au/HolgerBaumgardt/globular/ | **E** (with D-025 caveat, §5 Q1) | §2 observed side: binned profiles from stellar RVs and PMs. Baryonic side from R2 (same database). |
| R2 | Same database: parameter table (`parameter.html`) | https://people.smp.uq.edu.au/HolgerBaumgardt/globular/parameter.html | **E-pair** for R1 | V mag, r_h,l and R☉ per cluster. Listed `M/LV`, `Mass` and `σ0` come from N-body fits, so §2 rules them out as inputs: dynamical M/L is not a baryonic input, and model σ0 is not the observed side. |
| R3 | Baumgardt & Hilker 2018, VizieR J/MNRAS/478/1520 | https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/478/1520 ; https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/MNRAS/478/1520 ; https://ar5iv.labs.arxiv.org/html/1804.08359 | **E** (earlier version of R1) | §1.5 re-reduction, earlier release of the same reduction. §4 precedence goes to R1. The ReadMe was not readable, so it is unverified whether `tabled.dat` holds the profiles. |
| R4 | Baumgardt, Hilker, Sollima & Bellini 2019 (Gaia DR2 PM profiles), arXiv:1811.01507 | https://arxiv.org/pdf/1811.01507 | X | Duplicate of R1. Profiles are released through the R1 website (superseded by v4). |
| R5 | Hilker et al. 2019, IAU Symp. 351 (database description), arXiv:1908.02778 | https://ar5iv.arxiv.org/html/1908.02778 | X | Duplicate of R1 (describes the database). |
| R6 | Baumgardt 2017, arXiv:1609.08794 | search result only | NS | Not read. Probably an earlier RV compilation absorbed into R1 (unverified). |
| R7 | Vasiliev & Baumgardt 2021, VizieR J/MNRAS/505/5978 | https://cdsarc.cds.unistra.fr/VizieR/ftp/0/catj/J/MN/505/5978/ReadMe | X | §1.1 / §2: only `tablea1.dat` (mean parallaxes and PMs), no internal dispersions. The profiles are in R8. |
| R8 | Vasiliev & Baumgardt 2021, Zenodo 10.5281/zenodo.4891252 (v2) | https://zenodo.org/records/4891252 | **E** (PM only, §5 Q2) | §2 observed side: "radial profiles of proper motion dispersion". Baryonic side by pairing (R2). |
| R9 | Same, Zenodo v1 | https://zenodo.org/record/4549398 | X | Duplicate (earlier version) of R8. No licence shown. |
| R10 | Dickson et al. 2022, Zenodo 10.5281/zenodo.7344596 | https://zenodo.org/records/7344596 ; https://portal.mardi4nfdi.de/wiki/Dataset:6695506 | **E** (PM only) | §2 observed side. §1.5: a re-extraction of Gaia EDR3 using R8's membership, so it is not independent of R8. |
| R11 | Dickson et al. 2023, arXiv:2303.01637 | https://arxiv.org/pdf/2303.01637 | X | Duplicate: compiles R1, R14, R15, R16, R19 and others. Its new data are R10. |
| R12 | GCfit-results (GitHub, nmdickson) | https://gh.r-mj.com/nmdickson/GCfit-results | X | Duplicate of R10 plus model outputs. §1.4 no licence found. |
| R13 | pjs902/GC-modeling-with-pulsar-timing v1.0.0, Zenodo 13352366 | https://zenodo.org/records/13352366 | X | Duplicate: repackaged GCfit inputs for 6 fits. §1.4 no licence shown. |
| R14 | Watkins et al. 2015 (HSTPROMO II), VizieR J/ApJ/803/29 | https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/ApJ/803/29 ; https://ar5iv.arxiv.org/html/1502.00005 | **E** (PM only) | §2 observed side: binned PM dispersion profiles, inner regions. Overlaps R15 and R1 (§5 Q6). |
| R15 | Libralato et al. 2022 (HST UV Legacy XXIII), MAST HLSP "HACKS", 10.17909/jpfd-2m08 | https://archive.stsci.edu/hlsp/hacks ; https://arxiv.org/pdf/2206.09924 | **E** (PM only) | §2 observed side: `_vdisp.txt` per cluster. Baryonic side by pairing. |
| R16 | Kamann et al. 2018, MUSE, arXiv:1710.07257 | https://ar5iv.arxiv.org/html/1710.07257 | **E** | §2 observed side: LOS radial profiles from ≥100 stars per bin, released at musegc.uni-goettingen.de (not reached; unverified). Overlaps R1. |
| R17 | Ferraro et al. 2018, MIKiS I, arXiv:1804.08618 | https://ar5iv.arxiv.org/html/1804.08618 | **E** (tier 2) | §2 observed side: Table 6 projected dispersion profiles. RV catalogues are said to be on cosmic-lab.eu (not reached). |
| R18 | Häberle et al. 2025, oMEGACat VI (ω Cen), Zenodo 10.5281/zenodo.14978551 | https://zenodo.org/records/14978551 ; https://arxiv.org/pdf/2503.04903 | **E** (one system) | §2 observed side: LOS and PM dispersion profiles. Licence not shown on the page (§5 Q8). |
| R19 | Dalgleish et al. 2020, WAGGS III, arXiv:2001.01810 | https://ar5iv.labs.arxiv.org/html/2001.01810 | **P** | Central 1D dispersions for 59 GCs from individual stellar RVs (Table 2). Whether the tabulated value is direct or taken from the N-body fit is unverified (§5 Q4). |
| R20 | Kimmig et al. 2015, AJ 149, 53; VizieR J/AJ/149/53 | https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/AJ/149/53 ; https://arxiv.org/pdf/1411.1763 | **E** (tier 2 central σ; tier 1 RVs) | Table 4: central dispersions for 25 GCs. Profiles are in figures only. Overlaps R1. |
| R21 | Kamann et al. 2014, VizieR "Radial velocities in M3, M13, and M92" | https://ui.adsabs.harvard.edu/abs/2014yCat..35660058K/abstract | X | §2 A3 / D-025: individual velocities only. Computing σ would be new analysis. |
| R22 | Scarpa, Marconi & Gilmozzi 2003 (ω Cen outer RVs), astro-ph/0305388 | https://web3.arxiv.org/pdf/astro-ph/0305388 | **E** (tier 2, profile only) | Table 1: four binned outer dispersions. Baryonic side by pairing. D-025 profile-only means recorded, not plotted. |
| R23 | Scarpa, Marconi & Gilmozzi 2006 (conference), astro-ph/0601581 | https://ar5iv.arxiv.org/html/astro-ph/0601581 | X | §1a: profiles in figures only, and tier 1 or 2 data exist for the same clusters (R1). No data release. |
| R24 | Scarpa et al. 2007 (NGC 7099), astro-ph/0611504, and VizieR RVs "(Scarpa+, 2007)" | search results only | NS | Not read (§5 Q9). |
| R25 | Scarpa et al. 2011, A&A 525, A148 (NGC 1851, NGC 1904) | https://www.aanda.org/articles/aa/full_html/2011/01/aa14462-10/aa14462-10.html | **E** (tier 2, profile) | Tables 4 and 5: binned profiles. Online Tables 2 and 3: individual RVs. Baryonic side by pairing. |
| R26 | Lane et al. 2010 (AAOmega Paper III), arXiv:1004.4696 | https://ar5iv.labs.arxiv.org/html/1004.4696 | X | §1a: binned profiles in Fig. 4 only, and tier 1 or 2 data exist for the same clusters (R1). No data release. |
| R27 | Lane et al. 2011, A&A 530, A31 | https://www.aanda.org/10.1051/0004-6361/201116660 | X | §2: the CDS tables hold field-star parameters. Cluster members are excluded by design. |
| R28 | Jordi et al. 2009, Pal 14, arXiv:0903.4448 | https://ar5iv.labs.arxiv.org/html/0903.4448 | **P** | Global LOS σ from 16 to 17 members (Table 1 RVs). The baryonic side is a star-count mass function, not luminosity × SPS M/L (§5 Q5). Distance not read. |
| R29 | Frank et al. 2012, Pal 4, arXiv:1205.2693 | https://ar5iv.arxiv.org/html/1205.2693 | **P** | Global σ plus a running-bin profile (figure). Table 1 RVs. Baryonic side: King-fit L_V plus a counted mass function (§5 Q5). Distance 102.8 ± 2.4 kpc. |
| R30 | Baumgardt et al. 2009, NGC 2419, arXiv:0904.3329 | https://arxiv.org/pdf/0904.3329 | **E** | Global LOS σ from 39 to 40 members (Table 1 RVs). Light profile from Bellazzini (2007). Names SPS models (Maraston 2005; Bruzual & Charlot 2003). (m−M)₀ = 19.60 (Ripepi et al. 2007). |
| R31 | Ibata et al. 2011, NGC 2419 (Keck/DEIMOS), arXiv:1106.4909 | https://web3.arxiv.org/abs/1106.4909 (abstract only) | NS | Full text not reachable. 178 stars per R34 (unverified at the primary source). |
| R32 | "A Monte Carlo analysis of the velocity dispersion of … Palomar 14", arXiv:1111.1689 | search result only | NS | Title suggests a reanalysis of the R28 data (unverified). |
| R33 | Hernandez, Jiménez & Allen 2012, arXiv:1206.5024 | https://arxiv.org/pdf/1206.5024 | X | Duplicate: reanalysis of published data, with no new observations. |
| R34 | Frank 2014, "Observational dynamics of low-mass stellar systems" (thesis lecture), arXiv:1405.7823 | https://arxiv.org/pdf/1405.7823 | — | Review. Used for §3.4 citation leads. |
| R35 | Strader, Caldwell & Seth 2011, M31 GCs, arXiv:1104.4649 | https://ar5iv.labs.arxiv.org/html/1104.4649 | **E** (tier 2) | 200 GCs with integrated-light σ in a 0.75″ fibre aperture. V and K luminosities, King parameters (163). FSPS SPS named. Distance 780 kpc. |
| R36 | Taylor et al. 2010, NGC 5128 GCs, arXiv:1002.1973 | https://arxiv.org/pdf/1002.1973 | **E** (tier 2) | 23 GCs (UVES, pPXF), aperture-corrected with King-model N-body. BC03 with Chabrier IMF named. 3.8 ± 0.1 Mpc. Re-analysed in R37 (§1.5). |
| R37 | Taylor et al. 2015, NGC 5128 GCs, arXiv:1503.04198 | https://arxiv.org/pdf/1503.04198.pdf | **E** (tier 2; CDS deposit unverified) | 115 GCs (FLAMES/GIRAFFE, pPXF), aperture-corrected. No SPS used, so an SPS M/L must be registered. 3.8 ± 0.1 Mpc. |
| R38 | Dumont et al. 2022, ApJ 929, 147; VizieR J/ApJ/929/147 | https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/ApJ/929/147 | **E** | 57 NGC 5128 GCs with σ (48 new). Overlaps R36 and R37 (§5 Q6). Methods not read. |
| R39 | Fahrion et al. 2025, M104 GCs, arXiv:2509.14948 | https://arxiv.org/pdf/2509.14948 | **P** | 85 GCs (FLAMES, pPXF), aperture-corrected. Sizes are assumed (2.44 pc) where not measured. No data statement. The paper is a distance measurement, so the host distance must come from elsewhere (§5 Q7). |
| R40 | Beasley, Fahrion & Gvozdenko 2024, arXiv:2312.01420 | https://arxiv.org/pdf/2312.01420 | X | Compilation (duplicate). §1.2: "The data underlying this article will be shared on reasonable request." Used for §3.4 leads. |
| R41 | Song et al. 2021, Magellanic Cloud clusters, arXiv:2104.06882 | https://arxiv.org/pdf/2104.06882 | **P** | 26 clusters, of which 3 are old (NGC 1466, NGC 1841, NGC 2257). Central σ from individual stars via King/LIMEPY fits. Distance moduli per cluster. Kind boundary for the young ones (§5 Q10). |
| R42 | Hilker et al. 2007, Fornax-cluster UCDs, astro-ph/0612484 | https://ar5iv.labs.arxiv.org/html/astro-ph/0612484 | X | Kind: ultra-compact dwarfs, not globular clusters (§5 Q10). |
| R43 | Dalessandro et al. 2024, 3D kinematics of multiple populations, arXiv:2409.03827 | https://arxiv.org/pdf/2409.03827 | X | §1.2 / §1a: no data statement and no released numbers found. Tier 1 or 2 data exist for these clusters. |
| R44 | Flynn 2026, Milky Way Globular Cluster Corpus v1.3.1, Zenodo 19907766 | https://zenodo.org/records/19907766 | X | Duplicate (compilation of Harris, VB21, Baumgardt 2023 and Schiavon 2024). Its σ₀ is a scalar copy of model values. |
| R45 | arXiv:2605.03099 (paper describing R44) | search result | X | Duplicate of R44. |
| R46 | McLaughlin & van der Marel 2005, ApJS 161, 304; VizieR J/ApJS/161/304 | https://ar5iv.labs.arxiv.org/html/astro-ph/0605132 ; https://vizier.cds.unistra.fr/viz-bin/cite/J/ApJS/161/304 | **E-pair** | V-band surface-brightness profiles, structural fits, and **population-synthesis Υ_V** (Bruzual & Charlot 2003, Chabrier IMF). Its literature-compiled σ are duplicates of earlier sources (not named in the text read). |
| R47 | Baumgardt, Sollima & Hilker 2020, PASA, arXiv:2009.09611 | https://web3.arxiv.org/pdf/2009.09611 | **E-pair** | Total V for 153 GCs from summed member stars, with a modelled faint-star and coverage correction from N-body fits (labelled). Table 3: r10, r50 and surface brightness there. Full profiles: release unverified. |
| R48 | de Boer et al. 2019, Gaia DR2 number-density profiles, arXiv:1901.08072 | https://ar5iv.labs.arxiv.org/html/1901.08072 | **P** (pairing) | Number-density profiles for 81 GCs, not luminosity (§5 Q5). Members at github.com/tdboer/GC_profiles. Profile release unverified. |
| R49 | Harris 1996 (2010 edition), arXiv:1012.3224 | https://arxiv.org/pdf/1012.3224 | **E-pair** | Compiled M_V, HB-based distances and structural parameters. Its central σ is compiled (duplicate). Terms not stated. Hosted at physwww.mcmaster.ca (not read). |
| R50 | Baumgardt et al. 2023, MNRAS (stad631), arXiv:2303.01636 | https://arxiv.org/abs/2303.01636v1 | **P** (pairing) | HST mass functions for 120 clusters: a counted stellar-mass route, not luminosity × SPS (§5 Q5). |
| R51 | Caldwell et al. 2016, M31 GC RVs, VizieR (2016yCat..18240042C) | search-result title only | X (from title; unverified) | §1.1 / §2: systemic cluster velocities for global kinematics, not internal dispersions. |
| R52 | Watkins et al. 2015b, HSTPROMO III, arXiv:1509.00513 | search result only | NS | Title: dynamical distances and M/L, which are derived quantities. |
| R53 | Larsen et al. 2012, Fornax dSph GCs (abundances), arXiv:1209.1092 | search result only | NS | Whether it measures internal σ is unverified. R40 cites "Larsen et al. (2012)" for 3 Fornax GC dispersions. |
| R54 | Chantereau et al. 2020, "The loss of the intra-cluster medium in globular clusters", arXiv:2002.02401 | https://ar5iv.labs.arxiv.org/html/2002.02401 | — | Source for the §1.7 gas statement (below). Journal not shown on the page read (unverified). |

### §1.7 gas: statements read at source

From Chantereau et al., arXiv:2002.02401 (https://ar5iv.labs.arxiv.org/html/2002.02401):
- "However, the observed gas content in GCs is a couple of orders of magnitude below these expectations." (abstract)
- "there has been only a single certain detection of neutral intra-cluster medium (ICM) in GCs: M15 (NGC 7078)", which displays 0.3 M⊙ of HI (citing Evans et al. 2003; van Loon et al. 2006).
- For 47 Tuc, Abbate et al. (2018) "calculate a total mass of gas in the inner 1 pc of 47 Tuc to be 0.023" M⊙.
- Other HI, CO and Hα searches "all lead to only observational upper limits often lower than 1 M⊙ and as low as 10⁻⁵ M⊙".

None of the A3 dataset pages or methods sections read in this run states that gas is negligible. They simply do not model gas. §1.7 therefore needs the reading in §5 Q3.

---

## 3. Eligible datasets

Shared facts:
- "D-025" means each dataset depends on the ruled estimator. "SPS M/L" means it needs the stellar-population M/L ruling (SELECTION_PROTOCOL §5, still open).
- **Plottable under D-025 as ruled** means the source gives a global or luminosity-weighted LOS σ. Otherwise the system is recorded but not plotted.
- **Gas:** absent for all rows. This rests on §5 Q3, because no dataset source states it.
- **Licences:** CDS terms read at https://cds.unistra.fr/legals/: "Datasets containing only Public Information are distributed under an Open Licence or ODbL", or CC-BY; "Datasets subject to a specific licence from the data Contributor are distributed in accordance with the licence rights"; "The Data Sets must be cited … including - if available - the DOI". No per-record licence was shown on any VizieR page read.

| ID (record) | Citation | Tier | Observed side | Baryonic side | Distance per system | Licence / terms as read | N systems | Independence / overlaps | Rulings depended on; plottable under D-025? |
|---|---|---|---|---|---|---|---|---|---|
| A3-1 (R1+R2) | Baumgardt, Sollima, Hilker, Bellini, Vasiliev, Hénault-Brunet, Dickson, Galactic GC Database v4 (Mar 2023) | 1 (web tables, not a deposited file) | Binned σ profiles: `<r>` [arcsec], NStar, σ, Δσ_up, Δσ_low [km/s], Type. RV and PM shown separately. PMs converted to km/s with Baumgardt & Vasiliev (2021) distances. RV reduction: ML fit, iterative non-member removal, χ² binary rejection (per BH18) | V mag (Baumgardt+ 2020, R47) and r_h,l. Listed M/L_V and mass are N-body (dynamical), so they are **not usable**. Needs SPS M/L. No light profile on the parameter page | R☉ [kpc] per cluster, "mostly from Baumgardt & Vasiliev (2021)" | No licence. "If you use these profiles for your research, please give reference to the papers." © authors → link and hash, do not redistribute (D-004) | 156 profiles (veldis). 165 in the parameter table | **Compilation.** It contains R14, R15, R16, R8 and 11 other cited sources (Feldmeier 2013; Lützgendorf 2013, 2015; Dalessandro 2021; Carvajal 2022; Gran 2022; Cohen 2021; Häberle 2021; Taheri 2022; del Pino 2022) plus own RVs. R3 is its earlier version | D-025, SPS M/L, pairing to a light profile or r½. **Profiles only, so recorded but not plotted** unless a global σ is ruled derivable (§5 Q1) |
| A3-2 (R3) | Baumgardt & Hilker 2018, MNRAS 478, 1520; VizieR J/MNRAS/478/1520, doi:10.26093/cds/vizier.74781520 | 1 | As A3-1, an earlier version (~42 000 RVs of ~35 000 stars, 109 clusters) | As A3-1 (pairing) | Literature; some kinematic (paper) | CDS terms; per-record licence not stated | 112 | Earlier release of A3-1. §4 precedence to A3-1 | As A3-1 |
| A3-3 (R8) | Vasiliev & Baumgardt 2021, MNRAS 505, 5978; Zenodo 10.5281/zenodo.4891252 v2 | 1 (`clusters.zip`, md5 3a07093b…) | PM dispersion radial profiles from Gaia EDR3 (units in the file not read) | Pairing (A3-1/R2, R46, R47) | Pairing (Baumgardt & Vasiliev 2021) | **CC BY 4.0** | Up to 170 (count with profiles unverified) | Gaia EDR3. Included in A3-1 as "VB21". A3-4 re-extracts it | D-025 uses σ_los, so **PM-only data are not plotted** (§5 Q2) |
| A3-4 (R10) | Dickson et al. 2022, Zenodo 10.5281/zenodo.7344596 | 1 (`GEDR3_PM_profiles.dat`, md5 be9d8b3e…) | Radial and tangential PM dispersion profiles, Gaia EDR3 | Pairing | Pairing | **CC BY 4.0** | 37 | Re-reduction of A3-3's data (same membership) | As A3-3 |
| A3-5 (R14) | Watkins et al. 2015, ApJ 803, 29; VizieR J/ApJ/803/29, doi:10.26093/cds/vizier.18030029 | 1 | Binned HST PM dispersion and anisotropy profiles, inner regions | Pairing | Table 1 heliocentric distances from Harris (1996) | CDS terms; not stated per record | 22 | HST; in A3-1. Probably superseded by A3-6's re-reduction (unverified) | As A3-3 |
| A3-6 (R15) | Libralato et al. 2022, ApJ 934, 150; MAST HLSP HACKS, 10.17909/jpfd-2m08 | 1 (`_vdisp.txt` per cluster plus a combined file) | HST PM dispersion profiles, cluster centres | Pairing | Kinematic distances for 39 (derived assuming isotropy, so model-dependent); otherwise pairing | **CC BY 4.0** ("These HLSP data products are licensed for use under CC BY 4.0.") | 56 GCs (+1 open cluster) | In A3-1 as "LI22". Overlaps A3-5 | As A3-3 |
| A3-7 (R16) | Kamann et al. 2018, MNRAS 473, 5591 (MUSE) | 1 (musegc.uni-goettingen.de, unverified) / 2 (appendix) | LOS σ radial profiles (≥100 stars per bin, ML/MCMC), and a central value = weighted mean inside r_c | Pairing. r_c and r_h from Harris (1996) | Dynamical distances for 14; others not read | Unverified | 22 (of 25 observed) | In A3-1 as "K18" for some clusters only | D-025, SPS M/L. Central σ is not global, so **recorded, not plotted** (§5 Q4) |
| A3-8 (R17) | Ferraro et al. 2018, ApJ 860, 50 (MIKiS I) | 2 (Table 6). RV catalogues on cosmic-lab.eu (unverified) | Projected LOS σ profiles (FLAMES + KMOS, ~6 275 spectra) | Pairing | Not tabulated in the text read; pairing | Journal (AAS); site terms unverified | 11 | Not listed among A3-1's cited sources. A3-1's own ESO-archive RVs may share FLAMES spectra (unverified) | D-025, SPS M/L; profile only, so recorded, not plotted |
| A3-9 (R18) | Häberle et al. 2025, oMEGACat VI; Zenodo 10.5281/zenodo.14978551 | 1 | MUSE LOS σ, rotation and PA profiles; HST PM profiles (also in 9 mass bins) | Pairing | Kinematic distance 5 494 ± 61 pc (model-dependent) or pairing | **Not shown on the page** ("Please cite the paper") | 1 (ω Cen) | ω Cen appears in A3-1 (sources there include Häberle 2021) | D-025, SPS M/L; profile only |
| A3-10 (R20) | Kimmig et al. 2015, AJ 149, 53; VizieR J/AJ/149/53 | 1 (RVs) / 2 (central σ, Table 4) | Central σ from King-model fits to Hectochelle and archival RVs (1 951 new stars) | L from Harris (2010). King r_c and c from Harris | Harris HB distances ("a variety of sources") | CDS terms | 25 | Overlaps A3-1 clusters. Shared archival RVs (unverified) | D-025, SPS M/L. Central from a King fit is not global (§5 Q4) |
| A3-11 (R22, R25) | Scarpa, Marconi & Gilmozzi 2003 (ω Cen outer); Scarpa et al. 2011, A&A 525, A148 | 2 (Table 1 / Tables 4–5). 2011 individual RVs in online tables | Binned outer LOS σ profiles (UVES; FLAMES/GIRAFFE) | Pairing (authors' M/L = 1 is an assumption, not used) | Harris (1996) | Journal (A&A) | 3 (ω Cen, NGC 1851, NGC 1904) | Same clusters are in A3-1. Spectra possibly re-reduced in A3-1's ESO-archive RVs (unverified) | Profiles only, so recorded, not plotted |
| A3-12 (R30) | Baumgardt et al. 2009, MNRAS 396, 2051 (per R34), NGC 2419 | 2 (Table 1 RVs) | Global LOS σ (39 stars) plus a 3-bin profile (figure) | Light profile from Bellazzini (2007), cored Sérsic fit. SPS named: Maraston (2005, Kroupa), BC03 (Chabrier) | (m−M)₀ = 19.60 ± 0.05 (Ripepi et al. 2007) | Journal | 1 | NGC 2419 in A3-1. R31 is a larger independent Keck/DEIMOS sample (not screened) | D-025, SPS M/L. **Global σ given, so plottable** |
| A3-13 (R28) **pending** | Jordi et al. 2009, AJ 137, 4586 (per R34), Pal 14 | 2 (Table 1) | Global LOS σ (16 members, UVES + HIRES) | HST/WFPC2 counted mass function (≥0.53 M⊙) | Not read (unverified) | Journal | 1 | Pal 14 is probably in A3-1 (unverified) | D-025. Baryonic route is §5 Q5. Global σ given |
| A3-14 (R29) **pending** | Frank et al. 2012, MNRAS 423, 2917 (per R34), Pal 4 | 2 (Table 1) | Global σ (23 members) plus a running-bin profile (figure) | King-fit L_V (Keck/LRIS) and an HST counted mass function | 102.8 ± 2.4 kpc | Journal | 1 | As A3-13 | As A3-13 |
| A3-15 (R35) | Strader, Caldwell & Seth 2011, AJ (vol./page unverified), M31 | 2 (machine-readable status unverified) | Integrated-light σ (Hectochelle) in a 0.75″ (2.84 pc) fibre aperture, seeing-corrected | V and K luminosities (Barmby; Caldwell; Peacock; Galleti). King parameters (163). SPS named: FSPS (Conroy & Gunn 2010), Kroupa IMF | 780 kpc for all (host) | Journal | 200 | Independent. A3-16 to A3-18 are a different host | D-025 needs global σ and r½; aperture σ is neither (§5 Q4). SPS M/L |
| A3-16 (R36) | Taylor et al. 2010, ApJ, NGC 5128 | 2 | UVES σ via pPXF, aperture-corrected to central with King N-body (model-dependent) | V (Peng 2004; Holland 1999), HST r_h. SPS named: BC03 (Chabrier; Salpeter tested) | 3.8 ± 0.1 Mpc (host) | Journal | 23 (21 with masses) | Re-analysed within A3-17 | As A3-15 |
| A3-17 (R37) | Taylor et al. 2015, ApJ, NGC 5128 | 2 (CDS deposit implied, unverified) | FLAMES σ via pPXF, aperture-corrected to core and r_h | V (Woodley 2007) or r′/R. r_h from HST/IMACS. No SPS, so an SPS M/L must be registered | 3.8 ± 0.1 Mpc | Journal | 115 | Overlaps A3-16 and A3-18 | As A3-15 |
| A3-18 (R38) | Dumont et al. 2022, ApJ 929, 147; VizieR J/ApJ/929/147 | 1 | σ for 57 GCs (methods not read) | Not read | Host distance (not read) | CDS terms | 57 | Overlaps A3-17 (9 not new) | As A3-15 |
| A3-19 (R39) **pending** | Fahrion et al. 2025, OJAp (template; unverified), M104 | 2 (data statement absent) | FLAMES σ via pPXF, aperture-corrected | V (HST and ground). r_h (HST) for 29; 2.44 pc assumed otherwise. No SPS | The paper *measures* the host distance from these data. The Atlas would need an independent distance (§5 Q7) | Journal | 85 | Independent | As A3-15 |
| A3-20 (R41) **pending** | Song et al. 2021, MNRAS, Magellanic Clouds | 2 (Table 5 supplementary) | Central σ from individual stars via King/LIMEPY fits (model-dependent) | V aperture magnitudes plus King parameters from the literature. SPS not named in the text read | Distance moduli per cluster | Journal | 3 old of 26 | Independent | D-025; kind boundary (§5 Q10) |

Baryonic-side pairing sources (they supply no observed side):

| ID | Citation | Tier | Content | Distance | Terms | N |
|---|---|---|---|---|---|---|
| B-1 (R46) | McLaughlin & van der Marel 2005, ApJS 161, 304; VizieR J/ApJS/161/304 | 1 | V-band SB profiles (MW from Trager+ 1995), King/Wilson/power-law fits, luminosities, **population-synthesis Υ_V** (BC03, Chabrier) | Galactocentric listed; heliocentric unverified | CDS terms | 85 MW fitted (+63 MW with SPS only), 63 MC, 5 Fornax |
| B-2 (R47) | Baumgardt, Sollima & Hilker 2020, PASA | 2 (Table 3) | Total V; r10, r50 and surface brightness there | Baumgardt et al. (2019) | Journal | 153 |
| B-3 (R49) | Harris 1996 (2010 edition) | 1 (web file, not read) | M_V, distances, structural parameters | HB-based | Not stated | 157 |
| B-4 (R48), pending | de Boer et al. 2019 | ? | Number-density profiles | — | Not read | 81 |
| B-5 (R50), pending | Baumgardt et al. 2023 | ? | HST stellar mass functions | — | Not read | 120 |

---

## 4. PRISMA counts (2026-10-29, pre-freeze scoping run)

| Stage | Count |
|---|---|
| Records identified (all venues; deduplicated by record) | 54 |
| Not datasets (review, gas-statement source) | 2 (R34, R54) |
| Identified, not screened (not read at source) | 6 (R6, R24, R31, R32, R52, R53) |
| Screened | 46 |
| Excluded | 18 |
| — duplicate, earlier version, compilation or reanalysis (§1.5) | 10 (R4, R5, R9, R11, R12*, R13*, R33, R40, R44, R45). *Also §1.4: no licence |
| — §1.1/§2: no internal observed side (mean motions only) | 2 (R7, R51) |
| — §2 A3: individual velocities only, or non-members | 2 (R21, R27) |
| — §1a: figures only where tier 1 or 2 data exist for the same systems | 3 (R23, R26, R43) |
| — kind: not globular clusters | 1 (R42) |
| Eligible: observed side (with pairing) | 22 records → 20 datasets (A3-1 to A3-20). A3-1 merges R1 and R2; A3-11 merges R22 and R25. Of these, 5 are pending (A3-13, A3-14, A3-19, A3-20, and R19 WAGGS, which is held outside the table until §5 Q4 is resolved) |
| Eligible: baryonic pairing only | 4 (B-1, B-2, B-3; R2 is counted inside A3-1) + 2 pending (B-4, B-5) |
| Plottable as D-025 stands (global LOS σ given) | 3 single systems: A3-12 (NGC 2419); A3-13 and A3-14 if §5 Q5 allows them |
| Included | Not decided: inclusion follows the freeze and JvH's rulings |

---

## 5. Open questions (for JvH; recommendations where I have one)

1. **D-025 vs the main dataset.** D-025 as ruled plots only a source's global or luminosity-weighted LOS σ. The largest and deepest dataset (A3-1, 156 profiles) gives profiles only. Its σ0 is a model output and is excluded by §2. As ruled, A3-1 is recorded but not plotted, and globular clusters would reach v1.0 with roughly 1 to 3 plotted systems. Options:
   - (a) Accept this.
   - (b) Rule an exact, registered aggregation of a source's binned profile into a luminosity-weighted σ within r½. This is arithmetic on released numbers, but it is new analysis under D-025's own wording.
   - (c) Take the global σ from a source that publishes one (none was found for the Milky Way sample in this run).
   - **Recommendation:** (b), ruled blind under D-031, with the aggregation formula and light profile (B-1) registered. It must be decided before any profile is opened.
2. **PM-only datasets** (A3-3 to A3-6). D-025 uses σ_los. Rule whether PM dispersions are plotted under the estimator (σ_los ≈ σ_PM,1D assumes isotropy, which is exactly what Wolf et al. avoid) or only recorded. **Recommendation:** record only for v1.0.
3. **§1.7 gas.** No A3 dataset states that gas is negligible. Chantereau et al. (2020) does, with measurements and limits (quoted above). Rule whether a quoted review statement for the *kind* satisfies §1.7 / D-035(d). **Recommendation:** yes, with the quotation stored once per kind and the measured limits for M15 and 47 Tuc cited to their primary papers (Evans 2003; van Loon 2006; Freire 2001; Abbate 2018), which must be read at source first.
4. **Central and aperture dispersions.** Central σ (A3-7, A3-10, A3-20, WAGGS R19) and aperture-corrected integrated-light σ (A3-15 to A3-19) are neither global nor luminosity-weighted. Aperture corrections use King-model N-body runs, so they are model-dependent. Rule whether they enter D-025 (labelled `model_dependence`) or are recorded only. This decides whether the extragalactic samples (about 480 GCs across M31, NGC 5128 and M104) can be plotted.
5. **Counted stellar mass as the baryonic side.** Pal 14 and Pal 4 (and B-5) give stellar mass from HST star counts plus remnant modelling, not luminosity × SPS M/L. §2 names only the luminosity route. Rule whether counted mass is an allowed "measured" route (D-034), with remnants recorded as modelled. Number-density profiles (B-4) raise the same question.
6. **Independence and precedence.** A3-1 is a compilation that contains A3-3, A3-5, A3-6 and A3-7 and others. §4 precedence ("deepest observables released") favours the per-team releases for the systems they cover, and A3-1 for the rest. Rule how a compilation's components are de-duplicated per system. NGC 5128 (A3-16 to A3-18) needs the same treatment.
7. **M104 distance.** A3-19 derives the M104 distance from these dispersions. Using that distance would be circular for g_obs and g_bar. The Atlas needs an independent published distance for the host, read at source.
8. **Licences.** Only A3-3, A3-4 and A3-6 carry an explicit open licence (CC BY 4.0). A3-1 has none, so it is linked and hashed, not redistributed. VizieR records show no per-record licence. The oMEGACat Zenodo page shows none. Tier 2 transcriptions from journal tables need the D-004 reading.
9. **Unscreened records** (R6, R24, R31, R32, R52, R53) and **unreached pages**: musegc.uni-goettingen.de, cosmic-lab.eu, physwww.mcmaster.ca/~harris/Databases.html, the R3 ReadMe, the J/ApJS/161/304 ReadMe, and ADS. These are to be read in the formal post-freeze run.
10. **Kind boundary.** Young massive Magellanic Cloud clusters (R41) and UCDs (R42) are not globular clusters as defined here. Rule whether old Magellanic Cloud and dwarf-galaxy GCs (LMC, SMC, Fornax dSph, WLM, NGC 147, M33, NGC 6822, which are leads from R40 and still need to be read) belong in A3. UCDs go to A7 or are excluded.
11. **Citation leads not yet followed (§3.4):**
    - Pryor & Meylan 1993
    - Trager, King & Djorgovski 1995
    - Noyola & Gebhardt 2006
    - Drukier et al. 1998 (M15)
    - Côté et al. 2002 (outer-halo programme)
    - Lützgendorf 2013 and 2015; Feldmeier 2013
    - Sakari et al. 2015 and Larsen et al. 2022 (M31)
    - Larsen et al. 2002, 2014 and 2018
    - Dubath et al. 1997
    - Ibata et al. 2011a (ApJ 743, 43)
    - Scarpa & Falomo 2010
    - Sollima, Baumgardt & Hilker 2019
12. **Process.** This run predates the protocol freeze, and four of the §3 venues were unreachable. Before the cell is closed, it must be re-run after the freeze with direct ADS, VizieR, Zenodo and GitHub access, or registered as a §9 deviation.
