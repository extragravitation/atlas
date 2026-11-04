# Status at pause: v2 second readings (2026-11-04)

Branch `reading/v2-dwarfs-gc`. Nothing on it is frozen yet.

## Done

**Globular clusters:** the reading is complete, including Rees (1996), which was read from the ADS scan JvH supplied (SHA-256 `6a4d9cfa…37db9`; not redistributed). The files are in `data/packages/aeg-d-gc-baumgardt/v2/reading/`. One open question for JvH: are M3 and M13 anchors, given that Rees quotes their distances rather than deriving them? They are currently recorded as anchors, notes only.

**Dwarfs:** readers A and B are in `data/packages/aeg-d-dwarfs/v2/reading/`. They agree on 12 D-097 findings. A has 16, and B has 12.

## Waiting for JvH

**D-100, proposed (not ruled).** Three clarifications to D-099 rule 4, decided on wording only:
1. **The states form a closed list:** out of equilibrium or disequilibrium, unbound, being tidally disrupted, tidally disturbed. Tidal interaction, being affected, influenced or altered by tides, distortion, elongation, S-shape, stripping, tails and mass loss are "neither".
2. **The possibility hedges** also include "potentially", "tentative", "hints" and "possible". "Likely", "probably", "suggest", "support", "favour", "appears" and "evidence for" stay as findings.
3. **A statement must be about the system itself**, not about a class it belongs to.

**Result if ruled:**
- **8 findings:** And XXVII and Antlia II (already ruled), Boötes III, Boötes I, Hercules, Ursa Major II, Willman 1 and And XXI.
- **2 more possibilities:** Draco II and Eridanus IV.
- **"Neither":** And XV, And XVIII, And XIX, And XXV, Coma Berenices and Ursa Major I.

**Smaller calls:**
- **Fornax:** Wang 2019 says the "Sérsic model gives the best fit". Recommend Sérsic, 20.1′, under D-096 rule 1, which conflicts with v1's use of D-052 item 1.
- **Hercules:** recommend no change (1.8 km/s, D-038 addendum).

**A paper JvH needs to supply:** Monelli et al. 2025, A&A 700, A201 (Leo II distance). It has no arXiv version, and the journal site refused access.

## After the ruling

1. Log D-100.
2. Compare readers A and B field by field, resolve differences at source and write the resolved dwarf reading.
3. Check Tollerud 2012's velocity windows against the coverage member sets (D-096 rule 2).
4. Freeze both readings by hash (`data/frozen/gc-v2-reading.json`, and the dwarf reading hash in `v2/sources.json`).
5. Then the conversions.
