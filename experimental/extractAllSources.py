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

# search_ra = 18.53
# search_dec = 33.2
search_ra = 16.6
search_dec = 36.3
search_radius = 1.5

frames = []

for root, dirnames, filenames in os.walk('/media/dokeeffe/My Passport Ultra/CalibratedLight/'):
    for filename in fnmatch.filter(filenames, '*.fits'):
        hdulist = fits.open(os.path.join(root, filename))
        header = hdulist[0].header
        ra = header['OBJCTRA']
        dec = header['OBJCTDEC']
        date_obs = datetime.datetime.strptime(header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S')
        filter = header['FILTER']
        if ra > search_ra - search_radius and ra < search_ra + search_radius and dec > search_dec - search_radius and dec < search_dec + search_radius:
            # Parse the WCS keywords in the primary HDU
            w = wcs.WCS(hdulist[0].header)
            # Print out the "name" of the WCS, as defined in the FITS header
            print w.wcs.name
            # Print out all of the settings that were parsed from the header
            # w.wcs.print_contents()
	        # print os.path.join(root, filename)
            data = hdulist[0].data
            # data = hdulist[0].data[550:750,700:900]
            mean, median, std = sigma_clipped_stats(data, sigma=3.0, iters=5)
            daofind = DAOStarFinder(fwhm=4.5, threshold=5. * std)
            sources = daofind(data - median)
            positions = (sources['xcentroid'], sources['ycentroid'])
            apertures = CircularAperture(positions, r=4.)
            phot_table = aperture_photometry(data, apertures)
            xys = (phot_table['xcenter'], phot_table['ycenter'])
            wx, wy = w.wcs_pix2world(xys, 0)


            df = phot_table.to_pandas()
            df['date'] = date_obs
            df['filter'] = filter

            # ascii.write(phot_table, 'values.csv', format='csv', fast_writer=False)
            frames.append(df)
            # print df
            # plt.imshow(data, cmap='gray_r', origin='lower')
            # apertures.plot(color='blue', lw=1.5, alpha=0.5)
            # plt.show()
            #
            # print sources

result = pd.concat(frames)
result.to_csv('df.csv')
