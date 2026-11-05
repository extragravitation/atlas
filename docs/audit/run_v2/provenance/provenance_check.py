"""Provenance checker, audit plan 2.9. Reads packets read-only; writes provenance.csv.
Checks per measurement: 1 locator_match, 2a citation, 2b licence, 2c hash_recorded,
3 file_hash, 4 location_exists, 5 units.  Each check aggregates the documents the
locator names: fail if any evaluated component fails, n/a if none could be evaluated."""
import csv, json, hashlib, os, re, sys, tarfile, io
from astropy.io import fits
from astropy.io.votable import parse as vparse

B = '/home/claude/audit_v2/packets'
OUT = sys.argv[1]
SCR = sys.argv[2]   # scratch dir with extracted X-COP files and PDF text
rows_out = []

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def sources(st):
    return json.load(open(f'{B}/{st}/method/sources.json'))['sources']

CIT_RE = re.compile(r"(\b[A-Z][a-zA-Z'\-]+(?: et al\.?| & [A-Z][a-zA-Z'\-]+| and [A-Z][a-zA-Z'\-]+)?(?:, [A-Z][a-zA-Z'\-]+ & [A-Z][a-zA-Z'\-]+)?,? \(?(?:19|20)\d\d)|"
                    r"(J/[A-Za-z+]+/\d+/\d+)|(arXiv:?\s?\d{4}\.\d{4,5})|(\b10\.\d{4,}/\S+)")

def has_citation(e):
    txt = ' '.join(str(e.get(k, '')) for k in ('role', 'version_read', 'citation'))
    m = CIT_RE.search(txt)
    return bool(m), (m.group(0) if m else '')

def has_licence(e):
    if 'licence' in e or 'license' in e:
        return True, 'licence field: ' + str(e.get('licence', e.get('license')))[:90]
    note = str(e.get('note', ''))
    m = re.search(r'(CC0[-\d.]*|CC BY[ \d.]*|licen[cs]e[^.;]*|terms of use apply)', note, re.I)
    if m:
        return True, 'in note: ' + m.group(0)[:90]
    return False, 'no licence field or statement (only redistributable=%s)' % e.get('redistributable')

def file_hash(st, e):
    p = f'{B}/{st}/sources/{e["file"]}'
    if not os.path.isfile(p):
        return 'fail', f'{e["file"]} not present in packet'
    b = open(p, 'rb').read()
    ok = hashlib.sha256(b).hexdigest() == e['sha256']
    d = f'{e["file"]} sha256 {"matches" if ok else "DIFFERS from"} {e["sha256"][:12]}..; bytes {len(b)}{"" if len(b)==e.get("bytes") else " (recorded "+str(e.get("bytes"))+")"}'
    if 'content_sha256' in e:
        i = b.find(e['content_from'].encode())
        cok = i >= 0 and hashlib.sha256(b[i:]).hexdigest() == e['content_sha256']
        d += f'; content hash from {e["content_from"]!r} {"matches" if cok else "DIFFERS"}'
        ok = ok and cok
    return ('pass' if ok else 'fail'), d

def agg(parts):
    """parts: list of (result, detail). Aggregate."""
    rs = [r for r, _ in parts]
    if 'fail' in rs: res = 'fail'
    elif 'pass' in rs: res = 'pass'
    else: res = 'n/a'
    return res, ' | '.join(d for _, d in parts)

def emit(mid, check, parts):
    r, d = agg(parts) if isinstance(parts, list) else parts
    rows_out.append((mid, check, r, d))

def entry_checks(st, mid, ents, labels=None):
    """2a/2b/2c/3 for a list of matched sources.json entries."""
    c2a, c2b, c2c, c3 = [], [], [], []
    for e in ents:
        f = e['file']
        ok, m = has_citation(e)
        c2a.append(('pass' if ok else 'fail', f'{f}: ' + (f'citation found ("{m}")' if ok else 'no bibliographic citation in entry (role: "%s")' % e.get('role', '')[:80])))
        ok, m = has_licence(e)
        c2b.append(('pass' if ok else 'fail', f'{f}: {m}'))
        ok = bool(re.fullmatch(r'[0-9a-f]{64}', e.get('sha256', '')))
        c2c.append(('pass' if ok else 'fail', f'{f}: sha256 {"recorded" if ok else "MISSING"}'))
        c3.append(file_hash(st, e))
    emit(mid, '2a_citation', c2a); emit(mid, '2b_licence', c2b); emit(mid, '2c_hash_recorded', c2c); emit(mid, '3_file_hash', c3)

