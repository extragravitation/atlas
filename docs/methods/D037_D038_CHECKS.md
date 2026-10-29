# D-037 reproduction check and D-038 3A consistency check — frozen specification

**Frozen 2026-10-29, before any velocity file or dispersion value was opened** (issue #47). Code: `pipeline/aeg/repro_dispersion.py`; synthetic tests: `pipeline/tests/test_repro_dispersion.py`; hashes in `data/frozen/d037-d038-checks.json`, enforced by `python -m aeg.check`. Changes need a new version and a logged decision, applied only to later cases.

## Reproduction check (D-037)

Where a source releases per-star line-of-sight velocities and publishes a dispersion from them. The **published value is the one shown**; the recomputed value is never plotted in its place. The outcome (pass, fail or not testable, with the numbers) is published for every system.

| Step | Rule |
|---|---|
| Members | The source's member flags. Probabilities with a stated threshold: that threshold (≥). Probabilities without one: p > 0.5. Stars the source flags as binaries or velocity variables are excluded. A radial selection stated by the source for its published value is applied. If membership cannot be reproduced from the release: **not testable**. |
| Estimator | Maximum likelihood for a Gaussian with per-star errors, L = Π N(vᵢ \| μ, σ² + eᵢ²), μ profiled out, σ ≥ 0. 68% interval where 2(ln L_max − ln L(σ)) ≤ 1. No binary model, no clipping beyond the source's membership, no rotation model (dispersion about the sample mean). |
| Pass | **Pass** if the recomputed value lies inside the published 68% interval [σ − lo, σ + hi]; otherwise **fail**. Published upper limit only: pass if the recomputed value is at or below it. Fewer than 3 members: **not testable**. |
| Method differences | Where the published value removes rotation or a gradient, or models binaries, that is recorded with the result; the test still runs and is reported. |

## Consistency check, originals vs Geha et al. 2026 (D-038 3A)

| Step | Rule |
|---|---|
| Per system | z = (σ_G − σ_O) / √(err_G² + err_O²), each error the half-width on the side facing the other value. Consistent if \|z\| ≤ 2. Many pairs share raw spectra, so z is approximate; stated with the result. |
| Limits | A measured value and a limit agree if the value's lower interval edge is at or below the limit; two limits always agree; no z. |
| Population | **Consistent** if at most 10% of pairs with a z have \|z\| > 2 and the median z lies in [−0.5, +0.5]; otherwise **inconsistent**. Fewer than 5 pairs with a z: per-system results only. |
| Selections | No adjustment for differing radial selections (Geha: within 2 r½, extended for some clusters); each source's selection is recorded with the result. |

## Tests (synthetic, known answers)

ML equals the sample standard deviation when errors vanish; recovery of a known σ with uneven errors; the reported value is the likelihood maximum and the interval edges sit at Δ(2 ln L) = 1; interval coverage near 68% over 400 simulated samples; σ = 0 when the scatter is below the errors; membership rules (flags, binaries, probabilities with and without a threshold, radial cut); pass, fail, asymmetric intervals, upper limits and not-testable paths; a source using this exact estimator always passes; consistency z with facing errors, limits, and all population outcomes.

Result at freeze: all tests pass.
