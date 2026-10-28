# aeg-d-kids1000-rar/v1 — reproduction result

**Result: PASSED** (first run, 2026-10-28, data workflow run on commit `b4e0398`). `REPRODUCTION.md` (SHA-256 `71bcf439…`) unchanged.

| Check | Outcome |
|---|---|
| Frozen-file hash | pass |
| 1. Completeness: every row of the three in-scope ESD files once, nothing else (45 measurements) | pass |
| 2. g_bar equals the released first column | pass |
| 3. g_obs and its error within 0.001 dex of the README recipe with the README's constants | pass |
| 4. Covariance (675 entries) converted exactly; symmetric; positive diagonal | pass |
| 5. Package constants within 0.25 % of the README's | pass |

**Scope of this result (as stated in `REPRODUCTION.md`):** the paper publishes no tables, so this establishes that the package follows the authors' documented method exactly. It does not independently verify the authors' figures.
