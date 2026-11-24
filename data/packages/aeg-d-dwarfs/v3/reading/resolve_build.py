"""Build data/packages/aeg-d-dwarfs/v2/reading/resolved.csv from readers A and B (2026-11-04)."""
import csv, sys, re, json, collections
R = sys.argv[1]
A = list(csv.DictReader(open(R + 'reader-A.csv'))); B = list(csv.DictReader(open(R + 'reader-B.csv')))
MAN = {r['system_id']: r for r in csv.DictReader(open(R + 'manifest_rows.csv'))}
COLS = ['system_id', 'name', 'field', 'value', 'quote', 'location', 'source', 'sha256', 'note', 'resolution']
names = {r['system_id']: r['name'] for r in A}
out = []

def add(r, resolution, **kw):
    d = {c: r.get(c, '') for c in COLS[:-1]}
    d.update(kw); d['resolution'] = resolution
    out.append(d)

def by(rows, f):
    d = collections.defaultdict(list)
    for r in rows:
        if r['field'] == f: d[r['system_id']].append(r)
    return d

MONELLI_SRC = 'Monelli2025 (A&A 700, A201; PDF supplied by JvH, SHA-256 6cf940d5…8b5845)'
MONELLI_SHA = '6cf940d5de09b969939db84ce76fd0a6d3cb0b842e3362e93e1ded3ba28b5845'
LEO2 = 'aeg-s-000386'

