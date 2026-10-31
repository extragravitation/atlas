# aeg-d-dwarfs/v1: brief for reading the gas (Putman et al. 2021, ApJ 913, 53)

Written 2026-10-31, before any value was read. Every reader gets this file verbatim. Two independent readings are compared by script.

**Source.** The journal machine-readable Table 1, "Dwarf Galaxies within 2 Mpc: Positions and HI Parameters". Its byte-by-byte description and notes are in the file header.

**Task.** For each system on the sheet, find its row by galaxy name. Use the coordinates only to confirm. If a system is not in the table, write one row saying so. Copy, as stored:

`Galaxy`, `f_Galaxy`, `Vel`, `Dist`, `e_Dist`, `E_Dist`, `Data`, `Method`, `sigHI`, `l_MHI`, `MHI`, `e_MHI`, `E_MHI`, `r_Dist`

Also copy the full text of the header's Notes (1)–(5) once, in a separate file.

Output columns: `key`, `galaxy_as_printed`, then the fields above, then `identification_note`.

**Rules.** Compute nothing. Use no other source and no memory. Do not open any other reader's work.
