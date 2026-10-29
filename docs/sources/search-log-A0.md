# Search log: cell A0·orbits (Solar System × planetary and spacecraft orbits)

> Run on 2026-10-29 after the protocol freeze (see `docs/plans/DEVIATIONS.md` #1 and #2). The run calls itself "pre-freeze" or "exploratory" below because the protocol's status line had not been updated; the freeze record is authoritative. ADS and VizieR steps added in §6 (deviation #2). AI-run (Claude); metadata only.

- **Date run:** 2026-10-29
- **Run by:** Claude (AI), for JvH. Literature and metadata only. No candidate was plotted against any g_obs–g_bar data.
- **Protocol:** `docs/plans/SELECTION_PROTOCOL.md` (draft, **not yet frozen**). §2 row A0·orbits: observed side = "A published bound on an anomalous acceleration from ephemeris fits, with method"; baryonic side = "Known masses as used in the fit"; form = "Limit". Context: D-013 (Solar System points deferred, needing their own sourced package); D-028 item 6 (Solar System shown as a limit on anomalous acceleration, not as a point).
- **Status of this run:** **pre-freeze scoping run.** §3 says the logged search runs after the protocol is frozen on `main`. This run should be logged as a pilot and repeated, or registered in §9 as a deviation, once the freeze happens.
- **Rule applied:** every statement below was read at source in this session, at the URL given. Anything not read is marked **unverified**. Unit conversions (cm s⁻² to m s⁻²) are my own arithmetic and are labelled as such.

## 1. Queries

### 1a. Where queries were run

| Protocol step | Planned venue | Outcome |
|---|---|---|
| §3.1 ADS | ui.adsabs.harvard.edu, via WebFetch | **Not reachable.** The URL is not on the session allowlist. The query was attempted but nothing was fetched. Every ADS-style query was run through WebSearch instead. |
| §3.2 VizieR | — | **Not run.** VizieR was not reached in this session. This is a gap for the formal run, though bounds of this kind are not normally VizieR catalogues. |
| §3.3 Zenodo/GitHub | WebSearch | One query was run (Q19). No relevant dataset was found. |
| §3.4 Citations | Reference lists read inside screened papers | Partial. Leads are listed in §5. |

### 1b. Query strings, verbatim

ADS query attempted (not executed): `abs:"anomalous acceleration" abs:"ephemeris"`, sorted by date descending.

WebSearch queries, standard mode, US index, all on 2026-10-29:

| # | Query string | Purpose |
|---|---|---|
| Q1 | `planetary ephemeris constraint anomalous acceleration INPOP` | INPOP |
| Q2 | `EPM ephemeris Pitjeva constraint additional radial acceleration Sun planets` | EPM |
| Q3 | `Pitjeva Pitjev constraints dark matter solar system planetary ephemerides EPM2011 density` | EPM, extra mass |
| Q4 | `Standish planetary ephemerides Pioneer anomaly constant acceleration Uranus Neptune constraint` | JPL DE, outer planets, constant acceleration |
| Q5 | `Cassini ranging Saturn constraint MOND external field effect quadrupole Hees` | Saturn/Cassini (model-specific) |
| Q6 | `INPOP19a OR INPOP21a constraints fifth force anomalous acceleration planetary ephemeris arXiv` | Recent INPOP |
| Q7 | `Iorio constraints constant radial anomalous acceleration supplementary perihelion precessions INPOP planets m s^-2` | Constant acceleration from perihelia |
| Q8 | `Turyshev 2012 Pioneer anomaly thermal origin no anomalous acceleration remaining upper limit` | Spacecraft |
| Q9 | `Folkner planetary ephemerides Cassini range Saturn constraint anomalous acceleration Pioneer DE421` | JPL DE, Saturn |
| Q10 | `Wallin Dixon Page 2007 testing gravity outer solar system trans-Neptunian objects Pioneer anomaly constant acceleration` | 20–100 au |
| Q11 | `planetary ephemeris bound "anomalous acceleration" power-law distance dependent Saturn Mars 2020..2026 arXiv` | Power-law and recent work |
| Q12 | `INPOP10a Fienga 2011 Celestial Mechanics supplementary advances of perihelia Pioneer constraint` | Perihelion anomalies |
| Q13 | `Sereno Jetzer 2006 "Dark matter vs. modifications of the gravitational inverse-square law" MNRAS 371` | Metadata check |
| Q14 | `Iorio "Solar system constraints on a Rindler-type extra-acceleration" journal` | Metadata check |
| Q15 | `Hees 2014 "Tests of gravitation at Solar System scales beyond the PPN formalism" Physical Review D 89 102002` | Metadata check |
| Q16 | `Hees Folkner Jacobson Park "Constraints on MOND theory from radio tracking data of the Cassini spacecraft"` | Metadata check |
| Q17 | `Wallin 2007 ApJ 666 1296 TNO constant acceleration DOI 10.1086/520528` | Metadata check |
| Q18 | `Fienga 2009 "Gravity tests with INPOP planetary ephemerides" IAU Symposium 261 Proceedings` | Metadata check |
| Q19 | `zenodo planetary ephemeris residuals anomalous acceleration dataset` | §3.3 |
| Q20 | `Pitjeva Pitjev 2018 OR 2020 EPM dark matter density upper limit solar system planets new constraint` | Recent EPM |
| Q21 | `model-independent constraint extra acceleration solar system planetary ephemerides 2023 2024 2025 arXiv Mars Saturn Jupiter Juno` | Recent work |
| Q22 | `Fienga "Planetary ephemerides and gravity tests in the solar system" 2012 proceedings` | Metadata check |
| Q23 | `Frère Ling Vertongen 2008 "Bound on the dark matter density in the Solar System from planetary motions"` | Citation lead |
| Q24 | `Desmond Hees Famaey 2024 tension Radial Acceleration Relation Solar System quadrupole MNRAS 530` | Metadata check |

**Search limitations.** Q4–Q24 were partly steered by citations found in earlier results (§3.4 chasing), so they are not blind keyword queries. Recall for 2020–2026 work is weak. Q11 and Q21 returned no new model-independent bound after 2016, and the INPOP19a/21a/23 and EPM2017+ papers were not fully screened. An ADS full-text query run from an allowlisted machine is needed.

## 2. Records screened

Codes: **E** = eligible. **E-ms** = eligible to record, but model-specific (form fixed by a particular theory). **E-conv** = eligible, but converting to an acceleration needs an assumed spatial form. **X** = excluded. **P** = pending, not read in full.

| # | Record (read at) | Decision | Reason (protocol mapping) |
|---|---|---|---|
| R1 | Sereno & Jetzer 2006, MNRAS 371(2), 626–632 (journal ref read at doc.rero.ch/record/302492). Text: arxiv.org/pdf/astro-ph/0606197 | **E** | A published bound on a constant radial δA_R per planet, 2σ, using EPM2004 perihelion and mean-motion corrections from Pitjeva 2005. Model-independent form (constant). |
| R2 | Iorio 2011, "Solar system constraints on a Rindler-type extra-acceleration…", JCAP 2011(05) (osti.gov/biblio/22277660; text arxiv.org/pdf/1012.0226) | **E** | A bound on a constant radial acceleration per planet, from EPM range and range-rate residuals and from perihelion corrections. "Rindler" names the motivation, but the bounded form is a constant radial acceleration. **No confidence level stated.** DOI and pages not read (unverified). |
| R3 | Wallin, Dixon & Page 2007, ApJ 666, 1296–1302, doi:10.1086/520528 (arxiv.org/abs/0705.3408; text arxiv.org/pdf/0705.3408) | **E** | Constant radial δa at 20–100 au from orbit fits to 24 trans-Neptunian objects (MPC astrometry) with DE405 for the planets. 1σ. The method is orbit fitting against an ephemeris, not an ephemeris solution itself. Noted under "with method". |
| R4 | Fienga et al. 2009, "Gravity tests with INPOP planetary ephemerides", IAU Symp. 261 (ADS bibcode 2010IAUS..261..159F seen in Q18 results; text arxiv.org/pdf/0906.3962) | **E** (weak) | A constant acceleration added to Uranus, Neptune and Pluto and refit with INPOP08. The bound is stated **relative to the Pioneer value** ("no constant acceleration larger than 1/4 the Pioneer anomaly"). No confidence level. Neptune and Pluto absorb the acceleration. Also gives perihelion intervals (π̇) for INPOP08. |
| R5 | Fienga 2012, "Planetary ephemerides and gravity tests in the solar system", arXiv:1209.0635 (export.arxiv.org/abs/1209.0635: no journal-ref) | **P** → E if published | A Pioneer-direction constant acceleration on the outer planets, fitted over the INPOP10a sample and tested on Cassini Earth–Saturn ranges. "Only accelerations smaller than 5.10⁻¹³ m.s⁻² are acceptable". No confidence level. **Publication venue unverified.** |
| R6 | Fienga et al. 2011, "The INPOP10a planetary ephemeris and its applications in fundamental physics", CeMDA (link.springer.com/doi/10.1007/s10569-011-9377-8 listed in Q12; text web3.arxiv.org/pdf/1108.5546) | **E-conv** | Bounds on supplementary perihelion and node advances, Mercury–Saturn. The interval is "differences of postfit residuals from INPOP10a below 5%", **not a statistical confidence level**. Model-independent as a precession anomaly, but converting it to an acceleration needs an assumed radial form. |
| R7 | Fienga et al. 2016, "Tests of GR with INPOP15a…", arXiv:1601.00947 (proceedings; venue not stated) | **E-conv** | Supplementary perihelion advances for Mercury and Saturn under two residual-degradation criteria (5% and 35%). No confidence level. Venue unverified. |
| R8 | Pitjev & Pitjeva 2013, "Constraints on Dark Matter in the Solar System", doi:10.1134/S1063773713020060 (journal name not shown on page; unverified) (arxiv.org/abs/1306.5534, arxiv.org/pdf/1306.5534) | **E-conv** | EPM2011, about 677,000 observations. Gives perihelion-drift corrections, central-mass corrections, density limits and an enclosed-mass limit within Saturn's orbit. These are bounds on **extra mass**, which become an acceleration only under an assumed spherically symmetric distribution. The record uses "dark matter" as its own label; the Atlas would quote that label, not adopt it. Confidence level not explicit. |
| R9 | Pitjeva & Pitjev 2013, "Relativistic effects and dark matter in the solar system…", arXiv:1306.3043 ("Accepted 2013"; journal not named) | **E-conv** (duplicate) | Same EPM2011 solution as R8, with the same perihelion table. The concentrated-distribution mass limit is quoted as 7.88×10⁻¹¹ M☉, against 1.7×10⁻¹⁰ M☉ in R8; the two figures differ and are **unreconciled**. Precedence goes to R8 or R9 depending on journal verification. |
| R10 | Khriplovich & Pitjeva 2006, arXiv:astro-ph/0601422 (journal not named) | **E-conv** (superseded) | EPM2004 mass and density limits at Mercury, Earth and Mars. Same perihelion inputs as R1. Superseded by R8. |
| R11 | Frère, Ling & Vertongen 2008, PRD 77, 083005, doi:10.1103/PhysRevD.77.083005 (arxiv.org/abs/astro-ph/0701542) | **E-conv** (weak) | A density bound "of the order 10⁵ GeV/cm³" at Earth, assuming a spherical profile centred on the Sun. Only an order-of-magnitude bound. The ephemeris is not named in the abstract. |
| R12 | Park, Hees, Famaey, Desmond & Durakovic 2026, PRD, doi:10.1103/r7n8-kw38 (arxiv.org/abs/2602.17884) | **E-ms** | Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻² (1σ), using the DE440 dataset. A quadrupolar tidal-field parameter tied to the MOND external-field effect. **Model-specific.** It supersedes R13. |
| R13 | Hees, Folkner, Jacobson & Park 2014, PRD 89, 102002, doi:10.1103/PhysRevD.89.102002 (arxiv.org/abs/1402.6950) | **E-ms** (superseded) | Q₂ = (3 ± 3)×10⁻²⁷ s⁻² from 9 years of Cassini range and Doppler data. R16 states that DE430 was used. |
| R14 | Hees et al. 2014 proceedings, arXiv:1403.1365 | X | Duplicate of R13. |
| R15 | Hees, Famaey, Angus & Gentile 2015, MNRAS (arxiv.org/pdf/1510.01369) | X | Re-uses R13. No new bound. |
| R16 | Desmond, Hees & Famaey 2024, MNRAS 530(2), 1781–1795, doi:10.1093/mnras/stae955 (researchportal.port.ac.uk; text arxiv.org/html/2401.04796v2) | X | Re-uses R13 to test a theory. No new bound. |
| R17 | Bernus et al. 2020, INPOP19a Yukawa, arXiv:2006.12304 (journal not read) | X (record as model-specific) | The bound is on a Yukawa length λ_g (99.7% C.L.: λ_g > 3.43×10¹³ km), not on an acceleration. The form is theory-specific. |
| R18 | Iorio 2008, "Constraining MOND with Solar System dynamics", arXiv:0711.2791 | X | Constrains a MOND interpolation exponent only. Model-specific, with no acceleration bound. |
| R19 | Iorio, "Can the Pioneer anomaly be induced by velocity-dependent forces?…", arXiv:0806.3011 | X | No numerical acceleration bound. Velocity-dependent model forms. It does list EPM2006 perihelion corrections for Jupiter–Uranus, with errors rescaled by a factor of 10. |
| R20 | Iorio, "Gravitational anomalies in the Solar System?", IJMPD (arxiv.org/pdf/1412.7673) | X (review) | A review that compiles perihelion corrections across ephemerides. No new bound. Used for citation chasing (it points to R3). |
| R21 | Iorio, "Does the Neptunian system of satellites challenge a gravitational origin for the Pioneer anomaly?", arXiv:0912.2947 | X | Satellite orbits around Neptune. Tests only the Pioneer value and derives no bound. |
| R22 | Tangen, "Could the Pioneer anomaly have a gravitational origin?", arXiv:gr-qc/0602089 (journal not named in the text) | X / P | Tests only the fixed Pioneer value (8.7×10⁻¹⁰ m/s²) against DE414 right-ascension residuals for Uranus, Neptune and Pluto, at 99% confidence. It rejects that value for Uranus and Pluto but gives no upper bound. Kept as supporting evidence. |
| R23 | Standish 2009/2010, "Testing alternate gravitational theories", Proc. IAU 5(S261), 179–182, doi:10.1017/S1743921309990354 (Cambridge abstract page) | **P** | The abstract excludes several forms within 10 au but gives no numbers. The full PDF was blocked by the allowlist. **Unverified.** |
| R24 | Turyshev et al. 2012, "Support for the thermal origin of the Pioneer anomaly", arXiv:1204.2507 (PRL bibcode 2012PhRvL.108x1101T seen in Q8 results) | X | Spacecraft thermal modelling. No numerical bound stated. The page is self-ambiguous, with both "no statistically significant acceleration anomaly exists" and a "remaining 20%" phrase. Not an ephemeris bound. |
| R25 | Nieto 2008, PLB 659, 483, doi:10.1016/j.physletb.2007.11.067 | X | Reports the Pioneer measurement, not a bound. |
| R26 | Fienga & Minazzoli 2023/24, "Testing theories of gravity with planetary ephemerides", arXiv:2303.01821 | X (review), **important context** | Warns that published supplementary-perihelion results "have to be considered with a lot of caution because of the lack of consistency" with the framework used to build the ephemeris. The relevant Section 5 was not in the text read; **unverified**. |

**Identified at title level and not screened** (to finish in the formal run). These IDs appeared in results, but their titles or contents were not read: gr-qc/0608068, gr-qc/0611081, 0904.1562, gr-qc/0608101, 1309.7149, 1104.5192, 1210.3026, 1107.3445, 1301.1510, astro-ph/0702260, astro-ph/0504367 (an earlier TNO analysis, probably the precursor of R3), 2103.16745 (Planetary Ephemeris Program software), zenodo.org/records/3558850.

**Off-topic at title level:** 2601.10782 (high-frequency gravitational waves), 1909.00673, 2505.16317 (stellar flybys), 1005.1091 (LTB inhomogeneities), 0908.0040 (theory), 1001.3686 and 1107.2886 (Pioneer spacecraft analyses), gr-qc/9808081 and gr-qc/9903024 (Pioneer measurement).

## 3. Eligible bounds

All entries are **tier 2** (a bound printed in a paper). The baryonic side is "known masses as used in the fit": the Sun and planets as in the named ephemeris (EPM2004, EPM2011, INPOP08/10a/15a, DE405, DE430/DE440). The mass sets are **not yet read** for any record.

### 3a. Model-independent: constant radial extra acceleration

| Source | Quantity | Value, as printed | CL | Where | Ephemeris / data | Terms |
|---|---|---|---|---|---|---|
| R1 Sereno & Jetzer 2006 (Table 1, perihelia) | δA_R, constant radial | Mercury −1×10⁻¹² ≲ δA_R ≲ 5×10⁻¹³; Venus −4×10⁻¹² to 6×10⁻¹¹; Earth −5×10⁻¹⁴ to 3×10⁻¹⁴; Mars −3×10⁻¹⁴ to 4×10⁻¹⁴ m s⁻² | 2σ | at each planet's orbit | EPM2004 perihelion corrections (Pitjeva 2005b) | Journal copyright; the numbers are facts, quoted with citation |
| R1 (Table 2, mean motion) | δA_R | Mars ≲ 4×10⁻¹⁴; Earth ≲ 3×10⁻¹⁴ m s⁻² | 2σ | Mars, Earth | EPM2004 (Pitjeva 2005a) | as above |
| R1 (text) | δA_R | "≲ 5×10⁻¹² m/s² in the range 20-30 AU" | 2σ (paper-wide statement) | 20–30 au | Uranus and Neptune orbits, EPM2004 | as above |
| R2 Iorio 2011 JCAP | A_Rin, constant radial | Mercury and Venus 1–2×10⁻¹³; Mars ~10⁻¹⁵ (perihelion ≤7×10⁻¹⁵); Earth (perihelion) ≤7×10⁻¹⁶; Saturn ~1×10⁻¹⁴ (perihelion ≤3×10⁻¹⁴) m s⁻² | **not stated** | at each planet's orbit | EPM range and range-rate residuals (Mercury, Venus, Mars: Odyssey and MGS; Saturn: Cassini 2004–06); INPOP08 for Earth's perihelion | as above |
| R3 Wallin et al. 2007 | δa, constant radial beyond 20 au | 8.7×10⁻⁹ ± 1.6×10⁻⁸ cm s⁻² "directed outward" (my conversion: 8.7×10⁻¹¹ ± 1.6×10⁻¹⁰ m s⁻²) | 1σ | 20–100 au | 24 TNOs, MPC ECS astrometry (562 object-years), OrbFit with DE405 | as above; sign convention to check |
| R4 Fienga et al. 2009 | constant acceleration on Uranus | "no constant acceleration larger than 1/4 the Pioneer anomaly" | not stated | Uranus (~19 au; distance not stated in the text read) | INPOP08 | Stated relative to the Pioneer value, so it needs that value from its own source |
| R5 Fienga 2012 (venue unverified) | Pioneer-direction constant acceleration on the outer planets | "smaller than 5.10⁻¹³ m.s⁻²" | not stated | Saturn (Cassini ranges) | INPOP10a data sample | Pending venue |

### 3b. Model-independent precession anomalies (an assumed form is needed to convert)

| Source | Value (supplementary perihelion advance) | Interval definition | Ephemeris |
|---|---|---|---|
| R6 Fienga et al. 2011 | Mercury 0.4 ± 0.6; Venus 0.2 ± 1.5; EMB −0.2 ± 0.9; Mars −0.04 ± 0.15; Jupiter −41 ± 42; Saturn 0.15 ± 0.65 mas/cy | ≤5% degradation of postfit residuals (not a CL) | INPOP10a |
| R7 Fienga et al. 2016 | Mercury 0.0 ± 1.05 (5%) or ± 3.1 (35%); Saturn 0.05 ± 0.20 (5%) or 1.2 ± 5.0 (35%) mas/cy | residual criteria (not a CL) | INPOP15a |
| R8/R9 Pitjev & Pitjeva 2013 | Mercury −0.020 ± 0.030; Venus 0.026 ± 0.016; Earth 0.0019 ± 0.0019; Mars −0.00020 ± 0.00037; Jupiter 0.587 ± 0.283; Saturn −0.0032 ± 0.0047 mas/yr | σ, with the level not stated explicitly | EPM2011 |

### 3c. Extra-mass bounds (an assumed spherical form is needed to convert)

R8: ρ < 1.1×10⁻²⁰ g cm⁻³ at Saturn, < 1.4×10⁻²⁰ at Mars and < 1.4×10⁻¹⁹ at Earth. Extra mass within Saturn's orbit < 1.7×10⁻¹⁰ M☉ (concentrated profile; R9 gives 7.88×10⁻¹¹), or < 7.1×10⁻¹¹ M☉ (uniform). EPM2011. R10 and R11 are superseded or weak.

### 3d. Model-specific (recorded only, not for default views)

R12: Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻² (1σ), DE440 dataset. R13: (3 ± 3)×10⁻²⁷ s⁻². R17: Yukawa λ_g bound.

## 4. PRISMA-style counts (pilot run)

- **Identified:** 47 distinct records surfaced across Q1–Q24. The count is approximate: duplicates of the same paper across mirrors (arxiv, ar5iv, web3, Cambridge) were merged.
- **Excluded at title level as off-topic:** 8.
- **Not screened (pending):** 13 IDs whose titles or contents were not read.
- **Screened (full text or abstract read):** 26 (R1–R26).
- **Excluded after screening:** 11 (R14–R16, R18–R22, R24–R26). R17 is recorded under model-specific instead.
- **Pending a full read:** 2 (R5 venue, R23 full text).
- **Eligible:** 13. Model-independent constant acceleration: 4 (R1–R4). Precession or extra-mass, needing an assumed form: 6 (R6–R11). Model-specific: 3 (R12, R13, R17).
- **Included in a package:** 0. That awaits the §5 ruling, "Solar System limit: which published bound, and how a limit is drawn".

## 5. Open questions

1. **Which bound(s) to show.** The cleanest model-independent set is R1 (2σ, per planet, Mercury–Mars, plus 20–30 au) together with R3 (1σ, 20–100 au, TNOs). Both state their confidence level. R2 is tighter at Mars and Saturn but states no confidence level. R4 and R5 are weaker in documentation. All of these rest on ephemerides from 2004–2011 (EPM2004 and EPM2011, INPOP08 and INPOP10a, DE405). **No post-2016 model-independent bound on a constant or power-law acceleration was found.** The formal run should search ADS full text for INPOP19a, INPOP21a, INPOP23 and EPM2017+ papers. If none exists, that is itself a gap worth stating.
2. **Comparability.** The bounds differ in confidence level (2σ, 1σ, or none) and in interval definition (residual-degradation criteria). Showing them on one axis would need the Atlas to state each source's definition, without converting between them. Converting them would need new assumptions, which §1 forbids.
3. **The assumed form.** Every "acceleration" bound assumes a form, usually a constant radial term over the planet's orbit. A constant term is the least theory-laden choice, but it is still a choice. A precession or extra-mass bound converts to an acceleration only by assuming a form (constant, or a spherical extra mass). Proposal: show only bounds printed as accelerations by default, and list the others as precession or mass bounds with their native units.
4. **Fienga & Minazzoli's caution** (R26) about interpreting supplementary perihelion advances should be read in full (their Section 5). It may argue against using the R6, R7 or R8 precession bounds at all.
5. **How to draw the limit on an acceleration plot.** On a g_obs–g_bar plane, a planet sits at g_bar = GM_Sun/r² (Newtonian, known masses). A bound |δA| < A_lim at that r becomes a vertical error-bar-like **limit marker**: g_obs/g_bar − 1 lies within ±A_lim/g_bar at that g_bar. In a ratio view, it is an upper-limit arrow or band on |g_obs/g_bar − 1|, drawn as a small fractional deviation. Points should be one per bounded distance, or a horizontal segment for range bounds (20–30 au, 20–100 au). Each must be visibly a limit, not a measurement, and the CL should be printed on hover. **GM_Sun, the au, and the planets' mean distances must come from a cited source** (for example the ephemeris paper's own constants), not from memory. No fractional values are computed here for that reason.
6. **Sign conventions.** R1 gives signed two-sided intervals. R3 says "directed outward". R4 and R5 say "Pioneer-direction". The Atlas should record the sign convention per source and probably show |δA| limits.
7. **Baryonic side not yet read.** The planetary and asteroid-belt masses used by each ephemeris are needed for the "known masses as used in the fit" field.
8. **Terms.** All the bounds are printed values in copyrighted papers. Quoting a few numbers with citation is normal practice, but each record's licence still has to be read (rule 4). No files are redistributed.
9. **Process.** ADS and VizieR were not reachable from this session. The protocol is not yet frozen, so this is a pilot. The formal run must repeat Q1–Q24 plus ADS full-text queries after the freeze, or record this run in the §9 deviations register.
10. **Lunar laser ranging** (R2 mentions a Moon-based Rindler bound of ≲5×10⁻¹⁶ m s⁻²) and Earth-orbit tests are geocentric, not heliocentric. JvH should rule whether they belong in A0·orbits or need their own row.

