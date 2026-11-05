import csv,io,json,hashlib,os,re,shutil,glob,html,sys,urllib.request
REPO='/home/claude/atlas'; OUT='/home/claude/audit_v2'
CACHES=[REPO]+glob.glob('/home/claude/atlas/.claude/worktrees/*')+['/home/claude/atlas-a6']
S=[r for r in csv.DictReader(open(f'{REPO}/docs/audit/run_v2/sample.csv')) if r['status']=='sample']
def rows(p,t='measurements'):
    L=[l for l in open(f'{REPO}/data/packages/{p}/tables/{t}.ecsv') if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(L))))
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def find(pkg,f,h,ver='v1'):
    for c in CACHES:
        for v in (ver,'v2'):
            p=f'{c}/data/packages/{pkg}/{v}/source/{f}'
            if os.path.isfile(p) and sha(p)==h: return p
    return None
t=open(f'{REPO}/site/dist/methods/index.html').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>|<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>','',t,flags=re.S)
t=re.sub(r'<(h[1-4]|p|li|tr|br)[^>]*>',r'\n',t); t=html.unescape(re.sub(r'<[^>]+>',' ',t))
methods=re.sub(r'[ \t]+',' ',re.sub(r'\n\s*\n+','\n\n',t)).strip()
REDACT=[(r'Re = [\d.]+ \+- [\d.]+ pc at \(m-M\)0 = [\d.]+','Re [value redacted] pc at (m-M)0 [value redacted]'),
        (r'midpoint of [\d.]+ \+- [\d.]+ to [\d.]+ \+- [\d.]+','midpoint of two printed values [redacted]'),
        (r'D = \d+ kpc','D [value redacted] kpc')]
report=[]
for st in sorted({r['stratum'] for r in S}):
    pkg=st.split('/')[0]; P=f'{OUT}/packets/{st.replace("/","_")}'; os.makedirs(P+'/sources',exist_ok=True); os.makedirs(P+'/method',exist_ok=True)
    M={r['measurement_id']:r for r in rows(st)}; Y={r['system_id']:r for r in rows(st,'systems')} if os.path.exists(f'{REPO}/data/packages/{st}/tables/systems.ecsv') else {}
    with open(P+'/rows.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(['measurement_id','system_name','source_ref'])
        for s in S:
            if s['stratum']!=st: continue
            m=M[s['measurement_id']]; y=Y.get(m['system_id'],{}); ref=m['source_ref']
            for a,b in REDACT: ref=re.sub(a,b,ref)
            w.writerow([m['measurement_id'],y.get('name_in_source',''),ref])
    open(P+'/method/methods_page.txt','w').write(methods)
    d=f'{REPO}/data/packages/{st}'
    docs=['SOURCE.md'] if os.path.exists(d+'/SOURCE.md') else ['REPRODUCTION.md','descriptor.json']
    for x in docs+['sources.json']: shutil.copy(f'{d}/{x}',P+'/method/'+x)
    txt=''.join(open(f'{d}/{x}').read() for x in docs)
    for mf in sorted(glob.glob(f'{REPO}/docs/methods/*.md')):
        key=os.path.basename(mf).split('_')[0]
        if re.search(r'\b'+re.escape(key)+r'\b',txt) or os.path.basename(mf) in txt: shutil.copy(mf,P+'/method/')
    src=json.load(open(d+'/sources.json'))['sources']
    for x in src:
        f=x.get('file');h=x.get('sha256')
        if not f: continue
        p=find(pkg,f,h)
        dst=P+'/sources/'+f; os.makedirs(os.path.dirname(dst),exist_ok=True)
        if p: shutil.copy(p,dst); report.append(('ok',st,f))
        else: report.append(('MISSING',st,f))
    if pkg=='aeg-d-dwarfs':
        keys=set()
        for s in S:
            if s['stratum']==st:
                pr=json.loads(Y[M[s['measurement_id']]['system_id']]['properties'] or '{}'); keys.add(pr.get('lvdb_key'))
        oc=list(csv.DictReader(open(d+'/reading/originals.csv')))
        sel=[r for r in oc if keys & set(r['systems'].split(';'))]
        cols=['lvdb_ref','bibcode','doi','title','roles','systems','arxiv_id','arxiv_version','pdf_url','bytes','sha256','access_note']
        with open(P+'/method/documents_index.csv','w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore'); w.writeheader(); w.writerows(sel)
        os.makedirs(P+'/sources/papers',exist_ok=True)
        for r in sel:
            if not r['pdf_url']: report.append(('NOPDF',st,r['lvdb_ref'])); continue
            dst=f"{P}/sources/papers/{r['lvdb_ref']}.pdf"
            if not os.path.exists(dst) or sha(dst)!=r['sha256']:
                try:
                    req=urllib.request.Request(r['pdf_url'],headers={'User-Agent':'aeg-audit (extragravitation.org)'})
                    open(dst,'wb').write(urllib.request.urlopen(req,timeout=60).read())
                except Exception as e: report.append(('DLFAIL',st,r['lvdb_ref'],str(e)[:60])); continue
            report.append(('ok' if sha(dst)==r['sha256'] else 'HASHDIFF',st,r['lvdb_ref']))
for r in report:
    if r[0]!='ok': print(*r)
print(sum(r[0]=='ok' for r in report),'ok of',len(report))
