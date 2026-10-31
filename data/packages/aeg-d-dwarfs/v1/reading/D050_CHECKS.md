# D-050 checks: version of record and errata (2026-10-31)

Done through JvH's signed-in ADS session and the publisher sites, using Claude in Chrome for ADS and OUP and direct download for IOP. Results are per paper in `d050_version_of_record.csv`.

## Version of record (D-050 item 5)

24 originals show no acceptance signal on arXiv; 3 more have no arXiv copy. For every one that supplies a plotted value, the values the package uses were checked in the version of record:
- **IOP PDF (12 papers), with the hash of each copy:** every value found as packaged. The check is that each number occurs in the version of record's text. For Wang 2019 it was confirmed on the page image, because the text layer drops the decimal point.
- **OUP (2 papers):**
  - Charles 2023 agrees.
  - Koposov 2018: the version-of-record Table 1 is missing the values that have asymmetric errors, in both the PDF and the HTML. The affected cells are the half-light radii, the ellipticity, σ, the mass, M/L and J.
  - σ (abstract), the distance, M_V and [Fe/H] agree.
  - **Hydrus I's r_h = 7.42′ and ε = 0.21 therefore come from arXiv**, labelled, under D-050 item 2 (the version of record cannot be read for those cells).
- **Monelli 2025 and van de Rydt 1991** were already read in the version of record.
- **Unrefereed preprints**, still arXiv-only on ADS on this date, labelled as such:
  - Cerny 2026 (Draco II);
  - Li 2026 (Boötes III);
  - Willman et al. 2006 (Willman 1 distance). Never published since 2006.
- **No effect on the package:** eight papers supply no plotted value. They were not checked.

## Errata

One ADS query per block of about 62 bibcodes asked for documents titled erratum or corrigendum, or of type erratum, that cite any of the 186 bibcodes behind the package (`errata_bibcodes.txt`). Of 26 hits, two are errata of papers in the record:
- **Tan et al. 2025 (Leo VI) erratum** (ApJ 1010, 239; read in full): corrects figure labels only. No effect.
- **Kirby et al. 2012 (VV124) erratum** (ApJ 768, 96; read): [Fe/H] was too high by about 0.4 dex. The package's UGC 4879 metallicity comes from Kirby et al. 2013b (−1.43), not the 2012 paper, and VV124 has no plotted dispersion. No effect.

**Limit.** An erratum that cites nothing, or is not indexed with "erratum" in its title or type, would be missed.
