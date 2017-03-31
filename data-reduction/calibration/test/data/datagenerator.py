import numpy as np
from ccdproc import CCDData


def setup_bias_data():
    ccd = CCDData(np.arange(10), unit="adu")
    metadata = {'XBINNING': 1, 'FRAME': 'bias', 'CCD-TEMP': -20}
    ccd.header = metadata
    ccd.write('bias-20x1.fits')

    ccd = CCDData(np.arange(10), unit="adu")
    metadata = {'XBINNING': 2, 'FRAME': 'bias', 'CCD-TEMP': -20}
    ccd.header = metadata
    ccd.write('bias-20x2.fits')

    ccd = CCDData(np.arange(10), unit="adu")
    metadata = {'XBINNING': 1, 'FRAME': 'bias', 'CCD-TEMP': -25}
    ccd.header = metadata
    ccd.write('bias-25x1.fits')

    ccd = CCDData(np.arange(10), unit="adu")
    metadata = {'XBINNING': 2, 'FRAME': 'bias', 'CCD-TEMP': -25}
    ccd.header = metadata
    ccd.write('bias-25x2.fits')

def setup_dark_data():
    ccd = CCDData(np.arange(10), unit="adu")
    metadata = {'XBINNING': 1, 'FRAME': 'Dark', 'CCD-TEMP': -20, 'EXPTIME': 120}
    ccd.header = metadata
    ccd.write('dark-20x1_120.fits')

    ccd = CCDData(np.arange(10), unit="adu")
    metadata = {'XBINNING': 2, 'FRAME': 'Dark', 'CCD-TEMP': -20, 'EXPTIME': 120}
    ccd.header = metadata
    ccd.write('dark-20x2_120.fits')

    ccd = CCDData(np.arange(10), unit="adu")
    metadata = {'XBINNING': 1, 'FRAME': 'Dark', 'CCD-TEMP': -25, 'EXPTIME': 180}
    ccd.header = metadata
    ccd.write('dark-25x1_180.fits')

    ccd = CCDData(np.arange(10), unit="adu")
    metadata = {'XBINNING': 2, 'FRAME': 'Dark', 'CCD-TEMP': -25, 'EXPTIME': 180}
    ccd.header = metadata
    ccd.write('dark-25x2_180.fits')


setup_dark_data()
