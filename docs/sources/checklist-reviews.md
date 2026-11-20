# What the field's reviews use as tests (completeness plan, step 1.1)

2026-11-18. **Status: for JvH's review.** This is the input to steps 1.2 (taxonomy v3), 1.3 (test-system checklist) and 1.4 (scope statement). It records which systems, types and measurement routes five field reviews **use as tests**. It does not record what they conclude, and it gives no Atlas status. Statuses are step 1.3.

## Sources and how they were read

| Code | Review | Side | Pages read |
|:--|:--|:--|:--|
| FM | Famaey & McGaugh 2012, Living Rev. Relativ. 15, 10 (arXiv:1112.3960v2) | MOND-side | 1–130, all sections |
| BZ | Banik & Zhao 2022, Symmetry 14, 1331 (arXiv:2110.06936v9) | MOND-side | 1–77, all sections |
| BBK | Bullock & Boylan-Kolchin 2017, ARA&A 55, 343 (arXiv:1707.04256v2) | DM-side | 1–42, all sections |
| SAL | Salucci 2019, A&ARv 27, 2 (arXiv:1811.08843v2) | DM-side | 1–56, all sections |
| CSZ | Cirelli, Strumia & Zupan 2026, SciPost Phys. Rev. 1 (arXiv:2406.01705v3) | DM-side | 15–68, 300–310, 394–406 only (D-111) |

- **Process:**
  - The brief (`readings/checklist-2026-11-18/brief.md`) and the name scan (`scan_names.py`) were committed in e319717 before any reader started.
  - There was one reader per review, plus the script check (D-110 rule 5); no value is read in this step.
  - Every catalogue-style name the scan finds in a reader's page range is either in that reader's CSV or listed as a false match in their notes. I re-ran all five scans; the remaining unmatched names are equation symbols, mass labels and citations, and I confirmed four of them at source.
- **PDF hashes:** recorded in the brief.
- **Outputs:**
  - `readings/checklist-2026-11-18/<code>-items.csv` and `<code>-notes.md`: per reader, 1 051 rows in all (FM 292, BZ 282, BBK 107, SAL 176, CSZ 194).
  - `checklist-reviews.csv`: every row, with a canonical system name and the review's side.
  - `checklist-reviews-systems.csv`: one row per system.
  - Both are written by `merge.py`. The family counts below come from `families.py`.
- **Limits:**
  - One reader per review. A missed use of a catalogue-named system would be caught by the scan; a missed type or route would not.
  - CSZ was read only in the chapters D-111 names.
  - Eleven SAL rows come from bare numbers on the Fig. 13 panels, which the reader read as NGC numbers and as DDO 154. This was not checked against the source paper.

## 1. Corrections to CK-01

CK-01 (12 Nov) worked from the contents pages and partial reads. The full read changes four of its statements:

1. **NGC 1399, NGC 4472, M87 (NGC 4486), NGC 4649, NGC 1407 and MACS J0025** are not used as tests anywhere in the five reviews; they occur only in reference lists. They should not enter the 1.3 checklist on the strength of these reviews.
2. **Antlia II** is not used as a test either. CSZ lists it only in Table 2.3, among targets for indirect detection searches.
3. **Crater II** is used as a test only by BZ (p. 26: tidal survival).
4. **M94, M101, NGC 1042 and NGC 3351** are used (by BZ, p. 31), but for stellar-halo mass as a record of merger history. That is evidence outside the charter, not a pull comparison.

## 2. Named systems

184 canonical systems: **132 are used as a test** by at least one review, and 52 are only mentioned.

- **By side:**
  - 37 are used by both sides;
  - 59 by the MOND-side reviews only;
  - 36 by the DM-side reviews only.
- **By scale, for systems used by one side only:**
  - MOND-side only: galaxies, dwarfs, clusters, star clusters, cosmological structures, groups, a wide binary.
  - DM-side only: galaxies and dwarfs only.

  The DM-side cluster tests here (the Bullet Cluster and the Coma cluster) are shared with the MOND side. This follows from the reviews read; it is not a statement about the literature.

### Systems used as a test by two or more reviews

