// Plain versions of the not-plotted reasons recorded in the packages (audit v3 Part B, questions 5; D-125).
// The technical layer shows each reason exactly as recorded; the plain layer shows the matching sentence below.
// Unknown reasons fall back to the recorded text, so nothing is hidden.
const RULES = [
  [/^z_l ≥/, 'The lens is far away (redshift 0.30 or more). This version leaves such distant objects off the map and counts them as a gap.'],
  [/^no line-of-sight candidate passes the plotting rules/, 'The star-speed measurements cover too little of the cluster’s light, or have too few points, to give a reliable average.'],
  [/^Harris r_c reading rejected/, 'The size taken from the older catalogue failed a check against the source, so it is not used, and no other size is available.'],
  [/^Harris c carries a core-collapse flag/, 'The cluster’s core has collapsed, so the standard model of its shape does not apply, and no other model is available.'],
  [/^no tabulated population M\/L_V/, 'There is no published brightness-to-mass factor for its stars yet.'],
  [/^no structural model/, 'No published model of the cluster’s shape is available.'],
  [/^no Einstein radius or Einstein mass/, 'The source gives neither the size of the light-bending ring nor the mass inside it.'],
  [/^no Harris \(\d+\) horizontal-branch distance/, 'The catalogue gives no distance of the kind this dataset uses.'],
  [/^no Harris integrated magnitude/, 'The catalogue gives no total brightness for the cluster.'],
  [/^not early-type at source/, 'The source does not describe the lens as a round or lens-shaped galaxy, which this sample requires.'],
  [/^late-type lens galaxy/, 'The lens is a spiral or irregular galaxy, which this sample does not include.'],
  [/^morphology unclassified at source/, 'The source does not say what kind of galaxy the lens is.'],
  [/^lens and source redshifts not both measured spectroscopically/, 'The distances to the lens and to the background galaxy are not both measured directly.'],
  [/^kind not established at source/, 'The source does not establish what kind of galaxy the lens is.'],
  [/^grade [BC]: not a confirmed lens/, 'The source does not count it as a confirmed lens.'],
  [/^D-097 finding/, 'Its source reports star speeds rising towards the edge, which it says could be due to the cluster being pulled apart, so the method used here may not apply.'],
  [/^no line-of-sight profile \(proper motions only/, 'Only sideways star motions are measured, not motions towards and away from us, which this method needs.'],
  [/^classification disputed by sources/, 'Sources disagree on whether it is a star cluster or a small galaxy.'],
  [/^source structural parameters internally inconsistent/, 'The source’s size numbers do not agree with each other, so they are not used.'],
  [/^stellar mass not in the source/, 'The source gives no mass for the stars, so the pull from detected matter cannot be worked out in full.'],
];
export function plainReason(r) {
  const s = String(r || '');
  for (const [re, p] of RULES) if (re.test(s)) return p;
  return s;
}
