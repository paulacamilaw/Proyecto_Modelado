from __future__ import print_function
import os
from astropy.io import ascii

def ascii2hdf5(inputfile, outputfile, clobber=False, overwrite=True,
               verbose=False):
    """Convert a file to hdf5 using compression and path set to data"""
    if verbose:
        print('converting {} to {}'.format(inputfile, outputfile))
    
    tbl = ascii.read(inputfile)
    try:
        tbl.write(outputfile, format='hdf5', path='data', compression=True,
                  overwrite=overwrite)
    except:
        print('problem with {}'.format(inputfile))
        return

    if clobber:
        os.remove(inputfile)
        if verbose:
            print('removed {}'.format(inputfile))

    return

ascii2hdf5('DataSzbloque0400.tzl', 'var1')
