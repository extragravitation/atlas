import sys, numpy as np
from astropy.io import fits
cl=['A85','A644','A1644','A1795','A2029','A2142','A2255','A2319','A3158','A3266','RXC1825','ZW1215']
mod={'A1644','A2255','A3158','A3266','RXC1825'}
cum=0; cumc=0
for c in cl:
    h=fits.open(f'{c}/{c}_hydro_mass.fits'); r=np.array(h[1].data['RADIUS'],float)
    g=fits.open(f'{c}/{c}_fgas_profile.fits')['FGAS']; R500=g.header['R500']; rg=np.array(g.data['RADIUS'],float)*R500
    lo,hi=rg.min(),rg.max()
    try:
        s=fits.open(f'{c}/{c}_mstar.fits')['MSTAR_SMOOTHED']; rs=np.array(s.data['RADIUS'],float); lo=max(lo,rs.min()); hi=min(hi,rs.max())
    except FileNotFoundError: pass
    ok=np.where((r>=lo)&(r<=hi))[0]
    okc=ok
    if c in mod:
        x=r/R500; okc=np.array([i for i in ok if 0.145<=x[i]<=1.38])
    print(c,R500,h[1].header['R500'],len(ok),ok.min(),ok.max(),'start',cum,'| cut',len(okc),okc.min(),okc.max(),'startc',cumc)
    cum+=len(ok); cumc+=len(okc)
print(cum,cumc)
