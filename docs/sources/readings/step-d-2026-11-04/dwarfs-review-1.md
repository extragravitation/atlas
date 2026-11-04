# Independent review of the dwarf-galaxy v2 test, draft (2026-11-04)

An independent reader agent wrote this report under `brief.md` in this folder. It is kept verbatim below.

---

# Independent review of the dwarf-galaxy v2 test (draft), 2026-11-04

## Bottom line

The test should not be frozen yet. Its structure is sound, and the Phoenix II facts check out at source. But four things block it:

- Its precedence rule (l. 18) contradicts how it handles its only known D-096 case (l. 19).
- Three rows of the terms table would fail the validator, which item 12 requires to pass.
- The "five systems" for `g_bar_err_point_*` are named by the wrong criterion.
- The D-096 and D-097 readings are not required to exist before conversion, so "values change only where D-096 requires it" can still be steered.

All of these can be fixed in one revision. Nothing in the test assumes a cause.

**Phoenix II at source.** I checked arXiv 1805.07350v4 (`spec_v1_ref1_arx.tex`, SHA-256 9f7efbac…bd80):
- 9.5 (+6.8/−4.4) is at l. 446, and 11.0 (+9.4/−5.3) at l. 452, with the bold mark.
- The caption is at l. 436: "Above the line we show the values calculated from all possible members, below those from the certain members. We indicate in bold which determination we prefer".
- l. 393 reads "our preferred set of values are those derived when excluding this star".

All locators and values in l. 19 are correct.

## Errors (must fix)

1. **l. 18 against l. 19: Phoenix II is itself a D-038 2B conflict, by v1's own record.** v1's σ coding (`v1/reading/sigma_rules_rows_v3.csv`, phoenix_2 v2 row) has `whole_sample = no`, status `recorded`, reason "subset (D-038 2B)". That is why v1 selected 9.5 ("only passing value", `sigma_selection_v3.csv`). Adjudication F2 reads 2B more narrowly: "multi-population fits, not membership sets". Under l. 18 ("D-038's specific rules come first … where they conflict … brought to JvH"), Phoenix II should go to JvH. Yet l. 19 already decides it for D-096. Separately:
   - "D-038 first" is not in D-096. D-096 rule 2 has existing rules apply *after* D-096, as filters ("If a value then fails an existing rule … that rule applies"), not as selectors that come first. D-096's rejected alternative (leaving the source's stated choice unused) argues against carving exceptions.
   - The clause names only D-038. It is silent on the other value-selection rulings D-096 could override: D-052 (adopted fit and distance), D-055 items 2, 3 and 5, D-061 item 4 (Leo I midpoint) and D-062.
   - "Brought to JvH" after conversion would be a ruling made after results.

   **Fix:** before freezing, get a ruling (operating rule 6) on precedence between D-096 and the earlier value-selection rulings, including whether 2B covers membership subsets. Then write l. 18 as a complete, mechanical order with no escalation after conversion.

2. **l. 53: `half_light_radius` fails the validator.** It is `status = given` with neither `size_value` nor `size_column`. `validate.py` (e029a19, l. 222–229) reports "given term without a size", even though §2a rule 7 allows a size taken from observables. Item 12 then fails. In addition:
   - several R_h originals print no error (And VI, Antlia 2 and Tucana V observables say "no error"), so "given" on `*` is untrue for them;
   - `size_kind` is missing.

   **Fix:** use measurements `size_column`s for the R_h and ε errors, with `no_uncertainty` on observables without one, or split the row into "given" (a listed subset) and `not_given_by_source`.

3. **l. 69: `gas_inside_rhalf` fails the validator.** It is `scale = system` with a list-valued `applies_to`, which the validator rejects (l. 324: "a term for a listed subset … must have scale = dataset"). It is also written as names, and l. 72 converts only the Savino and Martin lists to `system_id`s.

4. **l. 67 (and l. 54): `size_column` must be one existing column.** `x_dwarfs_upsilon_v_low/high` is not a column name. The distance row names only `_hi`, so an asymmetric distance error (for example Tucana V, +3/−8 kpc) would be drawn from one side only. State which column is used and how the other side reaches the view.

