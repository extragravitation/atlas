import csv, sys, re, json
R = sys.argv[1]
A = list(csv.DictReader(open(R + 'reader-A.csv'))); B = list(csv.DictReader(open(R + 'reader-B.csv')))
STATE = re.compile(r"(out[- ]of[- ](dynamic(al)?[- ])?equilibri|not (be )?in (dynamic(al)? )?equilibri|not a system in dynamical equilibrium|disequilibri|(unlikely|not likely) (to be )?(currently )?in (dynamic(al)? )?equilibri|not (truly )?(a )?dynamically relaxed|\bunbound\b|no longer (be )?(a )?(gravitationally )?bound|not (be )?bound|tidal(ly)?[ -]+disrupt|disrupting|disruption|tidally disturbed|tidal disturbance|so disrupted|on the verge of disruption)", re.I)
HEDGE = re.compile(r"\b(may|might|could|possibly|perhaps|potentially|tentative|hints?|possible|possibility|cannot rule out|can not rule out|not possible to rule out|chance|uncertain whether|question whether|if)\b", re.I)
def norm(q): return re.sub(r'\W+', ' ', q).strip().lower()[:60]
stm = {}
for t, rows in (('A', A), ('B', B)):
    for r in rows:
        if r['field'] != 'd097' or not r['quote'].strip(): continue
        k = (r['system_id'], norm(r['quote']))
        if k not in stm:
            stm[k] = dict(r, readers=t, vals={t: r['value']})
        else:
            stm[k]['readers'] += t; stm[k]['vals'][t] = r['value']
out = []
for k, r in stm.items():
    q = ' '.join(r['quote'].split())
    if not STATE.search(q): auto = 'neither'
    elif HEDGE.search(q): auto = 'possibility'
    else: auto = 'finding'
    r['auto'] = auto
    out.append(r)
json.dump(out, open(sys.argv[2], 'w'), indent=0)
dis = [r for r in out if any(v != r['auto'] for v in r['vals'].values())]
print(len(out), 'statements;', len(dis), 'where auto differs from a reader')
for r in sorted(dis, key=lambda x: x['name']):
    print(f"{r['name']:16s} auto={r['auto']:11s} {r['vals']} [{r['source'][:22]}; {r['location'][:30]}] {' '.join(r['quote'].split())[:200]}")
