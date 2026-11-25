# Pilot result (D-118)

**Status.** The pilot is complete: 12 rows, two per package, and two readers each, 16 readers in all. Part 1 covered X-COP and the lenses. Part 2 covered SPARC, KiDS-1000, the globular clusters and the dwarfs; it ran after JvH allowed the source hosts, and every file was fetched and verified in the workspace. Each reader's own files are in `readers/<A|B>/<package>/`.

**Disclosure.**
- **Packet builder changed after packets were built.** The packets for part 1 were built before two fixes to `build_packets_v3.py`. Locator templates were left unfilled (`{column}`), and VizieR exports were checked by their whole-file hash. These are listed in "Packet builder" below. The fixes were committed before any reader output was opened.
- **Readers' instructions.** The readers were fresh agents, told to work only in their own folder.

## Values

All four readers reproduced every value within tolerance:
- **X-COP** (m000001, m000078): both readers' values are identical to the Atlas rows.
- **Lenses** (m000021, m000101): both readers agree with the Atlas rows to all five printed digits, which is better than 0.0001 dex.

No discrepancy.

## Method gaps reported, and what was done

| Gap (readers) | Done |
|---|---|
| X-COP: which FITS HDU (A, B) | Stated: HDU 1 |
| X-COP: row counting, and how measurement identifiers map to files and rows (A, B) | Stated: rows counted from 1 in stored order; the identifiers follow the files in a stated order with their row counts |
| X-COP: unit strings `m/s^2` and "m s⁻²" (A, B); "four" accelerations when there are five columns (A) | Stated: `m/s^2` is m s⁻²; five columns |
| X-COP: error form cited to a file not in the packet (A, B) | Stated in the text: errors are magnitudes; confidence level not stated by the source |
| X-COP: precision of stored values (A, B) | Stated: 32-bit floats, used as stored |
| X-COP: whether RADIUS is three-dimensional; which method the released GOBS comes from (B) | Stated as the source leaves it: the file does not say. The paper uses two methods and does not say which one the column holds. The methods page had said "the source's nonparametric g_obs", which overstated the source; corrected |
| X-COP: line 263 is in §3.5, not §3.4; the dynamical mass-to-light statement is at l. 101–112, not l. 456 (A, B) | Methods page corrected. The same two errors are in the package's own `source_ref` text: they need a ruling (proposed D-119) |
| X-COP: line numbering; e-print is a gzipped tar (A, B) | Stated: physical lines from 1 |
| Lenses: R10's cosmology paper not in the packet (A, B) | Packet builder fixed: every source of the same reading record is now included |
| Lenses: which input feeds which step; observables not in the packet (A, B) | Packet builder fixed: each input now carries its quantity name, never its value |
| Lenses: units of `MChaBC2`; its printed precision (A, B) | Stated: 10¹⁰ M☉, used as printed |
| Lenses: θ_E axis convention; R_eff not circularised; b_n tolerance; radians; H₀ in s⁻¹ (A, B) | Stated |
| Lenses: unused inputs (R_e, MSalBC2, R13's own z and θ_E) (A, B) | Stated what each is for and that it is not used in the value |
| Lenses: which field marks a redshift spectroscopic; which z_l the cut uses; no grade or kind rule stated (A, B) | Stated: the rules of §4, including the early-type and grade-A rule the page had left out |
| Lenses: name matching across records (A) | Stated: by J-coordinate name |
| Both: VizieR content hash (A, B) | Already in the builder; the readers confirmed the content hashes |

## Packet builder

- **Locator templates** (`{column}`, `{row}`) are now filled from the rule's match.
- **File checks:** files are verified exactly as `aeg.fetch` verifies them. VizieR exports are matched by content hash, and other VizieR mirrors are tried only on that hash.
- **Same-record sources:** sources of the same reading record are included.
- **Quantity names:** each input carries its quantity name.
- **Unreachable hosts.** Found while building, not by the readers:
  - The workspace cannot reach the SPARC, KiDS, Baumgardt, Harris and IDIA VizieR hosts.
  - The other VizieR mirrors give different content bytes for the IDIA exports, so they cannot replace them.


# Part 2: SPARC, KiDS-1000, globular clusters, dwarfs

**Packets:** built after the part 1 builder fixes, from commit `ea789b7`. Every file was found and verified.

## Values

All eight readers reproduced every value; no discrepancy:
- **SPARC** (m000669, m001593): identical to the Atlas rows, to all printed digits.
- **KiDS-1000** (m000003, m000012): identical, including which row is plotted.
- **Globular clusters** (m000066, m000020): within 0.00001 dex. Both readers wrote their own King (1966) integration from the text. Both reproduced the source's own concentration (`Conc`) for both clusters.
- **Dwarfs** (m000053 Reticulum III, an upper limit; m000014 Andromeda XVII): within 0.00001 dex.

## Method gaps reported, and what was done

| Gap (readers) | Done |
|---|---|
| SPARC: where data-row counting starts; how a galaxy's Table 1 row is found (A, B) | Stated: after the last line of dashes; by the galaxy's name |
| SPARC: Table 1's header byte positions do not fit its data lines (A, B) | Checked at source: the lines are 131 bytes, but the header describes 113. Stated: read by white space |
| SPARC: which distance; which columns are δi and δD; `g_bar_gas` vs `g_bar_gas_cold`; unused inputs `SBdisk`, `SBbul`, `f_D` (A, B) | Stated |
| SPARC: the quote "as suggested by SPS models" does not support Υ_disk = 0.5 in the cited paper (B) | Checked: the cited paper says "as suggested by stellar population models" (l. 29) and gives Υ_bul = 1.4 Υ_disk (l. 261). The quote came from a second paper. Corrected to cite those lines |
| SPARC: the uncertainty formula cites a paper not in the packet (A, B) | Stated as cited, not supplied. It does not enter g |
| KiDS: comment marker; identifier-to-row mapping (A, B) | Stated: lines beginning `#`; the identifiers in three blocks of 15. A first draft gave the wrong block order; the test caught it before commit |
| KiDS: README constants differ; h₇₀ scaling; the header calls g_bar "Radius" (A, B) | Stated |
| KiDS: the isolation limit also appears as g_bar < 10⁻¹³ m s⁻² (l. 595), which would also drop row 9 (B) | Checked at source. Stated: the Atlas follows the paper's count of seven points (l. 508), by row number. Known issue #169 covers the paper's inconsistent limit |
| Globular clusters: how to read `veldis.html` (where a cluster's rows end, spacer rows); how to read `mwgc.dat` (fixed width, blank names); the Harris lookup was given as code (A, B) | Stated as rules |
| Globular clusters: King integration start values, ρ for W ≤ 0, F at R/r₀, the projection grid (A, B) | Stated, with the `Conc` check |
| Globular clusters: unused inputs (`V_t`, `(M/L)2`, Δσ); which M/L column (A, B) | Stated |
| Globular clusters: the packet hides each bin's radius, because it is an input value (A) | Kept, as the plan requires. Stated: every row of the chosen Type is a bin, sorted by radius |
| **Dwarfs: the source of M_V on a "M_V + (m − M)" route was not named, and 11 candidate papers were listed (A, B)** | **The one gap that would have slowed a stranger most.** The per-system table now names the paper, table and row of M_V, and which modulus is added, from the structure reading |
| Dwarfs: σ and [Fe/H] places pointed to selection files not in the packet; which [Fe/H] (mean or median, spectroscopic or photometric) (B) | The per-system table now gives the page, table and row of σ, and of [Fe/H] with its quantity and kind, from the reading records |
| Dwarfs: modulus or printed distance when a paper prints both; ellipticity given only as an upper limit; duplicate [Fe/H] rows in the Υ table; how the `MW` prefix is matched; page numbering; rounding order (A, B) | Stated |

**New tests.** `test_stated_identifier_mappings` checks the identifier-to-row mappings now stated for SPARC, KiDS and X-COP.
