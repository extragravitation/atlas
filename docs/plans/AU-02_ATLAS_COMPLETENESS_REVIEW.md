# AU-02: Atlas completeness review: site and repository (v0.2, origin/main 3ab9151)

2026-11-12, clock 17:21 (TZ=America/Edmonton). **FILED as input to the completeness plan (JvH, 17:57: "file under a new folder").**
- **Read:**
  - every site page source;
  - TAXONOMY_v2, SELECTION_PROTOCOL, MASTER_PLAN_v2 §5 and §8;
  - DEVIATIONS (#1–#23);
  - the search logs A0, A3, A5, A6, A6-gas, A9, S9, and the A9 screening;
  - decisions D-028, D-067, D-074, D-110;
  - CK-01 (today's review comparison).
- **Not read:** GitHub issues (this session has no API access to the repository); per-package known_issues.
- **This supersedes AU-01 where they differ.**

## 1. What is already in place (the structure is strong)

- **Frozen taxonomy** (11 kinds × 6 tracers), frozen **selection protocol** (Zenodo 10.5281/zenodo.23780203), **data freeze 2026-12-24**, and a deviations register (23 entries).
- **Coverage page** rendered from the ruled documents:
  - in-hand table;
  - kinds;
  - frozen grid;
  - coverage on continuous axes (distance, radius, g_bar);
  - epoch gap;
  - protocol;
  - gate.
- **For-data-providers page.**
- **Tests page:** test ledger, plus "Accounts" (a template is defined; no pages yet; "which accounts are presented will be decided by a rule published here before any page is written").
- **Methods page:** a "Limitations and gaps" section; known-issues page; reproduction page; scale strip; system and dataset pages.

## 2. Status of every cell (from the search logs and decisions, not memory)

| Cell | State |
|:--|:--|
| A0 Solar System (limit) | **Searched** (5 eligible, 23 eligible-with-conversion). **Not packaged.** |
| A1 Wide binaries | **Not searched** (protocol order: step 3) |
| A2 Open clusters | **Not searched** (step 4) |
| A3 Globular clusters | Searched (49 eligible). **One package** (Baumgardt: 62 plotted / 243 recorded) |
| A4 Rotation | SPARC only. **Second disc set not searched** (step 3) |
| A4/A6 Weak lensing | KiDS-1000 packaged |
| A5 Dwarfs | Searched (46 eligible). One package (56 plotted / 66 recorded). Famous dwarfs out by the D-038 rules |
| A6 Strong lensing | Packaged (94) |
| A6 Stellar dynamics, GCs/PNe, X-ray, HI rings | **Not searched** |
| A7 Unusual configurations | **Not searched** (step 4) |
| A8 Groups | **Not searched** (step 4); leads logged in the A9 search |
| A9 Hot gas | X-COP: 5 plotted, 7 recorded without stars |
| A9 Lensing and member galaxies | **Searched and screened** (28 E + 33 E-pair). **Method rulings done** (D-067, D-071–D-074). **Route ruled** (D-074): about 8 case studies (A85, A2142, ZwCl 1215, A1689, A1835, A2390, MS 1455+22, Coma) + a LoCuSS one-radius layer + a funnel page. **Not built.** |
| A10 Colliding clusters | Leads only (logged in the A9 search). Maps need a data form the standard does not yet have |
| High redshift | Documented gap (D-033, D-066) |

**The protocol's own order of work** is:
1. A3, A5, A0;
2. A6, A9;
3. A4 second set, A10, A1;
4. A2, A7, A8.

**Steps 1–2 are part-done. Steps 3–4 have not started.**

## 3. What makes it incomplete in a reader's eyes

1. **Kinds and measurement routes missing from the frozen taxonomy** (CK-01):
   - vertical dynamics of discs;
   - the Milky Way as a multi-tracer system (including the escape-speed curve);
   - tidal streams;
   - shell galaxies;
   - binary galaxies and satellites;
   - the Local Group (timing argument, local Hubble flow);
   - direct acceleration measurements;
   - tidal radii.
2. **Famous test systems absent and not mentioned anywhere on the site:**
   - M33, LMC, M31, the Milky Way;
   - DF2, DF4, Dragonfly 44, AGC 114905;
   - Crater II, Carina, Antlia II;
   - Pal 5, Pal 14;
   - NGC 5291 (tidal dwarfs);
   - NGC 720, NGC 1521;
   - Bullet, Abell 520, El Gordo, Coma.
3. **No scope statement** beyond the taxonomy's single "Beyond clusters: not included" row. Evidence outside the charter is not listed for either side.
4. **Exclusion rules with possibly lopsided effects:** D-038 removes Crater II, Carina, Antlia II and others. Effect on balance not audited.
5. **Accounts layer empty.** The rule for which accounts appear is not yet written.

## 4. Stale or inconsistent text (credibility, quick to fix)

| Place | Problem |
|:--|:--|
| Coverage page, section heading | "Selection protocol (draft)". Frozen and deposited 29 Oct. |
| Coverage page lede and "Release gate" section | Describe v1.0 as covering every cell (D-028). D-110 / deviation #23 narrowed v1.0 on 5 Nov. |
| Methods page, "Limitations and gaps" | Same pre-D-110 v1.0 wording. |
| MASTER_PLAN_v2 §8 roadmap | Pre-D-110 v1.0 definition. Plan document only, but linked. |
| SELECTION_PROTOCOL.md opening line | "Draft… Not frozen". Part of the frozen text and cannot be edited. **The page that renders it should say it is frozen**, with the date and DOI. |

## 5. How to make it complete (proposed sequence; each step is JvH's ruling)

**Phase 0: text fixes (hours).** The section 4 items, by pull request.

**Phase 1: define "complete" (rulings; no new data).**
1. **Full-text read** of the four field reviews, plus one more from the dark-matter side, so the lists are exhaustive.
2. **Taxonomy v3:** add the kinds and measurement routes in section 3.1 (via the deviations register).
3. **Test-system checklist:** every system the reviews use as a test case. Each gets a status (in / candidate / excluded with rule / gap with reason) and is rendered on the Coverage page. The inclusion criterion is symmetric: "used as a test case in the published debate, by any side".
4. **Scope statement:** evidence outside the charter, listed for both sides, rendered on Coverage.
5. **Exclusion-effect audit:** for each exclusion rule, which named test systems it removes, and in whose favour.
6. **Accounts rule:** which accounts get pages, written before any page.

**Phase 2: build what is already searched and ruled.**
- A9 (D-074 route: case studies, LoCuSS layer, funnel page).
- A0 limit.
- Further eligible A3 and A5 records.

**Phase 3: search and build the unsearched cells**, in protocol order:
- A4 second set, A10 maps (needs a "map" data form), A1 case study;
- then A2, A7, A8;
- then the new v3 cells.

**Phase 4:** account pages and patterns.

**Release framing (D-110):**
- v1.0 = data in hand + re-issue + formal review + methods paper.
- Phases 2–4 arrive as v1.x.
- **Phase 1 should be live before v1.0**, so the formal review sees a complete *plan*, even where the data are not yet in.

## 6. Practical note

This session cannot push to the Atlas repository; GitHub access would need adding. **Atlas work should run in the Atlas project ("AEG Website")** under its own CONTINUATION guide. This note and CK-01 are its inputs.
