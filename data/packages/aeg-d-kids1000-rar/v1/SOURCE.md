# aeg-d-kids1000-rar/v1 — source

**KiDS-1000 weak-lensing radial acceleration relation.** Brouwer, M. M. et al. 2021, A&A 650, A113 (arXiv:2106.11677). Data release: https://kids.strw.leidenuniv.nl/sciencedata.php (read 2026-10-28), file `brouwer2021_rar.tar` and its README.

Full reading notes: `docs/sources/kids1000-rar.md`.

## Terms

The KiDS page states no licence; the acknowledgement requested is that of the paper ("See Acknowledgements section of Brouwer et al. (2021)"). Under D-004 the source file is not redistributed: it is fetched at build time and verified by hash.

## Method (as read at source)

- Lenses: isolated galaxies (no neighbour above 10 % of the lens stellar mass within 3 h70⁻¹ Mpc; M* < 10¹¹ h70⁻² M☉), from KiDS-bright (photometric redshifts) or GAMA (spectroscopic). Paper §3.3.
- g_bar: point mass of stars plus cold gas within the measurement radius; stellar masses from 9-band photometry (normalised to GAMA), cold gas from a scaling relation with stellar mass (Boselli et al. 2014). Stars and cold gas are not separately released. Paper §3.3, §4.3.
- g_obs = 4 G ΔΣ (singular isothermal sphere deprojection), validated by the authors against a shape-free piece-wise power-law method. Paper §2.2, App. B, §4.4.
- Systematic stellar-mass uncertainty ±0.2 dex, shown by the authors as a band (paper Fig. 4); the band is not part of the data release.
- **Source caveat:** for KiDS-bright, the isolation criterion "is no longer reliable when g_bar ≲ 10⁻¹³ m s⁻²" (R > 0.3 h70⁻¹ Mpc), where satellites raise ΔΣ by about 30 %. The authors state the GAMA results remain reliable there. Paper §5.2.
- Units carry h70; the Atlas takes h = 0.7 as the source does (physical units).

## Cite

Brouwer, M. M. et al. 2021, A&A 650, A113; with the KiDS acknowledgement given in that paper.
