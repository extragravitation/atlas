# Independent review of the X-COP v2 test part B, draft (2026-11-05)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Review: X-COP v2 test, part B (`REPRODUCTION_PART_B.md`, revision 1, commit 5735935)

## Bottom line

**Do not freeze it yet.** The structure is sound and close to the other v2 tests, but there are eight must-fix errors. Three of them conflict with frozen or ruled text:
- **`mass_model_choice` (E1):** it keeps only the smallest of part A's A7 ratios. That is a selection made after seeing the data.
- **`x_value_change_ruling` (E2):** item 10 leaves it unset, which contradicts part A §1, D-093 rule 5 and standard §9.
- **Consent gate (E3):** it leaves out D-090 rule 5's preview link for the authors.

The fixes are wording and rule changes. None needs new data. One more review after revision 2 should be enough.

The reviewed draft is at commit 5735935 on `test/xcop-v2-part-b`. Line numbers below refer to `/home/claude/atlas/data/packages/aeg-d-xcop/v2/REPRODUCTION_PART_B.md` at that commit.

**What I checked:**
- part A's frozen text and its published result, with the D-091 erratum;
- decisions D-025, D-070 and D-086 to D-104;
- data standard 2.5.1, `validate.py`, `site/src/lib/atlas.mjs`, `site_check.py`, the CI workflows and `data/assumptions.json`;
- the X-COP readings (§3, §3b, §3c, and reader A and B);
- quotes against the cached e-prints: E22 `hydromass.tex`, Loubser 2020, Ghizzardi 2021, Paper II and Ettori & Eckert 2022.

I computed no v2 value. My temporary worktree has been removed.

## Errors (must fix)

**E1. The `mass_model_choice` size drops part of what part A fixed (l. 94, l. 110, O2).**
- **The problem:**
  - Part A l. 197–202 says to report "each pair" of three masses: non-parametric, Einasto and Table 1's NFW M500. It then says "These ratios become the system-scale term."
  - The result (l. 114) publishes all of them:
    - non-parametric / Einasto: 0.97–1.04;
    - non-parametric / NFW: 0.80–1.15;
    - Einasto / NFW: 0.78–1.10.
  - Part B uses only |non-parametric/Einasto − 1|, which runs from 0.006 to 0.042. That drops the NFW comparisons, where A644 differs by about 20 %. Choosing the smallest subset after the results are public is re-scoring by selection.
  - The readings, written before any data were seen, also name the term as "Einasto against NFW against non-parametric" (§3b, consequence 3).
- **Fix:**
  - Carry all three published ratios per cluster as systems columns.
  - Fix the size by a rule stated now that does not depend on outcome, for example the largest |ratio − 1| across part A's pairs. Note that the NFW pairs were evaluated at Table 1's R500, as the result says.
- **Also:** `status = given` means "size read at source" (§7a), and an Atlas computation is not that. The O2 ruling must say so explicitly.

**E2. `x_value_change_ruling` is not set (l. 150).**
- Part A §1 l. 29 says "Part B carries it into the automated check by that rule, not by an ad hoc override."
- D-093 rule 5 created `x_value_change_ruling` for exactly this case: "a ruled exception to §10 item 13 (X-COP v2, D-090 rule 1)".
- Standard §9 says that when the key is set, the dataset page "states the ruling and that the values differ".
- v2's values do differ from v1's. KiDS correctly left the key unset only because its values do not change.
- **Fix:**
  - Set `x_value_change_ruling` = `D-090`. D-090 has a `**Ruling (` line, so it passes validator item 18.
  - Add to item 10 or item 12 that the v2 dataset page states the ruling and that the values differ.

**E3. The consent gate leaves out D-090 rule 5's preview (l. 44–49).**
- **What is missing:**
  - D-090 rule 5 says "the authors are offered a preview link before it goes live", and that one follow-up is sent after 4 weeks with no answer. Neither appears in part B.
  - Item 12 runs the site checks with v2's tables present locally. `atlas.mjs` (l. 38, l. 72) then makes v2 the current version and marks v1 as superseded. So item 12's last bullet, the sentence on v1's page, is checked on a build that is not the deployed one.
  - The site skips any package version without `tables/measurements.ecsv` (l. 38). So "generated from v2's descriptor" needs new site code that reads a version with no tables. The test does not name that change.
