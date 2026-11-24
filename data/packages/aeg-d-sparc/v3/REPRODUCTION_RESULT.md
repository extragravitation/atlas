# aeg-d-sparc/v2 — reproduction result

**Result: PASSED** (first run, 2026-11-01). `REPRODUCTION.md` (SHA-256 `7dd7fc38…`, frozen in #108, before any v2 value was computed) unchanged. Run by `tests/test_reproduction.py`, which implements tests 1–11 and 13 under their frozen numbers. Test 12 is the validator test there, plus the site build and `aeg.site_check` (CI).

| Test | Outcome |
|---|---|
| 1–2. Rows and values unchanged: g_obs, g_bar and every component bit-for-bit identical to v1 (commit `bf5c9ba`), 3 391 rows | pass |
| 3. Systems identical in every v1 column (175) | pass |
| 4. Point-scale g_obs error = g_obs · 2 e_Vobs / V_obs, to 1e-12 | pass |
| 5. Point, inclination and distance terms in quadrature reproduce v1's total on every row, to 1e-9 | pass |
| 6. g_bar error equal to v1's; equals 10 % gas and 25 % stars in quadrature to 1e-9; point-scale g_bar error empty; scales stated in the column descriptions | pass |
| 7. Uncertainty terms: exactly the 8 frozen rows, sizes and citations | pass |
| 8. Observables: 16 021 rows (175 distances, 3 391 velocities, and the velocity components and surface brightnesses), each linked exactly as frozen | pass |
| 9. Measurement columns; `model_dependence` only for D512-2, D564-8 and D631-7; the 4 flags of issue #8 | pass |
| 10. Descriptor fields | pass, with one deviation (below) |
| 11. Independent second reading: 32 269 values, 0 disagreements (`SECOND_READING.md`) | pass |
| 12. Standard 2.3.0 validator; site build; `site_check` 0 errors | pass locally; CI records the run |
| 13. v1 untouched | pass |

## Deviations and disclosures

1. **Test 10 names the wrong taxonomy cell.** The frozen text says `x_search_log` states that "the A1 search (#48) is pending". The search cell for disc galaxies is A4; A1 is wide binaries. The same slip is in D-084 item 4, and is corrected in the decision log. The descriptor states A4. The test's purpose is met: no search row is invented, and #48 is pending. The frozen file is not edited.
2. **Source files for the local run.** The canonical SPARC site was unreachable from the workspace. The two source files came from a public GitHub copy and were accepted only because their SHA-256 equals the hashes in `sources.json`. CI fetches the canonical URLs and verifies the same hashes.
3. **Implementation fixes before the first full pass.**
   - The first local run failed tests 10 and 12 only because `SECOND_READING.md` had not yet been written.
   - `plotted` and `distance_kinematic` were first written as booleans and changed to the strings "true"/"false" used by every other 2.x package. No value was affected.
   - Two tables were not yet wired into the site and were added: the uncertainty-terms download, and the reproduction ledger entry.
4. **Taxonomy kinds**, applied by the frozen taxonomy's morphology rule (not a new decision):
   - the 3 S0 galaxies are `A6` (lenticular);
   - the other 172 are `A4`.

   This is the first time SPARC systems carry kinds.

## Carried over from v1

The comparison with the authors' RAR file (v1 tests 1–2: FAILED, 4 points, issue #8) applies unchanged, because the values are identical. The same 4 rows are flagged.
