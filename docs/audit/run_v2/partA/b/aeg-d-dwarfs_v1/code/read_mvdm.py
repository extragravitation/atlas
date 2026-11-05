import sys, collections
from astropy.io.votable import parse_single_table
t = parse_single_table(sys.argv[1]).to_table()
mw=[r for r in t if str(r['Cluster']).startswith('MW')]
print(len(mw), collections.Counter(round(float(r['logAge']),2) for r in mw))
rows=sorted(((float(r['__Fe_H_']),float(r['__M_L_1']),str(r['Cluster']),int(r['recno'])) for r in mw))
for x in rows: print(x)