5. **l. 45: the "five systems" are misidentified.** The flag `mv_modulus_assumed` is on 3 rows (Leo T, Phoenix, Tucana V), and D-061 covers those 3. v1 folded a modulus error (`inputs_v2.py` l. 205–208, `MAG_OVERRIDE` with `mod_err`) for a different five: And VI, And VII, Phoenix, Leo T and Tucana. Tucana V has no modulus error. Also, Leo T's printed M_V has no error, so its point error would be empty. **Fix:** list the five by `system_id`, and say what Leo T's point column holds.

6. **l. 46–47: confidence levels are asserted, not read.**
   - v1 has no `err_level` column, so the levels cannot be "kept". They are strings in `x_dwarfs_sigma_limit_level`, including "90th percentile" and And XII's "1-sigma upper error (no limit stated; D-062)". The test must state And XII's `err_level` and status.
   - `g_bar_err_level_status = stated` claims the magnitude sources state 1σ, but nothing reads that. D-093 rule 1 says a level is "never read as 0.683".
   - Nothing at all is set for the σ levels of non-limit rows. The KiDS test sets the level with a citation.

   **Fix:** add confidence levels as printed to the item 11 second reading, and set each status from it.

7. **l. 30 against l. 33 and l. 80: decidability holes.**
   - Item 1 fixes `r_kpc`, but a D-096 change to a structure or distance value changes `r_kpc`, so items 1 and 3 can conflict.
   - Item 8 requires "every other row plotted, as in v1", but D-096 rule 2 says a changed value then goes through existing rules (D-051 coverage, D-038 1A). Phoenix II's coverage must be re-run with the five certain members (Fritz Table 2: 0.57, 1.78, 1.71, 1.82 and 1.54 times Fritz's R_half) against the plotted R_h (Richstein 2024), with both centres (D-055 item 9). A pass is likely but has to be computed.

   **Fix:** exempt rows listed under item 3 from item 1's `r_kpc` check and from item 8's "as in v1", and require the coverage re-run explicitly.

8. **l. 86–90 against l. 3: steering.** The D-096 and D-097 readings are not required to be finished before conversion, and nothing says who resolves disagreements, or blind to what. **Fix:**
   - complete and hash the second reading's D-096 and D-097 fields before the first v2 conversion run;
   - have the converter apply changes only from that reading;
   - have disagreements resolved at source by someone without access to the v2 values.

   Item 3 then becomes mechanical.

## Weaknesses (should fix)

- **l. 20, D-096 rule 2 is unbounded for printed values.** Every σ paper excludes non-members or binaries, and the printed value already reflects that. State that rule 2 changes an input only where the Atlas computes from data points the source excluded (here: D-051 member tables). Otherwise readers will flag every paper, and "matches on every field" becomes a matter of judgement.
- **l. 21 and l. 89, D-097 classification.**
  - Rule 2's test is lexical ("could", "may", "might"), but the ruling's own "finding" examples are hedged ("unlikely to be", "support a … scenario").
  - Add a third class, "neither": for example "tidal features detected", "no evidence of disruption", or orbital remarks.
  - Say how "likely/unlikely/suggest/consistent with" are classed.
  - Name the sources counted: D-097 rule 1 says "dispersion or structure source", rule 3 adds distance originals, and l. 89 says "own sources".
  - D-025's "tidally disturbed" is not covered by D-097 rule 1's three conditions. Say whether it excludes.
