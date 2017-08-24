#!/usr/bin/python
import logging
from astropy.io import fits
import os
import fnmatch

def add_fits_object_to_filename():
    for root, dirnames, filenames in os.walk('/home/dokeeffe/Pictures/CalibratedLight'):
        for filename in fnmatch.filter(filenames, '*.fits'):
            hdu = fits.open(os.path.join(root, filename))
            if 'OBJECT' in hdu[0].header:
                obj_name = hdu[0].header['OBJECT'].replace(' ', '_')
                if not filename.startswith(obj_name):
                    os.rename(os.path.join(root, filename),os.path.join(root, '{}-{}'.format(obj_name,filename)))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    add_fits_object_to_filename()

