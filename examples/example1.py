


# --- In this example you can see how to read an image, apply a mask, and work with an array of pixel values.

import numpy as np
from astropy.io import fits

image_dir = '../data' # define image directory relative to this script

f = 'f125w' # filter

sci = fits.getdata(f'{image_dir}/{f}_sci.fits') # read FITS file data into numpy array

print(f'dimensions of image: {sci.shape}') # print the shape (dimensions) of the image
print(f'total number of pixels (from image): {sci.size}') # total number of real data pixels

mask = fits.getdata(f'{image_dir}/mask.fits') # read in the image mask

sci = np.ma.masked_array(sci, mask = mask) # apply the mask to our image

pix = sci.flatten() # flatten the masked image to produce a list of pixels

print(f'total number of pixels (from masked image): {sci.size}') # total number of real data pixels
print(f'total number of pixels (from masked flattened image): {pix.size}') # total number of real data pixels

pix = pix[~pix.mask] # remove pixels that were masked

print(f'total number of pixels (from masked flattened image with masked pixels removed): {pix.size}') # total number of real data pixels

print(f'minimum: {np.min(pix)}') # print the minimum value
print(f'16th percentile: {np.percentile(pix, 16)}') # print the 16th percentile
print(f'median: {np.median(pix)}') # print the median
print(f'84th percentile: {np.percentile(pix, 84)}') # print the 84th percentile
print(f'maximum: {np.max(pix)}') # print the maximum
