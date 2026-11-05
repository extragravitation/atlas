# Independent review of the strong-lens v2 test, draft (2026-11-05)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Review: strong lenses v2 reproduction test (draft rev. 1, commit 1316f19)

## Bottom line

**Don't freeze it.** The core algebra holds up:
- g_obs = π G Σ_cr, so on rows where M_E is the mass at mean convergence 1, a θ_E error moves only g_bar and R_E.
- The exponent −2 + d ln f/d ln R_E is correct.
- The H0 formula is exact: g_obs ∝ H0, r ∝ 1/H0, and g_bar is unchanged at fixed Ω_m, because M* ∝ D_L² and R_E² ∝ D_A².
- No text assumes a cause.

But nine items would make the test fail mechanically, contradict the standard, or misread a source. All of them can be fixed by editing the text, and none needs new data.

What I checked:
- 40 quote locations against the reader B e-prints. Three are wrong.
- `lensing.py` and `test_lensing.py` still match their frozen hashes.
- No file in v1 has changed since commit 5dc4091.

What I did not check:
- I didn't run the validator on a mock package.
- I opened no g value. I did see some of R32's printed Table 2 inputs (θ_E, L_Ein, Υ_ref, M_DM) while checking line numbers. These inputs are already public in v1.

## Errors (must fix)

1. **The class A row counts are wrong (l. 46–49).**
   - SLACS has 96 rows (48 default and 48 alternative), SL2S has 6, and NGC 6505 has 2. The alternative rows also compute M_E from θ_E.
   - Fix: state that the class applies to every row of a system, alternatives included. The expected class A total is 106 rows: SLACS 96, SL2S 6, MaNGA 2, NGC 6505 2.

2. **NGC 6505's θ_E error is counted twice (l. 121, 134, 135).**
   - NGC 6505 is class A, so item 6 fills `theta_e_err_frac` and the term `theta_e` (`applies_to *`) covers it.
   - `theta_e_ngc6505` then carries the same error again.
   - Fix: leave the column empty on `aeg-s-000509` and say so. The same applies-to overlap affects `cosmology_h0` against the three per-source H0 rows, and `redshift_measurement` against `redshift_ngc6505`. Give the generic rows the complementary system lists.

