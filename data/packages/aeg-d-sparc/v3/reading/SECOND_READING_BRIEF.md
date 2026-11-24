# aeg-d-sparc/v2 — second reading brief (D-031 item 3; REPRODUCTION.md test 11)

Committed before the reading is opened. Given verbatim to the reader.

> You are the independent second reader of two public SPARC data files (Lelli, McGaugh & Schombert 2016, AJ 152, 157; arXiv:1606.09251). Work only in your folder, `/tmp/claude-0/sr-sparc/`. The files are in `input/`: `MassModels_Lelli2016c.mrt` and `SPARC_Lelli2016c.mrt`. Do not open, search or read anything under `/home/claude/` or any other copy of these data. Do not look for anyone else's parser or readings. You may read the SPARC paper on arXiv (1606.09251) to understand the columns.
>
> 1. Read each file's own header (title, byte-by-byte description, notes) and write your own parser from it. If the header and the data disagree, do not guess silently. Find out from the data and the paper what the true layout is, and report exactly what disagreed and how you resolved it, with byte positions.
> 2. From `MassModels_Lelli2016c.mrt`, write `out/massmodels.csv` with one row per data row, in file order, and the columns: row (1-based, data rows only), galaxy, D_Mpc, R_kpc, Vobs, e_Vobs, Vgas, Vdisk, Vbul, SBdisk, SBbul. Copy each value exactly as printed (as text, keeping the printed digits).
> 3. From `SPARC_Lelli2016c.mrt`, write `out/galaxies.csv` with one row per galaxy, in file order, and the columns: galaxy, T, D_Mpc, e_D, f_D, Inc, e_Inc, L36, e_L36, Reff, SBeff, Rdisk, SBdisk0, MHI, RHI, Vflat, e_Vflat, Q, Ref. Again copy the printed text.
> 4. Write `out/REPORT.md` with: the row counts; the header issue and its resolution; anything you could not read, and why; and the SHA-256 of both input files.
>
> Report back only that you are done and the row counts. Do not summarise any values.
