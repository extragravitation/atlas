// Uncertainty terms (tables/uncertainty_terms.ecsv; D-083): display names in both reading layers and
// the helpers that read a term's scope, status route and slider coverage from the package itself.
// No size or value lives here; everything numeric comes from the package or the registry.

// Names in both layers, and a plain description (the expert layer shows the package's own note).
// Keys are term ids without a per-system suffix (`_aeg-s-…`). No sizes here: they come from the table.
export const NAMES = {
  // SPARC
  g_bar_point: ['Per-point uncertainty on g_bar', 'Point-by-point uncertainty, detected matter', 'Uncertainty in the pull from detected matter that differs from one measurement to the next.'],
  g_bar_point_leo_t: ['Per-point uncertainty on g_bar (Leo T)', 'Point-by-point uncertainty, detected matter', 'The brightness of this galaxy is printed without an uncertainty.'],
  inclination: ['Inclination', 'Tilt of the disc', 'How tilted the disc is as we see it. It changes the observed pull of the whole galaxy at once.'],
  distance: ['Distance', 'Distance', 'How far away the system is. A different distance changes the pulls of the whole system at once.'],
  hi_flux_calibration: ['HI flux calibration (gas)', 'Gas measurement calibration', 'How well the radio measurement of the hydrogen gas is calibrated.'],
  ml_scatter_galaxy: ['Stellar mass-to-light ratio, galaxy to galaxy', 'How heavy the starlight is, galaxy by galaxy', 'Galaxies differ in how much mass each unit of starlight stands for.'],
  ml_disk: ['Stellar mass-to-light ratio, disc (population value)', 'How heavy the starlight is, disc (overall value)', 'One value used for the discs of all galaxies, with its published range.'],
  ml_bulge: ['Stellar mass-to-light ratio, bulge (population value)', 'How heavy the starlight is, bulge (overall value)', 'One value used for the central bulges of all galaxies, with its published range.'],
  geometry_3d_molecular: ['Disc thickness, bulge shape and molecular gas', 'Shape of the galaxy and unmeasured cold gas', 'The thickness of the disc, the shape of the bulge and gas that was not measured, mostly near the centre.'],
  // Dispersion systems: globular clusters and dwarf galaxies
  half_light_radius: ['Half-light radius R_h (measurement error)', 'Size holding half the light', 'How well the size is measured. It changes both pulls, so it is kept out of the error bars.'],
  ellipticity: ['Ellipticity (measurement error)', 'How flattened it looks', 'How well the flattening of its shape on the sky is measured.'],
  ellipticity_radial_variation: ['Ellipticity varying with radius', 'Shape changing from centre to edge', 'Some of these galaxies change shape from the centre outwards; one shape is used.'],
  rh_convention_profile: ['Half-light radius convention and profile family', 'How the size was defined', 'Papers define the size in slightly different ways.'],
  deprojection_4_3: ['Deprojection factor r½ ≈ (4/3) R_h', 'From the size on the sky to the size in space', 'Turning the size seen on the sky into a size in three dimensions uses a standard factor, which is approximate.'],
  distance_calibration_savino: ['Distance calibration (Savino et al. 2022)', 'Distance yardstick of one study', 'The method behind the distances from one study has its own uncertainty, shared by all its galaxies.'],
  distance_calibration_other: ['Distance calibration (other sources)', 'Distance yardstick of the other studies', 'The methods behind the other distances.'],
  velocity_error_model: ['Per-star velocity error model', 'How well each star’s speed is measured', 'Each study’s allowance for errors in the speeds of single stars.'],
  binaries: ['Binary stars', 'Stars in pairs', 'Stars orbiting a partner have extra motion of their own, which can raise the measured spread of speeds.'],
  membership: ['Membership', 'Which stars belong', 'Stars wrongly counted as members, or wrongly left out, change the measured spread of speeds.'],
  membership_contamination: ['Membership contamination', 'Which stars belong', 'Stars wrongly counted as members change the measured spread of speeds.'],
  rotation: ['Rotation', 'Spin', 'If the system spins, part of the motion is rotation rather than random swarming.'],
  light_weighting: ['Light weighting of σ', 'How the speeds are averaged', 'How the spread of speeds is averaged over the stars, compared with what the formula assumes.'],
  estimator_normalisation: ['Mass-estimator normalisation (Wolf et al. 2010)', 'Formula from speeds to pull', 'The standard formula that turns the spread of speeds into a pull is approximate.'],
  anisotropy_profile: ['Velocity anisotropy profile', 'Direction of the star motions', 'Whether stars move more in and out or more around changes the pull the formula gives.'],
  luminosity_function_martin: ['Luminosity function (Martin et al. 2016)', 'Counting faint stars (one study)', 'The total brightness includes stars too faint to see, added from an assumed mix of stars.'],
  luminosity_function_other: ['Luminosity function (other sources)', 'Counting faint stars (other studies)', 'The total brightness includes stars too faint to see, added from an assumed mix of stars.'],
  band_transformation: ['Photometric band transformation', 'Converting between colour filters', 'Brightness measured through one colour filter is converted to another.'],
  extinction: ['Extinction', 'Dimming by dust', 'Dust in our own galaxy dims the light; the correction for it is uncertain.'],
  solar_magnitude: ['Solar absolute magnitude', 'The Sun’s brightness as a yardstick', 'Brightness is counted in units of the Sun’s, and papers use slightly different values for it.'],
  stellar_ml: ['Stellar mass-to-light ratio Υ_V (range)', 'How heavy the starlight is', 'How much mass each unit of starlight stands for, with its published range.'],
  helium_factor: ['Helium correction factor', 'Helium added to the hydrogen', 'The measured hydrogen gas is scaled up by a standard factor for helium.'],
  gas_inside_rhalf: ['Gas inside r½', 'Gas inside the half-light size', 'Only the total gas is measured; a share of it is taken to lie inside.'],
  hi_flux: ['HI flux', 'Measured amount of hydrogen gas', 'How well the amount of hydrogen gas is measured.'],
  hi_limit_assumptions: ['HI upper-limit assumptions', 'Limits on undetected gas', 'Where no gas was detected, the limit depends on assumptions; such gas is counted as zero.'],
  molecular_ionised_gas: ['Molecular and ionised gas', 'Other kinds of gas', 'Gas in forms that were not measured for these galaxies.'],
  heterogeneity: ['Heterogeneity of the compilation', 'Mixing many studies', 'The numbers come from many studies made in different ways.'],
  king_w0: ['King model concentration W0', 'Shape of the cluster’s light profile', 'A fitted measure of how concentrated the light is.'],
  king_r0: ['King model scale radius r0', 'Core size of the light profile', 'The fitted size of the bright core.'],
  king_wilson_family: ['Model family (King or Wilson)', 'Choice of light-profile model', 'A different model of the light gives slightly different sizes.'],
  centre_position: ['Centre position', 'Where the centre is', 'How well the centre of the cluster is located.'],
  distance_hb_zero_point: ['Distance scale: horizontal-branch zero point', 'Distance yardstick: its calibration', 'Distances come from stars of a known brightness; how that brightness is calibrated.'],
  distance_hb_slope: ['Distance scale: horizontal-branch metallicity slope', 'Distance yardstick: effect of composition', 'How the yardstick stars’ brightness depends on their chemical make-up.'],
  distance_hb_scatter: ['Distance scale: scatter about the calibration', 'Distance yardstick: cluster-to-cluster scatter', 'Single clusters scatter about the calibration.'],
  reddening: ['Reddening E(B−V)', 'Dimming and reddening by dust', 'How much dust dims and reddens the light on its way to us.'],
  extinction_law_rv: ['Extinction law R_V', 'How dust dims different colours', 'The assumed link between reddening and dimming.'],
  integrated_magnitude: ['Integrated V magnitude', 'Total brightness of the cluster', 'How well the total brightness is measured.'],
  ml_population: ['Population mass-to-light ratio (model error)', 'How heavy the starlight is: model uncertainty', 'The uncertainty of the star-population model for this cluster, from its age and make-up.'],
  pop_synthesis_code: ['Population-synthesis code', 'Choice of star-population model', 'Different models of star populations give slightly different weights for the same light.'],
  tracer_mass: ['Tracer-star mass', 'Which stars were measured', 'Bright giant stars and fainter stars can move at slightly different speeds.'],
  rv_zero_points: ['Radial-velocity zero points', 'Matching speed scales between studies', 'Speeds from different instruments are shifted onto one scale.'],
  // KiDS-1000
  esd_to_gobs_conversion: ['ΔΣ-to-g_obs conversion', 'Turning the light-bending signal into a pull', 'The paper adds this to every error bar; the released errors leave it out.'],
  shear_calibration: ['Shear calibration', 'Calibration of the galaxy-shape measurements', 'The correction applied to the measured shapes of background galaxies.'],
  source_redshift_calibration: ['Source redshift calibration', 'Distances to the background galaxies', 'How well the distances of the background galaxies are known.'],
  random_subtraction: ['Random-point subtraction', 'Background signal removed', 'A small signal measured around random points is subtracted.'],
  stellar_mass_per_lens_kids: ['Per-galaxy stellar-mass scatter (KiDS-bright)', 'Star mass of each galaxy (KiDS-bright)', 'Errors in each galaxy’s star mass move galaxies between groups.'],
  stellar_mass_per_lens_gama: ['Per-galaxy stellar-mass scatter (GAMA)', 'Star mass of each galaxy (GAMA)', 'Errors in each galaxy’s star mass move galaxies between groups.'],
  stellar_mass_systematic: ['Stellar-mass systematic', 'Overall star-mass scale', 'All star masses could be higher or lower together.'],
  gama_normalisation: ['Normalisation to GAMA stellar masses', 'Matching two star-mass scales', 'One survey’s star masses are shifted to match the other’s.'],
  cold_gas_relation: ['Cold-gas scaling relation', 'Estimated cold gas', 'The cold gas is estimated from a relation with star mass, not measured.'],
  isolation_satellites: ['Isolation criterion: satellite contamination', 'Nearby smaller galaxies', 'Small neighbouring galaxies can add to the light-bending signal far from the centre.'],
  cosmology_h70: ['Cosmology (h70 units)', 'Model of the expanding universe', 'Distances depend on the assumed expansion of the universe.'],
  // Strong lenses
  theta_e: ['Einstein radius θ_E (measurement error)', 'Size of the ring', 'How well the ring size is measured. It changes the pull from detected matter and the radius, not the observed pull.'],
  theta_e_ngc6505: ['Einstein radius θ_E (NGC 6505)', 'Size of the ring (one lens)', 'How well the ring size of this lens is measured; the paper calls its numbers lower bounds.'],
  ellipticity_j0403: ['Lens-mass ellipticity (J0403−0239)', 'Flattening of the lens (one lens)', 'A flattened mass model raises the mass inside the ring a little.'],
  lens_model_profile: ['Lens-model mass profile', 'Shape assumed for the lens mass', 'The ring size fitted depends a little on the shape assumed for the mass.'],
  sie_axis_convention: ['SIE axis convention', 'How the ring size is defined', 'For a flattened lens, the ring size can be defined along different axes.'],
  external_shear: ['External shear', 'Tug of nearby mass on the light path', 'Mass near the lens distorts the ring a little.'],
  external_convergence: ['External convergence (line of sight)', 'Matter along the line of sight', 'Matter in front of or behind the lens adds a little light-bending.'],
  line_of_sight_snl0: ['Line-of-sight structure (SNL-0)', 'Matter along the line of sight (one lens)', 'Matter in front of or behind this lens adds a little light-bending.'],
  lens_light_subtraction: ['Lens-light subtraction', 'Removing the lens galaxy’s own light', 'The lens galaxy’s light is removed to see the ring; that step can shift the fit.'],
  aperture_radius_snl12: ['Aperture radius (SNL-1, SNL-2)', 'Size of the measuring circle (two lenses)', 'The circle used differs a little from the ring measured later.'],
  companion_snl2: ['Companion galaxy (SNL-2)', 'A neighbouring galaxy (one lens)', 'A nearby galaxy affects the fit of this lens.'],
  redshift_measurement: ['Redshift measurement', 'Measured redshifts', 'How well the redshifts of the lens and the background galaxy are measured.'],
  redshift_lens_ngc6505: ['Lens redshift (NGC 6505)', 'Redshift of the lens (one lens)', 'How well the lens galaxy’s redshift is measured.'],
  redshift_source_ngc6505: ['Source redshift (NGC 6505)', 'Redshift of the background galaxy (one lens)', 'How well the background galaxy’s redshift is measured.'],
  cosmology_h0: ['Hubble constant H0', 'Expansion rate of the universe', 'Distances, and so the observed pull, depend on the assumed expansion rate.'],
  cosmology_h0_snells: ['Hubble constant H0 (SNELLS)', 'Expansion rate of the universe (SNELLS lenses)', 'Distances, and so the observed pull, depend on the assumed expansion rate.'],
  cosmology_h0_j0403: ['Hubble constant H0 (J0403−0239)', 'Expansion rate of the universe (one lens)', 'Distances, and so the observed pull, depend on the assumed expansion rate.'],
  cosmology_h0_manga: ['Hubble constant H0 (MaNGA)', 'Expansion rate of the universe (MaNGA lenses)', 'Distances, and so the observed pull, depend on the assumed expansion rate.'],
  cosmology_omega_m: ['Matter density Ω_m', 'Model of the expanding universe', 'Distances depend on the assumed make-up of the universe.'],
  lens_distance_snl0: ['Lens distance (SNL-0)', 'Distance to the lens galaxy (one lens)', 'The galaxy’s own motion blurs the distance worked out from its redshift.'],
  lens_distance_snl1: ['Lens distance (SNL-1)', 'Distance to the lens galaxy (one lens)', 'The galaxy’s own motion blurs the distance worked out from its redshift.'],
  lens_distance_snl2: ['Lens distance (SNL-2)', 'Distance to the lens galaxy (one lens)', 'The galaxy’s own motion blurs the distance worked out from its redshift.'],
  lens_distance_ngc6505: ['Lens distance (NGC 6505)', 'Distance to the lens galaxy (one lens)', 'Two redshifts are printed for this galaxy, and the paper does not say which it uses.'],
  lens_distance_other: ['Lens distance (other lenses)', 'Distance to the lens galaxy', 'The galaxy’s own motion blurs the distance worked out from its redshift.'],
  aperture_factor_slacs: ['Aperture factor (SLACS)', 'Share of the stars inside the ring (SLACS)', 'The share of the star mass inside the ring is worked out from the light.'],
  r_eff_slacs: ['Effective radius R_e (SLACS)', 'Size of the galaxy’s light (SLACS)', 'How well the size holding half the light is measured.'],
  r_eff_sl2s: ['Effective radius R_e (SL2S)', 'Size of the galaxy’s light (SL2S)', 'How well the size holding half the light is measured.'],
  r_eff_s4tm: ['Effective radius R_e (S4TM)', 'Size of the galaxy’s light (S4TM)', 'How well the size holding half the light is measured.'],
  sps_templates_slacs: ['Stellar-population templates (SLACS)', 'Star models used for the mass (SLACS)', 'The star mass depends on the models of star populations used.'],
  sps_systematic_s4tm: ['Stellar-population systematic (S4TM)', 'Star models used for the mass (S4TM)', 'The star mass depends on the models of star populations used.'],
  sps_template_sl2s: ['Stellar-population template (SL2S)', 'Star models used for the mass (SL2S)', 'The star mass depends on the models of star populations used.'],
  luminosity_corrections_manga: ['Luminosity corrections (MaNGA)', 'Corrections to the brightness (MaNGA)', 'Corrections for dust, colour shift and blurring.'],
  upsilon_ref_manga: ['Reference mass-to-light ratio Υ_ref (MaNGA)', 'How heavy the starlight is (MaNGA)', 'One value shared by both lenses, with the range the models span.'],
  pop_model_family_j0403: ['Population-model family (J0403−0239)', 'Choice of star models (one lens)', 'A different family of star models gives a different star mass.'],
  pop_age_j0403: ['Population age (J0403−0239)', 'Assumed age of the stars (one lens)', 'A different age for the stars gives a different star mass.'],
  pop_model_family_manga: ['Population-model family (MaNGA)', 'Choice of star models (MaNGA lenses)', 'A different family of star models gives a different star mass.'],
  alpha_fe: ['[α/Fe] abundance', 'Chemical make-up of the stars', 'The star mass depends a little on the stars’ chemical make-up.'],
  stellar_imf: ['Stellar IMF (Chabrier/Kroupa to Salpeter)', 'How many faint stars there are for each bright one', 'Faint stars add mass but little light, so the star mass depends on how many there are.'],
  gas_in_re: ['Gas inside R_E', 'Gas inside the ring', 'Nobody has measured it for these lenses; a share from similar galaxies is used.'],
  neighbour_light_snl2: ['Neighbour light (SNL-2)', 'Light from a neighbouring galaxy (one lens)', 'Some light inside the ring comes from a neighbour.'],
  internal_dust_snl1: ['Internal dust (SNL-1)', 'Dust inside the lens galaxy (one lens)', 'Dust in the lens galaxy dims its light.'],
  lensed_source_light: ['Lensed-source light', 'Light of the background galaxy', 'Light from the bent image of the background galaxy mixed into the lens’s light.'],
  aperture_shape: ['Aperture shape', 'Round circle against an oval ring', 'The star mass is counted in a circle, while the ring may be oval.'],
  // X-COP
  radial_covariance: ['Covariance between radii', 'Links between neighbouring points', 'Errors at neighbouring distances are linked, but the links are not released.'],
  np_smoothing: ['Non-parametric smoothing', 'Smoothing of the profile', 'Details smaller than the measuring step are smoothed out.'],
  reconstruction_bias: ['Reconstruction bias', 'Accuracy of the method', 'How far the method could be off, tested by the source on simulated clusters.'],
  hse_bias: ['Hydrostatic bias', 'Gas support not counted by heat alone', 'If part of the gas is held up by motion rather than by heat, the observed pull comes out too low.'],
  hse_bias_a2319: ['Hydrostatic bias (A2319)', 'Gas support not counted by heat alone (this cluster)', 'The source calls this cluster strongly affected, without a size.'],
  nonthermal_pressure: ['Non-thermal pressure fraction', 'Gas motions besides heat', 'The share of the gas’s support that comes from motion, from a related study.'],
  gas_inhomogeneity: ['Gas inhomogeneity', 'Clumpy gas', 'Gas that is clumpy rather than smooth.'],
  xmm_calibration: ['XMM-Newton calibration', 'Calibration of the X-ray telescope', 'Two X-ray telescopes give somewhat different gas temperatures.'],
  mass_model_choice: ['Mass-model choice', 'Choice of method for the observed pull', 'Different fitting methods give somewhat different pulls; worked out by the Atlas from the source’s own results.'],
  cosmology: ['Cosmology', 'Model of the expanding universe', 'Distances depend on the assumed expansion of the universe.'],
  gas_density_conversion: ['X-ray emissivity to gas density', 'Turning the X-ray glow into an amount of gas', 'How the X-ray glow is turned into gas density.'],
  bcg_ml: ['Central-galaxy mass-to-light ratio', 'How heavy the central galaxy’s starlight is', 'How much mass each unit of the central galaxy’s light stands for.'],
  bcg_ml_extra_mass_model: ['Central-galaxy M/L: extra mass component in the model', 'Central galaxy: effect of the model used', 'Adding a further mass term to the model of the central galaxy lowers its star mass.'],
  bcg_jam_geometry: ['Central-galaxy dynamical-model geometry', 'Central galaxy: shape assumed in the model', 'The star mass changes with the shape assumed in the model.'],
  bcg_sersic_extrapolation: ['Central-galaxy light extrapolation', 'Central galaxy: light beyond where it was measured', 'Beyond the measured part, the light is extended with a fitted curve.'],
  satellite_cosmic_variance: ['Satellite galaxies: cosmic variance', 'Other galaxies: chance variation', 'Chance variation in the number of other galaxies.'],
  satellite_flux: ['Satellite galaxies: flux', 'Other galaxies: brightness', 'How well the brightness of the other galaxies is measured.'],
  satellite_gnfw_smoothing: ['Satellite galaxies: profile smoothing', 'Other galaxies: smoothed profile', 'Their profile is noisy and is smoothed with a fitted curve.'],
  satellite_projection: ['Satellite galaxies: projection', 'Other galaxies: seen through the whole cluster', 'Whether the star mass was counted in a ball or through a column of sky is not stated.'],
  satellite_mass_systematic: ['Satellite galaxies: stellar-mass systematic', 'Other galaxies: overall star-mass scale', 'All their star masses could be higher together.'],
  icl_omitted: ['Intracluster light (omitted)', 'Starlight between the galaxies', 'Not counted in the pull from detected matter.'],
};

