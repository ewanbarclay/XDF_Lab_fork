

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

sci = np.load('data/detection_sci.npy') # read detection sci image
wht = np.load('data/detection_wht.npy') # read detection wht image


# --- cut out a portion of the image for analysis

x = 3100 # x-center of the image
y = 1800 # y-center of the image
r = 200 # width/2 of cutout, must be int

sci = sci[x-r:x+r, y-r:y+r] # cutout a portion of the science image
wht = wht[x-r:x+r, y-r:y+r] # cutout a portion of the weight image

# --- define the noise in each pixel and make a significance map (signal/noise)

noise = 1./np.sqrt(wht) # conversion from weight to noise
sig = sci/noise # signifance map


# --- now run segmentation on the image

from photutils import detect_sources

threshold = 2.5
npixels = 5

segm = detect_sources(sig, threshold, npixels)


# --- now measure the flux in every source

# fluxes = np.zeros(segm.nlabels)
# for i in range(segm.nlabels):
#     masked_sci = np.ma.masked_where(segm.data != i+1, sci)
#     flux = np.sum(masked_sci)
#     fluxes[i] = flux

fluxes = np.array([np.sum(sci[np.where(segm.data == i+1)]) for i in range(segm.nlabels)])


from photutils import deblend_sources

segm_deblend = deblend_sources(sig, segm, npixels=npixels, nlevels=32, contrast=0.001)

fluxes_deblended = np.array([np.sum(sci[np.where(segm_deblend.data == i+1)]) for i in range(segm_deblend.nlabels)])

plt.hist(np.log10(fluxes), bins=10, alpha = 0.5, label = 'simple')
plt.hist(np.log10(fluxes_deblended), bins=10, alpha = 0.5, label = 'deblended')
plt.legend()
plt.show()