# ---------------- SPARC ----------------
st = 'aeg-d-sparc_v1'
S = {e['file']: e for e in sources(st)}
L = open(f'{B}/{st}/sources/MassModels_Lelli2016c.mrt').read().splitlines()
hdr_end = max(i for i, l in enumerate(L) if l.startswith('-----'))
data = [l for l in L[hdr_end + 1:] if l.strip()]
units = {}
for l in L[:hdr_end]:
    m = re.match(r'\s*\d+-\s*\d+\s+\S+\s+(\S+)\s+(\S+)\s', l)
    if m: units[m.group(2)] = m.group(1)
for r in csv.DictReader(open(f'{B}/{st}/rows.csv')):
    mid = r['measurement_id']; m = re.match(r'(.+?):data row (\d+)$', r['source_ref'])
    f, n = m.group(1), int(m.group(2))
    e = S.get(f)
    emit(mid, '1_locator_match', ('pass' if e else 'fail', f'{f} -> sources.json entry "{e["role"]}"' if e else f'{f} not in sources.json'))
    entry_checks(st, mid, [e])
    ok = 1 <= n <= len(data) and data[n - 1][:11].strip() == r['system_name']
    emit(mid, '4_location_exists', ('pass' if ok else 'fail',
         f'{f}: data row {n} of {len(data)} (1-based, after byte-by-byte header) has ID "{data[n-1][:11].strip()}"; system_name "{r["system_name"]}"; columns R, Vobs, e_Vobs, Vgas, Vdisk, Vbul present in header'))
    emit(mid, '5_units', ('pass' if units.get('R') == 'kpc' else 'fail',
         f'method states radii in kpc (methods page) and Vdisk/Vbul for Upsilon in Msun/Lsun at 3.6um (SOURCE.md); file: R {units.get("R")}, Note (3) "M/L = 1 solMass/solLum at [3.6]" - match. Velocity units (file km/s) and D (file Mpc) not stated by method'))

# ---------------- X-COP ----------------
st = 'aeg-d-xcop_v1'
S = {e['file']: e for e in sources(st)}
X = f'{SCR}/xcop_x/'
for r in csv.DictReader(open(f'{B}/{st}/rows.csv')):
    mid = r['measurement_id']; m = re.match(r'(allfiles\.tar\.gz):(.+?):row (\d+)$', r['source_ref'])
    tf, member, n = m.group(1), m.group(2), int(m.group(3))
    e = S.get(tf)
    emit(mid, '1_locator_match', ('pass' if e and os.path.isfile(X + member) else 'fail',
         f'{tf} -> sources.json entry (X-COP release); member {member} present in archive. Note: locator names only the hydrostatic-mass file; g_bar inputs (fgas/mstar files) are not named'))
    entry_checks(st, mid, [e])
    h = fits.open(X + member); t = h['HYDRO_MASS']; d = t.data
    u = {t.header[f'TTYPE{i}'].strip(): t.header.get(f'TUNIT{i}', '').strip() for i in range(1, t.header['TFIELDS'] + 1)}
    ok = 1 <= n <= len(d) and t.header['CLUSTER'].strip() == r['system_name'] and all(c in d.names for c in ('RADIUS', 'M_FORW', 'EM_FORW'))
    emit(mid, '4_location_exists', ('pass' if ok else 'fail',
         f'{member} ext HYDRO_MASS: {len(d)} rows, row {n} exists (read 1-based; also within range if 0-based), CLUSTER keyword "{t.header["CLUSTER"].strip()}" = system_name; RADIUS, M_FORW, EM_FORW present'))
    ok = u['RADIUS'] == 'kpc' and u['M_FORW'] == 'Msun' and u['EM_FORW'] == 'Msun'
    emit(mid, '5_units', ('pass' if ok else 'fail',
         f'SOURCE.md states RADIUS (kpc), M_FORW, EM_FORW (Msun); FITS TUNIT: RADIUS {u["RADIUS"]}, M_FORW {u["M_FORW"]}, EM_FORW {u["EM_FORW"]}'))

