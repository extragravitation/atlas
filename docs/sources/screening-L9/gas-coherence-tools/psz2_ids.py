"""Read only identifier columns (NAME, RA, DEC, GLON, GLAT, REDSHIFT, REDSHIFT_ID) from the Planck PSZ2 union catalogue.
python3 -I psz2_ids.py HFI_PCCS_SZ-union_R2.08.fits.gz out.csv"""
import sys
from astropy.io import fits
with fits.open(sys.argv[1]) as h:
    d = h[1].data
    cols = ['NAME', 'RA', 'DEC', 'REDSHIFT', 'REDSHIFT_ID']
    print([c for c in d.columns.names if c in cols or c.startswith('REDSHIFT')])
    with open(sys.argv[2], 'w') as f:
        f.write('name,ra,dec,z,redshift_id\n')
        for r in d:
            f.write(','.join([str(r['NAME']).strip(), '%.4f' % r['RA'], '%.4f' % r['DEC'], '%.4f' % r['REDSHIFT'], '"' + str(r['REDSHIFT_ID']).strip() + '"']) + '\n')
