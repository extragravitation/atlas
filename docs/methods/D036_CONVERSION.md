# D-036 (ii): light-weighted dispersion from a binned profile — frozen specification

**Frozen 2026-10-29, before any real dispersion profile was opened** (issue #46). Code: `pipeline/aeg/dispersion.py`; tests on synthetic profiles: `pipeline/tests/test_dispersion.py`. Hashes in `data/frozen/d036-conversion.json`; `python -m aeg.check` fails if either file changes. A change needs a new version (new files, new freeze record, logged decision), applied only to later cases.

## What it computes

For a source's binned line-of-sight dispersion profile (D-036 ii; the second moment where the source gives it, D-038 2A):

    <σ²_los> = Σ wᵢ σᵢ² / Σ wᵢ,     σ_rms = √<σ²_los>

with wᵢ the fraction of the system's total light in bin i, from the closed-form cumulative light of the source's own or a cited structural model. **Coverage** = Σ wᵢ, the fraction of total light inside the bins. The value is **plotted only if coverage ≥ 0.80**; otherwise it is recorded, not plotted. Coverage is shown either way.

## Fixed choices (no free parameters)

| Item | Rule |
|---|---|
| Structural models | Plummer (a); King 1962 (r_c, r_t); Sérsic (R_e, n; exponential = n 1). Closed forms; standard-library code only. Tabulated surface-brightness profiles are not supported in this version. |
| Bins | Annuli [r_in, r_out) in the model's radial unit and radius definition; no overlaps; gaps allowed and not counted as covered. |
| Edges not given | Midpoints between adjacent representative radii; innermost from 0; outermost to r_n + (r_n − r_{n−1})/2. Flagged `edges_inferred` and shown. |
| Errors | Bins independent; lower and upper errors on <σ²> propagated separately in quadrature; asymmetric errors kept. Structural-model uncertainty not propagated (stated as a known limitation on the page). |
| Limits | Any bin given as a limit: the conversion refuses; the system is recorded, not converted. |
| Inputs that are refused | Overlapping bins, empty input, negative or non-finite values, bins with no light. |

## Tests (synthetic, known answers)

Closed forms checked against an independent numerical integrator (Plummer, King 1962, Sérsic n = 4); the incomplete-gamma routine against P(1,x), P(2,x) and erf; Sérsic half-light and exponential identities; constant σ returns itself; equal-light bins average σ²; known three-bin weights; the 0.80 boundary on both sides; gaps; a central-only profile is not plotted; order independence; error propagation against a 200 000-draw Monte Carlo; asymmetric errors; inferred edges; every refusal path.

Result at freeze: all tests pass.

## Not decided here

Which structural model and parameters apply to each system is read at source per system and recorded in its package; distances are never kinematic (D-036 #6).
