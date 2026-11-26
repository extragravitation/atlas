# Gaps — reader A, aeg-d-xcop

No row was method incomplete or unreadable. All 10 rows were computed (g_obs = GOBS, g_bar = GBAR, as stored, METHOD §3 step 1). Every input was found at the place its locator gives.

These are small points about the method and the files. None of them blocked a value.

1. **The source file is not at the path sources.json gives.** sources.json lists S3 as `eprints/ep_2205.01110v1`. In this folder it is `files/ep_2205.01110v1`. Its sha256 matches (18fc2e80...). S1 `data_E22.tar.gz` and all 20 archive members also match their recorded sha256.
2. **The error convention is inferred, not stated.** METHOD §2 says the errors are magnitudes, and only the values support this. I checked it on all 109 rows: every GOBS_ERR_LO and GOBS_ERR_HI is smaller than GOBS, and every GBAR_ERR is smaller than GBAR. The confidence level of the errors is not stated by the source or by the method. Errors were not needed for g_obs or g_bar.
3. **The HDU and the radius are not fully described by the file.** HDU 1 has no EXTNAME. RADIUS is in kpc, but the file does not say whether it is three-dimensional (METHOD already says this). Neither point affects g_obs or g_bar.
4. **Precision of the values.** The values are float32. The 9 significant figures given in values.csv are the decimal form of the stored float32 values. They carry no more precision than the file holds.
5. **A section number in source_ref is wrong.** The source_ref text calls l. 263 "§3.4". In hydromass.tex, l. 263 falls under `\subsection{Optimization}` (l. 256), which is §3.5. The §3.4 subsection (Nonparametric log-normal mixture) starts at l. 226. The locators already carry this correction. The locator line citations hold:
   - l. 101 starts BCG (§2.4.1), and l. 112 is the last line before §2.4.2.
   - l. 263 says the NP method is evaluated at the radii of the data.
   - l. 410 says ICL is excluded.
   - l. 445 is the fig:rar caption: data points are NP.
   - l. 453 and l. 456 are the g_obs and g_bar equations.
   - l. 458 says both NP and Einasto are considered.
6. **Which method the released GOBS comes from is not stated** (METHOD §4 says this too). No FITS keyword or sentence I read says whether GOBS is the NP or the Einasto result. The method does not need this to read the value.
7. **The measurement identifiers check out.** The mapping in METHOD §2 (A644 19, A1795 21, A2029 22, A2142 20, A2319 27; total 109) matches the row counts in HDU 1 of each file. Each of the 10 rows maps to the member and row its locator gives.