---

## 6. Addendum, 2026-10-29: ADS step (deviation #2 remedy)

Run by Claude (AI) on 2026-10-29, through the browser on JvH's computer (approved by JvH, D-036 item 2). **Screening at this stage is on title and listing metadata only.** No values were read for this addendum.

**VizieR:** not applicable in practice for this cell (bounds are printed values in papers, not catalogues), and the native keyword search was not reachable from JvH's computer (see `docs/plans/DEVIATIONS.md` #2).

**Search vocabulary.** The queries use the literature's own terms, including names of accounts ("dark matter", "Pioneer anomaly", "external field effect"), because published bounds are indexed under them. The Atlas records the bound, not the account.

### 6a. Queries (verbatim), with counts

| # | Query | Sort | Records |
|---|---|---|---|
| ADS-A0-1 | `abs:(ephemeris OR ephemerides OR "planetary orbits" OR "perihelion precession" OR "planetary motions") abs:("anomalous acceleration" OR "extra acceleration" OR "additional acceleration" OR "constant acceleration" OR "dark matter" OR "external field effect" OR "Pioneer anomaly") property:refereed year:1990-2026` | citations | 111 |
| ADS-A0-2 | `abs:("planetary ephemeris" OR "planetary ephemerides" OR INPOP OR EPM OR "DE430" OR "DE440") abs:("gravity test" OR "gravity tests" OR "tests of gravity" OR "test of general relativity" OR "supplementary advance" OR "supplementary precession" OR constraint OR constraints) property:refereed year:1990-2026` | citations | 110 (the acronym "EPM" matched many off-topic records in other fields) |