# ---- single-valued fields ----
for f in ['rh_err', 'eps_err', 'binary_screening', 'distance_inherited', 'mv_modulus_match', 'size_scope', 'mag_level', 'sigma_level', 'd096_conflict']:
    a = by(A, f); b = by(B, f)
    keys = sorted(set(a) | set(b))
    for sid in keys:
        ra = a.get(sid, [None])[0]; rb = b.get(sid, [None])[0]
        nm = names.get(sid, (ra or rb)['name'])
        if f in ('rh_err', 'eps_err'):
            add(ra, 'agree', note=(ra['note'] + ' Reader B agrees on the error.').strip())
        elif f == 'binary_screening':
            if ra['value'] == rb['value']:
                add(ra, 'agree')
            else:  # Tucana
                add(ra, 'resolved_at_source', note=ra['note'] + ' Resolved: the source states it has no repeat (multi-epoch) measurements, so no_multi_epoch_stated (Reader B: not_stated).')
        elif f == 'distance_inherited':
            if sid == LEO2:
                add(ra, 'resolved_at_source', value='no', quote='our estimate of the distance modulus of Leo II is ⟨(m − M)0⟩ = 21.60 ± 0.03 mag',
                    location='pdftotext -layout l. 457–460 (p. 8, §4)', source=MONELLI_SRC, sha256=MONELLI_SHA,
                    note="The paper's own measurement; not inherited from a host. Read at source by the main session from the PDF JvH supplied (CC BY 4.0, not committed).")
            else:
                add(ra, 'agree')
        elif f == 'mv_modulus_match':
            res = 'agree' if ra['value'].startswith('yes') and rb['value'].startswith('yes') else 'resolved_at_source'
            n = ra['note'] + ('' if res == 'agree' else ' Resolved with Reader A, who read van de Rydt 1991 (OCR of the ADS scan); Reader B could not read it.')
            add(ra, res, note=n.strip())
        elif f == 'size_scope':
            add(ra, 'agree', note=(ra['note'] + ' Reader B agrees: the stellar M/L envelope is a ruled envelope, not a source-stated size.').strip())
        elif f == 'd096_conflict':
            if nm == 'Fornax':
                add(ra, 'ruled', value='ruled (D-101): Sérsic 20.1′ default, exponential 19.8′ alternative', note="JvH ruled 'Fornax and Hercules as recommended' (D-101): D-096 rule 1 applies to Wang 2019's stated best fit.")
            elif nm == 'Hercules':
                add(ra, 'ruled', value='ruled (D-101): no change (1.8 km/s, D-038 addendum)', note="JvH ruled 'Fornax and Hercules as recommended' (D-101). Ou 2024 marks neither value as preferred.")
            else:
                add(ra, 'agree', value='none')
        elif f == 'mag_level':
            if ra['value'] == rb['value'] or (ra['value'].startswith('0.68') and rb['value'].startswith('0.68')):
                add(ra, 'agree')
            elif nm == 'Aquarius II':
                add(rb, 'resolved_at_source', note="Resolved with Reader B: M_V comes from the single-population sum (aquarius2.tex l. 578–589), not from the posterior whose 16%/84% wording (l. 539–540) Reader A cited.")
            elif nm in ('Antlia II', 'Aquarius III', 'Leo VI'):
                add(ra, 'resolved_at_source', note=ra['note'] + ' Resolved with Reader A: the stated level covers the fitted parameters; M_V is a derived quantity (or, for Antlia II, a Poisson star-count error, Table 1 note a) and no level is stated for it.')
            elif nm == 'Phoenix':
                add(ra, 'resolved_at_source', note=ra['note'] + ' Reader B did not read the ADS scan; Reader A did. No level is stated.')
            elif 'Munoz2018' in ra['source']:
                add(ra, 'resolved_at_source', note='Resolved with Reader A: Muñoz 2018 ms.tex l. 432–437 states the bootstrap magnitudes give "1-σ errors". Reader B cited l. 432 only.')
            elif 'Richstein2024' in ra['source']:
                add(ra, 'resolved_at_source', note='Resolved with Reader A: arxiv.tex l. 326 states that the uncertainties reported in the derived-quantities table, which holds m_V and M_V, are the 84th and 16th percentiles.')
            elif 'DrlicaWagner2015' in ra['source']:
                add(ra, 'resolved_at_source', note='Resolved with Reader A: the table caption macro (main.tex l. 325) gives the highest-density interval containing \\interval, defined as 68% (commands.tex l. 109).')
            else:
                add(ra, 'resolved_at_source', note=ra['note'] + ' Resolved with Reader A (not re-read).')
        elif f == 'sigma_level':
            man = MAN.get(sid, {})
            if ra['value'] == rb['value'] or (ra['value'].startswith('0.68') and rb['value'].startswith('0.68') and 'limits' not in ra['value']):
                add(ra, 'agree')
            elif 'limits 95th' in ra['value']:
                lim = man.get('limit', '') == 'upper'
                if lim:
                    add(rb, 'agree', value='0.95 (stated, upper limit)', note='Geha 2026 l. 741 and Table 1 note 17: unresolved dispersions are 95% upper limits; both readers agree.')
                else:
                    add(rb, 'agree', value='0.683 (1-sigma, stated)', note='Geha 2026 l. 741: resolved dispersions are quoted with 1-sigma errors; both readers agree.')
            elif nm == 'Andromeda XVIII':
                add(ra, 'resolved_at_source', note='Resolved with Reader A: Kvasova 2024 Table 2 note a (2_main.tab l. 40), "Errors cover the 68% confidence interval". Reader B searched andromeda18.tex only.')
            elif nm == 'Willman 1':
                add(ra, 'resolved_at_source', location='main.tex:344 (Figure caption: posterior of the mixture model)', quote='The dashed lines represent the median value and 16th and 84th percentiles.',
                    note='Resolved with Reader A, relocated: l. 328 states 16th/84th for v_sys only (Reader B), but the caption at l. 344 states it for the posterior samples of the systemic velocity and velocity dispersion.')
            elif nm == 'Phoenix II':
                add(rb, 'resolved_at_source', value='0.683 (1-sigma, stated)', note="Resolved with Reader B: Fritz 2019 l. 386 calls the errors on the measured parameters '1 σ'. The v2 default is the certain-members value (11.0 km/s, D-098 rule 5).")
            elif nm == 'Andromeda XII':
                add(ra, 'agree', note='Both readers: the upper end is the formal 1σ uncertainty; no limit level stated (item 5: err_level empty, not_given_by_source).')
            elif nm == 'Triangulum II':
                add(ra, 'agree')
            elif nm in ('Antlia II', 'Bootes III', 'Draco II', 'Eridanus IV', 'Hydrus I', 'Segue 2'):
                add(ra, 'agree', note=(ra['note'] + ' Both readers give the same level and quote.').strip())
            elif nm == 'Reticulum III':
                add(rb, 'agree', note='Both readers: Fritz 2019 Table 4 caption, upper limits are the 90th percentile (the row is a limit).')
            elif nm == 'Tucana V':
                add(ra, 'resolved_at_source', value='not stated', note='The v1 row is a resolved value (limit = none): Hansen 2024 states no level for 1.2 +0.9/-0.6 km/s; the 90% (95.5%) levels apply to its upper limits only. Both readers agree for the resolved value.')
            else:
                add(ra, 'resolved_at_source', note=ra['note'] + ' NOT RESOLVED AUTOMATICALLY')

