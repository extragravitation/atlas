# Round L adjudication (printed cluster luminosities, D-071), 2026-10-31

Prepared by Claude (AI assistance, disclosed). The readings are kept as returned (`reader-{a,b}-{S,L1,L2}.md`). The comparison (`comparison.csv`, from `compare.py`, committed before the readings were opened) matched all 104 rows: **83 agree, 21 disagree**. Each disagreement, and each agreed P, was settled by Claude reading the source where that was possible. Final codes are in `final.csv`. **Six rule questions (QL1–QL6) are for JvH.**

**Final codes:** E 8, P 10, X 79, NS 6, — 1.

## What Claude read at source

| Item | Read | Result |
|---|---|---|
| L23b erratum | ADS abstract page of 2004ApJ...611.1208G | Corrects two appendix equations; "the results in the paper remain unchanged". |
| LV3 columns | GAVO registry record ivo://CDS.VizieR/J/MNRAS/449/2345 (column list only) | Per-cluster g, r, i luminosities (B and K converted), ID, position, spectroscopic z, N. |
| L5c columns and band | GAVO record ivo://CDS.VizieR/J/A+A/461/397 (column list); arXiv:astro-ph/0606191 text | The column is "Cluster optical luminosity" with no band; the text says "The optical luminosity is computed in the i-band". The method is referred to paper I (L5a), where the count-based sum includes the BCG. |
| S13d identity | ADS abstract page of 2021ApJ...915..106C | Contini & Gu 2021, a semi-analytic model. |
| BCG statements | arXiv texts of L2 (astro-ph/9907266), L4 (astro-ph/0006397), L8 (1407.1767), S4a (1304.6061), S4b (1108.3678), S4d (0804.1102), S6 (1901.11276), S9b (1903.08813), searched for BCG, brightest, central and cD, and the luminosity-method sentences read | See the rows in `final.csv`. |

Note: CDS pages (cdsarc, vizier) are not readable from JvH's Chrome or from this workspace; the GAVO registry mirror was used for column lists.

## The three central-galaxy checks (S4a, S4b, S9b)

None of the three states the BCG's inclusion in so many words:
- **S4a:** the text discusses a "missing stellar surface brightness to BCG magnitude ratio", which treats the BCG as a separate quantity.
- **S4b:** the text has no mention of the BCG; its total is an integral of a fitted luminosity function.
- **S9b:** "the very massive central galaxies tend to dominate the total mass" of its proxy, which implies the central galaxy is in the sum.

For the stellar-mass coverage, the S9 "main rule versus strict variant" split stands until QL2 is ruled.

## Disclosures

- **Reader A, L5a:** a fetch tool volunteered one fitted scaling-relation slope and scatter. This is not a per-cluster value and is not recorded.
- **Claude, BCG searches:** while searching S4d's text, Claude saw a cited literature statement of the share of BCG plus ICL in total stellar light. It is not a per-cluster value and is not recorded or used.
- **Readers:** both reader B blocks briefly wrote outside their folder (an empty file, deleted). No reader opened another reader's folder.
- **Reader A, block L1:** first returned one row; it was sent back to finish (same reader, same brief).
- **Search-log corrections** (from the readers):
  - L24d covers A85, A2457 and IIZw108 (not A2670);
  - LV7b is the 2MRS catalogue;
  - S12b's arXiv id 2007.01084 is Ghizzardi et al. 2021, "Iron in X-COP" (A&A 646, A92), which is the X-COP stellar-mass source as screened in S9. Only the label "2020, X-COP stellar masses" was loose.

## Rule questions for JvH (recommendation first)

**QL1. May the Atlas add a source's own printed cluster-level components?**
- The question arises where a source prints, for the same cluster and the same aperture, disjoint components but no total: BCG, red members and blue members (L10); BCG+ICL and galaxies (S3a); BCG, galaxies and residual diffuse light (L23b).
- **Recommended: yes**, when the source defines the components as disjoint and they share one aperture. This is arithmetic on the source's own cluster totals, not a sum over a member catalogue (D-069), and Test 3 checks it.
- Not used: dividing a printed ICL luminosity by a printed fraction to recover a total (L24a, L24b); rounding of the fraction makes this fragile. Those papers serve instead for the registered ICL range.

**QL2. The BCG's inclusion is not stated.**
- **Recommended:**
  - (i) a direct sum over all galaxies or members in the aperture, with no stated exclusion, counts as including the BCG, flagged "BCG by method" (L2, L8, LV3, S6);
  - (ii) a total that is only an analytic integral of a fitted Schechter function, with no separate BCG term, counts as members only and is excluded (L4, S4b, S4d). The fitted form replaces the brightest galaxy, which is often the largest single component.
- Alternative (strict): require an explicit statement. All seven become X.

**QL3. The faint end is truncated.**
- **Recommended:** accept a sum truncated at a stated faint limit at least 2 mag fainter than the characteristic magnitude M*, with or without the source's extrapolation, flagged with the limit (L1, L5c, L8, L9, S6). Where the source quantifies the missing faint light, show it as a range.
- Exclude bright-only sums, i.e. a limit brighter than M* + 1 (LV5a). The Atlas does not model missing light itself.

**QL4. Magnitudes and evolution corrections.**
- **Recommended:**
  - an absolute magnitude in a named band counts as a printed luminosity, converted with that band's solar absolute magnitude, read at source and registered (S3a);
  - an observed-frame apparent magnitude does not, because the Atlas would apply k-corrections (S10a: X);
  - a luminosity evolution-corrected by the source is accepted and paired with the mass-to-light ratio for the epoch the source corrected to (S16b, z = 0).

**QL5. The source's deprojection.**
- **Recommended:** a luminosity deprojected by the source's own model counts as 3D (pairs with row O), labelled `model_dependence` with the source's assumption (L1, S2b, L4).

**QL6. Precedence among luminosity sources for one cluster.**
- This goes into `docs/methods/A9_PRECEDENCE.md` for approval with the rest of that rule.
- **Recommended order:**
  1. the source's own measured stellar mass (route a), then luminosity × ratio (route b);
  2. within route (b), near-infrared bands first, since the stellar-population ratio varies least there;
  3. a team's later analysis of the same data supersedes its earlier one (S3b over S3a and L23b; L1 over S2b);
  4. the aperture matched to the observed side: projected with row L, 3D with row O.

## Effect of the rulings (codes only)

| Row | As recommended | Strict QL2 |
|---|---|---|
| L2, L8, LV3, S6 | E | X |
| L4, S4b, S4d | X | X |
| L10, L23b, S3a | E (QL1) | E (QL1) |
| S10a | X | X |

The coverage table (which A9 clusters gain measured stars) is computed next, under both readings of QL2.