- **l. 77–80.** Item 8 does not check that "possibility" quotes are in `notes` (D-097 rule 2). `data/registry/excluded.csv` does not exist at either commit. Define its columns (§5: system, dataset, reason, citation) and say whether site visibility (D-097 rule 5) is checked.
- **l. 32, no clause holding all other columns unchanged.** KiDS has one ("Every other v1 column is unchanged, except…"). As written, `x_dwarfs_*`, `source_ref`, `assumptions`, `flags` and `r_kind` can change freely.
- **Terms missing against the adjudication's union** (adjudication l. 22–52):
  - per-pipeline velocity error floors and calibration (Tollerud 2.2 km/s, Heiger 1 km/s, Kvasova 1.49 km/s; a shared term inside the point σ errors, which mixes scales under §2a rule 6);
  - HI detection and mass errors (system scale, g_bar);
  - band transformation (Muñoz, Martin, Richstein; plus D-055 item 7's Leo T transformation);
  - molecular and ionised gas;
  - distance calibrations other than Savino ("per calibration");
  - LF and IMF terms for sources other than Martin ("per source").

  Either add rows (`not_given_by_source` where no size is stated) or give the reason each is omitted. Also say why "equilibrium and sphericity" is not a row (§2a rule 4), as KiDS does.
- **Inconsistent use of sizes.**
  - `binaries` (l. 59) cites Wolf's "up to ∼20 %" but is marked `not_given_by_source`, while `deprojection_4_3` uses Wolf's "better than 2 %" as `upper_bound`. One rule should decide both.
  - `deprojection_4_3` is the one assumption that §2a rule 4 names as never a term. Keep it only as a parameter term with an `assumption_id`, and note that Wolf's table gives 1.305 to 1.352 (−2.1 %).
  - `anisotropy_profile` (l. 57) is moved from the adjudication's system scale to dataset scale, and drops the aperture and coverage part. Reader B (note 3) says applying it "is a judgement, not a quote". Say that the assignment is the Atlas's (as SPARC amendment 2 does), and give `correlated_with` against `estimator_normalisation`.
  - The Savino 3.5 % may already be inside the Table 5 errors (Reader A, Doubt 2). Resolve this, or say so in the note, to avoid counting it twice.
- **l. 54, `moves = g_obs` is false for Boötes III.** Use `moves = both`, with a registry formula that has an exponent of 0 except for systems flagged `mv_distance_independent`. Derive the exceptions from the flags rather than naming one system. Rows that need a computed effect also lack an `assumption_id`: `distance` (`dw_distance`), the rule-7 row, and `rh_convention_profile` (D-052 item 2 says its effect is computed). In v1 all of these registry entries have `effects: null`.
- **l. 45, point columns on the other 59 rows.** Under §3, an empty `g_bar_err_point_*` reads as "source gives no point error". Require point = total on those rows.
- **l. 84.** `distance_inherited` is not in the §11 closed list, so `flags` would fail the validator. Say it goes in `x_dwarfs_flags`.
- **l. 83.** `x_dwarfs_binary_screening` should be a closed list (for example multi-epoch stated / not stated), as D-025 asks for a flag, not free text.

## Notes

- **l. 19:** l. 393 is also an exclusion (one star dropped), so D-096 rule 2 gives the same result. Fritz l. 415 says σ "does not depend significantly on which set of members is considered"; worth quoting in the result. v1 already takes Phoenix II's [Fe/H] from the preferred certain-members row (−2.51), so v1 was internally inconsistent, and g_bar does not change.
- **l. 45:** the reason for dropping the modulus term is that the paper's own modulus cancels in m = M_V + μ_paper, not F1 (which is about the Atlas distance). The conclusion stands.
- **l. 55–58:** the Wolf, Savino and Pace locators match both reader reports. I did not re-read them at source.
- **l. 5:** D-095 to D-097 are on `standard/2.5.0` (e029a19), which is not an ancestor of 11a4853. Merge order matters.
- **l. 41:** the heading says 2.4.0; the package states 2.5.0.
- **Could be dropped without losing rigour:** l. 18's escalation clause (once item 1 above is ruled) and l. 48's "The second reading records them" (already in item 11).
- **Out of scope but seen:** v1's Columba I is Geha 2026 ("no original passes"), although Fritz 2019 prints a preferred limit (<16.1). It does not pass the plotting rules, so D-096 does not change it, but the second reader will record it.

I modified nothing in `/home/claude/atlas`. The e-print is in `/tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/review_dwarfs2/src/` (tarball SHA-256 41cad1cd…dc90).

**Next step:** get JvH's ruling on the l. 18 precedence (including whether 2B covers membership subsets), then revise items 1, 5, 7, 8 and 11 and the terms table, and run the validator on a dummy terms table before asking for the freeze.