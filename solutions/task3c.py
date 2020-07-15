

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


# --- loop through candidates and show cutouts of the detection image

ids = [83] # list of IDs of candidates

for id in ids:

    slices = segm.slices[id-1]

    plt.imshow(sci[slices], cmap = 'bone') # apply slice to science image
    plt.show()