3. **The exponent for SLACS can't be computed from what the package stores (item 2 against item 4 and item 6).**
   - SLACS uses v1's `printed_in_RE` route, so `x_strong_lensing_r_eff_arcsec` and `_sersic_n` are empty on all 96 SLACS rows.
   - The exponent needs R13's de Vaucouleurs R_e, a new input. But item 2 freezes every v1 `x_strong_lensing_*` column and forbids new observables.
   - So item 4 ("recomputed from the stored inputs") cannot pass, and the new input would break D-029, which requires every input to be recorded as an observable.
   - Fix: allow new columns for the profile inputs, allow appended observables (after v1's last ID) and the matching `baryonic_from` additions, and list both in item 2.

4. **Item 2's notes exception is incomplete.**
   - Item 6 says that any row with no size "gets an empty value, and the column name goes in `notes`". `lens_distance_frac` is empty on almost every row, so almost every row's `notes` changes.
   - Item 2 allows note changes only on class A rows and rows with a reading note, so item 2 fails.
   - Fix: add the item 6 notes to the exceptions, or record the empty columns in the column header instead of per row.

5. **J0403−0239 contradicts §2a rule 7 (l. 52).**
   - θ_E has its own printed error. R29 l. 196 gives "1.47 ± 0.03 arcsec", and M_E comes from "the symmetric lens equation" (l. 210), which is mean convergence 1.
   - Rule 7 forbids keeping that error on g_obs "at fixed radius". The 4 % is not inseparable: R29 states its parts, 2 % "dominated by the measurement of R_Ein" and +3 % for ellipticity (l. 210).
   - Fix: make J0403 class A for the ±0.03″. Carry the ellipticity and shear part as a g_obs term of 3 %, `given`, quoted. Do not subtract anything in quadrature. If J0403 stays class B, the test must say why rule 7 doesn't apply.

6. **Several θ_E-type systematics are put on the wrong side, against F1 (rows at l. 137, 138, 139, 142).**
   - `lens_model_profile` ("the Einstein radius parameter … becomes somewhat dependent on the assumed mass model"), `external_shear` (R9 l. 388 compares "the resulted Einstein radii"), `sie_axis_convention` and `lens_light_subtraction` all change the fitted θ_E. They move g_bar and r, not g_obs.
   - Only `external_convergence` and the line-of-sight term change M_E at a fixed radius, so only they belong on g_obs.
   - Fix: set `moves = g_bar` on those four rows.
   - `sie_axis_convention`'s size is also misread. R9 l. 117 says the Huterer *conversion relation* "is accurate to < 1%", which is not the size of the convention difference. Set it to `not_given_by_source` and move the quote to the note. SLACS uses the same b_SIE convention, so its `applies_to` should not be S4TM only.

7. **The H0 and peculiar-velocity sizes are α shifts, not shifts in the lensing M/L (l. 58, 123, 148–152, 186).**
   - R25, R29 and R32 define α = (M_Ein − M_DM)/(Υ_ref L_Ein). See R29 l. 206, R32 l. 288 and R25 l. 613.
   - Their 5 %, 4 %, 3.5 % and "up to 5 %" therefore include the effect on a *modelled dark-matter subtraction*. They are not the g_obs fraction.
   - The test describes them as "fractional change in the lensing mass-to-light ratio" and applies them straight to g_obs. That misdescribes the source and imports a quantity that depends on an account of the discrepancy.
   - Only R26's "3–4 %" is stated in the lensing M/L.
   - Fix:
     - Size the H0 terms in the parameter's own unit and let the exact formula do the work. SLC15 states H0 = 67 against 70. R29 names Planck 2016 and R32 names Bennett 2014, so read their H0 from the named papers, as the D-075 item 4 convention already requires.
     - Record the α percentages in the notes, labelled as α.
     - D-094 rule 2 names these sizes, so put the clarification to JvH. It doesn't reverse D-094.

8. **`lens_distance` can't be decided mechanically and contradicts D-094 (l. 152).**
   - "3–4 %" can't go in one column.
   - R26's statement covers all three SNELLS lenses (its Table 1 lists all three), and so does R25's. The test assigns R26 to SNL-0 only and gives no rule for SNL-1 and SNL-2.
   - D-094 rule 2 and D-093 item 4 require `upper_bound` for "up to 5 %", but the row uses one `as_released`.
   - The NGC 6505 entry is ambiguous: it is listed under "Expected sizes" but "carried as v1's alternative row".
   - Fix: one row per system for each stated size, with its own `size_kind`. `scale = system` can't take a list `applies_to`, because the validator then requires `dataset`. Use `lo` and `hi` for 3–4 %. State that NGC 6505's column is empty.

9. **The confidence-level mapping can't be represented in the columns (item 5 table).**
   - On class A rows `g_obs_err` is empty, so `err_level` and its status have nothing to describe.
   - R5's level ("g_bar via term theta_e") has no column, since §7a has no level field.
   - R20's "68 % credible intervals" (l. 462) is about the lens parameters, not M*. "both, stated 0.68" is unsupported for g_bar.
   - "no_uncertainty" is a flag, not an `err_level_status` value.
   - Fix: give a per-row rule: status empty where the error column is empty; term levels go in the term note; R20's g_bar level read at source or `not_given_by_source`.

10. **Two quotes have the wrong line.**
    - `pop_age_j0403` (l. 161): the quote is at R29 l. 241, not l. 208.
    - `pop_model_family_manga` (l. 162): the Maraston quote is at R32 l. 293, not l. 282.

11. **The D-096 reading leaves out R27 (l. 32).**
    - R27 (Collier et al. 2020) supplies J0403's alternative θ_E and redshift observables, and it is newer than R29.
    - D-096 rule 4 requires every source used. A stated preference in R27 would change a default.
    - Fix: add R27.

## Weaknesses (should fix)

- **The sizing rule is applied unevenly.**
  - R9's 0.5 % is excluded as "R9's own models" (l. 53), but R9's 2 % shear (also R9's fits of the S4TM lenses) is included. The only justification is R10 l. 308–309 ("as quantified in Shu15"), so state it.
  - `r_eff_profile` is `not_given_by_source` although R5 (3.5 %) and R20 (30 %, 10 %) state sizes for these systems.
- **Fill `dlngbar_dlntheta` on every row with a printed profile (S4TM and SL2S as well as class A).** Otherwise the θ_E-type terms in error 6 can never be computed. It adds no assumption.
- **The formulas interact.**
  - The v1 gas slider computes M* from `g_obs × mstar_re/m_e` (convert.py l. 120), and formulas apply "one after another in registry order" (formula.py).
  - So H0 would wrongly move the gas term, and θ_E would leave it at the old radius.
  - Item 7 only checks each formula alone at p0. Add a combined check, or rewrite the v2 gas formula without g_obs.
- **Item 7's check is not code that already exists.**
  - `formula_check.py` tests only the assumptions listed in `adjustable`, and the three new entries are not adjustable.
  - Name the script, and require Python/JS agreement for these formulas, because the site will compute the term shifts.
- **`a6s_lens_distance` doesn't move `r_kpc`**, but `a6s_source_cosmology` and `a6s_theta_e` do. Make the three consistent, or say why not.
- **`a6s_theta_e` is a log-linear (first-order) approximation.** It is fine at 2 %, but J1701's θ_E error is 10 %. Say so.
- **Empty `g_obs_err` on class A rows has no `no_uncertainty` flag**, against standard §2 ("an empty cell plus the flag"). State the exception explicitly in the column description.
- **The survey names in `applies_to` don't match the `x_strong_lensing_scope` values.** The values are "SLACS V-modelled lenses", "MaNGA J1436+4943" and so on, and "SNELLS" matches no single value. List the scope strings or the system IDs.
- **`redshift_ngc6505` misuses `size_lo` and `size_hi`** for two different quantities (z_l and z_s). Split it into two rows.
- **Size kinds and units:**
  - `sps_systematic_s4tm` (a lower-to-upper model span) should be `range`.
  - `cosmology_h0_j0403` should be `dataset` scale per D-094.
  - Give `size_unit` on every given row.
  - Set `in_error_columns` empty on `theta_e` (it is a rule 7 row).
- **`aperture_radius_snl12`:** R61's half-separation is at l. 155, not l. 156.
- **Item 12:** add `PYTHONPATH=pipeline` to the validate command.
- **The "Checked before freezing" section ran only `validate_v22`/`_v24`, not the full `validate()`.** Say so.

## Notes

- **D-094's formula as written:** the H0 entry is exact. Peculiar velocity enters through D_l alone, and g_obs ∝ D_s/(D_l D_ls) is close to 1/D_l only when D_s ≫ D_l. That holds for SNELLS and NGC 6505. State the approximation.
- **`theta_e_err_frac_lo`** is not named by any `size_column`, so the §12 exception (D-099 rule 1) covers only `_hi`. There is precedent in the globular-cluster `stellar_ml` row, but say so.
- **The `pop_*` α shifts** map to Υ_ref (α ∝ 1/Υ_ref at fixed M_DM), so +10 % in α is −9.1 % in g_bar, not −10 %. Note it.
- **Spot checks that matched:** R30 l. 639, 698, 778, 790, 798, 813; R32 l. 176, 261, 270–277, 293; R29 l. 196, 210, 241; R28 l. 317–325, 496; R9 l. 117, 138, 386, 388, 424–425; R10 l. 291–292; R25 l. 769, 772–773, 862–865; R26 l. 139, 141; R5 l. 843–848, 972–975, 1072–1076; R13 l. 1669–1705, 2975; R20 l. 354–359, 462, 477–478, 740. The SNL-0 black-hole figure is at R28 l. 691–693.

## O1 (black hole) and O2 (missing light profile)

**O1: the recommendation is sound, with a stronger reason and a different home.**
- The stronger reason: every quoted size comes from a scaling relation driven by the lens's own σ. R30 l. 778 uses the M–σ relation, R28 l. 693 gives a "mean expected" mass, and R25 gives an average for σ = 300 km/s. Adding any of them to g_bar would breach D-036 #6 (nothing derived from the system's own kinematics), whatever "detected baryon" is taken to mean.
- The different home: the sizes are stated for these systems, so `not_given_by_source` breaks the test's own sizing rule. Move the black hole out of the uncertainty terms and into `x_baryon_inventory`. Mark it `stated_negligible` where the source says so (R30, R25, R32), with the quotes, and `not_addressed` elsewhere.

**O2: accept (a) for v2, with the gap made visible.**
- In practice O2 affects only the two MaNGA rows. NGC 6505's 0.04 % lower bound is negligible.
- Under (a), J1701's 10 % θ_E error, which v1 showed as a 20 % g_obs bar, drops out of the bars entirely. Keep `theta_e_err_frac` filled on those rows, and have views state "θ_E error stated; effect on g_bar not computed".
- Reject (b): R32 prints θ_Eff but no profile form. R30 describes a "complex and varying isophotal structure" fitted with seven Sérsic components, so a de Vaucouleurs profile would contradict the source.
- A better later option, which needs a ruling: d ln M*(<R)/d ln R = 2Σ(R)/Σ̄(<R).
  - The exponent is therefore at least −2 with no assumption at all.
  - It is at most 0 if the surface density does not rise outward at R_E.
  - So the exponent can be bracketed in [−2, 0] without any profile.

**Next step:** apply fixes 1–11 as revision 2. Put the item 7 α/H0 clarification and O1/O2 to JvH in one message, then run a second review of revision 2, as D-093's "review in proportion" rule provides when the first review finds must-fix errors.

The temporary worktree has been removed. Nothing was pushed or changed in the main checkout.