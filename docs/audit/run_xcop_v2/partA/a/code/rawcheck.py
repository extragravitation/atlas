"""Independent check: parse FITS bytes directly (no astropy) and compare with compare.csv."""
import csv, struct, sys
base = sys.argv[1]
def raw_row(path, n):
    b = open(path, 'rb').read()
    # walk header blocks: primary HDU (NAXIS=0) then BINTABLE header
    off = 0; hdrs = []
    for _ in range(2):
        cards = {}
        while True:
            blk = b[off:off+2880]; off += 2880
            end = False
            for i in range(36):
                c = blk[i*80:(i+1)*80].decode()
                if c.startswith('END'): end = True; break
                if '=' in c[:10]: cards[c[:8].strip()] = c[10:].split('/')[0].strip().strip("'").strip()
            if end: break
        hdrs.append(cards)
    h = hdrs[1]; w = int(h['NAXIS1'])
    rec = b[off + (n-1)*w: off + n*w]
    return struct.unpack('>6f', rec), [h[f'TTYPE{i}'] for i in range(1,7)]
rows = {r['measurement_id']: r for r in csv.DictReader(open('/home/claude/audit_xcop/packet/rows.csv'))}
bad = 0
for c in csv.DictReader(open(f'{base}/compare.csv')):
    _, f, rs = rows[c['measurement_id']]['source_ref'].split(':')
    v, names = raw_row(f'{base}/ex/{f}', int(rs.split()[1]))
    d = dict(zip(names, v))
    exp = {'r_kpc':d['RADIUS'],'g_obs':d['GOBS'],'g_obs_err_lo':d['GOBS_ERR_LO'],'g_obs_err_hi':d['GOBS_ERR_HI'],'g_bar':d['GBAR'],'g_bar_err_lo':d['GBAR_ERR'],'g_bar_err_hi':d['GBAR_ERR']}
    for k, x in exp.items():
        if float(c[k]) != x: bad += 1; print('MISMATCH', c['measurement_id'], k, c[k], x)
print('mismatches:', bad)
