# Search log: gas inside the Einstein radius of early-type galaxies (D-075 item 1)

> Purpose: find **measured** gas masses (hot X-ray gas, atomic HI, molecular gas) inside about the effective radius of early-type galaxies, so the A6 gas term rests on quoted measurements (A6S precedence §3.4; protocol §1.7). Run by Claude for JvH. Read at source; nothing from memory.

## 0. Plan, committed before any query is run (2026-11-01)

### 0a. What counts
- A **measurement** of the gas mass, or a measured upper limit, inside a stated radius of the order of the effective radius R_e or a few kpc, for named early-type galaxies or a defined sample of them. It can be per galaxy, or given as a fraction of the stellar mass in the same radius.
- Each of the three phases separately: hot (X-ray, deprojected gas density or mass profiles), atomic (HI), molecular (CO-based H₂, conversion factor stated).
- Massive early-types (stellar masses comparable to the A6 lenses) are preferred, and the mass range is recorded.
- **Not eligible:**
  - whole-galaxy totals with no radius;
  - simulations;
  - gas masses inferred from dynamics or lensing;
  - review statements without a cited measurement (the cited measurement is read instead).

### 0b. Queries, verbatim

| # | Query (ADS, through JvH's Chrome) | Sort |
|---|---|---|
| ADS-G6-1 | `abs:("elliptical galaxies" OR "early-type galaxies") abs:("hot gas" OR "X-ray" OR "hot interstellar medium") abs:("gas mass" OR "gas fraction" OR "mass profile" OR "density profile") abs:(Chandra OR XMM) collection:astronomy property:refereed year:1995-2026` | citations |
| ADS-G6-2 | `abs:("early-type galaxies" OR "elliptical galaxies") abs:("molecular gas" OR "CO" OR "HI" OR "atomic gas") abs:("gas mass" OR "gas fraction" OR "upper limit" OR "detection rate") collection:astronomy property:refereed year:1995-2026` | citations |
| ADS-G6-3 | `abs:("strong lens" OR "lens galaxy" OR "lens galaxies") abs:(gas OR "interstellar medium" OR "X-ray") collection:astronomy property:refereed year:1995-2026` | citations |
| CIT-G6 | The measurement papers cited by the gas statements already read (inventory §4 and adjudication §5), read at source | — |

Fallback if ADS is unreachable: the same terms with WebSearch, with the result lists recorded verbatim.

### 0c. Screening and output
1. Title screening by Claude; exclusions counted.
2. Two independent readers, in separate folders, read the candidates to a committed brief. They record the phase, radius, measured quantity (value or limit, with location and quote), sample, galaxy stellar-mass range and method.
3. The result goes to JvH: per phase, the measurements that apply inside about R_E, and a proposed default and range for the A6 gas term (fraction of the stellar mass inside R_E, by phase, summed). It is registered as an assumption with a slider.
