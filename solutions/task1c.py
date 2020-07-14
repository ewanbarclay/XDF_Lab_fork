

import numpy as np
from astropy.io import fits
from matplotlib import cm
import matplotlib.pyplot as plt


image_dir = '../data/original' # image directory relative to this script

mask = fits.getdata(f'{image_dir}/mask.fits') # read in the image mask

# --- define the filters to be combined for each channel

filters = {}
filters['B'] = ['f435w','f606w']
filters['G'] = ['f775w','f850lp']
filters['R'] = ['f105w','f125w','f140w','f160w']

# --- combine the filters in each channel

im = {} # dictionary to hold the combined images

for channel in 'RGB':

    fs = filters[channel]

    sci = {f: fits.getdata(f'{image_dir}/{f}_sci.fits') for f in fs} # read sci images
    wht = {f: fits.getdata(f'{image_dir}/{f}_wht.fits') for f in fs} # read weight images

    shape = next(iter(sci.values())).shape
    combined_sci = np.zeros(shape)
    combined_wht = np.zeros(shape)

    for f in fs:
        combined_sci += sci[f] * wht[f]
        combined_wht += wht[f]

    combined_sci /= combined_wht

    # --- apply the mask to our image
    combined_sci = np.ma.masked_array(combined_sci, mask = mask)

    # --- clip negative and erroneously high values and rescale values to be 0 - 1
    # --- NOTE: you can play around here to change the colour balance and contrast of your images
    vmin = 0 # exclude negative values (anything less than vmin gets mapped to vmin)
    vmax =  np.percentile(combined_sci[~np.isnan(combined_sci)], 99) # exclude the brightest 1% of pixels (anything above gets mapped to that value)

    norm = cm.colors.Normalize(vmin, vmax) # normalisation function
    combined_sci = norm(combined_sci) # apply normalisation function

    # --- set masked values to zero
    im[channel] = np.ma.filled(combined_sci, 0.0) # return masked array with masked values set to 0.0 (this makes those pixels black)

rgb = np.dstack((im['R'],im['G'],im['B'])) # stack images into a single array




# --- make image and show

dpi = rgb.shape[0] # set dots per inch equal to the number of pixels.
fig = plt.figure(figsize = (1, 1), dpi = dpi)
ax = fig.add_axes((0.0, 0.0, 1.0, 1.0)) # define axes to cover entire field
ax.axis('off') # turn off axes frame, ticks, and labels

ax.imshow(rgb) # shouldn't see much because the scale is dominated by outlier pixels
fig.savefig('XDF_rgb.png')
