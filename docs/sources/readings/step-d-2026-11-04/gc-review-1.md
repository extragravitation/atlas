# Independent review of the globular-cluster v2 test, draft (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Independent review of the globular-cluster v2 test (draft), 2026-11-04

## Bottom line

Do not freeze this draft. Its handling of NGC 2298 and Pal 5 conflicts with v1's frozen code. With the draft as written, test 1 fails and test 3 cannot be filled in, before anything else is checked. It also rests on a premise that turns out to be false: v1's bins for these two clusters are not the bins BH18 dropped. That point needs a ruling from JvH. Several rows of the uncertainty-terms table give a size that the source does not state for clusters, and three "given" rows have no size the validator can read, so test 12 would fail too.

All quotes I checked match the source text and line numbers: B17 l. 586–589, BH18 l. 226–228, the BH18 table caption, Harris l. 148 and l. 152, MvdM l. 1358, Wolf l. 927, l. 974 and l. 1829, K18 l. 344, L13 l. 489, and BSH20 `tab:comp`. The e-print hashes match the step A records.

## Errors (must fix)

1. **NGC 2298 and Pal 5 lose their measurement rows under v1's code (l. 24–26, 36, 42).** In v1, each cluster has exactly two RV bins (`x_gc_baumgardt_n_bins` = 2). Dropping one leaves one bin. `aeg.dispersion.bins_from_radii` then refuses the profile ("edges cannot be inferred from fewer than two radii"), and `convert.py` skips refused candidates (`if c.result is None … continue`).
   - Each cluster becomes a recorded-only system with no measurement row. It does not become a row with `plotted = false` and `coverage_below_threshold`, as l. 25 says.
   - l. 26 says "plotted". That is impossible.
   - Test 1 (l. 36, "v1's 79 rows") fails: there will be 77 rows. Because measurement IDs are numbered in sequence, every later ID also shifts.
   - Test 3's "new σ, coverage" (l. 42) does not exist for these two clusters.
   - The test must state the expected outcome in advance (recorded only, 77 rows, rows matched by `system_id` and dataset rather than by ID), and say where the D-096 note goes when there is no row (systems `properties` or `notes`).
2. **For NGC 2298 and Pal 5, D-096 rule 2's premise is false (l. 24).** BH18 dropped a point from its own 2018 profile. v1 uses the updated `veldis.html` profile ("plus updates"), whose bins are different:

   | Cluster | BH18 Table 3 bins | v1 bins |
   |---|---|---|
   | NGC 2298 | 45.86″ (N = 20), 165.16″ (N = 19) | 23.12″ (21), 101.86″ (21) |
   | Pal 5 | 86.49″ (15), 205.13″ (17) | 129.05″ (20), 341.56″ (19) |

   The point BH18 excluded is not in v1. "Drop each cluster's outermost bin" is therefore the Atlas's own analogy, not deference to the source. It drops stars that BH18 kept, and it unplots both clusters. D-096's context paragraph states the false premise ("v1 uses the outermost bins, which BH18 dropped"). Per D-031 item 2 and rule 6, this goes back to JvH with options:
   - (a) The rule does not apply to the updated profile. Keep the bins, plot, and put the quote in `notes`.
   - (b) Drop by analogy. Both clusters become recorded only.
   - (c) Something else, ruled before conversion.

   M54 is not affected the same way: B17's cut is defined by radius, so it carries over to any binning.
3. **The confidence level is wrong on 8 of the 79 rows (l. 49).** `err_level_status = stated` from the BH18 caption covers only the RV-code profiles. v1 also has L13 (4 rows), K18, F13, D21 and L15 rows.
   - Reader A: L13 states no level, F13 gives the "sigma-clipped standard deviation" of Monte Carlo runs, and K18 and D21 use the 16th to 84th percentiles.
   - Status must be set per dataset code: `stated` with each paper's own quote where it gives a level, `not_given_by_source` otherwise.
