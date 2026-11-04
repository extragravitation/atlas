# Independent review of the KiDS-1000 v2 test, draft (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Independent review of the KiDS-1000 v2 test (draft), 2026-11-04

## Bottom line

**Not ready to freeze.** The structure follows the SPARC model and the core value-identity tests (lines 26–30) are sound. But the uncertainty-terms table misstates three of the source's terms (K7, K8, K13). One row is not allowed under §7a as written (K13), and one is an assumption that §2a rule 4 says is never an uncertainty term (K14). The README hash check is pushed past the freeze, and the README is what the test is built on. The consequence of a failure is weaker than in the model test. Every fix below is to wording or table entries; none needs a new standard.

**What I checked.**
- I read every quoted location against the arXiv LaTeX `RAR_paper_Brouwer_4.tex` (SHA-256 `45aa25ab…4b19`): lines 174, 183, 313, 315, 337, 339, 368, 370, 405–421, 438, 440, 483, 489, 491, 512–514, 746 and 748. Section numbers §2.1, §3.1, §3.3, §4.3, §4.4, §5.2 and App. A all match.
- The README on the mirror hashes to `b3680580696c5dbf5671c700d5e8f90fbfd1dc614fa7e3e07b2f66d1624e8645`, which is consistent with the truncated hash in the test. I did not check it against the canonical tarball.
- I compared ESD_t between the KiDS-bright and hot-gas files. I did not compare any g_bar value with a bin edge.

## Errors (must fix)

1. **Line 3: weaker failure consequence than the model test.** SPARC v2 says "v2 does not ship and the failure is published". This draft only says the failure is published. D-005 condition 1 also says a failed package does not ship. As written, a failed v2 could still ship. Add "v2 does not ship".

2. **Line 50 (K7), and line 58: misread.**
   - The source (l. 339) subtracts the ESD profile measured around random points. The "mean absolute value of only 1.85 ± 0.75 %" describes how small that subtracted profile is. It is not "an applied 1.85 %" correction.
   - The source never calls ±0.75 % a 1σ uncertainty of the correction, so `one_sigma` is invented.
   - Fix: `status = not_given_by_source`, with a `note` quoting "1.85 ± 0.75 %" as the source's description of the subtracted profile. Also correct the reading's K7 row.

3. **Line 51 (K8): size and kind misrepresented.**
   - "0.06 … the range the source tested" is wrong. The source tested only 0.29 dex ("using the maximal estimate … does not change the conclusions", l. 368). 0.06 is the LePhare estimate, which the source implies (0.12 is "twice the LePhare estimate") but did not test.
   - 0.12 dex is a σ (σ_M⋆), so `as_released` with lo/hi mixes two kinds in one row.
   - Fix: `size_value 0.12`, `size_kind one_sigma`. Put "0.29 dex tested, conclusions unchanged" in the `note`, or use a separate `range` statement only if the standard allows it.

4. **Line 54 (K13): wrong size kind, and the row does not conform to §7a.**
   - "~30 %" is an estimate from the offset MICE simulation (l. 489, l. 748). The source does not state it as a maximum, so `upper_bound` is wrong; use `as_released`.
   - §7a (line 211 of the 2.5.0 text) says a point-scale term that is stated with a size but left out of the error columns must have `in_error_columns = no`. Empty is reserved for terms the source does not give and for rule-7 rows. The draft leaves it empty.
   - The satellite contamination also moves all low-g_bar KiDS-bright bins together, which is not point scale (§2a: independent of every other row).
   - Recommended fix: `scale = dataset`, `applies_to = *`, with a `note` naming the affected rows. This matches the §3 guidance for population bins.

5. **Line 55 (K14): an assumption listed as an uncertainty term.** The point-mass approximation (l. 405–411) is a physical or geometric assumption. §2a rule 4 says such assumptions go in the registry, never in the uncertainty-terms table. Move it to the `assumptions` column (registry entry), alongside `deproj_lensing=sis`. Drop the row, or justify it explicitly against rule 4.

