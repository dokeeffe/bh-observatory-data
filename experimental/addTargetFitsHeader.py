import logging
import os
from astropy import log as astropylog
from astropy.io import fits

def add_target_header_from_dir_name():
    '''
    This script is used to add the target name (from the directory name) to the fits header.
    This is temporary until Kstars/EKOS adds a feature to do this on capture
    Run this script in a dir containing dirs of fits files where the dirs are the target names.
    :return:
    '''

    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir):
            target_name = dir
            print('processing files in target dir {}'.format(target_name))
            for subdir, dirs, files in os.walk(dir):
                for file in files:
                    if file.endswith('fits'):
                        hdulist = fits.open(os.path.join(subdir,file))
                        header = hdulist[0].header
                        header['TARGET'] = target_name
                        fits.writeto(os.path.join(subdir,file), overwrite=True)
                        print('Updated TARGET header to {} for {} in {}'.format(target_name, file, subdir))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    astropylog.setLevel('WARNING')
    add_target_header_from_dir_name()
