# D-049: the basis of a dwarf-galaxy label, version 2 — frozen rule

**Frozen 2026-10-30, before any velocity dispersion, structural value or luminosity of an A5 candidate was opened.** It replaces `docs/methods/D048_KIND_BASIS.md` (version 1), which stays frozen with its literal result on record (`aeg-d-dwarfs/v1/reading/kinds_v1.csv`). Version 2 was written **after** the version 1 coding was seen, and before any acceleration. D-049 therefore goes to the outside reader at the v1.0 review (D-031 item 2).

Everything in version 1 holds, except the four changes below.

## 1. What counts as X

A paper is coded **X** only if it:
- calls the system a star cluster; or
- **concludes** that its kind is undetermined, for example "we cannot tell whether it is a galaxy or a cluster", or "a stellar system of a new kind".

A galaxy label that is hedged ("likely", "probable", "candidate"), or provisional pending spectroscopy, is coded by the grounds the paper gives (L, P, G, D, M or N), not X. On the existing sheets: the Milky Way coder's subtypes `X(cluster)` and `X(open)` remain X; `X(provisional)` is not X, and the row keeps its other codes. A provisional row whose only code was X is re-coded from the paper by its grounds.

## 2. Supersession

An X counts unless a **later** paper in the evidence set gives the kind on ground L, P or G. Papers are ordered by publication year, taken from the reference key.
- If the later papers give only D, M or N, the X stands and the system is A7.
- An earlier paper with L does not supersede a later X.

## 3. Evidence set

As version 1 (the discovery papers and the first-dispersion paper), plus two additions:
- **Pre-arXiv papers** are read as scans on NASA ADS (articles.adsabs.harvard.edu) through JvH's browser, and coded like the others. A paper that cannot be reached by any route stays "unread" and contributes nothing.
- **Systems with no discovery reference** (naked-eye or catalogue objects: LMC, SMC, M32, NGC 205, Cassiopeia II) add their structural reference (LVDB `ref_structure`) to the evidence set.

## 4. Re-coding and double coding

The sheets are re-coded under items 1–3 by the same rule, and the 20% sample (same keys) is re-coded by a second reader who does not see the first. The agreement rate is published with that of version 1.

## Rule, in full (mechanical)

1. **A7** if an X stands after supersession.
2. Otherwise **A5** if any paper read gives L, P or G.
3. Otherwise **A7** ("galaxy label rests on dynamics or metallicity spread only", or "no stated ground").

## D-049a: first naming, and freeze

**Ruled 2026-10-30 13:47 MDT (after the version 2 result; before any acceleration).**

5. **First naming.** For every system that items 1–4 place in A7, the evidence set adds one more paper: **the earliest paper that calls the system a galaxy** (any wording: galaxy, dwarf galaxy, dSph, dE, dIrr, Sculptor-type system, extragalactic system or nebula). It is coded by the grounds it gives, like any other paper, and it supersedes an earlier X if it gives L, P or G (item 2).
   - The reader looks for the first naming only, not for favourable grounds. The search is logged: queries, the candidates found and why the earliest was chosen.
   - If the first naming rests on D or M, the system stays A7.
   - If no paper calls it a galaxy, the system stays A7.
6. **Readers.** arXiv-era papers are read by an independent agent. Pre-arXiv papers are read as ADS scans in JvH's browser by the main session, which also runs the conversion. This is disclosed, and a second reader checks a sample of the scan readings. Systems already in A5 are not re-examined: adding a first-naming paper cannot remove an L, P or G ground.
7. **No version 3.** This rule is frozen with this section. Whatever it produces is published with its reasons. Later disagreement with a placement is recorded as a known issue and returned to the outside reader; it never triggers a change applied to this package.