6. **Line 43: refers to a row that does not exist.** "except K1's, which is `published`" — the table has no K1 row, and §7a says point-scale terms already in the error columns need none. Reword: "K1's covariance is in `tables/covariance.ecsv`; every row here has `not_published`."

7. **Lines 47–56, together with §3: terms tied to one sample are applied to all three.** With `applies_to = *` and no systems, each term reads as applying to every bin. The source says otherwise:
   - K8 (0.12 dex) and K10 (normalisation) concern KiDS-bright stellar masses. GAMA uses Taylor et al. 2011 ugrizZY masses (l. 349).
   - K13 is KiDS-bright only.
   - K7 is stated for KiDS-bright.

   Require each such row's `note` to name the samples it applies to. Add a `not_given_by_source` row for GAMA's per-lens stellar-mass scatter.

8. **Lines 78 and 81 (`x_baryon_inventory`): two entries misstate the source.**
   - "9-band photometry, normalised to GAMA" is wrong for the GAMA rows (see item 7). The stars entry should be given per sample.
   - "ionised gas, dust … `not_addressed`" is contradicted by l. 419–421, where the source explicitly discusses cool and warm (ionised) gas and dust as present but not counted. These should be `known_unmeasured`, quoting l. 419/421.

9. **Line 90: the README hash check is not decidable.**
   - The hash is truncated (`b3680580…8645`), so an exact check cannot be run against it.
   - "If it differs … any change is reported" gives no pass or fail.
   - The reading itself (§1, "Not yet done") says the check must happen *before* the test is frozen, and lines 18 and 36 rest on README quotes.
   - Fix: run the check before merging, write the full hash into the test, and make a mismatch a fail.

## Weaknesses (should fix)

10. **Line 70: the hot-gas pairing by bin index needs a stated meaning.** ESD_t differs row by row between the hot-gas and KiDS-bright files (bin 1: 0.123 vs 0.749). So the variant was re-binned on its own g_bar: bin k holds different lens radii. "Alternative_of the same bin index" is therefore a formal pairing, not "the same point with hot gas added" (even though l. 514 describes it as points shifting right).
    - The `notes` should say this.
    - D-038's `alternative_value` was defined for several measurements of one system. The precedent for this case is D-014 ("alternative baseline").
    - Changing v1's display (45 plotted rows to 30) changes what the Atlas shows. Name it to JvH as a ruling rather than infer it.

11. **Lines 40 and 70: the hot-gas bin edges are inferred.** The source states the 15 bins in general (l. 174) and never states them for the hot-gas variant. The test should say the edges for that file are the Atlas's inference.
    - The edge rule itself is correct: 15 equal log bins from 1e-15 to 5e-12, Δ = log₁₀(5000)/15 ≈ 0.2466.
    - Add a float tolerance (for example rel 1e-12) for `g_bar_bin_lo/hi`.
    - Disclose that the reading already checked that the released g_bar values fall inside these bins (§1.1), so check 5 is not blind.

12. **Line 64: the hot-gas observable needs a fuller description.** "plus nominal hot gas" should say that it is an *assumed* isothermal halo with M_gas = M⋆ within 100 h70⁻¹ kpc, "only a rough order of magnitude estimate" (l. 483, l. 512).
    - Those rows' g_bar is not "from detected baryons" (§3), so they need `gas_hot_status = modelled` (D-034) and a statement that g_bar includes an undetected component.
    - `steps = photometry` is not the last step the source performed (§4 says steps end with it). At minimum, `source_ref` must carry the mass-estimation and binning steps.

