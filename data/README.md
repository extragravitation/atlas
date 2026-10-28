# Data

## System-ID registry

`registry/systems.csv` assigns every astronomical system its permanent ID (`aeg-s-000001`, decision D-006). Rules, enforced by `python -m aeg.check`:

- IDs are assigned once, in sequence, and never reused, renumbered or removed.
- Names and cross-identifications are stored alongside the ID, never encoded in it.
- `first_dataset` records the dataset version that introduced the system (e.g. `aeg-d-sparc/v1`).

The registry's columns are a first draft. They will be frozen together with the data standard (master plan §2–4) before any data are committed.

## Dataset packages

`packages/<dataset-name>/<version>/` (e.g. `packages/aeg-d-sparc/v1/`), one folder per dataset version, following the Frictionless Data Package standard. Each holds the metadata, the conversion script, the converted tables, and a hash-frozen reproduction test written before the conversion is run (decision D-005).

Source files are downloaded at build time and verified by checksum. They are never committed (see `.gitignore`), and files that may not be redistributed never enter the repository.

A released dataset version is never changed. A change is a new version.

First package: `aeg-d-sparc/v1`.

## How packages are built and checked

The `data` workflow (`.github/workflows/data.yml`) runs on every pull request that touches `data/` or `pipeline/`:

1. **Fetch** every package's sources from their published addresses and verify size and SHA-256 (`python -m aeg.fetch`). Sources are never committed or uploaded.
2. **Build** each package (`convert.py`), which writes the tables, `datapackage.json` and `checksums.sha256`.
3. **Test** each package: the frozen reproduction test, conversion integrity, and the data standard (`aeg.validate`).
4. **Check slider formulas** in Python and JavaScript on every measurement (`python -m aeg.formula_check`).
5. **Compare** the committed tables with the regenerated ones. On a pull request they are committed back to the branch by the workflow if they differ; on `main` a difference fails.

GitHub holds commits made by the workflow for manual approval before running checks on them. To avoid that, after editing any committed file in a package, refresh its checksums before committing: `python -m aeg.package checksums data/packages/<dataset>/<version>`. A later commit by a maintainer also runs the checks normally.
