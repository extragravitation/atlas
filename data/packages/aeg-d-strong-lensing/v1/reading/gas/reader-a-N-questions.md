# Reader A — part G, candidates N1–N22: questions and flags

Brief: `GAS_AND_SUPPLEMENT_BRIEF.md` v2, part G only. Output: `gas_reading.csv` (229 rows; sha256 0005ca00c32146b53ee88d02bc509aa80626945e23d1e7219cbb97d3512bae69). Builder: `scripts/build.py`; quote check: `scripts/verify.py` (every quote is at most 15 words and appears verbatim, after whitespace normalisation, in the pdftotext output). Source PDFs are in `dl/`, with hashes in `sha256.txt`.

## How the sources were reached
- arXiv ids were found with WebSearch by title, journal, volume and page. Titles were matched against the arXiv abstract metadata. Journal refs appear on arXiv only for N2, N4, N8, N9, N14a, N14b; for all other candidates the bibcode–arXiv match rests on title, authors and year.
- **Every row is `version = arXiv vN`.** No journal version or AAS table was read, and VizieR has no table for N7, N13, N18 or N20. VizieR does list J/A+A/573/A111 (CO spectra) and J/A+A/618/A126, but I did not use them.
- N20: the first hit, arXiv 0903.4417, is a conference proceeding. I did not use it; the A&A paper is arXiv 1001.5009.
- N19a and N19b are the same authors. N19b Table 2 reprints the 9 BCG values from N19a Table 3, so I recorded each galaxy once: the BCGs from N19a, and the 12 NCEGs plus M 87 from N19b. NGC 5044 comes from N19a only.

## Decisions needed (JvH)
1. **Rows with no qualifying value.** Thirteen papers print no gas mass inside ≤10 kpc or ≤2 R_e: N1, N3, N5, N6, N8–N12, N16, N21, N22, and N4 for per-galaxy values. The brief has no quantity for "read, nothing in scope", so I used `quantity = none_in_scope`, one row per paper, with a note. Rename this, or drop the rows?
2. **A beam used as the radius.** For single-dish CO (N13, N14a/b, N17) the only stated radius is the telescope beam. The papers print it as a **FWHM diameter** in kpc, or as 22″ for N17. I copied the diameter as printed and labelled it in `radius_unit`; I did not halve it. A beam is not a hard aperture, and N14 says CO may extend beyond it. Should these rows count as "inside a stated radius"?
3. **N14b mixed beams.** Table 1 reports "the larger mass or upper limit" of CO(1-0) and CO(2-1), so for some rows the effective beam may be the CO(2-1) beam, which is half the size. The per-line values are in its Table 2, which I did not transcribe.
4. **N2, NGC 4552:** Rm = 10.7 kpc exceeds the 10 kpc limit, so I left it out. In Table 5 it is Mgas 2.5×10^8 Msun. The N2 sample average (3×10^7) includes it.
5. **N6 (Babyk et al. 2018, 94 ETGs):** gas masses are given only within 5 r_e, which is out of scope. The β-model parameters (β, r_c, ρ0) are printed per galaxy, so a mass within 2 R_e could be computed. That is not a reader's job; your call.
6. **N4 (Lakhchaura et al. 2018, 49 giant ellipticals):** Mgas(<10 kpc) is plotted (Fig. 1) but not tabulated. To get the values: ask the authors, or digitise the figure.
7. **N18 central HI:** the region is "one WSRT resolution element" (typically 35″×45″), not a kpc or R_e radius. I recorded it as a catalogue_location only (Table 1, 166 galaxies).
8. **N20 (TANGO I):** MH2 includes a model source/beam coupling factor (exponential disc, h = D_B/10), so the values are model-extrapolated rather than beam-limited. No per-galaxy luminosity is tabulated, so I wrote only sample statistics and a catalogue_location row.
9. **Brightest quarter.** I took the ceiling of N/4: 11 of 42 for N7 (by LK within 2 r_e) and 17 of 67 for N13 (by MKs; three galaxies tie at −25.93, and all are included). Neither paper prints a per-galaxy stellar mass. For N13, 6 of the 17 have only literature values with no radius; I recorded those as `gas_total_no_radius`.
10. **Whole-galaxy HI.** Under the "recorded, not used" rule I wrote compiled HI masses (N14a/b) and N15's interferometric HI totals as `gas_total_no_radius`. That is 34 rows for N15 alone. Keep them, or cut them to sample statistics?
11. **Gas-to-stellar ratios that are not same-radius.** The ratios in N14b (M(H2)/M*) and N18 (M(H2)/M*) set a beam-limited H2 mass against a whole-galaxy M*, and I say so in the notes. Only N2's Mgas/M* = 8.0×10^-4 is close to same-radius, and its M* comes from LK through an assumed M*/LK = 0.8.

## Transcription conventions to confirm
- pdftotext drops superscripts, so "2.0 × 107" in the extracted text is printed 2.0×10^7. I wrote values as `2.0 × 10^7` and kept table units such as `10^8 Msun` in the `unit` column rather than converting. The quotes keep the raw extracted text, for example `107M⊙`.
- Symmetric errors (±) are copied into both err_minus and err_plus.
- I wrote "upper (3 sigma)" only where the paper states 3σ. N2's limits are 90% (its Fig. 4 caption).

## Not part G, but noted
- N10 (Mrk 1216) has a figure of g_obs against g_bar for the hydrostatic model, with Newtonian and MOND curves. I did not record it. Do you want it for the dynamics channel?
- In N19a/b the BCGs are named by their host cluster as printed (e.g., "Centaurus", "Abell 262"). I did not map them to galaxy names, which would be a judgement.