4. **Three "given" rows have no size the validator accepts (l. 56, 57, 65), so test 12 fails.** `validate.py` (e029a19, l. 222–230) requires `size_value`, `size_lo` and `size_hi`, or a `size_column`.
   - `half_light_radius` and `king_weights` give their size "from the observables".
   - `stellar_ml` gives "the registry range". The Salpeter end differs by cluster, so it needs a `size_column`, as the dwarf draft does.
   - The test should name the columns: for example, measurement extension columns copied from the R_h, W₀ and r₀ observable errors, and `x_gc_baumgardt_ml_v_salpeter`.
5. **`tracer_mass` (l. 73) applies a two-cluster statement to every cluster.** K18's "≲5%" compares its MUSE main-sequence samples in NGC 3201 and NGC 6121 with literature giant profiles. Every plotted default in v1 is RV code, which is mostly giants (BH18 l. 185). It should be `not_given_by_source` with the K18 statement in the note.
   - This is also inconsistent with `binaries` (l. 70), which is `not_given` even though K18 gives +0.3 and +0.6 km/s for NGC 6121.
6. **`estimator_normalisation` (l. 67) is not a stated size.** Wolf l. 927 says "The dashed lines indicate ±10% variation about the predicted relation". These are guide lines in a figure inset for classical dwarf spheroidals, not a stated accuracy. The draft itself says the accuracy for clusters is not stated. It should be `not_given_by_source`, with the figure described in the note. The same problem is in the dwarf draft.
7. **The horizontal-branch calibration slope is missing (l. 58).** Harris l. 148 gives a slope of ±0.033 in the same equation as the ±0.049 zero point. Adjudication F1 lists it. It is dataset scale, moves g_obs, and its effect scales with each cluster's [Fe/H] (`metallicity_feh` is already packaged). The zero point and slope come from one fit, so they are correlated, and that correlation is not published.
8. **The population M/L error has no uncertainty-terms row (l. 50, 52).** `g_bar_err_*` mix a dataset-scale age term with a system-scale [Fe/H] term. §2a rule 2 requires every system- and dataset-scale term to have a row, and F6 says "v2 states this in the term's note", which implies a row exists. Add one, for example `ml_population`: mixed scale per F6, `size_column` the M/L error, `in_error_columns` empty, with a note saying it already sits in the total columns.

## Weaknesses (should fix)

- **l. 44:** "to 10⁻⁹" must say relative, as v1 test 3 does. At g ≈ 10⁻¹⁰ m s⁻², an absolute tolerance of 10⁻⁹ checks nothing. Changed rows also need their own check: new σ and coverage equal `aeg.dispersion` run on v1's bins minus the listed bins. Test 4 only recomputes g from the stored σ.
- **l. 23:** Define the M54 cut as a bin's mean radius ⟨r⟩ > 200″, the only radius v1 stores. On v1's bins that drops 269″, 410″ and 679″, leaving 13 bins. Edge inference then moves the outer edge of the 170.92″ bin from 219.97″ to 195.76″, so the weights of the remaining bins change. The text should say this is expected.
- **l. 37:** "the `x_gc_baumgardt_*` values" should be "v1's `x_gc_baumgardt_*` columns". v2 adds two new extension columns, and a literal reader would fail them.
- **l. 43:** "expected to be listed" mixes an expectation into a pass/fail test. State the exact expected changes: the M54 row, and the NGC 2298 and Pal 5 rows removed, subject to Error 2's ruling.
- **l. 60, reddening:**
  - L13 is a secondary quotation of Harris (1996), whose own text was not read, and its "average" errors are applied to the 2010 edition.
  - `given_by_other_source` is defensible only if the note says "L13's description of Harris (1996), not read at source".
  - `as_released` should become `one_sigma`, or a note should say the kind is not stated.
  - The effect needs each cluster's E(B−V). v1 does not package E(B−V), or V_t, which l. 80 relies on. Require both as new observables.
- **l. 61, BSH20:** σ_V is the "standard deviation around the mean" (caption). It excludes the mean offsets (+0.03, +0.01 and −0.25 mag), and the −0.25 mag offset for V > 11 is a systematic shift the row does not carry; the note should state it.
  - The upper-bound argument holds only because BSH20 says the estimates are "more or less independent". Say so in the note.
  - Boundaries: the table uses "8 < V < 11", so V = 8 and V = 11 need an assignment.
  - Note also that BSH20's ranges may be in BSH20's own magnitudes, not Harris's.
