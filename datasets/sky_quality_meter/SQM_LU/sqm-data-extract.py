#!/usr/bin/env python3

import fnmatch
import pandas as pd
import os
from astropy.io import fits

# for root, dirnames, filenames in os.walk('/home/dokeeffe/Pictures/CalibratedLight'):
data = []
for root, dirnames, filenames in os.walk('/home/dokeeffe/Pictures/CalibratedLight'):
    for filename in fnmatch.filter(filenames, '*.fits'):
        try:
            hdulist = fits.open(os.path.join(root, filename))
            header = hdulist[0].header
            if 'MPSAS' in header:
                sqm = header['MPSAS']
                date_obs = header['DATE-OBS']
                data.append([date_obs,sqm])
        except:
            print(f'Could not open {filename}')

df = pd.DataFrame(data, columns=['datetime_obs', 'mpsas'])
df = df.set_index('datetime_obs')
df.sort_index(inplace=True)
df.to_csv('sqm.csv')

