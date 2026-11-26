// Kinds whose sources or readers do not settle them (audit v3 Part B, B10; D-122). The packages code these
// systems A7 with a kind_label beginning "ambiguous"; A7 is defined as galaxies in unusual configurations
// (TAXONOMY_v2), so the site names them "kind not settled" instead. The package data are not changed.
export function unsettled(R) {
  const l = String((R && R.kind_label) || '');
  return /^ambiguous/i.test(l) ? l.replace(/^ambiguous:?\s*/i, '') : null;
}
export const UNSETTLED_KEY = 'not settled';
export function kindKey(R) { return unsettled(R) !== null ? UNSETTLED_KEY : R.taxonomy_kind; }
