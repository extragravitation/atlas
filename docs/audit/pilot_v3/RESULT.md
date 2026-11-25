# Pilot result (D-118): part 1, X-COP and strong lenses

**Status.** Part 1 is done: the two packages whose source files the workspace can reach. The other four packages (SPARC, KiDS-1000, globular clusters, dwarfs) wait for their hosts to be allowed or their files to be supplied. Each reader's own files are in `readers/<A|B>/<package>/`.

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