export const termBase = (id) => id.replace(/_aeg-s-\d+$/, '');
export const termName = (t) => NAMES[termBase(t.term_id)] || [t.term_id.replace(/_/g, ' '), t.term_id.replace(/_/g, ' '), 'See the dataset page.'];
const ids = (t) => String(t.applies_to || '').split(';').filter(Boolean);
export const termApplies = (t, sysId) => t.applies_to === '*' || ids(t).includes(sysId);

// A column's description in the package's datapackage.json (resource matched by name or path).
export function fieldDesc(d, resource, col) {
  const r = (d.dp.resources || []).find((x) => new RegExp(resource).test(x.name || x.path || ''));
  return ((r?.schema?.fields || []).find((f) => f.name === col) || {}).description || '';
}

// A size the Atlas computed rather than read: the package marks its size column "Atlas-computed".
// Returns the column's description, which states the rule, or null.
export function atlasComputed(d, t) {
  if (!t.size_column) return null;
  const desc = fieldDesc(d, 'systems', t.size_column) || fieldDesc(d, 'measurements', t.size_column);
  return /Atlas-computed/.test(desc) ? desc : null;
}

// Systems that have measurement rows in this package.
export const systemsWithRows = (d) => new Set(d.measurements.rows.map((r) => r.system_id));