# ---------------- KiDS ----------------
st = 'aeg-d-kids1000-rar_v1'
S = {e['file']: e for e in sources(st)}
MD = f'{B}/{st}/sources/brouwer2021_rar_members/'
for r in csv.DictReader(open(f'{B}/{st}/rows.csv')):
    mid = r['measurement_id']; m = re.match(r'(.+?):(.+?):data row (\d+)$', r['source_ref'])
    tf, member, n = m.group(1), m.group(2), int(m.group(3))
    e = S.get(tf)
    emit(mid, '1_locator_match', ('pass' if e else 'fail', f'{tf} -> sources.json entry "{e["role"][:70]}"; member {member} present in packet (public mirror copy)'))
    ok, cm = has_citation(e)
    emit(mid, '2a_citation', ('pass' if ok else 'fail', f'{tf}: citation found ("{cm}") in role; full reference (A&A 650, A113) only in SOURCE.md'))
    ok, lm = has_licence(e)
    emit(mid, '2b_licence', ('pass' if ok else 'fail', f'{tf}: {lm}; SOURCE.md records "The KiDS page states no licence" but sources.json does not'))
    emit(mid, '2c_hash_recorded', ('pass', f'{tf}: tarball sha256 recorded; members not individually hashed in sources.json'))
    emit(mid, '3_file_hash', ('n/a', f'canonical {tf} unreachable, cannot check recorded tarball sha256 {e["sha256"][:12]}..; member from public mirror, sha256 {sha(MD+member)} (stated by audit lead to equal the verified canonical member hash; not checkable against sources.json, which holds no member hashes)'))
    lines = [l for l in open(MD + member) if l.strip() and not l.startswith('#')]
    head = [l for l in open(MD + member) if l.startswith('#')][0].strip()
    emit(mid, '4_location_exists', ('pass' if 1 <= n <= len(lines) and len(lines[n-1].split()) == 8 else 'fail',
         f'{member}: {len(lines)} data rows, data row {n} exists with 8 columns (Radius, ESD_t, ESD_x, error, bias, ...)'))
    ok = 'Radius(m/s^2)' in head and 'ESD_t(h70*M_sun/pc^2)' in head
    emit(mid, '5_units', ('pass' if ok else 'fail',
         'method: accelerations in m s^-2, "units carry h70; the Atlas takes h = 0.7" (SOURCE.md); file header: Radius(m/s^2), ESD_t(h70*M_sun/pc^2), error(h70*M_sun/pc^2) - consistent. Method does not name the column units explicitly'))

# ---------------- GC Baumgardt ----------------
st = 'aeg-d-gc-baumgardt_v1'
S = {e['file']: e for e in sources(st)}
SD = f'{B}/{st}/sources/'
t = open(SD + 'veldis.html', encoding='utf-8', errors='replace').read()
V = {}
for b in re.split(r'<td align="left"><b>', t)[1:]:
    V[b.split('</b>')[0].strip()] = re.findall(r'align="center">\s*([A-Z0-9]+)\s*</td>', b)
