# Independent review of the globular-cluster v2 test, revision 2 (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

**Freeze review: GC v2 reproduction test, revision 2 (`test/gc-v2` @ 0fb537d)**

## Bottom line

**Do not freeze yet.** Revision 2 fixes all eight must-fix items from review 1 and applies D-098 correctly:
- M54 is the only value change, under D-096 rule 2.
- NGC 2298 and Pal 5 are D-097 findings. Their rows and values are kept, and only their plotting changes.
- The three classes and the "sources that count" rule follow D-098.

Five problems remain. Each would make a test item fail or be undecidable as written. All five are text fixes that need no new ruling. The test has no cause-assuming language (no dark matter, modified gravity, halo or "mass discrepancy"). `python -m aeg.check` passes on the branch.

## Errors (must fix)

1. **Item 2's list of allowed changes is incomplete, so item 2 would fail (l. 54–61).**
   - **`role` and `alternative_of`.** In v1's `convert.py`, a row is `default` only if it is plotted: `is_default = (s.default is c and s.plotted)`. All 15 unplotted v1 rows are `alternative`, including 7 that are their system's only candidate. Under that convention, NGC 2298 (m000009), Pal 5 (m000078) and M54 (m000067, if it fails coverage) would become `alternative`, and item 2 does not allow that.
     - Fix: state the expected `role` for these rows and add `role`/`alternative_of` to the exceptions.
   - **`flags` and `notes`.** l. 94 adds the flag `no_uncertainty` and a note naming the column. Neither is in the exception list. Add both, or drop l. 94.
   - **Item 6's columns.** l. 61 allows new columns from items 5, 7 and 9 only, which leaves out item 6's size columns. Add item 6.
   - **Which tables item 2 covers is not said.**
     - The systems `properties` field will change: `status`, `reasons_not_plotted` and `candidates` (M54's `coverage`, `n_bins`, `sigma_rms_km_s`), plus the new `ebv_mag`.
     - The observables table gains the `err_level` columns and new `apparent_magnitude` rows.
     - Fix: name the tables item 2 covers and list the expected changes in each. Require new observables to be appended after `o003182`, so that v1's observable IDs differ only in the prefix. Say whether the V_t observable goes into `baryonic_from`.

2. **E(B−V) stored in `properties` cannot reach the reddening formula (l. 154 vs l. 112, 133).** The formula language resolves only `p`, `p0`, row columns and `system.<column>` (`pipeline/aeg/formula.py` docstring); it cannot read JSON properties.
   - Fix: store E(B−V) as a systems column, for example `x_gc_baumgardt_ebv_mag`. There is precedent: v1's `gc_stellar_ml` formulas already use `x_gc_baumgardt_ml_v_salpeter`.

3. **The registry update in item 7 cannot be represented, and the validator would fail (l. 99, 132–136).**
   - **One formula per cause won't fit.** Registry effects are stored per assumption per dataset version, as `datasets["aeg-d-gc-baumgardt/v2"].effects`: a list of `{column, formula}` with one parameter `p` and no term key.
     - `gc_distance_hb` cannot hold the calibration formula (g_obs ∝ D⁻¹) and the reddening formula (g_obs ∝ D⁻¹, g_bar ∝ D⁻²) at once.
     - `gc_rhalf_wolf` has the same problem for R_h, deprojection, anisotropy and normalisation.
     - So "an effects formula for the term" cannot be checked mechanically.
   - **The defaults are text.** The current defaults are `"harris2010"` and `"4/3"`, so `p0` is unusable. `formula_check` also requires every formula to leave values unchanged at the default.
   - **Fix:** use one assumption per distinct formula (for example `gc_distance_hb` for the calibration terms and a new `gc_reddening` for reddening and R_V), each with a numeric parameter that defaults to 0. Alternatively, define a `term_id` key on effects.
   - **The other row assumptions need v2 entries.** Every assumption on the rows (`gc_equilibrium`, `gc_light_model`, `gc_gas_absent` as well as the changed ones) needs an `aeg-d-gc-baumgardt/v2` entry. Otherwise validate.py reports "assumption … not in the registry for dataset/version". Replace "a new version of each changed entry" with "every gc_* entry gains a v2 dataset entry".

4. **The order of work conflicts with D-098 (l. 43 vs l. 45 and l. 49).**
   - If the second reader disagrees on NGC 2298, Pal 5 or M54, D-098 still cannot be reversed.
   - But `convert.py` applies changes and exclusions "only from the frozen reading files", and items 3 and 8 define changed and excluded rows from those files. That leaves two sources that can disagree.
   - Fix: the reading files record D-098's three outcomes as ruled inputs, and the reader's dissent goes in `resolutions.md`.

5. **Item 11's pass rule cannot be applied mechanically (l. 163).** "Disagreements are resolved at source … one resolved against the package is a fail" describes a resolution step after conversion. But all resolution happens, and is frozen, before conversion.
   - Fix: "the package equals the frozen reading files field by field; any mismatch is a fail."
   - Also name the file that holds the binary-screening values (l. 42 and l. 150).

## Weaknesses (should fix)

- **`pop_synthesis_code` (l. 118).** MvdM l. 1358–1359 reads: "although there are some exceptions, these differences are generally slight: … ≲10% in Υ_V". With "generally" and "exceptions", this is not an upper bound. Use `as_released`, quote the hedge, and correct the locator to l. 1358–1359.
- **`anisotropy_profile` (l. 121).** Wolf l. 963–976 gives 0.05 dex "in cases where extended kinematics are not available". It comes from the dEs and Es, and is offered "to allow for a range of β profiles". The note's "for dispersion-supported systems in general" misdescribes it. These rows have at least 80% light coverage, so the condition arguably does not apply. Either state the condition or use `not_given_by_source`.
- **`deprojection_4_3` (l. 122) has no locator.** Use Wolf l. 1814–1818 ("better than 2% accuracy for 0.30 ≤ c_k ≤ 3.00") and l. 1829.
- **`distance_hb_*` are labelled `one_sigma` (l. 109–111).** Harris does not say what its ± means. `reddening` uses `as_released` for exactly that reason; be consistent.
- **`ml_population` has scale `system` (l. 117).** The term also contains a dataset-scale age part (F6). The note says so, but the result should flag the label as a simplification.
- **`stellar_ml` is a `range` with one `size_column` (l. 119).** The column holds only the upper end. State how the lower end (0.53 × Υ_V) is to be read.
- **l. 95 reads the frozen standard by interpretation (§12 vs §7a).** That needs a one-line ruling from JvH or a deviation entry. Precedent: v1's slider formulas already use extension columns.
- **D-098 rule 3 counts distance originals, but the test reads only the Harris compilation (l. 33, 178).** That applies the ruled rule only in part. Get JvH's OK, or log a deviation, before freezing.
- **Harris's calibration includes dynamical parallaxes** (Harris l. 70, l. 125–127). If D-036 #6 were later ruled to apply, plotting would change, and a frozen test could not absorb that. Get a ruling before freezing, or state that it would apply only from v3.
- **Item 8, l. 147 needs site work.** No site code reads `data/registry/excluded.csv`, and the file does not exist on main. Name the site change, and make the check mechanical (search the built HTML for the quotation).
- **BSH20 provenance.** BSH20's values enter a data column (`vt_scatter_mag`), so require it in `v2/sources.json` with its hash and licence.
- **Missing locators:**
  - F13: 1304.4176, l. 352;
  - D21: 2105.02246, l. 418;
  - MvdM Wilson models: l. 2704–2705.
- **Item 12's command.** Write it as `python -m aeg.validate data/packages/aeg-d-gc-baumgardt/v2`; the bare command only prints usage.
- **M54's 269.01″ bin may also hold stars inside 200″,** since only ⟨r⟩ is stored. The known issue names only the 170.92″ bin.

## Notes

- **Quotes checked at source, all exact:**
  - B17 l. 586–589;
  - BH18 l. 185, 199, 203–204, 206, 226–227, 228–233, and the Table 3 caption ("$1\sigma$ upper and lower error bars");
  - K18 l. 282, 330, 344;
  - D21 l. 418;
  - F13 l. 352;
  - L13 l. 489;
  - Harris l. 94, 148, 152, 125;
  - MvdM l. 1212, 2187–2190, and Fig. 4's "∼30%";
  - Wolf l. 927, 974;
  - BSH20 l. 254, 257 (caption), 266;
  - the MvdM VOT fields: "The 1{sigma} error in BC/ChD" and "Upper/Lower 1{sigma} error in WO/r0".
- **Facts checked against v1 at commit 5dc4091:**
  - v1 is unchanged on main since that commit.
  - It has 79 rows: 71 RV, 4 L13, and one each for K18, F13, D21 and L15. 64 are plotted.
  - Every row is `observable_form` and flagged `edges_inferred`.
  - M54 has 16 RV bins; the outer three are at 269.01″, 410.12″ and 679.1″.
  - NGC 2298 and Pal 5 are plotted, with 2 bins each.
- **Review 1's items:**
  - All 8 must-fix items are fixed.
  - The should-fix items are addressed, except that the §12 question is answered by interpretation, not by a ruling.
- **Branch housekeeping:** the branch predates D-098 on main, so its `docs/decisions.md` lacks D-098. Rebase before merging.
- **Data I saw:** v1 bin radii, coverage, plotted flags and roles, and the σ_rms values printed inside the systems `properties` for M54, NGC 2298 and Pal 5. I saw no g_obs or g_bar values.
- I used a temporary worktree and removed it. Nothing was pushed or modified.

**Next step:** apply fixes 1–5 in one revision, get JvH's one-line calls on the §12 reading, the Harris-originals scope and D-036 #6, then freeze.