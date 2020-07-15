


# --- In this example we look at the properties of one of the sources identified by segmentation.


import numpy as np
from astropy.io import fits

image_dir = '../data' # define image directory relative to this script

f = 'f125w' # filter

sci = fits.getdata(f'{image_dir}/{f}_sci.fits') # read science FITS file data into numpy array
wht = fits.getdata(f'{image_dir}/{f}_wht.fits') # read weight FITS file data into numpy array

mask = fits.getdata(f'{image_dir}/mask.fits') # read in the image mask
sci = np.ma.masked_array(sci, mask = mask) # apply the mask to our science image
wht = np.ma.masked_array(wht, mask = mask) # apply the mask to our weight image

# --- cut out a portion of the image for analysis

x = 2500 # pixel x-centre of cutout, must be an integer
y = 2500 # pixel y-centre of cutout, must be an integer
r = 100 # width/2 of cutout, must be int

sci = sci[x-r:x+r, y-r:y+r] # cutout a portion of the science image
wht = wht[x-r:x+r, y-r:y+r] # cutout a portion of the weight image

# --- define the noise in each pixel and make a significance map (signal/noise)

noise = 1./np.sqrt(wht) # conversion from weight to noise
sig = sci/noise # signifance map



# --- now run segmentation on the image.

from photutils import detect_sources
import matplotlib.pyplot as plt

threshold = 2.5 # require each pixel have a significance of >2.5 (since we're using the significance image)
npixels = 5 # require at least 5 connected pixels

segm = detect_sources(sig, threshold, npixels=npixels) # make segmentation image

i = 11

# --- lets again determine the total flux of that same source by simply summing the pixels on the orginal science image where the segmentation map = the index of our target galaxy:

signal = np.sum(sci[np.where(segm.data==i)])

print(f'the signal is: {signal}')

# --- the signal alone isn't very useful, we need an estimate of the uncertainty or error. The error is the sqrt(sum(noise_i**2))

error = np.sqrt(np.sum(noise[np.where(segm.data==i)]**2))

print(f'the error (noise) is: {error}')
print(f'the signal-to-noise is: {signal/error}')
