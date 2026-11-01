# Reader B, part G: open questions (2026-11-01)

1. **Two extra `quantity` values.** The brief lists five. I added `none_in_radius` (paper read, no gas mass or limit printed within 10 kpc or 2 R_e) and `NS` (no full text reachable). Rename them, or fold them into another category?
2. **Beams as "radius".** Single-dish and interferometer apertures are printed as beam FWHM (a diameter), as an ellipse (WSRT major × minor), or as a square (Young 2002, 22.5″ side). I copied them as printed and wrote the shape in `radius_unit`. I did not halve or convert anything. Do these count as a "stated radius" under §0a? This affects C15, C16 (limits), C17 and C27.
3. **Diameter or radius.** For C26 (NGC 4150) the paper prints an HI diameter of 4 kpc. I recorded the diameter. C16 uses Table 5 R ("radius of the outer edge"), so that one is a true radius.
4. **arcsec apertures with no kpc conversion (C21).** The 22″ beam is described as "typically the central ∼23kpc region at z=0.05". I did not judge eligibility per galaxy, because that needs a conversion. I gave a catalogue pointer only. C21 also says Mgas = 1.36 M(H2) is "displayed in Table 4", but the column header reads M(H2). Which one is tabulated is unclear.
5. **Brightest-quarter rule (C17).** No stellar mass or K-band magnitude is printed, so I used the printed M_B. The brightest quarter of 43 observed galaxies is 10.75, and NGC 1023 and NGC 474 tie at −20.42, so I took 11. Is B-band acceptable?
6. **Massive per-galaxy rows not made for C13 or C30.** Neither table prints M* or M_K (both are in ATLAS3D Paper I, which is not a candidate). Should Paper I be read to select them?
7. **Not refereed.** C20 (Leon et al.) is a two-page ASP conference proceeding. The search log's X-type rule would exclude it.
8. **C4 statistic with no radius.** "< 0.04% of the mass in stars" comes from integrating the gas density profiles, and no radius is printed. I recorded it as `sample_statistic` with the radius blank.
9. **Totals compacted.** Under "recorded, not used", I gave whole-galaxy totals as one `gas_total_no_radius` row per candidate that points to the table. Do you want them transcribed per galaxy for the samples with 40 or fewer galaxies (C14, C18, C20, C26, C28)?
10. **Access.** VizieR (vizier.cfa.harvard.edu) timed out for J/MNRAS/414/940 (C13), so no machine-readable table was checked. All candidates were read from the arXiv version. No journal version was opened.
11. **Six NS (C11, C12, C22, C23, C24, C31).** An arXiv search found no record. Pre-1998 journal scans are not among the permitted routes.
12. **Inconsistency in the source (C28).** NGC 3108's M_HI is printed as 4.5×10^9 in the abstract, 4.59 (×10^9) in Table 5 and 4.6×10^9 in the text.
