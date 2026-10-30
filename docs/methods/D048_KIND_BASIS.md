# D-048 item 3: the basis of a dwarf-galaxy label — frozen rule

**Frozen 2026-10-30 (on merge of the pull request that adds it).** It must be frozen before any velocity dispersion, structural value or luminosity of an A5 candidate is opened. Applies to every system that could enter A5 (dwarf galaxies) or A7 (ambiguous) from the LVDB index or the original papers. Its hash goes into `data/frozen/`; any change needs a new version and a logged decision, and applies only to later cases.

## Question answered per system

Does the label "dwarf galaxy" rest on anything other than the system's own dynamics? D-036 #7 and D-048 item 3 say: kinds come from the sources' labels, except where the label rests on dynamics, or where sources disagree. In those cases the system is A7, labelled "ambiguous: dwarf galaxy or star cluster".

## Evidence read

For each system, an independent reader reads:
- the discovery paper or papers (LVDB `ref_discovery`);
- the paper of the first published line-of-sight dispersion (LVDB `ref_vlos`, or the earliest original in the A5 search log if earlier);
- any paper the search log or LVDB `ref_false_positive` lists as disputing the classification.

The reader records only what each paper says about the **kind** of system, and on what grounds, with a quote and its location. The reader does not record any dispersion, mass, mass-to-light ratio or acceleration.

## Grounds, coded per paper

| Code | Ground stated by the paper for calling it a galaxy |
|---|---|
| L | Light and structure: size, luminosity, surface brightness, morphology, or comparison with the known galaxy and cluster populations in those properties |
| P | Stellar population other than the metallicity spread: age spread, extended star-formation history, distinct populations by photometry |
| G | Gas detected in the system |
| D | Dynamics: velocity dispersion resolved, dynamical mass, or a dynamical mass-to-light ratio |
| M | Spread in metallicity ([Fe/H] dispersion) |
| N | No ground stated: the paper uses the label without justification |
| X | The paper calls it a star cluster, or says the kind is uncertain or disputed |

## Rule

1. **A7** if any paper read is coded **X** for the current kind (a dispute or a cluster label), or if the LVDB marks the system `confirmed_star_cluster = 1`.
2. Otherwise **A5** if at least one paper gives ground **L**, **P** or **G**. These are labels that do not rest on the system's own dynamics.
3. Otherwise (only **D**, **M** or **N**): **A7**, with the reason "galaxy label rests on dynamics or metallicity spread only" (or "no stated ground").
4. Systems whose label predates any kinematic measurement (discovered and called a galaxy before a dispersion was published) satisfy rule 2 through their discovery paper, if that paper gives L, P or G.
5. The A7 view on the map shows A7 systems that pass the plotting rules, labelled as ambiguous. They are never shown in the A3 or A5 default views (D-037, D-038 4A).
6. The coding sheet (one row per system and paper: code, quote, location) is published in the package, and the kind follows mechanically from it. A second reader codes a random 20% of systems independently; disagreements are logged and resolved by the rule text, never by the result.

## Not used as classifiers (D-036 #7)

Size, luminosity, ellipticity and metallicity spread are never thresholds applied by the Atlas. They count only as grounds a paper itself states (L, M), and M alone is not enough.
