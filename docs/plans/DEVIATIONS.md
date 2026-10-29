# Deviations register (selection protocol, D-028)

Departures from the frozen selection protocol (`docs/plans/SELECTION_PROTOCOL.md`, frozen at commit 817bc5a, recorded in `data/taxonomy.json`). Each entry: date, cell, what changed, why, and the data seen at the time. The frozen documents are not edited; this file is the record.

| # | Date | Cell | Deviation | Why | Data seen at the time |
|---|---|---|---|---|---|
| 1 | 2026-10-29 | all | The protocol's status line still reads "draft, not frozen"; the freeze is recorded in `data/taxonomy.json` (merge of PR #35, 2026-10-29 11:37 MDT). The A0, A3 and A5 searches started after that freeze. | The status line could not be changed without changing the frozen hash. | None. |
| 2 | 2026-10-29 | A0, A3, A5 | §3 steps 1–3 (ADS, VizieR keyword search, Zenodo and GitHub search) could not be run directly: those services are not reachable from the build environment. Queries were run through a general web search instead, recorded verbatim. | Environment limitation. Remedy pending JvH: run the ADS and VizieR steps through a browser on JvH's computer, and add their results to the logs. | Metadata, documentation and methods sections only; no data tables opened; no results seen. |
