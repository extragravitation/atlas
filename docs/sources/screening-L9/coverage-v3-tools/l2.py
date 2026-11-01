import sys,re
L=open(sys.argv[1]).read().split('\n')
seen={}
for i,l in enumerate(L[372:538],start=373):
    m=re.match(r'^(\S+)\s+(.*?)\s+(\d{6}\.\d[+-]\d{6})\s',l)
    if m:
        seen.setdefault(m.group(1),[]).append((m.group(2).strip(),m.group(3)))
    elif l.strip() and re.match(r'^[A-Z]',l): print('UNPARSED',i,l[:40])
for k,v in seen.items(): print(k,'|',';'.join(sorted(set(s for s,_ in v))),'|',sorted(set(c for _,c in v)))
print('N',len(seen))