### 6b. Title-level screening

Excluded at title level: theories or models constrained only through their own parameters (Yukawa, graviton mass, Lorentz violation, dilaton, Brans–Dicke, f(R), braneworld and similar: recorded as model-specific, as R17); spacecraft-only analyses (Pioneer trajectories); theory and reviews without a new bound; off-topic records.

**Already in this log:** 2006MNRAS.371..626S (R1); 2013AstL...39..141P (R8); 2013MNRAS.432.3431P (probably the journal version of R9; to confirm); 2006IJMPD..15..615K (R10); 2008PhRvD..77h3005F (R11); 2026PhRvD.114b4066P (probably R12; title "Improved constraints on modified Newtonian gravity from Cassini radio tracking data", to confirm against doi:10.1103/r7n8-kw38); 2014PhRvD..89j2002H (R13); 2016MNRAS.455..449H (R15); 2024MNRAS.530.1781D (R16); 2009IJMPD..18..947I (R19); 2015IJMPD..2430015I (R20); 2010MNRAS.405.2615I (R21); 2020PhRvD.102b1501B (Yukawa, INPOP19a: R17).

**New: pass to full-text screening** (R27–R41):

| # | Record | Title (short) |
|---|---|---|
| R27 | 1991AJ....101.2274H | Dynamical limits on dark mass in the Solar System |
| R28 | 1995ApJ...448..885A | Improved bounds on nonluminous matter in solar orbit |
| R29 | 1996ApJ...456..445G | Experimental limits on the density of dark matter in the Solar System |
| R30 | 2006NewA...11..600I | Orbital motions of the outer planets and the Pioneer anomaly |
| R31 | 2007JGrPh...1....5I | Jupiter, Saturn and the Pioneer anomaly |
| R32 | 2009AJ....137.3615I | The anomalous perihelion precession of Saturn |
| R33 | 2006JCAP...05..002I | Solar system planetary orbital motions and dark matter |
| R34 | 2010JCAP...05..018I | Sun- and planet-bound dark matter and planet and satellite dynamics |
| R35 | 2013Galax...1....6I | Pericentre precession from dark matter distributions: constraints |
| R36 | 2007IJMPD..16.1475K | Density of dark matter in the Solar System and perihelion precession |
| R37 | 2012MPLA...2750071I | Orbital effects of a time-dependent Pioneer-like anomalous acceleration |
| R38 | 2013SoSyR..47..386P; 2014CeMDA.119..237P | EPM2011 and EPM ephemerides and their scientific use |
| R39 | 2014A&A...561A.115V | MESSENGER data, planetary ephemeris and tests of general relativity |
| R40 | 2016A&A...587L...8F; 2020A&A...640A...6F | Constraints on a possible ninth planet from Cassini data and INPOP19a (residual-based limits on an extra pull) |
| R41 | 2009MNRAS.400..346I | Constraints on a distant body from inner Solar System dynamics |