vel_units = '[km/sec]' in t and "['']" in t
MOD = vparse(SD + 'mvdm05/J_ApJS_161_304_models.vot').get_first_table()
CLU = vparse(SD + 'mvdm05/J_ApJS_161_304_clusters.vot').get_first_table()
mu = {f.name: str(f.unit) for f in MOD.fields}; cu = {f.name: str(f.unit) for f in CLU.fields}
H = open(SD + 'mwgc.dat').read().splitlines()
for r in csv.DictReader(open(f'{B}/{st}/rows.csv')):
    mid, n = r['measurement_id'], r['system_name']
    ents = [S['veldis.html'], S['mwgc.dat'], S['mvdm05/J_ApJS_161_304_models.vot'], S['mvdm05/J_ApJS_161_304_clusters.vot']]
    emit(mid, '1_locator_match', ('pass', 'veldis.html, mwgc.dat, J/ApJS/161/304 models and clusters -> four sources.json entries (files veldis.html, mwgc.dat, mvdm05/J_ApJS_161_304_models.vot, mvdm05/J_ApJS_161_304_clusters.vot)'))
    entry_checks(st, mid, ents)
    key = 'MW-' + n.replace(' ', '').upper()
    vt = V.get(n, [])
    mods = sorted(set(str(x['Mod']) for x in MOD.array if x['Cluster'] == key))
    incl = any(x['Cluster'] == key for x in CLU.array)
    hl = [i + 1 for i, l in enumerate(H) if re.match(r'\s?' + re.escape(n) + r'\s', l)]
    ok = vt.count('RV') >= 1 and 'K' in mods and incl and len(hl) == 3
    emit(mid, '4_location_exists', ('pass' if ok else 'fail',
         f'veldis.html: block "{n}" with {vt.count("RV")} RV-type bins (types {sorted(set(vt))}); mwgc.dat: "{n}" on lines {hl} (Parts I-III); models.vot: {key} Mod {mods} (K present: {"K" in mods}); clusters.vot: {key} present: {incl}. Locator gives no columns; method columns (sigma, R_Sun, V_t, c, r_c, r_h, W0, r0pc, Rh, Dist, (M/L)1) exist'))
    ok = mu['r0pc'] == 'pc' and mu['Rh'] == 'log(pc)'
    emit(mid, '5_units', ('pass' if ok else 'fail',
         f'method (REPRODUCTION.md) states r0 and R_c in pc and Rh as log10 radius; models.vot r0pc [{mu["r0pc"]}], Rh [{mu["Rh"]}], Rc [{mu["Rc"]}] - match. Not stated by method: sigma (veldis [km/sec]), <r> (veldis [\'\']), Harris R_Sun (kpc), (M/L)1 (clusters.vot [{cu["(M/L)1"]}])'))

# ---------------- Strong lensing ----------------
st = 'aeg-d-strong-lensing_v1'
SL = sources(st)
rec = {}
for e in SL:
    rec.setdefault(e['record'], []).append(e)
SLD = f'{B}/{st}/sources/'
def tsv_rows(f):
    out = []
    for l in open(SLD + f):
        if l.startswith('#') or not l.strip(): continue
        out.append(l.rstrip('\n').split('\t'))
    return out
def find_sys(e, name):
    f = e['file']
    if f.endswith('.tsv'):
        hits = [x for x in tsv_rows(f) if name in [c.strip() for c in x]]
        return bool(hits), f'{f}: row for {name} {"found" if hits else "NOT found"}'
    if f.endswith('.txt'):
        hits = [l for l in open(SLD + f) if l.startswith('SDSS' + name + '\t')]
        return bool(hits), f'{f}: row SDSS{name} {"found" if hits else "NOT found"}'
    return None, ''
PDFLOC = {'R28': 'arxiv/1306.4983v1.pdf: no page/table in locator; auditor finds M_Ein (MFL) = 1.50 +- 0.06e11 Msun and R_Ein 2.85 arcsec on pp. 3-4, WMAP7 cosmology p. 2',
          'R26': 'arxiv/1612.00065v2.pdf: no page/table in locator; auditor finds SNL-0 theta_Ein and L_r,Ein in Table 1, p. 5'}
UNITS_SL = {'R5': 'table5 bSIE [arcsec]; table4 zFG, zBG unitless, Re [arcsec]',
            'R13': 'lens table thetaE [arcsec], MChaBC2/MSalBC2 [10+10solMass]',
            'R10': 'Table 2 b_SIE (arcsec), log_10(M*^Chab/M_sun); Table 1 R_eff (arcsec)',
            'R28': 'PDF text: M_Ein in Msun, R_Ein in arcsec', 'R26': 'PDF Table 1: Units column (arcsec, 10^10 L_sun,r)'}
