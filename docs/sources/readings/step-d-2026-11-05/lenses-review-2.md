# Independent review of the strong-lens v2 test, revision 2 (2026-11-05)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Review: strong-lens v2 reproduction test, revision 2 (commit 8cfa993)

## Bottom line

**Don't freeze it yet.** Revision 2 fixes all eleven must-fix errors from review 1. The core algebra still holds:
- the θ_E exponent is −2 + d ln f/d ln R_E;
- g_obs ∝ H0 exactly, with r ∝ 1/H0 and g_bar unchanged;
- the D_l approximation is stated;
- the gas rewrite on `g_bar_stars_ref` is consistent with the simultaneous-assignment rule in `formula.py`.

Seven errors remain. Two are D-104 bookkeeping, two would give wrong or NaN H0 shifts, and three contradict D-094 or standard 2.5.1. All can be fixed by editing the text, with no new data.

**What I checked:**
- About 45 quote locations against the reader B e-prints. All match apart from one rendering slip, noted under Weaknesses.
- v1 row counts by scope (147 rows, 212 systems, 107 in class A) and which v1 columns are empty or filled.
- The `a6s_*` registry entries, `formula.py`, `formula_check.py`, the validator's §7a code, and D-064, D-075, D-076, D-093, D-094, D-096, D-099 and D-104.

**What I didn't check:**
- I ran no validator on a mock package.
- I opened no g value. I read only cosmology inputs (`x_strong_lensing_h0`) and which v1 columns are empty.

## Errors (must fix)

1. **D-104 is still marked pending (l. 15, 57, 61, 166–168, 170–172, 230).**
   - Fix: replace each "subject to D-104 (pending)" with "D-104 (ruled 2026-11-05)". Rewrite l. 15 as a ruled dependency and delete "A different ruling changes only the text so marked". The commit message also still says "pending".

2. **The H0 term can't be computed as written (l. 197, 166, 168).**
   - The rule "turned into p by dividing by the row's source H0" fails on two sets of rows.
   - **SNELLS:** in v1, `x_strong_lensing_h0` = 70.4 on all three rows (R28 and R61 use WMAP7; R61 l. 130). R25's pair is 67 against 70. Dividing gives p from 0.952 to 0.994, which is neither R25's statement nor p0 at the adopted end.
   - **MaNGA:** `x_strong_lensing_h0` is empty on both rows. R32 names Planck 2018 without numbers, and v1 flags these rows `cosmology_named_only` and `R_E_printed_kpc`. So p is NaN. Item 2 freezes the v1 columns, and item 7's check skips rows with empty inputs, so this would pass silently.
   - Fix: define p from the term's own pair, p = H0_alt / H0_adopted, with no row column involved. That also gives the exact effect D-104 rule 1 asks for.

3. **Which H0 is read from a named paper is not decidable (l. 167–168; item 1 `distance.csv`).**
   - Three named papers are involved: Planck 2016 (A&A 594, A13; R29 bbl l. 185–188), Planck 2018 (arXiv:1807.06209) and Bennett et al. 2014. The Planck papers print several H0 values for different data combinations.
   - D-075 item 4 says "the numbers in the named paper" but doesn't say which.
   - Fix: give a mechanical rule, such as the paper's stated baseline result with its table, column and line. Better still, read the values now and write them into the test with their locations.

4. **The NGC 6505 lens distance is left unsized, against D-094 rule 2 and the test's own sizing rule (l. 173).**
   - D-094 rule 2 lists "NGC 6505 z = 0.041 ± 0.001 against 0.04243" as a size. R30 l. 790 states the bulk flow ("3%") and the peculiar velocity ("150 km s⁻¹") for this system. D-104 doesn't change any of this.
   - `not_given_by_source` is therefore false. The alternative row is a different value, not an uncertainty term.
   - Fix: make the term `given`, with the pair 0.04243 and 0.041 ± 0.001, unit redshift, `size_kind = range`, quoting l. 790. Either state "effect not computed in v2" or define p = D_l(0.041)/D_l(0.04243) − 1 from frozen `aeg.lensing`.

5. **The peculiar-velocity rows have the wrong scale and a size encoding that can't be read (l. 170–172).**
   - D-094 rule 2 says "system for peculiar velocity", but the three rows are `point`.
   - `size_lo` = 0.03 and `size_hi` = 0.04 under `as_released` will be read either as −3 %/+4 % or as p ∈ [0.03, 0.04]. Neither is R26's meaning: a magnitude of 3–4 %, in either direction.
   - Fix: set `scale = system`, and state in the test how the pair maps to p, for example "shift ±size_hi; the source states 3–4 %".

6. **Several `given` point terms for single systems have no valid §7a row type (l. 152, 158, 190).**
   - The rows are `ellipticity_j0403`, `line_of_sight_snl0` and `neighbour_light_snl2`.
   - §7a lets an empty `in_error_columns` mean only "not given by the source" or "a rule 7 row". `in_error_columns = no` requires `applies_to = *` (the validator enforces this at l. 336). So these rows would tell views that their sizes are already in, or absent from, the error bars.
   - Fix: give each `applies_to = *`, a per-row `size_column` filled only on its system, and `in_error_columns = no`. Alternatively, put J0403's 3 % in its `g_obs_err_*` and list the exception in item 2.
   - The 3 % is also signed ("increases the mass by 3 per cent"), so record it as one-sided or put the sign in the note.