### 6c. Counts for this addendum

| Stage | Count |
|---|---|
| Records identified (per query, not deduplicated across queries) | 111 + 110 = 221 |
| Already in this log | 13 records (two to confirm) |
| Passed to full-text screening | 15 entries (R27–R41), 17 records |
| Excluded at title level | the rest (regenerable by re-running the queries) |
| Full-text screening | **pending** (next step) |

---

## 7. Full-text screening of the §6 candidates (2026-10-29)

Screened by AI readers (Claude subagents) working to a written brief (`docs/sources/screening-brief-2026-10-29.md`): abstract, methods, observations, table captions and headings, data statements and release pages only; no dispersion, mass, mass-to-light or result values recorded. Checked by Claude against the brief (no values found in the output). Questions raised are consolidated for JvH in the PR; rulings will be recorded in `docs/decisions.md`. Decisions marked **P** wait on those rulings; **NS** rows are to be read through ADS full text.

### Block A0

Screened 2026-10-29 by Claude (AI). Every statement was read at the URL given. Anything not read is marked **unverified**. No numerical bound values were copied (A0 rule). D-036 default = a bound printed as an acceleration with a stated confidence level. Codes: E = eligible, default candidate. **E-rec** = eligible, recorded but not default: the bound is printed as an acceleration but no confidence level is stated. **E-conv** = an extra-mass, density or precession bound, which becomes an acceleration only under a stated form; recorded, not default. **E-ms** = model-specific, recorded only. X = excluded. P = pending. NS = could not read at source.