13. **Columns the test leaves open.**
    - Lines 66–70 do not fix `stars_status`, `gas_cold_status`, `gas_hot_status`, `assumptions`, `adjustable`, `method`, `channel`, `quality_source` or `notes`. A converter could change them freely.
    - Add: every v1 column not named in the test is unchanged, except `flags`, as stated. `assumptions` gains the point-mass entry (item 5).
    - Line 63's unit should be the exact astropy string (`solMass / pc2`, with h = 0.7 in the descriptor), not "h70 M☉ pc⁻²".
    - Line 86: compare at printed precision, as SPARC does. The second reading should also derive the bin edges from l. 174 independently.

14. **Lines 42 and 54: the hot-gas `source_quality_low` flags.** v1 applies the KiDS-bright limit (g_bar < 1e-13) to the hot-gas g_bar. The source sets the limit at R > 0.3 h70⁻¹ Mpc, translated with "the mean M_gal of the appropriate lens sample" (l. 748; 7.56e-14 for KiDS-bright). With hot gas added, the same radius sits at a higher g_bar, so some hot-gas rows may be under-flagged. Carrying the same 16 rows is fine for a no-change re-issue, but the K13 note should disclose this and open a known issue.

15. **Line 52 vs line 51: inconsistent `moves`.** K9 is `both` because lenses re-bin. K8 acts through the same re-binning but is `g_bar` only. Make them consistent, or say why they differ.

16. **K4/K10 inconsistency, and missing terms.**
    - K4 (an applied correction whose uncertainty is not stated) gets a row; K10 (same situation) does not. Add `not_given_by_source` for K10, or drop the row for K4.
    - The SPS/IMF choice (BC03, Chabrier; l. 349 and 360) is not listed anywhere. Put it in the inventory or registry.

17. **Line 71: `x_precedence` is missing.** §9 requires it where roles are used. With alternative rows present, it should say that stars plus cold gas is the source's "fiducial estimate" (l. 421).

18. **Line 73: `x_selection` is ambiguous.** "The lens redshift range stated by the source" does not say which statement. KiDS-bright: z_ANN < 0.5 and m_r < 20.0; GAMA: nQ ≥ 3 and m_r < 19.8 (l. 347–356). Require it per sample, with the bin definitions (§9).

## Notes

- **Line 6 (dropping `no_uncertainty`).** This is defensible under §3 `g_bar_basis` ("no point error by construction"). §2's sentence ("a missing uncertainty is an empty cell plus the flag") was not amended, though. Cite §3 as the basis, since #64 itself proposed a g_bar-specific flag.
- **Line 68 (`total_mass_form`).** Correct under D-087: SIS assumes ρ ∝ r⁻² for the total mass (l. 440). Since the label takes one value, the assumed hot-gas and point-mass baryon forms should be stated in `notes` and the inventory.
- **Possible other-source sizes.** K4 (Kannawadi et al. 2019) and K11 (Boselli et al. 2014) may have sizes in the papers the source cites, which would make them `given_by_other_source`. Leaving them `not_given_by_source` is honest; this is just a note.
- **Simplifications.**
  - The bin-membership check (line 41) duplicates validator §10 item 16. Keep it only for its stated consequence.
  - Item 12 shrinks to one line once the hash check is done before freezing.
- **Covariance.** v1 divides once by the covariance-file bias column. The README defines that column as (1+K_i)(1+K_j) with "covariance / bias", so v1 is consistent and test 3 is safe.
- **Bias factor.** `bias(1+K)` is an input to g_obs but has no §4a quantity. It survives only as an `x_` column. That is acceptable, but should be noted.
- **Neutrality.** No problems found. No cause-laden terms; source wording is quoted where it is used.

**Next step:** fix items 1–9 in the draft, run the README hash check against the canonical tarball, and record the full hash. Then bring item 10 (the hot-gas display change) to JvH as an explicit ruling before freezing.

Files: `/home/claude/atlas` at commit 86814dc (`data/packages/aeg-d-kids1000-rar/v2/REPRODUCTION.md`). Downloaded LaTeX: `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_kids2/src/x/RAR_paper_Brouwer_4.tex`. Mirror README: `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_kids2/readme/README.txt`. Nothing in the repository was modified.