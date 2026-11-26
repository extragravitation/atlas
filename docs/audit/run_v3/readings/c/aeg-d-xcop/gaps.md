# Gaps

No row is "method incomplete" or "unreadable". The method (copy GOBS and GBAR from HDU 1 of each gbar_gobs_<C>.fits, row counted from 1) was enough to produce all 10 rows. The source tar.gz, the eprint and all 20 archive members match the SHA-256 values in sources.json. Row counts are 19/21/22/20/27, 109 in total, as METHOD §2 states. Units are kpc and m/s^2 as stated. For all 10 rows, the row found from the identifier under METHOD §2 matches the locator.

Some points that are not gaps in the arithmetic:

1. sources.json gives S3's file as `eprints/ep_2205.01110v1`. In the audit folder it is at `files/ep_2205.01110v1`, a gzipped tar that contains `hydromass.tex`. Its hash matches.
2. rows.json `source_ref` strings for GOBS say "non-parametric hydrostatic reconstruction ... (E22 §3.4, l. 263)". In hydromass.tex (727 lines), l. 263 is in §3.5 Optimization, which starts at l. 256; §3.4 starts at l. 226. Line 263 says the NP method is evaluated "at the radii of the observed data". It does not say which method the released GOBS column holds. Line 458 names both methods (nonparametric and Einasto). The locator `note`/`correction` fields and METHOD §4 already record this. The source_ref text itself still asserts "non-parametric", which goes further than the source states.
3. rows.json `source_ref` strings for GBAR cite "E22 l. 456" for the central galaxy's dynamical mass-to-light ratio. Line 456 is the g_bar equation. The dynamical M/L (Upsilon_*DYN) is in §2.4.1 BCG, l. 101–112, as the locator correction says. Line 410 does contain "Intracluster light, which is not included in our analysis". All the S3 line locators (101–112, 263, 410, 445, 453, 456, 458) were checked and found as described.
4. The archive does not state whether RADIUS is three-dimensional, or the confidence level of the errors (METHOD already says so). Neither is needed to compute g_obs or g_bar. I checked that the errors are positive magnitudes smaller than the values on the 10 audited rows. I did not check the claim that this holds for all 109 rows.
5. Values are float32 and given as stored, to 9 significant digits (the float32 round-trip precision).
