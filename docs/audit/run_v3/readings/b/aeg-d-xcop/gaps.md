# Gaps: aeg-d-xcop (reader B)

none

No step of the method was incomplete for the 10 measurements in rows.json, and no value was unreadable. METHOD.md §3 step 1 takes g_obs = GOBS and g_bar = GBAR unchanged from HDU 1 of each cluster's gbar_gobs_<cluster>.fits file. No constants are needed. Every input was found at its locator (member, HDU 1, 1-based row in stored order, column).

Checks made (none changes a value):
- The SHA-256 of both source files and of all 20 archive members match sources.json.
- The row counts are A644 19, A1795 21, A2029 22, A2142 20 and A2319 27, for 109 rows in total, as METHOD §2 says. The ID-to-row mapping in METHOD §2 holds for all 10 rows.
- TUNIT is 'kpc' for RADIUS and 'm/s^2' for the five acceleration columns. All columns are stored as 32-bit floats (TFORM 'E').
- On all 109 rows, GOBS_ERR_LO and GOBS_ERR_HI are smaller than GOBS, and GBAR_ERR is smaller than GBAR, as METHOD §2 says.
- In hydromass.tex: l. 263 is in §3.5 Optimization, and it says the NP method is evaluated "at the radii of the observed data". l. 453 and l. 456 are the g_obs and g_bar equations. l. 458 names both methods for g_obs. §2.4.1 BCG runs from l. 101 to l. 112. The statement that intracluster light "is not included in our analysis" is inside physical line 410, which is one long paragraph. The rows.json locators match all of this.

Things the source leaves open. METHOD acknowledges these, and none of them blocks the computation:
- Whether RADIUS is three-dimensional.
- The confidence level of the errors.
- Which g_obs method (NP or Einasto) the GOBS column comes from.
- The source_ref strings in rows.json still say "§3.4, l. 263". The locator's `correction` field rightly gives §3.5.
