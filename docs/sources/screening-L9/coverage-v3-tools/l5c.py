import sys,re
L=open(sys.argv[1]).read().split('\n')
out=[]
for l in L[1079:]:
    m=re.match(r'^\s*(a\d{4}[a-z]?)\s+\d+\s+(0\.\d{4})\b',l)
    if m: out.append((m.group(1),m.group(2)))
print(len(out),len(set(n for n,_ in out)))
print(' '.join(f'{n}:{z}' for n,z in out))