| # | Record | Source read | Decision | Form of bound, ephemeris, confidence level stated | Method notes | Licence/terms | Notes |
|---|---|---|---|---|---|---|---|
| R27 | Hogg, Quinlan & Tremaine 1991, "Dynamic limits on dark mass in the outer solar system", AJ 101, 2274–2286, doi:10.1086/115849. The journal name comes from the bibcode and DOI; the page read did not state it. No arXiv version found. | data.zhenzhi.com/details/1/1001546323 (abstract only) | **P** (full text unverified) | Form: the minimum detectable dark mass in the outer Solar System, and how well a "Planet X" location can be predicted. Ephemeris: "modern ephemerides", name not stated. CL: none stated (significance discussed qualitatively). | Simplified model solar systems with known observational errors, used to assess search strategies. Fits to outer-planet and comet observations. Partly a detectability and simulation study. Whether it prints an actual bound from real data is **unverified**. | Journal copyright; terms not read | If it gives a bound, it is an extra-mass bound (E-conv). The full text is needed. |
| R28 | Anderson, Lau, Krisher, Dicus, Rosenbaum & Teplitz 1995, ApJ 448, 885, doi:10.1086/176017; arXiv:hep-ph/9503368. The journal comes from the bibcode and DOI; the arXiv page gives no journal-ref. | arxiv.org/abs/hep-ph/9503368; ar5iv.labs.arxiv.org/html/hep-ph/9503368 | **E-conv** (not default) | Form: an upper limit on the mass of a **spherically symmetric distribution interior to the orbits of Uranus and Neptune**, from the difference between the effective GM felt by those planets and GM_Sun from the inner planets. Ephemeris: JPL **DE242** (all 194 parameters refit; residuals relative to DE200). CL: formal errors ×3, called "realistic one-sigma". No formal CL. An isothermal-sphere density is also given, but the authors call it not meaningful. | Data: optical (meridian circle since 1911), radar, Mars spacecraft ranging, lunar laser ranging, Mariner 10 and Galileo ranging, and Pioneer 10/11 and Voyager 1/2 DSN ranging at the outer planets. No bound is printed as an acceleration. | Journal copyright; arXiv preprint, licence not shown | Spherical extra mass converts to a radial acceleration (GM/r²) only under the stated spherical form. A pre-2000 ephemeris. |
| R29 | Grøn & Soleng 1996, ApJ 456, 445, doi:10.1086/176669; arXiv:astro-ph/9507051 (preprint says "To appear in the Astrophysical Journal") | arxiv.org/abs/astro-ph/9507051; ar5iv.arxiv.org/html/astro-ph/9507051 | **X** (not derived from a planetary ephemeris fit) | Form: an upper limit on a constant dark-matter density (also given as enclosed mass within the Uranus and Pluto orbits). Data: the **perihelion precession of the asteroid Icarus**; the data source and ephemeris are not named. CL: none (the limit is set by the observed uncertainty). | Built on a TOV-type relativistic model with hydrostatic, dust-like matter matched to a galactic background. 1/r⁴ and 1/r² profiles were also tried. | Journal copyright | Excluded on the "planetary ephemeris fits" rule. It is also theory-laden through the galactic matching condition. Uranus appears only as a comparison with an earlier bound. |
| R30 | Iorio & Giudice 2006, "What do the orbital motions of the outer planets … tell us about the Pioneer anomaly?", New Astronomy, doi:10.1016/j.newast.2006.04.001; arXiv:gr-qc/0601055. Volume and pages are from the bibcode only (unverified). | arxiv.org/abs/gr-qc/0601055; ar5iv.labs.arxiv.org/html/gr-qc/0601055 | **X** | Form: tests only the **fixed Pioneer-magnitude** constant radial sunward acceleration beyond about 15 au. **No upper bound derived.** Ephemeris: **EPM2004** (Pitjeva 2005; Uranus, Neptune and Pluto optical data from 1913–2003). CL: none (largely a visual comparison of residuals). | Gauss-equation perturbations plus numerical integration (Mercury package), compared against Pitjeva's RA/Dec residuals. Robust to errors inflated by about 10×. | Journal copyright | Same handling as R21 and R22 in the log: a fixed-value test, not a bound. |
| R31 | Iorio 2007, "Jupiter, Saturn and the Pioneer anomaly: a planetary-based independent test", J. Grav. Phys. 1(1), 5–8; arXiv:0712.1273 (journal-ref printed on arXiv) | arxiv.org/abs/0712.1273; ar5iv.labs.arxiv.org/html/0712.1273 | **X** | Form: tests only the fixed Pioneer-type constant radial acceleration at Jupiter and Saturn. **No upper bound derived.** Ephemeris: **EPM2004** perihelion extra-rates (Pitjeva). CL: none (errors rescaled; contributions summed linearly). | Ratio of the two planets' apsidal extra-rates compared with the predicted precessions. | Journal copyright; arXiv licence not shown | A fixed-value test, not a bound. |
| R32 | "The recently determined anomalous perihelion precession of Saturn", AJ 137(3), 3615, doi:10.1088/0004-6256/137/3/3615 (OSTI). Matched by title to Iorio, arXiv:0811.0756 ("On the recently determined…"). | osti.gov/biblio/21269284; ar5iv.arxiv.org/html/0811.0756 | **E-rec** (not default) | Form: Saturn's anomalous perihelion precession converted to a **constant, uniform, Sun-directed acceleration ± uncertainty**. The paper calls it a phenomenological estimate, not a formal bound. Ephemeris: **EPM2008** (data 1913–2007, including Cassini normal points 2004–06). CL: **not stated** for the acceleration. Model exclusions elsewhere carry σ levels. | Critical assessment, not a new fit. Also tests TNOs, mass errors, Lense–Thirring, PPN, Yukawa, velocity-dependent forces, DGP, MOND, spherical dark matter and Λ. Those parts are model-specific. Argues that the inner-planet perihelia are inconsistent with such a constant term. | Journal copyright | The OSTI page names only "E. V. Pitjeva" as author. The author link to Iorio and to arXiv:0811.0756 rests on the title match and the bibcode initial "I", so it is **unverified**. The precession input is the EPM2008 value, which this paper did not produce. |
| R33 | Iorio 2006, "Solar System planetary orbital motions and dark matter", JCAP 2006(05), 002, doi:10.1088/1475-7516/2006/05/002; arXiv:gr-qc/0602095 | arxiv.org/abs/gr-qc/0602095; ar5iv.labs.arxiv.org/html/gr-qc/0602095 | **E-conv** (not default; superseded) | Form: an upper bound on a **constant-density, spherically symmetric** extra mass (in g cm⁻³). The radial acceleration (∝ density × r) is only an intermediate step. Ephemeris: **EPM2004** perihelion and mean-longitude formal errors. CL: **not stated** ("formal errors", "conservative"). | Gauss equations averaged over an orbit. A Mercury–Earth–Mars combination cancels Lense–Thirring and J2. Semimajor-axis systematics added in quadrature. | Journal copyright | Same EPM2004 inputs as R1 and R10. Superseded by EPM2011 bounds (R8). |
| R34 | Iorio 2010, "Effect of Sun and planet-bound dark matter on planet and satellite dynamics in the Solar System", JCAP 2010(05), 018, doi:10.1088/1475-7516/2010/05/018; arXiv:1001.1697 | arxiv.org/abs/1001.1697v2; ar5iv.labs.arxiv.org/html/1001.1697 | **X** (no new ephemeris bound; model-specific) | Form: a bound on the **fractional rate of change of the central body's GM** (per year), under an accretion model. Not an acceleration and not a static extra mass. Ephemeris: none fitted. It cites DE421, LLR and EPM results. CL: not stated. | Analytical secular perturbations for a time-varying GM, applied to planets, satellites and LAGEOS, using accretion rates from the literature. | Journal copyright | Re-uses published GM-dot and orbital-rate determinations. The form is tied to an accretion model. |
| R35 | Iorio 2013, "Exact expressions for the pericenter precession caused by some dark matter distributions…", Galaxies 1(1), 6, doi:10.3390/galaxies1010006; arXiv:1304.6396 | arxiv.org/abs/1304.6396; mdpi.com/2075-4434/1/1/6 | **E-conv** (not default; profile-specific) | Form: bounds on the local density parameter ρ₀ of **specific spherical profiles** (exponential and power-law). Ephemeris: **EPM2011** supplementary perihelion precessions (Pitjev & Pitjeva). CL: **not stated**. The author calls the bounds "generous" because the whole observed range is attributed to extra mass. | Poisson equation → orbit-averaged potential → Lagrange equations → secular pericentre precession, compared with the EPM2011 values. Also covers the double pulsar and the Galactic centre (outside A0). | **CC BY 3.0** (MDPI page metadata) | Same EPM2011 precession inputs as R8 and R9, re-interpreted with no new measurement. Converting to an acceleration needs the stated profile. |
| R36 | Khriplovich 2007, "Density of dark matter in Solar system and perihelion precession of planets", IJMPD, doi:10.1142/S0218271807010869; arXiv:astro-ph/0702260. Volume 16 and page 1475 are from the bibcode only (unverified). | arxiv.org/abs/astro-ph/0702260; ar5iv.labs.arxiv.org/html/astro-ph/0702260 | **E-conv** (not default; duplicate inputs) | Form: an upper limit on the **local density at each planet's orbit** (Mercury, Earth, Mars), via a small-eccentricity relation between perihelion shift and local density. Assumes a spherically symmetric distribution centred on the Sun. Ephemeris: **EPM** perihelion deviations (Pitjeva); version not stated on the page. CL: ± given, σ level not stated. | Perturbed potential → difference between the orbital and radial frequencies. Venus and the outer planets omitted. | Journal copyright | Re-interprets the same class of EPM perihelion data as R10 (Khriplovich & Pitjeva 2006). The text says its limits "agree with those derived previously". Superseded by R8. |
| R37 | Iorio 2012, "Orbital effects of a time-dependent Pioneer-like anomalous acceleration", MPLA, doi:10.1142/S021773231250071X; arXiv:1107.3445. Article number 1250071 is from the bibcode only. | arxiv.org/abs/1107.3445v1; ar5iv.arxiv.org/html/1107.3445 | **E-rec** for the constant term at Saturn (not default). The time-dependent part is **X**. | Form: (a) an upper bound on a **constant, radial, sunward acceleration at Saturn**, from the perihelion-precession uncertainty; (b) a linear time-dependent Pioneer-like term, tested only as a fixed model. Ephemerides: **INPOP10a** (Saturn perihelion) and **EPM2006/EPM2010** formal errors. CL: **not stated** (formal errors, with a 10× rescaling test). | Gauss equations for a and e, averaged over the eccentric anomaly. Saturn and Uranus are the focus; Earth, Neptune and Pluto are compared. | Journal copyright | The Saturn input is the INPOP10a supplementary precession already logged under R6. |
| R38a | Pitjeva 2013, "Updated IAA RAS planetary ephemerides EPM2011 and their use in scientific research", Solar System Research 47(5), 386–402; arXiv:1308.6416 (citation printed in the text) | ar5iv.labs.arxiv.org/html/1308.6416; web3.arxiv.org/pdf/1308.6416 | **X** (duplicate of R8 for the extra-mass bounds) | Form: density limits at the Saturn, Mars and Earth orbits and an enclosed-mass limit within Saturn's orbit, with a centrally concentrated case. **No acceleration bound.** Also gives PPN β and γ (formal σ, with a stated multiple), a GM_Sun rate, and additional perihelion motion. Ephemeris: **EPM2011** (about 680,000 positions, 1913–2011). CL for the extra-mass limits: none stated (estimates compared with errors). | The extra-mass section cites Pitjev & Pitjeva 2013 (Astronomy Letters, R8) as its source. | Journal copyright | The extra-mass bounds repeat R8. PPN and GM_Sun-rate results are model-specific or out of scope. |
| R38b | Pitjeva & Pitjev 2014, "Development of planetary ephemerides EPM and their applications", CeMDA 119(3–4), 237–256, doi:10.1007/s10569-014-9569-0 | pureportal.spbu.ru (record page); iaaras.ru/library/paper/39 (abstract) | **P** (full text unverified) | Form: the abstract mentions "the upper limit on the mass of dark matter in the Solar System" (an extra-mass bound, so E-conv if new). Ephemerides: EPM2004, EPM2008 and EPM2011, with early **EPM2013** results. CL: not stated in the abstract. | Abstract only. No arXiv version found. | Journal copyright | Need to check whether the mass limit is new (EPM2013) or repeats R8. |
| R39 | Verma, Fienga, Laskar, Manche & Gastineau 2014, "Use of MESSENGER radioscience data to improve planetary ephemeris and to test general relativity", A&A 561, A115, doi:10.1051/0004-6361/201322124; arXiv:1306.5569 | aanda.org/articles/aa/abs/2014/01/aa22124-13/aa22124-13.html; ar5iv.arxiv.org/html/1306.5569 | **E-ms** (record only) | Form: PPN β and γ estimates. **No anomalous-acceleration bound** in the abstract or the text read. Whether a supplementary perihelion advance is given (Sec. 4.2, Table 5) is **unverified**. Ephemeris: **INPOP13a** (MESSENGER range biases from GINS). CL and interval definition: **unverified**. | About 1.5 years of MESSENGER X-band Doppler and range, processed with GINS, then INPOP refit. | "© ESO, 2014"; no licence stated | If Table 5 gives a supplementary perihelion advance, that part would be E-conv (as R6/R7). |
| R40a | Fienga, Laskar, Manche & Gastineau 2016, "Constraints on the location of a possible 9th planet derived from the Cassini data", A&A 587, L8, doi:10.1051/0004-6361/201628227; arXiv:1602.06116 | arxiv.org/abs/1602.06116v3 | **E-conv** (not default) | Form: a residual-based **exclusion of positions (true-anomaly ranges) of an extra point mass** with assumed properties, plus a best-fit position. No mass limit or acceleration in the abstract. Ephemeris: INPOP (version not named in the abstract) with Cassini ranging. CL: **not defined** in the abstract. | Add the body, refit, and check residual degradation and improvement in the Cassini ranges. | A&A copyright; licence not read (unverified) | Point-mass form: implies a tidal (non-radial) acceleration only under the stated mass and position. See question 1. Superseded by R40b. |
| R40b | Fienga, Di Ruscio, Bernus, Deram, Durante, Laskar & Iess 2020, "New constraints on the location of P9 obtained with the INPOP19a planetary ephemeris", A&A 640, A6, doi:10.1051/0004-6361/202037919 | aanda.org/articles/aa/abs/2020/08/aa37919-20/aa37919-20.html | **E-conv** (not default) | Form: a **minimum distance as a function of assumed mass** for an extra point mass, plus zones where it degrades the ephemeris. No acceleration form. Ephemeris: **INPOP19a** (Juno-updated Jupiter, reanalysed Cassini). CL: compared with formal INPOP accuracy "in sigma units". The detailed definition is not in the abstract (unverified). | Two tests: position differences against the propagated covariance, and a χ² likelihood of postfit residuals. | **CC BY** ("Creative Commons Attribution License"; © the authors 2020) | The most recent ephemeris-based extra-mass bound in this batch. |
| R41 | Iorio 2009, "Constraints on planet X/Nemesis from Solar System's inner dynamics", MNRAS 400, 346, doi:10.1111/j.1365-2966.2009.15458.x; arXiv:0904.1562 | arxiv.org/abs/0904.1562v2; ar5iv.arxiv.org/html/0904.1562 | **E-conv** (not default) | Form: an upper limit on the **tidal parameter GM_X/r_X³ (s⁻²)** of a distant point mass, using a Hooke-type radial term plus a fixed-direction term, converted to a minimum distance by mass and sky position. Ephemeris: **EPM** inner-planet perihelion corrections (Pitjeva); version not specified. CL: **not stated** (the paper says the errors are not formal statistical errors). A pulsar-timing comparison uses 95%, but that is not an ephemeris bound. | Gauss perturbations on Mercury–Mars perihelia. Indirect effects via the outer planets are found negligible. | Journal copyright | A tidal form, so the acceleration is the parameter × r under the stated form. Inputs are the published EPM perihelia (no new fit). |
| C1 | 2013MNRAS.432.3431P vs R9 | pureportal.spbu.ru (MNRAS record); arxiv.org/abs/1306.3043 | **Confirmed** | — | — | — | The SPbU record gives Pitjeva & Pitjev, "Relativistic effects and dark matter in the Solar system from observations of planets and spacecraft", MNRAS 432(4), 3431–3437, 2013, doi:10.1093/mnras/stt695. arXiv:1306.3043 has the same authors and the same title (except "spacecrafts") and is marked "Accepted 2013". The arXiv page does not itself carry the journal-ref, so the match rests on authors and title. R9 = MNRAS 432, 3431. The R8/R9 mass-limit discrepancy in the log remains unreconciled. |
| C2 | 2026PhRvD.114b4066P vs R12 | journals.aps.org/prd/abstract/10.1103/r7n8-kw38 | **Confirmed** | — | — | — | The APS page gives Park, Hees, Famaey, Desmond & Durakovic, "Improved constraints on modified Newtonian gravity from Cassini radio tracking data", PRD 114, 024066, issue 2, published 28 July 2026, doi:10.1103/r7n8-kw38. This is R12. |

