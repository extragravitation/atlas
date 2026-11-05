import sys
from astropy.io import fits
for p in sys.argv[1:]:
    with fits.open(p) as h:
        print("=====",p); h.info()
        for e in h[1:]:
            print("--",e.name); print(repr(e.header))
            print(e.data[:3])