- **l. 80:** §12 says core views never depend on extension columns, yet `size_column` points at `x_gc_baumgardt_vt_scatter_mag`. The dwarf draft has the same tension. Either name it under §7a or log a deviation.
- **l. 69, `deprojection_4_3`:** §2a rule 4 says deprojection is an assumption. The row needs `assumption_id gc_rhalf_wolf` to qualify as a "both" term. The rows whose effect is computed (distance, reddening, R_h, magnitude) should also name their `assumption_id`. The table has no such column, so test 7 cannot check it.
- **l. 49:** `g_bar_err_level` and `g_bar_err_level_status` are left unset. The MvdM VOT says "The 1{sigma} error", so set `stated` with that quote.
- **l. 86, binary screening:** The column's values are not defined. BH18's screening applies to the RV code only, and only to multi-epoch stars ("1.8 radial velocity measurements" per member on average). Define a value per dataset code.
- **l. 90–91, D-097 scope:** D-097 rule 3 says "dispersion, structure and distance originals". For a pooled re-analysis (D-042), it is undecided whether the literature RV papers pooled into the RV code count. The Pal 5 outcome could depend on this: Odenkirchen et al. 2002 is cited by BH18 for Pal 5's tidal disruption, and is plausibly among the pooled RV sources, which I did not check. Also, Harris (2010) is a compilation whose per-cluster distance originals could not be read. Fix the source list before freezing.
- **Missing `not_given` rows** that step A found:
  - R_V = 3.1 (dataset);
  - centre position (G10);
  - King against Wilson model family for R_h (G15b; MvdM states the direction);
  - Harris's calibration includes dynamical parallaxes (G30). This also bears on D-036 #6 and deserves a note or a known issue.
- **Second reading of the new term sizes:** state that step A's two concordant readings serve as the D-031 second reading for these sizes, or add them to item 11.

## Notes

- **D-087 (l. 27).** `none` on every row is correct. All 79 rows are converted binned candidates, because refused or fitted candidates never become rows. The text should say "every row", not "every plotted value".
- **D-097 (l. 26).** Calling NGC 2298 and Pal 5 a "possibility" follows D-097, which uses them as its example. But BH18's wording presupposes the disruption ("the ongoing tidal disruption of these clusters"); "could" applies only to its being the cause of the rising profile. On D-097 rule 1's own test, that reads closer to a finding. This is for JvH's information. The test must follow the ruling, and if Error 2 resolves to (b), the point is moot for plotting.
- **Steering.** All three known changes cut bins that the sources describe as rising, so they move g_obs in a known direction (down). That is inherent to D-096 for M54. For NGC 2298 and Pal 5, though, the extension beyond the literal source (Error 2) is the Atlas's own choice, made with the direction known. That is the main steering risk, and another reason it needs a ruling and a log entry.
- **Overcomplication.** `mass_loss_models` (l. 66) is a model ingredient, not an uncertainty; fold it into the `stellar_ml` note. `king_weights` "effect not computed" is acceptable. Nothing else needs dropping.
- **Wording.** Neutral throughout. l. 70 "about 50 % for Pal 13" reads like a size of the error; it is the drop in σ when only multi-epoch stars are used. l. 46 says "2.4.0" for a 2.5.0 package. D-047 (Harris-only clusters recorded) should be named as carrying over, alongside D-046 (l. 18).
- **Data seen in this review.** BH18 Table 3 rows for NGC 2298 and Pal 5 (radii and counts; the σ values were visible in the printed row). v1 bin radii, counts, coverage and plotting flags. No v1 g_obs or g_bar values.
- **Downloads.** The e-prints are in `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_gc2/dl/`. Nothing in `/home/claude/atlas` was modified.

Next step: put Error 2 to JvH with options (a), (b) and (c). Then revise l. 24–26, 36 and 42–43, and the table rows in Errors 4–8, before the draft is frozen.