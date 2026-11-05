#!/usr/bin/env python3
"""Reader B audit of aeg-d-gc-baumgardt_v1.

Method followed (REPRODUCTION.md, the only written formula source in the packet):
  g_obs = 3 sigma^2 / r_half ; sigma = light-weighted LOS dispersion (aeg.dispersion.light_weighted_dispersion)
  g_bar = G (1/2 L_V Upsilon_V) / r_half^2
  r_half = 4/3 R_h ; R_h = MvdM King-fit Rh (log pc) rescaled from their Dist to Harris R_Sun
  L_V from Harris M_V,t with M_V,sun adopted by MvdM (read at source: arXiv astro-ph/0605132 tex line 2161: +4.85)
  Upsilon_V = MvdM (M/L)1 (clusters table)
  G = astropy.constants.G (named in REPRODUCTION.md test 3)

The light-weighting algorithm, bin-edge inference, coverage rule and choice among
line-of-sight candidate datasets are not written anywhere in the packet, so g_obs
is not computed (method incomplete). All line-of-sight bins are still transcribed.
"""
import csv, re, sys, html
import xml.etree.ElementTree as ET

PK = '/home/claude/audit_v2/packets/aeg-d-gc-baumgardt_v1/'
SRC = PK + 'sources/'
OUT = '/home/claude/audit_v2/readers/b/aeg-d-gc-baumgardt_v1/'
LOS_CODES = {'F13', 'L13', 'L15', 'RV', 'K18', 'D21', 'C22', 'G22'}  # veldis.html "Line-of-sight radial velocities" list
M_V_SUN = '4.85'  # McLaughlin & van der Marel (2005), arXiv:astro-ph/0605132, mclaughlin_vandermarel.tex line 2161

# ---------- veldis.html ----------
def parse_veldis():
    lines = open(SRC + 'veldis.html', encoding='latin-1').read().split('\n')
    rows = []  # dicts: cluster, r, N, sig, up, low, type, line
    cur = None
    buf = []
    start = None
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r'<td[^>]*>(.*?)</td>', ln):
            txt = m.group(1)
            b = re.search(r'<b>(.*?)</b>', txt)
            if b:
                cur = b.group(1).strip()
                buf = []; start = i
                continue
            t = html.unescape(re.sub('<[^>]+>', '', txt)).strip()
            if t == '' and not buf:
                start = i
                continue
            if not buf:
                start = i
            buf.append(t)
            if len(buf) == 6:
                rows.append(dict(cluster=cur, r=buf[0], N=buf[1], sig=buf[2], up=buf[3],
                                 low=buf[4], type=buf[5], line=start))
                buf = []
    return rows

# ---------- Harris ----------
def harris():
    lines = open(SRC + 'mwgc.dat', encoding='latin-1').read().split('\n')
    p1 = next(i for i, l in enumerate(lines) if 'Part I:' in l)
    p2 = next(i for i, l in enumerate(lines) if 'Part II:' in l)
    p3 = next(i for i, l in enumerate(lines) if 'Part III:' in l)
    return lines, p1, p2, p3

def harris_row(lines, a, b, name):
    for i in range(a, b):
        l = lines[i]
        if l[:12].strip() == name:
            return i + 1, l
    raise KeyError(name)

# ---------- VOTable (raw strings) ----------
def votable(fn):
    txt = open(fn, encoding='utf-8').read().split('\n')
    names = []
    for l in txt:
        m = re.search(r'<FIELD name="([^"]+)"', l)
        if m: names.append(html.unescape(m.group(1)))
    rows = []
    for i, l in enumerate(txt, 1):
        if l.startswith('<TR>'):
            vals = re.findall(r'<TD>(.*?)</TD>', l)
            rows.append((i, dict(zip(names, vals))))
    return rows

def mvdm_name(n):
    return 'MW-' + n.replace(' ', '').upper()

