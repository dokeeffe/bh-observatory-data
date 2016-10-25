import fnmatch
import glob
import os
import datetime
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils import DAOStarFinder
from photutils import aperture_photometry, CircularAperture
import matplotlib.pyplot as plt
from astropy.io import ascii
from astropy import wcs
import pandas as pd
import numpy as np


def load_all(pattern):
    allFiles = glob.glob(pattern)
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0)
        list_.append(df)
    frame = pd.concat(list_)
    return frame

if __name__ == '__main__':
    frame = load_all('*.csv')
    print frame