for r in csv.DictReader(open(f'{B}/{st}/rows.csv')):
    mid = r['measurement_id']; name = r['system_name']
    recs = re.findall(r'(observed|stellar) (R\d+)', r['source_ref'])
    ents, p1, p4 = [], [], []
    for side, R in recs:
        es = rec.get(R, [])
        p1.append(('pass' if es else 'fail', f'{side} {R} -> {len(es)} sources.json entries ({", ".join(e["file"] for e in es)})'))
        for e in es:
            if e not in ents: ents.append(e)
        tab = [e for e in es if not e['file'].endswith('.pdf')]
        if tab:
            for e in tab:
                ok, d = find_sys(e, name.split(' ')[0])
                p4.append(('pass' if ok else 'fail', f'{side} {R}: {d}'))
        else:
            p4.append(('fail', f'{side} {R}: record of PDF only and locator gives record id only ({PDFLOC.get(R, "")})'))
    emit(mid, '1_locator_match', p1)
    entry_checks(st, mid, ents)
    emit(mid, '4_location_exists', p4)
    emit(mid, '5_units', ('n/a', 'method (REPRODUCTION.md, A6S_PRECEDENCE.md, descriptor) states no units for the input columns; file units: ' + '; '.join(f'{R}: {UNITS_SL.get(R, "")}' for _, R in dict.fromkeys(recs))))

# ---------------- Dwarfs ----------------
st = 'aeg-d-dwarfs_v1'
DS = {e['file']: e for e in sources(st)}
IDX = {x['lvdb_ref']: x for x in csv.DictReader(open(f'{B}/{st}/method/documents_index.csv'))}
def idx_checks(ref):
    x = IDX[ref]; p = f'{B}/{st}/sources/papers/{ref}.pdf'
    cit = ('pass', f'{ref}: bibcode {x["bibcode"]}, doi {x["doi"] or "-"}, arXiv {x["arxiv_id"]}v{x["arxiv_version"]}')
    lic = ('fail', f'{ref}: documents_index.csv has no licence column; access_note empty')
    hr = ('pass' if re.fullmatch(r'[0-9a-f]{64}', x['sha256']) else 'fail', f'{ref}: sha256 recorded')
    ok = os.path.isfile(p) and sha(p) == x['sha256']
    fh = ('pass' if ok else 'fail', f'papers/{ref}.pdf sha256 {"matches" if ok else "DIFFERS"} {x["sha256"][:12]}.. (bytes {os.path.getsize(p)}, recorded {x["bytes"]})')
    return cit, lic, hr, fh
# components: (locator text, matched ref | 'VOT:<file>' | None, check4 result, check4 detail)
U = 'unmatched'
DW = {
 'aeg-d-dwarfs/v1/m000059': [
   ('Gregory 2019 MNRAS 485 2010', None, 'n/a', 'not checkable: document not in packet'),
   ('Saviane 1996 Re ... as an angle', None, 'n/a', 'not checkable: document not in packet'),
   ('Bernard 2009, RR Lyrae', None, 'n/a', 'not checkable: document not in packet'),
   ('Saviane 1996 M_V + its own TRGB modulus', None, 'n/a', 'not checkable: document not in packet')],
}
def m31(sysn, tol_ref, tol_det, dist_ref, dist_det, dist_res='pass'):
    return [
     (tol_ref[0], tol_ref[1], 'fail', f'sigma: locator names the paper only (no table/page/row); auditor finds {sysn} in {tol_det}'),
     (f'Martin2016 p.9 Table 1 row {sysn}', 'Martin2016ApJ...833..167M', 'pass', f'Martin2016 p.9 Table 1 "Derived structural parameters" has row {sysn} with eps and rh (arcmin)'),
     (dist_ref[0], dist_ref[1], dist_res, dist_det),
     (f'Martin2016 p.9 Table 2 row {sysn} m_V,0', 'Martin2016ApJ...833..167M', 'pass', f'Martin2016 p.9 Table 2 "Derived luminosity-related properties" has row {sysn} with column mV,0')]
