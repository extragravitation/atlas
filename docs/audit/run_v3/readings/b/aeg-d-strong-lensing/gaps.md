# Gaps

**Method incomplete, by row:** none. Every one of the 10 rows could be computed from METHOD.md alone. No value was unreadable.

These points did not change any value, but a reader should know about them:

1. **File paths in sources.json.** The `file` fields give subfolders (`vizier/...`, `iop/...`, `arxiv/...`). The audit folder holds every file flat in `files/`. Each file was matched by name and by the hash given. It was found in every case.
2. **R10 column headers differ from the locators.** The locators give `log10(M_Ein/M_sun)` and `log10(M*Chab/M_sun)`. The machine-readable Table 2 prints `log_10 (M_Ein/M_sun)` (column 7) and a LaTeX string `${\mathrm{log}}_{10}({M}_{* }^{\mathrm{Chab}}/{M}_{\odot })$` (column 8). They were matched by meaning and column number.
3. **R10 table names carry a prefix.** R10 prints names as `SDSSJhhmm+ddmm`. They were matched by J-coordinate, as METHOD.md says.
4. **R32 (J1436+4943), table numbering.** The paper's §5 text calls the table "Table 5", but the table is printed as "Table 1". The text in §3 gives θEin = 2.02±0.02″, while Table 1 gives 2.03±0.04″. θ_E is not used, because R_E is printed in kpc (4.72 kpc). So this does not affect the values.
5. **R32 IMF.** Υ_ref = 2.93 is for a Kroupa IMF, not Chabrier. METHOD.md §2 step 4 allows "the source's own fixed IMF", so it was used. Also, the R32 locator for Υ_ref says only "§5". The value is printed in §5 (p. 3) and also in Table 1, row Υref.
6. **R32 gas statement.** R32 states that gas is expected to be negligible (§5, p. 3). The registered hot-gas term (0.0012 M★) was still applied, as METHOD.md §2 step 5 says, and the statement is recorded as a quoted assumption (flag `gas_negligible_source_assumption`).
7. **R13 precision.** MChaBC2 is printed as integers in units of 10^10 M☉ (for example 5, +1 −1 for J1143-0144). It was used at that precision, as the method says. This coarse rounding (up to about ±10 % from rounding alone) carries into g_bar for the four SLACS rows.
8. **Selection rules (§4)** were checked for all 10 rows, and all 10 pass:
   - SLACS rows: Lens = A and Mph = E;
   - R10 rows: classification begins with E;
   - all rows: z_l < 0.30. The highest is J0920+3028 at 0.2881.

   The spectroscopic status of the redshifts was taken from the source descriptions (SDSS spectroscopy; R32 MaNGA/SDSS). The R32 z_l and z_s were not checked any further.
9. **Not used in values:**
   - z_s on the printed-M_E rows (R10, R32);
   - the Salpeter masses (R13 MSalBC2);
   - R5's R_e (from ms_arxiv.tex lines 1815, 1906, 1990 and 1956; they agree with VizieR table4 Re);
   - the θ_E, z_l and z_s that R13 also prints.

   All were read and are listed in inputs.csv.
