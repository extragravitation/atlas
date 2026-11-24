import sys, os, csv, hashlib, math
D = sys.argv[1]; OUT = sys.argv[2]
files = [("KiDS-bright","Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt","Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt"),
         ("GAMA","Fig-4-C1_RAR-GAMA-isolated_Nobins.txt","Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt"),
         ("KiDS-bright hot-gas variant","Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt","Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt")]
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
rows=[]; cov=[]
delta = math.log10(5e-12/1e-15)/15
edges=[10**(-15+k*delta) for k in range(16)]
report=[]
for samp,f,c in files:
    lines=[l for l in open(os.path.join(D,f)).read().splitlines() if l.strip() and not l.startswith('#')]
    assert len(lines)==15, (f,len(lines))
    for i,l in enumerate(lines):
        t=l.split(); assert len(t)==8
        rows.append(dict(sample=samp,file=f,row_index=i+1,g_bar=t[0],ESD_t=t[1],ESD_x=t[2],error=t[3],bias=t[4],
                         bin_lo=repr(edges[i]),bin_hi=repr(edges[i+1]),g_bar_in_bin=str(edges[i]<float(t[0])<edges[i+1])))
    cl=[l for l in open(os.path.join(D,c)).read().splitlines() if l.strip() and not l.startswith('#')]
    assert len(cl)==225,(c,len(cl))
    rad=[]
    for l in cl:
        t=l.split(); assert len(t)==7
        cov.append(dict(sample=samp,file=c,obs_min_m=t[0],obs_min_n=t[1],radius_i=t[2],radius_j=t[3],covariance=t[4],correlation=t[5],bias_product=t[6]))
        if t[2] not in rad: rad.append(t[2])
    # map radius to index, check diag vs error^2, symmetry
    idx={r:k+1 for k,r in enumerate(rad)}
    C={}
    for r in cov[-225:]:
        r['i']=idx[r['radius_i']]; r['j']=idx[r['radius_j']]; C[(r['i'],r['j'])]=float(r['covariance'])
    sym=max(abs(C[(a,b)]-C[(b,a)]) for a in range(1,16) for b in range(1,16))
    my=[r for r in rows if r['file']==f]
    dev=max(abs(math.sqrt(C[(k,k)])-float(my[k-1]['error']))/float(my[k-1]['error']) for k in range(1,16))
    radmatch=all(abs(float(rad[k])-float(my[k]['g_bar']))/float(my[k]['g_bar'])<6e-5 for k in range(15))
    bp=set(r['bias_product'] for r in cov[-225:])
    report.append(f"{samp}: radii distinct={len(rad)} radius==g_bar(5sf)={radmatch} max|C_ij-C_ji|={sym:.3e} max rel|sqrt(C_kk)-error|/error={dev:.2e} bias_product values={sorted(bp)} bias^2={float(my[0]['bias'])**2:.6e} all in bin={all(r['g_bar_in_bin']=='True' for r in my)}")
with open(os.path.join(OUT,'kids-second-reading.csv'),'w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(OUT,'kids-covariance.csv'),'w',newline='') as fh:
    k=['sample','file','i','j','obs_min_m','obs_min_n','radius_i','radius_j','covariance','correlation','bias_product']
    w=csv.DictWriter(fh,fieldnames=k); w.writeheader(); w.writerows(cov)
print("\n".join(report)); print(len(rows),len(cov))
print("delta",repr(delta)); 
for k in range(15): print(k+1, f"{edges[k]:.6e} {edges[k+1]:.6e}")
g=[float(r['radius_i']) for r in cov[:225:15]]
for k in range(15):
    a,b=edges[k],edges[k+1]
    print(k+1, repr(g[k]), "arith", (a+b)/2, "geo", math.sqrt(a*b), "loguniform-mean",(b-a)/math.log(b/a))
