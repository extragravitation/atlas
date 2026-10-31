# D-053: resolving compilation entries with several originals — frozen

**Frozen 2026-10-30, before any value in the originals is read.** The hashes of this file and of `data/packages/aeg-d-dwarfs/v1/reproduction/resolve_compilation.py` are in `data/frozen/d053-compilation-originals.json`.

## Inputs

- `reading/mcconnachie2012_originals.csv`: per (system, quantity), the originals McConnachie 2012 lists.
- The two-reader readings of those originals:
  - `reading/mcc_structure_values.csv`, read under `STRUCTURE_READING_BRIEF.md`;
  - `reading/mcc_sigma_values.csv`, read under `SIGMA_READING_BRIEF.md`.
- The two-reader readings of McConnachie 2012 itself, already in `reading/structure_values_all.csv` and `reading/sigma_values.csv`.

## Quantities matched

| Compilation quantity | Reading quantity |
|---|---|
| Apparent V | `m_v` |
| Structure | `r_h`, `ellipticity`, `pa` |
| Distance | `distance_modulus` |
| Dispersion | `sigma` |

The "M_V distance-modulus component" rows are not used: the Atlas applies its own distance (D-052 item 4).

## Steps, per (system, quantity)

1. **Printers.** A candidate *prints* the quantity if its reading has a row for it with a value that is not marked quoted from another paper.
2. **One printer.** It is used.
3. **Several printers.** Each candidate value is rounded to the number of decimals of McConnachie's printed value. A candidate whose rounded value equals McConnachie's printed value *matches*.
   - Exactly one candidate matches: it is used, with the matching locations recorded.
   - Several candidates match: the most recent of them is used, flagged.
   - None matches: go to step 5.
4. **Within one candidate.** Values are compared in the order the D-052 selection uses: headline, then abstract, then the rest. The first that matches counts.
5. **No match, or no McConnachie value read:** the most recent candidate that prints the quantity is used, flagged `no_match`.
6. **Centre.** The structure original's printed centre, else the discovery paper's.

## Output

`reading/mcc_resolution.csv`: per (system, quantity), the original chosen, how it was chosen, the matching locations and the flags.
