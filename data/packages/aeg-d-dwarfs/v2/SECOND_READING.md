# aeg-d-dwarfs/v2: independent second reading (D-031 item 3; REPRODUCTION.md item 11)

- **Readers.** Two independent agent sessions (readers A and B, Claude), 2026-11-04. Neither had access to the conversion code, v1's g values, any v2 table or the other reader's file.
- **Brief.** `reading/BRIEF.md`, with the g-free manifests `reading/manifest_rows.csv`, `manifest_observables.csv` and `manifest_systems.csv`, committed before the readings started.
- **Readings.** `reading/reader-A.csv` and `reading/reader-B.csv`.
- **Resolution.** A third session, which had seen no v2 value (none existed), compared the two readings field by field and resolved every difference at source: `reading/resolved.csv` and `reading/resolutions.md` (scripts `reading/resolve_build.py`, `reading/resolve_statements.py`).
- **Rulings applied before conversion.** D-098 (Phoenix II), D-100 (D-097 classes), D-101 (Fornax), D-102 (Tollerud 2012 velocity windows; Tucana V). No row awaited a ruling when the reading was frozen.
- **Freeze.** The SHA-256 of every reading file is in `data/frozen/dwarfs-v2-reading.json` (merged in #157), and the resolved file's in `sources.json`. `convert.py` refuses to run if `reading/resolved.csv` differs from its freeze record.

The converter takes D-096 changes, D-097 classes, confidence levels and binary-screening classes only from `reading/resolved.csv`. Whether the package equals the reading on every field is scored in `REPRODUCTION_RESULT.md`, item 11.