#### Questions raised by the screeners

1. **Localised extra mass (R40a, R40b, R41, and R27 if confirmed).** These bound a distant point mass ("Planet 9"/"Planet X"). The implied extra acceleration is tidal and direction-dependent, not radial. Should they sit in A0 as recorded E-conv entries, or in a separate "localised extra mass" sub-row? None qualifies as a D-036 default.
2. **Bounds printed as accelerations without a CL (R32, R37).** Under D-036 these are recorded, not default. That is consistent with R2, R4 and R5 in the existing log. No new default-eligible bound (acceleration + CL) was found in R27–R41.
3. **Non-ephemeris orbit data (R29, asteroid Icarus).** Excluded here because it is not a planetary ephemeris fit. Confirm, or rule that asteroid perihelia count (R3, the TNO astrometry case, was admitted with a note).
4. **Still to read in full:** R27 (AJ 1991, no open text found), R38b (CeMDA 2014), and R39 Sec. 4.2 / Table 5. The R32 author attribution should be confirmed against the AJ page.

---

## 8. Re-coding under D-038 (2026-10-29)

Applies JvH's rulings D-038 (and D-036, D-037) to the rows coded **P** in §7. No values were opened. New code **E-rec**: eligible and recorded, not plotted in v1.0 (the reason is given). "Plot" decisions remain subject to the conversion, coverage and pairing checks at packaging.

