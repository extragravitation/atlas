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

No packages exist yet.
