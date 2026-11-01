# Reader B — part G, candidates N1–N22: open questions

Brief: `GAS_AND_SUPPLEMENT_BRIEF.md` v2, part G only. Output: `gas_reading.csv` (232 rows). Sources: arXiv PDFs (pdftotext -layout) in `dl/` (SHA-256 in `sha256.txt`, versions in `versions.txt`), and one VizieR table (`dl/N14b_viz_table1.tsv`). The arXiv ids came from WebSearch (title + "arXiv") and were checked against the arXiv abstract page titles. N14 and N19 each have two records; both were read.

## Deviations that need a ruling
1. **`quantity = none_found`.** This value is not in the brief's list. I used it for 13 candidates whose full text I read but which print no qualifying value: N1, N3, N5–N12, N16, N21, N22. The brief's NS row is meant for text that could not be reached, so I did not use NS. Should these be NS rows, or should the list of quantities gain this value?
2. **Beam sizes are diameters.** For single-dish CO (N13, N14, N17, N20), the printed "radius" is the beam FWHM (N13: "diameter of the 22″ beam"). I recorded it as printed and said so in `radius_unit`; I did not halve it. Rule: is a beam-integrated mass a "gas mass inside a stated radius", and is the radius half the printed beam?
3. **N2, NGC 4552:** R_m = 10.7 kpc, which is over the 10 kpc limit. I recorded the row and flagged it in `note`. Keep it or drop it?
4. **Exponents.** pdftotext drops superscripts ("2.0 × 107"), so I wrote them back as "× 10^7". Raw quotes keep the extracted form.

## Facts for adjudication (no action taken)
- **N13 (MASSIVE XI):** 67 galaxies, and no stellar masses are printed. Following the brightest-quarter rule, I gave per-galaxy rows to 17 galaxies (M_Ks ≤ −25.87, ties included). Ten of these were observed in this paper and have a beam; seven are literature values with no radius (`gas_total_no_radius`).
- **N14:** For N14a I transcribed from the arXiv text. For N14b I used the journal's VizieR table J/A+A/618/A126/table1 (36 galaxies). Table note f says the larger of the CO(1-0) and CO(2-1) masses is reported, so some IRAM masses may come from the beam half the listed size. The stellar masses in both papers are totals, not measured in the same radius, so they appear only in `note`.
- **N18:** The central HI is measured within one WSRT beam (~30–40″). The ratios are to M_JAM, a dynamical mass that the paper says approximates stellar mass. The brief asks for gas-to-stellar ratios, so whether these count is for you to decide. Per-galaxy values are left in Table 1 (166 galaxies) because no per-galaxy M* is printed.
- **N19:** All masses are within 500 pc (ALMA). The 2023 sample is 9 cluster-centre BCGs. The 2024 Table 2 repeats those BCGs; I re-recorded only NGC 5044, with the same value, and noted it.
- **N4:** Mgas(<10 kpc) for 49 galaxies appears only in Fig. 1, and I found no VizieR catalogue. I recorded the Mgas–T_X fit. The paper's f_gas is Mgas/Mtot, not a gas-to-stellar ratio.
- **N6:** The paper gives gas masses only within 5 r_e. Per-galaxy β-model parameters (Table 3) would allow a mass inside ≤2 R_e to be computed. I did not compute one (readers do not compute).
- **N10, N5, N11:** Gas-mass profiles appear only in figures. N10 states that the gas mass stays below the stellar mass out to ~170 kpc (qualitative; quoted in the CSV).
- **N20:** There is no per-galaxy stellar mass or K-band luminosity, so the 52 galaxies are covered by the Table 5 location and the sample medians only.
- **Version:** All rows are arXiv versions except the N14b VizieR rows. I did not try the journal versions (AAS, MNRAS, A&A) for the arXiv-read papers.