| Row | Was | Now | Rule applied |
|---|---|---|---|
| R27 | P | P | Full text not reached; read through ADS (scanned article). |
| R38b | P | P | Full text not reached; read through ADS. |
| R40a, R40b, R41 | E-conv | E-conv, sub-row 'localised extra mass' | Single distant body: separate A0 sub-row, never default (D-038 5B). |
| R29 | X | E-conv (recorded, not default) | Single-asteroid (Icarus) bound recorded, consistent with R3 (D-038 5C). |

### 8a. Rows not read in §7, resolved through ADS (2026-10-29)

Read on ADS abstract pages through the browser on JvH's computer. Some abstracts of older papers state dispersion or mass-to-light values in the text; they were seen by Claude in passing and are **not recorded here**. Older single-system papers are coded by D-038 3B (precedence among originals): they are kept as alternatives where later originals release per-star velocities or have more members.

| Row | Was | Now | Basis |
|---|---|---|---|
| R27 | P | X | ADS abstract (1991AJ....101.2274H): detectability study on simulated model solar systems; no bound fitted to observations. |
| R38b | P | E-conv (likely duplicate of R8) | ADS abstract (2014CeMDA.119..237P): review of EPM ephemerides and their uses, including the dark-mass upper limit (EPM2011, as R8). EPM ephemeris files are public (ftp://quasar.ipa.nw.ru/incoming/EPM/): a source for the baryonic side (masses used). |
