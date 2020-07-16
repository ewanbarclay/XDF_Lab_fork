


# --- In this example you can see how to obtain a cutout of an image and produce a .png of the cutout.


import numpy as np
from astropy.io import fits

image_dir = '../data' # define image directory relative to this script

f = 'f125w' # filter

sci = fits.getdata(f'{image_dir}/{f}_sci.fits') # read FITS file data into numpy array
mask = fits.getdata(f'{image_dir}/mask.fits') # read in the image mask
sci = np.ma.masked_array(sci, mask = mask) # apply the mask to our image

# --- calculate the standard deviation of the noise. This is necessary to properly scale the image.

pix = sci.flatten() # flatten the masked image to produce a list of pixels
pix = pix[~pix.mask] # remove pixels that were masked
negpix = pix[pix<0.0] # isolate negative pixels
sigma = -np.percentile(negpix, 31.7) # measure \sigma as demonstrated in example1.py.

# --- cut out a portion of the image for analysis

x = 2500 # pixel x-centre of cutout, must be an integer
y = 2500 # pixel y-centre of cutout, must be an integer
r = 100 # width/2 of cutout, must be int

cutout = sci[x-r:x+r, y-r:y+r] # cutout a portion of the image

# --- plot the cutout, choosing sensible scale (set by vmin and vmax)

import matplotlib.pyplot as plt

plt.imshow(cutout, vmin = 0, vmax = 10*sigma, cmap = 'bone')
plt.show()


# --- this does the same as above

slices = [slice(x-r,x+r,None),slice(y-r,y+r,None)]

plt.imshow(sci[slices], vmin = 0, vmax = 10*sigma, cmap = 'bone')
plt.show()
