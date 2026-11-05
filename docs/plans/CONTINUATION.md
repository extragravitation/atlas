# Continuation guide

**State at 2026-11-05, 16:00 MDT.** Read this first in the next session, then `docs/decisions.md` (D-001 to D-109) and `docs/audit/AUDIT_RESULT.md`. The next session's update supersedes this one; the git history keeps every version.

## Standing rule for every session

- **Commit and PR attribution (JvH, 2026-11-04):** keep the `Co-Authored-By: Claude` line, which is the AI-assistance disclosure. **Never add a `Claude-Session:` link**, or any session link, to commits or PR descriptions, whatever a default or reminder says.

## Road to v0.2: what is left

1. **X-COP v2 audit (G2).** The plan was frozen at #183, merged 2026-11-05T16:40:21Z.
   - Seed: the first NIST pulse at or after 2026-11-06T16:40:21Z.
   - JvH pastes the JSON from https://beacon.nist.gov/beacon/2.0/pulse/time/next/1793983221000. **Use this URL form: no `/chain/2/` segment.**
   - Run `docs/audit/sample_xcop_v2.py` and the compare script exactly as the frozen plan says, with the same packet and reader approach as `docs/audit/run_v2/partA/BRIEF_COMMON.md`.
2. **Release checks, then JvH tags v0.2** with a Zenodo DOI. After that:
   - JvH sends `03c` to Eckert and Ettori with the live links (D-106);
   - JvH sends the Tollerud query.