// Systems a term is limited to, when that is fewer than the systems with rows; null when the term
// covers every system with rows (applies_to `*`, or a list that includes all of them).
export function termScope(d, t) {
  if (!t.applies_to || t.applies_to === '*') return null;
  const list = ids(t), have = systemsWithRows(d);
  return [...have].every((s) => list.includes(s)) ? null : list;
}

// g_bar is released only as a total: every row's component columns are empty and at least one
// component is recorded as not separable from the total.
export function gbarTotalOnly(d) {
  const rows = d.measurements.rows;
  const comps = ['g_bar_stars', 'g_bar_stars_disk', 'g_bar_stars_bulge', 'g_bar_gas_cold', 'g_bar_gas_hot'];
  return rows.length > 0 && rows.every((r) => comps.every((c) => r[c] === null || r[c] === undefined || r[c] === '')
    && ['stars_status', 'gas_hot_status', 'gas_cold_status'].some((c) => r[c] === 'not_separable'));
}

// Terms on g_bar that have a size (stated by the source or another source, or computed) and no
// registry assumption, in a package that releases g_bar only as a total: they cannot have a slider.
export function fixedGbarTerms(d) {
  if (!d.terms || !gbarTotalOnly(d)) return [];
  const has = (v) => v !== null && v !== undefined && v !== '';
  return d.terms.filter((t) => t.moves === 'g_bar' && t.status !== 'not_given_by_source' && !t.assumption_id
    && (has(t.size_value) || has(t.size_lo) || has(t.size_hi) || has(t.size_column)));
}