- **Fix:**
  - **Two builds in item 12:**
    - Build 1, with the tables: validator, `site_check`, and v2's own pages.
    - Build 2, with no tables, as deployed: v1 stays current and shows the rule 5 sentence; `git ls-files` is empty.
  - **Preview step:**
    - State how the authors' preview is produced and served without committing or pushing the tables. A table pushed to a branch, or built into the per-pull-request preview, is publication.
    - State the 4-week follow-up.
  - **Site change:** name the site change as part of the conversion pull request.

**E4. The registry assumptions "as in v1" do not exist (l. 97, l. 129 "New entries: none").**
- v1 is standard 1.2.1. Its `assumptions` column holds only `xray_hse_bias=0;icl_fraction=0`.
- `assumptions.json` has no X-COP entry for spherical symmetry or hydrostatic equilibrium.
- A 2.x package must list every inference step (D-029 2b), and the validator requires each listed id to have an `aeg-d-xcop/v2` entry.
- **Fix:** name the new entries, for example `xcop_hse_equilibrium` and `xcop_spherical`, each read at source with its locator. Remove "as in v1".

**E5. `hse_bias` (l. 106) misstates the source's bound in two ways.**
- **A2319 is excluded by the source's own sentence.**
  - E22 l. 502 says "with the exception of a single system that is known to be strongly biased (A2319) … we conclude that our measurements are mildly biased (<10 %) out to R500".
  - So `applies_to` for the 0.10 bound must be the other four clusters: `aeg-s-000177;aeg-s-000179;aeg-s-000180;aeg-s-000181`.
  - A2319 needs its own `not_given_by_source` row, with the quotes.
- **The bound holds only out to R500.**
  - The released rows reach 1.24–2.11 × R500 (part A result, A3).
  - The source says the hydrostatic assumption is "likely to be a poorer approximation beyond this point", and gives 10–20 % at R200 (l. 539).
  - A single dataset-scale ≤ 0.10 then states something the source does not say for rows beyond R500.
- **Fix:** state in the term, and on the page, that the bound applies to r ≤ R500, naming which R500. Beyond that radius, show the l. 539 figure in the note, or use a measurements `size_column` filled only where r ≤ R500.

**E6. Part A §5's "recorded on every row" is not carried out for the centroid shift (l. 144, l. 88).**
- Part A l. 259–260 puts w and its error on every row.
- Part B moves them to the systems table only, while l. 8 says part B "carries out" §5.
- **Fix:** add `x_xcop_centroid_w` and `x_xcop_centroid_w_err` to the measurement rows as well, or get a ruling that a column joined by `system_id` meets "every row".

**E7. Wrong or missing locators and names (l. 105, l. 122, l. 115).**
- **`reconstruction_bias`:** "follows the true profile with minimal bias (<5\%)" is at E22 **l. 309**, not l. 311. Reader A gives L309 and L311 together.
- **`satellite_imf`:** the Ghizzardi quote has no locator; it is `xcop-metallicity.tex` l. 923. It is not about the IMF. Its sentence begins "Although we lack a clear understanding for the origin of different estimates of M_star". Rename it, for example `satellite_mass_systematic`.
  - Ghizzardi also gives the Salpeter factor as "∼ 1.74" (l. 926), while reader A quotes "factor ∼2". The note should give both, with their lines.
- **`bcg_dm_component`:** the term_id is an Atlas label that uses "DM" (project rule 8). Rename it, for example `bcg_ml_extra_mass_model`, and keep the source's wording inside the quote only.