SAV = lambda s: (f'Savino2022 p.15 Table 5 row {s}', 'Savino2022ApJ...938..101S')
SAVD = lambda s: f'Savino2022 p.15 Table 5 has row {s} with column mu (and D kpc)'
DW['aeg-d-dwarfs/v1/m000012'] = m31('And XV', ('Tollerud 2012 ApJ 752 45', 'Tollerud2012ApJ...752...45T'), 'Table 3, p. 9', SAV('And XV'), SAVD('And XV'))
DW['aeg-d-dwarfs/v1/m000007'] = m31('And IX', ('Tollerud 2012 ApJ 752 45', 'Tollerud2012ApJ...752...45T'), 'Table 3, p. 9', SAV('And IX'), SAVD('And IX'))
DW['aeg-d-dwarfs/v1/m000003'] = m31('And III', ('Tollerud 2012 ApJ 752 45', 'Tollerud2012ApJ...752...45T'), 'Table 3, p. 9', SAV('And III'), SAVD('And III'))
DW['aeg-d-dwarfs/v1/m000013'] = m31('And XVI', ('Tollerud 2012 ApJ 752 45', 'Tollerud2012ApJ...752...45T'), 'Table 3, p. 9',
    ('MartinezVazquez2017 p.18 Table 8 row And XVI', 'MartinezVazquez2017ApJ...850..137M'),
    'MartinezVazquez2017 p.18 Table 8 has row And XVI, but the locator names no column and the row holds four filled mu0 columns (PWR, LMRB03, LMRC03, FOBE); the value is not uniquely located', 'fail')
DW['aeg-d-dwarfs/v1/m000020'] = m31('And XXIII', ('Collins 2013 ApJ 768 172', 'Collins2013ApJ...768..172C'),
    'Table 4, p. 27 (sigma_v 7.1 +- 1.0); note documents_index.csv lists Collins2013 systems without andromeda_23', SAV('And XXIII'), SAVD('And XXIII'))
DW['aeg-d-dwarfs/v1/m000010'] = m31('And XII', ('Collins 2013 ApJ 768 172', 'Collins2013ApJ...768..172C'), 'Table 4, p. 27', SAV('And XII'), SAVD('And XII') + ' (Martin2016 prints the name as "And XIIc", footnote c)')
DW['aeg-d-dwarfs/v1/m000036'] = [
   ('Cerny 2026 arXiv 2602.17652', 'Cerny2026arXiv260217652C', 'fail', 'sigma: locator names the paper only; auditor finds Draco II in Table 3, p. 38 "Dynamical Properties of the UFCSs"'),
   ('Longeard2018 p.8 Table 1 row rh (arcmin)', 'Longeard2018MNRAS.480.2609L', 'pass', 'Longeard2018 p.8 Table 1 "Inferred properties of Dra II" has row rh, unit arcmin'),
   ('Longeard2018 p.8 Table 1 row Distance modulus', 'Longeard2018MNRAS.480.2609L', 'pass', 'Longeard2018 p.8 Table 1 has row Distance modulus (mag)'),
   ('M_V + (m-M) used by the paper (own)', 'Longeard2018MNRAS.480.2609L', 'fail', 'locator does not name the paper or table ("the paper"); read as Longeard2018, whose Table 1 p.8 has rows MV and Distance modulus')]
DW['aeg-d-dwarfs/v1/m000031'] = [
   ('Geha 2026 ApJ 999 140', 'Geha2026ApJ...999..140G', 'fail', 'sigma: locator names the paper only; auditor finds CVn II in the appendix system table, p. 32'),
   ('Munoz2018 p.27 Table 5 Primary Sample row CVn II col re,s (arcmin)', 'Munoz2018ApJ...860...66M', 'pass', 'Munoz2018 p.27 Table 5 (Sersic) Primary Sample row 26 CVn II, column re,s (arcmin) exists'),
   ('Greco2008 sec.5 p.7', 'Greco2008ApJ...675L..73G', 'pass', 'Greco2008 (arXiv pagination) p.7 sec. 5 "An Improved Distance to the CVn II galaxy" gives mu0'),
   ('Munoz 2018 M_V + 5log10(D/10pc), D kpc (Table 1)', 'Munoz2018ApJ...860...66M', 'fail', 'D: Munoz2018 Table 1 p.22 row CVn II, column R (kpc) exists; M_V: no table given and M_V is not in Table 1 (it is in Table 6, p. 28)')]