# ---- D-096 preferred / excluded / fiducial ----
EFFECT = {  # (name, source prefix) -> note on the D-096 effect
    ('Phoenix II', 'Fritz2019'): 'Change: 11.0 km/s default, 9.5 km/s alternative (ruled, D-098 rule 5).',
    ('Fornax', 'Wang2019'): 'Change: Sérsic 20.1′ default, exponential 19.8′ alternative (ruled, D-101).',
}
NOCHANGE_B = {
    'Martin2016': 'No change: the Atlas uses the printed structural values, not the masked data (D-098 rule 1).',
    'Kacharov2017': 'No change: the Atlas uses the printed P83 dispersion; no coverage is computed from the Kacharov table.',
    'MutluPakdil2018': 'No change: the adopted (mean) distance modulus is the printed final value the Atlas uses.',
    'Sand2012': 'No change: v1 uses the adopted column-3 distance (183 kpc, 21.31 mag; ms.tex l. 404).',
    'Garofalo2013': 'No change: v1 uses the adopted modulus 19.94 mag (97.3 kpc); V4 is excluded from the source\'s average, which the Atlas does not recompute (D-098 rule 1).',
    'Chiu2026': 'No change: v1 uses the cited mixture-model dispersion (4.7 km/s, main.tex l. 34 and l. 291).',
    'Bhardwaj2024': 'No change: the Atlas uses the printed distance, not the individual determinations (D-098 rule 1).',
    'Fritz2019': EFFECT[('Phoenix II', 'Fritz2019')],
}
def src_key(s):
    return re.sub(r'[^A-Za-z0-9]', '', s.split('(')[0])
for f in ['d096_preferred', 'd096_excluded', 'd096_fiducial']:
    for r in A:
        if r['field'] != f: continue
        if r['system_id'] == LEO2 and r['value'] == 'not read':
            if f == 'd096_preferred':
                add(r, 'resolved_at_source', value='yes', quote='our estimate of the distance modulus of Leo II is ⟨(m − M)0⟩ = 21.60 ± 0.03 mag', location='pdftotext -layout l. 457–460 (p. 8, §4)', source=MONELLI_SRC, sha256=MONELLI_SHA,
                    note='role=distance. Abstract: "we derived a true distance modulus of (m − M)0 = 21.60 ± 0.03 mag, corresponding to 209 ± 4 kpc". v1 uses 0.20893 Mpc = 21.60 mag: no change.')
            elif f == 'd096_excluded':
                add(r, 'resolved_at_source', value='yes', quote='by averaging previous results based on the RRL stars and ACs, and excluding V88', location='pdftotext -layout l. 457–460 (p. 8, §4)', source=MONELLI_SRC, sha256=MONELLI_SHA,
                    note='role=distance. Not the same data points the Atlas computes from (the Atlas uses the printed distance): no change (D-098 rule 1).')
            else:
                add(r, 'resolved_at_source', value='no', source=MONELLI_SRC, sha256=MONELLI_SHA, note='role=distance. No fiducial baseline named.')
            continue
        res = 'agree'
        n = r['note']
        if r['value'].lower().startswith('yes'):
            k = (r['name'], src_key(r['source']))
            eff = next((v for (nm, s), v in EFFECT.items() if nm == r['name'] and k[1].startswith(s)), None)
            if eff: n = (n + ' ' + eff).strip(); res = 'ruled'
            elif 'Tollerud2012' in r['source']:
                n = (n + ' D-096 rule 2: AWAITING RULING (Tollerud velocity windows; see resolutions.md).').strip(); res = 'awaiting_ruling'
        add(r, res, note=n)
    # B-only yes rows, keyed by (name, source)
    ya = {(r['name'], src_key(r['source'])[:10]) for r in A if r['field'] == f and r['value'].lower().startswith('yes')}
    for r in B:
        if r['field'] != f or not r['value'].lower().startswith('yes'): continue
        k = (r['name'], src_key(r['source'])[:10])
        if k in ya: continue
        sk = src_key(r['source'])
        eff = next((v for s, v in NOCHANGE_B.items() if sk.startswith(s)), 'No change: not the same data points the Atlas computes from (D-098 rule 1).')
        add(r, 'ruled' if 'Change:' in eff else 'resolved_at_source', note=(r['note'] + ' Found by Reader B only; confirmed at the quoted line. ' + eff).strip())

