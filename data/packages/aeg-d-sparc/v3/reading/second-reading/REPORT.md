# SPARC second reading — report

Returned by the second reader (an independent agent session, 2026-11-01). The session could not write `.md` files, so Claude saved the text verbatim, apart from this header. The CSVs and scripts beside it are the reader's own files, copied unchanged.

Script: `/tmp/claude-0/sr-sparc/parse_sparc.py` (run as `python3 -I parse_sparc.py input out` from that folder). Diagnostics: `profile.py` (per-byte column occupancy), `spans.py` (byte span of each whitespace-separated value).

## Input SHA-256
- `MassModels_Lelli2016c.mrt` (269518 bytes): `9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c`
- `SPARC_Lelli2016c.mrt` (28259 bytes): `5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243`

## Row counts
- `massmodels.csv`: 3391 rows. The file has 3416 lines: 25 header lines and 3391 data lines. There are 175 galaxies, each in one contiguous block.
- `galaxies.csv`: 175 rows. The file has 273 lines: 98 header and notes lines and 175 data lines.
- Both files list the same galaxies in the same order.

## Format notes
- Line endings: MassModels uses CRLF and has 77-byte data lines. The SPARC table uses LF and has 131-byte data lines. Both files are ASCII with no tabs.
- File names in the headers: MassModels calls itself `datafile2.txt`; the SPARC table calls itself `Table1.mrt`.
- Galaxy names: left-justified in MassModels, right-justified in the SPARC table. They match exactly once the padding is stripped.

## Header vs data

**MassModels: no disagreement.** The header byte ranges match the data:

| Field | Bytes |
|---|---|
| ID | 1-11 |
| D | 13-18 |
| R | 20-25 |
| Vobs | 27-32 |
| e_Vobs | 34-38 |
| Vgas | 40-45 |
| Vdisk | 47-52 |
| Vbul | 54-59 |
| SBdisk | 61-67 |
| SBbul | 69-76 |

- The gap bytes (12, 19, 26, 33, 39, 46, 53, 60, 68) are blank in all 3391 rows.
- In every row, the whitespace-separated values equal the fixed-width fields.
- Format note: D is declared F6.2, but 2470 rows print it with fewer than 2 decimals. Those values are copied as printed. Numerically, D equals the SPARC-table D for every row.

**SPARC table: the header byte positions are wrong.**

What disagrees:
- The header ranges are contiguous with no separator bytes: Galaxy 1-11, T 12-13, D 14-19, …, Ref 100-113, for 113 bytes in total.
- The data lines are 131 bytes long.
- Applied as written, the header ranges give wrong values for every field after Galaxy, in all 175 rows.

How I resolved it:
- Every data line has exactly 19 whitespace-separated values, matching the 19 header fields. Ref never contains a space.
- The measured byte spans fit exactly one layout. The header's widths and field order are right, but each field is followed by one blank byte that the header ranges omit. Field *k* (Galaxy = 0) is therefore shifted right by *k* bytes, giving 113 + 18 = 131 bytes.
- I checked this layout on all 175 rows with zero exceptions:
  - every separator byte is blank;
  - every field is non-empty and matches its declared I or F format, including the number of decimals;
  - nothing appears after byte 131;
  - the whitespace-separated values equal the fixed-width fields.

Actual byte positions (header range → actual):

| Field | Header bytes | Actual bytes |
|---|---|---|
| Galaxy | 1-11 | 1-11 |
| T | 12-13 | 13-14 |
| D | 14-19 | 16-21 |
| e_D | 20-24 | 23-27 |
| f_D | 25-26 | 29-30 |
| Inc | 27-30 | 32-35 |
| e_Inc | 31-34 | 37-40 |
| L[3.6] | 35-41 | 42-48 |
| e_L[3.6] | 42-48 | 50-56 |
| Reff | 49-53 | 58-62 |
| SBeff | 54-61 | 64-71 |
| Rdisk | 62-66 | 73-77 |
| SBdisk | 67-74 | 79-86 |
| MHI | 75-81 | 88-94 |
| RHI | 82-86 | 96-100 |
| Vflat | 87-91 | 102-106 |
| e_Vflat | 92-96 | 108-112 |
| Q | 97-99 | 114-116 |
| Ref | 100-113 | 118-131 |

Output column names: L36 is L[3.6], e_L36 is e_L[3.6], and SBdisk0 is the header's SBdisk (disk central surface brightness).

Not verified against the paper: this session's allowlist blocked fetching arXiv:1606.09251, so the resolution rests on the data alone. I consider it unambiguous. Checking it against the paper or the VizieR ReadMe (J/AJ/152/157) is still outstanding.

## Anything not read
- No data byte failed to parse, and no field was empty.
- Zero entries (for example Vflat/e_Vflat `0.0`, RHI `0.00`) are copied as printed. I did not interpret them as "not measured"; that question is left to the primary reader or the paper.

## Output conventions
- CSV with comma separators, LF line endings and one header line.
- Each value is the printed text with only the blank padding removed.
- `row` in `massmodels.csv` counts data rows from 1, in file order.
