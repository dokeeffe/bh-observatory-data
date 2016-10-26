import fnmatch
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
from multiprocessing import Process, Queue

m13_ra = 16.6
m13_dec = 36.3


def find_fits_near(search_ra, search_dec, search_radius=1.5):
    fits_files_to_process = []
    for root, dirnames, filenames in os.walk('/media/dokeeffe/My Passport Ultra/CalibratedLight/'):
        for filename in fnmatch.filter(filenames, '*.fits'):
            hdulist = fits.open(os.path.join(root, filename))
            header = hdulist[0].header
            ra = header['OBJCTRA']
            dec = header['OBJCTDEC']
            if ra > search_ra - search_radius and ra < search_ra + search_radius and dec > search_dec - search_radius and dec < search_dec + search_radius:
                fits_files_to_process.append(os.path.join(root, filename))
    return fits_files_to_process


def process_files(q, files_to_process, csv_target):
    frames = []
    for file in files_to_process:
        hdulist = fits.open(file)
        header = hdulist[0].header
        date_obs = datetime.datetime.strptime(header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S')
        filter = header['FILTER']
        # Parse the WCS keywords in the primary HDU
        w = wcs.WCS(hdulist[0].header)
        data = hdulist[0].data
        # data = hdulist[0].data[550:750,700:900]
        mean, median, std = sigma_clipped_stats(data, sigma=3.0, iters=5)
        daofind = DAOStarFinder(fwhm=4.5, threshold=5. * std)
        sources = daofind(data - median)
        positions = (sources['xcentroid'], sources['ycentroid'])
        apertures = CircularAperture(positions, r=4.)
        phot_table = aperture_photometry(data, apertures)

        df = phot_table.to_pandas()
        df['fitsfile'] = file
        df['date'] = date_obs
        df['filter'] = filter
        df['ra'], df['dec'] = w.wcs_pix2world(df['xcenter'], df['ycenter'], 0)

        # ascii.write(phot_table, 'values.csv', format='csv', fast_writer=False)
        frames.append(df)
        # plt.imshow(data, cmap='gray_r', origin='lower')
        # apertures.plot(color='blue', lw=1.5, alpha=0.5)
        # plt.show()
    result = pd.concat(frames)
    q.put(result)
    # result.to_csv(csv_target)
    # print 'saved chunk {}',csv_target


def split_list(a_list):
    half = len(a_list) / 2
    return a_list[:half], a_list[half:]


if __name__ == '__main__':
    files_to_process = find_fits_near(m13_ra, m13_dec)

    # Split the work into 4 chunks and process in parallel.
    chunk_a, chunk_b = split_list(files_to_process)
    chunk_1, chunk_2 = split_list(chunk_a)
    chunk_3, chunk_4 = split_list(chunk_b)

    q = Queue()
    p1 = Process(target=process_files, args=(q,chunk_1, 'output1.csv'))
    p2 = Process(target=process_files, args=(q,chunk_2, 'output2.csv'))
    p3 = Process(target=process_files, args=(q,chunk_3, 'output3.csv'))
    p4 = Process(target=process_files, args=(q,chunk_4, 'output4.csv'))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    results = []
    results.append(q.get())
    results.append(q.get())
    results.append(q.get())
    results.append(q.get())
    result = pd.concat(results)
    result.to_csv('output.csv')
