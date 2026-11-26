# Gaps and observations (reader A, aeg-d-strong-lensing)

## Method incomplete
None. For all 10 rows, METHOD.md §2 and §3 (route table) gave every step needed to compute g_obs and g_bar.

## Unreadable values
None. Every input was read at the place its locator gives.

## Observations (these do not stop the computation)
1. **Hashes of the VizieR exports.** The whole-file sha256 of `J_ApJ_682_964_table4.tsv`, `J_ApJ_682_964_table5.tsv` and `J_A+A_501_461_lens.tsv` does not match `sources.json` `sha256`. The files stamp a request date of 2026-11-26; `sources.json` says retrieved 2026-11-01. The `content_sha256` taken from the `#RESOURCE=` line to the end of the file does match `sources.json` for all three. All other files match their `sha256`.
2. **File paths.** `sources.json` `file` names subfolders (`vizier/`, `iop/`, `arxiv/`), but the files sit directly in `files/`. Matched by file name.
3. **Record-pair locator.** The first input of each row points to "the observables rows named in observed_from and baryonic_from". rows.json has no `observed_from` or `baryonic_from` fields. I resolved it from the per-input locators listed with each row.
4. **R32 (J1436+4943).**
   - The paper's §5 text calls the table "Table 5", but the table is printed as Table 1 (p.5).
   - θ_Ein appears as 2.02±0.02 in §3 (one model) and as 2.03±0.04 in Table 1 and the Fig. 1 caption. θ_E does not enter the value, because R_E is printed (4.72 kpc).
   - Υ_ref is defined for a Kroupa IMF. I took it as "the source's own fixed IMF" under §4 of the method.
   - The source says gas is negligible (§5, p.3). The registered gas term was still applied, with flag `gas_negligible_source_assumption`.
5. **R13 MChaBC2 precision.** The values are integers in units of 10¹⁰ M☉ (for example "5" for J1143-0144), so g_bar carries only 1–2 significant figures of real precision on these rows. They were used as printed, as the method says.
6. **R13 cosmology.** R13's masses come from its own cosmology (H0 = 70, Ωm = 0.3, §1). That is identical to R5's, so the two sides of these rows do not conflict.
7. **R10 R_eff.** R_eff is stated in the intermediate-axis convention (Table 1 note). It was used as printed with no circularisation, as the method says.
8. **Simpson integration.** The integral used N = 2000 intervals as stated, and b_4 = 7.6692494425 matches the method's 7.669249….
