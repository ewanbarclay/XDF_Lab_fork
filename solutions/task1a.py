



import numpy as np
from astropy.io import fits

image_dir = '../data' # define image directory relative to this script

f = 'f125w' # filter

sci = fits.getdata(f'{image_dir}/{f}_sci.fits') # read FITS file data into numpy array

mask = fits.getdata(f'{image_dir}/mask.fits') # read in the image mask

sci = np.ma.masked_array(sci, mask = mask) # apply the mask to our image

pix = sci.flatten() # flatten the masked image to produce a list of pixels

pix = pix[~pix.mask] # remove pixels that were masked


# --- plot a histogram of the pixel values

import matplotlib.pyplot as plt
from scipy.stats import norm

negpix = pix[pix<0.0] # isolate negative pixels

sigma = -np.percentile(negpix, 31.7) # measure \sigma as suggested in hint

pix = pix[np.fabs(pix/sigma)<10] # exclude pixels with magnitudes larger than \sigma


plt.hist(pix, bins = 1000, density = True) # plot a density histogram of the pixel values

# -- add a gausian/normal distribution with the same \sigma

x = np.linspace(-10*sigma, 10*sigma, 1000)
plt.plot(x, norm.pdf(x, 0, sigma))

plt.show()