def main():
    from astropy import constants as const, units as u
    G = const.G.si.value
    MSUN = const.M_sun.si.value
    PC = u.pc.to(u.m)

    targets = list(csv.DictReader(open(PK + 'rows.csv')))
    vd = parse_veldis()
    hl, p1, p2, p3 = harris()
    models = votable(SRC + 'mvdm05/J_ApJS_161_304_models.vot')
    clus = votable(SRC + 'mvdm05/J_ApJS_161_304_clusters.vot')

    inp = []
    vals = []
    for t in targets:
        mid, name = t['measurement_id'], t['system_name']
        add = lambda m_, k, v, un, loc: inp.append([m_, k, v, un, loc])
        # sigma profile (line-of-sight bins only)
        bins = [r for r in vd if r['cluster'] == name]
        los = [r for r in bins if r['type'] in LOS_CODES]
        codes = sorted({r['type'] for r in los})
        for j, r in enumerate(bins):
            if r['type'] not in LOS_CODES:
                continue
            loc = f'veldis.html line {r["line"]} ({name} profile row {j+1}, Type {r["type"]})'
            inp.append([mid, f'<r> [{r["type"]} bin {j+1}]', r['r'], 'arcsec', loc])
            inp.append([mid, f'N_Star [{r["type"]} bin {j+1}]', r['N'], '', loc])
            inp.append([mid, f'sigma [{r["type"]} bin {j+1}]', r['sig'], 'km/s', loc])
            inp.append([mid, f'Delta sigma_Up [{r["type"]} bin {j+1}]', r['up'], 'km/s', loc])
            inp.append([mid, f'Delta sigma_Low [{r["type"]} bin {j+1}]', r['low'], 'km/s', loc])
        # Harris
        ln1, l1 = harris_row(hl, p1, p2, name)
        f1 = l1.split()
        rsun = f1[-5]
        add(mid, 'R_Sun', rsun, 'kpc', f'mwgc.dat line {ln1} (Part I, {name}, column R_Sun)')
        ln2, l2 = harris_row(hl, p2, p3, name)
        f2 = l2[12:].split()
        # columns: [Fe/H] wt E(B-V) V_HB (m-M)V V_t M_V,t ...
        mvt = f2[6]
        add(mid, 'M_V,t', mvt, 'mag', f'mwgc.dat line {ln2} (Part II, {name}, column M_V,t)')
        # MvdM King fit
        mk = [(i, r) for i, r in models if r['Cluster'] == mvdm_name(name) and r['Mod'] == 'K']
        assert len(mk) == 1, (name, len(mk))
        li, mr = mk[0]
        for k, un in [('Dist', 'kpc'), ('W0/gamma', ''), ('r0pc', 'pc'), ('Conc', ''), ('Rh', 'log(pc)')]:
            add(mid, k, mr[k], un, f'mvdm05/J_ApJS_161_304_models.vot line {li} (recno {mr["recno"]}, {mr["Cluster"]}, Mod=K, field {k})')
        cl = [(i, r) for i, r in clus if r['Cluster'] == mvdm_name(name)]
        assert len(cl) == 1
        ci, cr = cl[0]
        add(mid, '(M/L)1', cr['(M/L)1'], 'Msun/Lsun (V)', f'mvdm05/J_ApJS_161_304_clusters.vot line {ci} (recno {cr["recno"]}, {cr["Cluster"]}, field (M/L)1)')
        add(mid, 'M_V,sun', M_V_SUN, 'mag', 'arXiv:astro-ph/0605132 e-print, mclaughlin_vandermarel.tex line 2161 (Sect. on luminosities: "solar absolute magnitude $M_{V,\\odot}=+4.85$")')

        # g_bar
        Rh_pc = 10 ** float(mr['Rh']) * float(rsun) / float(mr['Dist'])
        r_half = 4.0 / 3.0 * Rh_pc * PC
        L = 10 ** (-0.4 * (float(mvt) - float(M_V_SUN)))
        Ups = float(cr['(M/L)1'])
        gbar = G * (0.5 * L * Ups * MSUN) / r_half ** 2

        notes = (f'g_obs not computed: method does not specify the light-weighted dispersion '
                 f'(no formula for aeg.dispersion.light_weighted_dispersion, King-weight definition, bin-edge inference '
                 f'from mean radii, light-coverage computation); only line-of-sight dataset present: {"/".join(codes)}, as in the locator. '
                 f'g_bar computed: Harris M_V,t, M_V,sun=4.85 (MvdM paper), (M/L)1, R_h=10^Rh*R_Sun/Dist, r_half=4/3 R_h; '
                 f'G, M_sun, pc from astropy {__import__("astropy").__version__} (M_sun and pc not stated in method).')
        vals.append([mid, '', f'{gbar:.6e}', 'method incomplete', notes])

    with open(OUT + 'inputs.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['measurement_id', 'input', 'value', 'unit', 'locator']); w.writerows(inp)
    with open(OUT + 'values.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['measurement_id', 'g_obs', 'g_bar', 'status', 'notes']); w.writerows(vals)

if __name__ == '__main__':
    main()
