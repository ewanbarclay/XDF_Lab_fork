

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

from photutils import source_properties, CircularAperture, aperture_photometry

cat = source_properties(detection_sci, segm)

# --- get a list of positions (x,y) of the sources

positions = []
for obj in cat:
    positions.append(np.transpose((obj.xcentroid.value, obj.ycentroid.value)))

# --- make a CicrcularAperture object. This can be plotted but is mostly used for the aperture photometry.

aper_r = 5. # radius of aperture in pixels
apertures = CircularAperture(positions, aper_r)


# --- now open all the individual filters

image_dir = '../data'

filters = ['f435w','f606w', 'f775w','f850lp', 'f105w','f125w','f140w','f160w']

aper_cat = {}

for f in filters:

    # --- read in the science image and slice for our region
    sci = fits.getdata(f'{image_dir}/{f}_sci.fits')[x-r:x+r, y-r:y+r]
    # --- run aperture photometry to get photometry table
    phot_table = aperture_photometry(sci, apertures)
    # --- convert aperture flux column to an array and place in output dictionary
    aper_cat[f+'_signal'] = np.array(phot_table['aperture_sum'])

    # --- read in the weight image and slice for our region
    wht = fits.getdata(f'{image_dir}/{f}_wht.fits')[x-r:x+r, y-r:y+r]
    # --- define the noise image
    noise = 1/np.sqrt(wht)
    # --- square this ready for summing
    noisesq = noise**2
    # --- run aperture photometry to get photometry table
    phot_table = aperture_photometry(noisesq, apertures)
    # --- convert aperture flux column to an array and place in output dictionary
    aper_cat[f+'_noise'] = np.sqrt(np.array(phot_table['aperture_sum']))

    print(phot_table)


pickle.dump(aper_cat, open('data/aper_cat.p','wb'))
