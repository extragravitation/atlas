// Plain-language layer for each known issue (D-008). The expert layer is the issue's own text on
// GitHub; each line here says the same thing in everyday words, and claims no more than the issue.
// An issue without an entry gets the fallback, which points to the expert layer.
export const ISSUE_PLAIN = {
  8: 'In the disc-galaxy data (SPARC), 4 of about 2,700 points do not match the authors’ own published list. We do not say which is right, and we have asked the authors. The 4 points are ringed on the charts.',
  19: 'For 3 of the 12 X-COP clusters (A644, A2029 and A2319), the mass profiles in the public archive differ by a few per cent from the table in the paper. We do not say which is right. Their points are ringed, and we have asked the team.',
  64: 'The KiDS-1000 points were labelled as having no uncertainty, but only the pull from detected matter lacks one; the observed pull has error bars. The label was misleading. No number or chart was affected.',
  91: 'For 5 X-COP clusters the star masses were not measured. They are estimated with a formula that uses each cluster’s total mass, and that total comes from the cluster’s own hot gas, so the two sides of the comparison are not fully separate. These points stay marked until measured star masses are found or a ruling is made.',
  124: 'In X-COP version 1 we treated the star masses as if they were measured inside a ball, but the study measured them through a whole column of sky. That makes the pull from detected matter too large where stars matter, most of all near the cluster centres. For version 2, whether the star profiles behind the released numbers are measured the same way is not yet settled.',
  129: 'Seven X-COP clusters have no star measurements from the source, so they are kept in the record but not drawn. A planned later step that would draw them using the gas alone is on hold.',
  136: 'For the cluster A644, the authors’ published pull from detected matter cannot be rebuilt from the separate gas and star files they shared: near the centre it differs by up to about a third. We show their published values and have asked them.',
  139: 'In lens version 1, the uncertainty in the size of the ring of images was put on the wrong side of the comparison, and the effect of the assumed distance was left out. No number was wrong. Version 2 shows these uncertainties where they belong.',
  140: 'Some dwarf galaxies and star clusters in version 1 were drawn even though their own studies describe them as not settled, or set some of their data aside. Version 2 follows what the studies themselves say.',
  141: 'For the dwarf galaxy Phoenix II, version 1 used the spread of star speeds from all possible member stars, but the study prefers the value from its certain members. The two agree within their uncertainties. Version 2 uses the study’s preferred value.',
  156: 'For ten Andromeda dwarf galaxies, the study rejected stars outside speed limits that it drew in figures but never printed as numbers. We cannot apply limits that were never published, so our check of how much of each galaxy’s light is covered may include stars the study left out. We have asked the authors.',
  159: 'For the star cluster M54, the study left out data far from the centre because stars from a neighbouring galaxy get mixed in. We follow that cut, but two groups of stars may straddle it, and the published data cannot separate them.',
  160: 'The distances to nine star clusters come from a distance scale that was partly calibrated with star motions in some clusters. Each distance comes from the scale as a whole, not from that cluster’s own motions, so nothing changes; those rows carry a note.',
  168: 'For the KiDS-1000 version that adds assumed hot gas, the limit used to mark the less reliable bins may mark too few of them. These bins are not drawn on the map, and no number changes.',
  169: 'The KiDS-1000 study writes the distance within which a galaxy counts as alone in two ways, ten times apart. The bins affected are the same either way. The authors could be asked which is meant.',
  174: 'Papers on two lens galaxies mention gas, and dust in one of them, that the current lens data do not include. No number changes in this version; the next version will decide how to record them.',
  178: 'In the X-COP files for the cluster A3158, the total mass comes out negative at some distances from the centre, which cannot be right. A3158 is not drawn on the map, and we have asked the authors.',
  179: 'Our own frozen test for X-COP version 2 said every file has 21 rows; in fact they hold 19 to 27. This was our mistake in writing the test. The test is not changed, its result stands, and no number is affected.',
  190: 'For every dataset, the list of files we read gives each file’s address and fingerprint, but most entries do not repeat the citation and the terms of use, which are recorded elsewhere in the package. No number is affected; the next versions will add them.',
  191: 'Some of the papers the dwarf-galaxy numbers come from are not recorded with a fingerprint, and some references do not say where in the paper a number is. An audit re-checked the sampled numbers, and they agree.',
  192: 'For two lens samples, the references do not say exactly where in the paper the values are, or which study a file came from. An audit re-checked the values, and they agree.',
  193: 'For KiDS-1000 we record a fingerprint for the downloaded bundle of files, but not for each file inside it. No number is affected.',
};
export const ISSUE_PLAIN_FALLBACK = 'A problem with this dataset is recorded here. The technical view gives the details and the evidence.';
export function issuePlain(n) { return ISSUE_PLAIN[n] || ISSUE_PLAIN_FALLBACK; }