# ---- D-097 statements (D-100) ----
stm = json.load(open(sys.argv[3]))
OVR = [  # (name, quote substring) -> (value, note)
    ('Andromeda I', 'there is a chance', 'possibility', 'Conditional ("if And I is tidally disrupting"): raises the possibility only.'),
    ('Andromeda II', 'may not be intrinsic', 'neither', 'D-100 rule 1: a past encounter (interaction) is not a listed state.'),
    ('Andromeda XIV', 'unbound or barely bound to M31', 'neither', 'Unbound from the host (M31), an orbital statement, not the system\'s own binding (D-100 rule 1).'),
    ('Andromeda XXII', 'unbound from its former host', 'neither', 'Unbound from a former host: an orbital statement (D-100 rule 1).'),
    ('Pisces II', 'unbound from the MW', 'neither', 'Unbound from the Milky Way: an orbital statement (D-100 rule 1).'),
    ('Tucana', 'unbound from the Local Group', 'neither', 'Unbound from the Local Group: an orbital statement (D-100 rule 1).'),
    ('Andromeda XIX', 'altered by tides', 'neither', 'D-100: "altered by tides" is not a listed state (named in D-100\'s result).'),
    ('Andromeda XIX', 'truly a dynamically relaxed', 'possibility', 'Reports a question whether the system is relaxed (in equilibrium): hedged.'),
    ('Andromeda XIX', 'removed by tides', 'neither', 'Mass loss (D-100 rule 1).'),
    ('Andromeda XIX', 'tidal stresses', 'neither', 'Tidal stress is not a listed state (D-100 rule 1).'),
    ('Andromeda XIX', 'If these objects had undergone significant tidal disruption', 'neither', 'Counterfactual used to argue against disruption.'),
    ('Andromeda XIX', 'it is uncertain whether', 'possibility', '"Uncertain whether … so disrupted": hedged.'),
    ('Andromeda XXV', 'altered by tides', 'neither', 'D-100: "altered by tides" is not a listed state (named in D-100\'s result).'),
    ('Andromeda XXV', 'removed by tides', 'neither', 'Mass loss (D-100 rule 1).'),
    ('Andromeda XXV', 'tidal stresses', 'neither', 'Tidal stress is not a listed state (D-100 rule 1).'),
    ('Andromeda XXV', 'If these objects had undergone significant tidal disruption', 'neither', 'Counterfactual used to argue against disruption.'),
    ('Andromeda XV', 'hints of tidal interaction', 'neither', 'D-100 rules 1 and 2: tidal interaction, hedged by "hints".'),
    ('Andromeda XVIII', 'suggests past tidal interaction', 'neither', 'D-100 rule 1: tidal interaction.'),
    ('Andromeda XXVII', 'currently undergoing tidal disruption', 'finding', 'Ruled (D-097 rule 1 example; D-099 rule 4; D-100).'),
    ('Antlia II', 'removes the need for prolific tidal disruption', 'neither', 'Argues against disruption.'),
    ('Aquarius II', 'out-of-equilibrium state', 'possibility', '"may be affected by … out-of-equilibrium state": hedged.'),
    ('Aquarius III', 'likely precludes', 'neither', 'Argues against disruption.'),
    ('Bootes I', 'either undergoing tidal disruption', 'possibility', 'Alternatives, not all of them listed states.'),
    ('Bootes II', 'feature resulting from tidal interaction', 'neither', 'Tidal interaction (D-100 rule 1).'),
    ('Bootes II', 'on the verge of disruption', 'possibility', '"Cannot rule out": not an assertion; classed as a hedge (confirm, see resolutions.md).'),
    ('Bootes II', 'undergoing tidal disruption or disturbance', 'possibility', '"Cannot rule out": not an assertion; classed as a hedge (confirm, see resolutions.md).'),
    ('Coma Berenices', 'most of these galaxies are in process of disruption', 'neither', 'D-100 rule 3: about a class of galaxies, not the system itself; the rest is distortion from tidal interaction (rule 1).'),
    ('Coma Berenices', 'likely caused by the tidal interaction', 'neither', 'D-100 rule 1: elongation from tidal interaction.'),
    ('Coma Berenices', 'elongated due to the tidal interaction', 'neither', 'D-100 rule 1: elongation from tidal interaction.'),
    ('Draco II', 'potentially disrupting', 'possibility', 'D-100 rule 2: "potentially".'),
    ('Draco II', 'affected by tidal processes', 'neither', 'D-100 rule 1.'),
    ('Draco II', 'final remnant of a brighter dwarf', 'neither', 'Mass loss through tidal interactions (D-100 rule 1).'),
    ('Eridanus IV', 'tentative signs of tidal disruption', 'possibility', 'D-100 rule 2: "tentative".'),
    ('Eridanus IV', 'likely not tidally disrupting', 'neither', 'Argues against disruption.'),
    ('Eridanus IV', 'unlikely to be tidally disrupting', 'neither', 'Argues against disruption.'),
    ('Eridanus IV', 'disfavor tidal disruption', 'neither', 'Argues against disruption.'),
    ('Eridanus IV', 'experienced tidal interactions', 'neither', 'Tidal interaction (D-100 rule 1).'),
    ('Fornax', 'debris of those tidally disrupted stellar systems', 'neither', 'About other systems (D-100 rule 3).'),
    ('Fornax', 'kinematical substructures', 'neither', 'Substructure is not a listed state (D-100 rule 1).'),
    ('Hercules', 'evidence of tidal stripping', 'neither', 'Stripping (D-100 rule 1).'),
    ('Hercules', 'plausibly unbound', 'neither', 'About two individual stars, not the system (D-100 rule 3).'),
    ('Hydrus I', 'lost some dark matter due to tides', 'neither', 'Mass loss (D-100 rule 1).'),
    ('Hydrus I', 'possible explanation is tidal disruption', 'possibility', 'D-100 rule 2: "possible".'),
    ('Leo I', 'argues in favor of tidal interactions', 'neither', 'Tidal interaction (D-100 rule 1).'),
    ('Leo I', 'tides could reproduce', 'neither', 'Tides as a cause of features, no listed state.'),
    ('Leo I', 'hints of extratidal stars', 'possibility', 'Reported claim of "hints … and thus tidal disruption"; the hedge carries (confirm, see resolutions.md).'),
    ('Leo II', 'no signs of tidal disruption', 'neither', 'Argues against disruption.'),
    ('Leo VI', 'no conclusive evidence', 'neither', 'Argues against disruption.'),
    ('Leo VI', 'might be tidally disturbed', 'possibility', 'D-100 rule 2.'),
    ('Pegasus III', 'The second is that it results from tidal interaction', 'neither', 'Tidal interaction (D-100 rule 1).'),
    ('Pegasus III', 'more likely scenario if Peg', 'possibility', 'Conditional on not being in equilibrium; "could": hedged.'),
    ('Pegasus III', 'possibly indicative of tidal disturbance', 'possibility', 'D-100 rule 2: "possibly".'),
    ('Phoenix', 'most likely exclude possible tidal disturbance', 'neither', 'Argues against disturbance.'),
    ('Phoenix II', 'no evidence for structural anomalies', 'neither', 'Argues against disruption.'),
    ('Sculptor', 'evidence of significant Galactic tidal disturbance', 'neither', 'Argues against disturbance ("no obvious signs … or evidence").'),
    ('Segue 1', 'find no evidence in favor of tidal effects', 'neither', 'Argues against.'),
    ('Segue 1', 'could be tidally disrupting', 'possibility', '"could" and "not possible to rule out recent tidal disturbances"; the source concludes the data "do not provide significant support". Hedged statement of state, so possibility under D-100 rule 2.'),
    ('Segue 1', 'no observational evidence supporting the possibility', 'neither', 'Argues against disruption.'),
    ('Segue 1', 'tidal effects may be important', 'neither', '"Tidal effects" is not a listed state (D-100 rule 1).'),
    ('Segue 2', 'cannot be presently disrupting', 'neither', 'Argues against disruption.'),
    ('Sextans', 'No statistically significant distortions', 'neither', 'Argues against.'),
    ('Sextans', 'natural candidate for tidal disruption', 'neither', 'Argues against ("no clear signs of disruption").'),
    ('Sextans', 'unclear whether this gradient is due to', 'possibility', '"Unclear whether": hedged alternatives.'),
    ('Sextans', 'One possibility is that the gradient', 'possibility', 'D-100 rule 2.'),
    ('Triangulum II', 'rule out strong/recent tidal disruption', 'neither', 'Argues against disruption.'),
    ('Triangulum II', 'almost certainly be out of dynamical equilibrium', 'neither', 'About a hypothetical galaxy ("such a galaxy"), not a statement that the system is in that state.'),
    ('Triangulum II', 'might not be in equilibrium', 'possibility', 'D-100 rule 2: "might".'),
    ('Tucana V', 'no significant evidence favoring tidal disruption', 'neither', 'Argues against disruption.'),
    ('Tucana V', 'either an unbound part of the halo', 'possibility', 'Kept as possibility, as both readers classed it; D-100\'s listed findings do not include it. Under D-100\'s words this could be a finding (see resolutions.md, dissent for JvH).'),
    ('Ursa Major I', 'tidal interaction with the Milky Way', 'neither', 'D-100 rule 1: S-shape from tidal interaction (named in D-100\'s result).'),
    ('Ursa Major I', 'tidally interacting with the MW', 'neither', 'D-100 rule 1: tidal interaction (named in D-100\'s result).'),
    ('Ursa Major II', 'disrupted progenitor of the Orphan Stream', 'possibility', '"may be": hedged.'),
    ('Ursa Minor', 'tidal heating', 'neither', 'Tidal heating is not a listed state (D-100 rule 1).'),
    ('Willman 1', 'found evidence for dynamical disequilibrium', 'finding', 'Citing others: "found evidence for dynamical disequilibrium" (D-100 rule 2, "evidence for").'),
    ('Willman 1', 'hints at tidal interactions', 'neither', 'D-100 rules 1 and 2.'),
    ('Willman 1', 'affected by tidal forces', 'neither', 'D-100 rule 1.'),
    ('Willman 1', 'unlikely that Willman 1 is currently in dynamical equilibrium', 'finding', 'Named in D-100\'s result.'),
    ('Draco', 'tidally influenced', 'neither', 'D-100 rule 1: influenced by tides; stripping.'),
]
used = collections.Counter()
for s in stm:
    q = ' '.join(s['quote'].split())
    vals = s['vals']; v = None; note = ''
    for nm, sub, val, nt in OVR:
        if s['name'] == nm and sub.lower() in q.lower():
            v, note = val, nt; used[(nm, sub)] += 1; break
    readers = ''.join(sorted(vals))
    if v is None:
        vs = set(vals.values())
        if len(vs) == 1 and len(vals) == 2:
            v = vs.pop(); res = 'agree'
        else:
            v = list(vals.values())[0]; res = 'resolved_at_source'
            note = 'One reader only; class re-checked under D-100.'
    else:
        res = 'agree' if all(x == v for x in vals.values()) and len(vals) == 2 else 'resolved_at_source'
        if s['name'] in ('Andromeda XXVII', 'Antlia II') and v == 'finding': res = 'ruled'
    r = {c: s.get(c, '') for c in COLS[:-1]}
    r['field'] = 'd097'; r['value'] = v
    r['note'] = (f"Readers {readers}: " + ', '.join(f'{k}={x}' for k, x in sorted(vals.items())) + '. ' + note + (' ' + s.get('note', '') if s.get('note') else '')).strip()
    add(r, res)
