# D-045: King (1966) light weights and the reconstructed-binning check — frozen specification

**Frozen 2026-10-30, before any dispersion profile, velocity or structural value of the globular-cluster sources was used.** Code: `pipeline/aeg/king66.py` and `pipeline/aeg/repro_bins.py`. Synthetic tests: `pipeline/tests/test_king66.py` and `pipeline/tests/test_repro_bins.py`. Hashes are in `data/frozen/d045-king66-bins.json` and enforced by `python -m aeg.check`. The D-036 conversion (`aeg.dispersion`) and the D-037 check (`aeg.repro_dispersion`) are used unchanged. Any change needs a new version and a logged decision, and applies only to later cases.

## Conversion version 2: King (1966) light weights (D-045 item 2)

The light-weighted dispersion is computed exactly as in D-036 (ii). Version 2 adds one structural model, **King (1966)**, the lowered isothermal sphere: density ∝ e^W erf(√W) − √(4W/π)(1 + 2W/3), with the Poisson equation in units of the scale radius r₀ and c = log₁₀(r_t/r₀).

| Item | Rule |
|---|---|
| Parameters | W₀ and r₀ from McLaughlin & van der Marel (2005), King-model fit (`Mod = K`). For clusters they do not fit: Harris (2010) c and r_c, read as log₁₀(r_t/r₀) and r₀, with W₀ found from c. This reading is a registered assumption, tested in REPRODUCTION.md before any Harris-only cluster is plotted. |
| Light inside R | Projected (cylinder) light from the 3D light, which comes from the potential gradient, plus the outer shells' share inside the cylinder. |
| Numerics | RK4 in ln r, 400 steps per decade from 10⁻⁶ r₀. The trapezoidal rule is used for projections. |
| Derived radii | Tidal radius; projected half-light radius; half-power radius, where the surface brightness falls to half its central value. |

**Tests (all pass at freeze):**
- the closed form against its small-W series;
- the light from the gradient against the light integrated from the density (10⁻⁴);
- c rises with W₀;
- grid convergence against a fourfold finer grid (c to 10⁻⁴; radii to 10⁻³ relative);
- the cumulative light is 0 at the centre, 1 at r_t, and monotonic;
- the cylinder light against an independent integral of 2πR Σ(R) (2 × 10⁻³);
- the half-radii are where they claim to be;
- the half-power radius tends to r₀ for concentrated models;
- scaling with r₀;
- the c → W₀ inversion;
- the refusals;
- the model works unchanged inside the frozen D-036 conversion, including the 80% coverage rule.

The model's agreement with the published fits is the package's reproduction test, not a unit test.

## Reconstructed-binning reproduction check (D-045 item 5)

This applies the frozen D-037 check bin by bin where a source publishes a binned profile with star counts but no bin edges, and releases the per-star velocities. The first case is the Baumgardt database's line-of-sight bins of type "RV".

| Step | Rule |
|---|---|
| Members | Radial-velocity membership probability > 0.5. No probability means not a member. |
| Binaries | Probability of being single < 0.5 is excluded. No probability means the star is kept. |
| Unusable | Stars without a finite radius, velocity or error are dropped, and their number is reported. |
| Count test | The selected stars must number exactly the sum of the published bins' star counts. If not, every bin is **not testable**, and both numbers are reported. |
| Bins | Consecutive groups of the published counts, taken in order of radius (ties in file order), innermost first. |
| Test | `aeg.repro_dispersion.reproduce` per bin: pass if the recomputed value lies inside the published 68% interval. |
| Diagnostic | The rebuilt mean radius beside the published one; not part of pass or fail. |
| Label | Every result is labelled "reconstructed binning", because a fail may come from the binning rather than from the data. |

**Tests (all pass at freeze):**
- the selection rules;
- an author who used exactly this rule always passes;
- non-members and binaries do not shift the bins;
- a count mismatch gives not testable;
- a wrong published value fails;
- the result does not depend on input order;
- a bin with fewer than 3 stars is not testable.
