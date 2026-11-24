# aeg-d-xcop v3: re-issue under data standard 3.0.0

**Decision:** D-114. **Test:** `docs/standard-3.0.0-reissue-test.md` (T1 to T7), frozen with the standard before this package was built.

## What changed from v2

- **`sources.json`:** all seven entries now have their `id`, `kind`, `citation`, `identifier` and a structured `licence`. Their files, hashes and member hashes are unchanged.
  - S1 and S2: the two archives shared by D. Eckert.
  - S3 to S7: the five arXiv e-prints read for quotations and sizes.
- **`locators.json` (new):** three rules resolve all 327 distinct `source_ref` values, 218 in observables and 109 in measurements. No correction was needed. The line citations to Eckert et al. 2022 were checked against `hydromass.tex` in the e-print on 2026-11-24:
  - §3.4 is the nonparametric reconstruction.
  - l. 263: "we evaluate it at the radii of the observed data".
  - l. 453: g_obs = G M_HSE(<r)/r².
  - l. 456: the g_bar equation.
  - l. 410: "Intracluster light, which is not included in our analysis".
- **`known_issues.json`:** the measurement identifiers read v3; the issues are unchanged.
- **Version labels:** `descriptor.json` and `datapackage.json` carry v3, and identifiers in the tables read `aeg-d-xcop/v3/…`.
- **`data/assumptions.json`:** the three registry entries for v2 are copied to v3 unchanged.
- **`tests/`:** runs the re-issue test (T1 to T6) and the standard validator.

## Correction: e-print licences

v2 recorded "arXiv non-exclusive distribution licence 1.0" for all five e-prints. On 2026-11-24 the arXiv records show CC BY 4.0 for three of them: Eckert et al. 2022 (2205.01110), Eckert et al. 2022b (2205.01123) and Ettori & Eckert 2022 (2112.07554). Loubser et al. 2020 and Ghizzardi et al. 2021 carry the non-exclusive licence. v3 records each as read, with v2's wording kept in the note. No file is redistributed either way.

## What did not change

- **Values and text:** every table equals v2's once the version labels are mapped back (T1).
- **The converter:** `convert.py` differs from v2's only in its version line (T2). It reads the archive hashes from `sources.json` as before. Its checks of the frozen records (parts A and B, the second reading) and of the known-issue measurement lists run unchanged.
- **Carried over from v2 and still valid:** parts A and B of the frozen test, their results, the second reading (`reading/`), `result_part_a.json` and `check_part_a.py`. v3 makes no new reading. Part A's failures and part B's pass stand as reported for v2.

## Licences, as read on 2026-11-24

- **S1 and S2, the archives:** no licence file in either archive. The question to the authors is recorded in issue #19, so the status is `asked`. Not redistributed, as in v2 (D-004).
- **S3 to S5:** CC BY 4.0 on arXiv.
- **S6 and S7:** the arXiv non-exclusive licence to distribute 1.0.

## Test result

T1 to T6: see `reproduction/reissue_check.txt`. T7: see `reproduction/reachability.json`.
