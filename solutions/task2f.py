

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import pickle

detection_sci = np.load('data/detection_sci.npy') # read detection sci image
detection_wht = np.load('data/detection_wht.npy') # read detection wht image

# --- cut out a portion of the image for analysis

x = 3100 # x-center of the image
y = 1800 # y-center of the image
r = 200 # width/2 of cutout, must be int

detection_sci = detection_sci[x-r:x+r, y-r:y+r] # cutout a portion of the science image
detection_wht = detection_wht[x-r:x+r, y-r:y+r] # cutout a portion of the weight image

# --- define the noise in each pixel and make a significance map (signal/noise)

detection_noise = 1./np.sqrt(detection_wht) # conversion from weight to noise
detection_sig = detection_sci/detection_noise # signifance map


# --- now run segmentation on the image

from photutils import detect_sources

threshold = 2.5
npixels = 5

segm = detect_sources(detection_sig, threshold, npixels)



# --- now open all the individual filters

image_dir = '../data'

filters = ['f435w','f606w', 'f775w','f850lp', 'f105w','f125w','f140w','f160w']

cat = {}

for f in filters:


    # get the signal
    sci = fits.getdata(f'{image_dir}/{f}_sci.fits')[x-r:x+r, y-r:y+r]
    cat[f+'_signal'] = np.array([np.sum(sci[np.where(segm.data == i+1)]) for i in range(segm.nlabels)])

    # get the noise
    wht = fits.getdata(f'{image_dir}/{f}_wht.fits')[x-r:x+r, y-r:y+r]
    noise = 1/np.sqrt(wht)
    cat[f+'_noise'] = np.array([np.sqrt(np.sum(noise[np.where(segm.data == i+1)]**2)) for i in range(segm.nlabels)])


pickle.dump(cat, open('data/cat.p','wb'))