**E8. R500 is hard-coded while rule 1 leaves it to the reading (l. 89 against l. 33).**
- Rule 1 says "Which R500 the source uses for that range is read at source".
- Item 6 fixes `x_xcop_r500_tot_kpc` as Table 1's R500,TOT.
- **Fix:** make the column hold the R500 the reading names, or drop it. `properties` already holds Table 1.

## Weaknesses (should fix)

**Not mechanically decidable:**
- l. 42: "if the reading finds at source that the released GOBS is the Einasto curve" needs a criterion, such as an explicit statement in a FITS header or a source line. Without one it becomes a judgement made at conversion.
- l. 115: "the reading confirms the systems" says nothing about what happens if it does not. E22 l. 109's "8.3 ± 2.9 per cent on average" is ambiguous: it may describe all the BCGs or only A644 and A2319.
- l. 142: "the hydrostatic-validity quotation" is singular, but `hse_statements.csv` will hold several. Fix it as all A2319 statements, in file order.
- l. 81, error form:
  - Reading the pair as bounds should require GOBS_ERR_LO < GOBS < GOBS_ERR_HI on every row, not only the HI condition.
  - The authors' question 6 should also ask what the error columns mean, not only their confidence level.

**Sizing rule applied unevenly:**
- `reconstruction_bias` (≤ 5 %) comes from a mock cluster, not from these clusters.
- `xmm_calibration` (15 %) is a figure E22 cites from Schellenberger 2015. Both are `given`.
- The lens test moved comparable figures (R9's 0.5 %) to the note.
- Either justify these two explicitly or move them to the note.
- `xmm_calibration` with `as_released` also misdescribes a one-sided, conditional shift (l. 506: "if the Chandra temperatures are correct").
- `given_by_other_source` is defined as "a cited independent source"; papers from the same programme are not independent. Say why the label is used.
- `satellite_mass_systematic`, at up to 60 %, is Ghizzardi's statement about Ghizzardi's own masses. A9 shows the shared files hold about twice those masses. Say in the note that the size's applicability to GBAR is therefore unclear.

**Contradiction with §2a rule 4:** `hse_validity_outskirts` (l. 111) is the hydrostatic assumption, which l. 97 itself says is a registry assumption. Fold it into the `hse_bias` note or into the new registry entry.

**Steps (l. 135–136):**
- `xray` and `deprojection` are taken from other tracers' ladders.
- `stellar_ml` and `newtonian_g` are marked as Atlas steps, but here the source performed them.
- The validator passes them, but the meaning is wrong. Use the hot-gas ladder in its order (`events;spectra;projected_t_and_density;deprojected_profiles;hydrostatic_mass;newtonian_g`), and say in `source_ref` that the source computed g.

**Units of α (l. 58, l. 88):** the per-cent unit is an inference (§3c). Record the value as printed, with a unit status, in `properties.csv`. Do not divide by 100 silently.

**`properties.status` (l. 138):** `plotted` and `recorded_not_plotted` are Atlas states, not "source-given properties" (§5). Use an extension column, or rely on the exclusion register.

**`xray_hse_bias` v2 entry (l. 126):** reusing v1's `default_ref` and `range_ref` (Eckert 2019, and 1 − b = 0.85 ± 0.05 for Planck SZ masses) cites the 2019 analysis for a 2022 package. Read the v2 range from E22 (l. 502, l. 539).

**D-096 rule 1 (l. 34):**
- The archives also release Einasto and non-parametric mass profiles, and E22 l. 458 uses both for g_obs.
- Close this explicitly by citing part A §5 ("Parametric files: used only for the checks and the uncertainty terms"), so that "no alternative rows" does not look like a choice made at conversion.

**CI and the gate:**
- `data.yml` will run v2's `convert.py` on every pull request and print `build.log` and `test.log` to logs, which are public for a public repository.
- Require that `convert.py` and any v2 tests print no row values.
- The "committed tables equal regenerated tables" step will pass trivially for the ignored tables. State which check covers determinism instead, for example `checksums.sha256` compared in CI.

**Pre-freeze mock (l. 184–187):**
- Only `validate_v22` and `validate_v24` were run.
- `validate_v2`, which checks the required systems columns (`name_in_source`, `class_in_source`, `distance_kinematic`) and the observables rules, was not.
- A full mock with a descriptor would have caught E4.

**`stars_status = measured` with no stellar component columns (l. 74):** check this against D-034's `not_separable`.

**E-numbers (l. 20, l. 91):** they are reader A's. Reader B numbers the rows differently (B's E19 and E26 are other terms). Say so.