7. **The `no_uncertainty` exception contradicts frozen standard §2 and v1's own flags (l. 90 against l. 92).**
   - §2 says a missing uncertainty is "an empty cell plus the flag `no_uncertainty`". A test can't make an exception to a frozen standard.
   - The text also contradicts itself on NGC 6505: v1's `flags` = `no_uncertainty` on both rows, and l. 92 freezes every other v1 column.
   - Fix: give class A rows `no_uncertainty`, which is true because no point error is stated for g_obs. Add `flags` to item 2's exceptions and keep the explanation in the column description.

8. **`x_baryon_inventory` can't hold two statuses for one component (l. 230–232, item 10).**
   - The descriptor has one entry per component, each with a single `status` (v1 `datapackage.json`). D-104 rule 2 needs `stated_negligible` for R25, R28, R30 and R32, and `not_addressed` for the other sources.
   - Fix: specify two entries, for example "central black hole (SNELLS, MaNGA, NGC 6505 sources)" and "central black hole (other sources)", each with its sources and quotes. Without this, item 11 can't be decided.

9. **Wrong side, or a duplicate listing, for model systematics on class A or class B systems (l. 153, 154, 157).**
   - `lens_model_systematic_ngc6505` has `moves = g_obs`. But NGC 6505 is class A, and R30 l. 798 speaks of the model parameters, θ_E included. That is review 1's error 6 again. It also overlaps `lens_model_profile` (`*`, g_bar).
   - On SNL-0, `lens_model_profile` (g_bar, via θ_E) duplicates the SIS-against-MFL difference already carried in g_obs_err (class B).
   - `external_convergence` (`*`) duplicates `line_of_sight_snl0`.
   - Fix: give complementary `applies_to` lists as review 1 error 2 required, and set `moves = g_bar` for NGC 6505 or merge the row into `lens_model_profile`.

10. **`applies_to` phrases the test doesn't define (l. 162, 174).**
    - "Every lens system except …" is ambiguous: the package has 212 systems, but only 94 carry rows.
    - Fix: add these phrases to the l. 146 vocabulary, as systems with measurement rows, in systems-table order.

## Weaknesses (should fix)

- **Combined check (l. 219):** add θ_E moved alone (g_obs unchanged; g_bar = stars + cold gas + hot gas after all entries), and H0 or lens distance moved with the IMF or gas slider at its ends.
- **Size kinds that don't fit their rows:**
  - `sps_systematic_s4tm` is `range` with one value; use `as_released` 0.5 dex.
  - `r_eff_sl2s` is two per-lens sizes (HST and CFHT), not a range. Use a `size_column` or two rows.
- **`pop_*` sizes are given as "fraction of α".** That puts the account-dependent α into the data, which goes against D-104 rule 1's reason. Size them as the Υ_ref change (fixed M_DM, stated), or as `not_given_by_source` with α in the note.
- **"Printed profile" needs a mechanical definition:** a single Sérsic or de Vaucouleurs with R_e and n. R30's seven-component fit (l. 656) can't go in `_theta_profile_*`.
- **New registry entries:** specify `role`, `not_adjustable_reason` and a numeric `default` for `a6s_theta_e` and `a6s_lens_distance`. This would be the first non-adjustable entry with `effects`.
- **Item 9:** add the dataset-page text "θ_E error stated; effect on g_bar not computed" (D-104 rule 3) as a checked line.
- **The site uses only `_hi`** (§12 exception), so asymmetric θ_E errors (SL2S) would be lost in views. Note it.
- **Rule 8 wording (l. 62):** "a modelled dark-matter subtraction" should follow D-104's wording, "subtracts a modelled mass (M_DM in the source's notation)".
- **Quote rendering (l. 167):** "Planck2016" is R29's citation key. The printed text is the citation (Planck Collaboration 2016).
- **Possible double count on SLACS:** the reading should record whether R13's M*(≤R_E) errors already include θ_E. R13's 5 % (l. 1669–1671) is stated for the lensing masses.
- **Wording of l. 220:** "Rows outside class A" is inaccurate, because S4TM rows have `dlngbar` filled and will be evaluated.

## Notes

- Review 1 errors 1–11: all addressed. Error 7 is addressed in principle but not mechanically (errors 2 and 3 above). Error 8 is addressed apart from scale and encoding (error 5).
- D-104 is otherwise applied faithfully:
  - the α percentages are in the notes only;
  - R26's 3–4 % is used directly;
  - the black hole is kept out of g_bar, with all four quotes verified (R25 l. 769, R28 l. 691, R30 l. 778, R32 l. 274);
  - θ_E is not computed where no profile is printed.
- R28 sizes the black hole at "2 per cent of M_Ein" (l. 693). As a share of M*, and so of g_bar, it is larger. This is ruled, but worth one line on the page.
- No step allows a choice after v2 values are seen. Error 3 is a choice left to the reader before conversion, but still a choice.
- Nothing in the text assumes a cause.
- No site code reads `assumption_id`, so term shifts (§2a rule 5) aren't rendered yet. "The site builds" doesn't test them.
- **Next step:** apply fixes 1–10 as revision 3. Errors 2–5 should go to JvH as a short note, because they touch D-094 and D-104 sizes. Under D-093's "review in proportion" rule this was the second review, so no third review: freeze after JvH confirms.

The worktree is removed. Nothing was pushed, and the main checkout's branch was left unchanged.