

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

sci = np.load('data/detection_sci.npy') # read detection sci image
wht = np.load('data/detection_wht.npy') # read detection wht image


# --- cut out a portion of the image for analysis

x = sci.shape[0] // 2 # x-center of the image
y = sci.shape[1] // 2 # y-center of the image
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

plt.imshow(segm) # plot all pixels and scale between significance = -threshold to threshold
plt.show()

from photutils import deblend_sources

segm_deblend = deblend_sources(sig, segm, npixels=5, nlevels=32, contrast=0.001)

plt.imshow(segm_deblend) # plot all pixels and scale between significance = -threshold to threshold
plt.show()


# --- now expore various choices of parameters


npixels_ = np.arange(1,10,1)
threshold_ = np.arange(0.5,8.,0.5)

N = np.zeros((npixels_.size, threshold_.size))
print(N.shape)

for i, npixels in enumerate(npixels_):
    for j, threshold in enumerate(threshold_):

        segm = detect_sources(sig, threshold, npixels)
        n = np.max(segm.data)
        N[i,j] = n


plt.imshow(N.T, extent = (npixels_[0]-(npixels_[1]-npixels_[0])/2.,npixels_[-1]+(npixels_[1]-npixels_[0])/2.,threshold_[0]-(threshold_[1]-threshold_[0])/2.,threshold_[-1]+(threshold_[1]-threshold_[0])/2.), origin='lower', vmin = 0)
plt.xlabel('N_pixels')
plt.ylabel('threshold')
plt.show()
