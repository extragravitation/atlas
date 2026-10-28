# Atlas of Extra Gravitation

*The acceleration discrepancy, from star clusters to galaxy clusters.*

The Atlas describes where and how the observed gravitational acceleration (g_obs) exceeds what Newtonian gravity predicts from detected baryonic matter (g_bar). It is a field guide, not an argument: it takes no side between the competing accounts of the discrepancy, and every number traces to a published source.

**Status:** pre-release. Building toward v0.1. No data have been released yet.

## Principles

- Describe observations; never assume a cause.
- Baseline: Newtonian gravity acting on detected baryonic matter.
- Dynamics and lensing are separate channels, never merged by default.
- Every number traces to a published source, with citation, licence, method, assumptions, units and file hash.
- Assumptions are shown with published ranges; their effects are computed from the data.
- Tests and predictions are frozen by hash before data are seen.

## Layout

| Folder | Contents |
|---|---|
| `data/` | Dataset packages (one folder per dataset version) and the system-ID registry |
| `pipeline/` | Python code that builds and checks every package (`aeg` package and tests) |
| `site/` | The static website (to come) |
| `docs/` | Decision log and project documentation |

## Identifiers

Permanent once published (see `docs/decisions.md`, D-006):

- Systems: `aeg-s-000001`
- Datasets: `aeg-d-<short-name>/v1`
- Measurements: `aeg-d-<short-name>/v1/m000001`

## Licences

- Code: MIT (`LICENSE`).
- Text, figures and Atlas-produced data tables: CC BY 4.0 (`LICENSE-CONTENT.md`), except where a source's terms govern a table; each dataset page states which.

## Authorship

The Atlas's framework, structure and purpose are John van Hemert's. Coding, research and data compilation use AI assistance (Claude, by Anthropic), under his direction and rulings.

## Checks

```
pip install -e "pipeline[test]"
pytest pipeline/tests
python -m aeg.check
```

Every pull request runs these automatically.
