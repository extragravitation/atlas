# Audit v3 reader notes (`readings/*/*/gaps.md`): triage for v0.4 (D-125)

Each point the 12 Part A readers recorded in their `gaps.md` files is listed below. Points the two readers of one dataset share are merged. None of these points changed a value. Every source claim was checked at the source before the text changed.

**Outcomes:**
- **change:** the methods text is amended;
- **no change:** a reason is given;
- **already:** the point is recorded elsewhere (known issue, decision or methods text).

## SPARC

| Point | Outcome |
|---|---|
| Inc and e_Inc have no row locator (A1, B1) | **change:** §2 says the row locators name the inputs of g_obs, g_bar and the distance, and that Inc and e_Inc are read from the same Table 1 row. The released locators are not changed (D-125). |
| e_Vobs is missing from the §2 input table (B4) | **change:** added to the table. |
| R has no column locator; the locator names the row (B3) | **change:** §2 says R and the velocities are read from the row the locator names. |
| Whether blank lines count as data rows (B6) | **change:** §2 says the data section has no blank lines. |
| Vbul = 0 on no-bulge rows is not listed (A2, B2) | **already:** §2 says so. |
| Negative Vgas, sign kept (A3, B7) | **already:** §3 step 3. |
| "§3.4" in two source_ref texts (A4, B5) | **already:** known issue #222, fixed in the v3 locators. |
| "[value]" placeholders in source_ref (A5) | **no change:** the placeholders are the package's redacted text in the audit packet, by design (brief §2.6). |
| arXiv:1610.08981 not supplied (A7) | **no change:** the paper is cited, not supplied, and the methods text says so. The attribution was corrected under D-124. |

## KiDS-1000

| Point | Outcome |
|---|---|
| The methods text said the README calls column 1 the baryonic acceleration (A1, B1) | **change:** the README actually describes column 1 as "the mean projected distance from the lens center … in meter-per-second-squared for the RAR data" (README.txt l. 25). That the column is g_bar comes from the paper (§2.1, l. 174), and the text now says so. Both were checked in the source files. |
| `reading/` files cited by rows are not in the packet (B2) | **no change:** a property of the audit packet, not of the method. |
| The README's G unit is written pc² (B4) | **no change:** the README constants are not used (§1), and the methods text already gives the correct unit. |
| Only 10 of 45 rows in the packet (B3) | **no change:** the packet holds the sampled rows only. |

## X-COP

| Point | Outcome |
|---|---|
| Whether RADIUS is 3-D, the error confidence level, and which method GOBS comes from (A2, A3, A6, B) | **already:** §2 and §4 state these as not given by the source (D-119). |
| "§3.4, l. 263" in source_ref (A5, B) | **already:** known issue #234; the locator corrects it (D-119). |
| Path of S3 in sources.json against the packet (A1) | **no change:** an artefact of the packet layout. |
| float32 precision (A4) | **no change:** the methods text says the values are copied as stored. |

## Globular clusters

| Point | Outcome |
|---|---|
| veldis.html spacer rows have one blank cell, not none (A1, B3) | **change:** §2 corrected. |
| mwgc.dat: how a value lines up with its label, and the ID width (A2, B1, B2) | **change:** §2 now gives v1's frozen reader rule: ID in characters 1–12; each value goes to the label with the nearest right edge; `c` and `c:` are flags (`v1/sources_io.py`, `_fixed_part`). |
| Tie-break between two Types of the same year is unspecified (A5, B5) | **change:** §3 says they are not ranked further, and that no v3 row needs it (every default is RV). |
| `<r> = [value]` placeholders in bin locators (A4, B4) | **no change:** these are the packet's redaction of values. Readers checked the bin counts, which match. |
| VizieR export hashes and paths (A3) | **no change:** the content hashes match, as the record's note says. |
| Numerical sensitivity (A6, B6) | **no change:** a confirmation (≤ 5 × 10⁻⁵ relative). |

## Strong lenses

| Point | Outcome |
|---|---|
| R10 column headers differ from the locator wording; names carry a prefix (B2, B3) | **change:** the route table gives R10's columns 7 and 8 and how names are matched. |
| R32 §5 calls the table "Table 5", but it is printed as Table 1; θ_Ein differs between §3 and Table 1 (A4, B4) | **no change:** source inconsistencies that do not enter the value (R_E is printed). |
| R32 IMF is Kroupa (A4, B5) | **already:** §2 step 4 allows "the source's own fixed IMF". |
| R13 integer precision (A5, B7) | **already:** the values are used as printed, as §2 says. |
| VizieR export hashes; file paths (A1, A2, B1) | **no change:** the content hashes match; an artefact of the packet layout. |
| "Record-pair locator" fields absent from rows.json (A3) | **no change:** an artefact of the packet layout; per-input locators resolve it. |

## Dwarfs

| Point | Outcome |
|---|---|
| Andromeda XVI: four moduli and no column named (A1, B1) | **change:** §4 names the PWR column, with the paper's adoption statement (Martínez-Vázquez 2017 p. 17). |
| Higgs e is defined from second moments, not as 1 − b/a; R_s axis (A2, B3) | **change:** §4 "Ellipticity conventions" says e is used as printed, with its definition (Higgs eq. 4) and that R_s is semi-major. Both were checked in the PDF. |
| Higgs ε table (A2, B3) | **already:** D-121, #243. |
| "(cited)" undefined; which modulus goes with M_V (B2) | **change:** §3 step 4 defines "(own)" and "(cited)", and names the paper per system, including the three exceptions of D-121. |
| Munoz 2018 Tables 6 and 1 have no page (A) | **change:** PDF p. 28 and p. 22 added. |
| Munoz 2018 ellipticity column not named (B7) | **change:** ε_s of Table 5 (PDF p. 27), checked in the PDF. |
| Fornax: which radius row (B6) | **change:** "2D Half-light r_h" (l. 106) and "Ellipticity" (l. 97), Sérsic column (20.1′, 0.31), checked in the TeX. |
| σ text names other papers' arXiv IDs (A, B4) | **already:** fixed by #248 (D-122). |
| Gas locators "Table 1, None" (A) | **already:** #232, fixed in the v3 locators. |
| Kvasova Table 2 column layout (B5) | **no change:** the value was confirmed against Table 4 and §4.1 by the reader; the locator names the column. |
| Boötes III "Tidally Disrupting" (A) | **already:** a D-097 finding, recorded and not plotted (`v2/reading/resolutions.md`). The packet did not hold the register. |
| VOTable export hash (A) | **no change:** the content hash matches. |