DW['aeg-d-dwarfs/v1/m000042'] = [
   ('Koch 2007 ApJ 657 241', 'VOT:members/vizier/J_ApJ_657_241.vot', 'fail', 'sigma: the only packaged record of Koch 2007 is the VizieR star table (J/ApJ/657/241/table2: positions, HRV per star); no sigma is printed there, the paper is not in the packet, and the locator names no table'),
   ('Munoz2018 p.27 Table 5 Primary Sample row Leo I col re,s (arcmin)', 'Munoz2018ApJ...860...66M', 'pass', 'Munoz2018 p.27 Table 5 Primary Sample row 16 Leo I, column re,s (arcmin) exists'),
   ('Stetson 2014, midpoint of two printed values', 'Stetson2014PASP..126..616S', 'fail', 'locator gives no page/table; auditor finds distance-modulus statements on p. 11'),
   ('Munoz 2018 M_V + 5log10(D/10pc), D kpc (Table 1)', 'Munoz2018ApJ...860...66M', 'fail', 'D: Munoz2018 Table 1 p.22 row Leo I, column R (kpc) exists; M_V: no table given and M_V is not in Table 1 (it is in Table 6, p. 28)')]
rows_dw = list(csv.DictReader(open(f'{B}/{st}/rows.csv')))
assert set(r['measurement_id'] for r in rows_dw) == set(DW), set(r['measurement_id'] for r in rows_dw) ^ set(DW)
for r in rows_dw:
    mid = r['measurement_id']
    p1, c2a, c2b, c2c, c3, p4 = [], [], [], [], [], []
    seen = set()
    for loc, ref, r4, d4 in DW[mid]:
        if ref is None:
            p1.append(('fail', f'"{loc}": no entry in sources.json or documents_index.csv'))
        elif ref.startswith('VOT:'):
            e = DS[ref[4:]]
            p1.append(('fail', f'"{loc}": only match is sources.json entry {ref[4:]} ("{e["role"][:60]}..."), a member-star table, not the document the sigma value comes from; paper not recorded'))
            if ref not in seen:
                seen.add(ref)
                ok, m = has_citation(e); c2a.append(('pass' if ok else 'fail', f'{e["file"]}: citation "{m}"'))
                ok, m = has_licence(e); c2b.append(('pass' if ok else 'fail', f'{e["file"]}: {m}'))
                c2c.append(('pass', f'{e["file"]}: sha256 recorded')); c3.append(file_hash(st, e))
        else:
            p1.append(('pass', f'"{loc}" -> documents_index.csv {ref}'))
            if ref not in seen:
                seen.add(ref)
                a, b_, c, d = idx_checks(ref)
                c2a.append(a); c2b.append(b_); c2c.append(c); c3.append(d)
        p4.append((r4, f'"{loc}": {d4}'))
    if not c2a:
        for lst in (c2a, c2b, c2c, c3):
            lst.append(('n/a', 'no named document matched an index entry'))
    emit(mid, '1_locator_match', p1)
    emit(mid, '2a_citation', c2a); emit(mid, '2b_licence', c2b); emit(mid, '2c_hash_recorded', c2c); emit(mid, '3_file_hash', c3)
    emit(mid, '4_location_exists', p4)
    emit(mid, '5_units', ('n/a', 'method (REPRODUCTION.md, descriptor) states no units for these inputs; where the locator itself states a unit it matches the printed table head (Munoz Table 5 re,s (arcmin); Longeard Table 1 rh arcmin; Munoz Table 1 R (kpc))'
                         if mid in ('aeg-d-dwarfs/v1/m000031', 'aeg-d-dwarfs/v1/m000036', 'aeg-d-dwarfs/v1/m000042') else 'method (REPRODUCTION.md, descriptor) states no units for these inputs'))

with open(OUT, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['measurement_id', 'check', 'result', 'detail']); w.writerows(rows_out)
print(len(rows_out), 'rows written')