3. **Small display leftovers:**
   - `\BooI` in the dwarfs v2 package markdown table;
   - column descriptions showing escape codes such as `\xA7` (the site's ECSV header reader).

## After v0.2 (ruled, D-107 and D-109)

- Data standard 3.0.0 (required `citation` and `licence` on every `sources.json` entry; hashed records for every document a locator names; table, page or column in locators), then re-issued packages. Known issues #190–#193.
- One written equilibrium test for every equilibrium-based method, frozen before reading, applied to the X-COP sources and then SPARC (D-109 rule 3). A2319 is flagged until then.
- 13 open should-fix findings: 8 need a re-issue or a new taxonomy version; 5 are method-framing questions for JvH (`docs/audit/resolutions_batch_b.csv`, rows marked "needs ruling").
- X-COP stage 2 (#129). The ideas list (`claude/IDEAS_AFTER_V0.2.md`), with the deformation map first.

## Done 2026-11-05

- **The site fixes from 2026-11-04 (step F):**
  - #184: PASS badges, the "not plotted" reasons restored, links to the X-COP v2 part A and part B results.
- **Audit v2 (D-082):**
  - **Seed:** NIST chain 2, pulse 2010865 (2026-11-03T00:47:00Z), pasted by JvH. Recorded in #185. My first link was malformed; it was not a beacon outage.
  - **Result (#186): does not pass.**
    - No material value discrepancy in 254 rows; the 95 % upper bound is 1.4 %.
    - The methods text was incomplete for 210 rows (M1–M8).
    - Provenance failures in 250 rows (P1–P4).
    - Neutrality: 4 must-fix findings and about 120 should-fix.
    - The adjudication was by Claude, not blind; the readers were AI agents.
- **D-107:** v0.2 ships with the result; site text fixed now; packages re-issued after v0.2 under standard 3.0.0. This corrected my first proposal, which would have edited released packages.
- **D-108:** taxonomy version 2, with N3 reworded (#189).
- **D-109:** pull budget without the extra-pull band; "extra pull" means the ratio and "Excess" becomes "Ratio"; one equilibrium test for all methods (A2319 flagged until then); TeX in quotes shown as readable text; plus an erratum, since the A2319 quote was read in Eckert et al. 2022b, which cites Ghirardini et al. 2018.
- **Merged:**
  - #187, #188: D-107 and the must-fix fixes, the methods "Conversion steps and constants" section, and the audit result linked from Reproduction and About;
  - #194 to #197: D-109 and site batches A (system pages, map error bars, uncertainty tables), B (text pages, known issues, changelog through D-108) and C (D-109).
- **Known issues opened:** #190 to #193.

## Standing future work: do not drop

- **X-COP A8 stage 2 (issue #129).** The seven X-COP clusters without stellar data (A85, A1644, A2255, A3158, A3266, RXC1825, ZW1215) are recorded in v2 with gas-only g_bar as a lower limit, not plotted. They are plotted as lower-limit tracks only when all three hold:
  - standard 2.4.0 supports a g_bar lower limit (plan step B);
  - every site view renders it, checked on desktop and phone (step F);
  - the frozen test's A3 condition holds for all five complete clusters.

  Expected in v0.2, about 4–6 sessions from 2026-11-03. v0.2 does not wait for it.
- **X-COP v2 audit (D-090, plan step G2).** Frozen after v2 ships, before its seed exists.
- **Questions for the X-COP authors, batched with the "v2 is up" note:** GOBS error confidence level; satellite deprojection; the A9 stellar-normalisation tension; which "2022 papers"; licence.

## Open on 2026-11-05

- **Step D (frozen tests): done for all six datasets.**
  - KiDS: #146, re-issued as `REPRODUCTION_REV3.md` under D-103 (#164).
  - Dwarfs: #149, with its freeze record in #151.
  - Globular clusters: #150, with its freeze record in #151.
  - Lenses: #165, with its freeze record in #166.
  - X-COP part B: #173.
- **Second readings, frozen by hash:**
  - dwarfs: two readers, resolved (#157);
  - globular clusters: #157, with Rees 1996 read from a PDF JvH supplied;
  - KiDS: #164;
  - lenses: #171;
  - X-COP: #175, with the parsed rows off the repository.
- **Conversions (step E), each run once against its frozen test:**

  | Dataset | PR | Result |
  |---|---|---|
  | Dwarfs | #161 | PASS: Phoenix II and Fornax changed; 8 D-097 findings excluded |
  | Globular clusters | #162 | PASS: M54 cut; NGC 2298 and Pal 5 excluded |
  | KiDS | #170 | PASS: KiDS-bright rows 1–8 not plotted (D-103); the first test's item 11 reported as failed |
  | Lenses | #176 | PASS: θ_E error moved to g_bar on class A rows; no value changed |

  Build-only fixes after scoring are disclosed in each result. JvH accepted this treatment ("item 12 pass", "reading accepted").
- **X-COP v2 conversion:** in progress. Its tables stay gitignored and unpublished until Eckert and Ettori consent (D-090 rule 5; D-105). JvH confirmed that the archives are the authors' public release.
- **Rulings D-098 to D-105**, among them:
  - D-100: the D-097 wording classes;
  - D-101: Fornax Sérsic;
  - D-102: Tollerud windows (known issue #156) and Tucana V;
  - D-103: KiDS isolation limit;
  - D-104: lens H0, black holes and profiles;
  - D-105: X-COP part B open items.
- **Site:**
  - the exclusion register is shown on system pages (#152);
  - excluded dwarfs keep their values on their pages (#167).
- **Correspondence:**
  - Lelli replied; the check of the four points is on #8.
  - van der Marel replied (no records; D-046 stands).
  - The Tollerud velocity-window query is drafted (`10_Tollerud_velocity_windows_v1`) for JvH to send.
  - **`03c` to Eckert and Ettori is due Friday 6 November** if they haven't replied.
- **Next:**
  1. the X-COP conversion result;
  2. site work (step F): uncertainty sections, the reproduction ledger, and a "Status and what's next" panel, which needs a ruling;
  3. the audit (step G);
  4. release checks and the v0.2 tag (JvH tags).
- **Display follow-ups after v0.2:** quotes stored with LaTeX (`\citet`, `~`) show raw on the pages for excluded systems. Cleaning them up must keep the frozen page checks working.
- **Outside the Atlas:** the "material resistance" side quest stays out of this project (JvH, 2026-11-04).

## Open on 2026-11-04 (work plan day)

- **Step A done** (#138): dwarfs, globular clusters and lenses, two readers each, adjudicated at source. Known issues opened: #139 (lens θ_E error axis; D-064 item 4 contradicted by the sources), #140 (plotted data the sources set aside), #141 (Phoenix II σ).
- **Standard 2.4.0** (#142): frozen 2026-11-04 under D-093, without the bound on g_bar. D-094 corrects D-064 item 4. The two working rules ("build for what ships", "review in proportion") are proposed in D-093 and await JvH's confirmation.
- **D-092** (#137): A644 shown with a neutral note; known issue #136. The `03c` email to Eckert goes before X-COP v2 is public.
- **Pal 1 notice (D-086): sent 2026-11-04** by JvH to R. van der Marel (marel@stsci.edu), about the McLaughlin & van der Marel (2005) table; draft `08_vanderMarel_Pal1_v2`. **Reply 2026-11-04:** the work was led by D. McLaughlin, who has left astronomy; no records remain; the Atlas may take whatever approach it thinks best. No value is confirmed, so D-046 stands unchanged (Pal 1 recorded, not plotted; the Atlas does not substitute its own recomputed 0.035 pc). The notice requirement is met. McLaughlin was not copied (no confirmed current address). Baumgardt's database is not flagged; a courtesy note can go with v0.2. Merged today: #137, #138, #142 (standard 2.4.0 frozen; D-093, D-094) and #143 (dataset pages list GitHub known issues).
- **Next (session 2 of the road to v0.2):** frozen v2 tests for KiDS, dwarfs, globular clusters and lenses (step D), and X-COP part B. D-064 item 4 is already corrected by D-094.

## Open on 2026-11-03 (evening)

- **X-COP v2 test part A: frozen (#128, #131) and run.** Result: `data/packages/aeg-d-xcop/v2/REPRODUCTION_RESULT_PART_A.md`, confirmed by an independent recomputation. A1, A2, A3's stage-2 condition, A4 and A8 stage 1 fail; A6 is undetermined.
  - A1 fails on the test's own error: it said 21 rows per file; the files hold 19–27 (109 in all).
  - A2: four clusters' GBAR is the Einasto gas plus M_STAR at R_OUT to 0.1 %; A644's is not.
  - Stage 2 (#129) is blocked by A3 (coarse inner grid; gas part fails with A2) and by A3158's negative masses.
  - D-091: the result stands, with an erratum; nothing is re-scored. The six questions go to Eckert and Ettori now (draft for JvH); the next test is built from their answers.
- **Next:** standard 2.4.0 (step B), then Part B of the X-COP v2 test; the reproduction ledger on the site gets the part A result with Part B.
- **Still to do in step A:** dwarfs, globular clusters, lenses (two readers each); draft `08_Baumgardt_GC` (required before v0.2); refresh the send list (Ghizzardi email cancelled; Eckert reply and Lelli forward sent 2026-11-03); read the audit beacon pulse.

## Earlier list for 2026-11-03 (set 2026-11-02 20:18; items 1 and 3 done, 2 cancelled)

1. **Merge the overnight PRs** (only on JvH's "merge N"):
   - #122: this guide;
   - #123: the X-COP reading;
   - #125: the D-088 correction note on the X-COP v1 page, which goes live on merge.
2. ~~**Send the Ghizzardi email** after #125 is live.~~ Cancelled 2026-11-03: superseded by D-089.
   - Draft: Dropbox `Drafts/09_Ghizzardi_XCOP_stars_v1.md`.
   - To simona.ghizzardi@inaf.it, cc Dominique.Eckert@unige.ch.
   - Change "earlier today" to "yesterday".
   - Then record the send date on #124 and in the send list.
3. **Refresh the send list** in Dropbox. Mark sent: Lelli, Eckert/Ettori and Brouwer (all 2026-11-02), and Ghizzardi (the 3rd). Add the Ghizzardi email as required under D-086.
4. **Continue step A:** read the dwarf galaxies, then the globular clusters, then the lenses, with two independent readers each, as for X-COP.
5. **Draft `08_Baumgardt_GC`** (Pal 1). It is required before v0.2.
6. **Audit seed:** read the NIST beacon pulse at or after 2026-11-03T00:46:17Z, in Chrome, and record it. Nothing is drawn until after WP2.

## Done 2026-11-02: patterns plan, validation plan, emails sent (PRs #113–#121 merged)

- **Rulings:**
  - D-085: patterns plan. P1–P3 now; P4 and P5 deferred. The P2/P3 criteria are frozen in `docs/patterns/P2_P3_CRITERIA.md`. The pattern pages are built after WP2 and WP3.
  - D-086: authors are notified before a release flags their data.
  - D-087: the #110 substitution rule for `model_dependence`, applied through the v2 packages.
- **The plan to finish validation:** `docs/plans/VALIDATION_COMPLETION_PLAN.md` (#117). Steps:
  - A: readings;
  - B: standard 2.4.0;
  - C: #110;
  - D: the frozen v2 tests;
  - E: conversions, in the order KiDS, X-COP, dwarfs, GC, lenses;
  - F: site;
  - G: audit.
- **Step A:**
  - **KiDS reading done** (#118, `docs/sources/uncertainty-readings.md` §1). The key finding is K2: the paper adds 0.1 dex to every RAR error bar for the ΔΣ-to-g_obs conversion (§4.4). The release and v1 omit it, and the site now says so (#121).
  - **g_bar is the binning coordinate**, so it has no point error by construction. Standard 2.4.0 needs a way to say that.
  - **X-COP reading done** (#123): two independent readers, adjudicated at source, 35 terms. Finding F1: the released stellar profiles are projected, and v1 treats them as spherical. This is the Atlas's error, handled under D-088 (#124, #125): v1's stellar values are upper bounds, and v2 corrects only from data that determine the correction.
- **Emails sent by JvH on 2026-11-02:**
  - Lelli (cc McGaugh, Schombert): SPARC, #8 and #9.
  - Eckert (cc Ettori): X-COP, #19.
  - Brouwer: KiDS, #64.

  All three are recorded on their issues. The drafts are in Dropbox `07 AEG/05 Correspondence/Drafts/`: Lelli v5, Eckert/Ettori v6, Brouwer v5. The send list `00_SEND_LIST_2026-11-02b.md` predates the last two sends.
  - **Still required before v0.2:** Baumgardt (Pal 1), to be drafted after step A.
- **Site:**
  - A failed test is now labelled "Not fully reproduced, on record" (#119).
  - The X-COP result has a dated correction note (#120).
  - The KiDS page has an error-bar note (#121).
  - Issues #8 and #19 were rewritten with links and neutral wording.
- **Lesson:** a Cloudflare preview build failed once with no reproducible cause. An empty re-push fixed it.
- **Next:**
  2. Read the dwarfs, globular clusters and lenses (step A).
  3. Draft `08_Baumgardt_GC`.
  4. Standard 2.4.0.
- **Audit seed:** the first NIST beacon pulse at or after 2026-11-03T00:46:17Z. Read it any time after; the audit runs after WP2.

## Done 2026-11-01 (evening): review readiness, WP1 fidelity (PRs #99–#105 merged; #106 open)

- **D-080:** new datasets frozen; fidelity first. Plan: `docs/plans/REVIEW_READINESS_PLAN.md` (WP1–WP7).
- **#8 SPARC:** the archival CDS tables equal the served tables (#100). The four points are unexplained, and the question is in the courtesy note.
- **#19 X-COP:** A2029 = Ghirardini et al. 2019 / Eckert et al. 2019 values; A2319 = Ghirardini et al. 2018 adopted values; A644 not found (#101).
- **#9 SPARC licence:** the CDS record's `rights_uri` and VizieR's general usage rules are recorded. The licence page is unreachable (CDS hosts are down from the workspace and from Chrome), so #9 stays open.
- **Audit plan frozen:** D-081, corrected by D-082 (v2: six packages, 254 rows; `docs/audit/AUDIT_PLAN_v2.md`, `sample_v2.py`).
  - **Seed:** the first NIST Beacon v2 (chain 2) pulse with timeStamp ≥ 2026-11-03T00:46:17Z (24 h after the #103 merge commit `1fbd47b`); drand as fallback. Read it in Chrome; the workspace cannot reach the beacon.
  - The audit runs after WP1 and WP2. No seed has been read and no sample drawn.
- **Site:**
  - `/reproduction/` page from `data/reproduction.json`; the build verifies the test hashes (#104);
  - SPARC "authors' selection" view; the build asserts 2 694 (#105).
- **Correspondence (Dropbox `07 AEG/05 Correspondence/Drafts/`, JvH sends):**
  - `01_Lelli_SPARC_v3.md`: JvH sends 2026-11-02.
  - `03_Eckert_Ettori_XCOP_v4.md`: questions 3 and 4 are data requests, JvH decides.
  - Tell Claude the send dates, so that issues #8 and #19 record them.
- **WP2 error budget.**
  - Ruled: D-083 (three-scale model, two phases; v2 values must equal v1 bit for bit) and D-084 (re-issued packages meet the current standard in full).
  - Data standards 2.2.0 (uncertainty scales, `uncertainty_terms.ecsv`) and 2.3.0 (`v_circ_component`).
  - **`aeg-d-sparc/v2` shipped (#111).** Its test passes, with an independent second reading of 32 269 values and 0 disagreements.
  - The site uses the latest version per dataset; v1 is marked superseded.
  - Issue #110: one rule for `model_dependence` across all datasets.
- **Next:**
  1. Phase-1 site display: point-scale error bars, the whole-system shift view (registry formulas), and uncertainty terms shown on dataset and system pages.
  2. KiDS-1000 v2: read Brouwer et al. 2021 for the ±0.2 dex stellar-mass systematic; it probably needs a 2.x minor version for its released g_bar.
  3. Then X-COP, dwarfs, globular clusters and lenses v2.
- **Sources offline:** astroweb.case.edu and CDS are unreachable from the workspace. Hash-identical GitHub copies of the SPARC files are acceptable for local builds; CI fetches the canonical URLs.

## Done 2026-10-31 (evening): A6 and A9 searches, rules frozen, A9 route chosen. PRs #88–#90 merged, #92 open

- **Accessibility first pass (#88, merged).** Report: `docs/reviews/2026-10-31-accessibility-pass-1.md`. Four findings remain open:
  1. keyboard selection of map points;
  2. the ends of the colour ramp in the light theme;
  3. translucent single points;
  4. the map payload (about 540 kB gzipped).
- **A6 strong lensing (#89, merged).** Search log A6, screening (E 21, E-pair 28, P 2, X 21). D-063 (eight rules), D-064 (project the baryons: G·M/R_E², "projected", own mark), D-065 (precedence frozen, `data/frozen/a6s-precedence.json`).
- **A9 clusters (#90, merged).**
  - Search log A9, screening (E 28, E-pair 33).
  - Epoch cut z < 0.30 (D-066); joint fits and stacks (D-067); measured stars, issue #91 for X-COP modelled stars (D-068); no summing of member catalogues (D-069); RXC1825/A1644/A2255/A3158/A3266 plan (D-070).
  - Printed luminosity × registered ratio counts as measured (D-071). Round L screened (`docs/sources/screening-L9/`, E 14).
  - Round L rules QL1–QL6 (D-072); A9 precedence frozen (D-073, `data/frozen/a9-precedence.json`).
  - Coverage v3: 116 of 319 clusters below z = 0.30 have measured stars; 79 can be paired with an observed side.
- **A9 gas coherence (#92, open).** No programme supplies an observed side, stars and gas density profiles for the same clusters. D-074 sets the A9 route:
  - case studies: A85, A2142 and ZwCl 1215 (dynamics plus X-COP baryons); A1689, A1835, A2390 and MS 1455+22 (lensing); Coma (both);
  - a LoCuSS one-radius layer at r500,WL, with two scoped rule changes: a 3D NFW-fit lensing mass, and projected stars as an upper bound. Its spec is to be frozen before any table is opened;
  - a CHEX-MATE watch and a funnel page.

## Done 2026-11-01: A6 strong lensing shipped (PRs #93, #94, #95)

- **Package and site.** `aeg-d-strong-lensing/v1` is live on the map and on lens pages: 94 plotted lenses, 212 recorded (CHANGELOG).
- **Rulings.** D-075 and D-076; data standard 2.1.0.
- **Lessons.**
  - In a git worktree, run the pipeline with `PYTHONPATH=<worktree>/pipeline`; the installed `aeg` points at /home/claude/atlas.
  - Never let a build agent add a passing outcome to a frozen test; check every test change.
  - Tell JvH before long background runs: a stop pressed from the phone kills subagents.

## Start here next

0. **v0.1 released (D-077):** pre-release, Zenodo DOI 10.5281/zenodo.23864356 (all versions 10.5281/zenodo.23864355). Competing interests are stated (D-078). Next: the review-readiness plan (awaiting JvH's answers: freeze new datasets, author contact, order).
1. **A6 packaging (done)** in the worktree `../atlas-a6`, branch `data/a6-strong-lensing`, to the frozen A6 rule:
   1. a source list and licences;
   2. REPRODUCTION.md frozen before conversion;
   3. two-reader input reading;
   4. tests 1–3.
2. **A9 X-COP case studies:** A85, A2142, ZwCl 1215. The baryons are already in `aeg-d-xcop`; the caustic profiles come from the SAO team.
3. **LoCuSS spec** (D-074 item 3): write it and freeze it, then package.
4. **Remaining case studies, then the funnel page;** tag v0.2 after A6 and v0.3 with the cluster layers.
5. **Still open from before:** #24 (A5 D-037 check); #23 (A3 R39, R83); SPARC #9 (CDS licence); accessibility findings 1–4; Zenodo switch-on (JvH); author data requests on hold (JvH).

## Done 2026-10-31 (earlier): A5 dwarf galaxies complete and on the site, PRs #82–#86 and this one

- **Package `aeg-d-dwarfs/v1` (#82, #83).** 65 systems; 64 plotted as one value each at the 3D half-light radius (one, And XII, as an upper limit under D-062); And XIII recorded, not plotted. 586 observables.
  - Gas (D-058): Putman 2021 HI rescaled to the package distance by (D_pkg/D_Putman)², helium 1.33, half inside r½.
  - Metallicity (D-059): read at source twice; the dispersion paper's value as a flagged fallback.
  - Υ_V (D-060): an envelope from the McLaughlin & van der Marel 2005 model tables; slider `dw_stellar_ml`.
  - Inputs (D-061, D-062): Boötes III, Muñoz 2018 magnitudes, Leo I, Phoenix, Leo T, Tucana V, And XII, Pegasus IV.
- **Tests.** 1: 534 of 534 numbers found as printed (after disclosed script fixes); 2: 554 of 554; 3: pass; 4: pass.
- **D-050 version of record and errata (#84).** All plotted values agree with the version of record; two errata found, neither changes a value.
- **Site (#85).** Dwarfs on the map (own colour, upper-limit marks), system pages with status, flag explanations and inputs.
- **Magnitude errors (#86).** Printed m_V,0 errors carried into g_bar; values unchanged.
- **D-038 3A consistency check (this branch).** Frozen before it was run: 13 pairs, none beyond 2σ, median z −0.03. Consistent. Reported in `SECOND_READING.md`.
- **#64 (this branch).** The KiDS dataset page says the `no_uncertainty` flag refers to g_bar only. The flag itself is renamed in the 2.0.0 re-issue.

## Where things stand

- **Repository** `github.com/extragravitation/atlas`, `main` protected (pull request plus required checks `checks` and `packages`). Preview site live at https://extragravitation.org (pre-release banner, not indexed).
- **Protocol** frozen and deposited on Zenodo: DOI 10.5281/zenodo.23780203. Data-freeze date 2026-12-24.
- **Frozen by hash** (`python -m aeg.check`): all files in `data/frozen/` (including the A6 and A9 precedence rules, D-065 and D-073), D-036 to D-073 where a method was frozen, and data standard 2.0.0.
- **Packages:** SPARC, KiDS-1000, X-COP v1 (standard 1.x); `aeg-d-gc-baumgardt/v1` and `aeg-d-dwarfs/v1` (2.0.0).
- **Release v1.0 (#16): not clear.** Open gates: every cell filled (#48), the data freeze, neutrality and outside review, accessibility (#14), the SPARC licence (#9), Zenodo, the release changelog.
- **For the outside reader at v1.0:** D-046, D-049, D-049a, D-051, and the Simon 2019 differences logged under D-053.
- **Open issues:** #8, #9, #13, #14, #16, #19, #21, #23, #24, #48, #64, #91.

## Working notes

- **Commits** are authored by JvH (his name and GitHub no-reply address), never his email. The stop hook asks to re-author commits as Claude; this is declined every time on JvH's instruction. Protected history is never rewritten.
- **Network.** The workspace reaches arxiv.org, iopscience PDFs (retry on 403), GitHub and Dropbox. It cannot reach CDS, aanda.org, OUP or Zenodo; OUP works in JvH's Chrome. VizieR Harvard is flaky; the IDIA mirror works. Use `git fetch origin main` then `FETCH_HEAD`, never `origin/main`.
- **ADS** works in JvH's signed-in Chrome (unquoted bibcode queries, chunks of about 60). Never extract its token.
- **Readings.** Agents do them under committed briefs. Every brief and script is committed before the data it processes is seen; any later fix keeps the earlier output on record.
- **JvH's computer link** is often offline; Dropbox works from any computer. Email drafts and private actions stay in Dropbox.
