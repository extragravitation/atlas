# Gaps (reader C, aeg-d-strong-lensing)

Method incomplete: none.
Values unreadable: none.

All 10 rows were computed from the written method alone. Every input was found where its locator says.

## Observations (these did not stop any computation)

1. The byte SHA-256 of the three VizieR files (J_ApJ_682_964_table4.tsv, J_ApJ_682_964_table5.tsv, J_A+A_501_461_lens.tsv) does not match `sha256` in sources.json. The files carry a request date of 2026-11-26, so they were re-exported. Hashing from the line `#RESOURCE=` to the end of each file gives exactly the `content_sha256` values in sources.json. The other files match `sha256` byte for byte. The tarball's ms_arxiv.tex hash matches the value quoted in sources.json (S29).
2. The column headers in the R10 Table 2 file differ in spelling from the locators. The locator `log10(M_Ein/M_sun)` is printed as `log_10 (M_Ein/M_sun)` (column 7). The locator `log10(M*Chab/M_sun)` is printed as LaTeX `${\mathrm{log}}_{10}({M}_{* }^{\mathrm{Chab}}/{M}_{\odot })$` (column 8). These are the same columns, so at_locator is "yes".
3. R32 (arXiv:1911.06338v1): the body text of §5 calls the table "Table 5", but the only table is labelled Table 1, which is what the locators name. Υref = 2.93 is the Kroupa-IMF value, which falls under the method's "source's own fixed IMF". R32 §5 says gas is "expected to be negligible". Under method §2 step 5 the registered hot-gas term (0.0012 × M★) was still applied, and the flag `gas_negligible_source_assumption` applies to this row.
4. Inputs that are listed but not used in any value were recorded in inputs.csv and marked "[not used]" or "[selection only]":
   - SLACS R_e (from the e-print, at the stated lines 1815, 1906, 1956 and 1990);
   - MSalBC2;
   - R32 θEin and zsrc;
   - R10 z_S.
5. Selection rules (§4) were checked for all 10 rows, and every row passes:
   - SLACS rows: Lens = A, Mph = E, zFG < 0.30.
   - R10 rows: Classification begins with E, z_L < 0.30. The largest z_L is J0920+3028 at 0.2881.
   - R32: §3 calls the lens "an elliptical". z_l = 0.125 comes from the SDSS spectrum and z_s from MaNGA/FOCAS [O ii] emission.
6. Cosmology, as read from each paper's §1, last paragraph:
   - R5: Ω_M = 0.3, Ω_Λ = 0.7, H0 = 70.
   - R10: Ω_m = 0.274, Ω_Λ = 0.726, H0 = 70 (WMAP7).
   - R32 adopts Planck 2018, which is not needed because R_E is printed.