| System | Used as a test by (rows) | Scale | Channel |
|:--|:--|:--|:--|
| Fornax (dwarf spheroidal) | FM(2), BZ(1), BBK(1), SAL(3), CSZ(2) | dwarf galaxy | dynamics, neither |
| Carina | FM(1), BZ(1), BBK(1), SAL(1) | dwarf galaxy | dynamics, neither |
| Draco | FM(1), BBK(1), SAL(1), CSZ(1) | dwarf galaxy | dynamics, neither |
| LMC | FM(1), BZ(2), BBK(2), CSZ(1) | dwarf galaxy, galaxy, group | dynamics, neither |
| Milky Way | FM(2), BZ(4), SAL(5), CSZ(6) | galaxy | dynamics |
| Sculptor | FM(1), BBK(1), SAL(2), CSZ(1) | dwarf galaxy | dynamics, neither |
| Bullet Cluster (1E 0657-56) | FM(3), BZ(4), CSZ(2) | cluster | both, dynamics, lensing |
| Leo I | FM(1), BBK(1), SAL(1) | dwarf galaxy | dynamics, neither |
| Leo II | FM(1), BBK(1), SAL(1) | dwarf galaxy | dynamics, neither |
| M31 | FM(1), BZ(4), CSZ(1) | galaxy, group | dynamics |
| M33 | FM(1), BZ(5), SAL(1) | galaxy | dynamics |
| NGC 1560 | FM(2), BZ(1), SAL(1) | dwarf galaxy, galaxy | dynamics |
| NGC 2419 | FM(1), BZ(1), CSZ(1) | star cluster | dynamics |
| Sagittarius stream | FM(1), BZ(2), CSZ(1) | dwarf galaxy, galaxy | dynamics |
| Sextans | FM(1), BBK(1), SAL(1) | dwarf galaxy | dynamics, neither |
| SMC | FM(1), BBK(1), CSZ(1) | dwarf galaxy, galaxy | dynamics, neither |
| Solar System | FM(4), BZ(2), CSZ(3) | Solar System | dynamics |
| Ursa Minor | FM(1), BBK(1), SAL(1) | dwarf galaxy | dynamics, neither |
| Abell 2390 | FM(1), BZ(1) | cluster | lensing |
| Abell 520 | FM(1), BZ(1) | cluster | both, lensing |
| Centaurus A group | BZ(2), BBK(1) | group | dynamics, neither |
| Coma cluster | BZ(3), CSZ(1) | cluster | dynamics |
| DDO 154 | FM(1), SAL(2) | dwarf galaxy | dynamics |
| DDO 210 | FM(1), SAL(1) | dwarf galaxy | dynamics |
| Holmberg II | BZ(1), SAL(1) | dwarf galaxy | dynamics |
| IC 2574 | FM(1), SAL(1) | dwarf galaxy | dynamics |
| M31 satellite system | FM(1), BBK(1) | dwarf galaxy, group | dynamics, neither |
| M81 group | BZ(1), SAL(1) | dwarf galaxy, group | dynamics |
| NGC 1052-DF2 | BZ(2), CSZ(1) | dwarf galaxy | dynamics |
| NGC 1052-DF4 | BZ(1), CSZ(1) | dwarf galaxy | dynamics |
| NGC 2403 | BZ(1), SAL(1) | galaxy | dynamics |
| NGC 2841 | FM(1), SAL(1) | galaxy | dynamics |
| NGC 2903 | FM(1), SAL(1) | galaxy | dynamics |
| NGC 3109 | BZ(2), SAL(1) | dwarf galaxy, group | dynamics |
| NGC 3198 | FM(1), SAL(2) | galaxy | dynamics |
| NGC 5291 system | FM(4), BZ(1) | dwarf galaxy, group | dynamics |
| NGC 5557 | BZ(1), SAL(1) | dwarf galaxy, galaxy | dynamics |
| NGC 6946 | FM(2), BZ(2) | galaxy | dynamics |
| NGC 7331 | FM(1), SAL(1) | galaxy | dynamics |
| Palomar 14 | FM(1), CSZ(1) | star cluster | dynamics |
| Sagittarius (dwarf spheroidal) | BZ(2), BBK(1) | dwarf galaxy | dynamics, neither |

"neither" marks a row where the same system is used for an outside-the-charter test, such as satellite counts or planes.

### Systems used as a test by one review

- **Clusters:** Abell 2218 (FM); Cl 0024+17 (FM); El Gordo (BZ); Fornax cluster (BZ); XMMU J2235.3-2557 (FM).
- **Groups and pairs:** Local Group (BZ); the Antennae (FM).
- **Galaxies:**
  - ALESS 073.1 (BZ);
  - Centaurus A (BZ);
  - ESO 509-98 (FM);
  - F563-1, F563-V2, F568-3, F583-1, F583-4 (FM);
  - IC 1024 (SAL);
  - NGC 474 (BZ), NGC 720 (BZ), NGC 1052 (BZ), NGC 1521 (BZ), NGC 1543 (FM), NGC 2481 (SAL), NGC 2824 (SAL), NGC 2998 (SAL), NGC 3521 (FM), NGC 3621 (FM), NGC 3626 (SAL), NGC 3923 (BZ), NGC 3953 (BZ), NGC 3992 (SAL), NGC 4111 (SAL), NGC 4452 (SAL), NGC 4494 (SAL), NGC 5005 (SAL), NGC 5055 (FM), NGC 5422 (SAL), NGC 5475 (SAL), NGC 5585 (SAL), NGC 5839 (SAL), NGC 5869 (SAL), NGC 6503 (SAL), NGC 7113 (SAL), NGC 7454 (SAL), NGC 7507 (FM), NGC 7693 (SAL);
  - OGC 0139 (BZ);
  - PGC 67207, PGC 170172 (SAL);
  - Q2237+030 (FM);
  - UGC 128 (BZ), UGC 1230 (FM), UGC 2487 (FM), UGC 2885 (FM), UGC 2953 (FM), UGC 3205 (CSZ), UGC 3960 (SAL), UGC 11919 (BZ).
