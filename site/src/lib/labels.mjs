// Display labels for the reading layers. Values and ranges never live here: they come from the
// registry (data/assumptions.json) and the packages.

export const DATASET = {
  'aeg-d-sparc': { t: 'SPARC', p: 'SPARC', kind_t: 'Disc galaxies, rotation curves', kind_p: 'Spinning disc galaxies', one_p: 'A spinning disc galaxy', unit: 'galaxy', units: 'galaxies', method_t: 'Rotation curves (dynamics)', method_p: 'Motions of stars and gas (spinning discs)' },
  'aeg-d-gc-baumgardt': { t: 'Baumgardt GCs', p: 'Globular clusters', kind_t: 'Globular clusters, line-of-sight dispersions', kind_p: 'Old star clusters in our galaxy', one_p: 'An old, dense ball of stars in our galaxy', unit: 'cluster', units: 'clusters', method_t: 'Stellar velocity dispersion at the half-light radius (dynamics)', method_p: 'How fast the stars swarm, at the size holding half the light' },
  'aeg-d-dwarfs': { t: 'Local Group dwarfs', p: 'Dwarf galaxies', kind_t: 'Dwarf galaxies of the Local Group, line-of-sight dispersions', kind_p: 'Small faint galaxies near ours', one_p: 'A small, faint galaxy near our own', unit: 'galaxy', units: 'galaxies', method_t: 'Stellar velocity dispersion at the half-light radius (dynamics)', method_p: 'How fast the stars swarm, at the size holding half the light' },
  'aeg-d-xcop': { t: 'X-COP', p: 'X-COP', kind_t: 'Galaxy clusters, X-ray hydrostatic', kind_p: 'Clusters of galaxies, hot gas in balance', one_p: 'A cluster of galaxies, with hot gas held in balance by the pull', unit: 'cluster', units: 'clusters', method_t: 'X-ray hydrostatic (dynamics)', method_p: 'Hot gas held in balance by the pull' },
  'aeg-d-strong-lensing': { t: 'Strong lenses (A6)', p: 'Lensing galaxies', kind_t: 'Early-type galaxies, strong lensing at the Einstein radius (projected)', kind_p: 'Single galaxies that bend light into rings and arcs', one_p: 'A galaxy whose pull bends the light of a galaxy behind it into a ring or arcs', unit: 'lens', units: 'lenses', method_t: 'Strong lensing, mass inside the Einstein radius (lensing, projected)', method_p: 'Light-bending, measured inside the ring of images, seen in projection' },
  'aeg-d-kids1000-rar': { t: 'KiDS-1000', p: 'KiDS-1000', kind_t: 'Isolated galaxies, stacked weak lensing', kind_p: 'Single galaxies, light-bending averaged over many', unit: 'bin', units: 'stacked bins', method_t: 'Weak lensing, stacked (lensing)', method_p: 'Light-bending, averaged over many galaxies' },
};

export const ASSUMPTION = {
  ml_disk: { short: 'Υ_disk', t: 'Disc mass-to-light, Υ_disk', p: 'How much mass each unit of disc starlight stands for', kind: 'value' },
  ml_bulge: { short: 'Υ_bul', t: 'Bulge mass-to-light, Υ_bul', p: 'How much mass each unit of bulge starlight stands for', kind: 'value' },
  distance: { short: 'distance', t: 'Distance', p: 'How far away the galaxy is', kind: 'sigma' },
  inclination: { short: 'inclination', t: 'Inclination', p: 'How tilted the disc is as we see it', kind: 'sigma' },
  xray_hse_bias: { short: 'hydrostatic bias b', t: 'X-ray hydrostatic bias, b', p: 'Support of the hot gas not counted by assuming pressure balance from heat alone', kind: 'value' },
  gc_stellar_ml: { short: 'Υ_V (clusters)', t: 'Cluster stellar mass-to-light, Υ_V', p: 'How much mass each unit of cluster starlight stands for', kind: 'span' },
  dw_stellar_ml: { short: 'Υ_V (dwarfs)', t: 'Dwarf stellar mass-to-light, Υ_V', p: 'How much mass each unit of dwarf-galaxy starlight stands for', kind: 'span' },
  a6s_stellar_imf: { short: 'IMF (lenses)', t: 'Stellar initial mass function, Chabrier/Kroupa to Salpeter', p: 'How many faint, low-mass stars there are for each bright one', kind: 'imf' },
  a6s_gas_in_RE: { short: 'gas in R_E', t: 'Gas inside the Einstein radius, as a fraction of the stars', p: 'How much gas sits inside the ring, compared with the stars', kind: 'range' },
  icl_fraction: { short: 'intracluster light', t: 'Intracluster light', p: 'Starlight between the galaxies that the star counts leave out', kind: 'percent' },
};

export function assumptionLabel(id) { return ASSUMPTION[id] || { short: id, t: id, p: id, kind: 'value' }; }
export function datasetLabel(name) { return DATASET[name] || { t: name, p: name, kind_t: name, kind_p: name, unit: 'system', units: 'systems', method_t: name, method_p: name }; }

// Position in an asymmetric published range (D-039): −1 = 0.53 × the default, 0 = default, +1 = Salpeter value.
export function spanText(v) {
  v = Number(v);
  if (Math.abs(v) < 1e-9) return 'default';
  if (v < 0) return `${(1 - 0.47 * Math.abs(v)).toFixed(2)} × default`;
  return v >= 1 ? 'Salpeter value' : `${Math.round(v * 100)}% to Salpeter`;
}

// IMF position (A6S_PRECEDENCE §3.2): 0 = Chabrier/Kroupa as printed, 1 = Salpeter.
export function imfText(v) {
  v = Number(v);
  if (Math.abs(v) < 1e-9) return 'Chabrier/Kroupa';
  return v >= 1 ? 'Salpeter' : `${Math.round(v * 100)}% to Salpeter`;
}

// Position in a registered range: −1 = minimum, 0 = default, +1 = maximum.
export function rangeText(v) {
  v = Number(v);
  if (Math.abs(v) < 1e-9) return 'default';
  if (v <= -1) return 'minimum';
  if (v >= 1) return 'maximum';
  return `${Math.round(Math.abs(v) * 100)}% to ${v < 0 ? 'minimum' : 'maximum'}`;
}

export function fmtParam(kind, v) {
  if (kind === 'sigma') return (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(1) + 'σ';
  if (kind === 'percent') return Math.round(v * 100) + '%';
  if (kind === 'span') return spanText(v);
  if (kind === 'imf') return imfText(v);
  if (kind === 'range') return rangeText(v);
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
