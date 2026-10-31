# Gas readings (Putman et al. 2021 Table 1): adjudication

Two independent readings of the journal MRT (`source/gas/putman2021/apjabe391t1_mrt.txt`, hash in `sources.json`) under `GAS_READING_BRIEF.md`, compared by `reproduction/compare_gas_readings.py` (committed before either reading was seen).

**Result.** 103 systems. Both readers matched the same 97 rows and agree on every copied field. Both found six systems absent by name: Aquarius III, Centaurus I, Eridanus IV, Leo VI, Pegasus IV and Cassiopeia II (the six "disagreements" are only the placeholder each reader wrote for "not found"). The two copies of the header Notes (1)–(5) are identical (`gas_notes/`).

**Cassiopeia II.** Both readers flagged the row "Andromeda XXX" and did not match it, because the table does not state the cross-identification. Two originals already double-read for this package state it: Martin et al. 2016 Table 1 ("Cas II/And XXX") and Savino et al. 2022 Table 1 (other name "Cas II" for And XXX). The table position (00 36 35, +49 38 48) lies 4″ from the LVDB index position of Cassiopeia II. Ruled: match. Both readers then read that row independently (`gas_reading_*_followup.csv`); they agree on every field.

**Noted for conversion, not changed here.** The table's HI masses are computed at Putman's own distance (`Dist`, reference `r_Dist`); for Cassiopeia II that is 682 kpc against the package's adopted 559.8 kpc (Savino 2022). Whether to rescale is a proposed ruling (D-058), not a reading matter.

`reproduction/resolve_gas_readings.py` writes `gas_values.csv`: 98 systems in the table, 5 not in it.