## Notes

- **D-070:** items 2 and 3 planned measured stars for A2255, A3158 and A3266 from other sources. D-089 and D-090 rule 4 implicitly supersede this. Say so in the decision log.
- **A3158 known issue:** the new known issue for A3158 (l. 145) is a public flag under D-086. Question 5 of `03c` serves as the notice, as D-092 rule 4 does for A644. State this.
- **A2319 across datasets:** Paper II l. 80 says "clear evidence of a breakdown of hydrostatic equilibrium". Under the dwarf and globular-cluster rules (D-099 and D-100), that would be a finding. Part A §5, which is frozen, plots A2319, and D-025 is limited to dispersions, so part B is consistent. JvH should still know about the asymmetry between datasets.
- **The share links are already public:** part A l. 24–25, in the public repository, holds the archives' share URLs. Anyone can therefore already download the files. This weakens the consent gate. It is outside part B, but worth raising with JvH.
- **The outcome under O4 is already visible in the published data:** part A's result shows A1795 reaching 2.11 and A2029 1.99 × Table 1's R500.
- **Quotes that checked out at source:**
  - E22 l. 56, 91, 97, 103, 109, 111, 114, 116, 235, 263, 373, 404, 408, 410, 435, 453, 456, 458, 502, 504, 506, 508, 528 and 539;
  - Loubser 2020 l. 547;
  - Ghizzardi 2021 l. 712 and 715;
  - Paper II l. 80;
  - Ettori & Eckert 2022 l. 182, 276 and 377.
- **Values from part A and its result:** the A9 ratios, the 109-row count, the five system IDs and the A7 non-parametric/Einasto values all match.

## O1–O4

- **O1 (observables for the seven clusters): agree, none.** No row would cite them. The only g_bar would be a bound the standard cannot hold. Writing them would publish privately shared values that nothing on the site uses. This also matches D-089 rule 1.
- **O2 (`mass_model_choice`): do not adopt as drafted (see E1).**
  - Recommend an A7-derived size that uses all of part A's published pairs, by a rule fixed now, with the note saying the Atlas computed it.
  - E22's sample statement (l. 373: 3 % and 10 %) goes in the note.
  - Since `given` means "read at source", the ruling should say explicitly that this term is the one Atlas-computed exception.
- **O3 (sliders): agree.** Keep `xray_hse_bias`, with v2-specific references read from E22. Drop `icl_fraction`. The stronger reason is not only that there is no stellar column: the source gives no radial ICL profile, so any formula on the total g_bar would assume one.
- **O4 (rule 1's radial range): recommend a different default.**
  - l. 528 is a sentence from the conclusions that summarises the analysed range.
  - l. 486 says "We fitted the nonparametric points" and excludes none.
  - D-096 rule 2, with D-098 rule 1 and the D-103 precedent, needs an explicit statement that points were removed or not used.
  - Make the criterion mechanical: only explicit exclusion wording counts. On that criterion, the expected outcome is no exclusion.
  - The valid range is already with the authors (question 5). If they state one, it comes in under a new ruling.

**Next step:** revise to revision 2 with E1–E8 fixed and the O2 and O4 wording changed, run the full `validate()` on a complete mock, then send it for one independent review before JvH rules O1–O4 and it is frozen.

**Possible memory item (source: this review):** X-COP registry assumptions for v1 are only `xray_hse_bias`, `icl_fraction` and `stars_cluster_modelled`, with no equilibrium or spherical-symmetry entries. I found this in `data/assumptions.json`, not in memory.