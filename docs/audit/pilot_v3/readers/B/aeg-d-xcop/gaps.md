# Method gaps (aeg-d-xcop/v3, rows m000001 and m000078)

No step was "method incomplete" for the two values themselves: g_obs and g_bar are read unchanged from the file (METHOD §3 step 1), so no constant and no arithmetic were needed. Every gap below is a step I had to infer.

1. **HDU not named in METHOD.md.** It says "one row of a cluster's FITS table" but not which HDU. I used HDU 1, the only table (the primary HDU is empty). rows.json does give "hdu": "1".
2. **Row base.** "Counted from 1" is stated. I took it to mean FITS row 1 = first data row (Python index 0).
3. **Unit string.** The file's TUNIT is `m/s^2`, not `m s⁻²`. I treated them as the same unit. METHOD says the Atlas "checks" units but does not give the accepted string(s).
4. **Precision / number format.** The columns are float32 (TFORM `E`). METHOD does not say how many digits to report, or whether to widen to float64 first. I report the shortest repr that round-trips float32 (e.g. 2.2402964e-10). A float64 widening would print extra spurious digits.
5. **Measurement-ID to row mapping not defined.** METHOD does not say how IDs are numbered. rows.json gives the mapping directly. I checked that m000078 = A2142 row 16 holds only if rows are numbered across files in the order A644 (19), A1795 (21), A2029 (22), A2142 (20), A2319 (27): 19+21+22+16 = 78. That order is inferred from the order METHOD §1 lists the clusters in.
6. **Which g_obs the file holds is not verifiable from the file.** METHOD says GOBS is the non-parametric (NP) hydrostatic value. The FITS header carries no provenance keyword. The paper (hydromass.tex l. 457) says both NP and the Einasto DM-only fit are used for g_obs. I accepted METHOD's statement but could not confirm it from S1. The same applies to whether GBAR comes from the NP or the Einasto (EIN3_bar_mass.fits) reconstruction.
7. **"Three-dimensional radius" is not stated in the file.** The header only says RADIUS [kpc]. Taken from METHOD. No cosmology/h is stated for the kpc conversion. Not needed here, because RADIUS is not used in the values.
8. **Error form.** METHOD points to `reading/error_form.md` for how to read GOBS_ERR_LO/HI. That file is not in the packet. I recorded the errors as printed (positive numbers) but could not check the stated reading. This does not affect g_obs or g_bar.
9. **Paper locator, section.** "§3.4, l. 263": line 263 sits in `\subsection{Optimization}` (l. 256 onward), which is Sect. 3.5 by counting subsections. Sect. 3.4 (NP log-normal mixture) is l. 226-255. The .tex has no printed section numbers, so the numbering is my count. The line citation itself is correct.
10. **Paper locator, BCG M/L.** rows.json's source_ref for GBAR mentions "the central galaxy's dynamical mass-to-light ratio" next to "(E22 l. 456)". The dynamical M/L is described at l. 107 (subsubsection BCG), not at l. 456. l. 456 is the g_bar equation only.
11. **Source file path.** sources.json gives S3 as `eprints/ep_2205.01110v1`. In the packet it is `files/ep_2205.01110v1`. It is a gzip-compressed tar with no extension, which nothing in the packet says. I found hydromass.tex inside it by unpacking.
12. **Line numbering of hydromass.tex.** I assumed 1-based physical lines of the unpacked file. The cited lines match under that assumption.

Verified: the sha256 of both packet files, and of all 20 archive members, matches sources.json.