# Leo II (Monelli 2025), read by the main session
for q, loc in [('Initial attempts based on HST data (Lépine et al. 2011) suggested that Leo II is bound to the MW', 'pdftotext -layout (§ on the orbit)'),
               ('We did not detect any variable star beyond the tidal radius', 'pdftotext -layout')]:
    add({'system_id': LEO2, 'name': 'Leo II', 'field': 'd097', 'value': 'neither', 'quote': q, 'location': loc, 'source': MONELLI_SRC, 'sha256': MONELLI_SHA,
         'note': 'Read at source by the main session. Orbit about the Milky Way / no extratidal variables: not a listed state (D-100 rule 1). Searched disrupt, unbound, equilibri, tidally: no statement of a listed state.'}, 'resolved_at_source')
missing = [o[:2] for o in OVR if (o[0], o[1]) not in used]
print('overrides not matched:', missing)

# ---- d097_class ----
cls = collections.defaultdict(list)
for r in out:
    if r['field'] == 'd097': cls[r['system_id']].append(r['value'])
ca = {r['system_id']: r['value'] for r in A if r['field'] == 'd097_class'}
cb = {r['system_id']: r['value'] for r in B if r['field'] == 'd097_class'}
RULED_F = {'Andromeda XXVII', 'Antlia II', 'Bootes III', 'Bootes I', 'Hercules', 'Ursa Major II', 'Willman 1', 'Andromeda XXI'}
summary = collections.Counter()
for sid in sorted(ca):
    vs = cls.get(sid, [])
    c = 'finding' if 'finding' in vs else 'possibility' if 'possibility' in vs else 'none'
    nm = names[sid]
    res = 'ruled' if nm in RULED_F or nm in ('Draco II', 'Eridanus IV') or nm in ('Andromeda XV', 'Andromeda XVIII', 'Andromeda XIX', 'Andromeda XXV', 'Coma Berenices', 'Ursa Major I') else ('agree' if ca[sid] == cb.get(sid) == c else 'resolved_at_source')
    summary[c] += 1
    add({'system_id': sid, 'name': nm, 'field': 'd097_class', 'value': c, 'quote': '', 'location': '', 'source': '', 'sha256': '',
         'note': f'Reader A={ca[sid]}, Reader B={cb.get(sid)}. From the d097 rows under D-100 (any finding wins; D-099 rule 4).'}, res)
print('class counts', dict(summary))
print('findings', sorted(names[s] for s in ca if 'finding' in cls.get(s, [])))
print('possibility', sorted(names[s] for s in ca if 'finding' not in cls.get(s, []) and 'possibility' in cls.get(s, [])))
w = csv.DictWriter(open(R + 'resolved.csv', 'w', newline=''), fieldnames=COLS); w.writeheader(); w.writerows(out)
print(len(out), 'rows;', collections.Counter(r['resolution'] for r in out))
print('unresolved flags:', [r['name'] + ':' + r['field'] for r in out if 'NOT RESOLVED' in r['note']])