- **Dwarf galaxies:**
  - AGC 114905 (BZ), Cetus (BZ), Crater II (BZ), Dragonfly 44 (BZ), HIZSS 3 and KKH 98 (BZ), Perseus I (BZ), Tucana (BZ), the Milky Way satellite system (BZ);
  - DDO 43 and DDO 126 (BBK);
  - DDO 53, DDO 101, DG1, DG2, Haro 36, Holmberg I, NGC 2366 (SAL);
  - DDO 161, FAST J0139+4328, Segue 1, Segue 2 (CSZ);
  - UGC 11583 (FM).
- **Star clusters:** NGC 1851, NGC 1904, Palomar 3 (FM); Palomar 5, Pleiades, Praesepe (BZ).
- **Wide binaries:** the Alpha Centauri system (BZ).
- **Large-scale structures:** Local Void, Local Volume, Shapley supercluster, Sloan Great Wall (FM); Perseus-Pisces superfilament (BZ).

Mentioned but not used as a test (52) are listed in `checklist-reviews-systems.csv`. Most are the CSZ Table 2.3 indirect-detection targets.

## 3. Measurement routes and types: which candidate families each review uses

These are indicative counts of rows per family, matched by keyword. They show **whether** a review uses a family, not exact numbers. The patterns are in `families.py`.

| Family | FM | BZ | BBK | SAL | CSZ |
|:--|--:|--:|--:|--:|--:|
| vertical dynamics | 11 | 9 | 0 | 7 | 1 |
| tidal streams | 2 | 8 | 1 | 0 | 2 |
| shells | 0 | 6 | 0 | 0 | 0 |
| direct accelerations | 0 | 3 | 0 | 0 | 1 |
| binary galaxies, satellites as tracers | 1 | 4 | 0 | 0 | 2 |
| Local Group timing, local flow | 2 | 6 | 0 | 0 | 0 |
| tidal radii | 2 | 5 | 0 | 0 | 0 |
| escape velocity | 2 | 2 | 0 | 0 | 1 |
| wide binaries | 1 | 5 | 0 | 0 | 1 |
| open clusters | 2 | 2 | 0 | 0 | 0 |
| colliding clusters, offsets | 9 | 8 | 0 | 0 | 3 |
| X-ray hydrostatics | 7 | 4 | 0 | 1 | 1 |
| galaxy-galaxy weak lensing | 1 | 3 | 0 | 3 | 2 |
| strong lensing | 4 | 6 | 0 | 6 | 0 |
| galaxy dynamics in clusters | 2 | 2 | 0 | 0 | 2 |
| polar rings | 0 | 2 | 0 | 0 | 0 |
| tidal dwarfs | 8 | 5 | 0 | 0 | 0 |
| ultra-diffuse galaxies | 0 | 8 | 0 | 0 | 4 |
| gravitational redshift in clusters | 1 | 0 | 0 | 0 | 0 |

**What this means for taxonomy v3 (1.2):**
- **Confirmed by both sides:** every route CK-01 proposed is used as a test by at least one review, and vertical dynamics, streams, satellites as tracers, escape velocity and direct accelerations by both sides.
- **Used by the MOND-side reviews only:** shells, tidal radii and the Local Group timing argument.
- **Not in CK-01's list:** gravitational redshifts in clusters (FM) and the moving-cluster effect (BZ) are additional routes.

## 4. Open item for step 1.4: where the boundary falls

The readers drew one line differently, and the scope statement has to settle it. The item is a comparison of the observed pull with a **model's predicted pull** rather than with the pull of detected matter. Examples:
- cusp versus core;
- too-big-to-fail;
- diversity of rotation-curve shapes;
- the velocity function;
- abundance-matching masses.

BBK filed these as dynamics routes and marked them as boundary cases. BZ filed stellar-halo mass and satellite planes as outside the charter.

**My recommendation for 1.4:**
- The observed side of such a test is inside the Atlas when it is a pull measured by dynamics or lensing.
- The comparison with a model belongs to the accounts layer.
- The scope statement would list these tests as "partly inside", with the observed half pointing to the Atlas's data. CK-01 already did this for cusp versus core.

This is for JvH's ruling when 1.4 is drafted. Nothing in this file depends on it, because every row keeps the reader's own classification.

## 5. Test cases the reviews themselves call contested

These come from the readers' notes, with page references there. A case is listed here only if a review frames it as contested between the two sides:
- NGC 1052-DF2 and DF4;
- Dragonfly 44;
- NGC 2419 and Palomar 14;
- Crater II;
- Carina (its mass-to-light ratio);
- Sextans, Draco and Ursa Minor (equilibrium, membership);
- the Bullet Cluster (collision velocity; lensing–gas offset);
- AGC 114905, UGC 11919 and Holmberg II (inclination);
- NGC 3198 (distance);
- NGC 1560 (non-circular motions);
- Milky Way vertical dynamics;
- the DiskMass weighting;
- wide binaries;
- the satellite planes of the Milky Way and M31;
- the external-field effect in SPARC;
- the baryonic Tully–Fisher relation and the radial acceleration relation (whether each account reproduces them).

These go into the "disputed inputs" column of the 1.3 checklist, with each review's page reference.