// Systems (with rows) for which every term tied to assumption `aid` has no size from the source:
// a slider for `aid` then moves them only across the registry's dataset-wide range.
export function unsizedSystems(d, aid) {
  const tied = (d.terms || []).filter((t) => t.assumption_id === aid);
  if (!tied.length) return [];
  return [...systemsWithRows(d)].filter((s) => { const ts = tied.filter((t) => termApplies(t, s)); return ts.length > 0 && ts.every((t) => t.status === 'not_given_by_source'); });
}

// Site-side handling of package notes, from the X-COP v2 neutrality audit
// (docs/audit/neutrality_xcop_v2.md, Resolution). The package files are never edited; a sentence
// is dropped or a route added here only with the reason shown on the page. The build fails if the
// package text changes, so a stale edit cannot silently persist.
const NOTE_EDITS = {
  'aeg-d-xcop/v2': {
    mass_model_choice: {
      drop: 'An equally conventional alternative, half the spread of the three masses, would give roughly half the size.',
      extra: 'One sentence of the package note, comparing this size with an alternative rule, is not shown here: that comparison was never computed.',
    },
    cosmology: {
      extra: 'The two other values, as stated by the sources named: H0 = 73 by Loubser et al. 2020 (central galaxy) and H0 = 70 by van der Burg et al. 2015 (satellites). The package records no line for them; one reader’s line references are in docs/sources/readings/xcop-e22-2026-11-03/reader-A.md (l. 319).',
    },
  },
};
// [note text to show, extra sentence or null]
export function termNote(d, t) {
  const e = NOTE_EDITS[d.key]?.[termBase(t.term_id)];
  let text = t.note || '—';
  if (!e) return [text, null];
  if (e.drop) {
    if (!text.includes(e.drop)) throw new Error(`terms: sentence to drop not found in ${d.key} ${t.term_id}`);
    text = text.replace(' ' + e.drop, '').replace(e.drop, '');
  }
  return [text, e.extra || null];
}

