"""Independent fixed-width parser for the two SPARC MRT files (second reader).
Usage: python3 -I parse_sparc.py <input_dir> <out_dir>
Column layouts:
  MassModels: exactly as its own byte-by-byte header (verified against data).
  SPARC table: header Format widths kept, but each field is separated by one blank
  byte, which the header's byte ranges omit (see REPORT.md). Positions below are 1-based inclusive.
"""
import sys, re, csv, os

MM = [  # (label, start, end, kind)
 ('galaxy',1,11,'A'),('D_Mpc',13,18,'F'),('R_kpc',20,25,'F'),('Vobs',27,32,'F'),
 ('e_Vobs',34,38,'F'),('Vgas',40,45,'F'),('Vdisk',47,52,'F'),('Vbul',54,59,'F'),
 ('SBdisk',61,67,'F'),('SBbul',69,76,'F')]

# header (as printed) for the SPARC table, used only for the comparison in the report
SP_HEADER = [('galaxy',1,11),('T',12,13),('D_Mpc',14,19),('e_D',20,24),('f_D',25,26),
 ('Inc',27,30),('e_Inc',31,34),('L36',35,41),('e_L36',42,48),('Reff',49,53),('SBeff',54,61),
 ('Rdisk',62,66),('SBdisk0',67,74),('MHI',75,81),('RHI',82,86),('Vflat',87,91),
 ('e_Vflat',92,96),('Q',97,99),('Ref',100,113)]
SP_KIND = dict(galaxy='A',T='I',f_D='I',Q='I',Ref='A')

def actual_sparc_layout():
    out, pos = [], 1
    for lab, s, e in SP_HEADER:
        w = e - s + 1
        out.append((lab, pos, pos + w - 1, SP_KIND.get(lab, 'F')))
        pos += w + 1          # one separating blank
    return out
SP = actual_sparc_layout()

NUM = {'F': re.compile(r'^-?\d+\.\d+$'), 'I': re.compile(r'^-?\d+$')}

def read_lines(path):
    raw = open(path, 'rb').read()
    txt = raw.decode('ascii')
    return [l[:-1] if l.endswith('\r') else l for l in txt.split('\n')]

def data_lines(lines):
    # data start after the last line of dashes
    last = max(i for i, l in enumerate(lines) if re.fullmatch(r'-{20,}', l))
    rows = lines[last+1:]
    while rows and rows[-1] == '': rows.pop()
    return last + 1, rows

def parse(path, layout):
    lines = read_lines(path)
    off, rows = data_lines(lines)
    width = layout[-1][2]
    seps = set(range(1, width+1)) - {c for _, s, e, _ in layout for c in range(s, e+1)}
    out, problems = [], []
    for i, l in enumerate(rows):
        lineno = off + i + 1
        if l.strip() == '':
            problems.append((lineno, 'blank line inside data')); continue
        trail = l[width:]
        if trail.strip():
            problems.append((lineno, f'non-blank beyond byte {width}: {trail!r}'))
        p = l.ljust(width)
        for c in seps:
            if p[c-1] != ' ':
                problems.append((lineno, f'separator byte {c} not blank'))
        rec = {}
        for lab, s, e, k in layout:
            v = p[s-1:e].strip()
            if v == '':
                problems.append((lineno, f'{lab} empty (bytes {s}-{e})'))
            elif k in NUM and not NUM[k].match(v):
                problems.append((lineno, f'{lab} not {k}: {v!r}'))
            if k == 'A' and ' ' in v:
                problems.append((lineno, f'{lab} contains internal space: {v!r}'))
            rec[lab] = v
        # cross-check: whitespace tokens must equal the fixed-width fields
        if l.split() != [rec[lab] for lab, *_ in layout]:
            problems.append((lineno, 'whitespace tokens differ from fixed-width fields'))
        out.append(rec)
    return out, problems, off

def main(indir, outdir):
    os.makedirs(outdir, exist_ok=True)
    mm, pmm, _ = parse(os.path.join(indir, 'MassModels_Lelli2016c.mrt'), MM)
    with open(os.path.join(outdir, 'massmodels.csv'), 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['row'] + [l for l, *_ in MM])
        for i, r in enumerate(mm, 1):
            w.writerow([i] + [r[l] for l, *_ in MM])
    sp, psp, _ = parse(os.path.join(indir, 'SPARC_Lelli2016c.mrt'), SP)
    with open(os.path.join(outdir, 'galaxies.csv'), 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow([l for l, *_ in SP])
        for r in sp:
            w.writerow([r[l] for l, *_ in SP])
    print('massmodels rows', len(mm), 'problems', pmm[:20], len(pmm))
    print('galaxies rows', len(sp), 'problems', psp[:20], len(psp))
    print('SPARC actual layout:')
    for (lab, s, e, k), (_, hs, he) in zip(SP, SP_HEADER):
        print(f'  {lab:8s} header {hs:3d}-{he:3d}  actual {s:3d}-{e:3d}  shift {s-hs:+d}')
    # header-as-written applied to data: count how many fields would differ
    lines = read_lines(os.path.join(indir, 'SPARC_Lelli2016c.mrt'))
    _, rows = data_lines(lines)
    bad = {lab: 0 for lab, *_ in SP_HEADER}
    for l in rows:
        for (lab, hs, he), (_, s, e, _) in zip(SP_HEADER, SP):
            if l[hs-1:he].strip() != l[s-1:e].strip(): bad[lab] += 1
    print('rows where header-as-written slice != actual field:', bad)
    print('example line 1 header-slices:', [lines and rows[0][hs-1:he] for _, hs, he in SP_HEADER])
    # duplicates / consistency checks
    names = [r['galaxy'] for r in sp]
    print('unique galaxies', len(set(names)))
    mmn = []
    for r in mm:
        if not mmn or mmn[-1] != r['galaxy']: mmn.append(r['galaxy'])
    print('massmodel galaxy blocks', len(mmn), 'unique', len(set(mmn)),
          'same set as table', set(mmn) == set(names), 'same order', mmn == names)
    dmis = [g for g in names if {r['D_Mpc'] for r in mm if r['galaxy']==g} != {next(x['D_Mpc'] for x in sp if x['galaxy']==g)}]
    print('galaxies whose printed D differs between files (text):', len(dmis), dmis[:10])

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
