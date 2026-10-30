// Display labels for the reading layers. Values and ranges never live here: they come from the
// registry (data/assumptions.json) and the packages.

export const DATASET = {
  'aeg-d-sparc': { t: 'SPARC', p: 'SPARC', kind_t: 'Disc galaxies, rotation curves', kind_p: 'Spinning disc galaxies', one_p: 'A spinning disc galaxy', unit: 'galaxy', units: 'galaxies', method_t: 'Rotation curves (dynamics)', method_p: 'Motions of stars and gas (spinning discs)' },
  'aeg-d-gc-baumgardt': { t: 'Baumgardt GCs', p: 'Globular clusters', kind_t: 'Globular clusters, line-of-sight dispersions', kind_p: 'Old star clusters in our galaxy', one_p: 'An old, dense ball of stars in our galaxy', unit: 'cluster', units: 'clusters', method_t: 'Stellar velocity dispersion at the half-light radius (dynamics)', method_p: 'How fast the stars swarm, at the size holding half the light' },
  'aeg-d-xcop': { t: 'X-COP', p: 'X-COP', kind_t: 'Galaxy clusters, X-ray hydrostatic', kind_p: 'Clusters of galaxies, hot gas in balance', one_p: 'A cluster of galaxies, with hot gas held in balance by the pull', unit: 'cluster', units: 'clusters', method_t: 'X-ray hydrostatic (dynamics)', method_p: 'Hot gas held in balance by the pull' },
  'aeg-d-kids1000-rar': { t: 'KiDS-1000', p: 'KiDS-1000', kind_t: 'Isolated galaxies, stacked weak lensing', kind_p: 'Single galaxies, light-bending averaged over many', unit: 'bin', units: 'stacked bins', method_t: 'Weak lensing, stacked (lensing)', method_p: 'Light-bending, averaged over many galaxies' },
};

export const ASSUMPTION = {
  ml_disk: { short: 'Υ_disk', t: 'Disc mass-to-light, Υ_disk', p: 'How much mass each unit of disc starlight stands for', kind: 'value' },
  ml_bulge: { short: 'Υ_bul', t: 'Bulge mass-to-light, Υ_bul', p: 'How much mass each unit of bulge starlight stands for', kind: 'value' },
  distance: { short: 'distance', t: 'Distance', p: 'How far away the galaxy is', kind: 'sigma' },
  inclination: { short: 'inclination', t: 'Inclination', p: 'How tilted the disc is as we see it', kind: 'sigma' },
  xray_hse_bias: { short: 'hydrostatic bias b', t: 'X-ray hydrostatic bias, b', p: 'Support of the hot gas not counted by assuming pressure balance from heat alone', kind: 'value' },
  icl_fraction: { short: 'intracluster light', t: 'Intracluster light', p: 'Starlight between the galaxies that the star counts leave out', kind: 'percent' },
};

export function assumptionLabel(id) { return ASSUMPTION[id] || { short: id, t: id, p: id, kind: 'value' }; }
export function datasetLabel(name) { return DATASET[name] || { t: name, p: name, kind_t: name, kind_p: name, unit: 'system', units: 'systems', method_t: name, method_p: name }; }

export function fmtParam(kind, v) {
  if (kind === 'sigma') return (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(1) + 'σ';
  if (kind === 'percent') return Math.round(v * 100) + '%';
  return Number(v).toFixed(2);
}

const SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹';
// A number to n significant figures, in powers of ten from 10⁴ up.
export function sigFig(v, n = 3) {
  if (!v) return '0';
  const e = Math.floor(Math.log10(Math.abs(v)));
  if (e < 4) return Number(v.toPrecision(n)).toString();
  return Number((v / 10 ** e).toPrecision(n)) + ' × 10' + String(e).replace(/[0-9]/g, (c) => SUP[c]);
}