// Notes shown by a slider (and under the dataset page's assumption table), in both layers:
// `range` where the package gives no size for a system the slider moves (X-COP v2 audit X4), and
// `fixed` for g_bar terms with sizes that no slider can move (JvH's ruling on the slider asymmetry).
export function sliderNotes(dd, a, page = null) {
  const e = a.datasets[dd.key];
  // Where the package gives no size for a system this slider moves, the range is the registry's
  // dataset-wide range, not one stated for that system (X-COP v2 audit X4).
  const sname = (id) => (dd?.systems?.rows.find((s) => s.system_id === id) || {}).name_in_source || id;
  const unsized = dd ? unsizedSystems(dd, a.id) : [];
  const tied = (dd?.terms || []).filter((t) => t.assumption_id === a.id && t.status === 'not_given_by_source').map((t) => t.term_id);
  const rangeNote = !unsized.length ? null : page && unsized.includes(page)
    ? [`No size of this assumption is stated for ${sname(page)} (${tied.join(', ')}). The range shown is the registry’s dataset-wide range (scope: dataset; see Sources), not one stated for ${sname(page)}.`, `The source gives no size for ${sname(page)}. The range is the one for the whole dataset, not one stated for ${sname(page)}.`]
    : [`The range is the registry’s dataset-wide range (scope: dataset). For ${unsized.map(sname).join(', ')} the source states no size (${tied.join(', ')}), so it is not a range stated for ${unsized.length === 1 ? 'that system' : 'those systems'}.`, `The range is the one for the whole dataset. For ${unsized.map(sname).join(', ')} the source gives no size of its own.`];
  // g_bar terms with sizes that no slider can move, because g_bar is released only as a total
  // (JvH's ruling on the X-COP v2 slider asymmetry). Shown by a slider that moves only g_obs.
  const onlyObs = (e.effects || []).length > 0 && (e.effects || []).every((x) => /^g_obs/.test(x.column));
  const fixed = dd && onlyObs ? [...new Map(fixedGbarTerms(dd).map((t) => [termName(t)[0], termName(t)])).values()] : [];
  const fixedNote = fixed.length ? [`The g_bar terms with published sizes (${fixed.map((n) => n[0]).join('; ')}; sizes in the dataset’s uncertainty table) cannot be adjusted, because the source releases g_bar only as a total. The Atlas does not split it without the components. The authors have been asked for the component profiles.`, `The uncertainties in the pull from detected matter that have published sizes (${fixed.map((n) => n[1].charAt(0).toLowerCase() + n[1].slice(1)).join('; ')}; sizes in the dataset’s uncertainty table) cannot be changed here, because the source gives that pull only as one total. We do not split it without the separate parts, and we have asked the authors for them.`] : null;
  return { range: rangeNote, fixed: fixedNote };
}
